import React, { useState, useEffect, createContext, useContext } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Link, useNavigate, useLocation } from "react-router-dom";

// Import Admin Sections
import { ContentSection, MenuSection } from './AdminSections';
import { ReviewsSection, ContactsSection, UsersSection } from './AdminSectionsExtended';
import { MediaSection, MaintenanceSection } from './AdminSectionsFinal';

// Import Page Components
import Home from './components/Home';
import Standorte from './components/Standorte';
import UeberUns from './components/UeberUns';
import Speisekarte from './components/Speisekarte';
import Bewertungen from './components/Bewertungen';
import Kontakt from './components/Kontakt';
import Impressum from './components/Impressum';
import Datenschutz from './components/Datenschutz';
import Footer from './components/Footer';

// Language Context - Only German
const LanguageContext = createContext();

const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

// Language Provider Component - Only German
const LanguageProvider = ({ children }) => {
  const [currentLanguage] = useState('de'); // Fixed to German only
  
  // Simplified t function - will be replaced by backend data
  const t = (key) => {
    // This will be replaced by backend-driven content
    return key;
  };

  return (
    <LanguageContext.Provider value={{ currentLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

// Cookie Banner Component
const CookieBanner = () => {
  const [showBanner, setShowBanner] = useState(false);

  useEffect(() => {
    const cookieConsent = localStorage.getItem('cookieConsent');
    if (!cookieConsent) {
      setShowBanner(true);
    }
  }, []);

  const acceptCookies = () => {
    localStorage.setItem('cookieConsent', 'accepted');
    setShowBanner(false);
  };

  const rejectCookies = () => {
    localStorage.setItem('cookieConsent', 'rejected');
    setShowBanner(false);
  };

  if (!showBanner) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-dark-brown border-t-2 border-warm-beige p-4 z-50">
      <div className="container mx-auto">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex-1">
            <h3 className="text-warm-beige font-serif text-lg mb-2">Diese Website verwendet Cookies</h3>
            <p className="text-light-beige text-sm">Wir verwenden Cookies, um Ihnen das beste Website-Erlebnis zu bieten. Durch die weitere Nutzung der Website stimmen Sie der Verwendung von Cookies zu.</p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={rejectCookies}
              className="px-4 py-2 border border-warm-beige text-warm-beige hover:bg-warm-beige hover:text-dark-brown transition-colors text-sm"
            >
              Ablehnen
            </button>
            <button
              onClick={acceptCookies}
              className="px-4 py-2 bg-warm-beige text-dark-brown hover:bg-light-beige transition-colors text-sm"
            >
              Akzeptieren
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Admin Panel Component
const AdminPanel = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loginForm, setLoginForm] = useState({ username: '', password: '' });
  const [activeSection, setActiveSection] = useState('dashboard');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // API Base URL
  const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  console.log('AdminPanel loaded, API_BASE_URL:', API_BASE_URL);

  // Check for existing login on mount
  useEffect(() => {
    const savedToken = localStorage.getItem('adminToken');
    console.log('Checking saved token:', savedToken ? 'Found' : 'Not found');
    if (savedToken) {
      setToken(savedToken);
      verifyToken(savedToken);
    }
  }, []);

  // Authentication Functions
  const verifyToken = async (tokenToVerify) => {
    try {
      console.log('Verifying token...');
      const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${tokenToVerify}`
      };

      const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
        method: 'GET',
        headers
      });
      
      console.log('Token verification response status:', response.status);
      
      if (response.ok) {
        const userData = await response.json();
        console.log('User data received:', userData);
        setUser(userData);
        setIsLoggedIn(true);
      } else {
        console.log('Token verification failed');
        localStorage.removeItem('adminToken');
        setToken(null);
      }
    } catch (error) {
      console.error('Token verification failed:', error);
      localStorage.removeItem('adminToken');
      setToken(null);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    console.log('Attempting login with:', loginForm.username);

    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(loginForm)
      });
      
      console.log('Login response status:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        const newToken = data.access_token;
        console.log('Login successful, token received');
        
        setToken(newToken);
        localStorage.setItem('adminToken', newToken);
        
        // Get user info
        const userResponse = await fetch(`${API_BASE_URL}/api/auth/me`, {
          headers: { 'Authorization': `Bearer ${newToken}` }
        });
        
        if (userResponse.ok) {
          const userData = await userResponse.json();
          setUser(userData);
          setIsLoggedIn(true);
          setSuccess('Erfolgreich angemeldet!');
        }
      } else {
        const errorData = await response.json();
        console.error('Login failed:', errorData);
        setError(errorData.detail || 'Anmeldung fehlgeschlagen');
      }
    } catch (error) {
      console.error('Login error:', error);
      setError('Verbindungsfehler. Bitte versuchen Sie es erneut.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('adminToken');
    setToken(null);
    setUser(null);
    setIsLoggedIn(false);
    setActiveSection('dashboard');
    setSuccess('Erfolgreich abgemeldet');
  };

  // Login Screen
  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
              Jimmy's Tapas Bar - Admin Panel
            </h2>
            <p className="mt-2 text-center text-sm text-gray-600">
              Melden Sie sich an, um das CMS zu verwalten
            </p>
          </div>
          <form className="mt-8 space-y-6" onSubmit={handleLogin}>
            <div className="rounded-md shadow-sm -space-y-px">
              <div>
                <input
                  type="text"
                  required
                  value={loginForm.username}
                  onChange={(e) => setLoginForm({...loginForm, username: e.target.value})}
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                  placeholder="Benutzername"
                />
              </div>
              <div>
                <input
                  type="password"
                  required
                  value={loginForm.password}
                  onChange={(e) => setLoginForm({...loginForm, password: e.target.value})}
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                  placeholder="Passwort"
                />
              </div>
            </div>

            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            {success && (
              <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
                {success}
              </div>
            )}

            <div>
              <button
                type="submit"
                disabled={loading}
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                {loading ? 'Anmelden...' : 'Anmelden'}
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  }

  // Admin Dashboard
  return (
    <div className="min-h-screen bg-gray-100" style={{paddingTop: '80px'}}>
      <div className="flex" style={{minHeight: 'calc(100vh - 80px)'}}>
        {/* Sidebar */}
        <div className="w-64 bg-white shadow-lg" style={{position: 'fixed', height: 'calc(100vh - 80px)', top: '80px', zIndex: 40}}>
          <div className="p-6">
            <h1 className="text-xl font-bold text-gray-900">Admin Panel</h1>
            <p className="text-sm text-gray-600">Willkommen, {user?.username}</p>
          </div>
          <nav className="mt-6">
            <button
              onClick={() => setActiveSection('dashboard')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'dashboard' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              Dashboard
            </button>
            <button
              onClick={() => setActiveSection('content')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'content' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              Homepage bearbeiten
            </button>
            <button
              onClick={() => setActiveSection('menu')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'menu' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              Speisekarte
            </button>
            <button
              onClick={() => setActiveSection('reviews')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'reviews' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              Bewertungen
            </button>
            <button
              onClick={() => setActiveSection('contacts')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'contacts' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              Kontakt-Nachrichten
            </button>
            <button
              onClick={() => setActiveSection('users')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'users' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              Benutzer-Verwaltung
            </button>
            <button
              onClick={() => setActiveSection('legal')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'legal' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              Impressum & Datenschutz
            </button>
            <button
              onClick={() => setActiveSection('media')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'media' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              Medien
            </button>
            <button
              onClick={() => setActiveSection('maintenance')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'maintenance' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              Wartungsmodus
            </button>
            <button
              onClick={handleLogout}
              className="w-full text-left px-6 py-3 text-sm text-red-600 hover:bg-red-50 mt-4 border-t"
            >
              Abmelden
            </button>
          </nav>
        </div>

        {/* Main Content */}
        <div className="flex-1 p-8" style={{marginLeft: '256px'}}>
          {activeSection === 'dashboard' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h2>
              <div className="bg-white rounded-lg shadow p-6">
                <p className="text-gray-600">Willkommen im Admin-Panel von Jimmy's Tapas Bar!</p>
                <p className="text-gray-600 mt-2">Verwenden Sie das Menü links, um verschiedene Bereiche zu verwalten.</p>
              </div>
            </div>
          )}
          {activeSection === 'content' && <ContentSection />}
          {activeSection === 'menu' && <MenuSection />}
          {activeSection === 'reviews' && <ReviewsSection />}
          {activeSection === 'contacts' && <ContactsSection />}
          {activeSection === 'users' && <UsersSection />}
          {activeSection === 'legal' && <LegalEditor />}
          {activeSection === 'media' && <MediaSection />}
          {activeSection === 'maintenance' && <MaintenanceSection />}
        </div>
      </div>
    </div>
  );
};

// Header Component  
const Header = () => {
  const location = useLocation();
  const [navigationTexts, setNavigationTexts] = useState({
    home: 'Startseite',
    locations: 'Standorte', 
    menu: 'Speisekarte',
    reviews: 'Bewertungen',
    about: 'Über uns',
    contact: 'Kontakt',
    privacy: 'Datenschutz',
    imprint: 'Impressum'
  });

  // Load navigation texts from backend
  useEffect(() => {
    const loadNavigationTexts = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/website-texts/navigation`);
        if (response.ok) {
          const data = await response.json();
          if (data.navigation) {
            setNavigationTexts(data.navigation);
          }
        }
      } catch (error) {
        console.error('Error loading navigation texts:', error);
      }
    };
    loadNavigationTexts();
  }, []);
  
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
            }`}>{navigationTexts.home}</Link>
            <Link to="/standorte" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/standorte') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>{navigationTexts.locations}</Link>
            <Link to="/speisekarte" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/speisekarte') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>{navigationTexts.menu}</Link>
            <Link to="/bewertungen" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/bewertungen') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>{navigationTexts.reviews}</Link>
            <Link to="/ueber-uns" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/ueber-uns') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>{navigationTexts.about}</Link>
            <Link to="/kontakt" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/kontakt') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>{navigationTexts.contact}</Link>
          </div>
        </nav>
      </div>
    </header>
  );
};

// Main App Component
function App() {
  return (
    <LanguageProvider>
      <div className="App">
        <BrowserRouter>
          <Header />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/standorte" element={<Standorte />} />
            <Route path="/speisekarte" element={<Speisekarte />} />
            <Route path="/bewertungen" element={<Bewertungen />} />
            <Route path="/ueber-uns" element={<UeberUns />} />
            <Route path="/kontakt" element={<Kontakt />} />
            <Route path="/impressum" element={<Impressum />} />
            <Route path="/datenschutz" element={<Datenschutz />} />
            <Route path="/admin" element={<AdminPanel />} />
          </Routes>
          <Footer />
          <CookieBanner />
        </BrowserRouter>
      </div>
    </LanguageProvider>
  );
}

export default App;