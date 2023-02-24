from rest_framework.serializers import Serializer, FileField


class UploadSerializer(Serializer):
    """
    Implements the class Serializer.
    The serializer below will grab the file from the request using the FileField object.
    """
    file = FileField()
