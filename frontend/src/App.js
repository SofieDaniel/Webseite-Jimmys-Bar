import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Link, useNavigate } from "react-router-dom";

// Cookie Consent Banner Component
const CookieBanner = () => {
  const [showBanner, setShowBanner] = useState(false);

  useEffect(() => {
    const cookieConsent = localStorage.getItem('cookieConsent');
    if (!cookieConsent) {
      setShowBanner(true);
    }
  }, []);

  const acceptAllCookies = () => {
    localStorage.setItem('cookieConsent', 'all');
    setShowBanner(false);
  };

  const acceptNecessaryCookies = () => {
    localStorage.setItem('cookieConsent', 'necessary');
    setShowBanner(false);
  };

  if (!showBanner) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-dark-brown-solid border-t-2 border-warm-beige p-6 z-50 shadow-2xl">
      <div className="container mx-auto max-w-6xl">
        <div className="flex flex-col md:flex-row items-start md:items-center gap-4">
          <div className="flex-1">
            <h3 className="text-lg font-serif text-warm-beige mb-2">Cookie-Einstellungen</h3>
            <p className="text-light-beige text-sm font-light leading-relaxed">
              Wir verwenden Cookies, um Ihnen die bestmögliche Erfahrung auf unserer Website zu bieten. 
              Einige Cookies sind notwendig für die Funktion der Website, andere helfen uns bei der Analyse und Verbesserung.
            </p>
            <Link to="/datenschutz" className="text-warm-beige hover:text-white text-sm underline">
              Mehr in der Datenschutzerklärung
            </Link>
          </div>
          <div className="flex gap-3">
            <button
              onClick={acceptNecessaryCookies}
              className="px-4 py-2 border border-warm-beige text-warm-beige hover:bg-warm-beige hover:text-dark-brown rounded transition-colors text-sm font-light"
            >
              Nur erforderliche
            </button>
            <button
              onClick={acceptAllCookies}
              className="px-6 py-2 bg-warm-beige text-dark-brown hover:bg-light-beige rounded transition-colors text-sm font-light"
            >
              Alle akzeptieren
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Header Component - FIXED positioning with proper spacing
const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-dark-brown-transparent backdrop-blur-sm">
      <div className="container mx-auto px-8 py-4">
        <nav className="flex justify-between items-center">
          <Link to="/" className="text-xl font-light text-stone-100 tracking-[0.2em]">
            JIMMY'S
            <span className="block text-xs text-stone-300 tracking-[0.3em] font-light mt-1">TAPAS BAR</span>
          </Link>
          
          <div className="hidden md:flex space-x-10">
            <Link to="/" className="text-stone-100 hover:text-stone-300 transition-colors font-light tracking-wide text-sm">Startseite</Link>
            <Link to="/standorte" className="text-stone-100 hover:text-stone-300 transition-colors font-light tracking-wide text-sm">Standorte</Link>
            <Link to="/speisekarte" className="text-stone-100 hover:text-stone-300 transition-colors font-light tracking-wide text-sm">Speisekarte</Link>
            <Link to="/bewertungen" className="text-stone-100 hover:text-stone-300 transition-colors font-light tracking-wide text-sm">Bewertungen</Link>
            <Link to="/ueber-uns" className="text-stone-100 hover:text-stone-300 transition-colors font-light tracking-wide text-sm">Über uns</Link>
            <Link to="/kontakt" className="text-stone-100 hover:text-stone-300 transition-colors font-light tracking-wide text-sm">Kontakt</Link>
          </div>
          
          <Link to="/speisekarte" className="hidden md:block border border-stone-300 text-stone-100 hover:bg-stone-100 hover:text-black px-6 py-2 rounded-full transition-all duration-300 font-light tracking-wider text-xs">
            ZUR SPEISEKARTE
          </Link>
          
          <button 
            className="md:hidden"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            <div className="w-5 h-5 flex flex-col justify-center space-y-1">
              <div className="w-5 h-0.5 bg-stone-100"></div>
              <div className="w-5 h-0.5 bg-stone-100"></div>
              <div className="w-5 h-0.5 bg-stone-100"></div>
            </div>
          </button>
        </nav>
        
        {isMenuOpen && (
          <div className="md:hidden mt-4 bg-black bg-opacity-90 rounded-lg p-4">
            <Link to="/" className="block py-2 text-stone-100 hover:text-stone-300 font-light">Startseite</Link>
            <Link to="/standorte" className="block py-2 text-stone-100 hover:text-stone-300 font-light">Standorte</Link>
            <Link to="/speisekarte" className="block py-2 text-stone-100 hover:text-stone-300 font-light">Speisekarte</Link>
            <Link to="/bewertungen" className="block py-2 text-stone-100 hover:text-stone-300 font-light">Bewertungen</Link>
            <Link to="/ueber-uns" className="block py-2 text-stone-100 hover:text-stone-300 font-light">Über uns</Link>
            <Link to="/kontakt" className="block py-2 text-stone-100 hover:text-stone-300 font-light">Kontakt</Link>
          </div>
        )}
      </div>
    </header>
  );
};

// Home Page Component - EXACT match to reference image
const Home = () => {
  const navigate = useNavigate();
  
  return (
    <div className="min-h-screen">
      {/* Hero Section - EXACT match to reference image */}
      <section className="relative h-screen bg-cover bg-center hero-background" 
               style={{backgroundImage: `url('https://images.pexels.com/photos/5975429/pexels-photo-5975429.jpeg')`}}>
        <div className="absolute inset-0 bg-hero-overlay"></div>
        <div className="relative z-10 flex items-center justify-center h-full text-center px-4">
          <div className="max-w-6xl">
            {/* Main Headline - exactly as in reference */}
            <h1 className="hero-headline font-serif text-warm-beige mb-16 tracking-wide leading-tight drop-shadow-text">
              AUTHENTISCHE<br />
              TAPAS & WEIN
            </h1>
            
            {/* CTA Button - exactly as in reference */}
            <div className="flex justify-center">
              <button 
                onClick={() => navigate('/standorte')}
                className="border-2 border-warm-beige text-warm-beige hover:bg-warm-beige hover:text-dark-brown px-12 py-4 rounded-lg text-lg font-light transition-all duration-500 tracking-wide bg-transparent backdrop-blur-sm"
              >
                STANDORT WÄHLEN
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section - Professional redesign with new content */}
      <section className="py-20 bg-warm-brown">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-5xl font-serif text-warm-beige mb-6 tracking-wide">
              Spanische Genusskultur an der Ostsee
            </h2>
            <p className="text-xl text-light-beige font-light leading-relaxed max-w-4xl mx-auto">
              Erleben Sie echte Tapas, frische Paella und mediterrane Lebensfreude – direkt in Grömitz und Neustadt.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-12 max-w-6xl mx-auto">
            <div className="text-center bg-dark-brown rounded-lg p-8 border border-warm-brown hover:bg-medium-brown transition-all duration-300">
              <div className="w-20 h-20 bg-warm-beige rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl">🍷</span>
              </div>
              <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">Authentische Tapas</h3>
              <div className="w-16 h-0.5 bg-warm-beige mx-auto mb-4"></div>
              <p className="text-light-beige font-light leading-relaxed">
                Traditionelle spanische Gerichte, mit Liebe zubereitet und perfekt zum Teilen.
              </p>
            </div>
            
            <div className="text-center bg-dark-brown rounded-lg p-8 border border-warm-brown hover:bg-medium-brown transition-all duration-300">
              <div className="w-20 h-20 bg-warm-beige rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl">🥘</span>
              </div>
              <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">Frische Paella</h3>
              <div className="w-16 h-0.5 bg-warm-beige mx-auto mb-4"></div>
              <p className="text-light-beige font-light leading-relaxed">
                Täglich frisch serviert – mit Meeresfrüchten, Gemüse oder Huhn.
              </p>
            </div>
            
            <div className="text-center bg-dark-brown rounded-lg p-8 border border-warm-brown hover:bg-medium-brown transition-all duration-300">
              <div className="w-20 h-20 bg-warm-beige rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl">🏖️</span>
              </div>
              <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">Zwei Standorte an der Küste</h3>
              <div className="w-16 h-0.5 bg-warm-beige mx-auto mb-4"></div>
              <p className="text-light-beige font-light leading-relaxed">
                Genießen Sie unsere Küche in Grömitz oder Neustadt – immer in Strandnähe.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Food Gallery */}
      <section className="py-20 bg-medium-brown">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-serif text-center text-warm-beige mb-16 tracking-wide">
            Unsere Spezialitäten
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-warm-brown">
              <img src="https://images.unsplash.com/photo-1565599837634-134bc3aadce8" alt="Patatas Bravas" className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="font-serif text-warm-beige text-lg tracking-wide">Patatas Bravas</h3>
                <p className="text-light-beige text-sm font-light">Klassische spanische Kartoffeln</p>
              </div>
            </div>
            <div className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-warm-brown">
              <img src="https://images.unsplash.com/photo-1630175860333-5131bda75071" alt="Paella" className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="font-serif text-warm-beige text-lg tracking-wide">Paella Valenciana</h3>
                <p className="text-light-beige text-sm font-light">Traditionelle spanische Paella</p>
              </div>
            </div>
            <div className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-warm-brown">
              <img src="https://images.pexels.com/photos/17336549/pexels-photo-17336549.jpeg" alt="Tapas" className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="font-serif text-warm-beige text-lg tracking-wide">Tapas Variation</h3>
                <p className="text-light-beige text-sm font-light">Auswahl spanischer Köstlichkeiten</p>
              </div>
            </div>
            <div className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-warm-brown">
              <img src="https://images.unsplash.com/photo-1588276552401-30058a0fe57b" alt="Seafood Paella" className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="font-serif text-warm-beige text-lg tracking-wide">Paella Mariscos</h3>
                <p className="text-light-beige text-sm font-light">Meeresfrüchte-Paella</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

