---
name: dndbeyond-homebrew
description: >-
  Create homebrew magic items on D&D Beyond from this vault's item notes, by
  driving the user's real Chrome. Use whenever the user asks to put an item,
  weapon or potion onto D&D Beyond, to publish homebrew, or to get vault loot
  onto a character sheet.
allowed-tools: Read, Bash, Glob, Grep
---

# D&D Beyond homebrew

There is **no API and no JSON import** for D&D Beyond homebrew. The web form is
the only route, so this is a browser task: Claude in Chrome
(`mcp__claude-in-chrome__*`), which uses the user's real signed-in Chrome. The
in-app browser has no sign-in and cannot do this.

Account in use: **Zerdiox**.

## Before you start

Load the `anthropic-skills:chrome-browser` skill, then load the tools in ONE
ToolSearch call:

```
select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__find,mcp__claude-in-chrome__form_input,mcp__claude-in-chrome__browser_batch,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__tabs_close_mcp
```

Then `tabs_context_mcp {createIfEmpty: true}` to get a tab id. Batch everything
after that with `browser_batch`.

## URLs

| What | URL |
|---|---|
| Blank magic item form | `https://www.dndbeyond.com/homebrew/creations/create-magic-item/create` |
| Homebrew hub | `https://www.dndbeyond.com/homebrew` |
| A saved item | `https://www.dndbeyond.com/homebrew/creations/magic-items/<id>-<slug>/edit` |

**These 404 — do not use them:** `/magic-items/create`, `/homebrew/creations`.

## The form

All on one page. `find` returns the refs; they are not stable between loads.

| Field | Required | Notes |
|---|---|---|
| Name | yes | plain textbox, `form_input` works |
| Version | no | leave blank |
| Rarity | yes | dropdown. **`Unknown Rarity` is an option** — use it rather than inventing a rarity |
| Base Item Type | yes | `Item`, `Armor` or `Weapon`. Defaults to `Item` |
| Magic Item Type | yes | only populates after Base Item Type. For `Item`: Wondrous Item, Rod, Scroll, Staff, Wand, Ring, Potion |
| Base Armor / Dex Bonus / Str Requirement / Stealth Check | no | only for `Armor` |
| Base Weapon | no | only for `Weapon` |
| Requires Attunement | no | checkbox |
| Attunement Description | shows `*` | **not actually enforced** — a save with it empty succeeds |
| Description | yes | TinyMCE — see the gotcha below |

### The description editor gotcha

The description is a TinyMCE instance in an iframe. `form_input` on it does
nothing, and clicking its `ref` focuses the wrapper, not the text body — typing
then goes nowhere and the box stays visibly empty.

**Click inside the text area by coordinate instead**, then `type`. Use `zoom` on
the description region to find the body, then click the middle of it. `Return`
between paragraphs works normally. Always `zoom` afterwards to confirm the text
actually landed.

## Mapping vault frontmatter to the form

Read the item note first (`python .claude/tools/vault.py get "<name>"`).

| Vault | Form |
|---|---|
| note filename | Name |
| `rarity: unknown` | Rarity → `Unknown Rarity` |
| `item_type: wondrous item` | Base Item Type `Item` + Magic Item Type `Wondrous Item` |
| `item_type: weapon` | Base Item Type `Weapon`, then pick a Base Weapon |
| `item_type: potion` | Base Item Type `Item` + Magic Item Type `Potion` |
| `attunement:` blank | leave the checkbox off |
| `## Description` | first paragraph of the form Description |
| `## Properties` | the paragraphs after it, as prose |

Never invent a rarity, an attunement requirement, or mechanics the vault does
not have. `identified: false` items have nothing to publish — say so instead.

## After saving

Click **Create Magic Item**. The page becomes the item's edit page and the URL
carries the new id. Record it on the vault note:

```bash
python .claude/tools/vault.py set "Crown of Fear" ddb "https://www.dndbeyond.com/homebrew/creations/magic-items/12140241-crown-of-fear"
```

`ddb` is an optional frontmatter key that `vault.py lint` accepts and does not
require. Use it to tell at a glance what has already been published:

```bash
python .claude/tools/vault.py ls --type item --where "ddb=" --where identified=true
```

The edit page then offers **Modifiers**, **Conditions** and **Spells**. These
drive the character-sheet integration (damage bonuses, applied conditions,
castable spells). They are optional; only fill them when the user asks, and only
from mechanics the vault actually records.

