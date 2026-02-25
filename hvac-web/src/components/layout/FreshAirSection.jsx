import { useHvacData } from '../../contexts/HvacDataContext';
import { DataDisplay } from '../ui/DataDisplay';
import './FreshAirSection.css';

export function FreshAirSection() {
  const { freshAir } = useHvacData();

  const getStatusText = (code) => {
    if (code === 0x8104 || code === 33028) return '正常运行';
    return `状态码: 0x${code?.toString(16)}`;
  };

  const isNormalStatus = (code) => {
    return code === 0x8104 || code === 33028;
  };

  if (!freshAir) {
    return (
      <div className="fresh-air-section">
        <h2 className="fresh-air-section__title">新风系统</h2>
        <div className="data-card data-card--readonly">
          <p className="fresh-air-section__empty">暂无数据</p>
        </div>
      </div>
    );
  }

  return (
    <div className="fresh-air-section">
      <h2 className="fresh-air-section__title">新风系统</h2>
      
      <div className="fresh-air-section__content">
        {/* 系统状态 - 只读 */}
        <div className="data-card data-card--readonly">
          <h3 className="section-header section-header--readonly">系统状态</h3>
          <div className="fresh-air-section__status">
            <DataDisplay 
              label="压缩机频率" 
              value={freshAir.compressorFreq?.value?.toFixed(0)} 
              unit="Hz"
              address={freshAir.compressorFreq?.address}
              rawValue={freshAir.compressorFreq?.raw}
              showDetails={true}
            />
            <DataDisplay 
              label="供水温度" 
              value={freshAir.supplyTemp?.value?.toFixed(1)} 
              unit="°C"
              address={freshAir.supplyTemp?.address}
              rawValue={freshAir.supplyTemp?.raw}
              showDetails={true}
            />
            <DataDisplay 
              label="回水温度" 
              value={freshAir.returnTemp?.value?.toFixed(1)} 
              unit="°C"
              address={freshAir.returnTemp?.address}
              rawValue={freshAir.returnTemp?.raw}
              showDetails={true}
            />
            <div className={`fresh-air-section__status-indicator ${isNormalStatus(freshAir.statusCode) ? 'fresh-air-section__status-indicator--normal' : 'fresh-air-section__status-indicator--warning'}`}>
              <span className="fresh-air-section__status-label">运行状态</span>
              <span className="fresh-air-section__status-value">
                {getStatusText(freshAir.statusCode)}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
