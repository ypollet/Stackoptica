"""The manifest schema of stackoptica (stack.json), on top of the common one of optica_core."""

import copy
import glob
import json
import os

import pytest

pytest.importorskip("jsonschema")
from optica_core.schema import errors, validator  # noqa: E402

HERE = os.path.dirname(__file__)
SCHEMA = os.path.join(HERE, "..", "manifest.schema.json")
DATA = os.path.join(HERE, "..", "data")

EXAMPLE = {
    "format": "optica-manifest",
    "version": 1,
    "viewer": "stackoptica",
    "unit": "mm",
    "acquisitions": [
        {
            "id": "stack",
            "size": {
                "width": 10,
                "height": 20
            },
            "pixelSize": [
                0.1,
                0.2
            ],
            "images": [
                {
                    "file": "p0.jpg",
                    "z": 0
                },
                {
                    "file": "p1.jpg",
                    "z": 0.002,
                    "pixelSize": [
                        0.3,
                        0.3
                    ]
                }
            ],
            "standaloneImages": [
                {
                    "file": "dorsal.jpg",
                    "label": "Dorsal"
                }
            ]
        }
    ]
}


@pytest.fixture(scope="module")
def check():
    return validator(SCHEMA)


def test_example(check):
    assert errors(check, EXAMPLE) == []


def a_slice_without_z(manifest):
    del manifest["acquisitions"][0]["images"][0]["z"]


def the_manifest_of_another_viewer(manifest):
    manifest["viewer"] = "depthoptica"


@pytest.mark.parametrize("mistake", [
    a_slice_without_z,
    the_manifest_of_another_viewer,
])
def test_mistakes_are_refused(check, mistake):
    manifest = copy.deepcopy(EXAMPLE)
    mistake(manifest)
    assert errors(check, manifest) != []


# the manifests of the data folder, when there is one (it isn't in git)
@pytest.mark.parametrize("path", sorted(glob.glob(os.path.join(DATA, "**", "stack.json"), recursive=True)) or [None])
def test_data(check, path):
    if path is None:
        pytest.skip("no stack.json in data/")
    with open(path) as f:
        assert errors(check, json.load(f)) == []
