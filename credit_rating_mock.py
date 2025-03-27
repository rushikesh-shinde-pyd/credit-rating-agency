import json
from enum import Enum
from typing import List, Dict, Union

class LoanType(Enum):
    FIXED = "fixed"
    ADJUSTABLE = "adjustable"

class PropertyType(Enum):
    SINGLE_FAMILY = "single_family"
    CONDO = "condo"

class CreditRating(Enum):
    AAA = "AAA"
    BBB = "BBB"
    C = "C"

def calculate_mortgage_risk_score(mortgage: Dict[str, Union[int, float, str]]) -> int:
    """
    Calculate the risk score for an individual mortgage.
    
    Args:
        mortgage (Dict): A dictionary containing mortgage details
    
    Returns:
        int: Risk score for the mortgage
    """
    risk_score = 0
    
    # 1. Loan-to-Value (LTV) Ratio Calculation
    ltv = mortgage['loan_amount'] / mortgage['property_value'] * 100
    if ltv > 90:
        risk_score += 2
    elif ltv > 80:
        risk_score += 1
    
    # 2. Debt-to-Income (DTI) Ratio Calculation
    dti = mortgage['debt_amount'] / mortgage['annual_income'] * 100
    if dti > 50:
        risk_score += 2
    elif dti > 40:
        risk_score += 1
    
    # 3. Credit Score Assessment
    credit_score = mortgage['credit_score']
    if credit_score >= 700:
        risk_score -= 1
    elif credit_score < 650:
        risk_score += 1
    
    # 4. Loan Type Risk
    if mortgage['loan_type'] == LoanType.ADJUSTABLE:
        risk_score += 1
    elif mortgage['loan_type'] == LoanType.FIXED:
        risk_score -= 1
    
    # 5. Property Type Risk
    if mortgage['property_type'] == PropertyType.CONDO:
        risk_score += 1
    
    return risk_score

def calculate_credit_rating(mortgages: List[Dict[str, Union[int, float, str]]]) -> CreditRating:
    """
    Calculate the overall credit rating for a residential mortgage-backed security.
    
    Args:
        mortgages (List[Dict]): A list of mortgage dictionaries
    
    Returns:
        CreditRating: Credit rating enum
    """
    # Validate input
    if not mortgages or not isinstance(mortgages, list):
        raise ValueError("Invalid input: mortgages must be a non-empty list")
    
    # Calculate individual mortgage risk scores
    mortgage_risk_scores = [calculate_mortgage_risk_score(mortgage) for mortgage in mortgages]
    
    # Calculate total risk score
    total_risk_score = sum(mortgage_risk_scores)
    
    # Calculate average credit score for potential final adjustment
    avg_credit_score = sum(mortgage['credit_score'] for mortgage in mortgages) / len(mortgages)
    
    # Final score adjustment based on average credit score
    if avg_credit_score >= 700:
        total_risk_score -= 1
    elif avg_credit_score < 650:
        total_risk_score += 1
    
    # Determine credit rating
    if total_risk_score <= 2:
        return CreditRating.AAA
    elif 3 <= total_risk_score <= 5:
        return CreditRating.BBB
    else:
        return CreditRating.C

def parse_mortgage_from_json(json_payload: str) -> List[Dict[str, Union[int, float, str]]]:
    """
    Parse mortgage data from a JSON payload.
    
    Args:
        json_payload (str): JSON string containing mortgage data
    
    Returns:
        List[Dict]: List of mortgage dictionaries
    """
    try:
        # Parse the JSON payload
        payload = json.loads(json_payload)
        
        # Validate the payload structure
        if not isinstance(payload, dict) or 'mortgages' not in payload:
            raise ValueError("Invalid JSON payload: Must contain 'mortgages' key")
        
        mortgages = payload['mortgages']
        
        # Validate mortgages is a list
        if not isinstance(mortgages, list):
            raise ValueError("'mortgages' must be a list")

        return mortgages
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format")
    except ValueError as e:
        raise ValueError(f"Payload validation error: {str(e)}")


