import json
from kakeibox_serializer_json.serializer.json_serializer \
    import JsonInputSerializer


class JsonDeleteInputSerializer(object):

    def serialize(self, str_json):
        serializer = JsonInputSerializer()
        result = serializer.serialize(str_json)
        return result['code']
