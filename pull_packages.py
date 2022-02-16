import json
import logging
import sys
from pathlib import Path

from oras import Oras

owner = sys.argv[1]
target_platform = str(sys.argv[2])
conda_prefix = sys.argv[3]
token = sys.argv[4]

directory = "conda-bld"
oras = Oras(owner, token, conda_prefix, target_platform)
oras.login()

base = Path(conda_prefix) / directory
# unix= #/home/runner/micromamba/envs/buildenv/ #conda-bld/
# win = C:\Users\runneradmin\micromamba\envs\buildenv\conda-bld\
if not base.is_dir():
    logging.warning(f" {base} did NOT exist")
    base.mkdir(mode=511, parents=False, exist_ok=True)

if "win" in target_platform:
    target_platform = "win-64"

path = base / target_platform
# expl=#/home/runner/micromamba/envs/buildenv/ #conda-bld/ #linux-aarch64/
# win = C:\Users\runneradmin\micromamba\envs\buildenv\conda-bld\win-64\

if not path.is_dir:
    path.mkdir(mode=511, parents=False, exist_ok=True)(f" {base} did NOT exist")

trgt = "linux"
if "osx" in target_platform:
    trgt = "osx"
elif "win" in target_platform:
    trgt = "win-64"

with open("packages.json", "r") as read_file:
    packages_json = json.load(read_file)

packagesList = packages_json["pkgs"][trgt]

versions_dict = {}
for pkg in packagesList:
    versions_dict = oras.pull(pkg, "latest", str(path), versions_dict)

with open("versions.json", "w") as fp:
    json.dump(versions_dict, fp)
