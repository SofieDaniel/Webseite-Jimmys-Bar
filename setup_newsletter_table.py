#!/usr/bin/env python3
import asyncio
import aiomysql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

async def setup_newsletter_table():
    conn = await aiomysql.connect(
        host=os.environ['MYSQL_HOST'],
        port=int(os.environ['MYSQL_PORT']),
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        db=os.environ['MYSQL_DATABASE'],
        charset='utf8mb4',
        autocommit=True
    )
    
    try:
        cursor = await conn.cursor()
        
        # Create newsletter table
        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS newsletter_subscribers (
                id VARCHAR(36) PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(255),
                subscribed BOOLEAN DEFAULT TRUE,
                subscribe_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                unsubscribe_date TIMESTAMP NULL
            )
        """)
        
        print("✅ Newsletter table created successfully")
        
    finally:
        conn.close()

if __name__ == "__main__":
    asyncio.run(setup_newsletter_table())