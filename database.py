import sqlite3
import pandas as pd
from datetime import datetime

# Use in-memory database for Streamlit Cloud
def get_connection():
    """Get database connection - use in-memory for Streamlit Cloud"""
    return sqlite3.connect(':memory:', check_same_thread=False)

def init_database():
    """Initialize the database and create tables if they don't exist"""
    conn = get_connection()
    c = conn.cursor()
    
    # Create table with new schema including 'ano'
    c.execute('''
        CREATE TABLE IF NOT EXISTS pricing_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_cliente TEXT NOT NULL,
            id_cliente TEXT NOT NULL,
            ano INTEGER NOT NULL,
            comision_seguro REAL NOT NULL,
            reaseguro_proporcional REAL NOT NULL,
            comision_reaseguro REAL NOT NULL,
            nit_cc TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("In-memory database initialized successfully")

def save_record(record_data):
    """Save a new record to the database"""
    conn = get_connection()
    c = conn.cursor()
    
    # Insert record
    c.execute('''
        INSERT INTO pricing_records 
        (nombre_cliente, id_cliente, ano, comision_seguro, reaseguro_proporcional, comision_reaseguro, nit_cc)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        record_data['nombre_cliente'],
        record_data['id_cliente'],
        record_data['ano'],
        record_data['comision_seguro'],
        record_data['reaseguro_proporcional'],
        record_data['comision_reaseguro'],
        record_data.get('nit_cc', '')
    ))
    
    conn.commit()
    record_id = c.lastrowid
    conn.close()
    
    return record_id, 0

def find_record(record_id):
    """Find a record by ID"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        SELECT * FROM pricing_records WHERE id = ?
    ''', (record_id,))
    
    record = c.fetchone()
    conn.close()
    
    if record:
        columns = ['id', 'nombre_cliente', 'id_cliente', 'ano', 'comision_seguro', 'reaseguro_proporcional', 
                  'comision_reaseguro', 'nit_cc', 'created_date']
        return dict(zip(columns, record))
    return None

def get_all_records():
    """Get all records for display"""
    conn = get_connection()
    df = pd.read_sql('SELECT * FROM pricing_records ORDER BY created_date DESC', conn)
    conn.close()
    return df
