import React, { useState, useEffect } from 'react';

const Impressum = () => {
  const [imprintContent, setImprintContent] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load imprint content from backend
  useEffect(() => {
    const loadImprintContent = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/legal/imprint`);
        if (response.ok) {
          const data = await response.json();
          setImprintContent(data);
        }
      } catch (error) {
        console.error('Error loading imprint content:', error);
      } finally {
        setLoading(false);
      }
    };
    loadImprintContent();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-warm-beige"></div>
      </div>
    );
  }

  // Fallback content if backend is unavailable
  const content = imprintContent || {
    title: "Impressum",
    content: "Impressum wird geladen...",
    contact_name: "Jimmy Rodriguez",
    contact_address: "Strandstraße 1, 18225 Kühlungsborn",
    contact_phone: "+49 38293 12345",
    contact_email: "info@jimmys-tapasbar.de"
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
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('https://images.unsplash.com/photo-1589829545856-d10d557cf95f')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              {content.title}
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              Rechtliche Informationen
            </p>
          </div>
        </div>
      </div>

      {/* Content Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          <div className="bg-medium-brown rounded-lg border border-warm-brown p-8 mb-8">
            <div className="prose prose-invert max-w-none">
              {formatContent(content.content)}
            </div>
          </div>

          {/* Quick Contact Info */}
          <div className="bg-dark-brown rounded-lg border border-warm-brown p-6">
            <h2 className="text-2xl font-serif text-warm-beige mb-6">Schnellkontakt</h2>
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-medium text-warm-beige mb-2">Geschäftsführung</h3>
                <p className="text-light-beige">{content.contact_name}</p>
              </div>
              <div>
                <h3 className="font-medium text-warm-beige mb-2">Adresse</h3>
                <p className="text-light-beige">{content.contact_address}</p>
              </div>
              <div>
                <h3 className="font-medium text-warm-beige mb-2">Telefon</h3>
                <p className="text-light-beige">{content.contact_phone}</p>
              </div>
              <div>
                <h3 className="font-medium text-warm-beige mb-2">E-Mail</h3>
                <p className="text-light-beige">{content.contact_email}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Impressum;