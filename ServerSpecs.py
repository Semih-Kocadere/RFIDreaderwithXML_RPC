import http.client
import xmlrpc.client

#For ServerProxy() method, we need to specify the server attributes.
class ServerSpecs:
    xmlrpc_server_instance = None

    def __init__(self, url, transport=None, encoding=None, verbose=False, allow_none=False, use_datetime=False,
                 use_builtin_types=False, headers=(), context=None):
        self.url = url
        self.transport = transport
        self.encoding = encoding
        self.verbose = verbose
        self.allow_none = allow_none
        self.use_datetime = use_datetime
        self.use_builtin_types = use_builtin_types
        self.headers = headers
        self.context = context

    def create_server_proxy(self):
        # Create a server proxy object
        return xmlrpc.client.ServerProxy(
            self.url,
            transport=self.transport,
            encoding=self.encoding,
            verbose=self.verbose,
            allow_none=self.allow_none,
            use_datetime=self.use_datetime,
            use_builtin_types=self.use_builtin_types,
            headers=self.headers,
            context=self.context
        )

    @classmethod
    def get_xmlrpc_server_instance(cls):
        if cls.xmlrpc_server_instance is None:
            cls.xmlrpc_server_instance = ServerSpecs(
                url="http://your_server_ip:8000",
                transport=http.client.HTTPSConnection,
                verbose=True,
                allow_none=False,
            )
        return cls.xmlrpc_server_instance.create_server_proxy()
