import mysql.connector
from config import DB_CONFIG

def connect_db():
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        return db, db.cursor()
    except mysql.connector.Error as e:
        print(f"❌ Database connection error: {e}")
        raise

def setup_orders_table(cursor):
    try:
        cursor.execute("DROP TABLE IF EXISTS orders_order")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders_order (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email_date VARCHAR(255),
                sender VARCHAR(255),
                Order_No VARCHAR(255),
                Customer_Name TEXT,
                Mobile_No VARCHAR(20),
                Item_Details LONGTEXT,
                Item_Description LONGTEXT,
                Sub_Total DECIMAL(10, 2),
                Delivery_Charges DECIMAL(10, 2),
                GST DECIMAL(10, 2),
                Grand_Total DECIMAL(10, 2),
                Pay_Mode VARCHAR(100),
                Delivery_Date VARCHAR(255),
                Station VARCHAR(100),
                Train_No_Name VARCHAR(50),
                Coach VARCHAR(50),
                subject TEXT
            )
        """)
    except mysql.connector.Error as e:
        print(f"❌ Table setup error: {e}")
        raise
