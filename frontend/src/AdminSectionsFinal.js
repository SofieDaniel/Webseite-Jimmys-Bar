import React, { useState, useEffect } from 'react';

// Media Management Section
export const MediaSection = ({ user, token, apiCall }) => {
  const [uploadedImages, setUploadedImages] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [selectedImage, setSelectedImage] = useState(null);

  const handleImageUpload = async (files) => {
    if (!files || files.length === 0) return;

    setUploading(true);
    const newImages = [];

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      setUploadProgress(((i + 1) / files.length) * 100);

      try {
        // Create FormData for file upload
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/upload-image`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          },
          body: formData
        });

        if (response.ok) {
          const data = await response.json();
          newImages.push({
            id: Date.now() + i,
            filename: file.name,
            size: file.size,
            uploadDate: new Date().toISOString(),
            dataUrl: data.image_url
          });
        }
      } catch (error) {
        console.error('Error uploading image:', error);
      }
    }

    setUploadedImages(prev => [...prev, ...newImages]);
    setUploading(false);
    setUploadProgress(0);
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const deleteImage = (imageId) => {
    if (window.confirm('Sind Sie sicher, dass Sie dieses Bild löschen möchten?')) {
      setUploadedImages(prev => prev.filter(img => img.id !== imageId));
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Medien verwalten</h1>
        <p className="text-gray-600">Bilder hochladen und verwalten</p>
      </div>

      {/* Upload Area */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Bilder hochladen</h3>
        
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-gray-400 transition-colors">
          <input
            type="file"
            multiple
            accept="image/*"
            onChange={(e) => handleImageUpload(e.target.files)}
            className="hidden"
            id="image-upload"
            disabled={uploading}
          />
          <label htmlFor="image-upload" className="cursor-pointer">
            <svg className="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            <div className="text-xl font-medium text-gray-900 mb-2">
              Bilder hochladen
            </div>
            <p className="text-gray-500 mb-2">
              Klicken Sie hier oder ziehen Sie Dateien in diesen Bereich
            </p>
            <p className="text-sm text-gray-400">
              Unterstützte Formate: PNG, JPG, GIF, WEBP (Max. 10MB pro Datei)
            </p>
          </label>
        </div>

        {uploading && (
          <div className="mt-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">Upload läuft...</span>
              <span className="text-sm text-gray-500">{Math.round(uploadProgress)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              ></div>
            </div>
          </div>
        )}
      </div>

      {/* Image Gallery */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-lg font-semibold text-gray-900">Hochgeladene Bilder</h3>
          <span className="text-sm text-gray-500">
            {uploadedImages.length} Bilder
          </span>
        </div>

        {uploadedImages.length === 0 ? (
          <div className="text-center py-12">
            <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-gray-900">Keine Bilder</h3>
            <p className="mt-1 text-sm text-gray-500">Laden Sie Ihr erstes Bild hoch.</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {uploadedImages.map((image) => (
              <div key={image.id} className="group relative bg-gray-100 rounded-lg overflow-hidden">
                <img
                  src={image.dataUrl}
                  alt={image.filename}
                  className="w-full h-48 object-cover cursor-pointer"
                  onClick={() => setSelectedImage(image)}
                />
                <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-50 transition-all duration-200 flex items-center justify-center">
                  <div className="opacity-0 group-hover:opacity-100 transition-opacity space-x-2">
                    <button
                      onClick={() => setSelectedImage(image)}
                      className="bg-white text-gray-800 p-2 rounded-lg hover:bg-gray-100"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                    </button>
                    <button
                      onClick={() => deleteImage(image.id)}
                      className="bg-red-600 text-white p-2 rounded-lg hover:bg-red-700"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
                <div className="p-3">
                  <p className="text-sm font-medium text-gray-900 truncate">{image.filename}</p>
                  <p className="text-xs text-gray-500">{formatFileSize(image.size)}</p>
                  <p className="text-xs text-gray-500">
                    {new Date(image.uploadDate).toLocaleDateString('de-DE')}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Image Detail Modal */}
      {selectedImage && (
        <ImageDetailModal
          image={selectedImage}
          onClose={() => setSelectedImage(null)}
          onDelete={deleteImage}
        />
      )}
    </div>
  );
};

// Image Detail Modal
const ImageDetailModal = ({ image, onClose, onDelete }) => {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(image.dataUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-gray-900">Bild-Details</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 p-2"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <img
                src={image.dataUrl}
                alt={image.filename}
                className="w-full rounded-lg border border-gray-200"
              />
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Dateiname</label>
                <p className="text-gray-900">{image.filename}</p>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Dateigröße</label>
                <p className="text-gray-900">{formatFileSize(image.size)}</p>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Upload-Datum</label>
                <p className="text-gray-900">
                  {new Date(image.uploadDate).toLocaleDateString('de-DE')} um{' '}
                  {new Date(image.uploadDate).toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' })}
                </p>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Bild-URL</label>
                <div className="flex">
                  <input
                    type="text"
                    value={image.dataUrl}
                    readOnly
                    className="flex-1 p-2 border border-gray-300 rounded-l-lg bg-gray-50 text-sm"
                  />
                  <button
                    onClick={copyToClipboard}
                    className="px-4 py-2 bg-blue-600 text-white rounded-r-lg hover:bg-blue-700 text-sm"
                  >
                    {copied ? 'Kopiert!' : 'Kopieren'}
                  </button>
                </div>
              </div>

              <div className="pt-4 border-t border-gray-200">
                <button
                  onClick={() => {
                    onDelete(image.id);
                    onClose();
                  }}
                  className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
                >
                  Bild löschen
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

// Maintenance Mode Section
export const MaintenanceSection = ({ user, token, apiCall }) => {
  const [maintenanceData, setMaintenanceData] = useState({
    is_active: false,
    message: 'Die Website befindet sich derzeit im Wartungsmodus.'
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    loadMaintenanceStatus();
  }, []);

  const loadMaintenanceStatus = async () => {
    try {
      setLoading(true);
      const response = await apiCall('/maintenance');
      if (response.ok) {
        const data = await response.json();
        setMaintenanceData(data);
      }
    } catch (error) {
      setError('Fehler beim Laden des Wartungsmodus-Status');
    } finally {
      setLoading(false);
    }
  };

  const updateMaintenanceMode = async () => {
    try {
      setSaving(true);
      setError('');
      setSuccess('');
      
      const response = await apiCall('/admin/maintenance', 'PUT', maintenanceData);
      if (response.ok) {
        setSuccess('Wartungsmodus erfolgreich aktualisiert!');
        setTimeout(() => setSuccess(''), 3000);
        loadMaintenanceStatus();
      } else {
        setError('Fehler beim Aktualisieren des Wartungsmodus');
      }
    } catch (error) {
      setError('Verbindungsfehler beim Speichern');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-32">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Wartungsmodus</h1>
        <p className="text-gray-600">Website-Wartungsmodus aktivieren oder deaktivieren</p>
      </div>

      {success && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
          {success}
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {/* Current Status */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Aktueller Status</h3>
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${
            maintenanceData.is_active 
              ? 'bg-red-100 text-red-800' 
              : 'bg-green-100 text-green-800'
          }`}>
            {maintenanceData.is_active ? 'Wartungsmodus AKTIV' : 'Website ONLINE'}
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className={`p-4 rounded-lg border-2 ${
            maintenanceData.is_active 
              ? 'border-red-200 bg-red-50' 
              : 'border-green-200 bg-green-50'
          }`}>
            <div className="flex items-center mb-3">
              {maintenanceData.is_active ? (
                <svg className="w-8 h-8 text-red-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              ) : (
                <svg className="w-8 h-8 text-green-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              )}
              <h4 className={`text-lg font-semibold ${
                maintenanceData.is_active ? 'text-red-800' : 'text-green-800'
              }`}>
                {maintenanceData.is_active ? 'Wartungsmodus' : 'Normal-Betrieb'}
              </h4>
            </div>
            <p className={`text-sm ${
              maintenanceData.is_active ? 'text-red-700' : 'text-green-700'
            }`}>
              {maintenanceData.is_active 
                ? 'Die Website ist für Besucher nicht erreichbar. Nur Administratoren können darauf zugreifen.'
                : 'Die Website ist normal erreichbar und alle Funktionen sind verfügbar.'
              }
            </p>
          </div>

          <div className="space-y-4">
            {maintenanceData.activated_by && (
              <div>
                <p className="text-sm text-gray-600">
                  <span className="font-medium">Aktiviert von:</span> {maintenanceData.activated_by}
                </p>
                {maintenanceData.activated_at && (
                  <p className="text-sm text-gray-600">
                    <span className="font-medium">Aktiviert am:</span>{' '}
                    {new Date(maintenanceData.activated_at).toLocaleDateString('de-DE')} um{' '}
                    {new Date(maintenanceData.activated_at).toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' })}
                  </p>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Maintenance Settings */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Wartungsmodus konfigurieren</h3>
        
        <div className="space-y-6">
          {/* Toggle Switch */}
          <div className="flex items-center justify-between">
            <div>
              <h4 className="text-sm font-medium text-gray-900">Wartungsmodus aktivieren</h4>
              <p className="text-sm text-gray-500">
                Aktiviert eine Wartungsseite für alle Besucher
              </p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={maintenanceData.is_active}
                onChange={(e) => setMaintenanceData({
                  ...maintenanceData,
                  is_active: e.target.checked
                })}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>

          {/* Message Configuration */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Wartungsnachricht
            </label>
            <textarea
              value={maintenanceData.message}
              onChange={(e) => setMaintenanceData({
                ...maintenanceData,
                message: e.target.value
              })}
              rows={4}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Nachricht, die den Besuchern angezeigt wird..."
            />
            <p className="text-sm text-gray-500 mt-1">
              Diese Nachricht wird Besuchern angezeigt, wenn der Wartungsmodus aktiv ist.
            </p>
          </div>

          {/* Save Button */}
          <div className="flex justify-end">
            <button
              onClick={updateMaintenanceMode}
              disabled={saving}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center"
            >
              {saving ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Speichern...
                </>
              ) : (
                <>
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  Änderungen speichern
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Warning Notice */}
      {maintenanceData.is_active && (
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-amber-800">
                Wartungsmodus ist aktiviert
              </h3>
              <div className="mt-2 text-sm text-amber-700">
                <p>
                  Die Website ist derzeit für normale Besucher nicht erreichbar. 
                  Vergessen Sie nicht, den Wartungsmodus zu deaktivieren, wenn die Arbeiten abgeschlossen sind.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};