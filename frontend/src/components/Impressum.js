import React from 'react';

const Impressum = () => {
  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Header Section mit spanischem Bild */}
      <div className="relative overflow-hidden bg-gradient-to-r from-dark-brown via-medium-brown to-dark-brown">
        <div className="absolute inset-0 bg-black bg-opacity-50"></div>
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage: "url('https://images.unsplash.com/photo-1533777857889-4be7c70b33f7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80')"
          }}
        ></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <div className="max-w-4xl mx-auto">
              <h1 className="text-6xl md:text-7xl font-serif text-warm-beige mb-6 tracking-wide drop-shadow-lg">
                Impressum
              </h1>
              <div className="bg-dark-brown/40 backdrop-blur-sm rounded-xl p-6 border border-warm-beige/30">
                <p className="text-xl md:text-2xl text-light-beige font-light leading-relaxed">
                  Rechtliche Informationen
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          <div className="bg-medium-brown/50 rounded-xl p-8 border border-warm-beige/20">
            
            {/* Schnellkontakt */}
            <div className="grid md:grid-cols-2 gap-8 mb-12">
              <div>
                <h2 className="text-2xl font-serif text-warm-beige mb-6">Schnellkontakt</h2>
                
                <div className="space-y-4">
                  <div className="bg-dark-brown/50 rounded-lg p-4">
                    <h3 className="text-lg font-semibold text-warm-beige mb-2">Geschäftsführung</h3>
                    <p className="text-light-beige">Jimmy Rodríguez</p>
                  </div>
                  
                  <div className="bg-dark-brown/50 rounded-lg p-4">
                    <h3 className="text-lg font-semibold text-warm-beige mb-2">Adresse</h3>
                    <p className="text-light-beige">Strandstraße 1, 18225 Kühlungsborn</p>
                  </div>
                  
                  <div className="bg-dark-brown/50 rounded-lg p-4">
                    <h3 className="text-lg font-semibold text-warm-beige mb-2">Telefon</h3>
                    <p className="text-light-beige">+49 38293 12345</p>
                  </div>
                  
                  <div className="bg-dark-brown/50 rounded-lg p-4">
                    <h3 className="text-lg font-semibold text-warm-beige mb-2">E-Mail</h3>
                    <p className="text-light-beige">info@jimmys-tapasbar.de</p>
                  </div>
                </div>
              </div>
              
              <div>
                <h2 className="text-2xl font-serif text-warm-beige mb-6">Rechtliche Angaben</h2>
                
                <div className="space-y-4">
                  <div className="bg-dark-brown/50 rounded-lg p-4">
                    <h3 className="text-lg font-semibold text-warm-beige mb-2">Handelsregister</h3>
                    <p className="text-light-beige">HRB 12345<br/>Amtsgericht Rostock</p>
                  </div>
                  
                  <div className="bg-dark-brown/50 rounded-lg p-4">
                    <h3 className="text-lg font-semibold text-warm-beige mb-2">Steuer-Nr.</h3>
                    <p className="text-light-beige">123/456/78901</p>
                  </div>
                  
                  <div className="bg-dark-brown/50 rounded-lg p-4">
                    <h3 className="text-lg font-semibold text-warm-beige mb-2">USt-IdNr.</h3>
                    <p className="text-light-beige">DE 123456789</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Detaillierte Angaben */}
            <div className="bg-dark-brown/30 rounded-lg p-6">
              <h2 className="text-2xl font-serif text-warm-beige mb-6">Angaben gemäß § 5 TMG</h2>
              
              <div className="prose prose-invert max-w-none text-light-beige">
                <h3 className="text-xl font-serif text-warm-beige mt-6 mb-3">Diensteanbieter</h3>
                <p>Jimmy's Tapas-Bar<br/>
                Ravinder Pal Singh<br/>
                Am Strande 21 Promenade<br/>
                23730 Neustadt in Holstein</p>

                <h3 className="text-xl font-serif text-warm-beige mt-6 mb-3">Kontaktmöglichkeiten</h3>
                <p><strong>Telefon:</strong> +49 4561 123456<br/>
                <strong>E-Mail-Adresse:</strong> info@jimmys-tapasbar.de</p>

                <h3 className="text-xl font-serif text-warm-beige mt-6 mb-3">Verantwortlich für den Inhalt</h3>
                <p>Ravinder Pal Singh (Anschrift wie oben)</p>

                <h3 className="text-xl font-serif text-warm-beige mt-6 mb-3">EU-Streitschlichtung</h3>
                <p>Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung (OS) bereit: 
                <a href="https://ec.europa.eu/consumers/odr/" target="_blank" rel="noopener noreferrer" className="text-warm-beige hover:text-orange-500">
                  https://ec.europa.eu/consumers/odr/
                </a></p>

                <h3 className="text-xl font-serif text-warm-beige mt-6 mb-3">Verbraucherstreitbeilegung</h3>
                <p>Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer 
                Verbraucherschlichtungsstelle teilzunehmen.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Impressum;