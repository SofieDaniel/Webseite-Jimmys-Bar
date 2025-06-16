import React, { useState, useEffect } from 'react';

// ===============================================
// ENHANCED MENU MANAGEMENT SECTION (With Edit/Delete)
// ===============================================

export const EnhancedMenuSection = ({ user, token, apiCall }) => {
  const [menuItems, setMenuItems] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');
  const [editingItem, setEditingItem] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('alle');

  // Form state for new/edit item
  const [itemForm, setItemForm] = useState({
    name: '',
    description: '',
    detailed_description: '',
    price: '',
    category: 'inicio',
    image: '',
    vegan: false,
    vegetarian: false,
    glutenfree: false
  });

  useEffect(() => {
    loadMenuData();
    loadCategories();
  }, []);

  const loadMenuData = async () => {
    setLoading(true);
    try {
      const response = await apiCall('/menu/items');
      if (response.ok) {
        const data = await response.json();
        setMenuItems(data);
      }
    } catch (error) {
      setError('Fehler beim Laden der Menü-Items');
    } finally {
      setLoading(false);
    }
  };

  const loadCategories = async () => {
    // Static categories for now - could be loaded from API
    setCategories([
      { slug: 'inicio', name: 'Inicio' },
      { slug: 'salat', name: 'Salate' },
      { slug: 'kleiner-salat', name: 'Kleine Salate' },
      { slug: 'tapas-vegetarian', name: 'Tapas Vegetarisch' },
      { slug: 'tapas-pescado', name: 'Tapas Fisch' },
      { slug: 'tapas-carne', name: 'Tapas Fleisch' },
      { slug: 'tapa-paella', name: 'Tapa Paella' },
      { slug: 'bebidas', name: 'Getränke' },
      { slug: 'postres', name: 'Nachspeisen' },
      { slug: 'arroces', name: 'Reis-Gerichte' },
      { slug: 'pescado-grande', name: 'Fisch-Hauptgerichte' }
    ]);
  };

  const resetForm = () => {
    setItemForm({
      name: '',
      description: '',
      detailed_description: '',
      price: '',
      category: 'inicio',
      image: '',
      vegan: false,
      vegetarian: false,
      glutenfree: false
    });
    setEditingItem(null);
    setShowAddForm(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const method = editingItem ? 'PUT' : 'POST';
      const endpoint = editingItem ? `/menu/items/${editingItem.id}` : '/menu/items';
      
      const payload = {
        ...itemForm,
        price: parseFloat(itemForm.price)
      };

      const response = await apiCall(endpoint, method, payload);
      
      if (response.ok) {
        setSuccess(editingItem ? 'Menü-Item erfolgreich aktualisiert' : 'Menü-Item erfolgreich erstellt');
        resetForm();
        loadMenuData();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Fehler beim Speichern des Menü-Items');
      }
    } catch (error) {
      setError('Verbindungsfehler beim Speichern');
    } finally {
      setLoading(false);
    }
  };

  const startEdit = (item) => {
    setItemForm({
      name: item.name,
      description: item.description,
      detailed_description: item.detailed_description || '',
      price: item.price.toString(),
      category: item.category,
      image: item.image || '',
      vegan: item.vegan || false,
      vegetarian: item.vegetarian || false,
      glutenfree: item.glutenfree || false
    });
    setEditingItem(item);
    setShowAddForm(true);
  };

  const deleteItem = async (item) => {
    if (!confirm(`Sind Sie sicher, dass Sie "${item.name}" löschen möchten?`)) {
      return;
    }

    setLoading(true);
    try {
      const response = await apiCall(`/menu/items/${item.id}`, 'DELETE');
      if (response.ok) {
        setSuccess('Menü-Item erfolgreich gelöscht');
        loadMenuData();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Fehler beim Löschen des Menü-Items');
      }
    } catch (error) {
      setError('Verbindungsfehler beim Löschen');
    } finally {
      setLoading(false);
    }
  };

  const getFilteredItems = () => {
    if (selectedCategory === 'alle') {
      return menuItems;
    }
    return menuItems.filter(item => item.category === selectedCategory);
  };

  const formatPrice = (price) => {
    if (typeof price === 'string') {
      return price.includes('€') ? price : `${price}€`;
    }
    return `${price.toFixed(2).replace('.', ',')}€`;
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Erweiterte Speisekarten-Verwaltung</h1>
        <p className="text-gray-600">Verwalten Sie alle Menü-Items mit vollständiger Bearbeitungs- und Löschfunktion</p>
      </div>

      {/* Messages */}
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

      {/* Control Panel */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex justify-between items-center mb-6">
          <div className="flex items-center space-x-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Kategorie filtern</label>
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="alle">Alle Kategorien ({menuItems.length} Items)</option>
                {categories.map(cat => {
                  const count = menuItems.filter(item => item.category === cat.slug).length;
                  return (
                    <option key={cat.slug} value={cat.slug}>
                      {cat.name} ({count} Items)
                    </option>
                  );
                })}
              </select>
            </div>
          </div>
          
          <div className="flex space-x-3">
            <button
              onClick={loadMenuData}
              className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
              disabled={loading}
            >
              {loading ? 'Laden...' : 'Aktualisieren'}
            </button>
            <button
              onClick={() => setShowAddForm(true)}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              + Neues Item hinzufügen
            </button>
          </div>
        </div>

        {/* Add/Edit Form */}
        {showAddForm && (
          <div className="border-t border-gray-200 pt-6 mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              {editingItem ? `"${editingItem.name}" bearbeiten` : 'Neues Menü-Item hinzufügen'}
            </h3>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Name *</label>
                  <input
                    type="text"
                    value={itemForm.name}
                    onChange={(e) => setItemForm({...itemForm, name: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Kategorie *</label>
                  <select
                    value={itemForm.category}
                    onChange={(e) => setItemForm({...itemForm, category: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  >
                    {categories.map(cat => (
                      <option key={cat.slug} value={cat.slug}>{cat.name}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Preis (€) *</label>
                  <input
                    type="number"
                    step="0.10"
                    value={itemForm.price}
                    onChange={(e) => setItemForm({...itemForm, price: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Bild URL</label>
                  <input
                    type="url"
                    value={itemForm.image}
                    onChange={(e) => setItemForm({...itemForm, image: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="https://images.unsplash.com/..."
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Kurze Beschreibung *</label>
                <textarea
                  value={itemForm.description}
                  onChange={(e) => setItemForm({...itemForm, description: e.target.value})}
                  rows={2}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Detaillierte Beschreibung</label>
                <textarea
                  value={itemForm.detailed_description}
                  onChange={(e) => setItemForm({...itemForm, detailed_description: e.target.value})}
                  rows={3}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Ausführliche Beschreibung mit Zutaten und Herkunft..."
                />
              </div>

              {/* Tags */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">Eigenschaften</label>
                <div className="flex space-x-6">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={itemForm.vegan}
                      onChange={(e) => setItemForm({...itemForm, vegan: e.target.checked})}
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <span className="ml-2 text-sm text-gray-700">Vegan</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={itemForm.vegetarian}
                      onChange={(e) => setItemForm({...itemForm, vegetarian: e.target.checked})}
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <span className="ml-2 text-sm text-gray-700">Vegetarisch</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={itemForm.glutenfree}
                      onChange={(e) => setItemForm({...itemForm, glutenfree: e.target.checked})}
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <span className="ml-2 text-sm text-gray-700">Glutenfrei</span>
                  </label>
                </div>
              </div>

              <div className="flex space-x-3">
                <button
                  type="submit"
                  disabled={loading}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                >
                  {loading ? 'Speichern...' : (editingItem ? 'Aktualisieren' : 'Hinzufügen')}
                </button>
                <button
                  type="button"
                  onClick={resetForm}
                  className="bg-gray-300 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-400 transition-colors"
                >
                  Abbrechen
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Menu Items Table */}
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Gericht
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Kategorie
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Preis
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Eigenschaften
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Aktionen
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {getFilteredItems().map((item) => (
                <tr key={item.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      {item.image && (
                        <img 
                          src={item.image} 
                          alt={item.name}
                          className="h-12 w-12 rounded-lg object-cover mr-4"
                        />
                      )}
                      <div>
                        <div className="text-sm font-medium text-gray-900">{item.name}</div>
                        <div className="text-sm text-gray-500">{item.description}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                      {categories.find(cat => cat.slug === item.category)?.name || item.category}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {formatPrice(item.price)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex space-x-1">
                      {item.vegan && (
                        <span className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded">Vegan</span>
                      )}
                      {item.vegetarian && (
                        <span className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded">Vegetarisch</span>
                      )}
                      {item.glutenfree && (
                        <span className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">Glutenfrei</span>
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex space-x-2">
                      <button
                        onClick={() => startEdit(item)}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        Bearbeiten
                      </button>
                      <button
                        onClick={() => deleteItem(item)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Löschen
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          
          {getFilteredItems().length === 0 && (
            <div className="text-center py-8 text-gray-500">
              {selectedCategory === 'alle' ? 'Keine Menü-Items gefunden' : `Keine Items in der Kategorie "${categories.find(cat => cat.slug === selectedCategory)?.name}" gefunden`}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Export placeholder functions for other CMS sections (until fixed)
export const HomepageContentSection = () => <div>Homepage CMS wird geladen...</div>;
export const LocationsManagementSection = () => <div>Locations CMS wird geladen...</div>;
export const AboutContentSection = () => <div>About CMS wird geladen...</div>;
export const ContactLegalSection = () => <div>Contact CMS wird geladen...</div>;