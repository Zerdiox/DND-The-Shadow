# -*- coding: utf-8 -*-
"""
vault.py — query and lint the frontmatter of this Obsidian vault.

Run from anywhere; it locates the vault relative to this file.

    python .claude/tools/vault.py <command> [options]

Commands
    ls        list notes, filtered, as a table
    get       print one note's frontmatter and section names
    fields    every frontmatter key in use, with counts per type
    links     broken [[wikilinks]] and notes nothing links to
    lint      schema and consistency problems
    grep      search note bodies
    stats     counts per folder
    set       change one frontmatter value on one note

Examples
    vault.py ls --type item --where identified=false
    vault.py ls --type item --fields name,owner,value --where magical=true
    vault.py ls --where 'owner~Echo'
    vault.py get "Crown of Fear"
    vault.py fields --type item
    vault.py links
    vault.py lint
    vault.py grep "prismatic"
    vault.py set "Prismatic Keys" magical true --dry-run

Filters for --where (repeatable, all must match)
    key=value     equals (case-insensitive)
    key!=value    not equals
    key~text      contains
    key=          empty or missing
    key?          present and non-empty
"""

import argparse
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = os.path.abspath(os.path.join(HERE, "..", ".."))

SKIP_DIRS = (".stversions", ".trash", ".obsidian", ".smart-env", ".stfolder",
             ".claude", "gemini-scribe")
ARCHIVE_DIRS = ("99-Processed", "00-Inbox")

# markdown at the vault root that is tooling, not a campaign note
NOT_NOTES = ("CLAUDE.md", "README.md")

FOLDER_TYPE = {
    "01-Sessions": "session",
    "02-NPCs": "npc",
    "03-Locations": "location",
    "04-Quests-Plot": "quest",
    "05-Items-Loot": "item",
    "06-Lore-Factions": "lore",
}

# what each type is expected to carry
EXPECTED = {
    "npc": ["type", "status", "pronouns", "location", "faction", "first_appeared", "tags"],
    "location": ["type", "region", "first_visited", "tags"],
    "quest": ["type", "status", "related_npcs", "related_locations", "started", "tags"],
    "item": ["type", "item_type", "rarity", "attunement", "magical", "quantity",
             "weight", "value", "owner", "found", "identified", "tags"],
    "session": ["type", "date", "tags"],
    "lore": ["type", "tags"],
}

WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")


# --------------------------------------------------------------------- model

class Note(object):
    def __init__(self, path):
        self.path = path
        self.rel = os.path.relpath(path, VAULT).replace("\\", "/")
        parts = self.rel.split("/")
        self.folder = parts[0] if len(parts) > 1 else "(root)"
        self.name = os.path.splitext(os.path.basename(path))[0]
        self.raw = io.open(path, encoding="utf-8").read()
        self.fm, self.fm_raw, self.body = _split(self.raw)
        self.type = self.fm.get("type") or FOLDER_TYPE.get(self.folder, "")

    def sections(self):
        out = {}
        cur = None
        for line in self.body.splitlines():
            m = re.match(r"^##\s+(.*)$", line)
            if m:
                cur = m.group(1).strip()
                out[cur] = []
            elif cur:
                out[cur].append(line)
        return dict((k, "\n".join(v).strip()) for k, v in out.items())

    def links(self):
        return [m.split("/")[-1][:-3] if m.endswith(".md") else m
                for m in WIKILINK.findall(self.raw)]

    def get(self, key):
        v = self.fm.get(key)
        if isinstance(v, list):
            return ", ".join(v)
        return v or ""


def _split(text):
    """Return (frontmatter dict, frontmatter raw text, body)."""
    if not text.startswith("---"):
        return {}, "", text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, "", text
    block = text[text.find("\n") + 1:end]
    body = text[end + 4:].lstrip("\n")
    fm = {}
    key = None
    for line in block.splitlines():
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z0-9_\-]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val.startswith("[") and val.endswith("]") and not val.startswith("[["):
                fm[key] = [p.strip() for p in val[1:-1].split(",") if p.strip()]
            else:
                fm[key] = val
        elif line.lstrip().startswith("-") and key:
            val = line.lstrip()[1:].strip()
            if not isinstance(fm.get(key), list):
                fm[key] = [] if not fm.get(key) else [fm[key]]
            fm[key].append(val)
    return fm, block, body


def load(include_archive=False):
    notes = []
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        rel_root = os.path.relpath(root, VAULT).replace("\\", "/").split("/")[0]
        if not include_archive and rel_root in ARCHIVE_DIRS:
            continue
        for f in files:
            if f.endswith(".md") and not (rel_root == "." and f in NOT_NOTES):
                notes.append(Note(os.path.join(root, f)))
    return sorted(notes, key=lambda n: (n.folder, n.name))


# -------------------------------------------------------------------- output

