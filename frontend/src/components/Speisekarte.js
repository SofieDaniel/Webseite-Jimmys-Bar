import React, { useState, useEffect } from 'react';

const Speisekarte = () => {
  const [menuItems, setMenuItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('Alle Kategorien');
  const [hoveredItem, setHoveredItem] = useState(null);

  // Load menu items from backend
  useEffect(() => {
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
    loadMenuItems();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-warm-beige"></div>
      </div>
    );
  }

  // Get unique categories with proper mapping
  const categoryMapping = {
    'Inicio': 'Inicio',
    'Salat': 'Salat', 
    'Kleiner Salat': 'Kleiner Salat',
    'Tapas Warme': 'Tapas Warme',
    'Tapa Paella': 'Tapa Paella',
    'Tapas Vegetar': 'Tapas Vegetar',
    'Tapas de Carne': 'Tapas de Carne',
    'Kroketten': 'Kroketten',
    'Pasta': 'Pasta',
    'Pizza': 'Pizza',
    'Snacks': 'Snacks',
    'Dessert': 'Dessert',
    'Helados': 'Helados'
  };

  const allCategories = ['Alle Kategorien', ...Object.keys(categoryMapping)];
  const filteredItems = selectedCategory === 'Alle Kategorien' 
    ? menuItems 
    : menuItems.filter(item => item.category === selectedCategory);

  // Group items by category for display
  const groupedItems = filteredItems.reduce((acc, item) => {
    const category = item.category;
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(item);
    return acc;
  }, {});

  // Get allergy icons
  const getAllergyIcons = (item) => {
    const icons = [];
    if (item.vegan) icons.push('🌱');
    if (item.vegetarian && !item.vegan) icons.push('🌿');
    if (item.glutenfree) icons.push('🌾');
    return icons;
  };

  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Header Section */}
      <div className="pt-24 pb-8 bg-dark-brown">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide">
            Speisekarte
          </h1>
          <p className="text-xl text-light-beige font-light tracking-wide">
            Authentische spanische Küche - Bewegen Sie die Maus über Gerichte für Details
          </p>
        </div>
      </div>

      {/* Category Filter Buttons */}
      <div className="container mx-auto px-4 mb-8">
        <div className="flex flex-wrap justify-center gap-3 max-w-6xl mx-auto">
          {allCategories.map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-4 py-2 rounded-full border transition-all ${
                selectedCategory === category
                  ? 'bg-warm-beige text-dark-brown border-warm-beige'
                  : 'bg-transparent text-warm-beige border-warm-beige hover:bg-warm-beige hover:text-dark-brown'
              }`}
            >
              {category}
            </button>
          ))}
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 pb-16">
        <div className="flex gap-8 max-w-7xl mx-auto">
          {/* Left Side - Menu Items List */}
          <div className="flex-1">
            {Object.entries(groupedItems).map(([category, items]) => (
              <div key={category} className="mb-8">
                {selectedCategory === 'Alle Kategorien' && (
                  <h2 className="text-2xl font-serif text-warm-beige mb-4 pb-2 border-b border-warm-beige/30">
                    {category}
                  </h2>
                )}
                
                <div className="space-y-1">
                  {items.map((item) => (
                    <div
                      key={item.id}
                      className={`p-4 rounded-lg cursor-pointer transition-all duration-200 ${
                        hoveredItem?.id === item.id 
                          ? 'bg-warm-beige/10 border border-warm-beige/30' 
                          : 'hover:bg-warm-beige/5'
                      }`}
                      onMouseEnter={() => setHoveredItem(item)}
                      onMouseLeave={() => setHoveredItem(null)}
                    >
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <h3 className="text-lg font-medium text-warm-beige">
                              {item.name}
                            </h3>
                            <div className="flex gap-1">
                              {getAllergyIcons(item).map((icon, index) => (
                                <span key={index} className="text-sm">{icon}</span>
                              ))}
                            </div>
                          </div>
                          <p className="text-light-beige text-sm leading-relaxed">
                            {item.description.length > 80 
                              ? `${item.description.substring(0, 80)}...` 
                              : item.description}
                          </p>
                          <div className="text-xs text-warm-beige/70 mt-1">
                            {item.category}
                          </div>
                        </div>
                        <div className="ml-4 text-right">
                          <span className="text-xl font-semibold text-warm-beige">
                            {item.price}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Right Side - Hover Details */}
          <div className="w-96 sticky top-24 h-fit">
            {hoveredItem ? (
              <div className="bg-dark-brown border border-warm-beige/30 rounded-xl p-6 shadow-2xl">
                {/* Image */}
                <div className="w-full h-48 rounded-lg overflow-hidden mb-4">
                  <img 
                    src={hoveredItem.image || 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'}
                    alt={hoveredItem.name}
                    className="w-full h-full object-cover"
                  />
                </div>
                
                {/* Details */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="text-xl font-serif text-warm-beige">
                      {hoveredItem.name}
                    </h3>
                    <span className="text-2xl font-bold text-warm-beige">
                      {hoveredItem.price}
                    </span>
                  </div>
                  
                  <p className="text-light-beige text-sm leading-relaxed">
                    {hoveredItem.description}
                  </p>
                  
                  <div className="text-sm text-warm-beige/70">
                    <strong>Kategorie:</strong> {hoveredItem.category}
                  </div>
                  
                  {/* Allergy Information */}
                  <div className="pt-3 border-t border-warm-beige/20">
                    <h4 className="text-sm font-semibold text-warm-beige mb-2">
                      Allergie-Informationen:
                    </h4>
                    <div className="space-y-1 text-xs">
                      <div className="flex items-center gap-2">
                        <span className={hoveredItem.vegan ? 'text-green-400' : 'text-gray-500'}>
                          🌱
                        </span>
                        <span className={hoveredItem.vegan ? 'text-light-beige' : 'text-gray-500'}>
                          Vegan
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className={hoveredItem.vegetarian ? 'text-green-400' : 'text-gray-500'}>
                          🌿
                        </span>
                        <span className={hoveredItem.vegetarian ? 'text-light-beige' : 'text-gray-500'}>
                          Vegetarisch
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className={hoveredItem.glutenfree ? 'text-green-400' : 'text-gray-500'}>
                          🌾
                        </span>
                        <span className={hoveredItem.glutenfree ? 'text-light-beige' : 'text-gray-500'}>
                          Glutenfrei
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-dark-brown border border-warm-beige/30 rounded-xl p-6 text-center">
                <div className="text-warm-beige/50 mb-4">
                  <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <p className="text-warm-beige/70 text-sm">
                  Bewegen Sie die Maus über ein Gericht<br/>
                  um Details und Bilder zu sehen
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Allergy Legend */}
        <div className="max-w-7xl mx-auto mt-12 pt-8 border-t border-warm-beige/20">
          <h3 className="text-lg font-serif text-warm-beige mb-4 text-center">
            Allergie-Legende
          </h3>
          <div className="flex justify-center gap-8 text-sm">
            <div className="flex items-center gap-2">
              <span>🌱</span>
              <span className="text-light-beige">Vegan</span>
            </div>
            <div className="flex items-center gap-2">
              <span>🌿</span>
              <span className="text-light-beige">Vegetarisch</span>
            </div>
            <div className="flex items-center gap-2">
              <span>🌾</span>
              <span className="text-light-beige">Glutenfrei</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Speisekarte;
          </div>
        </div>
      </div>

      {/* Category Filter */}
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-wrap justify-center gap-4 mb-8">
          <button
            onClick={() => setSelectedCategory('all')}
            className={`px-6 py-3 rounded-lg font-medium transition-colors ${
              selectedCategory === 'all' 
                ? 'bg-warm-beige text-dark-brown' 
                : 'bg-medium-brown text-light-beige hover:bg-warm-brown'
            }`}
          >
            Alle Gerichte
          </button>
          {categories.map(category => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-6 py-3 rounded-lg font-medium transition-colors capitalize ${
                selectedCategory === category 
                  ? 'bg-warm-beige text-dark-brown' 
                  : 'bg-medium-brown text-light-beige hover:bg-warm-brown'
              }`}
            >
              {category.replace('-', ' ')}
            </button>
          ))}
        </div>

        {/* Menu Items Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredItems.map((item, index) => (
            <div key={index} className="bg-medium-brown rounded-lg border border-warm-brown overflow-hidden shadow-lg">
              {item.image_url && (
                <img 
                  src={item.image_url} 
                  alt={item.name} 
                  className="w-full h-48 object-cover"
                />
              )}
              <div className="p-6">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-xl font-serif text-warm-beige">{item.name}</h3>
                  <span className="text-xl font-semibold text-orange-400">{item.price}€</span>
                </div>
                <p className="text-light-beige text-sm mb-4">{item.description}</p>
                {item.detailed_description && (
                  <p className="text-gray-300 text-xs mb-4">{item.detailed_description}</p>
                )}
                <div className="flex flex-wrap gap-2">
                  {item.vegetarian && (
                    <span className="px-2 py-1 bg-green-600 text-white text-xs rounded">Vegetarisch</span>
                  )}
                  {item.vegan && (
                    <span className="px-2 py-1 bg-green-700 text-white text-xs rounded">Vegan</span>
                  )}
                  {item.glutenfree && (
                    <span className="px-2 py-1 bg-blue-600 text-white text-xs rounded">Glutenfrei</span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredItems.length === 0 && (
          <div className="text-center py-16">
            <p className="text-light-beige text-lg">Keine Gerichte in dieser Kategorie gefunden.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Speisekarte;