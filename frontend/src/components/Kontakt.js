import React, { useState, useEffect } from 'react';

const Kontakt = () => {
  const [pageData, setPageData] = useState(null);
  const [locationsData, setLocationsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: ''
  });
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    loadPageData();
    loadLocationsData();
  }, []);

  const loadPageData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/kontakt-page`);
      if (response.ok) {
        const data = await response.json();
        console.log('Loaded kontakt page data:', data);
        setPageData(data);
      } else {
        throw new Error('Failed to load contact page data');
      }
    } catch (error) {
      console.error('Error loading contact page:', error);
      setError('Fehler beim Laden der Seite. Bitte versuchen Sie es später erneut.');
    } finally {
      setLoading(false);
    }
  };

  const loadLocationsData = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/standorte-enhanced`);
      if (response.ok) {
        const data = await response.json();
        console.log('Loaded locations data for contact:', data);
        
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
        
        setLocationsData(data);
      }
    } catch (error) {
      console.error('Error loading locations data:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setMessage('');

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/contact`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        setMessage('Vielen Dank für Ihre Nachricht! Wir melden uns bald bei Ihnen.');
        setFormData({ name: '', email: '', phone: '', subject: '', message: '' });
      } else {
        setMessage('Fehler beim Senden der Nachricht. Bitte versuchen Sie es erneut.');
      }
    } catch (error) {
      setMessage('Verbindungsfehler. Bitte versuchen Sie es später erneut.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="text-warm-beige text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-warm-beige mx-auto mb-4"></div>
          <p className="text-xl">Lade Kontakt-Seite...</p>
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
            onClick={loadPageData}
            className="bg-warm-beige text-dark-brown px-6 py-3 rounded-lg hover:bg-light-beige transition-colors"
          >
            Erneut versuchen
          </button>
        </div>
      </div>
    );
  }

  if (!pageData) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="text-warm-beige text-center">
          <p className="text-xl">Keine Daten verfügbar</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Header Section */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('${pageData.header_background || 'https://images.unsplash.com/photo-1578662996442-48f60103fc96'}')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              {pageData.page_title || 'Kontakt'}
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              {pageData.page_subtitle || 'Nehmen Sie Kontakt mit uns auf'}
            </p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-16">
        <div className="grid lg:grid-cols-2 gap-16 max-w-6xl mx-auto">
          {/* Contact Information */}
          <div>
            <h2 className="text-3xl font-serif text-warm-beige mb-8">
              {pageData.locations_section_title || 'Besuchen Sie uns'}
            </h2>
            
            {/* Dynamic Locations from CMS */}
            {locationsData && locationsData.neustadt && (
              <div className="bg-medium-brown rounded-lg border border-warm-brown p-6 mb-6">
                <h3 className="text-xl font-serif text-warm-beige mb-4">{locationsData.neustadt.name}</h3>
                <div className="space-y-3 text-light-beige">
                  <p className="flex items-center">
                    <span className="text-warm-beige mr-3">📍</span>
                    {locationsData.neustadt.address}
                  </p>
                  <p className="flex items-center">
                    <span className="text-warm-beige mr-3">📞</span>
                    {locationsData.neustadt.phone}
                  </p>
                  <p className="flex items-center">
                    <span className="text-warm-beige mr-3">✉️</span>
                    {locationsData.neustadt.email}
                  </p>
                  
                  {/* Opening Hours */}
                  {locationsData.neustadt.opening_hours && (
                    <div className="mt-4">
                      <h4 className="text-warm-beige font-medium mb-2">
                        {pageData.opening_hours_title || 'Öffnungszeiten'}:
                      </h4>
                      <div className="text-sm space-y-1">
                        {Object.entries(locationsData.neustadt.opening_hours).map(([day, hours]) => (
                          <div key={day} className="flex justify-between">
                            <span>{day}:</span>
                            <span>{hours}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Location 2 */}
            {locationsData && locationsData.grossenbrode && (
              <div className="bg-medium-brown rounded-lg border border-warm-brown p-6 mb-6">
                <h3 className="text-xl font-serif text-warm-beige mb-4">{locationsData.grossenbrode.name}</h3>
                <div className="space-y-3 text-light-beige">
                  <p className="flex items-center">
                    <span className="text-warm-beige mr-3">📍</span>
                    {locationsData.grossenbrode.address}
                  </p>
                  <p className="flex items-center">
                    <span className="text-warm-beige mr-3">📞</span>
                    {locationsData.grossenbrode.phone}
                  </p>
                  <p className="flex items-center">
                    <span className="text-warm-beige mr-3">✉️</span>
                    {locationsData.grossenbrode.email}
                  </p>
                  
                  {/* Opening Hours */}
                  {locationsData.grossenbrode.opening_hours && (
                    <div className="mt-4">
                      <h4 className="text-warm-beige font-medium mb-2">
                        {pageData.opening_hours_title || 'Öffnungszeiten'}:
                      </h4>
                      <div className="text-sm space-y-1">
                        {Object.entries(locationsData.grossenbrode.opening_hours).map(([day, hours]) => (
                          <div key={day} className="flex justify-between">
                            <span>{day}:</span>
                            <span>{hours}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Additional Information */}
            {pageData.additional_info && (
              <div className="text-light-beige bg-dark-brown p-4 rounded-lg border border-warm-brown">
                <p className="text-sm">{pageData.additional_info}</p>
              </div>
            )}
                  </p>
                  <p className="flex items-center">
                    <span className="text-warm-beige mr-3">✉️</span>
                    {locationsData.neustadt.email}
                  </p>
                  
                  {/* Opening Hours */}
                  {locationsData.neustadt.opening_hours && (
                    <div className="mt-4">
                      <h4 className="text-warm-beige font-medium mb-2">
                        {pageData.opening_hours_title || 'Öffnungszeiten'}:
                      </h4>
                      <div className="text-sm space-y-1">
                        {Object.entries(locationsData.neustadt.opening_hours).map(([day, hours]) => (
                          <div key={day} className="flex justify-between">
                            <span>{day}:</span>
                            <span>{hours}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Location 2 */}
            {locationsData && locationsData.grossenbrode && (
              <div className="bg-medium-brown rounded-lg border border-warm-brown p-6 mb-6">
                <h3 className="text-xl font-serif text-warm-beige mb-4">{locationsData.grossenbrode.name}</h3>
                <div className="space-y-3 text-light-beige">
                  <p className="flex items-center">
                    <span className="text-warm-beige mr-3">📍</span>
                    {locationsData.grossenbrode.address}
                  </p>
                  <p className="flex items-center">
                    <span className="text-warm-beige mr-3">📞</span>
                    {locationsData.grossenbrode.phone}
                  </p>
                  <p className="flex items-center">
                    <span className="text-warm-beige mr-3">✉️</span>
                    {locationsData.grossenbrode.email}
                  </p>
                  
                  {/* Opening Hours */}
                  {locationsData.grossenbrode.opening_hours && (
                    <div className="mt-4">
                      <h4 className="text-warm-beige font-medium mb-2">
                        {pageData.opening_hours_title || 'Öffnungszeiten'}:
                      </h4>
                      <div className="text-sm space-y-1">
                        {Object.entries(locationsData.grossenbrode.opening_hours).map(([day, hours]) => (
                          <div key={day} className="flex justify-between">
                            <span>{day}:</span>
                            <span>{hours}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Additional Information */}
            {pageData.additional_info && (
              <div className="text-light-beige bg-dark-brown p-4 rounded-lg border border-warm-brown">
                <p className="text-sm">{pageData.additional_info}</p>
              </div>
            )}

            {/* Newsletter Signup */}
            <div className="bg-dark-brown rounded-lg border border-warm-brown p-6">
              <h3 className="text-xl font-serif text-warm-beige mb-4">Newsletter abonnieren</h3>
              <p className="text-light-beige mb-4">Bleiben Sie über neue Gerichte und Events informiert</p>
              <form className="flex gap-3">
                <input
                  type="email"
                  placeholder="Ihre E-Mail-Adresse"
                  className="flex-1 px-4 py-2 bg-medium-brown border border-warm-brown rounded text-light-beige focus:ring-2 focus:ring-warm-beige focus:border-transparent"
                />
                <button
                  type="submit"
                  className="bg-warm-beige text-dark-brown px-6 py-2 rounded font-medium hover:bg-light-beige transition-colors"
                >
                  Anmelden
                </button>
              </form>
            </div>
          </div>

          {/* Contact Form */}
          <div>
            <h2 className="text-3xl font-serif text-warm-beige mb-8">Schreiben Sie uns</h2>
            
            {message && (
              <div className={`mb-6 p-4 rounded-lg ${
                message.includes('Vielen Dank') 
                  ? 'bg-green-600 text-white' 
                  : 'bg-red-600 text-white'
              }`}>
                {message}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-warm-beige font-medium mb-2">Name *</label>
                  <input
                    type="text"
                    required
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    className="w-full px-4 py-3 bg-medium-brown border border-warm-brown rounded-lg text-light-beige focus:ring-2 focus:ring-warm-beige focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-warm-beige font-medium mb-2">E-Mail *</label>
                  <input
                    type="email"
                    required
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    className="w-full px-4 py-3 bg-medium-brown border border-warm-brown rounded-lg text-light-beige focus:ring-2 focus:ring-warm-beige focus:border-transparent"
                  />
                </div>
              </div>

              <div>
                <label className="block text-warm-beige font-medium mb-2">Telefon</label>
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData({...formData, phone: e.target.value})}
                  className="w-full px-4 py-3 bg-medium-brown border border-warm-brown rounded-lg text-light-beige focus:ring-2 focus:ring-warm-beige focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-warm-beige font-medium mb-2">Betreff *</label>
                <input
                  type="text"
                  required
                  value={formData.subject}
                  onChange={(e) => setFormData({...formData, subject: e.target.value})}
                  className="w-full px-4 py-3 bg-medium-brown border border-warm-brown rounded-lg text-light-beige focus:ring-2 focus:ring-warm-beige focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-warm-beige font-medium mb-2">Nachricht *</label>
                <textarea
                  required
                  rows={5}
                  value={formData.message}
                  onChange={(e) => setFormData({...formData, message: e.target.value})}
                  className="w-full px-4 py-3 bg-medium-brown border border-warm-brown rounded-lg text-light-beige focus:ring-2 focus:ring-warm-beige focus:border-transparent"
                  placeholder="Ihre Nachricht an uns..."
                />
              </div>

              <button
                type="submit"
                disabled={submitting}
                className="w-full bg-warm-beige text-dark-brown py-3 rounded-lg font-medium hover:bg-light-beige transition-colors disabled:opacity-50"
              >
                {submitting ? 'Wird gesendet...' : 'Nachricht senden'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Kontakt;