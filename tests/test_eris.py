from unittest import TestCase
from unittest.mock import patch, MagicMock

import eris


class ErisTest(TestCase):
    """Tests the eris.py module"""

    def setUp(self):
        self.message = MagicMock()
        self.message.author.id = 10
        eris.client = MagicMock()
        eris.client.user.id = 20

    @patch("eris.print")
    def test_on_ready(self, mock_print):
        # Nothing really happens here...
        eris.on_ready()
        self.assertTrue(mock_print.called)

    @patch("eris.commands.get_command_from_list", MagicMock())
    def test_on_message_self_message(self):
        self.message.author.id = 20

        eris.on_message(self.message)
        eris.commands.get_command_from_list.assert_not_called()

    @patch("eris.client.send_message", MagicMock())
    @patch("eris.commands.get_command_from_list", MagicMock(return_value=None))
    def test_on_message_wrong_command(self):
        eris.on_message(self.message)
        eris.commands.get_command_from_list.assert_called_with(self.message)
        eris.client.send_message.assert_not_called()

    @patch("eris.commands.get_command_from_list", MagicMock(return_value=MagicMock(channel_required=True)))
    @patch("eris.client.send_message", MagicMock())
    @patch("eris.is_direct_message", MagicMock(return_value=True))
    def test_on_message_channel_required(self):
        eris.on_message(self.message)
        eris.client.send_message.assert_called_with(self.message.channel, eris.settings.CHANNEL_REQUIRED_MSG)

    @patch("eris.commands.get_command_from_list", MagicMock(return_value=MagicMock(admin_required=True)))
    @patch("eris.client.send_message", MagicMock())
    @patch("eris.message_is_from_admin", MagicMock(return_value=False))
    def test_on_message_admin_required(self):
        eris.on_message(self.message)
        eris.client.send_message.assert_called_with(self.message.channel, eris.settings.UNAUTHORIZED_MSG)

    @patch("eris.message_is_from_admin", MagicMock(return_value=True))
    @patch("eris.is_direct_message", MagicMock(return_value=False))
    @patch("eris.commands.HelpCommand.execute", MagicMock(return_value="help message!"))
    @patch("eris.client.send_message", MagicMock())
    def test_on_message_execute_message(self):
        self.message.content = "!help"

        eris.on_message(self.message)
        eris.client.send_message.assert_called_once_with(self.message.channel, eris.commands.HelpCommand.execute())

    def test_message_is_from_owner(self):
        message = MagicMock()

        message.author.id = 10
        message.server.owner = 10
        self.assertTrue(eris.message_is_from_server_owner(message))

        message.server.owner = 20
        self.assertFalse(eris.message_is_from_server_owner(message))

    def test_message_is_from_admin(self):
        role = MagicMock()
        role.name = eris.settings.ADMIN_ROLE

        self.message.author.roles = [role]
        self.assertTrue(eris.message_is_from_admin(self.message))

        self.message.author.roles = []
        self.assertFalse(eris.message_is_from_admin(self.message))

    def test_message_is_direct_message(self):
        self.message = MagicMock()

        self.message.channel = MagicMock(eris.discord.Channel)
        self.assertFalse(eris.is_direct_message(self.message))

        self.message.channel = MagicMock(eris.discord.PrivateChannel)
        self.assertTrue(eris.is_direct_message(self.message))
