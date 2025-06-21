import React, { useState, useEffect } from 'react';

const Locations = () => {
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

  if (!locationsData || !locationsData.neustadt || !locationsData.grossenbrode) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="text-warm-beige text-center">
          <p className="text-xl">Keine Standortdaten verfügbar</p>
          <button
            onClick={loadLocationsData}
            className="mt-4 bg-warm-beige text-dark-brown px-6 py-3 rounded-lg hover:bg-light-beige transition-colors"
          >
            Neu laden
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Header Section */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('${locationsData.header_background || 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f'}')`}}>
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
          
          {/* Neustadt Location */}
          <div className="bg-medium-brown rounded-xl border border-warm-brown overflow-hidden shadow-2xl">
            <div className="relative">
              <img 
                src={locationsData.neustadt.image_url || "https://images.unsplash.com/photo-1571197119738-26123cb0d22f"} 
                alt="Jimmy's Tapas Bar Neustadt" 
                className="w-full h-72 object-cover"
              />
              <div className="absolute top-4 left-4 bg-warm-beige text-dark-brown px-4 py-2 rounded-lg">
                <span className="font-serif font-semibold">Hauptstandort</span>
              </div>
            </div>
            <div className="p-8">
              <h2 className="text-3xl font-serif text-warm-beige mb-6 tracking-wide">
                {locationsData.neustadt.name}
              </h2>
              
              <div className="space-y-6 text-light-beige">
                {/* Address */}
                <div className="flex items-start space-x-4">
                  <div className="w-16 h-16 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0 overflow-hidden">
                    <img 
                      src="https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9" 
                      alt="Adresse"
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div>
                    <h3 className="font-semibold text-warm-beige mb-1">Adresse</h3>
                    <p className="font-light text-lg">{locationsData.neustadt.address}</p>
                  </div>
                </div>

                {/* Contact */}
                <div className="flex items-start space-x-4">
                  <div className="w-16 h-16 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0 overflow-hidden">
                    <img 
                      src="https://images.unsplash.com/photo-1556742049-0cfed4f6a45d" 
                      alt="Kontakt"
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div>
                    <h3 className="font-semibold text-warm-beige mb-1">Kontakt</h3>
                    <p className="font-light text-lg">{locationsData.neustadt.phone}</p>
                    <p className="font-light">{locationsData.neustadt.email}</p>
                  </div>
                </div>

                {/* Opening Hours */}
                {locationsData.neustadt.opening_hours && (
                  <div className="flex items-start space-x-4">
                    <div className="w-16 h-16 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0 overflow-hidden">
                      <img 
                        src="https://images.unsplash.com/photo-1501139083538-0139583c060f" 
                        alt="Öffnungszeiten"
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div>
                      <h3 className="font-semibold text-warm-beige mb-2">Öffnungszeiten</h3>
                      <div className="space-y-1 text-sm">
                        {Object.entries(locationsData.neustadt.opening_hours).map(([day, hours]) => (
                          <div key={day} className="flex justify-between">
                            <span className="w-20">{day}:</span>
                            <span>{hours}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {/* Features */}
                {locationsData.neustadt.features && locationsData.neustadt.features.length > 0 && (
                  <div className="flex items-start space-x-4">
                    <div className="w-16 h-16 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0 overflow-hidden">
                      <img 
                        src="https://images.unsplash.com/photo-1414235077428-338989a2e8c0" 
                        alt="Besonderheiten"
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div>
                      <h3 className="font-semibold text-warm-beige mb-2">Besonderheiten</h3>
                      <div className="flex flex-wrap gap-2">
                        {locationsData.neustadt.features.map((feature, index) => (
                          <span key={index} className="bg-dark-brown text-warm-beige px-3 py-1 rounded-full text-sm">
                            {feature}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {/* Description */}
                {locationsData.neustadt.description && (
                  <div className="bg-dark-brown p-4 rounded-lg">
                    <p className="text-light-beige font-light italic">
                      {locationsData.neustadt.description}
                    </p>
                  </div>
                )}

                {/* Navigation Button */}
                <button
                  onClick={() => openGoogleMaps(locationsData.neustadt.address)}
                  className="w-full bg-warm-beige text-dark-brown py-3 px-6 rounded-lg font-medium hover:bg-light-beige transition-colors flex items-center justify-center space-x-2"
                >
                  <span>🗺️</span>
                  <span>Route planen</span>
                </button>
              </div>
            </div>
          </div>

          {/* Großenbrode Location */}
          <div className="bg-medium-brown rounded-xl border border-warm-brown overflow-hidden shadow-2xl">
            <div className="relative">
              <img 
                src={locationsData.grossenbrode.image_url || "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d"} 
                alt="Jimmy's Tapas Bar Großenbrode" 
                className="w-full h-72 object-cover"
              />
              <div className="absolute top-4 left-4 bg-warm-beige text-dark-brown px-4 py-2 rounded-lg">
                <span className="font-serif font-semibold">Panoramablick</span>
              </div>
            </div>
            <div className="p-8">
              <h2 className="text-3xl font-serif text-warm-beige mb-6 tracking-wide">
                {locationsData.grossenbrode.name}
              </h2>
              
              <div className="space-y-6 text-light-beige">
                {/* Address */}
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-xl text-dark-brown">📍</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-warm-beige mb-1">Adresse</h3>
                    <p className="font-light text-lg">{locationsData.grossenbrode.address}</p>
                  </div>
                </div>

                {/* Contact */}
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-xl text-dark-brown">📞</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-warm-beige mb-1">Kontakt</h3>
                    <p className="font-light text-lg">{locationsData.grossenbrode.phone}</p>
                    <p className="font-light">{locationsData.grossenbrode.email}</p>
                  </div>
                </div>

                {/* Opening Hours */}
                {locationsData.grossenbrode.opening_hours && (
                  <div className="flex items-start space-x-4">
                    <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                      <span className="text-xl text-dark-brown">🕐</span>
                    </div>
                    <div>
                      <h3 className="font-semibold text-warm-beige mb-2">Öffnungszeiten</h3>
                      <div className="space-y-1 text-sm">
                        {Object.entries(locationsData.grossenbrode.opening_hours).map(([day, hours]) => (
                          <div key={day} className="flex justify-between">
                            <span className="w-20">{day}:</span>
                            <span>{hours}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {/* Features */}
                {locationsData.grossenbrode.features && locationsData.grossenbrode.features.length > 0 && (
                  <div className="flex items-start space-x-4">
                    <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                      <span className="text-xl text-dark-brown">✨</span>
                    </div>
                    <div>
                      <h3 className="font-semibold text-warm-beige mb-2">Besonderheiten</h3>
                      <div className="flex flex-wrap gap-2">
                        {locationsData.grossenbrode.features.map((feature, index) => (
                          <span key={index} className="bg-dark-brown text-warm-beige px-3 py-1 rounded-full text-sm">
                            {feature}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {/* Description */}
                {locationsData.grossenbrode.description && (
                  <div className="bg-dark-brown p-4 rounded-lg">
                    <p className="text-light-beige font-light italic">
                      {locationsData.grossenbrode.description}
                    </p>
                  </div>
                )}

                {/* Navigation Button */}
                <button
                  onClick={() => openGoogleMaps(locationsData.grossenbrode.address)}
                  className="w-full bg-warm-beige text-dark-brown py-3 px-6 rounded-lg font-medium hover:bg-light-beige transition-colors flex items-center justify-center space-x-2"
                >
                  <span>🗺️</span>
                  <span>Route planen</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Additional Info Section */}
        {locationsData.info_section && locationsData.info_section.sections && locationsData.info_section.sections.length > 0 && (
          <div className="mt-16 max-w-6xl mx-auto">
            <h2 className="text-4xl font-serif text-warm-beige text-center mb-12">
              Wissenswertes
            </h2>
            <div className="grid md:grid-cols-3 gap-8">
              {locationsData.info_section.sections.map((section, index) => (
                <div key={index} className="bg-medium-brown rounded-xl overflow-hidden border border-warm-brown shadow-lg">
                  {/* Image Header */}
                  <div className="h-48 overflow-hidden">
                    <img 
                      src={section.image || `https://images.unsplash.com/photo-${1449824913935 + index}`} 
                      alt={section.title}
                      className="w-full h-full object-cover hover:scale-110 transition-transform duration-300"
                    />
                  </div>
                  {/* Content */}
                  <div className="p-6 text-center">
                    <div className="text-3xl mb-3">{section.icon}</div>
                    <h3 className="text-xl font-serif text-warm-beige mb-4">{section.title}</h3>
                    <p className="text-light-beige font-light leading-relaxed">{section.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Locations;