from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from accounts.serializers import UserSerializer
from rest_framework.authtoken.models import Token


@api_view(["GET", "POST"])
def hello_world(request):

    if request.method == 'POST':
        return Response({'message': 'Post request-Response'}, status=status.HTTP_201_CREATED)

    return Response({"message": "Hello, world!"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def example_view(request):
    content = { 'user': str(request.user), 'auth': str(request.auth), }
    return Response(content)


@api_view(['POST'])
def register(request,**prams):
    serializedUser=UserSerializer(data=request.data)
    if serializedUser.is_valid():
        serializedUser.save()
    else:
        return Response(data=serializedUser.errors,status=status.HTTP_400_BAD_REQUEST)
    data = {
        'firstname': serializedUser.data.get('first_name'),
        'token' : Token.objects.get(user__username=serializedUser.data.get('username')).key,
        'id': serializedUser.data.get('id')
    }
    return Response(data=data,status=status.HTTP_201_CREATED)