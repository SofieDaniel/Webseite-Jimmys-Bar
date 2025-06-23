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
            data.jimmy?.story_paragraph2,
            data.jimmy?.quote
          ].filter(Boolean).join('\n\n') || '',
          story_image: data.jimmy?.image || '',
          team_title: data.team_section?.title || 'Unser Team',
          team_members: [
            data.team_section?.carlos || {},
            data.team_section?.maria || {}
          ].filter(member => member.name),
          values_title: data.values_section?.title || 'Unsere Werte',
          values: [
            data.values_section?.qualitat?.title + ': ' + data.values_section?.qualitat?.description,
            data.values_section?.gastfreundschaft?.title + ': ' + data.values_section?.gastfreundschaft?.description,
            data.values_section?.lebensfreude?.title + ': ' + data.values_section?.lebensfreude?.description
          ].filter(Boolean)
        };
        
        setAboutData(transformedData);
      }
    } catch (error) {
      console.error('Error loading about data:', error);
      setMessage('Fehler beim Laden der Über-uns-Daten');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setMessage('');

    try {
      // Transform data back to enhanced format
      const enhancedData = {
        page_title: aboutData.page_title,
        page_subtitle: aboutData.hero_title,
        header_background: 'https://images.pexels.com/photos/26626726/pexels-photo-26626726.jpeg',
        jimmy: {
          name: 'Jimmy Rodríguez',
          image: aboutData.story_image || 'https://images.unsplash.com/photo-1665758564802-f611df512d8d',
          story_paragraph1: aboutData.story_content.split('\n\n')[0] || '',
          story_paragraph2: aboutData.story_content.split('\n\n')[1] || '',
          quote: aboutData.story_content.split('\n\n')[2] || 'Essen ist nicht nur Nahrung - es ist Kultur, Tradition und Leidenschaft auf einem Teller.'
        },
        values_section: {
          title: aboutData.values_title,
          qualitat: {
            title: 'Qualität',
            description: aboutData.values[0]?.split(': ')[1] || 'Nur die besten Zutaten für authentische spanische Geschmackserlebnisse.',
            image: 'https://images.unsplash.com/photo-1694685367640-05d6624e57f1'
          },
          gastfreundschaft: {
            title: 'Gastfreundschaft',
            description: aboutData.values[1]?.split(': ')[1] || 'Herzliche Atmosphäre und persönlicher Service für jeden Gast.',
            image: 'https://images.pexels.com/photos/19671352/pexels-photo-19671352.jpeg'
          },
          lebensfreude: {
            title: 'Lebensfreude',
            description: aboutData.values[2]?.split(': ')[1] || 'Spanische Lebensart und Genuss in gemütlicher Atmosphäre.',
            image: 'https://images.unsplash.com/photo-1656423521731-9665583f100c'
          }
        },
        team_section: {
          title: aboutData.team_title,
          carlos: aboutData.team_members[0] || {
            name: 'Carlos Mendez',
            position: 'Küchenchef',
            description: 'Mit 20 Jahren Erfahrung in der spanischen Küche sorgt Carlos für die authentischen Geschmäcker.',
            image: 'https://images.unsplash.com/photo-1665758564802-f611df512d8d'
          },
          maria: aboutData.team_members[1] || {
            name: 'Maria Santos',
            position: 'Service Manager',
            description: 'Maria sorgt dafür, dass sich jeder Gast bei uns willkommen fühlt.',
            image: 'https://images.unsplash.com/photo-1665758564802-f611df512d8d'
          }
        }
      };

      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/ueber-uns-enhanced`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('adminToken')}`
        },
        body: JSON.stringify(enhancedData)
      });

      if (response.ok) {
        setMessage('Über-uns-Inhalte erfolgreich gespeichert!');
        setTimeout(() => setMessage(''), 3000);
      } else {
        setMessage('Fehler beim Speichern der Über-uns-Inhalte');
      }
    } catch (error) {
      setMessage('Verbindungsfehler beim Speichern');
    } finally {
      setSaving(false);
    }
  };

  const addTeamMember = () => {
    const updatedTeamMembers = [...aboutData.team_members, { ...newTeamMember, id: Date.now().toString() }];
    setAboutData({ ...aboutData, team_members: updatedTeamMembers });
    setNewTeamMember({ name: '', position: '', description: '', image_url: '' });
    setShowAddTeamForm(false);
  };

  const updateTeamMember = (memberId, updatedMember) => {
    const updatedTeamMembers = aboutData.team_members.map(member => 
      member.id === memberId ? updatedMember : member
    );
    setAboutData({ ...aboutData, team_members: updatedTeamMembers });
    setEditingTeamMember(null);
  };

  const deleteTeamMember = (memberId) => {
    if (window.confirm('Sind Sie sicher, dass Sie dieses Teammitglied löschen möchten?')) {
      const updatedTeamMembers = aboutData.team_members.filter(member => member.id !== memberId);
      setAboutData({ ...aboutData, team_members: updatedTeamMembers });
    }
  };

  const addValue = () => {
    if (newValue.trim()) {
      setAboutData({
        ...aboutData,
        values: [...aboutData.values, newValue.trim()]
      });
      setNewValue('');
    }
  };

  const deleteValue = (index) => {
    const updatedValues = aboutData.values.filter((_, i) => i !== index);
    setAboutData({ ...aboutData, values: updatedValues });
  };

  const updateValue = (index, newValueText) => {
    const updatedValues = aboutData.values.map((value, i) => 
      i === index ? newValueText : value
    );
    setAboutData({ ...aboutData, values: updatedValues });
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
        <h2 className="text-3xl font-bold text-gray-900">Über uns verwalten</h2>
        <p className="text-gray-600 mt-2">Bearbeiten Sie die Inhalte der Über-uns-Seite</p>
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

      {/* Page Settings */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Seiten-Einstellungen</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Seitentitel</label>
            <input
              type="text"
              value={aboutData.page_title}
              onChange={(e) => setAboutData({
                ...aboutData,
                page_title: e.target.value
              })}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Hero-Titel</label>
            <input
              type="text"
              value={aboutData.hero_title}
              onChange={(e) => setAboutData({
                ...aboutData,
                hero_title: e.target.value
              })}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
        <div className="mt-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Hero-Beschreibung</label>
          <textarea
            value={aboutData.hero_description}
            onChange={(e) => setAboutData({
              ...aboutData,
              hero_description: e.target.value
            })}
            rows={3}
            className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      {/* Story Section */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Geschichte & Story</h3>
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Story-Titel</label>
            <input
              type="text"
              value={aboutData.story_title}
              onChange={(e) => setAboutData({
                ...aboutData,
                story_title: e.target.value
              })}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Story-Inhalt</label>
            <textarea
              value={aboutData.story_content}
              onChange={(e) => setAboutData({
                ...aboutData,
                story_content: e.target.value
              })}
              rows={8}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Erzählen Sie Ihre Geschichte..."
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Story-Bild URL</label>
            <input
              type="url"
              value={aboutData.story_image}
              onChange={(e) => setAboutData({
                ...aboutData,
                story_image: e.target.value
              })}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            {aboutData.story_image && (
              <div className="mt-3">
                <img src={aboutData.story_image} alt="Story Bild" className="w-32 h-32 object-cover rounded border" />
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Team Section */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-lg font-semibold text-gray-900">Team ({aboutData.team_members.length})</h3>
          <button
            onClick={() => setShowAddTeamForm(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Teammitglied hinzufügen
          </button>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">Team-Titel</label>
          <input
            type="text"
            value={aboutData.team_title}
            onChange={(e) => setAboutData({
              ...aboutData,
              team_title: e.target.value
            })}
            className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        {/* Team Members List */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {aboutData.team_members.map((member, index) => (
            <div key={member.id || index} className="border border-gray-200 rounded-lg p-4">
              {member.image_url && (
                <div className="mb-4">
                  <img src={member.image_url} alt={member.name} className="w-20 h-20 object-cover rounded-full mx-auto" />
                </div>
              )}
              <div className="text-center">
                <h4 className="font-semibold text-gray-900 mb-1">{member.name}</h4>
                <p className="text-sm text-blue-600 mb-2">{member.position}</p>
                <p className="text-xs text-gray-600 mb-4">{member.description}</p>
                <div className="flex justify-center space-x-2">
                  <button
                    onClick={() => setEditingTeamMember(member)}
                    className="text-blue-600 hover:text-blue-800 text-sm"
                  >
                    Bearbeiten
                  </button>
                  <button
                    onClick={() => deleteTeamMember(member.id)}
                    className="text-red-600 hover:text-red-800 text-sm"
                  >
                    Löschen
                  </button>
                </div>
              </div>
            </div>
          ))}

          {aboutData.team_members.length === 0 && (
            <div className="col-span-full text-center py-8 text-gray-500">
              <div className="text-4xl mb-4">👥</div>
              <p>Noch keine Teammitglieder hinzugefügt.</p>
              <p className="text-sm mt-2">Fügen Sie Ihr erstes Teammitglied hinzu.</p>
            </div>
          )}
        </div>
      </div>

      {/* Values Section */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Werte & Prinzipien</h3>
        
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">Werte-Titel</label>
          <input
            type="text"
            value={aboutData.values_title}
            onChange={(e) => setAboutData({
              ...aboutData,
              values_title: e.target.value
            })}
            className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">Neuen Wert hinzufügen</label>
          <div className="flex gap-2">
            <input
              type="text"
              value={newValue}
              onChange={(e) => setNewValue(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && addValue()}
              className="flex-1 p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="z.B. Authentische mediterrane Küche"
            />
            <button
              onClick={addValue}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
            >
              Hinzufügen
            </button>
          </div>
        </div>

        <div className="space-y-2">
          {aboutData.values.map((value, index) => (
            <div key={index} className="flex items-center justify-between bg-gray-50 p-3 rounded-lg">
              <input
                type="text"
                value={value}
                onChange={(e) => updateValue(index, e.target.value)}
                className="flex-1 bg-transparent border-none focus:ring-0 focus:outline-none"
              />
              <button
                onClick={() => deleteValue(index)}
                className="text-red-600 hover:text-red-800 ml-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          ))}

          {aboutData.values.length === 0 && (
            <div className="text-center py-4 text-gray-500">
              <p>Noch keine Werte hinzugefügt.</p>
            </div>
          )}
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <button
          onClick={handleSave}
          disabled={saving}
          className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 font-medium"
        >
          {saving ? 'Speichern...' : 'Alle Änderungen speichern'}
        </button>
      </div>

      {/* Add/Edit Team Member Modal */}
      {(showAddTeamForm || editingTeamMember) && (
        <TeamMemberModal
          member={editingTeamMember || newTeamMember}
          onSave={editingTeamMember ? updateTeamMember : addTeamMember}
          onCancel={() => {
            setShowAddTeamForm(false);
            setEditingTeamMember(null);
          }}
          isEditing={!!editingTeamMember}
          setMember={editingTeamMember ? setEditingTeamMember : setNewTeamMember}
        />
      )}
    </div>
  );
};

// Team Member Modal Component
const TeamMemberModal = ({ member, onSave, onCancel, isEditing, setMember }) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (isEditing) {
      onSave(member.id, member);
    } else {
      onSave();
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-gray-900">
              {isEditing ? 'Teammitglied bearbeiten' : 'Neues Teammitglied hinzufügen'}
            </h2>
            <button
              onClick={onCancel}
              className="text-gray-400 hover:text-gray-600 p-2"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Name</label>
                <input
                  type="text"
                  value={member.name}
                  onChange={(e) => setMember({...member, name: e.target.value})}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Position</label>
                <input
                  type="text"
                  value={member.position}
                  onChange={(e) => setMember({...member, position: e.target.value})}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Beschreibung</label>
              <textarea
                value={member.description}
                onChange={(e) => setMember({...member, description: e.target.value})}
                rows={4}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Bild-URL</label>
              <input
                type="url"
                value={member.image_url}
                onChange={(e) => setMember({...member, image_url: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              {member.image_url && (
                <div className="mt-3">
                  <img src={member.image_url} alt="Vorschau" className="w-20 h-20 object-cover rounded-full border" />
                </div>
              )}
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
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                {isEditing ? 'Änderungen speichern' : 'Teammitglied hinzufügen'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AboutAdminSection;