from potholder import potholder
from potholder import primitives

if __name__ == '__main__':

    potholder_instance = potholder.Potholder(host="127.0.0.1", port=7788)
    potholder_instance.connect()
    print(potholder_instance.get_connection_status())

    server_a = primitives.Server(
        ipv4="127.0.0.1",
        name="vagrant server",
        ssh_port=2222,
        ssh_user="vagrant",
        ssh_password="vagrant"
    )

    potholder_instance.add_server(server_a)
    print(potholder_instance.get_server_list())
