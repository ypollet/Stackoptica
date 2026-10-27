# Stackoptica (core)

Stackoptica rebuilt on [`core/`](../core): the viewers, landmark and distance lists, menu, models and data layer come from `@optica/core` and `optica_core`; this folder only keeps what is specific to focus stacks.

- `app.py`: the `stack.json` adapter of the common API. One acquisition `stack`: the slices (`images`, sorted by depth) and the stacked results (`standaloneImages`, labelled by their key in `Stacked_images`). Positions are computed on the slices only.
- `src/data/setup.ts`: registers the core `ProjectRepository`, the payload is the standard one.
- `src/lib/stores.ts`: the project and the settings.
- `src/components/`: the logo, the sidebar (stack / stacked toggle, slice slider, annotations, measures), the viewer and the menu wiring.

Landmarks are placed on the slices; the stacked images can be viewed (the landmarks are drawn on them) but not edited.

## Run

```bash
# backend, objects in ./data/<id>/stack.json ($OPTICA_DATA_FOLDER to use another folder)
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/flask --app app run --port 5000

# frontend (http://localhost:5173/?series=<id>)
npm install
npm run dev
```

`.env` selects the backend (`VITE_BACKEND_TYPE=WEB|ORTHANC`, `VITE_BACKEND_URL`).
