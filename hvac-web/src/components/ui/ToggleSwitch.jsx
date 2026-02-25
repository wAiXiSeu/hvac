import { useState } from 'react';
import './ToggleSwitch.css';

export function ToggleSwitch({ 
  label, 
  checked, 
  onChange, 
  disabled = false,
  address,
  rawValue,
  showDetails = true
}) {
  const [isLoading, setIsLoading] = useState(false);

  const handleToggle = async () => {
    if (disabled || isLoading) return;
    
    setIsLoading(true);
    try {
      await onChange(!checked);
    } catch (error) {
      console.error('Toggle failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="toggle-switch">
      <div className="toggle-switch__header">
        <span className="toggle-switch__label">{label}</span>
        {showDetails && (address !== undefined || rawValue !== undefined) && (
          <span className="toggle-switch__details">
            {address !== undefined && `[${address}]`}
            {rawValue !== undefined && ` = ${rawValue}`}
          </span>
        )}
      </div>
      <div className="toggle-switch__control">
        <button
          className={`toggle-switch__btn ${checked ? 'toggle-switch__btn--on' : ''} ${disabled ? 'toggle-switch__btn--disabled' : ''}`}
          onClick={handleToggle}
          disabled={disabled || isLoading}
        >
          <span className="toggle-switch__slider">
            {isLoading && <span className="toggle-switch__loading"></span>}
          </span>
        </button>
        <span className="toggle-switch__status">
          {checked ? '开' : '关'}
        </span>
      </div>
    </div>
  );
}
