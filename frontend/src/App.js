import React, { useState } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Link, useNavigate } from "react-router-dom";

// Header Component
const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  
  return (
    <header className="bg-gradient-to-r from-amber-900 via-amber-800 to-amber-900 text-amber-50 shadow-2xl relative">
      <div className="absolute inset-0 bg-texture opacity-20"></div>
      <div className="container mx-auto px-4 py-4 relative z-10">
        <nav className="flex justify-between items-center">
          <Link to="/" className="text-3xl font-serif font-bold text-amber-100 tracking-wide">
            JIMMY'S
            <span className="block text-sm text-amber-300 tracking-[0.3em] font-sans">TAPAS BAR</span>
          </Link>
          
          <div className="hidden md:flex space-x-8">
            <Link to="/" className="hover:text-amber-300 transition-colors font-medium">Startseite</Link>
            <Link to="/standorte" className="hover:text-amber-300 transition-colors font-medium">Standorte</Link>
            <Link to="/speisekarte" className="hover:text-amber-300 transition-colors font-medium">Speisekarte</Link>
            <Link to="/bewertungen" className="hover:text-amber-300 transition-colors font-medium">Bewertungen</Link>
            <Link to="/ueber-uns" className="hover:text-amber-300 transition-colors font-medium">Über uns</Link>
            <Link to="/kontakt" className="hover:text-amber-300 transition-colors font-medium">Kontakt</Link>
          </div>
          
          <Link to="/speisekarte" className="hidden md:block bg-amber-600 hover:bg-amber-500 px-6 py-2 rounded-full transition-colors font-medium border border-amber-400">
            ZUR SPEISEKARTE
          </Link>
          
          <button 
            className="md:hidden"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            <div className="w-6 h-6 flex flex-col justify-center space-y-1">
              <div className="w-6 h-0.5 bg-amber-100"></div>
              <div className="w-6 h-0.5 bg-amber-100"></div>
              <div className="w-6 h-0.5 bg-amber-100"></div>
            </div>
          </button>
        </nav>
        
        {isMenuOpen && (
          <div className="md:hidden mt-4 bg-amber-800 rounded-lg p-4">
            <Link to="/" className="block py-2 hover:text-amber-300">Startseite</Link>
            <Link to="/standorte" className="block py-2 hover:text-amber-300">Standorte</Link>
            <Link to="/speisekarte" className="block py-2 hover:text-amber-300">Speisekarte</Link>
            <Link to="/bewertungen" className="block py-2 hover:text-amber-300">Bewertungen</Link>
            <Link to="/ueber-uns" className="block py-2 hover:text-amber-300">Über uns</Link>
            <Link to="/kontakt" className="block py-2 hover:text-amber-300">Kontakt</Link>
          </div>
        )}
      </div>
    </header>
  );
};

