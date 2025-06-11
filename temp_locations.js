const Standorte = () => {
  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Elegant Header Section with Background */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('https://images.pexels.com/photos/26626726/pexels-photo-26626726.jpeg')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              Unsere Standorte
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              Besuchen Sie uns an der malerischen Ostseeküste
            </p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-16">
        <div className="grid lg:grid-cols-2 gap-16 max-w-7xl mx-auto">
          {/* Neustadt Location - Enhanced */}
          <div className="bg-dark-brown rounded-xl border border-warm-brown overflow-hidden shadow-2xl">
            <div className="relative">
              <img 
                src="https://images.unsplash.com/photo-1665758564776-f2aa6b41327e" 
                alt="Jimmy's Tapas Bar Neustadt" 
                className="w-full h-72 object-cover"
              />
              <div className="absolute top-4 left-4 bg-warm-beige text-dark-brown px-4 py-2 rounded-lg">
                <span className="font-serif font-semibold">Hauptstandort</span>
              </div>
            </div>
            <div className="p-8">
              <h2 className="text-3xl font-serif text-warm-beige mb-6 tracking-wide">
                Jimmy's Tapas Bar Neustadt
              </h2>
              <div className="space-y-6 text-light-beige">
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-xl text-dark-brown">📍</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-warm-beige mb-1">Adresse</h3>
                    <p className="font-light text-lg">Am Strande 21</p>
                    <p className="font-light">23730 Neustadt in Holstein</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-xl text-dark-brown">🕒</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-warm-beige mb-1">Öffnungszeiten</h3>
                    <p className="font-light">Mo-So: 12:00–22:00 Uhr</p>
                    <p className="text-sm text-warm-beige font-light">(Sommersaison)</p>
                    <p className="text-sm text-orange-400 font-light">Winterbetrieb unregelmäßig</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-xl text-dark-brown">📞</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-warm-beige mb-1">Kontakt</h3>
                    <p className="font-light">+49 (0) 4561 123456</p>
                    <p className="font-light text-sm">neustadt@jimmys-tapasbar.de</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-xl text-dark-brown">🏖️</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-warm-beige mb-1">Besonderheiten</h3>
                    <p className="font-light text-sm">Direkt am Strand • Terrasse mit Meerblick</p>
                    <p className="font-light text-sm">Parkplätze vorhanden • Familienfreundlich</p>
                  </div>
                </div>
              </div>
              <div className="mt-8">
                <a 
                  href="https://www.google.com/maps/dir/?api=1&destination=Am+Strande+21,+23730+Neustadt+in+Holstein,+Germany"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full bg-warm-beige hover:bg-light-beige text-dark-brown px-6 py-3 rounded-lg font-medium transition-colors inline-block text-center"
                >
                  Route planen
                </a>
              </div>
            </div>
          </div>

          {/* Großenbrode Location - Enhanced */}
          <div className="bg-dark-brown rounded-xl border border-warm-brown overflow-hidden shadow-2xl">
            <div className="relative">
              <img 
                src="https://images.unsplash.com/photo-1665758564796-5162ff406254" 
                alt="Jimmy's Tapas Bar Großenbrode" 
                className="w-full h-72 object-cover"
              />
              <div className="absolute top-4 left-4 bg-orange-500 text-white px-4 py-2 rounded-lg">
                <span className="font-serif font-semibold">Zweigstelle</span>
              </div>
            </div>
            <div className="p-8">
              <h2 className="text-3xl font-serif text-warm-beige mb-6 tracking-wide">
                Jimmy's Tapas Bar Großenbrode
              </h2>
              <div className="space-y-6 text-light-beige">
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-xl text-dark-brown">📍</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-warm-beige mb-1">Adresse</h3>
                    <p className="font-light text-lg">Südstrand 54</p>
                    <p className="font-light">23755 Großenbrode</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-xl text-dark-brown">🕒</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-warm-beige mb-1">Öffnungszeiten</h3>
                    <p className="font-light">Mo-So: 12:00–22:00 Uhr</p>
                    <p className="text-sm text-warm-beige font-light">(Sommersaison)</p>
                    <p className="text-sm text-orange-400 font-light">Winterbetrieb unregelmäßig</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-xl text-dark-brown">📞</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-warm-beige mb-1">Kontakt</h3>
                    <p className="font-light">+49 (0) 4561 789012</p>
                    <p className="font-light text-sm">grossenbrode@jimmys-tapasbar.de</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-warm-beige rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-xl text-dark-brown">🌊</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-warm-beige mb-1">Besonderheiten</h3>
                    <p className="font-light text-sm">Strandnähe • Gemütliche Atmosphäre</p>
                    <p className="font-light text-sm">Kostenlose Parkplätze • Hundefreundlich</p>
                  </div>
                </div>
              </div>
              <div className="mt-8">
                <a 
                  href="https://www.google.com/maps/dir/?api=1&destination=Südstrand+54,+23755+Großenbrode,+Germany"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full bg-warm-beige hover:bg-light-beige text-dark-brown px-6 py-3 rounded-lg font-medium transition-colors inline-block text-center"
                >
                  Route planen
                </a>
              </div>
            </div>
          </div>
        </div>

        {/* Additional Information Section */}
        <div className="mt-16 bg-dark-brown rounded-xl border border-warm-brown p-8">
          <h3 className="text-3xl font-serif text-warm-beige mb-8 text-center tracking-wide">
            Warum Jimmy's Tapas Bar?
          </h3>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-24 h-24 bg-cover bg-center rounded-lg mx-auto mb-4 border-2 border-warm-beige" 
                   style={{backgroundImage: `url('https://images.pexels.com/photos/16715741/pexels-photo-16715741.jpeg')`}}>
              </div>
              <h4 className="text-xl font-serif text-warm-beige mb-2">Authentische Atmosphäre</h4>
              <p className="text-light-beige font-light text-sm">
                Erleben Sie echtes spanisches Flair in gemütlicher Atmosphäre direkt an der Ostsee.
              </p>
            </div>
            <div className="text-center">
              <div className="w-24 h-24 bg-cover bg-center rounded-lg mx-auto mb-4 border-2 border-warm-beige" 
                   style={{backgroundImage: `url('https://images.pexels.com/photos/9570408/pexels-photo-9570408.jpeg')`}}>
              </div>
              <h4 className="text-xl font-serif text-warm-beige mb-2">Traditionelle Küche</h4>
              <p className="text-light-beige font-light text-sm">
                Frisch zubereitete Paella und Tapas nach original spanischen Familienrezepten.
              </p>
            </div>
            <div className="text-center">
              <div className="w-24 h-24 bg-cover bg-center rounded-lg mx-auto mb-4 border-2 border-warm-beige" 
                   style={{backgroundImage: `url('https://images.pexels.com/photos/8696561/pexels-photo-8696561.jpeg')`}}>
              </div>
              <h4 className="text-xl font-serif text-warm-beige mb-2">Spanisches Lebensgefühl</h4>
              <p className="text-light-beige font-light text-sm">
                Genießen Sie entspannte Abende mit spanischen Weinen und der besten Tapas-Auswahl.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Reviews Page Component
