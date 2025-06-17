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
      
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/locations`);
      if (response.ok) {
        const data = await response.json();
        console.log('Loaded locations data:', data);
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

  const formatPhoneNumber = (phone) => {
    return phone?.replace(/^\+49\s?/, '0').replace(/\s/g, ' ') || '';
  };

  const getGoogleMapsUrl = (location) => {
    if (location.coordinates) {
      return `https://www.google.com/maps/dir/?api=1&destination=${location.coordinates.lat},${location.coordinates.lng}`;
    }
    return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(location.address)}`;
  };

  const getReservationUrl = (location) => {
    return `tel:${location.phone}`;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-warm-white py-16">
        <div className="container mx-auto px-4 text-center">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-300 rounded mb-4 mx-auto max-w-xs"></div>
            <div className="h-4 bg-gray-300 rounded mb-8 mx-auto max-w-md"></div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {[1, 2].map((i) => (
                <div key={i} className="bg-white rounded-xl shadow-lg p-6">
                  <div className="h-48 bg-gray-300 rounded-lg mb-4"></div>
                  <div className="h-6 bg-gray-300 rounded mb-2"></div>
                  <div className="h-4 bg-gray-300 rounded mb-4 w-3/4"></div>
                  <div className="space-y-2">
                    <div className="h-4 bg-gray-300 rounded"></div>
                    <div className="h-4 bg-gray-300 rounded w-5/6"></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-warm-white py-16">
        <div className="container mx-auto px-4 text-center">
          <div className="max-w-md mx-auto bg-red-50 border border-red-200 rounded-lg p-6">
            <div className="text-red-600 text-6xl mb-4">⚠️</div>
            <h2 className="text-xl font-semibold text-red-800 mb-2">Fehler beim Laden</h2>
            <p className="text-red-600 mb-4">{error}</p>
            <button
              onClick={loadLocationsData}
              className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition-colors"
            >
              Erneut versuchen
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!locationsData || !locationsData.locations || locationsData.locations.length === 0) {
    return (
      <div className="min-h-screen bg-warm-white py-16">
        <div className="container mx-auto px-4 text-center">
          <div className="max-w-md mx-auto">
            <div className="text-6xl mb-4">🏖️</div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-2">Keine Standorte verfügbar</h2>
            <p className="text-gray-600">Derzeit sind keine Standortinformationen verfügbar.</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-warm-white">
      {/* Hero Section */}
      <section className="py-16 bg-gradient-to-br from-dark-brown to-warm-brown">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-5xl font-serif text-warm-beige mb-4 tracking-wide">
            {locationsData.page_title || 'Unsere Standorte'}
          </h1>
          <p className="text-lg text-light-beige max-w-2xl mx-auto">
            {locationsData.page_description || 'Besuchen Sie uns an einem unserer beiden Standorte'}
          </p>
        </div>
      </section>

      {/* Locations Grid */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
            {locationsData.locations.map((location, index) => (
              <div key={location.id || index} className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
                {/* Location Image */}
                <div className="h-64 bg-gray-300 overflow-hidden">
                  {location.image_url ? (
                    <img
                      src={location.image_url}
                      alt={location.name}
                      className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                      onError={(e) => {
                        e.target.style.display = 'none';
                        e.target.nextElementSibling.style.display = 'flex';
                      }}
                    />
                  ) : null}
                  <div className="w-full h-full bg-gradient-to-br from-dark-brown to-warm-brown flex items-center justify-center" style={{ display: location.image_url ? 'none' : 'flex' }}>
                    <div className="text-warm-beige text-6xl">🏖️</div>
                  </div>
                </div>

                {/* Location Content */}
                <div className="p-6">
                  <h2 className="text-2xl font-serif text-dark-brown mb-2">{location.name}</h2>
                  <p className="text-gray-600 mb-4">{location.description}</p>

                  {/* Address */}
                  <div className="mb-4">
                    <h3 className="font-semibold text-dark-brown mb-2 flex items-center">
                      <span className="mr-2">📍</span>
                      Adresse
                    </h3>
                    <p className="text-gray-700">{location.address}</p>
                  </div>

                  {/* Contact */}
                  <div className="mb-4">
                    <h3 className="font-semibold text-dark-brown mb-2 flex items-center">
                      <span className="mr-2">📞</span>
                      Kontakt
                    </h3>
                    <p className="text-gray-700">
                      Tel: <a href={`tel:${location.phone}`} className="text-warm-brown hover:underline">
                        {formatPhoneNumber(location.phone)}
                      </a>
                    </p>
                    {location.email && (
                      <p className="text-gray-700">
                        E-Mail: <a href={`mailto:${location.email}`} className="text-warm-brown hover:underline">
                          {location.email}
                        </a>
                      </p>
                    )}
                  </div>

                  {/* Opening Hours */}
                  {location.opening_hours && (
                    <div className="mb-4">
                      <h3 className="font-semibold text-dark-brown mb-2 flex items-center">
                        <span className="mr-2">🕒</span>
                        Öffnungszeiten
                      </h3>
                      <div className="text-sm text-gray-700 space-y-1">
                        {Object.entries(location.opening_hours).map(([day, hours]) => (
                          <div key={day} className="flex justify-between">
                            <span className="font-medium">{day}:</span>
                            <span>{hours}</span>
                          </div>
                        ))}
                      </div>
                      {location.seasonal_note && (
                        <p className="text-xs text-warm-brown mt-2 italic">
                          {location.seasonal_note}
                        </p>
                      )}
                    </div>
                  )}

                  {/* Specialties */}
                  {location.specialties && location.specialties.length > 0 && (
                    <div className="mb-6">
                      <h3 className="font-semibold text-dark-brown mb-2 flex items-center">
                        <span className="mr-2">✨</span>
                        Besonderheiten
                      </h3>
                      <div className="flex flex-wrap gap-2">
                        {location.specialties.map((specialty, idx) => (
                          <span
                            key={idx}
                            className="bg-warm-beige text-dark-brown px-3 py-1 rounded-full text-sm"
                          >
                            {specialty}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Action Buttons */}
                  <div className="flex flex-col sm:flex-row gap-3">
                    <a
                      href={getGoogleMapsUrl(location)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex-1 bg-warm-brown text-white text-center py-3 px-4 rounded-lg hover:bg-dark-brown transition-colors"
                    >
                      📍 Route planen
                    </a>
                    <a
                      href={getReservationUrl(location)}
                      className="flex-1 bg-warm-beige text-dark-brown text-center py-3 px-4 rounded-lg hover:bg-light-beige transition-colors"
                    >
                      📞 Reservieren
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Info Section - "Gut zu wissen" */}
      {locationsData.info_sections && locationsData.info_sections.length > 0 && (
        <section className="py-16 bg-light-beige">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-serif text-dark-brown text-center mb-12">
              Gut zu wissen
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
              {locationsData.info_sections.map((info, index) => (
                <div key={info.id || index} className="text-center">
                  <div className="text-4xl mb-4">{info.icon}</div>
                  <h3 className="text-xl font-semibold text-dark-brown mb-3">
                    {info.title}
                  </h3>
                  <p className="text-gray-700 leading-relaxed">
                    {info.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* General Info */}
      {locationsData.general_info && (
        <section className="py-12 bg-warm-brown">
          <div className="container mx-auto px-4 text-center">
            <div className="max-w-2xl mx-auto text-warm-beige">
              {locationsData.general_info.special_note && (
                <p className="text-lg mb-4">{locationsData.general_info.special_note}</p>
              )}
              {locationsData.general_info.reservation_phone && (
                <p className="mb-2">
                  Reservierungen: <a href={`tel:${locationsData.general_info.reservation_phone}`} className="text-light-beige hover:underline">
                    {formatPhoneNumber(locationsData.general_info.reservation_phone)}
                  </a>
                </p>
              )}
              {locationsData.general_info.opening_season && (
                <p className="text-sm opacity-90">
                  Saison: {locationsData.general_info.opening_season}
                </p>
              )}
            </div>
          </div>
        </section>
      )}
    </div>
  );
};

export default Locations;