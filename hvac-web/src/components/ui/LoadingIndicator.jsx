import './LoadingIndicator.css';

export function LoadingIndicator({ size = 'medium', text }) {
  return (
    <div className={`loading-indicator loading-indicator--${size}`}>
      <span className="loading-indicator__spinner"></span>
      {text && <span className="loading-indicator__text">{text}</span>}
    </div>
  );
}
