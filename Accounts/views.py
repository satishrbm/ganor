from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import EmailPasswordSerializer
from rest_framework import status

class LoginAPI(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email, password=password)
            serializer = EmailPasswordSerializer(user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

