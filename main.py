from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import psycopg2
import logging
import json
from typing import List, Optional
from datetime import date,datetime
from typing import Dict
import uuid
import shutil
from typing import List
from pathlib import Path

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
    expose_headers=["Content-Disposition"]  # Important for file downloads
)


# Database connection
DATABASE_URL=os.getenv("DATABASE_URL", "postgresql://itech_l1q2_user:AoqQkrtzrQW7WEDOJdh0C6hhlY5Xe3sv@dpg-cuvnsbggph6c73ev87g0-a/itech_l1q2")

def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Pydantic models
class Task(BaseModel):
    title: str
    content: str
    date: str
    status: str  # "pending", "ongoing", "completed"

class DiaryEntry(BaseModel):
    content: str
    date: str

class TaskStatusUpdate(BaseModel):
    status: str
    
class StockUpdate(BaseModel):
    quantity: int
    price_per_unit: float

class Notification(BaseModel):
    message: str
    type: str
    created_at: Optional[datetime] = None
    is_read: Optional[bool] = False

class Transaction(BaseModel):
    date: str
    type: str  # "deposit" or "withdraw"
    amount: float
    purpose: str
    
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

class Asset(BaseModel):
    name: str
    type: str
    cost_price: float
    current_value: float
    quantity: int

class SaleItem(BaseModel):
    name: str
    type: str  # "product" or "service"
    quantity: int
    unit_price: float
    total: float

class Sale(BaseModel):
    client_name: str
    items: List[SaleItem]
    total_amount: float
    
class Expense(BaseModel):
    date: str
    person: str
    description: str
    cost: float
    quantity: int   

class Folder(BaseModel):
    id: str
    name: str
    parent_id: Optional[str] = None

class FileItem(BaseModel):
    id: str
    name: str
    type: str
    size: int
    folder_id: Optional[str] = None

class FolderContents(BaseModel):
    folders: List[Folder]
    files: List[FileItem]

class FolderCreate(BaseModel):
    name: str
    
class DonorCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    donor_type: Optional[str] = None
    notes: Optional[str] = None
    category: Optional[str] = "one-time"
    
class Donation(BaseModel):
    donor_name: str
    amount: float
    payment_method: str
    date: date
    project: Optional[str] = None
    notes: Optional[str] = None
    status: str = "pending"  # "pending", "completed"

class Donor(BaseModel):
    id: Optional[int] = None
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    donor_type: Optional[str] = None  # "individual", "corporate", "foundation", etc.
    notes: Optional[str] = None
    created_at: Optional[datetime] = None

class DonationCreate(BaseModel):
    donor_name: str
    amount: float
    payment_method: str
    date: str
    project: Optional[str] = None
    notes: Optional[str] = None

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: str
    end_date: str
    budget: float
    funding_source: str
    status: str = "planned"

