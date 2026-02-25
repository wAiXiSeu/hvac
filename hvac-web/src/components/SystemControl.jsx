import { useState, useEffect } from 'react';
import { getSystem, updateSystem } from '../services/api';

export function SystemControl() {
  const [systemData, setSystemData] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const fetchSystem = async () => {
      try {
        const response = await getSystem();
        setSystemData(response.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchSystem();
    const interval = setInterval(fetchSystem, 3000);
    return () => clearInterval(interval);
  }, []);
  
  const handleControl = async (key, value) => {
    try {
      await updateSystem({ [key]: value });
      const response = await getSystem();
      setSystemData(response.data);
    } catch (err) {
      console.error('Control failed:', err);
    }
  };
  
  if (loading || !systemData) {
    return <div className="card">加载中...</div>;
  }
  
  const modeNames = { 1: '制冷', 2: '制热', 3: '通风', 4: '除湿' };
  
  return (
    <div className="card">
      <h3>系统控制</h3>
      <div className="control-section">
        <span className="label">电源</span>
        <div className="button-group">
          <button className={systemData.power === 1 ? 'active' : ''} onClick={() => handleControl('power', true)}>开机</button>
          <button className={systemData.power === 0 ? 'active' : ''} onClick={() => handleControl('power', false)}>关机</button>
        </div>
      </div>
      <div className="control-section">
        <span className="label">模式</span>
        <div className="button-group">
          {[1, 2, 3, 4].map((mode) => (
            <button key={mode} className={systemData.run_mode === mode ? 'active' : ''} onClick={() => handleControl('run_mode', mode)}>
              {modeNames[mode]}
            </button>
          ))}
        </div>
      </div>
      <div className="control-section">
        <span className="label">风速</span>
        <input type="range" min="0" max="100" value={systemData.fan_speed || 0} onChange={(e) => handleControl('fan_speed', parseInt(e.target.value))} />
        <span className="value">{systemData.fan_speed || 0}%</span>
      </div>
    </div>
  );
}
