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
    quantity: int
    price_per_unit: float

class Client(BaseModel):
    name: str
    email: str
    phone: str

# Create tables in PostgreSQL
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
            quantity INTEGER NOT NULL,
            price_per_unit REAL NOT NULL
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

# Stock endpoints
@app.post("/stock/")
def add_stock(stock: Stock):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO stock (product_name, quantity, price_per_unit)
        VALUES (%s, %s, %s)
    ''', (stock.product_name, stock.quantity, stock.price_per_unit))
    conn.commit()
    conn.close()
    return {"message": "Stock added successfully"}

@app.get("/stock/")
def get_stock():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stock')
    stock = cursor.fetchall()
    conn.close()
    return {"stock": [dict(zip([col[0] for col in cursor.description], row)) for row in stock]}

# Client endpoints
@app.post("/clients/")
def add_client(client: Client):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clients (name, email, phone)
        VALUES (%s, %s, %s)
    ''', (client.name, client.email, client.phone))
    conn.commit()
    conn.close()
    return {"message": "Client added successfully"}

@app.get("/clients/")
def get_clients():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients')
    clients = cursor.fetchall()
    conn.close()
    return {"clients": [dict(zip([col[0] for col in cursor.description], row)) for row in clients]}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
