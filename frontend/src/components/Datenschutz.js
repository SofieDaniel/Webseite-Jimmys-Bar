import React, { useState, useEffect } from 'react';

const Datenschutz = () => {
  const [privacyContent, setPrivacyContent] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load privacy content from backend
  useEffect(() => {
    const loadPrivacyContent = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/legal/privacy`);
        if (response.ok) {
          const data = await response.json();
          setPrivacyContent(data);
        }
      } catch (error) {
        console.error('Error loading privacy content:', error);
      } finally {
        setLoading(false);
      }
    };
    loadPrivacyContent();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-warm-beige"></div>
      </div>
    );
  }

  // Fallback content if backend is unavailable
  const content = privacyContent || {
    title: "Datenschutzerklärung",
    content: "Datenschutzerklärung wird geladen...",
    contact_name: "Jimmy Rodriguez",
    contact_email: "datenschutz@jimmys-tapasbar.de"
  };

  // Convert markdown-like content to HTML structure
  const formatContent = (text) => {
    return text.split('\n').map((line, index) => {
      if (line.startsWith('**') && line.endsWith('**')) {
        return <h3 key={index} className="text-xl font-serif text-warm-beige mt-6 mb-3">{line.slice(2, -2)}</h3>;
      }
      if (line.trim() === '') {
        return <br key={index} />;
      }
      return <p key={index} className="text-light-beige mb-2 leading-relaxed">{line}</p>;
    });
  };

  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Header Section */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('https://images.unsplash.com/photo-1614064641938-3bbee52942c7')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              {content.title}
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              Ihre Daten sind uns wichtig
            </p>
          </div>
        </div>
      </div>

      {/* Content Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          {/* Content */}
          <div className="bg-medium-brown rounded-lg border border-warm-brown p-8 mb-8">
            <div className="prose prose-invert max-w-none">
              {formatContent(content.content)}
            </div>
          </div>

          {/* Contact for Privacy Questions */}
          <div className="bg-dark-brown rounded-lg border border-warm-brown p-6">
            <h2 className="text-2xl font-serif text-warm-beige mb-4">Fragen zum Datenschutz?</h2>
            <p className="text-light-beige mb-4">
              Bei Fragen zum Datenschutz oder zur Verarbeitung Ihrer personenbezogenen Daten können Sie sich jederzeit an uns wenden:
            </p>
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-medium text-warm-beige mb-2">Datenschutzbeauftragter</h3>
                <p className="text-light-beige">{content.contact_name}</p>
              </div>
              <div>
                <h3 className="font-medium text-warm-beige mb-2">E-Mail für Datenschutz</h3>
                <p className="text-light-beige">{content.contact_email}</p>
              </div>
            </div>
            
            <div className="mt-6 p-4 bg-warm-brown rounded-lg">
              <h4 className="font-medium text-warm-beige mb-2">Ihre Rechte</h4>
              <ul className="text-light-beige text-sm space-y-1">
                <li>• Recht auf Auskunft über gespeicherte Daten</li>
                <li>• Recht auf Berichtigung unrichtiger Daten</li>
                <li>• Recht auf Löschung Ihrer Daten</li>
                <li>• Recht auf Einschränkung der Verarbeitung</li>
                <li>• Recht auf Datenübertragbarkeit</li>
                <li>• Widerspruchsrecht gegen die Verarbeitung</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Datenschutz;