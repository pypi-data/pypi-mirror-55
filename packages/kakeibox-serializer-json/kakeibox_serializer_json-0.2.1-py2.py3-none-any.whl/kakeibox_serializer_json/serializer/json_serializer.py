import json


class JsonInputSerializer(object):

    def serialize(self, str_json):
        return json.loads(str_json)
