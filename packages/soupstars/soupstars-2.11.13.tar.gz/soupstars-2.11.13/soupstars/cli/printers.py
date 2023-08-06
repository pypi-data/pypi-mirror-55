import json

from pygments import highlight, lexers, formatters
from terminaltables import SingleTable

pygments_style = "native"


def jsonify(data):
    formatted_json = json.dumps(data, sort_keys=True, indent=2)
    colorful_json = highlight(
        formatted_json,
        lexers.JsonLexer(),
        formatters.Terminal256Formatter(style=pygments_style)
    )
    print(colorful_json)


def pythonify(module):
    result = highlight(
        module,
        lexers.PythonLexer(),
        formatters.Terminal256Formatter(style=pygments_style)
    )
    print(result)


def tableify(headers, rows):
    data = [headers]
    for row in rows:
        row = [str(item) for item in row]
        data.append(row)
    table = SingleTable(data)
    print(table.table)
