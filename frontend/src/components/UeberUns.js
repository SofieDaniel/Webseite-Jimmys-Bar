import React, { useState, useEffect } from 'react';

const UeberUns = () => {
  const [pageData, setPageData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadPageData();
  }, []);

  const loadPageData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/about`);
      if (response.ok) {
        const data = await response.json();
        console.log('Loaded enhanced about data:', data);
        setPageData(data);
      } else {
        throw new Error('Failed to load about page data');
      }
    } catch (error) {
      console.error('Error loading about page:', error);
      setError('Fehler beim Laden der Seite. Bitte versuchen Sie es später erneut.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="text-warm-beige text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-warm-beige mx-auto mb-4"></div>
          <p className="text-xl">Lade Seite...</p>
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
      {/* Elegant Header Section with Background */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('${pageData.header_background || 'https://images.pexels.com/photos/26626726/pexels-photo-26626726.jpeg'}')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              {pageData.page_title || 'Über uns'}
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              {pageData.page_subtitle || 'Die Geschichte hinter Jimmy\'s Tapas Bar'}
            </p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-16">
        <div className="max-w-6xl mx-auto">
          <div className="bg-dark-brown rounded-xl border border-warm-brown p-12 mb-16 shadow-2xl">
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div>
                <img 
                  src={pageData.jimmy?.image || "https://images.unsplash.com/photo-1665758564802-f611df512d8d"} 
                  alt="Jimmy Rodríguez" 
                  className="w-full rounded-xl shadow-lg"
                />
              </div>
              <div>
                <h2 className="text-4xl font-serif text-warm-beige mb-6 tracking-wide">
                  {pageData.jimmy?.name || 'Jimmy Rodríguez'}
                </h2>
                <div className="text-light-beige space-y-6 leading-relaxed font-light text-lg">
                  <p>
                    {pageData.jimmy?.story_paragraph1 || 'Seit über 15 Jahren bringe ich die authentischen Aromen Spaniens an die deutsche Ostseeküste. Meine Leidenschaft für die spanische Küche begann in den kleinen Tapas-Bars von Sevilla, wo ich die Geheimnisse traditioneller Rezepte erlernte.'}
                  </p>
                  <p>
                    {pageData.jimmy?.story_paragraph2 || 'In Jimmy\'s Tapas Bar verwenden wir nur die besten Zutaten - von handverlesenem Olivenöl aus Andalusien bis hin zu frischen Meeresfrüchten aus der Ostsee. Jedes Gericht wird mit Liebe und Respekt vor der spanischen Tradition zubereitet.'}
                  </p>
                  <p className="text-warm-beige font-medium">
                    "{pageData.jimmy?.quote || 'Essen ist nicht nur Nahrung - es ist Kultur, Tradition und Leidenschaft auf einem Teller.'}"
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Values Section with Images */}
          <h3 className="text-4xl font-serif text-warm-beige mb-12 text-center tracking-wide">
            {pageData.values_section?.title || 'Unsere Werte'}
          </h3>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-dark-brown rounded-xl border border-warm-brown overflow-hidden shadow-lg">
              <img 
                src={pageData.values_section?.qualitat?.image || "https://images.unsplash.com/photo-1694685367640-05d6624e57f1"} 
                alt="Qualität" 
                className="w-full h-48 object-cover"
              />
              <div className="p-8 text-center">
                <h4 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">
                  {pageData.values_section?.qualitat?.title || 'Qualität'}
                </h4>
                <p className="text-light-beige font-light leading-relaxed">
                  {pageData.values_section?.qualitat?.description || 'Nur die besten Zutaten für authentische spanische Geschmackserlebnisse. Frische und Qualität stehen bei uns an erster Stelle.'}
                </p>
              </div>
            </div>
            <div className="bg-dark-brown rounded-xl border border-warm-brown overflow-hidden shadow-lg">
              <img 
                src={pageData.values_section?.gastfreundschaft?.image || "https://images.pexels.com/photos/19671352/pexels-photo-19671352.jpeg"} 
                alt="Gastfreundschaft" 
                className="w-full h-48 object-cover"
              />
              <div className="p-8 text-center">
                <h4 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">
                  {pageData.values_section?.gastfreundschaft?.title || 'Gastfreundschaft'}
                </h4>
                <p className="text-light-beige font-light leading-relaxed">
                  {pageData.values_section?.gastfreundschaft?.description || 'Herzliche Atmosphäre und persönlicher Service für jeden Gast. Bei uns sollen Sie sich wie zu Hause fühlen.'}
                </p>
              </div>
            </div>
            <div className="bg-dark-brown rounded-xl border border-warm-brown overflow-hidden shadow-lg">
              <img 
                src={pageData.values_section?.lebensfreude?.image || "https://images.unsplash.com/photo-1656423521731-9665583f100c"} 
                alt="Lebensfreude" 
                className="w-full h-48 object-cover"
              />
              <div className="p-8 text-center">
                <h4 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">
                  {pageData.values_section?.lebensfreude?.title || 'Lebensfreude'}
                </h4>
                <p className="text-light-beige font-light leading-relaxed">
                  {pageData.values_section?.lebensfreude?.description || 'Spanische Lebensart und Genuss in gemütlicher Atmosphäre. Erleben Sie das echte España-Gefühl an der Ostsee.'}
                </p>
              </div>
            </div>
          </div>

          {/* Team Section */}
          <div className="mt-16 bg-dark-brown rounded-xl border border-warm-brown p-12">
            <h3 className="text-4xl font-serif text-warm-beige mb-12 text-center tracking-wide">
              {pageData.team_section?.title || 'Unser Team'}
            </h3>
            <div className="grid md:grid-cols-2 gap-12">
              <div className="text-center">
                <div className="w-32 h-32 bg-medium-brown rounded-full mx-auto mb-6 flex items-center justify-center overflow-hidden">
                  <img 
                    src={pageData.team_section?.carlos?.image || "https://images.unsplash.com/photo-1665758564802-f611df512d8d"} 
                    alt="Küchenchef" 
                    className="w-full h-full object-cover"
                  />
                </div>
                <h4 className="text-2xl font-serif text-warm-beige mb-2">
                  {pageData.team_section?.carlos?.name || 'Carlos Mendez'}
                </h4>
                <p className="text-orange-400 mb-4">
                  {pageData.team_section?.carlos?.position || 'Küchenchef'}
                </p>
                <p className="text-light-beige font-light leading-relaxed">
                  {pageData.team_section?.carlos?.description || 'Mit 20 Jahren Erfahrung in der spanischen Küche sorgt Carlos für die authentischen Geschmäcker in jedem unserer Gerichte.'}
                </p>
              </div>
              <div className="text-center">
                <div className="w-32 h-32 bg-medium-brown rounded-full mx-auto mb-6 flex items-center justify-center overflow-hidden">
                  <img 
                    src={pageData.team_section?.maria?.image || "https://images.unsplash.com/photo-1665758564802-f611df512d8d"} 
                    alt="Service Manager" 
                    className="w-full h-full object-cover"
                  />
                </div>
                <h4 className="text-2xl font-serif text-warm-beige mb-2">
                  {pageData.team_section?.maria?.name || 'Maria Santos'}
                </h4>
                <p className="text-orange-400 mb-4">
                  {pageData.team_section?.maria?.position || 'Service Manager'}
                </p>
                <p className="text-light-beige font-light leading-relaxed">
                  {pageData.team_section?.maria?.description || 'Maria sorgt dafür, dass sich jeder Gast bei uns willkommen fühlt und einen unvergesslichen Abend erlebt.'}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UeberUns;