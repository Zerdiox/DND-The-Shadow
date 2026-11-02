# Gemini image models and the app UI

**Checked 1 November 2026.** Image models change every few months; treat
anything here older than a season as a starting point to re-verify, not fact.
Re-checking is cheap: open the app and look.

## What the user's account actually offers

Verified by opening `https://gemini.google.com/app` in the user's own Chrome:

- Signed in as **Zerdiox**, **free tier** (an Upgrade button is present).
- Location Belgium. Image generation **is available** — an older claim that the
  Gemini app withholds image generation in the EEA, Switzerland and the UK did
  not hold here. Do not repeat that claim without checking.
- Tools menu (**Upload and tools**) contains: Upload files, Add from Drive,
  More uploads, **Create image**, Create music, Canvas, Deep Research, Guided
  Learning.
- Conversation modes (**mode picker**): Auto, 3.1 Pro, 4 Argon — each with a
  thinking level of Low, Medium or High. Default is Auto.
- Generated images collect under **Images** in the left sidebar.

The app gives **no by-name image model picker.** Google routes the request.
What you choose is the conversation mode, and image intent via Create image.

## The model family, as of the check

From Google's developer documentation:

| Model | ID | Position |
|---|---|---|
| Nano Banana 2.1 | `gemini-nano-banana-2.1` | Latest efficient generation and conversational editing model, October 2026 |
| Nano Banana Pro | Gemini 3 Pro Image | Highest quality, more expensive |
| Nano Banana 2 Lite | — | Fastest and cheapest of the family |
| Nano Banana 2 | Gemini 3.1 Flash Image | Predecessor, superseded |

Nano Banana 2.1 outputs at 1K (default), 2K or 4K, accepts up to 14 reference
images with character consistency across 4 and object fidelity across 10, and
supports minimal/medium/high thinking. `gemini-3.1-flash-image` was retired on
29 October 2026.

Reference-image support is the interesting one for this vault: it is the
mechanism that would let a batch of items share an established look by passing
an already-approved plate as a reference, rather than relying on the prompt
alone.

## Quotas

**There is a usage page, and it is exact: <https://gemini.google.com/usage>.**
Found on 1 November 2026 when the account hit the wall mid-batch. Read it
instead of guessing — guessing quota is a mistake this skill has already
recorded once.

It shows two bars and the reset time for each:

```
Current usage   100% used   Resets at 23:06
Weekly limit      9% used   Resets on 2 Nov at 21:06
```

Two things follow. **The short window is what binds**, not the weekly one —
at exhaustion the weekly bar was still at 9%, so the account is limited by a
roughly daily cycle and the week will never be the problem at this pace. And
the reset is an absolute clock time, so the wait is knowable: say so rather
than telling the user it is indefinite.

What it cost to get there on 1 November 2026: nine vial images earlier in the
day, then eight more in the evening — two for the Bottled Silver Tear, three
for the Tornado Prisms, one for the Red Lanterns, two for the Chain — and the
next request was refused.

**Measured properly on 2 November: twelve generations read 46%, so the day
holds roughly twenty-six.** That is the figure to plan with. The earlier
"fifteen to twenty" was inferred from where the wall fell rather than read
off the page, and it was low.

Read the percentage rather than counting. The window rolls, so a count from
the start of a session drifts, and the page is authoritative and free.

How exhaustion presents, so it is recognised rather than diagnosed:

- The composer sends normally and the conversation is created.
- No image arrives, and the reply reads *"I can create more images as soon as
  your limit resets. Check your usage in Settings."*
- The tab may navigate itself to `/usage`.

**That refusal still spends the request.** The Chain's third prompt returned
nothing and is gone. When a run is near the limit, check `/usage` before
sending rather than after.

The older guidance still holds: do the showpieces first, and expect to stop
early rather than finish a batch. The claim that free accounts get roughly
two Pro-quality images per day before falling back to the standard model
remains **unverified** — the usage page does not break usage down by model.

## Why not the API

The user has no billing enabled. Image generation is charged per image on the
API, and the free API tier for image models is inconsistent-to-absent. The web
app uses an allowance the account already has. If billing is ever enabled, the
API becomes much the better route for a batch — it is scriptable, it takes
reference images cleanly, and it does not involve driving a chat UI.

## Sources

- [Gemini Nano Banana 2.1 model documentation](https://ai.google.dev/gemini-api/docs/models/gemini-nano-banana-2.1)
- [Gemini image generation best practices](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/gemini-image-generation-best-practices)
- [Nano Banana 2 announcement](https://blog.google/innovation-and-ai/technology/ai/nano-banana-2/)
- [Nano Banana Pro announcement](https://blog.google/innovation-and-ai/products/nano-banana-pro/)
