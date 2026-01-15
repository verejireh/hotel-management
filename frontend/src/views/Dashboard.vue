<template>
  <div class="dashboard">
    <h1 class="page-title">Dashboard</h1>
    
    <!-- 알림 섹션 -->
    <div v-if="upcomingAlerts.length > 0 || roomAlerts.urgent.length > 0 || roomAlerts.afterCheckout.length > 0" class="alerts-section">
      <!-- 긴급 알람 -->
      <div v-if="roomAlerts.urgent.length > 0" class="alert-category">
        <h2 class="section-title">🚨 Urgent Room Notes</h2>
        <div class="alerts-list">
          <div v-for="alert in roomAlerts.urgent" :key="alert.id" class="alert-item urgent">
            <div class="alert-icon">⚠️</div>
            <div class="alert-content">
              <div class="alert-title">{{ alert.title }} - Room {{ getRoomNumber(alert.room_id) }}</div>
              <div class="alert-details">{{ alert.description }}</div>
              <div class="alert-meta">Created: {{ formatDate(alert.created_at) }}</div>
            </div>
            <button class="btn-complete-alert" @click="completeNote(alert.id)">Complete</button>
          </div>
        </div>
      </div>

      <!-- 체크아웃 후 알람 -->
      <div v-if="roomAlerts.afterCheckout.length > 0" class="alert-category">
        <h2 class="section-title">📋 After Checkout Tasks</h2>
        <div class="alerts-list">
          <div v-for="alert in roomAlerts.afterCheckout" :key="alert.id" class="alert-item after-checkout">
            <div class="alert-icon">📝</div>
            <div class="alert-content">
              <div class="alert-title">{{ alert.title }} - Room {{ getRoomNumber(alert.room_id) }}</div>
              <div class="alert-details">{{ alert.description }}</div>
              <div class="alert-meta">Created: {{ formatDate(alert.created_at) }}</div>
            </div>
            <button class="btn-complete-alert" @click="completeNote(alert.id)">Complete</button>
          </div>
        </div>
      </div>

      <!-- 예정된 체크인/체크아웃 -->
      <div v-if="upcomingAlerts.length > 0" class="alert-category">
        <h2 class="section-title">⚠️ Upcoming Check-ins/Check-outs</h2>
        <div class="alerts-list">
          <div v-for="alert in upcomingAlerts" :key="alert.id" class="alert-item" :class="alert.type">
            <div class="alert-icon">{{ alert.type === 'checkin' ? '🔑' : '🚪' }}</div>
            <div class="alert-content">
              <div class="alert-title">{{ alert.type === 'checkin' ? 'Check-in' : 'Check-out' }} - Room {{ getRoomNumber(alert.room_id) }}</div>
              <div class="alert-details">{{ formatDate(alert.date) }} - {{ getCustomerName(alert.customer_id) }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 노트 섹션 -->
    <div class="notes-section">
      <div class="section-header">
        <h2 class="section-title">📝 Notes</h2>
        <div class="filter-controls">
          <label>Filter by Progress:</label>
          <select v-model="progressFilter" @change="loadNotes">
            <option :value="null">All notes</option>
            <option value="">No progress</option>
            <option value="confirm">Confirm</option>
            <option value="In progress">In progress</option>
            <option value="finished">Finished</option>
          </select>
        </div>
      </div>
      <div v-if="notesLoading" class="loading">Loading notes...</div>
      <div v-else-if="filteredNotes.length === 0" class="empty-state">
        No notes found. (Total notes: {{ notes.length }}, Filter: {{ progressFilter }})
      </div>
      <div v-else class="notes-list">
        <div v-for="note in filteredNotes" :key="note.id" class="note-item">
          <div class="note-header">
            <span class="note-title">{{ note.title }}</span>
            <span class="note-type-badge" :class="note.note_type">
              {{ note.note_type === 'urgent' ? 'Urgent' : 'After Checkout' }}
            </span>
          </div>
          <div class="note-details">
            <div class="note-info">
              <span>Room: {{ getRoomNumber(note.room_id) }}</span>
              <span v-if="note.progress" class="progress-badge" :class="getProgressClass(note.progress)">
                {{ note.progress }}
              </span>
            </div>
            <div class="note-description">{{ note.description }}</div>
            <div class="note-actions">
              <select v-model="note.progress" @change="updateNoteProgress(note.id, note.progress)" class="progress-select">
                <option value="">No progress</option>
                <option value="confirm">Confirm</option>
                <option value="In progress">In progress</option>
                <option value="finished">Finished</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 통계 카드 -->
    <div class="stats-grid" v-if="stats">
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.total_reservations }}</div>
          <div class="stat-label">Total Reservations</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.active_reservations }}</div>
          <div class="stat-label">Active Reservations</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🛏️</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.available_rooms }} / {{ stats.total_rooms }}</div>
          <div class="stat-label">Available Rooms</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📈</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.occupancy_rate }}%</div>
          <div class="stat-label">Occupancy Rate</div>
        </div>
      </div>
    </div>

    <!-- 오늘의 체크인/체크아웃 -->
    <div class="checkin-out-section">
      <div class="checkin-out-card">
        <h2 class="section-title">
          <span class="title-icon">🔑</span>
          Today's Check-ins ({{ summary?.check_ins?.length || 0 }})
        </h2>
        <div v-if="loading" class="loading">Loading...</div>
        <div v-else-if="summary?.check_ins?.length === 0" class="empty-state">
          No check-ins scheduled for today.
        </div>
        <div v-else class="reservation-list">
          <div 
            v-for="reservation in summary?.check_ins" 
            :key="reservation.id"
            class="reservation-item"
          >
            <div class="reservation-header">
              <span class="room-number">Room {{ getRoomNumber(reservation.room_id) }}</span>
              <span class="status-badge" :class="reservation.status">
                {{ getStatusText(reservation.status) }}
              </span>
            </div>
            <div class="reservation-details">
              <div class="detail-item">
                <span class="detail-label">Customer:</span>
                <span>{{ getCustomerName(reservation.customer_id) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Check-in:</span>
                <span>{{ formatDate(reservation.check_in) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Check-out:</span>
                <span>{{ formatDate(reservation.check_out) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Guests:</span>
                <span>{{ reservation.guests }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Booking Ref:</span>
                <span>{{ reservation.booking_reference }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="checkin-out-card">
        <h2 class="section-title">
          <span class="title-icon">🚪</span>
          Today's Check-outs ({{ summary?.check_outs?.length || 0 }})
        </h2>
        <div v-if="loading" class="loading">Loading...</div>
        <div v-else-if="summary?.check_outs?.length === 0" class="empty-state">
          No check-outs scheduled for today.
        </div>
        <div v-else class="reservation-list">
          <div 
            v-for="reservation in summary?.check_outs" 
            :key="reservation.id"
            class="reservation-item"
          >
            <div class="reservation-header">
              <span class="room-number">Room {{ getRoomNumber(reservation.room_id) }}</span>
              <span class="status-badge" :class="reservation.status">
                {{ getStatusText(reservation.status) }}
              </span>
            </div>
            <div class="reservation-details">
              <div class="detail-item">
                <span class="detail-label">Customer:</span>
                <span>{{ getCustomerName(reservation.customer_id) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Check-in:</span>
                <span>{{ formatDate(reservation.check_in) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Check-out:</span>
                <span>{{ formatDate(reservation.check_out) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Guests:</span>
                <span>{{ reservation.guests }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Booking Ref:</span>
                <span>{{ reservation.booking_reference }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'Dashboard',
  data() {
    return {
      loading: true,
      stats: null,
      summary: null,
      rooms: [],
      customers: [],
      upcomingAlerts: [],
      roomAlerts: {
        urgent: [],
        afterCheckout: []
      },
      notesLoading: false,
      notes: [],
      progressFilter: null // 기본값: 모든 노트 표시
    }
  },
  computed: {
    filteredNotes() {
      return this.notes
    }
  },
  async mounted() {
    console.log('Dashboard mounted')
    try {
      await this.loadData()
      await this.loadAlerts()
      await this.loadRoomAlerts()
      await this.loadNotes()
      
      // 노트 추가 이벤트 리스너
      window.addEventListener('note-added', this.handleNoteAdded)
      console.log('Dashboard initialization complete')
    } catch (error) {
      console.error('Dashboard initialization error:', error)
    }
  },
  beforeUnmount() {
    window.removeEventListener('note-added', this.handleNoteAdded)
  },
  methods: {
    async loadData() {
      try {
        this.loading = true
        console.log('Loading dashboard data...')
        // 순차적으로 로드하여 타임아웃 방지 (Google Sheets API는 느릴 수 있음)
        const statsRes = await api.getDashboardStats().catch(err => {
          console.warn('Failed to load stats:', err)
          return { data: null }
        })
        const summaryRes = await api.getCheckInOutSummary().catch(err => {
          console.warn('Failed to load summary:', err)
          return { data: null }
        })
        const roomsRes = await api.getRooms().catch(err => {
          console.warn('Failed to load rooms:', err)
          return { data: [] }
        })
        
        console.log('Data loaded:', { stats: statsRes.data, summary: summaryRes.data, rooms: roomsRes.data })
        this.stats = statsRes.data
        this.summary = summaryRes.data
        this.rooms = roomsRes.data || []
      } catch (error) {
        console.error('Failed to load data:', error)
        console.error('Error details:', error.response || error.message)
        // alert 대신 콘솔 로그만 (사용자 경험 개선)
        if (error.code === 'ECONNABORTED') {
          console.error('Request timeout - Google Sheets API가 느립니다. 잠시 후 다시 시도해주세요.')
        }
        // 기본값 설정
        this.stats = null
        this.summary = null
        this.rooms = []
      } finally {
        this.loading = false
      }
    },
    async loadAlerts() {
      try {
        const response = await api.getUpcomingCheckinsCheckouts(7)
        const checkins = response.data.upcoming_checkins || []
        const checkouts = response.data.upcoming_checkouts || []
        
        this.upcomingAlerts = [
          ...checkins.map(r => ({ ...r, type: 'checkin', date: r.check_in })),
          ...checkouts.map(r => ({ ...r, type: 'checkout', date: r.check_out }))
        ].sort((a, b) => new Date(a.date) - new Date(b.date))
      } catch (error) {
        console.error('Failed to load alerts:', error)
      }
    },
    async loadRoomAlerts() {
      try {
        const response = await api.getAllAlerts()
        this.roomAlerts.urgent = response.data.urgent_notes || []
        this.roomAlerts.afterCheckout = response.data.after_checkout_notes || []
      } catch (error) {
        console.error('Failed to load room alerts:', error)
      }
    },
    async completeNote(noteId) {
      if (!confirm('Mark this note as completed?')) return
      
      try {
        await api.completeRoomNote(noteId)
        await this.loadRoomAlerts()
      } catch (error) {
        alert('Failed to complete note')
      }
    },
    handleNoteAdded() {
      // 노트 추가 후 알람 새로고침
      this.loadRoomAlerts()
      this.loadNotes()
    },
    async loadNotes() {
      try {
        this.notesLoading = true
        console.log('Dashboard: Loading notes with filter:', this.progressFilter)
        // progressFilter가 null이면 undefined로 전달 (모든 노트), 빈 문자열이면 빈 문자열로 전달 (progress 없는 노트만)
        let progressParam = undefined
        if (this.progressFilter === '') {
          progressParam = ''
        } else if (this.progressFilter !== null) {
          progressParam = this.progressFilter
        }
        console.log('Dashboard: Calling API with progressParam:', progressParam)
        const response = await api.getRoomNotes(null, progressParam)
        console.log('Dashboard: API response:', response)
        console.log('Dashboard: Notes data:', response.data)
        console.log('Dashboard: Number of notes:', response.data?.length || 0)
        this.notes = response.data || []
        console.log('Dashboard: Notes set to:', this.notes)
        console.log('Dashboard: Notes length:', this.notes.length)
        console.log('Dashboard: filteredNotes computed:', this.filteredNotes)
        console.log('Dashboard: filteredNotes length:', this.filteredNotes.length)
        
        // 디버깅: 각 노트의 내용 확인
        if (this.notes.length > 0) {
          console.log('Dashboard: First note:', this.notes[0])
        } else {
          console.warn('Dashboard: No notes in array!')
        }
      } catch (error) {
        console.error('Dashboard: Failed to load notes:', error)
        console.error('Dashboard: Error details:', error.response || error.message)
        if (error.response) {
          console.error('Dashboard: Error response data:', error.response.data)
          console.error('Dashboard: Error response status:', error.response.status)
        }
        this.notes = []
      } finally {
        this.notesLoading = false
      }
    },
    async updateNoteProgress(noteId, progress) {
      try {
        await api.updateNoteProgress(noteId, progress)
        await this.loadNotes()
      } catch (error) {
        alert('Failed to update note progress')
        console.error(error)
      }
    },
    getProgressClass(progress) {
      const classMap = {
        'confirm': 'progress-confirm',
        'In progress': 'progress-in-progress',
        'finished': 'progress-finished'
      }
      return classMap[progress] || ''
    },
    getRoomNumber(roomId) {
      const room = this.rooms.find(r => r.id === roomId)
      return room ? room.room_number : roomId
    },
    getCustomerName(customerId) {
      // 실제로는 customers API를 호출해야 하지만, 간단히 ID만 표시
      return `Customer #${customerId}`
    },
    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toLocaleDateString('en-US')
    },
    getStatusText(status) {
      const statusMap = {
        'confirmed': 'Confirmed',
        'checked_in': 'Checked In',
        'checked_out': 'Checked Out',
        'cancelled': 'Cancelled'
      }
      return statusMap[status] || status
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 2rem 0;
}

.page-title {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #333;
}

.alerts-section {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.alerts-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 1rem;
}

.alert-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid;
}

.alert-item.checkin {
  background: #e3f2fd;
  border-left-color: #2196f3;
}

.alert-item.checkout {
  background: #fff3e0;
  border-left-color: #ff9800;
}

.alert-item.urgent {
  background: #ffebee;
  border-left-color: #f44336;
}

.alert-item.after-checkout {
  background: #e8f5e9;
  border-left-color: #4caf50;
}

.alert-category {
  margin-bottom: 2rem;
}

.alert-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid;
}

.alert-meta {
  font-size: 0.85rem;
  color: #999;
  margin-top: 0.25rem;
}

.btn-complete-alert {
  padding: 0.5rem 1rem;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.85rem;
  margin-left: auto;
}

.btn-complete-alert:hover {
  background: #388e3c;
}

.alert-icon {
  font-size: 1.5rem;
}

.alert-content {
  flex: 1;
}

.alert-title {
  font-weight: 600;
  color: #333;
  margin-bottom: 0.25rem;
}

.alert-details {
  font-size: 0.9rem;
  color: #666;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.stat-icon {
  font-size: 2.5rem;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #667eea;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.25rem;
}

.checkin-out-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 2rem;
}

.checkin-out-card {
  background: white;
  border-radius: 10px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.section-title {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: #333;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.title-icon {
  font-size: 1.5rem;
}

.loading, .empty-state {
  text-align: center;
  padding: 2rem;
  color: #999;
}

.reservation-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.reservation-item {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  transition: box-shadow 0.2s;
}

.reservation-item:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.reservation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #f0f0f0;
}

.room-number {
  font-weight: 600;
  font-size: 1.1rem;
  color: #667eea;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.status-badge.confirmed {
  background-color: #e3f2fd;
  color: #1976d2;
}

.status-badge.checked_in {
  background-color: #e8f5e9;
  color: #388e3c;
}

.status-badge.checked_out {
  background-color: #fff3e0;
  color: #f57c00;
}

.reservation-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
}

.detail-item {
  display: flex;
  gap: 0.5rem;
}

.detail-label {
  font-weight: 500;
  color: #666;
}

/* Notes Section */
.notes-section {
  background: white;
  border-radius: 10px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.filter-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-controls label {
  font-weight: 500;
  color: #666;
}

.filter-controls select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 0.9rem;
}

.notes-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.note-item {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  transition: box-shadow 0.2s;
}

.note-item:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.note-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #f0f0f0;
}

.note-title {
  font-weight: 600;
  font-size: 1.1rem;
  color: #333;
}

.note-type-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.note-type-badge.urgent {
  background-color: #ffebee;
  color: #c62828;
}

.note-type-badge.after_checkout {
  background-color: #e3f2fd;
  color: #1565c0;
}

.note-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.note-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  color: #666;
}

.progress-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.progress-confirm {
  background-color: #fff3e0;
  color: #e65100;
}

.progress-in-progress {
  background-color: #e3f2fd;
  color: #1565c0;
}

.progress-finished {
  background-color: #e8f5e9;
  color: #388e3c;
}

.note-description {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.5;
}

.note-actions {
  margin-top: 0.75rem;
}

.progress-select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 0.9rem;
  cursor: pointer;
}

@media (max-width: 768px) {
  .checkin-out-section {
    grid-template-columns: 1fr;
  }
  
  .reservation-details {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}
</style>

