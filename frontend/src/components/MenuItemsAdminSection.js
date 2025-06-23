import React, { useState, useEffect } from 'react';

const MenuItemsAdminSection = () => {
  const [menuItems, setMenuItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingItem, setEditingItem] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [showForm, setShowForm] = useState(false);

  // Categories for dropdown
  const categories = [
    'Vorspeisen', 'Salate', 'Paella', 'Vegetarisch', 'Hähnchen', 'Fleisch', 
    'Fisch', 'Kroketten', 'Pasta', 'Pizza', 'Snacks', 'Dessert', 
    'Heißgetränke', 'Softdrinks', 'Limonaden', 'Säfte', 'Schorlen', 
    'Aperitifs', 'Bier', 'Weine', 'Shots', 'Gin', 'Whiskey', 'Brandy', 
    'Cocktails', 'Sangria'
  ];

  const loadMenuItems = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/menu/items`);
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

  useEffect(() => {
    loadMenuItems();
  }, []);

  const handleSave = async (itemData) => {
    try {
      const token = localStorage.getItem('auth_token');
      const url = editingItem 
        ? `${process.env.REACT_APP_BACKEND_URL}/api/menu/items/${editingItem.id}`
        : `${process.env.REACT_APP_BACKEND_URL}/api/menu/items`;
      
      const method = editingItem ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(itemData)
      });

      if (response.ok) {
        loadMenuItems();
        setEditingItem(null);
        setShowForm(false);
      }
    } catch (error) {
      console.error('Error saving menu item:', error);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Möchten Sie diesen Artikel wirklich löschen?')) return;
    
    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/menu/items/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        loadMenuItems();
      }
    } catch (error) {
      console.error('Error deleting menu item:', error);
    }
  };

  const filteredItems = menuItems.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = !selectedCategory || item.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-warm-beige"></div>
      </div>
    );
  }

  return (
    <div className="w-full h-full min-h-screen bg-gray-50 p-6">
      <div className="max-w-full mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-serif text-gray-900">🍽️ Speisekarte verwalten</h2>
          <button
            onClick={() => {
              setEditingItem(null);
              setShowForm(true);
            }}
            className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Neues Gericht hinzufügen
          </button>
        </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <input
            type="text"
            placeholder="Suchen nach Name oder Beschreibung..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="bg-white border border-gray-300 rounded-lg px-4 py-2 text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="bg-white border border-gray-300 rounded-lg px-4 py-2 text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">Alle Kategorien</option>
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Items List */}
      <div className="bg-white rounded-lg shadow-sm">
        <div className="p-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">
            Gerichte ({filteredItems.length})
          </h3>
        </div>
        <div className="space-y-0 max-h-[70vh] overflow-y-auto">
        {filteredItems.map(item => (
          <div key={item.id} className="border-b border-gray-200 p-4 hover:bg-gray-50 transition-colors">
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <h3 className="text-gray-900 font-semibold text-lg">{item.name}</h3>
                <p className="text-gray-700 text-sm mb-2">{item.description}</p>
                <div className="flex items-center gap-4 text-xs text-gray-600">
                  <span>Kategorie: {item.category}</span>
                  <span>Preis: {item.price}€</span>
                  <div className="flex gap-1">
                    {item.vegan && <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs">🌱 Vegan</span>}
                    {item.vegetarian && !item.vegan && <span className="bg-emerald-100 text-emerald-800 px-2 py-1 rounded text-xs">🌿 Vegetarisch</span>}
                    {item.glutenfree && <span className="bg-amber-100 text-amber-800 px-2 py-1 rounded text-xs">🌾 Glutenfrei</span>}
                  </div>
                </div>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => {
                    setEditingItem(item);
                    setShowForm(true);
                  }}
                  className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-sm transition-colors"
                >
                  Bearbeiten
                </button>
                <button
                  onClick={() => handleDelete(item.id)}
                  className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm transition-colors"
                >
                  Löschen
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Form Modal */}
      {showForm && (
        <MenuItemForm
          item={editingItem}
          categories={categories}
          onSave={handleSave}
          onCancel={() => {
            setShowForm(false);
            setEditingItem(null);
          }}
        />
      )}
      </div>
    </div>
  );
};

const MenuItemForm = ({ item, categories, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    name: item?.name || '',
    description: item?.description || '',
    detailed_description: item?.detailed_description || '',
    price: item?.price || '',
    category: item?.category || '',
    origin: item?.origin || '',
    allergens: item?.allergens || '',
    additives: item?.additives || '',
    preparation_method: item?.preparation_method || '',
    ingredients: item?.ingredients || '',
    vegan: item?.vegan || false,
    vegetarian: item?.vegetarian || false,
    glutenfree: item?.glutenfree || false,
    order_index: item?.order_index || 0,
    is_active: item?.is_active !== undefined ? item.is_active : true
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-medium-brown rounded-xl border border-warm-brown p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <h3 className="text-xl font-serif text-warm-beige mb-6">
          {item ? 'Gericht bearbeiten' : 'Neues Gericht hinzufügen'}
        </h3>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Name */}
            <div>
              <label className="block text-warm-beige text-sm font-medium mb-2">Name*</label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                className="w-full bg-dark-brown border border-warm-brown rounded-lg px-4 py-2 text-light-beige"
              />
            </div>

            {/* Price */}
            <div>
              <label className="block text-warm-beige text-sm font-medium mb-2">Preis*</label>
              <input
                type="text"
                required
                value={formData.price}
                onChange={(e) => setFormData({...formData, price: e.target.value})}
                className="w-full bg-dark-brown border border-warm-brown rounded-lg px-4 py-2 text-light-beige"
              />
            </div>

            {/* Category */}
            <div>
              <label className="block text-warm-beige text-sm font-medium mb-2">Kategorie*</label>
              <select
                required
                value={formData.category}
                onChange={(e) => setFormData({...formData, category: e.target.value})}
                className="w-full bg-dark-brown border border-warm-brown rounded-lg px-4 py-2 text-light-beige"
              >
                <option value="">Kategorie wählen</option>
                {categories.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            {/* Origin */}
            <div>
              <label className="block text-warm-beige text-sm font-medium mb-2">Herkunft</label>
              <input
                type="text"
                value={formData.origin}
                onChange={(e) => setFormData({...formData, origin: e.target.value})}
                className="w-full bg-dark-brown border border-warm-brown rounded-lg px-4 py-2 text-light-beige"
              />
            </div>
          </div>

          {/* Description */}
          <div>
            <label className="block text-warm-beige text-sm font-medium mb-2">Kurze Beschreibung</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              rows={2}
              className="w-full bg-dark-brown border border-warm-brown rounded-lg px-4 py-2 text-light-beige"
            />
          </div>

          {/* Detailed Description */}
          <div>
            <label className="block text-warm-beige text-sm font-medium mb-2">Detaillierte Beschreibung</label>
            <textarea
              value={formData.detailed_description}
              onChange={(e) => setFormData({...formData, detailed_description: e.target.value})}
              rows={3}
              className="w-full bg-dark-brown border border-warm-brown rounded-lg px-4 py-2 text-light-beige"
            />
          </div>

          {/* Ingredients */}
          <div>
            <label className="block text-warm-beige text-sm font-medium mb-2">Zutaten</label>
            <textarea
              value={formData.ingredients}
              onChange={(e) => setFormData({...formData, ingredients: e.target.value})}
              rows={2}
              className="w-full bg-dark-brown border border-warm-brown rounded-lg px-4 py-2 text-light-beige"
            />
          </div>

          {/* Preparation Method */}
          <div>
            <label className="block text-warm-beige text-sm font-medium mb-2">Zubereitung</label>
            <textarea
              value={formData.preparation_method}
              onChange={(e) => setFormData({...formData, preparation_method: e.target.value})}
              rows={2}
              className="w-full bg-dark-brown border border-warm-brown rounded-lg px-4 py-2 text-light-beige"
            />
          </div>

          {/* Allergens */}
          <div>
            <label className="block text-warm-beige text-sm font-medium mb-2">Allergene</label>
            <input
              type="text"
              value={formData.allergens}
              onChange={(e) => setFormData({...formData, allergens: e.target.value})}
              className="w-full bg-dark-brown border border-warm-brown rounded-lg px-4 py-2 text-light-beige"
            />
          </div>

          {/* Additives */}
          <div>
            <label className="block text-warm-beige text-sm font-medium mb-2">Zusatzstoffe</label>
            <input
              type="text"
              value={formData.additives}
              onChange={(e) => setFormData({...formData, additives: e.target.value})}
              className="w-full bg-dark-brown border border-warm-brown rounded-lg px-4 py-2 text-light-beige"
            />
          </div>

          {/* Checkboxes */}
          <div className="flex flex-wrap gap-4">
            <label className="flex items-center text-light-beige">
              <input
                type="checkbox"
                checked={formData.vegan}
                onChange={(e) => setFormData({...formData, vegan: e.target.checked})}
                className="mr-2"
              />
              🌱 Vegan
            </label>
            <label className="flex items-center text-light-beige">
              <input
                type="checkbox"
                checked={formData.vegetarian}
                onChange={(e) => setFormData({...formData, vegetarian: e.target.checked})}
                className="mr-2"
              />
              🌿 Vegetarisch
            </label>
            <label className="flex items-center text-light-beige">
              <input
                type="checkbox"
                checked={formData.glutenfree}
                onChange={(e) => setFormData({...formData, glutenfree: e.target.checked})}
                className="mr-2"
              />
              🌾 Glutenfrei
            </label>
            <label className="flex items-center text-light-beige">
              <input
                type="checkbox"
                checked={formData.is_active}
                onChange={(e) => setFormData({...formData, is_active: e.target.checked})}
                className="mr-2"
              />
              Aktiv
            </label>
          </div>

          {/* Order Index */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-warm-beige text-sm font-medium mb-2">Reihenfolge</label>
              <input
                type="number"
                value={formData.order_index}
                onChange={(e) => setFormData({...formData, order_index: parseInt(e.target.value) || 0})}
                className="w-full bg-dark-brown border border-warm-brown rounded-lg px-4 py-2 text-light-beige"
              />
            </div>
          </div>

          {/* Buttons */}
          <div className="flex gap-4 pt-4">
            <button
              type="submit"
              className="bg-orange-500 hover:bg-orange-600 text-white px-6 py-2 rounded-lg transition-colors"
            >
              Speichern
            </button>
            <button
              type="button"
              onClick={onCancel}
              className="bg-gray-500 hover:bg-gray-600 text-white px-6 py-2 rounded-lg transition-colors"
            >
              Abbrechen
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default MenuItemsAdminSection;