from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from ...models import User
from .serializers import RegistrationSerializer

class RegistrationApiView(generics.GenericAPIView):
    model = User
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'email': serializer.validated_data['email']
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


