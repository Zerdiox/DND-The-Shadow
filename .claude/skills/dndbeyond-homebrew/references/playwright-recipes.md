# Driving the D&D Beyond character sheet with Playwright MCP

Step-by-step recipes for the party inventory. Playwright MCP is configured with
`--extension`, so it attaches to the user's real signed-in Chrome — the same
session Claude in Chrome would use. Reading the inventory out of the DOM avoids
the screenshot timeouts the sheet suffers once the inventory is large.

Character sheet: `https://www.dndbeyond.com/characters/147071691`

**Status of each recipe** — be honest about this when relying on them:

| Recipe | Verified |
|---|---|
| 1. Open the party inventory | end to end, 31 Oct 2026 |
| 2. Read the whole inventory | end to end, 31 Oct 2026 |
| 3. Edit or rename a row | end to end, 31 Oct 2026 |
| 4. Add a custom item | selectors mapped; **add not executed** |
| 5. Add a homebrew item | selectors mapped; **add not executed** |

Recipes 4 and 5 have had every control located and labelled, but the final
ADD click has never been performed through them. Treat the last step as
unproven and verify by the `Contents (n)` count.

---

## 1. Open the party inventory

```
browser_navigate   https://www.dndbeyond.com/characters/147071691
browser_wait_for   time: 4
browser_click      button[data-testid="EQUIPMENT"]
browser_click      button[data-testid="party-inventory"]
```

Both steps are mandatory. **The sheet always opens on the Actions tab after a
load**, whatever was open before. And a click issued immediately after load
fails with `TimeoutError ... waiting for element to be visible, enabled and
stable`: the element resolves, then React re-renders under it. Wait first.

Use `my-inventory` in place of `party-inventory` for the character's own bag.

## 2. Read the whole inventory

`browser_evaluate`:

```js
[...document.querySelectorAll('.ct-inventory-item')].map(r => {
  const n = r.querySelector('.ct-inventory-item__name');
  return { name: n ? n.textContent.trim() : '',
           cells: [...r.children].map(c => c.textContent.trim()) };
})
```

Two caveats:

- The result includes **two container header nodes**, `Party Equipment (n)` and
  `Bag of Devouring (n)`. Row count = node count − 2.
- Names come back with the type appended — `Acidic EmeraldsCustom`,
  `Crown of FearWondrous item`. Match by prefix, and match against a note's
  `ddb_name` where it has one.

Pass `filename:` to `browser_evaluate` to dump straight to a file instead of
into the transcript.

## 3. Edit or rename a row

```
browser_click      .ct-inventory-item:has-text("<current name>")
browser_click      .ddbc-collapsible__heading:has-text("Customize")
                   (confirm the fields — see "Identifying form fields" below)
browser_fill_form  Name -> ..., Description -> ...
browser_press_key  Tab
```

**Tab commits; there is no save button.** Never press Escape — it closes the
whole panel and loses what was typed.

Then verify: reload, re-enter via recipe 1, and read the name back from the
DOM. A `fill` that silently fails looks exactly like one that worked.

## 4. Add a custom item to Party Equipment

Go through the **scoped** panel. This is the whole trick — scoped, ADD has no
destination menu and drops straight into Party Equipment.

```
(recipe 1 first)
browser_click   button[data-testid="open-manage-equipment"]
browser_click   .ct-inventory__action:has-text("Add items to your Party Equipment")
browser_click   .ddbc-collapsible__heading:has-text("Add Custom Item")
                (confirm fields, then fill)
browser_click   button[data-testid="theme-button-with-menu-add,-,-item"]
```

The panel retitles itself *Party Equipment* and shows `Contents (n)`.

- **Name is pre-filled** with `Custom Item <n>`. `browser_fill_form` replaces
  it outright, so the old triple-click advice is unnecessary.
- **Cost Override is per unit.** `10` at quantity `219` shows as `2190 gp`.
  Set it only where the vault gives a gold value per item.
- **Notes vs Description.** Notes is one line and shows on the row — put the
  provenance there (`Vault chest 14, Session 03. Drivik.`). Description carries
  the vault's own text.
- That `data-testid` really does contain a double space and commas; it is
  generated from the label "Add  Item". Copy it exactly.

## 5. Add a homebrew item to Party Equipment

```
(recipe 1, then open-manage-equipment and the scoped panel as in recipe 4)
browser_click      button:text-is("Homebrew")        // Filter By Source Category
browser_fill_form  input.styles_search__A3o1k -> "<unique fragment>"
browser_click      (the ADD control on the single result row)
```

- **The sheet caches the homebrew list at page load.** An item created after
  the sheet was opened returns *No Results Found* however you spell it. Reload
  after a batch of creations, then re-enter the panel.
- Use a fragment matching exactly one item — `Lesser Growth`, not
  `Potion of Growth`. `Prune`, `Vantablack`, `Extending` are each unique.
- `browser_fill_form` replaces the filter box contents, so the old
  "triple-click or you get `crownCrown`" warning no longer applies.

