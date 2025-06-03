"""
Exception handling tests for the Food Waste Reduction System.
"""

import unittest
import os
import importlib
import sys
import warnings
from test.TestUtils import TestUtils

# Configure warnings
warnings.filterwarnings("ignore")

class TestExceptional(unittest.TestCase):

    def check_file_exists(self, filename):
        """Check if a file exists in the current directory."""
        return os.path.exists(filename)

    def safely_import_module(self, module_name):
        """Safely import a module, returning None if import fails."""
        try:
            return importlib.import_module(module_name)
        except ImportError:
            return None

    def check_function_exists(self, module, function_name):
        """Check if a function exists in a module."""
        return hasattr(module, function_name) and callable(getattr(module, function_name))

    def safely_call_function(self, module, function_name, *args, **kwargs):
        """Safely call a function, returning None if it fails."""
        if not self.check_function_exists(module, function_name):
            return None
        try:
            return getattr(module, function_name)(*args, **kwargs)
        except Exception:
            return None

    def test_input_validation(self):
        """Test input validation and error handling"""
        test_obj = TestUtils()
        try:
            # Check if module can be imported
            module_obj = self.safely_import_module("skeleton")
            if module_obj is None:
                module_obj = self.safely_import_module("solution")
            
            if module_obj is None:
                test_obj.yakshaAssert("TestInputValidation", False, "exception")
                print("TestInputValidation = Failed")
                return
            
            # Test validate_food_item with None input
            result = self.safely_call_function(module_obj, "validate_food_item", None)
            if result is not None and isinstance(result, dict) and "is_valid" in result and result["is_valid"]:
                test_obj.yakshaAssert("TestInputValidation", False, "exception")
                print("TestInputValidation = Failed")
                return
            
            # Test validate_food_item with invalid item (missing required fields)
            invalid_item = {"id": "F001", "name": "Test Item"}
            result = self.safely_call_function(module_obj, "validate_food_item", invalid_item)
            if result is not None and isinstance(result, dict) and "is_valid" in result and result["is_valid"]:
                test_obj.yakshaAssert("TestInputValidation", False, "exception")
                print("TestInputValidation = Failed")
                return
            
            # Test calculate_days_until_expiration with invalid date format
            invalid_date = "12/15/2023"  # MM/DD/YYYY instead of YYYY-MM-DD
            days = self.safely_call_function(module_obj, "calculate_days_until_expiration", invalid_date)
            if days is not None and days >= 0:
                test_obj.yakshaAssert("TestInputValidation", False, "exception")
                print("TestInputValidation = Failed")
                return
            
            # Test identify_expiring_items with invalid threshold
            valid_items = [{"id": "F001", "expiration_date": "2023-12-15"}]
            expiring = self.safely_call_function(module_obj, "identify_expiring_items", valid_items, "not a number")
            if expiring is None:
                test_obj.yakshaAssert("TestInputValidation", False, "exception")
                print("TestInputValidation = Failed")
                return
            
            test_obj.yakshaAssert("TestInputValidation", True, "exception")
            print("TestInputValidation = Passed")
        
        except:
            test_obj.yakshaAssert("TestInputValidation", False, "exception")
            print("TestInputValidation = Failed")

    def test_error_handling(self):
        """Test specific error handling scenarios"""
        test_obj = TestUtils()
        try:
            # Check if module can be imported
            module_obj = self.safely_import_module("skeleton")
            if module_obj is None:
                module_obj = self.safely_import_module("solution")
            
            if module_obj is None:
                test_obj.yakshaAssert("TestErrorHandling", False, "exception")
                print("TestErrorHandling = Failed")
                return
            
            # Test with valid inputs to confirm proper functionality
            valid_items = [
                {"id": "F001", "name": "Test", "expiration_date": "2023-12-15", "category": "Produce"},
                {"id": "F002", "name": "Test2", "expiration_date": "2023-12-10", "category": "Dairy"}
            ]
            
            sorted_items = self.safely_call_function(module_obj, "sort_items_by_expiration", valid_items)
            if sorted_items is None or len(sorted_items) != 2 or sorted_items[0]["id"] != "F002":
                test_obj.yakshaAssert("TestErrorHandling", False, "exception")
                print("TestErrorHandling = Failed")
                return
            
            # Test with items that have no expiration_date field
            items_no_date = [
                {"id": "F001", "name": "Test"},
                {"id": "F002", "name": "Test2", "expiration_date": "2023-12-15"}
            ]
            
            expiring = self.safely_call_function(module_obj, "identify_expiring_items", items_no_date, 7)
            if expiring is None:
                test_obj.yakshaAssert("TestErrorHandling", False, "exception")
                print("TestErrorHandling = Failed")
                return
            
            # Test format_food_item with partial data
            partial_item = {"id": "F001", "name": "Test"}
            formatted = self.safely_call_function(module_obj, "format_food_item", partial_item)
            if formatted is None or not isinstance(formatted, str):
                test_obj.yakshaAssert("TestErrorHandling", False, "exception")
                print("TestErrorHandling = Failed")
                return
            
            test_obj.yakshaAssert("TestErrorHandling", True, "exception")
            print("TestErrorHandling = Passed")
        
        except:
            test_obj.yakshaAssert("TestErrorHandling", False, "exception")
            print("TestErrorHandling = Failed")

if __name__ == '__main__':
    unittest.main(verbosity=0, buffer=True)