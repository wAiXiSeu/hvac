import './DataDisplay.css';

export function DataDisplay({ label, value, unit, icon }) {
  return (
    <div className="data-display">
      {icon && <span className="data-display__icon">{icon}</span>}
      <div className="data-display__content">
        <span className="data-display__label">{label}</span>
        <span className="data-display__value">
          {value !== null && value !== undefined ? value : '--'}
          {unit && <span className="data-display__unit">{unit}</span>}
        </span>
      </div>
    </div>
  );
}
