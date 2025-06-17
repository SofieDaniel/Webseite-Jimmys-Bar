import React, { useState, useEffect } from 'react';

const LocationsAdminSection = () => {
  const [locationsData, setLocationsData] = useState({
    page_title: 'Unsere Standorte',
    page_description: 'Besuchen Sie uns an einem unserer beiden Standorte',
    locations: []
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');
  const [editingLocation, setEditingLocation] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);

  const [newLocation, setNewLocation] = useState({
    name: '',
    address: '',
    phone: '',
    email: '',
    opening_hours: {
      "Montag": "16:00 - 23:00",
      "Dienstag": "16:00 - 23:00", 
      "Mittwoch": "16:00 - 23:00",
      "Donnerstag": "16:00 - 23:00",
      "Freitag": "16:00 - 24:00",
      "Samstag": "12:00 - 24:00",
      "Sonntag": "12:00 - 23:00"
    },
    description: '',
    image_url: '',
    maps_embed: ''
  });

  useEffect(() => {
    loadLocationsData();
  }, []);

  const loadLocationsData = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/locations`);
      if (response.ok) {
        const data = await response.json();
        console.log('Loaded locations data:', data);
        
        // Handle MySQL response structure
        const normalizedData = {
          page_title: data.page_title || 'Unsere Standorte',
          page_description: data.page_description || 'Besuchen Sie uns an einem unserer beiden Standorte',
          locations: data.locations_data || data.locations || []
        };
        
        setLocationsData(normalizedData);
      } else {
        console.error('Failed to load locations:', response.status);
        setMessage('Fehler beim Laden der Standort-Daten');
      }
    } catch (error) {
      console.error('Error loading locations data:', error);
      setMessage('Fehler beim Laden der Standort-Daten');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setMessage('');

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/locations`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('adminToken')}`
        },
        body: JSON.stringify(locationsData)
      });

      if (response.ok) {
        setMessage('Standort-Inhalte erfolgreich gespeichert!');
        setTimeout(() => setMessage(''), 3000);
      } else {
        setMessage('Fehler beim Speichern der Standort-Inhalte');
      }
    } catch (error) {
      setMessage('Verbindungsfehler beim Speichern');
    } finally {
      setSaving(false);
    }
  };

  const addLocation = () => {
    const updatedLocations = [...locationsData.locations, { ...newLocation, id: Date.now().toString() }];
    setLocationsData({ ...locationsData, locations: updatedLocations });
    setNewLocation({
      name: '',
      address: '',
      phone: '',
      email: '',
      opening_hours: {
        "Montag": "16:00 - 23:00",
        "Dienstag": "16:00 - 23:00", 
        "Mittwoch": "16:00 - 23:00",
        "Donnerstag": "16:00 - 23:00",
        "Freitag": "16:00 - 24:00",
        "Samstag": "12:00 - 24:00",
        "Sonntag": "12:00 - 23:00"
      },
      description: '',
      image_url: '',
      maps_embed: ''
    });
    setShowAddForm(false);
  };

  const updateLocation = (locationId, updatedLocation) => {
    const updatedLocations = locationsData.locations.map(loc => 
      loc.id === locationId ? updatedLocation : loc
    );
    setLocationsData({ ...locationsData, locations: updatedLocations });
    setEditingLocation(null);
  };

  const deleteLocation = (locationId) => {
    if (window.confirm('Sind Sie sicher, dass Sie diesen Standort löschen möchten?')) {
      const updatedLocations = locationsData.locations.filter(loc => loc.id !== locationId);
      setLocationsData({ ...locationsData, locations: updatedLocations });
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
        <h2 className="text-3xl font-bold text-gray-900">Standorte verwalten</h2>
        <p className="text-gray-600 mt-2">Bearbeiten Sie die Informationen zu Ihren Standorten</p>
      </div>

      {message && (
        <div className={`mb-6 p-4 rounded-lg ${
          message.includes('erfolgreich') 
            ? 'bg-green-100 text-green-700 border border-green-200' 
            : 'bg-red-100 text-red-700 border border-red-200'
        }`}>
          {message}
        </div>
      )}

      {/* Page Settings */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Seiten-Einstellungen</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Seitentitel</label>
            <input
              type="text"
              value={locationsData.page_title}
              onChange={(e) => setLocationsData({
                ...locationsData,
                page_title: e.target.value
              })}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Seitenbeschreibung</label>
            <input
              type="text"
              value={locationsData.page_description}
              onChange={(e) => setLocationsData({
                ...locationsData,
                page_description: e.target.value
              })}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>

      {/* Locations Management */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-lg font-semibold text-gray-900">Standorte ({locationsData.locations.length})</h3>
          <button
            onClick={() => setShowAddForm(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Neuen Standort hinzufügen
          </button>
        </div>

        {/* Locations List */}
        <div className="space-y-6">
          {locationsData.locations.map((location, index) => (
            <div key={location.id || index} className="border border-gray-200 rounded-lg p-6">
              <div className="flex justify-between items-start mb-4">
                <div className="flex-1">
                  <h4 className="text-xl font-semibold text-gray-900 mb-2">{location.name}</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
                    <div>
                      <p><strong>Adresse:</strong> {location.address}</p>
                      <p><strong>Telefon:</strong> {location.phone}</p>
                      <p><strong>E-Mail:</strong> {location.email}</p>
                    </div>
                    <div>
                      <p><strong>Beschreibung:</strong> {location.description}</p>
                      {location.image_url && (
                        <div className="mt-2">
                          <img src={location.image_url} alt={location.name} className="w-20 h-20 object-cover rounded border" />
                        </div>
                      )}
                    </div>
                  </div>
                </div>
                <div className="flex space-x-2 ml-4">
                  <button
                    onClick={() => setEditingLocation(location)}
                    className="text-blue-600 hover:text-blue-800 p-2"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button
                    onClick={() => deleteLocation(location.id)}
                    className="text-red-600 hover:text-red-800 p-2"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>

              {/* Opening Hours */}
              <div className="mt-4">
                <h5 className="font-medium text-gray-900 mb-2">Öffnungszeiten:</h5>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs text-gray-600">
                  {Object.entries(location.opening_hours || {}).map(([day, hours]) => (
                    <div key={day} className="flex justify-between">
                      <span className="font-medium">{day}:</span>
                      <span>{hours}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}

          {locationsData.locations.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              <div className="text-4xl mb-4">📍</div>
              <p>Noch keine Standorte hinzugefügt.</p>
              <p className="text-sm mt-2">Fügen Sie Ihren ersten Standort hinzu.</p>
            </div>
          )}
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end mb-6">
        <button
          onClick={handleSave}
          disabled={saving}
          className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 font-medium"
        >
          {saving ? 'Speichern...' : 'Alle Änderungen speichern'}
        </button>
      </div>

      {/* Add/Edit Location Modal */}
      {(showAddForm || editingLocation) && (
        <LocationModal
          location={editingLocation || newLocation}
          onSave={editingLocation ? updateLocation : addLocation}
          onCancel={() => {
            setShowAddForm(false);
            setEditingLocation(null);
          }}
          isEditing={!!editingLocation}
          setLocation={editingLocation ? setEditingLocation : setNewLocation}
        />
      )}
    </div>
  );
};

// Location Modal Component
const LocationModal = ({ location, onSave, onCancel, isEditing, setLocation }) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (isEditing) {
      onSave(location.id, location);
    } else {
      onSave();
    }
  };

  const updateOpeningHours = (day, time) => {
    setLocation({
      ...location,
      opening_hours: {
        ...location.opening_hours,
        [day]: time
      }
    });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-gray-900">
              {isEditing ? 'Standort bearbeiten' : 'Neuen Standort hinzufügen'}
            </h2>
            <button
              onClick={onCancel}
              className="text-gray-400 hover:text-gray-600 p-2"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Basic Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Standort-Name</label>
                <input
                  type="text"
                  value={location.name}
                  onChange={(e) => setLocation({...location, name: e.target.value})}
                  className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Adresse</label>
                <input
                  type="text"
                  value={location.address}
                  onChange={(e) => setLocation({...location, address: e.target.value})}
                  className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Telefon</label>
                <input
                  type="tel"
                  value={location.phone}
                  onChange={(e) => setLocation({...location, phone: e.target.value})}
                  className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">E-Mail</label>
                <input
                  type="email"
                  value={location.email}
                  onChange={(e) => setLocation({...location, email: e.target.value})}
                  className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Beschreibung</label>
              <textarea
                value={location.description}
                onChange={(e) => setLocation({...location, description: e.target.value})}
                rows={3}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Bild-URL</label>
              <input
                type="url"
                value={location.image_url}
                onChange={(e) => setLocation({...location, image_url: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Opening Hours */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-4">Öffnungszeiten</label>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.entries(location.opening_hours || {}).map(([day, time]) => (
                  <div key={day} className="flex items-center space-x-3">
                    <span className="w-20 text-sm font-medium text-gray-700">{day}:</span>
                    <input
                      type="text"
                      value={time}
                      onChange={(e) => updateOpeningHours(day, e.target.value)}
                      className="flex-1 p-2 border border-gray-300 rounded bg-white text-gray-900 placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="z.B. 10:00 - 22:00"
                    />
                  </div>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Google Maps Embed-Code (optional)</label>
              <textarea
                value={location.maps_embed}
                onChange={(e) => setLocation({...location, maps_embed: e.target.value})}
                rows={3}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="<iframe src='...' ..."
              />
            </div>

            <div className="flex justify-end space-x-4 pt-6 border-t border-gray-200">
              <button
                type="button"
                onClick={onCancel}
                className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
              >
                Abbrechen
              </button>
              <button
                type="submit"
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                {isEditing ? 'Änderungen speichern' : 'Standort hinzufügen'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LocationsAdminSection;