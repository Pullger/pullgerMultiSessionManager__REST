from rest_framework.test import APITestCase
from pullgerAuthJWT.tests import unit as unit_auth_jwt
from pullgerMultiSessionManager__REST.tests import UnitOperations


class Test_000_Operations(APITestCase):
    def setUp(self):
        unit_auth_jwt.UnitOperations.CreateUser(self)
        unit_auth_jwt.UnitOperations.GetToken(self)

    def test_004_00_00_LinkedIN_Sessions(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        from pullgerSquirrel.connectors import connector

        uuid_session = UnitOperations.add_session(self, connector.selenium.chrome.standard)
        # uuid_session = UnitOperations.add_session(self, connector.selenium.chrome.headless)

        url = "https://google.com"
        resultGet = self.client.get(f"/pullgerMSM/api/sessions/{uuid_session}/get_page?url={url}")
        self.assertEqual(resultGet.status_code, 200, "General API Critical error.")

        resultGet = self.client.get(f"/pullgerMSM/api/sessions/{uuid_session}/get_html")
        self.assertEqual(resultGet.status_code, 200, "General API Critical error.")

        pass

        # UnitOperations.add_session_linkedin_standard(self)
        #
        # UnitOperations.make_all_session_authorization(self)
        #
        # pass