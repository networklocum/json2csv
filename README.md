# JSON2CSV

Consumes a paginated JSON endpoint response and turns it into a csv file.

## Installation

    git clone https://github.com/evidens/json2csv.git
    cd json2csv
    pip install -r requirements.txt

## How it works

1. Consumes an endpoint string.
2. Hits that endpoint to get #1 The data schema. #2 The first set of results. Writes the first set of results to a new csv file.
3. Hits the next page and writes to the csv file until there are no more pages.
4. TODO: Checks the number of rows against the expected number of rows (gathered from first endpoint access).
5. TODO: Checks for duplicate rows.
6. TODO: Writes above metadata to the report.

## Example endpoint format:

```javascript
{
"count": 1337,
"next": "some_url&page=2",
"previous": null,
"results": [
{
"id": 1,
"contacts": [
{
"id": 89
}
]
},
{
"id": 2,
"contacts": [
{
"id": 82
},
{
"id": 4867
}
]
},
{
"id": 3,
"contacts": [
{
"id": 82
}
]
},
{
"id": 4,
"contacts": [
{
"id": 89
}
]
},
{
"id": 5,
"contacts": [
{
"id": 89
}
]
},
{
"id": 6,
"contacts": [
{
"id": 89
}
]
},
{
"id": 7,
"contacts": [
{
"id": 89
}
]
},
{
"id": 8,
"contacts": [
{
"id": 89
}
]
},
{
"id": 10,
"contacts": [
{
"id": 89
}
]
},
{
"id": 12,
"contacts": [
{
"id": 7664
}
]
}
],
"next_page": 2,
"previous_page": null
}
```

## Original Usage

Basic (convert from a JSON file to a CSV file in same path):

    python json2csv.py /path/to/json_file.json /path/to/outline_file.json

Specify CSV file

    python json2csv.py /path/to/json_file.json /path/to/outline_file.json -o /some/other/file.csv


For this JSON file:

    {
      "nodes": [
        {"source": {"author": "Someone"}, "message": {"original": "Hey!", "Revised": "Hey yo!"}},
        {"source": {"author": "Another"}, "message": {"original": "Howdy!", "Revised": "Howdy partner!"}},
        {"source": {"author": "Me too"}, "message": {"original": "Yo!", "Revised": "Yo, 'sup?"}}
      ]
    }

Use this outline file:

    {
      "map": [
        ["author", "source.author"],
        ["message", "message.original"]
      ],
      "collection": "nodes"
    }

## Generating outline files

To automatically generate an outline file from a json file:

    python gen_outline.py --collection nodes /path/to/the.json

This will generate an outline file with the union of all keys in the json
collection at `/path/to/the.outline.json`.  You can specify the output file
with the `-o` option, as above.

## Unquoting strings

To remove quotation marks from strings in nested data types:

    python json2csv.py /path/to/json_file.json /path/to/outline_file.json --strings

This will modify field contents such that:

    {
      "sandwiches": ["ham", "turkey", "egg salad"],
      "toppings": {
        "cheese": ["cheddar", "swiss"],
        "spread": ["mustard", "mayonaise", "tapenade"]
        }
    }

Is parsed into

|sandwiches            |toppings                                                       |
|:---------------------|:--------------------------------------------------------------|
|ham, turkey, egg salad|cheese: cheddar, swiss<br>spread: mustard, mayonaise, tapenade|

The class variables `SEP_CHAR`, `KEY_VAL_CHAR`, `DICT_SEP_CHAR`, `DICT_OPEN`, and `DICT_CLOSE` can be changed to modify the output formatting. For nested dictionaries, there are settings that have been commented out that work well. 
