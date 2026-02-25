import { useState, useEffect } from 'react';
import { getGroupedRegisters, writeRegister } from '../services/api';

export function RegistersPanel() {
  const [groupedData, setGroupedData] = useState({});
  const [loading, setLoading] = useState(true);
  const [editingAddr, setEditingAddr] = useState(null);
  const [editValue, setEditValue] = useState(0);
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getGroupedRegisters();
        setGroupedData(response.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, []);
  
  const handleWrite = async (address, value) => {
    try {
      await writeRegister(address, value);
      setEditingAddr(null);
      const response = await getGroupedRegisters();
      setGroupedData(response.data);
    } catch (err) {
      console.error('Failed to write register:', err);
    }
  };
  
  if (loading) {
    return <div className="card">加载中...</div>;
  }
  
  const groupOrder = ['environment', 'system', 'york', 'living_room', 'master_bedroom', 'second_bedroom', 'study_room', 'kitchen', 'fresh_air'];
  
  return (
    <div className="registers-panel">
      {groupOrder.map((group) => {
        if (!groupedData[group]) return null;
        const groupInfo = groupedData[group];
        
        return (
          <div key={group} className="card register-group">
            <h3>{groupInfo.name}</h3>
            <div className="register-list">
              {Object.entries(groupInfo.registers).map(([addr, data]) => (
                <div key={addr} className="register-item">
                  <div className="register-info">
                    <span className="register-name">{data.name}</span>
                    <span className="register-address">[{addr}]</span>
                    {data.rw === 'RW' && <span className="register-rw">RW</span>}
                  </div>
                  <div className="register-value">
                    {editingAddr === parseInt(addr) ? (
                      <span>
                        <input 
                          type="number" 
                          value={editValue} 
                          onChange={(e) => setEditValue(parseFloat(e.target.value))}
                          style={{width: '60px'}}
                        />
                        <button onClick={() => handleWrite(parseInt(addr), editValue)}>OK</button>
                        <button onClick={() => setEditingAddr(null)}>X</button>
                      </span>
                    ) : (
                      <span 
                        className={data.rw === 'RW' ? 'editable-value' : ''}
                        onClick={() => {
                          if (data.rw === 'RW') {
                            setEditingAddr(parseInt(addr));
                            setEditValue(data.value);
                          }
                        }}
                      >
                        {data.value !== null && data.value !== undefined 
                          ? (typeof data.value === 'number' ? data.value.toFixed(1) : data.value)
                          : '--'}
                        {data.unit && <small> {data.unit}</small>}
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}
