from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from pullgerMultisessionManager import api
from . import serializers

class ping(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content ={'message': 'Pong'}
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
def sessionOperations(request, uuid):
    if request.method == 'DELETE':
        statusResp = status.HTTP_200_OK
        try:
            api.killSession(uuid=uuid)
            content = {'message': f'Session {uuid} deleted:'}
        except:
            content = {'message': 'error'}
            statusResp = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(content, status=statusResp)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def sessionOperationsGeneral(request):
    if request.method == 'GET':
        sessionList = api.getSessionsList()

        serializedContent = serializers.SessionsListSerializer(sessionList, many=True)
        content ={'message': 'OK', 'data': serializedContent.data}

        response = Response(content)
        response['Cache-Control'] = 'no-cache'

        return response
    elif request.method == 'POST':
        try:
            api.addNewSession()
            content = {'message': 'Session added'}
        except BaseException as e:
            content ={'message': f'error: {str(e)}'}

        return Response(content)