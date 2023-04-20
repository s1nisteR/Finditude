from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
from .models import MissingPerson
import jwt
import datetime

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            raise AuthenticationFailed('Incorrect username or password!')
        
        #JWT Payload
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret_key', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        
        return response
    
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logged out!'
        }
        return response
    
class MissingPersonRegView(APIView):
    def post(self, request):
        #TODO: Check if authenticated or not
        full_name = request.data['full_name']
        age = request.data['age']
        gender = request.data['gender']
        identifying_info = request.data['identifying_info']
        newMissingPerson = MissingPerson(full_name=full_name, age=age, gender=gender, identifying_info=identifying_info)
        #Actually write to the database
        newMissingPerson.save()
        return Response(status=status.HTTP_200_OK)

class MissingPersonGetView(APIView):
    def post(self, request):
        id = request.data['id']
        missingPerson = MissingPerson.objects.filter(id=id).first()
        response = Response()
        response.data = {
            'full_name': missingPerson.full_name,
            'age': missingPerson.age,
            'gender': missingPerson.gender,
            'identifying_info': missingPerson.identifying_info
        }
        return response

        