## Rules of engagement

- Fill the whole form, then **stop and show the user a screenshot before
  clicking Create Magic Item**. Creating is a real change to their account.
- One item at a time unless the user says to batch, and confirm the first of a
  batch before continuing with the rest.
- Never enter credentials. If the session is signed out, say so and wait.
- Homebrew is private to the account by default. Do not publish or share it.

## What to push: `ddb_add` decides, not you

Every item note carries `ddb_add: yes | no`, and **it is the user's call.**

```bash
python .claude/tools/vault.py ls --type item --where ddb_add=yes --where 'ddb='
```

That is the work queue: marked for D&D Beyond, not there yet. Nothing else goes
up. A blank `ddb_add` means undecided — list those for the user instead of
guessing, and never flip a `no` back to `yes` on your own.

`ddb` then records what happened: a homebrew URL, `custom item in Party
Equipment`, or `n/a - <reason>`.

**When the user prunes the party list**, `ddb` goes stale — the note still
claims a row that is gone. Reconcile by reading the Party Equipment contents,
then for anything no longer there set `ddb_add: no` and clear `ddb`. Offer this;
do not assume a missing row means the user wants it put back.

## Homebrew or custom item? Decide this first

Once an item is marked for pushing, this is yours to judge. Not every vault item
wants to be homebrew. The party inventory already holds
custom rows (`Cervit wit`, `bag of boulders`, `dwergenkop met rune`) alongside
the homebrew, and for most loot a custom row is the better fit.

| | Custom item | Homebrew magic item |
|---|---|---|
| Lives in | the party inventory row itself | My Creations, account-wide |
| Carries | name, notes, description, quantity, cost, weight | all of that plus rarity, type, modifiers, conditions, spells, charges |
| Costs | one form fill, one click | a page load, a form, then an edit page per subsystem |
| Name clashes | none - free text | clashes with official items, needs a `(Cradle)` suffix |

**Use a custom item** when the note records no mechanical effect: currency,
books, bulk gear, inert gems and crystals, ruined equipment, and anything still
`identified: false` (there is nothing to publish yet, but the party is carrying
it and it belongs in the list).

**Use homebrew** when the note gives the item a property that could come up at
the table - a save, a sense, a resistance, a weapon profile, charges, a spell.

### What not to put on D&D Beyond at all

- items the party no longer has (returned, left behind, sold) - the vault note
  is the record; an inventory row would be a lie
- items already present as a custom row someone else created - check the party
  list first and reconcile instead of duplicating

## Adding a custom item to Party Equipment

**Go through the Party Equipment-scoped panel.** This is the whole trick:

1. Inventory tab -> **PARTY INVENTORY** sub-tab -> **MANAGE INVENTORY**.
2. Scroll the panel to the **PARTY INVENTORY** heading and click
   **`+ Add items to your Party Equipment`**. The panel retitles itself
   *Party Equipment* and shows *Contents (n)*.
3. Expand **Add Custom Item**.

Scoped like this, **ADD ITEM has no caret and no destination menu** - it drops
the item straight into Party Equipment. One batch per item, no verification
click needed beyond the count.

> **Trap: in the UNSCOPED Manage Inventory panel, clicking the ADD ITEM button
> body silently discards everything you typed and creates a blank
> `Custom Item N` in the character's own Equipment.** Only the caret's
> destination menu submits the form. The caret moves as the button text grows
> (`ADD ITEM` -> `Add 11 Items`), so a fixed coordinate drifts onto the body.
> Avoid the whole problem by using the scoped panel above.

### Field coordinates (scoped panel, 1568-wide frame)

| Field | Coordinate |
|---|---|
| Cost Override | `(1180, 363)` |
| Weight Override | `(1237, 363)` |
| Name | `(1243, 382)` |
| Notes | `(1243, 400)` |
| Description | `(1204, 421)` |
| Quantity | `(1272, 458)` |
| ADD ITEM | `(1255, 478)` |
| Contents (n), to verify | zoom `[1155, 320, 1360, 560]` |

Triple-click Name and Quantity before typing - both are pre-filled. Everything
lands in one batch; two or three items per batch is comfortable.

**Cost Override is per unit.** `10` with quantity `219` shows as `2190 gp` on
the row. Set it only where the vault states a gold value per item.

