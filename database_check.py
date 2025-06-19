#!/usr/bin/env python3
"""
Umfassende Datenbankprüfung für Jimmy's Tapas Bar
Prüft alle Tabellen, Strukturen und Datenintegrität
"""

import asyncio
import aiomysql
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

# Database connection parameters
DB_CONFIG = {
    'host': os.environ['MYSQL_HOST'],
    'port': int(os.environ['MYSQL_PORT']),
    'user': os.environ['MYSQL_USER'],
    'password': os.environ['MYSQL_PASSWORD'],
    'db': os.environ['MYSQL_DATABASE'],
    'charset': 'utf8mb4'
}

async def check_database():
    """Führt eine umfassende Datenbankprüfung durch"""
    
    print("=" * 80)
    print("🔍 UMFASSENDE DATENBANKPRÜFUNG - JIMMY'S TAPAS BAR")
    print("=" * 80)
    print(f"Zeitpunkt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Datenbank: {DB_CONFIG['db']}")
    print(f"Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print()

    try:
        # Verbindung zur Datenbank herstellen
        connection = await aiomysql.connect(**DB_CONFIG)
        cursor = await connection.cursor(aiomysql.DictCursor)
        
        print("✅ Datenbankverbindung erfolgreich")
        print()
        
        # 1. Alle Tabellen auflisten
        print("📋 1. VORHANDENE TABELLEN")
        print("-" * 40)
        await cursor.execute("SHOW TABLES")
        tables = await cursor.fetchall()
        table_names = [list(table.values())[0] for table in tables]
        
        print(f"Anzahl Tabellen: {len(table_names)}")
        for i, table_name in enumerate(table_names, 1):
            print(f"{i:2d}. {table_name}")
        print()
        
        # 2. Tabellenstrukturen prüfen
        print("🏗️  2. TABELLENSTRUKTUREN")
        print("-" * 40)
        
        table_info = {}
        for table_name in table_names:
            await cursor.execute(f"DESCRIBE {table_name}")
            columns = await cursor.fetchall()
            
            await cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            count = await cursor.fetchone()
            row_count = count['count']
            
            table_info[table_name] = {
                'columns': columns,
                'row_count': row_count
            }
            
            print(f"📊 Tabelle: {table_name} ({row_count} Datensätze)")
            for col in columns:
                null_status = "NULL" if col['Null'] == 'YES' else "NOT NULL"
                default = f"DEFAULT: {col['Default']}" if col['Default'] else ""
                print(f"   - {col['Field']}: {col['Type']} {null_status} {default}")
            print()
        
        # 3. Datenintegrität prüfen
        print("🔍 3. DATENINTEGRITÄT & SAMPLE-DATEN")
        print("-" * 40)
        
        # Wichtige Tabellen mit Sample-Daten prüfen
        important_tables = [
            'users', 'menu_items', 'reviews', 'contact_messages',
            'delivery_info', 'standorte_enhanced', 'bewertungen_page'
        ]
        
        for table_name in important_tables:
            if table_name in table_names:
                await cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
                count = await cursor.fetchone()
                row_count = count['count']
                
                print(f"📋 {table_name}: {row_count} Datensätze")
                
                if row_count > 0:
                    # Sample-Daten anzeigen (erste 3 Datensätze)
                    await cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                    sample_data = await cursor.fetchall()
                    
                    for i, row in enumerate(sample_data, 1):
                        print(f"   Sample {i}:")
                        for key, value in row.items():
                            if isinstance(value, str) and len(value) > 50:
                                value = value[:47] + "..."
                            print(f"     {key}: {value}")
                        print()
                else:
                    print("   ⚠️  Keine Daten vorhanden")
                print()
        
        # 4. Spezifische Prüfungen
        print("🔧 4. SPEZIFISCHE PRÜFUNGEN")
        print("-" * 40)
        
        # Admin-Benutzer prüfen
        await cursor.execute("SELECT COUNT(*) as count FROM users WHERE role = 'admin'")
        admin_count = await cursor.fetchone()
        print(f"👤 Admin-Benutzer: {admin_count['count']}")
        
        if admin_count['count'] > 0:
            await cursor.execute("SELECT username, email, is_active FROM users WHERE role = 'admin'")
            admins = await cursor.fetchall()
            for admin in admins:
                status = "✅ Aktiv" if admin['is_active'] else "❌ Deaktiviert"
                print(f"   - {admin['username']} ({admin['email']}) - {status}")
        print()
        
        # Delivery-Info prüfen
        if 'delivery_info' in table_names:
            await cursor.execute("SELECT * FROM delivery_info WHERE is_active = TRUE")
            delivery = await cursor.fetchone()
            if delivery:
                print("🚚 Lieferinformationen:")
                print(f"   - Lieferzeit: {delivery['delivery_time_min']}-{delivery['delivery_time_max']} Min")
                print(f"   - Mindestbestellwert: {delivery['minimum_order_value']}€")
                print(f"   - Liefergebühr: {delivery['delivery_fee']}€")
                print(f"   - Aktiv: {'✅' if delivery['is_active'] else '❌'}")
            else:
                print("⚠️  Keine aktiven Lieferinformationen")
        print()
        
        # Menu-Items prüfen
        if 'menu_items' in table_names:
            await cursor.execute("SELECT COUNT(*) as total, COUNT(CASE WHEN is_active = TRUE THEN 1 END) as active FROM menu_items")
            menu_stats = await cursor.fetchone()
            print(f"🍽️  Speisekarte: {menu_stats['active']}/{menu_stats['total']} aktive Gerichte")
            
            await cursor.execute("SELECT category, COUNT(*) as count FROM menu_items WHERE is_active = TRUE GROUP BY category")
            categories = await cursor.fetchall()
            for cat in categories:
                print(f"   - {cat['category']}: {cat['count']} Gerichte")
        print()
        
        # Reviews prüfen
        if 'reviews' in table_names:
            await cursor.execute("SELECT COUNT(*) as total, COUNT(CASE WHEN is_approved = TRUE THEN 1 END) as approved FROM reviews")
            review_stats = await cursor.fetchone()
            print(f"⭐ Bewertungen: {review_stats['approved']}/{review_stats['total']} genehmigt")
            
            await cursor.execute("SELECT AVG(rating) as avg_rating FROM reviews WHERE is_approved = TRUE")
            avg_rating = await cursor.fetchone()
            if avg_rating['avg_rating']:
                print(f"   - Durchschnittsbewertung: {avg_rating['avg_rating']:.1f}/5")
        print()
        
        # 5. Potenzielle Probleme identifizieren
        print("⚠️  5. POTENZIELLE PROBLEME")
        print("-" * 40)
        
        problems = []
        
        # Prüfen auf leere wichtige Tabellen
        if table_info.get('users', {}).get('row_count', 0) == 0:
            problems.append("❌ Keine Benutzer in der Datenbank")
        
        if table_info.get('delivery_info', {}).get('row_count', 0) == 0:
            problems.append("⚠️  Keine Lieferinformationen konfiguriert")
        
        # Prüfen auf nicht genehmigte Reviews
        if 'reviews' in table_names:
            await cursor.execute("SELECT COUNT(*) as count FROM reviews WHERE is_approved = FALSE")
            pending_reviews = await cursor.fetchone()
            if pending_reviews['count'] > 0:
                problems.append(f"📝 {pending_reviews['count']} ausstehende Bewertungen zur Genehmigung")
        
        # Prüfen auf ungelesene Kontaktnachrichten
        if 'contact_messages' in table_names:
            await cursor.execute("SELECT COUNT(*) as count FROM contact_messages WHERE is_read = FALSE")
            unread_messages = await cursor.fetchone()
            if unread_messages['count'] > 0:
                problems.append(f"📧 {unread_messages['count']} ungelesene Kontaktnachrichten")
        
        if problems:
            for problem in problems:
                print(problem)
        else:
            print("✅ Keine kritischen Probleme gefunden")
        
        print()
        
        # 6. Zusammenfassung
        print("📊 6. ZUSAMMENFASSUNG")
        print("-" * 40)
        
        total_records = sum(info['row_count'] for info in table_info.values())
        print(f"📋 Gesamtanzahl Tabellen: {len(table_names)}")
        print(f"📊 Gesamtanzahl Datensätze: {total_records}")
        print(f"👤 Benutzer: {table_info.get('users', {}).get('row_count', 0)}")
        print(f"🍽️  Speisekarte: {table_info.get('menu_items', {}).get('row_count', 0)}")
        print(f"⭐ Bewertungen: {table_info.get('reviews', {}).get('row_count', 0)}")
        print(f"📧 Kontaktnachrichten: {table_info.get('contact_messages', {}).get('row_count', 0)}")
        
        print()
        print("=" * 80)
        print("✅ DATENBANKPRÜFUNG ABGESCHLOSSEN")
        print("=" * 80)
        
        await cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Fehler bei der Datenbankprüfung: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_database())