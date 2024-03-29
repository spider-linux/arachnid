import shutil
import os
import urllib.request
import mimetypes
import subprocess
import tempfile
import sqlite3

''' Arachnid Specific '''
import src.parser as parser
import src.stower as stower
import src.log as log

def get_sources(build_file, build_directory):
    package = parser.parse_build_file(build_file)
    for source in package.sources.urls:
        log.log(f"downloading from {source}")
        *_, source_file = source.split("/")
        urllib.request.urlretrieve(source, os.path.join(build_directory, source_file))

def build_and_install_package(build_file):
    # 1: Prepare the directories
    build_file = os.path.abspath(build_file)
    package = parser.parse_build_file(build_file)

    source_directories = []

    arachnid_build_directory = tempfile.mkdtemp()
    log.log(f"creating {arachnid_build_directory}")

    log.log(f"moving into {arachnid_build_directory}")
    os.chdir(arachnid_build_directory)

    get_sources(build_file, arachnid_build_directory)

    log.log(f"extracting archives in {arachnid_build_directory}")
    package_source_directory = package.meta.name
    with os.scandir(arachnid_build_directory) as dir:
        for entry in dir:
            try:
                shutil.unpack_archive(entry.name, package_source_directory)
                source_directories.append(entry.path)
            except ValueError:
                continue

    for archive in source_directories:
        log.log(f"deleting {archive}")
        os.remove(archive)

    log.log(f"moving into extracted directory {package_source_directory}")
    os.chdir(package_source_directory)

    # 2: Run the commands
    build_commands = [command for command in package.build.install]
    subprocess.run(" && ".join(build_commands), shell=True)

    # 3: Clean-up
    os.chdir(f"{arachnid_build_directory}/..")

    log.log(f"removing build directory at {arachnid_build_directory}")
    shutil.rmtree(arachnid_build_directory, ignore_errors=False)

    with os.scandir("/opt") as package_installation_directory:
        for entry in package_installation_directory:
            if f"{package.meta.name}-{package.meta.version}" in entry.name:
                install_directory_within_target = f"{entry.path}/"

    # 4: Actual install section
    stow = stower.Stower()
    stow.stow(install_directory_within_target)

    conn = sqlite3.connect("/var/db/arachnid.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO packages VALUES(?, ?, ?)", (package.meta.name, package.meta.version, package.meta.description))
    conn.commit()
    conn.close()
