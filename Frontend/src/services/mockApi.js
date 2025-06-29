// src/services/mockApi.js

// This file simulates a backend API and database.
// The data is stored in memory and will be consistent across all pages
// for the duration of the user's session.

// --- SIMULATED DATABASE TABLES ---

const db = {
  // Corresponds to the User model, representing the CURRENT user's dependents.
  // This is the "CaregiverSeniorMap" for the logged-in user.
  users: [
    { id: 'dep_001', firstName: 'Eleanor', lastName: 'Vance', birthDate: '1958-05-15', relation: 'Mom', gender: 'female' },
    { id: 'dep_002', firstName: 'Hugh', lastName: 'Crain', birthDate: '1955-11-20', relation: 'Dad', gender: 'male' },
    { id: 'dep_003', firstName: 'Theo', lastName: 'Vance', birthDate: '1962-09-01', relation: 'Uncle', gender: 'male' },
  ],
  
  // A master list of ALL users in the system, for searching purposes.
  allSystemUsers: [
    { id: 'user_101', firstName: 'John', lastName: 'Doe', username: 'johndoe' },
    { id: 'user_102', firstName: 'Jane', lastName: 'Smith', username: 'janesmith' },
    { id: 'user_103', firstName: 'Peter', lastName: 'Jones', username: 'peterj' },
    { id: 'user_104', firstName: 'Mary', lastName: 'Williams', username: 'maryw' },
    // Include existing dependents here so they aren't searchable again initially
    { id: 'dep_001', firstName: 'Eleanor', lastName: 'Vance', username: 'eleanorv' },
    { id: 'dep_002', firstName: 'Hugh', lastName: 'Crain', username: 'hughc' },
    { id: 'dep_003', firstName: 'Theo', lastName: 'Vance', username: 'theov' },
  ],
  
  // Corresponds to the Medicine model (master list of all possible medicines)
  medicines: [
    { id: 1, title: 'Lisinopril', description: 'For high blood pressure.' },
    { id: 2, title: 'Metformin', description: 'For type 2 diabetes.' },
    { id: 3, title: 'Atorvastatin', description: 'To lower cholesterol.' },
    { id: 4, title: 'Amlodipine', description: 'For high blood pressure and angina.' },
    { id: 5, title: 'Albuterol', description: 'For asthma and COPD.' },
  ],
  
  // Corresponds to the UserMedMap model
  userMedMaps: [
    // Meds for "Mom" (dep_001)
    { id: 101, userId: 'dep_001', medicineId: 1, dosage: '10mg', breakfast_after: true },
    { id: 102, userId: 'dep_001', medicineId: 3, dosage: '20mg', dinner_after: true },
    // Meds for "Dad" (dep_002)
    { id: 103, userId: 'dep_002', medicineId: 2, dosage: '500mg', breakfast_after: true, dinner_after: true },
    { id: 104, userId: 'dep_002', medicineId: 4, dosage: '5mg', lunch_before: true },
  ],
};

// --- HELPER FUNCTIONS ---
const simulateDelay = (ms = 500) => new Promise(res => setTimeout(res, ms));

const calculateAge = (birthDate) => {
  if (!birthDate) return null;
  const today = new Date();
  const birth = new Date(birthDate);
  let age = today.getFullYear() - birth.getFullYear();
  const m = today.getMonth() - birth.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) {
    age--;
  }
  return age;
};

// --- MOCK API ENDPOINT FUNCTIONS ---

// GET /api/dependents
export async function getDependentsList() {
  await simulateDelay(300);
  console.log(`[Mock API] GET /api/dependents`);
  // Return a copy to prevent direct mutation from components
  return [...db.users];
}

// DELETE /api/dependents/:userId
export async function deleteDependent(userId) {
  await simulateDelay(300);
  console.log(`[Mock API] DELETE /api/dependents/${userId}`);
  const index = db.users.findIndex(d => d.id === userId);
  if (index > -1) {
    db.users.splice(index, 1);
    return { success: true };
  }
  return { success: false, message: 'Dependent not found.' };
}

