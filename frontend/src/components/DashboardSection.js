import React, { useState, useEffect } from 'react';

const DashboardSection = () => {
  const [stats, setStats] = useState({
    menuItems: 0,
    subscribers: 0,
    reviews: 0,
    contacts: 0
  });
  const [recentActivity, setRecentActivity] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const token = localStorage.getItem('adminToken');
      const headers = {
        'Authorization': `Bearer ${token}`
      };

      // Load stats
      const [menuResponse, subscribersResponse, reviewsResponse, contactsResponse] = await Promise.all([
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/menu/items`),
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/newsletter/subscribers`, { headers }),
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/reviews`, { headers }),
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/contact`, { headers })
      ]);

      const menuData = await menuResponse.json();
      const subscribersData = await subscribersResponse.json();
      const reviewsData = await reviewsResponse.json();
      const contactsData = await contactsResponse.json();

      setStats({
        menuItems: Array.isArray(menuData) ? menuData.length : 0,
        subscribers: Array.isArray(subscribersData) ? subscribersData.length : 0,
        reviews: Array.isArray(reviewsData) ? reviewsData.length : 0,
        contacts: Array.isArray(contactsData) ? contactsData.filter(c => !c.read).length : 0
      });

      // Recent activity
      setRecentActivity([
        { type: 'newsletter', message: `${stats.subscribers} Newsletter-Abonnenten`, time: 'Aktuell' },
        { type: 'reviews', message: `${stats.reviews} Bewertungen erhalten`, time: 'Gesamt' },
        { type: 'menu', message: `${stats.menuItems} Gerichte in der Speisekarte`, time: 'Aktuell' },
        { type: 'contacts', message: `${stats.contacts} ungelesene Nachrichten`, time: 'Aktuell' }
      ]);

    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
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
    <div>
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900">Dashboard</h2>
        <p className="text-gray-600 mt-2">Übersicht über Jimmy's Tapas Bar CMS</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                <span className="text-white text-sm">🍽️</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Speisekarte</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.menuItems}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-green-500">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                <span className="text-white text-sm">📮</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Newsletter</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.subscribers}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-yellow-500">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-yellow-500 rounded-full flex items-center justify-center">
                <span className="text-white text-sm">⭐</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Bewertungen</p>
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