import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 30000 // 30초 타임아웃 (Google Sheets API는 느릴 수 있음)
})

// 요청 인터셉터
api.interceptors.request.use(
  config => {
    console.log('API Request:', config.method?.toUpperCase(), config.url)
    return config
  },
  error => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// 응답 인터셉터
api.interceptors.response.use(
  response => {
    console.log('API Response:', response.config.url, response.status)
    return response
  },
  error => {
    console.error('API Response Error:', error.config?.url, error.response?.status, error.message)
    return Promise.reject(error)
  }
)

export default {
  // 예약 관련
  getReservations() {
    return api.get('/reservations/')
  },
  getReservation(id) {
    return api.get(`/reservations/${id}`)
  },
  createReservation(data) {
    return api.post('/reservations/', data)
  },
  checkRoomAvailability(roomId, checkIn, checkOut) {
    return api.get(`/reservations/room/${roomId}/availability`, {
      params: { check_in: checkIn, check_out: checkOut }
    })
  },
  
  // 방 관련
  getRooms() {
    return api.get('/rooms/')
  },
  getRoom(id) {
    return api.get(`/rooms/${id}`)
  },
  
  // 대시보드 관련
  getCheckInOutSummary() {
    return api.get('/dashboard/checkin-out')
  },
  getDashboardStats() {
    return api.get('/dashboard/stats')
  },
  
  // 캘린더 관련
  getMonthReservations(year, month) {
    return api.get(`/calendar/month/${year}/${month}`)
  },
  getWeekReservations(year, week) {
    return api.get(`/calendar/week/${year}/${week}`)
  },
  
  // 수익 분석 관련
  getDailyRevenue(startDate, endDate) {
    return api.get(`/revenue/daily/${startDate}/${endDate}`)
  },
  getMonthlyRevenue(year) {
    return api.get(`/revenue/monthly/${year}`)
  },
  getPlatformRevenue(startDate, endDate) {
    return api.get(`/revenue/platform/${startDate}/${endDate}`)
  },
  
  // 고객 관련
  getCustomers() {
    return api.get('/customers/')
  },
  getCustomer(id) {
    return api.get(`/customers/${id}`)
  },
  getCustomerReservations(customerId) {
    return api.get(`/customers/${customerId}/reservations`)
  },
  createCustomer(data) {
    return api.post('/customers/', data)
  },
  
  // 체크인/체크아웃 관련
  checkIn(reservationId) {
    return api.post(`/checkinout/checkin/${reservationId}`)
  },
  checkOut(reservationId) {
    return api.post(`/checkinout/checkout/${reservationId}`)
  },
  updateReservationStatus(reservationId, status) {
    // 공백이 포함된 status를 URL 인코딩
    const encodedStatus = encodeURIComponent(status)
    return api.put(`/reservations/${reservationId}/status?status=${encodedStatus}`)
  },
  getUpcomingCheckinsCheckouts(days = 7) {
    return api.get('/checkinout/upcoming', { params: { days } })
  },
  
  // 청소 관리 관련
  getCleaningRooms() {
    return api.get('/cleaning/rooms')
  },
  completeCleaning(roomId) {
    return api.post(`/cleaning/complete/${roomId}`)
  },
  
  // 리포트 관련
  exportReservationsExcel(startDate, endDate) {
    const params = {}
    if (startDate) params.start_date = startDate
    if (endDate) params.end_date = endDate
    return api.get('/reports/reservations/excel', { params, responseType: 'blob' })
  },
  exportReservationsCSV(startDate, endDate) {
    const params = {}
    if (startDate) params.start_date = startDate
    if (endDate) params.end_date = endDate
    return api.get('/reports/reservations/csv', { params, responseType: 'blob' })
  },
  
  // 관리자 관련
  getAdmins() {
    return api.get('/admins/')
  },
  getAdmin(id) {
    return api.get(`/admins/${id}`)
  },
  createAdmin(data) {
    return api.post('/admins/', data)
  },
  deleteAdmin(id) {
    return api.delete(`/admins/${id}`)
  },
  
  // 룸 메모 관련
  getRoomNotes(roomId = null, progress = undefined) {
    const params = {}
    if (roomId) params.room_id = roomId
    // progress가 undefined가 아니면 전달 (빈 문자열도 포함, null은 제외)
    if (progress !== null && progress !== undefined) {
      params.progress = progress
    }
    console.log('API: getRoomNotes called with params:', params)
    return api.get('/room-notes/', { params })
  },
  getUrgentNotes() {
    return api.get('/room-notes/urgent')
  },
  getAfterCheckoutNotes() {
    return api.get('/room-notes/after-checkout')
  },
  getAllAlerts() {
    return api.get('/room-notes/alerts')
  },
  createRoomNote(data) {
    return api.post('/room-notes/', data)
  },
  completeRoomNote(noteId) {
    return api.post(`/room-notes/${noteId}/complete`)
  },
  updateNoteProgress(noteId, progress) {
    return api.put(`/room-notes/${noteId}/progress?progress=${encodeURIComponent(progress || '')}`)
  }
}

