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
  // Load menu items from backend
    if (!item) return null;
    
    return (
      <>
        <style>
          {`
            .modal-overlay {
              position: fixed !important;
              top: 0 !important;
              left: 0 !important;
              right: 0 !important;
              bottom: 0 !important;
              width: 100vw !important;
              height: 100vh !important;
              background: rgba(0, 0, 0, 0.8) !important;
              z-index: 999999 !important;
              overflow-y: auto !important;
              padding: 20px !important;
            }
            .modal-content {
              background: white !important;
              border-radius: 8px !important;
              max-width: 600px !important;
              width: 90% !important;
              margin: 10vh auto !important;
              min-height: 200px !important;
              box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25) !important;
              position: relative !important;
            }
          `}
        </style>
        <div className="modal-overlay" onClick={onClose}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            {/* Header */}
            <div style={{
              padding: '24px',
              borderBottom: '1px solid #fed7aa',
              background: 'linear-gradient(to right, #fef3c7, #fde68a)'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <h2 style={{
                    fontSize: '24px',
                    fontWeight: 'bold',
                    color: '#374151',
                    marginBottom: '8px',
                    fontFamily: 'serif'
                  }}>
                    {item.name}
                  </h2>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <span style={{
                      fontSize: '24px',
                      fontWeight: 'bold',
                      color: '#ea580c'
                    }}>
                      {item.price}
                    </span>
                    <span style={{
                      fontSize: '12px',
                      background: '#fed7aa',
                      color: '#c2410c',
                      padding: '4px 12px',
                      borderRadius: '20px',
                      border: '1px solid #fdba74'
                    }}>
                      {item.category}
                    </span>
                  </div>
                </div>
                <button 
                  onClick={onClose}
                  style={{
                    background: 'none',
                    border: 'none',
                    fontSize: '24px',
                    color: '#6b7280',
                    cursor: 'pointer',
                    width: '32px',
                    height: '32px',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}
                  onMouseOver={(e) => e.target.style.background = '#f3f4f6'}
                  onMouseOut={(e) => e.target.style.background = 'none'}
                >
                  ×
                </button>
              </div>
            </div>
            
            {/* Content */}
            <div style={{ padding: '24px', background: 'white' }}>
              {/* Beschreibung */}
              <div style={{ marginBottom: '24px' }}>
                <h3 style={{
                  color: '#374151',
                  fontWeight: '600',
                  marginBottom: '8px',
                  fontSize: '18px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px'
                }}>
                  <span style={{
                    width: '8px',
                    height: '8px',
                    background: '#f97316',
                    borderRadius: '50%'
                  }}></span>
                  Beschreibung
                </h3>
                <p style={{
                  color: '#4b5563',
                  lineHeight: '1.6'
                }}>
                  {item.detailed_description || item.description}
                </p>
              </div>
              
              {/* Zutaten */}
              {item.ingredients && (
                <div style={{ marginBottom: '24px' }}>
                  <h3 style={{
                    color: '#374151',
                    fontWeight: '600',
                    marginBottom: '8px',
                    fontSize: '18px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px'
                  }}>
                    <span style={{
                      width: '8px',
                      height: '8px',
                      background: '#10b981',
                      borderRadius: '50%'
                    }}></span>
                    Hauptzutaten
                  </h3>
                  <p style={{
                    color: '#4b5563',
                    lineHeight: '1.6'
                  }}>
                    {item.ingredients}
                  </p>
                </div>
              )}
              
              {/* Herkunft */}
              {item.origin && (
                <div style={{ marginBottom: '24px' }}>
                  <h3 style={{
                    color: '#374151',
                    fontWeight: '600',
                    marginBottom: '8px',
                    fontSize: '18px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px'
                  }}>
                    <span style={{
                      width: '8px',
                      height: '8px',
                      background: '#3b82f6',
                      borderRadius: '50%'
                    }}></span>
                    Herkunft
                  </h3>
                  <p style={{
                    color: '#4b5563'
                  }}>
                    {item.origin}
                  </p>
                </div>
              )}
              
              {/* Zubereitung */}
              {item.preparation_method && (
                <div style={{ marginBottom: '24px' }}>
                  <h3 style={{
                    color: '#374151',
                    fontWeight: '600',
                    marginBottom: '8px',
                    fontSize: '18px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px'
                  }}>
                    <span style={{
                      width: '8px',
                      height: '8px',
                      background: '#8b5cf6',
                      borderRadius: '50%'
                    }}></span>
                    Zubereitung
                  </h3>
                  <p style={{
                    color: '#4b5563'
                  }}>
                    {item.preparation_method}
                  </p>
                </div>
              )}
              
              {/* Allergene */}
              {item.allergens && (
                <div style={{
                  background: '#fef2f2',
                  border: '1px solid #fecaca',
                  borderRadius: '8px',
                  padding: '16px',
                  marginBottom: '24px'
                }}>
                  <h3 style={{
                    color: '#b91c1c',
                    fontWeight: '600',
                    marginBottom: '8px',
                    display: 'flex',
                    alignItems: 'center'
                  }}>
                    ⚠️ Allergene & Unverträglichkeiten
                  </h3>
                  <p style={{
                    color: '#dc2626'
                  }}>
                    {item.allergens}
                  </p>
                </div>
              )}
              
              {/* Zusatzstoffe */}
              {item.additives && item.additives !== "Keine Zusatzstoffe" && (
                <div style={{
                  background: '#fffbeb',
                  border: '1px solid #fed7aa',
                  borderRadius: '8px',
                  padding: '16px',
                  marginBottom: '24px'
                }}>
                  <h3 style={{
                    color: '#b45309',
                    fontWeight: '600',
                    marginBottom: '8px'
                  }}>
                    Zusatzstoffe
                  </h3>
                  <p style={{
                    color: '#d97706'
                  }}>
                    {item.additives}
                  </p>
                </div>
              )}
              
              {/* Eigenschaften */}
              <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                {item.vegan && (
                  <span style={{
                    background: '#dcfce7',
                    color: '#166534',
                    padding: '4px 12px',
                    borderRadius: '20px',
                    fontSize: '12px',
                    border: '1px solid #bbf7d0'
                  }}>
                    🌱 Vegan
                  </span>
                )}
                {item.vegetarian && !item.vegan && (
                  <span style={{
                    background: '#dcfce7',
                    color: '#166534',
                    padding: '4px 12px',
                    borderRadius: '20px',
                    fontSize: '12px',
                    border: '1px solid #bbf7d0'
                  }}>
                    🥬 Vegetarisch
                  </span>
                )}
                {item.glutenfree && (
                  <span style={{
                    background: '#dbeafe',
                    color: '#1e40af',
                    padding: '4px 12px',
                    borderRadius: '20px',
                    fontSize: '12px',
                    border: '1px solid #93c5fd'
                  }}>
                    🌾 Glutenfrei
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>
      </>
    );
  };

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
                      } border border-warm-beige/20`}
                      onMouseEnter={() => setHoveredItem(item)}
                      onMouseLeave={() => setHoveredItem(null)}
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
          <div className="w-96 sticky top-24 h-fit">
            {hoveredItem ? (
              <div className="bg-gradient-to-br from-medium-brown to-dark-brown border-2 border-warm-beige/40 rounded-xl p-6 shadow-2xl">
                {/* Header */}
                <div className="border-b border-warm-beige/30 pb-4 mb-4">
                  <h3 className="text-xl font-serif text-warm-beige mb-2">
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

                {/* Content */}
                <div className="space-y-4">
                  {/* Detaillierte Beschreibung */}
                  <div className="bg-dark-brown/50 rounded-lg p-4 border border-warm-beige/20">
                    <h4 className="text-sm font-semibold text-warm-beige mb-2 flex items-center gap-2">
                      <span className="w-2 h-2 bg-warm-beige rounded-full"></span>
                      Detaillierte Beschreibung
                    </h4>
                    <p className="text-light-beige leading-relaxed text-sm line-clamp-4">
                      {hoveredItem.detailed_description || hoveredItem.description}
                    </p>
                  </div>

                  {/* Zutaten */}
                  {hoveredItem.ingredients && (
                    <div className="bg-orange-900/20 rounded-lg p-4 border border-orange-500/30">
                      <h4 className="text-sm font-semibold text-orange-300 mb-2 flex items-center gap-2">
                        <span className="w-2 h-2 bg-orange-400 rounded-full"></span>
                        Zutaten
                      </h4>
                      <p className="text-orange-100 text-sm leading-relaxed line-clamp-3">
                        {hoveredItem.ingredients}
                      </p>
                    </div>
                  )}

                  {/* Allergene & Zusatzstoffe */}
                  {(hoveredItem.allergens || hoveredItem.additives) && (
                    <div className="bg-red-900/20 rounded-lg p-4 border border-red-500/30">
                      <h4 className="text-sm font-semibold text-red-300 mb-2 flex items-center gap-2">
                        <span className="w-2 h-2 bg-red-400 rounded-full"></span>
                        Allergene & Zusatzstoffe
                      </h4>
                      
                      {hoveredItem.allergens && (
                        <div className="mb-2">
                          <p className="text-xs font-medium text-red-200 mb-1">⚠️ Allergene:</p>
                          <p className="text-red-100 text-xs line-clamp-2">
                            {hoveredItem.allergens}
                          </p>
                        </div>
                      )}
                      
                      {hoveredItem.additives && hoveredItem.additives !== "Keine Zusatzstoffe" && (
                        <div>
                          <p className="text-xs font-medium text-yellow-200 mb-1">🧪 Zusatzstoffe:</p>
                          <p className="text-yellow-100 text-xs line-clamp-2">
                            {hoveredItem.additives}
                          </p>
                        </div>
                      )}
                    </div>
                  )}
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
      

    </div>
  );
};

export default Speisekarte;