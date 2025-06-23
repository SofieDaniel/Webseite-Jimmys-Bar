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

  // Get unique categories with proper mapping
  const categoryMapping = {
    'Inicio / Vorspeisen': 'Inicio / Vorspeisen',
    'Salat': 'Salat', 
    'Kleine Gerichte': 'Kleine Gerichte',
    'Tapa Paella': 'Tapa Paella',
    'Tapas Vegetarian': 'Tapas Vegetarian',
    'Tapas de Pollo': 'Tapas de Pollo',
    'Tapas de Carne': 'Tapas de Carne',
    'Tapas de Pescado': 'Tapas de Pescado',
    'Kroketten': 'Kroketten',
    'Pasta': 'Pasta',
    'Pizza': 'Pizza',
    'Dessert': 'Dessert',
    'Heißgetränke': 'Heißgetränke',
    'Tee': 'Tee',
    'Softdrinks': 'Softdrinks',
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
                        {categoryMapping[category] || category}
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
                                  {parseFloat(item.price).toFixed(2).replace('.', ',')} €
                                </span>
                              </div>
                            </div>
                            
                            {/* Verfügbarkeit */}
                            {!item.is_available && (
                              <div className="text-center py-2">
                                <span className="text-red-400 text-sm font-medium">
                                  Derzeit nicht verfügbar
                                </span>
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
          </div>

          {/* Right Side - Hover Details (Detaillierte Beschreibungen, kein Preis) */}
          <div className="w-96 sticky top-24 h-fit">
            {hoveredItem ? (
              <div className="bg-gradient-to-br from-medium-brown/95 to-dark-brown/95 border-2 border-warm-beige/40 rounded-xl p-6 shadow-2xl backdrop-blur-sm">
                {/* Header */}
                <div className="border-b border-warm-beige/30 pb-4 mb-4">
                  <h3 className="text-2xl font-serif text-warm-beige mb-3 font-bold">
                    {hoveredItem.name}
                  </h3>
                  
                  <div className="flex items-center gap-2 flex-wrap mb-2">
                    <span className="bg-warm-beige/20 text-warm-beige px-3 py-1 rounded-full text-xs font-medium border border-warm-beige/30">
                      {hoveredItem.category}
                    </span>
                    <span className="bg-orange-500/20 text-orange-300 px-3 py-1 rounded-full text-xs font-medium border border-orange-500/30">
                      {hoveredItem.price} €
                    </span>
                    <div className="flex gap-1">
                      {getAllergyIcons(hoveredItem).map((icon, index) => (
                        <span key={index} className="text-lg bg-warm-beige/15 px-2 py-1 rounded border border-warm-beige/20">{icon}</span>
                      ))}
                    </div>
                  </div>

                  {/* Kurze Beschreibung */}
                  {hoveredItem.description && (
                    <p className="text-light-beige/90 text-sm italic">
                      {hoveredItem.description}
                    </p>
                  )}
                </div>

                {/* Content */}
                <div className="space-y-4">
                  {/* Detaillierte Beschreibung */}
                  <div className="bg-dark-brown/60 rounded-lg p-4 border border-warm-beige/20">
                    <h4 className="text-sm font-semibold text-warm-beige mb-3 flex items-center gap-2">
                      <span className="w-3 h-3 bg-warm-beige rounded-full"></span>
                      Detaillierte Beschreibung
                    </h4>
                    <p className="text-light-beige leading-relaxed text-sm">
                      {hoveredItem.detailed_description || hoveredItem.description || 'Authentisches spanisches Gericht, zubereitet nach traditionellem Rezept mit frischen, hochwertigen Zutaten und viel Liebe.'}
                    </p>
                  </div>

                  {/* Herkunft */}
                  {hoveredItem.origin && (
                    <div className="bg-dark-brown/60 rounded-lg p-4 border border-warm-beige/20">
                      <h4 className="text-sm font-semibold text-warm-beige mb-3 flex items-center gap-2">
                        <span className="w-3 h-3 bg-orange-400 rounded-full"></span>
                        Herkunft & Tradition
                      </h4>
                      <p className="text-light-beige text-sm leading-relaxed flex items-center gap-2">
                        <span className="text-lg">🌍</span>
                        {hoveredItem.origin}
                      </p>
                    </div>
                  )}

                  {/* Zutaten */}
                  {hoveredItem.ingredients && (
                    <div className="bg-dark-brown/60 rounded-lg p-4 border border-warm-beige/20">
                      <h4 className="text-sm font-semibold text-warm-beige mb-3 flex items-center gap-2">
                        <span className="w-3 h-3 bg-green-400 rounded-full"></span>
                        Zutaten
                      </h4>
                      <p className="text-light-beige text-sm leading-relaxed">
                        {hoveredItem.ingredients}
                      </p>
                    </div>
                  )}

                  {/* Zubereitung */}
                  {hoveredItem.preparation_method && (
                    <div className="bg-dark-brown/60 rounded-lg p-4 border border-warm-beige/20">
                      <h4 className="text-sm font-semibold text-warm-beige mb-3 flex items-center gap-2">
                        <span className="w-3 h-3 bg-blue-400 rounded-full"></span>
                        Zubereitung
                      </h4>
                      <p className="text-light-beige text-sm leading-relaxed">
                        {hoveredItem.preparation_method}
                      </p>
                    </div>
                  )}

                  {/* Allergene & Zusatzstoffe */}
                  {(hoveredItem.allergens || hoveredItem.additives) && (
                    <div className="bg-dark-brown/60 rounded-lg p-4 border border-red-400/30">
                      <h4 className="text-sm font-semibold text-red-300 mb-3 flex items-center gap-2">
                        <span className="w-3 h-3 bg-red-400 rounded-full"></span>
                        Allergene & Zusatzstoffe
                      </h4>
                      
                      {hoveredItem.allergens && hoveredItem.allergens.trim() !== '' && (
                        <div className="mb-3">
                          <p className="text-xs font-medium text-red-200 mb-2 flex items-center gap-1">
                            ⚠️ Allergene:
                          </p>
                          <p className="text-light-beige text-xs leading-relaxed bg-red-900/20 p-2 rounded">
                            {hoveredItem.allergens}
                          </p>
                        </div>
                      )}
                      
                      {hoveredItem.additives && hoveredItem.additives !== "Keine Zusatzstoffe" && hoveredItem.additives.trim() !== '' && (
                        <div>
                          <p className="text-xs font-medium text-yellow-200 mb-2 flex items-center gap-1">
                            🧪 Zusatzstoffe:
                          </p>
                          <p className="text-light-beige text-xs leading-relaxed bg-yellow-900/20 p-2 rounded">
                            {hoveredItem.additives}
                          </p>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Ernährungshinweise */}
                  {(hoveredItem.vegan || hoveredItem.vegetarian || hoveredItem.glutenfree) && (
                    <div className="bg-dark-brown/60 rounded-lg p-4 border border-warm-beige/20">
                      <h4 className="text-sm font-semibold text-warm-beige mb-3 flex items-center gap-2">
                        <span className="w-3 h-3 bg-green-500 rounded-full"></span>
                        Ernährungshinweise
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {hoveredItem.vegan && (
                          <span className="bg-green-600/30 text-green-200 px-3 py-1 rounded-full text-xs border border-green-500/50 flex items-center gap-1">
                            🌱 Vegan
                          </span>
                        )}
                        {hoveredItem.vegetarian && !hoveredItem.vegan && (
                          <span className="bg-green-600/30 text-green-200 px-3 py-1 rounded-full text-xs border border-green-500/50 flex items-center gap-1">
                            🌿 Vegetarisch
                          </span>
                        )}
                        {hoveredItem.glutenfree && (
                          <span className="bg-orange-600/30 text-orange-200 px-3 py-1 rounded-full text-xs border border-orange-500/50 flex items-center gap-1">
                            🌾 Glutenfrei
                          </span>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="bg-gradient-to-br from-amber-900/20 to-orange-900/20 border-2 border-dashed border-amber-600/40 rounded-xl p-8 text-center backdrop-blur-sm">
                <div className="text-amber-400/70 mb-6">
                  <div className="w-20 h-20 mx-auto bg-amber-600/20 rounded-full flex items-center justify-center border-2 border-amber-500/30">
                    <span className="text-4xl">🍽️</span>
                  </div>
                </div>
                <h3 className="text-amber-200 font-serif text-lg mb-3 font-semibold">Gericht-Details</h3>
                <p className="text-amber-300/80 text-sm leading-relaxed">
                  <strong>Bewegen Sie die Maus über ein Gericht</strong><br/>
                  um detaillierte Informationen zu sehen:<br/><br/>
                  🌍 <span className="text-amber-200">Herkunft & Tradition</span><br/>
                  🥘 <span className="text-amber-200">Zutaten & Zubereitung</span><br/>
                  ⚠️ <span className="text-amber-200">Allergene & Zusatzstoffe</span><br/>
                  🌱 <span className="text-amber-200">Ernährungshinweise</span>
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