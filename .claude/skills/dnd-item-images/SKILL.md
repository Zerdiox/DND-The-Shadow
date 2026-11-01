---
name: dnd-item-images
description: >-
  Generate illustrations for this vault's items using Gemini in the user's own
  Chrome, then put them on D&D Beyond homebrew entries and the group-facing
  archive. Use this whenever the user wants art, an image, an illustration, a
  picture, an avatar or a thumbnail for an item, weapon, potion or piece of
  loot — and also when they ask to "make the homebrew look better", to
  illustrate the campaign archive, or to add visuals to anything in
  05-Items-Loot. Covers choosing the model, building the prompt from the item
  note, keeping 24 items looking like one set, and staying inside the free
  tier.
---

# Item images from Gemini

Images come from the **Gemini web app** driven through the user's signed-in
Chrome, not the API. The user has no billing enabled, and image generation is
charged per image on the API — the web app uses the free allowance that is
already sitting there. That constraint drives most of what follows.

Read `references/gemini-models.md` before the first generation of a session.
It records which models exist, what the app actually offers, and when that was
last checked — image models change every few months and the names in it will
go stale faster than this file will.

## The loop

1. Read the item note: `python .claude/tools/vault.py get "<item>"`, and the
   note of the room it was found in.
2. Assemble the prompt from the four layers.
3. **Ask before generating, not after.** Aim for one generation per item.
4. Generate at <https://gemini.google.com/images>, aspect ratio 1:1.
5. Show the user before downloading anything. Downloading is a real change to
   their disk, and a wasted generation is cheaper than an unwanted file.
6. Save to `images/items/<slug>.png`, commit, push.
7. Use the resulting `raw.githubusercontent.com` URL for the D&D Beyond avatar
   and the archive page.

### Step 3 in full: ask, do not iterate

Refining an image in four passes looks like craft and is mostly waste. Every
pass the Crown of Fear needed was a *rule* being discovered — magical items do
not age, fear reads red, cruelty reads jagged — and those are written down now.
They apply automatically to the next item.

What stays genuinely open per item is small, and the user can answer it in a
sentence:

- **What does it actually look like?** Most notes give one clause. "An
  ornamental crown" left the material, period and form to be guessed, and the
  first attempt guessed all three wrong. Asking "what's it made of?" cost one
  message and settled it.
- **Should its effect show, and how?** A recorded effect may shape the design,
  but how much is taste. Ask.
- **Is there anything from the room worth carrying over?** Only if the room
  earns it.

Put the assembled prompt in front of the user with those questions attached,
then generate once. A question costs nothing; a generation comes out of a
daily allowance nobody can see the size of.

When a correction does arrive, decide whether it is general or specific. "Fear
reads red" belongs in the skill; "this particular crown has a dent" belongs in
the note. Rules go in the skill so no item needs them discovered twice.

Because the repository is public, one committed file serves both destinations
and there is no second copy to keep in sync. That is the whole reason for
putting them in the repo rather than uploading separately to each place.

## Driving the Gemini UI

Verified working in the user's Chrome. Selectors and quirks:

| Target | How |
|---|---|
| Tools menu | `button[aria-label="Upload and tools"]` |
| Image mode | the **Create image** entry in that menu |
| Mode picker | `button[data-test-id="bard-mode-menu-button"]` |
| Generated images | the **Images** entry in the left sidebar |

Two things will waste your time:

- **`browser_click` times out on this UI.** The elements resolve and are
  visible and unobstructed, but Angular Material animates them continuously so
  Playwright's "stable" check never passes. Click via `browser_evaluate`
  instead: `document.querySelector(sel).click()`. This is not a workaround for
  a permission check, just for an animation.
- **The tools menu items are not `role="menuitem"`.** Reading the menu by that
  selector returns nothing even when it is open on screen. Take a screenshot if
  you need to see what is in it.

## Choosing the model

The app does not let you pick an image model by name — Google routes it. What
you *can* control is the conversation mode, via the mode picker: **Auto**,
**3.1 Pro**, **4 Argon**, each with a Low/Medium/High thinking level.

Reported, but not verified here: starting from a higher reasoning mode yields
Pro-quality images for the first couple of generations per day, after which the
account falls back to the standard image model. If that matters for a
particular item, spend the good generations on the showpieces — the Crown of
Fear, the Bottled Silver Tear — and let ordinary gear take the default.

Treat daily limits as unknown and variable. Google does not publish a fixed
number and third-party figures disagree wildly. Plan on a handful of items per
sitting, not a batch of twenty-four, and check `references/gemini-models.md`
for what was last observed.

