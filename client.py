import socket
import time

class ClientError(Exception):
    """Wrong server response"""
    pass

class Client():
    def __init__(self, ip_address, port, timeout = None):
        self.ip_address = ip_address
        self.port = port
        self.timeout = timeout

    def client_create_connection(self):
        """
        Method will create connection
        """
        sock = socket.create_connection((self.ip_address, self.port))
        sock.settimeout(self.timeout)
        return sock

    def get_answer_parser(self, data):
        """
        Method will parse get request
        response example <status><\n><key> <value> <timestamp><\n\n>
        """
        result = {}
        status, payload = data.split("\n", 1)
        payload = payload.strip()

        if status != 'ok':
            raise ClientError('Server returns an error')

        if payload == '':
            return result

        try:
            for row in payload.splitlines():
                key, value, timestamp = row.split(' ')
                if key in result:
                    result[key].append((int(timestamp), float(value)))
                else:
                    result[key] = [(int(timestamp), float(value))]
        except Exception as err:
            raise ClientError('Server returns invalid data', err)

        #sort dict by timestamp
        {item.sort(key=lambda tup: tup[0]) for item in result.values()}

        return result

    def get(self, message):
        """
        Method will retrive and show data on client
        """
        with self.client_create_connection() as sock:
            try:
                message_to_send = 'get ' + str(message) + '\n'
                sock.sendall(message_to_send.encode('utf-8'))
                data = sock.recv(1024).decode("utf-8")
            except socket.timeout:
                raise ClientError("Timeout error") from timeout_err
            except socket.error as ex:
                raise ClientError("Socket error : ", ex) from ex
            else:
                return self.get_answer_parser(data)

    def put(self, metric_name, metric_value, timestamp = None):
        """
        Method will try to write given data to server
        """
        if not timestamp:
            timestamp_value = str(int(time.time()))
        else:
            timestamp_value = str(timestamp)

        timestamp_value += '\n'

        with self.client_create_connection() as sock:
            try:
                message_to_send = ' '.join(['put', str(metric_name), str(metric_value), timestamp_value])
                sock.sendall(message_to_send.encode('utf-8'))
                data = sock.recv(1024).decode("utf-8")
            except socket.timeout as timeout_err:
                raise ClientError("Timeout error") from timeout_err
            except socket.error as ex:
                raise ClientError("Socket error : ", ex) from ex

            if data == 'error\nwrong command\n\n':
                raise ClientError("Wrong server response : " + data)

if __name__ == "__main__":
    client_inst = Client('127.0.0.1', 10001)
    #client_inst.get("")
    print(client_inst.get_answer_parser('ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n\n'))
    print(int(time.time()))