## 6. Change a quantity

```
browser_click      .ct-inventory-item:has-text("<name>")
browser_fill_form  input[data-testid="change-quantity"] -> "<n>"
browser_press_key  Tab
```

---

## Identifying form fields

Inside **Customize** and **Add Custom Item** the editable fields carry no id,
class or testid. Read their labels before typing — `browser_evaluate`:

```js
[...document.querySelectorAll('input,textarea')].map(e => {
  let row = e.parentElement, txt = '';
  for (let k = 0; k < 5 && row; k++) {
    const t = row.innerText && row.innerText.trim();
    if (t && t.length > 0 && t.length < 40) { txt = t; break; }
    row = row.parentElement;
  }
  return { label: txt, type: e.type, val: e.value };
})
```

**A naive `previousElementSibling` walk reports the labels off by one** and
will aim an edit at the wrong field — it labelled the Name box
"Weight Override" on the first attempt here. Use the version above.

In DOM order within an open panel the fields are Cost Override, Weight
Override, **Name**, **Notes**, **Description** (the only `textarea`), Quantity.
The page's other search boxes are `type="search"`, so they do not interleave.

## Item avatars cannot be uploaded from here

Tested 1 November 2026 and it does not work. Record of the dead end so
nobody spends the time again.

The homebrew item edit page is at `<item url>/edit` and carries two hidden
file inputs under Additional Information:

| Field | Selector |
|---|---|
| Avatar | `#field-avatar` |
| Large Avatar | `#field-large-avatar` |

Both are `input[type="file"]`, zero-size but enabled, and **D&D Beyond takes
an uploaded file — there is no URL field.** So a public image URL is no help
here, however convenient it is for the archive page.

Clicking the input with `element.click()` does raise a file chooser, and
Playwright intercepts it properly — no native dialog appears on the user's
screen. But the upload itself fails:

```
fileChooser.setFiles: Protocol error (DOM.setFileInputFiles):
{"code":-32000,"message":"Not allowed"}
```

That is the **extension bridge refusing to put local files into a page**, a
deliberate security boundary of `--extension` mode rather than a bug or a
selector problem. Nothing on this side gets past it, and it should not be
worked around.

If a chooser has been opened, close it with `browser_file_upload` and an
empty `paths` array, or the page is left with a modal pending.

**So avatars are the user's job.** The files sit in `images/items/`; they
upload them by hand on each item's edit page. Offer the list of item URLs
and matching filenames rather than attempting it.

## Selector reference

| Target | Selector |
|---|---|
| Inventory tab | `button[data-testid="EQUIPMENT"]` |
| My Inventory sub-tab | `button[data-testid="my-inventory"]` |
| Party Inventory sub-tab | `button[data-testid="party-inventory"]` |
| Manage Inventory | `button[data-testid="open-manage-equipment"]` |
| Scope panel to Party Equipment | `.ct-inventory__action:has-text("Add items to your Party Equipment")` |
| Contents count (verification) | `.ddbc-collapsible__heading:has-text("Contents")` |
| Add Custom Item section | `.ddbc-collapsible__heading:has-text("Add Custom Item")` |
| Customize section | `.ddbc-collapsible__heading:has-text("Customize")` |
| ADD ITEM | `button[data-testid="theme-button-with-menu-add,-,-item"]` |
| Homebrew source chip | `button:text-is("Homebrew")` |
| Catalogue filter box | `input.styles_search__A3o1k` |
| Every inventory row | `.ct-inventory-item` |
| A row's name cell | `.ct-inventory-item__name` |
| One row by name | `.ct-inventory-item:has-text("<name>")` |
| Quantity | `input[data-testid="change-quantity"]` |
| Move | `button[data-testid="theme-button-with-menu-move"]` |
| Delete | `button[data-testid="delete-item-button"]` |

`data-testid` and text-based selectors are preferred because they survive
restyling. Anything matching `styles_*__hash` is a CSS-module name and **can
change on any deploy** — only `input.styles_search__A3o1k` relies on one, so
check that first if recipe 5 breaks.

## Verification, not optimism

`Contents (n)` is plain text in the accessibility tree, so the count can be
read without a screenshot or a zoom:

```js
[...document.querySelectorAll('.ddbc-collapsible__heading')]
  .map(e => e.textContent.trim()).filter(t => /^Contents/.test(t))
```

Check it before and after any add. The row still reads ADD whether or not the
click landed, so the count is the only honest signal.

## Things that will waste your time

- **Never press Escape.** It closes the entire panel and loses the form.
- **Avoid `browser_run_code_unsafe`.** It executes arbitrary JavaScript in the
  Playwright server process and is RCE-equivalent. Everything here works with
  the ordinary tools.
- In the **unscoped** Manage Inventory panel, clicking the ADD ITEM button body
  silently discards the form and creates a blank `Custom Item N` in the
  character's own Equipment. Recipes 4 and 5 avoid this by scoping the panel
  first; do not shortcut them.
