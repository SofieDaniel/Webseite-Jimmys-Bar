import React from 'react';

const Datenschutz = () => {
  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Header Section mit spanischem Bild */}
      <div className="relative overflow-hidden bg-gradient-to-r from-dark-brown via-medium-brown to-dark-brown">
        <div className="absolute inset-0 bg-black bg-opacity-50"></div>
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage: "url('https://images.unsplash.com/photo-1571197119738-26123cb0d22f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80')"
          }}
        ></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <div className="max-w-4xl mx-auto">
              <h1 className="text-6xl md:text-7xl font-serif text-warm-beige mb-6 tracking-wide drop-shadow-lg">
                Datenschutz
              </h1>
              <div className="bg-dark-brown/40 backdrop-blur-sm rounded-xl p-6 border border-warm-beige/30">
                <p className="text-xl md:text-2xl text-light-beige font-light leading-relaxed">
                  Schutz Ihrer persönlichen Daten
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
            
            {/* Übersicht */}
            <div className="mb-12">
              <h2 className="text-2xl font-serif text-warm-beige mb-6">Datenschutzerklärung</h2>
              <div className="bg-dark-brown/30 rounded-lg p-6">
                <p className="text-light-beige leading-relaxed">
                  Wir freuen uns über Ihr Interesse an unserem Unternehmen. Der Schutz Ihrer Privatsphäre 
                  ist für uns sehr wichtig. Nachstehend informieren wir Sie ausführlich über den Umgang mit Ihren Daten.
                </p>
              </div>
            </div>

            {/* Verantwortlicher */}
            <div className="mb-8">
              <h3 className="text-xl font-serif text-warm-beige mb-4">1. Verantwortlicher</h3>
              <div className="bg-dark-brown/50 rounded-lg p-4">
                <p className="text-light-beige">
                  Jimmy's Tapas Bar<br/>
                  Jimmy Rodríguez<br/>
                  Strandstraße 1<br/>
                  18225 Kühlungsborn<br/>
                  Telefon: +49 38293 12345<br/>
                  E-Mail: info@jimmys-tapasbar.de
                </p>
              </div>
            </div>

            {/* Erhebung von Daten */}
            <div className="mb-8">
              <h3 className="text-xl font-serif text-warm-beige mb-4">2. Erhebung und Verarbeitung von Daten</h3>
              <div className="space-y-4">
                <div className="bg-dark-brown/50 rounded-lg p-4">
                  <h4 className="font-semibold text-warm-beige mb-2">Website-Besuch</h4>
                  <p className="text-light-beige">
                    Bei jedem Zugriff auf unsere Website werden automatisch Informationen erfasst. 
                    Diese Daten können nicht einer bestimmten Person zugeordnet werden.
                  </p>
                </div>
                
                <div className="bg-dark-brown/50 rounded-lg p-4">
                  <h4 className="font-semibold text-warm-beige mb-2">Kontaktformular</h4>
                  <p className="text-light-beige">
                    Wenn Sie uns über unser Kontaktformular kontaktieren, werden die von Ihnen 
                    eingegebenen Daten zur Bearbeitung Ihrer Anfrage gespeichert.
                  </p>
                </div>
                
                <div className="bg-dark-brown/50 rounded-lg p-4">
                  <h4 className="font-semibold text-warm-beige mb-2">Reservierungen</h4>
                  <p className="text-light-beige">
                    Für Tischreservierungen erheben wir Ihren Namen, Telefonnummer und 
                    gewünschte Reservierungszeit zur Durchführung der Reservierung.
                  </p>
                </div>
              </div>
            </div>

            {/* Zweck der Verarbeitung */}
            <div className="mb-8">
              <h3 className="text-xl font-serif text-warm-beige mb-4">3. Zweck der Datenverarbeitung</h3>
              <div className="bg-dark-brown/50 rounded-lg p-4">
                <ul className="text-light-beige space-y-2">
                  <li>• Bereitstellung und Verbesserung unserer Website</li>
                  <li>• Bearbeitung von Anfragen und Reservierungen</li>
                  <li>• Kommunikation mit unseren Gästen</li>
                  <li>• Erfüllung gesetzlicher Verpflichtungen</li>
                </ul>
              </div>
            </div>

            {/* Cookies */}
            <div className="mb-8">
              <h3 className="text-xl font-serif text-warm-beige mb-4">4. Cookies</h3>
              <div className="bg-dark-brown/50 rounded-lg p-4">
                <p className="text-light-beige">
                  Unsere Website verwendet Cookies, um die Benutzerfreundlichkeit zu verbessern. 
                  Sie können Ihren Browser so einstellen, dass Sie über das Setzen von Cookies informiert werden 
                  oder Cookies ganz abschalten.
                </p>
              </div>
            </div>

            {/* Ihre Rechte */}
            <div className="mb-8">
              <h3 className="text-xl font-serif text-warm-beige mb-4">5. Ihre Rechte</h3>
              <div className="bg-dark-brown/50 rounded-lg p-4">
                <p className="text-light-beige mb-4">Sie haben das Recht auf:</p>
                <ul className="text-light-beige space-y-2">
                  <li>• Auskunft über Ihre gespeicherten Daten</li>
                  <li>• Berichtigung unrichtiger Daten</li>
                  <li>• Löschung Ihrer Daten</li>
                  <li>• Einschränkung der Verarbeitung</li>
                  <li>• Datenübertragbarkeit</li>
                  <li>• Widerspruch gegen die Verarbeitung</li>
                </ul>
              </div>
            </div>

            {/* SSL-Verschlüsselung */}
            <div className="mb-8">
              <h3 className="text-xl font-serif text-warm-beige mb-4">6. SSL-Verschlüsselung</h3>
              <div className="bg-dark-brown/50 rounded-lg p-4">
                <p className="text-light-beige">
                  Diese Website nutzt zur Gewährleistung der Sicherheit der Datenverarbeitung und zum Schutz 
                  der Übertragung vertraulicher Inhalte eine SSL-Verschlüsselung.
                </p>
              </div>
            </div>

            {/* Kontakt */}
            <div className="bg-dark-brown/30 rounded-lg p-6">
              <h3 className="text-xl font-serif text-warm-beige mb-4">Fragen zum Datenschutz?</h3>
              <p className="text-light-beige">
                Bei Fragen zu dieser Datenschutzerklärung oder zur Verarbeitung Ihrer persönlichen Daten 
                kontaktieren Sie uns gerne unter:
              </p>
              <p className="text-warm-beige mt-2">
                <strong>E-Mail:</strong> datenschutz@jimmys-tapasbar.de<br/>
                <strong>Telefon:</strong> +49 38293 12345
              </p>
              <p className="text-light-beige mt-4 text-sm">
                Stand dieser Datenschutzerklärung: Januar 2024
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Datenschutz;