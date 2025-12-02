"""
Example usage of CSV processor helper functions.
This file demonstrates how to use the process_standardized_csv function.
"""
import pandas as pd
from app.helpers.csv_processor import process_standardized_csv

# Example 1: Basic usage with DataFrame
def example_basic():
    # Create sample DataFrame
    df = pd.DataFrame({
        'old_customer_id': ['CUST-001', 'CUST-002', 'CUST-003'],
        'old_date': ['2024-01-15', '2024-01-16', '2024-01-17'],
        'price': [100.0, 200.0, 150.0],
        'unwanted_col': ['A', 'B', 'C']
    })
    
    # Define mapping
    mapping = [
        ('old_customer_id', 'rename', 'customer_id'),
        ('old_date', 'rename', 'event_date'),
        ('unwanted_col', 'drop', None),
        ('price', 'operate', ('multiply', 1.1))  # Increase prices by 10%
    ]
    
    # Process
    result = process_standardized_csv(df, mapping)
    print("Example 1 - Basic Usage:")
    print(result)
    print()


# Example 2: Using with file path
def example_with_file():
    # Assuming you have a CSV file
    mapping = [
        ('User ID', 'rename', 'customer_id'),
        ('Purchase Date', 'rename', 'event_date'),
        ('Amount', 'rename', 'amount'),
        ('Notes', 'drop', None),
        ('amount', 'operate', ('add', 5.0))  # Add $5 to each amount
    ]
    
    # result = process_standardized_csv('input.csv', mapping)
    # print(result)


# Example 3: Complex operations
def example_complex():
    df = pd.DataFrame({
        'customer_id': ['CUST-001', 'CUST-002'],
        'revenue': [1000.0, 2000.0],
        'discount': [0.1, 0.2],
        'temp_col': ['X', 'Y']
    })
    
    mapping = [
        ('revenue', 'operate', ('multiply', 0.9)),  # Apply 10% discount
        ('discount', 'operate', ('multiply', 100)),  # Convert to percentage
        ('temp_col', 'drop', None)
    ]
    
    result = process_standardized_csv(df, mapping)
    print("Example 3 - Complex Operations:")
    print(result)
    print()


# Example 4: All operations
def example_all_operations():
    df = pd.DataFrame({
        'old_id': ['1', '2', '3'],
        'old_date': ['2024-01-15', '2024-01-16', '2024-01-17'],
        'value': [10, 20, 30],
        'remove_me': ['A', 'B', 'C']
    })
    
    mapping = [
        ('old_id', 'rename', 'customer_id'),
        ('old_date', 'rename', 'event_date'),
        ('value', 'operate', ('add', 5)),      # Add 5
        ('value', 'operate', ('multiply', 2)), # Then multiply by 2
        ('remove_me', 'drop', None)
    ]
    
    result = process_standardized_csv(df, mapping)
    print("Example 4 - All Operations:")
    print(result)
    print()


if __name__ == "__main__":
    example_basic()
    example_complex()
    example_all_operations()

