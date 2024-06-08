from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from QR_generator.models import QRCode, Category, Transition

from datetime import datetime, timedelta, timezone


class CategoryTest(TestCase):
	CATEGORY_NAME = 'Тестирование'
	def setUp(self):
		self.test_category = Category.objects.create(category=self.CATEGORY_NAME)

	def test_category_creation(self):
		self.assertIsInstance(self.test_category, Category)
		self.assertEqual(self.test_category.category, self.CATEGORY_NAME)


class QRCodeTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(category='TestCategory')
        self.qr_code_data = {
            'code_name': 'Test QR Code',
            'owner': self.user,
            'direction': 'http://example.com',
            'category': self.category,
            'end_time': datetime.now(timezone.utc) + timedelta(days=1),
            'path_to_file': '/path/to/qrcode',
            'code_hash': 'some_unique_hash'
        }

    def test_qr_code_creation(self):
        qr_code = QRCode.objects.create(**self.qr_code_data)
        self.assertIsInstance(qr_code, QRCode)
        self.assertEqual(qr_code.code_name, 'Test QR Code')
        self.assertEqual(qr_code.owner, self.user)
        self.assertEqual(qr_code.direction, 'http://example.com')
        self.assertEqual(qr_code.category, self.category)
        self.assertEqual(qr_code.path_to_file, '/path/to/qrcode')
        self.assertEqual(qr_code.code_hash, 'some_unique_hash')

    def test_unique_code_hash(self):
        QRCode.objects.create(**self.qr_code_data)
        with self.assertRaises(IntegrityError):
            QRCode.objects.create(**self.qr_code_data)

    def test_unique_code_name_owner(self):
        QRCode.objects.create(**self.qr_code_data)
        qr_code_data_different_owner = self.qr_code_data.copy()
        qr_code_data_different_owner['owner'] = None
        qr_code_data_different_owner['code_hash'] = 'another_unique_hash'
        QRCode.objects.create(**qr_code_data_different_owner)

        qr_code_data_same_name_diff_owner = self.qr_code_data.copy()
        qr_code_data_same_name_diff_owner['code_name'] = 'Test QR Code'
        qr_code_data_same_name_diff_owner['code_hash'] = 'third_unique_hash'
        with self.assertRaises(IntegrityError):
            QRCode.objects.create(**qr_code_data_same_name_diff_owner)

    def test_str_method(self):
        qr_code = QRCode.objects.create(**self.qr_code_data)
        self.assertEqual(str(qr_code), '<QR code: Test QR Code>')

    def test_end_time_validator(self):
        qr_code_data_invalid_end_time = self.qr_code_data.copy()
        qr_code_data_invalid_end_time['end_time'] = datetime.now(timezone.utc) - timedelta(days=1)
        qr_code = QRCode(**qr_code_data_invalid_end_time)
        with self.assertRaises(ValidationError):
            qr_code.full_clean()
            

class TransitionTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(category='TestCategory')
        self.qr_code = QRCode.objects.create(
            code_name='Test QR Code',
            owner=self.user,
            direction='http://example.com',
            category=self.category,
            end_time=datetime.now(timezone.utc) + timedelta(days=1),
            path_to_file='/path/to/qrcode',
            code_hash='some_unique_hash'
        )
        self.transition_data = {
            'code': self.qr_code,
            'user_agent': 'Mozilla/5.0',
            'ip_address': '127.0.0.1'
        }

    def test_transition_creation(self):
        transition = Transition.objects.create(**self.transition_data)
        self.assertIsInstance(transition, Transition)
        self.assertEqual(transition.code, self.qr_code)
        self.assertEqual(transition.user_agent, 'Mozilla/5.0')
        self.assertEqual(transition.ip_address, '127.0.0.1')

    def test_transition_without_ip(self):
        transition_data_no_ip = self.transition_data.copy()
        transition_data_no_ip['ip_address'] = None
        transition = Transition.objects.create(**transition_data_no_ip)
        self.assertIsInstance(transition, Transition)
        self.assertEqual(transition.code, self.qr_code)
        self.assertEqual(transition.user_agent, 'Mozilla/5.0')
        self.assertIsNone(transition.ip_address)

    def test_transition_with_invalid_ip(self):
        transition_data_invalid_ip = self.transition_data.copy()
        transition_data_invalid_ip['ip_address'] = 'invalid_ip'
        with self.assertRaises(ValidationError):
            transition = Transition(**transition_data_invalid_ip)
            transition.full_clean()
