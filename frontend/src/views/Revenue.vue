<template>
  <div class="revenue">
    <h1 class="page-title">Revenue Analysis</h1>
    
    <div class="filters">
      <div class="filter-group">
        <label>Start Date:</label>
        <input type="date" v-model="startDate" />
      </div>
      <div class="filter-group">
        <label>End Date:</label>
        <input type="date" v-model="endDate" />
      </div>
      <button class="btn-primary" @click="loadRevenueData">Apply</button>
      <button class="btn-secondary" @click="exportReport">Export Excel</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else class="revenue-content">
      <!-- Daily Revenue Chart -->
      <div class="chart-section">
        <h2>Daily Revenue</h2>
        <canvas ref="dailyChart"></canvas>
      </div>

      <!-- Platform Revenue -->
      <div class="chart-section">
        <h2>Revenue by Platform</h2>
        <canvas ref="platformChart"></canvas>
      </div>

      <!-- Summary Stats -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">Total Revenue</div>
          <div class="stat-value">${{ formatPrice(totalRevenue) }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Total Reservations</div>
          <div class="stat-value">{{ totalReservations }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Average per Reservation</div>
          <div class="stat-value">${{ formatPrice(avgRevenue) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

export default {
  name: 'Revenue',
  data() {
    return {
      loading: true,
      startDate: new Date(new Date().setMonth(new Date().getMonth() - 1)).toISOString().split('T')[0],
      endDate: new Date().toISOString().split('T')[0],
      dailyData: [],
      platformData: [],
      dailyChart: null,
      platformChart: null
    }
  },
  computed: {
    totalRevenue() {
      return this.dailyData.reduce((sum, day) => sum + day.revenue, 0)
    },
    totalReservations() {
      return this.dailyData.reduce((sum, day) => sum + day.reservations, 0)
    },
    avgRevenue() {
      return this.totalReservations > 0 ? this.totalRevenue / this.totalReservations : 0
    }
  },
  async mounted() {
    await this.loadRevenueData()
  },
  methods: {
    async loadRevenueData() {
      try {
        this.loading = true
        const [dailyRes, platformRes] = await Promise.all([
          api.getDailyRevenue(this.startDate, this.endDate),
          api.getPlatformRevenue(this.startDate, this.endDate)
        ])
        
        this.dailyData = dailyRes.data.daily_data || []
        this.platformData = platformRes.data.platform_data || []
        
        this.$nextTick(() => {
          this.renderCharts()
        })
      } catch (error) {
        console.error('Failed to load revenue data:', error)
        alert('Failed to load revenue data')
      } finally {
        this.loading = false
      }
    },
    renderCharts() {
      // Daily Revenue Chart
      if (this.dailyChart) {
        this.dailyChart.destroy()
      }
      
      const dailyCtx = this.$refs.dailyChart?.getContext('2d')
      if (dailyCtx) {
        this.dailyChart = new Chart(dailyCtx, {
          type: 'line',
          data: {
            labels: this.dailyData.map(d => d.date),
            datasets: [{
              label: 'Revenue',
              data: this.dailyData.map(d => d.revenue),
              borderColor: '#667eea',
              backgroundColor: 'rgba(102, 126, 234, 0.1)',
              tension: 0.4
            }]
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        })
      }

      // Platform Revenue Chart
      if (this.platformChart) {
        this.platformChart.destroy()
      }
      
      const platformCtx = this.$refs.platformChart?.getContext('2d')
      if (platformCtx) {
        this.platformChart = new Chart(platformCtx, {
          type: 'bar',
          data: {
            labels: this.platformData.map(d => d.platform),
            datasets: [{
              label: 'Revenue',
              data: this.platformData.map(d => d.revenue),
              backgroundColor: '#764ba2'
            }]
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        })
      }
    },
    async exportReport() {
      try {
        const response = await api.exportReservationsExcel(this.startDate, this.endDate)
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `revenue_report_${this.startDate}_${this.endDate}.xlsx`)
        document.body.appendChild(link)
        link.click()
        link.remove()
      } catch (error) {
        alert('Failed to export report')
      }
    },
    formatPrice(price) {
      return new Intl.NumberFormat('en-US').format(price)
    }
  },
  beforeUnmount() {
    if (this.dailyChart) this.dailyChart.destroy()
    if (this.platformChart) this.platformChart.destroy()
  }
}
</script>

<style scoped>
.revenue {
  padding: 2rem 0;
}

.page-title {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #333;
}

.filters {
  display: flex;
  gap: 1rem;
  align-items: end;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 500;
  font-size: 0.9rem;
}

.filter-group input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.btn-primary, .btn-secondary {
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 5px;
  font-weight: 500;
  cursor: pointer;
  height: fit-content;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-secondary {
  background: #f5f5f5;
  color: #333;
}

.chart-section {
  background: white;
  border-radius: 10px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.chart-section h2 {
  margin-bottom: 1.5rem;
  color: #333;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #667eea;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #999;
}
</style>







