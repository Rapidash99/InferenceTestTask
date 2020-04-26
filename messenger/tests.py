from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from .models import Message, User


class GetAllTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='Test1', password='qwertest')
        self.user2 = User.objects.create_user(username='Test2', password='qwertest')
        self.user3 = User.objects.create_user(username='Test3', password='qwertest')
        self.admin = User.objects.create_superuser(username='admin', password='admin')
        self.anon = AnonymousUser()

        self.token_user1 = Token.objects.create(user = self.user1)
        self.token_user2 = Token.objects.create(user = self.user2)
        self.token_user3 = Token.objects.create(user = self.user3)
        self.token_admin = Token.objects.create(user = self.admin)

        self.message00 = Message.objects.create(sender=self.admin, receiver=self.admin,
                                                text='TestMessageFromAdminToAdmin')
        self.message01 = Message.objects.create(sender=self.admin, receiver=self.user1,
                                                text='TestMessageFromAdminToUser1')
        self.message02 = Message.objects.create(sender=self.admin, receiver=self.user2,
                                                text='TestMessageFromAdminToUser2')
        self.message03 = Message.objects.create(sender=self.admin, receiver=self.user3,
                                                text='TestMessageFromAdminToUser3')
        self.message10 = Message.objects.create(sender=self.user1, receiver=self.admin,
                                                text='TestMessageFromUser1ToAdmin')
        self.message11 = Message.objects.create(sender=self.user1, receiver=self.user1,
                                                text='TestMessageFromUser1ToUser1')
        self.message12 = Message.objects.create(sender=self.user1, receiver=self.user2,
                                                text='TestMessageFromUser1ToUser2')
        self.message13 = Message.objects.create(sender=self.user1, receiver=self.user3,
                                                text='TestMessageFromUser1ToUser3')
        self.message20 = Message.objects.create(sender=self.user2, receiver=self.admin,
                                                text='TestMessageFromUser2ToAdmin')
        self.message21 = Message.objects.create(sender=self.user2, receiver=self.user1,
                                                text='TestMessageFromUser2ToUser1')
        self.message22 = Message.objects.create(sender=self.user2, receiver=self.user2,
                                                text='TestMessageFromUser2ToUser2')
        self.message23 = Message.objects.create(sender=self.user2, receiver=self.user3,
                                                text='TestMessageFromUser2ToUser3')
        self.message30 = Message.objects.create(sender=self.user3, receiver=self.admin,
                                                text='TestMessageFromUser3ToAdmin')
        self.message31 = Message.objects.create(sender=self.user3, receiver=self.user1,
                                                text='TestMessageFromUser3ToUser1')
        self.message32 = Message.objects.create(sender=self.user3, receiver=self.user2,
                                                text='TestMessageFromUser3ToUser2')
        self.message33 = Message.objects.create(sender=self.user3, receiver=self.user3,
                                                text='TestMessageFromUser3ToUser3')

        self.url_message_create = 'http://127.0.0.1:8000/api/v1/messenger/message/create/'
        self.url_message_all = 'http://127.0.0.1:8000/api/v1/messenger/message/all/'
        self.url_message_user = 'http://127.0.0.1:8000/api/v1/messenger/message/user/'
        self.url_message = 'http://127.0.0.1:8000/api/v1/messenger/message/'
        self.url_user_list = 'http://127.0.0.1:8000/api/v1/messenger/users/'

        self.client = APIClient()

    '''
    request 'get' method to get all the messages that User1 may see
    '''
    def test_get_all(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user1.key) # login by token as user1
        response = self.client.get(self.url_message_all) # request 'get' method

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 7) # got only his messages (where he is owner or receiver)

    def test_get_all_401(self):
        response = self.client.get(self.url_message_all) # request 'get' method to get all the messages that he may see

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'].code, 'not_authenticated')

    '''
    request 'post' method to create the message
    '''
    def test_post(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user1.key)
        response = self.client.post(self.url_message_create, data={'text': 'Yet another test text', 'receiver': 2})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        message_id = response.data['id']
        message = Message.objects.get(id=message_id)
        self.assertEqual(message.text, 'Yet another test text') # text is same
        self.assertEqual(message.receiver.id, 2) # user2 is receiver
        self.assertEqual(message.sender.id, 1) # user1 is sender
        self.assertFalse(message.edited) # message is not marked as 'edited'

    def test_post_401(self):
        response = self.client.post(self.url_message_create, data={'text': 'Yet another test text', 'receiver': 3})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'].code, 'not_authenticated')

    '''
    request 'get' method to get all the messages from chat with User2 by nickname
    '''
    def test_get_by_username(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user1.key)
        response = self.client.get(self.url_message_user + 'Test2')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # got only their messages (where User2 is owner or receiver, and User is receiver or owner)

    def test_get_by_username_401(self):
        response = self.client.get(self.url_message_user + 'Test2')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'].code, 'not_authenticated')

    '''
    request 'get' method to get all the messages from chat with User2 by id
    '''
    def test_get_by_user_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user1.key)
        response = self.client.get(self.url_message_user + '2')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # got only their messages

    def test_get_by_user_id_401(self):
        response = self.client.get(self.url_message_user + '2')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'].code, 'not_authenticated')

    '''
    request 'get' method to get the message by id
    '''
    def test_get_message_by_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user1.key)
        response = self.client.get(self.url_message + '7')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['receiver'] == self.user1.id or
                        response.data['sender'] == self.user1.id) # got his message

    def test_get_message_by_id_403(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user1.key)
        response = self.client.get(self.url_message + '9')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'].code, 'permission_denied')

    def test_get_message_by_id_401(self):
        response = self.client.get(self.url_message + '7')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'].code, 'not_authenticated')

    '''
    request 'patch' method to patch the message by id
    '''
    def test_patch_message_by_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user1.key)
        response = self.client.patch(self.url_message + '7', data={'text': 'Edited Text'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 'Edited Text')
        self.assertTrue(response.data['edited'])

    def test_patch_message_by_id_403(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user1.key)
        response = self.client.patch(self.url_message + '9', data={'text': 'Edited Text'})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'].code, 'permission_denied')

    def test_patch_message_by_id_401(self):
        response = self.client.patch(self.url_message + '7', data={'text': 'Edited Text'})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'].code, 'not_authenticated')

    '''
    request 'delete' method to delete the message by id
    '''

    def test_delete_message_by_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user1.key)

        count_before = Message.objects.count()
        response = self.client.delete(self.url_message + '7')
        count_after = Message.objects.count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(count_before - 1, count_after) # one message is deleted

    def test_delete_message_by_id_403(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user1.key)

        count_before = Message.objects.count()
        response = self.client.delete(self.url_message + '9')
        count_after = Message.objects.count()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'].code, 'permission_denied')
        self.assertEqual(count_before, count_after)

    def test_delete_message_by_id_401(self):
        count_before = Message.objects.count()
        response = self.client.delete(self.url_message + '7')
        count_after = Message.objects.count()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'].code, 'not_authenticated')
        self.assertEqual(count_before, count_after)


    def tearDown(self):
        self.client.credentials()
