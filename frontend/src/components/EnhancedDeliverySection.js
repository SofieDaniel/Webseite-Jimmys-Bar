import React, { useState, useEffect } from 'react';

const EnhancedDeliverySection = () => {
  const [deliveryInfo, setDeliveryInfo] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDeliveryInfo = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/delivery/info`);
        if (response.ok) {
          const data = await response.json();
          setDeliveryInfo(data);
        }
      } catch (error) {
        console.error('Error fetching delivery info:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDeliveryInfo();
  }, []);

  if (loading) {
    return (
      <div className="py-20 bg-dark-brown">
        <div className="container mx-auto px-8 text-center">
          <div className="animate-pulse">
            <div className="h-8 bg-warm-beige/20 rounded w-1/3 mx-auto mb-4"></div>
            <div className="h-4 bg-warm-beige/20 rounded w-2/3 mx-auto"></div>
          </div>
        </div>
      </div>
    );
  }

  if (!deliveryInfo) {
    return null;
  }

  const handleOrderClick = () => {
    // Open Lieferando in new tab
    window.open('https://www.lieferando.de/restaurants-neustadt-in-holstein', '_blank');
  };

  return (
    <section className="py-20 bg-dark-brown">
      <div className="container mx-auto px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-serif text-warm-beige mb-6">
            Jetzt auch bequem nach Hause bestellen
          </h2>
          <p className="text-lg text-light-beige max-w-3xl mx-auto leading-relaxed">
            Genießen Sie unsere authentischen mediterranen Spezialitäten gemütlich zu Hause. 
            Bestellen Sie direkt über Lieferando und lassen Sie sich verwöhnen.
          </p>
        </div>

        {/* Main Content Area */}
        <div className="max-w-6xl mx-auto">
          {/* Top Section with Images and CTA */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
            {/* Left - Fast Delivery */}
            <div className="text-center">
              <div className="w-32 h-32 mx-auto mb-4 rounded-xl overflow-hidden">
                <img 
                  src="https://images.unsplash.com/photo-1593513167664-40d04b73afac?ixlib=rb-4.0.3&auto=format&fit=crop&w=320&q=80"
                  alt="Schnelle Lieferung"
                  className="w-full h-full object-cover"
                />
              </div>
              <h3 className="text-xl font-serif text-warm-beige mb-2">Schnelle Lieferung</h3>
              <p className="text-light-beige text-sm">Frisch und warm zu Ihnen</p>
            </div>

            {/* Center - CTA Button */}
            <div className="flex flex-col justify-center items-center">
              <button
                onClick={handleOrderClick}
                className="bg-[#ff5722] hover:bg-[#e64919] text-white font-bold py-4 px-8 rounded-lg text-lg transition-all transform hover:scale-105 shadow-lg mb-4"
              >
                Jetzt bei Lieferando bestellen
              </button>
              <p className="text-light-beige text-sm text-center">
                Verfügbar für beide Standorte
              </p>
            </div>

            {/* Right - Authentic Mediterranean */}
            <div className="text-center">
              <div className="w-32 h-32 mx-auto mb-4 rounded-xl overflow-hidden">
                <img 
                  src="https://images.unsplash.com/photo-1555939594-58d7cb561ad1?ixlib=rb-4.0.3&auto=format&fit=crop&w=320&q=80"
                  alt="Authentisch Mediterran"
                  className="w-full h-full object-cover"
                />
              </div>
              <h3 className="text-xl font-serif text-warm-beige mb-2">Authentisch Mediterran</h3>
              <p className="text-light-beige text-sm">Direkt vom Küchenchef</p>
            </div>
          </div>

          {/* Delivery Info Cards with Images instead of Icons */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Delivery Time */}
            <div className="bg-gradient-to-br from-warm-beige/10 to-warm-beige/5 rounded-xl p-6 text-center border border-warm-beige/20">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full overflow-hidden">
                <img 
                  src="https://images.unsplash.com/photo-1606744824163-985d376605aa?ixlib=rb-4.0.3&auto=format&fit=crop&w=64&q=80"
                  alt="Lieferzeit"
                  className="w-full h-full object-cover"
                />
              </div>
              <h4 className="text-lg font-semibold text-warm-beige mb-2">Lieferzeit</h4>
              <p className="text-light-beige text-sm">
                {deliveryInfo.delivery_time_min}-{deliveryInfo.delivery_time_max} Minuten
              </p>
            </div>

            {/* Minimum Order */}
            <div className="bg-gradient-to-br from-warm-beige/10 to-warm-beige/5 rounded-xl p-6 text-center border border-warm-beige/20">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full overflow-hidden">
                <img 
                  src="https://images.unsplash.com/photo-1554749204-293d9d7fae8d?ixlib=rb-4.0.3&auto=format&fit=crop&w=64&q=80"
                  alt="Mindestbestellwert"
                  className="w-full h-full object-cover"
                />
              </div>
              <h4 className="text-lg font-semibold text-warm-beige mb-2">Mindestbestellwert</h4>
              <p className="text-light-beige text-sm">
                {parseFloat(deliveryInfo.minimum_order_value).toFixed(2)}€
              </p>
            </div>

            {/* Delivery Fee */}
            <div className="bg-gradient-to-br from-warm-beige/10 to-warm-beige/5 rounded-xl p-6 text-center border border-warm-beige/20">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full overflow-hidden">
                <img 
                  src="https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=64&q=80"
                  alt="Liefergebühr"
                  className="w-full h-full object-cover"
                />
              </div>
              <h4 className="text-lg font-semibold text-warm-beige mb-2">Liefergebühr</h4>
              <p className="text-light-beige text-sm">
                {parseFloat(deliveryInfo.delivery_fee).toFixed(2)}€
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default EnhancedDeliverySection;