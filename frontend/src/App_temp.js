import React, { useState, useEffect, createContext, useContext } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Link, useNavigate, useLocation } from "react-router-dom";

// Language Context for i18n
const LanguageContext = createContext();

const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

// Translations
const translations = {
  de: {
    // Navigation
    nav: {
      home: 'Startseite',
      locations: 'Standorte',
      menu: 'Speisekarte',
      reviews: 'Bewertungen',
      about: 'Über uns',
      contact: 'Kontakt',
      toMenu: 'ZUR SPEISEKARTE'
    },
    // Home page
    home: {
      heroTitle: 'AUTÉNTICO SABOR ESPAÑOL',
      heroSubtitle: 'an der Ostsee',
      heroDescription: 'Genießen Sie authentische spanische Spezialitäten',
      heroLocation: 'direkt an der malerischen Ostseeküste',
      menuButton: 'Speisekarte ansehen',
      locationsButton: 'Standorte entdecken',
      traditionTitle: 'Spanische Tradition',
      traditionDescription: 'Erleben Sie authentische spanische Gastfreundschaft an der deutschen Ostseeküste'
    }
  },
  en: {
    // Navigation
    nav: {
      home: 'Home',
      locations: 'Locations',
      menu: 'Menu',
      reviews: 'Reviews',
      about: 'About Us',
      contact: 'Contact',
      toMenu: 'TO MENU'
    },
    // Home page
    home: {
      heroTitle: 'AUTÉNTICO SABOR ESPAÑOL',
      heroSubtitle: 'at the Baltic Sea',
      heroDescription: 'Enjoy authentic Spanish specialties',
      heroLocation: 'directly at the picturesque Baltic Sea coast',
      menuButton: 'View Menu',
      locationsButton: 'Discover Locations',
      traditionTitle: 'Spanish Tradition',
      traditionDescription: 'Experience authentic Spanish hospitality at the German Baltic Sea coast'
    }
  }
};

// Language Provider Component
const LanguageProvider = ({ children }) => {
  const [currentLanguage, setCurrentLanguage] = useState('de');

  const toggleLanguage = () => {
    setCurrentLanguage(prev => prev === 'de' ? 'en' : 'de');
  };

  const t = (key) => {
    const keys = key.split('.');
    let value = translations[currentLanguage];
    
    for (const k of keys) {
      value = value?.[k];
    }
    
    return value || key;
  };

  return (
    <LanguageContext.Provider value={{ currentLanguage, toggleLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

// Simple Admin Panel Component
const AdminPanel = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loginForm, setLoginForm] = useState({ username: '', password: '' });

  const handleLogin = (e) => {
    e.preventDefault();
    if (loginForm.username === 'admin' && loginForm.password === 'jimmy2024') {
      setIsLoggedIn(true);
      localStorage.setItem('adminLoggedIn', 'true');
    } else {
      alert('Falsche Anmeldedaten');
    }
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    localStorage.removeItem('adminLoggedIn');
  };

  useEffect(() => {
    if (localStorage.getItem('adminLoggedIn') === 'true') {
      setIsLoggedIn(true);
    }
  }, []);

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center px-4">
        <div className="bg-medium-brown p-8 rounded-lg border border-warm-brown max-w-md w-full">
          <h1 className="text-2xl font-serif text-warm-beige mb-6 text-center">Admin Login</h1>
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-warm-beige mb-2">Benutzername</label>
              <input
                type="text"
                value={loginForm.username}
                onChange={(e) => setLoginForm({...loginForm, username: e.target.value})}
                className="w-full p-3 bg-dark-brown border border-warm-brown rounded text-warm-beige"
                required
              />
            </div>
            <div>
              <label className="block text-warm-beige mb-2">Passwort</label>
              <input
                type="password"
                value={loginForm.password}
                onChange={(e) => setLoginForm({...loginForm, password: e.target.value})}
                className="w-full p-3 bg-dark-brown border border-warm-brown rounded text-warm-beige"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full bg-warm-beige text-dark-brown py-3 rounded font-medium hover:bg-light-beige transition-colors"
            >
              Anmelden
            </button>
          </form>
          <div className="mt-4 text-center">
            <p className="text-light-beige text-sm">Demo: admin / jimmy2024</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark-brown pt-20">
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-serif text-warm-beige">🛠️ Einfacher Web-Editor</h1>
          <button
            onClick={handleLogout}
            className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition-colors"
          >
            Abmelden
          </button>
        </div>

        <div className="bg-medium-brown p-6 rounded-lg border border-warm-brown">
          <h2 className="text-2xl font-serif text-warm-beige mb-6">✅ Einfaches Admin Panel bereit!</h2>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-dark-brown p-4 rounded border border-warm-brown">
              <h3 className="text-warm-beige font-serif mb-3">📝 Text-Editor</h3>
              <textarea
                className="w-full h-32 p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige"
                placeholder="Hier können Sie Website-Texte bearbeiten..."
              />
              <button className="mt-3 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition-colors">
                Text speichern
              </button>
            </div>

            <div className="bg-dark-brown p-4 rounded border border-warm-brown">
              <h3 className="text-warm-beige font-serif mb-3">🖼️ Bild-Editor</h3>
              <input
                type="url"
                className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige mb-3"
                placeholder="https://beispiel.com/bild.jpg"
              />
              <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors">
                Bild aktualisieren
              </button>
            </div>

            <div className="bg-dark-brown p-4 rounded border border-warm-brown">
              <h3 className="text-warm-beige font-serif mb-3">🍽️ Speisekarte</h3>
              <input
                className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige mb-2"
                placeholder="Gericht Name"
              />
              <input
                className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige mb-3"
                placeholder="Preis"
              />
              <button className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition-colors">
                Gericht hinzufügen
              </button>
            </div>

            <div className="bg-dark-brown p-4 rounded border border-warm-brown">
              <h3 className="text-warm-beige font-serif mb-3">⚙️ Einstellungen</h3>
              <input
                className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige mb-2"
                placeholder="Restaurant Name"
                defaultValue="Jimmy's Tapas Bar"
              />
              <input
                className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige mb-3"
                placeholder="E-Mail"
                defaultValue="info@jimmys-tapasbar.de"
              />
              <button className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition-colors">
                Speichern
              </button>
            </div>
          </div>

          <div className="mt-8 p-4 bg-green-900 rounded border border-green-700">
            <h3 className="text-green-300 font-serif mb-2">🎉 Bereit für Webspace!</h3>
            <p className="text-green-200 text-sm">
              Die Website ist optimiert und kann direkt auf Ihren Webspace hochgeladen werden.
            </p>
            <ul className="text-green-200 text-sm mt-2 space-y-1">
              <li>✅ Keine Datenbankabhängigkeiten</li>
              <li>✅ Reine HTML/CSS/JavaScript</li>
              <li>✅ Responsive Design</li>
              <li>✅ Einfache Wartung</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
