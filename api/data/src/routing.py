from channels.routing import route_class
from ws_consumer import ApiConsumer

channel_routing = [
    route_class(ApiConsumer, path=r"^/_/ws/$")
]
