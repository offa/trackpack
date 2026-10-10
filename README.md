# Track Pack

[![CI](https://github.com/offa/trackpack/workflows/ci/badge.svg)](https://github.com/offa/trackpack/actions)
[![GitHub release](https://img.shields.io/github/release/offa/trackpack.svg)](https://github.com/offa/trackpack/releases)
[![License](https://img.shields.io/badge/license-GPLv3-yellow.svg)](LICENSE)
![Python 3.10](https://img.shields.io/badge/python-3.10-green.svg)

Packaging of audio / stem files.

A package consists of a required master track with `<project name>.wav` name and optional stem files (`*.wav`).
If no files are passed, all files found in `Export` are packed.

Packed archives are saved to `Export` directory.


## Usage

```sh
# Create package using 'pack.yml':
trackpack pack

# Pack master only
trackpack pack project1.wav stem1.wav stem2.wav

# Pack master and some stems:
trackpack pack project1.wav stem1.wav stem2.wav
```

Use `trackpack --help` for full usage documentation.


### YAML config format

The YAML configuration uses the same format as the CLI arguments, but `_` instead of `-`:

```yaml
# Required:
name: "project name"

# Optional:
archive_name: "package_archive_name"    # Default: Same as required 'name' ('.zip' is optional)
append_date: True                       # Default: False
```

CLI arguments to have higher priority and override file settings.
