import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import EnhancedDeliverySection from './EnhancedDeliverySection';

const Home = () => {
  const navigate = useNavigate();
  const [homepageContent, setHomepageContent] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load homepage content from backend
  useEffect(() => {
    const loadHomepageContent = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/homepage`);
        if (response.ok) {
          const data = await response.json();
          setHomepageContent(data);
        }
      } catch (error) {
        console.error('Error loading homepage content:', error);
      } finally {
        setLoading(false);
      }
    };
    loadHomepageContent();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-warm-beige"></div>
      </div>
    );
  }

  // Use backend data if available, otherwise fallback to default
  const hero = homepageContent ? {
    title: homepageContent.hero_title || "JIMMY'S TAPAS BAR",
    subtitle: homepageContent.hero_subtitle || "an der Ostsee",
    description: homepageContent.hero_description || "Genießen Sie authentische mediterrane Spezialitäten direkt an der malerischen Ostseeküste",
    background_image: homepageContent.hero_background || "https://images.unsplash.com/photo-1656423521731-9665583f100c"
  } : {
    title: "JIMMY'S TAPAS BAR",
    subtitle: "an der Ostsee", 
    description: "Genießen Sie authentische mediterrane Spezialitäten direkt an der malerischen Ostseeküste",
    background_image: "https://images.unsplash.com/photo-1656423521731-9665583f100c"
  };

  // Features from API or default Jimmy's content
  const features = homepageContent?.features_data?.features ? 
    homepageContent.features_data.features : [
    {
      title: "Authentische Tapas",
      description: "Traditionelle mediterrane Gerichte, mit Liebe zubereitet und perfekt zum Teilen",
      image_url: "https://images.pexels.com/photos/19671352/pexels-photo-19671352.jpeg"
    },
    {
      title: "Frische Paella",
      description: "Täglich hausgemacht mit Meeresfrüchten, Gemüse oder Huhn",
      image_url: "https://images.unsplash.com/photo-1694685367640-05d6624e57f1"
    },
    {
      title: "Strandnähe",
      description: "Beide Standorte direkt an der malerischen Ostseeküste – perfekt für entspannte Stunden",
      image_url: "https://images.pexels.com/photos/32508247/pexels-photo-32508247.jpeg"
    }
  ];

  // Specialties from API or default Jimmy's menu
  const specialties = homepageContent?.specialties_data?.specialties ? 
    homepageContent.specialties_data.specialties.map(item => ({
      title: item.name,
      description: item.description,
      image_url: item.image,
      price: item.price
    })) : [
    {
      title: "Patatas Bravas",
      description: "Klassische mediterrane Kartoffeln",
      image_url: "https://images.unsplash.com/photo-1565599837634-134bc3aadce8"
    },
    {
      title: "Paella Valenciana", 
      description: "Traditionelle mediterrane Paella",
      image_url: "https://images.pexels.com/photos/7085661/pexels-photo-7085661.jpeg"
    },
    {
      title: "Tapas Variación",
      description: "Auswahl mediterraner Köstlichkeiten", 
      image_url: "https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg"
    },
    {
      title: "Gambas al Ajillo",
      description: "Garnelen in Knoblauchöl",
      image_url: "https://images.unsplash.com/photo-1619860705243-dbef552e7118"
    }
  ];
  
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section id="main-content" className="relative h-screen bg-cover bg-center hero-background" 
               style={{backgroundImage: `url('${hero.background_image}')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-50"></div>
        <div className="relative z-10 flex items-center justify-center h-full text-center px-4" style={{paddingTop: '80px'}}>
          <div className="max-w-4xl">
            <h1 className="hero-headline font-serif text-warm-beige mb-8 tracking-wide leading-tight drop-shadow-text" style={{fontSize: 'clamp(2.5rem, 8vw, 6rem)', lineHeight: '1.1', marginTop: '40px'}}>
              {hero.title}<br />
              <span className="font-light opacity-90" style={{fontSize: 'clamp(1.8rem, 5vw, 4rem)'}}>{hero.subtitle}</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-warm-beige font-light mb-12 max-w-3xl mx-auto leading-relaxed opacity-95">
              {hero.description}
            </p>
            
            <div className="flex flex-col md:flex-row justify-center gap-6">
              <button 
                onClick={() => navigate('/speisekarte')}
                className="bg-warm-beige text-dark-brown hover:bg-light-beige px-10 py-4 rounded-lg text-lg font-medium transition-all duration-300 tracking-wide shadow-lg hover:shadow-xl"
              >
                Zur Speisekarte
              </button>
              <button 
                onClick={() => navigate('/standorte')}
                className="border-2 border-warm-beige text-warm-beige hover:bg-warm-beige hover:text-dark-brown px-10 py-4 rounded-lg text-lg font-medium transition-all duration-300 tracking-wide shadow-lg hover:shadow-xl"
              >
                Unsere Standorte
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Professional Features Section */}
      <section className="py-24 bg-gradient-to-b from-dark-brown to-medium-brown">
        <div className="container mx-auto px-4">
          <div className="text-center mb-20">
            <h2 className="text-5xl font-serif text-warm-beige mb-8 tracking-wide">
              Mediterrane Tradition
            </h2>
            <p className="text-xl text-light-beige font-light leading-relaxed max-w-3xl mx-auto">
              Erleben Sie authentische mediterrane Gastfreundschaft an der deutschen Ostseeküste
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {features.map((card, index) => (
              <div key={index} className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-all duration-300 border border-warm-brown shadow-lg">
                <img 
                  src={card.image_url} 
                  alt={card.title} 
                  className="w-full h-48 object-cover"
                />
                <div className="p-8 text-center">
                  <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">{card.title}</h3>
                  <p className="text-light-beige font-light leading-relaxed">
                    {card.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Clean Food Gallery */}
      <section className="py-20 bg-medium-brown">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-serif text-center text-warm-beige mb-16 tracking-wide">
            Unsere Spezialitäten
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {specialties.map((card, index) => (
              <div 
                key={index}
                className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-warm-brown cursor-pointer"
                onClick={() => navigate('/speisekarte')}
              >
                <img src={card.image_url} alt={card.title} className="w-full h-48 object-cover" />
                <div className="p-6">
                  <h3 className="font-serif text-warm-beige text-lg tracking-wide">{card.title}</h3>
                  <p className="text-light-beige text-sm font-light">{card.description}</p>
                  {card.price && (
                    <p className="text-warm-beige font-semibold mt-2">{card.price}</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Enhanced Lieferando Section */}
      <EnhancedDeliverySection />
    </div>
  );
};

export default Home;