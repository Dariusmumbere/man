from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import psycopg2
import logging
import json
from typing import List, Optional
from datetime import date,datetime
from typing import Dict

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

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle the message (you can parse JSON here if needed)
            await manager.broadcast(f"User {user_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        await manager.broadcast(f"User {user_id} left the chat")

    
# Initialize database tables
def init_db():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS diary_entries')
        # Drop and recreate tables to ensure the correct schema
        
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

        # For services: quantity * unit_price * 0.7 (since services have a 30% profit margin)
        cursor.execute('''
            SELECT SUM((item->>'quantity')::int * (item->>'unit_price')::float * 0.7)
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

        # For services: quantity * unit_price * 0.7 (since services have a 30% profit margin)
        cursor.execute('''
            SELECT SUM((item->>'quantity')::int * (item->>'unit_price')::float * 0.7)
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

            
# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
