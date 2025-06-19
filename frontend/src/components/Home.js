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
        const response = await fetch(`/api/cms/homepage`);
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

  // Simple default content that always works
  const hero = {
    title: "JIMMY'S TAPAS BAR",
    subtitle: "an der Ostsee",
    description: "Genießen Sie authentische mediterrane Spezialitäten",
    location: "direkt an der malerischen Ostseeküste",
    background_image: "https://images.unsplash.com/photo-1656423521731-9665583f100c",
    menu_button_text: "Zur Speisekarte",
    locations_button_text: "Unsere Standorte"
  };

  const features = [
    {
      title: "Authentische Tapas",
      description: "Traditionelle spanische Rezepte mit frischen Zutaten",
      icon: "🍽️"
    },
    {
      title: "Direkt am Strand",
      description: "Genießen Sie Ihre Mahlzeit mit Blick auf die Ostsee",
      icon: "🏖️"
    },
    {
      title: "Familiär & Freundlich",
      description: "Warme Atmosphäre für die ganze Familie",
      icon: "👨‍👩‍👧‍👦"
    }
  ];

  const specialties = [
    {
      name: "Paella Valenciana",
      description: "Traditionelle Paella mit Huhn, Kaninchen und Gemüse",
      price: "18.90€",
      image: "https://images.unsplash.com/photo-1534080564583-6be75777b70a"
    },
    {
      name: "Gambas al Ajillo",
      description: "Garnelen in Knoblauchöl mit frischen Kräutern",
      price: "12.90€",
      image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b"
    }
  ];
  
  return (
    <div className="min-h-screen">
      {/* Clean Professional Hero Section */}
      <section id="main-content" className="relative h-screen bg-cover bg-center hero-background" 
               style={{backgroundImage: `url('${hero.background_image}')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-50"></div>
        <div className="relative z-10 flex items-center justify-center h-full text-center px-4" style={{paddingTop: '80px'}}>
          <div className="max-w-4xl mx-auto">
            <h1 className="text-6xl md:text-8xl font-serif font-bold text-warm-beige mb-6 tracking-wide">
              {hero.title}
            </h1>
            <p className="text-2xl md:text-3xl text-light-beige font-light mb-4 tracking-wider">
              {hero.subtitle}
            </p>
            <p className="text-xl md:text-2xl text-light-beige font-light mb-8 max-w-2xl mx-auto leading-relaxed">
              {hero.description} {hero.location}
            </p>
            <div className="space-y-4 md:space-y-0 md:space-x-6 md:flex md:justify-center">
              <button 
                onClick={() => navigate('/speisekarte')}
                className="w-full md:w-auto bg-warm-beige text-dark-brown px-8 py-4 text-lg font-semibold rounded-lg hover:bg-light-beige transition-all duration-300 transform hover:scale-105 shadow-lg"
              >
                {hero.menu_button_text}
              </button>
              <button 
                onClick={() => navigate('/standorte')}
                className="w-full md:w-auto border-2 border-warm-beige text-warm-beige px-8 py-4 text-lg font-semibold rounded-lg hover:bg-warm-beige hover:text-dark-brown transition-all duration-300 transform hover:scale-105"
              >
                {hero.locations_button_text}
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
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
            {features.map((feature, index) => (
              <div key={index} className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-all duration-300 border border-warm-brown shadow-lg">
                <div className="w-full h-48 flex items-center justify-center bg-warm-brown">
                  <span className="text-6xl">{feature.icon}</span>
                </div>
                <div className="p-8 text-center">
                  <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">{feature.title}</h3>
                  <p className="text-light-beige font-light leading-relaxed">{feature.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Specialties Section */}
      <section className="py-20 bg-medium-brown">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-serif text-center text-warm-beige mb-16 tracking-wide">
            Unsere Spezialitäten
          </h2>
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {specialties.map((specialty, index) => (
              <div 
                key={index}
                className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-warm-brown cursor-pointer"
                onClick={() => navigate('/speisekarte')}
              >
                <img src={specialty.image} alt={specialty.name} className="w-full h-48 object-cover" />
                <div className="p-6">
                  <h3 className="font-serif text-warm-beige text-lg tracking-wide">{specialty.name}</h3>
                  <p className="text-light-beige text-sm font-light">{specialty.description}</p>
                  <p className="text-warm-beige font-semibold mt-2">{specialty.price}</p>
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