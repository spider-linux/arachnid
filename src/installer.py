import shutil
import src.parser as parser
import src.stower as stower
import os
import urllib.request
import mimetypes
import subprocess
import src.log as log

def get_sources(build_file, build_directory):
    package = parser.parse_build_file(build_file)
    for source in package.sources.urls:
        log.log(f"downloading from {source}")
        *_, source_file = source.split("/")
        urllib.request.urlretrieve(source, os.path.join(build_directory, source_file))

def build_install_package(build_file):
    build_file = os.path.abspath(build_file)
    package = parser.parse_build_file(build_file)

    archives_for_removal = []

    build_directory = os.path.join("/tmp", "arachnid", "build")

    if os.path.exists(build_directory):
        log.log(f"{build_directory} exists already, removing")
        shutil.rmtree(build_directory, ignore_errors=False)

    log.log(f"creating {build_directory}")

    os.makedirs(build_directory)

    log.log(f"moving into {build_directory}")
    os.chdir(build_directory)

    get_sources(build_file, build_directory)

    log.log(f"extracting archives in {build_directory}")
    extracted_dir_name = package.meta.name
    with os.scandir(build_directory) as dir:
        for entry in dir:
            try:
                shutil.unpack_archive(entry.name, extracted_dir_name)
                archives_for_removal.append(entry.path)
            except ValueError:
                continue

    for archive in archives_for_removal:
        log.log(f"deleting {archive}")
        os.remove(archive)

    log.log(f"moving into extracted directory {extracted_dir_name}")
    os.chdir(extracted_dir_name)

    commands = [command for command in package.build.install]
    subprocess.run(" && ".join(commands), shell=True)

    log.log(f"removing {os.getcwd()}")
    os.chdir("..")
    shutil.rmtree(extracted_dir_name, ignore_errors=False)

    with os.scandir("/opt") as opt:
        for entry in opt:
            if f"{package.meta.name}-{package.meta.version}" in entry.name:
                target_install_directory = f"{entry.path}/"

    stow = stower.Stower()
    stow.stow(target_install_directory)
