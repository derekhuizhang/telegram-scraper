from .validators import *

RETRY = [
    {
        'name': 'CONTINUE',
        'type': 'confirm',
        'message': 'Try again? (default=N)',
        'default': False,
    }
]

API_INFO = [
    {
        'name': 'API_ID',
        'type': 'input',
        'message': 'What is your API ID?'
    },
    {
        'name': 'API_HASH',
        'type': 'input',
        'message': 'What is your API hash?'
    }
]

COMMAND = [
    {
        'name': 'TYPE',
        'type': 'list',
        'message': 'Do you want to get users or messages?',
        'choices': ['Users', 'Messages']
    }
]

MESSAGE_DETAILS = [
    {
        'name': 'ID',
        'type': 'input',
        'message': 'What is the ID, username, or URL of the group?'
    },
    {
        'name': 'FILE_NAME',
        'type': 'input',
        'message': 'What file do you want to write to (default=data.txt)?',
        'default': 'data.txt'
    },
    {
        'name': 'VERBOSE',
        'type': 'confirm',
        'message': 'Include all, including null, fields? (default=N)',
        'default': False
    },
    {
        'name': 'COUNT',
        'type': 'input',
        'message': 'How many objects to retrieve? (-1 will retrieve all; default=-1)',
        'default': '-1',
        'validate': CountValidator
    },
    {
        'name': 'DETAIL',
        'type': 'list',
        'message': 'How much detail to include in stdout?',
        'choices': ['0', '1', '2']
    }
]

USER_DETAILS = [
    {
        'name': 'FILE_NAME',
        'type': 'input',
        'message': 'What file do you want to write to (default=data.txt)?',
        'default': 'data.txt'
    },
    {
        'name': 'ID',
        'type': 'input',
        'message': 'What is the ID, username, or URL of the group?'
    },
    {
        'name': 'LARGE',
        'type': 'confirm',
        'message': 'More than 10,000 users? (Y/N; default=N will retrieve 10,000 users)',
        'default': False
    },
    {
        'name': 'COUNT',
        'type': 'input',
        'message': 'How many objects to retrieve? (-1 will retrieve all; default=-1)',
        'default': '-1',
        'validate': CountValidator
    },
    {
        'name': 'DETAIL',
        'type': 'list',
        'message': 'How much detail to include in stdout?',
        'choices': ['0', '1', '2']
    }
]
