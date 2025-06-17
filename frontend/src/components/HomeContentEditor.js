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
    </div>
  );
};

export default HomeContentEditor;