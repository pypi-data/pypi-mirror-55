import logging
from collections import namedtuple

jim_keys = namedtuple('JIM', ('ACTION', 'TIME', 'USER', 'SENDER', 'RECEIVER',
                              'FRIEND', 'CONTACTS', 'KEY', 'AUTH_DATA'))
"""Ключи протокола"""
proto_keys = namedtuple('PROTO', ('PRESENCE', 'RESPONSE', 'ERROR', 'MESSAGE',
                                  'MESSAGE_TEXT', 'EXIT', 'DESCRIPTION',
                                  'ADD_CONTACT', 'DEL_CONTACT', 'GET_CONTACTS',
                                  'UPDATE_CONTACTS', 'KEY_EXCHANGE',
                                  'USERNAME', 'PASSWORD'))
"""Значения ключей протокола"""
interface_commands = namedtuple('COMMANDS', ('MESSAGE', 'EXIT'))
"""Команды вводимые в интерфейсе"""
user_status = namedtuple("STATUS", ('ONLINE', 'OFFLINE'))
mode = namedtuple('MODE', ('SEND', 'LISTEN'))
DEF_LISTEN_ADDR = ''
DEF_SERVER_ADDR = '127.0.0.1'
DEF_LISTEN_PORT = 7777
DEF_SERVER_PORT = 7777
MAX_CONNECTIONS = 25
PACKAGE_LENGTH = 4096
ENCODING = 'utf-8'
JIM = jim_keys('action', 'time', 'user', 'sender', 'receiver', 'friend',
               'contacts', 'key', 'auth_data')
PROTO = proto_keys('presence', 'response', 'error', 'message', 'message_text',
                   'exit', 'description', 'add_contact',
                   'del_contact', 'get_contacts', 'update_contacts',
                   'key_exchange', 'username', 'password')
MODE = mode('send', 'listen')
COMMAND = interface_commands('message', 'exit')
USER_STATUS = user_status('online', 'offline')
LOGGING_LEVEL = logging.DEBUG
