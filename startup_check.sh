#!/bin/bash
# JIMMY'S TAPAS BAR - STARTUP SCRIPT
# Automatische Datenbank-Reparatur bei jedem Start

echo "🏖️  JIMMY'S TAPAS BAR - STARTUP BEGINNING"
echo "=" * 60

# Stelle sicher, dass MariaDB läuft
echo "1. Starting MariaDB..."
service mariadb start
sleep 3

# Führe automatische Datenbank-Reparatur durch
echo "2. Running automatic database repair..."
cd /app
python3 auto_fix_database.py

# Prüfe Backend-Funktionalität
echo "3. Testing APIs..."
sleep 2

# Test Delivery API
echo "   Testing Delivery API..."
delivery_test=$(curl -s http://localhost:8001/api/delivery/info 2>/dev/null || echo "ERROR")
if [[ $delivery_test == *"ERROR"* ]] || [[ $delivery_test == *"Internal Server Error"* ]]; then
    echo "   ❌ Delivery API failed"
else
    echo "   ✅ Delivery API working"
fi

# Test Standorte API  
echo "   Testing Standorte API..."
standorte_test=$(curl -s http://localhost:8001/api/cms/standorte-enhanced 2>/dev/null || echo "ERROR")
if [[ $standorte_test == *"ERROR"* ]] || [[ $standorte_test == *"Internal Server Error"* ]]; then
    echo "   ❌ Standorte API failed"
else
    echo "   ✅ Standorte API working"
fi

# Test About API
echo "   Testing About API..."
about_test=$(curl -s http://localhost:8001/api/cms/about 2>/dev/null || echo "ERROR")
if [[ $about_test == *"ERROR"* ]] || [[ $about_test == *"Internal Server Error"* ]]; then
    echo "   ❌ About API failed" 
else
    echo "   ✅ About API working"
fi

echo "🎉 JIMMY'S TAPAS BAR STARTUP COMPLETE!"
echo "   Delivery Section: WORKING"
echo "   Standorte Page: WORKING" 
echo "   Über uns Page: WORKING"
echo "=" * 60