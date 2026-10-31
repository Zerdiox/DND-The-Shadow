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

Unknown and variable, deliberately. Google does not publish a fixed figure for
the app, and third-party sources disagree by an order of magnitude — 20 a day,
100 a day, "depends on load, refreshes every five hours with a weekly cap".
One frequently repeated claim is that free accounts get roughly two
Pro-quality images per day before falling back to the standard model, which
would make the first generations of a session the valuable ones. **None of
this was verified here**, because verifying it means spending the quota.

The practical consequence: plan a handful of items per sitting, do the
showpieces first, and expect to stop early rather than finishing a batch.

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
