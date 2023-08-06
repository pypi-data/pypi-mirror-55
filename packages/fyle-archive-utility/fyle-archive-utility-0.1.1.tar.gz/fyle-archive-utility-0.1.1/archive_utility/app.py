"""
Fyle-Archive-Utility
"""
import logging
import os
import json
import click
from archive_utility.dumper import Dumper
from archive_utility.fyle_connection import FyleConnector

logger = logging.getLogger('FyleArchiveUtility')


@click.group()
@click.version_option(version='0.01', prog_name='Fyle-Archive-Utility')
def main():
    """  Fyle Archive Utility """


# Using this command to get FYLE credentials and store them in a json file
@main.command()
@click.option('--client_id', prompt='client_id', help='Enter Your CLIENT_ID')
@click.option('--client_secret', prompt='client_secret', help='Enter Your CLIENT_SECRET')
@click.option('--refresh_token', prompt='refresh_token', help='Enter Your REFRESH_TOKEN')
@click.option('--base_url', prompt='base_url', help='Enter Your BASE_URL')
def connect(client_id, client_secret, refresh_token, base_url):
    """
    :param client_id: Client ID for Fyle API.
    :param client_secret: Client secret for Fyle API.
    :param refresh_token: Refresh Token for Fyle API.
    :param base_url: BaseURL.
    """
    cred_file = os.path.expanduser('~/.config.json')
    with open(cred_file, 'w') as handler:
        json.dump({'client_id': client_id, 'client_secret': client_secret, 'refresh_token': refresh_token,
                   'base_url': base_url}, handler, sort_keys=True, indent=4)
        handler.close()
        logger.info('Your FYLE credentials are saved.')


@main.command()
@click.option('--file_format', help="Enter the format of the file 'csv' or 'json' ", required=True)
@click.option('--state', help="Enter the state of Expenses [ 'PAID' , 'APPROVED' ]")
@click.option('--path', help='Enter the directory where you want to save your file', required=True)
def expenses(file_format, state, path):
    """

    :param format: format of the file to be generated 'CSV' or 'JSON'
    :param state:  state of the Expense [ 'PAID' , 'DRAFT' , 'APPROVED' , 'APPROVER_PENDING' , 'COMPLETE' ]
    :param path:   Takes the path of the file to save the data.
    """
    if file_format == 'json':
        response_data = fyle_connection.extract_expenses(state=state)
        logger.info('Downloading data from Fyle in JSON format.')
        Dumper.dump_json(response_data, path)
    elif file_format == 'csv':
        response_data = fyle_connection.extract_expenses(state=state)
        logger.info('Downloading data from Fyle in CSV format.')
        Dumper.dump_csv(response_data, path)
    else:
        logger.warning('Some of the parameters are wrong')


if __name__ == "__main__":
    # Extracting FYLE Credentials from the json file
    try:
        path_to_json = os.path.expanduser('~/.config.json')
        with open(path_to_json, 'r') as config_file:
            credentials = json.load(config_file)
            config_file.close()
        CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, BASE_URL = credentials['client_id'], credentials['client_secret'], credentials['refresh_token'], credentials['base_url']
        # Make connection with FYLE using the above credentials
        fyle_connection = FyleConnector(
            CLIENT_ID, CLIENT_SECRET, BASE_URL, REFRESH_TOKEN)
    except:
        click.echo(click.style('Please make connection with FYLE', fg='red'))
    main()
