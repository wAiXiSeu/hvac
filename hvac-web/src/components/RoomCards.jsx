import { useState, useEffect } from 'react';
import { getRooms, updateRoomSetpoint } from '../services/api';

export function RoomCards() {
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingId, setEditingId] = useState(null);
  const [tempValue, setTempValue] = useState(20);
  
  useEffect(() => {
    const fetchRooms = async () => {
      try {
        const response = await getRooms();
        setRooms(response.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchRooms();
    const interval = setInterval(fetchRooms, 3000);
    return () => clearInterval(interval);
  }, []);
  
  const handleSetpoint = async (roomId, temp) => {
    try {
      await updateRoomSetpoint(roomId, temp);
      setEditingId(null);
      const response = await getRooms();
      setRooms(response.data);
    } catch (err) {
      console.error('Failed to set temperature:', err);
    }
  };
  
  if (loading) {
    return <div className="card">加载中...</div>;
  }
  
  return (
    <div className="card">
      <h3>房间控制</h3>
      <div className="rooms-grid">
        {rooms.map((room) => (
          <div key={room.id} className="room-card">
            <h4>{room.name}</h4>
            <div className="room-data">
              <div className="data-row">
                <span>当前温度</span>
                <span>{(room.temp ?? 0).toFixed(1)}°C</span>
              </div>
              <div className="data-row">
                <span>当前湿度</span>
                <span>{(room.humidity ?? 0).toFixed(1)}%</span>
              </div>
              <div className="data-row">
                <span>设定温度</span>
                {editingId === room.id ? (
                  <span>
                    <input type="number" value={tempValue} onChange={(e) => setTempValue(parseFloat(e.target.value))} min="16" max="30" step="0.5" style={{width: '50px'}} />
                    <button onClick={() => handleSetpoint(room.id, tempValue)}>OK</button>
                    <button onClick={() => setEditingId(null)}>X</button>
                  </span>
                ) : (
                  <span className="setpoint-value" onClick={() => { setEditingId(room.id); setTempValue(room.setpoint || 20); }}>
                    {(room.setpoint ?? 0).toFixed(1)}°C
                  </span>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
