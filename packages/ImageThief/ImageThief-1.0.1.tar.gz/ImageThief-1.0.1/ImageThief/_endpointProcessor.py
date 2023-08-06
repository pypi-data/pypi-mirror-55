from flask import Response
from ._imageEncoder import VideoCamera
from base64 import b64encode

class EndpointProcessor(object):

    def __init__(self, action):
        self.action = action

    def __call__(self, *args):
        frame = VideoCamera().get_frame()
        self.response = Response(b64encode(frame),status=200)
        self.action()
        return self.response
