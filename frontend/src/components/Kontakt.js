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

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setMessage('');

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/contact`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        setMessage('Vielen Dank für Ihre Nachricht! Wir melden uns bald bei Ihnen.');
        setFormData({
          name: '',
          email: '',
          phone: '',
          subject: '',
          message: ''
        });
      } else {
        setMessage('Fehler beim Senden der Nachricht. Bitte versuchen Sie es erneut.');
      }
    } catch (error) {
      console.error('Error submitting contact form:', error);
      setMessage('Verbindungsfehler. Bitte versuchen Sie es später erneut.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Header Section mit spanischem Hintergrundbild */}
      <div className="relative overflow-hidden bg-gradient-to-r from-dark-brown via-medium-brown to-dark-brown">
        <div className="absolute inset-0 bg-black bg-opacity-50"></div>
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage: "url('https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2074&q=80')"
          }}
        ></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <div className="max-w-4xl mx-auto">
              <h1 className="text-6xl md:text-7xl font-serif text-warm-beige mb-6 tracking-wide drop-shadow-lg">
                Kontakt
              </h1>
              <div className="bg-dark-brown/40 backdrop-blur-sm rounded-xl p-6 border border-warm-beige/30">
                <p className="text-xl md:text-2xl text-light-beige font-light leading-relaxed">
                  Wir freuen uns auf Ihre Nachricht
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content - Nur Kontaktformular */}
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          
          {/* Kontaktformular */}
          <div className="bg-medium-brown/50 rounded-xl p-8 border border-warm-beige/20 shadow-2xl">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-serif text-warm-beige mb-4">Schreiben Sie uns</h2>
              <p className="text-light-beige">
                Haben Sie Fragen zu unserer Speisekarte, möchten Sie eine größere Gruppe anmelden oder 
                haben andere Anliegen? Wir antworten schnell und persönlich.
              </p>
            </div>

            {message && (
              <div className={`mb-6 p-4 rounded-lg ${
                message.includes('Vielen Dank') 
                  ? 'bg-green-100 border border-green-300 text-green-800' 
                  : 'bg-red-100 border border-red-300 text-red-800'
              }`}>
                {message}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-warm-beige mb-2">
                    Name *
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 bg-dark-brown/50 border border-warm-beige/30 rounded-lg text-light-beige placeholder-gray-400 focus:ring-2 focus:ring-warm-beige focus:border-transparent transition-all duration-300"
                    placeholder="Ihr vollständiger Name"
                  />
                </div>
                
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-warm-beige mb-2">
                    E-Mail *
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 bg-dark-brown/50 border border-warm-beige/30 rounded-lg text-light-beige placeholder-gray-400 focus:ring-2 focus:ring-warm-beige focus:border-transparent transition-all duration-300"
                    placeholder="ihre.email@beispiel.de"
                  />
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="phone" className="block text-sm font-medium text-warm-beige mb-2">
                    Telefon
                  </label>
                  <input
                    type="tel"
                    id="phone"
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 bg-dark-brown/50 border border-warm-beige/30 rounded-lg text-light-beige placeholder-gray-400 focus:ring-2 focus:ring-warm-beige focus:border-transparent transition-all duration-300"
                    placeholder="+49 123 456789"
                  />
                </div>
                
                <div>
                  <label htmlFor="subject" className="block text-sm font-medium text-warm-beige mb-2">
                    Betreff *
                  </label>
                  <select
                    id="subject"
                    name="subject"
                    value={formData.subject}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 bg-dark-brown/50 border border-warm-beige/30 rounded-lg text-light-beige focus:ring-2 focus:ring-warm-beige focus:border-transparent transition-all duration-300"
                  >
                    <option value="">Betreff wählen</option>
                    <option value="allgemeine-anfrage">Allgemeine Anfrage</option>
                    <option value="gruppenbuchung">Gruppenbuchung</option>
                    <option value="feedback">Feedback</option>
                    <option value="beschwerden">Beschwerden</option>
                    <option value="kooperation">Kooperation</option>
                    <option value="sonstiges">Sonstiges</option>
                  </select>
                </div>
              </div>

              <div>
                <label htmlFor="message" className="block text-sm font-medium text-warm-beige mb-2">
                  Nachricht *
                </label>
                <textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleInputChange}
                  required
                  rows={6}
                  className="w-full px-4 py-3 bg-dark-brown/50 border border-warm-beige/30 rounded-lg text-light-beige placeholder-gray-400 focus:ring-2 focus:ring-warm-beige focus:border-transparent transition-all duration-300 resize-vertical"
                  placeholder="Teilen Sie uns mit, wie wir Ihnen helfen können..."
                ></textarea>
              </div>

              <div className="text-center">
                <button
                  type="submit"
                  disabled={submitting}
                  className={`px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-300 ${
                    submitting
                      ? 'bg-gray-400 text-gray-700 cursor-not-allowed'
                      : 'bg-warm-beige text-dark-brown hover:bg-orange-500 hover:text-white shadow-lg hover:shadow-xl'
                  }`}
                >
                  {submitting ? 'Wird gesendet...' : 'Nachricht senden'}
                </button>
              </div>
            </form>

            {/* Zusätzliche Kontakt-Info */}
            <div className="mt-12 pt-8 border-t border-warm-beige/20">
              <div className="text-center">
                <h3 className="text-xl font-serif text-warm-beige mb-4">Weitere Kontaktmöglichkeiten</h3>
                <div className="grid md:grid-cols-3 gap-6">
                  <div className="bg-dark-brown/50 rounded-lg p-4">
                    <div className="flex items-center justify-center mb-2">
                      <span className="text-warm-beige text-2xl">📞</span>
                    </div>
                    <h4 className="font-semibold text-warm-beige mb-1">Telefon</h4>
                    <p className="text-light-beige text-sm">015735256793</p>
                  </div>
                  
                  <div className="bg-dark-brown/50 rounded-lg p-4">
                    <div className="flex items-center justify-center mb-2">
                      <span className="text-warm-beige text-2xl">📧</span>
                    </div>
                    <h4 className="font-semibold text-warm-beige mb-1">E-Mail</h4>
                    <p className="text-light-beige text-sm">info@jimmys-tapasbar.de</p>
                  </div>
                  
                  <div className="bg-dark-brown/50 rounded-lg p-4">
                    <div className="flex items-center justify-center mb-2">
                      <span className="text-warm-beige text-2xl">⏰</span>
                    </div>
                    <h4 className="font-semibold text-warm-beige mb-1">Antwortzeit</h4>
                    <p className="text-light-beige text-sm">Innerhalb von 24h</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Kontakt;