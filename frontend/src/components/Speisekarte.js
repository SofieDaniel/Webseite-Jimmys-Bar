import React, { useState, useEffect } from 'react';

const Speisekarte = () => {
  const [menuItems, setMenuItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('Alle Kategorien');
  const [hoveredItem, setHoveredItem] = useState(null);
  const [selectedItem, setSelectedItem] = useState(null);

  // Load menu items from backend
  useEffect(() => {
    const loadMenuItems = async () => {
      try {
        const response = await fetch(`/api/menu/items`);
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

  // Modal für Gericht-Details
  const ItemDetailModal = ({ item, onClose }) => {
    if (!item) return null;
    
    return (
      <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
        <div className="bg-dark-brown border border-warm-beige rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
          {/* Header */}
          <div className="p-6 border-b border-warm-beige/30">
            <div className="flex justify-between items-start">
              <div>
                <h2 className="text-2xl font-serif text-warm-beige mb-2">{item.name}</h2>
                <div className="flex items-center gap-3">
                  <span className="text-2xl font-bold text-warm-beige">{item.price}</span>
                  <span className="text-sm bg-warm-beige/20 text-warm-beige px-3 py-1 rounded-full">
                    {item.category}
                  </span>
                </div>
              </div>
              <button 
                onClick={onClose}
                className="text-warm-beige hover:text-white text-2xl"
              >
                ×
              </button>
            </div>
          </div>
          
          {/* Content */}
          <div className="p-6 space-y-6">
            {/* Beschreibung */}
            <div>
              <h3 className="text-warm-beige font-semibold mb-2">Beschreibung</h3>
              <p className="text-light-beige leading-relaxed">
                {item.detailed_description || item.description}
              </p>
            </div>
            
            {/* Herkunft */}
            {item.origin && (
              <div>
                <h3 className="text-warm-beige font-semibold mb-2">Herkunft</h3>
                <p className="text-light-beige">{item.origin}</p>
              </div>
            )}
            
            {/* Zubereitung */}
            {item.preparation_method && (
              <div>
                <h3 className="text-warm-beige font-semibold mb-2">Zubereitung</h3>
                <p className="text-light-beige">{item.preparation_method}</p>
              </div>
            )}
            
            {/* Zutaten */}
            {item.ingredients && (
              <div>
                <h3 className="text-warm-beige font-semibold mb-2">Hauptzutaten</h3>
                <p className="text-light-beige">{item.ingredients}</p>
              </div>
            )}
            
            {/* Allergene */}
            {item.allergens && (
              <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-4">
                <h3 className="text-red-300 font-semibold mb-2 flex items-center">
                  ⚠️ Allergene & Unverträglichkeiten
                </h3>
                <p className="text-red-200">{item.allergens}</p>
              </div>
            )}
            
            {/* Zusatzstoffe */}
            {item.additives && item.additives !== "Keine Zusatzstoffe" && (
              <div className="bg-yellow-900/20 border border-yellow-500/30 rounded-lg p-4">
                <h3 className="text-yellow-300 font-semibold mb-2">Zusatzstoffe</h3>
                <p className="text-yellow-200">{item.additives}</p>
              </div>
            )}
            
            {/* Eigenschaften */}
            <div className="flex gap-2 flex-wrap">
              {item.vegan && (
                <span className="bg-green-600/20 text-green-300 px-3 py-1 rounded-full text-sm border border-green-500/30">
                  🌱 Vegan
                </span>
              )}
              {item.vegetarian && !item.vegan && (
                <span className="bg-green-600/20 text-green-300 px-3 py-1 rounded-full text-sm border border-green-500/30">
                  🥬 Vegetarisch
                </span>
              )}
              {item.glutenfree && (
                <span className="bg-blue-600/20 text-blue-300 px-3 py-1 rounded-full text-sm border border-blue-500/30">
                  🌾 Glutenfrei
                </span>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Load menu items from backend
  useEffect(() => {
    const loadMenuItems = async () => {
      try {
        const response = await fetch(`/api/menu/items`);
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
    'Tapa Paella': 'Tapa Paella',
    'Tapas Vegetar': 'Tapas Vegetar',
    'Tapas de Pollo': 'Tapas de Pollo',
    'Tapas de Carne': 'Tapas de Carne',
    'Tapas de Pescado': 'Tapas de Pescado',
    'Kroketten': 'Kroketten',
    'Pasta': 'Pasta',
    'Pizza': 'Pizza',
    'Snacks': 'Snacks',
    'Dessert': 'Dessert',
    'Helados': 'Helados',
    'Heißgetränke': 'Heißgetränke',
    'Tee': 'Tee',
    'Softdrinks': 'Softdrinks',
    'Limonaden': 'Limonaden',
    'Säfte': 'Säfte',
    'Aperitifs': 'Aperitifs',
    'Bier': 'Bier',
    'Weine': 'Weine',
    'Cocktails': 'Cocktails',
    'Spanische Getränke': 'Spanische Getränke',
    'Spirituosen': 'Spirituosen'
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
      {/* Schönerer Header Section */}
      <div className="relative overflow-hidden bg-gradient-to-r from-dark-brown via-medium-brown to-dark-brown">
        <div className="absolute inset-0 bg-black bg-opacity-30"></div>
        <div className="absolute inset-0">
          <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-warm-beige/10 via-transparent to-orange-500/10"></div>
          <div className="absolute -top-10 -left-10 w-40 h-40 bg-warm-beige/20 rounded-full blur-xl"></div>
          <div className="absolute -bottom-10 -right-10 w-60 h-60 bg-orange-500/20 rounded-full blur-xl"></div>
        </div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <div className="max-w-4xl mx-auto">
              <h1 className="text-6xl md:text-7xl font-serif text-warm-beige mb-6 tracking-wide drop-shadow-lg">
                Speisekarte
              </h1>
              <div className="bg-dark-brown/40 backdrop-blur-sm rounded-xl p-6 border border-warm-beige/30">
                <p className="text-xl md:text-2xl text-light-beige font-light leading-relaxed">
                  Authentische spanische Küche - Detaillierte Allergie-Informationen
                </p>
                <div className="flex justify-center items-center gap-6 mt-4 text-light-beige">
                  <span className="flex items-center gap-2 text-sm">
                    <span className="w-2 h-2 bg-warm-beige rounded-full"></span>
                    Zutaten & Herkunft
                  </span>
                  <span className="flex items-center gap-2 text-sm">
                    <span className="w-2 h-2 bg-orange-500 rounded-full"></span>
                    Hover für Details
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Category Filter Buttons */}
      <div className="container mx-auto px-4 mb-8">
        <div className="bg-medium-brown/50 rounded-xl p-6 border border-warm-beige/20">
          <div className="flex flex-wrap justify-center gap-3 max-w-6xl mx-auto">
            {allCategories.map((category) => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-6 py-3 rounded-full border transition-all duration-300 ${
                  selectedCategory === category
                    ? 'bg-warm-beige text-dark-brown border-warm-beige shadow-lg'
                    : 'bg-transparent text-warm-beige border-warm-beige hover:bg-warm-beige hover:text-dark-brown'
                }`}
              >
                {category}
              </button>
            ))}
          </div>
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
                    <div className="flex-1 h-px bg-gradient-to-r from-transparent via-warm-beige/50 to-transparent"></div>
                    <h2 className="text-2xl font-serif text-warm-beige px-4 bg-dark-brown">
                      {category}
                    </h2>
                    <div className="flex-1 h-px bg-gradient-to-r from-transparent via-warm-beige/50 to-transparent"></div>
                  </div>
                )}
                
                <div className="space-y-3">
                  {items.map((item, index) => (
                    <div
                      key={item.id}
                      className={`group relative overflow-hidden rounded-xl transition-all duration-300 ${
                        hoveredItem?.id === item.id 
                          ? 'bg-gradient-to-r from-warm-beige/15 via-orange-500/10 to-warm-beige/15 border-l-4 border-warm-beige shadow-lg transform scale-[1.02]' 
                          : index % 2 === 0 
                            ? 'bg-gradient-to-r from-medium-brown/30 to-dark-brown/30 hover:from-warm-beige/10 hover:to-orange-500/10 border-l-4 border-transparent hover:border-warm-beige/50'
                            : 'bg-gradient-to-r from-dark-brown/30 to-medium-brown/30 hover:from-orange-500/10 hover:to-warm-beige/10 border-l-4 border-transparent hover:border-orange-500/50'
                      } cursor-pointer border border-warm-beige/20`}
                      onMouseEnter={() => setHoveredItem(item)}
                      onMouseLeave={() => setHoveredItem(null)}
                      onClick={() => setSelectedItem(item)}
                    >
                      <div className="p-5">
                        <div className="flex justify-between items-start">
                          <div className="flex-1 pr-4">
                            <div className="flex items-center gap-3 mb-2">
                              <h3 className="text-lg font-medium text-warm-beige group-hover:text-white transition-colors">
                                {item.name}
                              </h3>
                              <div className="flex gap-1">
                                {getAllergyIcons(item).map((icon, index) => (
                                  <span key={index} className="text-sm bg-warm-beige/20 px-1 rounded">{icon}</span>
                                ))}
                              </div>
                            </div>
                            <p className="text-light-beige text-sm leading-relaxed group-hover:text-gray-200 transition-colors">
                              {item.description.length > 100 
                                ? `${item.description.substring(0, 100)}...` 
                                : item.description}
                            </p>
                            
                            {/* Kleine Vorschau der Details */}
                            <div className="mt-3 space-y-1 text-xs">
                              {item.origin && (
                                <div className="text-orange-300 truncate">
                                  <span className="font-semibold">🌍</span> {item.origin}
                                </div>
                              )}
                              {item.allergens && (
                                <div className="text-red-300 truncate">
                                  <span className="font-semibold">⚠️</span> {item.allergens.length > 30 ? `${item.allergens.substring(0, 30)}...` : item.allergens}
                                </div>
                              )}
                            </div>
                            <div className="flex items-center gap-2 mt-2">
                              <span className={`text-xs px-3 py-1 rounded-full font-medium ${
                                index % 3 === 0 ? 'bg-orange-500/20 text-orange-300'
                                : index % 3 === 1 ? 'bg-warm-beige/20 text-warm-beige'
                                : 'bg-yellow-500/20 text-yellow-300'
                              }`}>
                                {item.category}
                              </span>
                            </div>
                          </div>
                          <div className="text-right">
                            <div className={`px-4 py-2 rounded-lg ${
                              hoveredItem?.id === item.id 
                                ? 'bg-warm-beige text-dark-brown shadow-lg'
                                : 'bg-dark-brown/50 border border-warm-beige/30'
                            } transition-all duration-300`}>
                              <span className={`text-lg font-bold ${hoveredItem?.id === item.id ? 'text-dark-brown' : 'text-warm-beige'}`}>
                                {item.price}
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      {/* Hover indicator */}
                      <div className={`absolute bottom-0 left-0 h-1 bg-gradient-to-r from-warm-beige to-orange-500 transition-all duration-300 ${
                        hoveredItem?.id === item.id ? 'w-full' : 'w-0'
                      }`}></div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Right Side - Hover Details (Detaillierte Beschreibungen, kein Preis) */}
          <div className="w-96 sticky top-24 h-fit max-h-[calc(100vh-120px)] overflow-y-auto">
            {hoveredItem ? (
              <div className="bg-gradient-to-br from-medium-brown to-dark-brown border-2 border-warm-beige/40 rounded-xl p-6 shadow-2xl">
                {/* Header */}
                <div className="border-b border-warm-beige/30 pb-4 mb-4">
                  <h3 className="text-2xl font-serif text-warm-beige mb-2">
                    {hoveredItem.name}
                  </h3>
                  
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="bg-orange-500/20 text-orange-300 px-3 py-1 rounded-full text-xs font-medium">
                      {hoveredItem.category}
                    </span>
                    <span className="bg-warm-beige/20 text-warm-beige px-3 py-1 rounded-full text-xs font-medium">
                      {hoveredItem.price}
                    </span>
                    <div className="flex gap-1">
                      {getAllergyIcons(hoveredItem).map((icon, index) => (
                        <span key={index} className="text-lg bg-warm-beige/20 px-1 rounded">{icon}</span>
                      ))}
                    </div>
                  </div>
                </div>
                
                {/* Detaillierte Beschreibung */}
                <div className="bg-dark-brown/50 rounded-lg p-4 mb-4 border border-warm-beige/20">
                  <h4 className="text-sm font-semibold text-warm-beige mb-2 flex items-center gap-2">
                    <span className="w-2 h-2 bg-warm-beige rounded-full"></span>
                    Detaillierte Beschreibung
                  </h4>
                  <p className="text-light-beige leading-relaxed text-sm">
                    {hoveredItem.detailed_description || hoveredItem.description}
                  </p>
                </div>

                {/* Zutaten */}
                {hoveredItem.ingredients && (
                  <div className="bg-orange-900/20 rounded-lg p-4 mb-4 border border-orange-500/30">
                    <h4 className="text-sm font-semibold text-orange-300 mb-2 flex items-center gap-2">
                      <span className="w-2 h-2 bg-orange-400 rounded-full"></span>
                      Zutaten
                    </h4>
                    <p className="text-orange-100 text-sm leading-relaxed">
                      {hoveredItem.ingredients}
                    </p>
                  </div>
                )}

                {/* Herkunft & Zubereitung */}
                <div className="grid grid-cols-1 gap-3 mb-4">
                  {hoveredItem.origin && (
                    <div className="bg-blue-900/20 rounded-lg p-3 border border-blue-500/30">
                      <h4 className="text-xs font-semibold text-blue-300 mb-1 flex items-center gap-2">
                        <span className="w-1.5 h-1.5 bg-blue-400 rounded-full"></span>
                        Herkunft
                      </h4>
                      <p className="text-blue-100 text-xs">
                        {hoveredItem.origin}
                      </p>
                    </div>
                  )}
                  
                  {hoveredItem.preparation_method && (
                    <div className="bg-purple-900/20 rounded-lg p-3 border border-purple-500/30">
                      <h4 className="text-xs font-semibold text-purple-300 mb-1 flex items-center gap-2">
                        <span className="w-1.5 h-1.5 bg-purple-400 rounded-full"></span>
                        Zubereitung
                      </h4>
                      <p className="text-purple-100 text-xs">
                        {hoveredItem.preparation_method}
                      </p>
                    </div>
                  )}
                </div>

                {/* Allergene & Zusatzstoffe */}
                {(hoveredItem.allergens || hoveredItem.additives) && (
                  <div className="bg-red-900/20 rounded-lg p-4 mb-4 border border-red-500/30">
                    <h4 className="text-sm font-semibold text-red-300 mb-2 flex items-center gap-2">
                      <span className="w-2 h-2 bg-red-400 rounded-full"></span>
                      Allergene & Zusatzstoffe
                    </h4>
                    
                    {hoveredItem.allergens && (
                      <div className="mb-2">
                        <p className="text-xs font-medium text-red-200 mb-1">⚠️ Allergene:</p>
                        <p className="text-red-100 text-xs">
                          {hoveredItem.allergens}
                        </p>
                      </div>
                    )}
                    
                    {hoveredItem.additives && hoveredItem.additives !== "Keine Zusatzstoffe" && (
                      <div>
                        <p className="text-xs font-medium text-yellow-200 mb-1">🧪 Zusatzstoffe:</p>
                        <p className="text-yellow-100 text-xs">
                          {hoveredItem.additives}
                        </p>
                      </div>
                    )}
                  </div>
                )}
                
                {/* Diät-Eigenschaften */}
                <div className="bg-warm-beige/5 rounded-lg p-4 border border-warm-beige/20">
                  <h4 className="text-sm font-semibold text-warm-beige mb-3 flex items-center gap-2">
                    <span className="w-2 h-2 bg-green-400 rounded-full"></span>
                    Diät-Eigenschaften
                  </h4>
                  <div className="grid grid-cols-3 gap-3">
                    <div className={`text-center p-3 rounded-lg transition-all ${hoveredItem.vegan ? 'bg-green-500/20 border-2 border-green-500/30' : 'bg-gray-500/10 border border-gray-500/20'}`}>
                      <div className="text-xl mb-1">🌱</div>
                      <div className={`text-xs font-medium ${hoveredItem.vegan ? 'text-green-300' : 'text-gray-400'}`}>
                        Vegan
                      </div>
                    </div>
                    <div className={`text-center p-3 rounded-lg transition-all ${hoveredItem.vegetarian ? 'bg-green-500/20 border-2 border-green-500/30' : 'bg-gray-500/10 border border-gray-500/20'}`}>
                      <div className="text-xl mb-1">🌿</div>
                      <div className={`text-xs font-medium ${hoveredItem.vegetarian ? 'text-green-300' : 'text-gray-400'}`}>
                        Vegetarisch
                      </div>
                    </div>
                    <div className={`text-center p-3 rounded-lg transition-all ${hoveredItem.glutenfree ? 'bg-green-500/20 border-2 border-green-500/30' : 'bg-gray-500/10 border border-gray-500/20'}`}>
                      <div className="text-xl mb-1">🌾</div>
                      <div className={`text-xs font-medium ${hoveredItem.glutenfree ? 'text-green-300' : 'text-gray-400'}`}>
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
                <h3 className="text-warm-beige font-medium mb-2">Detaillierte Gericht-Informationen</h3>
                <p className="text-warm-beige/70 text-sm">
                  Bewegen Sie die Maus über ein Gericht<br/>
                  um detaillierte Beschreibungen,<br/>
                  Zutaten, Herkunft, Zubereitung<br/>
                  und Allergie-Informationen zu sehen
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
      
      {/* Detail Modal */}
      {selectedItem && (
        <ItemDetailModal 
          item={selectedItem} 
          onClose={() => setSelectedItem(null)} 
        />
      )}
    </div>
  );
};

export default Speisekarte;
