import React, { useState, useEffect } from 'react';

// ===============================================
// HOMEPAGE CONTENT MANAGEMENT
// ===============================================

export const HomepageContentSection = ({ user, token, apiCall }) => {
  const [activeTab, setActiveTab] = useState('hero');
  const [heroData, setHeroData] = useState(null);
  const [featuresData, setFeaturesData] = useState(null);
  const [galleryData, setGalleryData] = useState(null);
  const [lieferandoData, setLieferandoData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    loadHomepageContent();
  }, [activeTab]);

  const loadHomepageContent = async () => {
    setLoading(true);
    try {
      if (activeTab === 'hero') {
        const response = await apiCall('/cms/homepage/hero');
        if (response.ok) {
          const data = await response.json();
          setHeroData(data);
        }
      } else if (activeTab === 'features') {
        const response = await apiCall('/cms/homepage/features');
        if (response.ok) {
          const data = await response.json();
          setFeaturesData(data);
        }
      } else if (activeTab === 'gallery') {
        const response = await apiCall('/cms/homepage/food-gallery');
        if (response.ok) {
          const data = await response.json();
          setGalleryData(data);
        }
      } else if (activeTab === 'lieferando') {
        const response = await apiCall('/cms/homepage/lieferando');
        if (response.ok) {
          const data = await response.json();
          setLieferandoData(data);
        }
      }
    } catch (error) {
      setError('Fehler beim Laden der Inhalte');
    } finally {
      setLoading(false);
    }
  };

  const saveContent = async (endpoint, data) => {
    setLoading(true);
    try {
      const response = await apiCall(endpoint, 'PUT', data);
      if (response.ok) {
        setSuccess('Inhalte erfolgreich gespeichert!');
        setTimeout(() => setSuccess(''), 3000);
      } else {
        setError('Fehler beim Speichern');
      }
    } catch (error) {
      setError('Fehler beim Speichern');
    } finally {
      setLoading(false);
    }
  };

  const MultiLanguageInput = ({ label, value, onChange, type = 'text', rows = null }) => (
    <div className="space-y-3">
      <label className="block text-sm font-medium text-gray-700">{label}</label>
      <div className="grid grid-cols-3 gap-4">
        {['de', 'en', 'es'].map(lang => (
          <div key={lang}>
            <label className="block text-xs text-gray-500 mb-1">
              {lang.toUpperCase()}
            </label>
            {rows ? (
              <textarea
                rows={rows}
                value={value?.[lang] || ''}
                onChange={(e) => onChange({...value, [lang]: e.target.value})}
                className="w-full p-2 border border-gray-300 rounded-md text-sm text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            ) : (
              <input
                type={type}
                value={value?.[lang] || ''}
                onChange={(e) => onChange({...value, [lang]: e.target.value})}
                className="w-full p-2 border border-gray-300 rounded-md text-sm text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            )}
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Homepage Inhalte</h1>
        <p className="text-gray-600">Verwalten Sie alle Inhalte der Startseite in allen Sprachen</p>
      </div>

      {success && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
          {success}
        </div>
      )}

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'hero', name: 'Hero Section' },
            { id: 'features', name: 'Features' },
            { id: 'gallery', name: 'Food Gallery' },
            { id: 'lieferando', name: 'Lieferando' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {tab.name}
            </button>
          ))}
        </nav>
      </div>

      {loading && (
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        </div>
      )}

      {/* Hero Section Tab */}
      {activeTab === 'hero' && heroData && (
        <div className="bg-white rounded-lg shadow p-6 space-y-6">
          <h2 className="text-xl font-semibold">Hero Section</h2>
          
          <MultiLanguageInput
            label="Haupttitel"
            value={heroData.title}
            onChange={(value) => setHeroData({...heroData, title: value})}
          />

          <MultiLanguageInput
            label="Untertitel"
            value={heroData.subtitle}
            onChange={(value) => setHeroData({...heroData, subtitle: value})}
          />

          <MultiLanguageInput
            label="Beschreibung"
            value={heroData.description}
            onChange={(value) => setHeroData({...heroData, description: value})}
            rows={3}
          />

          <MultiLanguageInput
            label="Standort Text"
            value={heroData.location_text}
            onChange={(value) => setHeroData({...heroData, location_text: value})}
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Hintergrundbild URL</label>
            <input
              type="url"
              value={heroData.background_image || ''}
              onChange={(e) => setHeroData({...heroData, background_image: e.target.value})}
              className="w-full p-2 border border-gray-300 rounded-md text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <MultiLanguageInput
            label="Menü Button Text"
            value={heroData.menu_button_text}
            onChange={(value) => setHeroData({...heroData, menu_button_text: value})}
          />

          <MultiLanguageInput
            label="Standorte Button Text"
            value={heroData.locations_button_text}
            onChange={(value) => setHeroData({...heroData, locations_button_text: value})}
          />

          <button
            onClick={() => saveContent('/cms/homepage/hero', heroData)}
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Speichern...' : 'Hero Section Speichern'}
          </button>
        </div>
      )}

      {/* Features Section Tab */}
      {activeTab === 'features' && featuresData && (
        <div className="bg-white rounded-lg shadow p-6 space-y-6">
          <h2 className="text-xl font-semibold">Features Section</h2>
          
          <MultiLanguageInput
            label="Sektion Titel"
            value={featuresData.section_title}
            onChange={(value) => setFeaturesData({...featuresData, section_title: value})}
          />

          <MultiLanguageInput
            label="Sektion Beschreibung"
            value={featuresData.section_description}
            onChange={(value) => setFeaturesData({...featuresData, section_description: value})}
            rows={3}
          />

          <div className="space-y-4">
            <h3 className="text-lg font-medium">Features</h3>
            {featuresData.features?.map((feature, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4 space-y-4">
                <h4 className="font-medium">Feature {index + 1}</h4>
                
                <MultiLanguageInput
                  label="Titel"
                  value={feature.title}
                  onChange={(value) => {
                    const newFeatures = [...featuresData.features];
                    newFeatures[index] = {...feature, title: value};
                    setFeaturesData({...featuresData, features: newFeatures});
                  }}
                />

                <MultiLanguageInput
                  label="Beschreibung"
                  value={feature.description}
                  onChange={(value) => {
                    const newFeatures = [...featuresData.features];
                    newFeatures[index] = {...feature, description: value};
                    setFeaturesData({...featuresData, features: newFeatures});
                  }}
                  rows={3}
                />

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Bild URL</label>
                  <input
                    type="url"
                    value={feature.image_url || ''}
                    onChange={(e) => {
                      const newFeatures = [...featuresData.features];
                      newFeatures[index] = {...feature, image_url: e.target.value};
                      setFeaturesData({...featuresData, features: newFeatures});
                    }}
                    className="w-full p-2 border border-gray-300 rounded-md text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
            ))}
          </div>

          <button
            onClick={() => saveContent('/cms/homepage/features', featuresData)}
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Speichern...' : 'Features Speichern'}
          </button>
        </div>
      )}

      {/* Gallery Section Tab */}
      {activeTab === 'gallery' && galleryData && (
        <div className="bg-white rounded-lg shadow p-6 space-y-6">
          <h2 className="text-xl font-semibold">Food Gallery</h2>
          
          <MultiLanguageInput
            label="Sektion Titel"
            value={galleryData.section_title}
            onChange={(value) => setGalleryData({...galleryData, section_title: value})}
          />

          <div className="space-y-4">
            <h3 className="text-lg font-medium">Gallery Items</h3>
            {galleryData.gallery_items?.map((item, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4 space-y-4">
                <h4 className="font-medium">Item {index + 1}</h4>
                
                <MultiLanguageInput
                  label="Name"
                  value={item.name}
                  onChange={(value) => {
                    const newItems = [...galleryData.gallery_items];
                    newItems[index] = {...item, name: value};
                    setGalleryData({...galleryData, gallery_items: newItems});
                  }}
                />

                <MultiLanguageInput
                  label="Beschreibung"
                  value={item.description}
                  onChange={(value) => {
                    const newItems = [...galleryData.gallery_items];
                    newItems[index] = {...item, description: value};
                    setGalleryData({...galleryData, gallery_items: newItems});
                  }}
                />

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Bild URL</label>
                  <input
                    type="url"
                    value={item.image_url || ''}
                    onChange={(e) => {
                      const newItems = [...galleryData.gallery_items];
                      newItems[index] = {...item, image_url: e.target.value};
                      setGalleryData({...galleryData, gallery_items: newItems});
                    }}
                    className="w-full p-2 border border-gray-300 rounded-md text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Kategorie Link</label>
                  <input
                    type="text"
                    value={item.category_link || ''}
                    onChange={(e) => {
                      const newItems = [...galleryData.gallery_items];
                      newItems[index] = {...item, category_link: e.target.value};
                      setGalleryData({...galleryData, gallery_items: newItems});
                    }}
                    className="w-full p-2 border border-gray-300 rounded-md text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
            ))}
          </div>

          <button
            onClick={() => saveContent('/cms/homepage/food-gallery', galleryData)}
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Speichern...' : 'Gallery Speichern'}
          </button>
        </div>
      )}

      {/* Lieferando Section Tab */}
      {activeTab === 'lieferando' && lieferandoData && (
        <div className="bg-white rounded-lg shadow p-6 space-y-6">
          <h2 className="text-xl font-semibold">Lieferando Section</h2>
          
          <MultiLanguageInput
            label="Titel"
            value={lieferandoData.title}
            onChange={(value) => setLieferandoData({...lieferandoData, title: value})}
          />

          <MultiLanguageInput
            label="Beschreibung"
            value={lieferandoData.description}
            onChange={(value) => setLieferandoData({...lieferandoData, description: value})}
            rows={3}
          />

          <MultiLanguageInput
            label="Button Text"
            value={lieferandoData.button_text}
            onChange={(value) => setLieferandoData({...lieferandoData, button_text: value})}
          />

          <MultiLanguageInput
            label="Lieferung Text"
            value={lieferandoData.delivery_text}
            onChange={(value) => setLieferandoData({...lieferandoData, delivery_text: value})}
          />

          <MultiLanguageInput
            label="Authentisch Text"
            value={lieferandoData.authentic_text}
            onChange={(value) => setLieferandoData({...lieferandoData, authentic_text: value})}
          />

          <MultiLanguageInput
            label="Verfügbarkeit Text"
            value={lieferandoData.availability_text}
            onChange={(value) => setLieferandoData({...lieferandoData, availability_text: value})}
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Lieferando URL</label>
            <input
              type="url"
              value={lieferandoData.lieferando_url || ''}
              onChange={(e) => setLieferandoData({...lieferandoData, lieferando_url: e.target.value})}
              className="w-full p-2 border border-gray-300 rounded-md text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <button
            onClick={() => saveContent('/cms/homepage/lieferando', lieferandoData)}
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Speichern...' : 'Lieferando Section Speichern'}
          </button>
        </div>
      )}
    </div>
  );
};

