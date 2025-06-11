import React, { useState, useEffect } from 'react';

// Content Management Section
export const ContentSection = ({ user, token, apiCall }) => {
  const [pages, setPages] = useState({
    home: { sections: [] },
    locations: { sections: [] },
    about: { sections: [] },
    contact: { sections: [] },
    privacy: { sections: [] },
    imprint: { sections: [] }
  });
  const [activePageTab, setActivePageTab] = useState('home');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    loadPageContent();
  }, [activePageTab]);

  const loadPageContent = async () => {
    try {
      setLoading(true);
      const response = await apiCall(`/content/${activePageTab}`);
      if (response.ok) {
        const data = await response.json();
        setPages(prev => ({
          ...prev,
          [activePageTab]: { sections: data }
        }));
      }
    } catch (error) {
      setError('Fehler beim Laden der Inhalte');
    } finally {
      setLoading(false);
    }
  };

  const saveContent = async (section, content) => {
    try {
      setSaving(true);
      const response = await apiCall(`/content/${activePageTab}/${section}`, 'PUT', {
        content: content,
        images: []
      });
      
      if (response.ok) {
        setSuccess('Inhalt erfolgreich gespeichert!');
        setTimeout(() => setSuccess(''), 3000);
        loadPageContent();
      } else {
        setError('Fehler beim Speichern');
      }
    } catch (error) {
      setError('Verbindungsfehler beim Speichern');
    } finally {
      setSaving(false);
    }
  };

  const pageNames = {
    home: 'Startseite',
    locations: 'Standorte',
    about: 'Über uns',
    contact: 'Kontakt',
    privacy: 'Datenschutz',
    imprint: 'Impressum'
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Inhalte verwalten</h1>
        <p className="text-gray-600">Bearbeiten Sie die Inhalte Ihrer Website-Seiten</p>
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

      {/* Page Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {Object.entries(pageNames).map(([key, name]) => (
            <button
              key={key}
              onClick={() => setActivePageTab(key)}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activePageTab === key
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {name}
            </button>
          ))}
        </nav>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-32">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Content Editors */}
          {activePageTab === 'home' && <HomeContentEditor saveContent={saveContent} saving={saving} />}
          {activePageTab === 'locations' && <LocationsContentEditor saveContent={saveContent} saving={saving} />}
          {activePageTab === 'about' && <AboutContentEditor saveContent={saveContent} saving={saving} />}
          {activePageTab === 'contact' && <ContactContentEditor saveContent={saveContent} saving={saving} />}
          {activePageTab === 'privacy' && <PrivacyContentEditor saveContent={saveContent} saving={saving} />}
          {activePageTab === 'imprint' && <ImprintContentEditor saveContent={saveContent} saving={saving} />}
        </div>
      )}
    </div>
  );
};

