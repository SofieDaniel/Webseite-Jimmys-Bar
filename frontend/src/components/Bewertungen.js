import React, { useState, useEffect } from 'react';

const Bewertungen = () => {
  const [feedback, setFeedback] = useState({
    name: '',
    email: '',
    rating: 5,
    comment: ''
  });
  
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [pageData, setPageData] = useState(null);

  useEffect(() => {
    loadPageData();
    loadReviews();
  }, []);

  const loadPageData = async () => {
    try {
      const response = await fetch(`/api/cms/bewertungen-page`);
      if (response.ok) {
        const data = await response.json();
        setPageData(data);
      }
    } catch (error) {
      console.error('Error loading page data:', error);
    }
  };

  const loadReviews = async () => {
    try {
      setLoading(true);
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setMessage('');
    
    try {
      const reviewData = {
        customer_name: feedback.name,
        rating: parseInt(feedback.rating),
        comment: feedback.comment
      };

      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/reviews`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(reviewData)
      });

      if (response.ok) {
        setMessage('Vielen Dank für Ihr Feedback! Es wurde intern gespeichert.');
        setFeedback({ name: '', email: '', rating: 5, comment: '' });
      } else {
        setMessage('Fehler beim Senden der Bewertung. Bitte versuchen Sie es erneut.');
      }
    } catch (error) {
      console.error('Error submitting review:', error);
      setMessage('Fehler beim Senden der Bewertung. Bitte versuchen Sie es erneut.');
    } finally {
      setSubmitting(false);
    }
  };

  const renderStars = (rating) => {
    return Array.from({ length: 5 }, (_, i) => (
      <span key={i} className={`text-2xl ${i < rating ? 'text-yellow-400' : 'text-warm-brown'}`}>
        ★
      </span>
    ));
  };

  const formatDate = (dateString) => {
    try {
      if (!dateString) return 'Unbekanntes Datum';
      
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return 'Unbekanntes Datum';
      
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

  return (
    <div className="min-h-screen bg-dark-brown">
      {/* Elegant Header Section with Background */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('${pageData?.header_background || 'https://images.pexels.com/photos/26626726/pexels-photo-26626726.jpeg'}')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              {pageData?.page_title || 'Bewertungen & Feedback'}
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              {pageData?.page_subtitle || 'Was unsere Gäste über uns sagen'}
            </p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-16">
        
        <div className="grid lg:grid-cols-2 gap-12 max-w-7xl mx-auto">
          {/* Public Reviews */}
          <div>
            <h2 className="text-3xl font-serif text-warm-beige mb-8 tracking-wide">
              {pageData?.reviews_section_title || 'Kundenbewertungen'}
            </h2>
            <div className="space-y-8">
              {loading ? (
                <div className="text-warm-beige text-center">Lade Bewertungen...</div>
              ) : reviews.length === 0 ? (
                <div className="bg-dark-brown rounded-lg border border-warm-brown p-8">
                  <p className="text-light-beige font-light text-center">Noch keine Bewertungen vorhanden.</p>
                </div>
              ) : (
                reviews.map((review, index) => (
                  <div key={index} className="bg-dark-brown rounded-lg border border-warm-brown p-8">
                    <div className="flex justify-between items-start mb-4">
                      <h3 className="font-light text-warm-beige text-lg tracking-wide">
                        {review.customer_name || review.name}
                      </h3>
                      <span className="text-sm text-light-beige font-light">
                        {formatDate(review.date || review.created_at)}
                      </span>
                    </div>
                    <div className="flex mb-4">
                      {renderStars(review.rating)}
                    </div>
                    <p className="text-light-beige font-light leading-relaxed">{review.comment}</p>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Feedback Form */}
          <div>
            <h2 className="text-3xl font-serif text-warm-beige mb-8 tracking-wide">
              {pageData?.feedback_section_title || 'Ihr Feedback'}
            </h2>
            <div className="bg-dark-brown rounded-lg border border-warm-brown p-8">
              <p className="text-light-beige mb-6 text-sm font-light">
                {pageData?.feedback_note || 'Dieses Feedback wird intern gespeichert und nicht öffentlich angezeigt.'}
              </p>
              
              {message && (
                <div className={`mb-6 p-4 rounded-lg ${message.includes('Vielen Dank') ? 'bg-green-800 border border-green-600' : 'bg-red-800 border border-red-600'}`}>
                  <p className="text-white text-sm">{message}</p>
                </div>
              )}
              
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="block text-warm-beige font-light mb-3 tracking-wide">Name</label>
                  <input
                    type="text"
                    value={feedback.name}
                    onChange={(e) => setFeedback({...feedback, name: e.target.value})}
                    className="w-full p-4 bg-medium-brown border border-warm-brown rounded-lg focus:ring-2 focus:ring-warm-beige focus:border-warm-beige text-warm-beige font-light"
                    required
                    disabled={submitting}
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
                    disabled={submitting}
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
                        disabled={submitting}
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
                    disabled={submitting}
                  />
                </div>
                <button
                  type="submit"
                  className="w-full bg-warm-beige hover:bg-light-beige text-dark-brown py-4 rounded-lg font-light transition-colors tracking-wide disabled:opacity-50"
                  disabled={submitting}
                >
                  {submitting ? 'Wird gesendet...' : 'Feedback senden'}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Bewertungen;