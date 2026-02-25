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
          value={data.supplyTemp?.value?.toFixed(1)} 
          unit="°C"
          address={data.supplyTemp?.address}
          rawValue={data.supplyTemp?.raw}
          showDetails={true}
        />
        <DataDisplay 
          label="回水温度" 
          value={data.returnTemp?.value?.toFixed(1)} 
          unit="°C"
          address={data.returnTemp?.address}
          rawValue={data.returnTemp?.raw}
          showDetails={true}
        />
        <DataDisplay 
          label="制热设定点" 
          value={data.heatingSetpoint?.value?.toFixed(1)} 
          unit="°C"
          address={data.heatingSetpoint?.address}
          rawValue={data.heatingSetpoint?.raw}
          showDetails={true}
        />
        <DataDisplay 
          label="制冷设定点" 
          value={data.coolingSetpoint?.value?.toFixed(1)} 
          unit="°C"
          address={data.coolingSetpoint?.address}
          rawValue={data.coolingSetpoint?.raw}
          showDetails={true}
        />
      </div>
    </div>
  );
}
