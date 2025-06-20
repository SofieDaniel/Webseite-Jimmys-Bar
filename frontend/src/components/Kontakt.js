import React, { useState } from 'react';

const Kontakt = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: ''
  });
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState('');

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

  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Header Section */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('https://images.unsplash.com/photo-1578662996442-48f60103fc96')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              Kontakt
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              Wir freuen uns auf Ihre Nachricht
            </p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-16">
        <div className="grid lg:grid-cols-2 gap-16 max-w-6xl mx-auto">
          {/* Contact Information */}
          <div>
            <h2 className="text-3xl font-serif text-warm-beige mb-8">Besuchen Sie uns</h2>
            
            {/* Location 1 */}
            <div className="bg-medium-brown rounded-lg border border-warm-brown p-6 mb-6">
              <h3 className="text-xl font-serif text-warm-beige mb-4">Jimmy's Tapas Bar Kühlungsborn</h3>
              <div className="space-y-3 text-light-beige">
                <p className="flex items-center">
                  <span className="text-warm-beige mr-3">📍</span>
                  Strandstraße 1, 18225 Kühlungsborn
                </p>
                <p className="flex items-center">
                  <span className="text-warm-beige mr-3">📞</span>
                  +49 38293 12345
                </p>
                <p className="flex items-center">
                  <span className="text-warm-beige mr-3">✉️</span>
                  kuehlungsborn@jimmys-tapasbar.de
                </p>
                <div className="mt-4">
                  <p className="font-medium text-warm-beige mb-2">Öffnungszeiten:</p>
                  <p className="text-sm">Mo-Do: 16:00 - 23:00</p>
                  <p className="text-sm">Fr: 16:00 - 24:00</p>
                  <p className="text-sm">Sa: 12:00 - 24:00</p>
                  <p className="text-sm">So: 12:00 - 23:00</p>
                </div>
              </div>
            </div>

            {/* Location 2 */}
            <div className="bg-medium-brown rounded-lg border border-warm-brown p-6 mb-6">
              <h3 className="text-xl font-serif text-warm-beige mb-4">Jimmy's Tapas Bar Warnemünde</h3>
              <div className="space-y-3 text-light-beige">
                <p className="flex items-center">
                  <span className="text-warm-beige mr-3">📍</span>
                  Am Strom 2, 18119 Warnemünde
                </p>
                <p className="flex items-center">
                  <span className="text-warm-beige mr-3">📞</span>
                  +49 381 987654
                </p>
                <p className="flex items-center">
                  <span className="text-warm-beige mr-3">✉️</span>
                  warnemuende@jimmys-tapasbar.de
                </p>
                <div className="mt-4">
                  <p className="font-medium text-warm-beige mb-2">Öffnungszeiten:</p>
                  <p className="text-sm">Mo-Do: 17:00 - 23:00</p>
                  <p className="text-sm">Fr: 17:00 - 24:00</p>
                  <p className="text-sm">Sa: 12:00 - 24:00</p>
                  <p className="text-sm">So: 12:00 - 23:00</p>
                </div>
              </div>
            </div>

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