"""Serverless Updater
Copyright (c) 2026 Louis Liu  All rights reserved.
"""

import os
import hashlib
import zipfile
import shutil

import requests
from packaging import version

GITHUB_REPO = "36lyx/ServerlessUpdaterDemoProject"


def check_update(current_version):
    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Unable to connect to the server:", e)
        return

    release = response.json()
    latest_version = release["tag_name"].lstrip("v")
    if version.parse(latest_version) <= version.parse(current_version):
        return

    package, checksum = None, None
    for asset in release["assets"]:
        name = asset["name"]
        if name.endswith(".zip"):
            package = asset
        elif name.endswith(".sha256"):
            checksum = asset
    if package is None:
        raise Exception("No packages found")
    if checksum is None:
        raise Exception("No checksum files found")
    return {
        "version": latest_version,
        "package_url": package["browser_download_url"],
        "sha256_url": checksum["browser_download_url"],
        "release_note": release["body"],
        "name": release["name"],
    }


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()


def download_and_update(info):
    package_url = info["package_url"]
    filename = "temp/update.zip"
    print("Downloading...")
    expected_sha256 = requests.get(info["sha256_url"]).text.strip().split()[0]
    r = requests.get(package_url)
    with open(filename, "wb") as f:
        f.write(r.content)
    if sha256(filename) != expected_sha256:
        raise Exception("Hash error")
    print("Verified")
    with zipfile.ZipFile(filename) as z:
        z.extractall("new_version")
    for f in os.listdir("new_version"):
        shutil.copy("new_version/" + f, f)
    print("Update finished")
