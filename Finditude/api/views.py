from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import User
from .models import MissingPerson
from .models import MissingImage
import jwt
import datetime
import json
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from .models import MissingImage, MissingPersonLocations




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
        contact = request.data['contact']
        newMissingPerson = MissingPerson(full_name=full_name, age=age, gender=gender, identifying_info=identifying_info, contact=contact)
        #Actually write to the database
        newMissingPerson.save()
        #Save the ID of this missing person to the myReports of the reporter
        user = User.objects.filter(id=payload['id']).first()
        user.myReports.append(newMissingPerson.id)
        user.save()
        return Response({"id": newMissingPerson.id}, status=status.HTTP_200_OK)

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
            'identifying_info': missingPerson.identifying_info,
            'contact': missingPerson.contact
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
        randomMissingPersons = MissingPerson.objects.order_by('?')[:100]
        #recordList = list(randomMissingPersons.values('id', 'full_name'))
        recordList = []
        for missingPerson in randomMissingPersons:
            missing_image = MissingImage.objects.filter(missingid=missingPerson.id).first()
            image_url = None

            if missing_image is not None:
                image_url = request.build_absolute_uri(missing_image.photo.url)
            #image_url = request.build_absolute_uri(missing_image.photo.url)
            recordList.append({
                'id': missingPerson.id,
                'full_name': missingPerson.full_name,
                'photo': image_url
            })
        #print(json.dumps(recordList, ensure_ascii=False)) 
        return JsonResponse(recordList, safe=False)
    
class MissingPersonImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
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
        id = request.data.get('id')
        photo = request.data.get('photo')

        if id and photo:
            image = MissingImage.objects.create(missingid=id, photo=photo)
            return Response({'photo': image.photo.url}, status=200)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class MissingPersonImageGetView(APIView):
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
        allPictures = MissingImage.objects.filter(missingid=id)
        image_urls = [request.build_absolute_uri(image.photo.url) for image in allPictures]
        return Response({'images': image_urls})

class MyReportsGetView(APIView):
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
        return Response({'reports': User.objects.filter(id=payload['id']).first().myReports})

class StartFindingView(APIView):
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
        missingid = request.data['id']
        user = User.objects.filter(id=payload['id']).first()
        user.myFindings.append(int(missingid))
        user.save()
        return Response(status=status.HTTP_200_OK)

class MyFindingsGetView(APIView):
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
        return Response({'findings': User.objects.filter(id=payload['id']).first().myFindings})
        
class ReportLocationView(APIView):
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
        lattitude = request.data['lattitude']
        longitude = request.data['longitude']
        if id and lattitude and longitude:
            location = MissingPersonLocations.objects.create(missingid=id, lattitude=lattitude, longitude=longitude)
            location.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST) #otherwise return that it was a bad request

class GetLocationView(APIView):
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
        if id:
            locations = MissingPersonLocations.objects.filter(missingid=id) 
            # Extract latitudes and longitudes from the locations
            latitudes = [location.lattitude for location in locations]
            longitudes = [location.longitude for location in locations]
            return Response({'lattitudes': latitudes, 'longitudes': longitudes})
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
