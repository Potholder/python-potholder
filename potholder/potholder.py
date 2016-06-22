import requests
from requests.exceptions import ConnectionError
from potholder import primitives

class Potholder:

    CONNECTION_STATUS_NOT_FOUND = "not_found"
    CONNECTION_STATUS_OK = "ok"
    CONNECTION_STATUS_ERROR = "error"

    def __init__(self, host="127.0.0.1", port=7788):
        self.__host = host
        self.__port = port

        self.__servers = []

        self.__connection_status = Potholder.CONNECTION_STATUS_ERROR

    def get_connection_status(self):
        return self.__connection_status

    def add_server(self, server):
        self.__servers.append(server)
        self.__push_new_servers_to_potholder()

    def get_server_list(self):
        self.__servers = self.__pull_servers_from_potholder()
        return self.__servers

    def __send_request_to_potholder(self, request_path="", data="", request_type="get"):
        request_string = "http://" + self.__host + ":" + str(self.__port) + "/" + request_path
        headers = {'Content-Type': 'application/json'}

        try:
            if request_type == "get":
                r = requests.get(request_string, headers=headers)
            elif request_type == "post":
                r = requests.post(request_string, data=data, headers=headers)
            else:
                raise Exception("Wrong request type")

            if r.status_code == 200:
                self.__connection_status = Potholder.CONNECTION_STATUS_OK
            else:
                self.__connection_status = Potholder.CONNECTION_STATUS_ERROR

            return r.json()

        except ConnectionError:
            self.__connection_status = Potholder.CONNECTION_STATUS_ERROR

    def connect(self):
        self.__send_request_to_potholder()

    def __pull_servers_from_potholder(self):
        raw_servers = self.__send_request_to_potholder(
            request_path="server",
            request_type="get"
        )
        servers = []
        for raw_server in raw_servers:
            servers.append(primitives.Server(
                ipv4=raw_server['IP'],
                name=raw_server['Name'],
                ssh_port=raw_server['SSHPort'],
                ssh_password=raw_server['SSHPassword'],
                ssh_user=raw_server['SSHUser']
            ))
        return servers

    def __push_new_server_to_potholder(self, server):
        self.__send_request_to_potholder(
            request_path="server",
            data=server.get_json_representation(),
            request_type="post"
        )

    def __push_new_servers_to_potholder(self):
        servers_form_potholder = self.__pull_servers_from_potholder()

        for server in self.__servers:
            server_is_to_be_pushed = True
            for server_form_potholder in servers_form_potholder:
                if server_form_potholder == server:
                    server_is_to_be_pushed = False

            if server_is_to_be_pushed:
                self.__push_new_server_to_potholder(server)

        self.__servers = self.__pull_servers_from_potholder()
