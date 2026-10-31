# Handoff — 31 October 2026

Written at the end of a session that ran from 4 September to 31 October 2026.
That conversation is gone; this is what the next one needs to know that the
files do not already say. Read it once, then trust the vault and the skills.

## Start here

```bash
python .claude/tools/vault.py lint      # schema + consistency
python .claude/tools/vault.py links     # broken wikilinks, orphans
python .claude/tools/vault.py stats     # folder counts, unidentified items
```

Three skills matter: `dnd-session-sorter` (raw notes → structured notes),
`dndbeyond-homebrew` (vault → D&D Beyond), and `vault.py` itself, which exists
so nobody hand-rolls another frontmatter script. **Read the skill before the
task, not after it goes wrong** — both carry traps that cost real hours.

## Where things stand

- **Sessions 01–06 are sorted.** 06 was *The Silver Tongue*, 23 October.
- **The group-facing archive** is one artifact, updated per session, not a new
  one each time: <https://claude.ai/artifact/7oHa5EKVDLApxf2i3ues5J>
- **D&D Beyond is current.** Party Equipment holds 77 rows: 24 homebrew magic
  items, 26 custom rows added 31 October, and what was already there. Every
  item note records the outcome in `ddb`.
- **`ddb_add` is the user's field, not yours.** `yes` means it belongs on D&D
  Beyond; `no` means deliberately not. Never flip a `no`. The work queue is
  `vault.py ls --type item --where ddb_add=yes --where 'ddb='`.

## Open, in rough priority order

1. **The user was deleting rows from Party Equipment** on 31 October and had not
   said which. Until they do, `ddb` on those notes is stale — it claims a row
   that may be gone. Offer to reconcile; do not assume a missing row should go
   back.
2. **Campaign sharing is unsolved.** The user is a player, not the DM (that is
   Zedicius). No player-side "share homebrew with the campaign" control exists
   on the item edit page, My Creations, or the campaign page. **Publishing is
   not sharing** — it submits the item to D&D Beyond's public listing for
   moderation. Do not use it as a workaround. The user thought there was
   "some other option"; ask them before hunting again.
3. **Playwright MCP was configured on 31 October** with `--extension`, and the
   Playwright Extension is installed in Chrome's Default profile. It has never
   been exercised — the session that set it up could not load it. Whether it
   coexists with the Claude extension in the same browser is **unknown**. If it
   works it should beat coordinate-clicking for D&D Beyond; if it does not,
   Claude in Chrome still does the job.
4. **`Untitled.md`** at the vault root has no frontmatter — a sync test from
   months ago. Lint has flagged it every run since. It has never been deleted
   because of the standing rule below. Ask whether to archive it to
   `99-Processed/`.

## Gaps in the vault

Flagged, never filled. Worth asking about when the subject comes up, not worth a
special trip.

- **Muradin** has no pronouns; the other four PCs do. **Vraaxis** (Zedicius's
  lizardfolk barbarian) has no note at all.
- **14 of 16 NPCs have no pronouns**, and `race`/`class` are blank throughout.
  Only Crystal Sisters and The Woman in the Ice are filled.
- **Priest** has no name, race or class.
- **The Crystal Sister whose heart was stolen** is still unnamed.
- **Three items remain unidentified**: Green Sword, Prismatic Keys, Silver
  Tongue. All three are recorded as observed-but-not-identified; do not invent
  mechanics for them.
- **Pre-existing party inventory rows** nobody has reconciled with the vault:
  `firestarter marble` ×6, `bag of boulders`, `chest of preserving`,
  `dwergenkop met rune`, `Koper bal met knop`, `Avatar leftover`.

## How this user works

Learned the hard way; worth more than it looks.

- **Never delete files.** `DnD Campaign.md` carries the rule: only create or
  append. `99-Processed/` exists so raw notes can be archived instead.
