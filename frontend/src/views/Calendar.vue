<template>
  <div class="calendar">
    <div class="page-header">
      <h1 class="page-title">Reservation Calendar</h1>
      <div class="controls">
        <button @click="previousMonth" class="btn-nav">← Previous</button>
        <span class="month-year">{{ currentMonthName }} {{ currentYear }}</span>
        <button @click="nextMonth" class="btn-nav">Next →</button>
      </div>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else class="calendar-grid">
      <div class="calendar-header">
        <div v-for="day in weekDays" :key="day" class="day-header">{{ day }}</div>
      </div>
      <div class="calendar-body">
        <div v-for="(week, weekIndex) in calendarWeeks" :key="weekIndex" class="calendar-week">
          <div
            v-for="(day, dayIndex) in week"
            :key="dayIndex"
            class="calendar-day"
            :class="{ 'other-month': !day.isCurrentMonth, 'today': day.isToday }"
          >
            <div class="day-number">{{ day.date.getDate() }}</div>
            <div class="day-reservations">
              <div
                v-for="reservation in day.reservations"
                :key="reservation.id"
                class="reservation-badge"
                :class="getStatusClass(reservation.status)"
                :title="`Room ${getRoomNumber(reservation.room_id)} - ${reservation.booking_reference} (${reservation.status})`"
              >
                Room {{ getRoomNumber(reservation.room_id) }}
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
import { format, startOfMonth, endOfMonth, startOfWeek, endOfWeek, eachDayOfInterval, isSameMonth, isToday, addMonths, subMonths } from 'date-fns'

export default {
  name: 'Calendar',
  data() {
    return {
      loading: true,
      reservations: [],
      rooms: [],
      currentDate: new Date(),
      weekDays: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    }
  },
  computed: {
    currentYear() {
      return this.currentDate.getFullYear()
    },
    currentMonth() {
      return this.currentDate.getMonth() + 1
    },
    currentMonthName() {
      return format(this.currentDate, 'MMMM')
    },
    calendarWeeks() {
      const monthStart = startOfMonth(this.currentDate)
      const monthEnd = endOfMonth(this.currentDate)
      const calendarStart = startOfWeek(monthStart, { weekStartsOn: 0 })
      const calendarEnd = endOfWeek(monthEnd, { weekStartsOn: 0 })
      
      const days = eachDayOfInterval({ start: calendarStart, end: calendarEnd })
      const weeks = []
      
      for (let i = 0; i < days.length; i += 7) {
        const week = days.slice(i, i + 7).map(day => {
          const dayReservations = this.reservations.filter(res => {
            const checkIn = new Date(res.check_in)
            const checkOut = new Date(res.check_out)
            return day >= checkIn && day <= checkOut
          })
          
          return {
            date: day,
            isCurrentMonth: isSameMonth(day, this.currentDate),
            isToday: isToday(day),
            reservations: dayReservations
          }
        })
        weeks.push(week)
      }
      
      return weeks
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      try {
        this.loading = true
        const [reservationsRes, roomsRes] = await Promise.all([
          api.getMonthReservations(this.currentYear, this.currentMonth),
          api.getRooms()
        ])
        
        this.reservations = reservationsRes.data.reservations || []
        this.rooms = roomsRes.data
      } catch (error) {
        console.error('Failed to load calendar data:', error)
        alert('Failed to load calendar data')
      } finally {
        this.loading = false
      }
    },
    previousMonth() {
      this.currentDate = subMonths(this.currentDate, 1)
      this.loadData()
    },
    nextMonth() {
      this.currentDate = addMonths(this.currentDate, 1)
      this.loadData()
    },
    getRoomNumber(roomId) {
      const room = this.rooms.find(r => r.id === roomId)
      return room ? room.room_number : roomId
    },
    getStatusClass(status) {
      const statusMap = {
        'Reserved': 'status-reserved',
        'Checked in': 'status-checked-in',
        'Checked out': 'status-checked-out'
      }
      return statusMap[status] || 'status-reserved'
    }
  }
}
</script>

<style scoped>
.calendar {
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

.controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.btn-nav {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  background: white;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-nav:hover {
  background: #f5f5f5;
}

.month-year {
  font-size: 1.2rem;
  font-weight: 600;
  min-width: 200px;
  text-align: center;
}

.calendar-grid {
  background: white;
  border-radius: 10px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.calendar-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.day-header {
  padding: 0.75rem;
  text-align: center;
  font-weight: 600;
  color: #666;
  background: #f8f9fa;
  border-radius: 5px;
}

.calendar-body {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.calendar-week {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.5rem;
}

.calendar-day {
  min-height: 100px;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  padding: 0.5rem;
  background: white;
}

.calendar-day.other-month {
  background: #f8f9fa;
  color: #999;
}

.calendar-day.today {
  background: #e3f2fd;
  border-color: #2196f3;
}

.day-number {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.day-reservations {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.reservation-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 3px;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.reservation-badge.status-reserved {
  background: #f44336;
  color: white;
}

.reservation-badge.status-checked-in {
  background: #2196f3;
  color: white;
}

.reservation-badge.status-checked-out {
  background: #4caf50;
  color: white;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #999;
}
</style>

