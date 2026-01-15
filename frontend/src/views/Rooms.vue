<template>
  <div class="rooms">
    <h1 class="page-title">Rooms</h1>
    
    <div class="rooms-grid" v-if="!loading">
      <div 
        v-for="room in rooms" 
        :key="room.id"
        class="room-card"
        :class="room.status"
      >
        <div class="room-card-header">
          <h3 class="room-number">Room {{ room.room_number }}</h3>
          <span class="status-badge" :class="room.status">
            {{ getStatusText(room.status) }}
          </span>
        </div>
        <div class="room-card-body">
          <div class="room-info">
            <div class="info-item">
              <span class="info-label">Type:</span>
              <span>{{ room.room_type }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Max Guests:</span>
              <span>{{ room.max_guests }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Price per Night:</span>
              <span class="price">${{ formatPrice(room.price_per_night) }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="rooms.length === 0" class="empty-state">
        No rooms found.
      </div>
    </div>

    <div v-else class="loading">Loading...</div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'Rooms',
  data() {
    return {
      loading: true,
      rooms: []
    }
  },
  async mounted() {
    await this.loadRooms()
  },
  methods: {
    async loadRooms() {
      try {
        this.loading = true
        const response = await api.getRooms()
        this.rooms = response.data
      } catch (error) {
        console.error('Failed to load room data:', error)
        alert('An error occurred while loading room data.')
      } finally {
        this.loading = false
      }
    },
    formatPrice(price) {
      return new Intl.NumberFormat('en-US').format(price)
    },
    getStatusText(status) {
      const statusMap = {
        'available': 'Available',
        'occupied': 'Occupied',
        'maintenance': 'Maintenance',
        'cleaning': 'Cleaning'
      }
      return statusMap[status] || status
    }
  }
}
</script>

<style scoped>
.rooms {
  padding: 2rem 0;
}

.page-title {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #333;
}

.rooms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.room-card {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  border-left: 4px solid #ddd;
}

.room-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.room-card.available {
  border-left-color: #4caf50;
}

.room-card.occupied {
  border-left-color: #f44336;
}

.room-card.maintenance {
  border-left-color: #ff9800;
}

.room-card.cleaning {
  border-left-color: #2196f3;
}

.room-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.room-number {
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.status-badge.available {
  background-color: #e8f5e9;
  color: #388e3c;
}

.status-badge.occupied {
  background-color: #ffebee;
  color: #c62828;
}

.status-badge.maintenance {
  background-color: #fff3e0;
  color: #e65100;
}

.status-badge.cleaning {
  background-color: #e3f2fd;
  color: #1565c0;
}

.room-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
}

.info-label {
  font-weight: 500;
  color: #666;
}

.price {
  font-weight: 600;
  color: #667eea;
  font-size: 1.1rem;
}

.empty-state, .loading {
  text-align: center;
  padding: 3rem;
  color: #999;
  background: white;
  border-radius: 10px;
}
</style>

