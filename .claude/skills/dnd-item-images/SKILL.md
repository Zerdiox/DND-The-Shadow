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

1. Read the item note: `python .claude/tools/vault.py get "<item>"`.
2. Build the prompt (see below).
3. Generate in Gemini: tools menu → **Create image**.
4. Show the user before downloading anything. Downloading is a real change to
   their disk and a wasted generation is cheaper than an unwanted file.
5. Save to `images/items/<slug>.png`, commit, push.
6. Use the resulting `raw.githubusercontent.com` URL for the D&D Beyond avatar
   and the archive page.

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

### The template

Two blocks. The house style block is **identical for every item** — copy it,
do not retype it. Twenty-four images that each look lovely on their own and
nothing like each other are worse than twenty-four plainer ones that read as a
set, and the set is the point: these sit side by side on the archive page and
in a single D&D Beyond inventory.

```
Create an image of <SUBJECT>, <MATERIAL AND CONDITION DETAIL>.

<ONE LINE ON WHERE IT WAS FOUND OR WHAT IT DOES, if the note gives one>

Style: a single object photographed as an archaeological catalogue plate,
recovered from a buried research facility. Centred on a plain desaturated
grey-green stone background. Low raking lamplight from the upper left, one soft
shadow beneath. Square framing, the object filling about two thirds of the
frame. Photographic realism with fine surface texture — corroded bronze, pitted
iron, salt crust, damp stone. Muted cold palette. No text, no border, no hands,
no people.
```

### Why that style and not another

It is derived from the campaign rather than chosen for looks, which is what
keeps it consistent as new items arrive. See `references/house-style.md` for
the full derivation and the palette values; the short version:

- **The setting is not high fantasy.** Sessions 01-06 run from a flooded dam
  full of dead Lemurian engineers down into the Cradle, a buried facility built
  to study deadly things. The recurring materials are bronze, iron, salt,
  crystal, resin, dried coral and damp stone — corroded and abandoned, not
  gleaming. "Archaeological catalogue plate" is the register the loot actually
  lives in.
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
| `magical: false` | no glow, no runes, no aura |
| `identified: false` | describe only what was observed, nothing about effects |

**The honesty rule matters more here than anywhere.** Most of this hoard is
inert — acidic emeralds, a stone disc, fabric — and the user corrects
over-reading briskly. An image that gives a mundane object a magical glow is
the same failure as writing an invented mechanic into its note, except harder
to notice later. If `magical` is `false` or `unknown`, the image shows an
ordinary object. If the item is unidentified, the picture shows what the party
saw and nothing more.

### A worked example

`Crown of Fear` — wondrous item, magical, carried by Vicaster.

```
Create an image of a dark iron crown, its band uneven and hand-beaten, the
points rising at irregular heights like something made in a hurry.

It was found in a vault and worn once; wearing it pushed everyone nearby into
fear until it was removed.

Style: a single object photographed as a museum catalogue plate. Centred on a
plain dark stone-grey background, soft directional light from upper left, one
soft shadow beneath. Square framing, the object filling about two thirds of the
frame. Photographic realism, fine surface texture, no text, no border, no hands,
no people.
```

Contrast with `Stone Disc`, which is `magical: false` and unremarkable: same
style block, and a subject line that says only what it is — a plain worked
stone disc, chipped at one edge. No glow, no carving the note does not mention.

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
