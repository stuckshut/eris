import discord
import dice
import settings

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
        # Echo
        if message.content.startswith('!echo'):
            client.send_message(message.channel, message.content[5:])
        # Help
        elif message.content.startswith('!help'):
            client.send_message(message.channel, send_help())
        # Dice
        elif message.content.startswith('!roll'):
            client.send_message(message.channel, roll(message.content[5:]))


def send_help():
    msg = "Commands:\n" \
          "!help - show this message\n" \
          "!echo - Echo chamber\n" \
          "!roll - Roll dice: !roll 3d6\n"
    return msg


def roll(message):
    result = dice.roll(message)
    return result


if __name__ == '__main__':
    client.run()
