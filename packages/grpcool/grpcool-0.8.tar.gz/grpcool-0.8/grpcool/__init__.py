import logging

class Proxy:
    def __init__(self, stub, connection):
        self.stub = stub
        self.connection = connection


    def __pstr(self, proto_data_structure):
        if proto_data_structure == None:
          return str(None)
        name = proto_data_structure.__class__.__name__
        return "%s:\n\t%s" % (name, str(proto_data_structure).replace("\n", "\n\t"))


    def __getattr__(self, method_name):
        def f(req):
            logging.debug("calling %s ...", method_name)
            logging.debug("req:%s", self.__pstr(req))
            stub_instance = self.stub(self.connection.make_channel())
            if not hasattr(stub_instance, method_name):
                msg = "method {method_name} not found in stub {stub_module}.{stub_name}".format(
                    method_name=method_name,
                    stub_module=self.stub.__module__,
                    stub_name=self.stub.__name__,
                )
                raise Exception(msg)
            method = getattr(stub_instance, method_name)
            res = method(req, metadata=self.connection.make_metadata(), timeout=self.connection.make_timeout())
            logging.debug("res:%s", self.__pstr(res))
            return res
        return f
