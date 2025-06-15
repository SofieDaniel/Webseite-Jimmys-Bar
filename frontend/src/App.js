import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Link, useNavigate, useLocation } from "react-router-dom";

// Import Admin Sections
import { ContentSection, MenuSection } from './AdminSections';
import { ReviewsSection, ContactsSection, UsersSection } from './AdminSectionsExtended';
import { MediaSection, MaintenanceSection } from './AdminSectionsFinal';
import { HomepageContentSection, LocationsManagementSection, EnhancedMenuSection, AboutContentSection, ContactLegalSection } from './AdminSectionsCMS';
import { NewsletterSection } from './NewsletterSection';
import { NewsletterSection } from './NewsletterSection';
import { NewsletterSection } from './NewsletterSection';
import { NewsletterSection } from './NewsletterSection';

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
  const [activeSection, setActiveSection] = useState('homepage');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // API Base URL
  const API_BASE_URL = process.env.REACT_APP_BACKEND_URL ? `${process.env.REACT_APP_BACKEND_URL}/api` : 'http://localhost:8001/api';

  // Check for existing login on mount
  useEffect(() => {
    const savedToken = localStorage.getItem('adminToken');
    if (savedToken) {
      setToken(savedToken);
      verifyToken(savedToken);
    }
  }, []);

  // API Helper Functions
  const apiCall = async (endpoint, method = 'GET', data = null, includeAuth = true) => {
    const headers = {
      'Content-Type': 'application/json',
    };

    if (includeAuth && token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
      method,
      headers,
    };

    if (data) {
      config.body = JSON.stringify(data);
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
    return response;
  };

  // Authentication Functions
  const verifyToken = async (tokenToVerify) => {
    try {
      const response = await apiCall('/auth/me', 'GET', null, true);
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
        setIsLoggedIn(true);
      } else {
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

    try {
      const response = await apiCall('/auth/login', 'POST', loginForm, false);
      
      if (response.ok) {
        const data = await response.json();
        const newToken = data.access_token;
        setToken(newToken);
        localStorage.setItem('adminToken', newToken);
        
        // Get user info
        const userResponse = await fetch(`${API_BASE_URL}/auth/me`, {
          headers: { 'Authorization': `Bearer ${newToken}` }
        });
        const userData = await userResponse.json();
        setUser(userData);
        setIsLoggedIn(true);
        setSuccess('Erfolgreich angemeldet!');
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Anmeldung fehlgeschlagen');
      }
    } catch (error) {
      setError('Verbindungsfehler. Bitte versuchen Sie es erneut.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUser(null);
    setToken(null);
    localStorage.removeItem('adminToken');
    setActiveSection('dashboard');
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
            <h1 className="text-3xl font-bold text-white mb-2">Jimmy´s Webseiten CMS by Daniel Böttche</h1>
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
                <h1 className="text-xl font-bold text-gray-900">Jimmy´s Webseiten CMS by Daniel Böttche</h1>
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
                { id: 'homepage', name: 'Homepage CMS', icon: 'M3 7v10a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2 2z' },
                { id: 'locations', name: 'Standorte CMS', icon: 'M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z M15 11a3 3 0 11-6 0 3 3 0 016 0z' },
                { id: 'enhanced-menu', name: 'Speisekarten CMS', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
                { id: 'about-cms', name: 'Über uns CMS', icon: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z' },
                { id: 'contact-legal', name: 'Kontakt & Rechtliches', icon: 'M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z' },
                { id: 'reviews', name: 'Bewertungen', icon: 'M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z' },
                { id: 'contacts', name: 'Kontakte', icon: 'M3 8l7.89 7.89a2 2 0 002.83 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' },
                { id: 'users', name: 'Benutzer', icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z' },
                { id: 'media', name: 'Medien', icon: 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z' },
                { id: 'maintenance', name: 'Wartung', icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z' },
                { id: 'newsletter', name: 'Newsletter', icon: 'M3 8l7.89 7.89a2 2 0 002.83 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' }
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
          {activeSection === 'homepage' && <HomepageContentSection user={user} token={token} apiCall={apiCall} />}
          {activeSection === 'locations' && <LocationsManagementSection user={user} token={token} apiCall={apiCall} />}
          {activeSection === 'enhanced-menu' && <EnhancedMenuSection user={user} token={token} apiCall={apiCall} />}
          {activeSection === 'about-cms' && <AboutContentSection user={user} token={token} apiCall={apiCall} />}
          {activeSection === 'contact-legal' && <ContactLegalSection user={user} token={token} apiCall={apiCall} />}
          {activeSection === 'reviews' && <ReviewsSection user={user} token={token} apiCall={apiCall} />}
          {activeSection === 'contacts' && <ContactsSection user={user} token={token} apiCall={apiCall} />}
          {activeSection === 'users' && <UsersSection user={user} token={token} apiCall={apiCall} />}
          {activeSection === 'media' && <MediaSection user={user} token={token} apiCall={apiCall} />}
          {activeSection === 'maintenance' && <MaintenanceSection user={user} token={token} apiCall={apiCall} />}
          {activeSection === 'newsletter' && <NewsletterSection user={user} token={token} apiCall={apiCall} />}
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
          Hier ist eine Übersicht über Ihr Jimmy´s Webseiten CMS by Daniel Böttche Dashboard.
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
            { name: 'Newsletter senden', icon: 'M3 8l7.89 7.89a2 2 0 002.83 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z', color: 'purple' }
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

// Header Component (Simplified German-only)
const Header = () => {
  const location = useLocation();
  
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
            }`}>Startseite</Link>
            <Link to="/standorte" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/standorte') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>Standorte</Link>
            <Link to="/speisekarte" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/speisekarte') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>Speisekarte</Link>
            <Link to="/bewertungen" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/bewertungen') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>Bewertungen</Link>
            <Link to="/ueber-uns" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/ueber-uns') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>Über uns</Link>
            <Link to="/kontakt" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/kontakt') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>Kontakt</Link>
          </div>
        </nav>
      </div>
    </header>
  );
};

// Simplified Homepage Component (German-only)
const Home = () => {
  const navigate = useNavigate();
  
  // CMS Content State
  const [heroData, setHeroData] = useState(null);
  const [featuresData, setFeaturesData] = useState(null);
  const [galleryData, setGalleryData] = useState(null);
  const [lieferandoData, setLieferandoData] = useState(null);
  const [loading, setLoading] = useState(true);

  // API Base URL
  const API_BASE_URL = process.env.REACT_APP_BACKEND_URL ? `${process.env.REACT_APP_BACKEND_URL}/api` : 'http://localhost:8001/api';

  useEffect(() => {
    loadHomepageContent();
  }, []);

  const loadHomepageContent = async () => {
    setLoading(true);
    try {
      const [heroResponse, featuresResponse, galleryResponse, lieferandoResponse] = await Promise.all([
        fetch(`${API_BASE_URL}/cms/homepage/hero`),
        fetch(`${API_BASE_URL}/cms/homepage/features`),
        fetch(`${API_BASE_URL}/cms/homepage/food-gallery`),
        fetch(`${API_BASE_URL}/cms/homepage/lieferando`)
      ]);

      if (heroResponse.ok) {
        const heroData = await heroResponse.json();
        setHeroData(heroData);
      }

      if (featuresResponse.ok) {
        const featuresData = await featuresResponse.json();
        setFeaturesData(featuresData);
      }

      if (galleryResponse.ok) {
        const galleryData = await galleryResponse.json();
        setGalleryData(galleryData);
      }

      if (lieferandoResponse.ok) {
        const lieferandoData = await lieferandoResponse.json();
        setLieferandoData(lieferandoData);
      }
    } catch (error) {
      console.error('Error loading homepage content:', error);
    } finally {
      setLoading(false);
    }
  };

  // Helper function to get text (German only now)
  const getText = (textObj) => {
    if (!textObj) return '';
    if (typeof textObj === 'string') return textObj;
    return textObj.de || textObj.en || textObj.es || '';
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-dark-brown">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-warm-beige"></div>
      </div>
    );
  }
  
  return (
    <div className="min-h-screen">
      {/* Dynamic CMS Hero Section */}
      {heroData && (
        <section id="main-content" className="relative h-screen bg-cover bg-center hero-background" 
                 style={{backgroundImage: `url('${heroData.background_image || 'https://images.unsplash.com/photo-1656423521731-9665583f100c'}')`}}>
          <div className="absolute inset-0 bg-black bg-opacity-50"></div>
          <div className="relative z-10 flex items-center justify-center h-full text-center px-4" style={{paddingTop: '80px'}}>
            <div className="max-w-4xl">
              {/* Dynamic CMS Headlines */}
              <h1 className="hero-headline font-serif text-warm-beige mb-8 tracking-wide leading-tight drop-shadow-text" style={{fontSize: 'clamp(2.5rem, 8vw, 6rem)', lineHeight: '1.1', marginTop: '40px'}}>
                {getText(heroData.title)}<br />
                <span className="font-light opacity-90" style={{fontSize: 'clamp(1.8rem, 5vw, 4rem)'}}>{getText(heroData.subtitle)}</span>
              </h1>
              
              {/* Dynamic CMS Subtitle */}
              <p className="text-xl md:text-2xl text-warm-beige font-light mb-12 max-w-3xl mx-auto leading-relaxed opacity-95">
                {getText(heroData.description)}<br/>
                <span className="text-lg opacity-80">{getText(heroData.location_text)}</span>
              </p>
              
              {/* Dynamic CMS Buttons */}
              <div className="flex flex-col md:flex-row justify-center gap-6">
                <button 
                  onClick={() => navigate('/speisekarte')}
                  className="bg-warm-beige text-dark-brown hover:bg-light-beige px-10 py-4 rounded-lg text-lg font-medium transition-all duration-300 tracking-wide shadow-lg hover:shadow-xl"
                >
                  {getText(heroData.menu_button_text)}
                </button>
                <button 
                  onClick={() => navigate('/standorte')}
                  className="border-2 border-warm-beige text-warm-beige hover:bg-warm-beige hover:text-dark-brown px-10 py-4 rounded-lg text-lg font-medium transition-all duration-300 tracking-wide shadow-lg hover:shadow-xl"
                >
                  {getText(heroData.locations_button_text)}
                </button>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Dynamic CMS Features Section */}
      {featuresData && (
        <section className="py-24 bg-gradient-to-b from-dark-brown to-medium-brown">
          <div className="container mx-auto px-4">
            <div className="text-center mb-20">
              <h2 className="text-5xl font-serif text-warm-beige mb-8 tracking-wide">
                {getText(featuresData.section_title)}
              </h2>
              <p className="text-xl text-light-beige font-light leading-relaxed max-w-3xl mx-auto">
                {getText(featuresData.section_description)}
              </p>
            </div>
            
            {/* Dynamic CMS Feature Cards */}
            <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
              {featuresData.features?.map((feature, index) => (
                <div key={index} className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-all duration-300 border border-warm-brown shadow-lg">
                  <img 
                    src={feature.image_url} 
                    alt={getText(feature.image_alt || feature.title)} 
                    className="w-full h-48 object-cover"
                  />
                  <div className="p-8 text-center">
                    <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">
                      {getText(feature.title)}
                    </h3>
                    <p className="text-light-beige font-light leading-relaxed">
                      {getText(feature.description)}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Dynamic CMS Food Gallery Section */}
      {galleryData && (
        <section className="py-20 bg-medium-brown">
          <div className="container mx-auto px-4">
            <h2 className="text-4xl font-serif text-center text-warm-beige mb-16 tracking-wide">
              {getText(galleryData.section_title)}
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {galleryData.gallery_items?.map((item, index) => (
                <div 
                  key={index}
                  className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-warm-brown cursor-pointer"
                  onClick={() => {
                    navigate('/speisekarte');
                    // Set category after navigation
                    setTimeout(() => {
                      window.location.href = `/speisekarte${item.category_link}`;
                    }, 100);
                  }}
                >
                  <img src={item.image_url} alt={getText(item.name)} className="w-full h-48 object-cover" />
                  <div className="p-6">
                    <h3 className="font-serif text-warm-beige text-lg tracking-wide">
                      {getText(item.name)}
                    </h3>
                    <p className="text-light-beige text-sm font-light">
                      {getText(item.description)}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Dynamic CMS Lieferando Section */}
      {lieferandoData && (
        <section className="py-16 bg-gradient-to-r from-dark-brown to-medium-brown">
          <div className="container mx-auto px-4 text-center">
            <div className="max-w-4xl mx-auto">
              <h2 className="text-4xl font-serif text-warm-beige mb-8 tracking-wide">
                {getText(lieferandoData.title)}
              </h2>
              <p className="text-xl text-light-beige font-light mb-12 leading-relaxed">
                {getText(lieferandoData.description)}
              </p>
              <div className="bg-dark-brown rounded-lg p-8 border border-warm-brown shadow-lg">
                <div className="flex flex-col md:flex-row items-center justify-center gap-8">
                  <div className="text-center">
                    <div className="w-24 h-24 bg-cover bg-center rounded-lg mx-auto mb-4 border-2 border-warm-beige" 
                         style={{backgroundImage: `url('https://images.pexels.com/photos/6969962/pexels-photo-6969962.jpeg')`}}>
                    </div>
                    <h3 className="text-xl font-serif text-warm-beige mb-2">
                      {getText(lieferandoData.delivery_text)}
                    </h3>
                    <p className="text-light-beige text-sm">Frisch und warm zu Ihnen</p>
                  </div>
                  <div className="text-center">
                    <a 
                      href={lieferandoData.lieferando_url || "https://www.lieferando.de"} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="inline-block bg-orange-500 hover:bg-orange-600 text-white px-8 py-4 rounded-lg text-lg font-medium transition-all duration-300 tracking-wide shadow-lg hover:shadow-xl transform hover:scale-105"
                    >
                      {getText(lieferandoData.button_text)}
                    </a>
                    <p className="text-light-beige text-sm mt-2">
                      {getText(lieferandoData.availability_text)}
                    </p>
                  </div>
                  <div className="text-center">
                    <div className="w-24 h-24 bg-cover bg-center rounded-lg mx-auto mb-4 border-2 border-warm-beige" 
                         style={{backgroundImage: `url('https://images.pexels.com/photos/31748679/pexels-photo-31748679.jpeg')`}}>
                    </div>
                    <h3 className="text-xl font-serif text-warm-beige mb-2">
                      {getText(lieferandoData.authentic_text)}
                    </h3>
                    <p className="text-light-beige text-sm">Direkt vom Küchenchef</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      )}
    </div>
  );
};

// Newsletter Registration Component (for website footer)
const NewsletterRegistration = () => {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const API_BASE_URL = process.env.REACT_APP_BACKEND_URL ? `${process.env.REACT_APP_BACKEND_URL}/api` : 'http://localhost:8001/api';
      
      const response = await fetch(`${API_BASE_URL}/newsletter/subscribe`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });

      if (response.ok) {
        setMessage('Vielen Dank! Sie haben sich erfolgreich für unseren Newsletter angemeldet.');
        setEmail('');
      } else {
        setMessage('Fehler bei der Anmeldung. Bitte versuchen Sie es erneut.');
      }
    } catch (error) {
      setMessage('Verbindungsfehler. Bitte versuchen Sie es später erneut.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-dark-brown border border-warm-brown rounded-lg p-6">
      <h3 className="text-xl font-serif text-warm-beige mb-4">Newsletter</h3>
      <p className="text-light-beige text-sm mb-4">
        Bleiben Sie auf dem Laufenden über neue Gerichte, Events und Angebote!
      </p>
      
      <form onSubmit={handleSubmit} className="space-y-3">
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Ihre E-Mail-Adresse"
          className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige placeholder-light-beige focus:outline-none focus:ring-2 focus:ring-warm-beige"
          required
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-warm-beige text-dark-brown py-3 rounded font-medium hover:bg-light-beige transition-colors disabled:opacity-50"
        >
          {loading ? 'Anmelden...' : 'Anmelden'}
        </button>
      </form>
      
      {message && (
        <p className="mt-3 text-sm text-light-beige">{message}</p>
      )}
    </div>
  );
};

// Speisekarte Component (Simplified German-only)
const Speisekarte = () => {
  const [selectedCategory, setSelectedCategory] = useState('alle');
  
  // Get menu data from CMS or fallback to static data
  const [menuData, setMenuData] = useState(null);
  const [loading, setLoading] = useState(true);

  const API_BASE_URL = process.env.REACT_APP_BACKEND_URL ? `${process.env.REACT_APP_BACKEND_URL}/api` : 'http://localhost:8001/api';

  useEffect(() => {
    loadMenuData();
  }, []);

  const loadMenuData = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/menu/items`);
      if (response.ok) {
        const data = await response.json();
        setMenuData(data);
      }
    } catch (error) {
      console.error('Error loading menu data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Static fallback menu data (simplified structure)
  const staticMenuItems = {
    'inicio': [
      { name: 'Aioli', description: 'Hausgemachte Knoblauch-Mayonnaise', price: '3,50€', image: 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f' },
      { name: 'Oliven', description: 'Marinierte spanische Oliven', price: '3,90€', image: 'https://images.unsplash.com/photo-1714583357992-98f0ad946902' },
      { name: 'Spanischer Käseteller', description: 'Auswahl spanischer Käsesorten', price: '8,90€', image: 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d' },
    ],
    'tapas-vegetarian': [
      { name: 'Papas Bravas', description: 'Klassische spanische Kartoffeln mit scharfer Soße', price: '6,90€', vegan: true },
      { name: 'Pimientos de Padrón', description: 'Gebratene grüne Paprika', price: '6,90€', vegan: true },
      { name: 'Tortilla de Patata', description: 'Spanisches Kartoffel-Omelett', price: '6,90€', vegetarian: true },
    ],
    'tapas-pescado': [
      { name: 'Gambas al Ajillo', description: 'Garnelen in Knoblauchöl', price: '9,90€' },
      { name: 'Calamares a la Romana', description: 'Panierte Tintenfischringe', price: '7,50€' },
      { name: 'Boquerones Fritos', description: 'Frittierte Sardellen', price: '7,50€' },
    ]
  };

  const categories = [
    { id: 'alle', name: 'Alle Kategorien' },
    { id: 'inicio', name: 'Inicio' },
    { id: 'tapas-vegetarian', name: 'Tapas Vegetarisch' },
    { id: 'tapas-pescado', name: 'Tapas Fisch' },
    { id: 'tapas-carne', name: 'Tapas Fleisch' },
    { id: 'pasta', name: 'Pasta' },
    { id: 'dessert', name: 'Dessert' }
  ];

  const getFilteredItems = () => {
    if (selectedCategory === 'alle') {
      return Object.values(staticMenuItems).flat();
    }
    return staticMenuItems[selectedCategory] || [];
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-dark-brown">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-warm-beige"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark-brown pt-20">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-serif text-warm-beige mb-4">Speisekarte</h1>
          <p className="text-light-beige text-lg">Authentische spanische Küche</p>
        </div>

        {/* Category Filter */}
        <div className="flex flex-wrap justify-center gap-4 mb-12">
          {categories.map((category) => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`px-6 py-3 rounded-lg transition-all duration-300 ${
                selectedCategory === category.id
                  ? 'bg-warm-beige text-dark-brown'
                  : 'bg-medium-brown text-light-beige hover:bg-warm-brown'
              }`}
            >
              {category.name}
            </button>
          ))}
        </div>

        {/* Menu Items */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
          {getFilteredItems().map((item, index) => (
            <div key={index} className="bg-medium-brown rounded-lg overflow-hidden border border-warm-brown hover:border-warm-beige transition-all duration-300">
              {item.image && (
                <img src={item.image} alt={item.name} className="w-full h-48 object-cover" />
              )}
              <div className="p-6">
                <div className="flex justify-between items-start mb-3">
                  <h3 className="text-xl font-serif text-warm-beige">{item.name}</h3>
                  <span className="text-warm-beige font-semibold">{item.price}</span>
                </div>
                <p className="text-light-beige text-sm leading-relaxed">{item.description}</p>
                
                {/* Tags */}
                <div className="flex gap-2 mt-3">
                  {item.vegan && (
                    <span className="px-2 py-1 bg-green-600 text-white text-xs rounded">Vegan</span>
                  )}
                  {item.vegetarian && (
                    <span className="px-2 py-1 bg-green-500 text-white text-xs rounded">Vegetarisch</span>
                  )}
                  {item.glutenfree && (
                    <span className="px-2 py-1 bg-blue-500 text-white text-xs rounded">Glutenfrei</span>
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

// Footer Component with Newsletter
const Footer = () => {
  return (
    <footer className="bg-dark-brown border-t border-warm-brown py-16">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-8">
          {/* Restaurant Info */}
          <div>
            <h3 className="text-xl font-serif text-warm-beige mb-4">Jimmy's Tapas Bar</h3>
            <p className="text-light-beige text-sm leading-relaxed">
              Authentische spanische Küche an der deutschen Ostseeküste. 
              Erleben Sie echte spanische Gastfreundschaft.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-serif text-warm-beige mb-4">Schnelllinks</h4>
            <ul className="space-y-2 text-light-beige text-sm">
              <li><Link to="/standorte" className="hover:text-warm-beige transition-colors">Standorte</Link></li>
              <li><Link to="/speisekarte" className="hover:text-warm-beige transition-colors">Speisekarte</Link></li>
              <li><Link to="/bewertungen" className="hover:text-warm-beige transition-colors">Bewertungen</Link></li>
              <li><Link to="/kontakt" className="hover:text-warm-beige transition-colors">Kontakt</Link></li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="text-lg font-serif text-warm-beige mb-4">Kontakt</h4>
            <div className="space-y-2 text-light-beige text-sm">
              <p>📍 Warnemünde & Kühlungsborn</p>
              <p>📞 +49 381 123456</p>
              <p>✉️ info@jimmys-tapas.de</p>
            </div>
          </div>

          {/* Newsletter */}
          <div>
            <NewsletterRegistration />
          </div>
        </div>

        <div className="border-t border-warm-brown mt-12 pt-8 text-center">
          <p className="text-light-beige text-sm">
            © 2024 Jimmy's Tapas Bar. Alle Rechte vorbehalten.
          </p>
        </div>
      </div>
    </footer>
  );
};

// Layout Component that conditionally renders Header/Footer
const MainLayout = ({ children }) => {
  const location = useLocation();
  const isAdminRoute = location.pathname.startsWith('/admin');

  if (isAdminRoute) {
    return <>{children}</>;
  }

  return (
    <>
      <Header />
      {children}
      <Footer />
      <CookieBanner />
    </>
  );
};

// Placeholder Components for other pages
const Standorte = () => (
  <div className="min-h-screen bg-dark-brown pt-20 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-4xl font-serif text-warm-beige mb-4">Unsere Standorte</h1>
      <p className="text-light-beige">Standorte-Seite wird entwickelt...</p>
    </div>
  </div>
);

const Bewertungen = () => (
  <div className="min-h-screen bg-dark-brown pt-20 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-4xl font-serif text-warm-beige mb-4">Bewertungen</h1>
      <p className="text-light-beige">Bewertungen-Seite wird entwickelt...</p>
    </div>
  </div>
);

const UeberUns = () => (
  <div className="min-h-screen bg-dark-brown pt-20 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-4xl font-serif text-warm-beige mb-4">Über uns</h1>
      <p className="text-light-beige">Über uns-Seite wird entwickelt...</p>
    </div>
  </div>
);

const Kontakt = () => (
  <div className="min-h-screen bg-dark-brown pt-20 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-4xl font-serif text-warm-beige mb-4">Kontakt</h1>
      <p className="text-light-beige">Kontakt-Seite wird entwickelt...</p>
    </div>
  </div>
);

// Main App Component
const App = () => {
  return (
    <BrowserRouter>
      <div className="App">
        <MainLayout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/standorte" element={<Standorte />} />
            <Route path="/speisekarte" element={<Speisekarte />} />
            <Route path="/bewertungen" element={<Bewertungen />} />
            <Route path="/ueber-uns" element={<UeberUns />} />
            <Route path="/kontakt" element={<Kontakt />} />
            <Route path="/admin" element={<AdminPanel />} />
          </Routes>
        </MainLayout>
      </div>
    </BrowserRouter>
  );
};

export default App;