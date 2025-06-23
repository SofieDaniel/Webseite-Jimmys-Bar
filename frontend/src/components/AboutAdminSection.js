import React, { useState, useEffect } from 'react';

const AboutAdminSection = () => {
  const [aboutData, setAboutData] = useState({
    page_title: 'Über uns',
    page_subtitle: 'Die Geschichte hinter Jimmy\'s Tapas Bar',
    header_background: 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f',
    jimmy_data: {
      name: 'Jimmy Rodríguez',
      title: 'Inhaber & Küchenchef',
      story1: 'Seit über 15 Jahren bringe ich die authentischen Aromen Spaniens an die deutsche Ostseeküste. Meine Leidenschaft für die spanische Küche begann in den kleinen Tapas-Bars von Sevilla, wo ich die Geheimnisse traditioneller Rezepte erlernte.',
      story2: 'In Jimmy\'s Tapas Bar verwenden wir nur die besten Zutaten - von handverlesenem Olivenöl aus Andalusien bis hin zu frischen Meeresfrüchten aus der Ostsee. Jedes Gericht wird mit Liebe und Respekt vor der spanischen Tradition zubereitet.',
      image: 'https://images.unsplash.com/photo-1544025162-d76694265947'
    },
    leidenschaft_data: {
      title: 'Unsere Leidenschaft',
      subtitle: 'Entdecken Sie die Leidenschaft hinter Jimmy\'s Tapas Bar',
      intro: 'Seit der Gründung steht Jimmy\'s Tapas Bar für authentische mediterrane Küche an der deutschen Ostseeküste.',
      text1: 'Unsere Leidenschaft gilt den traditionellen Rezepten und frischen Zutaten, die wir täglich mit Liebe zubereiten.',
      text2: 'Von den ersten kleinen Tapas bis hin zu unseren berühmten Paellas - jedes Gericht erzählt eine Geschichte',
      text3: 'von Tradition und Qualität.',
      text4: 'An beiden Standorten erleben Sie die entspannte Atmosphäre des Mittelmeers,',
      text5: 'während Sie den Blick auf die Ostsee genießen können.'
    }
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    loadAboutData();
  }, []);

  const loadAboutData = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/ueber-uns-enhanced`);
      if (response.ok) {
        const data = await response.json();
        console.log('Loaded about data:', data);
        setAboutData(data);
      } else {
        console.error('Failed to load about data:', response.status);
        setMessage('Fehler beim Laden der Über uns-Daten');
      }
    } catch (error) {
      console.error('Error loading about data:', error);
      setMessage('Fehler beim Laden der Über uns-Daten');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setMessage('');

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/ueber-uns-enhanced`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('adminToken')}`
        },
        body: JSON.stringify(aboutData)
      });

      if (response.ok) {
        setMessage('Über uns-Inhalte erfolgreich gespeichert!');
        setTimeout(() => setMessage(''), 3000);
      } else {
        setMessage('Fehler beim Speichern der Über uns-Inhalte');
      }
    } catch (error) {
      setMessage('Verbindungsfehler beim Speichern');
    } finally {
      setSaving(false);
    }
  };

  const updateJimmyData = (field, value) => {
    setAboutData(prev => ({
      ...prev,
      jimmy_data: { ...prev.jimmy_data, [field]: value }
    }));
  };

  const updateLeidenschaftData = (field, value) => {
    setAboutData(prev => ({
      ...prev,
      leidenschaft_data: { ...prev.leidenschaft_data, [field]: value }
    }));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-32">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6 bg-white">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">📖 Über uns verwalten</h1>
          <p className="text-gray-600">Bearbeiten Sie die Inhalte der "Über uns" Seite</p>
          <code className="text-sm text-gray-600">GET/PUT /api/cms/ueber-uns-enhanced</code>
        </div>
        <button
          onClick={handleSave}
          disabled={saving}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
        >
          {saving ? 'Speichert...' : 'Änderungen speichern'}
        </button>
      </div>

      {/* Success/Error Message */}
      {message && (
        <div className={`mb-6 p-4 rounded-lg ${
          message.includes('erfolgreich') 
            ? 'bg-green-50 border border-green-200 text-green-700' 
            : 'bg-red-50 border border-red-200 text-red-700'
        }`}>
          {message}
        </div>
      )}

      {/* Page Header Settings */}
      <div className="bg-gray-50 rounded-lg p-6 mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">🎯 Seiten-Header</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Seitentitel</label>
            <input
              type="text"
              value={aboutData.page_title}
              onChange={(e) => setAboutData({...aboutData, page_title: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Untertitel</label>
            <input
              type="text"
              value={aboutData.page_subtitle}
              onChange={(e) => setAboutData({...aboutData, page_subtitle: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900"
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">Header-Hintergrundbild URL</label>
            <input
              type="url"
              value={aboutData.header_background}
              onChange={(e) => setAboutData({...aboutData, header_background: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900"
            />
          </div>
        </div>
      </div>

      {/* Jimmy Rodríguez Section */}
      <div className="bg-gray-50 rounded-lg p-6 mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">👨‍🍳 Jimmy Rodríguez Sektion</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Name</label>
            <input
              type="text"
              value={aboutData.jimmy_data.name}
              onChange={(e) => updateJimmyData('name', e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Titel/Position</label>
            <input
              type="text"
              value={aboutData.jimmy_data.title}
              onChange={(e) => updateJimmyData('title', e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900"
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">Bild URL</label>
            <input
              type="url"
              value={aboutData.jimmy_data.image}
              onChange={(e) => updateJimmyData('image', e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900"
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">Geschichte - Absatz 1</label>
            <textarea
              value={aboutData.jimmy_data.story1}
              onChange={(e) => updateJimmyData('story1', e.target.value)}
              rows={4}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900"
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">Geschichte - Absatz 2</label>
            <textarea
              value={aboutData.jimmy_data.story2}
              onChange={(e) => updateJimmyData('story2', e.target.value)}
              rows={4}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900"
            />
          </div>
        </div>
      </div>

      {/* Leidenschaft Section */}
      <div className="bg-gray-50 rounded-lg p-6 mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">🔥 Unsere Leidenschaft Sektion</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Titel</label>
            <input
              type="text"
              value={aboutData.leidenschaft_data.title}
              onChange={(e) => updateLeidenschaftData('title', e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Untertitel</label>
            <input
              type="text"
              value={aboutData.leidenschaft_data.subtitle}
              onChange={(e) => updateLeidenschaftData('subtitle', e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900"
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">Einführungstext</label>
            <textarea
              value={aboutData.leidenschaft_data.intro}
              onChange={(e) => updateLeidenschaftData('intro', e.target.value)}
              rows={2}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Text 1</label>
            <textarea
              value={aboutData.leidenschaft_data.text1}
              onChange={(e) => updateLeidenschaftData('text1', e.target.value)}
              rows={3}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Text 2</label>
            <textarea
              value={aboutData.leidenschaft_data.text2}
              onChange={(e) => updateLeidenschaftData('text2', e.target.value)}
              rows={3}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Text 3</label>
            <textarea
              value={aboutData.leidenschaft_data.text3}
              onChange={(e) => updateLeidenschaftData('text3', e.target.value)}
              rows={3}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Text 4</label>
            <textarea
              value={aboutData.leidenschaft_data.text4}
              onChange={(e) => updateLeidenschaftData('text4', e.target.value)}
              rows={3}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Text 5</label>
            <textarea
              value={aboutData.leidenschaft_data.text5}
              onChange={(e) => updateLeidenschaftData('text5', e.target.value)}
              rows={3}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900"
            />
        </div>
    </div>
  );
};

export default AboutAdminSection;
