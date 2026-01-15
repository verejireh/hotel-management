<template>
  <div class="customers">
    <div class="page-header">
      <h1 class="page-title">Customers</h1>
      <button class="btn-primary" @click="showAddModal = true">+ New Customer</button>
    </div>

    <!-- 필터 섹션 -->
    <div class="filter-section">
      <div class="filter-group">
        <label>Name:</label>
        <input type="text" v-model="filterName" @input="applyFilters" placeholder="Search by name..." />
      </div>
      <div class="filter-group">
        <label>Email:</label>
        <input type="text" v-model="filterEmail" @input="applyFilters" placeholder="Search by email..." />
      </div>
      <div class="filter-group">
        <label>Phone:</label>
        <input type="text" v-model="filterPhone" @input="applyFilters" placeholder="Search by phone..." />
      </div>
      <button class="btn-clear-filter" @click="clearFilters">Clear Filters</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else class="customers-list">
      <div v-for="customer in filteredCustomers" :key="customer.id" class="customer-card" @click="viewCustomer(customer.id)">
        <div class="customer-header">
          <h3>{{ customer.name }}</h3>
          <span class="customer-id">ID: {{ customer.id }}</span>
        </div>
        <div class="customer-details">
          <div v-if="customer.email" class="detail-item">
            <span class="detail-icon">📧</span>
            <span>{{ customer.email }}</span>
          </div>
          <div v-if="customer.phone" class="detail-item">
            <span class="detail-icon">📞</span>
            <span>{{ customer.phone }}</span>
          </div>
          <div v-if="customer.nationality" class="detail-item">
            <span class="detail-icon">🌍</span>
            <span>{{ customer.nationality }}</span>
          </div>
        </div>
      </div>
      
      <div v-if="filteredCustomers.length === 0" class="empty-state">No customers found.</div>
    </div>

    <!-- Customer Detail Modal -->
    <div v-if="selectedCustomer" class="modal-overlay" @click="selectedCustomer = null">
      <div class="modal-content" @click.stop>
        <h2>Customer Details</h2>
        <div class="customer-info">
          <div class="info-row">
            <span class="info-label">Name:</span>
            <span>{{ selectedCustomer.name }}</span>
          </div>
          <div class="info-row" v-if="selectedCustomer.email">
            <span class="info-label">Email:</span>
            <span>{{ selectedCustomer.email }}</span>
          </div>
          <div class="info-row" v-if="selectedCustomer.phone">
            <span class="info-label">Phone:</span>
            <span>{{ selectedCustomer.phone }}</span>
          </div>
          <div class="info-row" v-if="selectedCustomer.nationality">
            <span class="info-label">Nationality:</span>
            <span>{{ selectedCustomer.nationality }}</span>
          </div>
        </div>
        
        <h3 style="margin-top: 2rem; margin-bottom: 1rem;">Reservation History</h3>
        <div v-if="customerReservations.length === 0" class="empty-state">No reservations</div>
        <div v-else class="reservations-list">
          <div v-for="res in customerReservations" :key="res.id" class="reservation-item">
            <div class="res-header">
              <span>Room {{ getRoomNumber(res.room_id) }}</span>
              <span class="status-badge" :class="res.status">{{ getStatusText(res.status) }}</span>
            </div>
            <div class="res-details">
              <span>{{ formatDate(res.check_in) }} - {{ formatDate(res.check_out) }}</span>
              <span>${{ formatPrice(res.total_price) }}</span>
            </div>
          </div>
        </div>
        
        <div class="modal-actions">
          <button class="btn-secondary" @click="selectedCustomer = null">Close</button>
        </div>
      </div>
    </div>

    <!-- Add Customer Modal -->
    <div v-if="showAddModal" class="modal-overlay" @click="showAddModal = false">
      <div class="modal-content" @click.stop>
        <h2>New Customer</h2>
        <form @submit.prevent="handleAddCustomer">
          <div class="form-group">
            <label>Name *</label>
            <input type="text" v-model="newCustomer.name" required />
          </div>
          <div class="form-group">
            <label>Email</label>
            <input type="email" v-model="newCustomer.email" />
          </div>
          <div class="form-group">
            <label>Phone</label>
            <input type="tel" v-model="newCustomer.phone" />
          </div>
          <div class="form-group">
            <label>Nationality</label>
            <input type="text" v-model="newCustomer.nationality" />
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
  name: 'Customers',
  data() {
    return {
      loading: true,
      customers: [],
      rooms: [],
      selectedCustomer: null,
      customerReservations: [],
      showAddModal: false,
      filterName: '',
      filterEmail: '',
      filterPhone: '',
      newCustomer: {
        name: '',
        email: '',
        phone: '',
        nationality: ''
      }
    }
  },
  computed: {
    filteredCustomers() {
      let filtered = [...this.customers]
      
      if (this.filterName) {
        const nameLower = this.filterName.toLowerCase()
        filtered = filtered.filter(c => 
          c.name && c.name.toLowerCase().includes(nameLower)
        )
      }
      
      if (this.filterEmail) {
        const emailLower = this.filterEmail.toLowerCase()
        filtered = filtered.filter(c => 
          c.email && c.email.toLowerCase().includes(emailLower)
        )
      }
      
      if (this.filterPhone) {
        const phoneLower = this.filterPhone.toLowerCase()
        filtered = filtered.filter(c => 
          c.phone && c.phone.toLowerCase().includes(phoneLower)
        )
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
        console.log('Loading customers data...')
        const [customersRes, roomsRes] = await Promise.all([
          api.getCustomers(),
          api.getRooms()
        ])
        console.log('Customers loaded:', customersRes.data)
        this.customers = customersRes.data || []
        this.rooms = roomsRes.data || []
      } catch (error) {
        console.error('Failed to load customers:', error)
        console.error('Error details:', error.response || error.message)
        alert(`Failed to load customers: ${error.message || 'Unknown error'}`)
        this.customers = []
        this.rooms = []
      } finally {
        this.loading = false
      }
    },
    async viewCustomer(customerId) {
      try {
        const [customerRes, reservationsRes] = await Promise.all([
          api.getCustomer(customerId),
          api.getCustomerReservations(customerId)
        ])
        this.selectedCustomer = customerRes.data
        this.customerReservations = reservationsRes.data.reservations || []
      } catch (error) {
        console.error('Failed to load customer details:', error)
        alert('Failed to load customer details')
      }
    },
    async handleAddCustomer() {
      try {
        await api.createCustomer(this.newCustomer)
        alert('Customer added successfully')
        this.showAddModal = false
        this.newCustomer = { name: '', email: '', phone: '', nationality: '' }
        await this.loadData()
      } catch (error) {
        alert('Failed to add customer')
      }
    },
    getRoomNumber(roomId) {
      const room = this.rooms.find(r => r.id === roomId)
      return room ? room.room_number : roomId
    },
    formatDate(dateStr) {
      if (!dateStr) return ''
      return new Date(dateStr).toLocaleDateString('en-US')
    },
    formatPrice(price) {
      return new Intl.NumberFormat('en-US').format(price)
    },
    getStatusText(status) {
      const map = {
        'confirmed': 'Confirmed',
        'checked_in': 'Checked In',
        'checked_out': 'Checked Out',
        'cancelled': 'Cancelled'
      }
      return map[status] || status
    },
    applyFilters() {
      // computed 속성이 자동으로 업데이트됨
    },
    clearFilters() {
      this.filterName = ''
      this.filterEmail = ''
      this.filterPhone = ''
    }
  }
}
</script>

