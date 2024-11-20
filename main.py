# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import gzip
import json
import csv


def get_leaf_nodes(obj, leaves=None):

    if leaves is None:
        leaves = []

    if isinstance(obj, dict):  # If the object is a dictionary
        for value in obj.values():
            get_leaf_nodes(value, leaves)
    elif isinstance(obj, list):  # If the object is a list
        for item in obj:
            get_leaf_nodes(item, leaves)
    else:  # If it's a leaf node (not dict or list)
        leaves.append(obj)

    return leaves


def get_type_values(obj, result=None):
    if result is None:
        result = []

    if isinstance(obj, dict):
        # If it's a dictionary, check each key
        for key, value in obj.items():
            if key == "type" and isinstance(value, str):  # If key is 'type', add its value
                result.append(value)
            else:
                # Recursively check for nested dictionaries
                get_type_values(value, result)
    elif isinstance(obj, list):
        # If it's a list, recursively check each item
        for item in obj:
            get_type_values(item, result)

    return result


def open_gz(filename):
    # Open and read the .json.gz file
    with gzip.open(filename, 'rt', encoding='utf-8') as f:
        return json.load(f)


def read_csv_names(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header line
        names = [row[0] for row in reader]
    return names


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    json_data = open_gz("flow.json.gz")

    # Extract all values for key 'type'
    type_values = get_type_values(json_data)
    components = list(filter(lambda x: (x != "FUNNEL" and x != "PROCESSOR"),
                             map(lambda x: x.split(".")[-1], type_values)))

    deprecated_list = read_csv_names("deprecated.csv")
    # print(deprecated_list)
    # print(components)
    intersection = list(set(components).intersection(deprecated_list))
    print(intersection)