**Notes vs Description.** Notes is one line and shows in the row; put the
provenance there (`Vault chest 14, Session 03. Drivik.`). Description carries
the vault's own text.

### Changing a quantity afterwards

Click the row in the inventory list. The right-hand detail pane has a Quantity
stepper: **triple-click the number, type the new one, press Tab**. The row
updates immediately. The same pane has **Customize** (name, notes, description),
**MOVE** (Equipment / Party Equipment / Bag of Devouring) and **DELETE**.

That MOVE is also the repair for anything that landed in the wrong bag.

### Two things that will waste your time

- **Never press Escape.** It closes the entire Manage Inventory panel and
  everything typed into the form is lost.
- **Screenshots time out on the character sheet** (`Page.captureScreenshot`
  after 30s) once the inventory is large. `zoom` on a small region usually still
  works, and `find` on the *Party Equipment count heading* reads the number out
  of the accessibility tree without any screenshot at all. Use that to verify.

## Adding a homebrew item to the party inventory

Same scoped panel as the custom items - Party Inventory sub-tab ->
MANAGE INVENTORY -> `+ Add items to your Party Equipment`. Then:

1. Click the **HOMEBREW** chip under *Filter By Source Category*.
2. Triple-click the Filter box and type a fragment that matches one item.
3. Click **ADD**. Scoped like this there is no destination menu.

| Control | Coordinate (1568-wide frame) |
|---|---|
| Filter box | `(1255, 188)` |
| HOMEBREW chip | `(1299, 301)` |
| ADD, single result | `(1324, 326)` |
| Contents (n), to verify | zoom `[1155, 240, 1360, 460]` |

> **The character sheet caches the homebrew list at page load.** An item created
> after the sheet was opened returns *No Results Found* no matter what you type.
> **Reload the sheet** after a batch of creations, then re-enter the panel.

**Triple-click the filter, never just click** - it keeps its previous text and
typing appends, producing searches like `crownCrown` that match nothing.

**Use a fragment that matches exactly one item**; extra rows push ADD down and
the fixed coordinate lands on the wrong one. `Lesser Growth`, not `Potion of
Growth`. `Prune`, `Vantablack`, `Extending` are each unique.

**Verify by *Contents (n)*, not the click** - the row still reads ADD either way.

## Sharing with the campaign — unresolved

**The user is a player in this campaign, not the DM.** The DM is `Zedicius`;
the campaign is *The Shadow*, `/campaigns/5164540`.

Checked and found no "share with campaign" control:

- the item's edit page — only Basic Information, Additional Information
  (charges, weight, avatar, tags), Modifiers, Conditions and Spells
- **My Creations** (`/my-creations`) — the only status axis is
  `Private, Never Submitted` ↔ **Published**, and publishing submits the item to
  D&D Beyond's *public* listing for moderation. That is publication, not
  campaign sharing, so do not use it to share with the group.
- the campaign page — the player view offers an invite link and the roster, no
  content-sharing controls

What does work: an item added to **Party Equipment** is visible to the campaign
there. Campaign-wide homebrew sharing appears to be a DM-side setting, so it may
need `Zedicius` to enable it. **Ask the user before trying anything else here**,
and never click Publish to achieve sharing.

## The campaign roster

From `/campaigns/5164540` — fuller than the vault's:

| Character | Player | Build |
|---|---|---|
| Vicaster Cloudwink | Zerdiox (the user) | Eladrin Warlock / Celestial Patron |
| Drivik | rogegijs | Gnome Rogue / Inquisitive |
| Aslaug Frostbane | JanWithAD | Halfling Bard / College of Whispers |
| Muradin Bugman | Cinnead | Dwarf Paladin / Oath of Devotion |
| Echo of Twilight | Mondy89682 | Tabaxi Druid / Circle of the Stars |
| Vraaxis | Zedicius (DM) | Lizardfolk Barbarian / Path of the Giant, level 6 |

## Other homebrew already on the account

Nine creations existed before this skill, all `Private, Never Submitted`:
Belt of Constitution, Bracers of Flux, Coin of the Double Bluff,
Jade Dragon Wistle, Pact Thread Cloak, Pendant of the Fractured Mind,
Ring of Lesser Spell Storing, and the spell Starlight of Aurorion.

