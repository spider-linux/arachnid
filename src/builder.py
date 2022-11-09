import shutil
import parser
import os
import urllib.request
import mimetypes

def get_sources(build_file, build_directory):
    for source in package.sources.urls:
        print(f"downloading from {source}")
        *_, source_file = source.split("/")
        urllib.request.urlretrieve(source, os.path.join(build_directory, source_file))

def build_package(build_file):
    archives_for_removal = []

    build_directory = os.path.join("/tmp", "arachnid", "build")

    if os.path.exists(build_directory):
        print(f"{build_directory} exists already, removing")
        shutil.rmtree(build_directory, ignore_errors=False)

    print(f"creating {build_directory}")

    os.makedirs(build_directory)

    print(f"moving into {build_directory}")
    os.chdir(build_directory)

    get_sources(build_file, build_directory)

    print(f"extracting archives in {build_directory}")
    extracted_dir_name = package.meta.name + "-" + str(package.meta.version)
    with os.scandir(build_directory) as dir:
        for entry in dir:
            try:
                shutil.unpack_archive(entry.name, extracted_dir_name)
                archives_for_removal.append(entry.path)
            except ValueError:
                continue

    for archive in archives_for_removal:
        print(f"deleting {archive}")
        os.remove(archive)

    print(f"moving into extracted directory {extracted_dir_name}")
    os.chdir(extracted_dir_name)

    commands = [command for command in package.build.install]
    print(commands)
    os.system(" && ".join(commands))

package = parser.parse_build_file("bash-example.toml")
build_package("bash-example.toml")
