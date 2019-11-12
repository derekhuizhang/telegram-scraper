import click
from pprint import pprint
from .scraper import *
from .util import *
from .commands import *
from .errors import *
import sys
import time
import configparser
import os

@click.command()
@click.option('--config', default=False, help='Config file path')
@click.option('--debug', is_flag='True', help='Show detailed debug information')
def main(config, debug):

    # Retrieve proper API ID and hash
    if config:
        if debug:
            print('Config file: ' + config)
        try:
            parser = configparser.ConfigParser()
            parser.read(config)
            user = {
                'API_ID': parser['API']['ID'],
                'API_HASH': parser['API']['HASH']
            }
        except Exception as e:
            print(e)
            print(CONFIG_ERROR)
            sys.exit(1)
    else:
        user = prompt_info(API_INFO)

    # Connect to Telegram
    while True:
        try:
            if debug:
                print('User: ' + str(user))
            scraper = Scraper(user['API_ID'], user['API_HASH'])
            scraper.connect()
            print('Successfully connected to Telegram...')
            break
        except Exception as e:
            print(e)
            print(AUTH_ERROR)
            retry = prompt_info(RETRY)
            if retry['CONTINUE']:
                user = prompt_info(API_INFO)
                continue
            else:
                sys.exit(1)

    # Retrieve proper info
    while True:
        command = prompt_info(COMMAND)

        # Retrieve messages
        if (command['TYPE'] == 'Messages'):
            message_config = prompt_info(MESSAGE_DETAILS)
            if debug:
                print('Command: ' + str(command))
                print('Message retrieval config: ' + str(message_config))
            try:
                scraper.get_messages(message_config['ID'], message_config['FILE_NAME'],
                    verbose=message_config['VERBOSE'],
                    count=int(message_config['COUNT']),
                    detail=int(message_config['DETAIL']),
                    debug=debug)
            except Exception as e:
                print(e)
                print(RETRIEVAL_ERROR)

            retry = prompt_info(RETRY)
            if retry['CONTINUE']:
                continue
            else:
                sys.exit(1)

        # Retrieve users
        if (command['TYPE'] == 'Users'):
            user_config = prompt_info(USER_DETAILS)
            if debug:
                print('Command: ' + str(command))
                print('User retrieval config: ' + str(user_config))
            try:
                scraper.get_users(user_config['ID'], user_config['FILE_NAME'],
                    count=int(user_config['COUNT']),
                    detail=int(user_config['DETAIL']),
                    large=user_config['LARGE'],
                    debug=debug)
            except Exception as e:
                print(e)
                print('Error: Did not successfully retrieve data.')
            retry = prompt_info(RETRY)
            if retry['CONTINUE']:
                continue
            else:
                sys.exit(1)

if __name__ == '__main__':
    main()
