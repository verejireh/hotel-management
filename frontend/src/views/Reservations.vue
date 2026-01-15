<template>
  <div class="reservations">
    <div class="page-header">
      <h1 class="page-title">Reservations</h1>
      <button class="btn-primary" @click="showAddModal = true">
        + New Reservation
      </button>
    </div>

    <!-- 필터 섹션 -->
    <div class="filter-section">
      <div class="filter-group">
        <label>Start Date:</label>
        <input type="date" v-model="filterStartDate" @change="applyFilters" />
      </div>
      <div class="filter-group">
        <label>End Date:</label>
        <input type="date" v-model="filterEndDate" @change="applyFilters" />
      </div>
      <div class="filter-group">
        <label>Status:</label>
        <select v-model="filterStatus" @change="applyFilters">
          <option value="">All reservations</option>
          <option value="Reserved">Reserved</option>
          <option value="Checked in">Checked in</option>
          <option value="Checked out">Checked out</option>
        </select>
      </div>
      <button class="btn-clear-filter" @click="clearFilters">Clear Filters</button>
    </div>

    <!-- 예약 목록 -->
    <div class="reservations-list" v-if="!loading">
      <div 
        v-for="reservation in filteredReservations" 
        :key="reservation.id"
        class="reservation-card"
      >
        <div class="reservation-card-header">
          <div>
            <span class="room-number">Room {{ getRoomNumber(reservation.room_id) }}</span>
            <span class="booking-ref">Booking Ref: {{ reservation.booking_reference }}</span>
          </div>
          <span class="status-badge" :class="getStatusClass(reservation.status)">
            {{ getStatusText(reservation.status) }}
          </span>
        </div>
        <div class="reservation-card-body">
          <div class="info-row">
            <span class="info-label">Customer:</span>
            <span>{{ getCustomerName(reservation.customer_id) }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">Check-in:</span>
            <span>{{ formatDate(reservation.check_in) }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">Check-out:</span>
            <span>{{ formatDate(reservation.check_out) }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">Guests:</span>
            <span>{{ reservation.guests }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">Total Price:</span>
            <span class="price">${{ formatPrice(reservation.total_price) }}</span>
          </div>
          <div class="info-row" v-if="reservation.notes">
            <span class="info-label">Notes:</span>
            <span>{{ reservation.notes }}</span>
          </div>
        </div>
        <div class="reservation-actions">
          <div class="status-toggle-group">
            <button
              class="status-toggle-btn"
              :class="{ active: reservation.status === 'Reserved' }"
              @click="updateStatus(reservation.id, 'Reserved')"
            >
              Reserved
            </button>
            <button
              class="status-toggle-btn"
              :class="{ active: reservation.status === 'Checked in' }"
              @click="updateStatus(reservation.id, 'Checked in')"
            >
              Checked in
            </button>
            <button
              class="status-toggle-btn"
              :class="{ active: reservation.status === 'Checked out' }"
              @click="updateStatus(reservation.id, 'Checked out')"
            >
              Checked out
            </button>
          </div>
        </div>
      </div>
      
      <div v-if="filteredReservations.length === 0" class="empty-state">
        No reservations found.
      </div>
    </div>

    <div v-else class="loading">Loading...</div>

    <!-- 예약 추가 모달 -->
    <div v-if="showAddModal" class="modal-overlay" @click="showAddModal = false">
      <div class="modal-content" @click.stop>
        <h2>New Reservation</h2>
        <form @submit.prevent="handleAddReservation">
          <div class="form-group">
            <label>Select Room</label>
            <select v-model="newReservation.room_id" required>
              <option value="">Please select a room</option>
              <option v-for="room in rooms" :key="room.id" :value="room.id">
                {{ room.room_number }} ({{ room.room_type }})
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Check-in Date</label>
            <input type="date" v-model="newReservation.check_in" required />
          </div>
          <div class="form-group">
            <label>Check-out Date</label>
            <input type="date" v-model="newReservation.check_out" required />
          </div>
          <div class="form-group">
            <label>Number of Guests</label>
            <input type="number" v-model.number="newReservation.guests" min="1" required />
          </div>
          <div class="form-group">
            <label>Total Price</label>
            <input type="number" v-model.number="newReservation.total_price" min="0" required />
          </div>
          <div class="form-group">
            <label>Booking Reference (External Platform)</label>
            <input type="text" v-model="newReservation.booking_reference" required />
          </div>
          <div class="form-group">
            <label>Notes</label>
            <textarea v-model="newReservation.notes" rows="3"></textarea>
          </div>
          <div class="form-actions">
            <button type="button" class="btn-secondary" @click="showAddModal = false">Cancel</button>
            <button type="submit" class="btn-primary">Add</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'Reservations',
  data() {
    return {
      loading: true,
      reservations: [],
      rooms: [],
      showAddModal: false,
      filterStartDate: '',
      filterEndDate: '',
      filterStatus: '', // 기본값: 모든 예약 표시
      newReservation: {
        customer_id: '1', // 임시로 고정, 실제로는 선택해야 함
        room_id: '',
        platform_id: '1', // 임시로 고정
        check_in: '',
        check_out: '',
        guests: 1,
        total_price: 0,
        booking_reference: '',
        notes: '',
        status: 'Reserved' // 기본값
      }
    }
  },
  computed: {
    filteredReservations() {
      let filtered = [...this.reservations]
      
      // Status 필터링
      if (this.filterStatus) {
        filtered = filtered.filter(r => r.status === this.filterStatus)
      }
      
      // 날짜 필터링 (날짜가 입력된 경우에만)
      if (this.filterStartDate) {
        const startDate = new Date(this.filterStartDate)
        startDate.setHours(0, 0, 0, 0) // 시간 초기화
        filtered = filtered.filter(r => {
          const checkIn = new Date(r.check_in)
          checkIn.setHours(0, 0, 0, 0)
          return checkIn >= startDate
        })
      }
      
      if (this.filterEndDate) {
        const endDate = new Date(this.filterEndDate)
        endDate.setHours(23, 59, 59, 999) // 하루 끝 시간으로 설정
        filtered = filtered.filter(r => {
          const checkIn = new Date(r.check_in)
          checkIn.setHours(0, 0, 0, 0)
          return checkIn <= endDate
        })
      }
      
      return filtered
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      try {
        this.loading = true
        console.log('Loading reservations data...')
        const [reservationsRes, roomsRes] = await Promise.all([
          api.getReservations(),
          api.getRooms()
        ])
        
        console.log('Reservations loaded:', reservationsRes.data)
        this.reservations = reservationsRes.data || []
        this.rooms = roomsRes.data || []
      } catch (error) {
        console.error('Failed to load data:', error)
        console.error('Error details:', error.response || error.message)
        alert(`An error occurred while loading data: ${error.message || 'Unknown error'}`)
        this.reservations = []
        this.rooms = []
      } finally {
        this.loading = false
      }
    },
    async handleAddReservation() {
      try {
        await api.createReservation(this.newReservation)
        alert('Reservation added successfully.')
        this.showAddModal = false
        this.resetForm()
        await this.loadData()
      } catch (error) {
        if (error.response?.status === 400) {
          alert(error.response.data.detail || 'Failed to add reservation. Room may be already booked.')
        } else {
          alert('An error occurred while adding reservation.')
        }
      }
    },
    resetForm() {
      this.newReservation = {
        customer_id: '1',
        room_id: '',
        platform_id: '1',
        check_in: '',
        check_out: '',
        guests: 1,
        total_price: 0,
        booking_reference: '',
        notes: '',
        status: 'Reserved'
      }
    },
    getRoomNumber(roomId) {
      const room = this.rooms.find(r => r.id === roomId)
      return room ? room.room_number : roomId
    },
    getCustomerName(customerId) {
      return `Customer #${customerId}`
    },
    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toLocaleDateString('en-US')
    },
    formatPrice(price) {
      return new Intl.NumberFormat('en-US').format(price)
    },
    getStatusText(status) {
      return status || 'Reserved'
    },
    getStatusClass(status) {
      const statusMap = {
        'Reserved': 'status-reserved',
        'Checked in': 'status-checked-in',
        'Checked out': 'status-checked-out'
      }
      return statusMap[status] || 'status-reserved'
    },
    async updateStatus(reservationId, newStatus) {
      try {
        console.log('Updating status:', reservationId, newStatus)
        const response = await api.updateReservationStatus(reservationId, newStatus)
        console.log('Status updated successfully:', response.data)
        await this.loadData()
      } catch (error) {
        console.error('Failed to update status:', error)
        console.error('Error details:', error.response?.data || error.message)
        const errorMessage = error.response?.data?.detail || error.message || 'Failed to update status'
        alert(`Failed to update status: ${errorMessage}`)
      }
    },
    applyFilters() {
      // computed 속성이 자동으로 업데이트됨
    },
    clearFilters() {
      this.filterStartDate = ''
      this.filterEndDate = ''
      this.filterStatus = ''
    }
  }
}
</script>

<style scoped>
.reservations {
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

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: transform 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.reservations-list {
  display: grid;
  gap: 1.5rem;
}

.reservation-card {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: box-shadow 0.2s;
}

.reservation-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.reservation-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.room-number {
  font-weight: 600;
  font-size: 1.2rem;
  color: #667eea;
  margin-right: 1rem;
}

.booking-ref {
  color: #666;
  font-size: 0.9rem;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.status-badge.status-reserved {
  background-color: #f44336;
  color: white;
}

.status-badge.status-checked-in {
  background-color: #2196f3;
  color: white;
}

.status-badge.status-checked-out {
  background-color: #4caf50;
  color: white;
}

.reservation-card-body {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.reservation-actions {
  display: flex;
  gap: 0.5rem;
  padding-top: 1rem;
  border-top: 1px solid #f0f0f0;
}

.status-toggle-group {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.status-toggle-btn {
  padding: 0.5rem 1rem;
  border: 2px solid #ddd;
  border-radius: 5px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  background: white;
  color: #666;
}

.status-toggle-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.status-toggle-btn.active {
  color: white;
  border-color: transparent;
}

.status-toggle-btn:first-child.active {
  background: #f44336; /* Red */
}

.status-toggle-btn:nth-child(2).active {
  background: #2196f3; /* Blue */
}

.status-toggle-btn:nth-child(3).active {
  background: #4caf50; /* Green */
}

.info-row {
  display: flex;
  gap: 0.5rem;
}

.info-label {
  font-weight: 500;
  color: #666;
  min-width: 80px;
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

/* 필터 섹션 */
.filter-section {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 1.5rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 500;
  color: #333;
  font-size: 0.9rem;
}

.filter-group input[type="date"] {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 0.9rem;
}

.filter-group input[type="checkbox"] {
  margin-right: 0.5rem;
}

.btn-clear-filter {
  background: #f5f5f5;
  color: #333;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  font-weight: 500;
  cursor: pointer;
  margin-left: auto;
}

.btn-clear-filter:hover {
  background: #e0e0e0;
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 10px;
  padding: 2rem;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-content h2 {
  margin-bottom: 1.5rem;
  color: #333;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.btn-secondary {
  background: #f5f5f5;
  color: #333;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
}

.btn-secondary:hover {
  background: #e0e0e0;
}
</style>

