from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import User
from .models import MissingPerson
import jwt
import datetime
import json
from django.http import JsonResponse




# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        user = User.objects.filter(email=request.data['email']).first()
        if user is None:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
            #raise AuthenticationFailed('Incorrect username or password!')
        
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
    #TODO: Make logout work properly
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logged out!'
        }
        return response
    
class MissingPersonRegView(APIView):
    def post(self, request):
        token = request.data['jwt']
        if not token:
            return Response(status=status.HTTP_401_UNAUTHORIZED) 
        try:
            payload = jwt.decode(token, 'secret_key', algorithms=['HS256'], options={'verify_exp': False})
            user = User.objects.filter(id=payload['id']).first()
            if user is None:
                raise Exception("Unauthenticated")
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        #Otherwise we are authenticated, continue normally
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
        token = request.data['jwt']
        if not token:
            return Response(status=status.HTTP_401_UNAUTHORIZED) 
        try:
            payload = jwt.decode(token, 'secret_key', algorithms=['HS256'], options={'verify_exp': False})
            user = User.objects.filter(id=payload['id']).first()
            print(user)
            if user is None:
                raise Exception("Unauthenticated")
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        #Otherwise we are authenticated, continue normally
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

class MissingPersonRandom(APIView):
    def post(self, request):
        token = request.data['jwt']
        if not token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            payload = jwt.decode(token, 'secret_key', algorithms=['HS256'], options={'verify_exp': False})
            user = User.objects.filter(id=payload['id']).first()
            print(user)
            if user is None:
                raise Exception("Unauthenticated")
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        #Otherwise we are authenticated, continue normally

        # Try to get the results from the cache
        randomMissingPersons = MissingPerson.objects.order_by('?')[:100] #Warning: Could be slow when database is larger
        recordList = list(randomMissingPersons.values())
        #print(json.dumps(recordList, ensure_ascii=False)) 
        return JsonResponse(json.dumps(recordList, ensure_ascii=False), safe=False)



        

