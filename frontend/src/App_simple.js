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
          <h1 className="text-3xl font-serif text-warm-beige">🛠️ Einfacher Web-Editor - Webspace Ready</h1>
          <button
            onClick={handleLogout}
            className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition-colors"
          >
            Abmelden
          </button>
        </div>

        <div className="bg-medium-brown p-6 rounded-lg border border-warm-brown">
          <h2 className="text-2xl font-serif text-warm-beige mb-6">✅ Admin Panel funktioniert!</h2>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-dark-brown p-4 rounded border border-warm-brown">
              <h3 className="text-warm-beige font-serif mb-3">📝 Text-Editor</h3>
              <textarea
                className="w-full h-32 p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige"
                placeholder="Website-Texte hier bearbeiten..."
              />
              <button className="mt-3 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                Speichern
              </button>
            </div>

            <div className="bg-dark-brown p-4 rounded border border-warm-brown">
              <h3 className="text-warm-beige font-serif mb-3">🖼️ Bild-URLs</h3>
              <input
                type="url"
                className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige mb-3"
                placeholder="https://beispiel.com/bild.jpg"
              />
              <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
                Aktualisieren
              </button>
            </div>

            <div className="bg-dark-brown p-4 rounded border border-warm-brown">
              <h3 className="text-warm-beige font-serif mb-3">🍽️ Speisekarte</h3>
              <input
                className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige mb-2"
                placeholder="Gericht"
              />
              <input
                className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige mb-3"
                placeholder="Preis"
              />
              <button className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                Hinzufügen
              </button>
            </div>

            <div className="bg-dark-brown p-4 rounded border border-warm-brown">
              <h3 className="text-warm-beige font-serif mb-3">⚙️ Einstellungen</h3>
              <input
                className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige mb-2"
                defaultValue="Jimmy's Tapas Bar"
              />
              <input
                className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige mb-3"
                defaultValue="info@jimmys-tapasbar.de"
              />
              <button className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                Speichern
              </button>
            </div>
          </div>

          <div className="mt-8 p-4 bg-green-900 rounded border border-green-700">
            <h3 className="text-green-300 font-serif mb-2">🎉 Bereit für jeden Webspace!</h3>
            <p className="text-green-200 text-sm">
              Diese Website kann direkt auf Ihren Webspace hochgeladen werden - ohne Datenbankprobleme!
            </p>
            <ul className="text-green-200 text-sm mt-2 space-y-1">
              <li>✅ Reine HTML/CSS/JavaScript</li>
              <li>✅ Keine Serverabhängigkeiten</li>
              <li>✅ Funktioniert auf jedem Hosting</li>
              <li>✅ Einfache Wartung</li>
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

// Simple Home Component for demo
const Home = () => {
  const navigate = useNavigate();
  const { t } = useLanguage();
  
  return (
    <div className="min-h-screen">
      <section id="main-content" className="relative h-screen bg-cover bg-center hero-background" 
               style={{backgroundImage: `url('https://images.unsplash.com/photo-1656423521731-9665583f100c')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-50"></div>
        <div className="relative z-10 flex items-center justify-center h-full text-center px-4" style={{paddingTop: '80px'}}>
          <div className="max-w-4xl">
            <h1 className="hero-headline font-serif text-warm-beige mb-8 tracking-wide leading-tight drop-shadow-text" style={{fontSize: 'clamp(2.5rem, 8vw, 6rem)', lineHeight: '1.1', marginTop: '40px'}}>
              {t('home.heroTitle')}<br />
              <span className="font-light opacity-90" style={{fontSize: 'clamp(1.8rem, 5vw, 4rem)'}}>{t('home.heroSubtitle')}</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-warm-beige font-light mb-12 max-w-3xl mx-auto leading-relaxed opacity-95">
              {t('home.heroDescription')}<br/>
              <span className="text-lg opacity-80">{t('home.heroLocation')}</span>
            </p>
            
            <div className="flex flex-col md:flex-row justify-center gap-6">
              <button 
                onClick={() => navigate('/speisekarte')}
                className="bg-warm-beige text-dark-brown hover:bg-light-beige px-10 py-4 rounded-lg text-lg font-medium transition-all duration-300 tracking-wide shadow-lg hover:shadow-xl"
              >
                Speisekarte ansehen
              </button>
              <button 
                onClick={() => navigate('/admin')}
                className="border-2 border-warm-beige text-warm-beige hover:bg-warm-beige hover:text-dark-brown px-10 py-4 rounded-lg text-lg font-medium transition-all duration-300 tracking-wide shadow-lg hover:shadow-xl"
              >
                Admin Panel
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

// Simple placeholder components
const SimpleComponent = ({ title, description }) => (
  <div className="min-h-screen bg-dark-brown pt-20">
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-serif text-warm-beige mb-6">{title}</h1>
      <p className="text-light-beige">{description}</p>
    </div>
  </div>
);

const Speisekarte = () => <SimpleComponent title="Speisekarte" description="Hier ist die Speisekarte." />;
const Standorte = () => <SimpleComponent title="Standorte" description="Unsere Standorte." />;
const Bewertungen = () => <SimpleComponent title="Bewertungen" description="Kundenbewertungen." />;
const UeberUns = () => <SimpleComponent title="Über uns" description="Informationen über uns." />;
const Kontakt = () => <SimpleComponent title="Kontakt" description="Kontaktinformationen." />;

// Footer Component
const Footer = () => {
  return (
    <footer className="bg-dark-brown-solid text-light-beige py-12">
      <div className="container mx-auto px-4">
        <div className="border-t border-warm-brown mt-8 pt-6">
          <div className="flex flex-col md:flex-row justify-between items-center text-light-beige font-light">
            <div className="mb-4 md:mb-0">
              <p className="text-sm">
                Website erstellt von{' '}
                <span className="text-warm-beige font-serif tracking-wide">Daniel Böttche</span>
              </p>
            </div>
            <div className="text-center md:text-right">
              <p>&copy; 2024 Jimmy's Tapas Bar. Alle Rechte vorbehalten.</p>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

// Scroll to Top Button Component
const ScrollToTop = () => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const toggleVisibility = () => {
      if (window.pageYOffset > 300) {
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    };

    window.addEventListener('scroll', toggleVisibility);

    return () => window.removeEventListener('scroll', toggleVisibility);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  };

  return (
    <div 
      className={`scroll-to-top ${isVisible ? 'visible' : ''}`}
      onClick={scrollToTop}
    >
      <svg 
        fill="none" 
        stroke="currentColor" 
        viewBox="0 0 24 24" 
        xmlns="http://www.w3.org/2000/svg"
      >
        <path 
          strokeLinecap="round" 
          strokeLinejoin="round" 
          strokeWidth={2} 
          d="M5 10l7-7m0 0l7 7m-7-7v18" 
        />
      </svg>
    </div>
  );
};

// Main App Component
function App() {
  return (
    <LanguageProvider>
      <div className="App min-h-screen bg-dark-brown">
        <BrowserRouter>
          <Header />
          <ScrollToTop />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/speisekarte" element={<Speisekarte />} />
            <Route path="/standorte" element={<Standorte />} />
            <Route path="/ueber-uns" element={<UeberUns />} />
            <Route path="/bewertungen" element={<Bewertungen />} />
            <Route path="/kontakt" element={<Kontakt />} />
            <Route path="/admin" element={<AdminPanel />} />
          </Routes>
          <Footer />
        </BrowserRouter>
      </div>
    </LanguageProvider>
  );
}

export default App;