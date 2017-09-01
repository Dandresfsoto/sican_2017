from channels.generic.websockets import JsonWebsocketConsumer
from channels.sessions import channel_session
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
from channels import Channel, Group
from usuarios.models import User
import json
from inbox.models import Mensaje


class ChatServer(JsonWebsocketConsumer):

    # Set to True if you want them, else leave out
    strict_ordering = False
    slight_ordering = False
    channel_session_user = True

    def raw_connect(self, message, **kwargs):
        """
        Called when a WebSocket connection is opened. Base level so you don't
        need to call super() all the time.
        """
        Group("%s" % message.user.id, channel_layer=message.channel_layer).add(message.reply_channel)
        self.connect(message, **kwargs)

    def raw_disconnect(self, message, **kwargs):
        """
        Called when a WebSocket connection is closed. Base level so you don't
        need to call super() all the time.
        """
        Group("%s" % message.user.id).discard(message.reply_channel)
        self.disconnect(message, **kwargs)

    def connect(self, message, **kwargs):
        """
        Perform things on connection start
        """
        self.set_user_online(message,online = True)
        content = {}
        content['conected'] = self.get_users_online()
        self.send(content)
        pass

    def receive(self, content, **kwargs):
        """
        Called when a message is received with decoded JSON content
        """
        # Simple echo
        if 'conected' in content.keys():
            content['conected'] = self.get_users_online()
            self.send(content)
        if 'mensaje' in content.keys():
            content['mensaje']['de'] = str(self.message.user.id)
            self.save_message_backend(content['mensaje']['de'],content['mensaje']['para'],content['mensaje']['mensaje'])
            self.group_send(name = str(self.message.user.id), content=content)
            self.group_send(name = content['mensaje']['para'], content=content)

    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        self.set_user_online(message,online = False)
        pass

    def get_users_online(self):
        conected_tuple = User.objects.exclude(id=self.message.user.id).exclude(email="AnonymousUser").values_list("id","is_online")
        conected = []
        for x in conected_tuple:
            conected.append({'id':x[0],'online':x[1]})
        return conected

    def get_handler(self, message, **kwargs):
        """
        Return handler uses method_mapping to return the right method to call.
        """
        handler = getattr(self, self.method_mapping[message.channel.name])
        if message.channel.name == u'websocket.connect':
            handler = channel_session_user_from_http(handler)
        if self.channel_session_user:
            return channel_session_user(handler)
        elif self.channel_session:
            return channel_session(handler)
        else:
            return handler

    def set_user_online(self, message, online):
        user = User.objects.get(id=message.user.id)
        user.is_online = online
        user.save()
        pass

    def save_message_backend(self,sender,receiver,text):
        user_sender = User.objects.get(id=sender)
        user_receiver = User.objects.get(id=receiver)

        mensaje_sender = Mensaje(user=user_sender,de=user_sender,para=user_receiver,texto=text)
        mensaje_sender.save()
        mensaje_receiver = Mensaje(user=user_receiver,de=user_sender,para=user_receiver,texto=text)
        mensaje_receiver.save()

        pass