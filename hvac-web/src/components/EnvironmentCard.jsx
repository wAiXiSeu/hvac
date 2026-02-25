import { usePolling } from '../hooks/usePolling';
import { getEnvironment } from '../services/api';

export function EnvironmentCard() {
  const { data, loading } = usePolling(getEnvironment, 3000);
  
  if (loading || !data) {
    return <div className="card">加载中...</div>;
  }
  
  return (
    <div className="card">
      <h3>环境数据</h3>
      <div className="data-grid">
        <div className="data-item">
          <span className="label">室内 PM2.5</span>
          <span className="value">{data.pm25 ?? '--'}<small>μg/m³</small></span>
        </div>
        <div className="data-item">
          <span className="label">室内 CO2</span>
          <span className="value">{data.co2 ?? '--'}<small>PPM</small></span>
        </div>
        <div className="data-item">
          <span className="label">室外温度</span>
          <span className="value">{(data.outdoor_temp ?? 0).toFixed(1)}<small>°C</small></span>
        </div>
        <div className="data-item">
          <span className="label">室外湿度</span>
          <span className="value">{(data.outdoor_humidity ?? 0).toFixed(1)}<small>%</small></span>
        </div>
      </div>
    </div>
  );
}
