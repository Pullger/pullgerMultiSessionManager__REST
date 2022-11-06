from rest_framework.test import APITestCase
from pullgerAuthJWT.tests import unit as unit_auth_jwt
from pullgerMultiSessionManager__REST.tests.tools import unitOperationsMSMRest


class Test_000_Operations(APITestCase):
    def setUp(self):
        unit_auth_jwt.UnitOperations.CreateUser(self)
        unit_auth_jwt.UnitOperations.GetToken(self)

    def test_002_00_00_send_string_operation_all_sessions(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        from pullgerSquirrel.connectors import connector

        # for i in range(2):
        # if i == 0:
        #                 uuid_session = UnitOperations.add_new_session_selenium_standard(self)
        #             elif i == 1:
        #                 uuid_session = UnitOperations.add_new_session_selenium_headless(self)

        # uuid_session = UnitOperations.add_session(self, connector.selenium.chrome.standard)
        # uuid_session = UnitOperations.add_session(self, connector.selenium.chrome.headless)
        uuid_session = unitOperationsMSMRest.add_session(self, connector.selenium.stand_alone.general)

        url = "https://google.com"
        resultGet = self.client.get(f"/pullgerMSM/api/sessions/{uuid_session}/get_page?url={url}")
        self.assertEqual(resultGet.status_code, 200, "General API Critical error.")

        result_scan = self.client.post(f"/pullgerMSM/api/sessions/{uuid_session}/elements_scan")

        result_elements_list = self.client.get(f"/pullgerMSM/api/sessions/{uuid_session}/elements_list")

        uuid_element = result_elements_list.data['data'][1]['uuid_auto_element']

        send_data = {'string': "test"}
        result_sending = self.client.post(
            f"/pullgerMSM/api/sessions/{uuid_session}/{uuid_element}/send_string",
            send_data
        )

        result_sending = self.client.post(
            f"/pullgerMSM/api/sessions/{uuid_session}/{uuid_element}/send_enter"
        )

        result_sending = self.client.get(
            f"/pullgerMSM/api/sessions/{uuid_session}/get_current_url"
        )

        current_url = result_sending.data['data']
        find_mark = current_url.find("google.com/search?")
        self.assertNotEqual(find_mark, -1, "Incorrect search operation.")

        self.client.delete(f"/pullgerMSM/api/sessions/{uuid_session}")

    def test_000_01_00_send_string_operation_all_sessions(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        from pullgerSquirrel.connectors import connector

        # for i in range(2):
        # if i == 0:
        #                 uuid_session = UnitOperations.add_new_session_selenium_standard(self)
        #             elif i == 1:
        #                 uuid_session = UnitOperations.add_new_session_selenium_headless(self)

        # uuid_session = UnitOperations.add_session(self, connector.selenium.chrome.standard)
        # uuid_session = UnitOperations.add_session(self, connector.selenium.chrome.headless)
        uuid_session = unitOperationsMSMRest.add_session(self, connector.selenium.stand_alone.general)


        url = "https://translate.google.com"
        resultGet = self.client.get(f"/pullgerMSM/api/sessions/{uuid_session}/get_page?url={url}")
        self.assertEqual(resultGet.status_code, 200, "General API Critical error.")

        result_elements_list = self.client.get(f"/pullgerMSM/api/sessions/{uuid_session}/elements_list")

        uuid_element = result_elements_list.data['data'][11]['uuid_auto_element']

        result_sending = self.client.post(
            f"/pullgerMSM/api/sessions/{uuid_session}/{uuid_element}/send_click"
        )

        self.client.delete(f"/pullgerMSM/api/sessions/{uuid_session}")