- **Ask rather than guess.** They would far rather answer a question than find
  an invention in their campaign later. When notes are ambiguous, list the
  reading and ask — they answer fast and in a few words ("Nvm, it was the
  heart", "just metal").
- **"Validate what you do."** Their words, after a form field silently refused a
  value and reported success. Verify by reading the result back, not by trusting
  that the click landed. This caught several real errors.
- **Not everything is magical.** Most of the Vault hoard is inert — acidic
  emeralds, a stone disc, fabric. The user corrects over-reading briskly. Write
  what the notes say.
- **Cookie banners: always reject, never ask.**
- They read the vault in Obsidian, synced by Syncthing, often from a phone.
  Keep notes legible as prose, not just as data.

## Things that were got wrong

So they are not got wrong again.

- The chain going down the shaft is **plain metal**, not prismatic. That claim
  came from over-reading a Session 02 raw note.
- Parenthesised numbers in the Session 03 notes are **chest numbers**, not dice
  rolls. Proved by chest "(1)" appearing twice.
- The "salt room" in Session 05 **is** the Crystal Hall.
- Echo of Twilight is **he/him**.

## Update — 31 October 2026, later

Appended after the handoff above was written. Both items correct something
stated there.

- **Playwright MCP works.** Open item 3 above says it "has never been exercised"
  and that coexistence with the Claude extension is "unknown". Both are now
  settled: it was exercised on 31 October and it does coexist. With
  `--extension` it attaches to the user's real Chrome 156 — their own profile,
  their live D&D Beyond login, verified by reading the Vicaster sheet while
  signed in as Zerdiox. Tab control, accessibility snapshots, clicks and
  screenshots all confirmed on a throwaway tab. It should beat
  coordinate-clicking for the `dndbeyond-homebrew` work; `browser_fill_form` and
  `browser_snapshot` map well onto that form. Two cautions: it writes scratch
  files to `.playwright-mcp/` inside the vault, which Syncthing is not ignoring,
  and `browser_run_code_unsafe` is RCE-equivalent — the ordinary tools suffice.
- **Obsidian has been dropped**, the vault structure deliberately kept. See the
  update appended to `CLAUDE.md`.
- **Open item 1 is still open.** The Party Equipment rows the user deleted on
  31 October were never identified, so `ddb` on the 50 `ddb_add: yes` notes
  (24 homebrew URLs, 26 custom) may still be stale. Reconciliation was offered
  and not yet taken up.

## Update — 31 October 2026, git

- **The vault is a git repository now.** Obsidian and Syncthing are both being
  dropped, which would have left these files as a single uncopied directory;
  git replaces the history `.stversions` was providing. `.gitattributes` sets
  `* -text` so notes are stored byte-for-byte — do not remove it, or every
  checkout rewrites line endings across the vault.
  `.smart-env/`, `.stfolder/` and `.playwright-mcp/` are ignored as derived
  data. `.obsidian/`, `.trash/` and `.stversions/` are deliberately **tracked**,
  despite looking like junk: `.stversions/00-Inbox/` holds old raw-note versions
  that exist nowhere else, and the standing rule is never delete.
- **Pushed to GitHub**, 31 October: <https://github.com/Zerdiox/dnd_the_shadow>,
  `main` tracking `origin/main`. The repository is **public, and that is the
  user's deliberate choice** — they said so when asked. Do not treat it as a
  mistake or offer to make it private again. Practical consequence: everything
  committed is published, including history, so the files removed in the
  cleanup are still readable there.
- **`.trash/Session 01 - 2026-08-29.md` is a superseded draft, not a lost
  edit.** Checked on 31 October. It duplicates `Session 01 - 2026-08-01.md` but
  is dated to Session 02's date and its recap is a strict subset — the live note
  additionally names Gaius Seberam, Octanius Rex and Quintus Valerian as the
  deceased engineers. Nothing to recover; left in place under the never-delete
  rule.
- **Open item 1 is closed.** See `RECONCILIATION-2026-10-31.md`: the five
  deleted Party Equipment rows were identified and their notes now read
  `ddb: removed 2026-10-31`. A second decision from that reconciliation is
  still open — the Cervits are on D&D Beyond under Dutch names despite
  `ddb_add: no`.

## Update — 31 October 2026, cleanup

Obsidian, Syncthing and the Gemini Scribe plugin are all dropped and their
files deleted; the vault went from 212 tracked files to 149, and from 6.8 MB
to 615 KB.

**Nothing campaign-related was touched.** 6 sessions, 21 NPCs, 31 locations,
4 quests, 55 items, 4 lore notes and 15 processed raw notes all remain. `lint`
is clean for the first time (the `Untitled.md` it had flagged every run was a
9-byte sync test, now gone).

**To get any of it back**, the pre-squash history is kept as a bundle outside
the repository:

```bash
git clone "D:/Documents/Dungeons and dragons/dnd_the_shadow-history-2026-10-31.bundle" old-history
```

That bundle holds all 13 original commits and verifies as a complete history.
It is the only copy — it is deliberately outside the vault so the repository
does not carry it, which also means nothing backs it up. The restore itself was
tested before the squash: a deleted file was recovered from history and removed
again.

Three things were never tracked and so are **permanently gone**: `.stfolder/`
(empty Syncthing marker), `.smart-env/` (Obsidian plugin cache, regenerable)
and `.playwright-mcp/` (tool scratch, including the raw inventory JSON behind
`RECONCILIATION-2026-10-31.md`; the report itself is the durable record).

`DnD Campaign.md` was removed too. It was Gemini Scribe project config and its
rules are duplicated in `CLAUDE.md`.

**`CLAUDE.md` still says "Never delete files. Only create or append."** That
rule predates git and is now wrong, but rewriting it needs the user's approval
— it governs assistant behaviour, so it is gated. Until it is updated, read it
as: commit first, then delete freely; check `git ls-files <path>` before
removing anything, because untracked files have no safety net.

**Orphan, pre-existing:** `vault.py links` reports `Rem Koolhuis` (02-NPCs) as
a note nothing links to. Not caused by the cleanup — nothing deleted referenced
an NPC. Belongs with the gaps list above; worth a question when the subject
comes up.

**Cervits renamed to English (31 October).** `Cervit wit` / `Cervit zwart` on
D&D Beyond are now `White Cervit` / `Black Cervit`, descriptions translated,
verified after a reload. `ddb_name` dropped from both notes as a result — the
names agree again. The user's standing preference: **keep D&D Beyond in
English**, matching the vault.

**Driving the sheet is now documented.** See
`dndbeyond-homebrew/references/playwright-recipes.md` — six numbered recipes
(open the inventory, read it, edit a row, add a custom item, add a homebrew
item, change a quantity), a full selector table, and the verification snippet.
Each recipe states whether it has been run end to end: 1-3 have, 4-5 have
their selectors mapped but the final ADD click is unproven. `SKILL.md` points
there; its coordinate tables stay only as a fallback.


## Why things are the way they are

The repository history was squashed to a single commit on 31 October 2026 at
the user's request, to stop the deleted Obsidian/Syncthing/Gemini files being
published in a public repo. These four explanations lived only in the commit
messages that squash discarded, so they are recorded here instead.

- **The five `ddb: removed 2026-10-31` items.** Claw Knives, Crossbow Bolts,
  Crossbow Snares, Crossbows and Rusted Gas Masks were deleted from Party
  Equipment on D&D Beyond. Their notes were set to `removed <date>` rather than
  blanked, deliberately: blanking `ddb` would push all five back into the
  work queue as items to add, and a missing row may have been removed on
  purpose. The count corroborated them — 77 recorded minus these 5 equals the
  72 rows then live.
- **`.gitattributes` holds `* -text`, and why one commit changed 6,525 lines.**
  autocrlf is on globally, so the first commit was stored LF-normalised while
  everything after it was stored verbatim. Renormalising touched 6,525 lines —
  insertions exactly equalling deletions, because **no content changed, only
  how git stored it**. Removing `.gitattributes` would restart that churn.
- **What was checked before `.stversions` was deleted.** Every `.md` in it
  either had a live counterpart elsewhere in the vault or was 0 bytes. Five
  files had no live copy; all five were empty. Nothing unique was lost. The
  same check cleared `.trash`, whose only non-empty file was a superseded
  Session 01 draft.
- **Why `ddb_name` is absent from the Cervits.** It exists to record a D&D
  Beyond row whose name differs from the note. Both rows were renamed to
  English, so the names agree and the key is correctly absent. Seven other
  items still carry it, and any reconciliation matching note names against the
  live inventory must consult it or it will report false negatives.