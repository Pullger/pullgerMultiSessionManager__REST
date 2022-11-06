from django.urls import path
from . import apiREST

urlpatterns = [
    path('ping', apiREST.Ping.as_view()),
    path('pingAuth', apiREST.PingAuth.as_view()),
    path('ping2/<str:uuid>', apiREST.pingParam),
    path('sessions', apiREST.session_operations_general),
    path('sessions/make-all-session-authorization', apiREST.make_all_authorization),
    path('sessions/execute-task-in-the-queue', apiREST.ExecuteTaskInTheQueue.as_view()),
    path('sessions/<str:uuid>', apiREST.session_operations),
    path('sessions/<str:uuid>/get-page', apiREST.OperationGetPage.as_view()),
    path('sessions/<str:uuid>/get-html', apiREST.OperationGetHTML.as_view()),
    path('sessions/<str:uuid_session>/get-current-url', apiREST.OperationGetCurrentUrl.as_view()),
    path('sessions/<str:uuid_session>/elements-scan', apiREST.OperationElementsScan.as_view()),
    path('sessions/<str:uuid_session>/elements-list', apiREST.OperationElementsList.as_view()),
    path('sessions/<str:uuid_session>/<str:uuid_element>/send-string', apiREST.OperationElementsSendString.as_view()),
    path('sessions/<str:uuid_session>/<str:uuid_element>/send-enter', apiREST.OperationElementsSendEnter.as_view()),
    path('sessions/<str:uuid_session>/<str:uuid_element>/send-click', apiREST.OperationElementsSendClick.as_view()),
]
