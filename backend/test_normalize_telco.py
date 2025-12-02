"""
Simple test script to normalize Telco Churn dataset.
Run this to convert telco_churn.csv to standard schema format.
"""
import pandas as pd
from datetime import datetime, timedelta
import os

def normalize_telco_dataset(input_file: str = 'datasets/telco_churn.csv',
                            output_file: str = 'datasets/telco_churn_normalized.csv'):
    """
    Convert Telco Churn dataset to standard schema.
    
    Mapping:
    - customerID -> customer_id
    - tenure (months) -> used to calculate event_date (last transaction date)
    - MonthlyCharges -> amount
    - event_type -> 'monthly_charge'
    
    Args:
        input_file: Path to input CSV
        output_file: Path to save normalized CSV
    """
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file)
    
    print(f"Loaded {len(df)} customers")
    print(f"Columns: {df.columns.tolist()[:5]}...")  # Show first 5 columns
    
    # Base date (today)
    base_date = datetime.now().date()
    
    # Create transactions
    transactions = []
    
    for _, row in df.iterrows():
        customer_id = str(row['customerID'])
        tenure_months = int(row['tenure']) if pd.notna(row['tenure']) else 0
        monthly_charges = float(row['MonthlyCharges']) if pd.notna(row['MonthlyCharges']) else 0.0
        
        # Calculate last transaction date based on tenure
        # If tenure is 0, use base_date. Otherwise, go back by tenure months
        if tenure_months == 0:
            last_date = base_date
        else:
            # Approximate: tenure months ago (30 days per month)
            last_date = base_date - timedelta(days=30 * tenure_months)
        
        transactions.append({
            'customer_id': customer_id,
            'event_date': last_date.strftime('%Y-%m-%d'),
            'amount': monthly_charges,
            'event_type': 'monthly_charge'
        })
    
    # Create DataFrame
    normalized_df = pd.DataFrame(transactions)
    
    # Ensure proper column order
    normalized_df = normalized_df[['customer_id', 'event_date', 'amount', 'event_type']]
    
    # Save to CSV
    normalized_df.to_csv(output_file, index=False)
    
    print(f"\n[OK] Created {len(normalized_df)} transactions")
    print(f"[OK] Saved to {output_file}")
    print(f"\nSample output (first 5 rows):")
    print(normalized_df.head())
    print(f"\nDate range: {normalized_df['event_date'].min()} to {normalized_df['event_date'].max()}")
    print(f"Unique customers: {normalized_df['customer_id'].nunique()}")
    
    # Validate schema
    required_cols = ['customer_id', 'event_date']
    missing = [col for col in required_cols if col not in normalized_df.columns]
    if missing:
        print(f"\n[WARNING] Missing required columns: {missing}")
    else:
        print(f"\n[OK] Schema validation passed")
    
    return normalized_df


if __name__ == "__main__":
    # Check if input file exists
    input_file = 'datasets/telco_churn.csv'
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        print("Please ensure the file exists in the datasets/ directory")
        exit(1)
    
    # Normalize
    normalized_df = normalize_telco_dataset()
    
    print("\n" + "="*50)
    print("Normalization complete!")
    print("="*50)
    print(f"\nNext steps:")
    print(f"1. Review the normalized CSV: {normalized_df.shape[0]} rows")
    print(f"2. Upload via API: POST /api/v1/churn/organizations/{{org_id}}/upload-data")
    print(f"3. Train model: POST /api/v1/churn/organizations/{{org_id}}/train")

