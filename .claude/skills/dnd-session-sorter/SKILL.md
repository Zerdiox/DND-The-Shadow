---
name: dnd-session-sorter
description: >-
  Sorts raw, unstructured D&D session notes from 00-Inbox into properly
  organized NPC, Location, Quest, Item, and Session files, updating existing
  entries instead of duplicating them. Use whenever the user asks to sort,
  organize, process, file, or clean up their D&D / campaign / session notes.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# D&D Session Sorter

Organize notes for an ongoing tabletop D&D campaign. The input is a raw, messy
session note — usually the most recently modified file in `00-Inbox/`. If the
user did not name a file, find it and confirm which one before editing anything:

```bash
ls -t 00-Inbox/*.md | head -5
```

Anything still in `00-Inbox/` is unsorted by definition; sorted originals live
in `99-Processed/`.

Work through the steps in order.

## 1. Search the vault first

Use the vault tool rather than ad-hoc scripts — `python .claude/tools/vault.py`:

```bash
python .claude/tools/vault.py ls --type item --where identified=false
python .claude/tools/vault.py get "Crown of Fear"
python .claude/tools/vault.py grep "prismatic"
python .claude/tools/vault.py lint      # run this after every sort
python .claude/tools/vault.py links     # broken wikilinks and orphans
```

`ls` filters with `--where key=value`, `key!=value`, `key~substring`, `key=`
(empty) and `key?` (present); `--fields` picks the columns. `fields` lists every
frontmatter key in use with empty counts, `stats` counts notes and outstanding
items, and `set <note> <key> <value>` changes one value (`--dry-run` first).
Run `vault.py` with no arguments for the full help.

Before creating any new file, search for existing notes matching each NPC,
location, item, or quest mentioned in the raw note:

- `Glob` on `02-NPCs/*.md`, `03-Locations/*.md`, `04-Quests-Plot/*.md`,
  `05-Items-Loot/*.md`, `06-Lore-Factions/*.md` to see what already exists.
- `Grep` for each name across the whole vault to catch entities filed in an
  unexpected folder or referenced only by an alias.

Match on name and obvious aliases/nicknames. If a match is ambiguous, ask the
user rather than guessing.

All vault folders already exist, including `04-Quests-Plot/` and
`06-Lore-Factions/` (currently empty) and `99-Processed/` (sorted originals).
Search `99-Processed/` too — an entity may have been described in an older raw
note that has already been archived.

## 2. Update existing notes, don't duplicate

If a note already exists for an entity, `Edit` it to add a dated bullet at the
end of its `## Session Log` section:

```
- [[Session NN - YYYY-MM-DD]]: What happened this session, in one or two sentences.
```

Never overwrite or rewrite existing sections — only append. Leave earlier log
bullets untouched even when they use an older link format.

If the `## Description` is thin and the raw notes add genuinely new standing
facts (not events), you may extend it. Events belong in the Session Log.

## 3. Create new notes for new entities

For any entity with no existing note, `Write` one file per entity in the correct
folder, using the matching template below. Fill in whatever the raw notes
support and leave other frontmatter fields blank rather than guessing.

Filename is the entity's name as it should appear in a `[[wikilink]]` —
`02-NPCs/Cassius Varro.md`, not a slug.

## 4. Update quest/plot status

If a quest note exists and the raw notes show it advanced, completed, or failed,
`Edit` its frontmatter `status:` field and add a `## Session Log` bullet. If it's
a brand-new thread, create a quest note from the template.

## 5. Write a clean session summary

Determine the next session number from the existing files:

```bash
ls 01-Sessions/
```

Session numbers are zero-padded and sequential; do not renumber existing ones.

Create `01-Sessions/Session NN - YYYY-MM-DD - Title.md` from the session
template, with a short recap, key decisions, notable moments, `[[wikilinks]]` to
every entity touched, and a `## Raw Notes` link back to the archived original.

