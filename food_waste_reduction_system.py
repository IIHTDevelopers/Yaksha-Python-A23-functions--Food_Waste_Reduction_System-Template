"""
Food Waste Reduction System

This module provides functions for tracking food inventory, monitoring expiration dates,
and identifying donation opportunities.

Version: 1.0
"""

import datetime
from typing import Dict, List


def validate_food_item(food_item: Dict) -> Dict:
    """
    Validates if the food item data contains all required fields and correct data types.
    
    Parameters:
    food_item (dict): Dictionary containing food item information
    
    Returns:
    dict: Validation result with format {"is_valid": bool, "message": str}
    
    Example:
    >>> validate_food_item({"id": "F001", "name": "Apples", "category": "Produce", 
                           "quantity": 25, "unit": "kg", "expiration_date": "2023-12-15", 
                           "storage_location": "Cooler 3"})
    {'is_valid': True, 'message': 'Food item data is valid'}
    """
    # Check if food_item is None or not a dictionary
    if food_item is None or not isinstance(food_item, dict):
        return {"is_valid": False, "message": "Food item must be a dictionary"}
        
    required_fields = ["id", "name", "category", "quantity", "unit", "expiration_date", "storage_location"]
    validation_result = {"is_valid": True, "message": "Food item data is valid"}
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in food_item:
            validation_result["is_valid"] = False
            validation_result["message"] = f"Missing required field: {field}"
            return validation_result
    
    # Validate data types
    if not isinstance(food_item["id"], str):
        validation_result["is_valid"] = False
        validation_result["message"] = "ID must be a string"
        return validation_result
        
    if not isinstance(food_item["name"], str):
        validation_result["is_valid"] = False
        validation_result["message"] = "Name must be a string"
        return validation_result
        
    if not isinstance(food_item["quantity"], (int, float)) or food_item["quantity"] < 0:
        validation_result["is_valid"] = False
        validation_result["message"] = "Quantity must be a positive number"
        return validation_result
    
    # Validate category
    valid_categories = ["Produce", "Dairy", "Bakery", "Meat", "Frozen", 
                        "Canned", "Dry Goods", "Prepared"]
    
    if not isinstance(food_item["category"], str):
        validation_result["is_valid"] = False
        validation_result["message"] = "Category must be a string"
        return validation_result
        
    if food_item["category"] not in valid_categories:
        validation_result["is_valid"] = False
        validation_result["message"] = f"Invalid category. Must be one of: {', '.join(valid_categories)}"
        return validation_result
    
    return validation_result


def calculate_days_until_expiration(expiration_date: str) -> int:
    """
    Calculates the number of days until the given expiration date.
    
    Parameters:
    expiration_date (str): Expiration date in YYYY-MM-DD format
    
    Returns:
    int: Number of days until expiration
    
    Example:
    >>> calculate_days_until_expiration("2023-12-15")  # Assuming today is 2023-12-10
    5
    """
    # Check if expiration_date is None
    if expiration_date is None:
        return -1
        
    try:
        # Parse the expiration date
        expiration_date_obj = datetime.datetime.strptime(expiration_date, "%Y-%m-%d").date()
        
        # Calculate days until expiration
        current_date = datetime.date.today()
        days_until_expiration = (expiration_date_obj - current_date).days
        
        return days_until_expiration
    except ValueError:
        # Return a negative value to indicate invalid date
        return -1


def identify_expiring_items(food_items: List[Dict], days_threshold: int = 7) -> List[Dict]:
    """
    Identifies food items that will expire within the given threshold of days.
    
    Parameters:
    food_items (list): List of dictionaries containing food item information
    days_threshold (int): Number of days threshold for identifying expiring items
    
    Returns:
    list: List of food items that will expire within the threshold
    
    Example:
    >>> food_items = [{"id": "F001", "name": "Apples", "expiration_date": "2023-12-15"}]
    >>> identify_expiring_items(food_items, 7)  # Assuming today is 2023-12-10
    [{"id": "F001", "name": "Apples", "expiration_date": "2023-12-15"}]
    """
    # Check if food_items is None or not a list
    if food_items is None or not isinstance(food_items, list):
        return []
        
    # Check if days_threshold is None or not an int
    if days_threshold is None or not isinstance(days_threshold, int):
        days_threshold = 7  # Default value
        
    # Identify expiring items
    expiring_items = []
    for item in food_items:
        if not isinstance(item, dict) or "expiration_date" not in item:
            continue
            
        days = calculate_days_until_expiration(item["expiration_date"])
        if 0 <= days <= days_threshold:
            expiring_items.append(item)
    
    return expiring_items


def sort_items_by_expiration(food_items: List[Dict]) -> List[Dict]:
    """
    Sorts food items by expiration date (soonest first).
    
    Parameters:
    food_items (list): List of dictionaries containing food item information
    
    Returns:
    list: Sorted list of food items
    
    Example:
    >>> food_items = [
    ...     {"id": "F001", "name": "Apples", "expiration_date": "2023-12-15"},
    ...     {"id": "F002", "name": "Milk", "expiration_date": "2023-12-10"}
    ... ]
    >>> sort_items_by_expiration(food_items)
    [{"id": "F002", "name": "Milk", "expiration_date": "2023-12-10"}, 
     {"id": "F001", "name": "Apples", "expiration_date": "2023-12-15"}]
    """
    # Check if food_items is None or not a list
    if food_items is None or not isinstance(food_items, list):
        return []
        
    # Create a copy to avoid modifying the original
    sorted_items = food_items.copy()
    
    # Sort by expiration date
    return sorted(sorted_items, key=lambda x: x.get("expiration_date", "9999-12-31") if isinstance(x, dict) else "9999-12-31")


