import React, { useState, useEffect } from 'react';

// Reviews Management Section
export const ReviewsSection = ({ user, token, apiCall }) => {
  const [pendingReviews, setPendingReviews] = useState([]);
  const [approvedReviews, setApprovedReviews] = useState([]);
  const [activeTab, setActiveTab] = useState('pending');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadReviews();
  }, [activeTab]);

  const loadReviews = async () => {
    try {
      setLoading(true);
      if (activeTab === 'pending') {
        const response = await apiCall('/admin/reviews/pending');
        if (response.ok) {
          const data = await response.json();
          setPendingReviews(data);
        }
      } else {
        const response = await apiCall('/reviews');
        if (response.ok) {
          const data = await response.json();
          setApprovedReviews(data);
        }
      }
    } catch (error) {
      console.error('Error loading reviews:', error);
    } finally {
      setLoading(false);
    }
  };

  const approveReview = async (reviewId) => {
    try {
      const response = await apiCall(`/reviews/${reviewId}/approve`, 'PUT');
      if (response.ok) {
        loadReviews();
      }
    } catch (error) {
      console.error('Error approving review:', error);
    }
  };

  const renderStars = (rating) => {
    return Array.from({ length: 5 }, (_, i) => (
      <svg
        key={i}
        className={`w-5 h-5 ${i < rating ? 'text-yellow-400' : 'text-gray-300'}`}
        fill="currentColor"
        viewBox="0 0 20 20"
      >
        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
      </svg>
    ));
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Bewertungen verwalten</h1>
        <p className="text-gray-600">Kundenbewertungen moderieren und freigeben</p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('pending')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'pending'
                ? 'border-yellow-500 text-yellow-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            Wartende Bewertungen ({pendingReviews.length})
          </button>
          <button
            onClick={() => setActiveTab('approved')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'approved'
                ? 'border-green-500 text-green-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            Freigegebene Bewertungen
          </button>
        </nav>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-32">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        </div>
      ) : (
        <div className="space-y-4">
          {activeTab === 'pending' && (
            <>
              {pendingReviews.length === 0 ? (
                <div className="text-center py-12">
                  <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <h3 className="mt-2 text-sm font-medium text-gray-900">Keine wartenden Bewertungen</h3>
                  <p className="mt-1 text-sm text-gray-500">Alle Bewertungen wurden bereits bearbeitet.</p>
                </div>
              ) : (
                pendingReviews.map((review) => (
                  <div key={review.id} className="bg-white border border-gray-200 rounded-lg p-6">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center mb-3">
                          <h3 className="text-lg font-medium text-gray-900 mr-4">{review.customer_name}</h3>
                          <div className="flex">{renderStars(review.rating)}</div>
                          <span className="ml-2 text-sm text-gray-600">({review.rating}/5)</span>
                        </div>
                        <p className="text-gray-700 mb-3">{review.comment}</p>
                        <p className="text-sm text-gray-500">
                          Eingereicht am: {new Date(review.date).toLocaleDateString('de-DE')}
                        </p>
                      </div>
                      <button
                        onClick={() => approveReview(review.id)}
                        className="ml-4 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center"
                      >
                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        Freigeben
                      </button>
                    </div>
                  </div>
                ))
              )}
            </>
          )}

          {activeTab === 'approved' && (
            <>
              {approvedReviews.length === 0 ? (
                <div className="text-center py-12">
                  <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                  </svg>
                  <h3 className="mt-2 text-sm font-medium text-gray-900">Keine freigegebenen Bewertungen</h3>
                  <p className="mt-1 text-sm text-gray-500">Noch keine Bewertungen wurden freigegeben.</p>
                </div>
              ) : (
                approvedReviews.map((review) => (
                  <div key={review.id} className="bg-white border border-gray-200 rounded-lg p-6">
                    <div className="flex items-center mb-3">
                      <h3 className="text-lg font-medium text-gray-900 mr-4">{review.customer_name}</h3>
                      <div className="flex">{renderStars(review.rating)}</div>
                      <span className="ml-2 text-sm text-gray-600">({review.rating}/5)</span>
                      <span className="ml-auto text-sm text-green-600 bg-green-100 px-2 py-1 rounded-full">
                        Freigegeben
                      </span>
                    </div>
                    <p className="text-gray-700 mb-3">{review.comment}</p>
                    <div className="flex justify-between text-sm text-gray-500">
                      <span>Eingereicht: {new Date(review.date).toLocaleDateString('de-DE')}</span>
                      {review.approved_at && (
                        <span>Freigegeben: {new Date(review.approved_at).toLocaleDateString('de-DE')} von {review.approved_by}</span>
                      )}
                    </div>
                  </div>
                ))
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
};

// Contacts Management Section
export const ContactsSection = ({ user, token, apiCall }) => {
  const [contacts, setContacts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedContact, setSelectedContact] = useState(null);

  useEffect(() => {
    loadContacts();
  }, []);

  const loadContacts = async () => {
    try {
      setLoading(true);
      const response = await apiCall('/admin/contact');
      if (response.ok) {
        const data = await response.json();
        setContacts(data);
      }
    } catch (error) {
      console.error('Error loading contacts:', error);
    } finally {
      setLoading(false);
    }
  };

  const markAsRead = async (contactId) => {
    try {
      const response = await apiCall(`/admin/contact/${contactId}/read`, 'PUT');
      if (response.ok) {
        loadContacts();
      }
    } catch (error) {
      console.error('Error marking as read:', error);
    }
  };

  const unreadCount = contacts.filter(c => !c.is_read).length;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Kontakt-Nachrichten</h1>
          <p className="text-gray-600">
            Kundennachrichten verwalten ({unreadCount} ungelesen)
          </p>
        </div>
        <div className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
          {contacts.length} Nachrichten gesamt
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-32">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        </div>
      ) : (
        <div className="space-y-4">
          {contacts.length === 0 ? (
            <div className="text-center py-12">
              <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 7.89a2 2 0 002.83 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <h3 className="mt-2 text-sm font-medium text-gray-900">Keine Nachrichten</h3>
              <p className="mt-1 text-sm text-gray-500">Es sind noch keine Kontaktanfragen eingegangen.</p>
            </div>
          ) : (
            contacts.map((contact) => (
              <div
                key={contact.id}
                className={`bg-white border rounded-lg p-6 cursor-pointer hover:shadow-md transition-shadow ${
                  !contact.is_read ? 'border-blue-200 bg-blue-50' : 'border-gray-200'
                }`}
                onClick={() => setSelectedContact(contact)}
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center mb-2">
                      <h3 className="text-lg font-medium text-gray-900 mr-3">{contact.name}</h3>
                      {!contact.is_read && (
                        <span className="bg-blue-600 text-white text-xs px-2 py-1 rounded-full">
                          Neu
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-600 mb-1">
                      <span className="font-medium">Betreff:</span> {contact.subject}
                    </p>
                    <p className="text-sm text-gray-600 mb-2">
                      <span className="font-medium">E-Mail:</span> {contact.email}
                      {contact.phone && (
                        <span className="ml-4">
                          <span className="font-medium">Telefon:</span> {contact.phone}
                        </span>
                      )}
                    </p>
                    <p className="text-gray-700 line-clamp-2">{contact.message}</p>
                  </div>
                  <div className="text-right text-sm text-gray-500 ml-4">
                    <p>{new Date(contact.date).toLocaleDateString('de-DE')}</p>
                    <p>{new Date(contact.date).toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' })}</p>
                    {!contact.is_read && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          markAsRead(contact.id);
                        }}
                        className="mt-2 text-blue-600 hover:text-blue-800 text-xs underline"
                      >
                        Als gelesen markieren
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* Contact Detail Modal */}
      {selectedContact && (
        <ContactDetailModal
          contact={selectedContact}
          onClose={() => setSelectedContact(null)}
          onMarkRead={markAsRead}
        />
      )}
    </div>
  );
};

// Contact Detail Modal
const ContactDetailModal = ({ contact, onClose, onMarkRead }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-gray-900">Kontakt-Nachricht</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 p-2"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                <p className="text-gray-900">{contact.name}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">E-Mail</label>
                <p className="text-gray-900">
                  <a href={`mailto:${contact.email}`} className="text-blue-600 hover:underline">
                    {contact.email}
                  </a>
                </p>
              </div>
              {contact.phone && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Telefon</label>
                  <p className="text-gray-900">
                    <a href={`tel:${contact.phone}`} className="text-blue-600 hover:underline">
                      {contact.phone}
                    </a>
                  </p>
                </div>
              )}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Datum</label>
                <p className="text-gray-900">
                  {new Date(contact.date).toLocaleDateString('de-DE')} um{' '}
                  {new Date(contact.date).toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' })}
                </p>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Betreff</label>
              <p className="text-gray-900 font-medium">{contact.subject}</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Nachricht</label>
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-gray-900 whitespace-pre-wrap">{contact.message}</p>
              </div>
            </div>

            <div className="flex justify-between items-center pt-4 border-t border-gray-200">
              <div className="flex items-center">
                {!contact.is_read ? (
                  <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                    Ungelesen
                  </span>
                ) : (
                  <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                    Gelesen
                  </span>
                )}
              </div>
              <div className="space-x-3">
                {!contact.is_read && (
                  <button
                    onClick={() => {
                      onMarkRead(contact.id);
                      onClose();
                    }}
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
                  >
                    Als gelesen markieren
                  </button>
                )}
                <button
                  onClick={onClose}
                  className="bg-gray-200 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-300"
                >
                  Schließen
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Users Management Section
export const UsersSection = ({ user, token, apiCall }) => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [saving, setSaving] = useState(false);
  const [newUser, setNewUser] = useState({
    username: '',
    email: '',
    password: '',
    role: 'viewer'
  });

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      const response = await apiCall('/users');
      if (response.ok) {
        const data = await response.json();
        setUsers(data);
      }
    } catch (error) {
      console.error('Error loading users:', error);
    } finally {
      setLoading(false);
    }
  };

  const createUser = async (userData) => {
    try {
      setSaving(true);
      const response = await apiCall('/users', 'POST', userData);
      if (response.ok) {
        loadUsers();
        setShowAddForm(false);
        setNewUser({ username: '', email: '', password: '', role: 'viewer' });
      }
    } catch (error) {
      console.error('Error creating user:', error);
    } finally {
      setSaving(false);
    }
  };

  const deleteUser = async (userId) => {
    if (window.confirm('Sind Sie sicher, dass Sie diesen Benutzer löschen möchten?')) {
      try {
        const response = await apiCall(`/users/${userId}`, 'DELETE');
        if (response.ok) {
          loadUsers();
        }
      } catch (error) {
        console.error('Error deleting user:', error);
      }
    }
  };

  const roleNames = {
    admin: 'Administrator',
    editor: 'Redakteur',
    viewer: 'Betrachter'
  };

  const roleColors = {
    admin: 'bg-red-100 text-red-800',
    editor: 'bg-blue-100 text-blue-800',
    viewer: 'bg-gray-100 text-gray-800'
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Benutzer verwalten</h1>
          <p className="text-gray-600">System-Benutzer und deren Rechte verwalten</p>
        </div>
        {user?.role === 'admin' && (
          <button
            onClick={() => setShowAddForm(true)}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 flex items-center"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Neuer Benutzer
          </button>
        )}
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-32">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        </div>
      ) : (
        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Benutzer
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Rolle
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Erstellt
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Letzter Login
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Aktionen
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {users.map((userItem) => (
                <tr key={userItem.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 h-10 w-10">
                        <div className="h-10 w-10 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center">
                          <span className="text-white font-medium text-sm">
                            {userItem.username.charAt(0).toUpperCase()}
                          </span>
                        </div>
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">{userItem.username}</div>
                        <div className="text-sm text-gray-500">{userItem.email}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${roleColors[userItem.role]}`}>
                      {roleNames[userItem.role]}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(userItem.created_at).toLocaleDateString('de-DE')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {userItem.last_login ? new Date(userItem.last_login).toLocaleDateString('de-DE') : 'Nie'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    {user?.role === 'admin' && userItem.id !== user.id && (
                      <button
                        onClick={() => deleteUser(userItem.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Löschen
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Add User Modal */}
      {showAddForm && (
        <UserModal
          user={newUser}
          onSave={createUser}
          onCancel={() => setShowAddForm(false)}
          saving={saving}
          roleNames={roleNames}
        />
      )}
    </div>
  );
};

// User Modal Component
const UserModal = ({ user: userData, onSave, onCancel, saving, roleNames }) => {
  const [formData, setFormData] = useState(userData);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-md w-full">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-gray-900">Neuen Benutzer erstellen</h2>
            <button onClick={onCancel} className="text-gray-400 hover:text-gray-600 p-2">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Benutzername</label>
              <input
                type="text"
                value={formData.username}
                onChange={(e) => setFormData({...formData, username: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">E-Mail</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Passwort</label>
              <input
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Rolle</label>
              <select
                value={formData.role}
                onChange={(e) => setFormData({...formData, role: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {Object.entries(roleNames).map(([key, name]) => (
                  <option key={key} value={key}>{name}</option>
                ))}
              </select>
            </div>

            <div className="flex justify-end space-x-4 pt-6 border-t border-gray-200">
              <button
                type="button"
                onClick={onCancel}
                className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
              >
                Abbrechen
              </button>
              <button
                type="submit"
                disabled={saving}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                {saving ? 'Erstellen...' : 'Erstellen'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};