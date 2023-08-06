# bhdg-toml

Some utilities for working with toml files.

## Usage

To convert toml to json:

```bash
$ toml2json < pyproject.toml > pyproject.json
$ toml2json pyproject.toml > pyproject.json
$ toml2json pyproject.toml - > pyproject.json
$ toml2json pyproject.toml pyproject.json
$ cat pyproject.toml | toml2json
$ cat pyproject.toml | toml2json -
```
To convert json to toml:

```bash
$ json2toml < pyproject.json
$ json2toml pyproject.json
$ cat pyproject.toml | json2toml
$ cat pyproject.toml | json2toml -
```