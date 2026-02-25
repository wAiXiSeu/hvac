import { useHvacData } from '../../contexts/HvacDataContext';
import { EnvironmentMonitoring } from './EnvironmentMonitoring';
import { SystemControl } from './SystemControl';
import { YorkHost } from './YorkHost';
import './SystemOverview.css';

export function SystemOverview() {
  const { environment, system, york } = useHvacData();

  return (
    <div className="system-overview">
      <h2 className="system-overview__title">系统概览</h2>
      <div className="system-overview__grid">
        <EnvironmentMonitoring data={environment} />
        <SystemControl data={system} />
        <YorkHost data={york} />
      </div>
    </div>
  );
}
