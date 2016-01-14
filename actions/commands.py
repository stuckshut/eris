import dice
import settings


class Command:
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


def get_command_from_message(message):
    return message.content.split(' ', 1)[0]


class HelpCommand(Command):
    command = '!help'
    help_message = '{} - Show this message'.format(command)

    def execute(self):
        return self._get_help_string()

    @staticmethod
    def _get_help_string():
        help_string = '\n'.join([command.help_message for command in commands])
        return 'Commands\n{}'.format(help_string)


class EchoCommand(Command):
    command = '!echo'
    help_message = '{} - Echo chamber'.format(command)

    def execute(self):
        return self.args


class RollCommand(Command):
    command = '!roll'
    help_message = '{} - Roll dice: !roll 3d6'.format(command)

    def execute(self):
        if self.args:
            return self._roll(self.args)
        else:
            return self._roll(settings.DEFAULT_DIE_ROLL)

    @staticmethod
    def _roll(message):
        result = dice.roll(message)
        return result


class KillCommand(Command):
    command = '!kill'
    help_message = '{} - Kills the bot'.format(command)
    admin_required = True
    channel_required = True

    def execute(self):
        quit()

commands = [
    HelpCommand,
    EchoCommand,
    RollCommand,
    KillCommand
]