## Building the prompt

Google's own guidance, which the template below follows:

- **Say it is an image.** Begin with "Create an image of". Without that intent
  signal the model may answer with text instead.
- **Be specific.** Name materials and details. "Fantasy armour" produces
  generic output; "pitted bronze greaves with verdigris in the engraving" does
  not.
- **Describe what you want, not what you don't.** Positive phrasing only.
  "Plain iron, no decoration" invites decoration.
- **Control the camera** with photographic terms — macro, three-quarter view,
  low angle.
- **Expect to iterate.** The first result is a draft. Follow-up messages in the
  same conversation refine it; starting over loses the thread.

### The template: four layers, narrowing

Build every prompt by cascading from the widest context to the narrowest:

| Layer | Scope | Varies? |
|---|---|---|
| 0 | It is D&D — fantasy, pre-modern, nothing machined | never |
| 1 | The Cradle — the buried building holding nearly all of it | never |
| 2 | The room inside the Cradle where this item was found | per item |
| 3 | The item itself, from its note | per item |

Each layer inherits from the one above and may refine it, never contradict it.
That is what keeps twenty-four images reading as one set while still letting
each object be itself — and it is also what stops one room's materials leaking
onto an object from another.

**Layer 0 — it is D&D.** The outermost frame, and the easiest to lose. This is
a fantasy world with no modern anything: objects are forged, cast, carved,
blown, woven or hand-worked. No machining, no injection moulding, no printed
labels, no plastics, no screws, no contemporary industrial design. "Very old"
here means pre-modern craft, not a disused twentieth-century plant.

Watch two words in the block below. *Photographed* and *catalogue plate*
describe how **we** are presenting the object now — a modern convention, and
the right one, because it is how the archive page lays loot out. They say
nothing about the object, which stays firmly pre-modern. And while the Cradle
was built for research, it is an ancient fantasy structure, not a laboratory;
if images start coming back looking like a bunker, that word is the culprit.

**Layer 1 — the Cradle.** Nearly everything was recovered from it: a vast
buried place, very old, built to study deadly things. Eldritch and wrong as
much as it is abandoned.

Layers 0 and 1 are identical for every item and live in one fixed block. Copy
it; never retype it.

```
Style: a single object from a high-fantasy world, made by pre-modern hands in
the tradition of a long-lost classical civilisation — hand-forged, cast and
carved. Painted as a fantasy roleplaying rulebook item illustration: a digital
painting with visible brushwork, confident edges and painterly texture
throughout. Laid out as a catalogue plate — the object alone, centred on
weathered grey-green stone, filling about two thirds of the frame. Low raking
lamplight from the upper left, one soft shadow beneath. Muted cold palette. A
clean, unlettered plate.
```

Say **the Cradle**, not "the vault". `03-Locations/Vault.md` is one specific
room — the chamber above the Library with twenty chests — and most loot did not
come from it. `The Cradle` is the `region` on the location notes and the right
name for the whole place.

**Layer 2 — the room. Optional, and the riskiest layer.** Most items need none
at all.

Where it applies it is **one short phrase about a mark on the object's own
surface**, never a description of the room. "Recovered from beneath an oily,
salty pool" invites a pool into the frame and wets the stone, overriding layer
1; "a faint salt bloom on its surface" cannot. Provenance belongs in the note;
only the residue belongs in the prompt.

The test: could someone holding the object tell where it came from? Chests,
shelves and crates say where a thing was stored and leave no trace, so they
earn nothing. Four rooms earn a phrase; the rest are skipped. When in doubt,
leave it out — a slightly generic image is recoverable, one with a room baked
into it is not.

`references/layer-templates.md` has the four phrases and the rule for adding
more.

**Layer 3 — the item.**

```
Create an image of <SUBJECT>, <MATERIAL DETAIL from the note>.

<CONDITION LINE — chosen by `magical`, see below>

<ONE CLAUSE OF ROOM CONTEXT from layer 2, if the note places it>
```

Then set the aspect ratio to **1:1** with the control in the composer rather
than asking for square framing in words — it is a real setting, and words are
a guess.

Assemble as: layer 3, then layer 2's clause, then the fixed layer 0+1 block
verbatim at the end.

### The condition line is not optional, and it depends on `magical`

In D&D, **magical items do not age or wear.** Centuries underground leave them
exactly as they were made. That is a rule of the setting, not a stylistic
preference, so an item's `magical` value decides how it is depicted:

