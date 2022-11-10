#!/usr/bin/python

import os
import src.log as log

class Stower(object):
    def init(self): pass

    def stow(self, package, target="/"):
        log.log(f"installing {package}")
        for root, dirs, files in os.walk(package):
            root = root.replace(package, "")

            if not root:
                continue

            target_found = os.path.join(target, root)
            same_dir = os.path.isdir(target_found)

            if not same_dir:
                os.mkdir(target_found)

            if not files:
                continue

            for f in files:
                target_symlink = os.path.join(target, root, f)
                package_file = os.path.join(package, root, f)

                if os.path.islink(target_symlink):
                    print(f"{target_symlink}: found symlink: cannot stow again.")
                    continue

                print(f"linking {target_symlink} to {package_file}")

                os.symlink(package_file, target_symlink)

    def unstow(self, package, target="/"):
        log.log(f"uninstalling {package}")
        for root, dirs, files in os.walk(package):
            root = root.replace(package, "")

            if not root:
                continue

            target_found = os.path.join(target, root)

            if not files:
                continue

            for f in files:
                target_symlink = os.path.join(target, os.path.join(root, f))

                if os.path.islink(target_symlink):
                    print(f"unlinking {target_symlink}")
                    os.unlink(target_symlink)
