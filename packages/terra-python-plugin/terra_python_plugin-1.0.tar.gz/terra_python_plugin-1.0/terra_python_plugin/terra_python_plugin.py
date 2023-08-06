import json
import requests
from os import environ


class PythonPlugin:
    """
    A python plugin to send data(json) from any data platform to a connected API.
    """

    def __init__(self):
        pass

    def send_data(self, data, data_source, data_type):
        """
        send the data to the API.
        :param data
        :param data_source
        :param data_type
        :return status_code:
        """

        self.data = data
        self.data_source = data_source
        self.data_type = data_type

        # try to open the data as a json file
        try:
            with open(f'{self.data}') as datafile:
                data_obj = json.load(datafile)

        # in case the data is not a file, then it will be an object.
        except:
            data_obj = json.loads(self.data)

        # the data structure with the set of data that is expected at the API endpoint.
        self.payload = {
            "data": {
                "source": self.data_source,
                "type": self.data_type,
                "payload": data_obj
            }
        }

        # send the data
        try:
            r = requests.post(url=environ.get('API_URL'), json=self.payload)
        except BaseException as e:
            print(e)
        else:
            print(r.status_code)