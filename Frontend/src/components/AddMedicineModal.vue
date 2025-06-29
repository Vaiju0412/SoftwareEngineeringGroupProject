<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h2>Add Medicine Schedule</h2>
      
      <!-- Step 1: Search for a medicine -->
      <div class="form-step">
        <label>1. Find or create a medicine</label>
        <input type="text" v-model="searchQuery" placeholder="Search for medicine name..." @input="handleSearch" />
        <div v-if="isSearching" class="search-status">Searching...</div>
        
        <ul v-if="searchResults.length > 0 && !selectedMedicine" class="search-results">
          <li v-for="med in searchResults" :key="med.id" @click="selectMedicine(med)">
            {{ med.title }}
          </li>
        </ul>

        <div v-if="searchAttempted && searchResults.length === 0 && !isSearching" class="search-status">
          No medicine found. You can create it.
          <button class="create-new-btn" @click="createNewMedicine" :disabled="!searchQuery.trim()">
            Create "{{ searchQuery }}"
          </button>
        </div>

        <div v-if="selectedMedicine" class="selected-medicine">
          Selected: <strong>{{ selectedMedicine.title }}</strong>
          <button @click="clearSelection">Change</button>
        </div>
      </div>
      
      <!-- Step 2: Define Dosage and Schedule -->
      <div class="form-step" :class="{ disabled: !selectedMedicine }">
        <label>2. Set dosage and schedule</label>
        <input type="text" v-model="dosage" placeholder="e.g., 1 pill, 10mg" />
        
        <div class="schedule-grid">
          <div class="meal-group">
            <h4>Breakfast</h4>
            <label><input type="checkbox" v-model="schedule.breakfast_before"> Before</label>
            <label><input type="checkbox" v-model="schedule.breakfast_after"> After</label>
          </div>
          <div class="meal-group">
            <h4>Lunch</h4>
            <label><input type="checkbox" v-model="schedule.lunch_before"> Before</label>
            <label><input type="checkbox" v-model="schedule.lunch_after"> After</label>
          </div>
          <div class="meal-group">
            <h4>Dinner</h4>
            <label><input type="checkbox" v-model="schedule.dinner_before"> Before</label>
            <label><input type="checkbox" v-model="schedule.dinner_after"> After</label>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="modal-actions">
        <button class="modal-btn-cancel" @click="$emit('close')">Cancel</button>
        <button class="modal-btn-confirm" @click="submit" :disabled="!isFormValid">Add to Schedule</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, defineEmits } from 'vue';
import { searchMasterMedicineList, createNewMasterMedicine } from '../services/mockApi';

const emit = defineEmits(['close', 'add-medication']);

// --- State ---
const searchQuery = ref('');
const searchResults = ref([]);
const isSearching = ref(false);
const searchAttempted = ref(false);

const selectedMedicine = ref(null);
const dosage = ref('');
const schedule = reactive({
  breakfast_before: false,
  breakfast_after: false,
  lunch_before: false,
  lunch_after: false,
  dinner_before: false,
  dinner_after: false,
});

// --- Computed ---
const isFormValid = computed(() => {
  const hasSchedule = Object.values(schedule).some(v => v);
  return selectedMedicine.value && dosage.value.trim() && hasSchedule;
});

// --- Methods ---
let searchTimeout;
function handleSearch() {
  clearTimeout(searchTimeout);
  isSearching.value = true;
  searchAttempted.value = true;
  searchTimeout = setTimeout(async () => {
    searchResults.value = await searchMasterMedicineList(searchQuery.value);
    isSearching.value = false;
  }, 300); // Debounce search
}

function selectMedicine(med) {
  selectedMedicine.value = med;
}

function clearSelection() {
    selectedMedicine.value = null;
    searchQuery.value = '';
    searchResults.value = [];
    searchAttempted.value = false;
}

async function createNewMedicine() {
  const newMed = await createNewMasterMedicine(searchQuery.value);
  if (newMed) {
    selectMedicine(newMed);
  }
}

function submit() {
  if (!isFormValid.value) return;
  
  const payload = {
    medicineId: selectedMedicine.value.id,
    dosage: dosage.value,
    ...schedule,
  };
  
  emit('add-medication', payload);
}
</script>

<style scoped>
.modal-overlay {
  /* ... same as previous answer ... */
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: rgba(0, 0, 0, 0.6); display: flex; justify-content: center; align-items: center; z-index: 1000;
}
.modal-content {
  /* ... same as previous answer ... */
  background: white; padding: 2rem; border-radius: 10px; width: 90%; max-width: 550px; font-family: Arial, sans-serif;
}
.modal-content h2 { margin-top: 0; }
.form-step {
  margin-bottom: 1.5rem;
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 8px;
  transition: opacity 0.3s;
}
.form-step.disabled {
    opacity: 0.5;
    pointer-events: none;
    background-color: #f9f9f9;
}
.form-step label {
  font-weight: bold;
  display: block;
  margin-bottom: 0.75rem;
}
input[type="text"] {
    width: 100%;
    padding: 10px;
    font-size: 1rem;
    border-radius: 5px;
    border: 1px solid #ccc;
}
.search-status {
    font-style: italic;
    color: #666;
    margin-top: 0.5rem;
}
.search-results {
  list-style: none; padding: 0; margin: 10px 0 0 0; max-height: 150px; overflow-y: auto; border: 1px solid #ddd; border-radius: 5px;
}
.search-results li { padding: 10px; cursor: pointer; border-bottom: 1px solid #eee; }
.search-results li:hover { background-color: #f0f0f0; }
.create-new-btn {
    margin-left: 10px;
    padding: 5px 10px;
    border: 1px solid #007bff;
    background: #e7f3ff;
    color: #007bff;
    border-radius: 5px;
    cursor: pointer;
}
.selected-medicine {
    background-color: #e7f3ff;
    border: 1px solid #007bff;
    padding: 10px;
    margin-top: 10px;
    border-radius: 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.selected-medicine button { background: none; border: none; color: #007bff; cursor: pointer; text-decoration: underline; }

.schedule-grid {
  display: flex;
  justify-content: space-around;
  margin-top: 1rem;
  text-align: center;
}
.meal-group h4 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}
.meal-group label {
  font-weight: normal;
  display: block;
}
.modal-actions {
  display: flex; justify-content: flex-end; gap: 1rem; margin-top: 1.5rem;
}
.modal-btn-cancel, .modal-btn-confirm {
  padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 1rem;
}
.modal-btn-cancel { background-color: #6c757d; color: white; }
.modal-btn-confirm { background-color: #28a745; color: white; }
.modal-btn-confirm:disabled { background-color: #aaa; cursor: not-allowed; }
</style>