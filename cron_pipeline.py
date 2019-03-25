#!/Users/eric/anaconda3/bin/python3

import json
import subprocess

# result = subprocess.check_output("/anaconda3/bin/pip3 install pydomo", universal_newlines=True, shell=True) 



from pydomo import Domo
from pydomo.datasets import Sorting, DataSetRequest, Schema, Column, ColumnType
import logging



import sys

def run_pipeline(working_dir='.', program_dir='/Users/eric/anaconda3/bin/'):
    
    ####################################
    #   Create Link to Domo Instance   #
    ####################################

    # read the secret, client_id, and scope
    client_secret = None
    scope = None
    client_id = None
    api_host = 'api.domo.com'

    with open("secret.txt", 'r') as secret_file:
        client_secret = secret_file.read().strip()

    with open("client.txt", 'r') as client_file:
        client_id = client_file.read().strip()

    with open("scope.txt", 'r') as scope_file:
        scope = scope_file.read().strip()

    # link to domo instance
    domo = Domo(client_id, client_secret, logger_name="Eric", log_level=logging.INFO, api_host=api_host)

    ################################################
    #   Find Our Dataset Without Knowing It's ID   #
    ################################################

    # get the input and output datasets
    to_find = ['BASE|ERIC|Billboard Top 10','BASE|ERIC|Billboard Top 10 OUTPUT']

    def find_datasets_by_name(dataset_names, domo):
        datasets = list(domo.datasets.list())
        results = dict()
        for dataset in datasets:
            if dataset['name'] in dataset_names:
                results[dataset['name']] = dataset
        return results

    # datasets = find_datasets_by_name(to_find, domo)

    ####################################
    #         Read in all data         #
    ####################################

    include_csv_header = True
    csv_file_path = './input.csv'
    csv_download = domo.datasets.data_export_to_file(
    #     datasets['BASE|ERIC|Billboard Top 10 OUTPUT']['id']
        'e9d1c87f-6640-421b-9d13-4ad92f9ea525', csv_file_path, include_csv_header)

    ####################################
    #           Run R Script           #
    ####################################

    r_script_path = 'script_for_domo.R'
    # r_script_path = './script_for_domo.R'
    command = program_dir + 'Rscript'
    outfile_name = 'output.csv'
    args = [working_dir, csv_file_path, outfile_name] # could place several command arguments here
    cmd = [command, r_script_path] + args

    # run the command and store result
    result = subprocess.check_output(cmd, universal_newlines=True) 
    # universal newlines tells python to interpret returned output as a string
    # and handle both windows and linux newline characters

    #################################################
    #  Replace Target Dataset in DOMO with new Data #
    #################################################

    domo.datasets.data_import_from_file(
    #     datasets['BASE|ERIC|Billboard Top 10 OUTPUT']['id'], 
        'e9d1c87f-6640-421b-9d13-4ad92f9ea525', outfile_name, update_method='REPLACE')
    
    print("Pipeline ran successfully!")

# run!
run_pipeline()