import { useEffect, useState } from 'react';
import './FeedbackMessage.css';

export function FeedbackMessage({ 
  type = 'success', 
  message, 
  duration = 2000, 
  onClose 
}) {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        setIsVisible(false);
        onClose?.();
      }, duration);
      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);

  const handleClick = () => {
    setIsVisible(false);
    onClose?.();
  };

  if (!isVisible) return null;

  const icon = type === 'success' ? '✓' : '✗';

  return (
    <div 
      className={`feedback-message feedback-message--${type}`}
      onClick={handleClick}
    >
      <span className="feedback-message__icon">{icon}</span>
      <span className="feedback-message__text">{message}</span>
    </div>
  );
}