// Menu Page Component - Fixed Layout with proper images between name and price
const Speisekarte = () => {
  const [selectedCategory, setSelectedCategory] = useState('alle');
  
  // Complete menu data with authentic, dish-specific images
  const menuItems = {
    'inicio': [
      { name: 'Aioli', description: 'Spanische Knoblauch-Mayonnaise', price: '3,50', image: 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f' },
      { name: 'Oliven', description: 'Marinierte spanische Oliven', price: '3,90', image: 'https://images.unsplash.com/photo-1714583357992-98f0ad946902' },
      { name: 'Extra Brot', description: 'Frisches spanisches Brot', price: '1,90', image: 'https://images.unsplash.com/photo-1549931319-a545dcf3bc73' },
      { name: 'Hummus', description: 'Cremiger Kichererbsen-Dip', price: '3,90', image: 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f' },
      { name: 'Guacamole', description: 'Frische Avocado-Creme', price: '3,90', image: 'https://images.unsplash.com/photo-1553909489-cd47e0ef937f' },
      { name: 'Spanischer Käseteller', description: 'Auswahl spanischer Käsesorten', price: '8,90', image: 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d' },
      { name: 'Schinken-Käse-Wurst Teller', description: 'Spanische Charcuterie-Platte', price: '11,90', image: 'https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg' },
      { name: 'Jamón Serrano Teller', description: 'Hochwertiger spanischer Schinken', price: '9,90', image: 'https://images.pexels.com/photos/24706530/pexels-photo-24706530.jpeg' },
      { name: 'Boquerones en Vinagre', description: 'Sardellen in Essig eingelegt', price: '8,90', image: 'https://images.unsplash.com/photo-1565299507177-b0ac66763828' },
      { name: 'Pata Negra', description: 'Premium Iberico Schinken', price: '10,90', image: 'https://images.unsplash.com/photo-1598989519542-077da0f51c09' },
      { name: 'Tres (Hummus, Avocado Cream, Aioli mit Brot)', description: 'Drei köstliche Dips mit Brot', price: '10,90', image: 'https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg' }
    ],
    'salat': [
      { name: 'Ensalada Mixta', description: 'Gemischter Salat mit spanischen Zutaten', price: '8,90', image: 'https://images.unsplash.com/photo-1540420773420-3366772f4999' },
      { name: 'Ensalada Tonno', description: 'Salat mit Thunfisch', price: '14,90', image: 'https://images.unsplash.com/photo-1551248429-40975aa4de74' },
      { name: 'Ensalada Pollo', description: 'Salat mit gegrilltem Hähnchen', price: '14,90', image: 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd' },
      { name: 'Ensalada Garnelen', description: 'Salat mit frischen Garnelen', price: '15,90', image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b' }
    ],
    'kleiner-salat': [
      { name: 'Tomaten/Gurken mit Zwiebeln', description: 'Frischer Gemüsesalat', price: '6,90', image: 'https://images.unsplash.com/photo-1567306226416-28f0efdc88ce' },
      { name: 'Rote Beete mit Ziegenkäse', description: 'Süße rote Beete mit cremigem Ziegenkäse', price: '7,90', image: 'https://images.unsplash.com/photo-1547592180-85f173990554' },
      { name: 'Kichererbsen mit Feta', description: 'Proteinreicher Salat mit Feta', price: '7,90', image: 'https://images.unsplash.com/photo-1551248429-40975aa4de74' }
    ],
    'tapa-paella': [
      { name: 'Paella mit Hähnchen & Meeresfrüchten', description: 'Traditionelle spanische Paella als Tapa-Portion', price: '8,90', image: 'https://images.pexels.com/photos/7085661/pexels-photo-7085661.jpeg' },
      { name: 'Paella vegetarisch', description: 'Vegetarische Paella mit frischem Gemüse', price: '7,90', image: 'https://images.pexels.com/photos/10750986/pexels-photo-10750986.jpeg' }
    ],
    'tapas-vegetarian': [
      { name: 'Gebratenes Gemüse', description: 'Vegan - Saisonales Gemüse mediterran gewürzt', price: '6,90', image: 'https://images.unsplash.com/photo-1518779578993-ec3579fee39f' },
      { name: 'Papas Bravas', description: 'Vegan - Klassische spanische Kartoffeln mit scharfer Soße', price: '6,90', image: 'https://images.unsplash.com/photo-1565599837634-134bc3aadce8' },
      { name: 'Tortilla de Patata mit Aioli', description: 'Spanisches Kartoffel-Omelett mit Aioli', price: '6,90', image: 'https://images.unsplash.com/photo-1639669794539-952631b44515' },
      { name: 'Pimientos de Padrón', description: 'Vegan - Gebratene grüne Paprika', price: '6,90', image: 'https://images.unsplash.com/photo-1584464491033-06628f3a6b7b' },
      { name: 'Kanarische Kartoffeln', description: 'Vegan - Traditionelle Kartoffeln mit Meersalz', price: '6,90', image: 'https://images.unsplash.com/photo-1518977676601-b53f82aba655' },
      { name: 'Fetahäppchen auf Johannisbeersauce', description: 'Cremiger Feta mit süß-saurer Sauce', price: '6,90', image: 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f' },
      { name: 'Ziegenkäse auf Johannisbeersauce oder Honig-Senf', description: 'Mild-cremiger Ziegenkäse mit Sauce nach Wahl', price: '6,90', image: 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d' },
      { name: 'Falafel mit Joghurt-Minz-Sauce', description: 'Knusprige Kichererbsenbällchen mit erfrischender Sauce', price: '6,90', image: 'https://images.unsplash.com/photo-1593504049359-74330189a5d8' },
      { name: 'Überbackener Feta mit Cherrytomaten', description: 'Warmer Feta mit süßen Cherrytomaten', price: '6,90', image: 'https://images.unsplash.com/photo-1570197788417-0e82375c9371' },
      { name: 'Champignons mit Reis & Pinienkernen auf Roquefort', description: 'Aromatische Pilze mit würzigem Käse', price: '6,90', image: 'https://images.unsplash.com/photo-1614887009518-7b9355a3a0e4' },
      { name: 'Überbackene Tomaten mit Spinat & Roquefort', description: 'Mediterrane Gemüse-Käse-Kombination', price: '6,90', image: 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f' },
      { name: 'Frittierte Auberginen mit Honig', description: 'Süß-herzhafte Auberginen-Kreation', price: '6,90', image: 'https://images.unsplash.com/photo-1526057565006-20beab8dd2ed' },
      { name: 'Champignons al Ajillo', description: 'Vegan - Pilze in Knoblauchöl', price: '6,90', image: 'https://images.unsplash.com/photo-1505851498219-ee2449c18936' },
      { name: 'Teigtaschen mit Spinat & Kräutersauce', description: 'Hausgemachte Teigtaschen mit frischen Kräutern', price: '6,90', image: 'https://images.unsplash.com/photo-1574484284002-952d92456975' },
      { name: 'Feta Feigen', description: 'Süße Feigen mit salzigem Feta', price: '6,90', image: 'https://images.unsplash.com/photo-1570197788417-0e82375c9371' },
      { name: 'Ziegenkäse auf Fenchel & Walnuss', description: 'Aromatische Kombination mit Nüssen', price: '6,90', image: 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d' },
      { name: 'Gebratener Spinat mit Cherrytomaten', description: 'Vegan - Frischer Spinat mit süßen Tomaten', price: '6,90', image: 'https://images.unsplash.com/photo-1567306226416-28f0efdc88ce' }
    ],
    'tapas-pollo': [
      { name: 'Hähnchen mit Limetten-Sauce', description: 'Zartes Hähnchen in frischer Zitrus-Sauce', price: '7,20', image: 'https://images.unsplash.com/photo-1598103442097-8b74394b95c6' },
      { name: 'Knuspriges Hähnchen mit Honig-Senf', description: 'Goldbraun gebratenes Hähnchen mit süß-scharfer Sauce', price: '7,20', image: 'https://images.unsplash.com/photo-1562967914-608f82629710' },
      { name: 'Hähnchenspieß mit Chili', description: 'Würziger Hähnchen-Spieß mit Chili', price: '7,20', image: 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1' },
      { name: 'Hähnchen mit Curry', description: 'Exotisch gewürztes Hähnchen', price: '7,20', image: 'https://images.unsplash.com/photo-1574484284002-952d92456975' },
      { name: 'Hähnchen mit Mandelsauce', description: 'Cremige Mandel-Sauce zu zartem Hähnchen', price: '7,20', image: 'https://images.unsplash.com/photo-1598103442097-8b74394b95c6' },
      { name: 'Hähnchen-Chorizo-Spieß', description: 'Spanische Wurst-Fleisch-Kombination', price: '7,20', image: 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1' },
      { name: 'Hähnchen mit Brandy-Sauce', description: 'Edle Brandy-Sauce zu saftigem Hähnchen', price: '7,20', image: 'https://images.unsplash.com/photo-1562967914-608f82629710' }
    ],
    'tapas-carne': [
      { name: 'Dátiles con Bacon', description: 'Süße Datteln mit knusprigem Speck', price: '6,90', image: 'https://images.unsplash.com/photo-1544025162-d76694265947' },
      { name: 'Albondigas', description: 'Spanische Hackfleischbällchen in Tomatensoße', price: '6,90', image: 'https://images.unsplash.com/photo-1574484284002-952d92456975' },
      { name: 'Pincho de Cerdo', description: 'Schweinefleisch-Spieß gegrillt', price: '7,90', image: 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1' },
      { name: 'Pincho de Cordero', description: 'Lammfleisch-Spieß mit Kräutern', price: '8,90', image: 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1' },
      { name: 'Chuletas de Cordero', description: 'Gegrillte Lammkoteletts', price: '9,90', image: 'https://images.unsplash.com/photo-1529193591184-b1d58069ecdd' },
      { name: 'Rollitos Serrano mit Feige', description: 'Serrano-Schinken-Röllchen mit süßer Feige', price: '9,90', image: 'https://images.pexels.com/photos/24706530/pexels-photo-24706530.jpeg' },
      { name: 'Ziegenkäse mit Bacon', description: 'Cremiger Ziegenkäse mit knusprigem Speck', price: '7,90', image: 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d' },
      { name: 'Chorizo al Diablo', description: 'Scharfe Chorizo in Teufelssauce', price: '7,90', image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b' },
      { name: 'Medaillons vom Schwein', description: 'Zarte Schweinefilet-Medaillons', price: '9,90', image: 'https://images.unsplash.com/photo-1529193591184-b1d58069ecdd' },
      { name: 'Champignons mit Käse', description: 'Überbackene Pilze mit geschmolzenem Käse', price: '8,90', image: 'https://images.unsplash.com/photo-1614887009518-7b9355a3a0e4' },
      { name: 'Schweinefilet mit Cherrytomaten', description: 'Saftiges Filet mit süßen Tomaten', price: '9,50', image: 'https://images.unsplash.com/photo-1529193591184-b1d58069ecdd' },
      { name: 'Schweinefilet in Sauce', description: 'Zartes Filet in aromatischer Sauce', price: '9,50', image: 'https://images.unsplash.com/photo-1529193591184-b1d58069ecdd' },
      { name: 'Chorizo a la Plancha', description: 'Gegrillte spanische Wurst', price: '7,90', image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b' },
      { name: 'Lammfilet', description: 'Premium Lammfilet rosa gebraten', price: '9,90', image: 'https://images.unsplash.com/photo-1529193591184-b1d58069ecdd' },
      { name: 'Spareribs mit BBQ', description: 'Zarte Rippchen mit BBQ-Sauce', price: '8,90', image: 'https://images.unsplash.com/photo-1529193591184-b1d58069ecdd' },
      { name: 'Chicken Wings', description: 'Würzige Hähnchenflügel', price: '9,90', image: 'https://images.unsplash.com/photo-1562967914-608f82629710' }
    ],
    'tapas-pescado': [
      { name: 'Boquerones Fritos', description: 'Frittierte Sardellen', price: '7,50', image: 'https://images.unsplash.com/photo-1565299507177-b0ac66763828' },
      { name: 'Calamares a la Plancha', description: 'Gegrillte Tintenfischringe', price: '8,90', image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b' },
      { name: 'Calamares a la Romana', description: 'Panierte Tintenfischringe', price: '7,50', image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b' },
      { name: 'Lachs mit Spinat', description: 'Frischer Lachs auf Spinatbett', price: '9,90', image: 'https://images.unsplash.com/photo-1467003909585-2f8a72700288' },
      { name: 'Gambas a la Plancha', description: 'Gegrillte Garnelen', price: '9,90', image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b' },
      { name: 'Garnelen-Dattel-Spieß', description: 'Süß-salzige Kombination am Spieß', price: '9,90', image: 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1' },
      { name: 'Gambas al Ajillo', description: 'Garnelen in Knoblauchöl', price: '9,90', image: 'https://images.unsplash.com/photo-1619860705243-dbef552e7118' },
      { name: 'Muslitos de Mar', description: 'Gebackene Muscheln', price: '6,90', image: 'https://images.unsplash.com/photo-1580370908410-85f1eafc5e5b' },
      { name: 'Gegrillter Oktopus', description: 'Zarter Oktopus vom Grill', price: '9,90', image: 'https://images.unsplash.com/photo-1531890820402-2a683fbfd30c' },
      { name: 'Jacobsmuscheln', description: 'Edle Jakobsmuscheln gegrillt', price: '9,90', image: 'https://images.unsplash.com/photo-1580370908410-85f1eafc5e5b' },
      { name: 'Gambas PIL PIL', description: 'Garnelen in würzigem Olivenöl', price: '9,90', image: 'https://images.unsplash.com/photo-1619860705619-1e0ba34091e0' },
      { name: 'Empanadas', description: 'Spanische Teigtaschen mit Füllung', price: '6,90', image: 'https://images.unsplash.com/photo-1574484284002-952d92456975' },
      { name: 'Pfahlmuscheln', description: 'Frische Miesmuscheln in Sud', price: '8,90', image: 'https://images.unsplash.com/photo-1580370908410-85f1eafc5e5b' },
      { name: 'Pulpo al Ajillo', description: 'Oktopus in Knoblauchöl', price: '9,90', image: 'https://images.unsplash.com/photo-1531890820402-2a683fbfd30c' },
      { name: 'Zanderfilet', description: 'Zartes Zanderfilet gebraten', price: '9,90', image: 'https://images.unsplash.com/photo-1467003909585-2f8a72700288' },
      { name: 'Tiger Garnelen', description: 'Große Tiger-Garnelen gegrillt', price: '9,90', image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b' },
      { name: 'Brocheta de Gambas', description: 'Garnelen-Spieß mit Gemüse', price: '8,90', image: 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1' },
      { name: 'Boqueron in Tempura', description: 'Sardellen im Tempura-Teig', price: '7,50', image: 'https://images.unsplash.com/photo-1565299507177-b0ac66763828' },
      { name: 'Chipirones', description: 'Baby-Tintenfische gegrillt', price: '8,90', image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b' }
    ],
    'kroketten': [
      { name: 'Bacalao', description: 'Stockfisch-Kroketten', price: '5,90', image: 'https://images.unsplash.com/photo-1718912334263-1518476fe9b1' },
      { name: 'Käse', description: 'Cremige Käse-Kroketten', price: '5,90', image: 'https://images.unsplash.com/photo-1718912334263-1518476fe9b1' },
      { name: 'Mandeln', description: 'Mandel-Kroketten mit feinem Aroma', price: '6,50', image: 'https://images.pexels.com/photos/30877123/pexels-photo-30877123.jpeg' },
      { name: 'Jamón', description: 'Schinken-Kroketten klassisch', price: '5,90', image: 'https://images.unsplash.com/photo-1718912334263-1518476fe9b1' },
      { name: 'Kartoffel', description: 'Traditionelle Kartoffel-Kroketten', price: '5,50', image: 'https://images.pexels.com/photos/30877123/pexels-photo-30877123.jpeg' }
    ],
    'pasta': [
      { name: 'Spaghetti Aglio e Olio', description: 'Klassisch mit Knoblauch und Olivenöl', price: '12,90', image: 'https://images.unsplash.com/photo-1621996346565-e3dbc353d2e5' },
      { name: 'Spaghetti Bolognese', description: 'Mit hausgemachter Fleischsauce', price: '14,90', image: 'https://images.unsplash.com/photo-1555949258-eb67b1ef0ceb' },
      { name: 'Pasta Brokkoli Gorgonzola', description: 'Cremige Gorgonzola-Sauce mit Brokkoli', price: '14,90', image: 'https://images.unsplash.com/photo-1621996346565-e3dbc353d2e5' },
      { name: 'Pasta Verdura', description: 'Mit frischem Saisongemüse', price: '14,90', image: 'https://images.unsplash.com/photo-1518779578993-ec3579fee39f' },
      { name: 'Pasta Garnelen', description: 'Mit frischen Garnelen und Knoblauch', price: '16,90', image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b' }
    ],
    'pizza': [
      { name: 'Margherita', description: 'Tomaten, Mozzarella, Basilikum', price: '9,90', image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b' },
      { name: 'Schinken', description: 'Mit spanischem Schinken', price: '12,90', image: 'https://images.unsplash.com/photo-1615478503562-ec2d8aa0e24e' },
      { name: 'Funghi', description: 'Mit frischen Champignons', price: '12,90', image: 'https://images.unsplash.com/photo-1614887009518-7b9355a3a0e4' },
      { name: 'Tonno', description: 'Mit Thunfisch und Zwiebeln', price: '13,90', image: 'https://images.unsplash.com/photo-1551248429-40975aa4de74' },
      { name: 'Hawaii', description: 'Mit Schinken und Ananas', price: '13,90', image: 'https://images.unsplash.com/photo-1615478503562-ec2d8aa0e24e' },
      { name: 'Verdura', description: 'Mit gegrilltem Gemüse', price: '13,90', image: 'https://images.unsplash.com/photo-1518779578993-ec3579fee39f' },
      { name: 'Salami', description: 'Mit würziger Salami', price: '12,90', image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b' },
      { name: 'Garnelen', description: 'Mit frischen Garnelen', price: '15,90', image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b' },
      { name: 'Bolognese', description: 'Mit Hackfleischsauce', price: '13,90', image: 'https://images.unsplash.com/photo-1555949258-eb67b1ef0ceb' },
      { name: "Jimmy's Special", description: 'Unsere Haus-Spezial-Pizza', price: '13,90', image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b' }
    ],
    'snacks': [
      { name: 'Pommes', description: 'Goldgelbe Kartoffel-Pommes', price: '5,50', image: 'https://images.unsplash.com/photo-1518779578993-ec3579fee39f' },
      { name: 'Chicken Nuggets', description: 'Knusprige Hähnchen-Nuggets', price: '8,90', image: 'https://images.unsplash.com/photo-1562967914-608f82629710' },
      { name: 'Chicken Wings', description: 'Würzige Hähnchenflügel', price: '9,90', image: 'https://images.unsplash.com/photo-1562967914-608f82629710' },
      { name: 'Currywurst', description: 'Deutsche Currywurst klassisch', price: '10,90', image: 'https://images.unsplash.com/photo-1529193591184-b1d58069ecdd' }
    ],
    'dessert': [
      { name: 'Crema Catalana', description: 'Katalanische Crème brûlée', price: '5,50', image: 'https://images.unsplash.com/photo-1736752346246-61f4daedfde0' },
      { name: 'Tarte de Santiago', description: 'Spanischer Mandelkuchen', price: '7,50', image: 'https://images.pexels.com/photos/32512507/pexels-photo-32512507.jpeg' },
      { name: 'Eis', description: 'Hausgemachtes Eis nach Wahl', price: '6,90', image: 'https://images.unsplash.com/photo-1563379091329-5dc8e2f8e1db' },
      { name: 'Churros mit Schokolade', description: 'Spanisches Spritzgebäck mit warmer Schokolade', price: '6,90', image: 'https://images.unsplash.com/photo-1505851498219-ee2449c18936' },
      { name: 'Schoko Soufflé', description: 'Warmes Schokoladen-Soufflé', price: '7,50', image: 'https://images.pexels.com/photos/32512507/pexels-photo-32512507.jpeg' }
    ],
    'helados': [
      { name: 'Kokos', description: 'Eis im Fruchtschälchen - Kokos', price: '6,90', image: 'https://images.unsplash.com/photo-1563379091329-5dc8e2f8e1db' },
      { name: 'Zitrone', description: 'Eis im Fruchtschälchen - Zitrone', price: '6,90', image: 'https://images.unsplash.com/photo-1563379091329-5dc8e2f8e1db' },
      { name: 'Orange', description: 'Eis im Fruchtschälchen - Orange', price: '6,90', image: 'https://images.unsplash.com/photo-1563379091329-5dc8e2f8e1db' },
      { name: 'Nuss', description: 'Eis im Fruchtschälchen - Nuss', price: '6,90', image: 'https://images.unsplash.com/photo-1563379091329-5dc8e2f8e1db' }
    ]
  };

  const categories = [
    { id: 'alle', name: 'Alle Kategorien', icon: '🍽️' },
    { id: 'inicio', name: 'Inicio', icon: '🫒' },
    { id: 'salat', name: 'Salat', icon: '🥗' },
    { id: 'kleiner-salat', name: 'Kleiner Salat', icon: '🌿' },
    { id: 'tapa-paella', name: 'Tapa Paella', icon: '🍚' },
    { id: 'tapas-vegetarian', name: 'Tapas Vegetarian', icon: '🥬' },
    { id: 'tapas-pollo', name: 'Tapas de Pollo', icon: '🍗' },
    { id: 'tapas-carne', name: 'Tapas de Carne', icon: '🥩' },
    { id: 'tapas-pescado', name: 'Tapas de Pescado', icon: '🐟' },
    { id: 'kroketten', name: 'Kroketten', icon: '🧆' },
    { id: 'pasta', name: 'Pasta', icon: '🍝' },
    { id: 'pizza', name: 'Pizza', icon: '🍕' },
    { id: 'snacks', name: 'Snacks', icon: '🍟' },
    { id: 'dessert', name: 'Dessert', icon: '🍮' },
    { id: 'helados', name: 'Helados', icon: '🍨' }
  ];

  const getDisplayItems = () => {
    if (selectedCategory === 'alle') {
      return Object.entries(menuItems).flatMap(([category, items]) => 
        items.map(item => ({ ...item, category }))
      );
    }
    return menuItems[selectedCategory]?.map(item => ({ ...item, category: selectedCategory })) || [];
  };

  return (
    <div className="min-h-screen mediterranean-texture pt-24">
      <div className="container mx-auto px-4 py-12">
        <h1 className="text-6xl font-serif text-center text-warm-beige mb-4 tracking-wide drop-shadow-text">
          Speisekarte
        </h1>
        <p className="text-center text-light-beige mb-12 text-lg font-light">
          Authentische spanische Küche • Alle Gerichte mit Bildern
        </p>
        
        {/* Category Filter */}
        <div className="flex flex-wrap justify-center gap-3 mb-12">
          {categories.map(category => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`menu-category px-4 py-3 rounded-lg transition-all duration-300 font-light tracking-wide text-sm ${
                selectedCategory === category.id
                  ? 'bg-warm-beige text-dark-brown'
                  : 'border border-warm-beige text-warm-beige hover:bg-warm-beige hover:text-dark-brown'
              }`}
            >
              <span className="mr-2">{category.icon}</span>
              {category.name}
            </button>
          ))}
        </div>

        {/* Menu Items - Two-column layout with enhanced hover images */}
        <div className="grid md:grid-cols-2 gap-6 max-w-7xl mx-auto">
          {getDisplayItems().map((item, index) => (
            <div key={index} className="menu-item bg-dark-brown rounded-lg border border-warm-brown p-6 hover:bg-medium-brown transition-all duration-300 relative group">
              <div className="flex justify-between items-center">
                {/* Dish name and description */}
                <div className="flex-1">
                  <h3 className="dish-name text-xl font-serif text-warm-beige mb-2 tracking-wide cursor-pointer">
                    {item.name}
                  </h3>
                  <p className="text-light-beige mb-2 font-light leading-relaxed text-sm">{item.description}</p>
                  <span className="text-xs text-warm-beige capitalize font-light tracking-wide opacity-75">
                    {categories.find(c => c.id === item.category)?.name}
                  </span>
                </div>
                
                {/* Price */}
                <div className="price text-2xl font-serif text-warm-beige tracking-wide flex-shrink-0 ml-4">
                  {item.price} €
                </div>
              </div>
              
              {/* Enhanced Hover Image - Large, centered, more prominent */}
              <div className="tooltip-image absolute left-1/2 top-full mt-4 transform -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-all duration-300 pointer-events-none z-50 hidden md:block">
                <div className="bg-warm-beige p-2 rounded-lg shadow-2xl">
                  <img 
                    src={item.image} 
                    alt={item.name}
                    className="w-[280px] h-[280px] object-cover rounded-lg"
                    loading="lazy"
                  />
                  <div className="text-center mt-2 text-dark-brown font-serif text-sm font-medium">
                    {item.name}
                  </div>
                </div>
              </div>
              
              {/* Mobile: Show image on tap/touch */}
              <div className="md:hidden mt-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <img 
                  src={item.image} 
                  alt={item.name}
                  className="w-full h-40 object-cover rounded-lg border border-warm-brown"
                  loading="lazy"
                />
              </div>
            </div>
          ))}
        </div>
        
        {/* Menu Footer */}
        <div className="text-center mt-16 p-8 bg-dark-brown rounded-lg border border-warm-brown">
          <h3 className="text-2xl font-serif text-warm-beige mb-4">Allergien und Unverträglichkeiten</h3>
          <p className="text-light-beige font-light leading-relaxed max-w-3xl mx-auto">
            Bitte informieren Sie uns über eventuelle Allergien oder Unverträglichkeiten. 
            Unsere Küche berücksichtigt gerne Ihre individuellen Bedürfnisse. 
            Vegan = 🌱 • Vegetarisch = 🥬 • Glutenfrei auf Anfrage möglich
          </p>
        </div>
      </div>
    </div>
  );
};

// Locations Page Component
const Standorte = () => {
  return (
    <div className="min-h-screen bg-warm-brown pt-24">
      <div className="container mx-auto px-4 py-12">
        <h1 className="text-5xl font-serif text-center text-warm-beige mb-16 tracking-wide">
          Unsere Standorte
        </h1>
        
        <div className="grid lg:grid-cols-2 gap-12">
          {/* Neustadt Location */}
          <div className="bg-dark-brown rounded-lg border border-warm-brown overflow-hidden">
            <img 
              src="https://images.unsplash.com/photo-1665758564776-f2aa6b41327e" 
              alt="Restaurant Neustadt" 
              className="w-full h-64 object-cover"
            />
            <div className="p-8">
              <h2 className="text-3xl font-serif text-warm-beige mb-6 tracking-wide">
                Jimmy's Tapas Bar Neustadt
              </h2>
              <div className="space-y-4 text-light-beige">
                <div className="flex items-center">
                  <span className="text-xl mr-4">📍</span>
                  <div>
                    <p className="font-light text-lg">Am Strande 21</p>
                    <p className="font-light">23730 Neustadt in Holstein</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <span className="text-xl mr-4">🕒</span>
                  <div>
                    <p className="font-light text-lg">Öffnungszeiten:</p>
                    <p className="font-light">Täglich 12:00–22:00 Uhr (Sommersaison)</p>
                    <p className="text-sm text-warm-beige font-light">Winterbetrieb unregelmäßig</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <span className="text-xl mr-4">📞</span>
                  <p className="font-light">Telefon: +49 (0) 4561 123456</p>
                </div>
              </div>
              <div className="mt-8 h-64 bg-medium-brown rounded-lg flex items-center justify-center border border-warm-brown">
                <div className="text-center">
                  <p className="text-light-beige font-light">Google Maps Karte - Neustadt</p>
                  <p className="text-sm text-warm-beige font-light mt-2">(Integration folgt)</p>
                </div>
              </div>
            </div>
          </div>

          {/* Großenbrode Location */}
          <div className="bg-dark-brown rounded-lg border border-warm-brown overflow-hidden">
            <img 
              src="https://images.unsplash.com/photo-1665758564796-5162ff406254" 
              alt="Restaurant Großenbrode" 
              className="w-full h-64 object-cover"
            />
            <div className="p-8">
              <h2 className="text-3xl font-serif text-warm-beige mb-6 tracking-wide">
                Jimmy's Tapas Bar Großenbrode
              </h2>
              <div className="space-y-4 text-light-beige">
                <div className="flex items-center">
                  <span className="text-xl mr-4">📍</span>
                  <div>
                    <p className="font-light text-lg">Südstrand 54</p>
                    <p className="font-light">23755 Großenbrode</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <span className="text-xl mr-4">🕒</span>
                  <div>
                    <p className="font-light text-lg">Öffnungszeiten:</p>
                    <p className="font-light">Täglich 12:00–22:00 Uhr (Sommersaison)</p>
                    <p className="text-sm text-warm-beige font-light">Winterbetrieb unregelmäßig</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <span className="text-xl mr-4">📞</span>
                  <p className="font-light">Telefon: +49 (0) 4561 789012</p>
                </div>
              </div>
              <div className="mt-8 h-64 bg-medium-brown rounded-lg flex items-center justify-center border border-warm-brown">
                <div className="text-center">
                  <p className="text-light-beige font-light">Google Maps Karte - Großenbrode</p>
                  <p className="text-sm text-warm-beige font-light mt-2">(Integration folgt)</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Reviews Page Component
const Bewertungen = () => {
  const [feedback, setFeedback] = useState({
    name: '',
    email: '',
    rating: 5,
    comment: ''
  });

  const reviews = [
    {
      name: "Maria Schmidt",
      rating: 5,
      comment: "Absolut authentische spanische Küche! Die Paella war fantastisch und der Service sehr herzlich.",
      date: "März 2024"
    },
    {
      name: "Thomas Müller",
      rating: 5,
      comment: "Die beste Tapas-Bar an der Ostsee! Wir kommen immer wieder gerne nach Neustadt.",
      date: "Februar 2024"
    },
    {
      name: "Anna Petersen",
      rating: 4,
      comment: "Tolle Atmosphäre und leckeres Essen. Besonders die Gambas al Ajillo sind zu empfehlen!",
      date: "Januar 2024"
    }
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    alert('Vielen Dank für Ihr Feedback! Es wurde intern gespeichert.');
    setFeedback({ name: '', email: '', rating: 5, comment: '' });
  };

  const renderStars = (rating) => {
    return Array.from({ length: 5 }, (_, i) => (
      <span key={i} className={`text-2xl ${i < rating ? 'text-yellow-400' : 'text-warm-brown'}`}>
        ★
      </span>
    ));
  };

  return (
    <div className="min-h-screen bg-warm-brown pt-24">
      <div className="container mx-auto px-4 py-12">
        <h1 className="text-5xl font-serif text-center text-warm-beige mb-16 tracking-wide">
          Bewertungen & Feedback
        </h1>
        
        <div className="grid lg:grid-cols-2 gap-12 max-w-7xl mx-auto">
          {/* Public Reviews */}
          <div>
            <h2 className="text-3xl font-serif text-warm-beige mb-8 tracking-wide">
              Kundenbewertungen
            </h2>
            <div className="space-y-8">
              {reviews.map((review, index) => (
                <div key={index} className="bg-dark-brown rounded-lg border border-warm-brown p-8">
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="font-light text-warm-beige text-lg tracking-wide">{review.name}</h3>
                    <span className="text-sm text-light-beige font-light">{review.date}</span>
                  </div>
                  <div className="flex mb-4">
                    {renderStars(review.rating)}
                  </div>
                  <p className="text-light-beige font-light leading-relaxed">{review.comment}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Feedback Form */}
          <div>
            <h2 className="text-3xl font-serif text-warm-beige mb-8 tracking-wide">
              Ihr Feedback
            </h2>
            <div className="bg-dark-brown rounded-lg border border-warm-brown p-8">
              <p className="text-light-beige mb-6 text-sm font-light">
                Dieses Feedback wird intern gespeichert und nicht öffentlich angezeigt.
              </p>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="block text-warm-beige font-light mb-3 tracking-wide">Name</label>
                  <input
                    type="text"
                    value={feedback.name}
                    onChange={(e) => setFeedback({...feedback, name: e.target.value})}
                    className="w-full p-4 bg-medium-brown border border-warm-brown rounded-lg focus:ring-2 focus:ring-warm-beige focus:border-warm-beige text-warm-beige font-light"
                    required
                  />
                </div>
                <div>
                  <label className="block text-warm-beige font-light mb-3 tracking-wide">E-Mail</label>
                  <input
                    type="email"
                    value={feedback.email}
                    onChange={(e) => setFeedback({...feedback, email: e.target.value})}
                    className="w-full p-4 bg-medium-brown border border-warm-brown rounded-lg focus:ring-2 focus:ring-warm-beige focus:border-warm-beige text-warm-beige font-light"
                    required
                  />
                </div>
                <div>
                  <label className="block text-warm-beige font-light mb-3 tracking-wide">Bewertung</label>
                  <div className="flex space-x-2">
                    {[1,2,3,4,5].map(star => (
                      <button
                        key={star}
                        type="button"
                        onClick={() => setFeedback({...feedback, rating: star})}
                        className={`text-3xl ${star <= feedback.rating ? 'text-yellow-400' : 'text-warm-brown'} hover:text-yellow-400 transition-colors`}
                      >
                        ★
                      </button>
                    ))}
                  </div>
                </div>
                <div>
                  <label className="block text-warm-beige font-light mb-3 tracking-wide">Kommentar</label>
                  <textarea
                    value={feedback.comment}
                    onChange={(e) => setFeedback({...feedback, comment: e.target.value})}
                    className="w-full p-4 bg-medium-brown border border-warm-brown rounded-lg focus:ring-2 focus:ring-warm-beige focus:border-warm-beige h-32 text-warm-beige font-light"
                    required
                  />
                </div>
                <button
                  type="submit"
                  className="w-full bg-warm-beige hover:bg-light-beige text-dark-brown py-4 rounded-lg font-light transition-colors tracking-wide"
                >
                  Feedback senden
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// About Us Page Component
const UeberUns = () => {
  return (
    <div className="min-h-screen bg-warm-brown pt-24">
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-5xl font-serif text-center text-warm-beige mb-16 tracking-wide">
            Über uns
          </h1>
          
          <div className="bg-dark-brown rounded-lg border border-warm-brown p-10 mb-12">
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div>
                <img 
                  src="https://images.unsplash.com/photo-1665758564802-f611df512d8d" 
                  alt="Jimmy" 
                  className="w-full rounded-lg"
                />
              </div>
              <div>
                <h2 className="text-4xl font-serif text-warm-beige mb-6 tracking-wide">
                  Jimmy Rodríguez
                </h2>
                <p className="text-light-beige mb-6 leading-relaxed font-light text-lg">
                  Seit über 15 Jahren bringe ich die authentischen Aromen Spaniens an die deutsche Ostseeküste. 
                  Meine Leidenschaft für die spanische Küche begann in den kleinen Tapas-Bars von Sevilla, 
                  wo ich die Geheimnisse traditioneller Rezepte erlernte.
                </p>
                <p className="text-light-beige mb-6 leading-relaxed font-light text-lg">
                  In Jimmy's Tapas Bar verwenden wir nur die besten Zutaten - von handverlesenem Olivenöl 
                  aus Andalusien bis hin zu frischen Meeresfrüchten aus der Ostsee. Jedes Gericht wird mit 
                  Liebe und Respekt vor der spanischen Tradition zubereitet.
                </p>
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-dark-brown rounded-lg border border-warm-brown p-8 text-center">
              <div className="text-5xl mb-6">🍷</div>
              <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">Qualität</h3>
              <p className="text-light-beige font-light leading-relaxed">
                Nur die besten Zutaten für authentische spanische Geschmackserlebnisse
              </p>
            </div>
            <div className="bg-dark-brown rounded-lg border border-warm-brown p-8 text-center">
              <div className="text-5xl mb-6">❤️</div>
              <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">Gastfreundschaft</h3>
              <p className="text-light-beige font-light leading-relaxed">
                Herzliche Atmosphäre und persönlicher Service für jeden Gast
              </p>
            </div>
            <div className="bg-dark-brown rounded-lg border border-warm-brown p-8 text-center">
              <div className="text-5xl mb-6">🎉</div>
              <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">Lebensfreude</h3>
              <p className="text-light-beige font-light leading-relaxed">
                Spanische Lebensart und Genuss in gemütlicher Atmosphäre
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Contact Page Component
const Kontakt = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: '',
    location: 'neustadt'
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    alert('Vielen Dank für Ihre Nachricht! Wir melden uns bald bei Ihnen.');
    setFormData({ name: '', email: '', phone: '', message: '', location: 'neustadt' });
  };

  return (
    <div className="min-h-screen bg-warm-brown pt-24">
      <div className="container mx-auto px-4 py-12">
        <h1 className="text-5xl font-serif text-center text-warm-beige mb-16 tracking-wide">
          Kontakt
        </h1>
        
        <div className="grid lg:grid-cols-2 gap-12 max-w-7xl mx-auto">
          {/* Contact Information */}
          <div>
            <h2 className="text-3xl font-serif text-warm-beige mb-8 tracking-wide">
              Kontaktinformationen
            </h2>
            
            <div className="bg-dark-brown rounded-lg border border-warm-brown p-8 mb-8">
              <h3 className="text-2xl font-serif text-warm-beige mb-6 tracking-wide">Neustadt in Holstein</h3>
              <div className="space-y-3 text-light-beige">
                <p className="font-light">📍 Am Strande 21, 23730 Neustadt in Holstein</p>
                <p className="font-light">📞 +49 (0) 4561 123456</p>
                <p className="font-light">✉️ neustadt@jimmys-tapasbar.de</p>
              </div>
            </div>

            <div className="bg-dark-brown rounded-lg border border-warm-brown p-8 mb-8">
              <h3 className="text-2xl font-serif text-warm-beige mb-6 tracking-wide">Großenbrode</h3>
              <div className="space-y-3 text-light-beige">
                <p className="font-light">📍 Südstrand 54, 23755 Großenbrode</p>
                <p className="font-light">📞 +49 (0) 4561 789012</p>
                <p className="font-light">✉️ grossenbrode@jimmys-tapasbar.de</p>
              </div>
            </div>

            <div className="bg-dark-brown rounded-lg border border-warm-brown p-8">
              <h3 className="text-2xl font-serif text-warm-beige mb-6 tracking-wide">Allgemein</h3>
              <div className="space-y-3 text-light-beige">
                <p className="font-light">🌐 www.jimmys-tapasbar.de</p>
                <p className="font-light">✉️ info@jimmys-tapasbar.de</p>
                <p className="font-light">🕒 Täglich 12:00–22:00 Uhr (Sommersaison)</p>
              </div>
            </div>
          </div>

          {/* Contact Form */}
          <div>
            <h2 className="text-3xl font-serif text-warm-beige mb-8 tracking-wide">
              Nachricht senden
            </h2>
            <div className="bg-dark-brown rounded-lg border border-warm-brown p-8">
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="block text-warm-beige font-light mb-3 tracking-wide">Name *</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    className="w-full p-4 bg-medium-brown border border-warm-brown rounded-lg focus:ring-2 focus:ring-warm-beige focus:border-warm-beige text-warm-beige font-light"
                    required
                  />
                </div>
                <div>
                  <label className="block text-warm-beige font-light mb-3 tracking-wide">E-Mail *</label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    className="w-full p-4 bg-medium-brown border border-warm-brown rounded-lg focus:ring-2 focus:ring-warm-beige focus:border-warm-beige text-warm-beige font-light"
                    required
                  />
                </div>
                <div>
                  <label className="block text-warm-beige font-light mb-3 tracking-wide">Telefon</label>
                  <input
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => setFormData({...formData, phone: e.target.value})}
                    className="w-full p-4 bg-medium-brown border border-warm-brown rounded-lg focus:ring-2 focus:ring-warm-beige focus:border-warm-beige text-warm-beige font-light"
                  />
                </div>
                <div>
                  <label className="block text-warm-beige font-light mb-3 tracking-wide">Standort</label>
                  <select
                    value={formData.location}
                    onChange={(e) => setFormData({...formData, location: e.target.value})}
                    className="w-full p-4 bg-medium-brown border border-warm-brown rounded-lg focus:ring-2 focus:ring-warm-beige focus:border-warm-beige text-warm-beige font-light"
                  >
                    <option value="neustadt">Neustadt in Holstein</option>
                    <option value="grossenbrode">Großenbrode</option>
                    <option value="beide">Beide Standorte</option>
                  </select>
                </div>
                <div>
                  <label className="block text-warm-beige font-light mb-3 tracking-wide">Nachricht *</label>
                  <textarea
                    value={formData.message}
                    onChange={(e) => setFormData({...formData, message: e.target.value})}
                    className="w-full p-4 bg-medium-brown border border-warm-brown rounded-lg focus:ring-2 focus:ring-warm-beige focus:border-warm-beige h-32 text-warm-beige font-light"
                    required
                  />
                </div>
                <button
                  type="submit"
                  className="w-full bg-warm-beige hover:bg-light-beige text-dark-brown py-4 rounded-lg font-light transition-colors tracking-wide"
                >
                  Nachricht senden
                </button>
              </form>
              
              <div className="mt-8 pt-8 border-t border-warm-brown">
                <h4 className="font-light text-warm-beige mb-3 tracking-wide">Datenschutz</h4>
                <p className="text-sm text-light-beige font-light leading-relaxed">
                  Ihre Daten werden vertraulich behandelt und gemäß DSGVO verarbeitet. 
                  Weitere Informationen finden Sie in unserem Impressum.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Impressum Page Component
const Impressum = () => {
  return (
    <div className="min-h-screen bg-warm-brown pt-24">
      <div className="container mx-auto px-4 py-12">
        <h1 className="text-5xl font-serif text-center text-warm-beige mb-16 tracking-wide">
          Impressum
        </h1>
        
        <div className="max-w-4xl mx-auto bg-dark-brown rounded-lg border border-warm-brown p-8">
          <div className="space-y-8 text-light-beige">
            <div>
              <h2 className="text-2xl font-serif text-warm-beige mb-4">Angaben gemäß § 5 TMG</h2>
              <div className="space-y-2 font-light">
                <p><strong>Jimmy's Tapas Bar</strong></p>
                <p>Inhaber: Jimmy Rodríguez</p>
                <p>Am Strande 21</p>
                <p>23730 Neustadt in Holstein</p>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-serif text-warm-beige mb-3">Kontakt</h3>
              <div className="space-y-2 font-light">
                <p>Telefon: +49 (0) 4561 123456</p>
                <p>E-Mail: info@jimmys-tapasbar.de</p>
                <p>Website: www.jimmys-tapasbar.de</p>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-serif text-warm-beige mb-3">Zweiter Standort</h3>
              <div className="space-y-2 font-light">
                <p>Jimmy's Tapas Bar Großenbrode</p>
                <p>Südstrand 54</p>
                <p>23755 Großenbrode</p>
                <p>Telefon: +49 (0) 4561 789012</p>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-serif text-warm-beige mb-3">Umsatzsteuer-ID</h3>
              <p className="font-light">Umsatzsteuer-Identifikationsnummer gemäß §27 a Umsatzsteuergesetz:<br />
              DE123456789 (Beispiel - bitte echte USt-IdNr. eintragen)</p>
            </div>

            <div>
              <h3 className="text-xl font-serif text-warm-beige mb-3">Verantwortlich für den Inhalt nach § 55 Abs. 2 RStV</h3>
              <div className="space-y-2 font-light">
                <p>Jimmy Rodríguez</p>
                <p>Am Strande 21</p>
                <p>23730 Neustadt in Holstein</p>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-serif text-warm-beige mb-3">Haftungsausschluss</h3>
              <div className="space-y-4 font-light">
                <div>
                  <h4 className="font-medium text-warm-beige mb-2">Haftung für Inhalte</h4>
                  <p>Als Diensteanbieter sind wir gemäß § 7 Abs.1 TMG für eigene Inhalte auf diesen Seiten nach den allgemeinen Gesetzen verantwortlich. Nach §§ 8 bis 10 TMG sind wir als Diensteanbieter jedoch nicht unter der Verpflichtung, übermittelte oder gespeicherte fremde Informationen zu überwachen oder nach Umständen zu forschen, die auf eine rechtswidrige Tätigkeit hinweisen.</p>
                </div>
                
                <div>
                  <h4 className="font-medium text-warm-beige mb-2">Haftung für Links</h4>
                  <p>Unser Angebot enthält Links zu externen Websites Dritter, auf deren Inhalte wir keinen Einfluss haben. Deshalb können wir für diese fremden Inhalte auch keine Gewähr übernehmen. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber der Seiten verantwortlich.</p>
                </div>
                
                <div>
                  <h4 className="font-medium text-warm-beige mb-2">Urheberrecht</h4>
                  <p>Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen dem deutschen Urheberrecht. Die Vervielfältigung, Bearbeitung, Verbreitung und jede Art der Verwertung außerhalb der Grenzen des Urheberrechtes bedürfen der schriftlichen Zustimmung des jeweiligen Autors bzw. Erstellers.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Datenschutz Page Component
const Datenschutz = () => {
  return (
    <div className="min-h-screen bg-warm-brown pt-24">
      <div className="container mx-auto px-4 py-12">
        <h1 className="text-5xl font-serif text-center text-warm-beige mb-16 tracking-wide">
          Datenschutzerklärung
        </h1>
        
        <div className="max-w-4xl mx-auto bg-dark-brown rounded-lg border border-warm-brown p-8">
          <div className="space-y-8 text-light-beige">
            <div>
              <h2 className="text-2xl font-serif text-warm-beige mb-4">1. Datenschutz auf einen Blick</h2>
              <div className="space-y-4 font-light">
                <div>
                  <h3 className="text-lg font-serif text-warm-beige mb-2">Allgemeine Hinweise</h3>
                  <p>Die folgenden Hinweise geben einen einfachen Überblick darüber, was mit Ihren personenbezogenen Daten passiert, wenn Sie diese Website besuchen. Personenbezogene Daten sind alle Daten, mit denen Sie persönlich identifiziert werden können.</p>
                </div>
                
                <div>
                  <h3 className="text-lg font-serif text-warm-beige mb-2">Datenerfassung auf dieser Website</h3>
                  <p><strong>Wer ist verantwortlich für die Datenerfassung auf dieser Website?</strong></p>
                  <p>Die Datenverarbeitung auf dieser Website erfolgt durch den Websitebetreiber. Dessen Kontaktdaten können Sie dem Impressum dieser Website entnehmen.</p>
                </div>
              </div>
            </div>

            <div>
              <h2 className="text-2xl font-serif text-warm-beige mb-4">2. Hosting und Content Delivery Networks (CDN)</h2>
              <div className="space-y-4 font-light">
                <p>Wir hosten die Inhalte unserer Website bei folgenden Anbietern:</p>
                <p>Diese Website wird extern gehostet. Die personenbezogenen Daten, die auf dieser Website erfasst werden, werden auf den Servern des Hosters gespeichert.</p>
              </div>
            </div>

            <div>
              <h2 className="text-2xl font-serif text-warm-beige mb-4">3. Allgemeine Hinweise und Pflichtinformationen</h2>
              <div className="space-y-4 font-light">
                <div>
                  <h3 className="text-lg font-serif text-warm-beige mb-2">Datenschutz</h3>
                  <p>Die Betreiber dieser Seiten nehmen den Schutz Ihrer persönlichen Daten sehr ernst. Wir behandeln Ihre personenbezogenen Daten vertraulich und entsprechend der gesetzlichen Datenschutzvorschriften sowie dieser Datenschutzerklärung.</p>
                </div>
                
                <div>
                  <h3 className="text-lg font-serif text-warm-beige mb-2">Hinweis zur verantwortlichen Stelle</h3>
                  <p>Die verantwortliche Stelle für die Datenverarbeitung auf dieser Website ist:</p>
                  <div className="ml-4 mt-2">
                    <p>Jimmy Rodríguez</p>
                    <p>Am Strande 21</p>
                    <p>23730 Neustadt in Holstein</p>
                    <p>Telefon: +49 (0) 4561 123456</p>
                    <p>E-Mail: info@jimmys-tapasbar.de</p>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <h2 className="text-2xl font-serif text-warm-beige mb-4">4. Datenerfassung auf dieser Website</h2>
              <div className="space-y-4 font-light">
                <div>
                  <h3 className="text-lg font-serif text-warm-beige mb-2">Cookies</h3>
                  <p>Unsere Internetseiten verwenden so genannte „Cookies". Cookies sind kleine Textdateien und richten auf Ihrem Endgerät keinen Schaden an. Sie werden entweder vorübergehend für die Dauer einer Sitzung (Session-Cookies) oder dauerhaft (dauerhafte Cookies) auf Ihrem Endgerät gespeichert.</p>
                </div>
                
                <div>
                  <h3 className="text-lg font-serif text-warm-beige mb-2">Kontaktformular</h3>
                  <p>Wenn Sie uns per Kontaktformular Anfragen zukommen lassen, werden Ihre Angaben aus dem Anfrageformular inklusive der von Ihnen dort angegebenen Kontaktdaten zwecks Bearbeitung der Anfrage und für den Fall von Anschlussfragen bei uns gespeichert.</p>
                </div>
              </div>
            </div>

            <div>
              <h2 className="text-2xl font-serif text-warm-beige mb-4">5. Ihre Rechte</h2>
              <div className="space-y-4 font-light">
                <p>Sie haben jederzeit das Recht unentgeltlich Auskunft über Herkunft, Empfänger und Zweck Ihrer gespeicherten personenbezogenen Daten zu erhalten. Sie haben außerdem ein Recht, die Berichtigung, Sperrung oder Löschung dieser Daten zu verlangen.</p>
                
                <p>Hierzu sowie zu weiteren Fragen zum Thema Datenschutz können Sie sich jederzeit unter der im Impressum angegebenen Adresse an uns wenden.</p>
                
                <p>Des Weiteren steht Ihnen ein Beschwerderecht bei der zuständigen Aufsichtsbehörde zu.</p>
              </div>
            </div>

            <div className="border-t border-warm-brown pt-6 mt-8">
              <p className="text-sm text-light-beige font-light">
                Stand dieser Datenschutzerklärung: März 2024<br />
                Quelle: Erstellt mit dem Datenschutz-Generator von eRecht24
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
// Footer Component
const Footer = () => {
  return (
    <footer className="bg-dark-brown-solid text-light-beige py-12 border-t border-warm-brown">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-xl font-serif mb-4 tracking-wide text-warm-beige">Jimmy's Tapas Bar</h3>
            <p className="text-light-beige font-light">
              Spanische Genusskultur – Authentisch & Gemütlich
            </p>
          </div>
          <div>
            <h4 className="font-serif mb-4 tracking-wide text-warm-beige">Standorte</h4>
            <div className="space-y-2 text-light-beige font-light">
              <p>Neustadt in Holstein</p>
              <p>Großenbrode</p>
            </div>
          </div>
          <div>
            <h4 className="font-serif mb-4 tracking-wide text-warm-beige">Kontakt</h4>
            <div className="space-y-2 text-light-beige font-light">
              <p>info@jimmys-tapasbar.de</p>
              <p>www.jimmys-tapasbar.de</p>
            </div>
          </div>
          <div>
            <h4 className="font-serif mb-4 tracking-wide text-warm-beige">Rechtliches</h4>
            <div className="space-y-2 text-light-beige font-light">
              <Link to="/impressum" className="block hover:text-warm-beige transition-colors">Impressum</Link>
              <Link to="/datenschutz" className="block hover:text-warm-beige transition-colors">Datenschutz</Link>
            </div>
          </div>
        </div>
        <div className="border-t border-warm-brown mt-8 pt-6 text-center text-light-beige font-light">
          <p>&copy; 2024 Jimmy's Tapas Bar. Alle Rechte vorbehalten.</p>
        </div>
      </div>
    </footer>
  );
};

// Main App Component
function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/speisekarte" element={<Speisekarte />} />
          <Route path="/standorte" element={<Standorte />} />
          <Route path="/ueber-uns" element={<UeberUns />} />
          <Route path="/bewertungen" element={<Bewertungen />} />
          <Route path="/kontakt" element={<Kontakt />} />
          <Route path="/impressum" element={<Impressum />} />
          <Route path="/datenschutz" element={<Datenschutz />} />
        </Routes>
        <Footer />
        <CookieBanner />
      </BrowserRouter>
    </div>
  );
}

export default App;