import json


class Server:

    def __init__(self, ipv4, name, ssh_port, ssh_user, ssh_password, pk=None,):
        self.pk = pk
        self.__ipv4 = ipv4
        self.__name = name
        self.__ssh_port = ssh_port
        self.__ssh_user = ssh_user
        self.__ssh_password = ssh_password

    def get_json_representation(self):
        return json.dumps({
            "IP": self.__ipv4,
            "Name": self.__name,
            "SSHUser": self.__ssh_user,
            "SSHPassword": self.__ssh_password,
            "SSHPort": self.__ssh_port
        })

    def get_ipv4(self):
        return self.__ipv4

    def get_name(self):
        return self.__name

    def get_ssh_port(self):
        return self.__ssh_port

    def get_ssh_user(self):
        return self.__ssh_user

    def get_ssh_password(self):
        return self.__ssh_password

    def __eq__(self, other):
        return self.__ipv4 == other.get_ipv4() and self.__ssh_port == other.get_ssh_port()

    def __repr__(self):
        return "Name:" + self.__name + " IP:" + self.__ipv4


class Application:
    pass


class Data:
    pass


class Domain:

    def __init__(self, domain_name):
        self.__domain_name = domain_name
