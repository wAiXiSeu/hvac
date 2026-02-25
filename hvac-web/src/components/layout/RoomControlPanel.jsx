import { useState } from 'react';
import { DataDisplay } from '../ui/DataDisplay';
import { ControlInput } from '../ui/ControlInput';
import { FeedbackMessage } from '../ui/FeedbackMessage';
import { updateRoomSetpoint } from '../../services/api';
import { useHvacData } from '../../contexts/HvacDataContext';
import './RoomControlPanel.css';

export function RoomControlPanel({ room }) {
  const [feedback, setFeedback] = useState(null);
  const { refreshData } = useHvacData();

  const handleSetpointChange = async (newTemp) => {
    try {
      await updateRoomSetpoint(room.id, newTemp);
      setFeedback({ type: 'success', message: '温度设定已更新' });
      setTimeout(() => refreshData(), 500);
    } catch (error) {
      setFeedback({ type: 'error', message: '温度设定失败' });
      throw error;
    }
  };

  return (
    <div className="data-card data-card--editable room-control-panel">
      <h3 className="room-control-panel__name">{room.name}</h3>
      
      <div className="room-control-panel__data">
        <DataDisplay 
          label="当前温度" 
          value={room.temp?.value?.toFixed(1)} 
          unit="°C"
          address={room.temp?.address}
          rawValue={room.temp?.raw}
          showDetails={true}
        />
        <DataDisplay 
          label="当前湿度" 
          value={room.humidity?.value?.toFixed(1)} 
          unit="%"
          address={room.humidity?.address}
          rawValue={room.humidity?.raw}
          showDetails={true}
        />
        <DataDisplay 
          label="露点温度" 
          value={room.dew_point?.value?.toFixed(1)} 
          unit="°C"
          address={room.dew_point?.address}
          rawValue={room.dew_point?.raw}
          showDetails={true}
        />
      </div>

      <div className="room-control-panel__control">
        <ControlInput 
          label="设定温度"
          value={room.setpoint?.value || 20}
          unit="°C"
          min={16}
          max={30}
          step={0.5}
          onSave={handleSetpointChange}
          address={room.setpoint?.address}
          rawValue={room.setpoint?.raw}
        />
      </div>

      {feedback && (
        <div className="room-control-panel__feedback">
          <FeedbackMessage 
            type={feedback.type}
            message={feedback.message}
            onClose={() => setFeedback(null)}
          />
        </div>
      )}
    </div>
  );
}
