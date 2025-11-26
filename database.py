import sqlite3
import pandas as pd
from datetime import datetime
import os

def init_database():
    """Initialize the database and create tables if they don't exist"""
    conn = sqlite3.connect('pricing.db')
    c = conn.cursor()
    
    # ONLY create table if it doesn't exist - NO DROP TABLE
    c.execute('''
        CREATE TABLE IF NOT EXISTS pricing_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_cliente TEXT NOT NULL,
            id_cliente TEXT NOT NULL,
            comision_seguro REAL NOT NULL,
            reaseguro_proporcional REAL NOT NULL,
            comision_reaseguro REAL NOT NULL,
            nit_cc TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database checked/initialized successfully")

def save_record(record_data):
    """Save a new record to the database"""
    conn = sqlite3.connect('pricing.db')
    c = conn.cursor()
    
    # Insert record
    c.execute('''
        INSERT INTO pricing_records 
        (nombre_cliente, id_cliente, comision_seguro, reaseguro_proporcional, comision_reaseguro, nit_cc)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        record_data['nombre_cliente'],
        record_data['id_cliente'],
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
    conn = sqlite3.connect('pricing.db')
    c = conn.cursor()
    
    c.execute('''
        SELECT * FROM pricing_records WHERE id = ?
    ''', (record_id,))
    
    record = c.fetchone()
    conn.close()
    
    if record:
        columns = ['id', 'nombre_cliente', 'id_cliente', 'comision_seguro', 'reaseguro_proporcional', 
                  'comision_reaseguro', 'nit_cc', 'created_date', 'last_modified']
        return dict(zip(columns, record))
    return None

def find_record_by_nombre(nombre_cliente):
    """Find records by Nombre Cliente (partial match)"""
    conn = sqlite3.connect('pricing.db')
    c = conn.cursor()
    
    c.execute('''
        SELECT * FROM pricing_records WHERE nombre_cliente LIKE ? ORDER BY id DESC
    ''', (f'%{nombre_cliente}%',))
    
    records = c.fetchall()
    conn.close()
    
    if records:
        columns = ['id', 'nombre_cliente', 'id_cliente', 'comision_seguro', 'reaseguro_proporcional', 
                  'comision_reaseguro', 'nit_cc', 'created_date', 'last_modified']
        return [dict(zip(columns, record)) for record in records]
    return None

def find_record_by_id_cliente(id_cliente):
    """Find records by ID Cliente (exact match)"""
    conn = sqlite3.connect('pricing.db')
    c = conn.cursor()
    
    c.execute('''
        SELECT * FROM pricing_records WHERE id_cliente = ? ORDER BY id DESC
    ''', (id_cliente,))
    
    records = c.fetchall()
    conn.close()
    
    if records:
        columns = ['id', 'nombre_cliente', 'id_cliente', 'comision_seguro', 'reaseguro_proporcional', 
                  'comision_reaseguro', 'nit_cc', 'created_date', 'last_modified']
        return [dict(zip(columns, record)) for record in records]
    return None

def update_record(record_id, record_data):
    """Update an existing record in the database"""
    conn = sqlite3.connect('pricing.db')
    c = conn.cursor()
    
    try:
        # Update record
        c.execute('''
            UPDATE pricing_records 
            SET nombre_cliente = ?, 
                id_cliente = ?, 
                comision_seguro = ?, 
                reaseguro_proporcional = ?, 
                comision_reaseguro = ?, 
                nit_cc = ?,
                last_modified = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            record_data['nombre_cliente'],
            record_data['id_cliente'],
            record_data['comision_seguro'],
            record_data['reaseguro_proporcional'],
            record_data['comision_reaseguro'],
            record_data.get('nit_cc', ''),
            record_id
        ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating record: {e}")
        conn.close()
        return False

def get_all_records():
    """Get all records for display"""
    conn = sqlite3.connect('pricing.db')
    df = pd.read_sql('SELECT * FROM pricing_records ORDER BY created_date DESC', conn)
    conn.close()
    return df

# Remove the __main__ section to prevent recreation on import
