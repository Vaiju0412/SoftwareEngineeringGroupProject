<template>
  <div class="page-container">
    <h1>Member Details</h1>

    <div class="members-container">
      <!-- Loading State -->
      <div v-if="isLoading" class="loading">Loading members...</div>

      <!-- Member Cards Grid -->
      <div v-else-if="dependents.length > 0" class="members-grid">
        <div 
          v-for="dep in dependents" 
          :key="dep.id" 
          class="member-card"
          :style="{ backgroundColor: getCardColor(dep.gender) }"
          @click="viewProfile(dep)"
        >
          <div class="card-header">
            <!-- Displaying firstName as the main name now -->
            <span class="member-name">{{ dep.firstName }}</span>
            <span class="edit-icon">✎</span>
          </div>
          <div class="member-icon">
            <svg v-if="dep.gender === 'female'" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 288 512" fill="currentColor"><path d="M144 0a80 80 0 1 1 0 160A80 80 0 1 1 144 0zM96 192c-35.3 0-64 28.7-64 64V448c0 17.7 14.3 32 32 32s32-14.3 32-32V384h64v64c0 17.7 14.3 32 32 32s32-14.3 32-32V256c0-35.3-28.7-64-64-64H96z"/></svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" fill="currentColor"><path d="M160 0a80 80 0 1 1 0 160A80 80 0 1 1 160 0zM56 192c-33.1 0-60.3 25.5-63.8 57.9l-2.4 23.3C-14.5 306.9 1.7 344.4 29.3 365.2l2.3 1.7c29.1 21.6 68.3 21.6 97.4 0l2.3-1.7c27.6-20.8 43.8-58.3 29.1-89.1l-2.4-23.3C176.3 217.5 149.1 192 116 192H56zM232 256c-13.3 0-24 10.7-24 24V448c0 17.7 14.3 32 32 32s32-14.3 32-32V280c0-13.3-10.7-24-24-24z"/></svg>
          </div>
          <!-- Use the consistent `dep.id` now -->
          <button class="delete-btn" @click.stop="handleDelete(dep.id)">Delete Profile</button>
        </div>
      </div>
      
      <!-- No Dependents Message -->
      <div v-if="!isLoading && dependents.length === 0" class="empty-state">
          <p>No members found. Please add one.</p>
      </div>

      <!-- Add Member Button -->
      <div class="add-button-container">
        <button class="add-member-btn" @click="openAddModal">Add a member</button>
      </div>
    </div>

    <!-- Add Dependent Modal -->
    <div v-if="showAddModal" class="modal-overlay" @click.self="closeAddModal">
      <div class="modal-content">
        <h2>Add a New Dependent</h2>
        <p>Search for a user by name or username and select them to add.</p>
        <div class="search-container">
          <input type="text" v-model="searchQuery" placeholder="Enter username or name..." @input="handleSearch" />
          <div v-if="isSearching" class="search-loading">Searching...</div>
        </div>
        <ul v-if="searchResults.length > 0" class="search-results">
          <li 
            v-for="user in searchResults" 
            :key="user.id" 
            @click="selectUser(user)"
            :class="{ selected: selectedNewDependent && selectedNewDependent.id === user.id }"
          >
            {{ user.firstName }} {{ user.lastName }} ({{ user.username }})
          </li>
        </ul>
        <div v-if="searchAttempted && searchResults.length === 0 && !isSearching" class="no-results">
          No users found.
        </div>
        <div class="modal-actions">
          <button class="modal-btn-cancel" @click="closeAddModal">Cancel</button>
          <button class="modal-btn-confirm" @click="handleAddDependent" :disabled="!selectedNewDependent">Add Dependent</button>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
// Import from our centralized mock API service
import { 
  getDependentsList,
  deleteDependent as apiDeleteDependent,
  searchAllUsers,
  addDependent as apiAddDependent
} from '../services/mockApi.js';

// --- Reactive State ---
const router = useRouter();
const dependents = ref([]);
const isLoading = ref(true);
const showAddModal = ref(false);

// State for "Add Dependent" modal
const searchQuery = ref('');
const searchResults = ref([]);
const selectedNewDependent = ref(null);
const isSearching = ref(false);
const searchAttempted = ref(false);