def validate_mortgage_data(mortgages: List[Dict[str, Union[int, float, str]]]) -> List[Dict[str, Union[int, float, str]]]:
    """
    Validate a list of mortgage dictionaries.
    
    Args:
        mortgages (List[Dict]): A list of mortgage dictionaries to validate
    
    Returns:
        List[Dict]: Validated mortgage dictionaries
    
    Raises:
        ValueError: If the mortgage data is invalid
    """
    # Check if input is a list and not empty
    if not isinstance(mortgages, list) or len(mortgages) == 0:
        raise ValueError("Input must be a non-empty list of mortgages")
    
    # Validate each mortgage
    validated_mortgages = []
    errors = []
    
    for idx, mortgage in enumerate(mortgages):
        mortgage_errors = []
        
        # 1. Check for required keys
        required_keys = [
            "credit_score", 
            "loan_amount", 
            "property_value", 
            "annual_income", 
            "debt_amount", 
            "loan_type", 
            "property_type"
        ]
        
        # Check for missing keys
        missing_keys = [key for key in required_keys if key not in mortgage]
        if missing_keys:
            mortgage_errors.append(f"Mortgage {idx}: Missing required keys: {', '.join(missing_keys)}")
        
        # 2. Validate specific fields if present
        if "credit_score" in mortgage:
            if not isinstance(mortgage['credit_score'], int):
                mortgage_errors.append(f"Mortgage {idx}: Credit score must be an integer")
            elif not (300 <= mortgage['credit_score'] <= 850):
                mortgage_errors.append(f"Mortgage {idx}: Credit score must be between 300 and 850")
        
        # Numeric validations
        numeric_validations = [
            ("loan_amount", lambda x: x > 0, "Loan amount must be positive"),
            ("property_value", lambda x: x > 0, "Property value must be positive"),
            ("annual_income", lambda x: x > 0, "Annual income must be positive"),
            ("debt_amount", lambda x: x >= 0, "Debt amount must be non-negative")
        ]
        
        for key, validator, error_msg in numeric_validations:
            if key in mortgage:
                if not isinstance(mortgage[key], (int, float)):
                    mortgage_errors.append(f"Mortgage {idx}: {key} must be a number")
                elif not validator(mortgage[key]):
                    mortgage_errors.append(f"Mortgage {idx}: {error_msg}")
        
        # 3. Validate loan type
        if "loan_type" in mortgage:
            try:
                mortgage['loan_type'] = LoanType(mortgage['loan_type'])
            except ValueError:
                mortgage_errors.append(f"Mortgage {idx}: Invalid loan type. Must be 'fixed' or 'adjustable'")
        
        # 4. Validate property type
        if "property_type" in mortgage:
            try:
                mortgage['property_type'] = PropertyType(mortgage['property_type'])
            except ValueError:
                mortgage_errors.append(f"Mortgage {idx}: Invalid property type. Must be 'single_family' or 'condo'")
        
        # 5. Additional business logic validations
        if "loan_amount" in mortgage and "property_value" in mortgage:
            ltv = mortgage['loan_amount'] / mortgage['property_value'] * 100
            if ltv > 100:
                mortgage_errors.append(f"Mortgage {idx}: Loan amount cannot exceed property value")
        
        if "debt_amount" in mortgage and "annual_income" in mortgage:
            dti = mortgage['debt_amount'] / mortgage['annual_income'] * 100
            if dti > 70:  # Typical maximum DTI threshold
                mortgage_errors.append(f"Mortgage {idx}: Debt-to-income ratio too high")
        
        # Collect errors
        if mortgage_errors:
            errors.extend(mortgage_errors)
        else:
            validated_mortgages.append(mortgage)
    
    # Raise comprehensive error if any issues found
    if errors:
        raise ValueError("Mortgage Validation Failed:\n" + "\n".join(errors))
    
    return validated_mortgages

def main():
    # Valid mortgages
    json_payload = json.dumps({
        "mortgages": [
            {
                "credit_score": 750,
                "loan_amount": 200000,
                "property_value": 250000,
                "annual_income": 60000,
                "debt_amount": 20000,
                "loan_type": "fixed",
                "property_type": "single_family"
            },
            {
                "credit_score": 680,
                "loan_amount": 150000,
                "property_value": 175000,
                "annual_income": 45000,
                "debt_amount": 10000,
                "loan_type": "adjustable",
                "property_type": "condo"
            }
        ]
    })

    # # Invalid mortgages
    # json_payload = json.dumps({
    #     "mortgages": [
    #         {
    #             "credit_score": 250,  # Invalid credit score
    #             "loan_amount": -10000,  # Negative loan amount
    #             "property_value": 100000,
    #             "annual_income": 30000,
    #             "debt_amount": 20000,
    #             "loan_type": "variable",  # Invalid loan type
    #             "property_type": "townhouse"  # Invalid property type
    #         }
    #     ]
    # })
    
    try:
        mortgages = parse_mortgage_from_json(json_payload)

        validate_mortgage_data(mortgages)
    except ValueError as e:
        print(f"Validation Error: {e}")
    else:
        rating = calculate_credit_rating(mortgages)
        print(f"Credit Rating: {rating.value}")

if __name__ == "__main__":
    main()