from .delayed_msg.publisher import Publisher
from .delayed_msg.router import router as delayed_router


def get_stream_routers():
    return [delayed_router]


__all__ = ["Publisher", "get_stream_routers"]
