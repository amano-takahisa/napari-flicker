# napari-flicker

Blink selected layers in [napari](https://napari.org/) to compare them visually.

## Installation

Install the plugin with pip:

```bash
pip install napari-flicker
```

You can also install it from napari via **Plugins > Install/Uninstall Plugins...**
and searching for `napari-flicker`.

## Usage

Start napari with the plugin:

```bash
napari --with napari-flicker 'Flicker Widget'
```

Or open the widget from the menu: **Plugins > Flicker > Flicker Widget**.

1. Load the layers you want to compare.
2. Tick the layers you want to blink in the **Available Layers** list.
3. Click **Start Flicker**. The selected layers toggle their visibility every
   0.5 seconds, so you can spot differences between them.
4. Click **Stop Flicker** to stop.

## Notes

- Only **Image** and **Labels** layers can be flickered.
- The flicker interval is fixed at 0.5 seconds.
- All selected layers toggle together.
- The layer list updates automatically when layers are added to or removed
  from the viewer.
- Nothing happens if you start flickering without selecting a layer.
