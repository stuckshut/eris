USER = ''
PASS = ''
ADMIN_ROLE = 'Admin'
UNAUTHORIZED_MSG = 'You do not have the required permissions to perform ' \
                   'that action.'
CHANNEL_REQUIRED_MSG = 'This action must be performed from a channel.'
DEFAULT_DIE_ROLL = '1d6'

try:
    from settingslocal import *
except ImportError:
    pass
