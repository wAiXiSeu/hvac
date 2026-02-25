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
          value={data.pm25?.value?.toFixed(1)} 
          unit="μg/m³"
          address={data.pm25?.address}
          rawValue={data.pm25?.raw}
          showDetails={true}
        />
        <DataDisplay 
          label="室内 CO2" 
          value={data.co2?.value?.toFixed(0)} 
          unit="PPM"
          address={data.co2?.address}
          rawValue={data.co2?.raw}
          showDetails={true}
        />
        <DataDisplay 
          label="室外温度" 
          value={data.outdoor_temp?.value?.toFixed(1)} 
          unit="°C"
          address={data.outdoor_temp?.address}
          rawValue={data.outdoor_temp?.raw}
          showDetails={true}
        />
        <DataDisplay 
          label="室外湿度" 
          value={data.outdoor_humidity?.value?.toFixed(1)} 
          unit="%"
          address={data.outdoor_humidity?.address}
          rawValue={data.outdoor_humidity?.raw}
          showDetails={true}
        />
      </div>
    </div>
  );
}
