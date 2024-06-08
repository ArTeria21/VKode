# testing/test_services.py

from django.test import TestCase
from QR_generator.models import QRCode, Transition, Category
from QR_generator.generation_services import (
    count_qr_code_hash,
    create_redirect_url,
    generate_qr_code,
    create_redirect_code,
    create_list_of_codes,
    get_transitions_by_code,
    get_dataframe_by_code,
    prepare_data_to_plot,
    get_plot_html,
    create_plot_from_qr
)
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from datetime import datetime, timezone, timedelta
import hashlib
import pandas as pd
import os

class ServicesTest(TestCase):
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
        self.request = HttpRequest()
        self.request.user = self.user

    def test_count_qr_code_hash(self):
        result = count_qr_code_hash(self.user.username, self.qr_code.code_name)
        expected_result = hashlib.sha3_256(f'{self.user.username} {self.qr_code.code_name}'.encode()).hexdigest()
        self.assertEqual(result, expected_result)

    def test_generate_qr_code(self):
        direction = 'http://example.com'
        file_path = generate_qr_code(direction)
        self.assertTrue(file_path.endswith('.png'))
        self.assertTrue(os.path.isfile(file_path))
        os.remove(file_path)  # Cleanup after test

    def test_create_redirect_code(self):
        code_hash, qr_path = create_redirect_code(self.user.username, 'Test QR Code')
        self.assertIsInstance(code_hash, str)
        self.assertTrue(qr_path.endswith('.png'))
        self.assertTrue(os.path.isfile(qr_path))
        os.remove(qr_path)  # Cleanup after test

    def test_create_list_of_codes(self):
        result = create_list_of_codes(self.request)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_get_transitions_by_code(self):
        Transition.objects.create(code=self.qr_code, user_agent='Mozilla/5.0', ip_address='127.0.0.1')
        transitions = get_transitions_by_code(self.qr_code)
        self.assertEqual(transitions.count(), 1)

    def test_get_dataframe_by_code(self):
        Transition.objects.create(code=self.qr_code, user_agent='Mozilla/5.0', ip_address='127.0.0.1')
        df = get_dataframe_by_code(self.qr_code)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)

    def test_prepare_data_to_plot(self):
        data = pd.DataFrame({
            'time_of_transition': [datetime.now(timezone.utc)],
            'users': ['Mozilla/5.0']
        })
        prepared_data = prepare_data_to_plot(data)
        self.assertIsInstance(prepared_data, pd.DataFrame)
        self.assertIn('minute_of_transition', prepared_data.columns)

    def test_get_plot_html(self):
        data = pd.DataFrame({
            'minute_of_transition': [datetime.now(timezone.utc)],
            'users': [1]
        })
        plot_html = get_plot_html(data)
        self.assertIn('<div>', plot_html)

    def test_create_plot_from_qr(self):
        Transition.objects.create(code=self.qr_code, user_agent='Mozilla/5.0', ip_address='127.0.0.1')
        plot_html = create_plot_from_qr(self.qr_code)
        self.assertIn('<div>', plot_html)
