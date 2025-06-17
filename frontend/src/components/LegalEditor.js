import React, { useState, useEffect } from 'react';

// Legal Editor Component for Impressum and Datenschutz
const LegalEditor = () => {
  const [activeTab, setActiveTab] = useState('imprint');
  const [imprintData, setImprintData] = useState(null);
  const [privacyData, setPrivacyData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  // Load legal pages data
  useEffect(() => {
    loadLegalData();
  }, []);

  const loadLegalData = async () => {
    try {
      setLoading(true);
      
      // Load imprint data
      const imprintResponse = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/legal/imprint`);
      if (imprintResponse.ok) {
        const imprintResult = await imprintResponse.json();
        setImprintData(imprintResult);
      }

      // Load privacy data
      const privacyResponse = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/legal/privacy`);
      if (privacyResponse.ok) {
        const privacyResult = await privacyResponse.json();
        setPrivacyData(privacyResult);
      }
    } catch (error) {
      console.error('Error loading legal data:', error);
      setMessage('Fehler beim Laden der Daten');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (pageType) => {
    setSaving(true);
    setMessage('');

    try {
      const data = pageType === 'imprint' ? imprintData : privacyData;
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/legal/${pageType}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('adminToken')}`
        },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        setMessage(`${pageType === 'imprint' ? 'Impressum' : 'Datenschutzerklärung'} erfolgreich gespeichert!`);
      } else {
        setMessage('Fehler beim Speichern');
      }
    } catch (error) {
      setMessage('Verbindungsfehler beim Speichern');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  const currentData = activeTab === 'imprint' ? imprintData : privacyData;
  const setCurrentData = activeTab === 'imprint' ? setImprintData : setPrivacyData;

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Impressum & Datenschutz bearbeiten</h2>
      
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
          <button
            onClick={() => setActiveTab('imprint')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'imprint'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Impressum bearbeiten
          </button>
          <button
            onClick={() => setActiveTab('privacy')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'privacy'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Datenschutz bearbeiten
          </button>
        </nav>
      </div>

      {/* Content Editor */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="space-y-6">
          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Seitentitel</label>
            <input
              type="text"
              value={currentData?.title || ''}
              onChange={(e) => setCurrentData({
                ...currentData,
                title: e.target.value
              })}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Main Content */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Hauptinhalt</label>
            <textarea
              value={currentData?.content || ''}
              onChange={(e) => setCurrentData({
                ...currentData,
                content: e.target.value
              })}
              rows={20}
              className="w-full p-4 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
              placeholder="Geben Sie hier den Inhalt ein. Verwenden Sie **Text** für Überschriften."
            />
            <p className="mt-2 text-sm text-gray-500">
              Tipp: Verwenden Sie **Text** für Überschriften und leere Zeilen für Absätze.
            </p>
          </div>

          {/* Contact Information */}
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Kontaktperson</label>
              <input
                type="text"
                value={currentData?.contact_name || ''}
                onChange={(e) => setCurrentData({
                  ...currentData,
                  contact_name: e.target.value
                })}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Kontakt E-Mail</label>
              <input
                type="email"
                value={currentData?.contact_email || ''}
                onChange={(e) => setCurrentData({
                  ...currentData,
                  contact_email: e.target.value
                })}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Adresse</label>
              <input
                type="text"
                value={currentData?.contact_address || ''}
                onChange={(e) => setCurrentData({
                  ...currentData,
                  contact_address: e.target.value
                })}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Telefon</label>
              <input
                type="text"
                value={currentData?.contact_phone || ''}
                onChange={(e) => setCurrentData({
                  ...currentData,
                  contact_phone: e.target.value
                })}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Company Information (only for imprint) */}
          {activeTab === 'imprint' && (
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Firmeninformationen</h3>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Firmenname</label>
                  <input
                    type="text"
                    value={currentData?.company_info?.company_name || ''}
                    onChange={(e) => setCurrentData({
                      ...currentData,
                      company_info: {
                        ...currentData.company_info,
                        company_name: e.target.value
                      }
                    })}
                    className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Registergericht</label>
                  <input
                    type="text"
                    value={currentData?.company_info?.register_court || ''}
                    onChange={(e) => setCurrentData({
                      ...currentData,
                      company_info: {
                        ...currentData.company_info,
                        register_court: e.target.value
                      }
                    })}
                    className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Registernummer</label>
                  <input
                    type="text"
                    value={currentData?.company_info?.register_number || ''}
                    onChange={(e) => setCurrentData({
                      ...currentData,
                      company_info: {
                        ...currentData.company_info,
                        register_number: e.target.value
                      }
                    })}
                    className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Umsatzsteuer-ID</label>
                  <input
                    type="text"
                    value={currentData?.company_info?.vat_id || ''}
                    onChange={(e) => setCurrentData({
                      ...currentData,
                      company_info: {
                        ...currentData.company_info,
                        vat_id: e.target.value
                      }
                    })}
                    className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>
            </div>
          )}

          {/* Save Button */}
          <div className="flex justify-between items-center pt-6 border-t">
            <div className="text-sm text-gray-500">
              Zuletzt bearbeitet: {currentData?.updated_at ? new Date(currentData.updated_at).toLocaleString('de-DE') : 'Nie'}
            </div>
            <button
              onClick={() => handleSave(activeTab)}
              disabled={saving}
              className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 font-medium"
            >
              {saving ? 'Speichern...' : `${activeTab === 'imprint' ? 'Impressum' : 'Datenschutz'} speichern`}
            </button>
          </div>

          {/* Preview Link */}
          <div className="border-t pt-4">
            <a
              href={`/${activeTab === 'imprint' ? 'impressum' : 'datenschutz'}`}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center text-blue-600 hover:text-blue-800"
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
              {activeTab === 'imprint' ? 'Impressum' : 'Datenschutz'} in neuem Tab ansehen
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LegalEditor;