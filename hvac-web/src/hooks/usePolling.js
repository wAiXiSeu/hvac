import { useState, useEffect, useRef } from 'react';

export function usePolling(fetchFn, interval = 3000) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const intervalRef = useRef(null);

  const fetchData = async () => {
    try {
      const response = await fetchFn();
      setData(response.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    intervalRef.current = setInterval(fetchData, interval);
    return () => clearInterval(intervalRef.current);
  }, []);

  return { data, loading, refetch: fetchData };
}
