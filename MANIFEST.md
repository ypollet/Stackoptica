# Stackoptica manifest: `stack.json`

The fields stackoptica adds to the common manifest ([core/MANIFEST.md](../core/MANIFEST.md)). The JSON Schema is [`manifest.schema.json`](manifest.schema.json).

`images` are the slices, each at its height `z` in `unit`. `standaloneImages` are the images stacked from them, labelled by their method. The pixel size of the acquisition applies to every slice; a slice gives its own `pixelSize` if the magnification changed.

```jsonc
"images": [{ "file": "Plane000.jpg", "z": 0 }, { "file": "Plane001.jpg", "z": 0.002 }],
"standaloneImages": [{ "file": "dorsal.jpg", "label": "Dorsal" }]
```

Check a manifest (the tests in `tests/test_manifest.py` check every manifest of `data/`):

```bash
python -m optica_core.schema manifest.schema.json data/<object>/stack.json
```
