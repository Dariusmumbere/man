from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import psycopg2
import logging
from typing import List, Optional

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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

class BankAccountUpdate(BaseModel):
    balance: float
    purpose: str

class Client(BaseModel):
    name: str
    email: str
    phone: str

# Initialize database tables
def init_db():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        # Drop and recreate tables to ensure the correct schema
        cursor.execute('DROP TABLE IF EXISTS products;')
        cursor.execute('DROP TABLE IF EXISTS services;')
        cursor.execute('DROP TABLE IF EXISTS stock;')
        cursor.execute('DROP TABLE IF EXISTS bank_account;')
        cursor.execute('DROP TABLE IF EXISTS clients;')

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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        ''')
        # Initialize the balance to 0 if the table is empty
        cursor.execute('SELECT COUNT(*) FROM bank_account')
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO bank_account (balance) VALUES (0)')
        conn.commit()
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

# Initialize database
init_db()

# Product endpoints
@app.post("/products/")
def add_product(product: Product):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        logger.debug(f"Adding product: {product}")
        cursor.execute('''
            INSERT INTO products (name, type, buying_price, selling_price)
            VALUES (%s, %s, %s, %s)
        ''', (
            product.name, product.type, product.buying_price, product.selling_price
        ))
        conn.commit()
        return {"message": "Product added successfully"}
    except Exception as e:
        logger.error(f"Error adding product: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add product: {str(e)}")
    finally:
        if conn:
            conn.close()

@app.get("/products/")
def get_products():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        return {"products": [dict(zip([col[0] for col in cursor.description], row)) for row in products]}
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch products")
    finally:
        if conn:
            conn.close()

@app.delete("/products/{product_name}/{product_type}")
def delete_product(product_name: str, product_type: str):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE name = %s AND type = %s', (product_name, product_type))
        product = cursor.fetchone()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        cursor.execute('DELETE FROM products WHERE name = %s AND type = %s', (product_name, product_type))
        conn.commit()
        return {"message": "Product deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting product: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete product")
    finally:
        if conn:
            conn.close()

# Stock endpoints
@app.post("/stock/")
def add_stock(stock: Stock):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Insert into the stock table
        cursor.execute('''
            INSERT INTO stock (product_name, product_type, quantity, price_per_unit)
            VALUES (%s, %s, %s, %s)
        ''', (
            stock.product_name, stock.product_type, stock.quantity, stock.price_per_unit
        ))
        conn.commit()
        return {"message": "Stock added successfully"}
    except Exception as e:
        logger.error(f"Error adding stock: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add stock: {str(e)}")
    finally:
        if conn:
            conn.close()

@app.get("/stock/")
def get_stock():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM stock')
        stock = cursor.fetchall()
        return {"stock": [dict(zip([col[0] for col in cursor.description], row)) for row in stock]}
    except Exception as e:
        logger.error(f"Error fetching stock: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch stock")
    finally:
        if conn:
            conn.close()

@app.delete("/stock/{product_name}/{product_type}")
def delete_stock(product_name: str, product_type: str):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM stock WHERE product_name = %s AND product_type = %s', (product_name, product_type))
        stock_item = cursor.fetchone()
        if not stock_item:
            raise HTTPException(status_code=404, detail="Stock item not found")

        cursor.execute('DELETE FROM stock WHERE product_name = %s AND product_type = %s', (product_name, product_type))
        conn.commit()
        return {"message": "Stock item deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting stock item: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete stock item")
    finally:
        if conn:
            conn.close()

# Service endpoints
@app.post("/services/")
def add_service(service: Service):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO services (name, description, price)
            VALUES (%s, %s, %s)
        ''', (service.name, service.description, service.price))
        conn.commit()
        return {"message": "Service added successfully"}
    except Exception as e:
        logger.error(f"Error adding service: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to add service")
    finally:
        if conn:
            conn.close()

@app.get("/services/")
def get_services():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM services')
        services = cursor.fetchall()
        return {"services": [dict(zip([col[0] for col in cursor.description], row)) for row in services]}
    except Exception as e:
        logger.error(f"Error fetching services: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch services")
    finally:
        if conn:
            conn.close()

@app.delete("/services/{service_name}")
def delete_service(service_name: str):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM services WHERE name = %s', (service_name,))
        service = cursor.fetchone()
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")

        cursor.execute('DELETE FROM services WHERE name = %s', (service_name,))
        conn.commit()
        return {"message": "Service deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting service: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete service")
    finally:
        if conn:
            conn.close()

# Bank Account endpoints
@app.get("/bank_account/")
def get_bank_account():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT balance FROM bank_account WHERE id = 1')
        balance = cursor.fetchone()[0]
        return {"balance": balance}
    except Exception as e:
        logger.error(f"Error fetching bank account balance: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch bank account balance")
    finally:
        if conn:
            conn.close()

@app.post("/bank_account/")
def update_bank_account(bank_account: BankAccountUpdate):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT balance FROM bank_account WHERE id = 1')
        current_balance = cursor.fetchone()[0]
        new_balance = current_balance + bank_account.balance
        cursor.execute('UPDATE bank_account SET balance = %s WHERE id = 1', (new_balance,))
        conn.commit()
        return {"message": "Bank account balance updated successfully"}
    except Exception as e:
        logger.error(f"Error updating bank account balance: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to update bank account balance")
    finally:
        if conn:
            conn.close()

# Client endpoints
@app.post("/clients/")
def add_client(client: Client):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clients (name, email, phone)
            VALUES (%s, %s, %s)
        ''', (client.name, client.email, client.phone))
        conn.commit()
        return {"message": "Client added successfully"}
    except Exception as e:
        logger.error(f"Error adding client: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to add client")
    finally:
        if conn:
            conn.close()

@app.get("/clients/")
def get_clients():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clients')
        clients = cursor.fetchall()
        return {"clients": [dict(zip([col[0] for col in cursor.description], row)) for row in clients]}
    except Exception as e:
        logger.error(f"Error fetching clients: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch clients")
    finally:
        if conn:
            conn.close()

@app.delete("/clients/{client_name}")
def delete_client(client_name: str):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clients WHERE name = %s', (client_name,))
        client = cursor.fetchone()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")

        cursor.execute('DELETE FROM clients WHERE name = %s', (client_name,))
        conn.commit()
        return {"message": "Client deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting client: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete client")
    finally:
        if conn:
            conn.close()

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
