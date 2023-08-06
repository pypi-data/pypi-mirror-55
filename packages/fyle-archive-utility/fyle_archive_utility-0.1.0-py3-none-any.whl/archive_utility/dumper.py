"""
Dumper file used to dump data to CSV or JSON format
"""
import csv
import json
import os
import logging
from datetime import datetime
import click

logger = logging.getLogger('FyleConnector')


class Dumper:
    """
    Used to Dump the expenses data into a CSV or JSON file
    """
    @staticmethod
    def dump_csv(data, path):
        """
        :param data: Takes existing Expenses Data, that match the parameters
        :param path: Takes the path of the file
        :return: CSV file with the list of existing Expenses, that match the parameters
        """
        try:
            filename = path + '/{0}--Date--{1}.csv'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename.format(data[0]['org_name'], datetime.now()), 'w') as export_file:
                logger.info('Downloading data from Fyle in CSV format.')
                keys = data[0].keys()
                dict_writer = csv.DictWriter(export_file, fieldnames=keys, delimiter=',')
                dict_writer.writeheader()
                dict_writer.writerows(data)
                click.echo('Download Successful !')
        except:
            click.echo('Some of the parameters are wrong')

    @staticmethod
    def dump_json(data, path):
        """
        :param data: Takes existing Expenses Data, that match the parameters
        :param path: Takes the path of the file
        :return:  JSON file with the list of existing Expenses, that match the parameters
        """
        try:
            filename = path + '/{0}--Date--{1}.json'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename.format(data[0]['org_name'], datetime.now()), 'w') as export_file:
                logger.info('Downloading data from Fyle in JSON format.')
                json.dump(data, export_file, indent=4, sort_keys=True)
                click.echo('Download Successful !')
        except:
            click.echo('Some of the parameters are wrong')
