from rest_framework.test import APITestCase


def addSession(self: APITestCase):
    responseCreateSession = self.client.post('/pullgerMM/api/sessions')
    self.assertEqual(responseCreateSession.status_code, 200, "Incorrect status session creating request")

    responseSessionList = self.client.get('/pullgerMM/api/sessions')
    self.assertEqual(len(responseSessionList.data.get('data')), 1, "Incorrect appending session.")


def add_session(self: APITestCase, conn):
    from pullgerAccountManager import authorizationsServers

    bodyRequest = {
        'authorization': str(authorizationsServers.linkedin.instances.general),
        'connector': str(conn)
    }

    responseCreateSession = self.client.post(f"/pullgerMSM/api/sessions", bodyRequest)
    self.assertEqual(responseCreateSession.status_code, 200, "Incorrect status session creating request")
    self.assertNotEquals(responseCreateSession.data.get('data'), None, "Incorrect response structure")
    session_uuid = responseCreateSession.data.get('data').get('uuid')
    self.assertNotEquals(session_uuid, None, "Incorrect response structure")
    self.assertIsInstance(session_uuid, str, "Incorrect type in response")
    self.assertEqual(len(session_uuid), 36, "Incorrect response value")

    responseSession_list = self.client.get(f"/pullgerMSM/api/sessions")
    self.assertEqual(responseCreateSession.status_code, 200, "Incorrect status session get sessions list")
    self.assertEqual(len(responseSession_list.data.get('data')), 1, "Incorrect appending session.")

    return session_uuid


def add_session_linkedin_standard(self: APITestCase):
    from pullgerAccountManager import authorizationsServers
    from pullgerSquirrel.connectors import connector

    bodyRequest = {
        'authorization': str(authorizationsServers.linkedin.instances.general),
        'connector': str(connector.selenium.chrome.standard)
    }

    responseCreateSession = self.client.post(f"/pullgerMSM/api/sessions", bodyRequest)
    self.assertEqual(responseCreateSession.status_code, 200, "Incorrect status session creating request")

    responseSessionList = self.client.get(f"/pullgerMSM/api/sessions")
    self.assertEqual(responseCreateSession.status_code, 200, "Incorrect status session get sessions list")
    self.assertEqual(len(responseSessionList.data.get('data')), 1, "Incorrect appending session.")


def add_session_linkedin_no_head(self: APITestCase):
    from pullgerAccountManager import authorizationsServers
    from pullgerSquirrel.connectors import connector

    bodyRequest = {
        'authorization': str(authorizationsServers.linkedin.instances.general),
        'connector': str(connector.selenium.chrome.headless)
    }

    responseCreateSession = self.client.post(f"/pullgerMSM/api/sessions", bodyRequest)
    self.assertEqual(responseCreateSession.status_code, 200, "Incorrect status session creating request")

    responseSessionList = self.client.get(f"/pullgerMSM/api/sessions")
    self.assertEqual(responseCreateSession.status_code, 200, "Incorrect status session get sessions list")
    self.assertEqual(len(responseSessionList.data.get('data')), 1, "Incorrect appending session.")


def make_all_session_authorization(self: APITestCase):
    responseCreateSession = self.client.put(f'/pullgerMSM/api/sessions/makeAllSessionAuthorization')
    self.assertEqual(responseCreateSession.status_code, 200, 'Error on authorization sessions')


def execute_task_in_the_queue(self: APITestCase):
    resultPost = self.client.post(f"/pullgerMSM/api/sessions/executeTaskInTheQueue")
    self.assertEqual(resultPost.status_code, 200, "Error on task executed.")

