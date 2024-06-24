import unittest
from api.main import app
from unittest.mock import patch

class TestMain(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_simulations_success(self):
        with patch('simulation.simulation.Simulation.run', return_value = ({"message": "Simulation successful"}, 200)):
            response = self.app.get('/simulations', query_string = {
                'bank': 'Inter',
                'financing_value': '150000',
                'installments_number': '120',
                'age': '30'
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), { "message": "Simulation successful" })

    def test_simulations_missing_params(self):
        response = self.app.get('/simulations', query_string={
            'bank': 'Inter',
            'financing_value': '150000',
            'installments_number': '120'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), { "error": "It's necessary to specify all these parameters: bank, financing_value, installments_number, age"})

    def test_simulations_bank_not_supported(self):
        response = self.app.get('/simulations', query_string={
            'bank': 'Nubank',
            'financing_value': '150000',
            'installments_number': '120',
            'age': '30'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), { "error": "Bank 'Nubank' is not supported."})

    def test_simulations_invalid_financing_value(self):
        response = self.app.get('/simulations', query_string={
            'bank': 'Inter',
            'financing_value': '90000',
            'installments_number': '120',
            'age': '30'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Value error, Financing value must be greater than 100000"})
    
    def test_simulations_invalid_installments_number(self):
        response = self.app.get('/simulations', query_string={
            'bank': 'Inter',
            'financing_value': '150000',
            'installments_number': '50',
            'age': '30'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Value error, Invalid installments number, must be one of 60, 90, 120, 150, 180, 240, 360, 420"})

    def test_simulations_invalid_age_plus_installments_number(self):
        response = self.app.get('/simulations', query_string={
            'bank': 'Inter',
            'financing_value': '150000',
            'installments_number': '120',
            'age': '79'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "The age of the customer plus the number of installments cannot exceed 80 years"})
    
    def test_simulations_invalid_age(self):
        response = self.app.get('/simulations', query_string={
            'bank': 'Inter',
            'financing_value': '150000',
            'installments_number': '120',
            'age': '85'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Value error, Age must be between 18 and 80"})

    def test_simulations_validate_order_1(self):
        response = self.app.get('/simulations', query_string={
            'bank': 'Inter',
            'financing_value': '150000',
            'installments_number': '50',
            'age': '85'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Value error, Age must be between 18 and 80"})

    def test_simulations_validate_order_2(self):
        response = self.app.get('/simulations', query_string={
            'bank': 'Inter',
            'financing_value': '150',
            'installments_number': '50',
            'age': '20'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Value error, Invalid installments number, must be one of 60, 90, 120, 150, 180, 240, 360, 420"})

if __name__ == '__main__':
    unittest.main()
