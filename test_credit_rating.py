# import unittest
# import json
# from enum import Enum
# from typing import Dict, Union

# # Import the functions and classes from the original script
# from credit_rating_mock import (
#     LoanType, 
#     PropertyType, 
#     CreditRating,
#     calculate_mortgage_risk_score,
#     calculate_credit_rating,
#     parse_mortgage_from_json,
#     validate_mortgage_data
# )

# class TestMortgageRiskAssessment(unittest.TestCase):
#     def setUp(self):
#         """Set up test data that can be reused across multiple test methods."""
        # self.valid_mortgage_low_risk = {
        #     "credit_score": 750,
        #     "loan_amount": 200000,
        #     "property_value": 250000,
        #     "annual_income": 60000,
        #     "debt_amount": 20000,
        #     "loan_type": 'fixed',
        #     "property_type": 'single_family'
        # }
        
        # self.valid_mortgage_high_risk = {
        #     "credit_score": 620,
        #     "loan_amount": 220000,
        #     "property_value": 230000,
        #     "annual_income": 40000,
        #     "debt_amount": 25000,
        #     "loan_type": 'adjustable',
        #     "property_type": 'condo'
        # }

#     def test_calculate_mortgage_risk_score_low_risk(self):
#         """Test risk score calculation for a low-risk mortgage."""
#         risk_score = calculate_mortgage_risk_score(self.valid_mortgage_low_risk)
#         self.assertEqual(risk_score, 0)  # Expecting lowest risk score

#     def test_calculate_mortgage_risk_score_high_risk(self):
#         """Test risk score calculation for a high-risk mortgage."""
#         risk_score = calculate_mortgage_risk_score(self.valid_mortgage_high_risk)
#         self.assertEqual(risk_score, 4)  # Expecting higher risk score

#     def test_calculate_credit_rating_multiple_mortgages(self):
#         """Test credit rating calculation with multiple mortgages."""
#         mortgages = [
#             self.valid_mortgage_low_risk,
#             {
#                 "credit_score": 680,
#                 "loan_amount": 180000,
#                 "property_value": 200000,
#                 "annual_income": 50000,
#                 "debt_amount": 15000,
#                 "loan_type": 'fixed',
#                 "property_type": 'single_family'
#             }
#         ]
#         rating = calculate_credit_rating(mortgages)
#         self.assertEqual(rating, CreditRating.AAA)

#     def test_parse_mortgage_from_json_valid(self):
#         """Test parsing valid JSON payload."""
#         json_payload = json.dumps({
#             "mortgages": [self.valid_mortgage_low_risk]
#         })
#         mortgages = parse_mortgage_from_json(json_payload)
#         self.assertEqual(len(mortgages), 1)
#         self.assertEqual(mortgages[0]['credit_score'], 750)

#     def test_parse_mortgage_from_json_invalid_format(self):
#         """Test parsing invalid JSON format."""
#         with self.assertRaises(ValueError):
#             parse_mortgage_from_json("invalid json")

#     def test_validate_mortgage_data_valid(self):
#         """Test validation of valid mortgage data."""
#         mortgages = validate_mortgage_data([self.valid_mortgage_low_risk])
#         self.assertEqual(len(mortgages), 1)

#     def test_validate_mortgage_data_missing_keys(self):
#         """Test validation with missing keys."""
#         invalid_mortgage = {
#             "credit_score": 700,
#         }
#         with self.assertRaises(ValueError) as context:
#             validate_mortgage_data([invalid_mortgage])
        
#         self.assertIn("Missing required keys", str(context.exception))

#     def test_validate_mortgage_data_invalid_credit_score(self):
#         """Test validation with invalid credit score."""
#         invalid_mortgage = dict(self.valid_mortgage_low_risk)
#         invalid_mortgage['credit_score'] = 200  # Out of valid range
        
#         with self.assertRaises(ValueError) as context:
#             validate_mortgage_data([invalid_mortgage])
        
