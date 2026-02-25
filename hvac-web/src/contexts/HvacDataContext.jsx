import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { getStatus, getGroupedRegisters, getSystem, getRooms } from '../services/api';

const HvacDataContext = createContext(null);

export function HvacDataProvider({ children }) {
  const [connection, setConnection] = useState({ status: 'disconnected', lastUpdate: null });
  const [environment, setEnvironment] = useState(null);
  const [system, setSystem] = useState(null);
  const [york, setYork] = useState(null);
  const [rooms, setRooms] = useState([]);
  const [freshAir, setFreshAir] = useState(null);
  const [isPolling, setIsPolling] = useState(true);

  // 获取所有数据
  const fetchAllData = useCallback(async () => {
    try {
      // 获取连接状态
      const statusRes = await getStatus();
      setConnection({
        status: statusRes.data.connected ? 'connected' : 'disconnected',
        lastUpdate: new Date()
      });

      if (statusRes.data.connected) {
        // 并行获取分组数据、系统、房间数据
        const [groupedRes, sysRes, roomsRes] = await Promise.all([
          getGroupedRegisters(),
          getSystem(),
          getRooms()
        ]);

        const grouped = groupedRes.data;

        // 提取环境监测数据（保留完整对象）
        const envGroup = grouped.environment?.registers || {};
        setEnvironment({
          pm25: envGroup[1024],
          co2: envGroup[1026],
          outdoor_temp: envGroup[1027],
          outdoor_humidity: envGroup[1028]
        });

        // 提取约克主机数据（保留完整对象）
        const yorkGroup = grouped.york?.registers || {};
        setYork({
          supplyTemp: yorkGroup[1029],
          returnTemp: yorkGroup[1030],
          heatingSetpoint: yorkGroup[1062],
          coolingSetpoint: yorkGroup[1066]
        });

        // 提取新风系统数据（保留完整对象）
        const freshAirGroup = grouped.fresh_air?.registers || {};
        setFreshAir({
          compressorFreq: freshAirGroup[1161],
          supplyTemp: freshAirGroup[1164],
          returnTemp: freshAirGroup[1165],
          statusCode: freshAirGroup[1049]?.value,
          humidifier: freshAirGroup[1168]?.value,
          fanSpeed: sysRes.data.fan_speed
        });

        setSystem(sysRes.data);
        setRooms(roomsRes.data);
      }
    } catch (error) {
      console.error('Failed to fetch data:', error);
      setConnection({ status: 'error', lastUpdate: new Date() });
    }
  }, []);

  // 初始加载
  useEffect(() => {
    fetchAllData();
  }, [fetchAllData]);

  // 轮询逻辑
  useEffect(() => {
    if (!isPolling) return;

    const interval = setInterval(fetchAllData, 5000);
    return () => clearInterval(interval);
  }, [isPolling, fetchAllData]);

  // 窗口失焦时暂停轮询
  useEffect(() => {
    const handleVisibilityChange = () => {
      setIsPolling(!document.hidden);
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, []);

  const value = {
    connection,
    environment,
    system,
    york,
    rooms,
    freshAir,
    refreshData: fetchAllData
  };

  return (
    <HvacDataContext.Provider value={value}>
      {children}
    </HvacDataContext.Provider>
  );
}

export function useHvacData() {
  const context = useContext(HvacDataContext);
  if (!context) {
    throw new Error('useHvacData must be used within HvacDataProvider');
  }
  return context;
}
