import React, { useState, useEffect } from 'react';

const UeberUns = () => {
  const [loading, setLoading] = useState(false);

  // Statische Daten direkt in der Komponente - funktioniert garantiert
  const pageData = {
    page_title: 'Über uns',
    page_subtitle: 'Die Geschichte hinter Jimmy\'s Tapas Bar',
    header_background: 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f',
    jimmy_data: {
      name: 'Jimmy Rodríguez',
      title: 'Inhaber & Küchenchef',
      story: 'Geboren in Andalusien, aufgewachsen mit den Aromen der spanischen Küche. Jimmy brachte 2015 seine Familienrezepte an die deutsche Ostseeküste. Mit über 15 Jahren Erfahrung in der spanischen Gastronomie sorgt er persönlich dafür, dass jedes Gericht die authentischen Geschmäcker Spaniens widerspiegelt.',
      philosophy: 'Authentische spanische Küche mit frischen, regionalen Zutaten - das ist meine Leidenschaft. Jedes Gericht erzählt eine Geschichte.',
      image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d'
    },
    values_data: [
      {
        title: 'Authentizität',
        description: 'Echte spanische Rezepte aus Familientradition, unverfälscht und mit Liebe zubereitet.',
        icon: '🇪🇸'
      },
      {
        title: 'Frische',
        description: 'Täglich frische Zutaten aus der Region und direkt aus Spanien importierte Spezialitäten.',
        icon: '🌱'
      },
      {
        title: 'Gemeinschaft',
        description: 'Ein Ort, wo Familie und Freunde zusammenkommen und spanische Lebensfreude erleben.',
        icon: '❤️'
      }
    ],
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
          <div className="absolute inset-0 bg-dark-brown bg-opacity-70"></div>
        </div>
        
        <div className="relative z-10 h-full flex items-center justify-center text-center px-4">
          <div>
            <h1 className="text-5xl md:text-6xl font-serif text-warm-beige mb-4">
              {pageData.page_title}
            </h1>
            <p className="text-xl text-light-beige max-w-2xl mx-auto">
              {pageData.page_subtitle}
            </p>
          </div>
        </div>
      </div>

      {/* Jimmy Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <img 
              src={pageData.jimmy_data.image} 
              alt={pageData.jimmy_data.name}
              className="w-full h-96 object-cover rounded-xl shadow-lg"
            />
          </div>
          <div>
            <h2 className="text-4xl font-serif text-warm-beige mb-4">
              {pageData.jimmy_data.name}
            </h2>
            <h3 className="text-xl text-orange-400 mb-6">
              {pageData.jimmy_data.title}
            </h3>
            <p className="text-light-beige leading-relaxed mb-6 text-lg">
              {pageData.jimmy_data.story}
            </p>
            <blockquote className="border-l-4 border-orange-500 pl-6 italic text-warm-beige">
              "{pageData.jimmy_data.philosophy}"
            </blockquote>
          </div>
        </div>
      </div>

      {/* Values Section */}
      <div className="bg-medium-brown py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-serif text-warm-beige text-center mb-12">
            Unsere Werte
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {pageData.values_data.map((value, index) => (
              <div key={index} className="text-center bg-dark-brown rounded-xl p-8 border border-warm-brown">
                <div className="text-6xl mb-4">{value.icon}</div>
                <h3 className="text-2xl font-serif text-warm-beige mb-4">
                  {value.title}
                </h3>
                <p className="text-light-beige leading-relaxed">
                  {value.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Team Section */}
      <div className="container mx-auto px-4 py-16">
        <h2 className="text-4xl font-serif text-warm-beige text-center mb-12">
          Unser Team
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          {pageData.team_members.map((member, index) => (
            <div key={index} className="bg-medium-brown rounded-xl border border-warm-brown overflow-hidden">
              <img 
                src={member.image} 
                alt={member.name}
                className="w-full h-64 object-cover"
              />
              <div className="p-6">
                <h3 className="text-xl font-serif text-warm-beige mb-2">
                  {member.name}
                </h3>
                <h4 className="text-orange-400 mb-4 font-medium">
                  {member.position}
                </h4>
                <p className="text-light-beige leading-relaxed">
                  {member.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default UeberUns;