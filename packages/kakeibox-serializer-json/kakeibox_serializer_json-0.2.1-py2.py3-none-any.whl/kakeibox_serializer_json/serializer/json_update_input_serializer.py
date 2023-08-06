from kakeibox_serializer_json.serializer.json_serializer \
    import JsonInputSerializer


class JsonUpdateInputSerializerFabric(object):

    def _get_model_name(self, keys):
        ignored_keys = ['code', 'uuid']
        for k in keys:
            if k in ignored_keys:
                continue
            else:
                return k
        raise Exception("Could not get a valid model name to serialize")

    def serialize(self, input_dict):
        model_name = self._get_model_name(input_dict.keys())
        method_name = "serialize_{}".format(model_name)
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            return method(input_dict)
        else:
            raise Exception("Could not get a valid model name to serialize")

    def _serialize_code(self, model_name, input_dict):
        serializer = JsonInputSerializer()
        serialized_value = serializer.serialize(
            input_dict[model_name])
        result = {
            "code":input_dict['code'],
            model_name: serialized_value
        }
        return result

    def _serialize_uuid(self, model_name, input_dict):
        serializer = JsonInputSerializer()
        serialized_value = serializer.serialize(
            input_dict[model_name])
        result = {
            "uuid":input_dict['uuid'],
            model_name: serialized_value
        }
        return result

    def serialize_transaction_category(self, input_dict):
        return self._serialize_code('transaction_category', input_dict)

    def serialize_transaction_subcategory(self, input_dict):
        return self._serialize_code('transaction_subcategory', input_dict)

    def serialize_transaction(self, input_dict):
        return self._serialize_uuid('transaction', input_dict)
