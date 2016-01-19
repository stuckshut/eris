import logging
from discord import HTTPException, InvalidArgument
from actions import Command, command_list


class JoinServerCommand(Command):
    command = '.join'
    help_message = '{} - Join a server given an invite link'.format(command)
    admin_required = True
    channel_required = True

    def execute(self):
        if not self.args:
            return 'What do you want me to join?'
        else:
            try:
                self.client.accept_invite(self.args)
            except HTTPException as e:
                logging.log(logging.INFO, e)
                return 'I couldn\'t accept that request for some reason'
            except InvalidArgument:
                return 'That is not a valid request'
            return 'Joining that server now...'


class LeaveServerCommand(Command):
    command = '.leave'
    help_message = '{} - Leave a server given the server ID'.format(command)
    admin_required = True
    channel_required = True

    def execute(self):
        try:
            if not self.args:
                self.client.send_message(self.message.channel, 'Farewell!')
                self.client.leave_server(self.message.server)
                return True
            else:
                for server in self.client.servers:
                    if self.args == server.id or self.args == server.name:
                        self.client.send_message(self.message.channel, 'Leaving server: {}'.format(server.name))
                        self.client.leave_server(server)
                        return True
        except HTTPException as e:
            logging.log(logging.INFO, e)
            return 'The leave command failed'


command_list.append(JoinServerCommand)
command_list.append(LeaveServerCommand)
