"""
Django REST Framework views for Campus Social Auth
"""
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response


from .backends.utils import UsernameGenerator


class HintUsernameSerializer(serializers.Serializer):
    username = serializers.CharField()


class HintUsernameView(APIView):
    """
    DRF APIView to get a username suggestion.
    If the user exists then suggests a new username, otherwise
    returns the received base username.
    """

    # This end-point is available to anonymous users,
    # so do not require authentication.
    authentication_classes = []

    def get(self, request):
        """
        Returns a valid username suggestion checking against the database.
        """
        data_serializer = HintUsernameSerializer(data=request.query_params)
        data_serializer.is_valid(raise_exception=True)
        user_dict = data_serializer.data
        username = user_dict['username']

        new_username = UsernameGenerator().generate_username(username)
        return Response({'username': new_username})
