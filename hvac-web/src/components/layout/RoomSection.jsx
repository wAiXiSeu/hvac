import { useHvacData } from '../../contexts/HvacDataContext';
import { RoomControlPanel } from './RoomControlPanel';
import { KitchenControl } from './KitchenControl';
import './RoomSection.css';

export function RoomSection() {
  const { rooms } = useHvacData();

  return (
    <div className="room-section">
      <h2 className="room-section__title">房间信息</h2>
      <div className="room-section__grid">
        {rooms.map(room => (
          <RoomControlPanel key={room.id} room={room} />
        ))}
        <KitchenControl />
      </div>
    </div>
  );
}