def table(rows, headers, label="note"):
    if not rows:
        print("(none)")
        return
    widths = [len(h) for h in headers]
    for r in rows:
        for i, c in enumerate(r):
            widths[i] = max(widths[i], len(str(c)))
    line = "  ".join(h.upper().ljust(widths[i]) for i, h in enumerate(headers))
    print(line.rstrip())
    print("  ".join("-" * widths[i] for i in range(len(headers))))
    for r in rows:
        print("  ".join(str(c).ljust(widths[i]) for i, c in enumerate(r)).rstrip())
    print("\n%d %s%s" % (len(rows), label, "" if len(rows) == 1 else "s"))


def match(note, wheres):
    for w in wheres:
        if w.endswith("?"):
            if not note.get(w[:-1]).strip():
                return False
        elif "!=" in w:
            k, v = w.split("!=", 1)
            if note.get(k).lower() == v.strip().lower():
                return False
        elif "~" in w:
            k, v = w.split("~", 1)
            if v.strip().lower() not in note.get(k).lower():
                return False
        elif "=" in w:
            k, v = w.split("=", 1)
            v = v.strip()
            if v == "":
                if note.get(k).strip():
                    return False
            elif note.get(k).lower() != v.lower():
                return False
        else:
            if k not in note.fm:
                return False
    return True


# ------------------------------------------------------------------ commands

def cmd_ls(a):
    notes = [n for n in load(a.archive)
             if (not a.type or n.type == a.type) and match(n, a.where)]
    fields = [f.strip() for f in a.fields.split(",")] if a.fields else None
    if not fields:
        default = {"item": ["name", "identified", "magical", "owner", "value"],
                   "npc": ["name", "status", "location"],
                   "location": ["name", "region", "first_visited"],
                   "quest": ["name", "status"],
                   "session": ["name", "date", "title"],
                   "lore": ["name", "tags"]}
        fields = default.get(a.type, ["name", "type", "tags"])
    rows = [[n.name if f == "name" else (n.type if f == "type" else n.get(f))
             for f in fields] for n in notes]
    table(rows, fields)


def cmd_get(a):
    hits = [n for n in load(True) if n.name.lower() == a.name.lower()]
    if not hits:
        hits = [n for n in load(True) if a.name.lower() in n.name.lower()]
    if not hits:
        print("no note matching %r" % a.name)
        return 1
    for n in hits:
        print("=" * 60)
        print(n.rel)
        print("=" * 60)
        for k, v in n.fm.items():
            print("  %-16s %s" % (k + ":", ", ".join(v) if isinstance(v, list) else v))
        secs = n.sections()
        print("  --")
        for name, text in secs.items():
            first = text.splitlines()[0] if text.strip() else "(empty)"
            print("  ## %-18s %s" % (name, first[:70]))
        if a.full:
            print("\n" + n.body)
    return 0


def cmd_fields(a):
    notes = [n for n in load(a.archive) if not a.type or n.type == a.type]
    keys, order = {}, []
    for n in notes:
        for k in n.fm:
            if k not in keys:
                keys[k] = {"count": 0, "empty": 0, "types": set()}
                order.append(k)
            keys[k]["count"] += 1
            keys[k]["types"].add(n.type or "?")
            if not n.get(k).strip():
                keys[k]["empty"] += 1
    rows = [[k, keys[k]["count"], keys[k]["empty"], ",".join(sorted(keys[k]["types"]))]
            for k in order]
    table(rows, ["key", "used", "empty", "on types"])


def cmd_links(a):
    notes = load(False)
    names = set(n.name for n in load(True))   # archived raw notes are valid targets
    broken, inbound = [], dict((n.name, 0) for n in notes)
    for n in notes:
        for t in n.links():
            t = t.strip()
            if t in names:
                inbound[t] = inbound.get(t, 0) + 1
            else:
                broken.append([n.rel, "[[%s]]" % t])
    print("BROKEN LINKS")
    table([list(x) for x in sorted(set(map(tuple, broken)))],
          ["in note", "target"], "broken link")
    orphans = [[n.name, n.folder] for n in notes
               if inbound[n.name] == 0 and n.type != "session"]
    print("\nNOTHING LINKS TO THESE")
    table(orphans, ["note", "folder"], "orphan")


