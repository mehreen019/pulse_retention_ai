"""
CSV Processing Helper Functions
Modular functions for renaming, dropping, and operating on CSV columns.
"""
import pandas as pd
from typing import Union, List, Tuple, Any, Optional


def rename_column(df: pd.DataFrame, old_col_name: str, new_col_name: str) -> pd.DataFrame:
    """
    Rename a column in the DataFrame.
    
    Args:
        df: Input DataFrame
        old_col_name: Current column name
        new_col_name: New column name
        
    Returns:
        DataFrame with renamed column
        
    Raises:
        ValueError: If old_col_name doesn't exist
    """
    if old_col_name not in df.columns:
        raise ValueError(f"Column '{old_col_name}' not found in DataFrame")
    
    df = df.copy()  # Avoid modifying original
    df.rename(columns={old_col_name: new_col_name}, inplace=True)
    return df


def drop_column(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """
    Drop a column from the DataFrame.
    
    Args:
        df: Input DataFrame
        col_name: Column name to drop
        
    Returns:
        DataFrame with column dropped
        
    Raises:
        ValueError: If col_name doesn't exist
    """
    if col_name not in df.columns:
        raise ValueError(f"Column '{col_name}' not found in DataFrame")
    
    df = df.copy()  # Avoid modifying original
    df.drop(columns=[col_name], inplace=True)
    return df


def operate_column(
    df: pd.DataFrame,
    col_name: str,
    operation: str,
    value: Union[int, float]
) -> pd.DataFrame:
    """
    Apply mathematical operation to column values.
    
    Args:
        df: Input DataFrame
        col_name: Column name to operate on
        operation: Operation type ('add', 'subtract', 'multiply', 'divide')
        value: Value to use in operation
        
    Returns:
        DataFrame with modified column values
        
    Raises:
        ValueError: If col_name doesn't exist or operation is invalid
    """
    if col_name not in df.columns:
        raise ValueError(f"Column '{col_name}' not found in DataFrame")
    
    valid_operations = ['add', 'subtract', 'multiply', 'divide']
    if operation not in valid_operations:
        raise ValueError(f"Invalid operation '{operation}'. Must be one of: {valid_operations}")
    
    df = df.copy()  # Avoid modifying original
    
    # Convert column to numeric if possible
    df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
    
    # Apply operation
    if operation == 'add':
        df[col_name] = df[col_name] + value
    elif operation == 'subtract':
        df[col_name] = df[col_name] - value
    elif operation == 'multiply':
        df[col_name] = df[col_name] * value
    elif operation == 'divide':
        if value == 0:
            raise ValueError("Cannot divide by zero")
        df[col_name] = df[col_name] / value
    
    return df


def process_standardized_csv(
    input_csv: Union[pd.DataFrame, str],
    mapping: List[Tuple[str, str, Any]]
) -> pd.DataFrame:
    """
    Process CSV according to mapping specifications.
    
    Args:
        input_csv: Input CSV as DataFrame or file path (str)
        mapping: List of tuples with format (column_name, operation, operation_args)
                 - For 'rename': (old_col_name, 'rename', new_col_name)
                 - For 'drop': (col_name, 'drop', None)
                 - For 'operate': (col_name, 'operate', (operation_type, value))
                                 where operation_type is 'add', 'subtract', 'multiply', or 'divide'
    
    Returns:
        Processed DataFrame
        
    Example:
        mapping = [
            ('old_name', 'rename', 'new_name'),
            ('unwanted_col', 'drop', None),
            ('amount', 'operate', ('multiply', 1.1)),  # Increase by 10%
            ('price', 'operate', ('add', 5.0))  # Add 5 to each value
        ]
    """
    # Load CSV if string path provided
    if isinstance(input_csv, str):
        df = pd.read_csv(input_csv)
    elif isinstance(input_csv, pd.DataFrame):
        df = input_csv.copy()
    else:
        raise TypeError("input_csv must be a pandas DataFrame or file path string")
    
    # Process each mapping instruction
    for instruction in mapping:
        if len(instruction) < 2:
            raise ValueError(f"Invalid mapping instruction: {instruction}. Must have at least (column_name, operation)")
        
        column_name = instruction[0]
        operation = instruction[1].lower()
        operation_args = instruction[2] if len(instruction) > 2 else None
        
        if operation == 'rename':
            if operation_args is None:
                raise ValueError(f"Rename operation requires new column name as third argument")
            new_col_name = operation_args
            df = rename_column(df, column_name, new_col_name)
            
        elif operation == 'drop':
            df = drop_column(df, column_name)
            
        elif operation == 'operate':
            if operation_args is None:
                raise ValueError(f"Operate operation requires (operation_type, value) tuple as third argument")
            
            # operation_args should be a tuple: (operation_type, value)
            if not isinstance(operation_args, (tuple, list)) or len(operation_args) != 2:
                raise ValueError(f"Operate operation args must be tuple/list of (operation_type, value)")
            
            operation_type, value = operation_args
            df = operate_column(df, column_name, operation_type, value)
            
        else:
            raise ValueError(f"Unknown operation: '{operation}'. Must be 'rename', 'drop', or 'operate'")
    
    return df

