import os
import random
import string
from faker import Faker
import pandas as pd

fake = Faker()


# Config
NUM_STATEMENTS = 100
# LOCAL_SAVE_FOLDER = "bank_statements"


# For prompt generation, generating a test number of files.
# NUM_STATEMENTS = 10
# LOCAL_SAVE_FOLDER = "bank_statements_prompt_gen"


CATEGORY_DISTRIBUTIONS = {
    "group1": {"groceries": 0.25, "online_shopping": 0.15, "utilities": 0.15, "travel": 0.15, "others": 0.1, "stocks": 0.05, "funds": 0.05, "job": 0.05, "misc": 0.05},
    "group2": {"groceries": 0.3, "online_shopping": 0.1, "utilities": 0.15, "travel": 0.1, "others": 0.1, "stocks": 0.05, "funds": 0.1, "job": 0.05, "misc": 0.05},
}


CATEGORIES = list(CATEGORY_DISTRIBUTIONS["group1"].keys())


MERCHANTS_IND = {
    "groceries": ["Reliance Fresh", "Spencers", "D-Mart"],
    "online_shopping": ["Flipkart", "Myntra", "Amazon India"],
    "utilities": ["Electricity Bill", "Water Bill", "Mobile Recharge", "Petrol Bunk"],
    "travel": ["Ola", "Uber", "IRCTC", "MakeMyTrip"],
    "others": ["Barista", "INOX", "Swiggy"],
    "stocks": ["Zerodha", "Groww", "Upstox"],
    "funds": ["HDFC Mutual", "SBI Mutual", "Nippon AMC"],
    "job": ["Company Payroll", "Freelance Payment", "Internship Stipend"],
    "misc": ["Gift", "Refund", "Cashback"]
}


MERCHANTS_US = {
    "groceries": ["Walmart", "Costco", "Whole Foods"],
    "online_shopping": ["Amazon", "Etsy", "eBay"],
    "utilities": ["Verizon", "AT&T", "Comcast"],
    "travel": ["Lyft", "Uber", "Greyhound"],
    "others": ["Starbucks", "Netflix", "AMC Theatres"],
    "stocks": ["Robinhood", "Charles Schwab", "Fidelity"],
    "funds": ["Vanguard", "BlackRock", "T. Rowe Price"],
    "job": ["Company Payroll", "Freelance Payment", "Part-time Work"],
    "misc": ["Gift", "Refund", "Cashback"]
}


PAYMENT_MODES_IND = ["card", "netbanking", "cash", "UPI"]
PAYMENT_MODES_US = ["card", "netbanking", "cash", "apple pay", "paypal"]


CREDIT_CATEGORIES = {"stocks", "funds", "job", "misc"}


def generate_transaction_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=14))

def generate_account_number():
    return ''.join(random.choices(string.digits, k=13))



def generate_transaction(category: str, currency: str, receiver_acc_no: str, date: pd.Timestamp = None, force_merchant: str = None):
    is_credit = category in CREDIT_CATEGORIES
    merchant_list = MERCHANTS_IND if currency == "INR" else MERCHANTS_US
    merchant = force_merchant if force_merchant else random.choice(merchant_list[category])

    if category == "job" and merchant == "Company Payroll":
        amount = round(random.uniform(20000, 90000), 2) if currency == "INR" else round(random.uniform(500, 3000), 2)
        if date is None:
            year = fake.date_between(start_date='-12M', end_date='-1d').year
            month = fake.date_between(start_date='-12M', end_date='-1d').month
            day = random.randint(1, 7)
            date = pd.Timestamp(year=year, month=month, day=day)
    elif category == "job":
        amount = round(random.uniform(5000, 30000), 2) if currency == "INR" else round(random.uniform(100, 1000), 2)
        if date is None:
            date = fake.date_between(start_date='-12M', end_date='today')
    elif category in {"stocks", "funds"}:
        amount = round(random.uniform(1000, 15000), 2) if currency == "INR" else round(random.uniform(100, 1200), 2)
        if date is None:
            date = fake.date_between(start_date='-12M', end_date='today')
    else:
        amount = round(random.uniform(50, 5000), 2) if currency == "INR" else round(random.uniform(1, 100), 2)
        if date is None:
            date = fake.date_between(start_date='-12M', end_date='today')

    if category in {"job", "stocks", "funds"}:
        payment_mode = "netbanking"
    elif category == "misc":
        payment_mode = random.choice(PAYMENT_MODES_IND if currency == "INR" else PAYMENT_MODES_US)
    else:
        payment_mode = random.choice(PAYMENT_MODES_IND if currency == "INR" else PAYMENT_MODES_US)

    return {
        "transaction_id": generate_transaction_id(),
        "date": date.strftime("%Y-%m-%d"),
        "merchant": merchant,
        "category": category,
        "amount": amount,
        "currency": currency,
        "payment_mode": payment_mode,
        "receiver_acc_no": receiver_acc_no,
        "sender_acc_no": generate_account_number(),
        "type": "credit" if is_credit else "debit"
    }



def generate_statement(customer_group: str, currency: str):
    distribution = CATEGORY_DISTRIBUTIONS[customer_group]
    num_transactions = random.randint(25, 50)
    transactions = []

    receiver_acc_no = generate_account_number()

    months_to_generate = sorted(set(
        pd.date_range(end=pd.Timestamp.today(), periods=12, freq='M').to_period('M')
    ))

    for month in months_to_generate:
        year = month.year
        month_num = month.month
        day = random.randint(1, 7)
        salary_date = pd.Timestamp(year=year, month=month_num, day=day)
        transactions.append(generate_transaction(
            category="job",
            currency=currency,
            receiver_acc_no=receiver_acc_no,
            date=salary_date,
            force_merchant="Company Payroll"
        ))

    for _ in range(num_transactions):
        category = random.choices(list(distribution.keys()), weights=distribution.values())[0]

        if category == "job":
            merchant = random.choice([
                m for m in (MERCHANTS_IND if currency == "INR" else MERCHANTS_US)["job"]
                if m != "Company Payroll"
            ])
            transactions.append(generate_transaction(category, currency, receiver_acc_no, force_merchant=merchant))
        else:
            transactions.append(generate_transaction(category, currency, receiver_acc_no))

    return pd.DataFrame(transactions)




def save_statement(df: pd.DataFrame, filename: str, folder):
    path = os.path.join(folder, filename)
    df.to_csv(path, index=False)
    return path

def generate_statements(NUM_STATEMENTS, folder):
    os.makedirs(folder, exist_ok=True)

    for i in range(NUM_STATEMENTS):
        customer_group = random.choice(["group1", "group2"])
        currency = random.choices(["INR", "USD"], weights=[0.4, 0.6])[0]
        df = generate_statement(customer_group, currency)
        filename = f"statement_{i}_{currency}.csv"
        filepath = save_statement(df, filename, folder)
        print(f"Generated statement: {filepath}")

# generate_statements(NUM_STATEMENTS, LOCAL_SAVE_FOLDER)