// Home Page Component
const Home = () => {
  const navigate = useNavigate();
  
  return (
    <div className="min-h-screen bg-amber-50">
      {/* Hero Section */}
      <section className="relative h-screen bg-cover bg-center bg-gradient-to-b from-black/40 to-black/60" 
               style={{backgroundImage: `url('https://images.pexels.com/photos/19250676/pexels-photo-19250676.jpeg')`}}>
        <div className="absolute inset-0 bg-gradient-to-b from-black/30 to-black/50"></div>
        <div className="relative z-10 flex items-center justify-center h-full text-center text-white px-4">
          <div className="max-w-4xl">
            <h1 className="text-5xl md:text-7xl font-serif font-bold mb-6 text-amber-100 drop-shadow-2xl">
              AUTHENTISCHE<br />
              <span className="text-amber-300">TAPAS & WEIN</span>
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-amber-100 drop-shadow-xl">
              Spanische Genüsse – Authentisch & Gemütlich
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button 
                onClick={() => navigate('/standorte')}
                className="bg-amber-600 hover:bg-amber-500 text-white px-8 py-4 rounded-full text-lg font-medium transition-all duration-300 transform hover:scale-105 shadow-xl"
              >
                STANDORT WÄHLEN
              </button>
              <button 
                onClick={() => navigate('/speisekarte')}
                className="border-2 border-amber-300 text-amber-100 hover:bg-amber-300 hover:text-amber-900 px-8 py-4 rounded-full text-lg font-medium transition-all duration-300"
              >
                ZUR SPEISEKARTE
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-amber-50">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-20 h-20 bg-amber-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">🍷</span>
              </div>
              <h3 className="text-xl font-serif font-bold text-amber-900 mb-2">Authentische Tapas</h3>
              <p className="text-amber-800">Traditionelle spanische Küche mit frischen, hochwertigen Zutaten</p>
            </div>
            <div className="text-center">
              <div className="w-20 h-20 bg-amber-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">🥘</span>
              </div>
              <h3 className="text-xl font-serif font-bold text-amber-900 mb-2">Frische Paella</h3>
              <p className="text-amber-800">Täglich frisch zubereitet mit den besten Meeresfrüchten und Zutaten</p>
            </div>
            <div className="text-center">
              <div className="w-20 h-20 bg-amber-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">🏖️</span>
              </div>
              <h3 className="text-xl font-serif font-bold text-amber-900 mb-2">Zwei Standorte</h3>
              <p className="text-amber-800">In Neustadt und Großenbrode direkt an der Ostsee</p>
            </div>
          </div>
        </div>
      </section>

      {/* Food Gallery */}
      <section className="py-16 bg-gradient-to-b from-amber-100 to-amber-50">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-serif font-bold text-center text-amber-900 mb-12">
            Unsere Spezialitäten
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white rounded-lg shadow-xl overflow-hidden transform hover:scale-105 transition-transform">
              <img src="https://images.unsplash.com/photo-1565599837634-134bc3aadce8" alt="Patatas Bravas" className="w-full h-48 object-cover" />
              <div className="p-4">
                <h3 className="font-serif font-bold text-amber-900">Patatas Bravas</h3>
                <p className="text-amber-700 text-sm">Klassische spanische Kartoffeln</p>
              </div>
            </div>
            <div className="bg-white rounded-lg shadow-xl overflow-hidden transform hover:scale-105 transition-transform">
              <img src="https://images.unsplash.com/photo-1630175860333-5131bda75071" alt="Paella" className="w-full h-48 object-cover" />
              <div className="p-4">
                <h3 className="font-serif font-bold text-amber-900">Paella Valenciana</h3>
                <p className="text-amber-700 text-sm">Traditionelle spanische Paella</p>
              </div>
            </div>
            <div className="bg-white rounded-lg shadow-xl overflow-hidden transform hover:scale-105 transition-transform">
              <img src="https://images.pexels.com/photos/19671352/pexels-photo-19671352.jpeg" alt="Tapas" className="w-full h-48 object-cover" />
              <div className="p-4">
                <h3 className="font-serif font-bold text-amber-900">Tapas Variation</h3>
                <p className="text-amber-700 text-sm">Auswahl spanischer Köstlichkeiten</p>
              </div>
            </div>
            <div className="bg-white rounded-lg shadow-xl overflow-hidden transform hover:scale-105 transition-transform">
              <img src="https://images.unsplash.com/photo-1588276552401-30058a0fe57b" alt="Seafood Paella" className="w-full h-48 object-cover" />
              <div className="p-4">
                <h3 className="font-serif font-bold text-amber-900">Paella Mariscos</h3>
                <p className="text-amber-700 text-sm">Meeresfrüchte-Paella</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

// Menu Page Component
const Speisekarte = () => {
  const [selectedCategory, setSelectedCategory] = useState('alle');
  
  const menuItems = {
    'tapas-vegetarianas': [
      { name: 'Papas Bravas (vegan)', description: 'Klassische Kartoffeln mit scharfer Soße', price: '6,90' },
      { name: 'Falafel mit Joghurt-Minzsoße', description: 'Hausgemachte Falafel mit frischer Minzsoße', price: '6,90' },
      { name: 'Aceitunas Mixtas', description: 'Gemischte Oliven mit Kräutern', price: '4,90' },
      { name: 'Pan con Tomate', description: 'Geröstetes Brot mit Tomaten und Olivenöl', price: '5,90' }
    ],
    'tapas-pollo': [
      { name: 'Hähnchenfilet mit Limettensoße', description: 'Zartes Hähnchenfilet in würziger Limettensoße', price: '7,20' },
      { name: 'Pollo al Ajillo', description: 'Hähnchen in Knoblauchöl', price: '7,50' },
      { name: 'Alitas de Pollo', description: 'Würzige Hähnchenflügel', price: '6,90' }
    ],
    'tapas-carne': [
      { name: 'Chorizo al Diablo', description: 'Scharfe Chorizo in Teufelssauce', price: '6,90' },
      { name: 'Albóndigas', description: 'Spanische Hackfleischbällchen in Tomatensoße', price: '7,20' },
      { name: 'Jamón Ibérico', description: 'Hochwertiger spanischer Schinken', price: '12,90' }
    ],
    'tapas-pescado': [
      { name: 'Gambas al Ajillo', description: 'Garnelen in Knoblauchöl', price: '8,90' },
      { name: 'Pulpo a la Gallega', description: 'Oktopus nach galicischer Art', price: '9,90' },
      { name: 'Calamares Fritos', description: 'Frittierte Tintenfischringe', price: '7,90' }
    ],
    'paella': [
      { name: 'Paella Valenciana', description: 'Klassische Paella mit Hähnchen und Gemüse', price: '16,90' },
      { name: 'Paella Mariscos', description: 'Meeresfrüchte-Paella', price: '18,90' },
      { name: 'Paella Mixta', description: 'Gemischte Paella mit Fleisch und Meeresfrüchten', price: '17,90' }
    ],
    'pizza': [
      { name: 'Pizza Margherita', description: 'Tomaten, Mozzarella, Basilikum', price: '9,90' },
      { name: 'Pizza Española', description: 'Chorizo, Paprika, Zwiebeln', price: '11,90' },
      { name: 'Pizza Quattro Stagioni', description: 'Vier Jahreszeiten', price: '12,90' }
    ],
    'pasta': [
      { name: 'Spaghetti Carbonara', description: 'Klassische Carbonara mit Speck und Ei', price: '10,90' },
      { name: 'Penne Arrabiata', description: 'Scharfe Tomatensoße mit Chili', price: '9,90' },
      { name: 'Linguine alle Vongole', description: 'Mit Venusmuscheln', price: '13,90' }
    ],
    'dessert': [
      { name: 'Crema Catalana', description: 'Katalanische Crème brûlée', price: '5,90' },
      { name: 'Flan', description: 'Spanischer Karamellpudding', price: '5,50' },
      { name: 'Churros con Chocolate', description: 'Spanisches Spritzgebäck mit Schokolade', price: '6,90' }
    ],
    'getraenke': [
      { name: 'Aperol Spritz', description: 'Erfrischender Aperitif', price: '8,50' },
      { name: 'Sangria', description: 'Hausgemacht mit Früchten', price: '7,90' },
      { name: 'Rioja Tinto', description: 'Spanischer Rotwein', price: '4,90' },
      { name: 'Estrella Damm', description: 'Spanisches Bier', price: '3,90' }
    ]
  };

  const categories = [
    { id: 'alle', name: 'Alle Kategorien' },
    { id: 'tapas-vegetarianas', name: 'Tapas Vegetarianas' },
    { id: 'tapas-pollo', name: 'Tapas de Pollo' },
    { id: 'tapas-carne', name: 'Tapas de Carne' },
    { id: 'tapas-pescado', name: 'Tapas de Pescado' },
    { id: 'paella', name: 'Paella' },
    { id: 'pizza', name: 'Pizza' },
    { id: 'pasta', name: 'Pasta' },
    { id: 'dessert', name: 'Dessert' },
    { id: 'getraenke', name: 'Getränke' }
  ];

  const getDisplayItems = () => {
    if (selectedCategory === 'alle') {
      return Object.entries(menuItems).flatMap(([category, items]) => 
        items.map(item => ({ ...item, category }))
      );
    }
    return menuItems[selectedCategory]?.map(item => ({ ...item, category: selectedCategory })) || [];
  };

  return (
    <div className="min-h-screen bg-amber-50 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-serif font-bold text-center text-amber-900 mb-8">
          Speisekarte
        </h1>
        
        {/* Category Filter */}
        <div className="flex flex-wrap justify-center gap-2 mb-8">
          {categories.map(category => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`px-4 py-2 rounded-full transition-colors ${
                selectedCategory === category.id
                  ? 'bg-amber-600 text-white'
                  : 'bg-white text-amber-800 hover:bg-amber-100'
              }`}
            >
              {category.name}
            </button>
          ))}
        </div>

        {/* Menu Items */}
        <div className="grid gap-4 max-w-4xl mx-auto">
          {getDisplayItems().map((item, index) => (
            <div key={index} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="text-xl font-serif font-bold text-amber-900 mb-2">{item.name}</h3>
                  <p className="text-amber-700 mb-2">{item.description}</p>
                  <span className="text-sm text-amber-600 capitalize">
                    {categories.find(c => c.id === item.category)?.name}
                  </span>
                </div>
                <div className="text-2xl font-bold text-amber-900 ml-4">
                  {item.price} €
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// Locations Page Component
const Standorte = () => {
  return (
    <div className="min-h-screen bg-amber-50 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-serif font-bold text-center text-amber-900 mb-12">
          Unsere Standorte
        </h1>
        
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Neustadt Location */}
          <div className="bg-white rounded-lg shadow-xl overflow-hidden">
            <img 
              src="https://images.unsplash.com/photo-1665758564776-f2aa6b41327e" 
              alt="Restaurant Neustadt" 
              className="w-full h-64 object-cover"
            />
            <div className="p-6">
              <h2 className="text-2xl font-serif font-bold text-amber-900 mb-4">
                Jimmy's Tapas Bar Neustadt
              </h2>
              <div className="space-y-3 text-amber-800">
                <div className="flex items-center">
                  <span className="text-xl mr-3">📍</span>
                  <div>
                    <p className="font-medium">Am Strande 21</p>
                    <p>23730 Neustadt in Holstein</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <span className="text-xl mr-3">🕒</span>
                  <div>
                    <p className="font-medium">Öffnungszeiten:</p>
                    <p>Täglich 12:00–22:00 Uhr (Sommersaison)</p>
                    <p className="text-sm text-amber-600">Winterbetrieb unregelmäßig</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <span className="text-xl mr-3">📞</span>
                  <p>Telefon: +49 (0) 4561 123456</p>
                </div>
              </div>
              <div className="mt-6 h-64 bg-amber-100 rounded-lg flex items-center justify-center">
                <p className="text-amber-700">Google Maps Karte - Neustadt</p>
                <p className="text-sm text-amber-600 ml-2">(Integration folgt)</p>
              </div>
            </div>
          </div>

          {/* Großenbrode Location */}
          <div className="bg-white rounded-lg shadow-xl overflow-hidden">
            <img 
              src="https://images.unsplash.com/photo-1665758564796-5162ff406254" 
              alt="Restaurant Großenbrode" 
              className="w-full h-64 object-cover"
            />
            <div className="p-6">
              <h2 className="text-2xl font-serif font-bold text-amber-900 mb-4">
                Jimmy's Tapas Bar Großenbrode
              </h2>
              <div className="space-y-3 text-amber-800">
                <div className="flex items-center">
                  <span className="text-xl mr-3">📍</span>
                  <div>
                    <p className="font-medium">Südstrand 54</p>
                    <p>23755 Großenbrode</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <span className="text-xl mr-3">🕒</span>
                  <div>
                    <p className="font-medium">Öffnungszeiten:</p>
                    <p>Täglich 12:00–22:00 Uhr (Sommersaison)</p>
                    <p className="text-sm text-amber-600">Winterbetrieb unregelmäßig</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <span className="text-xl mr-3">📞</span>
                  <p>Telefon: +49 (0) 4561 789012</p>
                </div>
              </div>
              <div className="mt-6 h-64 bg-amber-100 rounded-lg flex items-center justify-center">
                <p className="text-amber-700">Google Maps Karte - Großenbrode</p>
                <p className="text-sm text-amber-600 ml-2">(Integration folgt)</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// About Us Page Component
const UeberUns = () => {
  return (
    <div className="min-h-screen bg-amber-50 py-8">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-serif font-bold text-center text-amber-900 mb-12">
            Über uns
          </h1>
          
          <div className="bg-white rounded-lg shadow-xl p-8 mb-8">
            <div className="grid md:grid-cols-2 gap-8 items-center">
              <div>
                <img 
                  src="https://images.unsplash.com/photo-1665758564802-f611df512d8d" 
                  alt="Jimmy" 
                  className="w-full rounded-lg shadow-lg"
                />
              </div>
              <div>
                <h2 className="text-3xl font-serif font-bold text-amber-900 mb-4">
                  Jimmy Rodríguez
                </h2>
                <p className="text-amber-800 mb-4 leading-relaxed">
                  Seit über 15 Jahren bringe ich die authentischen Aromen Spaniens an die deutsche Ostseeküste. 
                  Meine Leidenschaft für die spanische Küche begann in den kleinen Tapas-Bars von Sevilla, 
                  wo ich die Geheimnisse traditioneller Rezepte erlernte.
                </p>
                <p className="text-amber-800 mb-4 leading-relaxed">
                  In Jimmy's Tapas Bar verwenden wir nur die besten Zutaten - von handverlesenem Olivenöl 
                  aus Andalusien bis hin zu frischen Meeresfrüchten aus der Ostsee. Jedes Gericht wird mit 
                  Liebe und Respekt vor der spanischen Tradition zubereitet.
                </p>
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-white rounded-lg shadow-lg p-6 text-center">
              <div className="text-4xl mb-4">🍷</div>
              <h3 className="text-xl font-serif font-bold text-amber-900 mb-2">Qualität</h3>
              <p className="text-amber-800">
                Nur die besten Zutaten für authentische spanische Geschmackserlebnisse
              </p>
            </div>
            <div className="bg-white rounded-lg shadow-lg p-6 text-center">
              <div className="text-4xl mb-4">❤️</div>
              <h3 className="text-xl font-serif font-bold text-amber-900 mb-2">Gastfreundschaft</h3>
              <p className="text-amber-800">
                Herzliche Atmosphäre und persönlicher Service für jeden Gast
              </p>
            </div>
            <div className="bg-white rounded-lg shadow-lg p-6 text-center">
              <div className="text-4xl mb-4">🎉</div>
              <h3 className="text-xl font-serif font-bold text-amber-900 mb-2">Lebensfreude</h3>
              <p className="text-amber-800">
                Spanische Lebensart und Genuss in gemütlicher Atmosphäre
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Reviews Page Component
const Bewertungen = () => {
  const [feedback, setFeedback] = useState({
    name: '',
    email: '',
    rating: 5,
    comment: ''
  });

  const reviews = [
    {
      name: "Maria Schmidt",
      rating: 5,
      comment: "Absolut authentische spanische Küche! Die Paella war fantastisch und der Service sehr herzlich.",
      date: "März 2024"
    },
    {
      name: "Thomas Müller",
      rating: 5,
      comment: "Die beste Tapas-Bar an der Ostsee! Wir kommen immer wieder gerne nach Neustadt.",
      date: "Februar 2024"
    },
    {
      name: "Anna Petersen",
      rating: 4,
      comment: "Tolle Atmosphäre und leckeres Essen. Besonders die Gambas al Ajillo sind zu empfehlen!",
      date: "Januar 2024"
    }
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    alert('Vielen Dank für Ihr Feedback! Es wurde intern gespeichert.');
    setFeedback({ name: '', email: '', rating: 5, comment: '' });
  };

  const renderStars = (rating) => {
    return Array.from({ length: 5 }, (_, i) => (
      <span key={i} className={`text-2xl ${i < rating ? 'text-yellow-400' : 'text-gray-300'}`}>
        ★
      </span>
    ));
  };

  return (
    <div className="min-h-screen bg-amber-50 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-serif font-bold text-center text-amber-900 mb-12">
          Bewertungen & Feedback
        </h1>
        
        <div className="grid lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
          {/* Public Reviews */}
          <div>
            <h2 className="text-2xl font-serif font-bold text-amber-900 mb-6">
              Kundenbewertungen
            </h2>
            <div className="space-y-6">
              {reviews.map((review, index) => (
                <div key={index} className="bg-white rounded-lg shadow-lg p-6">
                  <div className="flex justify-between items-start mb-3">
                    <h3 className="font-bold text-amber-900">{review.name}</h3>
                    <span className="text-sm text-amber-600">{review.date}</span>
                  </div>
                  <div className="flex mb-3">
                    {renderStars(review.rating)}
                  </div>
                  <p className="text-amber-800">{review.comment}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Feedback Form */}
          <div>
            <h2 className="text-2xl font-serif font-bold text-amber-900 mb-6">
              Ihr Feedback
            </h2>
            <div className="bg-white rounded-lg shadow-lg p-6">
              <p className="text-amber-700 mb-4 text-sm">
                Dieses Feedback wird intern gespeichert und nicht öffentlich angezeigt.
              </p>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-amber-900 font-medium mb-2">Name</label>
                  <input
                    type="text"
                    value={feedback.name}
                    onChange={(e) => setFeedback({...feedback, name: e.target.value})}
                    className="w-full p-3 border border-amber-200 rounded-lg focus:ring-2 focus:ring-amber-400 focus:border-amber-400"
                    required
                  />
                </div>
                <div>
                  <label className="block text-amber-900 font-medium mb-2">E-Mail</label>
                  <input
                    type="email"
                    value={feedback.email}
                    onChange={(e) => setFeedback({...feedback, email: e.target.value})}
                    className="w-full p-3 border border-amber-200 rounded-lg focus:ring-2 focus:ring-amber-400 focus:border-amber-400"
                    required
                  />
                </div>
                <div>
                  <label className="block text-amber-900 font-medium mb-2">Bewertung</label>
                  <div className="flex space-x-2">
                    {[1,2,3,4,5].map(star => (
                      <button
                        key={star}
                        type="button"
                        onClick={() => setFeedback({...feedback, rating: star})}
                        className={`text-3xl ${star <= feedback.rating ? 'text-yellow-400' : 'text-gray-300'} hover:text-yellow-400`}
                      >
                        ★
                      </button>
                    ))}
                  </div>
                </div>
                <div>
                  <label className="block text-amber-900 font-medium mb-2">Kommentar</label>
                  <textarea
                    value={feedback.comment}
                    onChange={(e) => setFeedback({...feedback, comment: e.target.value})}
                    className="w-full p-3 border border-amber-200 rounded-lg focus:ring-2 focus:ring-amber-400 focus:border-amber-400 h-32"
                    required
                  />
                </div>
                <button
                  type="submit"
                  className="w-full bg-amber-600 hover:bg-amber-500 text-white py-3 rounded-lg font-medium transition-colors"
                >
                  Feedback senden
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Contact Page Component
const Kontakt = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: '',
    location: 'neustadt'
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    alert('Vielen Dank für Ihre Nachricht! Wir melden uns bald bei Ihnen.');
    setFormData({ name: '', email: '', phone: '', message: '', location: 'neustadt' });
  };

  return (
    <div className="min-h-screen bg-amber-50 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-serif font-bold text-center text-amber-900 mb-12">
          Kontakt
        </h1>
        
        <div className="grid lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
          {/* Contact Information */}
          <div>
            <h2 className="text-2xl font-serif font-bold text-amber-900 mb-6">
              Kontaktinformationen
            </h2>
            
            <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
              <h3 className="text-xl font-bold text-amber-900 mb-4">Neustadt in Holstein</h3>
              <div className="space-y-2 text-amber-800">
                <p>📍 Am Strande 21, 23730 Neustadt in Holstein</p>
                <p>📞 +49 (0) 4561 123456</p>
                <p>✉️ neustadt@jimmys-tapasbar.de</p>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
              <h3 className="text-xl font-bold text-amber-900 mb-4">Großenbrode</h3>
              <div className="space-y-2 text-amber-800">
                <p>📍 Südstrand 54, 23755 Großenbrode</p>
                <p>📞 +49 (0) 4561 789012</p>
                <p>✉️ grossenbrode@jimmys-tapasbar.de</p>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-bold text-amber-900 mb-4">Allgemein</h3>
              <div className="space-y-2 text-amber-800">
                <p>🌐 www.jimmys-tapasbar.de</p>
                <p>✉️ info@jimmys-tapasbar.de</p>
                <p>🕒 Täglich 12:00–22:00 Uhr (Sommersaison)</p>
              </div>
            </div>
          </div>

          {/* Contact Form */}
          <div>
            <h2 className="text-2xl font-serif font-bold text-amber-900 mb-6">
              Nachricht senden
            </h2>
            <div className="bg-white rounded-lg shadow-lg p-6">
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-amber-900 font-medium mb-2">Name *</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    className="w-full p-3 border border-amber-200 rounded-lg focus:ring-2 focus:ring-amber-400 focus:border-amber-400"
                    required
                  />
                </div>
                <div>
                  <label className="block text-amber-900 font-medium mb-2">E-Mail *</label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    className="w-full p-3 border border-amber-200 rounded-lg focus:ring-2 focus:ring-amber-400 focus:border-amber-400"
                    required
                  />
                </div>
                <div>
                  <label className="block text-amber-900 font-medium mb-2">Telefon</label>
                  <input
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => setFormData({...formData, phone: e.target.value})}
                    className="w-full p-3 border border-amber-200 rounded-lg focus:ring-2 focus:ring-amber-400 focus:border-amber-400"
                  />
                </div>
                <div>
                  <label className="block text-amber-900 font-medium mb-2">Standort</label>
                  <select
                    value={formData.location}
                    onChange={(e) => setFormData({...formData, location: e.target.value})}
                    className="w-full p-3 border border-amber-200 rounded-lg focus:ring-2 focus:ring-amber-400 focus:border-amber-400"
                  >
                    <option value="neustadt">Neustadt in Holstein</option>
                    <option value="grossenbrode">Großenbrode</option>
                    <option value="beide">Beide Standorte</option>
                  </select>
                </div>
                <div>
                  <label className="block text-amber-900 font-medium mb-2">Nachricht *</label>
                  <textarea
                    value={formData.message}
                    onChange={(e) => setFormData({...formData, message: e.target.value})}
                    className="w-full p-3 border border-amber-200 rounded-lg focus:ring-2 focus:ring-amber-400 focus:border-amber-400 h-32"
                    required
                  />
                </div>
                <button
                  type="submit"
                  className="w-full bg-amber-600 hover:bg-amber-500 text-white py-3 rounded-lg font-medium transition-colors"
                >
                  Nachricht senden
                </button>
              </form>
              
              <div className="mt-6 pt-6 border-t border-amber-200">
                <h4 className="font-bold text-amber-900 mb-2">Datenschutz</h4>
                <p className="text-sm text-amber-700">
                  Ihre Daten werden vertraulich behandelt und gemäß DSGVO verarbeitet. 
                  Weitere Informationen finden Sie in unserem Impressum.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Footer Component
const Footer = () => {
  return (
    <footer className="bg-gradient-to-r from-amber-900 via-amber-800 to-amber-900 text-amber-100 py-8">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-xl font-serif font-bold mb-4">Jimmy's Tapas Bar</h3>
            <p className="text-amber-200">
              Spanische Genüsse – Authentisch & Gemütlich
            </p>
          </div>
          <div>
            <h4 className="font-bold mb-4">Standorte</h4>
            <div className="space-y-2 text-amber-200">
              <p>Neustadt in Holstein</p>
              <p>Großenbrode</p>
            </div>
          </div>
          <div>
            <h4 className="font-bold mb-4">Kontakt</h4>
            <div className="space-y-2 text-amber-200">
              <p>info@jimmys-tapasbar.de</p>
              <p>www.jimmys-tapasbar.de</p>
            </div>
          </div>
        </div>
        <div className="border-t border-amber-700 mt-8 pt-4 text-center text-amber-300">
          <p>&copy; 2024 Jimmy's Tapas Bar. Alle Rechte vorbehalten. | Impressum | Datenschutz</p>
        </div>
      </div>
    </footer>
  );
};

// Main App Component
function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/speisekarte" element={<Speisekarte />} />
          <Route path="/standorte" element={<Standorte />} />
          <Route path="/ueber-uns" element={<UeberUns />} />
          <Route path="/bewertungen" element={<Bewertungen />} />
          <Route path="/kontakt" element={<Kontakt />} />
        </Routes>
        <Footer />
      </BrowserRouter>
    </div>
  );
}

export default App;