import React from 'react';
import { useNavigate } from 'react-router-dom';
import EnhancedDeliverySection from './EnhancedDeliverySection';

const Home = () => {
  const navigate = useNavigate();
  
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative h-screen bg-cover bg-center" 
               style={{backgroundImage: "url('https://images.unsplash.com/photo-1656423521731-9665583f100c')"}}>
        <div className="absolute inset-0 bg-black bg-opacity-50"></div>
        <div className="relative z-10 flex items-center justify-center h-full text-center px-4" style={{paddingTop: '80px'}}>
          <div className="max-w-4xl mx-auto">
            <h1 className="text-6xl md:text-8xl font-serif font-bold text-warm-beige mb-6 tracking-wide">
              JIMMY'S TAPAS BAR
            </h1>
            <p className="text-2xl md:text-3xl text-light-beige font-light mb-4 tracking-wider">
              an der Ostsee
            </p>
            <p className="text-xl md:text-2xl text-light-beige font-light mb-8 max-w-2xl mx-auto leading-relaxed">
              Genießen Sie authentische mediterrane Spezialitäten direkt an der malerischen Ostseeküste
            </p>
            <div className="space-y-4 md:space-y-0 md:space-x-6 md:flex md:justify-center">
              <button 
                onClick={() => navigate('/speisekarte')}
                className="w-full md:w-auto bg-warm-beige text-dark-brown px-8 py-4 text-lg font-semibold rounded-lg hover:bg-light-beige transition-all duration-300 transform hover:scale-105 shadow-lg"
              >
                Zur Speisekarte
              </button>
              <button 
                onClick={() => navigate('/standorte')}
                className="w-full md:w-auto border-2 border-warm-beige text-warm-beige px-8 py-4 text-lg font-semibold rounded-lg hover:bg-warm-beige hover:text-dark-brown transition-all duration-300 transform hover:scale-105"
              >
                Unsere Standorte
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
            <div className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-all duration-300 border border-warm-brown shadow-lg">
              <div className="w-full h-48 flex items-center justify-center bg-warm-brown">
                <span className="text-6xl">🍽️</span>
              </div>
              <div className="p-8 text-center">
                <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">Authentische Tapas</h3>
                <p className="text-light-beige font-light leading-relaxed">Traditionelle spanische Rezepte mit frischen Zutaten</p>
              </div>
            </div>
            
            <div className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-all duration-300 border border-warm-brown shadow-lg">
              <div className="w-full h-48 flex items-center justify-center bg-warm-brown">
                <span className="text-6xl">🏖️</span>
              </div>
              <div className="p-8 text-center">
                <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">Direkt am Strand</h3>
                <p className="text-light-beige font-light leading-relaxed">Genießen Sie Ihre Mahlzeit mit Blick auf die Ostsee</p>
              </div>
            </div>
            
            <div className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-all duration-300 border border-warm-brown shadow-lg">
              <div className="w-full h-48 flex items-center justify-center bg-warm-brown">
                <span className="text-6xl">👨‍👩‍👧‍👦</span>
              </div>
              <div className="p-8 text-center">
                <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">Familiär & Freundlich</h3>
                <p className="text-light-beige font-light leading-relaxed">Warme Atmosphäre für die ganze Familie</p>
              </div>
            </div>
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
            <div 
              className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-warm-brown cursor-pointer"
              onClick={() => navigate('/speisekarte')}
            >
              <img src="https://images.unsplash.com/photo-1534080564583-6be75777b70a" alt="Paella Valenciana" className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="font-serif text-warm-beige text-lg tracking-wide">Paella Valenciana</h3>
                <p className="text-light-beige text-sm font-light">Traditionelle Paella mit Huhn, Kaninchen und Gemüse</p>
                <p className="text-warm-beige font-semibold mt-2">18.90€</p>
              </div>
            </div>
            
            <div 
              className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-warm-brown cursor-pointer"
              onClick={() => navigate('/speisekarte')}
            >
              <img src="https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b" alt="Gambas al Ajillo" className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="font-serif text-warm-beige text-lg tracking-wide">Gambas al Ajillo</h3>
                <p className="text-light-beige text-sm font-light">Garnelen in Knoblauchöl mit frischen Kräutern</p>
                <p className="text-warm-beige font-semibold mt-2">12.90€</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Enhanced Delivery Section */}
      <EnhancedDeliverySection />
    </div>
  );
};

export default Home;