#         self.assertIn("Credit score must be between 300 and 850", str(context.exception))

#     def test_validate_mortgage_data_negative_loan_amount(self):
#         """Test validation with negative loan amount."""
#         invalid_mortgage = dict(self.valid_mortgage_low_risk)
#         invalid_mortgage['loan_amount'] = -50000
        
#         with self.assertRaises(ValueError) as context:
#             validate_mortgage_data([invalid_mortgage])
        
#         self.assertIn("Loan amount must be positive", str(context.exception))

#     def test_validate_mortgage_data_loan_exceeding_property_value(self):
#         """Test validation when loan amount exceeds property value."""
#         invalid_mortgage = dict(self.valid_mortgage_low_risk)
#         invalid_mortgage['loan_amount'] = 300000  # Exceeds property value
        
#         with self.assertRaises(ValueError) as context:
#             validate_mortgage_data([invalid_mortgage])
        
#         self.assertIn("Loan amount cannot exceed property value", str(context.exception))

#     def test_credit_rating_edge_cases(self):
#         """Test credit rating calculation with edge case mortgage portfolios."""
#         # Scenario 1: All high-risk mortgages
#         high_risk_mortgages = [self.valid_mortgage_high_risk] * 3
#         rating = calculate_credit_rating(high_risk_mortgages)
#         self.assertEqual(rating, CreditRating.C)

#         # Scenario 2: Mixed risk mortgages
#         mixed_risk_mortgages = [
#             self.valid_mortgage_low_risk,
#             self.valid_mortgage_high_risk
#         ]
#         rating = calculate_credit_rating(mixed_risk_mortgages)
#         self.assertEqual(rating, CreditRating.BBB)

# if __name__ == '__main__':
#     unittest.main()















import unittest
import json
from credit_rating_mock import calculate_credit_rating, parse_mortgage_from_json

class TestCreditRating(unittest.TestCase):
    def test_high_credit_score_low_risk(self):
        mortgages = [
            {
                "credit_score": 800,
                "loan_amount": 100000,
                "property_value": 200000,
                "annual_income": 80000,
                "debt_amount": 10000,
                "loan_type": "fixed",
                "property_type": "single_family"
            }
        ]
        self.assertEqual(calculate_credit_rating(mortgages), "AAA")

    def test_medium_risk_scenario(self):
        mortgages = [
            {
                "credit_score": 680,
                "loan_amount": 150000,
                "property_value": 175000,
                "annual_income": 45000,
                "debt_amount": 20000,
                "loan_type": "adjustable",
                "property_type": "condo"
            }
        ]
        self.assertEqual(calculate_credit_rating(mortgages), "BBB")

    def test_high_risk_scenario(self):
        mortgages = [
            {
                "credit_score": 600,
                "loan_amount": 180000,
                "property_value": 190000,
                "annual_income": 35000,
                "debt_amount": 20000,
                "loan_type": "adjustable",
                "property_type": "condo"
            }
        ]
        self.assertEqual(calculate_credit_rating(mortgages), "C")

    def test_no_mortgages(self):
        self.assertEqual(calculate_credit_rating([]), "Invalid Data")

    def test_parse_mortgage_from_json_valid(self):
        """Test parsing valid JSON payload."""
        json_payload = json.dumps({
            "mortgages": [{
                "credit_score": 750,
                "loan_amount": 200000,
                "property_value": 250000,
                "annual_income": 60000,
                "debt_amount": 20000,
                "loan_type": 'fixed',
                "property_type": 'single_family'
            }]
        })
        mortgages = parse_mortgage_from_json(json_payload)
        self.assertEqual(len(mortgages), 1)
        self.assertEqual(mortgages[0]['credit_score'], 750)

    def test_parse_mortgage_from_json_invalid_format(self):
        """Test parsing invalid JSON format."""
        with self.assertRaises(ValueError):
            parse_mortgage_from_json("invalid json")


if __name__ == '__main__':
    unittest.main()
