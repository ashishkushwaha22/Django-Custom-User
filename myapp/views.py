# Create your views here.


from rest_framework import generics, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import UserSerializer, UserLoginSerializer
from .models import MyUser
from .serializers import MyUserSerializer


class UserCreateView(generics.CreateAPIView):
    """
    API view to register user.
    """
    serializer_class = UserSerializer

class LoginAPIView(APIView):
    """
    API view to Login User
    """

    # overiding the POST method
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user) #getting auth token for User. GET it already present or CREATE it not.
            return Response({
                'id': user.pk,
                'name': user.name,
                'email': user.email,
                'token': token.key
            }, status=HTTP_200_OK)
            # return Response({'token': token.key}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
class UserLogoutAPIView(APIView):
    """
    API view to logout user
    """

    # Here we are defining that user should by LOGGED IN (IsAuthenticated,) and ACCEPT the Token that he gets when he Logged in.    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # over riding the post method
    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete() #deleting the user token from database for the current user.
        return Response({'detail': 'Successfully logged out.'})

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows all the CRUD operation on MyUser model but only for ADMIN.
    """
    permission_classes = (IsAdminUser,)
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
