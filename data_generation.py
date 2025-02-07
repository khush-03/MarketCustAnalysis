import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

conn = psycopg2.connect(
    dbname="supermarket_analysis",
    user="postgres",
    password="1108",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

fake = Faker()

def generate_customers(n):
    for _ in range(n):
        age = random.randint(18, 70)
        gender = random.choice(['Male', 'Female'])
        cur.execute("INSERT INTO Customers (age, gender) VALUES (%s, %s)", (age, gender))
    conn.commit()

def generate_visits(n):
    cur.execute("SELECT MAX(customer_id) FROM Customers")
    max_customer_id = cur.fetchone()[0]
    for _ in range(n):
        customer_id = random.randint(1, max_customer_id)
        visit_date = fake.date_between(start_date='-1y', end_date='today')
        entry_time = fake.date_time_between(start_date='-1y', end_date='now')
        exit_time = entry_time + timedelta(minutes=random.randint(30, 120))
        season = random.choice(['Winter', 'Spring', 'Summer', 'Autumn'])
        cur.execute("INSERT INTO Visits (customer_id, visit_date, entry_time, exit_time, season) VALUES (%s, %s, %s, %s, %s)", (customer_id, visit_date, entry_time, exit_time, season))
    conn.commit()

def generate_sections():
    sections = [
        ('Produce', 'Veggies'),
        ('Produce', 'Fruits'),
        ('Dairy', 'Dairy & Eggs'),
        ('Bakery', 'Bakery'),
        ('Meat', 'Meat & Seafood'),
        ('Frozen', 'Frozen Foods'),
        ('Beverages', 'Beverages'),
        ('Snacks', 'Snacks'),
        ('Household', 'Household Supplies')
    ]
    for section_name, category in sections:
        cur.execute("INSERT INTO Sections (section_name, category) VALUES (%s, %s)", (section_name, category))
    conn.commit()

def generate_products(n):
    category_products = {
        'Veggies': ['Carrot', 'Broccoli', 'Spinach'],
        'Fruits': ['Apple', 'Banana', 'Orange'],
        'Dairy & Eggs': ['Milk', 'Cheese', 'Yogurt'],
        'Bakery': ['Bread', 'Croissant', 'Cake'],
        'Meat & Seafood': ['Chicken', 'Salmon', 'Beef'],
        'Frozen Foods': ['Frozen Pizza', 'Ice Cream', 'Frozen Vegetables'],
        'Beverages': ['Soda', 'Juice', 'Water'],
        'Snacks': ['Chips', 'Cookies', 'Nuts'],
        'Household Supplies': ['Detergent', 'Soap', 'Paper Towels']
    }
    for category, products in category_products.items():
        for product_name in products:
            price = round(random.uniform(1, 20), 2)
            cur.execute("INSERT INTO Products (product_name, category, price) VALUES (%s, %s, %s)", (product_name, category, price))
    conn.commit()

def generate_interactions(n):
    cur.execute("SELECT MAX(visit_id) FROM Visits")
    max_visit_id = cur.fetchone()[0]
    cur.execute("SELECT MAX(product_id) FROM Products")
    max_product_id = cur.fetchone()[0]
    cur.execute("SELECT MAX(section_id) FROM Sections")
    max_section_id = cur.fetchone()[0]
    for _ in range(n):
        visit_id = random.randint(1, max_visit_id)
        product_id = random.randint(1, max_product_id)
        section_id = random.randint(1, max_section_id)
        interaction_time = fake.date_time_between(start_date='-1y', end_date='now')
        cur.execute("INSERT INTO Interactions (visit_id, product_id, section_id, interaction_time) VALUES (%s, %s, %s, %s)", (visit_id, product_id, section_id, interaction_time))
    conn.commit()

def generate_purchases(n):
    cur.execute("SELECT MAX(visit_id) FROM Visits")
    max_visit_id = cur.fetchone()[0]
    cur.execute("SELECT MAX(product_id) FROM Products")
    max_product_id = cur.fetchone()[0]
    for _ in range(n):
        visit_id = random.randint(1, max_visit_id)
        product_id = random.randint(1, max_product_id)
        quantity = random.randint(1, 5)
        purchase_time = fake.date_time_between(start_date='-1y', end_date='now')
        total_price = round(random.uniform(1, 100), 2)
        cur.execute("INSERT INTO Purchases (visit_id, product_id, quantity, purchase_time, total_price) VALUES (%s, %s, %s, %s, %s)", (visit_id, product_id, quantity, purchase_time, total_price))
    conn.commit()

def generate_customer_paths(n):
    cur.execute("SELECT MAX(visit_id) FROM Visits")
    max_visit_id = cur.fetchone()[0]
    cur.execute("SELECT MAX(section_id) FROM Sections")
    max_section_id = cur.fetchone()[0]
    for visit_id in range(1, max_visit_id + 1):
        num_sections = random.randint(3, 10)
        sections_visited = random.sample(range(1, max_section_id + 1), num_sections)
        for sequence_number, section_id in enumerate(sections_visited, start=1):
            timestamp = fake.date_time_between(start_date='-1y', end_date='now')
            cur.execute("INSERT INTO Customer_Path (visit_id, section_id, sequence_number, timestamp) VALUES (%s, %s, %s, %s)", (visit_id, section_id, sequence_number, timestamp))
    conn.commit()

def generate_queue_wait_times(n):
    cur.execute("SELECT MAX(visit_id) FROM Visits")
    max_visit_id = cur.fetchone()[0]
    for _ in range(n):
        visit_id = random.randint(1, max_visit_id)
        start_time = fake.date_time_between(start_date='-1y', end_date='now')
        end_time = start_time + timedelta(minutes=random.randint(1, 15))
        wait_duration = (end_time - start_time).seconds // 60
        cur.execute("INSERT INTO Queue_Wait_Times (visit_id, start_time, end_time, wait_duration) VALUES (%s, %s, %s, %s)", (visit_id, start_time, end_time, wait_duration))
    conn.commit()

generate_customers(500)        
generate_sections()            
generate_products(50)          
generate_visits(2500)           
generate_interactions(5000)     
generate_purchases(2500)        
generate_customer_paths(2500)  
generate_queue_wait_times(500) 

cur.close()
conn.close()
