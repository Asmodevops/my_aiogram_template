from .delayed_msg.router import router as delayed_router

def get_stream_routers():
    return [delayed_router]
