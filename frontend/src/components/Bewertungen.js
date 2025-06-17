import React, { useState, useEffect } from 'react';

const Bewertungen = () => {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newReview, setNewReview] = useState({
    name: '',
    email: '',
    rating: 5,
    comment: ''
  });
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState('');

  // Helper function to format date
  const formatDate = (dateString) => {
    try {
      if (!dateString) return 'Unbekanntes Datum';
      
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return 'Unbekanntes Datum';
      
      // Format as "März 2024"
      const options = { 
        year: 'numeric', 
        month: 'long'
      };
      return date.toLocaleDateString('de-DE', options);
    } catch (error) {
      console.error('Date formatting error:', error);
      return 'Unbekanntes Datum';
    }
  };

  // Load approved reviews from backend
  useEffect(() => {
    const loadReviews = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/reviews?approved_only=true`);
        if (response.ok) {
          const data = await response.json();
          setReviews(data);
        }
      } catch (error) {
        console.error('Error loading reviews:', error);
      } finally {
        setLoading(false);
      }
    };
    loadReviews();
  }, []);

  const handleSubmitReview = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setMessage('');

    try {
      const reviewData = {
        customer_name: newReview.name,
        rating: parseInt(newReview.rating),
        comment: newReview.comment
      };

      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/reviews`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(reviewData)
      });

      if (response.ok) {
        setMessage('Vielen Dank für Ihre Bewertung! Sie wird nach Prüfung veröffentlicht.');
        setNewReview({ name: '', email: '', rating: 5, comment: '' });
      } else {
        setMessage('Fehler beim Senden der Bewertung. Bitte versuchen Sie es erneut.');
      }
    } catch (error) {
      setMessage('Verbindungsfehler. Bitte versuchen Sie es später erneut.');
    } finally {
      setSubmitting(false);
    }
  };

  const renderStars = (rating) => {
    return Array(5).fill(0).map((_, i) => (
      <span key={i} className={`text-2xl ${i < rating ? 'text-yellow-400' : 'text-gray-400'}`}>
        ★
      </span>
    ));
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-warm-beige"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Header Section */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('https://images.unsplash.com/photo-1559329007-40df8a9345d8')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              Bewertungen
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              Was unsere Gäste über uns sagen
            </p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-16">
        {/* Reviews Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          {reviews.map((review, index) => (
            <div key={index} className="bg-medium-brown rounded-lg border border-warm-brown p-6 shadow-lg">
              <div className="flex items-center mb-4">
                <div className="flex">
                  {renderStars(review.rating)}
                </div>
              </div>
              <p className="text-light-beige mb-4 italic">"{review.comment}"</p>
              <div className="text-warm-beige font-medium">{review.customer_name || review.name}</div>
              <div className="text-gray-400 text-sm">
                {formatDate(review.date || review.created_at)}
              </div>
            </div>
          ))}
        </div>

        {reviews.length === 0 && (
          <div className="text-center mb-16">
            <p className="text-light-beige text-lg">Noch keine Bewertungen vorhanden. Seien Sie der Erste!</p>
          </div>
        )}

        {/* Review Form */}
        <div className="max-w-2xl mx-auto">
          <div className="bg-medium-brown rounded-lg border border-warm-brown p-8">
            <h2 className="text-3xl font-serif text-warm-beige mb-6 text-center">Ihre Bewertung</h2>
            
            {message && (
              <div className={`mb-6 p-4 rounded-lg ${
                message.includes('Vielen Dank') 
                  ? 'bg-green-600 text-white' 
                  : 'bg-red-600 text-white'
              }`}>
                {message}
              </div>
            )}

            <form onSubmit={handleSubmitReview} className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-warm-beige font-medium mb-2">Name *</label>
                  <input
                    type="text"
                    required
                    value={newReview.name}
                    onChange={(e) => setNewReview({...newReview, name: e.target.value})}
                    className="w-full px-4 py-3 bg-dark-brown border border-warm-brown rounded-lg text-light-beige focus:ring-2 focus:ring-warm-beige focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-warm-beige font-medium mb-2">E-Mail *</label>
                  <input
                    type="email"
                    required
                    value={newReview.email}
                    onChange={(e) => setNewReview({...newReview, email: e.target.value})}
                    className="w-full px-4 py-3 bg-dark-brown border border-warm-brown rounded-lg text-light-beige focus:ring-2 focus:ring-warm-beige focus:border-transparent"
                  />
                </div>
              </div>

              <div>
                <label className="block text-warm-beige font-medium mb-2">Bewertung *</label>
                <div className="flex space-x-2">
                  {[1, 2, 3, 4, 5].map(star => (
                    <button
                      key={star}
                      type="button"
                      onClick={() => setNewReview({...newReview, rating: star})}
                      className={`text-3xl ${star <= newReview.rating ? 'text-yellow-400' : 'text-gray-400'} hover:text-yellow-300 transition-colors`}
                    >
                      ★
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-warm-beige font-medium mb-2">Kommentar *</label>
                <textarea
                  required
                  rows={4}
                  value={newReview.comment}
                  onChange={(e) => setNewReview({...newReview, comment: e.target.value})}
                  className="w-full px-4 py-3 bg-dark-brown border border-warm-brown rounded-lg text-light-beige focus:ring-2 focus:ring-warm-beige focus:border-transparent"
                  placeholder="Teilen Sie Ihre Erfahrung mit uns..."
                />
              </div>

              <button
                type="submit"
                disabled={submitting}
                className="w-full bg-warm-beige text-dark-brown py-3 rounded-lg font-medium hover:bg-light-beige transition-colors disabled:opacity-50"
              >
                {submitting ? 'Wird gesendet...' : 'Bewertung absenden'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Bewertungen;