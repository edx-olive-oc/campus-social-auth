from mock import patch
from six.moves.html_parser import HTMLParser

from django.test import TestCase
from django.contrib.auth.models import User

from campus_social_auth.backends.utils import UsernameGenerator


class GenerateUsernameTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='my_self_user'
        )
        self.fullname = 'My Self User'

    def test_separator(self):
        """
        The first step to generate a hinted username is the separator character of the
        full name string. This test makes sure that we are generating a username replacing
        all whitespaces by a character configured in settings or in site_configurations.
        """
        saml_other_settings = {'SEPARATOR': '.'}
        generator = UsernameGenerator(saml_other_settings)
        username = generator.replace_separator(self.fullname)
        return self.assertEqual(username, "My.Self.User")

    def test_generate_username_in_lowercase(self):
        """
        Test if the full name that comes from insert_separator method
        it's converted in lowercase.
        """
        saml_other_settings = {'LOWER': True}
        generator = UsernameGenerator(saml_other_settings)
        new_username = generator.process_case('My_Self_User')
        return self.assertEqual(new_username, 'my_self_user')

    def test_generate_username_not_lowercase(self):
        """
        Test if the full name that comes from insert_separator method
        is not converted in lowercase and preserves their original lowercases and
        uppers cases.
        """
        saml_other_settings = {'LOWER': False}
        generator = UsernameGenerator(saml_other_settings)
        new_username = generator.process_case('My_Self_User')
        return self.assertEqual(new_username, 'My_Self_User')

    def test_generate_username_unicode(self):
        """
        Ensure that unique usernames can be generated from unicode base names.

        Uses HTML escaping to accurately reproduce an issue experienced with unicode names in decoded HTML requests.
        """
        h = HTMLParser()
        escaped_name = '&#1495;&#1497;&#1497;&#1501;_&#1506;&#1502;&#1512;&#1504;&#1497;'
        username = h.unescape(escaped_name)
        user_exists = User.objects.create(username=username)

        generator = UsernameGenerator()
        new_username = generator.generate_username(username)
        return self.assertEqual(new_username, u'{}_1'.format(username))

    def test_generate_username_with_consecutive(self):
        """
        It should return a new user with a consecutive number.
        """
        saml_other_settings = {'RANDOM': False}
        for i in range(1, 6):
            User.objects.create(
                username='my_self_user_{}'.format(i)
            )
        generator = UsernameGenerator(saml_other_settings)
        new_username = generator.generate_username(self.fullname)
        # We have 6 users: Five created in the loop with a consecutive
        # number and another one that comes from initial setUp,
        # the first has not consecutive number due to is
        # not neccesary append an differentiator. We expect a new user with
        # the consecutive number 6.
        return self.assertEqual(new_username, 'my_self_user_6')

    @patch('campus_social_auth.backends.utils.UsernameGenerator.get_random')
    def test_generate_username_with_random(self, mock_random):
        """
        It should return a username with a random integer
        at the end of the username generated.
        """
        saml_other_settings = {'RANDOM': True}
        mock_random.return_value = 4589
        generator = UsernameGenerator(saml_other_settings)
        new_username = generator.generate_username(self.fullname)
        return self.assertEqual(new_username, 'my_self_user_4589')

    @patch('campus_social_auth.backends.utils.UsernameGenerator.get_random')
    def test_generate_username_with_repetitive_random(self, mock_random):
        """
        If a random generated number is repeated, should append
        a suffix with another random that does not exists.
        """
        saml_other_settings = {'RANDOM': True}
        mock_random.side_effect = [4589, 9819]
        User.objects.create(username='my_self_4589')
        User.objects.create(username='my_self')
        generator = UsernameGenerator(saml_other_settings)
        new_username = generator.generate_username('My Self')
        return self.assertEqual(new_username, 'my_self_9819')

    def test_username_without_modifications(self):
        """
        If the provided username does not exists
        in database, should return the username without
        any modifications of suffix number.
        """
        saml_other_settings = {'RANDOM': True}
        not_existing_user = 'Another Myself'
        generator = UsernameGenerator(saml_other_settings)
        new_username = generator.generate_username(not_existing_user)
        return self.assertEqual(new_username, 'another_myself')
