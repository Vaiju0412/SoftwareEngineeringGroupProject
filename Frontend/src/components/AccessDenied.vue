<template>
  <div class="access-denied-container">
    <h1>Access Denied</h1>
    <p>You do not have the necessary permissions to view this page.</p>
    <router-link to="/">Go to Home Page</router-link>
  </div>
</template>

<style scoped>
.access-denied-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 80vh;
  text-align: center;
  font-family: Arial, sans-serif;
}
h1 {
  color: #dc3545;
  margin-bottom: 1rem;
}
p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
}
a {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 5px;
}
</style>