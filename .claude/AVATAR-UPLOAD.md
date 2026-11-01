# Uploading the item avatars by hand

Twelve illustrations are finished and committed. They cannot be attached to
D&D Beyond from here — the avatar fields take an uploaded file, and the
Playwright extension bridge refuses to feed local files into a page
(`DOM.setFileInputFiles` → `Not allowed`). The reasoning is in
`skills/dndbeyond-homebrew/references/playwright-recipes.md`.

So it is a dozen manual uploads. For each row: open the edit link, scroll to
**Additional Information**, and set **Avatar** to the file. There is a second
field, **Large Avatar**; the same file works for both.

The files are in `images/items/` at the vault root.

| Item on D&D Beyond | File | Edit page |
|---|---|---|
| Crown of Fear | `crown-of-fear.png` | [edit](https://www.dndbeyond.com/homebrew/creations/magic-items/12140241-crown-of-fear/edit) |
| Headhunter's Mace | `headhunters-mace.png` | [edit](https://www.dndbeyond.com/homebrew/creations/magic-items/12140288-headhunters-mace/edit) |
| Poison Vial (Cradle) | `poison-vials.png` | [edit](https://www.dndbeyond.com/homebrew/creations/magic-items/12140478-poison-vial-cradle/edit) |
| Potion of Etherealness (Cradle) | `potion-of-etherealness.png` | [edit](https://www.dndbeyond.com/homebrew/creations/magic-items/12140454-potion-of-etherealness-cradle/edit) |
| Potion of Growth (Cradle) | `potion-of-growth.png` | [edit](https://www.dndbeyond.com/homebrew/creations/magic-items/12140447-potion-of-growth-cradle/edit) |
| Potion of Invulnerability (Cradle) | `potion-of-invulnerability.png` | [edit](https://www.dndbeyond.com/homebrew/creations/magic-items/12140472-potion-of-invulnerability-cradle/edit) |
| Potion of Lesser Growth | `potion-of-lesser-growth.png` | [edit](https://www.dndbeyond.com/homebrew/creations/magic-items/12140451-potion-of-lesser-growth/edit) |
| Potion of Phasing | `potion-of-phasing.png` | [edit](https://www.dndbeyond.com/homebrew/creations/magic-items/12140476-potion-of-phasing/edit) |
| Potion of Reversed Gravity | `potion-of-reversed-gravity.png` | [edit](https://www.dndbeyond.com/homebrew/creations/magic-items/12140473-potion-of-reversed-gravity/edit) |
| Potion of Shielding | `potion-of-shielding.png` | [edit](https://www.dndbeyond.com/homebrew/creations/magic-items/12140461-potion-of-shielding/edit) |
| Potion of Stopped Time | `potion-of-stopped-time.png` | [edit](https://www.dndbeyond.com/homebrew/creations/magic-items/12140452-potion-of-stopped-time/edit) |
| Potion of the Extra Action | `potion-of-the-extra-action.png` | [edit](https://www.dndbeyond.com/homebrew/creations/magic-items/12140467-potion-of-the-extra-action/edit) |

Delete this file once the uploads are done.
