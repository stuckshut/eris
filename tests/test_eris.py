from unittest import TestCase
from unittest.mock import MagicMock

import eris


class ErisTest(TestCase):
    """Tests the eris.py module"""

    def setUp(self):
        eris.client = MagicMock()

    def tearDown(self):
        pass

    def test_on_ready(self):
        # Nothing really happens here...
        eris.print = MagicMock()
        eris.on_ready()
        self.assertTrue(eris.print.called)

    def test_on_message_self_message(self):
        # Test setup items
        msg = MagicMock()
        eris.commands.get_command_from_list = MagicMock()

        # self_sent_message setup
        msg.author.id = 10
        eris.client.user.id = 10

        eris.on_message(msg)
        eris.commands.get_command_from_list.assert_not_called()

    def test_on_message_wrong_command(self):
        # Setup items
        msg = MagicMock()
        eris.client.send_message = MagicMock()

        # No command found setup
        eris.commands.get_command_from_list = MagicMock(return_value=None)

        eris.on_message(msg)
        eris.commands.get_command_from_list.assert_called_with(msg)
        eris.client.send_message.assert_not_called()

    def test_on_message_channel_required(self):
        # Test setup items
        msg = MagicMock()
        command = MagicMock()
        eris.commands.get_command_from_list = MagicMock(return_value=command)
        eris.client.send_message = MagicMock()

        # Channel_required setups
        command.channel_required = True
        eris.is_direct_message = MagicMock(return_value=True)

        eris.on_message(msg)
        eris.client.send_message.assert_called_with(msg.channel, eris.settings.CHANNEL_REQUIRED_MSG)

    def test_on_message_admin_required(self):
        # Test setup items
        msg = MagicMock()
        command = MagicMock()
        eris.commands.get_command_from_list = MagicMock(return_value=command)
        eris.client.send_message = MagicMock()

        # admin_required setups
        command.admin_required = True
        eris.message_is_from_admin = MagicMock(return_value=False)

        eris.on_message(msg)
        eris.client.send_message.assert_called_with(msg.channel, eris.settings.UNAUTHORIZED_MSG)

    def test_on_message_execute_message(self):
        # Test setup items
        msg = MagicMock()
        command_classes = MagicMock()
        command = command_classes[0].return_value
        command.execute = MagicMock(name="method")
        command.execute.return_value = MagicMock()
        eris.commands.get_command_from_list = MagicMock(return_value=command_classes)
        eris.client.send_message = MagicMock()

        # command requirement setups
        command.channel_required = False
        command.admin_required = False
        eris.is_direct_message = MagicMock(return_value=False)
        eris.message_is_from_admin = MagicMock(return_value=True)

        eris.on_message(msg)
        command.execute.assert_called_once_with()
        eris.client.send_message.assert_called_once_with(msg.channel, command.execute.return_value)

    def test_message_is_from_admin(self):
        message = MagicMock()
        role = MagicMock()
        role.name = eris.settings.ADMIN_ROLE

        message.author.roles = [role]
        self.assertTrue(eris.message_is_from_admin(message))

        message.author.roles = []
        self.assertFalse(eris.message_is_from_admin(message))

    def test_message_is_direct_message(self):
        message = MagicMock()

        message.author = MagicMock(eris.discord.User)
        self.assertTrue(eris.is_direct_message(message))

        message.author = False
        self.assertFalse(eris.is_direct_message(message))
