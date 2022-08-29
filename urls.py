from django.urls import path
from . import apiREST
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('ping/', apiREST.ping.as_view()),
    path('ping2/<str:uuid>/', apiREST.pingParam),
    path('sessions', apiREST.sessionOperationsGeneral),
    path('sessions/<str:uuid>/', apiREST.sessionOperations),
    path('api-token-auth/', obtain_auth_token),
]