| `magical` | Condition line |
|---|---|
| `true` | `The object itself is pristine and undimmed — no corrosion, no tarnish, no wear, crisp sharp detail, in contrast with the weathered stone it rests on.` |
| `false` or `unknown` | `The object is aged and worn as found — tarnish, corrosion and pitting from long burial.` |

This gives the set its logic: everything in the Cradle has been rotting for
centuries except the things that cannot. A magical item that looks excavated is
wrong in the same way an invented mechanic is wrong.

**Pristine is not the same as glowing.** A magical item is undamaged; it is not
luminous, radiant or wreathed in energy unless its note says something visible.
The Crown of Fear is flawless *and* inert-looking. Both rules apply at once.

### Why that style and not another

It is derived from the campaign rather than chosen for looks, which is what
keeps it consistent as new items arrive. See `references/house-style.md` for
the full derivation and the palette values; the short version:

- **The setting is not high fantasy.** Sessions 01-06 run from a flooded dam
  full of dead Lemurian engineers down into the Cradle, a buried facility built
  to study deadly things. The recurring materials are bronze, iron, salt,
  crystal, resin, dried coral and damp stone — corroded and abandoned, not
  gleaming. "Archaeological catalogue plate" is the register the loot actually
  lives in. That describes the *place*, though: which of those materials apply
  to a given item depends on the room it was found in, and whether the item
  itself looks decayed depends on `magical`. Both rules are above.
- **Lamplight, because that is how the party sees anything.** They are
  underground with lanterns the whole way down.
- **The palette matches the archive page**, which already uses a desaturated
  grey-green ground with verdigris, garnet and antique gold accents. Images
  generated to a different palette would fight the page they are embedded in.
- **Catalogue framing matches the page's existing structure** — it lays loot
  out as relic cards and exhibit placards, so object-on-plain-ground is the
  shape it is expecting.

One caution that follows from the honesty rule: the palette describes the
*lighting and background*, not licence to add verdigris or gold to an object
that has none. A plain iron spike stays plain.

### Filling the subject from the note

| Note field | Use |
|---|---|
| filename | the subject noun |
| `## Description` | material, colour, condition — the bulk of the subject line |
| `## Properties` | the one functional line, only if it would be *visible* |
| `item_type` | shapes the framing: a potion is a vessel, a weapon lies flat |
| `found` + the body | **the room it came from** — and only that room's character |
| `magical: true` | pristine, unaged — see the condition rule above |
| `magical: false` | aged as found, and no glow, no runes, no aura |
| `identified: false` | describe only what was observed, nothing about effects |

**Be mindful of where the item was found.** The campaign's materials are
room-specific: salt in the Crystal Hall, shells and coral in the Shell Room,
crated art in the Art Store, bronze and ice in the Spider Chamber. Read the
note's `found` field and its body, use that room, and leave the rest alone.
`references/house-style.md` has the per-room table.

**The honesty rule matters more here than anywhere.** Most of this hoard is
inert — acidic emeralds, a stone disc, fabric — and the user corrects
over-reading briskly. An image that gives a mundane object a magical glow is
the same failure as writing an invented mechanic into its note, except harder
to notice later. If `magical` is `false` or `unknown`, the image shows an
ordinary object. If the item is unidentified, the picture shows what the party
saw and nothing more.

### A worked example

`Crown of Fear` — wondrous item, magical, identified, carried by Vicaster. Its
note gives exactly one sentence of appearance: *"An ornamental crown recovered
from the Throne Room."* That is the whole of what can be depicted honestly.

Layer 2 comes from `03-Locations/Throne Room.md`, which the note links: a
chamber holding an ornamental throne, mace and crown, with an unidentified
serpent relief along the wall. So the crown is one of a matched set of
ornamental regalia — that is real context, and worth a clause.

```
Create an image of an ornamental crown, its decoration fine and clearly
deliberate work.

The object itself is pristine and undimmed — no corrosion, no tarnish, no wear,
crisp sharp detail, in contrast with the weathered stone it rests on.

Ornamental regalia workmanship, of a piece with a throne and a mace.

Style: a single object from a high-fantasy world, made by pre-modern hands in
the tradition of a long-lost classical civilisation — hand-forged, cast and
carved. Painted as a fantasy roleplaying rulebook item illustration: a digital
painting with visible brushwork, confident edges and painterly texture
throughout. Laid out as a catalogue plate — the object alone, centred on
weathered grey-green stone, filling about two thirds of the frame. Low raking
lamplight from the upper left, one soft shadow beneath. Muted cold palette. A
clean, unlettered plate.
```

Aspect ratio 1:1, set with the control.

