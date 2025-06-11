import React, { useState, useEffect } from 'react';

// Admin Components - Separate file for better organization
export const LocationsEditor = ({ content, saveContent }) => {
  const [localLocations, setLocalLocations] = useState(content.locations || [
    {
      id: 1,
      name: "Jimmy's Tapas Bar Neustadt",
      address: "Am Strande 21",
      city: "23730 Neustadt in Holstein",
      phone: "+49 (0) 4561 123456",
      email: "neustadt@jimmys-tapasbar.de",
      features: ["Direkt am Strand", "Terrasse mit Meerblick", "Parkplätze vorhanden", "Familienfreundlich"],
      image: "https://images.unsplash.com/photo-1665758564776-f2aa6b41327e",
      type: "Hauptstandort"
    },
    {
      id: 2,
      name: "Jimmy's Tapas Bar Großenbrode",
      address: "Südstrand 54",
      city: "23755 Großenbrode",
      phone: "+49 (0) 4561 789012",
      email: "grossenbrode@jimmys-tapasbar.de",
      features: ["Strandnähe", "Gemütliche Atmosphäre", "Kostenlose Parkplätze", "Hundefreundlich"],
      image: "https://images.unsplash.com/photo-1665758564796-5162ff406254",
      type: "Zweigstelle"
    }
  ]);

  const handleSaveLocations = () => {
    const newContent = { ...content, locations: localLocations };
    saveContent(newContent);
    alert('Standorte gespeichert!');
  };

  const updateLocation = (id, field, value) => {
    setLocalLocations(localLocations.map(loc => 
      loc.id === id ? { ...loc, [field]: value } : loc
    ));
  };

  const updateLocationFeature = (id, index, value) => {
    setLocalLocations(localLocations.map(loc => {
      if (loc.id === id) {
        const newFeatures = [...loc.features];
        newFeatures[index] = value;
        return { ...loc, features: newFeatures };
      }
      return loc;
    }));
  };

  const addLocationFeature = (id) => {
    setLocalLocations(localLocations.map(loc => 
      loc.id === id ? { ...loc, features: [...loc.features, ''] } : loc
    ));
  };

  const removeLocationFeature = (id, index) => {
    setLocalLocations(localLocations.map(loc => {
      if (loc.id === id) {
        const newFeatures = loc.features.filter((_, i) => i !== index);
        return { ...loc, features: newFeatures };
      }
      return loc;
    }));
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-serif text-warm-beige">Standorte verwalten</h2>
        <button
          onClick={handleSaveLocations}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition-colors"
        >
          Speichern
        </button>
      </div>

      {localLocations.map(location => (
        <div key={location.id} className="bg-dark-brown p-4 rounded border border-warm-brown">
          <h3 className="text-warm-beige font-serif mb-3">{location.name}</h3>
          
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-warm-beige mb-2">Name</label>
              <input
                type="text"
                value={location.name}
                onChange={(e) => updateLocation(location.id, 'name', e.target.value)}
                className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige"
              />
            </div>
            
            <div>
              <label className="block text-warm-beige mb-2">Typ</label>
              <select
                value={location.type}
                onChange={(e) => updateLocation(location.id, 'type', e.target.value)}
                className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige"
              >
                <option value="Hauptstandort">Hauptstandort</option>
                <option value="Zweigstelle">Zweigstelle</option>
              </select>
            </div>
            
            <div>
              <label className="block text-warm-beige mb-2">Adresse</label>
              <input
                type="text"
                value={location.address}
                onChange={(e) => updateLocation(location.id, 'address', e.target.value)}
                className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige"
              />
            </div>
            
            <div>
              <label className="block text-warm-beige mb-2">Stadt & PLZ</label>
              <input
                type="text"
                value={location.city}
                onChange={(e) => updateLocation(location.id, 'city', e.target.value)}
                className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige"
              />
            </div>
            
            <div>
              <label className="block text-warm-beige mb-2">Telefon</label>
              <input
                type="text"
                value={location.phone}
                onChange={(e) => updateLocation(location.id, 'phone', e.target.value)}
                className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige"
              />
            </div>
            
            <div>
              <label className="block text-warm-beige mb-2">E-Mail</label>
              <input
                type="email"
                value={location.email}
                onChange={(e) => updateLocation(location.id, 'email', e.target.value)}
                className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige"
              />
            </div>
            
            <div className="md:col-span-2">
              <label className="block text-warm-beige mb-2">Bild URL</label>
              <input
                type="url"
                value={location.image}
                onChange={(e) => updateLocation(location.id, 'image', e.target.value)}
                className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige"
              />
              {location.image && (
                <img src={location.image} alt="Preview" className="mt-2 w-32 h-20 object-cover rounded" />
              )}
            </div>
            
            <div className="md:col-span-2">
              <label className="block text-warm-beige mb-2">Besonderheiten</label>
              {location.features.map((feature, index) => (
                <div key={index} className="flex gap-2 mb-2">
                  <input
                    type="text"
                    value={feature}
                    onChange={(e) => updateLocationFeature(location.id, index, e.target.value)}
                    className="flex-1 p-2 bg-medium-brown border border-warm-brown rounded text-warm-beige"
                    placeholder="Besonderheit"
                  />
                  <button
                    onClick={() => removeLocationFeature(location.id, index)}
                    className="bg-red-600 text-white px-3 py-2 rounded hover:bg-red-700 transition-colors"
                  >
                    ×
                  </button>
                </div>
              ))}
              <button
                onClick={() => addLocationFeature(location.id)}
                className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors"
              >
                + Besonderheit hinzufügen
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export const SettingsEditor = ({ content, saveContent }) => {
  const [localSettings, setLocalSettings] = useState(content.settings);

  const handleSaveSettings = () => {
    const newContent = { ...content, settings: localSettings };
    saveContent(newContent);
    alert('Einstellungen gespeichert!');
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-serif text-warm-beige">Einstellungen</h2>
        <button
          onClick={handleSaveSettings}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition-colors"
        >
          Speichern
        </button>
      </div>

      <div className="bg-dark-brown p-4 rounded border border-warm-brown">
        <h3 className="text-warm-beige font-serif mb-3">Allgemeine Einstellungen</h3>
        
        <div className="space-y-4">
          <div>
            <label className="block text-warm-beige mb-2">Restaurant Name</label>
            <input
              type="text"
              value={localSettings.restaurantName}
              onChange={(e) => setLocalSettings({...localSettings, restaurantName: e.target.value})}
              className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige"
            />
          </div>
          
          <div>
            <label className="block text-warm-beige mb-2">Haupt E-Mail</label>
            <input
              type="email"
              value={localSettings.contactEmail}
              onChange={(e) => setLocalSettings({...localSettings, contactEmail: e.target.value})}
              className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige"
            />
          </div>
          
          <div>
            <label className="block text-warm-beige mb-2">Haupt Telefon</label>
            <input
              type="text"
              value={localSettings.phone}
              onChange={(e) => setLocalSettings({...localSettings, phone: e.target.value})}
              className="w-full p-3 bg-medium-brown border border-warm-brown rounded text-warm-beige"
            />
          </div>
        </div>
      </div>

      <div className="bg-dark-brown p-4 rounded border border-warm-brown">
        <h3 className="text-warm-beige font-serif mb-3">Daten-Management</h3>
        
        <div className="space-y-4">
          <div>
            <button
              onClick={() => {
                const dataStr = JSON.stringify(content, null, 2);
                const dataBlob = new Blob([dataStr], {type: 'application/json'});
                const url = URL.createObjectURL(dataBlob);
                const link = document.createElement('a');
                link.href = url;
                link.download = 'jimmys-website-backup.json';
                link.click();
              }}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors mr-3"
            >
              Backup exportieren
            </button>
            
            <input
              type="file"
              accept=".json"
              onChange={(e) => {
                const file = e.target.files[0];
                if (file) {
                  const reader = new FileReader();
                  reader.onload = (event) => {
                    try {
                      const importedData = JSON.parse(event.target.result);
                      if (confirm('Wirklich alle Daten importieren? Dies überschreibt alle aktuellen Einstellungen!')) {
                        setContent(importedData);
                        localStorage.setItem('adminContent', JSON.stringify(importedData));
                        alert('Daten erfolgreich importiert!');
                      }
                    } catch (error) {
                      alert('Fehler beim Importieren der Datei!');
                    }
                  };
                  reader.readAsText(file);
                }
              }}
              className="bg-medium-brown border border-warm-brown text-warm-beige rounded px-3 py-2"
            />
          </div>
          
          <div>
            <button
              onClick={() => {
                if (confirm('Wirklich alle Daten löschen? Dies kann nicht rückgängig gemacht werden!')) {
                  localStorage.removeItem('adminContent');
                  window.location.reload();
                }
              }}
              className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition-colors"
            >
              Alle Daten zurücksetzen
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};