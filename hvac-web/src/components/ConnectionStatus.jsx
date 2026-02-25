import { usePolling } from '../hooks/usePolling';
import { getStatus } from '../services/api';

export function ConnectionStatus() {
  const { data, loading } = usePolling(getStatus, 5000);
  const isConnected = data?.connected;
  
  return (
    <div className="connection-status">
      <span className={"status-indicator " + (isConnected ? "connected" : "disconnected")} />
      <span className="status-text">
        {loading ? '加载中...' : isConnected ? '已连接' : '未连接'}
      </span>
    </div>
  );
}
