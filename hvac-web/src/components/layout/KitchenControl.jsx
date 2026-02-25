import { useState } from 'react';
import { DataDisplay } from '../ui/DataDisplay';
import { ToggleSwitch } from '../ui/ToggleSwitch';
import { FeedbackMessage } from '../ui/FeedbackMessage';
import { updateKitchenRadiant } from '../../services/api';
import './KitchenControl.css';

export function KitchenControl() {
  const [enabled, setEnabled] = useState(false);
  const [feedback, setFeedback] = useState(null);

  const handleToggle = async (newValue) => {
    try {
      await updateKitchenRadiant(newValue);
      setEnabled(newValue);
      setFeedback({ type: 'success', message: '厨卫辐射已更新' });
    } catch (error) {
      setFeedback({ type: 'error', message: '厨卫辐射控制失败' });
      throw error;
    }
  };

  return (
    <div className="data-card data-card--editable kitchen-control">
      <h3 className="kitchen-control__name">厨卫控制</h3>
      
      <div className="kitchen-control__data">
        <DataDisplay 
          label="辐射状态" 
          value={enabled ? '开启' : '关闭'} 
          unit=""
        />
      </div>

      <div className="kitchen-control__control">
        <ToggleSwitch 
          label="辐射开关"
          checked={enabled}
          onChange={handleToggle}
        />
      </div>

      {feedback && (
        <div className="kitchen-control__feedback">
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
