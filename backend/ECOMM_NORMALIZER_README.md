# eCommerce Dataset Normalizer

## Overview

Converts the eCommerce customer churn dataset into our standard transaction schema for training churn prediction models.

---

## Input Dataset

**File:** `datasets/eComm.csv`

### Columns:
- `CustomerID` - Unique customer identifier
- `Churn` - Churn status (0 = active, 1 = churned)
- `Tenure` - Months as customer
- `OrderCount` - Total number of orders
- `DaySinceLastOrder` - Days since last order
- `CashbackAmount` - Total cashback earned
- Plus 14 other demographic/behavioral columns

### Sample Data:
```csv
CustomerID,Churn,Tenure,OrderCount,DaySinceLastOrder,CashbackAmount,...
50001,1,4,1,5,160,...
50002,1,,1,0,121,...
```

**Statistics:**
- Total customers: 5,630
- Churned: 948 (16.84%)
- Active: 4,682 (83.16%)

---

## Output Format

Converts to standard schema:

```csv
customer_id,event_date,amount,event_type,churn_label
50001,2025-11-27,160.0,order,1
50002,2025-12-02,121.0,order,1
```

**Columns:**
- `customer_id` - Customer ID
- `event_date` - Order date (YYYY-MM-DD)
- `amount` - Transaction amount (cashback distributed)
- `event_type` - Always "order"
- `churn_label` - Churn status (0 or 1)

---

## Usage

### Simple Mode (One Transaction Per Customer)

Creates one transaction per customer using last order date.

```bash
cd backend
python -m app.helpers.normalize_ecomm_dataset \
  --input datasets/eComm.csv \
  --output datasets/ecomm_normalized.csv \
  --mode simple
```

**Output:**
- 5,630 transactions (1 per customer)
- Uses `DaySinceLastOrder` to calculate order date
- Amount = full `CashbackAmount`

### Detailed Mode (Multiple Transactions Per Customer)

Creates multiple transactions per customer based on `OrderCount`.

```bash
cd backend
python -m app.helpers.normalize_ecomm_dataset \
  --input datasets/eComm.csv \
  --output datasets/ecomm_normalized_detailed.csv \
  --mode detailed
```

**Output:**
- 16,417 transactions (avg 2.9 per customer)
- Distributes orders over tenure period
- Amount = `CashbackAmount` / `OrderCount`

---

## Normalization Logic

### Date Calculation

```
Last Order Date = Today - DaySinceLastOrder
```

For detailed mode with multiple orders:
```
Days Between Orders = (Tenure * 30) / (OrderCount - 1)
Order Dates = Evenly distributed going backwards from last order
```

### Amount Calculation

**Simple Mode:**
```
Amount = CashbackAmount
```

**Detailed Mode:**
```
Amount per Order = CashbackAmount / OrderCount
```

### Churn Label

Directly uses the `Churn` column (0 or 1) from source data.

---

## Examples

### Example 1: Customer with 6 Orders

**Input:**
```csv
CustomerID: 50006
Churn: 1
Tenure: 4 months
OrderCount: 6
DaySinceLastOrder: 7 days
CashbackAmount: 139.0
```

**Output (Detailed Mode):**
```csv
customer_id,event_date,amount,event_type,churn_label
50006,2025-10-21,23.17,order,1
50006,2025-10-28,23.17,order,1
50006,2025-11-04,23.17,order,1
50006,2025-11-11,23.17,order,1
50006,2025-11-18,23.17,order,1
50006,2025-11-25,23.17,order,1
```

Orders spaced 7 days apart, amount split equally (139 / 6 = 23.17)

### Example 2: Customer with 1 Order

**Input:**
```csv
CustomerID: 50001
Churn: 1
Tenure: 4 months
OrderCount: 1
DaySinceLastOrder: 5 days
CashbackAmount: 160.0
```

**Output:**
```csv
customer_id,event_date,amount,event_type,churn_label
50001,2025-11-27,160.0,order,1
```

Single order 5 days ago with full cashback amount.

---

## Statistics

### Simple Mode Output
- **Total Transactions:** 5,630
- **Date Range:** 2025-10-17 to 2025-12-02 (46 days)
- **Churn Rate:** 16.84%

### Detailed Mode Output
- **Total Transactions:** 16,417
- **Transactions per Customer:**
  - Mean: 2.92
  - Median: 2
  - Max: 16
- **Date Range:** 2020-11-27 to 2025-12-02 (5+ years)
- **Churn Rate:** 16.84%

---

## Use Cases

### 1. Train Churn Model for eCommerce
```bash
# Normalize dataset
python -m app.helpers.normalize_ecomm_dataset --mode detailed

# Upload to API
curl -X POST ".../upload-dataset" -F "file=@datasets/ecomm_normalized_detailed.csv" -F "has_churn_label=true"

# Process features
curl -X POST ".../process-features"

# Train model
curl -X POST ".../train"
```

### 2. Compare with Telco Model
Train separate models for different industries:
- Telco dataset → Organization 1
- eCommerce dataset → Organization 2

Compare feature importance and metrics.

### 3. Multi-Industry Testing
Test if a model trained on telco data works on eCommerce (transfer learning).

---

## Data Quality Notes

### Missing Values
The normalizer handles:
- Missing `Tenure` → defaults to 0
- Missing `OrderCount` → defaults to 0
- Missing `CashbackAmount` → defaults to 0.0

### Edge Cases
- **No orders (OrderCount = 0):** Creates one transaction at last order date
- **Tenure = 0:** Orders spaced 7 days apart instead of over tenure
- **Future dates:** Capped at today's date

---

## Comparison with Telco Normalizer

| Feature | Telco | eCommerce |
|---------|-------|-----------|
| **Source Format** | Snapshot | Snapshot |
| **Event Type** | monthly_charge | order |
| **Transaction Count** | Based on tenure months | Based on OrderCount |
| **Amount Source** | MonthlyCharges | CashbackAmount |
| **Date Calculation** | Tenure months ago | DaySinceLastOrder |
| **Churn Label Source** | churned column | Churn column |

---

## Next Steps

1. **Normalize Dataset:**
   ```bash
   python -m app.helpers.normalize_ecomm_dataset --mode detailed
   ```

2. **Verify Output:**
   ```bash
   head datasets/ecomm_normalized_detailed.csv
   ```

3. **Upload to Churn API:**
   Use the normalized CSV with Churn V2 endpoints

4. **Train Model:**
   Follow standard training workflow

5. **Compare Results:**
   Compare eCommerce model metrics with telco model

---

## Files Created

- **Input:** `datasets/eComm.csv` (5,630 customers)
- **Output (Simple):** `datasets/ecomm_normalized.csv` (5,630 transactions)
- **Output (Detailed):** `datasets/ecomm_normalized_detailed.csv` (16,417 transactions)
- **Script:** `app/helpers/normalize_ecomm_dataset.py`

---

Ready to train churn models on eCommerce data! 🛒
