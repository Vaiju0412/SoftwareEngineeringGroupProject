<template>
  <div class="home-wrapper">
    <div class="header">
      <div class="date-info">
        <p>Today</p>
        <p>{{ currentDate }}</p>
        <h2>Greetings, {{ userName }}</h2>
        <h3>Today's medications</h3>
      </div>

      <div class="icons">
        <span>🔔</span>
        <span>📈</span>
        <span>👤</span>
      </div>
    </div>

    <div class="medications">
      <div class="med-card mom">
        <div class="label">Mom’s Next Medication <a href="#">View All</a></div>
        <div class="med-details">
          <span>🚫</span>
          <span>Medicine Name</span>
          <span>Dosage</span>
          <span>⏰ Time</span>
          <button>POKE</button>
        </div>
      </div>

      <div class="med-card dad">
        <div class="label">Dad’s Next Medication <a href="#">View All</a></div>
        <div class="med-details">
          <span>🚫</span>
          <span>Medicine Name</span>
          <span>Dosage</span>
          <span>⏰ Time</span>
          <button>POKE</button>
        </div>
      </div>

      <div class="med-card uncle">
        <div class="label">Uncle’s Next Medication <a href="#">View All</a></div>
        <div class="med-details">
          <span>🚫</span>
          <span>Medicine Name</span>
          <span>Dosage</span>
          <span>⏰ Time</span>
          <button>POKE</button>
        </div>
      </div>
    </div>

    <div class="calendar-section">
      <div class="calendar-header">
        <button class="legend mom">Mom</button>
        <button class="legend dad">Dad</button>
        <button class="legend uncle">Uncle</button>
      </div>
      <div class="calendar">
        <h2 class="month-label">June 2025</h2>
        <table>
          <thead>
            <tr>
              <th v-for="day in days" :key="day">{{ day }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(week, index) in weeks" :key="index">
              <td v-for="day in week" :key="day.date">
                <span :class="'day ' + day.status">{{ day.label }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
//import { ref } from 'vue'

const userName = 'User'
const currentDate = new Date().toDateString()

const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
const weeks = [
  [
    { label: '1', status: 'mom' },
    { label: '2', status: 'green' },
    { label: '3', status: 'green' },
    { label: '4', status: 'green' },
    { label: '5', status: 'mom' },
    { label: '6', status: 'red' },
    { label: '7', status: 'default' },
  ],
  ...Array(4).fill(Array(7).fill({ label: '•', status: 'default' })),
]
</script>

<style scoped>
.home-wrapper {
  background-color: #d6eed6;
  border-radius: 20px;
  padding: 2rem;
  font-family: sans-serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: start;
}

.date-info h2 {
  margin-top: 1rem;
}

.icons span {
  font-size: 1.5rem;
  margin: 0 0.5rem;
  cursor: pointer;
}

.medications {
  margin: 2rem 0;
}

.med-card {
  border-radius: 15px;
  margin-bottom: 1rem;
  padding: 1rem;
}

.mom {
  background-color: #fff9b0;
}
.dad {
  background-color: #fff9b0;
}
.uncle {
  background-color: #d9a8f9;
}

.med-card .label {
  display: flex;
  justify-content: space-between;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.med-details {
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.med-details button {
  background-color: #d62828;
  color: white;
  border: none;
  padding: 0.3rem 0.8rem;
  border-radius: 8px;
}

.calendar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.calendar-header {
  margin-bottom: 1rem;
}

.legend {
  margin-right: 0.5rem;
  padding: 0.3rem 1rem;
  border-radius: 12px;
  border: none;
}

.mom.legend {
  background-color: #adb8ff;
}
.dad.legend {
  background-color: #ffb4b4;
}
.uncle.legend {
  background-color: #e3b5f7;
}

.calendar {
  text-align: center;
}

.month-label {
  color: purple;
  font-size: 1.5rem;
  writing-mode: vertical-lr;
  transform: rotate(180deg);
  margin-right: 2rem;
}

table {
  border-collapse: collapse;
  width: 100%;
  max-width: 400px;
}

th, td {
  padding: 0.5rem;
  text-align: center;
}

.day {
  display: inline-block;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  line-height: 24px;
}

.green {
  background-color: green;
  color: white;
}
.red {
  background-color: red;
  color: white;
}
.default {
  background-color: lightgray;
}
.mom {
  background-color: lightgreen;
}
</style>