Choose the title yourself — a short, evocative noun phrase, typically two to
four words, drawn from the session's most memorable turn (`The Hungry
Ambassador`, `The Crown of Fear`). Name what happened, not the location, and
never reuse an earlier session's title. Repeat it in the `title:` frontmatter
field. Use the date the session was played, which is the raw note's
modification date unless the user says otherwise.

## 6. Archive the raw note

Once the sort is complete, move the original file from `00-Inbox/` to
`99-Processed/` so the inbox self-empties:

```bash
mv "00-Inbox/NAME.md" "99-Processed/NAME.md"
```

Move it, do not delete or rewrite it. Deleting is permitted in this vault
now that git carries the history, but a raw note is the only primary record of
what was said at the table, so it is archived rather than removed.
Point the session summary's `## Raw Notes` link at the new `99-Processed/`
path, not the old inbox path. If a file of that name already exists in
`99-Processed/`, ask the user before overwriting.

## 7. Ask before guessing

If a name could be an existing NPC or a brand-new one, or if it's unclear which
quest a development belongs to, ask the user rather than assuming. Batch the
questions into one message instead of interrupting repeatedly.

## 8. Add the session to the archive page

The campaign has **one** published page, not one per session. Add to it; never
create a second one.

> **The Shadow** — https://claude.ai/artifact/7oHa5EKVDLApxf2i3ues5J
> Source: `reports/The Shadow.html`, next to this file.

Load the `artifact-design` skill before editing it.

### How to add a session

1. Open `reports/The Shadow.html`.
2. Add a nav entry as the **first** button in `<nav class="nav">`:
   `<button type="button" data-s="NN"><span class="n">NN</span><span class="t">Title</span></button>`
3. Move `aria-current="true"` from the old newest button to the new one.
4. Add `hidden` to the previously newest `<article class="session">`, and insert
   the new panel immediately after the nav **without** `hidden` — the newest
   session is what the page shows at rest.
5. Update the four `.status` tiles in the masthead: where we are, what we are
   after, what is behind us, what is still unidentified.
6. Update the colophon's "Last updated after session NN".
7. Republish `reports/The Shadow.html`. In the conversation that last published
   it, the same file path keeps the URL. **From any other conversation, pass the
   URL above as `url`** — without it you create a duplicate page.

### Panel skeleton

```html
<article class="session" id="session-NN">
  <div class="session-head">
    <p class="eyebrow">Session NN · D Month YYYY</p>
    <h2>Title</h2>
    <p class="standfirst">One sentence.</p>
  </div>
  <div class="session-rule"></div>
  <section class="block-sec"> ... </section>
</article>
```

### Components already in the page

Reuse these; only build something new when a session genuinely calls for it.

| Component | Use |
|---|---|
| `.shaft` + `.room` | The descent. `.move` for the movement label (`↓ ladder`, `→ across the shaft`), `.danger` / `.peril` / `.reveal` to colour the station dot, `.pull` for the turning point |
| `.quarry` + `.tried` | A creature, with a table of what worked on it and what didn't |
| `.chest-grid` + `.chest` | Anything the notes number. `.flagged` and `.chest-tag` mark the notable ones, `.chest-by` says who found it |
| `.ledger` | Any table — loot values, identifications. `.num` for figures, `tfoot` for a total |
| `.relics` + `.relic` + `.mech` | Named items with mechanics. `.ingot` for a material swatch |
| `.gallery` + `.block` + `.band` | Objects drawn from their descriptions |
| `.thread-list` + `.thread` | Still-open questions, numbered |
| `.beats` | Short decisions / moments lists, for a session that doesn't need full prose |

### Writing

