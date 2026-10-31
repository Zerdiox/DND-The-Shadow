# Party Equipment reconciliation — 31 October 2026

Read live from D&D Beyond via Playwright (real Chrome, signed in as Zerdiox),
character sheet 147071691, Party Inventory tab. Read-only: nothing was added,
removed or edited. This closes open item 1 in `HANDOFF.md`.

**Live count: 72 rows.** The handoff recorded 77. The five missing rows are
identified below, so the arithmetic is fully accounted for.

## The five deleted rows

All five are `ddb: custom` in the vault, so their notes currently claim a Party
Equipment row that no longer exists.

| Item | Vault note still says |
|---|---|
| Claw Knives | `ddb: custom` |
| Crossbow Bolts | `ddb: custom` |
| Crossbow Snares | `ddb: custom` |
| Crossbows | `ddb: custom` |
| Rusted Gas Masks | `ddb: custom` |

They are a coherent group — armoury weapons and gear — which is consistent with
a deliberate clear-out rather than an accident. **Not re-added.** Per the
handoff, a missing row may have been removed on purpose.

## What is intact

- **All 24 homebrew items** are present and correct. None were touched.
- **21 of the 26 custom rows** remain.
- Four of the five `ddb_add: no` items are correctly absent: Green Sword,
  Milky Heart Crystal, Toga Sculpture, and (see below) the Cervits.

Matching was by name prefix, so the 45 "present" results are prefix matches —
`Poison Vials` resolved to `Poison Vial (Cradle)`, for instance. The five
missing rows do not rest on the matcher alone: 77 recorded minus those 5 equals
the 72 rows actually on the page, so the count corroborates them.

## Two things the diff turned up that nobody was looking for

### The Cervits are on D&D Beyond, under Dutch names

`White Cervit` and `Black Cervit` are both marked **`ddb_add: no`** — deliberately
not to be pushed. But Party Equipment holds:

| Live row | Quantity | Cost | Vault note |
|---|---|---|---|
| `Cervit wit` | 80 | -- | White Cervit — "100 gp per kg (8,000 gp)" |
| `Cervit zwart` | 10 | 1000 | Black Cervit — "100 gp per kg (1,000 gp)" |

80 kg x 100 gp = 8,000 and 10 kg x 100 gp = 1,000, so these are the same two
items, added by hand under Dutch names. The automated diff missed them because
the word order is reversed; they were caught by eye.

**Correction.** An earlier draft of this report called that a contradiction
between the vault and the account. It was not. Both notes already read
`ddb: n/a - already in Party Equipment as the custom row 'Cervit wit'`
(and `'Cervit zwart'`). The vault had the situation recorded correctly all
along; the `no` meant "do not add, it is already there", not "this does not
belong on D&D Beyond". The error was in the check — it tested only whether a
row was present and never read the `ddb` text.

### `Avatar leftover` is no longer in Party Equipment

The handoff lists it among the pre-existing unreconciled rows; it is not in the
live 72. Note the limit of that evidence: the detail pane offers **MOVE**
(Equipment / Party Equipment / Bag of Devouring) as well as DELETE, so a row can
leave Party Equipment without being deleted. Bag of Devouring reads (0), but the
characters' own Equipment was not checked. It has no vault note either way, so
there is nothing to correct.

## Still unreconciled: live rows with no vault note

Unchanged from the handoff, plus five it did not list. Ordinary adventuring gear
(Acid, Arrows, Crowbar, Piton, Rations, Tinderbox, Longbow, Longsword, two
Shortswords, Climber's Kit, Alchemist's Supplies, Hammer) is excluded as
uninteresting.

Pre-existing homebrew: `Bracers of Flux`, `Jade Dragon Wistle`.

Custom rows: `bag of boulders`, `chest of preserving`, `dwergenkop met rune`,
`firestarter marble` x6, `Koper bal met knop`, and newly noted — `music box`,
`nature Chrystal`, `some silver ore`, `sturdy metallike scroll`,
`wooden carved bird`.

## Open decisions — two, both the user's call

### 1. What the five stale notes should say

Claw Knives, Crossbow Bolts, Crossbow Snares, Crossbows and Rusted Gas Masks
still read `ddb: custom`. Until that changes they claim a row that is not there,
and the work-queue command (`ls --type item --where ddb_add=yes --where 'ddb='`)
will keep reporting an empty queue because the field is *filled*, not because
the work is done.

Suggested: `ddb: removed 2026-10-31`. That keeps the history, keeps lint clean,
and keeps them out of the queue. Blanking `ddb` instead would push all five back
into the work queue as things to add — which contradicts the handoff's rule that
a missing row may have been removed on purpose.

**Resolved 31 October 2026.** The user approved it; all five now read
`ddb: removed 2026-10-31`, verified by reading the frontmatter back. Lint is
unchanged (the only outstanding problem is still `Untitled.md`). The rows were
not re-added to D&D Beyond.

### 2. The Cervits — resolved 31 October 2026

The user confirmed they added `Cervit wit` and `Cervit zwart` to Party
Equipment by hand. Both notes now read `ddb_add: yes` and
`ddb: custom item in Party Equipment`, matching the other 21 custom rows, and
were verified by reading the frontmatter back. Nothing was changed on D&D
Beyond — the rows were already correct; only the notes needed bringing into
line.

That makes the vault's tally 23 custom rows and 24 homebrew items recorded as
live, 5 marked removed, and 3 deliberately absent (Green Sword, Milky Heart
Crystal, Toga Sculpture). 23 + 24 = 47 vault-recorded rows against 25 live rows
with no vault note, which is the 72 actually on the page.

One cosmetic mismatch, not worth acting on: `Cervit zwart` carries a 1000 gp
cost on its row while `Cervit wit` carries none, though the vault values both
at 100 gp per kg.

**Renamed to English, same day.** At the user's request the two rows were
renamed on D&D Beyond: `Cervit wit` -> `White Cervit`, `Cervit zwart` ->
`Black Cervit`. Their Dutch descriptions were translated too
("Brand weerstendig" -> "Fire resistant"; "Stof dat immuun is tegen magisch
ray casts" -> "Material immune to magical ray spells"). Verified by reloading
the sheet and reading the names back out of the DOM: no Dutch remains in the
72 rows.

`ddb_name` was therefore removed from both notes — note name and row name now
agree, which is the only condition under which that key should be absent. Seven
items still carry it.
