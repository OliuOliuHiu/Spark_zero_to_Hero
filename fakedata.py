import os
import random
import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)
np.random.seed(42)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# ----------------------------
# HELPERS
# ----------------------------
DEPARTMENTS = ["IT", "HR", "Finance", "Sales", "Marketing", "Operations"]
REGIONS = ["North", "South", "East", "West"]
COUNTRIES = ["US", "UK", "Germany", "France", "Canada", "Japan", "Vietnam"]
CATEGORIES = ["Electronics", "Fashion", "Home", "Sports", "Beauty", "Books"]
PAYMENT_METHODS = ["Credit Card", "Debit Card", "PayPal", "Bank Transfer"]
ORDER_STATUSES = ["SUCCESS", "FAILED", "PENDING", "success", "failed", "Success"]
TRANSACTION_TYPES = ["PURCHASE", "REFUND", "TRANSFER", "WITHDRAWAL"]
DELIVERY_STATUSES = ["DELIVERED", "FAILED", "IN_PROGRESS", "delivered", "failed"]

def random_date(start_days=1000):
    start = datetime.now() - timedelta(days=start_days)
    return start + timedelta(days=random.randint(0, start_days))

def maybe_null(value, prob=0.1):
    return None if random.random() < prob else value

def maybe_dirty_number(num, prob=0.1):
    if random.random() < prob:
        return str(num)
    return num

def maybe_bad_date(dt, prob=0.05):
    if random.random() < prob:
        return "bad_date"
    return dt.strftime("%Y-%m-%d")

# ----------------------------
# HR DATASET
# ----------------------------
def generate_hr_data(n=1000):
    rows = []

    manager_ids = list(range(1, 51))

    for emp_id in range(1, n + 1):
        salary = random.randint(1000, 10000)

        row = {
            "emp_id": emp_id,
            "name": fake.name(),
            "dept": random.choice(DEPARTMENTS),
            "salary": maybe_null(maybe_dirty_number(salary), 0.08),
            "age": maybe_null(random.randint(21, 60), 0.08),
            "join_date": maybe_bad_date(random_date(2500), 0.03),
            "performance_score": maybe_null(random.randint(40, 100), 0.1),
            "manager_id": random.choice(manager_ids),
            "employment_status": random.choice(
                ["ACTIVE", "INACTIVE", "active", "inactive"]
            ),
        }

        rows.append(row)

    df = pd.DataFrame(rows)

    # duplicates
    df = pd.concat([df, df.sample(20)], ignore_index=True)

    df.to_csv(f"{DATA_DIR}/hr_employees.csv", index=False)
    print("Generated hr_employees.csv")

# ----------------------------
# ECOMMERCE ORDERS
# ----------------------------
def generate_ecommerce_orders(n=5000):
    rows = []

    for order_id in range(1, n + 1):
        price = round(random.uniform(10, 1000), 2)

        row = {
            "order_id": order_id,
            "customer_id": random.randint(1, 2000),
            "product_id": random.randint(1, 500),
            "category": random.choice(CATEGORIES),
            "price": maybe_dirty_number(price, 0.15),
            "quantity": maybe_null(random.randint(1, 10), 0.1),
            "order_status": random.choice(ORDER_STATUSES),
            "order_date": maybe_bad_date(random_date(1200), 0.03),
            "payment_method": random.choice(PAYMENT_METHODS),
            "country": random.choice(COUNTRIES),
        }

        rows.append(row)

    df = pd.DataFrame(rows)

    # duplicates
    df = pd.concat([df, df.sample(50)], ignore_index=True)

    df.to_csv(f"{DATA_DIR}/ecommerce_orders.csv", index=False)
    print("Generated ecommerce_orders.csv")

# ----------------------------
# BANKING TRANSACTIONS
# ----------------------------
def generate_banking_transactions(n=8000):
    merchants = [
        "Amazon",
        "Walmart",
        "Apple",
        "Netflix",
        "Uber",
        "Starbucks",
        "Target",
        "Costco",
    ]

    rows = []

    for txn_id in range(1, n + 1):
        amount = round(random.uniform(5, 5000), 2)

        row = {
            "transaction_id": txn_id,
            "account_id": random.randint(10000, 20000),
            "customer_id": random.randint(1, 3000),
            "transaction_type": random.choice(TRANSACTION_TYPES),
            "amount": maybe_dirty_number(amount, 0.1),
            "currency": random.choice(["USD", "EUR", "GBP", "JPY"]),
            "transaction_date": maybe_bad_date(random_date(1000), 0.03),
            "status": random.choice(
                ["SUCCESS", "FAILED", "PENDING", "success", "failed"]
            ),
            "merchant": random.choice(merchants),
            "country": random.choice(COUNTRIES),
        }

        rows.append(row)

    df = pd.DataFrame(rows)

    # suspicious duplicates
    df = pd.concat([df, df.sample(100)], ignore_index=True)

    df.to_csv(f"{DATA_DIR}/banking_transactions.csv", index=False)
    print("Generated banking_transactions.csv")

