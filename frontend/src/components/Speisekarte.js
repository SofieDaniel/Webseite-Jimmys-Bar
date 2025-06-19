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

          {/* Right Side - Hover Details (No Images) */}
          <div className="w-96 sticky top-24 h-fit">
            {hoveredItem ? (
              <div className="bg-gradient-to-br from-medium-brown to-dark-brown border-2 border-warm-beige/40 rounded-xl p-6 shadow-2xl">
                {/* Header with decorative elements */}
                <div className="border-b border-warm-beige/30 pb-4 mb-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-2xl font-serif text-warm-beige">
                      {hoveredItem.name}
                    </h3>
                    <div className="text-right">
                      <div className="bg-warm-beige text-dark-brown px-3 py-1 rounded-full">
                        <span className="text-xl font-bold">
                          {hoveredItem.price}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-2 flex items-center gap-2">
                    <span className="bg-orange-500/20 text-orange-300 px-2 py-1 rounded text-xs font-medium">
                      {hoveredItem.category}
                    </span>
                    <div className="flex gap-1">
                      {getAllergyIcons(hoveredItem).map((icon, index) => (
                        <span key={index} className="text-lg">{icon}</span>
                      ))}
                    </div>
                  </div>
                </div>
                
                {/* Description */}
                <div className="bg-dark-brown/50 rounded-lg p-4 mb-4 border border-warm-beige/20">
                  <p className="text-light-beige leading-relaxed">
                    {hoveredItem.description}
                  </p>
                </div>
                
                {/* Allergy Information */}
                <div className="bg-warm-beige/5 rounded-lg p-4 border border-warm-beige/20">
                  <h4 className="text-sm font-semibold text-warm-beige mb-3 flex items-center gap-2">
                    <span className="w-2 h-2 bg-warm-beige rounded-full"></span>
                    Allergie-Informationen
                  </h4>
                  <div className="grid grid-cols-3 gap-3">
                    <div className={`text-center p-2 rounded ${hoveredItem.vegan ? 'bg-green-500/20 border border-green-500/30' : 'bg-gray-500/10 border border-gray-500/20'}`}>
                      <div className="text-lg mb-1">🌱</div>
                      <div className={`text-xs ${hoveredItem.vegan ? 'text-green-300' : 'text-gray-400'}`}>
                        Vegan
                      </div>
                    </div>
                    <div className={`text-center p-2 rounded ${hoveredItem.vegetarian ? 'bg-green-500/20 border border-green-500/30' : 'bg-gray-500/10 border border-gray-500/20'}`}>
                      <div className="text-lg mb-1">🌿</div>
                      <div className={`text-xs ${hoveredItem.vegetarian ? 'text-green-300' : 'text-gray-400'}`}>
                        Vegetarisch
                      </div>
                    </div>
                    <div className={`text-center p-2 rounded ${hoveredItem.glutenfree ? 'bg-green-500/20 border border-green-500/30' : 'bg-gray-500/10 border border-gray-500/20'}`}>
                      <div className="text-lg mb-1">🌾</div>
                      <div className={`text-xs ${hoveredItem.glutenfree ? 'text-green-300' : 'text-gray-400'}`}>
                        Glutenfrei
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-gradient-to-br from-warm-beige/10 to-orange-500/10 border-2 border-dashed border-warm-beige/30 rounded-xl p-8 text-center">
                <div className="text-warm-beige/60 mb-4">
                  <div className="w-16 h-16 mx-auto bg-warm-beige/10 rounded-full flex items-center justify-center">
                    <span className="text-2xl">🍽️</span>
                  </div>
                </div>
                <h3 className="text-warm-beige font-medium mb-2">Gericht-Details</h3>
                <p className="text-warm-beige/70 text-sm">
                  Bewegen Sie die Maus über ein Gericht<br/>
                  um Details und Allergie-Informationen zu sehen
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
