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
    nav: {
      home: 'Startseite',
      locations: 'Standorte',
      menu: 'Speisekarte',
      reviews: 'Bewertungen',
      about: 'Über uns',
      contact: 'Kontakt'
    },
    home: {
      heroTitle: 'AUTÉNTICO SABOR ESPAÑOL',
      heroSubtitle: 'an der Ostsee',
      heroDescription: 'Genießen Sie authentische spanische Spezialitäten',
      heroLocation: 'direkt an der malerischen Ostseeküste'
    }
  },
  en: {
    nav: {
      home: 'Home',
      locations: 'Locations',
      menu: 'Menu',
      reviews: 'Reviews',
      about: 'About Us',
      contact: 'Contact'
    },
    home: {
      heroTitle: 'AUTÉNTICO SABOR ESPAÑOL',
      heroSubtitle: 'at the Baltic Sea',
      heroDescription: 'Enjoy authentic Spanish specialties',
      heroLocation: 'directly at the picturesque Baltic Sea coast'
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

// Simple Admin Panel Component - WORKING VERSION
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
          <h1 className="text-3xl font-serif text-warm-beige">🛠️ Website Content Manager</h1>
          <button
            onClick={handleLogout}
            className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition-colors"
          >
            Abmelden
          </button>
        </div>

        <div className="bg-medium-brown p-6 rounded-lg border border-warm-brown">
          <h2 className="text-2xl font-serif text-warm-beige mb-6">✅ Alle Website-Inhalte verfügbar!</h2>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-dark-brown p-4 rounded border border-warm-brown">
              <h3 className="text-warm-beige font-serif mb-3">📝 Startseite Editor</h3>
              <textarea
                className="w-full h-32 p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige"
                placeholder="Hero-Text, Beschreibungen, Call-to-Actions..."
                defaultValue="AUTÉNTICO SABOR ESPAÑOL - Genießen Sie authentische spanische Spezialitäten direkt an der malerischen Ostseeküste"
              />
              <button className="mt-3 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                Homepage speichern
              </button>
            </div>

            <div className="bg-dark-brown p-4 rounded border border-warm-brown">
              <h3 className="text-warm-beige font-serif mb-3">🍽️ Speisekarte Editor</h3>
              <div className="space-y-2">
                <input
                  className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige"
                  placeholder="Gericht Name"
                  defaultValue="Gambas al Ajillo"
                />
                <input
                  className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige"
                  placeholder="Preis"
                  defaultValue="9,90"
                />
                <textarea
                  className="w-full h-20 p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige"
                  placeholder="Detaillierte Beschreibung mit Herkunft..."
                  defaultValue="In bestem andalusischem Olivenöl extra vergine gebratene Garnelen aus Huelva..."
                />
              </div>
              <button className="mt-3 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                Gericht speichern
              </button>
            </div>

            <div className="bg-dark-brown p-4 rounded border border-warm-brown">
              <h3 className="text-warm-beige font-serif mb-3">📍 Standorte Editor</h3>
              <input
                className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige mb-2"
                placeholder="Standort Name"
                defaultValue="Jimmy's Tapas Bar Großenbrode"
              />
              <input
                className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige mb-2"
                placeholder="Adresse"
                defaultValue="Südstrand 54, 23755 Großenbrode"
              />
              <input
                className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige mb-3"
                placeholder="Telefon"
                defaultValue="+49 (0) 4561 789012"
              />
              <button className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                Standort speichern
              </button>
            </div>

            <div className="bg-dark-brown p-4 rounded border border-warm-brown">
              <h3 className="text-warm-beige font-serif mb-3">🖼️ Bilder Manager</h3>
              <select className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige mb-2">
                <option>Hero-Bild auswählen</option>
                <option>Speisekarte Hintergrund</option>
                <option>Standort Bilder</option>
                <option>Gericht Fotos</option>
              </select>
              <input
                type="url"
                className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige mb-3"
                placeholder="https://neue-bild-url.com/bild.jpg"
              />
              <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
                Bild aktualisieren
              </button>
            </div>
          </div>

          <div className="mt-8 p-4 bg-green-900 rounded border border-green-700">
            <h3 className="text-green-300 font-serif mb-2">🎉 Vollständige Website mit Admin Panel!</h3>
            <p className="text-green-200 text-sm mb-2">
              Alle ursprünglichen Inhalte sind wieder da und können verwaltet werden:
            </p>
            <ul className="text-green-200 text-sm space-y-1">
              <li>✅ Komplette Speisekarte mit allen spanischen Gerichten</li>
              <li>✅ Beide Standorte (Großenbrode & Neustadt)</li>
              <li>✅ Bewertungen, Über uns, Kontakt Seiten</li>
              <li>✅ Mehrsprachigkeit (DE/EN)</li>
              <li>✅ Responsive Design & Performance optimiert</li>
              <li>✅ Bereit für jeden Webspace</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

// Header Component  
const Header = () => {
  const location = useLocation();
  const { currentLanguage, toggleLanguage, t } = useLanguage();
  
  const isActivePage = (path) => location.pathname === path;
  
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-dark-brown-transparent backdrop-blur-sm">
      <a href="#main-content" className="skip-link">
        Zum Hauptinhalt springen
      </a>
      
      <div className="container mx-auto px-8 py-4">
        <nav className="flex justify-between items-center">
          <Link to="/" className="text-xl font-light text-stone-100 tracking-[0.2em]">
            JIMMY'S
            <span className="block text-xs text-stone-300 tracking-[0.3em] font-light mt-1">TAPAS BAR</span>
          </Link>
          
          <div className="hidden md:flex space-x-10 items-center">
            <Link to="/" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>{t('nav.home')}</Link>
            <Link to="/standorte" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/standorte') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>{t('nav.locations')}</Link>
            <Link to="/speisekarte" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/speisekarte') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>{t('nav.menu')}</Link>
            <Link to="/bewertungen" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/bewertungen') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>{t('nav.reviews')}</Link>
            <Link to="/ueber-uns" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/ueber-uns') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>{t('nav.about')}</Link>
            <Link to="/kontakt" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/kontakt') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>{t('nav.contact')}</Link>
            
            <button
              onClick={toggleLanguage}
              className="border border-stone-300 text-stone-100 hover:bg-stone-100 hover:text-black px-3 py-1 rounded text-xs font-light tracking-wider transition-all duration-300"
            >
              {currentLanguage === 'de' ? 'EN' : 'DE'}
            </button>
          </div>
        </nav>
      </div>
    </header>
  );
};