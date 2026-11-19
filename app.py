from flask import abort
from optica_core import Dataset, acquisition, create_app, image, project


class StackDataset(Dataset):
    """Focus stack of an object: its slices and the images stacked from them (stack.json)."""

    manifest = "stack.json"
    viewer = "stackoptica"

    def images(self, id):
        manifest = self.load(id)
        folder = self.thumbnails_folder(id, manifest)
        acquisitions = []
        for stack in manifest["acquisitions"]:
            # slices from the lowest to the highest
            slices = sorted(stack["images"], key=lambda entry: entry["z"])
            acquisitions.append(acquisition(
                stack["id"],
                label=stack.get("label"),
                size=stack["size"],
                images=[image(entry["file"], entry.get("label"), hasThumbnail=self.has_thumbnail(folder, entry["file"]))
                        for entry in slices],
                # the stacked results, labelled by their method
                standalone_images=[image(entry["file"], entry.get("label"), hasThumbnail=self.has_thumbnail(folder, entry["file"]))
                                   for entry in stack.get("standaloneImages", [])],
            ))
        return project(*acquisitions, unit=manifest["unit"])

    # a pixel of a slice -> its position in the stack, only the slices have a z
    def position(self, id, image_id, x, y):
        stack, entry = self.find_image(self.load(id), image_id)
        if "z" not in entry:
            abort(404)
        pixel_size = self.pixel_size(stack, entry) or [1, 1]
        return {"x": x * pixel_size[0], "y": y * pixel_size[1], "z": entry["z"]}


app = create_app(StackDataset, logo="Stackoptica", version="2.1.0")


if __name__ == "__main__":
    app.run()
