# Todoget

- [Todoget](#todoget)
  - [Usage](#usage)
  - [Configuration file](#configuration-file)
    - [General configuration](#general-configuration)
    - [Patterns to track](#patterns-to-track)

`todoget` is a simple python script to keep track of `tags` from plain text files. The idea is similar to available tools from common IDEs with more customization and a minimal approach.

## Usage

There are two main arguments `init` and `scan`:

- `init` create the `.todoget` configuration file in the current working directory in `yaml` format.
- `scan` read the configuration file, scan selected files and create an `*.txt` file with lines matching the extracted patterns.

## Configuration file

### General configuration

The configuration file is a `.yml` file that can be easily customized creating custom tags and adding files to track.

The standard configuration file is:

```
config:
  include_all_files: false
  outfile: outfile.txt
  include_files:
  - 'file1'
  - 'file2'
  - ...
  exclude_files:
  - 'file1'
  - 'file2'
  - ...
todo:
  active: true
  name: todo
  pattern: TODO
```

The first entry is the general configuration file (`config`). The options are:

- **include_all_files** (`true` or `false`): as defalt the tool track only selected files. If `true` all non-hidden files and folders in the current directory and subdirectories are analyzed.
- **outfile** (`string`): the name of the output file
- **include_files** (bullet list of `strings`): file/s to scan. Adding more files as bullet list using `-`
- **exclude_files** (bullet list of `strings`): file/s to exclude. This is only relevant if the `include_all_files = True` but there are still some files to exclude. Useful when the amount of to-be-included files is greater than the to-be-included files. As default, the `outfile.txt` file is excluded.

### Patterns to track

As default, the `todoget` track the `TODO` tag. In order to add a custom tag is necessary to use the `todo` tag template:

```
tagname:
  active: true or false
  name: tagname
  pattern: PATTERN (the exact string to search)
```