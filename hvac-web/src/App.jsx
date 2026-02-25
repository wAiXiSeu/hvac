import { useState } from 'react';
import { HvacDataProvider } from './contexts/HvacDataContext';
import { ConnectionStatus } from './components/ConnectionStatus';
import { ConfigModal } from './components/ConfigModal';
import { SystemOverview } from './components/layout/SystemOverview';
import { RoomSection } from './components/layout/RoomSection';
import { FreshAirSection } from './components/layout/FreshAirSection';
import './App.css';
import './theme.css';

function App() {
  const [showConfig, setShowConfig] = useState(false);
  
  return (
    <HvacDataProvider>
      <div className="app">
        <header className="app-header">
          <h1>三恒系统控制</h1>
          <div className="header-actions">
            <ConnectionStatus />
            <button className="config-btn" onClick={() => setShowConfig(true)}>
              配置
            </button>
          </div>
        </header>
        
        <main className="app-main">
          <SystemOverview />
          <RoomSection />
          <FreshAirSection />
        </main>
        
        <ConfigModal isOpen={showConfig} onClose={() => setShowConfig(false)} />
      </div>
    </HvacDataProvider>
  );
}

export default App;
