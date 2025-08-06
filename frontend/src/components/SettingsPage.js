import React, { useState } from 'react';

const SettingsPage = ({ user }) => {
  const [settings, setSettings] = useState({
    notifications: {
      email: true,
      push: true,
      sms: false,
      chargingComplete: true,
      lowBattery: true,
      newStations: false,
      promotions: false
    },
    privacy: {
      shareLocation: true,
      shareChargingHistory: false,
      showOnMap: true,
      allowAnalytics: true
    },
    preferences: {
      defaultEnergyType: 'Level 2',
      autoStartCharging: false,
      ecoMode: true,
      darkMode: false,
      language: 'English',
      timezone: 'America/Los_Angeles'
    },
    account: {
      email: user.email,
      phone: '+1 (555) 123-4567',
      password: '••••••••',
      twoFactorAuth: false
    }
  });

  const [activeTab, setActiveTab] = useState('notifications');

  const handleSettingChange = (category, setting, value) => {
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [setting]: value
      }
    }));
  };

  const handleSaveSettings = () => {
    // Here you would typically save to backend
    alert('Settings saved successfully!');
  };

  const renderNotificationsTab = () => (
    <div>
      <h3 style={{ marginBottom: '1.5rem', color: '#28a745' }}>Notification Settings</h3>
      
      <div style={{ marginBottom: '2rem' }}>
        <h4 style={{ marginBottom: '1rem' }}>Notification Channels</h4>
        <div style={{ display: 'grid', gap: '1rem' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input 
              type="checkbox" 
              checked={settings.notifications.email}
              onChange={(e) => handleSettingChange('notifications', 'email', e.target.checked)}
            />
            Email Notifications
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input 
              type="checkbox" 
              checked={settings.notifications.push}
              onChange={(e) => handleSettingChange('notifications', 'push', e.target.checked)}
            />
            Push Notifications
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input 
              type="checkbox" 
              checked={settings.notifications.sms}
              onChange={(e) => handleSettingChange('notifications', 'sms', e.target.checked)}
            />
            SMS Notifications
          </label>
        </div>
      </div>

      <div style={{ marginBottom: '2rem' }}>
        <h4 style={{ marginBottom: '1rem' }}>Notification Types</h4>
        <div style={{ display: 'grid', gap: '1rem' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input 
              type="checkbox" 
              checked={settings.notifications.chargingComplete}
              onChange={(e) => handleSettingChange('notifications', 'chargingComplete', e.target.checked)}
            />
            Charging Session Complete
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input 
              type="checkbox" 
              checked={settings.notifications.lowBattery}
              onChange={(e) => handleSettingChange('notifications', 'lowBattery', e.target.checked)}
            />
            Low Battery Alert
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input 
              type="checkbox" 
              checked={settings.notifications.newStations}
              onChange={(e) => handleSettingChange('notifications', 'newStations', e.target.checked)}
            />
            New Stations Nearby
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input 
              type="checkbox" 
              checked={settings.notifications.promotions}
              onChange={(e) => handleSettingChange('notifications', 'promotions', e.target.checked)}
            />
            Promotional Offers
          </label>
        </div>
      </div>
    </div>
  );

  const renderPrivacyTab = () => (
    <div>
      <h3 style={{ marginBottom: '1.5rem', color: '#28a745' }}>Privacy Settings</h3>
      
      <div style={{ marginBottom: '2rem' }}>
        <h4 style={{ marginBottom: '1rem' }}>Location & Sharing</h4>
        <div style={{ display: 'grid', gap: '1rem' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input 
              type="checkbox" 
              checked={settings.privacy.shareLocation}
              onChange={(e) => handleSettingChange('privacy', 'shareLocation', e.target.checked)}
            />
            Share my location with other users
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input 
              type="checkbox" 
              checked={settings.privacy.shareChargingHistory}
              onChange={(e) => handleSettingChange('privacy', 'shareChargingHistory', e.target.checked)}
            />
            Share my charging history
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input 
              type="checkbox" 
              checked={settings.privacy.showOnMap}
              onChange={(e) => handleSettingChange('privacy', 'showOnMap', e.target.checked)}
            />
            Show me on the map
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input 
              type="checkbox" 
              checked={settings.privacy.allowAnalytics}
              onChange={(e) => handleSettingChange('privacy', 'allowAnalytics', e.target.checked)}
            />
            Allow analytics and usage data collection
          </label>
        </div>
      </div>

      <div style={{ 
        backgroundColor: '#f8f9fa', 
        padding: '1rem', 
        borderRadius: '4px',
        marginTop: '2rem'
      }}>
        <h4 style={{ marginBottom: '0.5rem' }}>Data Management</h4>
        <p style={{ fontSize: '0.9rem', color: '#6c757d', marginBottom: '1rem' }}>
          Control your data and privacy settings
        </p>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button style={{ 
            padding: '0.5rem 1rem', 
            backgroundColor: '#007bff', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px',
            cursor: 'pointer'
          }}>
            Download My Data
          </button>
          <button style={{ 
            padding: '0.5rem 1rem', 
            backgroundColor: '#dc3545', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px',
            cursor: 'pointer'
          }}>
            Delete My Account
          </button>
        </div>
      </div>
    </div>
  );

  const renderPreferencesTab = () => (
    <div>
      <h3 style={{ marginBottom: '1.5rem', color: '#28a745' }}>App Preferences</h3>
      
      <div style={{ marginBottom: '2rem' }}>
        <h4 style={{ marginBottom: '1rem' }}>Charging Preferences</h4>
        <div style={{ display: 'grid', gap: '1rem' }}>
          <div>
            <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '0.5rem' }}>
              Default Energy Type
            </label>
            <select 
              value={settings.preferences.defaultEnergyType}
              onChange={(e) => handleSettingChange('preferences', 'defaultEnergyType', e.target.value)}
              style={{ 
                width: '100%', 
                padding: '0.5rem', 
                border: '1px solid #ddd', 
                borderRadius: '4px' 
              }}
            >
              <option value="Level 1">Level 1</option>
              <option value="Level 2">Level 2</option>
              <option value="DC Fast">DC Fast</option>
            </select>
          </div>
          
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input 
              type="checkbox" 
              checked={settings.preferences.autoStartCharging}
              onChange={(e) => handleSettingChange('preferences', 'autoStartCharging', e.target.checked)}
            />
            Auto-start charging when connected
          </label>
          
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input 
              type="checkbox" 
              checked={settings.preferences.ecoMode}
              onChange={(e) => handleSettingChange('preferences', 'ecoMode', e.target.checked)}
            />
            Enable eco-friendly charging mode
          </label>
        </div>
      </div>

      <div style={{ marginBottom: '2rem' }}>
        <h4 style={{ marginBottom: '1rem' }}>Appearance</h4>
        <div style={{ display: 'grid', gap: '1rem' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input 
              type="checkbox" 
              checked={settings.preferences.darkMode}
              onChange={(e) => handleSettingChange('preferences', 'darkMode', e.target.checked)}
            />
            Dark Mode
          </label>
          
          <div>
            <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '0.5rem' }}>
              Language
            </label>
            <select 
              value={settings.preferences.language}
              onChange={(e) => handleSettingChange('preferences', 'language', e.target.value)}
              style={{ 
                width: '100%', 
                padding: '0.5rem', 
                border: '1px solid #ddd', 
                borderRadius: '4px' 
              }}
            >
              <option value="English">English</option>
              <option value="Spanish">Spanish</option>
              <option value="French">French</option>
              <option value="German">German</option>
            </select>
          </div>
          
          <div>
            <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '0.5rem' }}>
              Timezone
            </label>
            <select 
              value={settings.preferences.timezone}
              onChange={(e) => handleSettingChange('preferences', 'timezone', e.target.value)}
              style={{ 
                width: '100%', 
                padding: '0.5rem', 
                border: '1px solid #ddd', 
                borderRadius: '4px' 
              }}
            >
              <option value="America/Los_Angeles">Pacific Time</option>
              <option value="America/New_York">Eastern Time</option>
              <option value="America/Chicago">Central Time</option>
              <option value="America/Denver">Mountain Time</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );

  const renderAccountTab = () => (
    <div>
      <h3 style={{ marginBottom: '1.5rem', color: '#28a745' }}>Account Settings</h3>
      
      <div style={{ marginBottom: '2rem' }}>
        <h4 style={{ marginBottom: '1rem' }}>Account Information</h4>
        <div style={{ display: 'grid', gap: '1rem' }}>
          <div>
            <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '0.5rem' }}>
              Email Address
            </label>
            <input 
              type="email" 
              value={settings.account.email}
              onChange={(e) => handleSettingChange('account', 'email', e.target.value)}
              style={{ 
                width: '100%', 
                padding: '0.5rem', 
                border: '1px solid #ddd', 
                borderRadius: '4px' 
              }}
            />
          </div>
          
          <div>
            <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '0.5rem' }}>
              Phone Number
            </label>
            <input 
              type="tel" 
              value={settings.account.phone}
              onChange={(e) => handleSettingChange('account', 'phone', e.target.value)}
              style={{ 
                width: '100%', 
                padding: '0.5rem', 
                border: '1px solid #ddd', 
                borderRadius: '4px' 
              }}
            />
          </div>
          
          <div>
            <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '0.5rem' }}>
              Password
            </label>
            <input 
              type="password" 
              value={settings.account.password}
              onChange={(e) => handleSettingChange('account', 'password', e.target.value)}
              style={{ 
                width: '100%', 
                padding: '0.5rem', 
                border: '1px solid #ddd', 
                borderRadius: '4px' 
              }}
            />
          </div>
        </div>
      </div>

      <div style={{ marginBottom: '2rem' }}>
        <h4 style={{ marginBottom: '1rem' }}>Security</h4>
        <div style={{ display: 'grid', gap: '1rem' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input 
              type="checkbox" 
              checked={settings.account.twoFactorAuth}
              onChange={(e) => handleSettingChange('account', 'twoFactorAuth', e.target.checked)}
            />
            Enable Two-Factor Authentication
          </label>
        </div>
      </div>

      <div style={{ 
        backgroundColor: '#f8f9fa', 
        padding: '1rem', 
        borderRadius: '4px',
        marginTop: '2rem'
      }}>
        <h4 style={{ marginBottom: '0.5rem' }}>Account Actions</h4>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <button style={{ 
            padding: '0.5rem 1rem', 
            backgroundColor: '#007bff', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px',
            cursor: 'pointer'
          }}>
            Change Password
          </button>
          <button style={{ 
            padding: '0.5rem 1rem', 
            backgroundColor: '#ffc107', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px',
            cursor: 'pointer'
          }}>
            Export Data
          </button>
          <button style={{ 
            padding: '0.5rem 1rem', 
            backgroundColor: '#dc3545', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px',
            cursor: 'pointer'
          }}>
            Deactivate Account
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <div style={{ padding: '2rem', backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
      <div style={{ 
        backgroundColor: 'white', 
        borderRadius: '8px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        overflow: 'hidden'
      }}>
        {/* Header */}
        <div style={{ 
          backgroundColor: '#28a745', 
          color: 'white', 
          padding: '1.5rem 2rem'
        }}>
          <h1 style={{ margin: 0 }}>Settings</h1>
          <p style={{ margin: '0.5rem 0 0 0', opacity: 0.9 }}>
            Manage your account preferences and privacy settings
          </p>
        </div>

        {/* Navigation Tabs */}
        <div style={{ 
          display: 'flex', 
          borderBottom: '1px solid #e9ecef'
        }}>
          {[
            { id: 'notifications', label: 'Notifications', icon: '🔔' },
            { id: 'privacy', label: 'Privacy', icon: '🔒' },
            { id: 'preferences', label: 'Preferences', icon: '⚙️' },
            { id: 'account', label: 'Account', icon: '👤' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              style={{
                padding: '1rem 2rem',
                border: 'none',
                backgroundColor: activeTab === tab.id ? '#28a745' : 'transparent',
                color: activeTab === tab.id ? 'white' : '#6c757d',
                cursor: 'pointer',
                flex: 1,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '0.5rem'
              }}
            >
              <span>{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </div>

        {/* Content */}
        <div style={{ padding: '2rem' }}>
          {activeTab === 'notifications' && renderNotificationsTab()}
          {activeTab === 'privacy' && renderPrivacyTab()}
          {activeTab === 'preferences' && renderPreferencesTab()}
          {activeTab === 'account' && renderAccountTab()}
        </div>

        {/* Save Button */}
        <div style={{ 
          padding: '1.5rem 2rem', 
          borderTop: '1px solid #e9ecef',
          textAlign: 'right'
        }}>
          <button 
            onClick={handleSaveSettings}
            style={{ 
              padding: '0.75rem 2rem', 
              backgroundColor: '#28a745', 
              color: 'white', 
              border: 'none', 
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '1rem'
            }}
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage; 