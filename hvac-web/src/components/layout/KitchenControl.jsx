import { useState } from 'react';
import { DataDisplay } from '../ui/DataDisplay';
import { ToggleSwitch } from '../ui/ToggleSwitch';
import { FeedbackMessage } from '../ui/FeedbackMessage';
import { updateKitchenRadiant } from '../../services/api';
import { useHvacData } from '../../contexts/HvacDataContext';
import './KitchenControl.css';

export function KitchenControl() {
  const { rooms } = useHvacData();
  const [feedback, setFeedback] = useState(null);
  
  // 从 grouped data 中获取厨卫辐射状态 (寄存器 1133)
  // 注意：这里需要从后端获取真实数据，暂时使用 enabled 状态
  const kitchenRadiant = rooms?.kitchen_radiant || {};
  const enabled = kitchenRadiant?.value === 1;

  const handleToggle = async (newValue) => {
    try {
      await updateKitchenRadiant(newValue);
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
          address={1133}
          rawValue={enabled ? 1 : 0}
          showDetails={true}
        />
      </div>

      <div className="kitchen-control__control">
        <ToggleSwitch 
          label="辐射开关"
          checked={enabled}
          onChange={handleToggle}
          address={1133}
          rawValue={enabled ? 1 : 0}
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
