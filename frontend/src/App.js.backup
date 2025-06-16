import React, { useState, useEffect, createContext, useContext } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Link, useNavigate, useLocation } from "react-router-dom";

// Import Admin Sections
import { ContentSection, MenuSection } from './AdminSections';
import { ReviewsSection, ContactsSection, UsersSection } from './AdminSectionsExtended';
import { MediaSection, MaintenanceSection } from './AdminSectionsFinal';

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


// Professional Admin CMS Dashboard Component
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
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center px-4">
        <div className="bg-white/10 backdrop-blur-lg p-8 rounded-2xl border border-white/20 max-w-md w-full shadow-2xl">
          <div className="text-center mb-8">
            <div className="w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">CMS Login</h1>
            <p className="text-white/70">Jimmy's Tapas Bar Verwaltung</p>
          </div>

          {error && (
            <div className="bg-red-500/20 border border-red-500/50 text-red-200 px-4 py-3 rounded-lg mb-6">
              {error}
            </div>
          )}

          {success && (
            <div className="bg-green-500/20 border border-green-500/50 text-green-200 px-4 py-3 rounded-lg mb-6">
              {success}
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-6">
            <div>
              <label className="block text-white/90 mb-2 font-medium">Benutzername</label>
              <input
                type="text"
                value={loginForm.username}
                onChange={(e) => setLoginForm({...loginForm, username: e.target.value})}
                className="w-full p-4 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent backdrop-blur-sm"
                placeholder="admin"
                required
                disabled={loading}
              />
            </div>
            <div>
              <label className="block text-white/90 mb-2 font-medium">Passwort</label>
              <input
                type="password"
                value={loginForm.password}
                onChange={(e) => setLoginForm({...loginForm, password: e.target.value})}
                className="w-full p-4 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent backdrop-blur-sm"
                placeholder="••••••••"
                required
                disabled={loading}
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-200 transform hover:scale-105 disabled:opacity-50 disabled:transform-none"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Anmelden...
                </div>
              ) : (
                'Anmelden'
              )}
            </button>
          </form>

          <div className="mt-6 text-center">
            <div className="bg-white/5 rounded-lg p-4 border border-white/10">
              <p className="text-white/60 text-sm mb-2">Standard-Zugangsdaten:</p>
              <p className="text-white/80 text-sm font-mono">admin / jimmy2024</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Main Admin Dashboard
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Navigation Bar */}
      <nav className="bg-white border-b border-gray-200 fixed w-full z-30 top-0">
        <div className="px-6 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="flex items-center mr-6">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center mr-3">
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                </div>
                <h1 className="text-xl font-bold text-gray-900">Jimmy's CMS</h1>
              </div>
              <div className="text-sm text-gray-500">
                Content Management System
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className="flex items-center text-sm text-gray-700">
                <div className="w-8 h-8 bg-gradient-to-r from-green-400 to-blue-500 rounded-full flex items-center justify-center mr-2">
                  <span className="text-white font-medium text-xs">
                    {user?.username?.charAt(0).toUpperCase()}
                  </span>
                </div>
                <div>
                  <div className="font-medium">{user?.username}</div>
                  <div className="text-xs text-gray-500 capitalize">{user?.role}</div>
                </div>
              </div>
              <button
                onClick={handleLogout}
                className="bg-red-100 text-red-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-red-200 transition-colors"
              >
                Abmelden
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="flex pt-16">
        {/* Sidebar Navigation */}
        <aside className="w-64 bg-white border-r border-gray-200 min-h-screen fixed">
          <nav className="p-4">
            <div className="space-y-2">
              {[
                { id: 'dashboard', name: 'Dashboard', icon: 'M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z' },
                { id: 'content', name: 'Inhalte', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
                { id: 'menu', name: 'Speisekarte', icon: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253' },
                { id: 'reviews', name: 'Bewertungen', icon: 'M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z' },
                { id: 'contacts', name: 'Kontakte', icon: 'M3 8l7.89 7.89a2 2 0 002.83 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' },
                { id: 'users', name: 'Benutzer', icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z' },
                { id: 'media', name: 'Medien', icon: 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z' },
                { id: 'maintenance', name: 'Wartung', icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z' }
              ].map((item) => (
                <button
                  key={item.id}
                  onClick={() => setActiveSection(item.id)}
                  className={`w-full flex items-center px-4 py-3 text-left rounded-lg transition-colors ${
                    activeSection === item.id
                      ? 'bg-blue-50 text-blue-700 border border-blue-200'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={item.icon} />
                  </svg>
                  {item.name}
                </button>
              ))}
            </div>
          </nav>
        </aside>

        {/* Main Content Area */}
        <main className="flex-1 ml-64 p-8">
          {activeSection === 'dashboard' && <DashboardSection user={user} token={token} apiCall={apiCall} />}
          {activeSection === 'content' && <ContentSection user={user} token={token} apiCall={apiCall} />}
          {activeSection === 'menu' && <MenuSection user={user} token={token} apiCall={apiCall} />}
          {activeSection === 'reviews' && <ReviewsSection user={user} token={token} apiCall={apiCall} />}
          {activeSection === 'contacts' && <ContactsSection user={user} token={token} apiCall={apiCall} />}
          {activeSection === 'users' && <UsersSection user={user} token={token} apiCall={apiCall} />}
          {activeSection === 'media' && <MediaSection user={user} token={token} apiCall={apiCall} />}
          {activeSection === 'maintenance' && <MaintenanceSection user={user} token={token} apiCall={apiCall} />}
        </main>
      </div>
    </div>
  );
};

// Dashboard Overview Section
const DashboardSection = ({ user, token, apiCall }) => {
  const [stats, setStats] = useState({
    totalMenuItems: 0,
    pendingReviews: 0,
    totalContacts: 0,
    totalUsers: 0
  });
  const [recentActivities, setRecentActivities] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      // Load statistics
      const [menuResponse, reviewsResponse, contactsResponse, usersResponse] = await Promise.all([
        apiCall('/menu/items'),
        apiCall('/admin/reviews/pending'),
        apiCall('/admin/contact'),
        apiCall('/users')
      ]);

      if (menuResponse.ok) {
        const menuData = await menuResponse.json();
        setStats(prev => ({ ...prev, totalMenuItems: menuData.length }));
      }

      if (reviewsResponse.ok) {
        const reviewsData = await reviewsResponse.json();
        setStats(prev => ({ ...prev, pendingReviews: reviewsData.length }));
      }

      if (contactsResponse.ok) {
        const contactsData = await contactsResponse.json();
        setStats(prev => ({ ...prev, totalContacts: contactsData.length }));
      }

      if (usersResponse.ok) {
        const usersData = await usersResponse.json();
        setStats(prev => ({ ...prev, totalUsers: usersData.length }));
      }

    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Welcome Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Willkommen zurück, {user?.username}!
        </h1>
        <p className="text-gray-600">
          Hier ist eine Übersicht über Ihr Jimmy's Tapas Bar CMS Dashboard.
        </p>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Menü-Artikel</p>
              <p className="text-2xl font-bold text-gray-900">{stats.totalMenuItems}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <svg className="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Wartende Bewertungen</p>
              <p className="text-2xl font-bold text-gray-900">{stats.pendingReviews}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 7.89a2 2 0 002.83 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Kontakt-Nachrichten</p>
              <p className="text-2xl font-bold text-gray-900">{stats.totalContacts}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Benutzer</p>
              <p className="text-2xl font-bold text-gray-900">{stats.totalUsers}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Schnellzugriffe</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { name: 'Neues Gericht hinzufügen', icon: 'M12 6v6m0 0v6m0-6h6m-6 0H6', color: 'blue' },
            { name: 'Bewertungen prüfen', icon: 'M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z', color: 'yellow' },
            { name: 'Inhalte bearbeiten', icon: 'M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z', color: 'green' },
            { name: 'Wartungsmodus', icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z', color: 'red' }
          ].map((action, index) => (
            <button
              key={index}
              className={`p-4 rounded-lg border-2 border-dashed border-${action.color}-200 hover:border-${action.color}-300 hover:bg-${action.color}-50 transition-colors group`}
            >
              <svg className={`w-8 h-8 text-${action.color}-500 mx-auto mb-2`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={action.icon} />
              </svg>
              <p className="text-sm font-medium text-gray-700 group-hover:text-gray-900">{action.name}</p>
            </button>
          ))}
        </div>
      </div>

      {/* System Status */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">System Status</h2>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-gray-600">Backend API</span>
            <span className="flex items-center text-green-600">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
              Online
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-600">Datenbank</span>
            <span className="flex items-center text-green-600">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
              Verbunden
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-600">Letzte Aktualisierung</span>
            <span className="text-gray-500">Vor {Math.floor(Math.random() * 5) + 1} Minuten</span>
          </div>
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
};const Home = () => {
  const navigate = useNavigate();
  const [homepageContent, setHomepageContent] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load homepage content from backend
  useEffect(() => {
    const loadHomepageContent = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/homepage`);
        if (response.ok) {
          const data = await response.json();
          setHomepageContent(data);
        }
      } catch (error) {
        console.error('Error loading homepage content:', error);
      } finally {
        setLoading(false);
      }
    };
    loadHomepageContent();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-warm-beige"></div>
      </div>
    );
  }

  // Fallback to default content if backend is unavailable
  const hero = homepageContent?.hero || {
    title: "JIMMY'S TAPAS BAR",
    subtitle: "an der Ostsee",
    description: "Genießen Sie authentische mediterrane Spezialitäten",
    location: "direkt an der malerischen Ostseeküste",
    background_image: "https://images.unsplash.com/photo-1656423521731-9665583f100c",
    menu_button_text: "Zur Speisekarte",
    locations_button_text: "Unsere Standorte"
  };

  const features = homepageContent?.features || {
    title: "Mediterrane Tradition",
    subtitle: "Erleben Sie authentische mediterrane Gastfreundschaft an der deutschen Ostseeküste",
    cards: [
      {
        title: "Authentische Tapas",
        description: "Traditionelle mediterrane Gerichte, mit Liebe zubereitet und perfekt zum Teilen",
        image_url: "https://images.pexels.com/photos/19671352/pexels-photo-19671352.jpeg"
      },
      {
        title: "Frische Paella",
        description: "Täglich hausgemacht mit Meeresfrüchten, Gemüse oder Huhn",
        image_url: "https://images.unsplash.com/photo-1694685367640-05d6624e57f1"
      },
      {
        title: "Strandnähe",
        description: "Beide Standorte direkt an der malerischen Ostseeküste – perfekt für entspannte Stunden",
        image_url: "https://images.pexels.com/photos/32508247/pexels-photo-32508247.jpeg"
      }
    ]
  };

  const specialties = homepageContent?.specialties || {
    title: "Unsere Spezialitäten",
    cards: [
      {
        title: "Patatas Bravas",
        description: "Klassische mediterrane Kartoffeln",
        image_url: "https://images.unsplash.com/photo-1565599837634-134bc3aadce8",
        category_link: "tapas-vegetarian"
      },
      {
        title: "Paella Valenciana",
        description: "Traditionelle mediterrane Paella",
        image_url: "https://images.pexels.com/photos/7085661/pexels-photo-7085661.jpeg",
        category_link: "tapa-paella"
      },
      {
        title: "Tapas Variación",
        description: "Auswahl mediterraner Köstlichkeiten",
        image_url: "https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg",
        category_link: "inicio"
      },
      {
        title: "Gambas al Ajillo",
        description: "Garnelen in Knoblauchöl",
        image_url: "https://images.unsplash.com/photo-1619860705243-dbef552e7118",
        category_link: "tapas-pescado"
      }
    ]
  };

  const delivery = homepageContent?.delivery || {
    title: "Jetzt auch bequem nach Hause bestellen",
    description: "Genießen Sie unsere authentischen mediterranen Spezialitäten gemütlich zu Hause.",
    description_2: "Bestellen Sie direkt über Lieferando und lassen Sie sich verwöhnen.",
    delivery_feature_title: "Schnelle Lieferung",
    delivery_feature_description: "Frisch und warm zu Ihnen",
    delivery_feature_image: "https://images.pexels.com/photos/6969962/pexels-photo-6969962.jpeg",
    button_text: "Jetzt bei Lieferando bestellen",
    button_url: "https://www.lieferando.de",
    availability_text: "Verfügbar für beide Standorte",
    authentic_feature_title: "Authentisch Mediterran",
    authentic_feature_description: "Direkt vom Küchenchef",
    authentic_feature_image: "https://images.pexels.com/photos/31748679/pexels-photo-31748679.jpeg"
  };
  
  return (
    <div className="min-h-screen">
      {/* Clean Professional Hero Section */}
      <section id="main-content" className="relative h-screen bg-cover bg-center hero-background" 
               style={{backgroundImage: `url('${hero.background_image}')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-50"></div>
        <div className="relative z-10 flex items-center justify-center h-full text-center px-4" style={{paddingTop: '80px'}}>
          <div className="max-w-4xl">
            {/* Clean Main Headline with proper spacing */}
            <h1 className="hero-headline font-serif text-warm-beige mb-8 tracking-wide leading-tight drop-shadow-text" style={{fontSize: 'clamp(2.5rem, 8vw, 6rem)', lineHeight: '1.1', marginTop: '40px'}}>
              {hero.title}<br />
              <span className="font-light opacity-90" style={{fontSize: 'clamp(1.8rem, 5vw, 4rem)'}}>{hero.subtitle}</span>
            </h1>
            
            {/* Simple Subtitle */}
            <p className="text-xl md:text-2xl text-warm-beige font-light mb-12 max-w-3xl mx-auto leading-relaxed opacity-95">
              {hero.description}<br/>
              <span className="text-lg opacity-80">{hero.location}</span>
            </p>
            
            {/* Clean CTA Buttons */}
            <div className="flex flex-col md:flex-row justify-center gap-6">
              <button 
                onClick={() => navigate('/speisekarte')}
                className="bg-warm-beige text-dark-brown hover:bg-light-beige px-10 py-4 rounded-lg text-lg font-medium transition-all duration-300 tracking-wide shadow-lg hover:shadow-xl"
              >
                {hero.menu_button_text}
              </button>
              <button 
                onClick={() => navigate('/standorte')}
                className="border-2 border-warm-beige text-warm-beige hover:bg-warm-beige hover:text-dark-brown px-10 py-4 rounded-lg text-lg font-medium transition-all duration-300 tracking-wide shadow-lg hover:shadow-xl"
              >
                {hero.locations_button_text}
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Professional Features Section */}
      <section className="py-24 bg-gradient-to-b from-dark-brown to-medium-brown">
        <div className="container mx-auto px-4">
          <div className="text-center mb-20">
            <h2 className="text-5xl font-serif text-warm-beige mb-8 tracking-wide">
              {features.title}
            </h2>
            <p className="text-xl text-light-beige font-light leading-relaxed max-w-3xl mx-auto">
              {features.subtitle}
            </p>
          </div>
          
          {/* Clean Three Cards - Professional Layout with Product Images */}
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {features.cards.map((card, index) => (
              <div key={index} className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-all duration-300 border border-warm-brown shadow-lg">
                <img 
                  src={card.image_url} 
                  alt={card.title} 
                  className="w-full h-48 object-cover"
                />
                <div className="p-8 text-center">
                  <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">{card.title}</h3>
                  <p className="text-light-beige font-light leading-relaxed">
                    {card.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Clean Food Gallery - Professional with Navigation */}
      <section className="py-20 bg-medium-brown">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-serif text-center text-warm-beige mb-16 tracking-wide">
            {specialties.title}
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {specialties.cards.map((card, index) => (
              <div 
                key={index}
                className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-warm-brown cursor-pointer"
                onClick={() => {
                  navigate('/speisekarte');
                  if (card.category_link) {
                    setTimeout(() => {
                      window.location.href = `/speisekarte#${card.category_link}`;
                    }, 100);
                  }
                }}
              >
                <img src={card.image_url} alt={card.title} className="w-full h-48 object-cover" />
                <div className="p-6">
                  <h3 className="font-serif text-warm-beige text-lg tracking-wide">{card.title}</h3>
                  <p className="text-light-beige text-sm font-light">{card.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Lieferando Section */}
      <section className="py-16 bg-gradient-to-r from-dark-brown to-medium-brown">
        <div className="container mx-auto px-4 text-center">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-4xl font-serif text-warm-beige mb-8 tracking-wide">
              {delivery.title}
            </h2>
            <p className="text-xl text-light-beige font-light mb-12 leading-relaxed">
              {delivery.description}<br/>
              {delivery.description_2}
            </p>
            <div className="bg-dark-brown rounded-lg p-8 border border-warm-brown shadow-lg">
              <div className="flex flex-col md:flex-row items-center justify-center gap-8">
                <div className="text-center">
                  <div className="w-24 h-24 bg-cover bg-center rounded-lg mx-auto mb-4 border-2 border-warm-beige" 
                       style={{backgroundImage: `url('${delivery.delivery_feature_image}')`}}>
                  </div>
                  <h3 className="text-xl font-serif text-warm-beige mb-2">{delivery.delivery_feature_title}</h3>
                  <p className="text-light-beige text-sm">{delivery.delivery_feature_description}</p>
                </div>
                <div className="text-center">
                  <a 
                    href={delivery.button_url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="inline-block bg-orange-500 hover:bg-orange-600 text-white px-8 py-4 rounded-lg text-lg font-medium transition-all duration-300 tracking-wide shadow-lg hover:shadow-xl transform hover:scale-105"
                  >
                    {delivery.button_text}
                  </a>
                  <p className="text-light-beige text-sm mt-2">{delivery.availability_text}</p>
                </div>
                <div className="text-center">
                  <div className="w-24 h-24 bg-cover bg-center rounded-lg mx-auto mb-4 border-2 border-warm-beige" 
                       style={{backgroundImage: `url('${delivery.authentic_feature_image}')`}}>
                  </div>
                  <h3 className="text-xl font-serif text-warm-beige mb-2">{delivery.authentic_feature_title}</h3>
                  <p className="text-light-beige text-sm">{delivery.authentic_feature_description}</p>
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
const Speisekarte = () => {
  const [selectedCategory, setSelectedCategory] = useState('alle');
  
  // Complete menu data with authentic images for hover display (Screenshot Style)
  const menuItems = {
    'inicio': [
      { name: 'Aioli', description: 'Hausgemachte Knoblauch-Mayonnaise', price: '3,50', image: 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f', details: 'Hausgemachte, cremige Knoblauch-Mayonnaise nach traditionellem valencianischem Rezept. Zubereitet mit frischem Knoblauch aus Spanien, nativem Olivenöl extra aus Andalusien und Zitronensaft. Serviert mit ofentrischem, spanischem Weißbrot. Perfekt zum Einstieg in einen mediterranen Abend.' },
      { name: 'Oliven', description: 'Marinierte spanische Oliven', price: '3,90', image: 'https://images.unsplash.com/photo-1714583357992-98f0ad946902', details: 'Ausgewählte schwarze Arbequina-Oliven aus Katalonien und grüne Manzanilla-Oliven aus Sevilla, mariniert mit wildem Thymian, rosa Pfefferkörnern, Knoblauch und bestem Olivenöl extra vergine. 24 Stunden eingelegt für optimalen Geschmack.' },
      { name: 'Extra Brot', description: 'Frisches spanisches Brot', price: '1,90', image: 'https://images.unsplash.com/photo-1549931319-a545dcf3bc73', details: 'Warmes, knuspriges Pan de Pueblo nach traditionellem kastilischem Rezept. Täglich frisch gebacken mit Steinofenmehl aus der Region Castilla y León, Meersalz und natürlicher Hefe. Perfekt für Tapas und Dips.' },
      { name: 'Hummus', description: 'Cremiger Kichererbsen-Dip', price: '3,90', image: 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f', details: 'Hausgemachter Hummus aus Kichererbsen (Garbanzo-Bohnen) aus Kastilien, Tahini aus Sesam, Zitrone und Kreuzkümmel. Nach mediterraner Tradition zubereitet. Serviert mit frischem Gemüse und warmem Brot.' },
      { name: 'Spanischer Käseteller', description: 'Auswahl spanischer Käsesorten', price: '8,90', image: 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d', details: 'Edle Auswahl aus der Mancha: Manchego D.O.P. (12 Monate gereift), Cabrales D.O.P. aus Asturien (Blauschimmelkäse) und Murcia al Vino aus Murcia (in Rotwein gereift). Serviert mit Walnüssen aus Kalifornien, Akazienhonig und frischen Moscatel-Trauben.' },
      { name: 'Schinken-Käse-Wurst Teller', description: 'Spanische Charcuterie-Platte', price: '11,90', image: 'https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg', details: 'Edle Auswahl aus Jamón Serrano, Chorizo, Lomo und spanischen Käsesorten mit Oliven, Nüssen und Feigenmarmelade.' },
      { name: 'Jamón Serrano Teller', description: 'Hochwertiger spanischer Schinken', price: '9,90', image: 'https://images.pexels.com/photos/24706530/pexels-photo-24706530.jpeg', details: '18 Monate gereifter Jamón Serrano D.O. aus den Bergen der Sierra Nevada, hauchdünn geschnitten. Serviert mit 12 Monate gereiftem Manchego-Käse D.O.P. und geröstetem Brot aus Kastilien. Von freilaufenden iberischen Schweinen.' },
      { name: 'Pata Negra', description: 'Premium Iberico Schinken', price: '10,90', image: 'https://images.unsplash.com/photo-1598989519542-077da0f51c09', details: 'Der Edelste aller spanischen Schinken - Jamón Ibérico de Bellota D.O.P. aus Extremadura, 36 Monate gereift. Von schwarzfüßigen Iberico-Schweinen, die sich ausschließlich von Eicheln ernähren. Serviert mit Manchego Reserva und Tomaten-Brot.' },
      { name: 'Tres (Hummus, Avocado Cream, Aioli mit Brot)', description: 'Drei köstliche Dips mit Brot', price: '10,90', image: 'https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg', details: 'Trio aus hausgemachtem Hummus, cremiger Avocado-Creme und Aioli, serviert mit warmem spanischem Brot und Gemüse.' }
    ],
    'salat': [
      { name: 'Ensalada Mixta', description: 'Gemischter Salat mit spanischen Zutaten', price: '8,90', details: 'Frischer Salat mit Tomaten, Gurken, Oliven, roten Zwiebeln und Manchego-Käse in Sherry-Vinaigrette.' },
      { name: 'Ensalada Tonno', description: 'Salat mit Thunfisch', price: '14,90', details: 'Gemischter Salat mit saftigem Thunfisch, hartgekochten Eiern, Oliven und Kapern in mediteraner Vinaigrette.' },
      { name: 'Ensalada Pollo', description: 'Salat mit gegrilltem Hähnchen', price: '14,90', details: 'Frischer Salat mit gegrillten Hähnchenstreifen, Cherrytomaten, Avocado und gerösteten Pinienkernen.' },
      { name: 'Ensalada Garnelen', description: 'Salat mit frischen Garnelen', price: '15,90', details: 'Bunter Salat mit saftigen Garnelen, Avocado, Mango und einem Hauch von Chili in Limetten-Dressing.' }
    ],
    'kleiner-salat': [
      { name: 'Tomaten/Gurken mit Zwiebeln', description: 'Frischer Gemüsesalat', price: '6,90', details: 'Saftige Tomaten und knackige Gurken mit roten Zwiebeln in aromatischem Olivenöl und Kräutern.' },
      { name: 'Rote Beete mit Ziegenkäse', description: 'Süße rote Beete mit cremigem Ziegenkäse', price: '7,90', details: 'Geröstete rote Beete mit cremigem Ziegenkäse, Walnüssen und Honig-Thymian-Dressing.' },
      { name: 'Kichererbsen mit Feta', description: 'Proteinreicher Salat mit Feta', price: '7,90', details: 'Warme Kichererbsen mit Feta-Käse, frischen Kräutern, Tomaten und Zitronendressing.' }
    ],
    'tapa-paella': [
      { name: 'Paella mit Hähnchen & Meeresfrüchten', description: 'Traditionelle spanische Paella als Tapa-Portion', price: '8,90', details: 'Authentische Paella mit saftigem Hähnchen, frischen Garnelen, Muscheln und Bomba-Reis in würziger Safran-Brühe.' },
      { name: 'Paella vegetarisch', description: 'Vegetarische Paella mit frischem Gemüse', price: '7,90', details: 'Vegetarische Paella mit grünen Bohnen, Paprika, Artischocken und Bomba-Reis in aromatischer Gemüsebrühe.' }
    ],
    'tapas-vegetarian': [
      { name: 'Gebratenes Gemüse', description: 'Vegan - Saisonales Gemüse mediterran gewürzt', price: '6,90', vegan: true, glutenfree: true, details: 'Frisches Saisongemüse wie Zucchini, Paprika und Auberginen, gegrillt mit Rosmarin, Thymian und Olivenöl.' },
      { name: 'Papas Bravas', description: 'Vegan - Klassische spanische Kartoffeln mit scharfer Soße', price: '6,90', vegan: true, glutenfree: true, details: 'Knusprig gebratene Kartoffelwürfel aus der Region Galicia mit pikanter Bravas-Sauce aus San Marzano-Tomaten, geröstetem Paprikapulver aus Murcia (Pimentón de la Vera D.O.P.) und einem Hauch Cayenne-Chili. Original Madrider Rezept.' },
      { name: 'Tortilla de Patata mit Aioli', description: 'Spanisches Kartoffel-Omelett mit Aioli', price: '6,90', vegetarian: true, glutenfree: true, details: 'Klassische spanische Tortilla aus Kartoffeln der Region Castilla y León und frischen Eiern, golden gebraten nach traditionellem Rezept aus Madrid. Serviert mit hausgemachtem Aioli aus bestem andalusischem Olivenöl.' },
      { name: 'Pimientos de Padrón', description: 'Vegan - Gebratene grüne Paprika', price: '6,90', vegan: true, glutenfree: true, details: 'Original Pimientos de Padrón D.O.P. aus Galicien - kleine grüne Paprikaschoten, gebraten in nativem Olivenöl extra aus Jaén und mit Flor de Sal (Meersalz) aus Cádiz bestreut. Traditionell: manche scharf, manche mild!' },
      { name: 'Kanarische Kartoffeln', description: 'Vegan - Traditionelle Kartoffeln mit Meersalz', price: '6,90', vegan: true, glutenfree: true, details: 'Papas Arrugadas - kleine Kartoffeln aus Teneriffa in der Schale gekocht mit grobem Atlantik-Meersalz. Serviert mit grüner Mojo Verde (Koriander, Petersilie) und roter Mojo Rojo (geröstete Paprika) aus den Kanarischen Inseln.' },
      { name: 'Fetahäppchen auf Johannisbeersauce', description: 'Cremiger Feta mit süß-saurer Sauce', price: '6,90', details: 'Warme Feta-Würfel auf einer Reduktion aus roten Johannisbeeren mit einem Hauch Balsamico und frischen Kräutern.' },
      { name: 'Ziegenkäse auf Johannisbeersauce oder Honig-Senf', description: 'Mild-cremiger Ziegenkäse mit Sauce nach Wahl', price: '6,90', details: 'Warmer Ziegenkäse wahlweise mit süßer Johannisbeersauce oder würzigem Honig-Senf-Dressing und gerösteten Nüssen.' },
      { name: 'Falafel mit Joghurt-Minz-Sauce', description: 'Knusprige Kichererbsenbällchen mit erfrischender Sauce', price: '6,90', details: 'Hausgemachte Falafel aus Kichererbsen und orientalischen Gewürzen, serviert mit cremiger Joghurt-Minz-Sauce.' },
      { name: 'Überbackener Feta mit Cherrytomaten', description: 'Warmer Feta mit süßen Cherrytomaten', price: '6,90', details: 'Feta-Käse überbacken mit Cherrytomaten, Oliven, Oregano und einem Schuss Olivenöl, serviert mit frischem Brot.' },
      { name: 'Champignons mit Reis & Pinienkernen auf Roquefort', description: 'Aromatische Pilze mit würzigem Käse', price: '6,90', details: 'Gefüllte Champignons mit Reis, gerösteten Pinienkernen und würzigem Roquefort-Käse, überbacken und mit Kräutern garniert.' },
      { name: 'Überbackene Tomaten mit Spinat & Roquefort', description: 'Mediterrane Gemüse-Käse-Kombination', price: '6,90', details: 'Große Tomaten gefüllt mit frischem Spinat und würzigem Roquefort, überbacken und mit Basilikum garniert.' },
      { name: 'Frittierte Auberginen mit Honig', description: 'Süß-herzhafte Auberginen-Kreation', price: '6,90', details: 'Auberginenscheiben in leichtem Teig frittiert, mit spanischem Honig glasiert und mit frischen Kräutern garniert.' },
      { name: 'Champignons al Ajillo', description: 'Vegan - Pilze in Knoblauchöl', price: '6,90', details: 'Frische Champignons geschmort in Knoblauchöl mit Petersilie, Chili und einem Schuss Weißwein - ein Klassiker!' },
      { name: 'Teigtaschen mit Spinat & Kräutersauce', description: 'Hausgemachte Teigtaschen mit frischen Kräutern', price: '6,90', details: 'Hausgemachte Teigtaschen gefüllt mit Spinat und Ricotta, serviert mit einer cremigen Kräutersauce.' },
      { name: 'Feta Feigen', description: 'Süße Feigen mit salzigem Feta', price: '6,90', details: 'Frische Feigen gefüllt mit cremigem Feta-Käse, gerösteten Walnüssen und einem Hauch Honig.' },
      { name: 'Ziegenkäse auf Fenchel & Walnuss', description: 'Aromatische Kombination mit Nüssen', price: '6,90', details: 'Warmer Ziegenkäse auf einem Bett aus geröstetem Fenchel mit gerösteten Walnüssen und Honig-Balsamico-Glasur.' },
      { name: 'Gebratener Spinat mit Cherrytomaten', description: 'Vegan - Frischer Spinat mit süßen Tomaten', price: '6,90', details: 'Frischer Spinat geschmort mit Cherrytomaten, Knoblauch und Pinienkernen in bestem Olivenöl.' }
    ],
    'tapas-pollo': [
      { name: 'Hähnchen mit Limetten-Sauce', description: 'Zartes Hähnchen in frischer Zitrus-Sauce', price: '7,20', details: 'Saftige Hähnchenstücke in einer frischen Limetten-Sauce mit Koriander und einem Hauch Chili, serviert mit Kräuterreis.' },
      { name: 'Knuspriges Hähnchen mit Honig-Senf', description: 'Goldbraun gebratenes Hähnchen mit süß-scharfer Sauce', price: '7,20', details: 'Knusprig paniertes Hähnchen mit hausgemachter Honig-Senf-Sauce, garniert mit frischen Kräutern.' },
      { name: 'Hähnchenspieß mit Chili', description: 'Würziger Hähnchen-Spieß mit Chili', price: '7,20', details: 'Marinierte Hähnchenstücke am Spieß mit pikanter Chili-Sauce und gegrilltem Gemüse.' },
      { name: 'Hähnchen mit Curry', description: 'Exotisch gewürztes Hähnchen', price: '7,20', details: 'Zart geschmortes Hähnchen in aromatischer Curry-Sauce mit Kokosmilch und mediterranen Gewürzen.' },
      { name: 'Hähnchen mit Mandelsauce', description: 'Cremige Mandel-Sauce zu zartem Hähnchen', price: '7,20', details: 'Gebratenes Hähnchen in feiner Mandel-Sahne-Sauce mit gerösteten Mandelblättchen.' },
      { name: 'Hähnchen-Chorizo-Spieß', description: 'Spanische Wurst-Fleisch-Kombination', price: '7,20', details: 'Abwechselnd Hähnchen und würzige Chorizo am Spieß gegrillt, serviert mit Paprika und Zwiebeln.' },
      { name: 'Hähnchen mit Brandy-Sauce', description: 'Edle Brandy-Sauce zu saftigem Hähnchen', price: '7,20', details: 'Gebratenes Hähnchen in einer cremigen Sauce aus spanischem Brandy, Sahne und feinen Gewürzen.' }
    ],
    'tapas-carne': [
      { name: 'Dátiles con Bacon', description: 'Süße Datteln mit knusprigem Speck', price: '6,90', details: 'Saftige Datteln gefüllt mit Mandeln, umwickelt mit knusprigem Bacon und im Ofen gebacken.' },
      { name: 'Albondigas', description: 'Spanische Hackfleischbällchen in Tomatensoße', price: '6,90', details: 'Hausgemachte Fleischbällchen nach traditionellem Rezept in würziger Tomatensoße mit frischen Kräutern.' },
      { name: 'Pincho de Cerdo', description: 'Schweinefleisch-Spieß gegrillt', price: '7,90', details: 'Marinierte Schweinefleischstücke am Spieß mit Paprika und Zwiebeln, serviert mit Aioli.' },
      { name: 'Pincho de Cordero', description: 'Lammfleisch-Spieß mit Kräutern', price: '8,90', details: 'Zarte Lammfleischstücke am Spieß mit mediterranen Kräutern und Knoblauch mariniert.' },
      { name: 'Chuletas de Cordero', description: 'Gegrillte Lammkoteletts', price: '9,90', details: 'Saftige Lammkoteletts vom Grill mit Rosmarin und Thymian, serviert mit Knoblauchöl.' },
      { name: 'Rollitos Serrano mit Feige', description: 'Serrano-Schinken-Röllchen mit süßer Feige', price: '9,90', details: 'Hauchdünner Serrano-Schinken gefüllt mit süßen Feigen und Ziegenkäse.' },
      { name: 'Ziegenkäse mit Bacon', description: 'Cremiger Ziegenkäse mit knusprigem Speck', price: '7,90', details: 'Warmer Ziegenkäse in knusprigem Bacon eingewickelt, mit Honig und Pinienkernen.' },
      { name: 'Chorizo al Diablo', description: 'Scharfe Chorizo in Teufelssauce', price: '7,90', details: 'Gegrillte Chorizo in pikanter Sauce mit Rotwein und scharfen Chilischoten.' },
      { name: 'Medaillons vom Schwein', description: 'Zarte Schweinefilet-Medaillons', price: '9,90', details: 'Rosa gebratene Schweinefilet-Medaillons mit Sherrysoße und karamellisierten Zwiebeln.' },
      { name: 'Champignons mit Käse', description: 'Überbackene Pilze mit geschmolzenem Käse', price: '8,90', details: 'Frische Champignons gefüllt mit Serrano-Schinken und Käse überbacken.' },
      { name: 'Schweinefilet mit Cherrytomaten', description: 'Saftiges Filet mit süßen Tomaten', price: '9,50', details: 'Gebratenes Schweinefilet mit geschmorten Cherrytomaten und Basilikum.' },
      { name: 'Schweinefilet in Sauce', description: 'Zartes Filet in aromatischer Sauce', price: '9,50', details: 'Schweinefilet in cremiger Pilz-Sahne-Sauce mit frischen Kräutern.' },
      { name: 'Chorizo a la Plancha', description: 'Gegrillte spanische Wurst', price: '7,90', details: 'Traditionelle spanische Chorizo vom Grill mit Paprika und Zwiebeln.' },
      { name: 'Lammfilet', description: 'Premium Lammfilet rosa gebraten', price: '9,90', details: 'Zartes Lammfilet rosa gebraten mit Rosmarin-Knoblauch-Öl und Thymianjus.' },
      { name: 'Spareribs mit BBQ', description: 'Zarte Rippchen mit BBQ-Sauce', price: '8,90', details: 'Geschmorte Spareribs in hausgemachter BBQ-Sauce mit spanischen Gewürzen.' },
      { name: 'Chicken Wings', description: 'Würzige Hähnchenflügel', price: '9,90', details: 'Knusprige Chicken Wings mariniert in pikanter Sauce mit Knoblauch und Kräutern.' }
    ],
    'tapas-pescado': [
      { name: 'Boquerones Fritos', description: 'Frittierte Sardellen', price: '7,50', details: 'Frisch frittierte Sardellen in knuspriger Panade mit Zitrone und hausgemachter Aioli.' },
      { name: 'Calamares a la Plancha', description: 'Gegrillte Tintenfischringe', price: '8,90', details: 'Zart gegrillte Tintenfischringe mit Knoblauch, Petersilie und Zitrone.' },
      { name: 'Calamares a la Romana', description: 'Panierte Tintenfischringe', price: '7,50', details: 'Knusprig panierte Tintenfischringe serviert mit Zitrone und Aioli.' },
      { name: 'Lachs mit Spinat', description: 'Frischer Lachs auf Spinatbett', price: '9,90', details: 'Gebratenes Lachsfilet auf cremigem Blattspinat mit Knoblauch und Pinienkernen.' },
      { name: 'Gambas a la Plancha', description: 'Gegrillte Garnelen', price: '9,90', details: 'Große Garnelen vom Grill mit Meersalz und Knoblauchöl.' },
      { name: 'Garnelen-Dattel-Spieß', description: 'Süß-salzige Kombination am Spieß', price: '9,90', details: 'Garnelen und süße Datteln am Spieß mit Speck umwickelt.' },
      { name: 'Gambas al Ajillo', description: 'Garnelen in Knoblauchöl', price: '9,90', glutenfree: true, details: 'In bestem andalusischem Olivenöl extra vergine gebratene Garnelen aus Huelva mit frischem Knoblauch aus Las Pedroñeras (Cuenca), scharfem Guindilla-Chili aus dem Baskenland und frischer Petersilie. Ein Klassiker aus den Marisquerías von Cádiz, traditionell in der Cazuela de Barro (Tonschale) serviert.' },
      { name: 'Muslitos de Mar', description: 'Gebackene Muscheln', price: '6,90', details: 'Gratinierte Miesmuscheln mit Knoblauch-Kräuter-Kruste.' },
      { name: 'Gegrillter Oktopus', description: 'Zarter Oktopus vom Grill', price: '9,90', details: 'Gegrillter Oktopus mit Paprikapulver, Olivenöl und Meersalz.' },
      { name: 'Jacobsmuscheln', description: 'Edle Jakobsmuscheln gegrillt', price: '9,90', details: 'Gegrillte Jakobsmuscheln mit Knoblauchbutter und Petersilie.' },
      { name: 'Gambas PIL PIL', description: 'Garnelen in würzigem Olivenöl', price: '9,90', details: 'Garnelen in scharfem Olivenöl mit Knoblauch und Cayennepfeffer.' },
      { name: 'Empanadas', description: 'Spanische Teigtaschen mit Füllung', price: '6,90', details: 'Hausgemachte Teigtaschen gefüllt mit Thunfisch und Tomaten.' },
      { name: 'Pfahlmuscheln', description: 'Frische Miesmuscheln in Sud', price: '8,90', details: 'Miesmuscheln in Weißwein-Knoblauch-Sud mit frischen Kräutern.' },
      { name: 'Pulpo al Ajillo', description: 'Oktopus in Knoblauchöl', price: '9,90', details: 'Zarter Oktopus in Knoblauchöl mit Paprikapulver und Petersilie.' },
      { name: 'Zanderfilet', description: 'Zartes Zanderfilet gebraten', price: '9,90', details: 'Gebratenes Zanderfilet mit Zitronenbutter und mediterranem Gemüse.' },
      { name: 'Tiger Garnelen', description: 'Große Tiger-Garnelen gegrillt', price: '9,90', details: 'Gegrillte Tiger-Garnelen mit Knoblauch-Limetten-Butter.' },
      { name: 'Brocheta de Gambas', description: 'Garnelen-Spieß mit Gemüse', price: '8,90', details: 'Garnelen-Spieß mit Paprika und Zwiebeln vom Grill.' },
      { name: 'Boqueron in Tempura', description: 'Sardellen im Tempura-Teig', price: '7,50', details: 'Sardellen im leichten Tempura-Teig mit Zitronen-Aioli.' },
      { name: 'Chipirones', description: 'Baby-Tintenfische gegrillt', price: '8,90', details: 'Gegrillte Baby-Tintenfische mit Knoblauch und Petersilie.' }
    ],
    'kroketten': [
      { name: 'Bacalao', description: 'Stockfisch-Kroketten', price: '5,90', details: 'Cremige Kroketten aus Stockfisch und Kartoffeln, traditionell zubereitet.' },
      { name: 'Käse', description: 'Cremige Käse-Kroketten', price: '5,90', details: 'Hausgemachte Kroketten mit einer Füllung aus spanischen Käsesorten.' },
      { name: 'Mandeln', description: 'Mandel-Kroketten mit feinem Aroma', price: '6,50', details: 'Süße Kroketten aus gemahlenen Mandeln mit Honig und Zimt.' },
      { name: 'Jamón', description: 'Schinken-Kroketten klassisch', price: '5,90', details: 'Traditionelle Kroketten mit feiner Serrano-Schinken-Füllung.' },
      { name: 'Kartoffel', description: 'Traditionelle Kartoffel-Kroketten', price: '5,50', details: 'Klassische Kartoffelkroketten mit Kräutern und Gewürzen.' }
    ],
    'pasta': [
      { name: 'Spaghetti Aglio e Olio', description: 'Klassisch mit Knoblauch und Olivenöl', price: '12,90', details: 'Al dente gekochte Spaghetti mit bestem Olivenöl, frischem Knoblauch und Peperoncini.' },
      { name: 'Spaghetti Bolognese', description: 'Mit hausgemachter Fleischsauce', price: '14,90', details: 'Traditionelle Bolognese-Sauce mit Rinderhack, langsam geschmort mit Rotwein und Kräutern.' },
      { name: 'Pasta Brokkoli Gorgonzola', description: 'Cremige Gorgonzola-Sauce mit Brokkoli', price: '14,90', details: 'Frischer Brokkoli in cremiger Gorgonzola-Sauce mit gerösteten Pinienkernen.' },
      { name: 'Pasta Verdura', description: 'Mit frischem Saisongemüse', price: '14,90', details: 'Mediterranes Gemüse der Saison mit Olivenöl und frischen Kräutern.' },
      { name: 'Pasta Garnelen', description: 'Mit frischen Garnelen und Knoblauch', price: '16,90', details: 'Saftige Garnelen in Knoblauch-Weißwein-Sauce mit Kirschtomaten und Basilikum.' }
    ],
    'pizza': [
      { name: 'Margherita', description: 'Tomaten, Mozzarella, Basilikum', price: '9,90', details: 'Klassische Pizza mit hausgemachter Tomatensauce, frischem Mozzarella und Basilikum.' },
      { name: 'Schinken', description: 'Mit spanischem Schinken', price: '12,90', details: 'Pizza mit Serrano-Schinken, Mozzarella und frischen Rucola.' },
      { name: 'Funghi', description: 'Mit frischen Champignons', price: '12,90', details: 'Pizza mit sautierten Champignons, Mozzarella und frischen Kräutern.' },
      { name: 'Tonno', description: 'Mit Thunfisch und Zwiebeln', price: '13,90', details: 'Pizza mit Thunfisch, roten Zwiebeln, Kapern und schwarzen Oliven.' },
      { name: 'Hawaii', description: 'Mit Schinken und Ananas', price: '13,90', details: 'Pizza mit gekochtem Schinken, frischer Ananas und extra Käse.' },
      { name: 'Verdura', description: 'Mit gegrilltem Gemüse', price: '13,90', details: 'Pizza mit verschiedenem Grillgemüse, Mozzarella und Basilikumpesto.' },
      { name: 'Salami', description: 'Mit würziger Salami', price: '12,90', details: 'Pizza mit italienischer Salami, Mozzarella und frischen Kräutern.' },
      { name: 'Garnelen', description: 'Mit frischen Garnelen', price: '15,90', details: 'Pizza mit Garnelen, Knoblauch, Cherrytomaten und Rucola.' },
      { name: 'Bolognese', description: 'Mit Hackfleischsauce', price: '13,90', details: 'Pizza mit hausgemachter Bolognese-Sauce und extra Käse.' },
      { name: "Jimmy's Special", description: 'Unsere Haus-Spezial-Pizza', price: '13,90', details: 'Geheimrezept des Hauses mit ausgewählten spanischen Zutaten.' }
    ],
    'snacks': [
      { name: 'Pommes', description: 'Goldgelbe Kartoffel-Pommes', price: '5,50', details: 'Knusprige Pommes frites mit hausgemachten Dips nach Wahl.' },
      { name: 'Chicken Nuggets', description: 'Knusprige Hähnchen-Nuggets', price: '8,90', details: 'Hausgemachte Chicken Nuggets aus frischem Hähnchenfilet mit verschiedenen Dips.' },
      { name: 'Chicken Wings', description: 'Würzige Hähnchenflügel', price: '9,90', details: 'Marinierte und knusprig gebratene Chicken Wings mit BBQ-Sauce.' },
      { name: 'Currywurst', description: 'Deutsche Currywurst klassisch', price: '10,90', details: 'Klassische Currywurst mit hausgemachter Sauce und Pommes frites.' }
    ],
    'dessert': [
      { name: 'Crema Catalana', description: 'Katalanische Crème brûlée', price: '5,50', details: 'Traditionelle spanische Crème brûlée mit karamellisierter Zuckerkruste.' },
      { name: 'Tarte de Santiago', description: 'Spanischer Mandelkuchen', price: '7,50', details: 'Klassischer spanischer Mandelkuchen nach Originalrezept aus Galizien.' },
      { name: 'Eis', description: 'Hausgemachtes Eis nach Wahl', price: '6,90', details: 'Verschiedene Sorten hausgemachtes Eis mit frischen Früchten.' },
      { name: 'Churros mit Schokolade', description: 'Spanisches Spritzgebäck mit warmer Schokolade', price: '6,90', details: 'Frisch zubereitete Churros mit heißer Schokoladensauce zum Dippen.' },
      { name: 'Schoko Soufflé', description: 'Warmes Schokoladen-Soufflé', price: '7,50', details: 'Warmes Schokoladen-Soufflé mit flüssigem Kern und Vanilleeis.' }
    ],
    'helados': [
      { name: 'Kokos', description: 'Eis im Fruchtschälchen - Kokos', price: '6,90', details: 'Cremiges Kokoseis serviert in einer echten Kokosnussschale mit Kokosflocken.' },
      { name: 'Zitrone', description: 'Eis im Fruchtschälchen - Zitrone', price: '6,90', details: 'Erfrischendes Zitronensorbet in einer ausgehöhlten Zitrone serviert.' },
      { name: 'Orange', description: 'Eis im Fruchtschälchen - Orange', price: '6,90', details: 'Fruchtiges Orangensorbet in einer halbierten Orange präsentiert.' },
      { name: 'Nuss', description: 'Eis im Fruchtschälchen - Nuss', price: '6,90', details: 'Nusseis mit karamellisierten Nüssen in einer Kokosschale serviert.' }
    ]
  };

  const categories = [
    { id: 'alle', name: 'Alle Kategorien' },
    { id: 'inicio', name: 'Inicio' },
    { id: 'salat', name: 'Salat' },
    { id: 'kleiner-salat', name: 'Kleiner Salat' },
    { id: 'tapa-paella', name: 'Tapa Paella' },
    { id: 'tapas-vegetarian', name: 'Tapas Vegetarian' },
    { id: 'tapas-pollo', name: 'Tapas de Pollo' },
    { id: 'tapas-carne', name: 'Tapas de Carne' },
    { id: 'tapas-pescado', name: 'Tapas de Pescado' },
    { id: 'kroketten', name: 'Kroketten' },
    { id: 'pasta', name: 'Pasta' },
    { id: 'pizza', name: 'Pizza' },
    { id: 'snacks', name: 'Snacks' },
    { id: 'dessert', name: 'Dessert' },
    { id: 'helados', name: 'Helados' }
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
    <div className="min-h-screen speisekarte-background" style={{position: 'relative', zIndex: 0}}>
      {/* Elegant Header Section with Background Image */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('https://images.pexels.com/photos/24706530/pexels-photo-24706530.jpeg')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              Speisekarte
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              Authentische spanische Küche - Bewegen Sie die Maus über Gerichte für Bildvorschau
            </p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-12" style={{position: 'relative', zIndex: 1}}>        
        {/* Category Filter Buttons - No Icons */}
        <div className="flex flex-wrap justify-center gap-3 mb-12">
          {categories.map((category) => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`menu-category px-6 py-3 rounded-lg transition-all duration-300 font-light tracking-wide text-sm ${
                selectedCategory === category.id
                  ? 'bg-warm-beige text-dark-brown shadow-lg'
                  : 'border border-warm-beige text-warm-beige hover:bg-warm-beige hover:text-dark-brown hover:shadow-lg'
              }`}
            >
              {category.name}
            </button>
          ))}
        </div>

        {/* Menu Items - Screenshot Style Two-Column Layout with Hover Info */}
        <div className="grid md:grid-cols-2 gap-6 max-w-7xl mx-auto" style={{position: 'relative', zIndex: 1}}>
          {getDisplayItems().map((item, index) => (
            <div key={index} className="menu-item rounded-lg p-6 hover:bg-medium-brown transition-all duration-300 relative group">
              <div className="flex justify-between items-start">
                {/* Dish name and description */}
                <div className="flex-1 pr-4">
                  <h3 className="text-xl font-serif text-warm-beige mb-2 tracking-wide">
                    {item.name}
                    {item.vegan && <span className="ml-2 text-green-400 text-sm">🌱</span>}
                    {item.vegetarian && <span className="ml-2 text-green-300 text-sm">🥬</span>}
                    {item.glutenfree && <span className="ml-2 text-yellow-400 text-sm">GF</span>}
                  </h3>
                  <p className="text-light-beige mb-2 font-light leading-relaxed text-sm">{item.description}</p>
                  <span className="text-xs text-warm-beige capitalize font-light tracking-wide opacity-75">
                    {categories.find(c => c.id === item.category)?.name}
                  </span>
                </div>
                
                {/* Price - Right aligned like in screenshot */}
                <div className="text-2xl font-serif text-warm-beige tracking-wide flex-shrink-0">
                  {item.price} €
                </div>
              </div>
              
              {/* Enhanced Hover Details Popup - Only text without images - ALWAYS ON TOP */}
              <div className="menu-image-tooltip">
                <div className="tooltip-content bg-dark-brown border-2 border-warm-beige rounded-lg p-6 max-w-md">
                  <h4 className="text-lg font-serif text-warm-beige mb-3">{item.name}</h4>
                  <p className="text-light-beige text-sm mb-3 leading-relaxed">{item.details}</p>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-warm-beige opacity-75">
                      {categories.find(c => c.id === item.category)?.name}
                    </span>
                    <span className="text-xl font-serif text-warm-beige">{item.price} €</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        {/* Menu Footer */}
        <div className="text-center mt-16 p-8 bg-dark-brown rounded-lg border border-warm-brown">
          <h3 className="text-2xl font-serif text-warm-beige mb-4">Allergien und Unverträglichkeiten</h3>
          <p className="text-light-beige font-light leading-relaxed max-w-3xl mx-auto mb-4">
            Bitte informieren Sie uns über eventuelle Allergien oder Unverträglichkeiten. 
            Unsere Küche berücksichtigt gerne Ihre individuellen Bedürfnisse.
          </p>
          <div className="flex flex-wrap justify-center gap-6 text-sm">
            <span className="flex items-center text-light-beige">
              <span className="text-green-400 text-lg mr-2">🌱</span>
              Vegan
            </span>
            <span className="flex items-center text-light-beige">
              <span className="text-green-300 text-lg mr-2">🥬</span>
              Vegetarisch
            </span>
            <span className="flex items-center text-light-beige">
              <span className="text-yellow-400 text-sm font-bold mr-2">GF</span>
              Glutenfrei
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

// Enhanced Locations Page Component
const Standorte = () => {
  const [locationsContent, setLocationsContent] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load locations content from backend
  useEffect(() => {
    const loadLocationsContent = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/locations`);
        if (response.ok) {
          const data = await response.json();
          setLocationsContent(data);
        }
      } catch (error) {
        console.error('Error loading locations content:', error);
      } finally {
        setLoading(false);
      }
    };
    loadLocationsContent();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-warm-beige"></div>
      </div>
    );
  }

  // Fallback to default content if backend is unavailable
  const pageData = locationsContent || {
    page_title: "Unsere Standorte",
    page_description: "Besuchen Sie uns an der malerischen Ostseeküste",
    locations: [
      {
        name: "Jimmy's Tapas Bar Kühlungsborn",
        address: "Strandstraße 1, 18225 Kühlungsborn",
        phone: "+49 38293 12345",
        email: "kuehlungsborn@jimmys-tapasbar.de",
        opening_hours: {
          "Montag": "16:00 - 23:00",
          "Dienstag": "16:00 - 23:00",
          "Mittwoch": "16:00 - 23:00",
          "Donnerstag": "16:00 - 23:00",
          "Freitag": "16:00 - 24:00",
          "Samstag": "12:00 - 24:00",
          "Sonntag": "12:00 - 23:00"
        },
        description: "Unser Hauptstandort direkt am Strand von Kühlungsborn",
        image_url: "https://images.unsplash.com/photo-1571197119738-26123cb0d22f"
      },
      {
        name: "Jimmy's Tapas Bar Warnemünde",
        address: "Am Strom 2, 18119 Warnemünde",
        phone: "+49 381 987654",
        email: "warnemuende@jimmys-tapasbar.de",
        opening_hours: {
          "Montag": "17:00 - 23:00",
          "Dienstag": "17:00 - 23:00",
          "Mittwoch": "17:00 - 23:00",
          "Donnerstag": "17:00 - 23:00",
          "Freitag": "17:00 - 24:00",
          "Samstag": "12:00 - 24:00",
          "Sonntag": "12:00 - 23:00"
        },
        description: "Gemütlich am alten Strom mit Blick auf die Warnow",
        image_url: "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d"
      }
    ]
  };

  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Elegant Header Section with Background */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('https://images.pexels.com/photos/26626726/pexels-photo-26626726.jpeg')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              {pageData.page_title}
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              {pageData.page_description}
            </p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-16">
        <div className="grid lg:grid-cols-2 gap-16 max-w-7xl mx-auto">
          {pageData.locations.map((location, index) => (
            <div key={index} className="bg-dark-brown rounded-xl border border-warm-brown overflow-hidden shadow-2xl">
              <div className="relative">
                <img 
                  src={location.image_url} 
                  alt={location.name} 
                  className="w-full h-72 object-cover"
                />
                {index === 0 && (
                  <div className="absolute top-4 left-4 bg-warm-beige text-dark-brown px-4 py-2 rounded-lg">
                    <span className="font-serif font-semibold">Hauptstandort</span>
                  </div>
                )}
              </div>
              <div className="p-8">
                <h2 className="text-3xl font-serif text-warm-beige mb-6 tracking-wide">
                  {location.name}
                </h2>
                <div className="space-y-6 text-light-beige">
                  <div className="flex items-start space-x-4">
                    <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                      <span className="text-xl text-dark-brown">📍</span>
                    </div>
                    <div>
                      <h3 className="font-semibold text-warm-beige mb-1">Adresse</h3>
                      <p className="font-light text-lg">{location.address}</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-4">
                    <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                      <span className="text-xl text-dark-brown">🕒</span>
                    </div>
                    <div>
                      <h3 className="font-semibold text-warm-beige mb-1">Öffnungszeiten</h3>
                      {Object.entries(location.opening_hours).map(([day, hours]) => (
                        <p key={day} className="font-light text-sm">
                          {day}: {hours}
                        </p>
                      ))}
                    </div>
                  </div>
                  <div className="flex items-start space-x-4">
                    <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                      <span className="text-xl text-dark-brown">📞</span>
                    </div>
                    <div>
                      <h3 className="font-semibold text-warm-beige mb-1">Kontakt</h3>
                      <p className="font-light">{location.phone}</p>
                      <p className="font-light text-sm text-warm-beige">{location.email}</p>
                    </div>
                  </div>
                  {location.description && (
                    <div className="mt-4 p-4 bg-medium-brown rounded-lg border border-warm-brown">
                      <p className="font-light text-warm-beige">{location.description}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// About Us Page Component
const UeberUns = () => {
  const [aboutContent, setAboutContent] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load about content from backend
  useEffect(() => {
    const loadAboutContent = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/about`);
        if (response.ok) {
          const data = await response.json();
          setAboutContent(data);
        }
      } catch (error) {
        console.error('Error loading about content:', error);
      } finally {
        setLoading(false);
      }
    };
    loadAboutContent();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-warm-beige"></div>
      </div>
    );
  }

  // Fallback to default content if backend is unavailable
  const pageData = aboutContent || {
    page_title: "Über uns",
    hero_title: "Unsere Geschichte",
    hero_description: "Entdecken Sie die Leidenschaft hinter Jimmy's Tapas Bar",
    story_title: "Unsere Leidenschaft",
    story_content: "Seit der Gründung steht Jimmy's Tapas Bar für authentische mediterrane Küche an der deutschen Ostseeküste...",
    story_image: "https://images.unsplash.com/photo-1571197119738-26123cb0d22f",
    team_title: "Unser Team",
    team_members: [
      {
        name: "Jimmy Rodriguez",
        position: "Inhaber & Küchenchef",
        description: "Jimmy bringt über 20 Jahre Erfahrung in der mediterranen Küche mit",
        image_url: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d"
      }
    ],
    values_title: "Unsere Werte",
    values: [
      "Authentische mediterrane Küche",
      "Frische, regionale Zutaten",
      "Familiäre Atmosphäre",
      "Leidenschaft für Qualität",
      "Gastfreundschaft"
    ]
  };

  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Hero Section */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('${pageData.story_image}')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              {pageData.page_title}
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              {pageData.hero_description}
            </p>
          </div>
        </div>
      </div>

      {/* Story Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl font-serif text-warm-beige mb-8 text-center tracking-wide">
            {pageData.story_title}
          </h2>
          <div className="text-light-beige font-light text-lg leading-relaxed space-y-4">
            {pageData.story_content.split('\n').map((paragraph, index) => (
              paragraph.trim() && (
                <p key={index} className="mb-4">{paragraph.trim()}</p>
              )
            ))}
          </div>
        </div>
      </div>

      {/* Team Section */}
      {pageData.team_members && pageData.team_members.length > 0 && (
        <div className="py-16 bg-medium-brown">
          <div className="container mx-auto px-4">
            <h2 className="text-4xl font-serif text-warm-beige mb-12 text-center tracking-wide">
              {pageData.team_title}
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
              {pageData.team_members.map((member, index) => (
                <div key={index} className="bg-dark-brown rounded-lg border border-warm-brown overflow-hidden shadow-lg">
                  {member.image_url && (
                    <img 
                      src={member.image_url} 
                      alt={member.name} 
                      className="w-full h-64 object-cover"
                    />
                  )}
                  <div className="p-6">
                    <h3 className="text-xl font-serif text-warm-beige mb-2">{member.name}</h3>
                    <p className="text-orange-400 font-medium mb-3">{member.position}</p>
                    <p className="text-light-beige font-light text-sm">{member.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Values Section */}
      {pageData.values && pageData.values.length > 0 && (
        <div className="py-16">
          <div className="container mx-auto px-4">
            <h2 className="text-4xl font-serif text-warm-beige mb-12 text-center tracking-wide">
              {pageData.values_title}
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-4xl mx-auto">
              {pageData.values.map((value, index) => (
                <div key={index} className="bg-dark-brown rounded-lg border border-warm-brown p-6 text-center">
                  <p className="text-warm-beige font-light text-lg">{value}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// About Us Page Component
const UeberUns = () => {
  const [aboutContent, setAboutContent] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load about content from backend
  useEffect(() => {
    const loadAboutContent = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/about`);
        if (response.ok) {
          const data = await response.json();
          setAboutContent(data);
        }
      } catch (error) {
        console.error('Error loading about content:', error);
      } finally {
        setLoading(false);
      }
    };
    loadAboutContent();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-warm-beige"></div>
      </div>
    );
  }

  // Fallback to default content if backend is unavailable
  const pageData = aboutContent || {
    page_title: "Über uns",
    hero_title: "Unsere Geschichte",
    hero_description: "Entdecken Sie die Leidenschaft hinter Jimmy's Tapas Bar",
    story_title: "Unsere Leidenschaft",
    story_content: "Seit der Gründung steht Jimmy's Tapas Bar für authentische mediterrane Küche an der deutschen Ostseeküste...",
    story_image: "https://images.unsplash.com/photo-1571197119738-26123cb0d22f",
    team_title: "Unser Team",
    team_members: [
      {
        name: "Jimmy Rodriguez",
        position: "Inhaber & Küchenchef",
        description: "Jimmy bringt über 20 Jahre Erfahrung in der mediterranen Küche mit",
        image_url: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d"
      }
    ],
    values_title: "Unsere Werte",
    values: [
      "Authentische mediterrane Küche",
      "Frische, regionale Zutaten",
      "Familiäre Atmosphäre",
      "Leidenschaft für Qualität",
      "Gastfreundschaft"
    ]
  };

  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Hero Section */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('${pageData.story_image}')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              {pageData.page_title}
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              {pageData.hero_description}
            </p>
          </div>
        </div>
      </div>

      {/* Story Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl font-serif text-warm-beige mb-8 text-center tracking-wide">
            {pageData.story_title}
          </h2>
          <div className="text-light-beige font-light text-lg leading-relaxed space-y-4">
            {pageData.story_content.split('\n').map((paragraph, index) => (
              paragraph.trim() && (
                <p key={index} className="mb-4">{paragraph.trim()}</p>
              )
            ))}
          </div>
        </div>
      </div>

      {/* Team Section */}
      {pageData.team_members && pageData.team_members.length > 0 && (
        <div className="py-16 bg-medium-brown">
          <div className="container mx-auto px-4">
            <h2 className="text-4xl font-serif text-warm-beige mb-12 text-center tracking-wide">
              {pageData.team_title}
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
              {pageData.team_members.map((member, index) => (
                <div key={index} className="bg-dark-brown rounded-lg border border-warm-brown overflow-hidden shadow-lg">
                  {member.image_url && (
                    <img 
                      src={member.image_url} 
                      alt={member.name} 
                      className="w-full h-64 object-cover"
                    />
                  )}
                  <div className="p-6">
                    <h3 className="text-xl font-serif text-warm-beige mb-2">{member.name}</h3>
                    <p className="text-orange-400 font-medium mb-3">{member.position}</p>
                    <p className="text-light-beige font-light text-sm">{member.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Values Section */}
      {pageData.values && pageData.values.length > 0 && (
        <div className="py-16">
          <div className="container mx-auto px-4">
            <h2 className="text-4xl font-serif text-warm-beige mb-12 text-center tracking-wide">
              {pageData.values_title}
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-4xl mx-auto">
              {pageData.values.map((value, index) => (
                <div key={index} className="bg-dark-brown rounded-lg border border-warm-brown p-6 text-center">
                  <p className="text-warm-beige font-light text-lg">{value}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
                  href="https://www.google.com/maps/dir/?api=1&destination=Südstrand+54,+23755+Großenbrode,+Germany"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full bg-warm-beige hover:bg-light-beige text-dark-brown px-6 py-3 rounded-lg font-medium transition-colors inline-block text-center"
                >
                  Route planen
                </a>
              </div>
            </div>
          </div>
        </div>

        {/* Additional Information Section */}
        <div className="mt-16 bg-dark-brown rounded-xl border border-warm-brown p-8">
          <h3 className="text-3xl font-serif text-warm-beige mb-8 text-center tracking-wide">
            Warum Jimmy's Tapas Bar?
          </h3>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-24 h-24 bg-cover bg-center rounded-lg mx-auto mb-4 border-2 border-warm-beige" 
                   style={{backgroundImage: `url('https://images.pexels.com/photos/16715741/pexels-photo-16715741.jpeg')`}}>
              </div>
              <h4 className="text-xl font-serif text-warm-beige mb-2">Authentische Atmosphäre</h4>
              <p className="text-light-beige font-light text-sm">
                Erleben Sie echtes spanisches Flair in gemütlicher Atmosphäre direkt an der Ostsee.
              </p>
            </div>
            <div className="text-center">
              <div className="w-24 h-24 bg-cover bg-center rounded-lg mx-auto mb-4 border-2 border-warm-beige" 
                   style={{backgroundImage: `url('https://images.pexels.com/photos/9570408/pexels-photo-9570408.jpeg')`}}>
              </div>
              <h4 className="text-xl font-serif text-warm-beige mb-2">Traditionelle Küche</h4>
              <p className="text-light-beige font-light text-sm">
                Frisch zubereitete Paella und Tapas nach original spanischen Familienrezepten.
              </p>
            </div>
            <div className="text-center">
              <div className="w-24 h-24 bg-cover bg-center rounded-lg mx-auto mb-4 border-2 border-warm-beige" 
                   style={{backgroundImage: `url('https://images.pexels.com/photos/8696561/pexels-photo-8696561.jpeg')`}}>
              </div>
              <h4 className="text-xl font-serif text-warm-beige mb-2">Spanisches Lebensgefühl</h4>
              <p className="text-light-beige font-light text-sm">
                Genießen Sie entspannte Abende mit spanischen Weinen und der besten Tapas-Auswahl.
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
      <span key={i} className={`text-2xl ${i < rating ? 'text-yellow-400' : 'text-warm-brown'}`}>
        ★
      </span>
    ));
  };

  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Elegant Header Section with Background */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('https://images.pexels.com/photos/26626726/pexels-photo-26626726.jpeg')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              Bewertungen & Feedback
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              Was unsere Gäste über uns sagen
            </p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-16">
        
        <div className="grid lg:grid-cols-2 gap-12 max-w-7xl mx-auto">
          {/* Public Reviews */}
          <div>
            <h2 className="text-3xl font-serif text-warm-beige mb-8 tracking-wide">
              Kundenbewertungen
            </h2>
            <div className="space-y-8">
              {reviews.map((review, index) => (
                <div key={index} className="bg-dark-brown rounded-lg border border-warm-brown p-8">
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="font-light text-warm-beige text-lg tracking-wide">{review.name}</h3>
                    <span className="text-sm text-light-beige font-light">{review.date}</span>
                  </div>
                  <div className="flex mb-4">
                    {renderStars(review.rating)}
                  </div>
                  <p className="text-light-beige font-light leading-relaxed">{review.comment}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Feedback Form */}
          <div>
            <h2 className="text-3xl font-serif text-warm-beige mb-8 tracking-wide">
              Ihr Feedback
            </h2>
            <div className="bg-dark-brown rounded-lg border border-warm-brown p-8">
              <p className="text-light-beige mb-6 text-sm font-light">
                Dieses Feedback wird intern gespeichert und nicht öffentlich angezeigt.
              </p>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="block text-warm-beige font-light mb-3 tracking-wide">Name</label>
                  <input
                    type="text"
                    value={feedback.name}
                    onChange={(e) => setFeedback({...feedback, name: e.target.value})}
                    className="w-full p-4 bg-medium-brown border border-warm-brown rounded-lg focus:ring-2 focus:ring-warm-beige focus:border-warm-beige text-warm-beige font-light"
                    required
                  />
                </div>
                <div>
                  <label className="block text-warm-beige font-light mb-3 tracking-wide">E-Mail</label>
                  <input
                    type="email"
                    value={feedback.email}
                    onChange={(e) => setFeedback({...feedback, email: e.target.value})}
                    className="w-full p-4 bg-medium-brown border border-warm-brown rounded-lg focus:ring-2 focus:ring-warm-beige focus:border-warm-beige text-warm-beige font-light"
                    required
                  />
                </div>
                <div>
                  <label className="block text-warm-beige font-light mb-3 tracking-wide">Bewertung</label>
                  <div className="flex space-x-2">
                    {[1,2,3,4,5].map(star => (
                      <button
                        key={star}
                        type="button"
                        onClick={() => setFeedback({...feedback, rating: star})}
                        className={`text-3xl ${star <= feedback.rating ? 'text-yellow-400' : 'text-warm-brown'} hover:text-yellow-400 transition-colors`}
                      >
                        ★
                      </button>
                    ))}
                  </div>
                </div>
                <div>
                  <label className="block text-warm-beige font-light mb-3 tracking-wide">Kommentar</label>
                  <textarea
                    value={feedback.comment}
                    onChange={(e) => setFeedback({...feedback, comment: e.target.value})}
                    className="w-full p-4 bg-medium-brown border border-warm-brown rounded-lg focus:ring-2 focus:ring-warm-beige focus:border-warm-beige h-32 text-warm-beige font-light"
                    required
                  />
                </div>
                <button
                  type="submit"
                  className="w-full bg-warm-beige hover:bg-light-beige text-dark-brown py-4 rounded-lg font-light transition-colors tracking-wide"
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

// Enhanced About Us Page Component
const UeberUns = () => {
  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Elegant Header Section with Background */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('https://images.pexels.com/photos/26626726/pexels-photo-26626726.jpeg')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              Über uns
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              Die Geschichte hinter Jimmy's Tapas Bar
            </p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-16">
        <div className="max-w-6xl mx-auto">
          <div className="bg-dark-brown rounded-xl border border-warm-brown p-12 mb-16 shadow-2xl">
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div>
                <img 
                  src="https://images.unsplash.com/photo-1665758564802-f611df512d8d" 
                  alt="Jimmy Rodríguez" 
                  className="w-full rounded-xl shadow-lg"
                />
              </div>
              <div>
                <h2 className="text-4xl font-serif text-warm-beige mb-6 tracking-wide">
                  Jimmy Rodríguez
                </h2>
                <div className="text-light-beige space-y-6 leading-relaxed font-light text-lg">
                  <p>
                    Seit über 15 Jahren bringe ich die authentischen Aromen Spaniens an die deutsche Ostseeküste. 
                    Meine Leidenschaft für die spanische Küche begann in den kleinen Tapas-Bars von Sevilla, 
                    wo ich die Geheimnisse traditioneller Rezepte erlernte.
                  </p>
                  <p>
                    In Jimmy's Tapas Bar verwenden wir nur die besten Zutaten - von handverlesenem Olivenöl 
                    aus Andalusien bis hin zu frischen Meeresfrüchten aus der Ostsee. Jedes Gericht wird mit 
                    Liebe und Respekt vor der spanischen Tradition zubereitet.
                  </p>
                  <p className="text-warm-beige font-medium">
                    "Essen ist nicht nur Nahrung - es ist Kultur, Tradition und Leidenschaft auf einem Teller."
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Values Section with Images */}
          <h3 className="text-4xl font-serif text-warm-beige mb-12 text-center tracking-wide">
            Unsere Werte
          </h3>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-dark-brown rounded-xl border border-warm-brown overflow-hidden shadow-lg">
              <img 
                src="https://images.unsplash.com/photo-1694685367640-05d6624e57f1" 
                alt="Qualität" 
                className="w-full h-48 object-cover"
              />
              <div className="p-8 text-center">
                <h4 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">Qualität</h4>
                <p className="text-light-beige font-light leading-relaxed">
                  Nur die besten Zutaten für authentische spanische Geschmackserlebnisse. 
                  Frische und Qualität stehen bei uns an erster Stelle.
                </p>
              </div>
            </div>
            <div className="bg-dark-brown rounded-xl border border-warm-brown overflow-hidden shadow-lg">
              <img 
                src="https://images.pexels.com/photos/19671352/pexels-photo-19671352.jpeg" 
                alt="Gastfreundschaft" 
                className="w-full h-48 object-cover"
              />
              <div className="p-8 text-center">
                <h4 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">Gastfreundschaft</h4>
                <p className="text-light-beige font-light leading-relaxed">
                  Herzliche Atmosphäre und persönlicher Service für jeden Gast. 
                  Bei uns sollen Sie sich wie zu Hause fühlen.
                </p>
              </div>
            </div>
            <div className="bg-dark-brown rounded-xl border border-warm-brown overflow-hidden shadow-lg">
              <img 
                src="https://images.unsplash.com/photo-1656423521731-9665583f100c" 
                alt="Lebensfreude" 
                className="w-full h-48 object-cover"
              />
              <div className="p-8 text-center">
                <h4 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">Lebensfreude</h4>
                <p className="text-light-beige font-light leading-relaxed">
                  Spanische Lebensart und Genuss in gemütlicher Atmosphäre. 
                  Erleben Sie das echte España-Gefühl an der Ostsee.
                </p>
              </div>
            </div>
          </div>

          {/* Team Section */}
          <div className="mt-16 bg-dark-brown rounded-xl border border-warm-brown p-12">
            <h3 className="text-4xl font-serif text-warm-beige mb-12 text-center tracking-wide">
              Unser Team
            </h3>
            <div className="grid md:grid-cols-2 gap-12">
              <div className="text-center">
                <div className="w-32 h-32 bg-medium-brown rounded-full mx-auto mb-6 flex items-center justify-center overflow-hidden">
                  <img 
                    src="https://images.unsplash.com/photo-1665758564802-f611df512d8d" 
                    alt="Küchenchef" 
                    className="w-full h-full object-cover"
                  />
                </div>
                <h4 className="text-2xl font-serif text-warm-beige mb-2">Carlos Mendez</h4>
                <p className="text-orange-400 mb-4">Küchenchef</p>
                <p className="text-light-beige font-light leading-relaxed">
                  Mit 20 Jahren Erfahrung in der spanischen Küche sorgt Carlos für die 
                  authentischen Geschmäcker in jedem unserer Gerichte.
                </p>
              </div>
              <div className="text-center">
                <div className="w-32 h-32 bg-medium-brown rounded-full mx-auto mb-6 flex items-center justify-center overflow-hidden">
                  <img 
                    src="https://images.unsplash.com/photo-1665758564802-f611df512d8d" 
                    alt="Service Manager" 
                    className="w-full h-full object-cover"
                  />
                </div>
                <h4 className="text-2xl font-serif text-warm-beige mb-2">Maria Santos</h4>
                <p className="text-orange-400 mb-4">Service Manager</p>
                <p className="text-light-beige font-light leading-relaxed">
                  Maria sorgt dafür, dass sich jeder Gast bei uns willkommen fühlt und 
                  einen unvergesslichen Abend erlebt.
                </p>
              </div>
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
    <div className="min-h-screen bg-dark-brown">
      {/* Elegant Header Section with Background */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('https://images.pexels.com/photos/26626726/pexels-photo-26626726.jpeg')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              Kontakt
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              Wir freuen uns auf Ihre Nachricht
            </p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-16">
        
        <div className="grid lg:grid-cols-2 gap-12 max-w-7xl mx-auto">
          {/* Contact Information */}
          <div>
            <h2 className="text-3xl font-serif text-warm-beige mb-8 tracking-wide">
              Kontaktinformationen
            </h2>
            
            <div className="bg-dark-brown rounded-lg border border-warm-brown p-8 mb-8">
              <h3 className="text-2xl font-serif text-warm-beige mb-6 tracking-wide">Neustadt in Holstein</h3>
              <div className="space-y-3 text-light-beige">
                <p className="font-light">📍 Am Strande 21, 23730 Neustadt in Holstein</p>
                <p className="font-light">📞 +49 (0) 4561 123456</p>
                <p className="font-light">✉️ neustadt@jimmys-tapasbar.de</p>
              </div>
            </div>

            <div className="bg-dark-brown rounded-lg border border-warm-brown p-8 mb-8">
              <h3 className="text-2xl font-serif text-warm-beige mb-6 tracking-wide">Großenbrode</h3>
              <div className="space-y-3 text-light-beige">
                <p className="font-light">📍 Südstrand 54, 23755 Großenbrode</p>
                <p className="font-light">📞 +49 (0) 4561 789012</p>
                <p className="font-light">✉️ grossenbrode@jimmys-tapasbar.de</p>
              </div>
            </div>

            <div className="bg-dark-brown rounded-lg border border-warm-brown p-8">
              <h3 className="text-2xl font-serif text-warm-beige mb-6 tracking-wide">Allgemein</h3>
              <div className="space-y-3 text-light-beige">
                <p className="font-light">🌐 www.jimmys-tapasbar.de</p>
                <p className="font-light">✉️ info@jimmys-tapasbar.de</p>
                <p className="font-light">🕒 Täglich 12:00–22:00 Uhr (Sommersaison)</p>
              </div>
            </div>
          </div>

          {/* Contact Form */}
          <div>
            <h2 className="text-3xl font-serif text-warm-beige mb-8 tracking-wide">
              Nachricht senden
            </h2>
            <div className="bg-dark-brown rounded-lg border border-warm-brown p-8">
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="block text-warm-beige font-light mb-3 tracking-wide">Name *</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    className="w-full p-4 bg-medium-brown border border-warm-brown rounded-lg focus:ring-2 focus:ring-warm-beige focus:border-warm-beige text-warm-beige font-light"
                    required
                  />
                </div>
                <div>
                  <label className="block text-warm-beige font-light mb-3 tracking-wide">E-Mail *</label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    className="w-full p-4 bg-medium-brown border border-warm-brown rounded-lg focus:ring-2 focus:ring-warm-beige focus:border-warm-beige text-warm-beige font-light"
                    required
                  />
                </div>
                <div>
                  <label className="block text-warm-beige font-light mb-3 tracking-wide">Telefon</label>
                  <input
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => setFormData({...formData, phone: e.target.value})}
                    className="w-full p-4 bg-medium-brown border border-warm-brown rounded-lg focus:ring-2 focus:ring-warm-beige focus:border-warm-beige text-warm-beige font-light"
                  />
                </div>
                <div>
                  <label className="block text-warm-beige font-light mb-3 tracking-wide">Standort</label>
                  <select
                    value={formData.location}
                    onChange={(e) => setFormData({...formData, location: e.target.value})}
                    className="w-full p-4 bg-medium-brown border border-warm-brown rounded-lg focus:ring-2 focus:ring-warm-beige focus:border-warm-beige text-warm-beige font-light"
                  >
                    <option value="neustadt">Neustadt in Holstein</option>
                    <option value="grossenbrode">Großenbrode</option>
                    <option value="beide">Beide Standorte</option>
                  </select>
                </div>
                <div>
                  <label className="block text-warm-beige font-light mb-3 tracking-wide">Nachricht *</label>
                  <textarea
                    value={formData.message}
                    onChange={(e) => setFormData({...formData, message: e.target.value})}
                    className="w-full p-4 bg-medium-brown border border-warm-brown rounded-lg focus:ring-2 focus:ring-warm-beige focus:border-warm-beige h-32 text-warm-beige font-light"
                    required
                  />
                </div>
                <button
                  type="submit"
                  className="w-full bg-warm-beige hover:bg-light-beige text-dark-brown py-4 rounded-lg font-light transition-colors tracking-wide"
                >
                  Nachricht senden
                </button>
              </form>
              
              <div className="mt-8 pt-8 border-t border-warm-brown">
                <h4 className="font-light text-warm-beige mb-3 tracking-wide">Datenschutz</h4>
                <p className="text-sm text-light-beige font-light leading-relaxed">
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

// Impressum Page Component
const Impressum = () => {
  return (
    <div className="min-h-screen bg-dark-brown pt-24">
      <div className="container mx-auto px-4 py-12">
        <h1 className="text-5xl font-serif text-center text-warm-beige mb-16 tracking-wide">
          Impressum
        </h1>
        
        <div className="max-w-4xl mx-auto bg-dark-brown rounded-lg border border-warm-brown p-8">
          <div className="space-y-8 text-light-beige">
            <div>
              <h2 className="text-2xl font-serif text-warm-beige mb-4">Angaben gemäß § 5 TMG</h2>
              <div className="space-y-2 font-light">
                <p><strong>Jimmy's Tapas Bar</strong></p>
                <p>Inhaber: Jimmy Rodríguez</p>
                <p>Am Strande 21</p>
                <p>23730 Neustadt in Holstein</p>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-serif text-warm-beige mb-3">Kontakt</h3>
              <div className="space-y-2 font-light">
                <p>Telefon: +49 (0) 4561 123456</p>
                <p>E-Mail: info@jimmys-tapasbar.de</p>
                <p>Website: www.jimmys-tapasbar.de</p>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-serif text-warm-beige mb-3">Zweiter Standort</h3>
              <div className="space-y-2 font-light">
                <p>Jimmy's Tapas Bar Großenbrode</p>
                <p>Südstrand 54</p>
                <p>23755 Großenbrode</p>
                <p>Telefon: +49 (0) 4561 789012</p>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-serif text-warm-beige mb-3">Umsatzsteuer-ID</h3>
              <p className="font-light">Umsatzsteuer-Identifikationsnummer gemäß §27 a Umsatzsteuergesetz:<br />
              DE123456789 (Beispiel - bitte echte USt-IdNr. eintragen)</p>
            </div>

            <div>
              <h3 className="text-xl font-serif text-warm-beige mb-3">Verantwortlich für den Inhalt nach § 55 Abs. 2 RStV</h3>
              <div className="space-y-2 font-light">
                <p>Jimmy Rodríguez</p>
                <p>Am Strande 21</p>
                <p>23730 Neustadt in Holstein</p>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-serif text-warm-beige mb-3">Haftungsausschluss</h3>
              <div className="space-y-4 font-light">
                <div>
                  <h4 className="font-medium text-warm-beige mb-2">Haftung für Inhalte</h4>
                  <p>Als Diensteanbieter sind wir gemäß § 7 Abs.1 TMG für eigene Inhalte auf diesen Seiten nach den allgemeinen Gesetzen verantwortlich. Nach §§ 8 bis 10 TMG sind wir als Diensteanbieter jedoch nicht unter der Verpflichtung, übermittelte oder gespeicherte fremde Informationen zu überwachen oder nach Umständen zu forschen, die auf eine rechtswidrige Tätigkeit hinweisen.</p>
                </div>
                
                <div>
                  <h4 className="font-medium text-warm-beige mb-2">Haftung für Links</h4>
                  <p>Unser Angebot enthält Links zu externen Websites Dritter, auf deren Inhalte wir keinen Einfluss haben. Deshalb können wir für diese fremden Inhalte auch keine Gewähr übernehmen. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber der Seiten verantwortlich.</p>
                </div>
                
                <div>
                  <h4 className="font-medium text-warm-beige mb-2">Urheberrecht</h4>
                  <p>Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen dem deutschen Urheberrecht. Die Vervielfältigung, Bearbeitung, Verbreitung und jede Art der Verwertung außerhalb der Grenzen des Urheberrechtes bedürfen der schriftlichen Zustimmung des jeweiligen Autors bzw. Erstellers.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Datenschutz Page Component
const Datenschutz = () => {
  return (
    <div className="min-h-screen bg-dark-brown pt-24">
      <div className="container mx-auto px-4 py-12">
        <h1 className="text-5xl font-serif text-center text-warm-beige mb-16 tracking-wide">
          Datenschutzerklärung
        </h1>
        
        <div className="max-w-4xl mx-auto bg-dark-brown rounded-lg border border-warm-brown p-8">
          <div className="space-y-8 text-light-beige">
            <div>
              <h2 className="text-2xl font-serif text-warm-beige mb-4">1. Datenschutz auf einen Blick</h2>
              <div className="space-y-4 font-light">
                <div>
                  <h3 className="text-lg font-serif text-warm-beige mb-2">Allgemeine Hinweise</h3>
                  <p>Die folgenden Hinweise geben einen einfachen Überblick darüber, was mit Ihren personenbezogenen Daten passiert, wenn Sie diese Website besuchen. Personenbezogene Daten sind alle Daten, mit denen Sie persönlich identifiziert werden können.</p>
                </div>
                
                <div>
                  <h3 className="text-lg font-serif text-warm-beige mb-2">Datenerfassung auf dieser Website</h3>
                  <p><strong>Wer ist verantwortlich für die Datenerfassung auf dieser Website?</strong></p>
                  <p>Die Datenverarbeitung auf dieser Website erfolgt durch den Websitebetreiber. Dessen Kontaktdaten können Sie dem Impressum dieser Website entnehmen.</p>
                </div>
              </div>
            </div>

            <div>
              <h2 className="text-2xl font-serif text-warm-beige mb-4">2. Hosting und Content Delivery Networks (CDN)</h2>
              <div className="space-y-4 font-light">
                <p>Wir hosten die Inhalte unserer Website bei folgenden Anbietern:</p>
                <p>Diese Website wird extern gehostet. Die personenbezogenen Daten, die auf dieser Website erfasst werden, werden auf den Servern des Hosters gespeichert.</p>
              </div>
            </div>

            <div>
              <h2 className="text-2xl font-serif text-warm-beige mb-4">3. Allgemeine Hinweise und Pflichtinformationen</h2>
              <div className="space-y-4 font-light">
                <div>
                  <h3 className="text-lg font-serif text-warm-beige mb-2">Datenschutz</h3>
                  <p>Die Betreiber dieser Seiten nehmen den Schutz Ihrer persönlichen Daten sehr ernst. Wir behandeln Ihre personenbezogenen Daten vertraulich und entsprechend der gesetzlichen Datenschutzvorschriften sowie dieser Datenschutzerklärung.</p>
                </div>
                
                <div>
                  <h3 className="text-lg font-serif text-warm-beige mb-2">Hinweis zur verantwortlichen Stelle</h3>
                  <p>Die verantwortliche Stelle für die Datenverarbeitung auf dieser Website ist:</p>
                  <div className="ml-4 mt-2">
                    <p>Jimmy Rodríguez</p>
                    <p>Am Strande 21</p>
                    <p>23730 Neustadt in Holstein</p>
                    <p>Telefon: +49 (0) 4561 123456</p>
                    <p>E-Mail: info@jimmys-tapasbar.de</p>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <h2 className="text-2xl font-serif text-warm-beige mb-4">4. Datenerfassung auf dieser Website</h2>
              <div className="space-y-4 font-light">
                <div>
                  <h3 className="text-lg font-serif text-warm-beige mb-2">Cookies</h3>
                  <p>Unsere Internetseiten verwenden so genannte „Cookies". Cookies sind kleine Textdateien und richten auf Ihrem Endgerät keinen Schaden an. Sie werden entweder vorübergehend für die Dauer einer Sitzung (Session-Cookies) oder dauerhaft (dauerhafte Cookies) auf Ihrem Endgerät gespeichert.</p>
                </div>
                
                <div>
                  <h3 className="text-lg font-serif text-warm-beige mb-2">Kontaktformular</h3>
                  <p>Wenn Sie uns per Kontaktformular Anfragen zukommen lassen, werden Ihre Angaben aus dem Anfrageformular inklusive der von Ihnen dort angegebenen Kontaktdaten zwecks Bearbeitung der Anfrage und für den Fall von Anschlussfragen bei uns gespeichert.</p>
                </div>
              </div>
            </div>

            <div>
              <h2 className="text-2xl font-serif text-warm-beige mb-4">5. Ihre Rechte</h2>
              <div className="space-y-4 font-light">
                <p>Sie haben jederzeit das Recht unentgeltlich Auskunft über Herkunft, Empfänger und Zweck Ihrer gespeicherten personenbezogenen Daten zu erhalten. Sie haben außerdem ein Recht, die Berichtigung, Sperrung oder Löschung dieser Daten zu verlangen.</p>
                
                <p>Hierzu sowie zu weiteren Fragen zum Thema Datenschutz können Sie sich jederzeit unter der im Impressum angegebenen Adresse an uns wenden.</p>
                
                <p>Des Weiteren steht Ihnen ein Beschwerderecht bei der zuständigen Aufsichtsbehörde zu.</p>
              </div>
            </div>

            <div className="border-t border-warm-brown pt-6 mt-8">
              <p className="text-sm text-light-beige font-light">
                Stand dieser Datenschutzerklärung: März 2024<br />
                Quelle: Erstellt mit dem Datenschutz-Generator von eRecht24
              </p>
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
    <footer className="bg-dark-brown-solid text-light-beige py-12 border-t border-warm-brown">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-xl font-serif mb-4 tracking-wide text-warm-beige">Jimmy's Tapas Bar</h3>
            <p className="text-light-beige font-light">
              Spanische Genusskultur – Authentisch & Gemütlich
            </p>
          </div>
          <div>
            <h4 className="font-serif mb-4 tracking-wide text-warm-beige">Standorte</h4>
            <div className="space-y-2 text-light-beige font-light">
              <p>Neustadt in Holstein</p>
              <p>Großenbrode</p>
            </div>
          </div>
          <div>
            <h4 className="font-serif mb-4 tracking-wide text-warm-beige">Kontakt</h4>
            <div className="space-y-2 text-light-beige font-light">
              <p>info@jimmys-tapasbar.de</p>
              <p>+49 (0) 4561 123456</p>
            </div>
          </div>
        </div>
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

    window.addEventListener("scroll", toggleVisibility);

    return () => window.removeEventListener("scroll", toggleVisibility);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  };

  return (
    <div 
      className={`scroll-to-top ${isVisible ? "visible" : ""}`}
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
