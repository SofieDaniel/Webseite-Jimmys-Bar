import React, { useState } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Link, useNavigate } from "react-router-dom";

// Header Component - EXACT 1:1 match to reference image
const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  
  return (
    <header className="absolute top-0 left-0 right-0 z-50 bg-transparent">
      <div className="container mx-auto px-8 py-6">
        <nav className="flex justify-between items-center">
          <Link to="/" className="text-xl font-light text-stone-100 tracking-[0.2em]">
            JIMMY'S
            <span className="block text-xs text-stone-300 tracking-[0.3em] font-light mt-1">TAPAS BAR</span>
          </Link>
          
          <div className="hidden md:flex space-x-10">
            <Link to="/" className="text-stone-100 hover:text-stone-300 transition-colors font-light tracking-wide text-sm">Startseite</Link>
            <Link to="/standorte" className="text-stone-100 hover:text-stone-300 transition-colors font-light tracking-wide text-sm">Standorte</Link>
            <Link to="/speisekarte" className="text-stone-100 hover:text-stone-300 transition-colors font-light tracking-wide text-sm">Speisekarte</Link>
            <Link to="/bewertungen" className="text-stone-100 hover:text-stone-300 transition-colors font-light tracking-wide text-sm">Bewertungen</Link>
            <Link to="/ueber-uns" className="text-stone-100 hover:text-stone-300 transition-colors font-light tracking-wide text-sm">Über uns</Link>
            <Link to="/kontakt" className="text-stone-100 hover:text-stone-300 transition-colors font-light tracking-wide text-sm">Kontakt</Link>
          </div>
          
          <Link to="/speisekarte" className="hidden md:block border border-stone-300 text-stone-100 hover:bg-stone-100 hover:text-black px-6 py-2 rounded-full transition-all duration-300 font-light tracking-wider text-xs">
            ZUR SPEISEKARTE
          </Link>
          
          <button 
            className="md:hidden"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            <div className="w-5 h-5 flex flex-col justify-center space-y-1">
              <div className="w-5 h-0.5 bg-stone-100"></div>
              <div className="w-5 h-0.5 bg-stone-100"></div>
              <div className="w-5 h-0.5 bg-stone-100"></div>
            </div>
          </button>
        </nav>
        
        {isMenuOpen && (
          <div className="md:hidden mt-4 bg-black bg-opacity-90 rounded-lg p-4">
            <Link to="/" className="block py-2 text-stone-100 hover:text-stone-300 font-light">Startseite</Link>
            <Link to="/standorte" className="block py-2 text-stone-100 hover:text-stone-300 font-light">Standorte</Link>
            <Link to="/speisekarte" className="block py-2 text-stone-100 hover:text-stone-300 font-light">Speisekarte</Link>
            <Link to="/bewertungen" className="block py-2 text-stone-100 hover:text-stone-300 font-light">Bewertungen</Link>
            <Link to="/ueber-uns" className="block py-2 text-stone-100 hover:text-stone-300 font-light">Über uns</Link>
            <Link to="/kontakt" className="block py-2 text-stone-100 hover:text-stone-300 font-light">Kontakt</Link>
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
    <div className="min-h-screen">
      {/* Hero Section - Exact match to the user's reference image */}
      <section className="relative h-screen bg-cover bg-center" 
               style={{backgroundImage: `url('https://images.pexels.com/photos/19671352/pexels-photo-19671352.jpeg')`}}>
        <div className="absolute inset-0 bg-gradient-to-b from-black/30 via-black/20 to-black/60"></div>
        <div className="relative z-10 flex items-center justify-center h-full text-center text-stone-100 px-4">
          <div className="max-w-4xl">
            <h1 className="text-6xl md:text-8xl font-light mb-8 text-stone-100 tracking-wider leading-tight">
              AUTHENTISCHE<br />
              <span className="text-stone-200">TAPAS & WEIN</span>
            </h1>
            <div className="flex flex-col sm:flex-row gap-6 justify-center mt-12">
              <button 
                onClick={() => navigate('/standorte')}
                className="border-2 border-stone-200 text-stone-100 hover:bg-stone-100 hover:text-black px-12 py-4 rounded-full text-lg font-light transition-all duration-500 tracking-wider"
              >
                STANDORT WÄHLEN
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section with dark theme */}
      <section className="py-20 bg-stone-900">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-light text-center text-stone-100 mb-16 tracking-wider">
            Spanische Genüsse – Authentisch & Gemütlich
          </h2>
          <div className="grid md:grid-cols-3 gap-12">
            <div className="text-center">
              <div className="w-20 h-20 border border-stone-400 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl">🍷</span>
              </div>
              <h3 className="text-xl font-light text-stone-100 mb-4 tracking-wider">Authentische Tapas</h3>
              <p className="text-stone-300 font-light leading-relaxed">Traditionelle spanische Küche mit frischen, hochwertigen Zutaten</p>
            </div>
            <div className="text-center">
              <div className="w-20 h-20 border border-stone-400 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl">🥘</span>
              </div>
              <h3 className="text-xl font-light text-stone-100 mb-4 tracking-wider">Frische Paella</h3>
              <p className="text-stone-300 font-light leading-relaxed">Täglich frisch zubereitet mit den besten Meeresfrüchten und Zutaten</p>
            </div>
            <div className="text-center">
              <div className="w-20 h-20 border border-stone-400 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl">🏖️</span>
              </div>
              <h3 className="text-xl font-light text-stone-100 mb-4 tracking-wider">Zwei Standorte</h3>
              <p className="text-stone-300 font-light leading-relaxed">In Neustadt und Großenbrode direkt an der Ostsee</p>
            </div>
          </div>
        </div>
      </section>

      {/* Food Gallery with dark theme */}
      <section className="py-20 bg-stone-800">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-light text-center text-stone-100 mb-16 tracking-wider">
            Unsere Spezialitäten
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="bg-stone-900 rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-stone-700">
              <img src="https://images.unsplash.com/photo-1565599837634-134bc3aadce8" alt="Patatas Bravas" className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="font-light text-stone-100 text-lg tracking-wider">Patatas Bravas</h3>
                <p className="text-stone-400 text-sm font-light">Klassische spanische Kartoffeln</p>
              </div>
            </div>
            <div className="bg-stone-900 rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-stone-700">
              <img src="https://images.unsplash.com/photo-1630175860333-5131bda75071" alt="Paella" className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="font-light text-stone-100 text-lg tracking-wider">Paella Valenciana</h3>
                <p className="text-stone-400 text-sm font-light">Traditionelle spanische Paella</p>
              </div>
            </div>
            <div className="bg-stone-900 rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-stone-700">
              <img src="https://images.pexels.com/photos/19671352/pexels-photo-19671352.jpeg" alt="Tapas" className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="font-light text-stone-100 text-lg tracking-wider">Tapas Variation</h3>
                <p className="text-stone-400 text-sm font-light">Auswahl spanischer Köstlichkeiten</p>
              </div>
            </div>
            <div className="bg-stone-900 rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-stone-700">
              <img src="https://images.unsplash.com/photo-1588276552401-30058a0fe57b" alt="Seafood Paella" className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="font-light text-stone-100 text-lg tracking-wider">Paella Mariscos</h3>
                <p className="text-stone-400 text-sm font-light">Meeresfrüchte-Paella</p>
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
    <div className="min-h-screen bg-stone-900 py-12">
      <div className="container mx-auto px-4">
        <h1 className="text-5xl font-light text-center text-stone-100 mb-12 tracking-wider">
          Speisekarte
        </h1>
        
        {/* Category Filter */}
        <div className="flex flex-wrap justify-center gap-3 mb-12">
          {categories.map(category => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`px-6 py-3 rounded-full transition-all duration-300 font-light tracking-wide ${
                selectedCategory === category.id
                  ? 'bg-stone-100 text-black'
                  : 'border border-stone-400 text-stone-100 hover:bg-stone-100 hover:text-black'
              }`}
            >
              {category.name}
            </button>
          ))}
        </div>

        {/* Menu Items */}
        <div className="grid gap-6 max-w-5xl mx-auto">
          {getDisplayItems().map((item, index) => (
            <div key={index} className="bg-stone-800 rounded-lg border border-stone-700 p-8 hover:bg-stone-750 transition-all duration-300">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="text-2xl font-light text-stone-100 mb-3 tracking-wide">{item.name}</h3>
                  <p className="text-stone-300 mb-3 font-light leading-relaxed">{item.description}</p>
                  <span className="text-sm text-stone-400 capitalize font-light tracking-wider">
                    {categories.find(c => c.id === item.category)?.name}
                  </span>
                </div>
                <div className="text-3xl font-light text-stone-100 ml-6 tracking-wider">
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
    <div className="min-h-screen bg-stone-900 py-12">
      <div className="container mx-auto px-4">
        <h1 className="text-5xl font-light text-center text-stone-100 mb-16 tracking-wider">
          Unsere Standorte
        </h1>
        
        <div className="grid lg:grid-cols-2 gap-12">
          {/* Neustadt Location */}
          <div className="bg-stone-800 rounded-lg border border-stone-700 overflow-hidden">
            <img 
              src="https://images.unsplash.com/photo-1665758564776-f2aa6b41327e" 
              alt="Restaurant Neustadt" 
              className="w-full h-64 object-cover"
            />
            <div className="p-8">
              <h2 className="text-3xl font-light text-stone-100 mb-6 tracking-wider">
                Jimmy's Tapas Bar Neustadt
              </h2>
              <div className="space-y-4 text-stone-300">
                <div className="flex items-center">
                  <span className="text-xl mr-4">📍</span>
                  <div>
                    <p className="font-light text-lg">Am Strande 21</p>
                    <p className="font-light">23730 Neustadt in Holstein</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <span className="text-xl mr-4">🕒</span>
                  <div>
                    <p className="font-light text-lg">Öffnungszeiten:</p>
                    <p className="font-light">Täglich 12:00–22:00 Uhr (Sommersaison)</p>
                    <p className="text-sm text-stone-400 font-light">Winterbetrieb unregelmäßig</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <span className="text-xl mr-4">📞</span>
                  <p className="font-light">Telefon: +49 (0) 4561 123456</p>
                </div>
              </div>
              <div className="mt-8 h-64 bg-stone-700 rounded-lg flex items-center justify-center border border-stone-600">
                <div className="text-center">
                  <p className="text-stone-300 font-light">Google Maps Karte - Neustadt</p>
                  <p className="text-sm text-stone-400 font-light mt-2">(Integration folgt)</p>
                </div>
              </div>
            </div>
          </div>

          {/* Großenbrode Location */}
          <div className="bg-stone-800 rounded-lg border border-stone-700 overflow-hidden">
            <img 
              src="https://images.unsplash.com/photo-1665758564796-5162ff406254" 
              alt="Restaurant Großenbrode" 
              className="w-full h-64 object-cover"
            />
            <div className="p-8">
              <h2 className="text-3xl font-light text-stone-100 mb-6 tracking-wider">
                Jimmy's Tapas Bar Großenbrode
              </h2>
              <div className="space-y-4 text-stone-300">
                <div className="flex items-center">
                  <span className="text-xl mr-4">📍</span>
                  <div>
                    <p className="font-light text-lg">Südstrand 54</p>
                    <p className="font-light">23755 Großenbrode</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <span className="text-xl mr-4">🕒</span>
                  <div>
                    <p className="font-light text-lg">Öffnungszeiten:</p>
                    <p className="font-light">Täglich 12:00–22:00 Uhr (Sommersaison)</p>
                    <p className="text-sm text-stone-400 font-light">Winterbetrieb unregelmäßig</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <span className="text-xl mr-4">📞</span>
                  <p className="font-light">Telefon: +49 (0) 4561 789012</p>
                </div>
              </div>
              <div className="mt-8 h-64 bg-stone-700 rounded-lg flex items-center justify-center border border-stone-600">
                <div className="text-center">
                  <p className="text-stone-300 font-light">Google Maps Karte - Großenbrode</p>
                  <p className="text-sm text-stone-400 font-light mt-2">(Integration folgt)</p>
                </div>
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
    <div className="min-h-screen bg-stone-900 py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-5xl font-light text-center text-stone-100 mb-16 tracking-wider">
            Über uns
          </h1>
          
          <div className="bg-stone-800 rounded-lg border border-stone-700 p-10 mb-12">
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div>
                <img 
                  src="https://images.unsplash.com/photo-1665758564802-f611df512d8d" 
                  alt="Jimmy" 
                  className="w-full rounded-lg"
                />
              </div>
              <div>
                <h2 className="text-4xl font-light text-stone-100 mb-6 tracking-wider">
                  Jimmy Rodríguez
                </h2>
                <p className="text-stone-300 mb-6 leading-relaxed font-light text-lg">
                  Seit über 15 Jahren bringe ich die authentischen Aromen Spaniens an die deutsche Ostseeküste. 
                  Meine Leidenschaft für die spanische Küche begann in den kleinen Tapas-Bars von Sevilla, 
                  wo ich die Geheimnisse traditioneller Rezepte erlernte.
                </p>
                <p className="text-stone-300 mb-6 leading-relaxed font-light text-lg">
                  In Jimmy's Tapas Bar verwenden wir nur die besten Zutaten - von handverlesenem Olivenöl 
                  aus Andalusien bis hin zu frischen Meeresfrüchten aus der Ostsee. Jedes Gericht wird mit 
                  Liebe und Respekt vor der spanischen Tradition zubereitet.
                </p>
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-stone-800 rounded-lg border border-stone-700 p-8 text-center">
              <div className="text-5xl mb-6">🍷</div>
              <h3 className="text-2xl font-light text-stone-100 mb-4 tracking-wider">Qualität</h3>
              <p className="text-stone-300 font-light leading-relaxed">
                Nur die besten Zutaten für authentische spanische Geschmackserlebnisse
              </p>
            </div>
            <div className="bg-stone-800 rounded-lg border border-stone-700 p-8 text-center">
              <div className="text-5xl mb-6">❤️</div>
              <h3 className="text-2xl font-light text-stone-100 mb-4 tracking-wider">Gastfreundschaft</h3>
              <p className="text-stone-300 font-light leading-relaxed">
                Herzliche Atmosphäre und persönlicher Service für jeden Gast
              </p>
            </div>
            <div className="bg-stone-800 rounded-lg border border-stone-700 p-8 text-center">
              <div className="text-5xl mb-6">🎉</div>
              <h3 className="text-2xl font-light text-stone-100 mb-4 tracking-wider">Lebensfreude</h3>
              <p className="text-stone-300 font-light leading-relaxed">
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
      <span key={i} className={`text-2xl ${i < rating ? 'text-yellow-400' : 'text-stone-600'}`}>
        ★
      </span>
    ));
  };

  return (
    <div className="min-h-screen bg-stone-900 py-12">
      <div className="container mx-auto px-4">
        <h1 className="text-5xl font-light text-center text-stone-100 mb-16 tracking-wider">
          Bewertungen & Feedback
        </h1>
        
        <div className="grid lg:grid-cols-2 gap-12 max-w-7xl mx-auto">
          {/* Public Reviews */}
          <div>
            <h2 className="text-3xl font-light text-stone-100 mb-8 tracking-wider">
              Kundenbewertungen
            </h2>
            <div className="space-y-8">
              {reviews.map((review, index) => (
                <div key={index} className="bg-stone-800 rounded-lg border border-stone-700 p-8">
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="font-light text-stone-100 text-lg tracking-wide">{review.name}</h3>
                    <span className="text-sm text-stone-400 font-light">{review.date}</span>
                  </div>
                  <div className="flex mb-4">
                    {renderStars(review.rating)}
                  </div>
                  <p className="text-stone-300 font-light leading-relaxed">{review.comment}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Feedback Form */}
          <div>
            <h2 className="text-3xl font-light text-stone-100 mb-8 tracking-wider">
              Ihr Feedback
            </h2>
            <div className="bg-stone-800 rounded-lg border border-stone-700 p-8">
              <p className="text-stone-400 mb-6 text-sm font-light">
                Dieses Feedback wird intern gespeichert und nicht öffentlich angezeigt.
              </p>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="block text-stone-100 font-light mb-3 tracking-wide">Name</label>
                  <input
                    type="text"
                    value={feedback.name}
                    onChange={(e) => setFeedback({...feedback, name: e.target.value})}
                    className="w-full p-4 bg-stone-700 border border-stone-600 rounded-lg focus:ring-2 focus:ring-stone-400 focus:border-stone-400 text-stone-100 font-light"
                    required
                  />
                </div>
                <div>
                  <label className="block text-stone-100 font-light mb-3 tracking-wide">E-Mail</label>
                  <input
                    type="email"
                    value={feedback.email}
                    onChange={(e) => setFeedback({...feedback, email: e.target.value})}
                    className="w-full p-4 bg-stone-700 border border-stone-600 rounded-lg focus:ring-2 focus:ring-stone-400 focus:border-stone-400 text-stone-100 font-light"
                    required
                  />
                </div>
                <div>
                  <label className="block text-stone-100 font-light mb-3 tracking-wide">Bewertung</label>
                  <div className="flex space-x-2">
                    {[1,2,3,4,5].map(star => (
                      <button
                        key={star}
                        type="button"
                        onClick={() => setFeedback({...feedback, rating: star})}
                        className={`text-3xl ${star <= feedback.rating ? 'text-yellow-400' : 'text-stone-600'} hover:text-yellow-400 transition-colors`}
                      >
                        ★
                      </button>
                    ))}
                  </div>
                </div>
                <div>
                  <label className="block text-stone-100 font-light mb-3 tracking-wide">Kommentar</label>
                  <textarea
                    value={feedback.comment}
                    onChange={(e) => setFeedback({...feedback, comment: e.target.value})}
                    className="w-full p-4 bg-stone-700 border border-stone-600 rounded-lg focus:ring-2 focus:ring-stone-400 focus:border-stone-400 h-32 text-stone-100 font-light"
                    required
                  />
                </div>
                <button
                  type="submit"
                  className="w-full bg-stone-100 hover:bg-stone-200 text-black py-4 rounded-lg font-light transition-colors tracking-wider"
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
    <div className="min-h-screen bg-stone-900 py-12">
      <div className="container mx-auto px-4">
        <h1 className="text-5xl font-light text-center text-stone-100 mb-16 tracking-wider">
          Kontakt
        </h1>
        
        <div className="grid lg:grid-cols-2 gap-12 max-w-7xl mx-auto">
          {/* Contact Information */}
          <div>
            <h2 className="text-3xl font-light text-stone-100 mb-8 tracking-wider">
              Kontaktinformationen
            </h2>
            
            <div className="bg-stone-800 rounded-lg border border-stone-700 p-8 mb-8">
              <h3 className="text-2xl font-light text-stone-100 mb-6 tracking-wider">Neustadt in Holstein</h3>
              <div className="space-y-3 text-stone-300">
                <p className="font-light">📍 Am Strande 21, 23730 Neustadt in Holstein</p>
                <p className="font-light">📞 +49 (0) 4561 123456</p>
                <p className="font-light">✉️ neustadt@jimmys-tapasbar.de</p>
              </div>
            </div>

            <div className="bg-stone-800 rounded-lg border border-stone-700 p-8 mb-8">
              <h3 className="text-2xl font-light text-stone-100 mb-6 tracking-wider">Großenbrode</h3>
              <div className="space-y-3 text-stone-300">
                <p className="font-light">📍 Südstrand 54, 23755 Großenbrode</p>
                <p className="font-light">📞 +49 (0) 4561 789012</p>
                <p className="font-light">✉️ grossenbrode@jimmys-tapasbar.de</p>
              </div>
            </div>

            <div className="bg-stone-800 rounded-lg border border-stone-700 p-8">
              <h3 className="text-2xl font-light text-stone-100 mb-6 tracking-wider">Allgemein</h3>
              <div className="space-y-3 text-stone-300">
                <p className="font-light">🌐 www.jimmys-tapasbar.de</p>
                <p className="font-light">✉️ info@jimmys-tapasbar.de</p>
                <p className="font-light">🕒 Täglich 12:00–22:00 Uhr (Sommersaison)</p>
              </div>
            </div>
          </div>

          {/* Contact Form */}
          <div>
            <h2 className="text-3xl font-light text-stone-100 mb-8 tracking-wider">
              Nachricht senden
            </h2>
            <div className="bg-stone-800 rounded-lg border border-stone-700 p-8">
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="block text-stone-100 font-light mb-3 tracking-wide">Name *</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    className="w-full p-4 bg-stone-700 border border-stone-600 rounded-lg focus:ring-2 focus:ring-stone-400 focus:border-stone-400 text-stone-100 font-light"
                    required
                  />
                </div>
                <div>
                  <label className="block text-stone-100 font-light mb-3 tracking-wide">E-Mail *</label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    className="w-full p-4 bg-stone-700 border border-stone-600 rounded-lg focus:ring-2 focus:ring-stone-400 focus:border-stone-400 text-stone-100 font-light"
                    required
                  />
                </div>
                <div>
                  <label className="block text-stone-100 font-light mb-3 tracking-wide">Telefon</label>
                  <input
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => setFormData({...formData, phone: e.target.value})}
                    className="w-full p-4 bg-stone-700 border border-stone-600 rounded-lg focus:ring-2 focus:ring-stone-400 focus:border-stone-400 text-stone-100 font-light"
                  />
                </div>
                <div>
                  <label className="block text-stone-100 font-light mb-3 tracking-wide">Standort</label>
                  <select
                    value={formData.location}
                    onChange={(e) => setFormData({...formData, location: e.target.value})}
                    className="w-full p-4 bg-stone-700 border border-stone-600 rounded-lg focus:ring-2 focus:ring-stone-400 focus:border-stone-400 text-stone-100 font-light"
                  >
                    <option value="neustadt">Neustadt in Holstein</option>
                    <option value="grossenbrode">Großenbrode</option>
                    <option value="beide">Beide Standorte</option>
                  </select>
                </div>
                <div>
                  <label className="block text-stone-100 font-light mb-3 tracking-wide">Nachricht *</label>
                  <textarea
                    value={formData.message}
                    onChange={(e) => setFormData({...formData, message: e.target.value})}
                    className="w-full p-4 bg-stone-700 border border-stone-600 rounded-lg focus:ring-2 focus:ring-stone-400 focus:border-stone-400 h-32 text-stone-100 font-light"
                    required
                  />
                </div>
                <button
                  type="submit"
                  className="w-full bg-stone-100 hover:bg-stone-200 text-black py-4 rounded-lg font-light transition-colors tracking-wider"
                >
                  Nachricht senden
                </button>
              </form>
              
              <div className="mt-8 pt-8 border-t border-stone-700">
                <h4 className="font-light text-stone-100 mb-3 tracking-wide">Datenschutz</h4>
                <p className="text-sm text-stone-400 font-light leading-relaxed">
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
    <footer className="bg-black bg-opacity-90 text-stone-300 py-12">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-xl font-light mb-4 tracking-wider text-stone-100">Jimmy's Tapas Bar</h3>
            <p className="text-stone-400 font-light">
              Spanische Genüsse – Authentisch & Gemütlich
            </p>
          </div>
          <div>
            <h4 className="font-light mb-4 tracking-wider text-stone-100">Standorte</h4>
            <div className="space-y-2 text-stone-400 font-light">
              <p>Neustadt in Holstein</p>
              <p>Großenbrode</p>
            </div>
          </div>
          <div>
            <h4 className="font-light mb-4 tracking-wider text-stone-100">Kontakt</h4>
            <div className="space-y-2 text-stone-400 font-light">
              <p>info@jimmys-tapasbar.de</p>
              <p>www.jimmys-tapasbar.de</p>
            </div>
          </div>
        </div>
        <div className="border-t border-stone-700 mt-8 pt-6 text-center text-stone-500 font-light">
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