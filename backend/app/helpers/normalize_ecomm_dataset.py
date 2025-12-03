"""
Helper script to normalize eCommerce Churn dataset to standard schema.
Converts customer snapshot data to transaction-based format.
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def normalize_ecomm_to_standard_schema(
    input_file: str,
    output_file: str,
    base_date: Optional[str] = None
) -> pd.DataFrame:
    """
    Convert eCommerce Churn dataset to standard schema format.

    Strategy:
    - Create transaction events based on OrderCount and DaySinceLastOrder
    - Use CashbackAmount as transaction amount
    - Distribute orders over tenure period

    Args:
        input_file: Path to eComm.csv
        output_file: Path to save normalized CSV
        base_date: Base date for transactions (defaults to today)

    Returns:
        Normalized DataFrame
    """
    # Read input CSV
    df = pd.read_csv(input_file)

    print(f"Loaded {len(df)} customers from {input_file}")
    print(f"Columns: {df.columns.tolist()}")

    # Set base date (default to today)
    if base_date is None:
        base_date = datetime.now().date()
    else:
        base_date = datetime.strptime(base_date, "%Y-%m-%d").date()

    # Clean data
    df['Tenure'] = pd.to_numeric(df['Tenure'], errors='coerce').fillna(0).astype(int)
    df['OrderCount'] = pd.to_numeric(df['OrderCount'], errors='coerce').fillna(0).astype(int)
    df['DaySinceLastOrder'] = pd.to_numeric(df['DaySinceLastOrder'], errors='coerce').fillna(0).astype(int)
    df['CashbackAmount'] = pd.to_numeric(df['CashbackAmount'], errors='coerce').fillna(0).astype(float)
    df['Churn'] = pd.to_numeric(df['Churn'], errors='coerce').fillna(0).astype(int)

    # Create transaction events
    transactions = []

    for _, row in df.iterrows():
        customer_id = str(row['CustomerID'])
        tenure_months = int(row['Tenure'])
        order_count = int(row['OrderCount'])
        days_since_last = int(row['DaySinceLastOrder'])
        cashback = float(row['CashbackAmount'])
        churn_label = int(row['Churn'])

        # Calculate last order date
        last_order_date = base_date - timedelta(days=days_since_last)

        # If customer has no orders, create one snapshot transaction
        if order_count == 0:
            transactions.append({
                'customer_id': customer_id,
                'event_date': last_order_date.strftime('%Y-%m-%d'),
                'amount': cashback,
                'event_type': 'order',
                'churn_label': churn_label
            })
            continue

        # Create transactions for each order
        # Distribute orders over tenure period
        if tenure_months > 0:
            # Calculate approximate days between orders
            tenure_days = tenure_months * 30
            if order_count > 1:
                days_between = tenure_days / (order_count - 1) if order_count > 1 else tenure_days
            else:
                days_between = tenure_days

            # Create order transactions going backwards from last order date
            for i in range(order_count):
                # Calculate transaction date (going backwards)
                days_back = days_between * (order_count - i - 1)
                transaction_date = last_order_date - timedelta(days=days_back)

                # Ensure transaction is not in the future
                if transaction_date > base_date:
                    transaction_date = base_date

                # Distribute cashback amount across orders
                amount = cashback / order_count if order_count > 0 else cashback

                transactions.append({
                    'customer_id': customer_id,
                    'event_date': transaction_date.strftime('%Y-%m-%d'),
                    'amount': round(amount, 2),
                    'event_type': 'order',
                    'churn_label': churn_label
                })
        else:
            # If tenure is 0, create orders around last order date
            for i in range(order_count):
                # Space orders 7 days apart going backwards
                transaction_date = last_order_date - timedelta(days=7 * i)

                # Distribute cashback amount across orders
                amount = cashback / order_count if order_count > 0 else cashback

                transactions.append({
                    'customer_id': customer_id,
                    'event_date': transaction_date.strftime('%Y-%m-%d'),
                    'amount': round(amount, 2),
                    'event_type': 'order',
                    'churn_label': churn_label
                })

    # Create normalized DataFrame
    normalized_df = pd.DataFrame(transactions)

    # Ensure proper column order
    normalized_df = normalized_df[['customer_id', 'event_date', 'amount', 'event_type', 'churn_label']]

    # Sort by customer_id and event_date
    normalized_df = normalized_df.sort_values(['customer_id', 'event_date']).reset_index(drop=True)

    # Save to CSV
    normalized_df.to_csv(output_file, index=False)

    print(f"\nNormalized {len(normalized_df)} transactions from {len(df)} customers")
    print(f"Saved to {output_file}")
    print(f"\nSample output:")
    print(normalized_df.head(10))
    print(f"\nDate range: {normalized_df['event_date'].min()} to {normalized_df['event_date'].max()}")

    # Print churn statistics
    unique_customers = normalized_df[['customer_id', 'churn_label']].drop_duplicates()
    churn_rate = unique_customers['churn_label'].mean()
    print(f"\nChurn Statistics:")
    print(f"Total customers: {len(unique_customers)}")
    print(f"Churned customers: {unique_customers['churn_label'].sum()}")
    print(f"Churn rate: {churn_rate:.2%}")

    return normalized_df


def normalize_ecomm_simple(
    input_file: str,
    output_file: str
) -> pd.DataFrame:
    """
    Simple normalization: Creates one transaction per customer using last order date.

    Args:
        input_file: Path to eComm.csv
        output_file: Path to save normalized CSV

    Returns:
        Normalized DataFrame
    """
    # Read input CSV
    df = pd.read_csv(input_file)

    print(f"Loaded {len(df)} customers from {input_file}")

    # Base date (today)
    base_date = datetime.now().date()

    # Clean data
    df['Tenure'] = pd.to_numeric(df['Tenure'], errors='coerce').fillna(0).astype(int)
    df['DaySinceLastOrder'] = pd.to_numeric(df['DaySinceLastOrder'], errors='coerce').fillna(0).astype(int)
    df['CashbackAmount'] = pd.to_numeric(df['CashbackAmount'], errors='coerce').fillna(0).astype(float)
    df['Churn'] = pd.to_numeric(df['Churn'], errors='coerce').fillna(0).astype(int)

    transactions = []

    for _, row in df.iterrows():
        customer_id = str(row['CustomerID'])
        days_since_last = int(row['DaySinceLastOrder'])
        cashback = float(row['CashbackAmount'])
        churn_label = int(row['Churn'])

        # Calculate last order date
        last_order_date = base_date - timedelta(days=days_since_last)

        transactions.append({
            'customer_id': customer_id,
            'event_date': last_order_date.strftime('%Y-%m-%d'),
            'amount': cashback,
            'event_type': 'order',
            'churn_label': churn_label
        })

    # Create DataFrame
    normalized_df = pd.DataFrame(transactions)

    # Save to CSV
    normalized_df.to_csv(output_file, index=False)

    print(f"\nCreated {len(normalized_df)} transactions from {len(df)} customers")
    print(f"Saved to {output_file}")
    print(f"\nSample output:")
    print(normalized_df.head(10))
    print(f"\nDate range: {normalized_df['event_date'].min()} to {normalized_df['event_date'].max()}")

    # Print churn statistics
    churn_rate = normalized_df['churn_label'].mean()
    print(f"\nChurn Statistics:")
    print(f"Total customers: {len(normalized_df)}")
    print(f"Churned customers: {normalized_df['churn_label'].sum()}")
    print(f"Churn rate: {churn_rate:.2%}")

    return normalized_df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Normalize eCommerce Churn dataset to standard schema')
    parser.add_argument('--input', type=str, default='datasets/eComm.csv',
                        help='Input CSV file path')
    parser.add_argument('--output', type=str, default='datasets/ecomm_normalized.csv',
                        help='Output CSV file path')
    parser.add_argument('--mode', type=str, choices=['simple', 'detailed'], default='simple',
                        help='Normalization mode: simple (one transaction per customer) or detailed (multiple transactions)')
    parser.add_argument('--base-date', type=str, default=None,
                        help='Base date for transactions (YYYY-MM-DD). Defaults to today.')

    args = parser.parse_args()

    if args.mode == 'simple':
        normalize_ecomm_simple(args.input, args.output)
    else:
        normalize_ecomm_to_standard_schema(
            args.input,
            args.output,
            base_date=args.base_date
        )