Several appear in the party inventory alongside custom entries the vault has
never recorded — `firestarter marble` x6, `bag of boulders`,
`chest of preserving`, `dwergenkop met rune`, `Cervit wit` 80, `Cervit zwart` 10.

## Field reference

Every field on the create form, with the values it accepts. Write vault notes in
this vocabulary and publishing becomes pure transcription.

### Always shown

| Field | Required | Accepts |
|---|---|---|
| Name | yes | free text |
| Version | no | free text (`1`, `1.5`, `A`, `B`) |
| Rarity | yes | `Common`, `Uncommon`, `Rare`, `Very Rare`, `Legendary`, `Artifact`, `Varies`, **`Unknown Rarity`** |
| Base Item Type | yes | `Item` (default), `Armor`, `Weapon` |
| Requires Attunement | no | checkbox |
| Attunement Description | shows `*`, not enforced | free text |
| Description | yes | TinyMCE rich text |

### Shown by Base Item Type

Choosing the base type enables one branch and greys out the others.

**Base Item Type = `Item`** → **Magic Item Type** becomes required:
`Wondrous Item`, `Rod`, `Scroll`, `Staff`, `Wand`, `Ring`, `Potion`

**Base Item Type = `Weapon`** → **Base Weapon** becomes required, and Magic Item
Type greys out. The list is 200+ entries including many setting and third-party
weapons (Exandria, Grim Hollow, Obojima, magitech, firearms). The standard ones:

> Battleaxe · Blowgun · Club · Crossbow, Hand · Crossbow, Heavy · Crossbow,
> Light · Dagger · Dart · Flail · Glaive · Greataxe · Greatclub · Greatsword ·
> Halberd · Handaxe · Javelin · Lance · Light Hammer · Longbow · Longsword ·
> **Mace** · Maul · Morningstar · Net · Pike · Quarterstaff · Rapier · Scimitar ·
> Shortbow · Shortsword · Sickle · Sling · Spear · Trident · War Pick ·
> Warhammer · Whip

**Base Item Type = `Armor`** → **Base Armor** plus three armour-only fields:

- Base Armor: `Breastplate`, `Chain Mail`, `Chain Shirt`, `Half Plate`, `Hide`,
  `Leather`, `Padded`, `Plate`, `Ring Mail`, `Scale Mail`, `Shield`,
  `Spiked Armor`, `Splint`, `Studded Leather` (plus setting-specific ones)
- Dex Bonus: `Full Modifier`, `Max 2`, `None`
- Stealth Check: `None`, `Disadvantage`
- Str Requirement: free text

### Only on the edit page, after the item exists

**Additional Information** (collapsed by default — click the `+` to expand):
Has Charges, Number of Charges, Charge Reset Condition, Charge Reset
Description, Notes, Weight, Avatar, Large Avatar, Magic Item Tags.

**Modifiers**, **Conditions**, **Spells** — these drive character-sheet
integration. Optional, and only fill them from mechanics the vault records.

### Mapping from vault `item_type`

| Vault | Base Item Type | Then |
|---|---|---|
| `wondrous item` | Item | Magic Item Type = Wondrous Item |
| `potion` | Item | Magic Item Type = Potion |
| `scroll` | Item | Magic Item Type = Scroll |
| `ring` / `wand` / `staff` / `rod` | Item | matching Magic Item Type |
| `weapon` | Weapon | pick the Base Weapon (the vault note usually names it — "mace", "dagger") |
| `armor` | Armor | pick the Base Armor |
| `mundane` | Item | Wondrous Item, unless it is plainly a weapon or armour |

When writing a new item note, record the base weapon or armour by name in the
description so this step needs no guessing.

## Attaching mechanics: charges, spells, modifiers, conditions

Description text alone does nothing on a character sheet. An item with real
mechanics needs them attached, on the item's **edit** page after it exists.

**The sections start collapsed.** Each has a `+` on the right. The `ADD A ...`
buttons work without expanding, but you cannot see existing rows until you
expand. Click the `+` by coordinate; the section headers sit low on the page.

### Charges (Additional Information)

Expand **Additional Information** (`+` at roughly x 1136, y 242 at a 1568-wide
frame), then:

| Field | Notes |
|---|---|
| Has Charges | checkbox |
| Number of Charges | the item's capacity |
| Charge Reset Condition | `Short Rest`, `Long Rest`, `Dawn`, `Other`, **`None, Consumable`** |
| Charge Reset Description | free text |

