const Home = () => {
  const navigate = useNavigate();
  const { t } = useLanguage();
  
  return (
    <div className="min-h-screen">
      {/* Clean Professional Hero Section */}
      <section id="main-content" className="relative h-screen bg-cover bg-center hero-background" 
               style={{backgroundImage: `url('https://images.unsplash.com/photo-1656423521731-9665583f100c')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-50"></div>
        <div className="relative z-10 flex items-center justify-center h-full text-center px-4" style={{paddingTop: '80px'}}>
          <div className="max-w-4xl">
            {/* Clean Main Headline with proper spacing */}
            <h1 className="hero-headline font-serif text-warm-beige mb-8 tracking-wide leading-tight drop-shadow-text" style={{fontSize: 'clamp(2.5rem, 8vw, 6rem)', lineHeight: '1.1', marginTop: '40px'}}>
              {t('home.heroTitle')}<br />
              <span className="font-light opacity-90" style={{fontSize: 'clamp(1.8rem, 5vw, 4rem)'}}>{t('home.heroSubtitle')}</span>
            </h1>
            
            {/* Simple Subtitle */}
            <p className="text-xl md:text-2xl text-warm-beige font-light mb-12 max-w-3xl mx-auto leading-relaxed opacity-95">
              {t('home.heroDescription')}<br/>
              <span className="text-lg opacity-80">{t('home.heroLocation')}</span>
            </p>
            
            {/* Clean CTA Buttons */}
            <div className="flex flex-col md:flex-row justify-center gap-6">
              <button 
                onClick={() => navigate('/speisekarte')}
                className="bg-warm-beige text-dark-brown hover:bg-light-beige px-10 py-4 rounded-lg text-lg font-medium transition-all duration-300 tracking-wide shadow-lg hover:shadow-xl"
              >
                {t('home.menuButton')}
              </button>
              <button 
                onClick={() => navigate('/standorte')}
                className="border-2 border-warm-beige text-warm-beige hover:bg-warm-beige hover:text-dark-brown px-10 py-4 rounded-lg text-lg font-medium transition-all duration-300 tracking-wide shadow-lg hover:shadow-xl"
              >
                {t('home.locationsButton')}
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Professional Features Section - Clean Design like "Unsere Spezialitäten" */}
      <section className="py-24 bg-gradient-to-b from-dark-brown to-medium-brown">
        <div className="container mx-auto px-4">
          <div className="text-center mb-20">
            <h2 className="text-5xl font-serif text-warm-beige mb-8 tracking-wide">
              Spanische Tradition
            </h2>
            <p className="text-xl text-light-beige font-light leading-relaxed max-w-3xl mx-auto">
              Erleben Sie authentische spanische Gastfreundschaft an der deutschen Ostseeküste
            </p>
          </div>
          
          {/* Clean Three Cards - Professional Layout with Product Images */}
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <div className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-all duration-300 border border-warm-brown shadow-lg">
              <img 
                src="https://images.pexels.com/photos/19671352/pexels-photo-19671352.jpeg" 
                alt="Authentische Tapas" 
                className="w-full h-48 object-cover"
              />
              <div className="p-8 text-center">
                <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">Authentische Tapas</h3>
                <p className="text-light-beige font-light leading-relaxed">
                  Traditionelle spanische Gerichte, mit Liebe zubereitet und perfekt zum Teilen
                </p>
              </div>
            </div>
            
            <div className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-all duration-300 border border-warm-brown shadow-lg">
              <img 
                src="https://images.unsplash.com/photo-1694685367640-05d6624e57f1" 
                alt="Frische Paella" 
                className="w-full h-48 object-cover"
              />
              <div className="p-8 text-center">
                <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">Frische Paella</h3>
                <p className="text-light-beige font-light leading-relaxed">
                  Täglich hausgemacht mit Meeresfrüchten, Gemüse oder Huhn
                </p>
              </div>
            </div>
            
            <div className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-all duration-300 border border-warm-brown shadow-lg">
              <img 
                src="https://images.pexels.com/photos/32508247/pexels-photo-32508247.jpeg" 
                alt="Strandnähe mit Strandkörben" 
                className="w-full h-48 object-cover"
              />
              <div className="p-8 text-center">
                <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">Strandnähe</h3>
                <p className="text-light-beige font-light leading-relaxed">
                  Beide Standorte direkt an der malerischen Ostseeküste – perfekt für entspannte Stunden
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Clean Food Gallery - Professional with Navigation */}
      <section className="py-20 bg-medium-brown">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-serif text-center text-warm-beige mb-16 tracking-wide">
            Unsere Spezialitäten
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div 
              className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-warm-brown cursor-pointer"
              onClick={() => {
                navigate('/speisekarte');
                // Set category after navigation
                setTimeout(() => {
                  window.location.href = '/speisekarte#tapas-vegetarian';
                }, 100);
              }}
            >
              <img src="https://images.unsplash.com/photo-1565599837634-134bc3aadce8" alt="Patatas Bravas" className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="font-serif text-warm-beige text-lg tracking-wide">Patatas Bravas</h3>
                <p className="text-light-beige text-sm font-light">Klassische spanische Kartoffeln</p>
              </div>
            </div>
            <div 
              className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-warm-brown cursor-pointer"
              onClick={() => {
                navigate('/speisekarte');
                setTimeout(() => {
                  window.location.href = '/speisekarte#tapa-paella';
                }, 100);
              }}
            >
              <img src="https://images.pexels.com/photos/7085661/pexels-photo-7085661.jpeg" alt="Paella" className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="font-serif text-warm-beige text-lg tracking-wide">Paella Valenciana</h3>
                <p className="text-light-beige text-sm font-light">Traditionelle spanische Paella</p>
              </div>
            </div>
            <div 
              className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-warm-brown cursor-pointer"
              onClick={() => {
                navigate('/speisekarte');
                setTimeout(() => {
                  window.location.href = '/speisekarte#inicio';
                }, 100);
              }}
            >
              <img src="https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg" alt="Tapas" className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="font-serif text-warm-beige text-lg tracking-wide">Tapas Variación</h3>
                <p className="text-light-beige text-sm font-light">Auswahl spanischer Köstlichkeiten</p>
              </div>
            </div>
            <div 
              className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-warm-brown cursor-pointer"
              onClick={() => {
                navigate('/speisekarte');
                setTimeout(() => {
                  window.location.href = '/speisekarte#tapas-pescado';
                }, 100);
              }}
            >
              <img src="https://images.unsplash.com/photo-1619860705243-dbef552e7118" alt="Gambas al Ajillo" className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="font-serif text-warm-beige text-lg tracking-wide">Gambas al Ajillo</h3>
                <p className="text-light-beige text-sm font-light">Garnelen in Knoblauchöl</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Lieferando Section */}
      <section className="py-16 bg-gradient-to-r from-dark-brown to-medium-brown">
        <div className="container mx-auto px-4 text-center">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-4xl font-serif text-warm-beige mb-8 tracking-wide">
              Jetzt auch bequem nach Hause bestellen
            </h2>
            <p className="text-xl text-light-beige font-light mb-12 leading-relaxed">
              Genießen Sie unsere authentischen spanischen Spezialitäten gemütlich zu Hause.<br/>
              Bestellen Sie direkt über Lieferando und lassen Sie sich verwöhnen.
            </p>
            <div className="bg-dark-brown rounded-lg p-8 border border-warm-brown shadow-lg">
              <div className="flex flex-col md:flex-row items-center justify-center gap-8">
                <div className="text-center">
                  <div className="w-24 h-24 bg-cover bg-center rounded-lg mx-auto mb-4 border-2 border-warm-beige" 
                       style={{backgroundImage: `url('https://images.pexels.com/photos/6969962/pexels-photo-6969962.jpeg')`}}>
                  </div>
                  <h3 className="text-xl font-serif text-warm-beige mb-2">Schnelle Lieferung</h3>
                  <p className="text-light-beige text-sm">Frisch und warm zu Ihnen</p>
                </div>
                <div className="text-center">
                  <a 
                    href="https://www.lieferando.de" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="inline-block bg-orange-500 hover:bg-orange-600 text-white px-8 py-4 rounded-lg text-lg font-medium transition-all duration-300 tracking-wide shadow-lg hover:shadow-xl transform hover:scale-105"
                  >
                    Jetzt bei Lieferando bestellen
                  </a>
                  <p className="text-light-beige text-sm mt-2">Verfügbar für beide Standorte</p>
                </div>
                <div className="text-center">
                  <div className="w-24 h-24 bg-cover bg-center rounded-lg mx-auto mb-4 border-2 border-warm-beige" 
                       style={{backgroundImage: `url('https://images.pexels.com/photos/31748679/pexels-photo-31748679.jpeg')`}}>
                  </div>
                  <h3 className="text-xl font-serif text-warm-beige mb-2">Authentisch Spanisch</h3>
                  <p className="text-light-beige text-sm">Direkt vom Küchenchef</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

// Menu Page Component - Mouseover with detailed information only
