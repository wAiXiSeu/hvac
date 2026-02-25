import { useState } from 'react';
import './ControlInput.css';

export function ControlInput({ 
  label, 
  value, 
  unit, 
  min, 
  max, 
  step = 0.5, 
  onSave, 
  disabled = false 
}) {
  const [isEditing, setIsEditing] = useState(false);
  const [inputValue, setInputValue] = useState(value);
  const [error, setError] = useState('');

  const handleEdit = () => {
    if (disabled) return;
    setIsEditing(true);
    setInputValue(value);
    setError('');
  };

  const handleCancel = () => {
    setIsEditing(false);
    setInputValue(value);
    setError('');
  };

  const handleSave = async () => {
    const numValue = parseFloat(inputValue);
    
    // 验证
    if (isNaN(numValue)) {
      setError('请输入有效数字');
      return;
    }
    
    if (min !== undefined && numValue < min) {
      setError(`最小值为 ${min}`);
      return;
    }
    
    if (max !== undefined && numValue > max) {
      setError(`最大值为 ${max}`);
      return;
    }

    try {
      await onSave(numValue);
      setIsEditing(false);
      setError('');
    } catch (err) {
      setError('保存失败');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSave();
    } else if (e.key === 'Escape') {
      handleCancel();
    }
  };

  return (
    <div className="control-input">
      <span className="control-input__label">{label}</span>
      {isEditing ? (
        <div className="control-input__edit">
          <input
            type="number"
            className="control-input__field"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyPress}
            min={min}
            max={max}
            step={step}
            autoFocus
          />
          <button className="control-input__btn control-input__btn--save" onClick={handleSave}>
            ✓
          </button>
          <button className="control-input__btn control-input__btn--cancel" onClick={handleCancel}>
            ✗
          </button>
          {error && <span className="control-input__error">{error}</span>}
        </div>
      ) : (
        <span 
          className={`control-input__value ${!disabled ? 'control-input__value--editable' : ''}`}
          onClick={handleEdit}
        >
          {value !== null && value !== undefined ? value : '--'}
          {unit && <span className="control-input__unit">{unit}</span>}
        </span>
      )}
    </div>
  );
}
