# Save Prompt to .txt

A tiny Forge/A1111 extension: a **live checkbox** that saves a `.txt` containing **only the positive prompt** next to every image you generate.

## Why
Forge already has *Settings → Saving images → "Create a text file next to every image with generation parameters."* But that setting is **global**, needs an **Apply/reload**, and writes the **full** parameters (prompt **+ negative + all settings**). This extension instead gives you:

- ✅ A **per-generation on/off checkbox** — toggle it any time, **no restart**.
- ✅ The `.txt` contains **only the positive prompt** — no negative prompt, no settings.

## Use
1. Copy `sd-forge-save-prompt-txt` into your Forge `extensions/` folder and restart once.
2. In **txt2img** (or img2img), open **💾 Save prompt to .txt** and tick the box.
3. Generate. Each image `00123-....png` gets a sibling `00123-....txt` with just its prompt.

Untick to stop — takes effect on the next generation. Contact-sheet grids are skipped; each image in a batch gets **its own** prompt (correct for wildcards / prompt S&R).

*By [stableyogi.com](https://stableyogi.com).*
