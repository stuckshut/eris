import dice
import settings


class Command:
    """The base Command class

    Attributes:
        message (str): The message to parse from Discord
        command (str): The parsed command
        help_message (str): The help message for a command
        admin_required (bool): Whether or not a user needs to be an admin to
        execute the command.
        channel_required (bool,: Whether or not the command has to have been
        initiated from a channel to be executed.
    """
    message = None
    command = None
    help_message = None
    admin_required = False
    channel_required = False

    def __init__(self, message):
        self.message = message
        parts = message.content.split(' ', 1)
        self.command = parts[0]
        if len(parts) > 1:
            self.args = parts[1]
        else:
            self.args = None

    def __str__(self):
        return self.help_message

    def __repr__(self):
        return self.help_message

    def execute(self):
        """The main execution method for Command types

        This should be overridden by classes that extend Command.

        Returns:
            string
        """
        pass


def get_command_from_message(message):
    """Parse the command from a Discord message

    Args:
        message: The received Discord message

    Returns:
        string: The parsed command
    """
    return message.content.split(' ', 1)[0]


class HelpCommand(Command):
    """Show the user a help message

    This will show a help message:
        Commands
        !command1 - this command does something
        !command2 - this command does something as well
    """
    command = '!help'
    help_message = '{} - Show this message'.format(command)

    def execute(self):
        return self._get_help_string()

    @staticmethod
    def _get_help_string():
        """Builds the help message to display

        Returns:
            string: the help message
        """
        help_string = '\n'.join([command.help_message for command in command_list])
        return 'Commands\n{}'.format(help_string)


class EchoCommand(Command):
    """Echo text back to the user/channel."""
    command = '!echo'
    help_message = '{} - Echo chamber'.format(command)

    def execute(self):
        if not self.args:
            # Quote Starbuck
            message = "Nothin' but the rain"
        else:
            message = self.args
        return message


class RollCommand(Command):
    """Roll dice"""
    command = '!roll'
    help_message = '{} - Roll dice: !roll 3d6'.format(command)

    def execute(self):
        try:
            if self.args:
                return self._roll(self.args)
            else:
                return self._roll(settings.DEFAULT_DIE_ROLL)
        except:
            return 'Those dice were loaded.'

    @staticmethod
    def _roll(message):
        """Rolls dice given a message

        Args:
            message (str): A description of the dice to roll.

        Returns:
            list[int]: The result of the roll(s)
        """
        result = dice.roll(message)
        return result


class KillCommand(Command):
    """Kill Eris"""
    command = '!kill'
    help_message = '{} - Kills the bot'.format(command)
    admin_required = True
    channel_required = True

    def execute(self):
        quit()

command_list = [
    HelpCommand,
    EchoCommand,
    RollCommand,
    KillCommand
]


def get_command_from_list(message):
    """Get a command from the command_list given a command string

    Args:
        message: The received message from Discord

    Returns:
        Command: The command that was found. None if no matches.
    """
    command_string = get_command_from_message(message)
    command = [c for c in command_list if c.command == command_string]
    return command
