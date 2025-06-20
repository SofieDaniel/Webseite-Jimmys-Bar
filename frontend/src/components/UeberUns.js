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
        console.log('Loaded about data:', data);
        
        // Parse JSON strings if needed
        if (typeof data.team_members === 'string') {
          try {
            data.team_members = JSON.parse(data.team_members);
          } catch (e) {
            console.warn('Failed to parse team_members JSON:', e);
            data.team_members = [];
          }
        }
        
        if (typeof data.values_data === 'string') {
          try {
            data.values_data = JSON.parse(data.values_data);
          } catch (e) {
            console.warn('Failed to parse values_data JSON:', e);
            data.values_data = [];
          }
        }
        
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
      {/* Header Section */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('${pageData.story_image || 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f'}')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              {pageData.page_title || 'Über uns'}
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              {pageData.hero_description || 'Die Geschichte hinter Jimmy\'s Tapas Bar'}
            </p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-16">
        <div className="max-w-6xl mx-auto">
          {/* Story Section */}
          <div className="bg-gradient-to-br from-medium-brown to-dark-brown rounded-xl border border-warm-brown p-12 mb-16 shadow-2xl">
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div>
                <img 
                  src={pageData.story_image || "https://images.unsplash.com/photo-1571197119738-26123cb0d22f"} 
                  alt="Jimmy's Tapas Bar Story" 
                  className="w-full rounded-xl shadow-lg"
                />
              </div>
              <div>
                <h2 className="text-4xl font-serif text-warm-beige mb-6 tracking-wide">
                  {pageData.story_title || 'Unsere Geschichte'}
                </h2>
                <div className="text-light-beige space-y-6 leading-relaxed font-light text-lg">
                  <p>
                    {pageData.story_content || 'Seit der Gründung steht Jimmy\'s Tapas Bar für authentische mediterrane Küche an der deutschen Ostseeküste.'}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Team Section - Kleiner und eleganter */}
          {pageData.team_members && pageData.team_members.length > 0 && (
            <div className="mb-16">
              <h3 className="text-3xl font-serif text-warm-beige mb-8 text-center tracking-wide">
                {pageData.team_title || 'Unser Team'}
              </h3>
              <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
                {pageData.team_members.map((member, index) => (
                  <div key={index} className="bg-gradient-to-br from-medium-brown to-dark-brown rounded-lg border border-warm-brown overflow-hidden shadow-md">
                    <img 
                      src={member.image_url || "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d"} 
                      alt={member.name} 
                      className="w-full h-32 object-cover"
                    />
                    <div className="p-4 text-center">
                      <h4 className="text-lg font-serif text-warm-beige mb-1 tracking-wide">
                        {member.name}
                      </h4>
                      <p className="text-orange-400 mb-2 font-medium text-sm">
                        {member.role}
                      </p>
                      <p className="text-light-beige font-light leading-relaxed text-xs">
                        {member.description}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Values Section - Kompakter */}
          {pageData.values_data && pageData.values_data.length > 0 && (
            <div>
              <h3 className="text-3xl font-serif text-warm-beige mb-8 text-center tracking-wide">
                {pageData.values_title || 'Unsere Werte'}
              </h3>
              <div className="grid md:grid-cols-5 gap-4 max-w-5xl mx-auto">
                {pageData.values_data.slice(0, 5).map((value, index) => (
                  <div key={index} className="bg-gradient-to-br from-medium-brown to-dark-brown rounded-lg border border-warm-brown p-4 text-center shadow-md">
                    <div className="w-12 h-12 bg-warm-beige rounded-full flex items-center justify-center mx-auto mb-3">
                      <span className="text-lg text-dark-brown">
                        {index === 0 ? '🍽️' : index === 1 ? '🌿' : index === 2 ? '❤️' : index === 3 ? '⭐' : '🏆'}
                      </span>
                    </div>
                    <h4 className="text-sm font-serif text-warm-beige mb-2 tracking-wide leading-tight">
                      {value}
                    </h4>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UeberUns;