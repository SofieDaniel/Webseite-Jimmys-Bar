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
  const features = homepageContent?.features_data ? 
    homepageContent.features_data : [
    {
      title: "Authentische Tapas",
      description: "Traditionelle spanische Gerichte, mit Liebe zubereitet und perfekt zum Teilen",
      image: "https://images.unsplash.com/photo-1544025162-d76694265947"
    },
    {
      title: "Frische Meeresfrüchte", 
      description: "Täglich frisch aus der Ostsee und dem Mittelmeer",
      image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b"
    },
    {
      title: "Strandlage",
      description: "Genießen Sie Ihr Essen mit direktem Blick auf die Ostsee",
      image: "https://images.unsplash.com/photo-1571197119738-26123cb0d22f"
    }
  ];

  // Specialties from API or default Jimmy's menu
  const specialties = homepageContent?.specialties?.cards ? 
    homepageContent.specialties.cards : [
    {
      title: "Paella Valenciana",
      description: "Original spanische Paella mit Safran, Huhn und Gemüse",
      image: "https://images.unsplash.com/photo-1534080564583-6be75777b70a",
      price: "18,90€"
    },
    {
      title: "Gambas al Ajillo",
      description: "Knoblauchgarnelen in Olivenöl mit frischen Kräutern", 
      image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b",
      price: "12,90€"
    },
    {
      title: "Pulpo a la Gallega",
      description: "Galicischer Oktopus mit Paprika und Olivenöl",
      image: "https://images.unsplash.com/photo-1544025162-d76694265947",
      price: "14,90€"
    },
    {
      title: "Patatas Bravas",
      description: "Würzige Kartoffeln mit traditioneller Bravas-Sauce",
      image: "https://images.unsplash.com/photo-1565599837634-134bc3aadce8",
      price: "8,90€"
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
                  src={card.image} 
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
                <img src={card.image} alt={card.title} className="w-full h-48 object-cover" />
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