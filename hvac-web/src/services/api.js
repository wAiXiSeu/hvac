import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  timeout: 5000,
});

export const getConfig = () => api.get('/config');
export const updateConfig = (config) => api.put('/config', config);
export const getStatus = () => api.get('/status');
export const getAllRegisters = () => api.get('/registers');
export const getGroupedRegisters = () => api.get('/registers/grouped');
export const getRegisterGroups = () => api.get('/registers/groups');
export const writeRegister = (address, value) => api.post('/registers/write', { address, value });
export const getEnvironment = () => api.get('/environment');
export const getSystem = () => api.get('/system');
export const updateSystem = (control) => api.put('/system', control);
export const getRooms = () => api.get('/rooms');
export const updateRoomSetpoint = (roomId, temp) => api.put('/rooms/' + roomId, { temp });

// 新风控制
export const updateFreshAirSpeed = (speed) => writeRegister(1047, speed);
export const updateHumidifier = (enabled) => writeRegister(1168, enabled ? 1 : 0);

// 厨卫控制
export const updateKitchenRadiant = (enabled) => writeRegister(1133, enabled ? 1 : 0);

// 输入验证工具
export const validateTemperature = (temp, min = 16, max = 30) => {
  const numTemp = parseFloat(temp);
  if (isNaN(numTemp)) return { valid: false, error: '请输入有效数字' };
  if (numTemp < min) return { valid: false, error: `最小值为 ${min}°C` };
  if (numTemp > max) return { valid: false, error: `最大值为 ${max}°C` };
  return { valid: true };
};

export default api;
