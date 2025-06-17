import React, { useState, useEffect } from 'react';

const NewsletterSection = () => {
  const [activeTab, setActiveTab] = useState('subscribers');
  const [subscribers, setSubscribers] = useState([]);
  const [campaigns, setCampaigns] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [smtpConfig, setSmtpConfig] = useState({});
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  
  // Template Modal States
  const [showTemplateModal, setShowTemplateModal] = useState(false);
  const [editingTemplate, setEditingTemplate] = useState(null);
  const [templateForm, setTemplateForm] = useState({
    name: '',
    subject: '',
    content: '',
    description: ''
  });

  useEffect(() => {
    loadNewsletterData();
  }, []);

  const loadNewsletterData = async () => {
    try {
      const token = localStorage.getItem('adminToken');
      const headers = {
        'Authorization': `Bearer ${token}`
      };

      const [subscribersRes, campaignsRes, templatesRes, smtpRes] = await Promise.all([
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/newsletter/subscribers`, { headers }),
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/newsletter/campaigns`, { headers }),
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/newsletter/templates`, { headers }),
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/newsletter/smtp-config`, { headers })
      ]);

      if (subscribersRes.ok) setSubscribers(await subscribersRes.json());
      if (campaignsRes.ok) setCampaigns(await campaignsRes.json());
      if (templatesRes.ok) setTemplates(await templatesRes.json());
      if (smtpRes.ok) setSmtpConfig(await smtpRes.json());

    } catch (error) {
      console.error('Error loading newsletter data:', error);
      setMessage('Fehler beim Laden der Newsletter-Daten');
    } finally {
      setLoading(false);
    }
  };

  const deleteSubscriber = async (subscriberId) => {
    if (!confirm('Möchten Sie diesen Abonnenten wirklich löschen?')) return;

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/newsletter/subscribers/${subscriberId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('adminToken')}`
        }
      });

      if (response.ok) {
        setSubscribers(subscribers.filter(s => s.id !== subscriberId));
        setMessage('Abonnent erfolgreich gelöscht');
      } else {
        setMessage('Fehler beim Löschen des Abonnenten');
      }
    } catch (error) {
      setMessage('Verbindungsfehler');
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
        <h2 className="text-3xl font-bold text-gray-900">Newsletter-Verwaltung</h2>
        <p className="text-gray-600 mt-2">Verwalten Sie Newsletter-Abonnenten, Kampagnen und Einstellungen</p>
      </div>

      {message && (
        <div className={`mb-6 p-4 rounded-lg ${
          message.includes('erfolgreich') 
            ? 'bg-green-100 text-green-700 border border-green-200' 
            : 'bg-red-100 text-red-700 border border-red-200'
        }`}>
          {message}
        </div>
      )}

      {/* Tab Navigation */}
      <div className="mb-6">
        <nav className="flex space-x-8">
          {[
            { id: 'subscribers', label: 'Abonnenten', icon: '👥' },
            { id: 'campaigns', label: 'Kampagnen', icon: '📧' },
            { id: 'templates', label: 'Vorlagen', icon: '📝' },
            { id: 'settings', label: 'Einstellungen', icon: '⚙️' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center ${
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Subscribers Tab */}
      {activeTab === 'subscribers' && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">
              Newsletter-Abonnenten ({subscribers.length})
            </h3>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    E-Mail
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Anmeldedatum
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Aktionen
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {subscribers.map((subscriber) => (
                  <tr key={subscriber.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {subscriber.email}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {subscriber.name || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(subscriber.subscribe_date).toLocaleDateString('de-DE')}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <button
                        onClick={() => deleteSubscriber(subscriber.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Löschen
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {subscribers.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                Noch keine Newsletter-Abonnenten vorhanden.
              </div>
            )}
          </div>
        </div>
      )}

      {/* Campaigns Tab */}
      {activeTab === 'campaigns' && (
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-medium text-gray-900">Newsletter-Kampagnen</h3>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                Neue Kampagne
              </button>
            </div>
          </div>
          <div className="p-6">
            {campaigns.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <div className="text-4xl mb-4">📧</div>
                <p>Noch keine Newsletter-Kampagnen erstellt.</p>
                <p className="text-sm mt-2">Erstellen Sie Ihre erste Kampagne, um Newsletter zu versenden.</p>
              </div>
            ) : (
              <div className="space-y-4">
                {campaigns.map((campaign) => (
                  <div key={campaign.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between items-start">
                      <div>
                        <h4 className="font-medium text-gray-900">{campaign.name}</h4>
                        <p className="text-sm text-gray-500">Betreff: {campaign.subject}</p>
                        <p className="text-xs text-gray-400">
                          Erstellt: {new Date(campaign.created_at).toLocaleDateString('de-DE')}
                        </p>
                      </div>
                      <span className={`px-2 py-1 text-xs rounded ${
                        campaign.status === 'sent' ? 'bg-green-100 text-green-800' :
                        campaign.status === 'draft' ? 'bg-gray-100 text-gray-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {campaign.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Templates Tab */}
      {activeTab === 'templates' && (
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-medium text-gray-900">Newsletter-Vorlagen</h3>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                Neue Vorlage
              </button>
            </div>
          </div>
          <div className="p-6">
            {templates.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <div className="text-4xl mb-4">📝</div>
                <p>Noch keine Newsletter-Vorlagen erstellt.</p>
                <p className="text-sm mt-2">Erstellen Sie Vorlagen für wiederkehrende Newsletter.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {templates.map((template) => (
                  <div key={template.id} className="border border-gray-200 rounded-lg p-4">
                    <h4 className="font-medium text-gray-900 mb-2">{template.name}</h4>
                    <p className="text-sm text-gray-500 mb-2">Betreff: {template.subject}</p>
                    <p className="text-xs text-gray-400">
                      Erstellt: {new Date(template.created_at).toLocaleDateString('de-DE')}
                    </p>
                    <div className="mt-3 flex space-x-2">
                      <button className="text-blue-600 hover:text-blue-800 text-sm">Bearbeiten</button>
                      <button className="text-red-600 hover:text-red-800 text-sm">Löschen</button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Settings Tab */}
      {activeTab === 'settings' && (
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Newsletter-Einstellungen</h3>
          </div>
          <div className="p-6">
            <div className="max-w-lg">
              <h4 className="font-medium text-gray-900 mb-4">SMTP-Konfiguration</h4>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">SMTP Server</label>
                  <input
                    type="text"
                    value={smtpConfig.smtp_server || ''}
                    className="w-full p-2 border border-gray-300 rounded bg-white text-gray-900"
                    placeholder="smtp.gmail.com"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Port</label>
                  <input
                    type="number"
                    value={smtpConfig.smtp_port || ''}
                    className="w-full p-2 border border-gray-300 rounded bg-white text-gray-900"
                    placeholder="587"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Benutzername</label>
                  <input
                    type="text"
                    value={smtpConfig.username || ''}
                    className="w-full p-2 border border-gray-300 rounded bg-white text-gray-900"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Absender E-Mail</label>
                  <input
                    type="email"
                    value={smtpConfig.from_email || ''}
                    className="w-full p-2 border border-gray-300 rounded bg-white text-gray-900"
                  />
                </div>
                <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
                  Einstellungen speichern
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default NewsletterSection;