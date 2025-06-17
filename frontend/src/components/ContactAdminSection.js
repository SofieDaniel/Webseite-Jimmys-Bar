import React, { useState, useEffect } from 'react';

const ContactAdminSection = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  const [filter, setFilter] = useState('all'); // all, unread, read

  useEffect(() => {
    loadMessages();
  }, []);

  const loadMessages = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/contact`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setMessages(data);
      }
    } catch (error) {
      console.error('Error loading contact messages:', error);
      setMessage('Fehler beim Laden der Kontakt-Nachrichten');
    } finally {
      setLoading(false);
    }
  };

  const markAsRead = async (messageId) => {
    try {
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/contact/${messageId}/read`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        setMessage('Nachricht als gelesen markiert!');
        loadMessages();
        setTimeout(() => setMessage(''), 3000);
      } else {
        setMessage('Fehler beim Markieren der Nachricht');
      }
    } catch (error) {
      setMessage('Verbindungsfehler');
    }
  };

  const deleteMessage = async (messageId) => {
    if (!window.confirm('Sind Sie sicher, dass Sie diese Nachricht löschen möchten?')) return;

    try {
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/contact/${messageId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        setMessage('Nachricht erfolgreich gelöscht!');
        loadMessages();
        setTimeout(() => setMessage(''), 3000);
      } else {
        setMessage('Fehler beim Löschen der Nachricht');
      }
    } catch (error) {
      setMessage('Verbindungsfehler');
    }
  };

  const filteredMessages = messages.filter(msg => {
    if (filter === 'unread') return !msg.is_read;
    if (filter === 'read') return msg.is_read;
    return true;
  });

  const unreadCount = messages.filter(msg => !msg.is_read).length;

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
        <h2 className="text-3xl font-bold text-gray-900">Kontakt-Nachrichten</h2>
        <p className="text-gray-600 mt-2">Verwalten Sie eingehende Kontakt-Anfragen</p>
      </div>

      {message && (
        <div className={`mb-6 p-4 rounded-lg ${
          message.includes('erfolgreich') || message.includes('markiert')
            ? 'bg-green-100 text-green-700 border border-green-200' 
            : 'bg-red-100 text-red-700 border border-red-200'
        }`}>
          {message}
        </div>
      )}

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                <span className="text-white text-sm">📧</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Gesamt</p>
              <p className="text-2xl font-semibold text-gray-900">{messages.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center">
                <span className="text-white text-sm">🔴</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Ungelesen</p>
              <p className="text-2xl font-semibold text-gray-900">{unreadCount}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                <span className="text-white text-sm">✅</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Gelesen</p>
              <p className="text-2xl font-semibold text-gray-900">{messages.length - unreadCount}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Filter */}
      <div className="mb-6">
        <div className="flex space-x-4">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg text-sm font-medium ${
              filter === 'all'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Alle Nachrichten
          </button>
          <button
            onClick={() => setFilter('unread')}
            className={`px-4 py-2 rounded-lg text-sm font-medium ${
              filter === 'unread'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Ungelesen ({unreadCount})
          </button>
          <button
            onClick={() => setFilter('read')}
            className={`px-4 py-2 rounded-lg text-sm font-medium ${
              filter === 'read'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Gelesen ({messages.length - unreadCount})
          </button>
        </div>
      </div>

      {/* Messages List */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">
            Nachrichten ({filteredMessages.length})
          </h3>
        </div>
        <div className="divide-y divide-gray-200">
          {filteredMessages.length === 0 ? (
            <div className="p-6 text-center text-gray-500">
              <div className="text-4xl mb-4">📬</div>
              <p>
                {filter === 'unread' && 'Keine ungelesenen Nachrichten'}
                {filter === 'read' && 'Keine gelesenen Nachrichten'}
                {filter === 'all' && 'Noch keine Kontakt-Nachrichten erhalten'}
              </p>
            </div>
          ) : (
            filteredMessages.map((msg) => (
              <div key={msg.id} className={`p-6 ${!msg.is_read ? 'bg-blue-50' : ''}`}>
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center mb-2">
                      <h4 className="font-medium text-gray-900 mr-3">{msg.name}</h4>
                      {!msg.is_read && (
                        <span className="bg-red-100 text-red-800 text-xs px-2 py-1 rounded">
                          Neu
                        </span>
                      )}
                    </div>
                    <div className="text-sm text-gray-600 mb-2">
                      <p><strong>E-Mail:</strong> {msg.email}</p>
                      {msg.phone && <p><strong>Telefon:</strong> {msg.phone}</p>}
                      <p><strong>Betreff:</strong> {msg.subject}</p>
                    </div>
                    <div className="bg-gray-50 p-3 rounded-lg mb-3">
                      <p className="text-gray-700 whitespace-pre-wrap">{msg.message}</p>
                    </div>
                    <p className="text-sm text-gray-500">
                      Empfangen: {new Date(msg.date).toLocaleDateString('de-DE')} um{' '}
                      {new Date(msg.date).toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' })}
                    </p>
                  </div>
                  <div className="flex flex-col space-y-2 ml-4">
                    {!msg.is_read && (
                      <button
                        onClick={() => markAsRead(msg.id)}
                        className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700"
                      >
                        Als gelesen markieren
                      </button>
                    )}
                    <a
                      href={`mailto:${msg.email}?subject=Re: ${msg.subject}`}
                      className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700 text-center"
                    >
                      Antworten
                    </a>
                    <button
                      onClick={() => deleteMessage(msg.id)}
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
    </div>
  );
};

export default ContactAdminSection;