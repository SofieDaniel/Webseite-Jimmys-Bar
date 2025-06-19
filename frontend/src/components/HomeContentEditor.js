import React from 'react';

const HomeContentEditor = ({ content, setContent, onSave, saving }) => {
  if (!content) return null;

  return (
    <div className="space-y-8">
      {/* Hero Section Editor */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Hero-Bereich (Hauptbereich)</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Haupttitel</label>
            <input
              type="text"
              value={content.hero?.title || ''}
              onChange={(e) => setContent({
                ...content,
                hero: { ...content.hero, title: e.target.value }
              })}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Untertitel</label>
            <input
              type="text"
              value={content.hero?.subtitle || ''}
              onChange={(e) => setContent({
                ...content,
                hero: { ...content.hero, subtitle: e.target.value }
              })}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Beschreibung</label>
            <input
              type="text"
              value={content.hero?.description || ''}
              onChange={(e) => setContent({
                ...content,
                hero: { ...content.hero, description: e.target.value }
              })}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Standort-Text</label>
            <input
              type="text"
              value={content.hero?.location || ''}
              onChange={(e) => setContent({
                ...content,
                hero: { ...content.hero, location: e.target.value }
              })}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Hintergrundbild URL</label>
            <input
              type="url"
              value={content.hero?.background_image || ''}
              onChange={(e) => setContent({
                ...content,
                hero: { ...content.hero, background_image: e.target.value }
              })}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Menü-Button Text</label>
            <input
              type="text"
              value={content.hero?.menu_button_text || ''}
              onChange={(e) => setContent({
                ...content,
                hero: { ...content.hero, menu_button_text: e.target.value }
              })}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>

      {/* Features Section Editor */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Features-Bereich</h3>
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Bereichstitel</label>
              <input
                type="text"
                value={content.features?.title || ''}
                onChange={(e) => setContent({
                  ...content,
                  features: { ...content.features, title: e.target.value }
                })}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Bereichs-Untertitel</label>
              <textarea
                value={content.features?.subtitle || ''}
                onChange={(e) => setContent({
                  ...content,
                  features: { ...content.features, subtitle: e.target.value }
                })}
                rows={2}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          
          <div className="space-y-4">
            <h4 className="font-medium text-gray-900">Features-Karten bearbeiten:</h4>
            {content.features?.cards?.map((card, index) => (
              <div key={index} className="grid grid-cols-1 md:grid-cols-3 gap-4 p-6 bg-gray-50 rounded-lg border">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Karte {index + 1} Titel</label>
                  <input
                    type="text"
                    value={card.title || ''}
                    onChange={(e) => {
                      const newCards = [...(content.features?.cards || [])];
                      newCards[index] = { ...newCards[index], title: e.target.value };
                      setContent({
                        ...content,
                        features: { ...content.features, cards: newCards }
                      });
                    }}
                    className="w-full p-3 border border-gray-300 rounded-md bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Karte {index + 1} Beschreibung</label>
                  <textarea
                    value={card.description || ''}
                    onChange={(e) => {
                      const newCards = [...(content.features?.cards || [])];
                      newCards[index] = { ...newCards[index], description: e.target.value };
                      setContent({
                        ...content,
                        features: { ...content.features, cards: newCards }
                      });
                    }}
                    rows={3}
                    className="w-full p-3 border border-gray-300 rounded-md bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Karte {index + 1} Bild-URL</label>
                  <input
                    type="url"
                    value={card.image_url || ''}
                    onChange={(e) => {
                      const newCards = [...(content.features?.cards || [])];
                      newCards[index] = { ...newCards[index], image_url: e.target.value };
                      setContent({
                        ...content,
                        features: { ...content.features, cards: newCards }
                      });
                    }}
                    className="w-full p-3 border border-gray-300 rounded-md bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  {card.image_url && (
                    <div className="mt-2">
                      <img src={card.image_url} alt="Vorschau" className="w-20 h-20 object-cover rounded border" />
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Specialties Section Editor */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Spezialitäten-Bereich</h3>
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Bereichstitel</label>
            <input
              type="text"
              value={content.specialties?.title || ''}
              onChange={(e) => setContent({
                ...content,
                specialties: { ...content.specialties, title: e.target.value }
              })}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          
          <div className="space-y-4">
            <h4 className="font-medium text-gray-900">Spezialitäten-Karten bearbeiten:</h4>
            {content.specialties?.cards?.map((card, index) => (
              <div key={index} className="grid grid-cols-1 md:grid-cols-4 gap-4 p-6 bg-gray-50 rounded-lg border">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Karte {index + 1} Titel</label>
                  <input
                    type="text"
                    value={card.title || ''}
                    onChange={(e) => {
                      const newCards = [...(content.specialties?.cards || [])];
                      newCards[index] = { ...newCards[index], title: e.target.value };
                      setContent({
                        ...content,
                        specialties: { ...content.specialties, cards: newCards }
                      });
                    }}
                    className="w-full p-3 border border-gray-300 rounded-md bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Karte {index + 1} Beschreibung</label>
                  <textarea
                    value={card.description || ''}
                    onChange={(e) => {
                      const newCards = [...(content.specialties?.cards || [])];
                      newCards[index] = { ...newCards[index], description: e.target.value };
                      setContent({
                        ...content,
                        specialties: { ...content.specialties, cards: newCards }
                      });
                    }}
                    rows={3}
                    className="w-full p-3 border border-gray-300 rounded-md bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Karte {index + 1} Bild-URL</label>
                  <input
                    type="url"
                    value={card.image_url || ''}
                    onChange={(e) => {
                      const newCards = [...(content.specialties?.cards || [])];
                      newCards[index] = { ...newCards[index], image_url: e.target.value };
                      setContent({
                        ...content,
                        specialties: { ...content.specialties, cards: newCards }
                      });
                    }}
                    className="w-full p-3 border border-gray-300 rounded-md bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  {card.image_url && (
                    <div className="mt-2">
                      <img src={card.image_url} alt="Vorschau" className="w-20 h-20 object-cover rounded border" />
                    </div>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Kategorie-Link</label>
                  <select
                    value={card.category_link || ''}
                    onChange={(e) => {
                      const newCards = [...(content.specialties?.cards || [])];
                      newCards[index] = { ...newCards[index], category_link: e.target.value };
                      setContent({
                        ...content,
                        specialties: { ...content.specialties, cards: newCards }
                      });
                    }}
                    className="w-full p-3 border border-gray-300 rounded-md bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">Keine Kategorie</option>
                    <option value="inicio">Inicio</option>
                    <option value="tapas-vegetarian">Tapas Vegetarisch</option>
                    <option value="tapas-pescado">Tapas Fisch</option>
                    <option value="tapas-carne">Tapas Fleisch</option>
                    <option value="tapa-paella">Paella</option>
                    <option value="kroketten">Kroketten</option>
                    <option value="salat">Salate</option>
                  </select>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Delivery Section Editor */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">🚚 Lieferando-Bereich (Delivery)</h3>
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Haupttitel</label>
              <input
                type="text"
                value={content.delivery?.title || 'Jetzt auch bequem nach Hause bestellen'}
                onChange={(e) => setContent({
                  ...content,
                  delivery: { ...content.delivery, title: e.target.value }
                })}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Beschreibung</label>
              <textarea
                value={content.delivery?.description || 'Genießen Sie unsere authentischen mediterranen Spezialitäten gemütlich zu Hause.'}
                onChange={(e) => setContent({
                  ...content,
                  delivery: { ...content.delivery, description: e.target.value }
                })}
                rows={3}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Zweite Beschreibung</label>
              <textarea
                value={content.delivery?.description_2 || 'Bestellen Sie direkt über Lieferando und lassen Sie sich verwöhnen.'}
                onChange={(e) => setContent({
                  ...content,
                  delivery: { ...content.delivery, description_2: e.target.value }
                })}
                rows={3}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Button-Text</label>
              <input
                type="text"
                value={content.delivery?.button_text || 'Jetzt bei Lieferando bestellen'}
                onChange={(e) => setContent({
                  ...content,
                  delivery: { ...content.delivery, button_text: e.target.value }
                })}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Button-URL (Lieferando-Link)</label>
              <input
                type="url"
                value={content.delivery?.button_url || 'https://www.lieferando.de'}
                onChange={(e) => setContent({
                  ...content,
                  delivery: { ...content.delivery, button_url: e.target.value }
                })}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Verfügbarkeitstext</label>
              <input
                type="text"
                value={content.delivery?.availability_text || 'Verfügbar für beide Standorte'}
                onChange={(e) => setContent({
                  ...content,
                  delivery: { ...content.delivery, availability_text: e.target.value }
                })}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Delivery Features */}
          <div className="border-t pt-6">
            <h4 className="text-md font-semibold text-gray-800 mb-4">Delivery Features</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Schnelle Lieferung Feature */}
              <div className="bg-gray-50 p-4 rounded-lg">
                <h5 className="font-medium text-gray-700 mb-3">🚚 Schnelle Lieferung</h5>
                <div className="space-y-3">
                  <div>
                    <label className="block text-sm font-medium text-gray-600 mb-1">Titel</label>
                    <input
                      type="text"
                      value={content.delivery?.delivery_feature_title || 'Schnelle Lieferung'}
                      onChange={(e) => setContent({
                        ...content,
                        delivery: { ...content.delivery, delivery_feature_title: e.target.value }
                      })}
                      className="w-full p-2 border border-gray-300 rounded bg-white text-gray-900"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-600 mb-1">Beschreibung</label>
                    <input
                      type="text"
                      value={content.delivery?.delivery_feature_description || 'Frisch und warm zu Ihnen'}
                      onChange={(e) => setContent({
                        ...content,
                        delivery: { ...content.delivery, delivery_feature_description: e.target.value }
                      })}
                      className="w-full p-2 border border-gray-300 rounded bg-white text-gray-900"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-600 mb-1">Bild-URL</label>
                    <input
                      type="url"
                      value={content.delivery?.delivery_feature_image || 'https://images.pexels.com/photos/6969962/pexels-photo-6969962.jpeg'}
                      onChange={(e) => setContent({
                        ...content,
                        delivery: { ...content.delivery, delivery_feature_image: e.target.value }
                      })}
                      className="w-full p-2 border border-gray-300 rounded bg-white text-gray-900"
                    />
                  </div>
                </div>
              </div>

              {/* Authentisch Mediterran Feature */}
              <div className="bg-gray-50 p-4 rounded-lg">
                <h5 className="font-medium text-gray-700 mb-3">🍽️ Authentisch Mediterran</h5>
                <div className="space-y-3">
                  <div>
                    <label className="block text-sm font-medium text-gray-600 mb-1">Titel</label>
                    <input
                      type="text"
                      value={content.delivery?.authentic_feature_title || 'Authentisch Mediterran'}
                      onChange={(e) => setContent({
                        ...content,
                        delivery: { ...content.delivery, authentic_feature_title: e.target.value }
                      })}
                      className="w-full p-2 border border-gray-300 rounded bg-white text-gray-900"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-600 mb-1">Beschreibung</label>
                    <input
                      type="text"
                      value={content.delivery?.authentic_feature_description || 'Direkt vom Küchenchef'}
                      onChange={(e) => setContent({
                        ...content,
                        delivery: { ...content.delivery, authentic_feature_description: e.target.value }
                      })}
                      className="w-full p-2 border border-gray-300 rounded bg-white text-gray-900"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-600 mb-1">Bild-URL</label>
                    <input
                      type="url"
                      value={content.delivery?.authentic_feature_image || 'https://images.pexels.com/photos/31748679/pexels-photo-31748679.jpeg'}
                      onChange={(e) => setContent({
                        ...content,
                        delivery: { ...content.delivery, authentic_feature_image: e.target.value }
                      })}
                      className="w-full p-2 border border-gray-300 rounded bg-white text-gray-900"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <button
          onClick={onSave}
          disabled={saving}
          className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center space-x-2"
        >
          {saving ? (
            <>
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Speichern...
            </>
          ) : (
            'Änderungen speichern'
          )}
        </button>
      </div>
    </div>
  );
};

export default HomeContentEditor;