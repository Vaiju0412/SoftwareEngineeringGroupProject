<!-- SignupForm.vue -->
<template>
  <div class="signup-wrapper">
    <div class="form-container">
      <h1>Signup</h1>

      <form @submit.prevent="register">
        <label>First Name</label>
        <input type="text" v-model="firstName" required />

        <label>Last Name</label>
        <input type="text" v-model="lastName" required />

        <label>Username</label>
        <input type="text" v-model="username" required />

        <label>Password</label>
        <input type="password" v-model="password" required />

        <label>Confirm Password</label>
        <input type="password" v-model="confirmPassword" required />

        <label>Role</label>
        <input type="text" v-model="role" required />

        <button type="submit">Register</button>
      </form>

      <p v-if="message" :class="{ error: isError, success: !isError }">{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/services/apiService'

const router = useRouter()

const firstName = ref('')
const lastName = ref('')
const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const role = ref('')

const message = ref('')
const isError = ref(false)

async function register() {
  try {
    const response = await axios.post('/auth/signup', {
      first_name: firstName.value,
      last_name: lastName.value,
      username: username.value,
      password: password.value,
      confirm_password: confirmPassword.value,
      role: role.value,
    })
    message.value = response.data.message
    isError.value = false

    // Delay redirection to login to show the message
    setTimeout(() => {
      router.push('/login')
    }, 1500)
  } catch (error) {
    if (error.response && error.response.data && error.response.data.message) {
      message.value = error.response.data.message
    } else {
      message.value = 'Signup failed due to a server error.'
    }
    isError.value = true
  }
}
</script>

<style scoped>
.signup-wrapper {
  background-color: #d6eed6;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 20px;
}

.form-container {
  background-color: #a2d4f2;
  padding: 2rem;
  border-radius: 20px;
  width: 300px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

h1 {
  text-align: center;
  margin-bottom: 1.5rem;
}

form {
  display: flex;
  flex-direction: column;
}

label {
  margin: 0.5rem 0 0.2rem;
  font-weight: bold;
}

input {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #e2e2e2;
}

button {
  margin-top: 1.5rem;
  padding: 0.6rem;
  background-color: #2962ff;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

button:hover {
  background-color: #0039cb;
}

p.success {
  color: green;
  margin-top: 1rem;
  text-align: center;
}

p.error {
  color: red;
  margin-top: 1rem;
  text-align: center;
}
</style>