def cmd_lint(a):
    notes = load(False)
    names = set(n.name for n in load(True))   # archived raw notes are valid targets
    problems = []

    def flag(note, what):
        problems.append([note.rel, what])

    for n in notes:
        exp = EXPECTED.get(n.type)
        if exp:
            for k in exp:
                if k not in n.fm:
                    flag(n, "missing key: %s" % k)
            for k in n.fm:
                if k not in exp and k not in ("title", "aliases", "ddb", "ddb_name", "ddb_add"):
                    flag(n, "unexpected key: %s" % k)
        if not n.fm:
            flag(n, "no frontmatter")
        if re.search(r"(?m)^\s+-\s+-\s", n.fm_raw):
            flag(n, "malformed list in frontmatter ('- - value')")
        for k, v in n.fm.items():
            if isinstance(v, str) and v.startswith("[[") and not v.endswith("]]"):
                flag(n, "unclosed wikilink in %s" % k)
        if "\n" in n.fm_raw and re.search(r"\[\[[^\]]*\n", n.raw):
            flag(n, "wikilink broken across a line")

        if n.type == "item":
            ident = n.get("identified").lower()
            if ident not in ("true", "false"):
                flag(n, "identified is %r, expected true/false" % n.get("identified"))
            secs = n.sections()
            props = secs.get("Properties", "").strip()
            if ident == "false" and props:
                flag(n, "identified:false but Properties is filled")
            if ident == "true" and n.get("magical").lower() == "unknown" and not props:
                flag(n, "identified:true but magical unknown and no Properties")
            if n.get("magical").lower() not in ("true", "false", "unknown", ""):
                flag(n, "magical is %r" % n.get("magical"))

        if n.type in ("npc", "location", "item", "quest", "lore"):
            if "Session Log" not in n.sections():
                flag(n, "no ## Session Log section")

        if n.type == "session":
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", n.get("date")):
                flag(n, "date is %r" % n.get("date"))

        for t in n.links():
            if t.strip() not in names:
                flag(n, "broken link [[%s]]" % t.strip())

    table(problems, ["note", "problem"], "problem")


def cmd_grep(a):
    hits = []
    for n in load(a.archive):
        for i, line in enumerate(n.raw.splitlines(), 1):
            if a.pattern.lower() in line.lower():
                hits.append([n.rel, i, line.strip()[:90]])
    table(hits, ["note", "line", "text"], "hit")


def cmd_stats(a):
    notes = load(True)
    counts = {}
    for n in notes:
        counts[n.folder] = counts.get(n.folder, 0) + 1
    rows = [[k, counts[k]] for k in sorted(counts)]
    table(rows, ["folder", "notes"], "folder")
    items = [n for n in notes if n.type == "item" and n.folder == "05-Items-Loot"]
    un = [n.name for n in items if n.get("identified").lower() != "true"]
    print("items: %d   identified: %d   outstanding: %d" % (
        len(items), len(items) - len(un), len(un)))
    if un:
        print("outstanding: " + ", ".join(sorted(un)))


def cmd_set(a):
    hits = [n for n in load(True) if n.name.lower() == a.name.lower()]
    if len(hits) != 1:
        print("expected exactly one note named %r, found %d" % (a.name, len(hits)))
        return 1
    n = hits[0]
    line = "%s: %s" % (a.key, a.value) if a.value else "%s:" % a.key
    if a.key in n.fm:
        new, count = re.subn(r"(?m)^%s:.*$" % re.escape(a.key), lambda m: line, n.raw, count=1)
        assert count == 1
    else:
        end = n.raw.find("\n---", 3)
        new = n.raw[:end] + "\n" + line + n.raw[end:]
    print("%s\n  %s -> %s" % (n.rel, n.get(a.key) or "(empty)", a.value or "(empty)"))
    if a.dry_run:
        print("  [dry run, not written]")
    else:
        io.open(n.path, "w", encoding="utf-8").write(new)
        print("  written")
    return 0


# ---------------------------------------------------------------------- main

def main(argv):
    p = argparse.ArgumentParser(
        prog="vault.py", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd")

    def common(sp):
        sp.add_argument("--archive", action="store_true",
                        help="include 00-Inbox and 99-Processed")
        return sp

    s = common(sub.add_parser("ls", help="list notes"))
    s.add_argument("--type", help="npc|item|location|quest|session|lore")
    s.add_argument("--where", action="append", default=[], help="key=value filter")
    s.add_argument("--fields", help="comma-separated columns")
    s.set_defaults(fn=cmd_ls)

    s = sub.add_parser("get", help="show one note")
    s.add_argument("name")
    s.add_argument("--full", action="store_true", help="print the whole body")
    s.set_defaults(fn=cmd_get)

    s = common(sub.add_parser("fields", help="frontmatter keys in use"))
    s.add_argument("--type")
    s.set_defaults(fn=cmd_fields)

    s = sub.add_parser("links", help="broken links and orphans")
    s.set_defaults(fn=cmd_links)

    s = sub.add_parser("lint", help="schema and consistency problems")
    s.set_defaults(fn=cmd_lint)

    s = common(sub.add_parser("grep", help="search note text"))
    s.add_argument("pattern")
    s.set_defaults(fn=cmd_grep)

    s = sub.add_parser("stats", help="counts")
    s.set_defaults(fn=cmd_stats)

    s = sub.add_parser("set", help="change one frontmatter value")
    s.add_argument("name")
    s.add_argument("key")
    s.add_argument("value", nargs="?", default="")
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(fn=cmd_set)

    a = p.parse_args(argv)
    if not a.cmd:
        p.print_help()
        return 0
    return a.fn(a) or 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main(sys.argv[1:]))
