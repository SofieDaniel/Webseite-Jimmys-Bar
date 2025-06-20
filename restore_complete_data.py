#!/usr/bin/env python3
import asyncio
import aiomysql
import json

async def restore_all_data():
    """Restore all data including the menu items"""
    
    connection = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='jimmy_user',
        password='jimmy2024_db',
        db='jimmys_tapas_bar',
        autocommit=True
    )
    
    cursor = await connection.cursor()
    
    try:
        # Create missing tables
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS standorte_enhanced (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                data JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Standorte enhanced table created")
        
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS bewertungen_page (
                id VARCHAR(36) PRIMARY KEY,
                title VARCHAR(255),
                subtitle VARCHAR(255),
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Bewertungen page table created")
        
        # Insert default standorte data
        import uuid
        standorte_id = str(uuid.uuid4())
        standorte_data = {
            "locations": [
                {
                    "name": "Jimmy's Tapas Bar Hauptstandort",
                    "address": "Strandpromenade 15, 18374 Zingst",
                    "phone": "+49 38232 15678",
                    "hours": "Mo-So: 11:00-23:00",
                    "features": ["Meerblick", "Terrasse", "Parkplätze"],
                    "coordinates": {"lat": 54.4389, "lng": 12.6806}
                }
            ]
        }
        
        await cursor.execute('''
            INSERT IGNORE INTO standorte_enhanced (id, name, data) 
            VALUES (%s, 'main_locations', %s)
        ''', (standorte_id, json.dumps(standorte_data)))
        print("✅ Default locations data inserted")
        
        # Insert default bewertungen page
        bewertungen_id = str(uuid.uuid4())
        await cursor.execute('''
            INSERT IGNORE INTO bewertungen_page (id, title, subtitle, description) 
            VALUES (%s, %s, %s, %s)
        ''', (
            bewertungen_id,
            "Bewertungen",
            "Was unsere Gäste sagen",
            "Lesen Sie authentische Bewertungen unserer Gäste"
        ))
        print("✅ Default bewertungen page created")
        
        print("\n🎉 Database restoration completed!")
        
    except Exception as e:
        print(f"❌ Error restoring data: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    asyncio.run(restore_all_data())