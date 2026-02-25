import { useState } from 'react';
import './Slider.css';

export function Slider({ 
  label, 
  value, 
  min = 0, 
  max = 100, 
  step = 1, 
  unit = '%',
  onChange, 
  disabled = false,
  address,
  rawValue,
  showDetails = true
}) {
  const [localValue, setLocalValue] = useState(value);
  const [isChanging, setIsChanging] = useState(false);

  const handleChange = (e) => {
    const newValue = parseFloat(e.target.value);
    setLocalValue(newValue);
    setIsChanging(true);
  };

  const handleRelease = async () => {
    if (localValue !== value) {
      try {
        await onChange(localValue);
      } catch (error) {
        console.error('Slider change failed:', error);
        setLocalValue(value); // 回滚
      }
    }
    setIsChanging(false);
  };

  const percentage = ((localValue - min) / (max - min)) * 100;

  return (
    <div className="slider">
      <div className="slider__header">
        <div className="slider__title">
          <span className="slider__label">{label}</span>
          {showDetails && (address !== undefined || rawValue !== undefined) && (
            <span className="slider__details">
              {address !== undefined && `[${address}]`}
              {rawValue !== undefined && ` = ${rawValue}`}
            </span>
          )}
        </div>
        <span className="slider__value">{localValue}{unit}</span>
      </div>
      <div className="slider__track-container">
        <input
          type="range"
          className="slider__input"
          value={localValue}
          min={min}
          max={max}
          step={step}
          onChange={handleChange}
          onMouseUp={handleRelease}
          onTouchEnd={handleRelease}
          disabled={disabled}
          style={{
            background: `linear-gradient(to right, var(--color-primary) 0%, var(--color-primary) ${percentage}%, #ddd ${percentage}%, #ddd 100%)`
          }}
        />
      </div>
      {isChanging && <span className="slider__hint">松开以应用</span>}
    </div>
  );
}
