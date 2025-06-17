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
  const [content, setContent] = useState({
    hero: {
      title: "JIMMY'S TAPAS BAR",
      subtitle: "an der Ostsee",
      description: "Genießen Sie authentische mediterrane Spezialitäten",
      location: "direkt an der malerischen Ostseeküste",
      background_image: "https://images.unsplash.com/photo-1656423521731-9665583f100c",
      menu_button_text: "Zur Speisekarte",
      locations_button_text: "Unsere Standorte"
    },
    features: {
      title: "Mediterrane Tradition",
      subtitle: "Erleben Sie authentische mediterrane Gastfreundschaft an der deutschen Ostseeküste",
      cards: [
        {
          title: "Authentische Tapas",
          description: "Traditionelle mediterrane Gerichte, mit Liebe zubereitet und perfekt zum Teilen",
          image_url: "https://images.pexels.com/photos/19671352/pexels-photo-19671352.jpeg"
        },
        {
          title: "Frische Paella", 
          description: "Täglich hausgemacht mit Meeresfrüchten, Gemüse oder Huhn",
          image_url: "https://images.unsplash.com/photo-1694685367640-05d6624e57f1"
        },
        {
          title: "Strandnähe",
          description: "Beide Standorte direkt an der malerischen Ostseeküste – perfekt für entspannte Stunden",
          image_url: "https://images.pexels.com/photos/32508247/pexels-photo-32508247.jpeg"
        }
      ]
    },
    specialties: {
      title: "Unsere Spezialitäten",
      cards: [
        {
          title: "Patatas Bravas",
          description: "Klassische mediterrane Kartoffeln",
          image_url: "https://images.unsplash.com/photo-1565599837634-134bc3aadce8",
          category_link: "tapas-vegetarian"
        },
        {
          title: "Paella Valenciana",
          description: "Traditionelle mediterrane Paella", 
          image_url: "https://images.pexels.com/photos/7085661/pexels-photo-7085661.jpeg",
          category_link: "tapa-paella"
        },
        {
          title: "Tapas Variación",
          description: "Auswahl mediterraner Köstlichkeiten",
          image_url: "https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg",
          category_link: "inicio"
        },
        {
          title: "Gambas al Ajillo",
          description: "Garnelen in Knoblauchöl",
          image_url: "https://images.unsplash.com/photo-1619860705243-dbef552e7118",
          category_link: "tapas-pescado"
        }
      ]
    },
    delivery: {
      title: "Jetzt auch bequem nach Hause bestellen",
      description: "Genießen Sie unsere authentischen mediterranen Spezialitäten gemütlich zu Hause.",
      description_2: "Bestellen Sie direkt über Lieferando und lassen Sie sich verwöhnen.",
      delivery_feature_title: "Schnelle Lieferung",
      delivery_feature_description: "Frisch und warm zu Ihnen",
      delivery_feature_image: "https://images.pexels.com/photos/6969962/pexels-photo-6969962.jpeg",
      button_text: "Jetzt bei Lieferando bestellen",
      button_url: "https://www.lieferando.de",
      availability_text: "Verfügbar für beide Standorte",
      authentic_feature_title: "Authentisch Mediterran",
      authentic_feature_description: "Direkt vom Küchenchef",
      authentic_feature_image: "https://images.pexels.com/photos/31748679/pexels-photo-31748679.jpeg"
    }
  });
  
  const [loading, setLoading] = useState(true);

  // Load current content from backend
  useEffect(() => {
    const loadContent = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/homepage`);
        if (response.ok) {
          const data = await response.json();
          setContent(data);
        }
      } catch (error) {
        console.error('Error loading homepage content:', error);
      } finally {
        setLoading(false);
      }
    };
    loadContent();
  }, []);

  const handleSave = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/homepage`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('adminToken')}`
        },
        body: JSON.stringify(content)
      });
      
      if (response.ok) {
        alert('Homepage-Inhalte erfolgreich gespeichert!');
      } else {
        alert('Fehler beim Speichern der Homepage-Inhalte');
      }
    } catch (error) {
      alert('Verbindungsfehler beim Speichern');
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
    <div className="space-y-8">
      {/* Hero Section Editor */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Hero-Bereich (Hauptbereich)</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Haupttitel</label>
          <input
            type="text"
            value={content.hero.title}
            onChange={(e) => setContent({
              ...content,
              hero: { ...content.hero, title: e.target.value }
            })}
            className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Untertitel</label>
          <input
            type="text"
            value={content.hero.subtitle}
            onChange={(e) => setContent({
              ...content,
              hero: { ...content.hero, subtitle: e.target.value }
            })}
            className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Beschreibung</label>
          <input
            type="text"
            value={content.hero.description}
            onChange={(e) => setContent({
              ...content,
              hero: { ...content.hero, description: e.target.value }
            })}
            className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Standort-Text</label>
          <input
            type="text"
            value={content.hero.location}
            onChange={(e) => setContent({
              ...content,
              hero: { ...content.hero, location: e.target.value }
            })}
            className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Hintergrundbild URL</label>
          <input
            type="url"
            value={content.hero.background_image}
            onChange={(e) => setContent({
              ...content,
              hero: { ...content.hero, background_image: e.target.value }
            })}
            className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Menü-Button Text</label>
          <input
            type="text"
            value={content.hero.menu_button_text}
            onChange={(e) => setContent({
              ...content,
              hero: { ...content.hero, menu_button_text: e.target.value }
            })}
            className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>
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
                value={content.features.title}
                onChange={(e) => setContent({
                  ...content,
                  features: { ...content.features, title: e.target.value }
                })}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Bereichs-Untertitel</label>
              <textarea
                value={content.features.subtitle}
                onChange={(e) => setContent({
                  ...content,
                  features: { ...content.features, subtitle: e.target.value }
                })}
                rows={2}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          
          <div className="space-y-4">
            <h4 className="font-medium text-gray-900">Features-Karten bearbeiten:</h4>
            {content.features.cards.map((card, index) => (
              <div key={index} className="grid grid-cols-1 md:grid-cols-3 gap-4 p-6 bg-gray-50 rounded-lg border">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Karte {index + 1} Titel</label>
                  <input
                    type="text"
                    value={card.title}
                    onChange={(e) => {
                      const newCards = [...content.features.cards];
                      newCards[index].title = e.target.value;
                      setContent({
                        ...content,
                        features: { ...content.features, cards: newCards }
                      });
                    }}
                    className="w-full p-3 border border-gray-300 rounded-md bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Karte {index + 1} Beschreibung</label>
                  <textarea
                    value={card.description}
                    onChange={(e) => {
                      const newCards = [...content.features.cards];
                      newCards[index].description = e.target.value;
                      setContent({
                        ...content,
                        features: { ...content.features, cards: newCards }
                      });
                    }}
                    rows={3}
                    className="w-full p-3 border border-gray-300 rounded-md bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Karte {index + 1} Bild-URL</label>
                  <input
                    type="url"
                    value={card.image_url}
                    onChange={(e) => {
                      const newCards = [...content.features.cards];
                      newCards[index].image_url = e.target.value;
                      setContent({
                        ...content,
                        features: { ...content.features, cards: newCards }
                      });
                    }}
                    className="w-full p-3 border border-gray-300 rounded-md bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  {card.image_url && (
                    <div className="mt-2">
                      <img src={card.image_url} alt="Vorschau" className="w-20 h-20 object-cover rounded border" />
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <button
          onClick={handleSave}
          disabled={saving}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {saving ? 'Speichern...' : 'Homepage-Inhalte speichern'}
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