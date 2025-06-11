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

// Home Page Component - Professional high-end design
const Home = () => {
  const navigate = useNavigate();
  
  return (
    <div className="min-h-screen">
      {/* Clean Professional Hero Section */}
      <section className="relative h-screen bg-cover bg-center hero-background" 
               style={{backgroundImage: `url('https://images.pexels.com/photos/26626726/pexels-photo-26626726.jpeg')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-40"></div>
        <div className="relative z-10 flex items-center justify-center h-full text-center px-4">
          <div className="max-w-4xl">
            {/* Clean Main Headline */}
            <h1 className="hero-headline font-serif text-warm-beige mb-8 tracking-wide leading-tight drop-shadow-text">
              SPANISCHE<br />
              GENUSSKULTUR<br />
              <span className="text-4xl md:text-5xl font-light opacity-90">an der Ostsee</span>
            </h1>
            
            {/* Simple Subtitle */}
            <p className="text-xl md:text-2xl text-warm-beige font-light mb-12 max-w-3xl mx-auto leading-relaxed opacity-95">
              Authentische Tapas & frische Paella<br/>
              <span className="text-lg opacity-80">direkt in Grömitz und Neustadt</span>
            </p>
            
            {/* Clean CTA Buttons */}
            <div className="flex flex-col md:flex-row justify-center gap-6">
              <button 
                onClick={() => navigate('/speisekarte')}
                className="bg-warm-beige text-dark-brown hover:bg-light-beige px-10 py-4 rounded-lg text-lg font-medium transition-all duration-300 tracking-wide shadow-lg hover:shadow-xl"
              >
                Speisekarte ansehen
              </button>
              <button 
                onClick={() => navigate('/standorte')}
                className="border-2 border-warm-beige text-warm-beige hover:bg-warm-beige hover:text-dark-brown px-10 py-4 rounded-lg text-lg font-medium transition-all duration-300 tracking-wide shadow-lg hover:shadow-xl"
              >
                Standorte entdecken
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Professional Features Section - Clean Design like "Unsere Spezialitäten" */}
      <section className="py-24 bg-gradient-to-b from-warm-brown to-dark-brown">
        <div className="container mx-auto px-4">
          <div className="text-center mb-20">
            <h2 className="text-5xl font-serif text-warm-beige mb-8 tracking-wide">
              Spanische Tradition
            </h2>
            <p className="text-xl text-light-beige font-light leading-relaxed max-w-3xl mx-auto">
              Erleben Sie authentische spanische Gastfreundschaft an der deutschen Ostseeküste
            </p>
          </div>
          
          {/* Clean Three Cards - Professional Layout */}
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <div className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-all duration-300 border border-warm-brown shadow-lg">
              <div className="p-8 text-center">
                <div className="w-16 h-16 bg-warm-beige rounded-full flex items-center justify-center mx-auto mb-6">
                  <span className="text-2xl">🍷</span>
                </div>
                <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">Authentische Tapas</h3>
                <p className="text-light-beige font-light leading-relaxed">
                  Traditionelle spanische Gerichte, mit Liebe zubereitet und perfekt zum Teilen
                </p>
              </div>
            </div>
            
            <div className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-all duration-300 border border-warm-brown shadow-lg">
              <div className="p-8 text-center">
                <div className="w-16 h-16 bg-warm-beige rounded-full flex items-center justify-center mx-auto mb-6">
                  <span className="text-2xl">🥘</span>
                </div>
                <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">Frische Paella</h3>
                <p className="text-light-beige font-light leading-relaxed">
                  Täglich hausgemacht mit Meeresfrüchten, Gemüse oder Huhn
                </p>
              </div>
            </div>
            
            <div className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-all duration-300 border border-warm-brown shadow-lg">
              <div className="p-8 text-center">
                <div className="w-16 h-16 bg-warm-beige rounded-full flex items-center justify-center mx-auto mb-6">
                  <span className="text-2xl">🏖️</span>
                </div>
                <h3 className="text-2xl font-serif text-warm-beige mb-4 tracking-wide">Zwei Standorte</h3>
                <p className="text-light-beige font-light leading-relaxed">
                  In Grömitz und Neustadt an der Küste – immer in Strandnähe
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Clean Food Gallery - Professional */}
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
              <img src="https://images.pexels.com/photos/7085661/pexels-photo-7085661.jpeg" alt="Paella" className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="font-serif text-warm-beige text-lg tracking-wide">Paella Valenciana</h3>
                <p className="text-light-beige text-sm font-light">Traditionelle spanische Paella</p>
              </div>
            </div>
            <div className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-warm-brown">
              <img src="https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg" alt="Tapas" className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="font-serif text-warm-beige text-lg tracking-wide">Tapas Variación</h3>
                <p className="text-light-beige text-sm font-light">Auswahl spanischer Köstlichkeiten</p>
              </div>
            </div>
            <div className="bg-dark-brown rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 border border-warm-brown">
              <img src="https://images.unsplash.com/photo-1619860705243-dbef552e7118" alt="Gambas al Ajillo" className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="font-serif text-warm-beige text-lg tracking-wide">Gambas al Ajillo</h3>
                <p className="text-light-beige text-sm font-light">Garnelen in Knoblauchöl</p>
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
  
  // Complete menu data with authentic images for hover display (Screenshot Style)
  const menuItems = {
    'inicio': [
      { name: 'Aioli', description: 'Hausgemachte Knoblauch-Mayonnaise', price: '3,50', image: 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f', details: 'Hausgemachte, cremige Knoblauch-Mayonnaise mit nativem Olivenöl und Zitronensaft. Serviert mit ofentrischem, spanischem Weißbrot. Perfekt zum Einstieg in einen mediterranen Abend.' },
      { name: 'Oliven', description: 'Marinierte spanische Oliven', price: '3,90', image: 'https://images.unsplash.com/photo-1714583357992-98f0ad946902', details: 'Ausgewählte schwarze und grüne Oliven aus Andalusien, mariniert mit Kräutern, Knoblauch und bestem Olivenöl.' },
      { name: 'Extra Brot', description: 'Frisches spanisches Brot', price: '1,90', image: 'https://images.unsplash.com/photo-1549931319-a545dcf3bc73', details: 'Warmes, knuspriges Brot nach traditionellem spanischem Rezept, perfekt für Tapas und Dips.' },
      { name: 'Hummus', description: 'Cremiger Kichererbsen-Dip', price: '3,90', image: 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f', details: 'Hausgemachter Hummus aus Kichererbsen, Tahini, Zitrone und Gewürzen. Serviert mit frischem Gemüse und Brot.' },
      { name: 'Guacamole', description: 'Frische Avocado-Creme', price: '3,90', image: 'https://images.unsplash.com/photo-1553909489-cd47e0ef937f', details: 'Cremige Avocado-Creme mit Limette, Koriander, roten Zwiebeln und einem Hauch Chili. Serviert mit Tortilla-Chips.' },
      { name: 'Spanischer Käseteller', description: 'Auswahl spanischer Käsesorten', price: '8,90', image: 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d', details: 'Feine Auswahl von Manchego, Cabrales und Murcia al Vino, serviert mit Walnüssen, Honig und frischen Trauben.' },
      { name: 'Schinken-Käse-Wurst Teller', description: 'Spanische Charcuterie-Platte', price: '11,90', image: 'https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg', details: 'Edle Auswahl aus Jamón Serrano, Chorizo, Lomo und spanischen Käsesorten mit Oliven, Nüssen und Feigenmarmelade.' },
      { name: 'Jamón Serrano Teller', description: 'Hochwertiger spanischer Schinken', price: '9,90', image: 'https://images.pexels.com/photos/24706530/pexels-photo-24706530.jpeg', details: '18 Monate gereifter Jamón Serrano, hauchdünn geschnitten, serviert mit Manchego-Käse und geröstetem Brot.' },
      { name: 'Boquerones en Vinagre', description: 'Sardellen in Essig eingelegt', price: '8,90', image: 'https://images.unsplash.com/photo-1565299507177-b0ac66763828', details: 'Frische Sardellen aus dem Cantabrischen Meer, eingelegt in Weißweinessig mit Knoblauch, Petersilie und Olivenöl.' },
      { name: 'Pata Negra', description: 'Premium Iberico Schinken', price: '10,90', image: 'https://images.unsplash.com/photo-1598989519542-077da0f51c09', details: 'Der Edelste aller spanischen Schinken - 36 Monate gereift von freilaufenden Iberico-Schweinen, serviert mit Manchego.' },
      { name: 'Tres (Hummus, Avocado Cream, Aioli mit Brot)', description: 'Drei köstliche Dips mit Brot', price: '10,90', image: 'https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg', details: 'Trio aus hausgemachtem Hummus, cremiger Avocado-Creme und Aioli, serviert mit warmem spanischem Brot und Gemüse.' }
    ],
    'salat': [
      { name: 'Ensalada Mixta', description: 'Gemischter Salat mit spanischen Zutaten', price: '8,90', details: 'Frischer Salat mit Tomaten, Gurken, Oliven, roten Zwiebeln und Manchego-Käse in Sherry-Vinaigrette.' },
      { name: 'Ensalada Tonno', description: 'Salat mit Thunfisch', price: '14,90', details: 'Gemischter Salat mit saftigem Thunfisch, hartgekochten Eiern, Oliven und Kapern in mediteraner Vinaigrette.' },
      { name: 'Ensalada Pollo', description: 'Salat mit gegrilltem Hähnchen', price: '14,90', details: 'Frischer Salat mit gegrillten Hähnchenstreifen, Cherrytomaten, Avocado und gerösteten Pinienkernen.' },
      { name: 'Ensalada Garnelen', description: 'Salat mit frischen Garnelen', price: '15,90', details: 'Bunter Salat mit saftigen Garnelen, Avocado, Mango und einem Hauch von Chili in Limetten-Dressing.' }
    ],
    'kleiner-salat': [
      { name: 'Tomaten/Gurken mit Zwiebeln', description: 'Frischer Gemüsesalat', price: '6,90', details: 'Saftige Tomaten und knackige Gurken mit roten Zwiebeln in aromatischem Olivenöl und Kräutern.' },
      { name: 'Rote Beete mit Ziegenkäse', description: 'Süße rote Beete mit cremigem Ziegenkäse', price: '7,90', details: 'Geröstete rote Beete mit cremigem Ziegenkäse, Walnüssen und Honig-Thymian-Dressing.' },
      { name: 'Kichererbsen mit Feta', description: 'Proteinreicher Salat mit Feta', price: '7,90', details: 'Warme Kichererbsen mit Feta-Käse, frischen Kräutern, Tomaten und Zitronendressing.' }
    ],
    'tapa-paella': [
      { name: 'Paella mit Hähnchen & Meeresfrüchten', description: 'Traditionelle spanische Paella als Tapa-Portion', price: '8,90', details: 'Authentische Paella mit saftigem Hähnchen, frischen Garnelen, Muscheln und Bomba-Reis in würziger Safran-Brühe.' },
      { name: 'Paella vegetarisch', description: 'Vegetarische Paella mit frischem Gemüse', price: '7,90', details: 'Vegetarische Paella mit grünen Bohnen, Paprika, Artischocken und Bomba-Reis in aromatischer Gemüsebrühe.' }
    ],
    'tapas-vegetarian': [
      { name: 'Gebratenes Gemüse', description: 'Vegan - Saisonales Gemüse mediterran gewürzt', price: '6,90', details: 'Frisches Saisongemüse wie Zucchini, Paprika und Auberginen, gegrillt mit Rosmarin, Thymian und Olivenöl.' },
      { name: 'Papas Bravas', description: 'Vegan - Klassische spanische Kartoffeln mit scharfer Soße', price: '6,90', details: 'Knusprig gebratene Kartoffelwürfel mit pikanter Bravas-Sauce aus Tomaten, Paprika und einem Hauch Chili.' },
      { name: 'Tortilla de Patata mit Aioli', description: 'Spanisches Kartoffel-Omelett mit Aioli', price: '6,90', details: 'Klassische spanische Tortilla aus Kartoffeln und Eiern, golden gebraten, serviert mit hausgemachtem Aioli.' },
      { name: 'Pimientos de Padrón', description: 'Vegan - Gebratene grüne Paprika', price: '6,90', details: 'Kleine grüne Paprikaschoten aus Galicien, gebraten in Olivenöl und mit Meersalz bestreut - manche scharf, manche mild!' },
      { name: 'Kanarische Kartoffeln', description: 'Vegan - Traditionelle Kartoffeln mit Meersalz', price: '6,90', details: 'Kleine Kartoffeln in der Schale gekocht mit grobem Meersalz, serviert mit Mojo Verde und Mojo Rojo.' },
      { name: 'Fetahäppchen auf Johannisbeersauce', description: 'Cremiger Feta mit süß-saurer Sauce', price: '6,90', details: 'Warme Feta-Würfel auf einer Reduktion aus roten Johannisbeeren mit einem Hauch Balsamico und frischen Kräutern.' },
      { name: 'Ziegenkäse auf Johannisbeersauce oder Honig-Senf', description: 'Mild-cremiger Ziegenkäse mit Sauce nach Wahl', price: '6,90', details: 'Warmer Ziegenkäse wahlweise mit süßer Johannisbeersauce oder würzigem Honig-Senf-Dressing und gerösteten Nüssen.' },
      { name: 'Falafel mit Joghurt-Minz-Sauce', description: 'Knusprige Kichererbsenbällchen mit erfrischender Sauce', price: '6,90', details: 'Hausgemachte Falafel aus Kichererbsen und orientalischen Gewürzen, serviert mit cremiger Joghurt-Minz-Sauce.' },
      { name: 'Überbackener Feta mit Cherrytomaten', description: 'Warmer Feta mit süßen Cherrytomaten', price: '6,90', details: 'Feta-Käse überbacken mit Cherrytomaten, Oliven, Oregano und einem Schuss Olivenöl, serviert mit frischem Brot.' },
      { name: 'Champignons mit Reis & Pinienkernen auf Roquefort', description: 'Aromatische Pilze mit würzigem Käse', price: '6,90', details: 'Gefüllte Champignons mit Reis, gerösteten Pinienkernen und würzigem Roquefort-Käse, überbacken und mit Kräutern garniert.' },
      { name: 'Überbackene Tomaten mit Spinat & Roquefort', description: 'Mediterrane Gemüse-Käse-Kombination', price: '6,90', details: 'Große Tomaten gefüllt mit frischem Spinat und würzigem Roquefort, überbacken und mit Basilikum garniert.' },
      { name: 'Frittierte Auberginen mit Honig', description: 'Süß-herzhafte Auberginen-Kreation', price: '6,90', details: 'Auberginenscheiben in leichtem Teig frittiert, mit spanischem Honig glasiert und mit frischen Kräutern garniert.' },
      { name: 'Champignons al Ajillo', description: 'Vegan - Pilze in Knoblauchöl', price: '6,90', details: 'Frische Champignons geschmort in Knoblauchöl mit Petersilie, Chili und einem Schuss Weißwein - ein Klassiker!' },
      { name: 'Teigtaschen mit Spinat & Kräutersauce', description: 'Hausgemachte Teigtaschen mit frischen Kräutern', price: '6,90', details: 'Hausgemachte Teigtaschen gefüllt mit Spinat und Ricotta, serviert mit einer cremigen Kräutersauce.' },
      { name: 'Feta Feigen', description: 'Süße Feigen mit salzigem Feta', price: '6,90', details: 'Frische Feigen gefüllt mit cremigem Feta-Käse, gerösteten Walnüssen und einem Hauch Honig.' },
      { name: 'Ziegenkäse auf Fenchel & Walnuss', description: 'Aromatische Kombination mit Nüssen', price: '6,90', details: 'Warmer Ziegenkäse auf einem Bett aus geröstetem Fenchel mit gerösteten Walnüssen und Honig-Balsamico-Glasur.' },
      { name: 'Gebratener Spinat mit Cherrytomaten', description: 'Vegan - Frischer Spinat mit süßen Tomaten', price: '6,90', details: 'Frischer Spinat geschmort mit Cherrytomaten, Knoblauch und Pinienkernen in bestem Olivenöl.' }
    ],
    'tapas-pollo': [
      { name: 'Hähnchen mit Limetten-Sauce', description: 'Zartes Hähnchen in frischer Zitrus-Sauce', price: '7,20', details: 'Saftige Hähnchenstücke in einer frischen Limetten-Sauce mit Koriander und einem Hauch Chili, serviert mit Kräuterreis.' },
      { name: 'Knuspriges Hähnchen mit Honig-Senf', description: 'Goldbraun gebratenes Hähnchen mit süß-scharfer Sauce', price: '7,20', details: 'Knusprig paniertes Hähnchen mit hausgemachter Honig-Senf-Sauce, garniert mit frischen Kräutern.' },
      { name: 'Hähnchenspieß mit Chili', description: 'Würziger Hähnchen-Spieß mit Chili', price: '7,20', details: 'Marinierte Hähnchenstücke am Spieß mit pikanter Chili-Sauce und gegrilltem Gemüse.' },
      { name: 'Hähnchen mit Curry', description: 'Exotisch gewürztes Hähnchen', price: '7,20', details: 'Zart geschmortes Hähnchen in aromatischer Curry-Sauce mit Kokosmilch und mediterranen Gewürzen.' },
      { name: 'Hähnchen mit Mandelsauce', description: 'Cremige Mandel-Sauce zu zartem Hähnchen', price: '7,20', details: 'Gebratenes Hähnchen in feiner Mandel-Sahne-Sauce mit gerösteten Mandelblättchen.' },
      { name: 'Hähnchen-Chorizo-Spieß', description: 'Spanische Wurst-Fleisch-Kombination', price: '7,20', details: 'Abwechselnd Hähnchen und würzige Chorizo am Spieß gegrillt, serviert mit Paprika und Zwiebeln.' },
      { name: 'Hähnchen mit Brandy-Sauce', description: 'Edle Brandy-Sauce zu saftigem Hähnchen', price: '7,20', details: 'Gebratenes Hähnchen in einer cremigen Sauce aus spanischem Brandy, Sahne und feinen Gewürzen.' }
    ],
    'tapas-carne': [
      { name: 'Dátiles con Bacon', description: 'Süße Datteln mit knusprigem Speck', price: '6,90', details: 'Saftige Datteln gefüllt mit Mandeln, umwickelt mit knusprigem Bacon und im Ofen gebacken.' },
      { name: 'Albondigas', description: 'Spanische Hackfleischbällchen in Tomatensoße', price: '6,90', details: 'Hausgemachte Fleischbällchen nach traditionellem Rezept in würziger Tomatensoße mit frischen Kräutern.' },
      { name: 'Pincho de Cerdo', description: 'Schweinefleisch-Spieß gegrillt', price: '7,90', details: 'Marinierte Schweinefleischstücke am Spieß mit Paprika und Zwiebeln, serviert mit Aioli.' },
      { name: 'Pincho de Cordero', description: 'Lammfleisch-Spieß mit Kräutern', price: '8,90', details: 'Zarte Lammfleischstücke am Spieß mit mediterranen Kräutern und Knoblauch mariniert.' },
      { name: 'Chuletas de Cordero', description: 'Gegrillte Lammkoteletts', price: '9,90', details: 'Saftige Lammkoteletts vom Grill mit Rosmarin und Thymian, serviert mit Knoblauchöl.' },
      { name: 'Rollitos Serrano mit Feige', description: 'Serrano-Schinken-Röllchen mit süßer Feige', price: '9,90', details: 'Hauchdünner Serrano-Schinken gefüllt mit süßen Feigen und Ziegenkäse.' },
      { name: 'Ziegenkäse mit Bacon', description: 'Cremiger Ziegenkäse mit knusprigem Speck', price: '7,90', details: 'Warmer Ziegenkäse in knusprigem Bacon eingewickelt, mit Honig und Pinienkernen.' },
      { name: 'Chorizo al Diablo', description: 'Scharfe Chorizo in Teufelssauce', price: '7,90', details: 'Gegrillte Chorizo in pikanter Sauce mit Rotwein und scharfen Chilischoten.' },
      { name: 'Medaillons vom Schwein', description: 'Zarte Schweinefilet-Medaillons', price: '9,90', details: 'Rosa gebratene Schweinefilet-Medaillons mit Sherrysoße und karamellisierten Zwiebeln.' },
      { name: 'Champignons mit Käse', description: 'Überbackene Pilze mit geschmolzenem Käse', price: '8,90', details: 'Frische Champignons gefüllt mit Serrano-Schinken und Käse überbacken.' },
      { name: 'Schweinefilet mit Cherrytomaten', description: 'Saftiges Filet mit süßen Tomaten', price: '9,50', details: 'Gebratenes Schweinefilet mit geschmorten Cherrytomaten und Basilikum.' },
      { name: 'Schweinefilet in Sauce', description: 'Zartes Filet in aromatischer Sauce', price: '9,50', details: 'Schweinefilet in cremiger Pilz-Sahne-Sauce mit frischen Kräutern.' },
      { name: 'Chorizo a la Plancha', description: 'Gegrillte spanische Wurst', price: '7,90', details: 'Traditionelle spanische Chorizo vom Grill mit Paprika und Zwiebeln.' },
      { name: 'Lammfilet', description: 'Premium Lammfilet rosa gebraten', price: '9,90', details: 'Zartes Lammfilet rosa gebraten mit Rosmarin-Knoblauch-Öl und Thymianjus.' },
      { name: 'Spareribs mit BBQ', description: 'Zarte Rippchen mit BBQ-Sauce', price: '8,90', details: 'Geschmorte Spareribs in hausgemachter BBQ-Sauce mit spanischen Gewürzen.' },
      { name: 'Chicken Wings', description: 'Würzige Hähnchenflügel', price: '9,90', details: 'Knusprige Chicken Wings mariniert in pikanter Sauce mit Knoblauch und Kräutern.' }
    ],
    'tapas-pescado': [
      { name: 'Boquerones Fritos', description: 'Frittierte Sardellen', price: '7,50', details: 'Frisch frittierte Sardellen in knuspriger Panade mit Zitrone und hausgemachter Aioli.' },
      { name: 'Calamares a la Plancha', description: 'Gegrillte Tintenfischringe', price: '8,90', details: 'Zart gegrillte Tintenfischringe mit Knoblauch, Petersilie und Zitrone.' },
      { name: 'Calamares a la Romana', description: 'Panierte Tintenfischringe', price: '7,50', details: 'Knusprig panierte Tintenfischringe serviert mit Zitrone und Aioli.' },
      { name: 'Lachs mit Spinat', description: 'Frischer Lachs auf Spinatbett', price: '9,90', details: 'Gebratenes Lachsfilet auf cremigem Blattspinat mit Knoblauch und Pinienkernen.' },
      { name: 'Gambas a la Plancha', description: 'Gegrillte Garnelen', price: '9,90', details: 'Große Garnelen vom Grill mit Meersalz und Knoblauchöl.' },
      { name: 'Garnelen-Dattel-Spieß', description: 'Süß-salzige Kombination am Spieß', price: '9,90', details: 'Garnelen und süße Datteln am Spieß mit Speck umwickelt.' },
      { name: 'Gambas al Ajillo', description: 'Garnelen in Knoblauchöl', price: '9,90', details: 'In Knoblauchöl gebratene Garnelen mit Chili und frischer Petersilie.' },
      { name: 'Muslitos de Mar', description: 'Gebackene Muscheln', price: '6,90', details: 'Gratinierte Miesmuscheln mit Knoblauch-Kräuter-Kruste.' },
      { name: 'Gegrillter Oktopus', description: 'Zarter Oktopus vom Grill', price: '9,90', details: 'Gegrillter Oktopus mit Paprikapulver, Olivenöl und Meersalz.' },
      { name: 'Jacobsmuscheln', description: 'Edle Jakobsmuscheln gegrillt', price: '9,90', details: 'Gegrillte Jakobsmuscheln mit Knoblauchbutter und Petersilie.' },
      { name: 'Gambas PIL PIL', description: 'Garnelen in würzigem Olivenöl', price: '9,90', details: 'Garnelen in scharfem Olivenöl mit Knoblauch und Cayennepfeffer.' },
      { name: 'Empanadas', description: 'Spanische Teigtaschen mit Füllung', price: '6,90', details: 'Hausgemachte Teigtaschen gefüllt mit Thunfisch und Tomaten.' },
      { name: 'Pfahlmuscheln', description: 'Frische Miesmuscheln in Sud', price: '8,90', details: 'Miesmuscheln in Weißwein-Knoblauch-Sud mit frischen Kräutern.' },
      { name: 'Pulpo al Ajillo', description: 'Oktopus in Knoblauchöl', price: '9,90', details: 'Zarter Oktopus in Knoblauchöl mit Paprikapulver und Petersilie.' },
      { name: 'Zanderfilet', description: 'Zartes Zanderfilet gebraten', price: '9,90', details: 'Gebratenes Zanderfilet mit Zitronenbutter und mediterranem Gemüse.' },
      { name: 'Tiger Garnelen', description: 'Große Tiger-Garnelen gegrillt', price: '9,90', details: 'Gegrillte Tiger-Garnelen mit Knoblauch-Limetten-Butter.' },
      { name: 'Brocheta de Gambas', description: 'Garnelen-Spieß mit Gemüse', price: '8,90', details: 'Garnelen-Spieß mit Paprika und Zwiebeln vom Grill.' },
      { name: 'Boqueron in Tempura', description: 'Sardellen im Tempura-Teig', price: '7,50', details: 'Sardellen im leichten Tempura-Teig mit Zitronen-Aioli.' },
      { name: 'Chipirones', description: 'Baby-Tintenfische gegrillt', price: '8,90', details: 'Gegrillte Baby-Tintenfische mit Knoblauch und Petersilie.' }
    ],
    'kroketten': [
      { name: 'Bacalao', description: 'Stockfisch-Kroketten', price: '5,90', details: 'Cremige Kroketten aus Stockfisch und Kartoffeln, traditionell zubereitet.' },
      { name: 'Käse', description: 'Cremige Käse-Kroketten', price: '5,90', details: 'Hausgemachte Kroketten mit einer Füllung aus spanischen Käsesorten.' },
      { name: 'Mandeln', description: 'Mandel-Kroketten mit feinem Aroma', price: '6,50', details: 'Süße Kroketten aus gemahlenen Mandeln mit Honig und Zimt.' },
      { name: 'Jamón', description: 'Schinken-Kroketten klassisch', price: '5,90', details: 'Traditionelle Kroketten mit feiner Serrano-Schinken-Füllung.' },
      { name: 'Kartoffel', description: 'Traditionelle Kartoffel-Kroketten', price: '5,50', details: 'Klassische Kartoffelkroketten mit Kräutern und Gewürzen.' }
    ],
    'pasta': [
      { name: 'Spaghetti Aglio e Olio', description: 'Klassisch mit Knoblauch und Olivenöl', price: '12,90', details: 'Al dente gekochte Spaghetti mit bestem Olivenöl, frischem Knoblauch und Peperoncini.' },
      { name: 'Spaghetti Bolognese', description: 'Mit hausgemachter Fleischsauce', price: '14,90', details: 'Traditionelle Bolognese-Sauce mit Rinderhack, langsam geschmort mit Rotwein und Kräutern.' },
      { name: 'Pasta Brokkoli Gorgonzola', description: 'Cremige Gorgonzola-Sauce mit Brokkoli', price: '14,90', details: 'Frischer Brokkoli in cremiger Gorgonzola-Sauce mit gerösteten Pinienkernen.' },
      { name: 'Pasta Verdura', description: 'Mit frischem Saisongemüse', price: '14,90', details: 'Mediterranes Gemüse der Saison mit Olivenöl und frischen Kräutern.' },
      { name: 'Pasta Garnelen', description: 'Mit frischen Garnelen und Knoblauch', price: '16,90', details: 'Saftige Garnelen in Knoblauch-Weißwein-Sauce mit Kirschtomaten und Basilikum.' }
    ],
    'pizza': [
      { name: 'Margherita', description: 'Tomaten, Mozzarella, Basilikum', price: '9,90', details: 'Klassische Pizza mit hausgemachter Tomatensauce, frischem Mozzarella und Basilikum.' },
      { name: 'Schinken', description: 'Mit spanischem Schinken', price: '12,90', details: 'Pizza mit Serrano-Schinken, Mozzarella und frischen Rucola.' },
      { name: 'Funghi', description: 'Mit frischen Champignons', price: '12,90', details: 'Pizza mit sautierten Champignons, Mozzarella und frischen Kräutern.' },
      { name: 'Tonno', description: 'Mit Thunfisch und Zwiebeln', price: '13,90', details: 'Pizza mit Thunfisch, roten Zwiebeln, Kapern und schwarzen Oliven.' },
      { name: 'Hawaii', description: 'Mit Schinken und Ananas', price: '13,90', details: 'Pizza mit gekochtem Schinken, frischer Ananas und extra Käse.' },
      { name: 'Verdura', description: 'Mit gegrilltem Gemüse', price: '13,90', details: 'Pizza mit verschiedenem Grillgemüse, Mozzarella und Basilikumpesto.' },
      { name: 'Salami', description: 'Mit würziger Salami', price: '12,90', details: 'Pizza mit italienischer Salami, Mozzarella und frischen Kräutern.' },
      { name: 'Garnelen', description: 'Mit frischen Garnelen', price: '15,90', details: 'Pizza mit Garnelen, Knoblauch, Cherrytomaten und Rucola.' },
      { name: 'Bolognese', description: 'Mit Hackfleischsauce', price: '13,90', details: 'Pizza mit hausgemachter Bolognese-Sauce und extra Käse.' },
      { name: "Jimmy's Special", description: 'Unsere Haus-Spezial-Pizza', price: '13,90', details: 'Geheimrezept des Hauses mit ausgewählten spanischen Zutaten.' }
    ],
    'snacks': [
      { name: 'Pommes', description: 'Goldgelbe Kartoffel-Pommes', price: '5,50', details: 'Knusprige Pommes frites mit hausgemachten Dips nach Wahl.' },
      { name: 'Chicken Nuggets', description: 'Knusprige Hähnchen-Nuggets', price: '8,90', details: 'Hausgemachte Chicken Nuggets aus frischem Hähnchenfilet mit verschiedenen Dips.' },
      { name: 'Chicken Wings', description: 'Würzige Hähnchenflügel', price: '9,90', details: 'Marinierte und knusprig gebratene Chicken Wings mit BBQ-Sauce.' },
      { name: 'Currywurst', description: 'Deutsche Currywurst klassisch', price: '10,90', details: 'Klassische Currywurst mit hausgemachter Sauce und Pommes frites.' }
    ],
    'dessert': [
      { name: 'Crema Catalana', description: 'Katalanische Crème brûlée', price: '5,50', details: 'Traditionelle spanische Crème brûlée mit karamellisierter Zuckerkruste.' },
      { name: 'Tarte de Santiago', description: 'Spanischer Mandelkuchen', price: '7,50', details: 'Klassischer spanischer Mandelkuchen nach Originalrezept aus Galizien.' },
      { name: 'Eis', description: 'Hausgemachtes Eis nach Wahl', price: '6,90', details: 'Verschiedene Sorten hausgemachtes Eis mit frischen Früchten.' },
      { name: 'Churros mit Schokolade', description: 'Spanisches Spritzgebäck mit warmer Schokolade', price: '6,90', details: 'Frisch zubereitete Churros mit heißer Schokoladensauce zum Dippen.' },
      { name: 'Schoko Soufflé', description: 'Warmes Schokoladen-Soufflé', price: '7,50', details: 'Warmes Schokoladen-Soufflé mit flüssigem Kern und Vanilleeis.' }
    ],
    'helados': [
      { name: 'Kokos', description: 'Eis im Fruchtschälchen - Kokos', price: '6,90', details: 'Cremiges Kokoseis serviert in einer echten Kokosnussschale mit Kokosflocken.' },
      { name: 'Zitrone', description: 'Eis im Fruchtschälchen - Zitrone', price: '6,90', details: 'Erfrischendes Zitronensorbet in einer ausgehöhlten Zitrone serviert.' },
      { name: 'Orange', description: 'Eis im Fruchtschälchen - Orange', price: '6,90', details: 'Fruchtiges Orangensorbet in einer halbierten Orange präsentiert.' },
      { name: 'Nuss', description: 'Eis im Fruchtschälchen - Nuss', price: '6,90', details: 'Nusseis mit karamellisierten Nüssen in einer Kokosschale serviert.' }
    ]
  };

  const categories = [
    { id: 'alle', name: 'Alle Kategorien' },
    { id: 'inicio', name: 'Inicio' },
    { id: 'salat', name: 'Salat' },
    { id: 'kleiner-salat', name: 'Kleiner Salat' },
    { id: 'tapa-paella', name: 'Tapa Paella' },
    { id: 'tapas-vegetarian', name: 'Tapas Vegetarian' },
    { id: 'tapas-pollo', name: 'Tapas de Pollo' },
    { id: 'tapas-carne', name: 'Tapas de Carne' },
    { id: 'tapas-pescado', name: 'Tapas de Pescado' },
    { id: 'kroketten', name: 'Kroketten' },
    { id: 'pasta', name: 'Pasta' },
    { id: 'pizza', name: 'Pizza' },
    { id: 'snacks', name: 'Snacks' },
    { id: 'dessert', name: 'Dessert' },
    { id: 'helados', name: 'Helados' }
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
    <div className="min-h-screen speisekarte-background">
      {/* Elegant Header Section with Background Image */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('https://images.pexels.com/photos/24706530/pexels-photo-24706530.jpeg')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              Speisekarte
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              Authentische spanische Küche - Bewegen Sie die Maus über Gerichte für Bildvorschau
            </p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-12">        
        {/* Category Filter Buttons - No Icons */}
        <div className="flex flex-wrap justify-center gap-3 mb-12">
          {categories.map((category) => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`menu-category px-6 py-3 rounded-lg transition-all duration-300 font-light tracking-wide text-sm ${
                selectedCategory === category.id
                  ? 'bg-warm-beige text-dark-brown shadow-lg'
                  : 'border border-warm-beige text-warm-beige hover:bg-warm-beige hover:text-dark-brown hover:shadow-lg'
              }`}
            >
              {category.name}
            </button>
          ))}
        </div>

        {/* Menu Items - Screenshot Style Two-Column Layout with Hover Images */}
        <div className="grid md:grid-cols-2 gap-6 max-w-7xl mx-auto">
          {getDisplayItems().map((item, index) => (
            <div key={index} className="menu-item rounded-lg p-6 hover:bg-medium-brown transition-all duration-300 relative group">
              <div className="flex justify-between items-start">
                {/* Dish name and description */}
                <div className="flex-1 pr-4">
                  <h3 className="text-xl font-serif text-warm-beige mb-2 tracking-wide">
                    {item.name}
                  </h3>
                  <p className="text-light-beige mb-2 font-light leading-relaxed text-sm">{item.description}</p>
                  <span className="text-xs text-warm-beige capitalize font-light tracking-wide opacity-75">
                    {categories.find(c => c.id === item.category)?.name}
                  </span>
                </div>
                
                {/* Price - Right aligned like in screenshot */}
                <div className="text-2xl font-serif text-warm-beige tracking-wide flex-shrink-0">
                  {item.price} €
                </div>
              </div>
              
              {/* Screenshot-Style Hover Image */}
              <div className="menu-image-tooltip">
                <img 
                  src={item.image} 
                  alt={item.name}
                  loading="lazy"
                />
                <div className="absolute bottom-2 right-2 bg-black bg-opacity-70 text-white px-2 py-1 rounded text-sm">
                  {item.name}
                </div>
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
    <div className="min-h-screen bg-dark-brown pt-24">
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
    <div className="min-h-screen bg-dark-brown pt-24">
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
    <div className="min-h-screen bg-dark-brown pt-24">
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
    <div className="App min-h-screen bg-dark-brown">
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