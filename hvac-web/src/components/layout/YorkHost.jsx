import { DataDisplay } from '../ui/DataDisplay';
import './YorkHost.css';

export function YorkHost({ data }) {
  if (!data) {
    return (
      <div className="data-card data-card--readonly york-host">
        <h3 className="section-header section-header--readonly">约克主机</h3>
        <p className="york-host__empty">暂无数据</p>
      </div>
    );
  }

  return (
    <div className="data-card data-card--readonly york-host">
      <h3 className="section-header section-header--readonly">约克主机</h3>
      <div className="york-host__content">
        <DataDisplay 
          label="供水温度" 
          value={data.supplyTemp?.toFixed(1)} 
          unit="°C" 
        />
        <DataDisplay 
          label="回水温度" 
          value={data.returnTemp?.toFixed(1)} 
          unit="°C" 
        />
        <DataDisplay 
          label="制热设定点" 
          value={data.heatingSetpoint?.toFixed(1)} 
          unit="°C" 
        />
        <DataDisplay 
          label="制冷设定点" 
          value={data.coolingSetpoint?.toFixed(1)} 
          unit="°C" 
        />
      </div>
    </div>
  );
}
