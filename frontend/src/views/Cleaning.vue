<template>
  <div class="cleaning">
    <div class="page-header">
      <h1 class="page-title">Cleaning Management</h1>
      <button class="btn-refresh" @click="loadCleaningRooms">Refresh</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else class="cleaning-content">
      <div class="cleaning-stats">
        <div class="stat-card">
          <div class="stat-icon">🧹</div>
          <div class="stat-info">
            <div class="stat-value">{{ cleaningRooms.length }}</div>
            <div class="stat-label">Rooms Need Cleaning</div>
          </div>
        </div>
      </div>

      <div v-if="cleaningRooms.length === 0" class="empty-state">
        No rooms need cleaning at the moment.
      </div>
      
      <div v-else class="cleaning-rooms">
        <div
          v-for="room in cleaningRooms"
          :key="room.id"
          class="cleaning-room-card"
        >
          <div class="room-header">
            <h3>Room {{ room.room_number }}</h3>
            <span class="room-type">{{ room.room_type }}</span>
          </div>
          <div class="room-details">
            <div class="detail-item">
              <span class="detail-label">Max Guests:</span>
              <span>{{ room.max_guests }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Price per Night:</span>
              <span>${{ formatPrice(room.price_per_night) }}</span>
            </div>
          </div>
          <button class="btn-complete" @click="completeCleaning(room.id)">
            Mark as Cleaned
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'Cleaning',
  data() {
    return {
      loading: true,
      cleaningRooms: []
    }
  },
  async mounted() {
    await this.loadCleaningRooms()
  },
  methods: {
    async loadCleaningRooms() {
      try {
        this.loading = true
        const response = await api.getCleaningRooms()
        this.cleaningRooms = response.data.cleaning_rooms || []
      } catch (error) {
        console.error('Failed to load cleaning rooms:', error)
        alert('Failed to load cleaning rooms')
      } finally {
        this.loading = false
      }
    },
    async completeCleaning(roomId) {
      if (!confirm('Mark this room as cleaned?')) return
      
      try {
        await api.completeCleaning(roomId)
        alert('Room marked as cleaned successfully')
        await this.loadCleaningRooms()
      } catch (error) {
        alert('Failed to update room status')
      }
    },
    formatPrice(price) {
      return new Intl.NumberFormat('en-US').format(price)
    }
  }
}
</script>

<style scoped>
.cleaning {
  padding: 2rem 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  color: #333;
}

.btn-refresh {
  padding: 0.75rem 1.5rem;
  background: #f5f5f5;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
}

.cleaning-stats {
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.stat-icon {
  font-size: 3rem;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #667eea;
}

.stat-label {
  font-size: 1rem;
  color: #666;
  margin-top: 0.25rem;
}

.cleaning-rooms {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.cleaning-room-card {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-left: 4px solid #2196f3;
}

.room-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.room-header h3 {
  font-size: 1.3rem;
  color: #333;
}

.room-type {
  padding: 0.25rem 0.75rem;
  background: #e3f2fd;
  color: #1976d2;
  border-radius: 20px;
  font-size: 0.85rem;
}

.room-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
}

.detail-label {
  font-weight: 500;
  color: #666;
}

.btn-complete {
  width: 100%;
  padding: 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: transform 0.2s;
}

.btn-complete:hover {
  transform: translateY(-2px);
}

.empty-state, .loading {
  text-align: center;
  padding: 3rem;
  color: #999;
  background: white;
  border-radius: 10px;
}
</style>







