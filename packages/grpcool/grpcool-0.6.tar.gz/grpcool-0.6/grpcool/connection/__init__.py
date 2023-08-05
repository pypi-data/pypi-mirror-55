import grpc
import uuid
import logging

MAX_MESSAGE_LENGTH = 100000000


class AbstractConnection(object):
    def make_channel(self):
        raise Exception("not implemented")

    def make_metadata(self):
        raise Exception("not implemented")

    def make_timeout(self):
        raise Exception("not implemented")


class HostConnection(AbstractConnection):
    def __init__(self, hostport, timeout=None):
        assert type(hostport) in [str]
        assert ":" in hostport
        assert "/" not in hostport
        self.hostport = hostport
        self.timeout = timeout

    def make_timeout(self):
        return self.timeout

    def __str__(self):
        return "<%s hostport:%s>" % (self.__class__.__name__, self.hostport)


class StsConnection(HostConnection):
    def __init__(self, hostport, sts_token, timeout=None):
        HostConnection.__init__(self, hostport=hostport, timeout=timeout)
        self.sts_token = sts_token

    def make_channel(self):
        ssl_creds = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(self.hostport, ssl_creds)
        return channel

    def make_metadata(self):
        metadata = []
        metadata.append(('sts_token', self.sts_token))
        metadata.append(('request-id', str(uuid.uuid4())))
        logging.debug("metadata: %s", metadata)
        return metadata


class BearerConnection(HostConnection):
    def __init__(self, hostport, bearer_token, timeout=None):
        HostConnection.__init__(self, hostport=hostport, timeout=timeout)
        assert type(bearer_token) in [str], type(bearer_token)
        self.bearer_token = bearer_token

    def make_channel(self):
        ssl_creds = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(self.hostport, ssl_creds)
        return channel

    def make_metadata(self):
        metadata = []
        metadata.append(('request-id', str(uuid.uuid4())))
        metadata.append(('authorization', "Bearer %s" % self.bearer_token))
        logging.debug("metadata: %s", metadata)
        return metadata


class InsecureConnection(HostConnection):
    def make_channel(self):
        channel = grpc.insecure_channel(self.hostport, options=[
            ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
            ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH)
        ])
        return channel

    def make_metadata(self):
        return []

