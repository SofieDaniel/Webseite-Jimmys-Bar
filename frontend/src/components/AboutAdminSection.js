import React, { useState } from 'react';

const AboutAdminSection = () => {
  const [aboutData, setAboutData] = useState({
    // Jimmy Rodríguez Sektion
    jimmy: {
      name: 'Jimmy Rodríguez',
      title: 'Inhaber & Küchenchef',
      story1: 'Seit über 15 Jahren bringe ich die authentischen Aromen Spaniens an die deutsche Ostseeküste. Meine Leidenschaft für die spanische Küche begann in den kleinen Tapas-Bars von Sevilla, wo ich die Geheimnisse traditioneller Rezepte erlernte.',
      story2: 'In Jimmy\'s Tapas Bar verwenden wir nur die besten Zutaten - von handverlesenem Olivenöl aus Andalusien bis hin zu frischen Meeresfrüchten aus der Ostsee. Jedes Gericht wird mit Liebe und Respekt vor der spanischen Tradition zubereitet.',
      image: 'https://images.unsplash.com/photo-1544025162-d76694265947'
    },
    // Unsere Leidenschaft Sektion
    leidenschaft: {
      title: 'Unsere Leidenschaft',
      subtitle: 'Entdecken Sie die Leidenschaft hinter Jimmy\'s Tapas Bar',
      intro: 'Seit der Gründung steht Jimmy\'s Tapas Bar für authentische mediterrane Küche an der deutschen Ostseeküste.',
      text1: 'Unsere Leidenschaft gilt den traditionellen Rezepten und frischen Zutaten, die wir täglich mit Liebe zubereiten.',
      text2: 'Von den ersten kleinen Tapas bis hin zu unseren berühmten Paellas - jedes Gericht erzählt eine Geschichte',
      text3: 'von Tradition und Qualität.',
      text4: 'An beiden Standorten erleben Sie die entspannte Atmosphäre des Mittelmeers,',
      text5: 'während Sie den Blick auf die Ostsee genießen können.'
    },
    // Team Sektion
    team: [
      {
        name: 'Maria Gonzalez',
        position: 'Sous Chef',
        description: 'Expertin für Meeresfrüchte und Paella, sorgt für die perfekte Zubereitung unserer Spezialitäten.',
        image: 'https://images.unsplash.com/photo-1494790108755-2616c39ca7c0'
      },
      {
        name: 'Carlos Mendez',
        position: 'Barkeeper',
        description: 'Meister der spanischen Cocktails und Sangria, zaubert die perfekte Begleitung zu unseren Tapas.',
        image: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e'
      },
      {
        name: 'Isabella Schmidt',
        position: 'Service Manager',
        description: 'Sorgt für perfekten Service und spanische Gastfreundschaft, damit sich jeder Gast willkommen fühlt.',
        image: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80'
      }
    ]
  });

  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');
  const [editingTeam, setEditingTeam] = useState(null);

  const updateJimmy = (field, value) => {
    setAboutData(prev => ({
      ...prev,
      jimmy: { ...prev.jimmy, [field]: value }
    }));
  };

  const updateLeidenschaft = (field, value) => {
    setAboutData(prev => ({
      ...prev,
      leidenschaft: { ...prev.leidenschaft, [field]: value }
    }));
  };

  const updateTeamMember = (index, field, value) => {
    setAboutData(prev => ({
      ...prev,
      team: prev.team.map((member, i) => 
        i === index ? { ...member, [field]: value } : member
      )
    }));
  };

  const saveChanges = async () => {
    setSaving(true);
    setMessage('');
    
    try {
      // For now, simulate save (since the actual API needs to be implemented)
      await new Promise(resolve => setTimeout(resolve, 1000));
      setMessage('Über uns-Inhalte erfolgreich gespeichert!');
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage('Fehler beim Speichern: ' + error.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6 bg-white">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">📖 Über uns verwalten</h1>
          <p className="text-gray-600">Bearbeiten Sie die Inhalte der "Über uns" Seite</p>
        </div>
        <button
          onClick={saveChanges}
          disabled={saving}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors disabled:opacity-50"
        >
          {saving ? 'Speichern...' : 'Änderungen speichern'}
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

      {/* Jimmy Rodríguez Sektion */}
      <div className="bg-gray-50 rounded-lg p-6 mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-6">👨‍🍳 Jimmy Rodríguez Sektion</h2>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Name</label>
            <input
              type="text"
              value={aboutData.jimmy.name}
              onChange={(e) => updateJimmy('name', e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Titel</label>
            <input
              type="text"
              value={aboutData.jimmy.title}
              onChange={(e) => updateJimmy('title', e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          <div className="lg:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">Bild-URL</label>
            <input
              type="url"
              value={aboutData.jimmy.image}
              onChange={(e) => updateJimmy('image', e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          <div className="lg:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">Geschichte - Teil 1</label>
            <textarea
              value={aboutData.jimmy.story1}
              onChange={(e) => updateJimmy('story1', e.target.value)}
              rows={3}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          <div className="lg:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">Geschichte - Teil 2</label>
            <textarea
              value={aboutData.jimmy.story2}
              onChange={(e) => updateJimmy('story2', e.target.value)}
              rows={3}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>
      </div>

      {/* Leidenschaft Sektion */}
      <div className="bg-gray-50 rounded-lg p-6 mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-6">❤️ Unsere Leidenschaft Sektion</h2>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Titel</label>
            <input
              type="text"
              value={aboutData.leidenschaft.title}
              onChange={(e) => updateLeidenschaft('title', e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Untertitel</label>
            <input
              type="text"
              value={aboutData.leidenschaft.subtitle}
              onChange={(e) => updateLeidenschaft('subtitle', e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Intro-Text</label>
              <textarea
                value={aboutData.leidenschaft.intro}
                onChange={(e) => updateLeidenschaft('intro', e.target.value)}
                rows={2}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Text 1</label>
              <textarea
                value={aboutData.leidenschaft.text1}
                onChange={(e) => updateLeidenschaft('text1', e.target.value)}
                rows={2}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Text 2</label>
              <textarea
                value={aboutData.leidenschaft.text2}
                onChange={(e) => updateLeidenschaft('text2', e.target.value)}
                rows={2}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Text 3</label>
              <textarea
                value={aboutData.leidenschaft.text3}
                onChange={(e) => updateLeidenschaft('text3', e.target.value)}
                rows={2}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Text 4</label>
              <textarea
                value={aboutData.leidenschaft.text4}
                onChange={(e) => updateLeidenschaft('text4', e.target.value)}
                rows={2}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Text 5</label>
              <textarea
                value={aboutData.leidenschaft.text5}
                onChange={(e) => updateLeidenschaft('text5', e.target.value)}
                rows={2}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Team Sektion */}
      <div className="bg-gray-50 rounded-lg p-6">
        <h2 className="text-2xl font-semibold text-gray-900 mb-6">👥 Team Sektion</h2>
        
        <div className="space-y-6">
          {aboutData.team.map((member, index) => (
            <div key={index} className="bg-white rounded-lg p-6 border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Team-Mitglied {index + 1}</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Name</label>
                  <input
                    type="text"
                    value={member.name}
                    onChange={(e) => updateTeamMember(index, 'name', e.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Position</label>
                  <input
                    type="text"
                    value={member.position}
                    onChange={(e) => updateTeamMember(index, 'position', e.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Bild-URL</label>
                  <input
                    type="url"
                    value={member.image}
                    onChange={(e) => updateTeamMember(index, 'image', e.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Beschreibung</label>
                  <textarea
                    value={member.description}
                    onChange={(e) => updateTeamMember(index, 'description', e.target.value)}
                    rows={3}
                    className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AboutAdminSection;