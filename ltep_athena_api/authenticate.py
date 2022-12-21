from dataclasses import dataclass


@dataclass
class AthenaAuth:
    """Initializes Authentification parameters to authenticate developer at LTEP Athena Platform
        :param str email: user's email
        :param str developer_name: user's developr name
        :param str developer_token: user's developer token
        :param Optional[str] host_api_address_sandbox: hosting address of Sandbox Athena service (if seperated), default 'http://localhost:27000
        :param Optional[str] host_api_address_sandbox: hosting address of Sandbox Athena service (if seperated), default 'ws://localhost:27097
        :returns: AthenaAuth instance
        :rtype: AthenaAuth
        """
    email: str
    developer_name: str
    developer_token: str
    host_api_address_sandbox: str = None
    host_api_address_streaming: str = None