// --- Component Logic ---

// Central function to fetch data and update the component state
async function fetchDependents() {
  isLoading.value = true;
  dependents.value = await getDependentsList();
  isLoading.value = false;
}

onMounted(() => {
  fetchDependents();
});

function getCardColor(gender) {
  return gender === 'female' ? '#E8D2E8' : '#D2D9E8';
}

// --- Card Actions ---
function viewProfile(dependent) {
  router.push({ name: 'DependentProfile', params: { userId: dependent.id } });
}

async function handleDelete(userId) {
  if (confirm('Are you sure you want to delete this profile?')) {
    await apiDeleteDependent(userId);
    // Re-fetch the list from the "API" to update the UI
    await fetchDependents();
  }
}

// --- Add Modal Logic ---
function openAddModal() {
  showAddModal.value = true;
}

function closeAddModal() {
  showAddModal.value = false;
  // Reset modal state
  searchQuery.value = '';
  searchResults.value = [];
  selectedNewDependent.value = null;
  isSearching.value = false;
  searchAttempted.value = false;
}

let searchTimeout;
function handleSearch() {
  clearTimeout(searchTimeout);
  isSearching.value = true;
  searchAttempted.value = true;
  // Debounce the search to avoid API calls on every keystroke
  searchTimeout = setTimeout(async () => {
    searchResults.value = await searchAllUsers(searchQuery.value);
    isSearching.value = false;
  }, 300);
}

function selectUser(user) {
  selectedNewDependent.value = user;
}

async function handleAddDependent() {
  if (!selectedNewDependent.value) return;

  const response = await apiAddDependent(selectedNewDependent.value);

  if (response.success) {
    // Close the modal and refresh the list of dependents
    closeAddModal();
    await fetchDependents();
  } else {
    alert(response.message || 'Failed to add dependent.');
  }
}
</script>

<style scoped>
/* --- Main Layout --- */
.page-container {
  padding: 2rem;
  font-family: 'Serif', Georgia, Times, 'Times New Roman';
  display: flex;
  flex-direction: column;
  align-items: center;
}

h1 {
  margin-bottom: 1.5rem;
}

.members-container {
  background-color: #e0f0e0; /* Light green background */
  border-radius: 15px;
  padding: 2rem;
  width: 100%;
  max-width: 900px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.loading, .empty-state {
  text-align: center;
  padding: 3rem;
  color: #555;
  font-size: 1.2rem;
}

/* --- Member Cards --- */
.members-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
}

.member-card {
  width: 220px;
  border-radius: 12px;
  border: 1px solid rgba(0,0,0,0.2);
  padding: 1rem;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.member-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 15px rgba(0,0,0,0.15);
}

.card-header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.member-name {
  font-size: 1.5rem;
  font-weight: bold;
}

.edit-icon {
  font-size: 1.2rem;
  cursor: pointer;
}

.member-icon {
  width: 80px;
  height: 80px;
  color: #f0f0f0;
  margin: 1rem 0;
}

.member-icon svg {
    width: 100%;
    height: 100%;
}

.delete-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 1rem;
  transition: background-color 0.2s;
}

.delete-btn:hover {
  background-color: #c82333;
}

.add-button-container {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

.add-member-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 12px 24px;
  font-size: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.add-member-btn:hover {
  background-color: #0056b3;
}

/* --- Modal Styles --- */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
  font-family: Arial, sans-serif; /* Use a more standard font for modals */
}

.modal-content h2 {
    margin-top: 0;
}

.search-container {
    position: relative;
    margin-bottom: 1rem;
}
.search-container input {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.search-loading {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    color: #888;
}

.search-results {
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.search-results li {
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid #eee;
}

.search-results li:last-child {
  border-bottom: none;
}

.search-results li:hover {
  background-color: #f0f0f0;
}

.search-results li.selected {
  background-color: #007bff;
  color: white;
}

.no-results {
    padding: 10px;
    color: #777;
    text-align: center;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.modal-btn-cancel, .modal-btn-confirm {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}

.modal-btn-cancel {
  background-color: #6c757d;
  color: white;
}

.modal-btn-confirm {
  background-color: #28a745;
  color: white;
}
.modal-btn-confirm:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}
</style>