from dataclasses import dataclass
import requests


@dataclass
class AthenaAuth:
    """Initializes Authentification parameters to authenticate developer at LTEP Athena Platform
        :param str host_api_address: hosting address of Athena platform, e.g. 'http://localhost:5000
        :param str email: user's email
        :param str developer_name: user's developr name
        :param str developer_token: user's developer token
        :param str host_api_address_sandbox: hosting address of Sandbox Athena service (if seperated), e.g. 'http://localhost:27000
        :returns: AthenaAuth instance
        :rtype: AthenaAuth
        """
    host_api_address: str
    email: str
    developer_name: str
    developer_token: str
    host_api_address_sandbox: str = None

    @staticmethod
    def authenticate_access_athena(fn):
        """Decorator Function to authenticate with Athena Platform"""
        def wrapfn(*args, **kwargs):
            try:
                auth = kwargs.get('auth') if bool(kwargs.get('auth')) else [
                    arg for arg in args if isinstance(arg, AthenaAuth)][0]
            except Exception as e:
                print(e)
                raise Exception("No auth (authentification object) passed")
            if AthenaAuth.__authenticate_athena_platform(auth.host_api_address, auth.developer_name, auth.email, auth.developer_token):
                return fn(*args, **kwargs)
            else:
                return {'access': 'denied'}
        return wrapfn

    @staticmethod
    def __authenticate_athena_platform(host_api_address: str, developer_name: str, email: str, developer_token: str):
        """This method authenticates developer at LTEP Athena Platform
        :param str host_api_address: hosting address of Athena platform
        :param str email: user's email
        :param str developer_name: user's developr name
        :param str developer_token: user's developer token
        :raises Exception: if authenfication was unsuccessful
        :returns: Success in terms of boolean
        :rtype: Boolean
        """
        try:
            response = requests.get(host_api_address + '/developer/auth?email=' +
                                    email + '&developer_name=' + developer_name + '&developer_token=' + developer_token).json()
            return True if response.get('email') == email and response.get('Authorization') == 1 else False
        except Exception as e:
            print(e)
            raise Exception("Authentification to Athena Platform @ {host_api_address} failed. Check Credentials or raised Exceptions Log above".format(
                host_api_address=host_api_address))
