import React, { useState, useEffect } from 'react';

const ReviewsAdminSection = () => {
  const [reviews, setReviews] = useState([]);
  const [pendingReviews, setPendingReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  const [activeTab, setActiveTab] = useState('pending');

  useEffect(() => {
    loadReviews();
  }, []);

  const loadReviews = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('adminToken');
      const headers = {
        'Authorization': `Bearer ${token}`
      };

      // Load all reviews
      const reviewsResponse = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/reviews?approved_only=false`, { headers });
      if (reviewsResponse.ok) {
        const allReviews = await reviewsResponse.json();
        setReviews(allReviews.filter(r => r.is_approved));
        setPendingReviews(allReviews.filter(r => !r.is_approved));
      }
    } catch (error) {
      console.error('Error loading reviews:', error);
      setMessage('Fehler beim Laden der Bewertungen');
    } finally {
      setLoading(false);
    }
  };

  const approveReview = async (reviewId) => {
    try {
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/reviews/${reviewId}/approve`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        setMessage('Bewertung erfolgreich genehmigt!');
        loadReviews();
        setTimeout(() => setMessage(''), 3000);
      } else {
        setMessage('Fehler beim Genehmigen der Bewertung');
      }
    } catch (error) {
      setMessage('Verbindungsfehler');
    }
  };

  const deleteReview = async (reviewId) => {
    if (!window.confirm('Sind Sie sicher, dass Sie diese Bewertung löschen möchten?')) return;

    try {
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/reviews/${reviewId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        setMessage('Bewertung erfolgreich gelöscht!');
        loadReviews();
        setTimeout(() => setMessage(''), 3000);
      } else {
        setMessage('Fehler beim Löschen der Bewertung');
      }
    } catch (error) {
      setMessage('Verbindungsfehler');
    }
  };

  const renderStars = (rating) => {
    return Array.from({ length: 5 }, (_, index) => (
      <span key={index} className={index < rating ? 'text-yellow-400' : 'text-gray-300'}>
        ⭐
      </span>
    ));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900">Bewertungen verwalten</h2>
        <p className="text-gray-600 mt-2">Moderieren Sie Kundenbewertungen</p>
      </div>

      {message && (
        <div className={`mb-6 p-4 rounded-lg ${
          message.includes('erfolgreich') 
            ? 'bg-green-100 text-green-700 border border-green-200' 
            : 'bg-red-100 text-red-700 border border-red-200'
        }`}>
          {message}
        </div>
      )}

      {/* Tab Navigation */}
      <div className="mb-6">
        <nav className="flex space-x-8">
          <button
            onClick={() => setActiveTab('pending')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'pending'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Ausstehend ({pendingReviews.length})
          </button>
          <button
            onClick={() => setActiveTab('approved')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'approved'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Genehmigt ({reviews.length})
          </button>
        </nav>
      </div>

      {/* Reviews Content */}
      <div className="bg-white rounded-lg shadow">
        {activeTab === 'pending' && (
          <div>
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">
                Ausstehende Bewertungen ({pendingReviews.length})
              </h3>
            </div>
            <div className="divide-y divide-gray-200">
              {pendingReviews.length === 0 ? (
                <div className="p-6 text-center text-gray-500">
                  <div className="text-4xl mb-4">✅</div>
                  <p>Keine ausstehenden Bewertungen</p>
                </div>
              ) : (
                pendingReviews.map((review) => (
                  <div key={review.id} className="p-6">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center mb-2">
                          <h4 className="font-medium text-gray-900 mr-3">{review.customer_name}</h4>
                          <div className="flex">
                            {renderStars(review.rating)}
                          </div>
                        </div>
                        <p className="text-gray-700 mb-2">{review.comment}</p>
                        <p className="text-sm text-gray-500">
                          {new Date(review.date).toLocaleDateString('de-DE')} um{' '}
                          {new Date(review.date).toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' })}
                        </p>
                      </div>
                      <div className="flex space-x-2 ml-4">
                        <button
                          onClick={() => approveReview(review.id)}
                          className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700"
                        >
                          Genehmigen
                        </button>
                        <button
                          onClick={() => deleteReview(review.id)}
                          className="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700"
                        >
                          Löschen
                        </button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {activeTab === 'approved' && (
          <div>
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">
                Genehmigte Bewertungen ({reviews.length})
              </h3>
            </div>
            <div className="divide-y divide-gray-200">
              {reviews.length === 0 ? (
                <div className="p-6 text-center text-gray-500">
                  <div className="text-4xl mb-4">⭐</div>
                  <p>Noch keine genehmigten Bewertungen</p>
                </div>
              ) : (
                reviews.map((review) => (
                  <div key={review.id} className="p-6">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center mb-2">
                          <h4 className="font-medium text-gray-900 mr-3">{review.customer_name}</h4>
                          <div className="flex">
                            {renderStars(review.rating)}
                          </div>
                          <span className="ml-2 bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
                            Genehmigt
                          </span>
                        </div>
                        <p className="text-gray-700 mb-2">{review.comment}</p>
                        <div className="text-sm text-gray-500">
                          <p>Eingereicht: {new Date(review.date).toLocaleDateString('de-DE')}</p>
                          {review.approved_at && (
                            <p>Genehmigt: {new Date(review.approved_at).toLocaleDateString('de-DE')} von {review.approved_by}</p>
                          )}
                        </div>
                      </div>
                      <div className="ml-4">
                        <button
                          onClick={() => deleteReview(review.id)}
                          className="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700"
                        >
                          Löschen
                        </button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ReviewsAdminSection;