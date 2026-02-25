import { useState } from 'react';
import './ToggleSwitch.css';

export function ToggleSwitch({ label, checked, onChange, disabled = false }) {
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
      <span className="toggle-switch__label">{label}</span>
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
  );
}