class Project(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    start_date: str
    end_date: str
    budget: float
    funding_source: str
    status: str
    created_at: datetime

    
# File storage setup
UPLOAD_DIR = "uploads/fundraising"
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

# Initialize database tables
def init_db():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        # Drop and recreate tables to ensure the correct schema
        cursor.execute('DROP TABLE IF EXISTS diary_entries')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS donors (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                address TEXT,
                donor_type TEXT,
                notes TEXT,
                category TEXT DEFAULT 'one-time',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute("""
            DO $$
            BEGIN
                BEGIN
                    ALTER TABLE donors ADD COLUMN category TEXT DEFAULT 'one-time';
                EXCEPTION
                    WHEN duplicate_column THEN 
                    RAISE NOTICE 'column category already exists in donors';
                END;
            END $$;
        """)
                        
        
        
        
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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assets (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                cost_price REAL NOT NULL,
                current_value REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id SERIAL PRIMARY KEY,
                client_name TEXT NOT NULL,
                items JSONB NOT NULL,
                total_amount REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id SERIAL PRIMARY KEY,
                date DATE NOT NULL,
                person TEXT NOT NULL,
                description TEXT NOT NULL,
                cost REAL NOT NULL,
                quantity INTEGER NOT NULL,
                total REAL NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                type TEXT NOT NULL,  -- 'deposit' or 'withdraw'
                amount REAL NOT NULL,
                purpose TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id SERIAL PRIMARY KEY,
                message TEXT NOT NULL,
                type TEXT NOT NULL,  -- e.g., 'sale', 'transaction', 'stock_update'
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_read BOOLEAN DEFAULT FALSE  -- Track read/unread status
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
    CREATE TABLE diary_entries (
        id SERIAL PRIMARY KEY,
        content TEXT NOT NULL,
        date TEXT NOT NULL
    )
''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS folders (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                parent_id TEXT REFERENCES folders(id) ON DELETE CASCADE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS donations (
                id SERIAL PRIMARY KEY,
                donor_name TEXT NOT NULL,
                amount REAL NOT NULL,
                payment_method TEXT NOT NULL,
                date DATE NOT NULL,
                project TEXT,
                notes TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                size INTEGER NOT NULL,
                folder_id TEXT REFERENCES folders(id) ON DELETE CASCADE,
                path TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                budget REAL NOT NULL,
                funding_source TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('SELECT id FROM folders WHERE id = %s', ('root',))
        if not cursor.fetchone():
            cursor.execute('INSERT INTO folders (id, name) VALUES (%s, %s)', ('root', 'Fundraising Documents'))
        
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
@app.get("/total_stock/")
def get_total_stock():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(quantity * price_per_unit) FROM stock')
        total_stock = cursor.fetchone()[0] or 0
        return {"total_stock": total_stock}
    except Exception as e:
        logger.error(f"Error calculating total stock: {e}")
        raise HTTPException(status_code=500, detail="Failed to calculate total stock")
    finally:
        if conn:
            conn.close()

@app.post("/stock/")
def add_stock(stock: Stock):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
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

@app.put("/stock/{product_name}/{product_type}")
def update_stock(product_name: str, product_type: str, stock: Stock):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE stock
            SET quantity = %s, price_per_unit = %s
            WHERE product_name = %s AND product_type = %s
        ''', (stock.quantity, stock.price_per_unit, product_name, product_type))
        conn.commit()
        return {"message": "Stock updated successfully"}
    except Exception as e:
        logger.error(f"Error updating stock: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update stock: {str(e)}")
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
        
        # Get the current balance
        cursor.execute('SELECT balance FROM bank_account WHERE id = 1')
        current_balance = cursor.fetchone()[0]
        
        # Calculate the new balance
        new_balance = current_balance + bank_account.balance
        
        # Update the bank account balance
        cursor.execute('UPDATE bank_account SET balance = %s WHERE id = 1', (new_balance,))
        
        # Log the transaction
        transaction_type = "deposit" if bank_account.balance > 0 else "withdraw"
        cursor.execute('''
            INSERT INTO transactions (type, amount, purpose)
            VALUES (%s, %s, %s)
        ''', (transaction_type, abs(bank_account.balance), bank_account.purpose))
        
        conn.commit()
        return {"message": "Bank account balance updated and transaction logged successfully"}
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

# Asset endpoints
@app.post("/assets/")
def add_asset(asset: Asset):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO assets (name, type, cost_price, current_value, quantity)
            VALUES (%s, %s, %s, %s, %s)
        ''', (asset.name, asset.type, asset.cost_price, asset.current_value, asset.quantity))
        conn.commit()
        return {"message": "Asset added successfully"}
    except Exception as e:
        logger.error(f"Error adding asset: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add asset: {str(e)}")
    finally:
        if conn:
            conn.close()

@app.get("/assets/")
def get_assets():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM assets')
        assets = cursor.fetchall()
        return {"assets": [dict(zip([col[0] for col in cursor.description], row)) for row in assets]}
    except Exception as e:
        logger.error(f"Error fetching assets: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch assets")
    finally:
        if conn:
            conn.close()

@app.delete("/assets/{asset_id}")
def delete_asset(asset_id: int):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM assets WHERE id = %s', (asset_id,))
        asset = cursor.fetchone()
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")

        cursor.execute('DELETE FROM assets WHERE id = %s', (asset_id,))
        conn.commit()
        return {"message": "Asset deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting asset: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete asset")
    finally:
        if conn:
            conn.close()

# Total Investment endpoint
@app.get("/total_investment/")
def get_total_investment():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Get total investment from assets
        cursor.execute('SELECT SUM(cost_price * quantity) FROM assets')
        total_assets = cursor.fetchone()[0] or 0

        # Get bank account balance
        cursor.execute('SELECT balance FROM bank_account WHERE id = 1')
        bank_balance = cursor.fetchone()[0] or 0

        # Get total amount in stock
        cursor.execute('SELECT SUM(quantity * price_per_unit) FROM stock')
        total_stock = cursor.fetchone()[0] or 0

        # Calculate total investment
        total_investment = total_assets + bank_balance + total_stock

        return {"total_investment": total_investment}
    except Exception as e:
        logger.error(f"Error calculating total investment: {e}")
        raise HTTPException(status_code=500, detail="Failed to calculate total investment")
    finally:
        if conn:
            conn.close()

# Sales endpoints
@app.post("/sales/")
def create_sale(sale: Sale):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Insert the sale into the database
        cursor.execute('''
            INSERT INTO sales (client_name, items, total_amount)
            VALUES (%s, %s, %s)
        ''', (sale.client_name, json.dumps([item.dict() for item in sale.items]), sale.total_amount))

        # Create a notification for the sale
        notification_message = f"New sale to {sale.client_name} for UGX {sale.total_amount}"
        cursor.execute('''
            INSERT INTO notifications (message, type)
            VALUES (%s, %s)
        ''', (notification_message, "sale"))

        # Update the bank account balance
        cursor.execute('SELECT balance FROM bank_account WHERE id = 1')
        current_balance = cursor.fetchone()[0]
        new_balance = current_balance + sale.total_amount
        cursor.execute('UPDATE bank_account SET balance = %s WHERE id = 1', (new_balance,))

        # Update stock quantities for products only
        for item in sale.items:
            if item.type == "product":
                cursor.execute('SELECT * FROM stock WHERE product_name = %s', (item.name,))
                stock_item = cursor.fetchone()
                if not stock_item:
                    raise HTTPException(status_code=404, detail=f"Stock item {item.name} not found")
                if stock_item[3] < item.quantity:  # stock_item[3] is the quantity
                    raise HTTPException(status_code=400, detail=f"Insufficient stock for {item.name}")

                cursor.execute('''
                    UPDATE stock
                    SET quantity = quantity - %s
                    WHERE product_name = %s
                ''', (item.quantity, item.name))

        conn.commit()
        return {"message": "Sale created, bank account updated, stock quantities reduced, and notification sent successfully"}
    except Exception as e:
        logger.error(f"Error creating sale: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create sale: {str(e)}")
    finally:
        if conn:
            conn.close()
            
@app.get("/sales/")
def get_sales(date: str = None):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        if date:
            # Filter sales by the specified date
            cursor.execute('''
                SELECT * FROM sales 
                WHERE DATE(created_at) = %s
                ORDER BY created_at DESC
            ''', (date,))
        else:
            # Get all sales if no date filter
            cursor.execute('SELECT * FROM sales ORDER BY created_at DESC')
            
        sales = cursor.fetchall()
        return {"sales": [dict(zip([col[0] for col in cursor.description], row)) for row in sales]}
    except Exception as e:
        logger.error(f"Error fetching sales: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch sales")
    finally:
        if conn:
            conn.close()
@app.get("/sales/{sale_id}")
def get_sale(sale_id: int):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sales WHERE id = %s', (sale_id,))
        sale = cursor.fetchone()
        if not sale:
            raise HTTPException(status_code=404, detail="Sale not found")
        return {"sale": dict(zip([col[0] for col in cursor.description], sale))}
    except Exception as e:
        logger.error(f"Error fetching sale: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch sale")
    finally:
        if conn:
            conn.close()
@app.delete("/sales/{sale_id}")
def delete_sale(sale_id: int):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sales WHERE id = %s', (sale_id,))
        sale = cursor.fetchone()
        if not sale:
            raise HTTPException(status_code=404, detail="Sale not found")

        cursor.execute('DELETE FROM sales WHERE id = %s', (sale_id,))
        conn.commit()
        return {"message": "Sale deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting sale: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete sale")
    finally:
        if conn:
            conn.close()    
# Expense endpoints
@app.post("/expenses/")
def add_expense(expense: Expense):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        total = expense.cost * expense.quantity

        # Insert the expense into the database
        cursor.execute('''
            INSERT INTO expenses (date, person, description, cost, quantity, total)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (
            expense.date, expense.person, expense.description, expense.cost, expense.quantity, total
        ))

        # Update the bank account balance
        cursor.execute('SELECT balance FROM bank_account WHERE id = 1')
        current_balance = cursor.fetchone()[0]
        new_balance = current_balance - total
        cursor.execute('UPDATE bank_account SET balance = %s WHERE id = 1', (new_balance,))

        conn.commit()
        return {"message": "Expense added and balance updated successfully"}
    except Exception as e:
        logger.error(f"Error adding expense: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add expense: {str(e)}")
    finally:
        if conn:
            conn.close()

@app.get("/expenses/")
def get_expenses():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
        expenses = cursor.fetchall()
        return {"expenses": [dict(zip([col[0] for col in cursor.description], row)) for row in expenses]}
    except Exception as e:
        logger.error(f"Error fetching expenses: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch expenses")
    finally:
        if conn:
            conn.close()

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM expenses WHERE id = %s', (expense_id,))
        expense = cursor.fetchone()
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")

        # Restore the balance
        cursor.execute('SELECT balance FROM bank_account WHERE id = 1')
        current_balance = cursor.fetchone()[0]
        new_balance = current_balance + expense[5]  # expense[5] is the total
        cursor.execute('UPDATE bank_account SET balance = %s WHERE id = 1', (new_balance,))

        # Delete the expense
        cursor.execute('DELETE FROM expenses WHERE id = %s', (expense_id,))
        conn.commit()
        return {"message": "Expense deleted and balance restored successfully"}
    except Exception as e:
        logger.error(f"Error deleting expense: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete expense")
    finally:
        if conn:
            conn.close()       
@app.put("/stock/{product_name}/{product_type}")
def update_stock(product_name: str, product_type: str, stock: Stock):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Check if the stock item exists
        cursor.execute('SELECT * FROM stock WHERE product_name = %s AND product_type = %s', (product_name, product_type))
        stock_item = cursor.fetchone()
        if not stock_item:
            raise HTTPException(status_code=404, detail="Stock item not found")

        # Update the stock item
        cursor.execute('''
            UPDATE stock
            SET quantity = %s, price_per_unit = %s
            WHERE product_name = %s AND product_type = %s
        ''', (stock.quantity, stock.price_per_unit, product_name, product_type))
        conn.commit()
        return {"message": "Stock updated successfully"}
    except Exception as e:
        logger.error(f"Error updating stock: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update stock: {str(e)}")
    finally:
        if conn:
            conn.close()        


@app.get("/transactions/")
def get_transactions():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Fetch all transactions from the database
        cursor.execute('''
            SELECT date, type, amount, purpose
            FROM transactions
            ORDER BY date DESC
        ''')
        transactions = cursor.fetchall()
        
        # Format the transactions for the frontend
        formatted_transactions = [
            {
                "date": transaction[0].strftime("%Y-%m-%d %H:%M:%S"),  # Format date as string
                "type": transaction[1],
                "amount": transaction[2],
                "purpose": transaction[3]
            }
            for transaction in transactions
        ]
        
        return {"transactions": formatted_transactions}
    except Exception as e:
        logger.error(f"Error fetching transactions: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch transactions")
    finally:
        if conn:
            conn.close()
            
@app.get("/net_profit/")
def get_net_profit():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        # 1. Fetch total sales revenue
        cursor.execute('SELECT SUM(total_amount) FROM sales')
        total_sales_revenue = cursor.fetchone()[0] or 0

        # 2. Fetch total cost of goods sold (COGS)
        # For products: quantity * buying_price
        cursor.execute('''
            SELECT SUM((item->>'quantity')::int * p.buying_price)
            FROM sales, jsonb_array_elements(items) AS item
            JOIN products p ON p.name = item->>'name'
            WHERE item->>'type' = 'product'
        ''')
        total_cogs_products = cursor.fetchone()[0] or 0

        # For services: quantity * unit_price * 0.5 (since services have a 30% profit margin)
        cursor.execute('''
            SELECT SUM((item->>'quantity')::int * (item->>'unit_price')::float * 0.5)
            FROM sales, jsonb_array_elements(items) AS item
            WHERE item->>'type' = 'service'
        ''')
        total_cogs_services = cursor.fetchone()[0] or 0

        # Total COGS = COGS for products + COGS for services
        total_cogs = total_cogs_products + total_cogs_services

        # 3. Fetch total expenses
        cursor.execute('SELECT SUM(total) FROM expenses')
        total_expenses = cursor.fetchone()[0] or 0

        # 4. Calculate net profit
        net_profit = (total_sales_revenue - total_cogs) - total_expenses

        return {"net_profit": net_profit}
    except Exception as e:
        logger.error(f"Error calculating net profit: {e}")
        raise HTTPException(status_code=500, detail="Failed to calculate net profit")
    finally:
        if conn:
            conn.close() 

# Create a notification
@app.post("/notifications/")
def create_notification(notification: Notification):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO notifications (message, type)
            VALUES (%s, %s)
        ''', (notification.message, notification.type))
        conn.commit()
        return {"message": "Notification created successfully"}
    except Exception as e:
        logger.error(f"Error creating notification: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to create notification")
    finally:
        if conn:
            conn.close()

# Fetch all notifications
@app.get("/notifications/")
def get_notifications():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notifications ORDER BY created_at DESC')
        notifications = cursor.fetchall()
        return {"notifications": [dict(zip([col[0] for col in cursor.description], row)) for row in notifications]}
    except Exception as e:
        logger.error(f"Error fetching notifications: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch notifications")
    finally:
        if conn:
            conn.close()

# Fetch unread notifications count
@app.get("/notifications/unread/")
def get_unread_notifications():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM notifications WHERE is_read = FALSE')
        unread_count = cursor.fetchone()[0]
        return {"unread_count": unread_count}
    except Exception as e:
        logger.error(f"Error fetching unread notifications: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch unread notifications")
    finally:
        if conn:
            conn.close()

# Mark notifications as read
@app.put("/notifications/mark_as_read/")
def mark_notifications_as_read():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE notifications SET is_read = TRUE WHERE is_read = FALSE')
        conn.commit()
        return {"message": "All notifications marked as read"}
    except Exception as e:
        logger.error(f"Error marking notifications as read: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to mark notifications as read")
    finally:
        if conn:
            conn.close()

@app.put("/stock/{product_name}/{product_type}")
def update_stock(product_name: str, product_type: str, stock_update: StockUpdate):
    logger.debug(f"Updating stock: {product_name}, {product_type}, {stock_update}")
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Check if the stock item exists
        cursor.execute('SELECT * FROM stock WHERE product_name = %s AND product_type = %s', (product_name, product_type))
        stock_item = cursor.fetchone()
        if not stock_item:
            raise HTTPException(status_code=404, detail="Stock item not found")

        # Update the stock item
        cursor.execute('''
            UPDATE stock
            SET quantity = %s, price_per_unit = %s
            WHERE product_name = %s AND product_type = %s
        ''', (stock_update.quantity, stock_update.price_per_unit, product_name, product_type))
        conn.commit()
        return {"message": "Stock updated successfully"}
    except Exception as e:
        logger.error(f"Error updating stock: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update stock: {str(e)}")
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

@app.put("/stock/{product_name}/{product_type}/increment")
def increment_stock(product_name: str, product_type: str):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Check if the stock item exists
        cursor.execute('SELECT * FROM stock WHERE product_name = %s AND product_type = %s', (product_name, product_type))
        stock_item = cursor.fetchone()
        if not stock_item:
            raise HTTPException(status_code=404, detail="Stock item not found")

        # Increment the quantity by 1
        cursor.execute('''
            UPDATE stock
            SET quantity = quantity + 1
            WHERE product_name = %s AND product_type = %s
        ''', (product_name, product_type))
        conn.commit()
        return {"message": "Stock quantity incremented successfully"}
    except Exception as e:
        logger.error(f"Error incrementing stock: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to increment stock: {str(e)}")
    finally:
        if conn:
            conn.close()

@app.get("/products/{product_name}/{product_type}")
def get_product_by_name_and_type(product_name: str, product_type: str):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE name = %s AND type = %s', (product_name, product_type))
        product = cursor.fetchone()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return dict(zip([col[0] for col in cursor.description], product))
    except Exception as e:
        logger.error(f"Error fetching product: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch product")
    finally:
        if conn:
            conn.close()

@app.put("/stock/{product_name}/{product_type}/decrement")
def decrement_stock(product_name: str, product_type: str):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Check if the stock item exists
        cursor.execute('SELECT * FROM stock WHERE product_name = %s AND product_type = %s', (product_name, product_type))
        stock_item = cursor.fetchone()
        if not stock_item:
            raise HTTPException(status_code=404, detail="Stock item not found")

        # Decrement the quantity by 1, but ensure it doesn't go below 0
        new_quantity = stock_item[3] - 1  # stock_item[3] is the quantity
        if new_quantity < 0:
            raise HTTPException(status_code=400, detail="Stock quantity cannot be negative")

        cursor.execute('''
            UPDATE stock
            SET quantity = %s
            WHERE product_name = %s AND product_type = %s
        ''', (new_quantity, product_name, product_type))
        conn.commit()
        return {"message": "Stock quantity decremented successfully"}
    except Exception as e:
        logger.error(f"Error decrementing stock: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to decrement stock: {str(e)}")
    finally:
        if conn:
            conn.close()

@app.post("/tasks/")
def add_task(task: Task):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (title, content, date, status)
            VALUES (%s, %s, %s, %s)
        ''', (task.title, task.content, task.date, task.status))
        conn.commit()
        return {"message": "Task added successfully"}
    except Exception as e:
        logger.error(f"Error adding task: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add task: {str(e)}")
    finally:
        if conn:
            conn.close()

@app.get("/tasks/")
def get_tasks():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
        return {"tasks": [dict(zip([col[0] for col in cursor.description], row)) for row in tasks]}
    except Exception as e:
        logger.error(f"Error fetching tasks: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch tasks")
    finally:
        if conn:
            conn.close()

@app.put("/tasks/{task_id}/status")
def update_task_status(task_id: int, task_status: TaskStatusUpdate):
    if task_status.status not in ["pending", "ongoing", "completed"]:
        raise HTTPException(status_code=400, detail="Invalid status. Must be 'pending', 'ongoing', or 'completed'")

    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tasks
            SET status = %s
            WHERE id = %s
        ''', (task_status.status, task_id))
        conn.commit()
        return {"message": "Task status updated successfully"}
    except Exception as e:
        logger.error(f"Error updating task status: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update task status: {str(e)}")
    finally:
        if conn:
            conn.close()
            
# Diary endpoints
@app.post("/diary/")
def add_diary_entry(entry: DiaryEntry):
    try:
        datetime.strptime(entry.date, "%Y-%m-%d")  # Validate date format
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD'")

    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO diary_entries (content, date)
            VALUES (%s, %s)
        ''', (entry.content, entry.date))
        conn.commit()
        return {"message": "Diary entry added successfully"}
    except Exception as e:
        logger.error(f"Error adding diary entry: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add diary entry: {str(e)}")
    finally:
        if conn:
            conn.close()

@app.get("/diary/")
def get_diary_entries():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM diary_entries ORDER BY date DESC')
        entries = cursor.fetchall()
        return {"entries": [dict(zip([col[0] for col in cursor.description], row)) for row in entries]}
    except Exception as e:
        logger.error(f"Error fetching diary entries: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch diary entries")
    finally:
        if conn:
            conn.close()
            
@app.get("/gross_profit/")
def get_gross_profit():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        # 1. Fetch total sales revenue
        cursor.execute('SELECT SUM(total_amount) FROM sales')
        total_sales_revenue = cursor.fetchone()[0] or 0

        # 2. Fetch total cost of goods sold (COGS)
        # For products: quantity * buying_price
        cursor.execute('''
            SELECT SUM((item->>'quantity')::int * p.buying_price)
            FROM sales, jsonb_array_elements(items) AS item
            JOIN products p ON p.name = item->>'name'
            WHERE item->>'type' = 'product'
        ''')
        total_cogs_products = cursor.fetchone()[0] or 0

        # For services: quantity * unit_price * 0.5 (since services have a 30% profit margin)
        cursor.execute('''
            SELECT SUM((item->>'quantity')::int * (item->>'unit_price')::float * 0.5)
            FROM sales, jsonb_array_elements(items) AS item
            WHERE item->>'type' = 'service'
        ''')
        total_cogs_services = cursor.fetchone()[0] or 0

        # Total COGS = COGS for products + COGS for services
        total_cogs = total_cogs_products + total_cogs_services

        # 3. Calculate gross profit
        gross_profit = total_sales_revenue - total_cogs

        return {"gross_profit": gross_profit}
    except Exception as e:
        logger.error(f"Error calculating gross profit: {e}")
        raise HTTPException(status_code=500, detail="Failed to calculate gross profit")
    finally:
        if conn:
            conn.close()

@app.post("/folders/", response_model=Folder)
def create_folder(name: str = Form(...), parent_id: Optional[str] = Form(None)):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        folder_id = str(uuid.uuid4())
        
        if parent_id:
            cursor.execute('SELECT id FROM folders WHERE id = %s', (parent_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Parent folder not found")
            
            cursor.execute('''
                INSERT INTO folders (id, name, parent_id)
                VALUES (%s, %s, %s)
                RETURNING id, name, parent_id
            ''', (folder_id, name, parent_id))
        else:
            cursor.execute('''
                INSERT INTO folders (id, name)
                VALUES (%s, %s)
                RETURNING id, name, parent_id
            ''', (folder_id, name))
        
        folder = cursor.fetchone()
        conn.commit()
        return {"id": folder[0], "name": folder[1], "parent_id": folder[2]}
    except Exception as e:
        logger.error(f"Error creating folder: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to create folder")
    finally:
        if conn:
            conn.close()
            
@app.get("/folders/{folder_id}/contents", response_model=FolderContents)
def get_folder_contents(folder_id: str = "root"):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get subfolders
        if folder_id == "root":
            cursor.execute('SELECT id, name, parent_id FROM folders WHERE parent_id IS NULL')
        else:
            cursor.execute('SELECT id, name, parent_id FROM folders WHERE parent_id = %s', (folder_id,))
            
        folders = [
            {"id": row[0], "name": row[1], "parent_id": row[2]}
            for row in cursor.fetchall()
        ]
        
        # Get files
        if folder_id == "root":
            cursor.execute('SELECT id, name, type, size FROM files WHERE folder_id IS NULL')
        else:
            cursor.execute('SELECT id, name, type, size FROM files WHERE folder_id = %s', (folder_id,))
            
        files = [
            {"id": row[0], "name": row[1], "type": row[2], "size": row[3]}
            for row in cursor.fetchall()
        ]
        
        return {"folders": folders, "files": files}
    except Exception as e:
        logger.error(f"Error getting folder contents: {e}")
        raise HTTPException(status_code=500, detail="Failed to get folder contents")
    finally:
        if conn:
            conn.close()
            
@app.post("/upload/")
def upload_files(
    files: List[UploadFile] = File(...),
    folder_id: str = Form(None)
):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        uploaded_files = []
        
        for file in files:
            file_id = str(uuid.uuid4())
            file_ext = Path(file.filename).suffix
            file_path = Path(UPLOAD_DIR) / f"{file_id}{file_ext}"
            
            # Save file synchronously
            with open(file_path, "wb") as buffer:
                buffer.write(file.file.read())
            
            file_size = file_path.stat().st_size
            
            cursor.execute('''
                INSERT INTO files (id, name, type, size, folder_id, path)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (
                file_id,
                file.filename,
                file.content_type,
                file_size,
                folder_id,
                str(file_path)
            ))
            
            uploaded_files.append({
                "id": file_id,
                "name": file.filename,
                "type": file.content_type,
                "size": file_size
            })
        
        conn.commit()
        return {"uploadedFiles": uploaded_files}
    except Exception as e:
        logger.error(f"Error uploading files: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to upload files")
    finally:
        if conn:
            conn.close()

@app.get("/files/{file_id}/download")
def download_file(file_id: str):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT name, path FROM files WHERE id = %s', (file_id,))
        file_data = cursor.fetchone()
        
        if not file_data:
            raise HTTPException(status_code=404, detail="File not found")
        
        file_name, file_path = file_data
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found on server")
        
        return FileResponse(
            file_path,
            filename=file_name,
            media_type='application/octet-stream'
        )
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        raise HTTPException(status_code=500, detail="Failed to download file")
    finally:
        if conn:
            conn.close()

@app.put("/folders/{folder_id}")
def rename_folder(folder_id: str, name: str = Form(...)):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE folders
            SET name = %s
            WHERE id = %s
            RETURNING id, name, parent_id
        ''', (name, folder_id))
        
        updated_folder = cursor.fetchone()
        if not updated_folder:
            raise HTTPException(status_code=404, detail="Folder not found")
            
        conn.commit()
        return {"id": updated_folder[0], "name": updated_folder[1], "parent_id": updated_folder[2]}
    except Exception as e:
        logger.error(f"Error renaming folder: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to rename folder")
    finally:
        if conn:
            conn.close()

@app.delete("/folders/{folder_id}")
def delete_folder(folder_id: str):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if folder exists
        cursor.execute('SELECT id FROM folders WHERE id = %s', (folder_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Folder not found")
            
        # Delete folder (cascade will handle files)
        cursor.execute('DELETE FROM folders WHERE id = %s', (folder_id,))
        conn.commit()
        return {"message": "Folder deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting folder: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete folder")
    finally:
        if conn:
            conn.close()

@app.put("/files/{file_id}")
def rename_file(file_id: str, name: str = Form(...)):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE files
            SET name = %s
            WHERE id = %s
            RETURNING id, name, type, size, folder_id
        ''', (name, file_id))
        
        updated_file = cursor.fetchone()
        if not updated_file:
            raise HTTPException(status_code=404, detail="File not found")
            
        conn.commit()
        return {
            "id": updated_file[0],
            "name": updated_file[1],
            "type": updated_file[2],
            "size": updated_file[3],
            "folder_id": updated_file[4]
        }
    except Exception as e:
        logger.error(f"Error renaming file: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to rename file")
    finally:
        if conn:
            conn.close()

@app.delete("/files/{file_id}")
def delete_file(file_id: str):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get file path before deleting
        cursor.execute('SELECT path FROM files WHERE id = %s', (file_id,))
        file_data = cursor.fetchone()
        if not file_data:
            raise HTTPException(status_code=404, detail="File not found")
            
        # Delete from database
        cursor.execute('DELETE FROM files WHERE id = %s', (file_id,))
        
        # Delete physical file
        file_path = Path(file_data[0])
        if file_path.exists():
            file_path.unlink()
            
        conn.commit()
        return {"message": "File deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete file")
    finally:
        if conn:
            conn.close()

@app.get("/files/{file_id}/preview")
def preview_file(file_id: str):
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT name, path, type FROM files WHERE id = %s', (file_id,))
        file_data = cursor.fetchone()
        
        if not file_data:
            raise HTTPException(status_code=404, detail="File not found")
        
        file_name, file_path, file_type = file_data
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found on server")
        
        # For images and PDFs, return the file directly
        if file_type in ['image/jpeg', 'image/png', 'image/gif', 'application/pdf']:
            return FileResponse(
                file_path,
                filename=file_name,
                media_type=file_type
            )
        else:
            # For other types, return a download response
            return FileResponse(
                file_path,
                filename=file_name,
                media_type='application/octet-stream'
            )
    except Exception as e:
        logger.error(f"Error previewing file: {e}")
        raise HTTPException(status_code=500, detail="Failed to preview file")
    finally:
        if conn:
            conn.close()

@app.post("/donations/", response_model=Donation)
def create_donation(donation: DonationCreate):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Insert into donations table
        cursor.execute('''
            INSERT INTO donations (donor_name, amount, payment_method, date, project, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, donor_name, amount, payment_method, date, project, notes, status, created_at
        ''', (
            donation.donor_name,
            donation.amount,
            donation.payment_method,
            donation.date,
            donation.project,
            donation.notes
        ))
        
        new_donation = cursor.fetchone()
        
        # Also record as a transaction
        cursor.execute('''
            INSERT INTO transactions (date, type, amount, purpose)
            VALUES (%s, %s, %s, %s)
        ''', (
            donation.date,
            "deposit",
            donation.amount,
            f"Donation from {donation.donor_name} via {donation.payment_method}"
        ))
        
        # Create notification
        notification_message = f"New donation from {donation.donor_name} via {donation.payment_method}"
        cursor.execute('''
            INSERT INTO notifications (message, type)
            VALUES (%s, %s)
        ''', (notification_message, "donation"))
        
        conn.commit()
        
        return {
            "id": new_donation[0],
            "donor_name": new_donation[1],
            "amount": new_donation[2],
            "payment_method": new_donation[3],
            "date": new_donation[4],
            "project": new_donation[5],
            "notes": new_donation[6],
            "status": new_donation[7],
            "created_at": new_donation[8]
        }
    except Exception as e:
        logger.error(f"Error creating donation: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()
            
@app.get("/donations/", response_model=List[Donation])
def get_donations():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, donor_name, amount, payment_method, date, project, notes, status, created_at
            FROM donations
            ORDER BY date DESC
        ''')
        
        donations = []
        for row in cursor.fetchall():
            donations.append({
                "id": row[0],
                "donor_name": row[1],
                "amount": row[2],
                "payment_method": row[3],
                "date": row[4].strftime("%Y-%m-%d") if isinstance(row[4], date) else row[4],
                "project": row[5],
                "notes": row[6],
                "status": row[7],
                "created_at": row[8].strftime("%Y-%m-%d %H:%M:%S") if isinstance(row[8], datetime) else row[8]
            })
            
        return donations
    except Exception as e:
        logger.error(f"Error fetching donations: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch donations")
    finally:
        if conn:
            conn.close()
            
@app.delete("/donations/{donation_id}")
def delete_donation(donation_id: int):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # First get the donation to check if it exists
        cursor.execute('SELECT * FROM transactions WHERE id = %s', (donation_id,))
        donation = cursor.fetchone()
        if not donation:
            raise HTTPException(status_code=404, detail="Donation not found")
        
        # Delete the donation
        cursor.execute('DELETE FROM transactions WHERE id = %s', (donation_id,))
        
        # Create a notification about the deletion
        notification_message = f"Donation record {donation_id} deleted"
        cursor.execute('''
            INSERT INTO notifications (message, type)
            VALUES (%s, %s)
        ''', (notification_message, "donation_deletion"))
        
        conn.commit()
        return {"message": "Donation deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting donation: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete donation")
    finally:
        if conn:
            conn.close()

@app.get("/donors/", response_model=List[Donor])
def get_donors(search: Optional[str] = None):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Use DISTINCT ON to ensure unique donors
        if search:
            cursor.execute('''
                SELECT DISTINCT ON (id) id, name, email, phone, address, donor_type, notes, category, created_at
                FROM donors
                WHERE name ILIKE %s OR email ILIKE %s OR phone ILIKE %s
                ORDER BY id, name
            ''', (f"%{search}%", f"%{search}%", f"%{search}%"))
        else:
            cursor.execute('''
                SELECT DISTINCT ON (id) id, name, email, phone, address, donor_type, notes, category, created_at
                FROM donors
                ORDER BY id, name
            ''')
        
        donors = []
        for row in cursor.fetchall():
            donors.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "phone": row[3],
                "address": row[4],
                "donor_type": row[5],
                "notes": row[6],
                "category": row[7] if len(row) > 7 else "one-time",
                "created_at": row[8] if len(row) > 8 else None
            })
            
        return donors
    except Exception as e:
        logger.error(f"Error fetching donors: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch donors")
    finally:
        if conn:
            conn.close()
            
@app.get("/donors/{donor_id}", response_model=Donor)
def get_donor(donor_id: int):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, email, phone, address, donor_type, notes, created_at
            FROM donors
            WHERE id = %s
        ''', (donor_id,))
        
        donor = cursor.fetchone()
        if not donor:
            raise HTTPException(status_code=404, detail="Donor not found")
            
        return {
            "id": donor[0],
            "name": donor[1],
            "email": donor[2],
            "phone": donor[3],
            "address": donor[4],
            "donor_type": donor[5],
            "notes": donor[6],
            "created_at": donor[7]
        }
    except Exception as e:
        logger.error(f"Error fetching donor: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch donor")
    finally:
        if conn:
            conn.close()

@app.put("/donors/{donor_id}", response_model=Donor)
def update_donor(donor_id: int, donor: Donor):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE donors
            SET name = %s, email = %s, phone = %s, address = %s, 
                donor_type = %s, notes = %s
            WHERE id = %s
            RETURNING id, name, email, phone, address, donor_type, notes, created_at
        ''', (
            donor.name, donor.email, donor.phone, donor.address,
            donor.donor_type, donor.notes, donor_id
        ))
        
        updated_donor = cursor.fetchone()
        if not updated_donor:
            raise HTTPException(status_code=404, detail="Donor not found")
            
        conn.commit()
        return {
            "id": updated_donor[0],
            "name": updated_donor[1],
            "email": updated_donor[2],
            "phone": updated_donor[3],
            "address": updated_donor[4],
            "donor_type": updated_donor[5],
            "notes": updated_donor[6],
            "created_at": updated_donor[7]
        }
    except Exception as e:
        logger.error(f"Error updating donor: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to update donor")
    finally:
        if conn:
            conn.close()

@app.delete("/donors/{donor_id}")
def delete_donor(donor_id: int):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # First check if donor exists
        cursor.execute('SELECT id FROM donors WHERE id = %s', (donor_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Donor not found")
            
        # Delete donor
        cursor.execute('DELETE FROM donors WHERE id = %s', (donor_id,))
        conn.commit()
        
        return {"message": "Donor deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting donor: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete donor")
    finally:
        if conn:
            conn.close()

@app.get("/donors/{donor_id}/donations")
def get_donor_donations(donor_id: int):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # First check if donor exists
        cursor.execute('SELECT name FROM donors WHERE id = %s', (donor_id,))
        donor = cursor.fetchone()
        if not donor:
            raise HTTPException(status_code=404, detail="Donor not found")
            
        donor_name = donor[0]
        
        # Get all donations for this donor
        cursor.execute('''
            SELECT id, date, amount, purpose 
            FROM transactions 
            WHERE type = 'deposit' AND purpose LIKE %s
            ORDER BY date DESC
        ''', (f"Donation from {donor_name}%",))
        
        donations = []
        for row in cursor.fetchall():
            # Parse the purpose field to extract project
            purpose_parts = row[3].split(' for ')
            project = purpose_parts[1] if len(purpose_parts) > 1 else 'general fund'
            
            donations.append({
                "id": row[0],
                "date": row[1].strftime("%Y-%m-%d") if isinstance(row[1], datetime) else row[1],
                "amount": row[2],
                "project": project,
                "status": "completed"
            })
            
        return {
            "donor_id": donor_id,
            "donor_name": donor_name,
            "donations": donations,
            "total_donations": sum(d['amount'] for d in donations),
            "donation_count": len(donations)
        }
    except Exception as e:
        logger.error(f"Error fetching donor donations: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch donor donations")
    finally:
        if conn:
            conn.close()

@app.post("/donors/", response_model=Donor)
def create_donor(donor: DonorCreate):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Validate donor type and category
        if donor.donor_type not in ["individual", "corporate", "foundation", "other"]:
            raise HTTPException(status_code=400, detail="Invalid donor type")
            
        if donor.category not in ["regular", "one-time"]:
            raise HTTPException(status_code=400, detail="Invalid donor category")
        
        cursor.execute('''
            INSERT INTO donors (name, email, phone, address, donor_type, notes, category)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, name, email, phone, address, donor_type, notes, category, created_at
        ''', (
            donor.name, donor.email, donor.phone, donor.address, 
            donor.donor_type, donor.notes, donor.category
        ))
        
        new_donor = cursor.fetchone()
        conn.commit()
        
        return {
            "id": new_donor[0],
            "name": new_donor[1],
            "email": new_donor[2],
            "phone": new_donor[3],
            "address": new_donor[4],
            "donor_type": new_donor[5],
            "notes": new_donor[6],
            "category": new_donor[7],
            "created_at": new_donor[8]
        }
    except Exception as e:
        logger.error(f"Error creating donor: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@app.put("/donors/{donor_id}", response_model=Donor)
def update_donor(donor_id: int, donor: DonorCreate):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Validate donor type and category
        if donor.donor_type not in ["individual", "corporate", "foundation", "other"]:
            raise HTTPException(status_code=400, detail="Invalid donor type")
            
        if donor.category not in ["regular", "one-time"]:
            raise HTTPException(status_code=400, detail="Invalid donor category")
        
        cursor.execute('''
            UPDATE donors
            SET name = %s, email = %s, phone = %s, address = %s, 
                donor_type = %s, notes = %s, category = %s
            WHERE id = %s
            RETURNING id, name, email, phone, address, donor_type, notes, category, created_at
        ''', (
            donor.name, donor.email, donor.phone, donor.address,
            donor.donor_type, donor.notes, donor.category, donor_id
        ))
        
        updated_donor = cursor.fetchone()
        if not updated_donor:
            raise HTTPException(status_code=404, detail="Donor not found")
            
        conn.commit()
        return {
            "id": updated_donor[0],
            "name": updated_donor[1],
            "email": updated_donor[2],
            "phone": updated_donor[3],
            "address": updated_donor[4],
            "donor_type": updated_donor[5],
            "notes": updated_donor[6],
            "category": updated_donor[7],
            "created_at": updated_donor[8]
        }
    except Exception as e:
        logger.error(f"Error updating donor: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@app.get("/donors/stats/")
def get_donor_stats():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get donation statistics grouped by donor
        cursor.execute('''
            SELECT d.id as donor_id, d.name, 
                   COUNT(t.id) as donation_count,
                   SUM(t.amount) as total_donated,
                   MIN(t.date) as first_donation,
                   MAX(t.date) as last_donation
            FROM donors d
            LEFT JOIN transactions t ON t.purpose LIKE 'Donation from ' || d.name || '%' AND t.type = 'deposit'
            GROUP BY d.id, d.name
        ''')
        
        stats = {}
        for row in cursor.fetchall():
            stats[row[0]] = {  # donor_id as key
                "name": row[1],
                "donation_count": row[2] or 0,
                "total_donated": float(row[3] or 0),
                "first_donation": row[4].strftime("%Y-%m-%d") if row[4] else None,
                "last_donation": row[5].strftime("%Y-%m-%d") if row[5] else None
            }
            
        return {"donor_stats": stats}
    except Exception as e:
        logger.error(f"Error fetching donor stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch donor stats")
    finally:
        if conn:
            conn.close()

@app.post("/projects/", response_model=Project)
def create_project(project: ProjectCreate):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO projects (name, description, start_date, end_date, budget, funding_source, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, name, description, start_date, end_date, budget, funding_source, status, created_at
        ''', (
            project.name,
            project.description,
            project.start_date,
            project.end_date,
            project.budget,
            project.funding_source,
            project.status
        ))
        
        new_project = cursor.fetchone()
        conn.commit()
        
        return {
            "id": new_project[0],
            "name": new_project[1],
            "description": new_project[2],
            "start_date": new_project[3].strftime("%Y-%m-%d"),
            "end_date": new_project[4].strftime("%Y-%m-%d"),
            "budget": new_project[5],
            "funding_source": new_project[6],
            "status": new_project[7],
            "created_at": new_project[8]
        }
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@app.get("/projects/")
def get_projects():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, description, start_date, end_date, budget, funding_source, status, created_at
            FROM projects
            ORDER BY created_at DESC
        ''')
        
        projects = []
        for row in cursor.fetchall():
            projects.append({
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "start_date": row[3].strftime("%Y-%m-%d"),
                "end_date": row[4].strftime("%Y-%m-%d"),
                "budget": row[5],
                "funding_source": row[6],
                "status": row[7],
                "created_at": row[8].strftime("%Y-%m-%d %H:%M:%S")
            })
            
        return {"projects": projects}
    except Exception as e:
        logger.error(f"Error fetching projects: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch projects")
    finally:
        if conn:
            conn.close()

@app.get("/projects/{project_id}")
def get_project(project_id: int):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, description, start_date, end_date, budget, funding_source, status, created_at
            FROM projects
            WHERE id = %s
        ''', (project_id,))
        
        project = cursor.fetchone()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        return {
            "id": project[0],
            "name": project[1],
            "description": project[2],
            "start_date": project[3].strftime("%Y-%m-%d"),
            "end_date": project[4].strftime("%Y-%m-%d"),
            "budget": project[5],
            "funding_source": project[6],
            "status": project[7],
            "created_at": project[8].strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        logger.error(f"Error fetching project: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch project")
    finally:
        if conn:
            conn.close()

@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM projects WHERE id = %s', (project_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Project not found")
            
        cursor.execute('DELETE FROM projects WHERE id = %s', (project_id,))
        conn.commit()
        
        return {"message": "Project deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting project: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete project")
    finally:
        if conn:
            conn.close()

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