// ===============================================
// LOCATIONS MANAGEMENT
// ===============================================

export const LocationsManagementSection = ({ user, token, apiCall }) => {
  const [locations, setLocations] = useState([]);
  const [editingLocation, setEditingLocation] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    loadLocations();
  }, []);

  const loadLocations = async () => {
    setLoading(true);
    try {
      const response = await apiCall('/cms/locations');
      if (response.ok) {
        const data = await response.json();
        setLocations(data);
      }
    } catch (error) {
      setError('Fehler beim Laden der Standorte');
    } finally {
      setLoading(false);
    }
  };

  const MultiLanguageInput = ({ label, value, onChange, type = 'text', rows = null }) => (
    <div className="space-y-3">
      <label className="block text-sm font-medium text-gray-700">{label}</label>
      <div className="grid grid-cols-3 gap-4">
        {['de', 'en', 'es'].map(lang => (
          <div key={lang}>
            <label className="block text-xs text-gray-500 mb-1">
              {lang.toUpperCase()}
            </label>
            {rows ? (
              <textarea
                rows={rows}
                value={value?.[lang] || ''}
                onChange={(e) => onChange({...value, [lang]: e.target.value})}
                className="w-full p-2 border border-gray-300 rounded-md text-sm"
              />
            ) : (
              <input
                type={type}
                value={value?.[lang] || ''}
                onChange={(e) => onChange({...value, [lang]: e.target.value})}
                className="w-full p-2 border border-gray-300 rounded-md text-sm"
              />
            )}
          </div>
        ))}
      </div>
    </div>
  );

  const newLocation = {
    id: `location-${Date.now()}`,
    name: { de: '', en: '', es: '' },
    address: { de: '', en: '', es: '' },
    phone: '',
    email: '',
    opening_hours: {
      monday: { de: '', en: '', es: '' },
      tuesday: { de: '', en: '', es: '' },
      wednesday: { de: '', en: '', es: '' },
      thursday: { de: '', en: '', es: '' },
      friday: { de: '', en: '', es: '' },
      saturday: { de: '', en: '', es: '' },
      sunday: { de: '', en: '', es: '' }
    },
    description: { de: '', en: '', es: '' },
    features: [],
    image_url: '',
    google_maps_url: '',
    order: 0,
    is_active: true
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Standorte Verwaltung</h1>
          <p className="text-gray-600">Verwalten Sie alle Restaurant-Standorte</p>
        </div>
        <button
          onClick={() => {
            setEditingLocation(newLocation);
            setShowForm(true);
          }}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          + Neuer Standort
        </button>
      </div>

      {success && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
          {success}
        </div>
      )}

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {loading && (
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        </div>
      )}

      {/* Locations List */}
      {!showForm && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Standort
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Adresse
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Kontakt
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Aktionen
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {locations.map((location, index) => (
                <tr key={index}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {location.name?.de}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      {location.address?.de}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      {location.phone}<br/>
                      {location.email}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button
                      onClick={() => {
                        setEditingLocation(location);
                        setShowForm(true);
                      }}
                      className="text-blue-600 hover:text-blue-900 mr-4"
                    >
                      Bearbeiten
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Location Form */}
      {showForm && editingLocation && (
        <div className="bg-white rounded-lg shadow p-6 space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-semibold">
              {editingLocation.id.includes('location-') && editingLocation.id.includes(Date.now().toString().slice(-5)) ? 'Neuer Standort' : 'Standort bearbeiten'}
            </h2>
            <button
              onClick={() => {
                setShowForm(false);
                setEditingLocation(null);
              }}
              className="text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          </div>

          <MultiLanguageInput
            label="Standort Name"
            value={editingLocation.name}
            onChange={(value) => setEditingLocation({...editingLocation, name: value})}
          />

          <MultiLanguageInput
            label="Adresse"
            value={editingLocation.address}
            onChange={(value) => setEditingLocation({...editingLocation, address: value})}
          />

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Telefon</label>
              <input
                type="tel"
                value={editingLocation.phone || ''}
                onChange={(e) => setEditingLocation({...editingLocation, phone: e.target.value})}
                className="w-full p-2 border border-gray-300 rounded-md text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">E-Mail</label>
              <input
                type="email"
                value={editingLocation.email || ''}
                onChange={(e) => setEditingLocation({...editingLocation, email: e.target.value})}
                className="w-full p-2 border border-gray-300 rounded-md text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <MultiLanguageInput
            label="Beschreibung"
            value={editingLocation.description}
            onChange={(value) => setEditingLocation({...editingLocation, description: value})}
            rows={3}
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Bild URL</label>
            <input
              type="url"
              value={editingLocation.image_url || ''}
              onChange={(e) => setEditingLocation({...editingLocation, image_url: e.target.value})}
              className="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Google Maps URL</label>
            <input
              type="url"
              value={editingLocation.google_maps_url || ''}
              onChange={(e) => setEditingLocation({...editingLocation, google_maps_url: e.target.value})}
              className="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>

          <div className="flex space-x-4">
            <button
              onClick={() => {
                setShowForm(false);
                setEditingLocation(null);
              }}
              className="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400"
            >
              Abbrechen
            </button>
            <button
              disabled={loading}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Speichern...' : 'Speichern'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

// ===============================================
// ENHANCED MENU MANAGEMENT
// ===============================================

export const EnhancedMenuSection = ({ user, token, apiCall }) => {
  const [categories, setCategories] = useState([]);
  const [menuItems, setMenuItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    loadMenuData();
  }, []);

  const loadMenuData = async () => {
    setLoading(true);
    try {
      const [categoriesResponse, itemsResponse] = await Promise.all([
        apiCall('/cms/menu/categories'),
        apiCall('/cms/menu/items')
      ]);

      if (categoriesResponse.ok) {
        const categoriesData = await categoriesResponse.json();
        setCategories(categoriesData);
      }

      if (itemsResponse.ok) {
        const itemsData = await itemsResponse.json();
        setMenuItems(itemsData);
      }
    } catch (error) {
      setError('Fehler beim Laden der Menü-Daten');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Erweiterte Speisekarten-Verwaltung</h1>
        <p className="text-gray-600">Verwalten Sie Kategorien und Menü-Items mit vollständiger Mehrsprachigkeit</p>
      </div>

      {success && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
          {success}
        </div>
      )}

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {loading && (
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        </div>
      )}

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Menü Kategorien</h2>
        <p className="text-gray-600 mb-4">
          Diese Sektion ist in Entwicklung. Hier können Sie Kategorien verwalten und neue hinzufügen.
        </p>
        <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
          + Neue Kategorie
        </button>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Menü Items</h2>
        <p className="text-gray-600 mb-4">
          Diese Sektion ist in Entwicklung. Hier können Sie alle Menü-Items mit detaillierten Informationen verwalten.
        </p>
        <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
          + Neues Gericht
        </button>
      </div>
    </div>
  );
};

// ===============================================
// ABOUT US CONTENT MANAGEMENT
// ===============================================

export const AboutContentSection = ({ user, token, apiCall }) => {
  const [aboutData, setAboutData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    loadAboutContent();
  }, []);

  const loadAboutContent = async () => {
    setLoading(true);
    try {
      const response = await apiCall('/cms/about');
      if (response.ok) {
        const data = await response.json();
        setAboutData(data);
      }
    } catch (error) {
      setError('Fehler beim Laden der Über-uns Inhalte');
    } finally {
      setLoading(false);
    }
  };

  const MultiLanguageInput = ({ label, value, onChange, type = 'text', rows = null }) => (
    <div className="space-y-3">
      <label className="block text-sm font-medium text-gray-700">{label}</label>
      <div className="grid grid-cols-3 gap-4">
        {['de', 'en', 'es'].map(lang => (
          <div key={lang}>
            <label className="block text-xs text-gray-500 mb-1">
              {lang.toUpperCase()}
            </label>
            {rows ? (
              <textarea
                rows={rows}
                value={value?.[lang] || ''}
                onChange={(e) => onChange({...value, [lang]: e.target.value})}
                className="w-full p-2 border border-gray-300 rounded-md text-sm"
              />
            ) : (
              <input
                type={type}
                value={value?.[lang] || ''}
                onChange={(e) => onChange({...value, [lang]: e.target.value})}
                className="w-full p-2 border border-gray-300 rounded-md text-sm"
              />
            )}
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Über uns Inhalte</h1>
        <p className="text-gray-600">Verwalten Sie alle Inhalte der Über-uns Seite</p>
      </div>

      {success && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
          {success}
        </div>
      )}

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {loading && (
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        </div>
      )}

      {aboutData && (
        <div className="bg-white rounded-lg shadow p-6 space-y-6">
          <h2 className="text-xl font-semibold">Über uns Seite</h2>
          
          <MultiLanguageInput
            label="Hero Titel"
            value={aboutData.hero_title}
            onChange={(value) => setAboutData({...aboutData, hero_title: value})}
          />

          <MultiLanguageInput
            label="Hero Beschreibung"
            value={aboutData.hero_description}
            onChange={(value) => setAboutData({...aboutData, hero_description: value})}
            rows={3}
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Hero Bild URL</label>
            <input
              type="url"
              value={aboutData.hero_image || ''}
              onChange={(e) => setAboutData({...aboutData, hero_image: e.target.value})}
              className="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>

          <MultiLanguageInput
            label="Story Titel"
            value={aboutData.story_title}
            onChange={(value) => setAboutData({...aboutData, story_title: value})}
          />

          <MultiLanguageInput
            label="Story Inhalt"
            value={aboutData.story_content}
            onChange={(value) => setAboutData({...aboutData, story_content: value})}
            rows={6}
          />

          <MultiLanguageInput
            label="Team Titel"
            value={aboutData.team_title}
            onChange={(value) => setAboutData({...aboutData, team_title: value})}
          />

          <MultiLanguageInput
            label="Werte Titel"
            value={aboutData.values_title}
            onChange={(value) => setAboutData({...aboutData, values_title: value})}
          />

          <button
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Speichern...' : 'Über uns Inhalte Speichern'}
          </button>
        </div>
      )}
    </div>
  );
};