import React from 'react';

const GoogleReviews = () => {
  const handleRedirectToGoogle = () => {
    window.open('https://www.google.com/search?sca_esv=1b465dddb89ef670&hl=de-DE&sxsrf=AE3TifPTCHlfzGsueE5FhA1Y7gw34iRPPA:1750693794755&si=AMgyJEtREmoPL4P1I5IDCfuA8gybfVI2d5Uj7QMwYCZHKDZ-ExFC6bYc5Kk7Zl0JkSCw84yQJECdvqh15MjMcTOiH4tboA_bIbC_x-wzrBq0Q2_VIYdqZjLXVh5CxbzN6kbSycYInGMAOdGCVbzgIbFg6YtpMp23PPa_OCn242fuI99sOReum_o%3D&q=Jimmys+Tapas+Bar+-+Neustadt+in+Holstein+Rezensionen&sa=X&ved=2ahUKEwi3vvzN8oeOAxWXQvEDHVtDJWsQ0bkNegQIJxAD&biw=1920&bih=911&dpr=1', '_blank');
  };

  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Header Section */}
      <div className="relative overflow-hidden bg-gradient-to-r from-dark-brown via-medium-brown to-dark-brown">
        <div className="absolute inset-0 bg-black bg-opacity-30"></div>
        <div className="absolute inset-0">
          <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-warm-beige/10 via-transparent to-orange-500/10"></div>
          <div className="absolute -top-10 -left-10 w-40 h-40 bg-warm-beige/20 rounded-full blur-xl"></div>
          <div className="absolute -bottom-10 -right-10 w-60 h-60 bg-orange-500/20 rounded-full blur-xl"></div>
        </div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <div className="max-w-4xl mx-auto">
              <h1 className="text-6xl md:text-7xl font-serif text-warm-beige mb-6 tracking-wide drop-shadow-lg">
                Bewertungen
              </h1>
              <div className="bg-dark-brown/40 backdrop-blur-sm rounded-xl p-6 border border-warm-beige/30">
                <p className="text-xl md:text-2xl text-light-beige font-light leading-relaxed">
                  Lesen Sie echte Bewertungen unserer Gäste auf Google
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          
          {/* Google Reviews Section */}
          <div className="bg-medium-brown/50 rounded-xl p-8 border border-warm-beige/20 mb-12">
            <div className="text-center">
              <div className="flex justify-center items-center mb-6">
                <div className="bg-warm-beige/20 p-4 rounded-full">
                  <svg className="w-12 h-12 text-warm-beige" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                    <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                    <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                    <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                  </svg>
                </div>
              </div>
              
              <h2 className="text-3xl font-serif text-warm-beige mb-4">Google Bewertungen</h2>
              
              <p className="text-light-beige leading-relaxed mb-8">
                Erfahren Sie, was unsere Gäste über Jimmy's Tapas Bar sagen. 
                Lesen Sie authentische Bewertungen und Erfahrungsberichte direkt auf Google.
              </p>

              <div className="space-y-4 mb-8">
                <div className="bg-dark-brown/50 rounded-lg p-4 text-left">
                  <p className="text-light-beige text-sm mb-2">
                    <span className="text-warm-beige font-semibold">✨ Authentische Bewertungen</span>
                  </p>
                  <p className="text-light-beige text-sm">
                    Echte Erfahrungen von unseren Gästen
                  </p>
                </div>
                
                <div className="bg-dark-brown/50 rounded-lg p-4 text-left">
                  <p className="text-light-beige text-sm mb-2">
                    <span className="text-warm-beige font-semibold">⭐ Aktuelle Bewertungen</span>
                  </p>
                  <p className="text-light-beige text-sm">
                    Immer auf dem neuesten Stand
                  </p>
                </div>
                
                <div className="bg-dark-brown/50 rounded-lg p-4 text-left">
                  <p className="text-light-beige text-sm mb-2">
                    <span className="text-warm-beige font-semibold">📍 Standort-spezifisch</span>
                  </p>
                  <p className="text-light-beige text-sm">
                    Bewertungen für Neustadt in Holstein
                  </p>
                </div>
              </div>

              <button
                onClick={handleRedirectToGoogle}
                className="bg-warm-beige text-dark-brown px-8 py-4 rounded-full font-semibold text-lg hover:bg-orange-500 hover:text-white transition-all duration-300 shadow-lg hover:shadow-xl"
              >
                🔗 Google Bewertungen anzeigen
              </button>
              
              <p className="text-light-beige/70 text-sm mt-4">
                Sie werden zu Google weitergeleitet
              </p>
            </div>
          </div>

          {/* Info Section */}
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-medium-brown/30 rounded-xl p-6 border border-warm-beige/20">
              <h3 className="text-xl font-serif text-warm-beige mb-4">Warum Google Bewertungen?</h3>
              <ul className="text-light-beige space-y-2 text-sm">
                <li>• Transparenz und Authentizität</li>
                <li>• Direkte Kommunikation mit Gästen</li>
                <li>• Aktuelle und vertrauensvolle Meinungen</li>
                <li>• Teil der Google-Plattform</li>
              </ul>
            </div>
            
            <div className="bg-medium-brown/30 rounded-xl p-6 border border-warm-beige/20">
              <h3 className="text-xl font-serif text-warm-beige mb-4">Ihre Meinung zählt</h3>
              <p className="text-light-beige text-sm leading-relaxed">
                Waren Sie schon bei uns? Teilen Sie Ihre Erfahrungen mit anderen Gästen 
                und helfen Sie uns dabei, unser Angebot kontinuierlich zu verbessern.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GoogleReviews;