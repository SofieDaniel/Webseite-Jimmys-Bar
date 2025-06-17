import React, { useState, useEffect } from 'react';

const MaintenanceSection = () => {
  const [maintenanceMode, setMaintenanceMode] = useState(false);
  const [maintenanceMessage, setMaintenanceMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    loadMaintenanceStatus();
  }, []);

  const loadMaintenanceStatus = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/maintenance`);
      if (response.ok) {
        const data = await response.json();
        setMaintenanceMode(data.maintenance_mode || false);
        setMaintenanceMessage(data.message || 'Die Website befindet sich im Wartungsmodus. Bitte versuchen Sie es später erneut.');
      }
    } catch (error) {
      console.error('Error loading maintenance status:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleMaintenanceMode = async () => {
    setSaving(true);
    setMessage('');

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/maintenance`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('adminToken')}`
        },
        body: JSON.stringify({
          maintenance_mode: !maintenanceMode,
          message: maintenanceMessage
        })
      });

      if (response.ok) {
        setMaintenanceMode(!maintenanceMode);
        setMessage(`Wartungsmodus ${!maintenanceMode ? 'aktiviert' : 'deaktiviert'}`);
      } else {
        setMessage('Fehler beim Ändern des Wartungsmodus');
      }
    } catch (error) {
      setMessage('Verbindungsfehler');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900">Wartungsmodus</h2>
        <p className="text-gray-600 mt-2">Aktivieren Sie den Wartungsmodus, um die Website für Besucher zu sperren</p>
      </div>

      {message && (
        <div className={`mb-6 p-4 rounded-lg ${
          message.includes('aktiviert') || message.includes('deaktiviert')
            ? 'bg-green-100 text-green-700 border border-green-200' 
            : 'bg-red-100 text-red-700 border border-red-200'
        }`}>
          {message}
        </div>
      )}

      <div className="bg-white rounded-lg shadow p-6">
        <div className="space-y-6">
          {/* Current Status */}
          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div>
              <h3 className="text-lg font-medium text-gray-900">Aktueller Status</h3>
              <p className="text-sm text-gray-600">
                Die Website ist derzeit {maintenanceMode ? 'im Wartungsmodus' : 'online'}
              </p>
            </div>
            <div className={`px-4 py-2 rounded-full text-sm font-medium ${
              maintenanceMode 
                ? 'bg-red-100 text-red-800' 
                : 'bg-green-100 text-green-800'
            }`}>
              {maintenanceMode ? '🔴 Wartung aktiv' : '🟢 Online'}
            </div>
          </div>

          {/* Maintenance Message */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Wartungsnachricht für Besucher
            </label>
            <textarea
              value={maintenanceMessage}
              onChange={(e) => setMaintenanceMessage(e.target.value)}
              rows={4}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Diese Nachricht wird Besuchern angezeigt, wenn der Wartungsmodus aktiv ist."
            />
          </div>

          {/* Toggle Button */}
          <div className="flex justify-between items-center pt-6 border-t">
            <div className="text-sm text-gray-500">
              <strong>Wichtig:</strong> Im Wartungsmodus ist die Website nur für Administratoren zugänglich.
            </div>
            <button
              onClick={toggleMaintenanceMode}
              disabled={saving}
              className={`px-6 py-3 rounded-lg font-medium transition-colors ${
                maintenanceMode 
                  ? 'bg-green-600 text-white hover:bg-green-700' 
                  : 'bg-red-600 text-white hover:bg-red-700'
              } disabled:opacity-50`}
            >
              {saving 
                ? 'Wird geändert...' 
                : maintenanceMode 
                  ? 'Wartungsmodus deaktivieren' 
                  : 'Wartungsmodus aktivieren'
              }
            </button>
          </div>

          {/* Info Box */}
          <div className="bg-blue-50 rounded-lg p-4">
            <h4 className="font-medium text-blue-900 mb-2">ℹ️ Hinweise zum Wartungsmodus</h4>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Normale Besucher sehen nur die Wartungsnachricht</li>
              <li>• Administratoren können weiterhin auf die Website zugreifen</li>
              <li>• Das Admin-Panel bleibt immer erreichbar</li>
              <li>• Suchmaschinen erhalten einen 503-Status</li>
            </ul>
          </div>

          {/* Preview */}
          {maintenanceMode && (
            <div className="border border-yellow-200 rounded-lg p-4 bg-yellow-50">
              <h4 className="font-medium text-yellow-800 mb-2">🔍 Vorschau der Wartungsseite</h4>
              <div className="bg-white border rounded p-4 text-center">
                <div className="text-4xl mb-4">🔧</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Wartungsmodus</h3>
                <p className="text-gray-600">{maintenanceMessage}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MaintenanceSection;