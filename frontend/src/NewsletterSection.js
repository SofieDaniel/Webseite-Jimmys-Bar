import React, { useState, useEffect } from 'react';

// Newsletter Management Section for Admin Panel
export const NewsletterSection = ({ user, token, apiCall }) => {
  const [activeTab, setActiveTab] = useState('subscribers');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  // Subscribers State
  const [subscribers, setSubscribers] = useState([]);
  const [subscribersLoading, setSubscribersLoading] = useState(false);

  // SMTP Configuration State
  const [smtpConfig, setSmtpConfig] = useState(null);
  const [smtpForm, setSmtpForm] = useState({
    host: '',
    port: 587,
    username: '',
    password: '',
    use_tls: true,
    from_email: '',
    from_name: 'Jimmy\'s Tapas Bar'
  });

  // Newsletter Templates State
  const [templates, setTemplates] = useState([]);
  const [templateForm, setTemplateForm] = useState({
    name: '',
    subject: '',
    content: ''
  });

  // Newsletter Campaigns State
  const [campaigns, setCampaigns] = useState([]);
  const [campaignForm, setCampaignForm] = useState({
    subject: '',
    content: '',
    template_id: null
  });

  useEffect(() => {
    if (activeTab === 'subscribers') {
      loadSubscribers();
    } else if (activeTab === 'smtp') {
      loadSmtpConfig();
    } else if (activeTab === 'templates') {
      loadTemplates();
    } else if (activeTab === 'campaigns') {
      loadCampaigns();
    }
  }, [activeTab]);

  // Load Functions
  const loadSubscribers = async () => {
    setSubscribersLoading(true);
    try {
      const response = await apiCall('/admin/newsletter/subscribers');
      if (response.ok) {
        const data = await response.json();
        setSubscribers(data);
      }
    } catch (error) {
      setError('Fehler beim Laden der Abonnenten');
    } finally {
      setSubscribersLoading(false);
    }
  };

  const loadSmtpConfig = async () => {
    try {
      const response = await apiCall('/admin/newsletter/smtp');
      if (response.ok) {
        const data = await response.json();
        setSmtpConfig(data);
        if (data.host) {
          setSmtpForm({
            host: data.host,
            port: data.port,
            username: data.username,
            password: '', // Don't pre-fill password
            use_tls: data.use_tls,
            from_email: data.from_email,
            from_name: data.from_name
          });
        }
      }
    } catch (error) {
      setError('Fehler beim Laden der SMTP-Konfiguration');
    }
  };

  const loadTemplates = async () => {
    try {
      const response = await apiCall('/admin/newsletter/templates');
      if (response.ok) {
        const data = await response.json();
        setTemplates(data);
      }
    } catch (error) {
      setError('Fehler beim Laden der Vorlagen');
    }
  };

  const loadCampaigns = async () => {
    try {
      const response = await apiCall('/admin/newsletter/campaigns');
      if (response.ok) {
        const data = await response.json();
        setCampaigns(data);
      }
    } catch (error) {
      setError('Fehler beim Laden der Kampagnen');
    }
  };

  // SMTP Functions
  const handleSmtpSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');
    setError('');

    try {
      const method = smtpConfig?.host ? 'PUT' : 'POST';
      const endpoint = smtpConfig?.host ? `/admin/newsletter/smtp/${smtpConfig.id}` : '/admin/newsletter/smtp';
      
      const response = await apiCall(endpoint, method, smtpForm);
      if (response.ok) {
        setMessage('SMTP-Konfiguration erfolgreich gespeichert');
        loadSmtpConfig();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Fehler beim Speichern der SMTP-Konfiguration');
      }
    } catch (error) {
      setError('Verbindungsfehler beim Speichern der SMTP-Konfiguration');
    } finally {
      setLoading(false);
    }
  };

  const testSmtpConfig = async () => {
    setLoading(true);
    setMessage('');
    setError('');

    try {
      const response = await apiCall('/admin/newsletter/smtp/test', 'POST');
      if (response.ok) {
        const data = await response.json();
        setMessage(data.message);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'SMTP-Test fehlgeschlagen');
      }
    } catch (error) {
      setError('Verbindungsfehler beim SMTP-Test');
    } finally {
      setLoading(false);
    }
  };

  // Template Functions
  const handleTemplateSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');
    setError('');

    try {
      const response = await apiCall('/admin/newsletter/templates', 'POST', templateForm);
      if (response.ok) {
        setMessage('Newsletter-Vorlage erfolgreich erstellt');
        setTemplateForm({ name: '', subject: '', content: '' });
        loadTemplates();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Fehler beim Erstellen der Vorlage');
      }
    } catch (error) {
      setError('Verbindungsfehler beim Erstellen der Vorlage');
    } finally {
      setLoading(false);
    }
  };

  // Campaign Functions
  const handleCampaignSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');
    setError('');

    try {
      const response = await apiCall('/admin/newsletter/campaigns', 'POST', campaignForm);
      if (response.ok) {
        setMessage('Newsletter-Kampagne erfolgreich erstellt');
        setCampaignForm({ subject: '', content: '', template_id: null });
        loadCampaigns();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Fehler beim Erstellen der Kampagne');
      }
    } catch (error) {
      setError('Verbindungsfehler beim Erstellen der Kampagne');
    } finally {
      setLoading(false);
    }
  };

  const sendCampaign = async (campaignId) => {
    if (!confirm('Sind Sie sicher, dass Sie diese Kampagne versenden möchten?')) {
      return;
    }

    setLoading(true);
    setMessage('');
    setError('');

    try {
      const response = await apiCall(`/admin/newsletter/campaigns/${campaignId}/send`, 'POST');
      if (response.ok) {
        const data = await response.json();
        setMessage(data.message);
        loadCampaigns();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Fehler beim Versenden der Kampagne');
      }
    } catch (error) {
      setError('Verbindungsfehler beim Versenden der Kampagne');
    } finally {
      setLoading(false);
    }
  };

  const deleteSubscriber = async (subscriberId) => {
    if (!confirm('Sind Sie sicher, dass Sie diesen Abonnenten löschen möchten?')) {
      return;
    }

    try {
      const response = await apiCall(`/admin/newsletter/subscribers/${subscriberId}`, 'DELETE');
      if (response.ok) {
        setMessage('Abonnent erfolgreich gelöscht');
        loadSubscribers();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Fehler beim Löschen des Abonnenten');
      }
    } catch (error) {
      setError('Verbindungsfehler beim Löschen des Abonnenten');
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Newsletter Management</h1>
        <p className="text-gray-600">Verwalten Sie Newsletter-Abonnenten, SMTP-Konfiguration und Kampagnen</p>
      </div>

      {/* Messages */}
      {message && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
          {message}
        </div>
      )}

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'subscribers', name: 'Abonnenten', icon: '👥' },
            { id: 'smtp', name: 'SMTP-Konfiguration', icon: '⚙️' },
            { id: 'templates', name: 'Vorlagen', icon: '📄' },
            { id: 'campaigns', name: 'Kampagnen', icon: '📧' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {tab.icon} {tab.name}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        {/* Subscribers Tab */}
        {activeTab === 'subscribers' && (
          <div>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold text-gray-900">Newsletter-Abonnenten</h2>
              <button
                onClick={loadSubscribers}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Aktualisieren
              </button>
            </div>

            {subscribersLoading ? (
              <div className="flex justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              </div>
            ) : (
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
                        Angemeldet am
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Status
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
                          {new Date(subscriber.subscribed_at).toLocaleDateString('de-DE')}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                            subscriber.is_active 
                              ? 'bg-green-100 text-green-800' 
                              : 'bg-red-100 text-red-800'
                          }`}>
                            {subscriber.is_active ? 'Aktiv' : 'Inaktiv'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
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
                    Keine Abonnenten gefunden
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* SMTP Configuration Tab */}
        {activeTab === 'smtp' && (
          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-6">SMTP-Konfiguration</h2>
            
            <form onSubmit={handleSmtpSubmit} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    SMTP-Host
                  </label>
                  <input
                    type="text"
                    value={smtpForm.host}
                    onChange={(e) => setSmtpForm({...smtpForm, host: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="smtp.gmail.com"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Port
                  </label>
                  <input
                    type="number"
                    value={smtpForm.port}
                    onChange={(e) => setSmtpForm({...smtpForm, port: parseInt(e.target.value)})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Benutzername
                  </label>
                  <input
                    type="text"
                    value={smtpForm.username}
                    onChange={(e) => setSmtpForm({...smtpForm, username: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Passwort
                  </label>
                  <input
                    type="password"
                    value={smtpForm.password}
                    onChange={(e) => setSmtpForm({...smtpForm, password: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder={smtpConfig?.host ? "Leer lassen, um beizubehalten" : ""}
                    required={!smtpConfig?.host}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Absender E-Mail
                  </label>
                  <input
                    type="email"
                    value={smtpForm.from_email}
                    onChange={(e) => setSmtpForm({...smtpForm, from_email: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Absender Name
                  </label>
                  <input
                    type="text"
                    value={smtpForm.from_name}
                    onChange={(e) => setSmtpForm({...smtpForm, from_name: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>
              </div>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="use_tls"
                  checked={smtpForm.use_tls}
                  onChange={(e) => setSmtpForm({...smtpForm, use_tls: e.target.checked})}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="use_tls" className="ml-2 block text-sm text-gray-900">
                  TLS verwenden (empfohlen)
                </label>
              </div>

              <div className="flex space-x-4">
                <button
                  type="submit"
                  disabled={loading}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                >
                  {loading ? 'Speichern...' : 'SMTP-Konfiguration speichern'}
                </button>

                {smtpConfig?.host && (
                  <button
                    type="button"
                    onClick={testSmtpConfig}
                    disabled={loading}
                    className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50"
                  >
                    {loading ? 'Teste...' : 'SMTP testen'}
                  </button>
                )}
              </div>
            </form>

            {smtpConfig?.host && (
              <div className="mt-8 p-4 bg-gray-50 rounded-lg">
                <h3 className="text-lg font-medium text-gray-900 mb-2">Aktuelle Konfiguration</h3>
                <div className="grid grid-cols-2 gap-4 text-sm text-gray-600">
                  <div><strong>Host:</strong> {smtpConfig.host}</div>
                  <div><strong>Port:</strong> {smtpConfig.port}</div>
                  <div><strong>Benutzername:</strong> {smtpConfig.username}</div>
                  <div><strong>TLS:</strong> {smtpConfig.use_tls ? 'Ja' : 'Nein'}</div>
                  <div><strong>Absender:</strong> {smtpConfig.from_name} &lt;{smtpConfig.from_email}&gt;</div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Templates Tab */}
        {activeTab === 'templates' && (
          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Newsletter-Vorlagen</h2>
            
            {/* Create Template Form */}
            <div className="mb-8 p-6 bg-gray-50 rounded-lg">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Neue Vorlage erstellen</h3>
              <form onSubmit={handleTemplateSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Vorlagen-Name
                  </label>
                  <input
                    type="text"
                    value={templateForm.name}
                    onChange={(e) => setTemplateForm({...templateForm, name: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Betreff
                  </label>
                  <input
                    type="text"
                    value={templateForm.subject}
                    onChange={(e) => setTemplateForm({...templateForm, subject: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Inhalt (HTML)
                  </label>
                  <textarea
                    value={templateForm.content}
                    onChange={(e) => setTemplateForm({...templateForm, content: e.target.value})}
                    rows={8}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="<h1>Willkommen zu unserem Newsletter!</h1><p>Ihr Newsletter-Inhalt hier...</p>"
                    required
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                >
                  {loading ? 'Erstellen...' : 'Vorlage erstellen'}
                </button>
              </form>
            </div>

            {/* Templates List */}
            <div className="space-y-4">
              {templates.map((template) => (
                <div key={template.id} className="p-4 border border-gray-200 rounded-lg">
                  <div className="flex justify-between items-start">
                    <div>
                      <h4 className="text-lg font-medium text-gray-900">{template.name}</h4>
                      <p className="text-sm text-gray-600">Betreff: {template.subject}</p>
                      <p className="text-xs text-gray-500">
                        Erstellt von {template.created_by} am {new Date(template.created_at).toLocaleDateString('de-DE')}
                      </p>
                    </div>
                    <button
                      onClick={() => setCampaignForm({...campaignForm, template_id: template.id, subject: template.subject, content: template.content})}
                      className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors text-sm"
                    >
                      Verwenden
                    </button>
                  </div>
                </div>
              ))}
              {templates.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  Keine Vorlagen gefunden
                </div>
              )}
            </div>
          </div>
        )}

        {/* Campaigns Tab */}
        {activeTab === 'campaigns' && (
          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Newsletter-Kampagnen</h2>
            
            {/* Create Campaign Form */}
            <div className="mb-8 p-6 bg-gray-50 rounded-lg">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Neue Kampagne erstellen</h3>
              <form onSubmit={handleCampaignSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Betreff
                  </label>
                  <input
                    type="text"
                    value={campaignForm.subject}
                    onChange={(e) => setCampaignForm({...campaignForm, subject: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Inhalt (HTML)
                  </label>
                  <textarea
                    value={campaignForm.content}
                    onChange={(e) => setCampaignForm({...campaignForm, content: e.target.value})}
                    rows={10}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="<h1>Newsletter-Titel</h1><p>Ihr Newsletter-Inhalt hier...</p>"
                    required
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                >
                  {loading ? 'Erstellen...' : 'Kampagne erstellen'}
                </button>
              </form>
            </div>

            {/* Campaigns List */}
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-medium text-gray-900">Kampagnen</h3>
                <div className="text-sm text-gray-600">
                  Abonnenten gesamt: {subscribers.filter(s => s.is_active).length}
                </div>
              </div>

              {campaigns.map((campaign) => (
                <div key={campaign.id} className="p-4 border border-gray-200 rounded-lg">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h4 className="text-lg font-medium text-gray-900">{campaign.subject}</h4>
                      <p className="text-sm text-gray-600 mb-2">
                        Erstellt von {campaign.created_by} am {new Date(campaign.created_at).toLocaleDateString('de-DE')}
                      </p>
                      <div className="flex items-center space-x-4 text-xs text-gray-500">
                        <span className={`px-2 py-1 rounded-full ${
                          campaign.status === 'sent' ? 'bg-green-100 text-green-800' :
                          campaign.status === 'sending' ? 'bg-yellow-100 text-yellow-800' :
                          campaign.status === 'failed' ? 'bg-red-100 text-red-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {campaign.status === 'sent' ? 'Versendet' :
                           campaign.status === 'sending' ? 'Wird versendet' :
                           campaign.status === 'failed' ? 'Fehlgeschlagen' :
                           'Entwurf'}
                        </span>
                        {campaign.sent_at && (
                          <span>Versendet am: {new Date(campaign.sent_at).toLocaleDateString('de-DE')}</span>
                        )}
                        {campaign.recipients_count > 0 && (
                          <span>Empfänger: {campaign.recipients_count}</span>
                        )}
                      </div>
                    </div>
                    <div className="flex space-x-2">
                      {campaign.status === 'draft' && (
                        <button
                          onClick={() => sendCampaign(campaign.id)}
                          disabled={loading}
                          className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors text-sm disabled:opacity-50"
                        >
                          Versenden
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              ))}
              
              {campaigns.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  Keine Kampagnen gefunden
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};