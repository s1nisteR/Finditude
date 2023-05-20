from django.urls import path
from .views import RegisterView, LoginView, LogoutView, MissingPersonRegView, MissingPersonGetView, MissingPersonRandom
from .views import MissingPersonImageUploadView, MissingPersonImageGetView

urlpatterns = [
    path('register',RegisterView.as_view()), 
    path('login',LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('missingreg', MissingPersonRegView.as_view()),
    path('missingget', MissingPersonGetView.as_view()),
    path('missingrandom', MissingPersonRandom.as_view()),
    path('missingimageupload', MissingPersonImageUploadView.as_view()),
    path('missingimageget', MissingPersonImageGetView.as_view())
]
