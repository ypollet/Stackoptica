from flask import abort
from optica_core import Dataset, acquisition, create_app, image, project


class StackDataset(Dataset):
    """Focus stack of an object: its slices and the images stacked from them (stack.json)."""

    manifest = "stack.json"

    def images(self, id):
        stack_file = self.load(id)
        # slices from the lowest to the highest
        slices = sorted(stack_file["stack"], key=lambda name: stack_file["stack"][name]["SlicePosition"][2])
        return project(acquisition(
            "stack",
            size={"width": stack_file["width"], "height": stack_file["height"]},
            images=[image(name) for name in slices],
            # the stacked results, labelled by their method
            standalone_images=[image(name, label) for label, name in stack_file["Stacked_images"].items()],
            thumbnails=bool(stack_file.get("thumbnails")),
        ))

    # a pixel of a slice -> its position in the stack, only the slices are calibrated
    def position(self, id, image_id, x, y):
        image_data = self.load(id)["stack"].get(image_id)
        if image_data is None:
            abort(404)
        return {
            "x": x * image_data["PixelRatio"][0] + image_data["SlicePosition"][0],
            "y": y * image_data["PixelRatio"][1] + image_data["SlicePosition"][1],
            "z": image_data["SlicePosition"][2],
        }


app = create_app(StackDataset, logo="Stackoptica", version="2.1.0")


if __name__ == "__main__":
    app.run()
