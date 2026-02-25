import { useState } from 'react';
import { ConnectionStatus } from './components/ConnectionStatus';
import { RegistersPanel } from './components/RegistersPanel';
import { ConfigModal } from './components/ConfigModal';
import './App.css';

function App() {
  const [showConfig, setShowConfig] = useState(false);
  
  return (
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
        <RegistersPanel />
      </main>
      
      <ConfigModal isOpen={showConfig} onClose={() => setShowConfig(false)} />
    </div>
  );
}

export default App;
