import discord
import settings

from actions import commands

client = discord.Client()
client.login(settings.USER, settings.PASS)


@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('--------')


@client.event
def on_message(message):
    """

    Args:
        message: A received message object

    Returns:
        none

    """
    if message.author.id != client.user.id:
        command_string = commands.get_command_from_message(message)

        command = [c for c in commands.commands if c.command == command_string]
        if command:
            command = command[0](message)

            if command.channel_required and is_direct_message(message):
                # Don't allow Eris to be killed by direct message.
                client.send_message(
                    message.channel,
                    settings.CHANNEL_REQUIRED_MSG
                )
                return

            if command.admin_required and not message_is_from_admin(message):
                client.send_message(message.channel, settings.UNAUTHORIZED_MSG)
                return

            client.send_message(message.channel, command.execute())


def message_is_from_admin(message):
    if [r.name for r in message.author.roles if r.name == settings.ADMIN_ROLE]:
        return True
    return False


def is_direct_message(message):
    # If message.author is of type User, this was a direct message.
    print(message.author)
    return type(message.author) == discord.User

if __name__ == '__main__':
    client.run()
