"""
Save-Prompt-as-TXT — a live on/off checkbox that writes a .txt containing ONLY the positive
prompt next to each generated image.

Why this exists: Forge has a built-in "Create a text file next to every image" setting, but it is
global, applies after an Apply/reload, and writes the FULL parameters (prompt + negative + settings).
This is a per-generation checkbox (no restart) that writes just the positive prompt.

How it works: an AlwaysVisible script exposes the checkbox and records its state per generation;
a global on_image_saved callback writes "<image_basename>.txt" with the prompt from that image's
own generation info (so batches / wildcards / prompt S&R each get their real per-image prompt).
"""
import os

import gradio as gr

from modules import scripts, script_callbacks

try:                                              # header-checkbox accordion (built-in);
    from modules.ui_components import InputAccordion   # falls back to a plain accordion if unavailable
except Exception:
    InputAccordion = None

# Set per-generation by the script's process(); read by the (global) image-saved callback.
STATE = {"enabled": False}


def _prompt_from_geninfo(params):
    """Return ONLY the positive prompt for the just-saved image.

    Prefer the image's own generation-info string (correct per-image for batches / wildcards /
    prompt S&R), which is laid out as:  <prompt>\\nNegative prompt: <neg>\\nSteps: <params>
    (the 'Negative prompt:' line is omitted when the negative is empty). Fall back to p.prompt.
    """
    info = ""
    try:
        info = (getattr(params, "pnginfo", None) or {}).get("parameters", "") or ""
    except Exception:
        info = ""
    if info:
        cut = info.find("\nNegative prompt:")
        if cut == -1:
            cut = info.find("\nSteps:")
        if cut != -1:
            return info[:cut].strip()
        # no recognizable separator — fall through to the processing object's prompt
    try:
        return (getattr(params.p, "prompt", "") or "").strip()
    except Exception:
        return info.strip() if info else ""


def _is_grid(params):
    """Skip contact-sheet grids — we only want per-image prompts."""
    fn = getattr(params, "filename", "") or ""
    if os.path.basename(fn).startswith("grid-"):
        return True
    try:
        gpath = getattr(params.p, "outpath_grids", None)
        if gpath and os.path.normpath(os.path.dirname(fn)) == os.path.normpath(gpath):
            return True
    except Exception:
        pass
    return False


def _on_image_saved(params):
    if not STATE.get("enabled"):
        return
    try:
        fn = getattr(params, "filename", "") or ""
        if not fn or _is_grid(params):
            return
        prompt = _prompt_from_geninfo(params)
        if not prompt:
            return
        txt_path = os.path.splitext(fn)[0] + ".txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(prompt)
    except Exception:
        pass  # never let a side-file write break image saving


# Register the callback ONCE at import (module-level), not per Script instance/tab.
script_callbacks.on_image_saved(_on_image_saved)


class SavePromptTxt(scripts.Script):
    def title(self):
        return "Save prompt to .txt"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        note = ("Writes a **`.txt` with only the positive prompt** (no negative, no settings) next to "
                "every image you generate. Live on/off — no restart, no Settings page.")
        if InputAccordion is not None:
            with InputAccordion(False, label="💾 Save prompt to .txt (next to image)") as enabled:
                gr.Markdown(note)
        else:                                     # older builds without InputAccordion
            with gr.Accordion("💾 Save prompt to .txt (next to image)", open=False):
                enabled = gr.Checkbox(label="Enable", value=False)
                gr.Markdown(note)
        return [enabled]

    def process(self, p, enabled=False):
        STATE["enabled"] = bool(enabled)
