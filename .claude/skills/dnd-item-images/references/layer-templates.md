# Layer templates

Think of each layer as an interface. It declares what it must supply and what
it must never supply; a room or an item is an implementation of it. Prompts are
then assembled rather than composed, which is what keeps the set coherent as it
grows.

Compose outermost-in, but write the prompt innermost-first: **layer 3, then
layer 2, then the fixed 0+1 block verbatim at the end.**

---

## Layer 0 — `World` (constant)

**Supplies:** that this is D&D. A fantasy world, pre-modern craft, objects
forged, cast, carved, blown, woven or hand-worked.

**Never supplies:** machining, moulding, printed labels, plastics, screws,
contemporary industrial design. "Very old" means ancient craft, not a disused
twentieth-century plant.

## Layer 1 — `Site` (constant)

**Supplies:** the Cradle — a vast, very old buried building made to study
deadly things, eldritch and wrong as much as abandoned. The presentation
convention too: object alone, catalogue plate, weathered grey-green stone,
raking lamplight, 1:1.

**Never supplies:** anything about a specific room, or the object's condition.

**Implementation** — layers 0 and 1 together, copied verbatim into every
prompt:

```
Style: a single object from a high-fantasy world, made by pre-modern hands —
forged, cast or carved, with nothing machined or modern about it. Photographed
now as an archaeological catalogue plate: recovered from the Cradle, a vast and
very old buried place, eldritch and wrong as much as it is abandoned. Centred
on weathered grey-green stone. Low raking lamplight from the upper left, one
soft shadow beneath. The object fills about two thirds of the frame.
Photographic realism with fine surface texture. Muted cold palette. No text, no
border, no hands, no people.
```

## Layer 2 — `RoomContext` (optional, and the riskiest layer)

**Supplies:** at most one short phrase describing a mark on the object's own
surface, or its workmanship.

**Never supplies:** the room, the scene, water, furniture, other objects,
lighting or background. Layer 1 owns all of that. If a phrase could be read as
*put this in the picture*, it is written wrongly.

### Write it as a property, never as a provenance

This is the whole discipline of the layer, and getting it wrong does real
damage. "Recovered from beneath an oily, intensely salty pool" invites a pool
into the frame, wets the stone, and changes the light — layer 2 silently
overriding layer 1. "A faint salt bloom on its surface" cannot: it describes
the object and nothing else.

Provenance belongs in the note. Only the residue belongs in the prompt.

### Most items need no layer 2 at all

**The test:** could someone holding the object tell it came from there? A pool
of oily, salty water marks a thing that sat in it. A chest does not; a shelf
does not; a crate does not. If the room only says where the object was
*stored*, omit the layer and go straight from the item to the fixed block. A
prompt without it is missing nothing.

When in doubt, leave it out. An image that is slightly generic is recoverable;
one with a room's scenery baked into it is not, and it will not match the set.

### Rooms that earn a phrase

| Room | Phrase | Why it earns one |
|---|---|---|
| The Puddle | `A faint whitish salt bloom and a slight oily sheen on its surface.` | the *water* was oily and very salty; anything submerged would carry residue |
| Alchemy Hall | `Traces of dried, gummy alchemical residue in its crevices.` | the dried-out residue is over everything there |
| Astral Chamber | `Faint chalky white spotting where liquid dripped onto it over a long time.` | anything on that table was dripped on for centuries |
| Throne Room | `Ornamental regalia workmanship, of a piece with a throne and a mace.` | not a mark but a design fact: it was made to match two other objects |

Note what each one is: a surface, or a style of making. None names a room, and
none would survive being read as a scene instruction.

**The salt is in the water, not the room.** The tunnel itself is unremarkable.
So the phrase applies only to the three things that lay submerged in it — the
Green Sword, the Silver Tongue and the Screaming Baby — and not to anything
carried through. That is the layer marking objects that were actually in
contact with something, rather than tinting everything by postcode.

Everything else — the Vault's twenty chests, the Armoury's iron chests and
bare racks, the Library's geology shelves, the Art Store's crates, the Spider
Chamber, Cervit Storage — is storage. Interesting to read, invisible on the
object. Skip it.

Adding a room later: read its note in `03-Locations/`, apply the test, and
write a phrase only if it passes — as a surface or a workmanship, never as a
place. Do not invent detail the note lacks, and do not add a room for
completeness.

## Layer 3 — `Item` (one per note)

**Supplies:** the subject noun, its materials as the note gives them, and a
condition line.

**Never supplies:** materials the note does not state, effects for an
`identified: false` item, mechanical properties that are not visible, or a glow
that no note records.

**Implementation:**

```
Create an image of <SUBJECT>, <MATERIAL DETAIL from the note>.

<CONDITION — by `magical`, below>
```

| `magical` | Condition clause |
|---|---|
| `true` | `The object itself is pristine and undimmed — no corrosion, no tarnish, no wear, crisp sharp detail, in contrast with the weathered stone it rests on.` |
| `false` / `unknown` | `The object is aged and worn as found — tarnish, corrosion and pitting from long burial.` |

Magical items do not age in D&D; that is a rule of the setting, so this clause
is not optional and not a matter of taste. Pristine is not glowing.

---

## Worked assembly

`Crown of Fear` — `magical: true`, found in the Throne Room.

```
Create an image of an ornamental crown, its decoration fine and clearly
deliberate work.

The object itself is pristine and undimmed — no corrosion, no tarnish, no wear,
crisp sharp detail, in contrast with the weathered stone it rests on.

Ornamental regalia workmanship, of a piece with a throne and a mace.

Style: a single object from a high-fantasy world, made by pre-modern hands —
forged, cast or carved, with nothing machined or modern about it. Photographed
now as an archaeological catalogue plate: recovered from the Cradle, a vast and
very old buried place, eldritch and wrong as much as it is abandoned. Centred
on weathered grey-green stone. Low raking lamplight from the upper left, one
soft shadow beneath. The object fills about two thirds of the frame.
Photographic realism with fine surface texture. Muted cold palette. No text, no
border, no hands, no people.
```

Layer 3, layer 2, layers 0+1. Aspect ratio 1:1 set with the control.
