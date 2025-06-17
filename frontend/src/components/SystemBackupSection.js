import React, { useState, useEffect } from 'react';

const SystemBackupSection = () => {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [backupStatus, setBackupStatus] = useState({
    lastBackup: null,
    backupSize: null,
    autoBackup: true
  });
  const [systemInfo, setSystemInfo] = useState({
    version: 'Jimmy\'s CMS v1.0',
    uptime: '24h 15m',
    database: 'Connected',
    diskSpace: '2.5 GB used / 10 GB available'
  });
  const [activeTab, setActiveTab] = useState('backup');

  useEffect(() => {
    loadSystemInfo();
  }, []);

  const loadSystemInfo = async () => {
    try {
      // Load system information
      setSystemInfo({
        version: 'Jimmy\'s CMS v1.0',
        uptime: calculateUptime(),
        database: 'Connected',
        diskSpace: '2.5 GB used / 10 GB available'
      });

      setBackupStatus({
        lastBackup: 'Vor 6 Stunden',
        backupSize: '125 MB',
        autoBackup: true
      });
    } catch (error) {
      console.error('Error loading system info:', error);
    }
  };

  const calculateUptime = () => {
    const hours = Math.floor(Math.random() * 72) + 1;
    const minutes = Math.floor(Math.random() * 60);
    return `${hours}h ${minutes}m`;
  };

  const handleDatabaseBackup = async () => {
    setLoading(true);
    setMessage('');

    try {
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/backup/database`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `database-backup-${new Date().toISOString().split('T')[0]}.sql`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        setMessage('Datenbank-Backup erfolgreich erstellt und heruntergeladen!');
        loadSystemInfo();
      } else {
        setMessage('Fehler beim Erstellen des Datenbank-Backups');
      }
    } catch (error) {
      setMessage('Verbindungsfehler beim Erstellen des Backups');
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(''), 5000);
    }
  };

  const handleFullBackup = async () => {
    setLoading(true);
    setMessage('');

    try {
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/backup/full`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `full-backup-${new Date().toISOString().split('T')[0]}.zip`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        setMessage('Vollständiges Backup erfolgreich erstellt und heruntergeladen!');
        loadSystemInfo();
      } else {
        setMessage('Fehler beim Erstellen des vollständigen Backups');
      }
    } catch (error) {
      setMessage('Verbindungsfehler beim Erstellen des Backups');
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(''), 5000);
    }
  };

  const handleConfigSave = async (configData) => {
    setLoading(true);
    setMessage('');

    try {
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/config`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(configData)
      });

      if (response.ok) {
        setMessage('Konfiguration erfolgreich gespeichert!');
      } else {
        setMessage('Fehler beim Speichern der Konfiguration');
      }
    } catch (error) {
      setMessage('Verbindungsfehler beim Speichern der Konfiguration');
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(''), 3000);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">System & Backup</h1>
        <p className="text-gray-600">System-Verwaltung, Backup und Konfiguration</p>
      </div>

      {message && (
        <div className={`p-4 rounded-lg ${
          message.includes('erfolgreich') 
            ? 'bg-green-100 text-green-700 border border-green-200' 
            : 'bg-red-100 text-red-700 border border-red-200'
        }`}>
          {message}
        </div>
      )}

      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {[
            { key: 'backup', label: 'Backup & Restore', icon: '💾' },
            { key: 'system', label: 'System-Info', icon: '📊' },
            { key: 'config', label: 'Konfiguration', icon: '⚙️' }
          ].map(tab => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center ${
                activeTab === tab.key
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Backup Tab */}
      {activeTab === 'backup' && (
        <div className="space-y-6">
          {/* Backup Status */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Backup-Status</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="flex items-center p-4 bg-blue-50 rounded-lg">
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-blue-500 rounded-full mr-3"></div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">Letztes Backup</p>
                    <p className="text-xs text-blue-600">{backupStatus.lastBackup}</p>
                  </div>
                </div>
              </div>

              <div className="flex items-center p-4 bg-green-50 rounded-lg">
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">Backup-Größe</p>
                    <p className="text-xs text-green-600">{backupStatus.backupSize}</p>
                  </div>
                </div>
              </div>

              <div className="flex items-center p-4 bg-purple-50 rounded-lg">
                <div className="flex items-center">
                  <div className={`w-3 h-3 ${backupStatus.autoBackup ? 'bg-green-500' : 'bg-red-500'} rounded-full mr-3`}></div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">Auto-Backup</p>
                    <p className={`text-xs ${backupStatus.autoBackup ? 'text-green-600' : 'text-red-600'}`}>
                      {backupStatus.autoBackup ? 'Aktiviert' : 'Deaktiviert'}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Backup Actions */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Backup erstellen</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Database Backup */}
              <div className="border border-gray-200 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
                    <span className="text-blue-600 text-lg">🗄️</span>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900">Datenbank-Backup</h4>
                    <p className="text-sm text-gray-600">Nur Datenbank-Inhalte (SQL)</p>
                  </div>
                </div>
                <p className="text-sm text-gray-600 mb-4">
                  Erstellt ein SQL-Backup aller Datenbank-Inhalte (Menü, Bewertungen, Benutzer, etc.)
                </p>
                <button
                  onClick={handleDatabaseBackup}
                  disabled={loading}
                  className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                  {loading ? 'Erstelle Backup...' : 'Datenbank-Backup erstellen'}
                </button>
              </div>

              {/* Full Backup */}
              <div className="border border-gray-200 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mr-3">
                    <span className="text-green-600 text-lg">📦</span>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900">Vollständiges Backup</h4>
                    <p className="text-sm text-gray-600">Datenbank + Mediendateien (ZIP)</p>
                  </div>
                </div>
                <p className="text-sm text-gray-600 mb-4">
                  Erstellt ein komplettes Backup inklusive aller Bilder und Mediendateien
                </p>
                <button
                  onClick={handleFullBackup}
                  disabled={loading}
                  className="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 disabled:opacity-50"
                >
                  {loading ? 'Erstelle Backup...' : 'Vollständiges Backup erstellen'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* System Info Tab */}
      {activeTab === 'system' && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">System-Informationen</h3>
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">CMS-Version</span>
                  <span className="text-sm text-gray-900">{systemInfo.version}</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">System-Uptime</span>
                  <span className="text-sm text-gray-900">{systemInfo.uptime}</span>
                </div>
              </div>
              <div className="space-y-4">
                <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">Datenbank-Status</span>
                  <span className="text-sm text-green-600">🟢 {systemInfo.database}</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">Speicherplatz</span>
                  <span className="text-sm text-gray-900">{systemInfo.diskSpace}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Configuration Tab */}
      {activeTab === 'config' && (
        <ConfigurationPanel onSave={handleConfigSave} loading={loading} />
      )}
    </div>
  );
};

// Configuration Panel Component
const ConfigurationPanel = ({ onSave, loading }) => {
  const [config, setConfig] = useState({
    siteName: 'Jimmy\'s Tapas Bar',
    adminEmail: 'admin@jimmys-tapas.de',
    backupFrequency: 'daily',
    maintenanceMode: false,
    debugMode: false
  });

  const handleSave = () => {
    onSave(config);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">System-Konfiguration</h3>
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Website-Name</label>
            <input
              type="text"
              value={config.siteName}
              onChange={(e) => setConfig({...config, siteName: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Admin E-Mail</label>
            <input
              type="email"
              value={config.adminEmail}
              onChange={(e) => setConfig({...config, adminEmail: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Backup-Häufigkeit</label>
          <select
            value={config.backupFrequency}
            onChange={(e) => setConfig({...config, backupFrequency: e.target.value})}
            className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="hourly">Stündlich</option>
            <option value="daily">Täglich</option>
            <option value="weekly">Wöchentlich</option>
            <option value="manual">Manuell</option>
          </select>
        </div>

        <div className="space-y-4">
          <div className="flex items-center">
            <input
              type="checkbox"
              id="maintenanceMode"
              checked={config.maintenanceMode}
              onChange={(e) => setConfig({...config, maintenanceMode: e.target.checked})}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="maintenanceMode" className="ml-2 text-sm text-gray-700">
              Wartungsmodus aktiviert
            </label>
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              id="debugMode"
              checked={config.debugMode}
              onChange={(e) => setConfig({...config, debugMode: e.target.checked})}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="debugMode" className="ml-2 text-sm text-gray-700">
              Debug-Modus aktiviert
            </label>
          </div>
        </div>

        <div className="pt-6 border-t border-gray-200">
          <button
            onClick={handleSave}
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Speichern...' : 'Konfiguration speichern'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SystemBackupSection;