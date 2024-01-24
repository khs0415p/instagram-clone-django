from django.test import TestCase
from user.models import User
from django.contrib.auth.hashers import make_password

# Create your tests here.

class UserTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email='test_login@test.com',
            nickname='test_login_nickname',
            name='test_name',
            password=make_password('test_password'),
            profile_image='default_profile.jpg'
        )
    
    
    def test_join(self):
        response = self.client.post('/user/join', data = {
        'email' : 'test_email@test.com',
        'nickname' : 'test_nickname',
        'name' : 'test_name',
        'password' : 'test_password'
        })
        # 가입 API가 잘 동작하는지
        self.assertEqual(response.status_code, 200)
        
        # 실제 회원가입이 완료가 되었는지
        user = User.objects.filter(email='test_email@test.com').first()
        self.assertEqual(user.nickname, 'test_nickname')
        self.assertEqual(user.name, 'test_name')
        self.assertTrue(user.check_password('test_password'))
        
        
    def test_login(self):
        response = self.client.post('/user/login', data = {
            'email' : 'test_login@test.com',
            'password' : 'test_password'
        })