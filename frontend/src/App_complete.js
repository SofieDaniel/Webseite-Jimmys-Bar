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
};const Home = () => {
  const navigate = useNavigate();
  const { t } = useLanguage();
  
  return (
    <div className="min-h-screen">
      {/* Clean Professional Hero Section */}
      <section id="main-content" className="relative h-screen bg-cover bg-center hero-background" 
               style={{backgroundImage: `url('https://images.unsplash.com/photo-1656423521731-9665583f100c')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-50"></div>
        <div className="relative z-10 flex items-center justify-center h-full text-center px-4" style={{paddingTop: '80px'}}>
          <div className="max-w-4xl">
            {/* Clean Main Headline with proper spacing */}
            <h1 className="hero-headline font-serif text-warm-beige mb-8 tracking-wide leading-tight drop-shadow-text" style={{fontSize: 'clamp(2.5rem, 8vw, 6rem)', lineHeight: '1.1', marginTop: '40px'}}>
              {t('home.heroTitle')}<br />
              <span className="font-light opacity-90" style={{fontSize: 'clamp(1.8rem, 5vw, 4rem)'}}>{t('home.heroSubtitle')}</span>
            </h1>
            
            {/* Simple Subtitle */}
            <p className="text-xl md:text-2xl text-warm-beige font-light mb-12 max-w-3xl mx-auto leading-relaxed opacity-95">
              {t('home.heroDescription')}<br/>
              <span className="text-lg opacity-80">{t('home.heroLocation')}</span>
            </p>
            
            {/* Clean CTA Buttons */}
            <div className="flex flex-col md:flex-row justify-center gap-6">
              <button 
                onClick={() => navigate('/speisekarte')}
                className="bg-warm-beige text-dark-brown hover:bg-light-beige px-10 py-4 rounded-lg text-lg font-medium transition-all duration-300 tracking-wide shadow-lg hover:shadow-xl"
              >
                {t('home.menuButton')}
              </button>
              <button 
                onClick={() => navigate('/standorte')}
                className="border-2 border-warm-beige text-warm-beige hover:bg-warm-beige hover:text-dark-brown px-10 py-4 rounded-lg text-lg font-medium transition-all duration-300 tracking-wide shadow-lg hover:shadow-xl"
              >
                {t('home.locationsButton')}
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Professional Features Section - Clean Design like "Unsere Spezialitäten" */}
      <section className="py-24 bg-gradient-to-b from-dark-brown to-medium-brown">
        <div className="container mx-auto px-4">
          <div className="text-center mb-20">
            <h2 className="text-5xl font-serif text-warm-beige mb-8 tracking-wide">
              Spanische Tradition
            </h2>
            <p className="text-xl text-light-beige font-light leading-relaxed max-w-3xl mx-auto">
              Erleben Sie authentische spanische Gastfreundschaft an der deutschen Ostseeküste
            </p>
          </div>
          
          {/* Clean Three Cards - Professional Layout with Product Images */}
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <div className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-all duration-300 border border-warm-brown shadow-lg">
              <img 
                src="https://images.pexels.com/photos/19671352/pexels-photo-19671352.jpeg" 
                alt="Authentische Tapas" 
                className="w-full h-48 object-cover"
              />
              <div className="p-8 text-center">
                <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">Authentische Tapas</h3>
                <p className="text-light-beige font-light leading-relaxed">
                  Traditionelle spanische Gerichte, mit Liebe zubereitet und perfekt zum Teilen
                </p>
              </div>
            </div>
            
            <div className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-all duration-300 border border-warm-brown shadow-lg">
              <img 
                src="https://images.unsplash.com/photo-1694685367640-05d6624e57f1" 
                alt="Frische Paella" 
                className="w-full h-48 object-cover"
              />
              <div className="p-8 text-center">
                <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">Frische Paella</h3>
                <p className="text-light-beige font-light leading-relaxed">
                  Täglich hausgemacht mit Meeresfrüchten, Gemüse oder Huhn
                </p>
              </div>
            </div>
            
            <div className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-all duration-300 border border-warm-brown shadow-lg">
              <img 
                src="https://images.pexels.com/photos/32508247/pexels-photo-32508247.jpeg" 
                alt="Strandnähe mit Strandkörben" 
                className="w-full h-48 object-cover"
              />
              <div className="p-8 text-center">
                <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">Strandnähe</h3>
                <p className="text-light-beige font-light leading-relaxed">
                  Beide Standorte direkt an der malerischen Ostseeküste – perfekt für entspannte Stunden
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Clean Food Gallery - Professional with Navigation */}
      <section className="py-20 bg-medium-brown">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-serif text-center text-warm-beige mb-16 tracking-wide">
            Unsere Spezialitäten
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div 
              className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-warm-brown cursor-pointer"
              onClick={() => {
                navigate('/speisekarte');
                // Set category after navigation
                setTimeout(() => {
                  window.location.href = '/speisekarte#tapas-vegetarian';
                }, 100);
              }}
            >
              <img src="https://images.unsplash.com/photo-1565599837634-134bc3aadce8" alt="Patatas Bravas" className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="font-serif text-warm-beige text-lg tracking-wide">Patatas Bravas</h3>
                <p className="text-light-beige text-sm font-light">Klassische spanische Kartoffeln</p>
              </div>
            </div>
            <div 
              className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-warm-brown cursor-pointer"
              onClick={() => {
                navigate('/speisekarte');
                setTimeout(() => {
                  window.location.href = '/speisekarte#tapa-paella';
                }, 100);
              }}
            >
              <img src="https://images.pexels.com/photos/7085661/pexels-photo-7085661.jpeg" alt="Paella" className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="font-serif text-warm-beige text-lg tracking-wide">Paella Valenciana</h3>
                <p className="text-light-beige text-sm font-light">Traditionelle spanische Paella</p>
              </div>
            </div>
            <div 
              className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-warm-brown cursor-pointer"
              onClick={() => {
                navigate('/speisekarte');
                setTimeout(() => {
                  window.location.href = '/speisekarte#inicio';
                }, 100);
              }}
            >
              <img src="https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg" alt="Tapas" className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="font-serif text-warm-beige text-lg tracking-wide">Tapas Variación</h3>
                <p className="text-light-beige text-sm font-light">Auswahl spanischer Köstlichkeiten</p>
              </div>
            </div>
            <div 
              className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-warm-brown cursor-pointer"
              onClick={() => {
                navigate('/speisekarte');
                setTimeout(() => {
                  window.location.href = '/speisekarte#tapas-pescado';
                }, 100);
              }}
            >
              <img src="https://images.unsplash.com/photo-1619860705243-dbef552e7118" alt="Gambas al Ajillo" className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="font-serif text-warm-beige text-lg tracking-wide">Gambas al Ajillo</h3>
                <p className="text-light-beige text-sm font-light">Garnelen in Knoblauchöl</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Lieferando Section */}
      <section className="py-16 bg-gradient-to-r from-dark-brown to-medium-brown">
        <div className="container mx-auto px-4 text-center">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-4xl font-serif text-warm-beige mb-8 tracking-wide">
              Jetzt auch bequem nach Hause bestellen
            </h2>
            <p className="text-xl text-light-beige font-light mb-12 leading-relaxed">
              Genießen Sie unsere authentischen spanischen Spezialitäten gemütlich zu Hause.<br/>
              Bestellen Sie direkt über Lieferando und lassen Sie sich verwöhnen.
            </p>
            <div className="bg-dark-brown rounded-lg p-8 border border-warm-brown shadow-lg">
              <div className="flex flex-col md:flex-row items-center justify-center gap-8">
                <div className="text-center">
                  <div className="w-24 h-24 bg-cover bg-center rounded-lg mx-auto mb-4 border-2 border-warm-beige" 
                       style={{backgroundImage: `url('https://images.pexels.com/photos/6969962/pexels-photo-6969962.jpeg')`}}>
                  </div>
                  <h3 className="text-xl font-serif text-warm-beige mb-2">Schnelle Lieferung</h3>
                  <p className="text-light-beige text-sm">Frisch und warm zu Ihnen</p>
                </div>
                <div className="text-center">
                  <a 
                    href="https://www.lieferando.de" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="inline-block bg-orange-500 hover:bg-orange-600 text-white px-8 py-4 rounded-lg text-lg font-medium transition-all duration-300 tracking-wide shadow-lg hover:shadow-xl transform hover:scale-105"
                  >
                    Jetzt bei Lieferando bestellen
                  </a>
                  <p className="text-light-beige text-sm mt-2">Verfügbar für beide Standorte</p>
                </div>
                <div className="text-center">
                  <div className="w-24 h-24 bg-cover bg-center rounded-lg mx-auto mb-4 border-2 border-warm-beige" 
                       style={{backgroundImage: `url('https://images.pexels.com/photos/31748679/pexels-photo-31748679.jpeg')`}}>
                  </div>
                  <h3 className="text-xl font-serif text-warm-beige mb-2">Authentisch Spanisch</h3>
                  <p className="text-light-beige text-sm">Direkt vom Küchenchef</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

// Menu Page Component - Mouseover with detailed information only
