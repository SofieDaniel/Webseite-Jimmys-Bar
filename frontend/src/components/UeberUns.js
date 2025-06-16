import React, { useState, useEffect } from 'react';

const UeberUns = () => {
  const [aboutContent, setAboutContent] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load about content from backend
  useEffect(() => {
    const loadAboutContent = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/about`);
        if (response.ok) {
          const data = await response.json();
          setAboutContent(data);
        }
      } catch (error) {
        console.error('Error loading about content:', error);
      } finally {
        setLoading(false);
      }
    };
    loadAboutContent();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-warm-beige"></div>
      </div>
    );
  }

  // Fallback to default content if backend is unavailable
  const pageData = aboutContent || {
    page_title: "Über uns",
    hero_title: "Unsere Geschichte",
    hero_description: "Entdecken Sie die Leidenschaft hinter Jimmy's Tapas Bar",
    story_title: "Unsere Leidenschaft",
    story_content: "Seit der Gründung steht Jimmy's Tapas Bar für authentische mediterrane Küche an der deutschen Ostseeküste.\n\nUnsere Leidenschaft gilt den traditionellen Rezepten und frischen Zutaten, die wir täglich mit Liebe zubereiten. Von den ersten kleinen Tapas bis hin zu unseren berühmten Paellas - jedes Gericht erzählt eine Geschichte von Tradition und Qualität.\n\nAn beiden Standorten erleben Sie die entspannte Atmosphäre des Mittelmeers, während Sie den Blick auf die Ostsee genießen können.",
    story_image: "https://images.unsplash.com/photo-1571197119738-26123cb0d22f",
    team_title: "Unser Team",
    team_members: [
      {
        name: "Jimmy Rodriguez",
        position: "Inhaber & Küchenchef",
        description: "Jimmy bringt über 20 Jahre Erfahrung in der mediterranen Küche mit",
        image_url: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d"
      },
      {
        name: "Maria Santos",
        position: "Sous Chef",
        description: "Spezialistin für authentische Tapas und Paellas",
        image_url: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80"
      }
    ],
    values_title: "Unsere Werte",
    values: [
      "Authentische mediterrane Küche",
      "Frische, regionale Zutaten",
      "Familiäre Atmosphäre",
      "Leidenschaft für Qualität",
      "Gastfreundschaft"
    ]
  };

  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Hero Section */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('${pageData.story_image}')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              {pageData.page_title}
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              {pageData.hero_description}
            </p>
          </div>
        </div>
      </div>

      {/* Story Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl font-serif text-warm-beige mb-8 text-center tracking-wide">
            {pageData.story_title}
          </h2>
          <div className="text-light-beige font-light text-lg leading-relaxed space-y-4">
            {pageData.story_content.split('\n').map((paragraph, index) => (
              paragraph.trim() && (
                <p key={index} className="mb-4">{paragraph.trim()}</p>
              )
            ))}
          </div>
        </div>
      </div>

      {/* Team Section */}
      {pageData.team_members && pageData.team_members.length > 0 && (
        <div className="py-16 bg-medium-brown">
          <div className="container mx-auto px-4">
            <h2 className="text-4xl font-serif text-warm-beige mb-12 text-center tracking-wide">
              {pageData.team_title}
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
              {pageData.team_members.map((member, index) => (
                <div key={index} className="bg-dark-brown rounded-lg border border-warm-brown overflow-hidden shadow-lg">
                  {member.image_url && (
                    <img 
                      src={member.image_url} 
                      alt={member.name} 
                      className="w-full h-64 object-cover"
                    />
                  )}
                  <div className="p-6">
                    <h3 className="text-xl font-serif text-warm-beige mb-2">{member.name}</h3>
                    <p className="text-orange-400 font-medium mb-3">{member.position}</p>
                    <p className="text-light-beige font-light text-sm">{member.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Values Section */}
      {pageData.values && pageData.values.length > 0 && (
        <div className="py-16">
          <div className="container mx-auto px-4">
            <h2 className="text-4xl font-serif text-warm-beige mb-12 text-center tracking-wide">
              {pageData.values_title}
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-4xl mx-auto">
              {pageData.values.map((value, index) => (
                <div key={index} className="bg-dark-brown rounded-lg border border-warm-brown p-6 text-center">
                  <p className="text-warm-beige font-light text-lg">{value}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default UeberUns;