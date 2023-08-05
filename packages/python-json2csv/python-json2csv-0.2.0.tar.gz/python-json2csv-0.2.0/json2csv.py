#!/usr/bin/env python
import os
import io
import csv
import json
import codecs
import click

def dict_select(data, path):
    if path:
        for path in path.split("."):
            data = data[path]
    return data

def data_clean(data, keys):
    new_data = []
    for row in data:
        new_row = []
        if isinstance(row, dict):
            for key in keys:
                new_row.append(row.get(key, ""))
        else:
            new_row = row
        new_data.append(new_row)
    return new_data

def convert(json_text, output, keys, path):
    data = json.loads(json_text)
    data = dict_select(data, path)
    keys = keys and [key.strip() for key in keys.split(",")] or []
    data = data_clean(data, keys)
    writer = csv.writer(output)
    for row in data:
        if not isinstance(row, (list, set, tuple)):
            row = [row]
        writer.writerow(row)
    output.close()

@click.command()
@click.option("-f", "--file", default="-", type=click.File("rb"), help="Input file name, use - for stdin.")
@click.option("--file-encoding", default="utf-8", help="Input file encoding.")
@click.option("-o", "--output", default="-", type=click.File("wb"), help="Output file name, use - for stdout.")
@click.option("--output-encoding", default="utf-8", help="Output file encoding.")
@click.option("-k", "--keys", help="Output field names. Comma separated string list.")
@click.option("-p", "--path", help="Path of the data.")
def main(file, file_encoding, output, output_encoding, keys, path):
    """Convert json array data to csv.
    """
    json_text = file.read().decode(file_encoding)
    output = codecs.getwriter(output_encoding)(output)
    convert(json_text, output, keys, path)

if __name__ == "__main__":
    main()
