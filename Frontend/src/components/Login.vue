<template>
  <NavBar />
  <div class="container">
    <div v-if="message" :class="{'alert-success': success, 'alert-danger': !success}" class="alert mt-3">
      {{ message }}
    </div>
    <div class="row">
      <div class="col-md-6">
        <br><br><br><br><br><br><br><br><br><br>
        <h1 class="white-text">e-Pustak: Your Digital Library</h1>
        <br>
        <h5 class="white-text" style="text-align: center; font-family: Lucida Handwriting, Cursive;">
          Escape, Explore, and Learn - Anytime, Anywhere
        </h5>
      </div>
      <div class="col-md-6">
        <br><br><br><br><br><br><br>
        <form @submit.prevent="handleSubmit">
          <div class="form-container">
            <h3 align="center">Login</h3>
            <div class="form-group text-left">
              <label for="user_id">User ID</label>
              <input type="text" v-model="user_id" class="form-control" id="user_id" placeholder="Enter UserID" />
            </div>
            <div class="form-group text-left">
              <label for="password">Password</label>
              <input type="password" v-model="password" class="form-control" id="password" placeholder="Enter Password" />
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
            <div class="mt-2">
              <span style="font-size: smaller;">Not yet registered? <a href="/signup">Click here</a></span>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import apiService from '@/services/apiService';
import NavBar from '@/components/Navbar.vue';
import { jwtDecode } from "jwt-decode";

export default {
  name: 'LibLogin',
  components: {
    NavBar
  },
  data() {
    return {
      user_id: '',
      password: '',
      message: '', 
      success: false 
    };
  },
  methods: {
    async handleSubmit() {
      try {
        const result = await apiService.post("/login", {
          user_id: this.user_id,
          password: this.password
        });

        if (result.status === 200) {
          const decodedToken = jwtDecode(result.data.accesstoken);
          const role = decodedToken.sub.role;
          const user_id = decodedToken.sub.user_id;
          
          sessionStorage.setItem("accesstoken", result.data.accesstoken);
          sessionStorage.setItem("role", role);
          sessionStorage.setItem("user_id", user_id);
          sessionStorage.setItem("loggedIn", true);
        
          this.message = 'Logged in successfully!';
          this.success = true;

          setTimeout(() => {
            this.$router.push('/home');
          }, 2000); 
          
        }
      } catch (error) {
        console.error('Login failed:', error);
        this.message = 'Invalid credentials. Please try again!';
        this.success = false;

      }
    }
  },
  mounted() {
    if (sessionStorage.getItem('loggedIn')) {
      this.$router.push('/userHome');
    }
  }
}
</script>

<style>
.container {
  margin-top: 50px;
}

.form-container {
  max-width: 500px;
  margin: auto;
}

.form-group {
  margin-bottom: 15px;
  text-align: left; 
}

.form-control {
  width: 100%;
  height: 40px;
  padding-left: 15px;
  border: 1px solid skyblue;
}

.btn-primary {
  width: 100%;
  height: 40px;
  background-color: skyblue;
  color: #fff;
  border: 1px solid skyblue;
  cursor: pointer;
}
</style>
