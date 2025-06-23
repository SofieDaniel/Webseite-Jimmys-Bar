import React, { useState, useEffect } from 'react';
import HomeContentEditor from './components/HomeContentEditor';
import WebsiteTextsEditor from './components/WebsiteTextsEditor';
import MenuItemsAdminSection from './components/MenuItemsAdminSection';

// Content Management Section - FIXED VERSION
export const ContentSection = ({ user, token, apiCall }) => {
  const [activePageTab, setActivePageTab] = useState('homepage');
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  // Homepage Content
  const [homepageContent, setHomepageContent] = useState(null);
  
  // Website Texts
  const [websiteTexts, setWebsiteTexts] = useState({
    navigation: null,
    footer: null,
    buttons: null,
    general: null
  });

  useEffect(() => {
    loadContent();
  }, [activePageTab]);

  const loadContent = async () => {
    try {
      setLoading(true);
      setError('');

      if (activePageTab === 'homepage') {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/homepage`);
        if (response.ok) {
          const data = await response.json();
          console.log('Loaded homepage data:', data);
          
          // Convert MySQL format to frontend format
          const convertedData = {
            hero: {
              title: data.hero_title || 'JIMMY\'S TAPAS BAR',
              subtitle: data.hero_subtitle || 'an der Ostsee',
              description: data.hero_description || 'Genießen Sie authentische mediterrane Spezialitäten',
              location: data.hero_location || 'direkt an der malerischen Ostseeküste',
              background_image: data.hero_background_image,
              menu_button_text: data.hero_menu_button_text || 'Zur Speisekarte',
              locations_button_text: data.hero_locations_button_text || 'Unsere Standorte'
            },
            features: data.features_data || {},
            specialties: data.specialties_data || {},
            delivery: data.delivery_data || {}
          };
          
          setHomepageContent(convertedData);
        } else {
          setError('Fehler beim Laden der Homepage-Inhalte');
        }
      } else {
        // Load website texts for other sections
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/website-texts/${activePageTab}`);
        if (response.ok) {
          const data = await response.json();
          setWebsiteTexts(prev => ({
            ...prev,
            [activePageTab]: data
          }));
        } else {
          setError(`Fehler beim Laden der ${activePageTab}-Inhalte`);
        }
      }
    } catch (error) {
      console.error('Error loading content:', error);
      setError('Verbindungsfehler beim Laden der Inhalte');
    } finally {
      setLoading(false);
    }
  };

  const saveContent = async () => {
    try {
      setSaving(true);
      setError('');
      setSuccess('');

      let response;
      const token = localStorage.getItem('adminToken');
      const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      };

      if (activePageTab === 'homepage') {
        // Convert frontend format back to MySQL format
        const backendData = {
          hero_title: homepageContent.hero?.title,
          hero_subtitle: homepageContent.hero?.subtitle,
          hero_description: homepageContent.hero?.description,
          hero_location: homepageContent.hero?.location,
          hero_background_image: homepageContent.hero?.background_image,
          hero_menu_button_text: homepageContent.hero?.menu_button_text,
          hero_locations_button_text: homepageContent.hero?.locations_button_text,
          features_data: homepageContent.features,
          specialties_data: homepageContent.specialties,
          delivery_data: homepageContent.delivery
        };
        
        response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/homepage`, {
          method: 'PUT',
          headers,
          body: JSON.stringify(backendData)
        });
      } else {
        response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/website-texts/${activePageTab}`, {
          method: 'PUT',
          headers,
          body: JSON.stringify(websiteTexts[activePageTab])
        });
      }

      if (response.ok) {
        setSuccess('Inhalte erfolgreich gespeichert!');
        setTimeout(() => setSuccess(''), 3000);
      } else {
        setError('Fehler beim Speichern der Inhalte');
      }
    } catch (error) {
      console.error('Error saving content:', error);
      setError('Verbindungsfehler beim Speichern');
    } finally {
      setSaving(false);
    }
  };

  const pageNames = {
    homepage: 'Homepage',
    navigation: 'Navigation', 
    footer: 'Footer',
    buttons: 'Buttons',
    general: 'Allgemein'
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Inhalte verwalten</h1>
        <p className="text-gray-600">Bearbeiten Sie die Inhalte Ihrer Website</p>
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
          {/* Homepage Content Editor */}
          {activePageTab === 'homepage' && homepageContent && (
            <HomeContentEditor 
              content={homepageContent} 
              setContent={setHomepageContent}
              onSave={saveContent}
              saving={saving}
            />
          )}

          {/* Website Texts Editors */}
          {activePageTab !== 'homepage' && websiteTexts[activePageTab] && (
            <WebsiteTextsEditor 
              section={activePageTab}
              texts={websiteTexts[activePageTab]}
              setTexts={(newTexts) => setWebsiteTexts(prev => ({
                ...prev,
                [activePageTab]: newTexts
              }))}
              onSave={saveContent}
              saving={saving}
            />
          )}

          {/* Save Button */}
          <div className="flex justify-end">
            <button
              onClick={saveContent}
              disabled={saving || loading}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {saving ? 'Speichern...' : 'Änderungen speichern'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

// This component is now imported from /app/frontend/src/components/HomeContentEditor.js

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
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[9999] p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-gray-900">
              {isEditing ? 'Gericht bearbeiten' : 'Neues Gericht hinzufügen'}
            </h2>
            <button
              onClick={onCancel}
              className="text-gray-400 hover:text-gray-600 p-2 hover:bg-gray-100 rounded-full"
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