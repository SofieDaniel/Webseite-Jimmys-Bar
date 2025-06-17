import React, { useState, useEffect } from 'react';

const Speisekarte = () => {
  const [menuItems, setMenuItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('all');

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

  // Get unique categories
  const categories = [...new Set(menuItems.map(item => item.category))];
  const filteredItems = selectedCategory === 'all' ? menuItems : menuItems.filter(item => item.category === selectedCategory);

  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Header Section */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              Unsere Speisekarte
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              Authentische mediterrane Küche mit frischen Zutaten
            </p>
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