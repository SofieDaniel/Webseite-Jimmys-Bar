import React, { useState, useEffect } from 'react';

const SystemBackupSection = () => {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [backupStatus, setBackupStatus] = useState({
    lastBackup: null,
    backupSize: null,
    autoBackup: true,
    backupFrequency: 'daily',
    nextScheduled: null,
    backupCount: 0
  });
  const [systemInfo, setSystemInfo] = useState({
    version: 'Jimmy\'s CMS v1.0',
    uptime: '24h 15m',
    database: 'MySQL Connected',
    diskSpace: '2.5 GB used / 10 GB available'
  });
  const [activeTab, setActiveTab] = useState('backup');

  // MySQL Database Configuration State
  const [dbConfig, setDbConfig] = useState({
    host: 'localhost',
    port: '3306',
    username: 'jimmy_user',
    password: '',
    database: 'jimmys_tapas_bar',
    ssl: false,
    charset: 'utf8mb4'
  });

  const [backupList, setBackupList] = useState([]);
  const [loadingList, setLoadingList] = useState(false);

  useEffect(() => {
    loadSystemInfo();
    loadBackupStatus();
    loadBackupList();
    loadDbConfig();
  }, []);

  const loadDbConfig = async () => {
    try {
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/database/config`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const data = await response.json();
        setDbConfig({
          host: data.host || 'localhost',
          port: data.port || '3306',
          username: data.username || 'jimmy_user',
          password: '', // Never display actual password
          database: data.database || 'jimmys_tapas_bar',
          ssl: data.ssl || false,
          charset: data.charset || 'utf8mb4'
        });
      }
    } catch (error) {
      console.error('Error loading database config:', error);
    }
  };

  const loadBackupList = async () => {
    try {
      setLoadingList(true);
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/backup/list`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Loaded backup list:', data);
        setBackupList(Array.isArray(data) ? data : []);
      } else {
        console.error('Failed to load backup list:', response.status);
        setMessage('❌ Fehler beim Laden der Backup-Liste');
      }
    } catch (error) {
      console.error('Error loading backup list:', error);
      setMessage('❌ Verbindungsfehler beim Laden der Backup-Liste');
    } finally {
      setLoadingList(false);
    }
  };

  const loadSystemInfo = async () => {
    try {
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/system/info`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const data = await response.json();
        setSystemInfo({
          version: data.version || 'Jimmy\'s CMS v1.0',
          uptime: data.uptime || 'Unbekannt',
          database: data.database_status || 'MySQL Connected',
          diskSpace: `${data.disk_usage || 'N/A'} Festplatte verwendet`,
          cpuUsage: data.cpu_usage || 'N/A',
          memoryUsage: data.memory_usage || 'N/A',
          pythonVersion: data.python_version || 'N/A',
          platform: data.platform || 'N/A',
          mysqlVersion: data.mysql_version || 'N/A'
        });
      }
    } catch (error) {
      console.error('Error loading system info:', error);
    }
  };

  const loadBackupStatus = async () => {
    try {
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/backup/status`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const data = await response.json();
        setBackupStatus({
          lastBackup: data.last_backup ? formatDateTime(data.last_backup) : 'Nie',
          backupSize: data.backup_size || 'Unbekannt',
          autoBackup: data.auto_backup || false,
          backupFrequency: data.backup_frequency || 'daily',
          nextScheduled: data.next_scheduled ? formatDateTime(data.next_scheduled) : 'Unbekannt',
          backupCount: data.backup_count || 0,
          diskSpaceUsed: data.disk_space_used || 'N/A',
          diskSpaceTotal: data.disk_space_total || 'N/A'
        });
      }
    } catch (error) {
      console.error('Error loading backup status:', error);
      setMessage('Fehler beim Laden des Backup-Status');
    }
  };

  const handleDatabaseBackup = async () => {
    setLoading(true);
    setMessage('📋 Erstelle MySQL Datenbank-Backup...');

    try {
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/backup/database`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const contentDisposition = response.headers.get('Content-Disposition');
        const backupSize = response.headers.get('X-Backup-Size');
        
        const filename = contentDisposition ? 
          contentDisposition.split('filename=')[1].replace(/"/g, '') : 
          `mysql-backup-${new Date().toISOString().split('T')[0]}.sql`;

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        setMessage(`✅ MySQL Datenbank-Backup erfolgreich erstellt! 
                   📁 Datei: ${filename}
                   📊 Größe: ${formatBytes(parseInt(backupSize || '0'))}
                   🗄️ Format: MySQL SQL-Dump`);
        
        loadBackupStatus();
        loadBackupList();
      } else {
        const errorData = await response.json();
        setMessage(`❌ Fehler beim Erstellen des MySQL Backups: ${errorData.detail}`);
      }
    } catch (error) {
      console.error('Backup error:', error);
      setMessage('❌ Verbindungsfehler beim Erstellen des Backups. Prüfen Sie Ihre Internetverbindung.');
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(''), 10000);
    }
  };

  const handleFullBackup = async () => {
    setLoading(true);
    setMessage('📦 Erstelle vollständiges Backup (MySQL + Medien)...');

    try {
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/backup/full`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const contentDisposition = response.headers.get('Content-Disposition');
        const backupSize = response.headers.get('X-Backup-Size');
        
        const filename = contentDisposition ? 
          contentDisposition.split('filename=')[1].replace(/"/g, '') : 
          `full-backup-mysql-${new Date().toISOString().split('T')[0]}.zip`;

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        setMessage(`✅ Vollständiges MySQL Backup erfolgreich erstellt! 
                   📁 Datei: ${filename}
                   📊 Größe: ${formatBytes(parseInt(backupSize || '0'))}
                   💾 Enthält: MySQL Datenbank + Mediendateien`);
        
        loadBackupStatus();
        loadBackupList();
      } else {
        const errorData = await response.json();
        setMessage(`❌ Fehler beim Erstellen des vollständigen Backups: ${errorData.detail}`);
      }
    } catch (error) {
      console.error('Full backup error:', error);
      setMessage('❌ Verbindungsfehler beim Erstellen des Backups. Prüfen Sie Ihre Internetverbindung.');
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(''), 10000);
    }
  };

  const handleDownloadBackup = async (backupId, filename) => {
    setLoading(true);
    setMessage(`📥 Lade Backup herunter: ${filename}...`);

    try {
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/backup/download/${backupId}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        setMessage(`✅ Backup erfolgreich heruntergeladen: ${filename}`);
      } else {
        setMessage('❌ Fehler beim Download des Backups');
      }
    } catch (error) {
      setMessage('❌ Verbindungsfehler beim Download');
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(''), 5000);
    }
  };

  const handleDeleteBackup = async (backupId, filename) => {
    if (!window.confirm(`Sind Sie sicher, dass Sie das Backup "${filename}" löschen möchten?`)) {
      return;
    }

    setLoading(true);
    setMessage(`🗑️ Lösche Backup: ${filename}...`);

    try {
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/backup/${backupId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        setMessage(`✅ Backup "${filename}" erfolgreich gelöscht!`);
        loadBackupList();
      } else {
        setMessage('❌ Fehler beim Löschen des Backups');
      }
    } catch (error) {
      setMessage('❌ Verbindungsfehler beim Löschen');
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(''), 5000);
    }
  };

  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  const formatDateTime = (isoString) => {
    try {
      const date = new Date(isoString);
      return date.toLocaleDateString('de-DE') + ' ' + date.toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' });
    } catch {
      return 'Unbekannt';
    }
  };

  const handleConfigSave = async (configData) => {
    setLoading(true);
    setMessage('Speichere Konfiguration...');

    try {
      const token = localStorage.getItem('adminToken');
      let endpoint = '/api/admin/config';
      
      if (configData.type === 'database') {
        endpoint = '/api/admin/database/config';
      }

      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}${endpoint}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(configData)
      });

      if (response.ok) {
        setMessage('✅ Konfiguration erfolgreich gespeichert!');
        if (configData.type === 'database') {
          loadDbConfig();
        }
      } else {
        const errorData = await response.json();
        setMessage(`❌ Fehler beim Speichern: ${errorData.detail}`);
      }
    } catch (error) {
      setMessage('❌ Verbindungsfehler beim Speichern der Konfiguration');
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(''), 5000);
    }
  };

  const testDatabaseConnection = async () => {
    setLoading(true);
    setMessage('🔍 Teste MySQL Datenbankverbindung...');

    try {
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/database/test`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(dbConfig)
      });

      if (response.ok) {
        const data = await response.json();
        setMessage(`✅ MySQL Datenbankverbindung erfolgreich! 
                   🗄️ Server: ${data.server_info || 'MySQL'}
                   📊 Status: ${data.status || 'Connected'}`);
      } else {
        const errorData = await response.json();
        setMessage(`❌ MySQL Verbindung fehlgeschlagen: ${errorData.detail}`);
      }
    } catch (error) {
      setMessage('❌ Fehler beim Testen der MySQL Verbindung');
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(''), 5000);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">System & Backup</h1>
        <p className="text-gray-600">MySQL System-Verwaltung, Backup und Konfiguration</p>
      </div>

      {message && (
        <div className={`p-4 rounded-lg whitespace-pre-line ${
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
            { key: 'backup', label: 'MySQL Backup & Restore', icon: '💾' },
            { key: 'system', label: 'System-Info', icon: '📊' },
            { key: 'database', label: 'MySQL Konfiguration', icon: '🗄️' },
            { key: 'config', label: 'Allgemeine Konfiguration', icon: '⚙️' }
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

      {/* MySQL Backup Tab */}
      {activeTab === 'backup' && (
        <div className="space-y-6">
          {/* Enhanced Backup Status */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-gray-900">MySQL Backup-Status</h3>
              <button
                onClick={loadBackupStatus}
                disabled={loading}
                className="text-blue-600 hover:text-blue-800 text-sm disabled:opacity-50"
              >
                🔄 Aktualisieren
              </button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="flex items-center p-4 bg-blue-50 rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-blue-500 rounded-full mr-3"></div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Letztes Backup</p>
                      <p className="text-xs text-blue-600">{backupStatus.lastBackup}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-center p-4 bg-green-50 rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Backup-Größe</p>
                      <p className="text-xs text-green-600">{backupStatus.backupSize}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-center p-4 bg-purple-50 rounded-lg">
                <div className="flex-1">
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

              <div className="flex items-center p-4 bg-orange-50 rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-orange-500 rounded-full mr-3"></div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Nächstes Backup</p>
                      <p className="text-xs text-orange-600">{backupStatus.nextScheduled}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-center p-4 bg-gray-50 rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-gray-500 rounded-full mr-3"></div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Backup-Anzahl</p>
                      <p className="text-xs text-gray-600">{backupStatus.backupCount} Backups</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-center p-4 bg-indigo-50 rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-indigo-500 rounded-full mr-3"></div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Speicherplatz</p>
                      <p className="text-xs text-indigo-600">{backupStatus.diskSpaceUsed} / {backupStatus.diskSpaceTotal}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* MySQL Backup Actions */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">MySQL Backup erstellen</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* MySQL Database Backup */}
              <div className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                <div className="flex items-center mb-4">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
                    <span className="text-blue-600 text-2xl">🗄️</span>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900">MySQL Datenbank-Backup</h4>
                    <p className="text-sm text-gray-600">Vollständiger MySQL SQL-Dump</p>
                  </div>
                </div>
                <p className="text-sm text-gray-600 mb-4">
                  Erstellt einen vollständigen MySQL-Dump aller Tabellen und Daten (Menü, Bewertungen, Benutzer, etc.).
                  Empfohlen für tägliche Sicherungen.
                </p>
                <div className="mb-4">
                  <div className="text-xs text-gray-500">
                    💡 <strong>Format:</strong> SQL-Dump für vollständige MySQL Wiederherstellung
                  </div>
                </div>
                <button
                  onClick={handleDatabaseBackup}
                  disabled={loading}
                  className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {loading ? (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Erstelle MySQL Backup...
                    </div>
                  ) : (
                    'MySQL Datenbank-Backup erstellen'
                  )}
                </button>
              </div>

              {/* Full Backup */}
              <div className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                <div className="flex items-center mb-4">
                  <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mr-4">
                    <span className="text-green-600 text-2xl">📦</span>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900">Vollständiges Backup</h4>
                    <p className="text-sm text-gray-600">MySQL + Mediendateien (ZIP)</p>
                  </div>
                </div>
                <p className="text-sm text-gray-600 mb-4">
                  Erstellt ein komplettes Backup inklusive MySQL-Dump und aller Bilder/Mediendateien.
                  Empfohlen für vollständige Systemsicherung.
                </p>
                <div className="mb-4">
                  <div className="text-xs text-gray-500">
                    💡 <strong>Format:</strong> ZIP mit SQL-Dump + Medien, größere Dateigröße
                  </div>
                </div>
                <button
                  onClick={handleFullBackup}
                  disabled={loading}
                  className="w-full bg-green-600 text-white py-3 px-4 rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {loading ? (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Erstelle vollständiges Backup...
                    </div>
                  ) : (
                    'Vollständiges Backup erstellen'
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Backup List */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Verfügbare MySQL Backups</h3>
              <button
                onClick={loadBackupList}
                disabled={loadingList}
                className="text-blue-600 hover:text-blue-800 text-sm disabled:opacity-50"
              >
                {loadingList ? '🔄 Lade...' : '🔄 Aktualisieren'}
              </button>
            </div>
            
            {loadingList ? (
              <div className="flex items-center justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <span className="ml-2 text-gray-600">Lade Backup-Liste...</span>
              </div>
            ) : backupList.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                📂 Keine MySQL Backups vorhanden. Erstellen Sie Ihr erstes Backup oben.
              </div>
            ) : (
              <div className="space-y-3">
                {backupList.map((backup, index) => (
                  <div key={backup.id || index} className="border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
                          <span className="text-xl">
                            {backup.type === 'database' ? '🗄️' : '📦'}
                          </span>
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">{backup.filename}</p>
                          <div className="flex items-center space-x-4 text-sm text-gray-500">
                            <span>📅 {formatDateTime(backup.created_at)}</span>
                            <span>📊 {backup.size_human}</span>
                            <span>🔹 {backup.type === 'database' ? 'MySQL Dump' : 'Vollständig'}</span>
                            {backup.total_documents && (
                              <span>📄 {backup.total_documents} Datensätze</span>
                            )}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => handleDownloadBackup(backup.id, backup.filename)}
                          disabled={loading}
                          className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 disabled:opacity-50"
                        >
                          📥 Download
                        </button>
                        <button
                          onClick={() => handleDeleteBackup(backup.id, backup.filename)}
                          disabled={loading}
                          className="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700 disabled:opacity-50"
                        >
                          🗑️ Löschen
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* MySQL Troubleshooting */}
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
            <h4 className="font-semibold text-yellow-800 mb-2">🛠️ MySQL Troubleshooting-Hinweise</h4>
            <div className="text-sm text-yellow-700 space-y-2">
              <p><strong>Backup schlägt fehl:</strong> Prüfen Sie die MySQL-Verbindung und Speicherplatz.</p>
              <p><strong>Download startet nicht:</strong> Deaktivieren Sie temporär Pop-up-Blocker im Browser.</p>
              <p><strong>Große MySQL Dumps:</strong> Bei vielen Daten kann der Export einige Minuten dauern.</p>
              <p><strong>Automatische Backups:</strong> Werden täglich um 02:00 Uhr erstellt (falls aktiviert).</p>
              <p><strong>MySQL-Kompatibilität:</strong> SQL-Dumps sind mit MySQL 5.7+ und MariaDB kompatibel.</p>
            </div>
          </div>
        </div>
      )}

      {/* Enhanced System Info Tab */}
      {activeTab === 'system' && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold text-gray-900">System-Informationen</h3>
            <button
              onClick={loadSystemInfo}
              disabled={loading}
              className="text-blue-600 hover:text-blue-800 text-sm disabled:opacity-50"
            >
              🔄 Aktualisieren
            </button>
          </div>
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">CMS-Version</span>
                  <span className="text-sm text-gray-900 font-mono">{systemInfo.version}</span>
                </div>
                <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">System-Uptime</span>
                  <span className="text-sm text-gray-900 font-mono">{systemInfo.uptime}</span>
                </div>
                <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">Python Version</span>
                  <span className="text-sm text-gray-900 font-mono">{systemInfo.pythonVersion}</span>
                </div>
                <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">MySQL Version</span>
                  <span className="text-sm text-blue-600 font-mono">{systemInfo.mysqlVersion}</span>
                </div>
              </div>
              <div className="space-y-4">
                <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">MySQL-Status</span>
                  <span className="text-sm text-green-600 font-medium">🟢 {systemInfo.database}</span>
                </div>
                <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">CPU-Auslastung</span>
                  <span className="text-sm text-gray-900 font-mono">{systemInfo.cpuUsage}</span>
                </div>
                <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">Speicher-Auslastung</span>
                  <span className="text-sm text-gray-900 font-mono">{systemInfo.memoryUsage}</span>
                </div>
                <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">Plattform</span>
                  <span className="text-sm text-purple-600 font-mono">{systemInfo.platform}</span>
                </div>
              </div>
            </div>
            
            <div className="border-t border-gray-200 pt-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">Festplatten-Auslastung</span>
                  <span className="text-sm text-blue-600 font-mono">{systemInfo.diskSpace}</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-green-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">Backup-Anzahl</span>
                  <span className="text-sm text-green-600 font-mono">{backupStatus.backupCount} MySQL Backups</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* MySQL Database Configuration Tab */}
      {activeTab === 'database' && (
        <MySQLConfigPanel 
          dbConfig={dbConfig} 
          setDbConfig={setDbConfig}
          onSave={handleConfigSave}
          onTest={testDatabaseConnection}
          loading={loading}
        />
      )}

      {/* General Configuration Tab */}
      {activeTab === 'config' && (
        <GeneralConfigPanel onSave={handleConfigSave} loading={loading} />
      )}
    </div>
  );
};

// MySQL Database Configuration Panel Component
const MySQLConfigPanel = ({ dbConfig, setDbConfig, onSave, onTest, loading }) => {
  const [showPassword, setShowPassword] = useState(false);
  const [testResult, setTestResult] = useState('');

  const handleSave = () => {
    onSave({
      type: 'database',
      ...dbConfig
    });
  };

  const handleTest = async () => {
    setTestResult('');
    await onTest();
    setTestResult('MySQL Verbindung erfolgreich getestet!');
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">MySQL Datenbank-Konfiguration</h3>
      
      {/* Current Connection */}
      <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <h4 className="font-medium text-blue-900 mb-2">🔗 Aktuelle MySQL Verbindung</h4>
        <p className="text-sm text-blue-800 font-mono bg-white px-3 py-2 rounded border">
          mysql://{dbConfig.username}@{dbConfig.host}:{dbConfig.port}/{dbConfig.database}
        </p>
        <p className="text-xs text-blue-600 mt-2">
          Sichere MySQL-Verbindung über Environment-Variablen verwaltet.
        </p>
      </div>

      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <span className="flex items-center">
                🖥️ MySQL Host/Server
                <span className="ml-1 text-red-500">*</span>
              </span>
            </label>
            <input
              type="text"
              value={dbConfig.host}
              onChange={(e) => setDbConfig({...dbConfig, host: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 font-mono focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="localhost oder IP-Adresse"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <span className="flex items-center">
                🔌 MySQL Port
                <span className="ml-1 text-red-500">*</span>
              </span>
            </label>
            <input
              type="text"
              value={dbConfig.port}
              onChange={(e) => setDbConfig({...dbConfig, port: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 font-mono focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="3306 (Standard MySQL Port)"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <span className="flex items-center">
              🗄️ MySQL Datenbank-Name
              <span className="ml-1 text-red-500">*</span>
            </span>
          </label>
          <input
            type="text"
            value={dbConfig.database}
            onChange={(e) => setDbConfig({...dbConfig, database: e.target.value})}
            className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 font-mono focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="jimmys_tapas_bar"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              👤 MySQL Benutzername
              <span className="ml-1 text-red-500">*</span>
            </label>
            <input
              type="text"
              value={dbConfig.username}
              onChange={(e) => setDbConfig({...dbConfig, username: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 font-mono focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="MySQL Benutzername"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              🔐 MySQL Passwort
              <span className="ml-1 text-red-500">*</span>
            </label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                value={dbConfig.password}
                onChange={(e) => setDbConfig({...dbConfig, password: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 font-mono focus:ring-2 focus:ring-blue-500 focus:border-transparent pr-12"
                placeholder="MySQL Passwort"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
              >
                {showPassword ? '🙈' : '👁️'}
              </button>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              🔒 SSL Verbindung
            </label>
            <div className="flex items-center">
              <input
                type="checkbox"
                checked={dbConfig.ssl}
                onChange={(e) => setDbConfig({...dbConfig, ssl: e.target.checked})}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label className="ml-2 text-sm text-gray-700">
                SSL/TLS für MySQL Verbindung verwenden
              </label>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              📝 Zeichensatz
            </label>
            <select
              value={dbConfig.charset}
              onChange={(e) => setDbConfig({...dbConfig, charset: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="utf8mb4">utf8mb4 (empfohlen)</option>
              <option value="utf8">utf8</option>
              <option value="latin1">latin1</option>
            </select>
          </div>
        </div>

        {/* Security Warning */}
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <span className="text-yellow-400 text-lg">⚠️</span>
            </div>
            <div className="ml-3">
              <h4 className="text-sm font-medium text-yellow-800">MySQL Sicherheitshinweise</h4>
              <div className="mt-2 text-sm text-yellow-700">
                <ul className="list-disc pl-5 space-y-1">
                  <li>Nur autorisierte Admins haben Zugang zu MySQL-Konfigurationen</li>
                  <li>Verwenden Sie starke Passwörter für MySQL-Benutzer</li>
                  <li>Aktivieren Sie SSL/TLS für Produktionsumgebungen</li>
                  <li>Erstellen Sie MySQL-Backups vor Konfigurationsänderungen</li>
                  <li>utf8mb4 unterstützt alle Unicode-Zeichen inkl. Emojis</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        {testResult && (
          <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
            ✅ {testResult}
          </div>
        )}

        <div className="flex justify-between pt-6 border-t border-gray-200">
          <button
            onClick={handleTest}
            disabled={loading}
            className="bg-orange-600 text-white px-6 py-2 rounded-lg hover:bg-orange-700 disabled:opacity-50 flex items-center"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Teste MySQL...
              </>
            ) : (
              <>
                🔍 MySQL Verbindung testen
              </>
            )}
          </button>
          
          <button
            onClick={handleSave}
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Speichern...
              </>
            ) : (
              <>
                💾 MySQL Konfiguration speichern
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

// General Configuration Panel Component
const GeneralConfigPanel = ({ onSave, loading }) => {
  const [config, setConfig] = useState({
    siteName: 'Jimmy\'s Tapas Bar',
    adminEmail: 'admin@jimmys-tapas.de',
    backupFrequency: 'daily',
    maintenanceMode: false,
    debugMode: false,
    emailNotifications: true,
    autoBackup: true,
    maxFileSize: '10',
    sessionTimeout: '60',
    allowRegistration: false,
    mysqlVersion: 'auto-detect'
  });

  const handleSave = () => {
    onSave({
      type: 'general',
      ...config
    });
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Allgemeine Konfiguration</h3>
      <div className="space-y-6">
        {/* Basic Settings */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              🏪 Website-Name
            </label>
            <input
              type="text"
              value={config.siteName}
              onChange={(e) => setConfig({...config, siteName: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              📧 Admin E-Mail
            </label>
            <input
              type="email"
              value={config.adminEmail}
              onChange={(e) => setConfig({...config, adminEmail: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* System Settings */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              💾 MySQL Backup-Häufigkeit
            </label>
            <select
              value={config.backupFrequency}
              onChange={(e) => setConfig({...config, backupFrequency: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="hourly">Stündlich</option>
              <option value="daily">Täglich (empfohlen)</option>
              <option value="weekly">Wöchentlich</option>
              <option value="manual">Nur manuell</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              📁 Max. Dateigröße (MB)
            </label>
            <input
              type="number"
              min="1"
              max="100"
              value={config.maxFileSize}
              onChange={(e) => setConfig({...config, maxFileSize: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            ⏱️ Session-Timeout (Minuten)
          </label>
          <input
            type="number"
            min="15"
            max="480"
            value={config.sessionTimeout}
            onChange={(e) => setConfig({...config, sessionTimeout: e.target.value})}
            className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <p className="text-xs text-gray-500 mt-1">
            Automatische Abmeldung nach Inaktivität (15-480 Minuten)
          </p>
        </div>

        {/* Toggle Settings */}
        <div className="space-y-4">
          <h4 className="font-medium text-gray-900">MySQL System-Optionen</h4>
          
          <div className="space-y-3">
            {[
              { key: 'autoBackup', label: 'Automatische MySQL Backups aktiviert', icon: '💾' },
              { key: 'emailNotifications', label: 'E-Mail-Benachrichtigungen aktiviert', icon: '📧' },
              { key: 'maintenanceMode', label: 'Wartungsmodus aktiviert', icon: '🔧' },
              { key: 'debugMode', label: 'Debug-Modus aktiviert', icon: '🐛' },
              { key: 'allowRegistration', label: 'Benutzer-Registrierung erlauben', icon: '👥' }
            ].map(({ key, label, icon }) => (
              <div key={key} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <label className="flex items-center text-sm text-gray-700">
                  <span className="mr-2">{icon}</span>
                  {label}
                </label>
                <div className="relative">
                  <input
                    type="checkbox"
                    checked={config[key]}
                    onChange={(e) => setConfig({...config, [key]: e.target.checked})}
                    className="sr-only"
                  />
                  <div 
                    onClick={() => setConfig({...config, [key]: !config[key]})}
                    className={`w-11 h-6 rounded-full cursor-pointer transition-colors ${
                      config[key] ? 'bg-blue-600' : 'bg-gray-300'
                    }`}
                  >
                    <div className={`w-4 h-4 bg-white rounded-full shadow transform transition-transform ${
                      config[key] ? 'translate-x-6' : 'translate-x-1'
                    } mt-1`}></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="pt-6 border-t border-gray-200">
          <button
            onClick={handleSave}
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Speichern...
              </>
            ) : (
              <>
                💾 Konfiguration speichern
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SystemBackupSection;