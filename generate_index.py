import requests
import urllib.parse
import json
import os
import sys

from pathlib import Path

from dataclasses import dataclass

GH_REPO_PATH = "skybird23333/collection"
INCLUDED_PATH = "resources"
BASE_URL = "//"

OUTPUT = {}

suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


@dataclass
class File:
    name: str
    size: int
    url: str


def fetch_tree_flat(url):
    API_ENDPOINT = f"https://api.github.com/repos/{GH_REPO_PATH}/git/trees/main?recursive=1"
    return requests.get(API_ENDPOINT, verify=False).json() #TODO: Disable verify false


def create_tree(tree):
    new_tree = {}
    for obj in tree:
        if not obj["path"].startswith(INCLUDED_PATH):
            continue

        if obj["type"] == "tree":
            continue

        path = obj["path"].split("/")
        directory = path[:-1]
        filename = path[-1]

        file_url = f"https://github.com/{GH_REPO_PATH}/raw/main/{urllib.parse.quote(obj['path'])}"

        current_tree = new_tree

        for folder in directory:
            current_tree = current_tree.setdefault(folder, dict())

        current_tree[filename] = {
            "name": filename,
            "size": obj["size"],
            "url": file_url
        }

    return new_tree


def generate_index_recursively(base_path, output_path, is_root, tree):
    folder_path = base_path / output_path

    contents = []

    for name, obj in tree.items():
        # is a folder?
        if isinstance(obj, dict):
            generate_index_recursively(
                base_path, output_path / name, False, obj
            )
            contents.append({"name": name, "size": "-",
                            "icon": "folder-outline", "type": "folder"})
        elif isinstance(obj, File):
            content = {"name": obj.name, "size": humansize(obj.size),
                       "icon": "file", "type": "file", "url": obj.url}

            if content["name"].endswith("pdf"):
                content["icon"] = "file-pdf"
            elif content["name"].endswith("doc") or content["name"].endswith("docx"):
                content["icon"] = "file-word"

            contents.append(content)

    contents.sort(key=lambda x: (
        "A" if x["type"] == "folder" else "B") + x["name"])


if __name__ == "__main__":
    flat_tree = fetch_tree_flat(GH_REPO_PATH)
    tree = create_tree(flat_tree["tree"])

    with open('public/index.json', 'w') as file:
        file.write(json.dumps(tree))

    # generate_index_recursively(Path("."), Path(
    #     "."), True, tree[INCLUDED_PATH])