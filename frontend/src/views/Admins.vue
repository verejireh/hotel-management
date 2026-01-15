<template>
  <div class="admins">
    <div class="page-header">
      <h1 class="page-title">Admin Management</h1>
      <button class="btn-primary" @click="showAddModal = true">+ New Admin</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else class="admins-list">
      <div v-for="admin in admins" :key="admin.id" class="admin-card">
        <div class="admin-header">
          <h3>{{ admin.name }}</h3>
          <div class="admin-header-actions">
            <span class="admin-status" :class="{ active: admin.is_active, inactive: !admin.is_active }">
              {{ admin.is_active ? 'Active' : 'Inactive' }}
            </span>
            <button class="btn-delete" @click="handleDeleteAdmin(admin.id, admin.name)" title="Delete admin">
              🗑️
            </button>
          </div>
        </div>
        <div class="admin-details">
          <div v-if="admin.role" class="detail-item">
            <span class="detail-icon">👤</span>
            <span><strong>Role:</strong> {{ admin.role }}</span>
          </div>
          <div v-if="admin.email" class="detail-item">
            <span class="detail-icon">📧</span>
            <span>{{ admin.email }}</span>
          </div>
          <div v-if="admin.phone" class="detail-item">
            <span class="detail-icon">📞</span>
            <span>{{ admin.phone }}</span>
          </div>
        </div>
      </div>
      
      <div v-if="admins.length === 0" class="empty-state">No admins found.</div>
    </div>

    <!-- Add Admin Modal -->
    <div v-if="showAddModal" class="modal-overlay" @click="showAddModal = false">
      <div class="modal-content" @click.stop>
        <h2>New Admin</h2>
        <form @submit.prevent="handleAddAdmin">
          <div class="form-group">
            <label>Name *</label>
            <input type="text" v-model="newAdmin.name" required />
          </div>
          <div class="form-group">
            <label>Email</label>
            <input type="email" v-model="newAdmin.email" />
          </div>
          <div class="form-group">
            <label>Phone</label>
            <input type="tel" v-model="newAdmin.phone" />
          </div>
          <div class="form-group">
            <label>Role *</label>
            <select v-model="newAdmin.role" required>
              <option value="">Select role</option>
              <option value="Manager">Manager</option>
              <option value="Cleaning Staff">Cleaning Staff</option>
              <option value="Technical Staff">Technical Staff</option>
            </select>
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
  name: 'Admins',
  data() {
    return {
      loading: true,
      admins: [],
      showAddModal: false,
      newAdmin: {
        name: '',
        email: '',
        phone: '',
        role: ''
      }
    }
  },
  async mounted() {
    await this.loadAdmins()
  },
  methods: {
    async loadAdmins() {
      try {
        this.loading = true
        const response = await api.getAdmins()
        this.admins = response.data
      } catch (error) {
        console.error('Failed to load admins:', error)
        alert('Failed to load admins')
      } finally {
        this.loading = false
      }
    },
    async handleAddAdmin() {
      try {
        await api.createAdmin(this.newAdmin)
        alert('Admin added successfully')
        this.showAddModal = false
        this.newAdmin = { name: '', email: '', phone: '', role: '' }
        await this.loadAdmins()
      } catch (error) {
        alert('Failed to add admin')
      }
    },
    async handleDeleteAdmin(adminId, adminName) {
      if (!confirm(`Are you sure you want to delete "${adminName}"? This action cannot be undone.`)) {
        return
      }
      
      try {
        await api.deleteAdmin(adminId)
        alert('Admin deleted successfully')
        await this.loadAdmins()
      } catch (error) {
        console.error('Failed to delete admin:', error)
        alert('Failed to delete admin: ' + (error.response?.data?.detail || error.message))
      }
    }
  }
}
</script>

<style scoped>
.admins {
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

.admins-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.admin-card {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.admin-header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.admin-header h3 {
  font-size: 1.2rem;
  color: #333;
}

.admin-status {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.admin-status.active {
  background: #e8f5e9;
  color: #388e3c;
}

.admin-status.inactive {
  background: #ffebee;
  color: #c62828;
}

.admin-details {
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
  max-width: 500px;
  width: 90%;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input[type="text"],
.form-group input[type="email"],
.form-group input[type="tel"],
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.form-group input[type="checkbox"] {
  margin-right: 0.5rem;
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

.btn-delete {
  background: #ff4444;
  color: white;
  border: none;
  padding: 0.4rem 0.6rem;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-delete:hover {
  background: #cc0000;
}
</style>

