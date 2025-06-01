import unittest
from flask import current_app
from apps.user.models import User, UserRole
from core.extensions import db


class UserAuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = current_app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_registration(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123',
            'role': 'tenant'
        }

        response = self.client.post('/api/v1/auth/register', json=data)
        self.assertEqual(response.status_code, 201)

        user = User.get_by_username('testuser')
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')

    # 添加更多测试用例...