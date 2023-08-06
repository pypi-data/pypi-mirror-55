"""
NeurodataLab LLC 02.11.2019
Created by Andrey Belyaev
"""
import grpc


class IRService:
    name = 'AbstractService'
    short_name = 'as'
    stub_cls = None
    media_types = []

    def __init__(self, auth):
        ssl_cred = grpc.ssl_channel_credentials(auth.ssl_credentials().ca(),
                                                auth.ssl_credentials().key(),
                                                auth.ssl_credentials().cert())

        token_cred = grpc.access_token_call_credentials(auth.token())

        channel_cred = grpc.composite_channel_credentials(ssl_cred, token_cred)
        self.channel = grpc.secure_channel(auth.host(), channel_cred,
                                           options=[('grpc.max_send_message_length', -1),
                                                    ('grpc.max_receive_message_length', -1)])

        self.stub = self.stub_cls(self.channel)