Note the exact string is `None, Consumable` — *not* "None (Consumable)", which
`form_input` rejects. Use it for anything consumed permanently.

Then click **Save Changes** and re-expand the section to confirm the values
stored.

### Spells

**ADD A SPELL navigates to its own page**, `/magic-items/spell/create/<itemId>`.
It is not a modal, and nothing appears to happen on the edit page itself.

| Field | Notes |
|---|---|
| Spell Name | autocomplete. Type a fragment and pick from the list. It offers both `5.5e Core Rules` and `5e Core Rules (Legacy)` versions — **take the 5.5e one**, this table plays 2024 rules |
| Min - Max Spell Charges | **the cost per cast, not the item's capacity.** Same number in both when the spell cannot be scaled; a range when spending more charges casts it higher. Tooltip: *"enter the minimum and maximum number of spell charges it costs... Staff of Healing: Cure Wounds 1 \| 4; Lesser Restoration 2 \| 2"* |
| Save DC | leave blank unless the vault records one |
| Cast at Spell Level | offers the spell's own level upward (Evard's: 4-9) |
| Details | free text |

Save returns to the item edit page with `SPELLS (n)` and a row showing the spell,
its min and max charges, recovery type, save DC and restriction. Each row has
Edit (`/magic-items/spell/<spellRowId>/edit`) and Delete.

### What to attach, from the vault

Only what the notes actually record.

| Vault says | Attach |
|---|---|
| "casts <spell>, consumes one X per use" | Spell, Min-Max = `1 \| 1`; item charges = the number of X; reset `None, Consumable` |
| "+N weapon" | Modifier |
| "must succeed on a DC N save or be <condition>" | Condition, and the DC in the spell/modifier where it fits |
| a count of identical consumables (4 grenades) | **quantity in the inventory, not charges** |

### Conditions

`ADD A CONDITION` -> `/magic-items/condition/create/<itemId>`.

| Field | Accepts |
|---|---|
| Condition | Blinded, Charmed, Deafened, Exhaustion, Frightened, Grappled, Incapacitated, Invisible, Paralyzed, Petrified, Poisoned, Prone, Restrained, Stunned, Unconscious |
| Condition Duration | a number, **must be at least 1** |
| Duration Unit | Round, Minute, Hour, Day, Special, Until Dispelled |
| Details | free text - put the trigger and save DC here |

**Leaving the duration blank silently stores `0 Round`**, which reads as "for
zero rounds". When the notes give no duration, use `1` + `Special` and let the
Details carry the truth. A failed save re-renders the form and the dropdown refs
become DIVs - re-find them before retrying.

### Modifiers

`ADD A MODIFIER` -> `/modifier/create/<itemId>-112130694/0`. Note the entity
suffix; `/magic-items/modifier/create/<id>` is a 404.

> **Trap: Modifier Type and Subtype are custom dropdowns, not native selects.**
> `form_input` returns "Selected option Bonus" and changes nothing - the field
> still reads a dash. Click the control open, then click the option in the list.
> The subtype list has its own search box; type to filter, then click. Every
> other dropdown on the site is a real select, so this one is easy to miss.
> Always zoom and confirm both fields before saving.

Modifier types: Bonus, Damage, Advantage, Disadvantage, Resistance, Immunity,
Vulnerability, Sense, Set, Proficiency, Language, Expertise, Half Proficiency,
Feat, Carrying Capacity, Natural Weapon, Stealth Disadvantage, Speed Reduction,
Melee Weapon Attack, Ranged Weapon Attack, Weapon Property, Half Proficiency
Round Up, Favored Enemy, Ignore, Eldritch Blast, Replace Damage Type, Twice
Proficiency, Monk Weapon, Protection, Stacking Bonus, Set Base, Ignore Weapon
Property, Size, Weapon Mastery, Enable Feature, Replace Weapon Ability.

Other fields: Ability Score (CHA/CON/DEX/INT/STR/WIS), Dice Count, Die Type
(d4-d20), Fixed Value, Additional Bonus Types, Details, Duration Interval
(Round/Minute/Hour/Day), Requires Attunement.

**A +N magic weapon is one modifier, not two:** Type `Bonus`, Subtype `Magic`,
Fixed Value `N`. The `Magic` subtype covers attack and damage together.

