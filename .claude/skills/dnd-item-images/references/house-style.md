# House style for item images

Why the style block in `SKILL.md` says what it says, and what to hold constant
when extending it. The aim is that an item illustrated a year from now still
belongs beside one illustrated today.

## Derived from the campaign, not chosen for looks

Sessions 01-06 run from a flooded dam down into the Cradle — a buried facility
built to study dangerous things, long abandoned. Nothing about it is castles
and banners. The recurring physical vocabulary across the session notes is:

| Where | Materials and surfaces |
|---|---|
| The Dam | stone sarcophagi, sealed iron pots, a ship sarcophagus, carved plates and symbols |
| The Vault | chests of hoarded goods, platinum strips, golden beans, acidic emeralds |
| Cervit Storage | white and black Cervit — a resin- or glass-like alloy, in crates |
| The Strata Gallery | cut geological blocks, brick, flecked and bladed stone |
| The Crystal Hall | salt crust, crystal |
| The Shell Room | clam and spiral shells, crab shells, dried coral — a sea floor indoors |
| The Art Store | crated sculpture, a woman in a toga in worked stone |
| The Tool Storage | hammers, chisels, implements nobody can identify |
| The Spider Chamber | a bronze-and-iron construct, a block of ice, wall hieroglyphs |
| The Armoury | ten iron chests, crossbows, claw knives, climbing pickaxes, red-lensed lanterns, rusted gas masks |
| The Alchemy Hall | benches of dried-out glassware, sealed vials, project books |
| The Astral Chamber | a crystalline structure on chains, white fluid, overflowed flasks |

So: **bronze, iron, salt, crystal, resin, coral, damp stone** — corroded,
crusted and abandoned. Objects photographed as recovered artefacts read true.
Objects photographed as gleaming treasure do not.

The party is underground with lanterns throughout, which is where the low
raking lamplight comes from. Flat studio light would be wrong for the same
reason.

## Palette, taken from the archive page

The group-facing archive already has a design system, and images that ignore it
will fight the page they are embedded in. Its tokens:

| Role | Light | Dark |
|---|---|---|
| ground | `#E6E9E4` | `#0E1413` |
| surface | `#F3F5F1` | `#161E1D` |
| surface-2 | `#DDE2DB` | `#202B29` |
| ink | `#151C1A` | `#E2E8E4` |
| rule | `#C4CCC3` | `#2A3634` |
| patina (verdigris) | `#2C6B66` | `#5FB3AB` |
| garnet | `#8E2F3C` | `#D8707F` |
| gold | `#94682A` | `#D2A254` |
| glass | `#4A7F86` | `#74B6BE` |
| poison | `#3F7A2E` | `#8FCB6A` |

A desaturated grey-green ground with verdigris, garnet, antique gold and a
poison green. The image background should sit near `surface-2` so it reads on
both the light and dark versions of the page without a hard edge.

The page's type is Bodoni Moda for headings, Karla for body, IBM Plex Mono for
labels — relevant only if a composite or banner image is ever made. Individual
item plates carry no text at all, which is also why the prompt says "no text":
generated lettering is usually malformed, and the page supplies the captions.

## What stays fixed, and what varies

Fixed for every item — changing any of these breaks the set:

- object alone, centred, filling about two thirds of a square frame
- plain desaturated grey-green stone background, no scene, no props
- low raking lamplight from the upper left, one soft shadow beneath
- photographic realism with visible surface texture
- no text, no border, no hands, no people

Varies per item: the subject, its materials and its condition. That is all.

## The trap

The palette describes **lighting and background**, not permission to decorate.
An item note that says `magical: false` gets no glow; one that says nothing
about gold gets no gold. Most of this hoard is inert — the user corrects
over-reading briskly, and an invented verdigris patina is the same class of
error as an invented mechanic, just harder to spot later.

For an `identified: false` item, illustrate only what the party observed. The
Green Sword, the Prismatic Keys and the Silver Tongue are all in that state:
describe the object, never the effect.
