import { useState, useEffect } from 'react';
import { getConfig, updateConfig } from '../services/api';

export function ConfigModal({ isOpen, onClose }) {
  const [config, setConfig] = useState({ host: '', port: 502, slave_id: 1, timeout: 5 });
  const [saving, setSaving] = useState(false);
  
  useEffect(() => {
    if (isOpen) {
      getConfig().then((res) => setConfig(res.data));
    }
  }, [isOpen]);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await updateConfig(config);
      onClose();
    } catch (err) {
      console.error('Failed to save config:', err);
    } finally {
      setSaving(false);
    }
  };
  
  if (!isOpen) return null;
  
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <h3>Modbus 配置</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>IP地址</label>
            <input type="text" value={config.host} onChange={(e) => setConfig({ ...config, host: e.target.value })} required />
          </div>
          <div className="form-group">
            <label>端口</label>
            <input type="number" value={config.port} onChange={(e) => setConfig({ ...config, port: parseInt(e.target.value) })} required />
          </div>
          <div className="form-group">
            <label>Slave ID</label>
            <input type="number" value={config.slave_id} onChange={(e) => setConfig({ ...config, slave_id: parseInt(e.target.value) })} />
          </div>
          <div className="form-group">
            <label>超时时间 (秒)</label>
            <input type="number" value={config.timeout} onChange={(e) => setConfig({ ...config, timeout: parseInt(e.target.value) })} />
          </div>
          <div className="modal-actions">
            <button type="button" onClick={onClose}>取消</button>
            <button type="submit" disabled={saving}>{saving ? '保存中...' : '保存'}</button>
          </div>
        </form>
      </div>
    </div>
  );
}
