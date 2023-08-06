import json


class MessageMetadata:

    def __init__(self, content_encoding, content_type, delivery_info, delivery_tag, errors, headers, properties):
        self.content_encoding = content_encoding
        self.content_type = content_type
        self.delivery_info = delivery_info
        self.delivery_tag = delivery_tag
        self.errors = errors
        self.headers = headers
        self.properties = properties

    @staticmethod
    def from_str_json(str_json):
        j_data = json.loads(str_json)
        return MessageMetadata(**j_data)

    @staticmethod
    def from_message(message):
        d = {
            'content_encoding': message.content_encoding,
            'content_type': message.content_type,
            'delivery_info': message.delivery_info,
            'delivery_tag': message.delivery_tag,
            'errors': message.errors,
            'headers': message.headers,
            'properties': message.properties,
        }
        return MessageMetadata(**d)

    def __str__(self):
        d = {
            'content_encoding': self.content_encoding,
            'content_type': self.content_type,
            'delivery_info': self.delivery_info,
            'delivery_tag': self.delivery_tag,
            'errors': self.errors,
            'headers': self.headers,
            'properties': self.properties,
        }
        return json.dumps(d)
