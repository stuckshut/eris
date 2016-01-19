from unittest import TestCase
from unittest.mock import patch, MagicMock

import actions.admin_commands


class JoinServerCommand(TestCase):

    def test_join_server_command_object(self):
        client = MagicMock()
        client.accept_invite = MagicMock()
        message = MagicMock(content='.join')
        join_cmd = actions.admin_commands.JoinServerCommand(client, message)
        self.assertEqual(join_cmd.command, '.join')
        self.assertEqual(join_cmd.help_message, '.join - Join a server given an invite link')

    def test_join_server_command_execute(self):
        client = MagicMock()
        message = MagicMock(content='.join')

        # No args
        join_cmd = actions.admin_commands.JoinServerCommand(client, message)
        self.assertEqual(join_cmd.execute(), 'What do you want me to join?')

        # Server problem or expired invite
        client.accept_invite.side_effect = actions.HTTPException(MagicMock())
        message.content = '.join http://null.null/123123123'
        join_cmd = actions.admin_commands.JoinServerCommand(client, message)
        self.assertEqual(join_cmd.execute(), 'I couldn\'t accept that request for some reason')

        # Invalid arg
        client.accept_invite.side_effect = actions.InvalidArgument()
        message.content = '.join 2t94awgh-348yq3=4tq34=8tqa='
        join_cmd = actions.admin_commands.JoinServerCommand(client, message)
        self.assertEqual(join_cmd.execute(), 'That is not a valid request')

    def test_leave_server_command_object(self):
        client = MagicMock()
        message = MagicMock(content='.leave')
        leave_cmd = actions.admin_commands.LeaveServerCommand(client, message)

        self.assertEqual(leave_cmd.command, '.leave')
        self.assertEqual(leave_cmd.help_message, '.leave - Leave a server given the server ID')

    def test_leave_server_command_execute(self):
        client = MagicMock()
        message = MagicMock(content='.leave')

        # No args
        client.send_message = MagicMock()
        client.leave_server = MagicMock()
        leave_cmd = actions.admin_commands.LeaveServerCommand(client, message)
        self.assertTrue(leave_cmd.execute())
        client.send_message.assert_called_once_with(message.channel, 'Farewell!')
        client.leave_server.assert_called_once_with(message.server)

        # With args
        message.content = '.leave 12083t1141241'
        server = MagicMock(name='12083t1141241', id='12083t1141241')
        client.servers = [server]
        client.send_message = MagicMock()
        client.leave_server = MagicMock()
        leave_cmd = actions.admin_commands.LeaveServerCommand(client, message)
        self.assertTrue(leave_cmd.execute())
        client.send_message.assert_called_once_with(message.channel, 'Leaving server: {}'.format(server.name))
        client.leave_server.assert_called_once_with(server)

        # Exception
        client.send_message = MagicMock()
        client.leave_server = MagicMock()
        client.leave_server.side_effect = actions.admin_commands.HTTPException(MagicMock())
        leave_cmd = actions.admin_commands.LeaveServerCommand(client, message)
        self.assertEqual(leave_cmd.execute(), 'The leave command failed')
