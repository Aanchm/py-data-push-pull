import csv
import pandas as pd
import os
import json
import glob


def get_file_list_containing_strings(str_list, data_path):

    all_files = os.listdir(data_path)
    selected_files = [file for str in str_list for file in all_files if str in file]

    return selected_files


def load_dictionary_from_json(file, ignore_fields_list):

    with open(file, 'r') as file:
        read_lines = file.readlines()

        for line in read_lines:
            dictionary = line.replace(' ', '')

        file.close()
   
    dictionary = json.loads(dictionary[:-1])
    for field in ignore_fields_list:
        del dictionary[field]

    return dictionary


def get_most_recent_file(data_path, file_extension):

    file_path = f"{data_path} _*{file_extension}"
    data_file = max(glob.iglob(file_path), key=os.path.getctime)

    return data_file


def combine_files(files):
    data = pd.DataFrame()

    for file in files:
        new_data = pd.read_csv(file)
        data = pd.concat([data, new_data], ignore_index = True)
    
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
    return data


def append_dictionary_to_csv(file, dictionary):

    fields = list(dictionary.keys())

    if not os.path.isfile(file):
        with open(file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
    
    with open(file, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writerow(dictionary)
        print(f"Stats Appended: {file}")

