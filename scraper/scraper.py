from telethon import TelegramClient, sync
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.users import GetFullUserRequest
import re
from .util import to_dict
import json
import datetime
import sys
class Scraper:
    def __init__(self, API_ID, API_HASH, session_name='session_name'):
        self.client = TelegramClient(session_name, API_ID, API_HASH)

    def connect(self):
        self.client.start()

    def get_messages(self, name, file_name,
        verbose=False, count=-1, detail=1, debug=False):
        '''
        Gets information about messages from Telegram group.

        Args:
            name ('str' | 'int')
                username, id, or url of Telegram group
            file_name ('str')
                file to which data will be written
            verbose  ('bool', optional)
                verbose will include all fields
            count ('int', optional)
                how many messages to return total (-1 will return allF)
            detail ([0, 1, 2, 3], optional)
                level of detail to include in stdout:
                - 0 shows when all the function has been completed
                - 1 shows message after each successful API call
                - 2 shows complete JSON object
            debug ('bool', optional)
                enter debug mode, which will display all raw data
        '''
        file = open(file_name, 'w')
        file.write('[\n')
        group = self.client.get_input_entity(name)
        if debug:
            print("entity: " + str(group))
        offset = 0
        total = 0
        trailing_comma = False
        try:
            while True:
                if detail >= 1:
                    print('Getting request...')
                raw = self.client(GetHistoryRequest(
                    peer=group,
                    limit=100,
                    offset_date=None,
                    offset_id=0,
                    max_id=0,
                    min_id=0,
                    add_offset=offset,
                    hash=0))
                try:
                    if raw.messages:
                        if debug:
                            print(to_dict(raw.messages, verbose=verbose))
                        # if the total messages exceed the count, trim the remainder
                        if len(raw.messages) + total >= count and not count == -1:
                            remainder = count - total
                            data = json.dumps(to_dict(raw.messages[:remainder],
                                verbose=verbose), indent=2)[2:-2]
                            total += len(raw.messages[:remainder])
                        # else, dump all messages to the file
                        else:
                            data = json.dumps(to_dict(raw.messages, verbose=verbose),
                                indent=2)[2:-2]
                            total += len(raw.messages)
                        # workaround so no trailing comma at end of file
                        if trailing_comma:
                            file.write(',\n')
                        file.write(data)
                        # levels of info
                        if detail == 2:
                            print(data)
                        if detail >= 1:
                            print('Successfully wrote ' + str(total) + ' messages to file!')
                    else:
                        break
                except Exception as e:
                    print(e)
                    print('Failed to retrieve some messages! Continuing anyways...')
                offset = offset + 100
                if total >= count and not count == -1:
                    break
                trailing_comma = True

        except KeyboardInterrupt:
            print('Process aborted by user!')
        file.write('\n]')
        file.close()
        print('Scraped message data from ' + str(total) + ' messages to: ' + file_name)

    def get_users(self, name, file_name, large=False, count=-1,
        detail=1, debug=False):
        '''
        Gets information about messages from Telegram group.

        Args:
            name ('str' | 'int')
                username, id, or url of Telegram group
            file_name ('str')
                file to which data will be written
            large ('bool', optional)
                due to limitations of the Telegram API, it is impossible
                to retrieve more than 10,000 users in one batch. large will
                go through every letter of the alphabet in an attempt
                to retrieve as many users as possible.
            count ('int', optional)
                how many messages to return total (-1 will return all)
            detail ([0, 1, 2, 3], optional)
                level of detail to include in stdout:
                - 0 shows when all the function has been completed
                - 1 shows message after each successful API call
                - 2 shows complete JSON object
            debug ('bool', optional)
                enter debug mode, which will display all raw data
        '''
        file = open(file_name, 'w')
        group = self.client.get_input_entity(name)
        if debug:
            print('Entity: ' + str(group))
        if count == -1:
            data = self.client.get_participants(group, aggressive=large)
        else:
            data = self.client.get_participants(group, limit=count, aggressive=large)
        if debug:
            print(data)
        to_write = json.dumps(to_dict(data), indent=2)
        if detail == 2:
            print(to_write)
        file.write(to_write)
        file.close()
        print('Scraped user data from ' + str(len(data)) + ' users to: ' + file_name)
