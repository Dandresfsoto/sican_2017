from channels import route, route_class
from inbox.consumers import ChatServer

channel_routing = [
    route_class(ChatServer, path=r"^/realtime/"),
]