<style scoped>
.customers {
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
}

.customers-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.customer-card {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.customer-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.customer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.customer-header h3 {
  font-size: 1.2rem;
  color: #333;
}

.customer-id {
  font-size: 0.85rem;
  color: #666;
}

.customer-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
}

.detail-icon {
  font-size: 1rem;
}

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

.customer-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-row {
  display: flex;
  gap: 1rem;
}

.info-label {
  font-weight: 500;
  min-width: 100px;
}

.reservations-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.reservation-item {
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  padding: 1rem;
}

.res-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.res-details {
  display: flex;
  justify-content: space-between;
  color: #666;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
}

.status-badge.confirmed {
  background: #e3f2fd;
  color: #1976d2;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 5px;
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
  cursor: pointer;
}

.empty-state, .loading {
  text-align: center;
  padding: 3rem;
  color: #999;
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
  align-items: flex-end;
  gap: 1.5rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
  min-width: 200px;
}

.filter-group label {
  font-weight: 500;
  color: #333;
  font-size: 0.9rem;
}

.filter-group input[type="text"] {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 0.9rem;
}

.filter-group input:focus {
  outline: none;
  border-color: #667eea;
}

.btn-clear-filter {
  background: #f5f5f5;
  color: #333;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  font-weight: 500;
  cursor: pointer;
  height: fit-content;
}

.btn-clear-filter:hover {
  background: #e0e0e0;
}
</style>

