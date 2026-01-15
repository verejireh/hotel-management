<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <h1 class="logo">🏨 Hotel Management</h1>
        <div class="nav-links">
          <router-link to="/" class="nav-link">Dashboard</router-link>
          <router-link to="/reservations" class="nav-link">Reservations</router-link>
          <router-link to="/calendar" class="nav-link">Calendar</router-link>
          <router-link to="/rooms" class="nav-link">Rooms</router-link>
          <router-link to="/customers" class="nav-link">Customers</router-link>
          <router-link to="/revenue" class="nav-link">Revenue</router-link>
          <router-link to="/cleaning" class="nav-link">Cleaning</router-link>
          <router-link to="/admins" class="nav-link">Admins</router-link>
          <button class="nav-btn-add-note" @click="openNoteModal">+ Note</button>
        </div>
      </div>
    </nav>
    <main class="main-content">
      <router-view />
    </main>

    <!-- Add Note Modal -->
    <div v-if="showNoteModal" class="modal-overlay" @click="closeNoteModal">
      <div class="modal-content" @click.stop>
        <h2>Add Room Note</h2>
        <form @submit.prevent="handleAddNote">
          <div class="form-group">
            <label>Room Number *</label>
            <select v-model="newNote.room_id" required>
              <option value="">Select room</option>
              <option v-for="room in rooms" :key="room.id" :value="room.id">
                Room {{ room.room_number }} ({{ room.room_type }})
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Note Type *</label>
            <select v-model="newNote.note_type" required>
              <option value="">Select type</option>
              <option value="urgent">Urgent (Immediate action needed)</option>
              <option value="after_checkout">After Checkout (Process after checkout)</option>
            </select>
          </div>
          <div class="form-group">
            <label>Title *</label>
            <input type="text" v-model="newNote.title" required />
          </div>
          <div class="form-group">
            <label>Description *</label>
            <textarea v-model="newNote.description" rows="4" required></textarea>
          </div>
          <div class="form-group">
            <label>Name *</label>
            <select v-model="newNote.admin_id" required>
              <option value="">Select name</option>
              <option 
                v-for="admin in admins" 
                :key="admin.id" 
                :value="admin.id"
              >
                {{ admin.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Progress</label>
            <select v-model="newNote.progress">
              <option value="">No progress</option>
              <option value="confirm">Confirm</option>
              <option value="In progress">In progress</option>
              <option value="finished">Finished</option>
            </select>
          </div>
          <div class="form-actions">
            <button type="button" class="btn-secondary" @click="closeNoteModal">Cancel</button>
            <button type="submit" class="btn-primary">Add Note</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from './services/api'

export default {
  name: 'App',
  data() {
    return {
      showNoteModal: false,
      rooms: [],
      admins: [],
      newNote: {
        room_id: '',
        admin_id: '',
        note_type: '',
        title: '',
        description: '',
        reservation_id: null,
        progress: ''
      }
    }
  },
  async mounted() {
    console.log('App.vue mounted')
    await this.loadData()
  },
  methods: {
    async loadData() {
      try {
        console.log('App.vue: Loading data...')
        const [roomsRes, adminsRes] = await Promise.all([
          api.getRooms(),
          api.getAdmins()
        ])
        console.log('App.vue: Data loaded', { rooms: roomsRes.data, admins: adminsRes.data })
        this.rooms = roomsRes.data || []
        // is_active 필터 제거 - 모든 admin 표시
        this.admins = adminsRes.data || []
        console.log('App.vue: Rooms loaded', this.rooms)
        console.log('App.vue: Admins loaded', this.admins)
      } catch (error) {
        console.error('App.vue: Failed to load data:', error)
        console.error('Error details:', error.response || error.message)
        this.rooms = []
        this.admins = []
      }
    },
    async openNoteModal() {
      // 모달 열 때 rooms나 admins가 없으면 다시 로드
      if (this.rooms.length === 0 || this.admins.length === 0) {
        console.log('App.vue: Reloading data for modal...')
        try {
          const [roomsRes, adminsRes] = await Promise.all([
            this.rooms.length === 0 ? api.getRooms() : Promise.resolve({ data: this.rooms }),
            this.admins.length === 0 ? api.getAdmins() : Promise.resolve({ data: this.admins })
          ])
          
          if (this.rooms.length === 0) {
            this.rooms = roomsRes.data || []
            console.log('App.vue: Rooms reloaded', this.rooms)
          }
          
          if (this.admins.length === 0) {
            this.admins = adminsRes.data || []
            console.log('App.vue: Admins reloaded', this.admins)
          }
        } catch (error) {
          console.error('App.vue: Failed to reload data:', error)
        }
      }
      
      this.newNote = {
        room_id: '',
        admin_id: '',
        note_type: '',
        title: '',
        description: '',
        reservation_id: null,
        progress: ''
      }
      this.showNoteModal = true
    },
    closeNoteModal() {
      this.showNoteModal = false
      this.newNote = {
        room_id: '',
        admin_id: '',
        note_type: '',
        title: '',
        description: '',
        reservation_id: null,
        progress: ''
      }
    },
    async handleAddNote() {
      // Admin이 선택되었는지 확인
      if (!this.newNote.admin_id) {
        alert('Please select an admin')
        return
      }
      
      try {
        await api.createRoomNote(this.newNote)
        alert('Note added successfully')
        this.closeNoteModal()
        // Dashboard 새로고침을 위해 이벤트 발생
        window.dispatchEvent(new Event('note-added'))
      } catch (error) {
        console.error('Failed to add note:', error)
        alert('Failed to add note: ' + (error.response?.data?.detail || error.message))
      }
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background-color: #f5f5f5;
  color: #333;
}

#app {
  min-height: 100vh;
}

.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: 600;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.nav-link:hover,
.nav-link.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
}

.nav-btn-add-note {
  background: #ff6b6b;
  color: white;
  border: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 0.95rem;
}

.nav-btn-add-note:hover {
  background: #ee5a5a;
  transform: translateY(-1px);
}

.main-content {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 2rem;
}

/* Modal Styles */
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
  background: white;
}

.form-group select {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23333' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 12px;
  padding-right: 2.5rem;
  cursor: pointer;
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

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: #f5f5f5;
  color: #333;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

.error-message {
  color: #f44336;
  font-size: 0.875rem;
  margin-top: 0.5rem;
  font-style: italic;
}
</style>

