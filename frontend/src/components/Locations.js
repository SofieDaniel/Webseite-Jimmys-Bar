import React, { useState, useEffect } from 'react';

const Locations = () => {
  const [locationData, setLocationData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadLocationData = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/standorte-enhanced`);
        if (response.ok) {
          const data = await response.json();
          setLocationData(data);
        }
      } catch (error) {
        console.error('Error loading location data:', error);
      } finally {
        setLoading(false);
      }
    };
    loadLocationData();
  }, []);

  // Fallback data mit korrekten Adressen und Öffnungszeiten
  const defaultData = {
    page_title: "Unsere Standorte",
    page_subtitle: "Besuchen Sie uns an der malerischen Ostseeküste",
    neustadt: {
      name: "Neustadt in Holstein",
      address: "Am Strande 21 Promenade, 23730 Neustadt in Holstein",
      phone: "015735256793",
      email: "info@jimmys-tapasbar.de",
      opening_hours: {
        "Montag": "16:00 - 23:00", "Dienstag": "16:00 - 23:00", "Mittwoch": "16:00 - 23:00",
        "Donnerstag": "16:00 - 23:00", "Freitag": "16:00 - 24:00", "Samstag": "12:00 - 24:00", "Sonntag": "12:00 - 23:00"
      },
      features: ["Direkte Strandlage", "Große Terrasse", "Familienfreundlich", "Parkplatz kostenlos"]
    },
    grossenbrode: {
      name: "Großenbrode",
      address: "Südstrand 54 Promenade, 23755 Großenbrode",
      phone: "015782226373",
      email: "info@jimmys-tapasbar.de",
      opening_hours: {
        "Montag": "16:00 - 23:00", "Dienstag": "16:00 - 23:00", "Mittwoch": "16:00 - 23:00",
        "Donnerstag": "16:00 - 23:00", "Freitag": "16:00 - 24:00", "Samstag": "12:00 - 24:00", "Sonntag": "12:00 - 23:00"
      },
      features: ["Panorama-Meerblick", "Ruhige Lage", "Romantische Atmosphäre", "Sonnenuntergänge"]
    }
  };

  const data = locationData || defaultData;

  // Google Maps Route planen
  const planRoute = (address) => {
    const encodedAddress = encodeURIComponent(address);
    const googleMapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${encodedAddress}`;
    window.open(googleMapsUrl, '_blank');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-warm-beige"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Header Section mit spanischem Hintergrundbild */}
      <div className="relative overflow-hidden bg-gradient-to-r from-dark-brown via-medium-brown to-dark-brown">
        <div className="absolute inset-0 bg-black bg-opacity-50"></div>
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage: "url('https://images.unsplash.com/photo-1571197119738-26123cb0d22f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80')"
          }}
        ></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <div className="max-w-4xl mx-auto">
              <h1 className="text-6xl md:text-7xl font-serif text-warm-beige mb-6 tracking-wide drop-shadow-lg">
                {data.page_title}
              </h1>
              <div className="bg-dark-brown/40 backdrop-blur-sm rounded-xl p-6 border border-warm-beige/30">
                <p className="text-xl md:text-2xl text-light-beige font-light leading-relaxed">
                  {data.page_subtitle}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-7xl mx-auto">
          
          {/* Standorte Grid */}
          <div className="grid lg:grid-cols-2 gap-12">
            
            {/* Neustadt Location */}
            <div className="bg-medium-brown/50 rounded-xl overflow-hidden border border-warm-beige/20 shadow-2xl">
              {/* Location Image */}
              <div className="h-64 bg-cover bg-center relative" style={{
                backgroundImage: "url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80')"
              }}>
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                <div className="absolute bottom-4 left-4">
                  <h2 className="text-3xl font-serif text-warm-beige drop-shadow-lg">{data.neustadt.name}</h2>
                </div>
              </div>

              {/* Location Details */}
              <div className="p-8">
                {/* Contact Info */}
                <div className="grid md:grid-cols-2 gap-6 mb-8">
                  <div className="space-y-4">
                    <div className="bg-dark-brown/50 rounded-lg p-4">
                      <div className="flex items-center mb-2">
                        <span className="text-warm-beige text-lg mr-2">📍</span>
                        <h4 className="font-semibold text-warm-beige">Adresse</h4>
                      </div>
                      <p className="text-light-beige text-sm">{data.neustadt.address}</p>
                    </div>
                    
                    <div className="bg-dark-brown/50 rounded-lg p-4">
                      <div className="flex items-center mb-2">
                        <span className="text-warm-beige text-lg mr-2">📞</span>
                        <h4 className="font-semibold text-warm-beige">Telefon</h4>
                      </div>
                      <p className="text-light-beige text-sm">{data.neustadt.phone}</p>
                    </div>

                    <div className="bg-dark-brown/50 rounded-lg p-4">
                      <div className="flex items-center mb-2">
                        <span className="text-warm-beige text-lg mr-2">📧</span>
                        <h4 className="font-semibold text-warm-beige">E-Mail</h4>
                      </div>
                      <p className="text-light-beige text-sm">{data.neustadt.email}</p>
                    </div>
                  </div>

                  {/* Opening Hours */}
                  <div className="bg-dark-brown/50 rounded-lg p-4">
                    <div className="flex items-center mb-4">
                      <span className="text-warm-beige text-lg mr-2">🕒</span>
                      <h4 className="font-semibold text-warm-beige">Öffnungszeiten</h4>
                    </div>
                    <div className="space-y-1">
                      {Object.entries(data.neustadt.opening_hours).map(([day, hours]) => (
                        <div key={day} className="flex justify-between text-sm">
                          <span className="text-light-beige">{day}:</span>
                          <span className="text-warm-beige">{hours}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Features */}
                <div className="mb-6">
                  <h4 className="font-semibold text-warm-beige mb-3 flex items-center">
                    <span className="text-lg mr-2">✨</span>
                    Besonderheiten
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {data.neustadt.features.map((feature, index) => (
                      <span key={index} className="bg-warm-beige/20 text-warm-beige px-3 py-1 rounded-full text-sm">
                        {feature}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Action Button - Nur Route planen */}
                <div className="flex gap-4">
                  <button 
                    onClick={() => planRoute(data.neustadt.address)}
                    className="w-full bg-warm-beige text-dark-brown py-3 rounded-lg font-semibold hover:bg-orange-500 hover:text-white transition-all duration-300 flex items-center justify-center"
                  >
                    <span className="mr-2">🗺️</span>
                    Route planen
                  </button>
                </div>
              </div>
            </div>

            {/* Großenbrode Location */}
            <div className="bg-medium-brown/50 rounded-xl overflow-hidden border border-warm-beige/20 shadow-2xl">
              {/* Location Image */}
              <div className="h-64 bg-cover bg-center relative" style={{
                backgroundImage: "url('https://images.unsplash.com/photo-1559925393-8be0ec4767c8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2071&q=80')"
              }}>
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                <div className="absolute bottom-4 left-4">
                  <h2 className="text-3xl font-serif text-warm-beige drop-shadow-lg">{data.grossenbrode.name}</h2>
                </div>
              </div>

              {/* Location Details */}
              <div className="p-8">
                {/* Contact Info */}
                <div className="grid md:grid-cols-2 gap-6 mb-8">
                  <div className="space-y-4">
                    <div className="bg-dark-brown/50 rounded-lg p-4">
                      <div className="flex items-center mb-2">
                        <span className="text-warm-beige text-lg mr-2">📍</span>
                        <h4 className="font-semibold text-warm-beige">Adresse</h4>
                      </div>
                      <p className="text-light-beige text-sm">{data.grossenbrode.address}</p>
                    </div>
                    
                    <div className="bg-dark-brown/50 rounded-lg p-4">
                      <div className="flex items-center mb-2">
                        <span className="text-warm-beige text-lg mr-2">📞</span>
                        <h4 className="font-semibold text-warm-beige">Telefon</h4>
                      </div>
                      <p className="text-light-beige text-sm">{data.grossenbrode.phone}</p>
                    </div>

                    <div className="bg-dark-brown/50 rounded-lg p-4">
                      <div className="flex items-center mb-2">
                        <span className="text-warm-beige text-lg mr-2">📧</span>
                        <h4 className="font-semibold text-warm-beige">E-Mail</h4>
                      </div>
                      <p className="text-light-beige text-sm">{data.grossenbrode.email}</p>
                    </div>
                  </div>

                  {/* Opening Hours */}
                  <div className="bg-dark-brown/50 rounded-lg p-4">
                    <div className="flex items-center mb-4">
                      <span className="text-warm-beige text-lg mr-2">🕒</span>
                      <h4 className="font-semibold text-warm-beige">Öffnungszeiten</h4>
                    </div>
                    <div className="space-y-1">
                      {Object.entries(data.grossenbrode.opening_hours).map(([day, hours]) => (
                        <div key={day} className="flex justify-between text-sm">
                          <span className="text-light-beige">{day}:</span>
                          <span className="text-warm-beige">{hours}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Features */}
                <div className="mb-6">
                  <h4 className="font-semibold text-warm-beige mb-3 flex items-center">
                    <span className="text-lg mr-2">✨</span>
                    Besonderheiten
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {data.grossenbrode.features.map((feature, index) => (
                      <span key={index} className="bg-warm-beige/20 text-warm-beige px-3 py-1 rounded-full text-sm">
                        {feature}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Action Button - Nur Route planen */}
                <div className="flex gap-4">
                  <button 
                    onClick={() => planRoute(data.grossenbrode.address)}
                    className="w-full bg-warm-beige text-dark-brown py-3 rounded-lg font-semibold hover:bg-orange-500 hover:text-white transition-all duration-300 flex items-center justify-center"
                  >
                    <span className="mr-2">🗺️</span>
                    Route planen
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Spanisches Sprichwort Section */}
          <div className="mt-16 text-center">
            <div className="bg-medium-brown/30 rounded-xl p-8 border border-warm-beige/20">
              <h3 className="text-2xl font-serif text-warm-beige mb-6">Bienvenidos a Jimmy's Tapas-Bar</h3>
              
              <div className="max-w-4xl mx-auto space-y-6">
                <div className="bg-dark-brown/40 rounded-lg p-6">
                  <p className="text-xl text-warm-beige font-serif mb-2 italic">
                    "El buen comer y el buen beber, hacen la vida placer"
                  </p>
                  <p className="text-lg text-light-beige">
                    "Gutes Essen und gutes Trinken machen das Leben zum Vergnügen"
                  </p>
                </div>
                
                <p className="text-light-beige leading-relaxed">
                  Wir laden Sie herzlich ein, 
                  die Vielfalt der spanischen Küche an der Ostsee zu entdecken. Erleben Sie authentische Tapas 
                  und mediterrane Spezialitäten in einzigartiger Strandatmosphäre.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Locations;