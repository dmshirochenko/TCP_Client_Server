import asyncio

#global starage for all coroutines
storage_to_save_data = dict()

class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

        command_name, payload = self.method_parser(data.decode())
        if not command_name:
                resp = "error\nwrong command\n\n"
        else:
            if command_name == 'get':
                resp = self.get_parser(payload)
            elif command_name == 'put':
                resp = self.put_parser(payload)

        print('Current storage: ', storage_to_save_data)
        print('Data transmit: {}'.format(resp.encode()))
        self.transport.write(resp.encode())


    def put_parser(self, payload):
        """
        Method will parse put request and store data to global dict to recieve then
        """
        print('payload: ', payload)
        error_message = "error\nwrong command\n\n"
        ok_message = 'ok\n\n'
        try:
            key, value, timestamp = payload.split(' ')
            if key in storage_to_save_data:
                check_timestamp_in_dict = False
                for index, dict_value in enumerate(storage_to_save_data[key]):
                    if int(timestamp) == dict_value[0]:
                        storage_to_save_data[key][index] = (int(timestamp), float(value))
                        check_timestamp_in_dict = True
                if not check_timestamp_in_dict:
                    storage_to_save_data[key].append((int(timestamp), float(value)))
            else:
                storage_to_save_data[key] = [(int(timestamp), float(value))]
            return ok_message
        except Exception as err:
            return error_message


    def get_parser(self, payload):
        """
        Method will parse get request and return response.
        Response example 'ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n\n'
        """
        print('payload: ', payload)
        error_message = 'error\nwrong command\n\n'
        ok_message = 'ok\n'
        string_response = ''
        response_to_return = ''
        try:
            key = payload.strip()
            if key == '*':
                for dict_key, item in storage_to_save_data.items():
                    for metric in item:
                        string_response += str(dict_key) + ' ' + str(metric[1])+ ' ' + str(metric[0]) + '\n'
                response_to_return += ok_message + string_response + '\n'
                return response_to_return
            elif key in storage_to_save_data:
                for metric in storage_to_save_data[key]:
                    string_response += str(key) + ' ' + str(metric[1])+ ' ' + str(metric[0]) + '\n'
                response_to_return += ok_message + string_response + '\n'
                return response_to_return
            elif ' ' in key:
                return error_message
            elif not key:
                return error_message
            else:
                return ok_message + '\n'
        except Exception as err:
            print(err)
            return error_message


    def method_parser(self, data):
        """
        Method will parse recieved message and return command_name and stripped payload
        """
        #error_message = 'error\nwrong command\n\n'
        try:
            command_name, payload = data.split(" ", 1)
            payload = payload.strip()
        except Exception:
            return None, None

        if command_name == 'get':
            return command_name, payload
        elif command_name == 'put':
            return command_name, payload
        else:
            return None, None


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


run_server('127.0.0.1', 8888)