def match_donations(food_items: List[Dict], recipients: List[Dict]) -> List[Dict]:
    """
    Matches food items with suitable donation recipients.
    
    Parameters:
    food_items (list): List of dictionaries containing food item information
    recipients (list): List of dictionaries containing recipient information
    
    Returns:
    list: List of matching pairs with format [{"item": item_dict, "recipient": recipient_dict}]
    
    Example:
    >>> items = [{"id": "F001", "category": "Produce", "name": "Apples"}]
    >>> recipients = [{"id": "R001", "name": "Food Bank", "accepts_categories": ["Produce"]}]
    >>> match_donations(items, recipients)
    [{"item": {"id": "F001", "category": "Produce", "name": "Apples"}, 
      "recipient": {"id": "R001", "name": "Food Bank", "accepts_categories": ["Produce"]}}]
    """
    # Check if food_items or recipients is None or not a list
    if food_items is None or not isinstance(food_items, list) or recipients is None or not isinstance(recipients, list):
        return []
        
    matches = []
    
    for item in food_items:
        if not isinstance(item, dict) or "category" not in item:
            continue
            
        item_category = item["category"]
        
        for recipient in recipients:
            if not isinstance(recipient, dict) or "accepts_categories" not in recipient:
                continue
                
            accepted_categories = recipient["accepts_categories"]
            
            if item_category in accepted_categories:
                matches.append({
                    "item": item,
                    "recipient": recipient
                })
                break  # Match with first suitable recipient
    
    return matches


def format_food_item(food_item: Dict) -> str:
    """
    Formats a food item for display.
    
    Parameters:
    food_item (dict): Dictionary containing food item information
    
    Returns:
    str: Formatted string representation of the food item
    
    Example:
    >>> item = {"id": "F001", "name": "Apples", "quantity": 25, "unit": "kg", 
    ...         "expiration_date": "2023-12-15", "category": "Produce"}
    >>> format_food_item(item)
    "F001 | Apples | 25 kg | Produce | Expires: 2023-12-15"
    """
    # Check if food_item is None or not a dictionary
    if food_item is None or not isinstance(food_item, dict):
        return "Invalid food item format"
        
    try:
        return (f"{food_item['id']} | {food_item['name']} | "
                f"{food_item['quantity']} {food_item['unit']} | "
                f"{food_item['category']} | "
                f"Expires: {food_item['expiration_date']}")
    except KeyError:
        return "Invalid food item format"


def main():
    """
    Main function that demonstrates the food waste reduction system.
    """
    print("===== FOOD WASTE REDUCTION SYSTEM =====")
    
    # Initialize sample data
    inventory = [
        {
            "id": "F001",
            "name": "Apples",
            "category": "Produce",
            "quantity": 25,
            "unit": "kg",
            "expiration_date": "2023-12-15",
            "storage_location": "Cooler 3"
        },
        {
            "id": "F002",
            "name": "Milk",
            "category": "Dairy",
            "quantity": 15,
            "unit": "liter",
            "expiration_date": "2023-12-10",
            "storage_location": "Refrigerator 1"
        },
        {
            "id": "F003",
            "name": "Bread",
            "category": "Bakery",
            "quantity": 8,
            "unit": "loaf",
            "expiration_date": "2023-12-08",
            "storage_location": "Shelf 2"
        }
    ]
    
    recipients = [
        {
            "id": "R001",
            "name": "City Food Bank",
            "accepts_categories": ["Produce", "Canned", "Bakery"]
        },
        {
            "id": "R002",
            "name": "Community Shelter",
            "accepts_categories": ["Dairy", "Bakery", "Prepared"]
        }
    ]
    
    # Demonstrate validation function
    print("\n1. Validating Food Items:")
    for item in inventory:
        result = validate_food_item(item)
        print(f"  {item['name']}: {result['message']}")
    
    # Demonstrate expiration calculation function
    print("\n2. Days Until Expiration:")
    for item in inventory:
        days = calculate_days_until_expiration(item["expiration_date"])
        print(f"  {item['name']}: {days} days")
    
    # Demonstrate identifying expiring items function
    print("\n3. Identifying Expiring Items (within 7 days):")
    expiring = identify_expiring_items(inventory)
    for item in expiring:
        print(f"  {item['name']} - Expires soon")
    
    # Demonstrate sorting function
    print("\n4. Sorting Items by Expiration Date:")
    sorted_items = sort_items_by_expiration(inventory)
    for item in sorted_items:
        print(f"  {item['name']} - {item['expiration_date']}")
    
    # Demonstrate donation matching function
    print("\n5. Finding Donation Matches:")
    matches = match_donations(inventory, recipients)
    for match in matches:
        print(f"  {match['item']['name']} → {match['recipient']['name']}")
    
    # Demonstrate formatting function
    print("\n6. Formatted Food Items:")
    for item in inventory:
        print(f"  {format_food_item(item)}")


if __name__ == "__main__":
    main()