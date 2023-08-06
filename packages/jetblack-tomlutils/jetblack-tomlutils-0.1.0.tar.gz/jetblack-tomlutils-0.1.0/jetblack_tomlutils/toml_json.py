"""Convert TOML to JSON"""

from datetime import date, datetime
import json
import sys
from typing import Any, Dict

import qtoml

class _TomlDecoder(json.JSONEncoder):
    def default(self, obj): # pylint: disable=arguments-differ,method-hidden
        if isinstance(obj, date):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj) # pylint: disable=no-member

def _as_datetime(value):
    try:
        return datetime.fromisoformat(value)
    except: # pylint: disable=bare-except
        return value

def _load_toml(filename: str) -> Dict[str, Any]:
    if filename == '-':
        return qtoml.load(sys.stdin)
    with open(filename, 'rt') as file_ptr:
        return qtoml.load(file_ptr)

def _load_json(filename: str) -> Dict[str, Any]:
    if filename == '-':
        return json.load(sys.stdin, object_hook=_as_datetime)
    with open(filename, 'rt') as file_ptr:
        return json.load(file_ptr, object_hook=_as_datetime)
        

def _to_json(input_filename: str = '-', output_filename: str = '-'):
    content = _load_toml(input_filename)
    if output_filename == '-':
        json.dump(content, sys.stdout, cls=_TomlDecoder)
    else:
        with open(output_filename, 'wt') as file_ptr:
            json.dump(content, file_ptr, cls=_TomlDecoder)

def _from_json(input_filename: str = '-', output_filename: str = '-'):
    content = _load_json(input_filename)
    if output_filename == '-':
        qtoml.dump(content, sys.stdout)
    else:
        with open(output_filename, 'wt') as file_ptr:
            qtoml.dump(content, file_ptr, cls=_TomlDecoder)

def _convert(func):
    if len(sys.argv) == 1:
        func()
    elif len(sys.argv) == 2:
        func(sys.argv[1])
    elif len(sys.argv) == 3:
        func(sys.argv[1], sys.argv[2])
    else:
        print(f"""usage:
    {sys.argv[0]} [<input> [<output>]]

    input/output: either a path or '-' for stdin/stdout
""", file=sys.stderr)

def toml2json():
    _convert(_to_json)

def json2toml():
    _convert(_from_json)
