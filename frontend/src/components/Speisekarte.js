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
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Beautiful Header Section */}
      <div className="relative overflow-hidden bg-gradient-to-r from-orange-500 via-red-500 to-yellow-500">
        <div className="absolute inset-0 bg-black bg-opacity-40"></div>
        <div className="absolute inset-0">
          <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-orange-400/20 via-transparent to-yellow-400/20"></div>
          <div className="absolute -top-10 -left-10 w-40 h-40 bg-yellow-400/30 rounded-full blur-xl"></div>
          <div className="absolute -bottom-10 -right-10 w-60 h-60 bg-orange-400/30 rounded-full blur-xl"></div>
          <div className="absolute top-1/2 left-1/4 w-32 h-32 bg-red-400/20 rounded-full blur-xl"></div>
        </div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <div className="max-w-4xl mx-auto">
              <h1 className="text-6xl md:text-7xl font-serif text-white mb-6 tracking-wide drop-shadow-lg">
                Speisekarte
              </h1>
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
                <p className="text-xl md:text-2xl text-white font-light leading-relaxed">
                  Authentische spanische Küche - Entdecken Sie unsere Gerichte
                </p>
                <div className="flex justify-center items-center gap-4 mt-4 text-white/90">
                  <span className="flex items-center gap-2 text-sm">
                    <span className="w-2 h-2 bg-green-400 rounded-full"></span>
                    Detaillierte Allergie-Informationen
                  </span>
                  <span className="flex items-center gap-2 text-sm">
                    <span className="w-2 h-2 bg-blue-400 rounded-full"></span>
                    Hover für Details
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Category Filter Buttons */}
      <div className="container mx-auto px-4 mb-8 bg-gradient-to-r from-slate-800 to-slate-700 py-6 rounded-xl mx-4">
        <div className="flex flex-wrap justify-center gap-3 max-w-6xl mx-auto">
          {allCategories.map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-6 py-3 rounded-full border-2 transition-all duration-300 transform hover:scale-105 ${
                selectedCategory === category
                  ? 'bg-gradient-to-r from-orange-500 to-red-500 text-white border-orange-500 shadow-lg'
                  : 'bg-white/10 text-gray-200 border-gray-300 hover:bg-gradient-to-r hover:from-orange-400 hover:to-red-400 hover:text-white hover:border-orange-400'
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
                  <div className="flex items-center gap-4 mb-6">
                    <div className="flex-1 h-px bg-gradient-to-r from-transparent via-blue-400 to-transparent"></div>
                    <h2 className="text-2xl font-serif text-gray-200 px-4 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full py-2">
                      {category}
                    </h2>
                    <div className="flex-1 h-px bg-gradient-to-r from-transparent via-blue-400 to-transparent"></div>
                  </div>
                )}
                
                <div className="space-y-3">
                  {items.map((item, index) => (
                    <div
                      key={item.id}
                      className={`group relative overflow-hidden rounded-xl transition-all duration-300 ${
                        hoveredItem?.id === item.id 
                          ? 'bg-gradient-to-r from-blue-100 via-white to-blue-100 border-l-4 border-blue-500 shadow-xl transform scale-[1.02]' 
                          : index % 2 === 0 
                            ? 'bg-gradient-to-r from-white to-gray-50 hover:from-blue-50 hover:to-white border-l-4 border-transparent hover:border-blue-400'
                            : 'bg-gradient-to-r from-gray-50 to-white hover:from-indigo-50 hover:to-white border-l-4 border-transparent hover:border-indigo-400'
                      } cursor-pointer border border-gray-200 hover:border-gray-300`}
                      onMouseEnter={() => setHoveredItem(item)}
                      onMouseLeave={() => setHoveredItem(null)}
                    >
                      <div className="p-5">
                        <div className="flex justify-between items-start">
                          <div className="flex-1 pr-4">
                            <div className="flex items-center gap-3 mb-2">
                              <h3 className="text-lg font-medium text-gray-800 group-hover:text-gray-900 transition-colors">
                                {item.name}
                              </h3>
                              <div className="flex gap-1">
                                {getAllergyIcons(item).map((icon, index) => (
                                  <span key={index} className="text-sm bg-yellow-100 px-1 rounded border">{icon}</span>
                                ))}
                              </div>
                            </div>
                            <p className="text-gray-600 text-sm leading-relaxed group-hover:text-gray-700 transition-colors">
                              {item.description.length > 100 
                                ? `${item.description.substring(0, 100)}...` 
                                : item.description}
                            </p>
                            <div className="flex items-center gap-2 mt-2">
                              <span className={`text-xs px-3 py-1 rounded-full font-medium ${
                                index % 3 === 0 ? 'bg-orange-100 text-orange-700 border border-orange-200'
                                : index % 3 === 1 ? 'bg-blue-100 text-blue-700 border border-blue-200'
                                : 'bg-green-100 text-green-700 border border-green-200'
                              }`}>
                                {item.category}
                              </span>
                            </div>
                          </div>
                          <div className="text-right">
                            <div className={`px-4 py-2 rounded-lg ${
                              hoveredItem?.id === item.id 
                                ? 'bg-gradient-to-r from-blue-500 to-indigo-500 text-white shadow-lg'
                                : 'bg-gray-100 border border-gray-300'
                            } transition-all duration-300`}>
                              <span className={`text-lg font-bold ${hoveredItem?.id === item.id ? 'text-white' : 'text-gray-700'}`}>
                                {item.price}
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      {/* Hover indicator */}
                      <div className={`absolute bottom-0 left-0 h-1 bg-gradient-to-r from-blue-500 to-indigo-500 transition-all duration-300 ${
                        hoveredItem?.id === item.id ? 'w-full' : 'w-0'
                      }`}></div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Right Side - Hover Details (No Images, No Price) */}
          <div className="w-96 sticky top-24 h-fit">
            {hoveredItem ? (
              <div className="bg-gradient-to-br from-white via-gray-50 to-blue-50 border-2 border-blue-200 rounded-xl p-6 shadow-2xl">
                {/* Header with decorative elements */}
                <div className="border-b border-gray-200 pb-4 mb-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-2xl font-serif text-gray-800">
                      {hoveredItem.name}
                    </h3>
                  </div>
                  
                  <div className="mt-2 flex items-center gap-2">
                    <span className="bg-gradient-to-r from-orange-500 to-red-500 text-white px-3 py-1 rounded-full text-xs font-medium">
                      {hoveredItem.category}
                    </span>
                    <div className="flex gap-1">
                      {getAllergyIcons(hoveredItem).map((icon, index) => (
                        <span key={index} className="text-lg bg-yellow-100 px-1 rounded">{icon}</span>
                      ))}
                    </div>
                  </div>
                </div>
                
                {/* Detailed Description */}
                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-4 mb-4 border border-blue-200">
                  <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                    <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
                    Beschreibung & Zutaten
                  </h4>
                  <p className="text-gray-700 leading-relaxed text-sm">
                    {hoveredItem.description}
                  </p>
                </div>
                
                {/* Allergy Information */}
                <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg p-4 border border-green-200">
                  <h4 className="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
                    <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                    Allergie-Informationen
                  </h4>
                  <div className="grid grid-cols-3 gap-3">
                    <div className={`text-center p-3 rounded-lg transition-all ${hoveredItem.vegan ? 'bg-green-100 border-2 border-green-300 shadow-md' : 'bg-gray-100 border border-gray-200'}`}>
                      <div className="text-xl mb-1">🌱</div>
                      <div className={`text-xs font-medium ${hoveredItem.vegan ? 'text-green-700' : 'text-gray-400'}`}>
                        Vegan
                      </div>
                    </div>
                    <div className={`text-center p-3 rounded-lg transition-all ${hoveredItem.vegetarian ? 'bg-green-100 border-2 border-green-300 shadow-md' : 'bg-gray-100 border border-gray-200'}`}>
                      <div className="text-xl mb-1">🌿</div>
                      <div className={`text-xs font-medium ${hoveredItem.vegetarian ? 'text-green-700' : 'text-gray-400'}`}>
                        Vegetarisch
                      </div>
                    </div>
                    <div className={`text-center p-3 rounded-lg transition-all ${hoveredItem.glutenfree ? 'bg-green-100 border-2 border-green-300 shadow-md' : 'bg-gray-100 border border-gray-200'}`}>
                      <div className="text-xl mb-1">🌾</div>
                      <div className={`text-xs font-medium ${hoveredItem.glutenfree ? 'text-green-700' : 'text-gray-400'}`}>
                        Glutenfrei
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-gradient-to-br from-yellow-50 via-orange-50 to-red-50 border-2 border-dashed border-orange-300 rounded-xl p-8 text-center">
                <div className="text-orange-500 mb-4">
                  <div className="w-16 h-16 mx-auto bg-orange-100 rounded-full flex items-center justify-center">
                    <span className="text-2xl">🍽️</span>
                  </div>
                </div>
                <h3 className="text-gray-700 font-medium mb-2">Gericht-Details</h3>
                <p className="text-gray-600 text-sm">
                  Bewegen Sie die Maus über ein Gericht<br/>
                  um detaillierte Zutatenlisten und<br/>
                  Allergie-Informationen zu sehen
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
