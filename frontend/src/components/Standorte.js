import React, { useState, useEffect } from 'react';

const Standorte = () => {
  const [locationsContent, setLocationsContent] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load locations content from backend
  useEffect(() => {
    const loadLocationsContent = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/locations`);
        if (response.ok) {
          const data = await response.json();
          setLocationsContent(data);
        }
      } catch (error) {
        console.error('Error loading locations content:', error);
      } finally {
        setLoading(false);
      }
    };
    loadLocationsContent();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-warm-beige"></div>
      </div>
    );
  }

  // Fallback to default content if backend is unavailable
  const pageData = locationsContent || {
    page_title: "Unsere Standorte",
    page_description: "Besuchen Sie uns an der malerischen Ostseeküste",
    locations: [
      {
        name: "Jimmy's Tapas Bar Kühlungsborn",
        address: "Strandstraße 1, 18225 Kühlungsborn",
        phone: "+49 38293 12345",
        email: "kuehlungsborn@jimmys-tapasbar.de",
        opening_hours: {
          "Montag": "16:00 - 23:00",
          "Dienstag": "16:00 - 23:00",
          "Mittwoch": "16:00 - 23:00",
          "Donnerstag": "16:00 - 23:00",
          "Freitag": "16:00 - 24:00",
          "Samstag": "12:00 - 24:00",
          "Sonntag": "12:00 - 23:00"
        },
        description: "Unser Hauptstandort direkt am Strand von Kühlungsborn",
        image_url: "https://images.unsplash.com/photo-1571197119738-26123cb0d22f"
      },
      {
        name: "Jimmy's Tapas Bar Warnemünde",
        address: "Am Strom 2, 18119 Warnemünde",
        phone: "+49 381 987654",
        email: "warnemuende@jimmys-tapasbar.de",
        opening_hours: {
          "Montag": "17:00 - 23:00",
          "Dienstag": "17:00 - 23:00",
          "Mittwoch": "17:00 - 23:00",
          "Donnerstag": "17:00 - 23:00",
          "Freitag": "17:00 - 24:00",
          "Samstag": "12:00 - 24:00",
          "Sonntag": "12:00 - 23:00"
        },
        description: "Gemütlich am alten Strom mit Blick auf die Warnow",
        image_url: "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d"
      }
    ]
  };

  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Header Section */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('https://images.pexels.com/photos/26626726/pexels-photo-26626726.jpeg')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              {pageData.page_title}
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              {pageData.page_description}
            </p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-16">
        <div className="grid lg:grid-cols-2 gap-16 max-w-7xl mx-auto">
          {pageData.locations.map((location, index) => (
            <div key={index} className="bg-dark-brown rounded-xl border border-warm-brown overflow-hidden shadow-2xl">
              <div className="relative">
                <img 
                  src={location.image_url} 
                  alt={location.name} 
                  className="w-full h-72 object-cover"
                />
                {index === 0 && (
                  <div className="absolute top-4 left-4 bg-warm-beige text-dark-brown px-4 py-2 rounded-lg">
                    <span className="font-serif font-semibold">Hauptstandort</span>
                  </div>
                )}
              </div>
              <div className="p-8">
                <h2 className="text-3xl font-serif text-warm-beige mb-6 tracking-wide">
                  {location.name}
                </h2>
                <div className="space-y-6 text-light-beige">
                  <div className="flex items-start space-x-4">
                    <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                      <span className="text-xl text-dark-brown">📍</span>
                    </div>
                    <div>
                      <h3 className="font-semibold text-warm-beige mb-1">Adresse</h3>
                      <p className="font-light text-lg">{location.address}</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-4">
                    <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                      <span className="text-xl text-dark-brown">🕒</span>
                    </div>
                    <div>
                      <h3 className="font-semibold text-warm-beige mb-1">Öffnungszeiten</h3>
                      {Object.entries(location.opening_hours).map(([day, hours]) => (
                        <p key={day} className="font-light text-sm">
                          {day}: {hours}
                        </p>
                      ))}
                    </div>
                  </div>
                  <div className="flex items-start space-x-4">
                    <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                      <span className="text-xl text-dark-brown">📞</span>
                    </div>
                    <div>
                      <h3 className="font-semibold text-warm-beige mb-1">Kontakt</h3>
                      <p className="font-light">{location.phone}</p>
                      <p className="font-light text-sm text-warm-beige">{location.email}</p>
                    </div>
                  </div>
                  {location.description && (
                    <div className="mt-4 p-4 bg-medium-brown rounded-lg border border-warm-brown">
                      <p className="font-light text-warm-beige">{location.description}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Standorte;