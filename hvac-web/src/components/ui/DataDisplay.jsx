import './DataDisplay.css';

export function DataDisplay({ label, value, unit, icon, address, rawValue, showDetails = false }) {
  return (
    <div className="data-display">
      {icon && <span className="data-display__icon">{icon}</span>}
      <div className="data-display__content">
        <div className="data-display__header">
          <span className="data-display__label">{label}</span>
          {showDetails && (address !== undefined || rawValue !== undefined) && (
            <span className="data-display__details">
              {address !== undefined && `[${address}]`}
              {rawValue !== undefined && ` = ${rawValue}`}
            </span>
          )}
        </div>
        <span className="data-display__value">
          {value !== null && value !== undefined ? value : '--'}
          {unit && <span className="data-display__unit">{unit}</span>}
        </span>
      </div>
    </div>
  );
}