# ----------------------------
# SALES DATASET
# ----------------------------
def generate_sales_data(n=5000):
    rows = []

    for sale_id in range(1, n + 1):
        row = {
            "sale_id": sale_id,
            "salesperson_id": random.randint(1, 300),
            "region": random.choice(REGIONS),
            "product": f"Product_{random.randint(1, 800)}",
            "category": random.choice(CATEGORIES),
            "sale_amount": round(random.uniform(50, 10000), 2),
            "sale_date": maybe_bad_date(random_date(900), 0.03),
            "customer_id": random.randint(1, 2500),
        }

        rows.append(row)

    df = pd.DataFrame(rows)

    # duplicate rows
    df = pd.concat([df, df.sample(50)], ignore_index=True)

    df.to_csv(f"{DATA_DIR}/sales.csv", index=False)
    print("Generated sales.csv")


# ----------------------------
# DELIVERY DATASET
# ----------------------------
def generate_delivery_data(n=4000):
    cities = ["HCM", "Hanoi", "Da Nang", "Tokyo", "London", "New York"]

    rows = []

    for delivery_id in range(1, n + 1):
        pickup = random_date(500)
        duration = random.randint(10, 240)
        delivery = pickup + timedelta(minutes=duration)

        row = {
            "delivery_id": delivery_id,
            "order_id": random.randint(1, 7000),
            "driver_id": random.randint(1, 500),
            "city": random.choice(cities),
            "pickup_time": pickup.strftime("%Y-%m-%d %H:%M:%S"),
            "delivery_time": (
                "bad_time"
                if random.random() < 0.03
                else delivery.strftime("%Y-%m-%d %H:%M:%S")
            ),
            "delivery_status": random.choice(DELIVERY_STATUSES),
            "distance_km": round(random.uniform(1, 40), 2),
            "delivery_fee": round(random.uniform(1, 30), 2),
            "customer_rating": maybe_null(round(random.uniform(1, 5), 1), 0.1),
        }

        rows.append(row)

    df = pd.DataFrame(rows)

    # duplicates
    df = pd.concat([df, df.sample(40)], ignore_index=True)

    df.to_csv(f"{DATA_DIR}/deliveries.csv", index=False)
    print("Generated deliveries.csv")


# ----------------------------
# RETAIL PROJECT DATASETS
# ----------------------------
def generate_retail_project():
    # customers
    customers = []

    for customer_id in range(1, 2001):
        customers.append({
            "customer_id": customer_id,
            "name": fake.name(),
            "city": random.choice(["HCM", "Hanoi", "Tokyo", "London", "Berlin"]),
            "country": random.choice(COUNTRIES),
            "signup_date": maybe_bad_date(random_date(1500), 0.03),
            "segment": random.choice(["Consumer", "Corporate", "SMB"]),
        })

    customers_df = pd.DataFrame(customers)
    customers_df.to_csv(f"{DATA_DIR}/customers.csv", index=False)

    # products
    products = []

    for product_id in range(1, 501):
        products.append({
            "product_id": product_id,
            "product_name": f"Product_{product_id}",
            "category": random.choice(CATEGORIES),
            "brand": random.choice(["BrandA", "BrandB", "BrandC", "BrandD"]),
            "cost": round(random.uniform(5, 500), 2),
        })

    products_df = pd.DataFrame(products)
    products_df.to_csv(f"{DATA_DIR}/products.csv", index=False)

    # orders
    orders = []

    for order_id in range(1, 8001):
        orders.append({
            "order_id": order_id,
            "customer_id": random.randint(1, 2200),  # invalid FK intentionally
            "order_date": maybe_bad_date(random_date(1200), 0.03),
            "status": random.choice(
                ["SUCCESS", "FAILED", "PENDING", "success", "failed"]
            ),
            "payment_method": random.choice(PAYMENT_METHODS),
        })

    orders_df = pd.DataFrame(orders)

    # duplicates
    orders_df = pd.concat([orders_df, orders_df.sample(100)], ignore_index=True)

    orders_df.to_csv(f"{DATA_DIR}/orders.csv", index=False)

    # order_items
    order_items = []

    for _ in range(16000):
        order_items.append({
            "order_id": random.randint(1, 8000),
            "product_id": random.randint(1, 550),  # invalid FK intentionally
            "quantity": maybe_null(random.randint(1, 8), 0.05),
            "unit_price": maybe_dirty_number(
                round(random.uniform(10, 1000), 2),
                0.1
            ),
        })

    items_df = pd.DataFrame(order_items)

    # duplicates
    items_df = pd.concat([items_df, items_df.sample(150)], ignore_index=True)

    items_df.to_csv(f"{DATA_DIR}/order_items.csv", index=False)

    print("Generated retail project datasets")

# ----------------------------
# RUN PART 1
# ----------------------------
if __name__ == "__main__":
    generate_hr_data()
    generate_ecommerce_orders()
    generate_banking_transactions()
    generate_sales_data()
    generate_delivery_data()
    generate_retail_project()
    