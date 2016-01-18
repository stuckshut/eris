from unittest import TestCase
from unittest.mock import MagicMock

import actions.commands


class CommandTest(TestCase):

    def test_command_init(self):
        cmd = actions.commands.Command(MagicMock(), MagicMock(content="test"))

        self.assertIsInstance(cmd, actions.commands.Command)
        self.assertEqual(cmd.args, None)

        cmd = actions.commands.Command(MagicMock(), MagicMock(content="!cmd arg"))
        self.assertIsInstance(cmd, actions.commands.Command)
        self.assertEqual("!cmd", cmd.command)
        self.assertNotEqual(cmd.args, None)

    def test__str__(self):
        cmd = actions.commands.Command(MagicMock(), MagicMock())
        cmd.help_message = "test"
        self.assertEqual(str(cmd), "test")

    def test__repr__(self):
        cmd = actions.commands.Command(MagicMock(), MagicMock(content="!test arg"))
        self.assertEqual("Command(command={0}, message={1}".format(cmd.command, cmd.message),
                         repr(cmd))

    def test_parent_execute(self):
        self.assertRaises(NotImplementedError)

    def test_get_command_from_message(self):
        msg = MagicMock(content="!test arg")
        self.assertEqual("!test", actions.commands.get_command_from_message(msg))

    def test_get_command_from_list(self):
        cmd = actions.commands.get_command_from_list(MagicMock(content="!help"))
        self.assertEqual(cmd.__name__, actions.commands.HelpCommand.__name__)

        cmd = actions.commands.get_command_from_list(MagicMock(content='!!'))
        self.assertIsNone(cmd)


class HelpCommandTest(TestCase):

    def test_help_command_object(self):
        help_cmd = actions.commands.HelpCommand(MagicMock(), MagicMock(content="!help"))
        self.assertEqual("!help", help_cmd.command)
        self.assertEqual("!help - Show this message", help_cmd.help_message)

    def test_help_execute(self):
        help_cmd = actions.commands.HelpCommand(MagicMock(), MagicMock(content="!help"))
        actions.commands.HelpCommand._get_help_string = MagicMock()

        help_cmd.execute()
        actions.commands.HelpCommand._get_help_string.assert_called_once_with()

    def test_get_help_string(self):
        actions.commands.command_list = [
            actions.commands.HelpCommand,
            actions.commands.EchoCommand
        ]
        output = 'Commands\n!help - Show this message\n!echo - Echo chamber'
        self.assertEqual(output, actions.commands.HelpCommand._get_help_string())


class EchoCommandTest(TestCase):

    def test_echo_command_object(self):
        echo_cmd = actions.commands.EchoCommand(MagicMock(), MagicMock(content="!echo"))
        self.assertEqual("!echo", echo_cmd.command)
        self.assertEqual("!echo - Echo chamber", echo_cmd.help_message)

    def test_echo_command_execute(self):
        # Test empty echo
        echo_cmd = actions.commands.EchoCommand(MagicMock(), MagicMock(content="!echo"))
        msg = echo_cmd.execute()
        self.assertEqual("Nothin' but the rain", msg)

        # With args
        echo_cmd = actions.commands.EchoCommand(MagicMock(), MagicMock(content="!echo aardvark brazil, test' one 2"))
        msg = echo_cmd.execute()
        self.assertEqual("aardvark brazil, test' one 2", msg)


class RollCommandTest(TestCase):

    def test_roll_command_object(self):
        roll_cmd = actions.commands.RollCommand(MagicMock(), MagicMock(content="!roll"))
        self.assertEqual("!roll", roll_cmd.command)
        self.assertEqual("!roll - Roll dice: !roll 3d6", roll_cmd.help_message)

    def test_roll_command_execute(self):
        orig_roll = actions.commands.RollCommand._roll
        
        # Empty !roll
        roll_cmd = actions.commands.RollCommand(MagicMock(), MagicMock(content="!roll"))
        actions.commands.RollCommand._roll = MagicMock()
        roll_cmd.execute()
        actions.commands.RollCommand._roll.assert_called_once_with(actions.commands.settings.DEFAULT_DIE_ROLL)

        # Roll with args
        roll_cmd = actions.commands.RollCommand(MagicMock(), MagicMock(content="!roll 3d6"))
        actions.commands.RollCommand._roll = MagicMock()
        roll_cmd.execute()
        actions.commands.RollCommand._roll.assert_called_once_with("3d6")

        # Broken roll
        roll_cmd = actions.commands.RollCommand(MagicMock(), MagicMock(content="!roll pants"))
        actions.commands.RollCommand._roll = orig_roll
        msg = roll_cmd.execute()
        self.assertEqual('Those dice were loaded.', msg)

    def test__roll(self):
        actions.commands.dice.roll = MagicMock()
        actions.commands.RollCommand._roll("3d6")
        actions.commands.dice.roll.assert_called_once_with("3d6")


class KillCommandTest(TestCase):
    
    def test_kill_command_object(self):
        kill_cmd = actions.commands.KillCommand(MagicMock(), MagicMock(content='!kill'))
        self.assertEqual('!kill', kill_cmd.command)
        self.assertEqual('!kill - Kills the bot', kill_cmd.help_message)

    def test_kill_requires_admin(self):
        kill_cmd = actions.commands.KillCommand(MagicMock(), MagicMock(content='!kill'))
        self.assertTrue(kill_cmd.admin_required)
        self.assertTrue(kill_cmd.channel_required)

    def test_kill_command_execute(self):
        kill_cmd = actions.commands.KillCommand(MagicMock(), MagicMock(content='!kill'))
        actions.commands.quit = MagicMock()
        kill_cmd.execute()
        actions.commands.quit.assert_called_once_with()
