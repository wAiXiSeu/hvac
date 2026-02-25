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

export default api;
