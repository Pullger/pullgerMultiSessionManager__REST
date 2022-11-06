from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from pullgerMultiSessionManager import apiMSM
from pullgerAccountManager import authorizationsServers
from pullgerSquirrel import connectors
from pullgerInternalControl.pullgerMultiSessionManager.REST.logging import logger
from . import serializers


class Ping(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        content ={'message': 'Pong: MultiSessionManager'}
        return Response(content)


class PingAuth(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Pong: AUTH MultisessionManager'}
        return Response(content)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def pingParam(request, uuid):
    if request.method == 'GET':
        content = {'message': 'GET Pong:' + uuid}
        return Response(content)
    elif request.method == 'POST':
        content = {'message': 'POST Pong:' + uuid}
        return Response(content)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def session_operations(request, uuid):
    content = {
        'message': ''
    }

    if request.method == 'DELETE':
        try:
            apiMSM.kill_session(uuid_session=uuid)
            content['message'] = f'Session {uuid} deleted:'
            statusResp = status.HTTP_200_OK
        except BaseException as e:
            logger.critical(f"Error on executing request [{str(request)}] execute 'pullgerMultiSessionManager.apiMSM.killSession()': {str(e)}")
            content['message'] = 'error'
            statusResp = status.HTTP_500_INTERNAL_SERVER_ERROR

    returnResponse = Response(content, status=statusResp)

    return returnResponse


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def session_operations_general(request):

    if request.method == 'GET':
        content = {
            'message': '',
            'data': ''
        }
        try:
            sessionList = apiMSM.get_sessions_list()
            serializedContent = serializers.SessionsListSerializer(sessionList, many=True)
            content['message'] = 'OK'
            content['data'] = serializedContent.data
            statusResponse = status.HTTP_200_OK
        except BaseException as e:
            content['message'] = 'Error'
            logger.critical(f"Error on executing request [{str(request)}]': {str(e)}")
            statusResponse = status.HTTP_500_INTERNAL_SERVER_ERROR
    elif request.method == 'POST':
        content = {
            "message": ""
        }
        logger.debug(f"Creating session")
        try:
            errorExist = False
            authorization = request.data.get('authorization')
            if authorization is not None:
                try:
                    authorization = authorizationsServers.getByName(authorization)
                except BaseException as e:
                    content['message'] = f'error: {str(e)}'
                    statusResponse = status.HTTP_500_INTERNAL_SERVER_ERROR
                    logger.info(f"Incorrect authorization server {authorization}")
                    errorExist = True

            conn = request.data.get('connector')
            if conn is not None:
                try:
                    conn = connectors.get_by_name(conn=conn)
                except BaseException as e:
                    content['message'] = f'error: {str(e)}'
                    statusResponse = status.HTTP_500_INTERNAL_SERVER_ERROR
                    logger.info(f"Incorrect Squirrel connector {authorization}")
                    errorExist = True
        except BaseException as e:
            logger.critical(f"Error on request {str(request)}: {str(e)}")
            content['message'] = f'error: {str(e)}'
            statusResponse = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            try:
                if errorExist is False:
                    uuidSession = apiMSM.add_new_session(authorization=authorization, conn=conn)
                    content['message'] = 'Session added'
                    content['data'] = {'uuid': str(uuidSession)}
                    statusResponse = status.HTTP_200_OK
                    logger.info(f"Session with uuid [{str(uuidSession)}] was successfully added")
            except BaseException as e:
                logger.critical(
                    f"Error on request {str(request)} execute pullgerMultiSessionManager.apiMSM.addNewSession(): {str(e)}")
                content['message'] = f'error: {str(e)}'
                statusResponse = status.HTTP_500_INTERNAL_SERVER_ERROR

    response = Response(content)
    # >> Disable error log duplication
    response._has_been_logged = True
    # <<
    response['Cache-Control'] = 'no-cache'

    return Response(content, status=statusResponse)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def make_all_authorization(request):
    # TODO send uuid error message
    content = {'message': ''}
    try:
        apiMSM.make_all_session_authorization()
        content['message'] = 'OK'
        statusResponse = status.HTTP_200_OK
    except BaseException as e:
        logger.critical(
            msg=f"Error on request {str(request)} execute 'pullgerMultiSessionManager.apiMSM.makeAllSessionAuthorization': {str(e)}"
        )
        content ={'message': f'Internal system error.'}
        statusResponse = status.HTTP_500_INTERNAL_SERVER_ERROR

    response = Response(content, status = statusResponse)
    # >> Disable error log duplication
    response._has_been_logged = True
    # <<
    return response


class ExecuteTaskInTheQueue(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = 'post'
    # serializer_class
    # queryset

    def post(self, request):
        content = {
            'message': None
        }

        try:
            apiMSM.execute_task_in_the_queue()
        except BaseException as e:
            logRecord = logger.info(
                msgPrivat=f"{str(e)}",
                msgPublic="Internal server error."
            )
            # content['message'] = 'Pong: Thread Task'
            content['error'] = logRecord.msgPublic
            statusResponse = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            content['message'] = 'Task successfully executed'
            statusResponse = status.HTTP_200_OK

        return Response(content, status=statusResponse)

    # path('sessions/<str:uuid>/get_page', apiREST.OperationGetPage.as_view()),
    # path('sessions/<str:uuid>/get_html', apiREST.OperationGetHTML.as_view()),


class OperationGetPage(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = 'get'
    # serializer_class
    # queryset

    def get(self, request, **kwargs):
        content = {
            'message': None
        }

        uuid = kwargs.get('uuid')
        url = request.query_params.get('url')

        try:
            apiMSM.operation_get_page(uuid_session=uuid, url=url)
            statusResponse = status.HTTP_200_OK
        except BaseException as e:
            log_record = logger.info(
                msg=f"{str(e)}",
                msg_public="Internal server error."
            )
            content['message'] = 'ERROR'
            content['error'] = log_record.msg_public
            statusResponse = status.HTTP_500_INTERNAL_SERVER_ERROR

            pass

        return Response(content, status=statusResponse)


class OperationGetHTML(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = 'get'
    # serializer_class
    # queryset

    def get(self, request,  **kwargs):
        content = {
            'message': None
        }

        uuid = kwargs.get('uuid')

        try:
            page_html = apiMSM.operation_get_html(uuid_session=uuid)
            content = page_html
            statusResponse = status.HTTP_200_OK
        except BaseException as e:
            log_record = logger.info(
                msg=f"{str(e)}",
                msg_public="Internal server error."
            )
            content['message'] = 'ERROR'
            content['error'] = log_record.msg_public
            statusResponse = status.HTTP_500_INTERNAL_SERVER_ERROR

            pass

        return Response(content, status=statusResponse)


class OperationElementsScan(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = 'post'
    # serializer_class
    # queryset

    def post(self, request,  **kwargs):
        content = {
            'message': None
        }

        uuid_session = kwargs.get('uuid_session')

        amount = None
        try:
            amount = apiMSM.operation_elements_scan(uuid_session=uuid_session)
        except BaseException as e:
            if hasattr(e, 'level'):
                level_error = e.level
            else:
                level_error = 50
            # -------------------------------
            if hasattr(e, 'uuid_log'):
                uuid_log = e.uuid_log
            else:
                uuid_log = None
            # -------------------------------
            if level_error <= 30:
                logRecord = logger.info(
                    msg=f"{str(e)}",
                    uuid_log=uuid_log
                )
            else:
                logRecord = logger.info(
                    msg=f"{str(e)}",
                    msg_public="Internal server error.",
                    uuid_log=uuid_log
                )

            content['message'] = 'ERROR'
            content['error'] = logRecord.msg_public
            statusResponse = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            content['message'] = 'Page successfully scanned.'
            content['data'] = {'amount': amount}
            statusResponse = status.HTTP_200_OK

        return Response(content, status=statusResponse)


class OperationElementsList(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = 'get'
    # serializer_class
    # queryset

    def get(self, request,  **kwargs):
        content = {
            'message': None
        }

        uuid_session = kwargs.get('uuid_session')

        try:
            elements_list = apiMSM.operation_elements_list(uuid_session=uuid_session)
            content['data'] = elements_list
        except BaseException as e:
            if hasattr(e, 'level'):
                level_error = e.level
            else:
                level_error = 50
            # -------------------------------
            if hasattr(e, 'uuid_log'):
                uuid_log = e.uuid_log
            else:
                uuid_log = None
            # -------------------------------
            if level_error <= 30:
                logRecord = logger.info(
                    msg=f"{str(e)}",
                    uuid_log=uuid_log
                )
            else:
                logRecord = logger.info(
                    msg=f"{str(e)}",
                    msg_public="Internal server error.",
                    uuid_log=uuid_log
                )

            content['message'] = 'ERROR'
            content['error'] = logRecord.msg_public
            statusResponse = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            statusResponse = status.HTTP_200_OK

        return Response(content, status=statusResponse)


class OperationElementsSendString(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = 'post'
    # serializer_class
    # queryset

    def post(self, request,  **kwargs):
        content = {
            'message': None
        }

        uuid_session = kwargs.get('uuid_session')
        uuid_element = kwargs.get('uuid_element')
        send_string = request.data.get("string")

        try:
            apiMSM.operation_element_send_string(uuid_session=uuid_session, uuid_auto_element=uuid_element, string=send_string)
        except BaseException as e:
            if hasattr(e, 'level'):
                level_error = e.level
            else:
                level_error = 50
            # -------------------------------
            if hasattr(e, 'uuid_log'):
                uuid_log = e.uuid_log
            else:
                uuid_log = None
            # -------------------------------
            if level_error <= 30:
                logRecord = logger.info(
                    msg=f"{str(e)}",
                    uuid_log=uuid_log
                )
            else:
                logRecord = logger.info(
                    msg=f"{str(e)}",
                    msg_public="Internal server error.",
                    uuid_log=uuid_log
                )

            content['message'] = 'ERROR'
            content['error'] = logRecord.msg_public
            statusResponse = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            content['message'] = 'Page successfully scanned.'
            content['data'] = {}
            statusResponse = status.HTTP_200_OK

        return Response(content, status=statusResponse)


class OperationElementsSendEnter(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = 'post'
    # serializer_class
    # queryset

    def post(self, request,  **kwargs):
        content = {
            'message': None
        }

        uuid_session = kwargs.get('uuid_session')
        uuid_element = kwargs.get('uuid_element')

        try:
            apiMSM.operation_element_send_enter(uuid_session=uuid_session, uuid_auto_element=uuid_element)
        except BaseException as e:
            if hasattr(e, 'level'):
                level_error = e.level
            else:
                level_error = 50
            # -------------------------------
            if hasattr(e, 'uuid_log'):
                uuid_log = e.uuid_log
            else:
                uuid_log = None
            # -------------------------------
            if level_error <= 30:
                logRecord = logger.info(
                    msg=f"{str(e)}",
                    uuid_log=uuid_log
                )
            else:
                logRecord = logger.info(
                    msg=f"{str(e)}",
                    msg_public="Internal server error.",
                    uuid_log=uuid_log
                )

            content['message'] = 'ERROR'
            content['error'] = logRecord.msg_public
            statusResponse = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            content['message'] = 'Page successfully scanned.'
            content['data'] = {}
            statusResponse = status.HTTP_200_OK

        return Response(content, status=statusResponse)


class OperationElementsSendClick(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = 'post'
    # serializer_class
    # queryset

    def post(self, request,  **kwargs):
        content = {
            'message': None
        }

        uuid_session = kwargs.get('uuid_session')
        uuid_element = kwargs.get('uuid_element')

        try:
            apiMSM.operation_element_click(uuid_session=uuid_session, uuid_auto_element=uuid_element)
        except BaseException as e:
            if hasattr(e, 'level'):
                level_error = e.level
            else:
                level_error = 50
            # -------------------------------
            if hasattr(e, 'uuid_log'):
                uuid_log = e.uuid_log
            else:
                uuid_log = None
            # -------------------------------
            if level_error <= 30:
                logRecord = logger.info(
                    msg=f"{str(e)}",
                    uuid_log=uuid_log
                )
            else:
                logRecord = logger.info(
                    msg=f"{str(e)}",
                    msg_public="Internal server error.",
                    uuid_log=uuid_log
                )

            content['message'] = 'ERROR'
            content['error'] = logRecord.msg_public
            statusResponse = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            content['message'] = 'Page successfully scanned.'
            content['data'] = {}
            statusResponse = status.HTTP_200_OK

        return Response(content, status=statusResponse)


class OperationGetCurrentUrl(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = 'get'
    # serializer_class
    # queryset

    def get(self, request,  **kwargs):
        content = {
            'message': None,
            'data': None
        }

        uuid_session = kwargs.get('uuid_session')

        try:
            current_url = apiMSM.operation_get_current_url(uuid_session=uuid_session)
            content['data'] = current_url
        except BaseException as e:
            if hasattr(e, 'level'):
                level_error = e.level
            else:
                level_error = 50
            # -------------------------------
            if hasattr(e, 'uuid_log'):
                uuid_log = e.uuid_log
            else:
                uuid_log = None
            # -------------------------------
            if level_error <= 30:
                logRecord = logger.info(
                    msg=f"{str(e)}",
                    uuid_log=uuid_log
                )
            else:
                logRecord = logger.info(
                    msg=f"{str(e)}",
                    msg_public="Internal server error.",
                    uuid_log=uuid_log
                )

            content['message'] = 'ERROR'
            content['error'] = logRecord.msg_public
            statusResponse = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            statusResponse = status.HTTP_200_OK

        return Response(content, status=statusResponse)