// Home Page Content Editor
const HomeContentEditor = ({ saveContent, saving }) => {
  const [heroContent, setHeroContent] = useState({
    title: 'AUTÉNTICO SABOR ESPAÑOL',
    subtitle: 'an der Ostsee',
    description: 'Genießen Sie authentische spanische Spezialitäten',
    location: 'direkt an der malerischen Ostseeküste'
  });

  const [featuresContent, setFeaturesContent] = useState({
    sectionTitle: 'Spanische Tradition',
    sectionSubtitle: 'Erleben Sie authentische spanische Gastfreundschaft an der deutschen Ostseeküste',
    features: [
      {
        title: 'Authentische Tapas',
        description: 'Traditionelle spanische Gerichte, mit Liebe zubereitet und perfekt zum Teilen'
      },
      {
        title: 'Frische Paella',
        description: 'Täglich hausgemacht mit Meeresfrüchten, Gemüse oder Huhn'
      },
      {
        title: 'Strandnähe',
        description: 'Beide Standorte direkt an der malerischen Ostseeküste – perfekt für entspannte Stunden'
      }
    ]
  });

  return (
    <div className="space-y-8">
      {/* Hero Section Editor */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Hero-Bereich (Hauptbereich)</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Haupttitel</label>
            <input
              type="text"
              value={heroContent.title}
              onChange={(e) => setHeroContent({...heroContent, title: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Untertitel</label>
            <input
              type="text"
              value={heroContent.subtitle}
              onChange={(e) => setHeroContent({...heroContent, subtitle: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Beschreibung</label>
            <input
              type="text"
              value={heroContent.description}
              onChange={(e) => setHeroContent({...heroContent, description: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Standort-Text</label>
            <input
              type="text"
              value={heroContent.location}
              onChange={(e) => setHeroContent({...heroContent, location: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
        <button
          onClick={() => saveContent('hero', heroContent)}
          disabled={saving}
          className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {saving ? 'Speichern...' : 'Hero-Bereich speichern'}
        </button>
      </div>

      {/* Features Section Editor */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Features-Bereich</h3>
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Bereichstitel</label>
              <input
                type="text"
                value={featuresContent.sectionTitle}
                onChange={(e) => setFeaturesContent({...featuresContent, sectionTitle: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Bereichs-Untertitel</label>
              <input
                type="text"
                value={featuresContent.sectionSubtitle}
                onChange={(e) => setFeaturesContent({...featuresContent, sectionSubtitle: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          
          <div className="space-y-4">
            <h4 className="font-medium text-gray-900">Features bearbeiten:</h4>
            {featuresContent.features.map((feature, index) => (
              <div key={index} className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 bg-gray-50 rounded-lg">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Feature {index + 1} Titel</label>
                  <input
                    type="text"
                    value={feature.title}
                    onChange={(e) => {
                      const newFeatures = [...featuresContent.features];
                      newFeatures[index].title = e.target.value;
                      setFeaturesContent({...featuresContent, features: newFeatures});
                    }}
                    className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Feature {index + 1} Beschreibung</label>
                  <textarea
                    value={feature.description}
                    onChange={(e) => {
                      const newFeatures = [...featuresContent.features];
                      newFeatures[index].description = e.target.value;
                      setFeaturesContent({...featuresContent, features: newFeatures});
                    }}
                    rows={2}
                    className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
        <button
          onClick={() => saveContent('features', featuresContent)}
          disabled={saving}
          className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {saving ? 'Speichern...' : 'Features-Bereich speichern'}
        </button>
      </div>
    </div>
  );
};

// Menu Management Section
export const MenuSection = ({ user, token, apiCall }) => {
  const [menuItems, setMenuItems] = useState([]);
  const [categories, setCategories] = useState([
    'inicio', 'salat', 'kleiner-salat', 'tapa-paella', 'tapas-vegetarian', 
    'tapas-pollo', 'tapas-carne', 'tapas-pescado', 'kroketten', 'pasta', 
    'pizza', 'snacks', 'dessert', 'helados'
  ]);
  const [selectedCategory, setSelectedCategory] = useState('alle');
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [newItem, setNewItem] = useState({
    name: '',
    description: '',
    price: '',
    category: 'inicio',
    details: '',
    vegan: false,
    vegetarian: false,
    glutenfree: false,
    order_index: 0
  });

  useEffect(() => {
    loadMenuItems();
  }, []);

  const loadMenuItems = async () => {
    try {
      setLoading(true);
      const response = await apiCall('/menu/items');
      if (response.ok) {
        const data = await response.json();
        setMenuItems(data);
      }
    } catch (error) {
      console.error('Error loading menu items:', error);
    } finally {
      setLoading(false);
    }
  };

  const saveMenuItem = async (itemData) => {
    try {
      setSaving(true);
      const response = await apiCall('/menu/items', 'POST', itemData);
      if (response.ok) {
        loadMenuItems();
        setShowAddForm(false);
        setNewItem({
          name: '',
          description: '',
          price: '',
          category: 'inicio',
          details: '',
          vegan: false,
          vegetarian: false,
          glutenfree: false,
          order_index: 0
        });
      }
    } catch (error) {
      console.error('Error saving menu item:', error);
    } finally {
      setSaving(false);
    }
  };

  const updateMenuItem = async (itemId, itemData) => {
    try {
      setSaving(true);
      const response = await apiCall(`/menu/items/${itemId}`, 'PUT', itemData);
      if (response.ok) {
        loadMenuItems();
        setEditingItem(null);
      }
    } catch (error) {
      console.error('Error updating menu item:', error);
    } finally {
      setSaving(false);
    }
  };

  const deleteMenuItem = async (itemId) => {
    if (window.confirm('Sind Sie sicher, dass Sie dieses Gericht löschen möchten?')) {
      try {
        const response = await apiCall(`/menu/items/${itemId}`, 'DELETE');
        if (response.ok) {
          loadMenuItems();
        }
      } catch (error) {
        console.error('Error deleting menu item:', error);
      }
    }
  };

  const filteredItems = selectedCategory === 'alle' 
    ? menuItems 
    : menuItems.filter(item => item.category === selectedCategory);

  const categoryNames = {
    'alle': 'Alle Kategorien',
    'inicio': 'Inicio',
    'salat': 'Salate',
    'kleiner-salat': 'Kleine Salate',
    'tapa-paella': 'Tapa Paella',
    'tapas-vegetarian': 'Vegetarische Tapas',
    'tapas-pollo': 'Tapas de Pollo',
    'tapas-carne': 'Tapas de Carne',
    'tapas-pescado': 'Tapas de Pescado',
    'kroketten': 'Kroketten',
    'pasta': 'Pasta',
    'pizza': 'Pizza',
    'snacks': 'Snacks',
    'dessert': 'Desserts',
    'helados': 'Helados'
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Speisekarte verwalten</h1>
          <p className="text-gray-600">Gerichte hinzufügen, bearbeiten und organisieren</p>
        </div>
        <button
          onClick={() => setShowAddForm(true)}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 flex items-center"
        >
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Neues Gericht
        </button>
      </div>

      {/* Category Filter */}
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <div className="flex flex-wrap gap-2">
          {Object.entries(categoryNames).map(([key, name]) => (
            <button
              key={key}
              onClick={() => setSelectedCategory(key)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedCategory === key
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {name}
            </button>
          ))}
        </div>
      </div>

      {/* Menu Items Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredItems.map((item) => (
          <div key={item.id} className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-shadow">
            <div className="flex justify-between items-start mb-4">
              <div className="flex-1">
                <h3 className="font-semibold text-gray-900 mb-1">{item.name}</h3>
                <p className="text-sm text-gray-600 mb-2">{item.description}</p>
                <div className="flex items-center space-x-2">
                  <span className="text-lg font-bold text-blue-600">{item.price} €</span>
                  {item.vegan && <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">Vegan</span>}
                  {item.vegetarian && <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">Vegetarisch</span>}
                  {item.glutenfree && <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">Glutenfrei</span>}
                </div>
                <p className="text-xs text-gray-500 mt-2">Kategorie: {categoryNames[item.category]}</p>
              </div>
              <div className="flex space-x-2 ml-4">
                <button
                  onClick={() => setEditingItem(item)}
                  className="text-blue-600 hover:text-blue-800 p-1"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
                <button
                  onClick={() => deleteMenuItem(item.id)}
                  className="text-red-600 hover:text-red-800 p-1"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Add/Edit Item Modal */}
      {(showAddForm || editingItem) && (
        <MenuItemModal
          item={editingItem || newItem}
          categories={categories}
          categoryNames={categoryNames}
          onSave={editingItem ? updateMenuItem : saveMenuItem}
          onCancel={() => {
            setShowAddForm(false);
            setEditingItem(null);
          }}
          saving={saving}
          isEditing={!!editingItem}
        />
      )}
    </div>
  );
};

// Menu Item Modal Component
const MenuItemModal = ({ item, categories, categoryNames, onSave, onCancel, saving, isEditing }) => {
  const [formData, setFormData] = useState(item);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (isEditing) {
      onSave(item.id, formData);
    } else {
      onSave(formData);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-gray-900">
              {isEditing ? 'Gericht bearbeiten' : 'Neues Gericht hinzufügen'}
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
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Preis</label>
                <input
                  type="text"
                  value={formData.price}
                  onChange={(e) => setFormData({...formData, price: e.target.value})}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="9,90"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Beschreibung</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
                rows={3}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Details</label>
              <textarea
                value={formData.details}
                onChange={(e) => setFormData({...formData, details: e.target.value})}
                rows={4}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Detaillierte Beschreibung des Gerichts..."
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Kategorie</label>
                <select
                  value={formData.category}
                  onChange={(e) => setFormData({...formData, category: e.target.value})}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  {categories.map(cat => (
                    <option key={cat} value={cat}>{categoryNames[cat]}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Reihenfolge</label>
                <input
                  type="number"
                  value={formData.order_index}
                  onChange={(e) => setFormData({...formData, order_index: parseInt(e.target.value)})}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">Eigenschaften</label>
              <div className="space-y-2">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.vegan}
                    onChange={(e) => setFormData({...formData, vegan: e.target.checked})}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">Vegan</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.vegetarian}
                    onChange={(e) => setFormData({...formData, vegetarian: e.target.checked})}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">Vegetarisch</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.glutenfree}
                    onChange={(e) => setFormData({...formData, glutenfree: e.target.checked})}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">Glutenfrei</span>
                </label>
              </div>
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
                disabled={saving}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                {saving ? 'Speichern...' : (isEditing ? 'Aktualisieren' : 'Hinzufügen')}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

// Placeholder components for other content editors
const LocationsContentEditor = ({ saveContent, saving }) => (
  <div className="bg-white rounded-lg border border-gray-200 p-6">
    <h3 className="text-lg font-semibold text-gray-900 mb-4">Standorte bearbeiten</h3>
    <p className="text-gray-600">Standort-Editor wird hier implementiert...</p>
  </div>
);

const AboutContentEditor = ({ saveContent, saving }) => (
  <div className="bg-white rounded-lg border border-gray-200 p-6">
    <h3 className="text-lg font-semibold text-gray-900 mb-4">Über uns bearbeiten</h3>
    <p className="text-gray-600">Über uns-Editor wird hier implementiert...</p>
  </div>
);

const ContactContentEditor = ({ saveContent, saving }) => (
  <div className="bg-white rounded-lg border border-gray-200 p-6">
    <h3 className="text-lg font-semibold text-gray-900 mb-4">Kontakt bearbeiten</h3>
    <p className="text-gray-600">Kontakt-Editor wird hier implementiert...</p>
  </div>
);

const PrivacyContentEditor = ({ saveContent, saving }) => (
  <div className="bg-white rounded-lg border border-gray-200 p-6">
    <h3 className="text-lg font-semibold text-gray-900 mb-4">Datenschutz bearbeiten</h3>
    <p className="text-gray-600">Datenschutz-Editor wird hier implementiert...</p>
  </div>
);

const ImprintContentEditor = ({ saveContent, saving }) => (
  <div className="bg-white rounded-lg border border-gray-200 p-6">
    <h3 className="text-lg font-semibold text-gray-900 mb-4">Impressum bearbeiten</h3>
    <p className="text-gray-600">Impressum-Editor wird hier implementiert...</p>
  </div>
);