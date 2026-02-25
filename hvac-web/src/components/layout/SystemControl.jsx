import { useState } from 'react';
import { ToggleSwitch } from '../ui/ToggleSwitch';
import { Slider } from '../ui/Slider';
import { FeedbackMessage } from '../ui/FeedbackMessage';
import { updateSystem, updateFreshAirSpeed, updateHumidifier } from '../../services/api';
import { useHvacData } from '../../contexts/HvacDataContext';
import './SystemControl.css';

const RUN_MODES = [
  { value: 1, label: '制热' },
  { value: 2, label: '制冷' },
  { value: 3, label: '除湿' },
  { value: 4, label: '通风' }
];

export function SystemControl({ data }) {
  const { freshAir } = useHvacData();
  const [feedback, setFeedback] = useState(null);

  const showFeedback = (type, message) => {
    setFeedback({ type, message });
  };

  const handlePowerChange = async (newValue) => {
    try {
      await updateSystem({ power: newValue });
      showFeedback('success', '电源状态已更新');
    } catch (error) {
      showFeedback('error', '电源控制失败');
      throw error;
    }
  };

  const handleHomeModeChange = async (newValue) => {
    try {
      await updateSystem({ home_mode: newValue });
      showFeedback('success', '模式已更新');
    } catch (error) {
      showFeedback('error', '模式切换失败');
      throw error;
    }
  };

  const handleRunModeChange = async (e) => {
    try {
      await updateSystem({ run_mode: parseInt(e.target.value) });
      showFeedback('success', '运行模式已更新');
    } catch (error) {
      showFeedback('error', '运行模式切换失败');
    }
  };

  const handleFanSpeedChange = async (newValue) => {
    try {
      await updateSystem({ fan_speed: Math.round(newValue) });
      showFeedback('success', '新风风速已更新');
    } catch (error) {
      showFeedback('error', '风速调节失败');
      throw error;
    }
  };

  const handleFreshAirSpeedChange = async (newValue) => {
    try {
      await updateFreshAirSpeed(Math.round(newValue));
      showFeedback('success', '新风风速已更新');
    } catch (error) {
      showFeedback('error', '风速调节失败');
      throw error;
    }
  };

  const handleHumidifierChange = async (newValue) => {
    try {
      await updateHumidifier(newValue);
      showFeedback('success', '加湿功能已更新');
    } catch (error) {
      showFeedback('error', '加湿控制失败');
      throw error;
    }
  };

  if (!data) {
    return (
      <div className="data-card data-card--editable system-control">
        <h3 className="section-header section-header--editable">系统控制</h3>
        <p className="system-control__empty">暂无数据</p>
      </div>
    );
  }

  return (
    <div className="data-card data-card--editable system-control">
      <h3 className="section-header section-header--editable">系统控制</h3>
      <div className="system-control__content">
        <ToggleSwitch 
          label="系统电源" 
          checked={data.power === 1}
          onChange={handlePowerChange}
        />
        <ToggleSwitch 
          label="在家/离家模式" 
          checked={data.home_mode === 1}
          onChange={handleHomeModeChange}
        />
        
        <div className="system-control__field">
          <label className="system-control__label">运行模式</label>
          <select 
            className="system-control__select"
            value={data.run_mode || 1}
            onChange={handleRunModeChange}
          >
            {RUN_MODES.map(mode => (
              <option key={mode.value} value={mode.value}>
                {mode.label}
              </option>
            ))}
          </select>
        </div>

        <Slider 
          label="新风风速" 
          value={freshAir?.fanSpeed || data.fan_speed || 0} 
          min={0}
          max={100}
          step={5}
          unit="%"
          onChange={handleFreshAirSpeedChange}
        />

        {freshAir && (
          <ToggleSwitch 
            label="加湿功能"
            checked={freshAir.humidifier === 1}
            onChange={handleHumidifierChange}
          />
        )}
      </div>

      {feedback && (
        <div className="system-control__feedback">
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
