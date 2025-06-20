import React, { useState, useEffect } from 'react';

const Standorte = () => {
  const [locationsData, setLocationsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadLocationsData();
  }, []);

  const loadLocationsData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/standorte-enhanced`);
      if (response.ok) {
        const data = await response.json();
        console.log('Loaded enhanced locations data:', data);
        
        // Parse JSON strings if needed
        if (typeof data.neustadt === 'string') {
          try {
            data.neustadt = JSON.parse(data.neustadt);
          } catch (e) {
            console.warn('Failed to parse neustadt JSON:', e);
            data.neustadt = {};
          }
        }
        
        if (typeof data.grossenbrode === 'string') {
          try {
            data.grossenbrode = JSON.parse(data.grossenbrode);
          } catch (e) {
            console.warn('Failed to parse grossenbrode JSON:', e);
            data.grossenbrode = {};
          }
        }
        
        if (typeof data.info_section === 'string') {
          try {
            data.info_section = JSON.parse(data.info_section);
          } catch (e) {
            console.warn('Failed to parse info_section JSON:', e);
            data.info_section = { sections: [] };
          }
        }
        
        setLocationsData(data);
      } else {
        throw new Error('Failed to load locations data');
      }
    } catch (error) {
      console.error('Error loading locations:', error);
      setError('Fehler beim Laden der Standort-Daten. Bitte versuchen Sie es später erneut.');
    } finally {
      setLoading(false);
    }
  };

  // Google Maps navigation function
  const openGoogleMaps = (address) => {
    const encodedAddress = encodeURIComponent(address);
    const googleMapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${encodedAddress}`;
    window.open(googleMapsUrl, '_blank');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="text-warm-beige text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-warm-beige mx-auto mb-4"></div>
          <p className="text-xl">Lade Standorte...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="text-red-400 text-center max-w-md mx-auto">
          <p className="text-xl mb-4">{error}</p>
          <button
            onClick={loadLocationsData}
            className="bg-warm-beige text-dark-brown px-6 py-3 rounded-lg hover:bg-light-beige transition-colors"
          >
            Erneut versuchen
          </button>
        </div>
      </div>
    );
  }

  if (!locationsData) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="text-warm-beige text-center">
          <p className="text-xl">Keine Standortdaten verfügbar</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Elegant Header Section with Background */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('${locationsData.header_background || 'https://images.pexels.com/photos/26626726/pexels-photo-26626726.jpeg'}')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              {locationsData.page_title || 'Unsere Standorte'}
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              {locationsData.page_subtitle || 'Besuchen Sie uns an der malerischen Ostseeküste'}
            </p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-16">
        <div className="grid lg:grid-cols-2 gap-16 max-w-7xl mx-auto">
          {/* Neustadt Location - Enhanced */}
          <div className="bg-dark-brown rounded-xl border border-warm-brown overflow-hidden shadow-2xl">
            <div className="relative">
              <img 
                src={locationsData.neustadt?.image || "https://images.unsplash.com/photo-1665758564776-f2aa6b41327e"} 
                alt="Jimmy's Tapas Bar Neustadt" 
                className="w-full h-72 object-cover"
              />
              <div className="absolute top-4 left-4 bg-warm-beige text-dark-brown px-4 py-2 rounded-lg">
                <span className="font-serif font-semibold">{locationsData.neustadt?.badge || 'Hauptstandort'}</span>
              </div>
            </div>
            <div className="p-8">
              <h2 className="text-3xl font-serif text-warm-beige mb-6 tracking-wide">
                {locationsData.neustadt?.name || "Jimmy's Tapas Bar Neustadt"}
              </h2>
              <div className="space-y-6 text-light-beige">
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-xl text-dark-brown">📍</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-warm-beige mb-1">Adresse</h3>
                    <p className="font-light text-lg">{locationsData.neustadt?.address_line1 || 'Am Strande 21'}</p>
                    <p className="font-light">{locationsData.neustadt?.address_line2 || '23730 Neustadt in Holstein'}</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-xl text-dark-brown">🕒</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-warm-beige mb-1">Öffnungszeiten</h3>
                    <p className="font-light">{locationsData.neustadt?.opening_hours || 'Mo-So: 12:00–22:00 Uhr'}</p>
                    <p className="text-sm text-warm-beige font-light">{locationsData.neustadt?.season_note || '(Sommersaison)'}</p>
                    <p className="text-sm text-orange-400 font-light">{locationsData.neustadt?.winter_note || 'Winterbetrieb unregelmäßig'}</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-xl text-dark-brown">📞</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-warm-beige mb-1">Kontakt</h3>
                    <p className="font-light">{locationsData.neustadt?.phone || '+49 (0) 4561 123456'}</p>
                    <p className="font-light text-sm">{locationsData.neustadt?.email || 'neustadt@jimmys-tapasbar.de'}</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-xl text-dark-brown">🏖️</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-warm-beige mb-1">Besonderheiten</h3>
                    <p className="font-light text-sm">{locationsData.neustadt?.features_line1 || 'Direkt am Strand • Terrasse mit Meerblick'}</p>
                    <p className="font-light text-sm">{locationsData.neustadt?.features_line2 || 'Parkplätze vorhanden • Familienfreundlich'}</p>
                  </div>
                </div>
              </div>
              <div className="mt-8">
                <button 
                  onClick={() => openGoogleMaps(`${locationsData.neustadt?.address_line1 || 'Am Strande 21'}, ${locationsData.neustadt?.address_line2 || '23730 Neustadt in Holstein'}`)}
                  className="bg-warm-beige hover:bg-light-beige text-dark-brown px-6 py-3 rounded-lg font-medium transition-colors w-full"
                >
                  Route planen
                </button>
              </div>
            </div>
          </div>

          {/* Großenbrode Location - Enhanced */}
          <div className="bg-dark-brown rounded-xl border border-warm-brown overflow-hidden shadow-2xl">
            <div className="relative">
              <img 
                src={locationsData.grossenbrode?.image || "https://images.unsplash.com/photo-1665758564796-5162ff406254"} 
                alt="Jimmy's Tapas Bar Großenbrode" 
                className="w-full h-72 object-cover"
              />
              <div className="absolute top-4 left-4 bg-orange-500 text-white px-4 py-2 rounded-lg">
                <span className="font-serif font-semibold">{locationsData.grossenbrode?.badge || 'Zweigstelle'}</span>
              </div>
            </div>
            <div className="p-8">
              <h2 className="text-3xl font-serif text-warm-beige mb-6 tracking-wide">
                {locationsData.grossenbrode?.name || "Jimmy's Tapas Bar Großenbrode"}
              </h2>
              <div className="space-y-6 text-light-beige">
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-xl text-dark-brown">📍</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-warm-beige mb-1">Adresse</h3>
                    <p className="font-light text-lg">{locationsData.grossenbrode?.address_line1 || 'Südstrand 54'}</p>
                    <p className="font-light">{locationsData.grossenbrode?.address_line2 || '23755 Großenbrode'}</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-xl text-dark-brown">🕒</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-warm-beige mb-1">Öffnungszeiten</h3>
                    <p className="font-light">{locationsData.grossenbrode?.opening_hours || 'Mo-So: 12:00–22:00 Uhr'}</p>
                    <p className="text-sm text-warm-beige font-light">{locationsData.grossenbrode?.season_note || '(Sommersaison)'}</p>
                    <p className="text-sm text-orange-400 font-light">{locationsData.grossenbrode?.winter_note || 'Winterbetrieb unregelmäßig'}</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-xl text-dark-brown">📞</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-warm-beige mb-1">Kontakt</h3>
                    <p className="font-light">{locationsData.grossenbrode?.phone || '+49 (0) 4561 789012'}</p>
                    <p className="font-light text-sm">{locationsData.grossenbrode?.email || 'grossenbrode@jimmys-tapasbar.de'}</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-xl text-dark-brown">🌊</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-warm-beige mb-1">Besonderheiten</h3>
                    <p className="font-light text-sm">{locationsData.grossenbrode?.features_line1 || 'Strandnähe • Gemütliche Atmosphäre'}</p>
                    <p className="font-light text-sm">{locationsData.grossenbrode?.features_line2 || 'Kostenlose Parkplätze • Hundefreundlich'}</p>
                  </div>
                </div>
              </div>
              <div className="mt-8">
                <button 
                  onClick={() => openGoogleMaps(`${locationsData.grossenbrode?.address_line1 || 'Südstrand 54'}, ${locationsData.grossenbrode?.address_line2 || '23755 Großenbrode'}`)}
                  className="bg-warm-beige hover:bg-light-beige text-dark-brown px-6 py-3 rounded-lg font-medium transition-colors w-full"
                >
                  Route planen
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Enhanced "Gut zu wissen" Section with Images */}
        <div className="mt-16 bg-dark-brown rounded-xl border border-warm-brown p-8">
          <h3 className="text-3xl font-serif text-warm-beige mb-8 text-center tracking-wide">
            Gut zu wissen
          </h3>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-20 h-20 mx-auto mb-4 rounded-xl overflow-hidden">
                <img 
                  src="https://images.unsplash.com/photo-1449824913935-59a10b8d2000?ixlib=rb-4.0.3&auto=format&fit=crop&w=80&q=80"
                  alt="Ostsee-Ambiente"
                  className="w-full h-full object-cover"
                />
              </div>
              <h4 className="text-xl font-serif text-warm-beige mb-2">Ostsee-Ambiente</h4>
              <p className="text-light-beige font-light text-sm">
                Erleben Sie authentische Tapas-Kultur direkt an der deutschen Ostseeküste mit herrlichem Meerblick.
              </p>
            </div>
            <div className="text-center">
              <div className="w-20 h-20 mx-auto mb-4 rounded-xl overflow-hidden">
                <img 
                  src="https://images.unsplash.com/photo-1544148103-0773bf10d330?ixlib=rb-4.0.3&auto=format&fit=crop&w=80&q=80"
                  alt="Frische Zutaten"
                  className="w-full h-full object-cover"
                />
              </div>
              <h4 className="text-xl font-serif text-warm-beige mb-2">Frische Zutaten</h4>
              <p className="text-light-beige font-light text-sm">
                Täglich frische Zutaten aus der Region kombiniert mit authentischen spanischen Spezialitäten.
              </p>
            </div>
            <div className="text-center">
              <div className="w-20 h-20 mx-auto mb-4 rounded-xl overflow-hidden">
                <img 
                  src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3&auto=format&fit=crop&w=80&q=80"
                  alt="Gemütliche Atmosphäre"
                  className="w-full h-full object-cover"
                />
              </div>
              <h4 className="text-xl font-serif text-warm-beige mb-2">Entspannte Atmosphäre</h4>
              <p className="text-light-beige font-light text-sm">
                Genießen Sie mediterrane Gelassenheit in familiärer Atmosphäre - perfekt für entspannte Abende.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Standorte;