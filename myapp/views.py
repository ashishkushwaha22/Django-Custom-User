# Create your views here.


from rest_framework import generics
from .serializers import UserSerializer, UserLoginSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

class LoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'id': user.pk,
                'name': user.name,
                'email': user.email,
                'token': token.key
            }, status=HTTP_200_OK)
            # return Response({'token': token.key}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
class UserLogoutAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response({'detail': 'Successfully logged out.'})
