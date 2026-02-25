import { DataDisplay } from '../ui/DataDisplay';
import './EnvironmentMonitoring.css';

export function EnvironmentMonitoring({ data }) {
  if (!data) {
    return (
      <div className="data-card data-card--readonly environment-monitoring">
        <h3 className="section-header section-header--readonly">环境监测</h3>
        <p className="environment-monitoring__empty">暂无数据</p>
      </div>
    );
  }

  return (
    <div className="data-card data-card--readonly environment-monitoring">
      <h3 className="section-header section-header--readonly">环境监测</h3>
      <div className="environment-monitoring__content">
        <DataDisplay 
          label="室内 PM2.5" 
          value={data.pm25?.toFixed(1)} 
          unit="μg/m³" 
        />
        <DataDisplay 
          label="室内 CO2" 
          value={data.co2?.toFixed(0)} 
          unit="PPM" 
        />
        <DataDisplay 
          label="室外温度" 
          value={data.outdoor_temp?.toFixed(1)} 
          unit="°C" 
        />
        <DataDisplay 
          label="室外湿度" 
          value={data.outdoor_humidity?.toFixed(1)} 
          unit="%" 
        />
      </div>
    </div>
  );
}
