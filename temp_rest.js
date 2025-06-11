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
    <div className="min-h-screen bg-dark-brown">
      {/* Elegant Header Section with Background */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('https://images.pexels.com/photos/26626726/pexels-photo-26626726.jpeg')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              Kontakt
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              Wir freuen uns auf Ihre Nachricht
            </p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-16">
        
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
    <div className="min-h-screen bg-dark-brown pt-24">
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
    <div className="min-h-screen bg-dark-brown pt-24">
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
