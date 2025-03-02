from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import psycopg2

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://itech_l1q2_user:AoqQkrtzrQW7WEDOJdh0C6hhlY5Xe3sv@dpg-cuvnsbggph6c73ev87g0-a/itech_l1q2")

def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Pydantic models
class Product(BaseModel):
    name: str
    type: str
    buying_price: float
    selling_price: float

class Service(BaseModel):
    name: str
    description: str
    price: float

class Stock(BaseModel):
    product_name: str
    product_type: str
    quantity: int
    price_per_unit: float

class BankAccount(BaseModel):
    balance: float

# Initialize database tables
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            buying_price REAL NOT NULL,
            selling_price REAL NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock (
            id SERIAL PRIMARY KEY,
            product_name TEXT NOT NULL,
            product_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price_per_unit REAL NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bank_account (
            id SERIAL PRIMARY KEY,
            balance REAL NOT NULL
        )
    ''')
    # Initialize the balance to 0 if the table is empty
    cursor.execute('SELECT COUNT(*) FROM bank_account')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO bank_account (balance) VALUES (0)')
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Product endpoints
@app.post("/products/")
def add_product(product: Product):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (name, type, buying_price, selling_price)
        VALUES (%s, %s, %s, %s)
    ''', (product.name, product.type, product.buying_price, product.selling_price))
    conn.commit()
    conn.close()
    return {"message": "Product added successfully"}

@app.get("/products/")
def get_products():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return {"products": [dict(zip([col[0] for col in cursor.description], row)) for row in products]}

@app.delete("/products/{product_name}/{product_type}")
def delete_product(product_name: str, product_type: str):
    conn = get_db()
    cursor = conn.cursor()
    # Check if the product exists
    cursor.execute('SELECT * FROM products WHERE name = %s AND type = %s', (product_name, product_type))
    product = cursor.fetchone()
    if not product:
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Delete the product
    cursor.execute('DELETE FROM products WHERE name = %s AND type = %s', (product_name, product_type))
    conn.commit()
    conn.close()
    return {"message": "Product deleted successfully"}

# Stock endpoints
@app.post("/stock/")
def add_stock(stock: Stock):
    conn = get_db()
    cursor = conn.cursor()
    # Check if the stock item already exists
    cursor.execute('SELECT * FROM stock WHERE product_name = %s AND product_type = %s', (stock.product_name, stock.product_type))
    existing_stock = cursor.fetchone()
    
    if existing_stock:
        # Update the existing stock item
        new_quantity = existing_stock[3] + stock.quantity
        cursor.execute('''
            UPDATE stock
            SET quantity = %s, price_per_unit = %s
            WHERE product_name = %s AND product_type = %s
        ''', (new_quantity, stock.price_per_unit, stock.product_name, stock.product_type))
    else:
        # Insert a new stock item
        cursor.execute('''
            INSERT INTO stock (product_name, product_type, quantity, price_per_unit)
            VALUES (%s, %s, %s, %s)
        ''', (stock.product_name, stock.product_type, stock.quantity, stock.price_per_unit))
    
    conn.commit()
    conn.close()
    return {"message": "Stock added/updated successfully"}

@app.get("/stock/")
def get_stock():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stock')
    stock = cursor.fetchall()
    conn.close()
    return {"stock": [dict(zip([col[0] for col in cursor.description], row)) for row in stock]}

@app.delete("/stock/{product_name}/{product_type}")
def delete_stock(product_name: str, product_type: str):
    conn = get_db()
    cursor = conn.cursor()
    # Check if the stock item exists
    cursor.execute('SELECT * FROM stock WHERE product_name = %s AND product_type = %s', (product_name, product_type))
    stock_item = cursor.fetchone()
    if not stock_item:
        conn.close()
        raise HTTPException(status_code=404, detail="Stock item not found")
    
    # Delete the stock item
    cursor.execute('DELETE FROM stock WHERE product_name = %s AND product_type = %s', (product_name, product_type))
    conn.commit()
    conn.close()
    return {"message": "Stock item deleted successfully"}

# Service endpoints
@app.post("/services/")
def add_service(service: Service):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO services (name, description, price)
        VALUES (%s, %s, %s)
    ''', (service.name, service.description, service.price))
    conn.commit()
    conn.close()
    return {"message": "Service added successfully"}

@app.get("/services/")
def get_services():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM services')
    services = cursor.fetchall()
    conn.close()
    return {"services": [dict(zip([col[0] for col in cursor.description], row)) for row in services]}

# Bank Account endpoints
@app.get("/bank_account/")
def get_bank_account():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT balance FROM bank_account WHERE id = 1')
    balance = cursor.fetchone()[0]
    conn.close()
    return {"balance": balance}

@app.post("/bank_account/")
def update_bank_account(bank_account: BankAccount):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE bank_account SET balance = %s WHERE id = 1', (bank_account.balance,))
    conn.commit()
    conn.close()
    return {"message": "Bank account balance updated successfully"}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
