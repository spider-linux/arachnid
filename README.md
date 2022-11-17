# The Arachnid Package Manager

The `arachnid` package manager is a package manager for Spider Linux.

### Install Process

Packages are parsed via a [TOML](https://toml.io) file which contains package
information and build instructions. These packages are built and the prefix is
set as `/opt`. The packages are then installed to `/opt` and symlinks are then
set-up by comparing `/opt/package-version/usr/{bin,share,...}` to
`/usr/{bin,share,...}`. This is in similar fashion to [GNU Stow](https://www.gnu.org/software/stow/) but a lot simpler code-wise.
