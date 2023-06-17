import argparse as argparse
import re

import pandas as pd
import numpy as np
import json

def remove_underscore_numbers(string):
    # Regular expression pattern to match underscore and numbers
    pattern = r"_\d+"


    if re.search(pattern, string):
        # Remove underscore and numbers using regex substitution
        processed_string = re.sub(pattern, "", string)

    else:
        processed_string = string

    return processed_string

if __name__ == '__main__':
    argparse = argparse.ArgumentParser()
    argparse.add_argument('input', type=str)
    argparse.add_argument('layer', type=int)
    file=argparse.parse_args().input
    layer=argparse.parse_args().layer
    processed=[]
    df = pd.read_csv('zelda-totk.hashes.csv', sep=';', lineterminator='\n', header=None, names=['hash', 'type', 'id','status'])
    with open(file, 'r') as f:
        data = json.load(f)
        with open(f'locations_{layer}.txt', 'a') as f:
            for item in data:
                id = item["id"]
                name=item["name"]
                if name in processed:
                    continue
                hash=f'IsVisitLocation.{id}'
                found_row = df.loc[df.iloc[:, 2] == hash, df.columns[0]].tolist()
                if found_row:
                    found_row = found_row[0].upper()
                    converted = int(found_row.upper(),16)
                    f.write(f'Data::Location({converted}, \"{item["name"]}\", {float(item["x"])}f, {float(item["y"])}f, {float(item["z"])},{layer}),\n')
                    processed.append(id)
                else:
                    print(f'Could not find {id} {name}')
    print(f'Processed {len(processed)} locations')

