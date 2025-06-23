import React, { useState, useEffect } from 'react';

const UeberUns = () => {
  const [aboutData, setAboutData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadAboutData = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/ueber-uns-enhanced`);
        if (response.ok) {
          const data = await response.json();
          setAboutData(data);
        }
      } catch (error) {
        console.error('Error loading about data:', error);
      } finally {
        setLoading(false);
      }
    };
    loadAboutData();
  }, []);

  // Fallback data structure wie auf der Live-Website
  const defaultData = {
    page_title: 'Über uns',
    page_subtitle: 'Die Geschichte hinter Jimmy\'s Tapas Bar',
    header_background: 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f',
    jimmy_data: {
      name: 'Jimmy Rodríguez',
      title: 'Inhaber & Küchenchef',
      story1: 'Seit über 15 Jahren bringe ich die authentischen Aromen Spaniens an die deutsche Ostseeküste. Meine Leidenschaft für die spanische Küche begann in den kleinen Tapas-Bars von Sevilla, wo ich die Geheimnisse traditioneller Rezepte erlernte.',
      story2: 'In Jimmy\'s Tapas Bar verwenden wir nur die besten Zutaten - von handverlesenem Olivenöl aus Andalusien bis hin zu frischen Meeresfrüchten aus der Ostsee. Jedes Gericht wird mit Liebe und Respekt vor der spanischen Tradition zubereitet.',
      image: 'https://images.unsplash.com/photo-1544025162-d76694265947'
    },
    leidenschaft_data: {
      title: 'Unsere Leidenschaft',
      subtitle: 'Entdecken Sie die Leidenschaft hinter Jimmy\'s Tapas Bar',
      intro: 'Seit der Gründung steht Jimmy\'s Tapas Bar für authentische mediterrane Küche an der deutschen Ostseeküste.',
      text1: 'Unsere Leidenschaft gilt den traditionellen Rezepten und frischen Zutaten, die wir täglich mit Liebe zubereiten.',
      text2: 'Von den ersten kleinen Tapas bis hin zu unseren berühmten Paellas - jedes Gericht erzählt eine Geschichte',
      text3: 'von Tradition und Qualität.',
      text4: 'An beiden Standorten erleben Sie die entspannte Atmosphäre des Mittelmeers,',
      text5: 'während Sie den Blick auf die Ostsee genießen können.'
    }
  };

  // Exakte Daten wie in den Bildern gezeigt
  const pageData = {
    page_title: 'Über uns',
    page_subtitle: 'Die Geschichte hinter Jimmy\'s Tapas Bar',
    header_background: 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f',
    jimmy_data: {
      name: 'Jimmy Rodríguez',
      title: 'Inhaber & Küchenchef',
      story1: 'Seit über 15 Jahren bringe ich die authentischen Aromen Spaniens an die deutsche Ostseeküste. Meine Leidenschaft für die spanische Küche begann in den kleinen Tapas-Bars von Sevilla, wo ich die Geheimnisse traditioneller Rezepte erlernte.',
      story2: 'In Jimmy\'s Tapas Bar verwenden wir nur die besten Zutaten - von handverlesenem Olivenöl aus Andalusien bis hin zu frischen Meeresfrüchten aus der Ostsee. Jedes Gericht wird mit Liebe und Respekt vor der spanischen Tradition zubereitet.',
      image: 'https://images.unsplash.com/photo-1544025162-d76694265947'
    },
    leidenschaft_data: {
      title: 'Unsere Leidenschaft',
      subtitle: 'Entdecken Sie die Leidenschaft hinter Jimmy\'s Tapas Bar',
      intro: 'Seit der Gründung steht Jimmy\'s Tapas Bar für authentische mediterrane Küche an der deutschen Ostseeküste.',
      text1: 'Unsere Leidenschaft gilt den traditionellen Rezepten und frischen Zutaten, die wir täglich mit Liebe zubereiten.',
      text2: 'Von den ersten kleinen Tapas bis hin zu unseren berühmten Paellas - jedes Gericht erzählt eine Geschichte',
      text3: 'von Tradition und Qualität.',
      text4: 'An beiden Standorten erleben Sie die entspannte Atmosphäre des Mittelmeers,',
      text5: 'während Sie den Blick auf die Ostsee genießen können.'
    },
    team_members: [
      {
        name: 'Maria Gonzalez',
        position: 'Sous Chef',
        description: 'Expertin für Meeresfrüchte und Paella, sorgt für die perfekte Zubereitung unserer Spezialitäten.',
        image: 'https://images.unsplash.com/photo-1494790108755-2616c39ca7c0'
      },
      {
        name: 'Carlos Mendez', 
        position: 'Barkeeper',
        description: 'Meister der spanischen Cocktails und Sangria, zaubert die perfekte Begleitung zu unseren Tapas.',
        image: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e'
      },
      {
        name: 'Isabella Schmidt',
        position: 'Service Manager', 
        description: 'Sorgt für perfekten Service und spanische Gastfreundschaft, damit sich jeder Gast willkommen fühlt.',
        image: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80'
      }
    ]
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-warm-beige"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Hero Section */}
      <div className="relative h-96 overflow-hidden">
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage: `url(${pageData.header_background})`
          }}
        >
          <div className="absolute inset-0 bg-black bg-opacity-50"></div>
        </div>
        
        <div className="relative z-10 h-full flex items-center justify-center text-center px-4">
          <div>
            <h1 className="text-5xl md:text-6xl font-serif text-white mb-4">
              {pageData.page_title}
            </h1>
            <p className="text-xl text-gray-200 max-w-2xl mx-auto">
              {pageData.page_subtitle}
            </p>
          </div>
        </div>
      </div>

      {/* Jimmy Section - Exakt wie im Bild */}
      <div className="bg-dark-brown py-16">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            {/* Bild links */}
            <div>
              <img 
                src={pageData.jimmy_data.image} 
                alt={pageData.jimmy_data.name}
                className="w-full h-96 object-cover rounded-lg shadow-lg"
              />
            </div>
            {/* Text rechts */}
            <div>
              <h2 className="text-4xl font-serif text-warm-beige mb-6">
                {pageData.jimmy_data.name}
              </h2>
              <p className="text-light-beige leading-relaxed mb-6 text-base">
                {pageData.jimmy_data.story1}
              </p>
              <p className="text-light-beige leading-relaxed text-base">
                {pageData.jimmy_data.story2}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Unsere Leidenschaft Section - Schöne Box-Gestaltung */}
      <div className="bg-dark-brown py-16">
        <div className="container mx-auto px-4 max-w-4xl">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-serif text-warm-beige mb-4">
              {pageData.leidenschaft_data.title}
            </h2>
            <p className="text-lg text-light-beige mb-8">
              {pageData.leidenschaft_data.subtitle}
            </p>
          </div>
          
          {/* Schöne Box mit Hintergrund und Rahmen */}
          <div className="bg-gradient-to-br from-medium-brown/80 to-dark-brown/90 rounded-2xl border-2 border-warm-beige/30 p-8 md:p-12 shadow-2xl backdrop-blur-sm">
            <div className="text-light-beige space-y-6 text-base leading-relaxed">
              <p className="text-lg font-medium text-warm-beige mb-6">
                {pageData.leidenschaft_data.intro}
              </p>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <p>{pageData.leidenschaft_data.text1}</p>
                  <p>{pageData.leidenschaft_data.text2}</p>
                  <p>{pageData.leidenschaft_data.text3}</p>
                </div>
                <div className="space-y-4">
                  <p>{pageData.leidenschaft_data.text4}</p>
                  <p>{pageData.leidenschaft_data.text5}</p>
                  
                  {/* Dekorative Elemente */}
                  <div className="mt-8 flex items-center justify-center">
                    <div className="flex items-center space-x-4 text-orange-400">
                      <span className="text-2xl">🥘</span>
                      <div className="w-12 h-0.5 bg-warm-beige"></div>
                      <span className="text-2xl">🍷</span>
                      <div className="w-12 h-0.5 bg-warm-beige"></div>
                      <span className="text-2xl">🌊</span>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Call-to-Action */}
              <div className="text-center mt-8 pt-6 border-t border-warm-beige/20">
                <p className="text-warm-beige italic text-lg">
                  "Essen ist nicht nur Nahrung - es ist Kultur, Tradition und Leidenschaft auf einem Teller."
                </p>
                <p className="text-orange-400 mt-2 font-medium">- Jimmy Rodríguez</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UeberUns;