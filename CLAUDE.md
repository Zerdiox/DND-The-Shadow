# The Shadow — campaign vault

An Obsidian vault for a D&D 5e (2024) campaign, synced by Syncthing. The user
plays **Vicaster Cloudwink**; the DM is **Zedicius**. They are a player, not the
DM — do not assume DM-side access to anything.

**Read [.claude/HANDOFF.md](.claude/HANDOFF.md) first.** It carries the working
state, what is open, and the mistakes already made and corrected.

## Standing rules

- **Never delete files. Only create or append.** Archive to `99-Processed/`
  instead. This overrides any tidying instinct.
- **Ask rather than guess.** When the notes are ambiguous, say what the readings
  are and ask. Never invent a mechanic, a name, or a motive the notes do not
  give.
- **Validate what you do.** Read the result back; do not trust that an edit or a
  click landed.
- **Reject cookie banners** without asking.

## Tooling

`python .claude/tools/vault.py` — query and lint the frontmatter. Use it
instead of writing another one-off script. `lint`, `links`, `stats`, `ls`,
`get`, `grep`, `fields`, `set`; `ls --help` for the filter syntax.

## Skills

- **`dnd-session-sorter`** — raw session notes in `00-Inbox/` into structured
  notes. Read it before sorting.
- **`dndbeyond-homebrew`** — vault items onto D&D Beyond, by driving the user's
  real Chrome. Read it before touching that site; it records several traps that
  silently produce wrong data.

## Layout

```
00-Inbox/        raw notes waiting to be sorted
01-Sessions/     one note per session, "Session NN - YYYY-MM-DD - Title"
02-NPCs/         type: npc, plus the five PCs as type: pc
03-Locations/    04-Quests-Plot/   05-Items-Loot/   06-Lore-Factions/
99-Processed/    sorted raw notes, kept not deleted
```

## Update — 31 October 2026

**Obsidian is no longer used.** The user has dropped the Obsidian app. The
opening description above is superseded to that extent: this is now a folder of
plain markdown files synced by Syncthing, read in whatever editor is to hand.

Nothing else changed. Frontmatter, the folder layout, `vault.py` and the skills
all stay exactly as documented — the structure was kept deliberately, because it
is what makes the vault queryable. Do not strip frontmatter or flatten folders
on the assumption that "the vault is gone"; it is not.

**Correction, same day:** Syncthing is being dropped too. The note above says
"synced by Syncthing"; that will stop being true. The files then live on this
machine only, with no second copy — worth raising with the user, since the
vault's whole value is that it survives between sessions.
