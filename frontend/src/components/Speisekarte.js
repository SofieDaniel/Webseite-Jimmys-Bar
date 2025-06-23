import React, { useState, useEffect } from 'react';

// Custom styles for scrollbar and text truncation
const customScrollbarStyle = `
  .custom-scrollbar::-webkit-scrollbar {
    width: 6px;
  }
  .custom-scrollbar::-webkit-scrollbar-track {
    background: rgba(139, 69, 19, 0.3);
    border-radius: 3px;
  }
  .custom-scrollbar::-webkit-scrollbar-thumb {
    background: rgba(255, 228, 196, 0.5);
    border-radius: 3px;
  }
  .custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 228, 196, 0.7);
  }
  
  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  
  .line-clamp-3 {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  
  .line-clamp-4 {
    display: -webkit-box;
    -webkit-line-clamp: 4;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
`;

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

  // Get unique categories with proper mapping and custom order
  const categoryMapping = {
    'Inicio / Vorspeisen': 'Vorspeisen',
    'Salate': 'Salate', 
    'Tapa Paella': 'Paella',
    'Tapas Vegetarian': 'Vegetarisch',
    'Tapas de Pollo': 'Hähnchen',
    'Tapas de Carne': 'Fleisch',
    'Tapas de Pescado': 'Fisch',
    'Kroketten': 'Kroketten',
    'Pasta': 'Pasta',
    'Pizza': 'Pizza',
    'Für den kleinen und großen Hunger': 'Snacks',
    'Dessert & Eis': 'Dessert',
    'Heißgetränke & Tee': 'Heißgetränke',
    'Softdrinks': 'Softdrinks',
    'Spanische Getränke': 'Sangria'
  };

  // Define the order of categories (food first, drinks last) - using DB names
  const categoryOrder = [
    'Inicio / Vorspeisen', 'Salate', 'Tapa Paella', 'Tapas Vegetarian', 'Tapas de Pollo', 'Tapas de Carne', 'Tapas de Pescado', 
    'Kroketten', 'Pasta', 'Pizza', 'Für den kleinen und großen Hunger', 'Dessert & Eis',
    // Getränke zuletzt
    'Heißgetränke & Tee', 'Softdrinks', 'Spanische Getränke'
  ];

  // Get available categories from actual menu items
  const availableCategories = [...new Set(menuItems.map(item => item.category))];
  const availableCategoryOrder = categoryOrder.filter(cat => availableCategories.includes(cat));
  
  const allCategories = ['Alle Kategorien', ...availableCategoryOrder.map(cat => categoryMapping[cat] || cat)];
  const filteredItems = selectedCategory === 'Alle Kategorien' 
    ? menuItems 
    : menuItems.filter(item => (categoryMapping[item.category] || item.category) === selectedCategory);

  // Group items by category for display with custom order
  const groupedItems = availableCategoryOrder.reduce((acc, dbCategory) => {
    const displayCategory = categoryMapping[dbCategory] || dbCategory;
    const itemsInCategory = selectedCategory === 'Alle Kategorien' 
      ? menuItems.filter(item => item.category === dbCategory)
      : filteredItems.filter(item => item.category === dbCategory);
    if (itemsInCategory.length > 0) {
      acc[displayCategory] = itemsInCategory;
    }
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
      {/* Add custom scrollbar styles */}
      <style>{customScrollbarStyle}</style>
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
                  <div key={category} className="mb-12">
                    <div className="bg-dark-brown/95 backdrop-blur-sm py-4 mb-8 border-b border-warm-beige/30">
                      <h3 className="text-3xl font-serif text-warm-beige text-center tracking-wide">
                        {category}
                      </h3>
                    </div>
                    <div className="grid gap-6">
                      {items.map((item) => (
                        <div 
                          key={item.id} 
                          className="bg-medium-brown rounded-xl border border-warm-brown overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer hover:border-warm-beige hover:scale-[1.02]"
                          onMouseEnter={() => setHoveredItem(item)}
                          onMouseLeave={() => setHoveredItem(null)}
                        >
                          <div className="p-6">
                            <div className="flex justify-between items-start mb-4">
                              <div className="flex-1">
                                <h4 className="text-xl font-serif text-warm-beige mb-2 flex items-center gap-2">
                                  {item.name}
                                  <div className="flex gap-1">
                                    {getAllergyIcons(item).map((icon, idx) => (
                                      <span key={idx} className="text-sm">{icon}</span>
                                    ))}
                                  </div>
                                </h4>
                                {/* Gericht Beschreibung */}
                                {item.description && (
                                  <p className="text-light-beige font-light text-sm leading-relaxed mb-3">
                                    {item.description}
                                  </p>
                                )}
                                {/* Allergen Information */}
                                {item.allergens && item.allergens !== '-' && (
                                  <div className="bg-dark-brown/50 rounded-lg p-3 mb-3">
                                    <p className="text-orange-400 text-xs font-medium mb-1">Allergene:</p>
                                    <p className="text-light-beige text-xs leading-relaxed">
                                      {item.allergens}
                                    </p>
                                  </div>
                                )}
                              </div>
                              <div className="text-right ml-4">
                                <span className="text-2xl font-bold text-warm-beige">
                                  {typeof item.price === 'string' ? parseFloat(item.price).toFixed(2).replace('.', ',') : item.price.toFixed(2).replace('.', ',')} €
                                </span>
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
          </div>

          {/* Right Side - Hover Details (Kompakt mit Scroll) */}
          <div className="w-96 sticky top-24 h-fit">
            {hoveredItem ? (
              <div className="bg-gradient-to-br from-medium-brown/95 to-dark-brown/95 border-2 border-warm-beige/40 rounded-xl shadow-2xl backdrop-blur-sm max-h-[80vh] overflow-y-auto">
                {/* Header - Fixed */}
                <div className="border-b border-warm-beige/30 p-4 bg-dark-brown/80 sticky top-0">
                  <h3 className="text-xl font-serif text-warm-beige mb-2 font-bold">
                    {hoveredItem.name}
                  </h3>
                  
                  <div className="flex items-center gap-2 flex-wrap mb-2">
                    <span className="bg-warm-beige/20 text-warm-beige px-2 py-1 rounded-full text-xs font-medium">
                      {hoveredItem.category}
                    </span>
                    <span className="bg-orange-500/20 text-orange-300 px-2 py-1 rounded-full text-xs font-medium">
                      {hoveredItem.price} €
                    </span>
                    <div className="flex gap-1">
                      {getAllergyIcons(hoveredItem).map((icon, index) => (
                        <span key={index} className="text-sm bg-warm-beige/15 px-1 py-0.5 rounded">{icon}</span>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Scrollable Content */}
                <div className="p-4 space-y-3">
                  {/* Kompakte Beschreibung */}
                  {hoveredItem.detailed_description && (
                    <div className="bg-dark-brown/60 rounded-lg p-3">
                      <p className="text-light-beige leading-relaxed text-sm">
                        {hoveredItem.detailed_description}
                      </p>
                    </div>
                  )}

                  {/* Kompakte Infos in 2 Spalten */}
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    {/* Herkunft */}
                    {hoveredItem.origin && (
                      <div className="bg-dark-brown/40 rounded p-2">
                        <p className="text-orange-400 font-medium mb-1">Herkunft</p>
                        <p className="text-light-beige">{hoveredItem.origin}</p>
                      </div>
                    )}
                    
                    {/* Zubereitung */}
                    {hoveredItem.preparation_method && (
                      <div className="bg-dark-brown/40 rounded p-2">
                        <p className="text-orange-400 font-medium mb-1">Zubereitung</p>
                        <p className="text-light-beige">{hoveredItem.preparation_method}</p>
                      </div>
                    )}
                  </div>

                  {/* Zutaten */}
                  {hoveredItem.ingredients && (
                    <div className="bg-dark-brown/40 rounded p-2">
                      <p className="text-orange-400 font-medium text-xs mb-1">Zutaten</p>
                      <p className="text-light-beige text-xs leading-relaxed">
                        {hoveredItem.ingredients}
                      </p>
                    </div>
                  )}

                  {/* Allergene */}
                  {hoveredItem.allergens && hoveredItem.allergens.trim() !== '' && hoveredItem.allergens !== 'Keine' && (
                    <div className="bg-red-900/30 rounded p-2 border border-red-500/30">
                      <p className="text-red-400 font-medium text-xs mb-1">⚠️ Allergene</p>
                      <p className="text-light-beige text-xs">
                        {hoveredItem.allergens}
                      </p>
                    </div>
                  )}

                  {/* Dietary Tags */}
                  {(hoveredItem.vegan || hoveredItem.vegetarian || hoveredItem.glutenfree) && (
                    <div className="flex gap-1 flex-wrap">
                      {hoveredItem.vegan && (
                        <span className="bg-green-600/20 text-green-400 px-2 py-1 rounded text-xs border border-green-600/30">🌱 Vegan</span>
                      )}
                      {hoveredItem.vegetarian && !hoveredItem.vegan && (
                        <span className="bg-green-600/20 text-green-400 px-2 py-1 rounded text-xs border border-green-600/30">🌿 Vegetarisch</span>
                      )}
                      {hoveredItem.glutenfree && (
                        <span className="bg-blue-600/20 text-blue-400 px-2 py-1 rounded text-xs border border-blue-600/30">🌾 Glutenfrei</span>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="bg-gradient-to-br from-medium-brown/20 to-dark-brown/20 border-2 border-dashed border-warm-beige/30 rounded-xl p-8 text-center backdrop-blur-sm">
                <div className="text-warm-beige/70 mb-6">
                  <div className="w-20 h-20 mx-auto bg-warm-beige/10 rounded-full flex items-center justify-center border-2 border-warm-beige/20">
                    <span className="text-4xl">🍽️</span>
                  </div>
                </div>
                <h3 className="text-warm-beige font-serif text-lg mb-3 font-semibold">Gericht-Details</h3>
                <p className="text-light-beige/80 text-sm leading-relaxed">
                  <strong>Bewegen Sie die Maus über ein Gericht</strong><br/>
                  um detaillierte Informationen zu sehen:<br/><br/>
                  🌍 <span className="text-warm-beige">Herkunft & Tradition</span><br/>
                  🥘 <span className="text-warm-beige">Zutaten</span><br/>
                  ⚠️ <span className="text-warm-beige">Allergene & Zusatzstoffe</span><br/>
                  🌱 <span className="text-warm-beige">Ernährungshinweise</span>
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