**There is no crit-range modifier.** An expanded critical range ("crits on 19 or
20") has no mechanical equivalent - leave it in the description. The same goes
for pure flavour like "always aims for the head".

## Validate every change

The user asked for this explicitly. After every save, read the stored value back
- re-expand the section, or re-read the row - rather than trusting that the
click worked. When a field's meaning is not obvious, hover its `?` and read the
tooltip before filling it; that is how the Min-Max semantics above were settled.

## Already published

Party Equipment held 27 rows before any of this and holds **77** now.
Every item note carries the result in its `ddb` field: a URL for homebrew,
`custom item in Party Equipment` for a custom row, or `n/a - <reason>`.
`vault.py ls --type item --where 'ddb='` should return nothing.

### Homebrew magic items (24)

| Item | id | Attached |
|---|---|---|
| Crown of Fear | 12140241 | Frightened condition |
| Headhunter's Mace | 12140288 | Bonus/Magic +5 |
| Heartseeker Dagger | 12140290 | Bonus/Magic +2 |
| Mud Grenades | 12140296 | - |
| Tornado Prisms | 12140299 | - |
| Chain of 24 Links | 12140346 | Evard's Black Tentacles, 24 charges, consumable |
| Clay Mapmaker | 12140441 | - |
| Bottled Silver Tear | 12140443 | - |
| Potion of Growth (Cradle) | 12140447 | - |
| Potion of Lesser Growth | 12140451 | - |
| Potion of Stopped Time | 12140452 | - |
| Potion of Etherealness (Cradle) | 12140454 | - |
| Potion of Shielding | 12140461 | - |
| Potion of the Extra Action | 12140467 | - |
| Potion of Invulnerability (Cradle) | 12140472 | - |
| Potion of Reversed Gravity | 12140473 | - |
| Potion of Phasing | 12140476 | - |
| Poison Vial (Cradle) | 12140478 | quantity 10 |
| Radiant Gemstone | 12141703 | Wisdom check to look away, in the description |
| Red Lanterns | 12141704 | - |
| Vantablack Coin | 12141705 | - |
| White Pearl (Cradle) | 12141707 | - |
| Wrinkled Prune | 12141708 | - |
| Extending Halberd | 12141709 | Base Weapon Halberd |

Names carrying `(Cradle)` were suffixed because an official item of that name
already exists; the vault keeps the plain name and records the D&D Beyond one
in `ddb_name`.

### Custom rows in Party Equipment (26)

No homebrew entry - none of these has a mechanical effect. Quantity in
brackets; `(Armoury)` suffixes avoid confusion with the official items.

Acidic Emeralds (3), Black Resin (1), Claw Knives (1), Climbing Pickaxes (1), Crossbow Bolts (Armoury) (1), Crossbow Snares (1), Crossbows (Armoury) (1), Disease Books (2), Fire Crystals (4), Flame Streamers (11), Golden Beans (219), Interplanar Bank Notes (258), Loathsome Garnet (1), Mavemaren Bank Notes (1), Metal Scrolls (4), Planar Travel Book (1), Platinum Strips (120), Poison Books (3), Prismatic Keys (2), Restless Crystals (5), Rusted Gas Masks (1), Silver Tongue (1), Smoke Fabric (6), Stone Disc (1), The Black Book (1), Ways to Fly Easier (1).

### Deliberately not on D&D Beyond (5)

| Item | Why |
|---|---|
| Milky Heart Crystal | returned to the Crystal Sisters in Session 04 |
| Green Sword | left behind in the Puddle |
| Toga Sculpture | left in the Art Store |
| White Cervit | already a custom row, `Cervit wit` 80 |
| Black Cervit | already a custom row, `Cervit zwart` 10 |

Pre-existing custom rows nobody has reconciled with the vault:
`firestarter marble` x6, `bag of boulders`, `chest of preserving`,
`dwergenkop met rune`, `Koper bal met knop`, `Avatar leftover`.

## Driving the sheet with Playwright MCP

Prefer this to the coordinate tables above. Playwright MCP runs with
`--extension`, so it attaches to the user's real signed-in Chrome, and reading
the inventory from the DOM avoids the screenshot timeouts entirely.

Step-by-step recipes and the full selector table live in
**[references/playwright-recipes.md](references/playwright-recipes.md)**.
Read that before any inventory work. The coordinates above remain only as a
fallback if the selectors ever break.
