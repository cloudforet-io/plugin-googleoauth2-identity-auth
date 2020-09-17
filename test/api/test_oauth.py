import os
import uuid
import unittest
from spaceone.core.unittest.runner import RichTestRunner

from spaceone.tester.unittest import TestCase, to_json, print_json

def random_string():
    return uuid.uuid4().hex

TOKEN = "put your token"

class TestOAuth(TestCase):

    def test_login(self):
        options = {'domain': 'mz.co.kr'}
        credentials = {
        }
        user_credentials = {
            'access_token': TOKEN
        }
        user_info = self.identity.Auth.login({'options':options, 'secret_data':credentials, 'user_credentials':user_credentials})
        print_json(user_info)
        self.assertEqual(user_info.state, 'ENABLED')

    def test_verify(self):
        options = {
            'domain': 'mz.co.kr'
        }
        credentials = {}
 
        auth_v_info = self.identity.Auth.verify({'options':options, 'secret_data':credentials})
        j = to_json(auth_v_info)
        print(j)
        self.assertEqual(j['options']['auth_type'], 'google_oauth2')

    def test_find(self):
        options = {'domain': 'mz.co.kr'}
        credentials = {
        }
        user_id = 'choonho.son@mz.co.kr'
        users_info = self.identity.Auth.find({'options':options, 'secret_data':credentials, 'user_id':user_id})
        j = to_json(users_info)
        print(j)
        self.assertEqual(j['total_count'], 1)

    def test_find_failure(self):
        """ Wrong domain name
        """
        options = {'domain': 'mz.co.kr'}
        credentials = {
        }
        user_id = 'choonho.son@gmail.com'
        users_info = self.identity.Auth.find({'options':options, 'secret_data':credentials, 'user_id':user_id})

    def test_find_failure2(self):
        """ No domain name
        """
        options = {'domain': 'mz.co.kr'}
        credentials = {
        }
        user_id = 'choonho.son'
        users_info = self.identity.Auth.find({'options':options, 'secret_data':credentials, 'user_id':user_id})

    def test_find_failure3(self):
        """ Not support keyword search
        """
        options = {'domain': 'mz.co.kr'}
        credentials = {
        }
        user_id = 'choonho.son'
        users_info = self.identity.Auth.find({'options':options, 'secret_data':credentials, 'keyword':user_id})


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)