Narrate as the party — "we", past tense. The descent is prose and should flow:
let each room lead into the next with a connecting line ("So we took the stairs
instead"), vary sentence length so the short lines land, and keep a light touch
of humour where the table earned it (Drivik licking things). Don't pad and don't
invent: every fact comes from the session's vault notes. Tables, placards and
the open questions stay terse — the flow belongs in the descent. Take pronouns
from each character's `pronouns:` field.

The page is private until the user shares it from the page's Share menu.

### Superseded

These three per-session pages came before the archive. They are still live and
two of them are shared; leave them alone unless the user asks.

| Session | Page |
|---|---|
| 03 | https://claude.ai/artifact/YP3zYNZ5uUye13D7yVbVqw |
| 04 | https://claude.ai/code/artifact/c6af53cf-c4c7-414f-b00b-a13bbcca9f08 |
| 05 | https://claude.ai/artifact/BrsACJRqdFgDNvaYwWoohk |

Their source files stay in `reports/` as historical copies.

## 9. Report what you did

Run `python .claude/tools/vault.py lint` and `links` first and fix anything they
flag. Then finish with a short list: notes created, notes updated, anything you skipped or
could not resolve, and the link to the archive page.

---

## Conventions

- Cross-references are Obsidian `[[wikilinks]]`, including inside frontmatter
  (`location: [[The Dam]]`, `first_appeared: [[Session 01 - 2026-08-01]]`).
- Session links use the full filename, title included:
  `[[Session 03 - 2026-09-04 - The Hungry Ambassador]]`. Sessions 01 and 02 predate
  the title convention and keep their untitled names — link them as they are.
- `tags:` is an inline YAML list, with the type as the first tag plus any
  distinguishing extras — `tags: [npc, mummy]`.
- `pronouns:` records how a character is referred to. Use it rather than
  inferring from a name or a race. Leave it blank and use they/them in prose
  when the notes have not established it.
- `status:` on an NPC is free text describing their state, not a fixed
  vocabulary — `alive`, `dead`, `undead / mummy`.

## Note templates

### NPC (`02-NPCs/`)
```
---
type: npc
status: alive
pronouns:
location:
faction:
first_appeared:
tags: [npc]
---

## Description

## Session Log
```

### Location (`03-Locations/`)
```
---
type: location
region:
first_visited:
tags: [location]
---

## Description

## Session Log
```

### Quest / Plot thread (`04-Quests-Plot/`)
```
---
type: quest
status: active
related_npcs:
related_locations:
started:
tags: [quest]
---

## Summary

## Session Log
```

### Item / Loot (`05-Items-Loot/`)
```
---
type: item
item_type:        # weapon | armor | wondrous item | ring | wand | staff | rod | potion | scroll | mundane
rarity: unknown   # common | uncommon | rare | very rare | legendary | artifact | varies | unknown
attunement:       # false, true, or a requirement e.g. "by a spellcaster"
magical:          # true | false | unknown
quantity: 1
weight:
value:
owner:
found:
identified: false
ddb_add:          # yes | no — should this go onto D&D Beyond? leave blank if unsure
tags: [item]
---

## Description

## Properties

## Session Log
```

`ddb_add` is the user's call, not yours. Set `no` for anything the party no
longer has — returned, sold, left behind — and otherwise leave it blank and
mention the new items in your report so the user can mark them. The
`dndbeyond-homebrew` skill only pushes `ddb_add: yes`.

Item frontmatter mirrors the fields D&D Beyond and 5etools expect, so a note can
be exported to either later without rework. Rules for filling it:

- Only record what the party has actually established in play. An unidentified
  item keeps `rarity: unknown`, `magical: unknown`, `identified: false`, and an
  empty `## Properties` — never invent stats, rarity, or attunement.
- `## Description` is what the item looks like in the fiction. `## Properties`
  is mechanical text only (bonuses, charges, activation, save DCs), added once
  the party identifies it.
- Set `identified: true` and fill `rarity`/`magical`/`## Properties` in the same
  session the party learns them, and log that discovery in `## Session Log`.

### Session summary (`01-Sessions/`)
```
---
type: session
date: YYYY-MM-DD
title: Title
tags: [session]
---

## Recap

## Key decisions

## Notable moments

## Linked
- NPCs:
- Locations:
- Quests:
- Items:
- Lore:

## Raw Notes
- [[99-Processed/FILENAME.md|Original Session Notes]]
```
