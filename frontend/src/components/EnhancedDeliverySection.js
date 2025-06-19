import React, { useState, useEffect } from 'react';

const EnhancedDeliverySection = () => {
  const [deliveryInfo, setDeliveryInfo] = useState(null);
  const [selectedLocation, setSelectedLocation] = useState('neustadt');
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

  const handleLocationSelect = (location) => {
    setSelectedLocation(location);
  };

  const handleOrderClick = () => {
    // Open Lieferando in new tab (you can customize this URL)
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

          {/* Delivery Info Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            {/* Delivery Time */}
            <div className="bg-gradient-to-br from-warm-beige/10 to-warm-beige/5 rounded-xl p-6 text-center border border-warm-beige/20">
              <div className="w-16 h-16 bg-warm-beige/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-warm-beige" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h4 className="text-lg font-semibold text-warm-beige mb-2">Lieferzeit</h4>
              <p className="text-light-beige text-sm">
                {deliveryInfo.delivery_time_min}-{deliveryInfo.delivery_time_max} Minuten
              </p>
            </div>

            {/* Minimum Order */}
            <div className="bg-gradient-to-br from-warm-beige/10 to-warm-beige/5 rounded-xl p-6 text-center border border-warm-beige/20">
              <div className="w-16 h-16 bg-warm-beige/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-warm-beige" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                </svg>
              </div>
              <h4 className="text-lg font-semibold text-warm-beige mb-2">Mindestbestellwert</h4>
              <p className="text-light-beige text-sm">
                {deliveryInfo.minimum_order_value.toFixed(2)}€
              </p>
            </div>

            {/* Delivery Fee */}
            <div className="bg-gradient-to-br from-warm-beige/10 to-warm-beige/5 rounded-xl p-6 text-center border border-warm-beige/20">
              <div className="w-16 h-16 bg-warm-beige/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-warm-beige" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                </svg>
              </div>
              <h4 className="text-lg font-semibold text-warm-beige mb-2">Liefergebühr</h4>
              <p className="text-light-beige text-sm">
                {deliveryInfo.delivery_fee.toFixed(2)}€
              </p>
            </div>
          </div>

          {/* Location Selection */}
          <div className="bg-gradient-to-r from-warm-beige/5 to-light-beige/5 rounded-xl p-8">
            <h3 className="text-2xl font-serif text-warm-beige text-center mb-6">
              Oder direkt für Ihren Standort bestellen:
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {Object.entries(deliveryInfo.available_locations || {}).map(([key, location]) => (
                <button
                  key={key}
                  onClick={() => handleLocationSelect(key)}
                  className={`p-6 rounded-xl border-2 transition-all text-left ${
                    selectedLocation === key
                      ? 'border-warm-beige bg-warm-beige/10'
                      : 'border-warm-beige/30 hover:border-warm-beige/60 bg-transparent'
                  }`}
                >
                  <div className="flex items-center mb-3">
                    <div className="w-3 h-3 rounded-full bg-red-500 mr-3"></div>
                    <h4 className="text-lg font-semibold text-warm-beige">{location.name}</h4>
                  </div>
                  {location.address && (
                    <p className="text-light-beige text-sm mb-3">{location.address}</p>
                  )}
                  <div className="flex items-center text-green-400 text-sm">
                    <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    Verfügbar
                  </div>
                </button>
              ))}
            </div>
            
            <div className="text-center mt-8">
              <button
                onClick={handleOrderClick}
                className="bg-warm-beige hover:bg-light-beige text-dark-brown font-bold py-3 px-8 rounded-lg transition-all transform hover:scale-105"
              >
                Jetzt bestellen für {deliveryInfo.available_locations[selectedLocation]?.name || 'Standort'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default EnhancedDeliverySection;