// GET /api/users?search=... (For adding new dependents)
export async function searchAllUsers(query) {
  await simulateDelay(400);
  console.log(`[Mock API] GET /api/users?search=${query}`);
  if (!query) return [];
  
  // Find users from the master list who are NOT already in the dependents list
  const currentDependentIds = db.users.map(d => d.id);
  
  return db.allSystemUsers.filter(user => {
    const isAlreadyDependent = currentDependentIds.includes(user.id);
    const matchesQuery = user.username.toLowerCase().includes(query.toLowerCase()) ||
                         `${user.firstName} ${user.lastName}`.toLowerCase().includes(query.toLowerCase());
    return !isAlreadyDependent && matchesQuery;
  });
}

// POST /api/dependents
export async function addDependent(userToAdd) {
  await simulateDelay();
  console.log(`[Mock API] POST /api/dependents`, userToAdd);
  const isAlreadyDependent = db.users.some(d => d.id === userToAdd.id);
  if (isAlreadyDependent) {
    return { success: false, message: 'User is already a dependent.' };
  }
  
  // In a real app, you'd create a CaregiverSeniorMap entry. Here, we just add to the list.
  const newDependent = {
    ...userToAdd,
    relation: 'N/A', // Default relation
    gender: 'male', // Default gender
  };
  db.users.push(newDependent);
  return { success: true, dependent: newDependent };
}

// GET /api/user/:userId
export async function getDependentDetails(userId) {
  await simulateDelay();
  console.log(`[Mock API] GET /api/user/${userId}`);
  const user = db.users.find(u => u.id === userId);
  if (!user) return null;
  // Return data similar to what the backend would send
  return {
    ...user,
    age: calculateAge(user.birthDate),
  };
}

// GET /api/user/:userId/medications
export async function getDependentMedications(userId) {
  await simulateDelay();
  console.log(`[Mock API] GET /api/user/${userId}/medications`);
  const maps = db.userMedMaps.filter(m => m.userId === userId);
  
  // Join with medicine data, like the backend would
  const populatedMeds = maps.map(map => {
    const medicine = db.medicines.find(m => m.id === map.medicineId);
    return {
      ...map,
      medicineTitle: medicine ? medicine.title : 'Unknown Medicine',
    };
  });
  return populatedMeds;
}

// DELETE /api/medication-map/:mapId
export async function deleteMedicationMapping(mapId) {
  await simulateDelay(300);
  console.log(`[Mock API] DELETE /api/medication-map/${mapId}`);
  const index = db.userMedMaps.findIndex(m => m.id === mapId);
  if (index > -1) {
    db.userMedMaps.splice(index, 1);
    return { success: true, message: 'Medication deleted.' };
  }
  return { success: false, message: 'Medication not found.' };
}

// GET /api/medicines?search=...
export async function searchMasterMedicineList(query) {
  await simulateDelay(400);
  console.log(`[Mock API] GET /api/medicines?search=${query}`);
  if (!query) return [];
  return db.medicines.filter(m => 
    m.title.toLowerCase().includes(query.toLowerCase())
  );
}

// POST /api/medicines
export async function createNewMasterMedicine(title, description = '') {
  await simulateDelay();
  console.log(`[Mock API] POST /api/medicines with title: ${title}`);
  const newMedicine = {
    id: Date.now(), // simple unique ID
    title,
    description,
  };
  db.medicines.push(newMedicine);
  return newMedicine;
}

// POST /api/user/:userId/medications
export async function addMedicationToDependent(userId, medMapData) {
  await simulateDelay();
  console.log(`[Mock API] POST /api/user/${userId}/medications`, medMapData);
  const newMap = {
    id: Date.now(),
    userId,
    ...medMapData,
  };
  db.userMedMaps.push(newMap);
  
  // Return the newly created resource, joined with medicine data
  const medicine = db.medicines.find(m => m.id === newMap.medicineId);
  return {
    ...newMap,
    medicineTitle: medicine ? medicine.title : 'Unknown Medicine',
  };
}