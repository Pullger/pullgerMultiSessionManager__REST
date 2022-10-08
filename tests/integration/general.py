from rest_framework.test import APITestCase
from pullgerAuthJWT.tests import unit as unitAuthJWT
from pullgerMultiSessionManager__REST.tests import UnitOperations


class Test_000_REST(APITestCase):
    def setUp(self):
        unitAuthJWT.UnitOperations.CreateUser(self)
        unitAuthJWT.UnitOperations.GetToken(self)

    def test_001_00_00_Interface(self):
        resultGet = self.client.get("/pullgerMM/api/ping")
        self.assertEqual(resultGet.status_code, 200, "General API Critical error.")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        resultGet = self.client.get("/pullgerMM/api/pingAuth")

        self.assertEqual(resultGet.status_code, 200, "General API Critical error with authentication.")

    def test_002_00_00_AccessRestictions(self):
        response = self.client.post('/pullgerMM/api/sessions')
        self.assertEqual(response.status_code, 401, "Incorrect functioning of the authorization check.")

        # self.client.request()
        # self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # response = self.client.generic('GET', '/pullgerMM/api/sessions')
        pass
        #TODO Fill all requests

    def test_004_00_00_LinkedIN_Sessions(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        from pullgerAccountManager__REST.tests import UnitOperations as UnitOperationsAMRest
        UnitOperationsAMRest.addAccountForLinkedIN(self)

        UnitOperations.add_session_linkedin_standard(self)

        UnitOperations.make_all_session_authorization(self)

        pass

    def test_005_00_00_GeneralOperations(self):
        def createAndKillStandardSessions():
            UnitOperations.addSession(self)
            #TODO Fix error on creatin session
            #TODO Add request for delete sesion
            pass

            # sessionUUID = api.addNewSession()
            # self.assertNotEqual(sessionUUID, None, 'Error on creating new session')
            # resultKillSession = api.killSession(uuid=sessionUUID)
            # self.assertEqual(resultKillSession, None, 'Error on killing empy session')

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        createAndKillStandardSessions();

    def test_000_00_00_ExecutingQueue(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        UnitOperations.execute_task_in_the_queue(self)

        pass


#     def test_001_SessionManager_smoke(self):
#         def createAndKillStandardSessions():
#             sessionUUID = api.addNewSession()
#             self.assertNotEqual(sessionUUID, None, 'Error on creating new session')
#             resultKillSession = api.killSession(uuid=sessionUUID)
#             self.assertEqual(resultKillSession, None, 'Error on killing empy session')
#         def createAndKillAuthorizationLinkedINSessions():
#             resultKillSession = api.killSession(uuid=sessionUUID)
#             self.assertEqual(resultKillSession, None, 'Error on killing empy session')
#
#         createAndKillStandardSessions();
#         createAndKillAuthorizationLinkedINSessions()
#
#     def test_000_SessionManager_getSessionList(self):
#         testUUID = []
#         testUUID.append(api.addNewSession())
#         testUUID.append(api.addNewSession())
#         sessionList = api.getSessionsList()
#
#         for index in range(0, 2):
#             self.assertEqual(sessionList[index]['uuid'] , testUUID[index])
#
# class Test_001_Operation(TestCase):
#     def test_001_initiation(self):
#         '''
#             Testing mechenisme initialisation
#         '''
#
#
#         reglament_app = apps.get_app_config('pullgerMultiSessionManager')
#         self.assertIsInstance(reglament_app.multisessionManager, core.ConnectionManager, " Incorrect creating on django APP")
#
#     def test_002_TaskStack(self):
#         reglament_app = apps.get_app_config('pullgerMultiSessionManager')
#         multisessionManager = reglament_app.multisessionManager
#
#         def smokeTest():
#             uuidTask1 = None
#             uuidTask2 = None
#
#             def addTask():
#
#                 global uuidTask1
#                 uuidTask1 = multisessionManager.taskStack.addTask()
#                 self.assertIsInstance(uuidTask1, str, 'Incorrect retyrn type')
#                 self.assertEqual(len(uuidTask1), 36, 'Incorrect retyrn type')
#
#                 self.assertEqual(len(multisessionManager.taskStack._taskList), 1, "Incorrect append task")
#                 self.assertEqual(multisessionManager.taskStack._taskList[0]['uuid'], uuidTask1, "Incorrect task creating")
#
#                 global uuidTask2
#                 uuidTask2 = multisessionManager.taskStack.addTask()
#                 self.assertIsInstance(uuidTask2, str, 'Incorrect retyrn type')
#                 self.assertEqual(len(uuidTask2), 36, 'Incorrect retyrn type')
#
#                 self.assertEqual(len(multisessionManager.taskStack._taskList), 2, "Incorrect append task")
#                 self.assertEqual(multisessionManager.taskStack._taskList[1]['uuid'], uuidTask2, "Incorrect task creating")
#
#                 self.assertNotEqual(uuidTask1, uuidTask2)
#
#             def deleteTask():
#                 global uuidTask1
#                 global uuidTask2
#
#                 self.assertEqual(len(multisessionManager.taskStack._taskList), 2, "Incorrect start position")
#                 multisessionManager.taskStack.deleteTask(uuidTask1)
#                 self.assertEqual(len(multisessionManager.taskStack._taskList), 1, "Incorrect delete task")
#                 multisessionManager.taskStack.deleteTask(uuidTask2)
#                 self.assertEqual(len(multisessionManager.taskStack._taskList), 0, "Incorrect delete task")
#
#             addTask()
#             deleteTask()
#
#         def internalIntegration():
#             self.assertEqual(len(multisessionManager.taskStack._taskList), 0, "Incorrect initialisation state")
#
#             taskStructure1 = {
#                 'authorization': 'ATest1',
#                 'loader': 'LTest1',
#                 'finisher': 'FTest1',
#             }
#
#             uuidTask1 = multisessionManager.taskStack.addTask(**taskStructure1)
#             for curTSkey,  curTSValue in taskStructure1.items():
#                 self.assertIn(curTSkey, multisessionManager.taskStack._taskList[0], "Property does't exist.")
#                 self.assertEqual(multisessionManager.taskStack._taskList[0][curTSkey], curTSValue, 'Incorrect data translation.')
#             multisessionManager.taskStack.deleteTask(uuidTask1)
#
#         # def exceptations():
#         #     multisessionManager.taskStack.deleteTask('sfsfsf')
#         #     pass
#
#         smokeTest()
#         internalIntegration()
#
#     def test_003_SessionManager(self):
#         reglament_app = apps.get_app_config('pullgerMultiSessionManager')
#         multisessionManager = reglament_app.multisessionManager
#
#         def smokeTest():
#             sessionUUID = multisessionManager.sessionManager.addNewSession()
#             killResult =  multisessionManager.sessionManager.killSession(sessionUUID)
#             self.assertEqual(killResult, True, "Can't kill session after creation.")
#
#         smokeTest()