The serpent relief is deliberately **not** in there. It is on the room's wall,
not on the crown, and nothing says the motif carries over. That is the layer-2
discipline in miniature: the room supplies context, not decoration to graft on.

Note what is **absent**, and why:

- **No metal is named.** The note does not say what it is made of, so neither
  does the prompt.
- **No ageing, because `magical: true`.** This is the correction that matters
  most: a first attempt described it as "old and tarnished" and produced a
  heavily corroded crown, which is simply wrong for the setting.
- **No glow either.** The note records enchantment magic detected by an arcana
  check, not anything visible. Pristine, not luminous.
- **No salt, coral or shells.** Those materials belong to specific rooms — the
  Crystal Hall, the Shell Room — not to every object in the vault. A crown from
  the Throne Room has nothing to do with them.
- **The mechanical effect is omitted.** "Everyone who sees the wearer is
  frightened" is not a visual property of the object, and feeding it in invites
  skulls and menace the crown does not have.

Contrast with `Stone Disc`, which is `magical: false` and unremarkable: same
style block, and a subject line that says only what it is — a plain worked
stone disc, chipped at one edge. No glow, no carving the note does not mention.

The pull towards embellishment is strong here, because a restrained prompt
feels like a worse prompt. It is not. The vault is the source of truth and an
invented crown is an invented fact.

## Reading the item's effect into how it looks

The honesty rule bars **inventing facts**. It does not bar using facts the
vault already records to decide how a thing looks — and an early draft of this
skill got that wrong, excluding the Crown of Fear's fear effect as "not
visible" and producing pleasant museum goldwork for an object that terrifies
anyone who sees it worn.

An object made to do something generally looks like it. If a note records an
effect, let it shape the design:

- **The effect is a design brief, not decoration.** "Frightens onlookers" does
  not mean add skulls; it means the whole piece should be uncomfortable to
  look at — cruel proportions, predatory forms.
- **Motifs from the room can carry over.** The Throne Room has a serpent
  relief along its wall and the crown was made as part of a matched set with
  the throne. Working serpents into the crown's band is reading the room, not
  inventing.
- **"Too nice" is a real failure.** If an item's note says it does something
  awful and the image is merely handsome, the image is wrong.

This is where the vault stops deciding and taste begins, so it is the part to
check with the user rather than settle alone.

### The user's visual vocabulary

Established while making the Crown of Fear. These are conventions for this
campaign, so the set stays legible:

| Reads as | Rendered as |
|---|---|
| fear, menace | **deep garnet red** — dark blood red, never bright ruby |
| evil, cruelty | **jagged and angular** — shards, facets, uneven spines, never smooth domes or round cabochons |

Garnet is already in the archive page's palette, so red accents sit inside the
design system rather than fighting it. Keep red the only warm colour in an
otherwise cold frame and it reads as the source of the menace.

Add to this table as more items establish more conventions. Ask rather than
guess at a new one.

## Iterate in the thread, one change at a time

Refine in the same Gemini conversation rather than starting over. A fresh
prompt loses everything that was already right; a follow-up keeps it. State
what to preserve explicitly — "keep the gold, the serpents, the stone, the
lighting and the framing" — then make one change.

The Crown of Fear took four passes, and the sequence is worth knowing because
each step fixed exactly one thing:

1. *old and tarnished* → a corroded Gothic crown. **Wrong**: magical items do
   not age, and the Gothic form was the model's default, not the setting's.
2. gold, classical banded diadem, pristine → right materials and period, but
   pleasant and inert.
3. serpents in the band, unsettling → the room's motif carried over, and a
   serpent relief appeared in the background of its own accord.
4. garnet-red angular stones, jagged crest → menace, finally legible.

Starting over at step 3 would have lost the classical form won at step 2.

## After generating

Save as `images/items/<kebab-case-name>.png`. Commit with the item it belongs
to named in the message, so the image and the note stay traceable to each
other.

Then record it on the note so a later session knows the item has art:

```bash
python .claude/tools/vault.py set "Crown of Fear" image "images/items/crown-of-fear.png"
```

`image` is a new optional key. `vault.py lint` accepts unknown optional keys,
but confirm with `lint` after the first one rather than assuming.

For the D&D Beyond avatar, the item's edit page has an avatar field under
Additional Information — see the homebrew skill, and
`references/playwright-recipes.md` beside it for driving that site.

## Validate

Read back, as everywhere in this vault:

- Look at the downloaded file before committing it. A generation that failed or
  returned the wrong subject looks identical to a successful one from the file
  name alone.
- After setting `image`, re-read the frontmatter.
- After attaching an avatar on D&D Beyond, reload the item page and confirm it
  renders.
