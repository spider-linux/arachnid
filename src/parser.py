import tomllib
import os

# Stole this from https://joelmccune.com/python-dictionary-as-object/ because I'm lazy
# It does the job too.
class BuildFileToObject(object):
    def __init__(self, build_file):
        assert isinstance(build_file, dict)
        for key, val in build_file.items():
            if isinstance(val, (list, tuple)):
               setattr(self, key, [BuildFileToObject(x) if isinstance(x, dict) else x for x in val])
            else:
               setattr(self, key, BuildFileToObject(val) if isinstance(val, dict) else val)

def parse_build_file(file):
    # file = os.path.join(file)
    if not file.endswith("toml"):
        file = f"{file}.toml"
    with open(file, "rb") as f:
        build_file = tomllib.load(f)
        package = BuildFileToObject(build_file)
        return package
