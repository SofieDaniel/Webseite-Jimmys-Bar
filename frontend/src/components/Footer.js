import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  const [footerTexts, setFooterTexts] = useState({
    opening_hours_title: "Öffnungszeiten",
    contact_title: "Kontakt",
    follow_us_title: "Folgen Sie uns",
    copyright: "© 2024 Jimmy's Tapas Bar. Alle Rechte vorbehalten."
  });

  // Load footer texts from backend
  useEffect(() => {
    const loadFooterTexts = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/website-texts/footer`);
        if (response.ok) {
          const data = await response.json();
          if (data.footer) {
            setFooterTexts(data.footer);
          }
        }
      } catch (error) {
        console.error('Error loading footer texts:', error);
      }
    };
    loadFooterTexts();
  }, []);

  return (
    <footer className="bg-dark-brown border-t-2 border-warm-brown">
      <div className="container mx-auto px-4 py-16">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Restaurant Info */}
          <div>
            <h3 className="text-xl font-serif text-warm-beige mb-6 tracking-wide">Jimmy's Tapas Bar</h3>
            <p className="text-light-beige font-light mb-4">
              Authentische mediterrane Küche an der malerischen Ostseeküste
            </p>
            <div className="space-y-2">
              <p className="text-light-beige text-sm">Kühlungsborn</p>
              <p className="text-light-beige text-sm">Warnemünde</p>
            </div>
          </div>

          {/* Öffnungszeiten */}
          <div>
            <h3 className="text-xl font-serif text-warm-beige mb-6 tracking-wide">{footerTexts.opening_hours_title}</h3>
            <div className="space-y-2 text-light-beige text-sm">
              <p>Mo-Do: 16:00 - 23:00</p>
              <p>Fr: 16:00 - 24:00</p>
              <p>Sa: 12:00 - 24:00</p>
              <p>So: 12:00 - 23:00</p>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-xl font-serif text-warm-beige mb-6 tracking-wide">Schnellzugriff</h3>
            <nav className="space-y-3">
              <Link to="/speisekarte" className="block text-light-beige hover:text-warm-beige transition-colors text-sm">Speisekarte</Link>
              <Link to="/standorte" className="block text-light-beige hover:text-warm-beige transition-colors text-sm">Standorte</Link>
              <Link to="/bewertungen" className="block text-light-beige hover:text-warm-beige transition-colors text-sm">Bewertungen</Link>
              <Link to="/kontakt" className="block text-light-beige hover:text-warm-beige transition-colors text-sm">Kontakt</Link>
            </nav>
          </div>

          {/* Newsletter */}
          <div>
            <h3 className="text-xl font-serif text-warm-beige mb-6 tracking-wide">Newsletter</h3>
            <p className="text-light-beige text-sm mb-4">Bleiben Sie informiert über neue Gerichte und Events</p>
            <form className="space-y-3">
              <input
                type="email"
                placeholder="E-Mail-Adresse"
                className="w-full px-3 py-2 bg-medium-brown border border-warm-brown rounded text-light-beige placeholder-gray-400 focus:ring-2 focus:ring-warm-beige focus:border-transparent"
              />
              <button
                type="submit"
                className="w-full bg-warm-beige text-dark-brown py-2 rounded font-medium hover:bg-light-beige transition-colors"
              >
                Anmelden
              </button>
            </form>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-warm-brown mt-12 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-light-beige text-sm mb-4 md:mb-0">{footerTexts.copyright}</p>
            <div className="flex space-x-6">
              <Link to="/impressum" className="text-light-beige hover:text-warm-beige transition-colors text-sm">Impressum</Link>
              <Link to="/datenschutz" className="text-light-beige hover:text-warm-beige transition-colors text-sm">Datenschutz</Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;