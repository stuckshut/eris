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
    """Handler for messages that are transmitted in channels on the server

    Args:
        message: A received message object

    Returns:
        None
    """
    if message.author.id != client.user.id:
        command = commands.get_command_from_list(message)
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
    """Determine whether the received message is from an admin.

    A message is considered sent by an admin if the message.author is of type
    Member and message.author.roles contains the settings.ADMIN_ROLE.

    Args:
        message: A received message object

    Returns:
        bool: True when the message was sent by an admin. False when it wasn't.
    """
    if [r.name for r in message.author.roles if r.name == settings.ADMIN_ROLE]:
        return True
    return False


def is_direct_message(message):
    """Determine whether the received message was a direct message to Eris.

    A message is considered a direct message when the message.author is of type
    User.

    It is useful to know whether a message was a direct message so we know
    whether or not we can inspect message.author.roles.

    Args:
        message: A received message object

    Returns:
        True if the message was a direct message. False if it was not.
    """
    # If message.author is of type User, this was a direct message.
    return type(message.author) == discord.User

if __name__ == '__main__':
    client.run()
