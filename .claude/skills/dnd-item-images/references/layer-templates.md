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

## Layer 2 — `RoomContext` (one implementation per room)

**Supplies:** at most one clause, saying where the object has been.

**Never supplies:** another room's materials, or motifs from the room's
architecture grafted onto the object. The Throne Room has a serpent relief on
its wall; that does not put serpents on the crown.

**Most items do not need this layer at all.** It is optional, and there is no
need for a clause per room — only a handful of rooms leave any trace on what
was in them.

**The test:** could someone holding the object tell it came from there? A pool
of oily, very salty water marks a thing that sat in it. A chest does not; a
shelf does not; a crate does not. If the room only describes where the object
was *stored*, omit layer 2 entirely and go straight from the item to the fixed
block. A prompt without it is not missing anything.

**Rooms that earn a clause:**

| Room | Clause | Why it earns one |
|---|---|---|
| The Puddle | `Recovered from beneath an oily, intensely salty pool.` | the *water* is oily and very salty, so anything submerged in it would show residue |
| Alchemy Hall | `Found among alchemical benches of glassware dried out and gone gooey.` | the dried residue is everywhere, and most finds here are vessels |
| Astral Chamber | `From beneath a chained astral being, whose white blood has long overflowed its flasks.` | anything on that table has been dripped on for centuries |
| Throne Room | `One of a matched set of regalia — throne, mace and crown — made as ornamental work.` | not a mark but a design fact: it was made to match two other objects |

**The salt is in the water, not the room.** The tunnel itself is unremarkable;
it is the pool that is oily and intensely salty. So the clause applies only to
the three things that lay submerged in it — the Green Sword, the Silver Tongue
and the Screaming Baby — and not to anything merely carried through. That
precision is the whole point of the layer: it marks objects that were actually
in contact with something, rather than tinting everything from a postcode.

Everything else — the Vault's twenty chests, the Armoury's iron chests and bare
racks, the Library's geology shelves, the Art Store's crates, the Spider
Chamber, Cervit Storage — is storage. Interesting to read, invisible on the
object. Skip it.

Adding a room later: read its note in `03-Locations/`, apply the test, and only
write a clause if it passes. Do not invent detail the note lacks, and do not
add a room just for completeness.

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

One of a matched set of regalia — throne, mace and crown — made as ornamental
work.

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
