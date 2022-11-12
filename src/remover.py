import os
import shutil
import src.log as log
import src.stower as stower

def remove_package(package, package_dir="/opt"):
    for entry in os.listdir(package_dir):
        if entry.startswith(package):
            package_path = os.path.join(package_dir, entry)

            stow = stower.Stower()
            stow.unstow(package_path)

            log.log(f"removing {package_path}")
            shutil.rmtree(package_path, ignore_errors=False)

