"""Release Generator
Copyright (c) 2026 Louis Liu  All rights reserved.
"""

import os
import zipfile
import hashlib
import pathspec

import version

APP_NAME = "ServerlessUpdaterDemoProject"
APP_VERSION = version.VERSION
APP_DIR = "."
RELEASE_DIR = "release"


def load_gitignore(filename=".gitignore"):
    if not os.path.exists(filename):
        return
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return pathspec.PathSpec.from_lines("gitwildmatch", lines)


def calculate_sha256(filename):
    sha256 = hashlib.sha256()
    with open(filename, "rb") as f:
        while True:
            data = f.read(1024 * 1024)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


def create_zip(source, output):
    if os.path.exists(output):
        os.remove(output)
    spec = load_gitignore()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(source):
            for file in files:
                full_path = os.path.join(root, file)
                if RELEASE_DIR in full_path:
                    continue
                relative_path = os.path.relpath(full_path, source)
                if (
                    relative_path == ".gitignore"
                    or spec
                    and spec.match_file(relative_path)
                ):
                    continue
                z.write(full_path, relative_path)


def create_checksum_file(zip_file):
    digest = calculate_sha256(zip_file)
    checksum_file = zip_file + ".sha256"
    with open(checksum_file, "w", encoding="utf-8") as f:
        f.write(digest)
    return checksum_file


def build_release():
    name, version = APP_NAME, APP_VERSION
    print(f"Building {name} {version}")
    os.makedirs(RELEASE_DIR, exist_ok=True)
    zip_name = f"{name}-{version}.zip"
    zip_path = os.path.join(RELEASE_DIR, zip_name)

    print("Creating zip...")
    create_zip(APP_DIR, zip_path)
    print("Created:", zip_path)

    print("Calculating SHA256...")
    checksum_file = create_checksum_file(zip_path)
    print("Created:", checksum_file)
    print("Release files:")
    print(zip_path)
    print(checksum_file)


if __name__ == "__main__":
    build_release()
