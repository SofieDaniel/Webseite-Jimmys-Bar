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
      
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/ueber-uns-enhanced`);
      if (response.ok) {
        const data = await response.json();
        console.log('Loaded about data:', data);
        
        // Data is already parsed from backend - no need to parse again
        // But ensure we have the right structure
        if (data.team_members && Array.isArray(data.team_members)) {
          // Already an array, good
        } else if (typeof data.team_members === 'string') {
          try {
            data.team_members = JSON.parse(data.team_members);
          } catch (e) {
            console.warn('Failed to parse team_members JSON:', e);
            data.team_members = [];
          }
        } else {
          data.team_members = [];
        }
        
        if (data.values_data && Array.isArray(data.values_data)) {
          // Already an array, good
        } else if (typeof data.values_data === 'string') {
          try {
            data.values_data = JSON.parse(data.values_data);
          } catch (e) {
            console.warn('Failed to parse values_data JSON:', e);
            data.values_data = [];
          }
        } else {
          data.values_data = [];
        }
        
        setPageData(data);
      } else {
        throw new Error('Failed to load about page data');
      }
    } catch (error) {
      console.error('Error loading about page:', error);
      setError('Fehler beim Laden der Über uns-Seite. Bitte versuchen Sie es später erneut.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="text-warm-beige text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-warm-beige mx-auto mb-4"></div>
          <p className="text-xl">Lade Über uns-Seite...</p>
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
          <button
            onClick={loadPageData}
            className="mt-4 bg-warm-beige text-dark-brown px-6 py-3 rounded-lg hover:bg-light-beige transition-colors"
          >
            Neu laden
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Hero Section */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('${pageData.story_image || 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f'}')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              {pageData.hero_title || 'Über uns'}
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              {pageData.hero_description || 'Erfahren Sie mehr über unsere Geschichte'}
            </p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-16">
        {/* Story Section */}
        <div className="max-w-4xl mx-auto mb-20">
          <h2 className="text-4xl font-serif text-warm-beige text-center mb-12">
            {pageData.story_title || 'Unsere Geschichte'}
          </h2>
          <div className="bg-medium-brown rounded-xl p-8 border border-warm-brown">
            <div className="prose prose-lg max-w-none">
              <p className="text-light-beige leading-relaxed text-lg font-light">
                {pageData.story_content}
              </p>
            </div>
          </div>
        </div>

        {/* Team Section */}
        {pageData.team_members && pageData.team_members.length > 0 && (
          <div className="mb-20">
            <h2 className="text-4xl font-serif text-warm-beige text-center mb-12">
              {pageData.team_title || 'Unser Team'}
            </h2>
            <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
              {pageData.team_members.map((member, index) => (
                <div key={index} className="bg-medium-brown rounded-xl overflow-hidden border border-warm-brown shadow-lg">
                  <div className="h-80 overflow-hidden">
                    <img 
                      src={member.image || `https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400&h=400&fit=crop&crop=face`} 
                      alt={member.name}
                      className="w-full h-full object-cover hover:scale-110 transition-transform duration-300"
                    />
                  </div>
                  <div className="p-6">
                    <h3 className="text-2xl font-serif text-warm-beige mb-2">
                      {member.name}
                    </h3>
                    <p className="text-orange-400 mb-3 font-medium">
                      {member.role}
                    </p>
                    <p className="text-light-beige font-light leading-relaxed">
                      {member.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Values Section */}
        {pageData.values_data && pageData.values_data.length > 0 && (
          <div>
            <h2 className="text-4xl font-serif text-warm-beige text-center mb-12">
              {pageData.values_title || 'Unsere Werte'}
            </h2>
            <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
              {pageData.values_data.map((value, index) => (
                <div key={index} className="bg-medium-brown rounded-xl border border-warm-brown p-8 text-center">
                  <div className="text-4xl mb-4">{value.icon}</div>
                  <h3 className="text-xl font-serif text-warm-beige mb-4">{value.title}</h3>
                  <p className="text-light-beige font-light">{value.description}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default UeberUns;