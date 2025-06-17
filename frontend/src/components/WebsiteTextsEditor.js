import React from 'react';

const WebsiteTextsEditor = ({ section, texts, setTexts, onSave, saving }) => {
  if (!texts) return null;

  const renderNavigationEditor = () => (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-900">Navigation-Texte</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {Object.entries(texts.navigation || {}).map(([key, value]) => (
          <div key={key}>
            <label className="block text-sm font-medium text-gray-700 mb-2 capitalize">
              {key === 'home' ? 'Startseite' : 
               key === 'locations' ? 'Standorte' :
               key === 'menu' ? 'Speisekarte' :
               key === 'reviews' ? 'Bewertungen' :
               key === 'about' ? 'Über uns' :
               key === 'contact' ? 'Kontakt' :
               key === 'privacy' ? 'Datenschutz' :
               key === 'imprint' ? 'Impressum' : key}
            </label>
            <input
              type="text"
              value={value || ''}
              onChange={(e) => setTexts({
                ...texts,
                navigation: {
                  ...texts.navigation,
                  [key]: e.target.value
                }
              })}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        ))}
      </div>
    </div>
  );

  const renderFooterEditor = () => (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-900">Footer-Texte</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {Object.entries(texts.footer || {}).map(([key, value]) => (
          <div key={key}>
            <label className="block text-sm font-medium text-gray-700 mb-2 capitalize">
              {key === 'opening_hours_title' ? 'Öffnungszeiten Titel' :
               key === 'contact_title' ? 'Kontakt Titel' :
               key === 'follow_us_title' ? 'Social Media Titel' :
               key === 'copyright' ? 'Copyright Text' : key}
            </label>
            {key === 'copyright' ? (
              <textarea
                value={value || ''}
                onChange={(e) => setTexts({
                  ...texts,
                  footer: {
                    ...texts.footer,
                    [key]: e.target.value
                  }
                })}
                rows={2}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            ) : (
              <input
                type="text"
                value={value || ''}
                onChange={(e) => setTexts({
                  ...texts,
                  footer: {
                    ...texts.footer,
                    [key]: e.target.value
                  }
                })}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            )}
          </div>
        ))}
      </div>
    </div>
  );

  const renderButtonsEditor = () => (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-900">Button-Texte</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {Object.entries(texts.buttons || {}).map(([key, value]) => (
          <div key={key}>
            <label className="block text-sm font-medium text-gray-700 mb-2 capitalize">
              {key === 'menu_button' ? 'Menü Button' :
               key === 'locations_button' ? 'Standorte Button' :
               key === 'contact_button' ? 'Kontakt Button' :
               key === 'reserve_button' ? 'Reservieren Button' :
               key === 'order_button' ? 'Bestellen Button' : key}
            </label>
            <input
              type="text"
              value={value || ''}
              onChange={(e) => setTexts({
                ...texts,
                buttons: {
                  ...texts.buttons,
                  [key]: e.target.value
                }
              })}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        ))}
      </div>
    </div>
  );

  const renderGeneralEditor = () => (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-900">Allgemeine Texte</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {Object.entries(texts.general || {}).map(([key, value]) => (
          <div key={key}>
            <label className="block text-sm font-medium text-gray-700 mb-2 capitalize">
              {key === 'loading' ? 'Ladetext' :
               key === 'error' ? 'Fehlertext' :
               key === 'success' ? 'Erfolgstext' :
               key === 'required_field' ? 'Pflichtfeld Text' :
               key === 'email_invalid' ? 'E-Mail ungültig Text' : key}
            </label>
            <input
              type="text"
              value={value || ''}
              onChange={(e) => setTexts({
                ...texts,
                general: {
                  ...texts.general,
                  [key]: e.target.value
                }
              })}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      {section === 'navigation' && renderNavigationEditor()}
      {section === 'footer' && renderFooterEditor()}
      {section === 'buttons' && renderButtonsEditor()}
      {section === 'general' && renderGeneralEditor()}
      
      <div className="mt-6 pt-6 border-t border-gray-200">
        <p className="text-sm text-gray-500 mb-4">
          Zuletzt bearbeitet: {texts.updated_at ? new Date(texts.updated_at).toLocaleString('de-DE') : 'Nie'}
        </p>
      </div>
    </div>
  );
};

export default WebsiteTextsEditor;