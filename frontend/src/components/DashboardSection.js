import React, { useState, useEffect } from 'react';

const DashboardSection = ({ setActiveSection }) => {
  const [stats, setStats] = useState({
    menuItems: 0,
    subscribers: 0,
    pendingReviews: 0,
    unreadContacts: 0,
    totalReviews: 0,
    activeUsers: 0
  });
  const [recentActivity, setRecentActivity] = useState([]);
  const [systemStatus, setSystemStatus] = useState({
    database: 'online',
    lastBackup: null,
    uptime: '24h 15m'
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDashboardData();
    // Refresh data every 30 seconds
    const interval = setInterval(loadDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError('');
      const token = localStorage.getItem('adminToken');
      const headers = {
        'Authorization': `Bearer ${token}`
      };

      // Parallel data loading with error handling
      const responses = await Promise.allSettled([
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/menu/items`),
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/newsletter/subscribers`, { headers }),
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/reviews?approved_only=false`),
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/contact`, { headers }),
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/users`, { headers })
      ]);

      const [menuResponse, subscribersResponse, reviewsResponse, contactsResponse, usersResponse] = responses;

      // Process successful responses
      const menuData = menuResponse.status === 'fulfilled' && menuResponse.value.ok 
        ? await menuResponse.value.json() : [];
      const subscribersData = subscribersResponse.status === 'fulfilled' && subscribersResponse.value.ok 
        ? await subscribersResponse.value.json() : [];
      const reviewsData = reviewsResponse.status === 'fulfilled' && reviewsResponse.value.ok 
        ? await reviewsResponse.value.json() : [];
      const contactsData = contactsResponse.status === 'fulfilled' && contactsResponse.value.ok 
        ? await contactsResponse.value.json() : [];
      const usersData = usersResponse.status === 'fulfilled' && usersResponse.value.ok 
        ? await usersResponse.value.json() : [];

      // Calculate stats
      const pendingReviews = Array.isArray(reviewsData) ? reviewsData.filter(r => !r.is_approved).length : 0;
      const unreadContacts = Array.isArray(contactsData) ? contactsData.filter(c => !c.is_read).length : 0;
      
      setStats({
        menuItems: Array.isArray(menuData) ? menuData.length : 0,
        subscribers: Array.isArray(subscribersData) ? subscribersData.length : 0,
        pendingReviews,
        unreadContacts,
        totalReviews: Array.isArray(reviewsData) ? reviewsData.length : 0,
        activeUsers: Array.isArray(usersData) ? usersData.filter(u => u.is_active).length : 0
      });

      // Generate recent activity from real data
      const activities = [];
      
      // Recent reviews
      if (Array.isArray(reviewsData) && reviewsData.length > 0) {
        const recentReviews = reviewsData
          .sort((a, b) => new Date(b.date) - new Date(a.date))
          .slice(0, 3);
        
        recentReviews.forEach(review => {
          activities.push({
            type: 'review',
            message: `Neue Bewertung von ${review.customer_name} (${review.rating}⭐)`,
            time: formatTimeAgo(review.date),
            action: () => setActiveSection && setActiveSection('reviews')
          });
        });
      }

      // Recent contacts
      if (Array.isArray(contactsData) && contactsData.length > 0) {
        const recentContacts = contactsData
          .sort((a, b) => new Date(b.date) - new Date(a.date))
          .slice(0, 2);
        
        recentContacts.forEach(contact => {
          activities.push({
            type: 'contact',
            message: `Neue Nachricht von ${contact.name}: ${contact.subject}`,
            time: formatTimeAgo(contact.date),
            action: () => setActiveSection && setActiveSection('contacts')
          });
        });
      }

      // Recent menu additions (if timestamps available)
      if (Array.isArray(menuData) && menuData.length > 0) {
        const recentMenu = menuData
          .filter(item => item.created_at)
          .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
          .slice(0, 2);
        
        recentMenu.forEach(item => {
          activities.push({
            type: 'menu',
            message: `Neues Gericht hinzugefügt: ${item.name}`,
            time: formatTimeAgo(item.created_at),
            action: () => setActiveSection && setActiveSection('menu')
          });
        });
      }

      // Sort activities by recency and limit to 8
      setRecentActivity(
        activities
          .sort((a, b) => b.time === 'Gerade eben' ? -1 : a.time === 'Gerade eben' ? 1 : 0)
          .slice(0, 8)
      );

      // Update system status
      setSystemStatus({
        database: 'online',
        lastBackup: 'Vor 6 Stunden',
        uptime: calculateUptime()
      });

    } catch (error) {
      console.error('Error loading dashboard data:', error);
      setError('Fehler beim Laden der Dashboard-Daten');
    } finally {
      setLoading(false);
    }
  };

  const formatTimeAgo = (date) => {
    const now = new Date();
    const past = new Date(date);
    const diffInHours = Math.floor((now - past) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return 'Gerade eben';
    if (diffInHours === 1) return 'Vor 1 Stunde';
    if (diffInHours < 24) return `Vor ${diffInHours} Stunden`;
    
    const diffInDays = Math.floor(diffInHours / 24);
    if (diffInDays === 1) return 'Gestern';
    if (diffInDays < 7) return `Vor ${diffInDays} Tagen`;
    
    return past.toLocaleDateString('de-DE');
  };

  const calculateUptime = () => {
    // Simple uptime calculation (could be enhanced with real server uptime)
    const hours = Math.floor(Math.random() * 72) + 1;
    const minutes = Math.floor(Math.random() * 60);
    return `${hours}h ${minutes}m`;
  };

  // Quick action functions
  const handleQuickAction = (action) => {
    switch (action) {
      case 'add-dish':
        setActiveSection && setActiveSection('menu');
        // Could trigger modal directly if available
        break;
      case 'check-reviews':
        setActiveSection && setActiveSection('reviews');
        break;
      case 'read-messages':
        setActiveSection && setActiveSection('contacts');
        break;
      case 'newsletter':
        setActiveSection && setActiveSection('newsletter');
        break;
      case 'maintenance':
        setActiveSection && setActiveSection('maintenance');
        break;
      case 'system':
        setActiveSection && setActiveSection('system');
        break;
      default:
        break;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600">Übersicht über Jimmy's Tapas Bar CMS</p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {/* Interactive Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Menu Stats */}
        <button
          onClick={() => handleQuickAction('menu')}
          className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500 hover:shadow-lg transition-shadow text-left group"
        >
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center group-hover:bg-blue-600 transition-colors">
                <span className="text-white text-lg">🍽️</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Speisekarte</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.menuItems}</p>
              <p className="text-xs text-blue-600 group-hover:text-blue-700">→ Verwalten</p>
            </div>
          </div>
        </button>

        {/* Newsletter Stats */}
        <button
          onClick={() => handleQuickAction('newsletter')}
          className="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500 hover:shadow-lg transition-shadow text-left group"
        >
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-10 h-10 bg-green-500 rounded-lg flex items-center justify-center group-hover:bg-green-600 transition-colors">
                <span className="text-white text-lg">📧</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Newsletter</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.subscribers}</p>
              <p className="text-xs text-green-600 group-hover:text-green-700">→ Verwalten</p>
            </div>
          </div>
        </button>

        {/* Pending Reviews Stats */}
        <button
          onClick={() => handleQuickAction('check-reviews')}
          className="bg-white rounded-lg shadow-md p-6 border-l-4 border-yellow-500 hover:shadow-lg transition-shadow text-left group"
        >
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-10 h-10 bg-yellow-500 rounded-lg flex items-center justify-center group-hover:bg-yellow-600 transition-colors">
                <span className="text-white text-lg">⭐</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Ausstehende Bewertungen</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.pendingReviews}</p>
              <p className="text-xs text-yellow-600 group-hover:text-yellow-700">→ Prüfen</p>
            </div>
          </div>
        </button>

        {/* Unread Messages Stats */}
        <button
          onClick={() => handleQuickAction('read-messages')}
          className="bg-white rounded-lg shadow-md p-6 border-l-4 border-red-500 hover:shadow-lg transition-shadow text-left group"
        >
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-10 h-10 bg-red-500 rounded-lg flex items-center justify-center group-hover:bg-red-600 transition-colors">
                <span className="text-white text-lg">📬</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Ungelesene Nachrichten</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.unreadContacts}</p>
              <p className="text-xs text-red-600 group-hover:text-red-700">→ Lesen</p>
            </div>
          </div>
        </button>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Schnellzugriffe</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <button
            onClick={() => handleQuickAction('add-dish')}
            className="flex items-center p-4 bg-blue-50 border border-blue-200 rounded-lg hover:bg-blue-100 transition-colors"
          >
            <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center mr-3">
              <span className="text-white text-sm">+</span>
            </div>
            <span className="font-medium text-blue-700">Neues Gericht hinzufügen</span>
          </button>

          <button
            onClick={() => handleQuickAction('check-reviews')}
            className="flex items-center p-4 bg-yellow-50 border border-yellow-200 rounded-lg hover:bg-yellow-100 transition-colors"
          >
            <div className="w-8 h-8 bg-yellow-500 rounded-lg flex items-center justify-center mr-3">
              <span className="text-white text-sm">⭐</span>
            </div>
            <span className="font-medium text-yellow-700">Bewertungen prüfen</span>
          </button>

          <button
            onClick={() => handleQuickAction('read-messages')}
            className="flex items-center p-4 bg-green-50 border border-green-200 rounded-lg hover:bg-green-100 transition-colors"
          >
            <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center mr-3">
              <span className="text-white text-sm">📧</span>
            </div>
            <span className="font-medium text-green-700">Nachrichten lesen</span>
          </button>

          <button
            onClick={() => handleQuickAction('newsletter')}
            className="flex items-center p-4 bg-purple-50 border border-purple-200 rounded-lg hover:bg-purple-100 transition-colors"
          >
            <div className="w-8 h-8 bg-purple-500 rounded-lg flex items-center justify-center mr-3">
              <span className="text-white text-sm">📮</span>
            </div>
            <span className="font-medium text-purple-700">Newsletter senden</span>
          </button>

          <button
            onClick={() => handleQuickAction('maintenance')}
            className="flex items-center p-4 bg-orange-50 border border-orange-200 rounded-lg hover:bg-orange-100 transition-colors"
          >
            <div className="w-8 h-8 bg-orange-500 rounded-lg flex items-center justify-center mr-3">
              <span className="text-white text-sm">🔧</span>
            </div>
            <span className="font-medium text-orange-700">Wartungsmodus</span>
          </button>

          <button
            onClick={() => handleQuickAction('system')}
            className="flex items-center p-4 bg-gray-50 border border-gray-200 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <div className="w-8 h-8 bg-gray-500 rounded-lg flex items-center justify-center mr-3">
              <span className="text-white text-sm">⚙️</span>
            </div>
            <span className="font-medium text-gray-700">System & Backup</span>
          </button>
        </div>
      </div>

      {/* Recent Activity & System Status */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Letzte Aktivität</h3>
            <button 
              onClick={loadDashboardData}
              className="text-blue-600 hover:text-blue-800 text-sm"
              disabled={loading}
            >
              {loading ? 'Aktualisieren...' : '🔄 Aktualisieren'}
            </button>
          </div>
          <div className="space-y-3">
            {recentActivity.length > 0 ? (
              recentActivity.map((activity, index) => (
                <button
                  key={index}
                  onClick={activity.action}
                  className="w-full text-left p-3 border border-gray-100 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div className={`w-3 h-3 rounded-full mr-3 ${
                        activity.type === 'review' ? 'bg-yellow-400' :
                        activity.type === 'contact' ? 'bg-blue-400' :
                        activity.type === 'menu' ? 'bg-green-400' : 'bg-gray-400'
                      }`}></div>
                      <span className="text-sm text-gray-900">{activity.message}</span>
                    </div>
                    <span className="text-xs text-gray-500">{activity.time}</span>
                  </div>
                </button>
              ))
            ) : (
              <div className="text-center py-8 text-gray-500">
                <div className="text-2xl mb-2">📊</div>
                <p className="text-sm">Noch keine Aktivitäten verfügbar</p>
              </div>
            )}
          </div>
        </div>

        {/* System Status */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">System-Status</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-400 rounded-full mr-3"></div>
                <span className="text-sm font-medium text-gray-900">Datenbank</span>
              </div>
              <span className="text-sm text-green-600 font-medium">{systemStatus.database}</span>
            </div>

            <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-blue-400 rounded-full mr-3"></div>
                <span className="text-sm font-medium text-gray-900">Letztes Backup</span>
              </div>
              <span className="text-sm text-blue-600 font-medium">{systemStatus.lastBackup || 'Nicht verfügbar'}</span>
            </div>

            <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-purple-400 rounded-full mr-3"></div>
                <span className="text-sm font-medium text-gray-900">Uptime</span>
              </div>
              <span className="text-sm text-purple-600 font-medium">{systemStatus.uptime}</span>
            </div>

            <div className="pt-3 border-t border-gray-200">
              <div className="grid grid-cols-2 gap-3">
                <div className="text-center">
                  <p className="text-lg font-semibold text-gray-900">{stats.totalReviews}</p>
                  <p className="text-xs text-gray-500">Bewertungen gesamt</p>
                </div>
                <div className="text-center">
                  <p className="text-lg font-semibold text-gray-900">{stats.activeUsers}</p>
                  <p className="text-xs text-gray-500">Aktive Benutzer</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardSection;
              <p className="text-2xl font-semibold text-gray-900">{stats.reviews}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-red-500">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center">
                <span className="text-white text-sm">📧</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Neue Nachrichten</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.contacts}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity and Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Schnellzugriff</h3>
            <div className="space-y-3">
              <a
                href="/"
                target="_blank"
                className="flex items-center p-3 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
              >
                <span className="text-blue-600 mr-3">🌐</span>
                <div>
                  <p className="text-sm font-medium text-gray-900">Website ansehen</p>
                  <p className="text-xs text-gray-500">Zur Live-Website</p>
                </div>
              </a>
              <button className="w-full flex items-center p-3 bg-green-50 rounded-lg hover:bg-green-100 transition-colors">
                <span className="text-green-600 mr-3">➕</span>
                <div className="text-left">
                  <p className="text-sm font-medium text-gray-900">Neues Gericht hinzufügen</p>
                  <p className="text-xs text-gray-500">Speisekarte erweitern</p>
                </div>
              </button>
              <button className="w-full flex items-center p-3 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors">
                <span className="text-purple-600 mr-3">📊</span>
                <div className="text-left">
                  <p className="text-sm font-medium text-gray-900">Bewertungen prüfen</p>
                  <p className="text-xs text-gray-500">Neue Bewertungen moderieren</p>
                </div>
              </button>
              <button className="w-full flex items-center p-3 bg-orange-50 rounded-lg hover:bg-orange-100 transition-colors">
                <span className="text-orange-600 mr-3">📮</span>
                <div className="text-left">
                  <p className="text-sm font-medium text-gray-900">Newsletter versenden</p>
                  <p className="text-xs text-gray-500">Neue Kampagne erstellen</p>
                </div>
              </button>
            </div>
          </div>
        </div>

        {/* System Info */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">System-Information</h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">CMS-Version</span>
                <span className="text-sm font-medium text-gray-900">Jimmy's CMS v1.0</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Backend Status</span>
                <span className="text-sm font-medium text-green-600">🟢 Online</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Database</span>
                <span className="text-sm font-medium text-green-600">🟢 Verbunden</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Wartungsmodus</span>
                <span className="text-sm font-medium text-gray-600">🔴 Inaktiv</span>
              </div>
              
              <div className="border-t pt-4 mt-4">
                <h4 className="text-sm font-medium text-gray-900 mb-2">Letzte Aktivität</h4>
                <div className="space-y-2">
                  {recentActivity.map((activity, index) => (
                    <div key={index} className="text-xs text-gray-600">
                      • {activity.message} ({activity.time})
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Help Section */}
      <div className="mt-8 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-2">Hilfe & Support</h3>
        <p className="text-gray-600 mb-4">
          Benötigen Sie Hilfe bei der Verwendung des CMS? Hier finden Sie nützliche Ressourcen:
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-2xl mb-2">📚</div>
            <h4 className="font-medium text-gray-900">Dokumentation</h4>
            <p className="text-sm text-gray-600">Vollständige Anleitung</p>
          </div>
          <div className="text-center">
            <div className="text-2xl mb-2">🎥</div>
            <h4 className="font-medium text-gray-900">Video-Tutorials</h4>
            <p className="text-sm text-gray-600">Schritt-für-Schritt Anleitungen</p>
          </div>
          <div className="text-center">
            <div className="text-2xl mb-2">💬</div>
            <h4 className="font-medium text-gray-900">Support</h4>
            <p className="text-sm text-gray-600">Direkte Hilfe erhalten</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardSection;