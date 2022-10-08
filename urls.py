from django.urls import path
from . import apiREST

urlpatterns = [
    path('ping', apiREST.Ping.as_view()),
    path('pingAuth', apiREST.PingAuth.as_view()),
    path('ping2/<str:uuid>', apiREST.pingParam),
    path('sessions', apiREST.session_operations_general),
    path('sessions/makeAllSessionAuthorization', apiREST.make_all_authorization),
    path('sessions/executeTaskInTheQueue', apiREST.ExecuteTaskInTheQueue.as_view()),
    path('sessions/<str:uuid>', apiREST.session_operations),
    path('sessions/<str:uuid>/get_page', apiREST.OperationGetPage.as_view()),
    path('sessions/<str:uuid>/get_html', apiREST.OperationGetHTML.as_view()),
]