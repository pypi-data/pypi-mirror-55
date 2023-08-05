import logging

class Proxy:
    def __init__(self, stub, connection):
        self.stub = stub
        self.connection = connection

    def __getattr__(self, method_name):
        def f(req):
            logging.debug("calling %s(%s)", method_name, req)
            stub_instance = self.stub(self.connection.make_channel())
            if not hasattr(stub_instance, method_name):
                msg = "method {method_name} not found in stub {stub_module}.{stub_name}".format(
                    method_name=method_name,
                    stub_module=self.stub.__module__,
                    stub_name=self.stub.__name__,
                )
                raise Exception(msg)
            method = getattr(stub_instance, method_name)
            return method(req, metadata=self.connection.make_metadata(), timeout=self.connection.make_timeout())
        return f
