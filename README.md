# The Shadow — campaign vault

Notes for an ongoing D&D 5e (2024) campaign, kept as plain markdown and
versioned with git. No app is required to read or edit them: any text editor
will do. The user plays **Vicaster Cloudwink**; the DM is **Zedicius**.

This file documents the structure so it can be rebuilt or verified from
scratch. For how to *work* in the vault, see `CLAUDE.md`; for current state and
open threads, see `.claude/HANDOFF.md`.

## Layout

```
00-Inbox/          raw session dumps waiting to be sorted
01-Sessions/       one note per session, "Session NN - YYYY-MM-DD - Title"
02-NPCs/           one per character: type npc, plus the PCs as type pc
03-Locations/      one per place
04-Quests-Plot/    active and resolved plot threads
05-Items-Loot/     items and loot
06-Lore-Factions/  background lore and factions
99-Processed/      raw notes kept after sorting, plain prose, no frontmatter
.claude/           tooling, skills and handoff notes (see below)
```

`00-Inbox/` holds a `.gitkeep` so the folder survives a clone while empty —
git cannot track an empty directory, and the sorter expects it to exist. Any
folder that empties out needs the same treatment.

## Frontmatter

Every note outside `99-Processed/` carries YAML frontmatter. `type` and `tags`
are universal; the rest depend on `type`.

| type | keys |
|---|---|
| *all* | `type`, `tags` |
| `session` | `date`, `title` |
| `npc`, `pc` | `status`, `pronouns`, `location`, `faction`, `first_appeared` |
| `pc` | also `ddb` (character sheet URL) |
| `location` | `region`, `first_visited` |
| `quest` | `status`, `started`, `related_npcs`, `related_locations` |
| `item` | `item_type`, `rarity`, `attunement`, `magical`, `quantity`, `weight`, `value`, `owner`, `found`, `identified`, `ddb`, `ddb_add`, `ddb_name` |

Blank values are normal and meaningful — `attunement` is empty on all 55 items,
`weight` on 53. Empty means "not applicable or not known", not "missing".

### The three `ddb` keys

These track what is on D&D Beyond, and they are easy to confuse.

- **`ddb_add`** — *the user's decision*, `yes` or `no`. Whether the item belongs
  on D&D Beyond at all. Never flip a `no` without being asked.
- **`ddb`** — *the outcome*. A homebrew URL, `custom item in Party Equipment`,
  or `removed <date>` for a row that was deleted. Empty means the work is
  pending.
- **`ddb_name`** — *only when the row is named differently there*. Seven items
  use it, mostly disambiguating suffixes such as
  `Poison Vials` → `Poison Vial (Cradle)`.

`ddb_name` matters more than it looks: any reconciliation that matches vault
notes against the live inventory by note name alone will produce false
negatives on those nine. Match on `ddb_name` where present.

The pending-work queue is:

```bash
python .claude/tools/vault.py ls --type item --where ddb_add=yes --where 'ddb='
```

## Tooling

`python .claude/tools/vault.py` queries and lints the frontmatter. Use it
rather than writing another one-off script.

| Command | What it does |
|---|---|
| `lint` | schema and consistency problems |
| `links` | broken `[[wikilinks]]` and orphaned notes |
| `stats` | counts per folder, unidentified items |
| `ls` | list notes as a table; `--type`, `--fields`, `--where` |
| `get` | one note's frontmatter and section names |
| `grep` | search note bodies |
| `fields` | every frontmatter key in use, with counts |
| `set` | change one value on one note; `--dry-run` first |

`ls --help` documents the `--where` filter syntax.

## Skills

In `.claude/skills/`:

- **`dnd-session-sorter`** — raw notes in `00-Inbox/` into structured notes.
- **`dndbeyond-homebrew`** — vault items onto D&D Beyond through the browser.

Both record traps that cost real time. Read the relevant one before starting.

## Working copy

Everything needed is in the repository; a clone is a complete working copy.
The remote is <https://github.com/Zerdiox/dnd_the_shadow>, **public by the
user's deliberate choice** — treat anything committed here as published.

```bash
git clone https://github.com/Zerdiox/dnd_the_shadow.git "DnD - The Shadow"
cd "DnD - The Shadow"
python .claude/tools/vault.py lint     # should report no problems
python .claude/tools/vault.py stats    # folder counts
```

`.gitattributes` sets `* -text`, so notes are stored byte-for-byte. Removing it
makes git rewrite line endings on checkout and turns every diff into a
whole-file rewrite.

Obsidian, Syncthing and the Gemini Scribe plugin were all dropped on
31 October 2026 and their files removed. The history predating that cleanup is
kept as a git bundle outside the repository; see `.claude/HANDOFF.md` for the
path and how to restore from it.
