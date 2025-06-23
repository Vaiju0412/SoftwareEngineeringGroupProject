<template>
    <div class="page-wrapper">
    <NavBar />
    <div class="container">
        <div v-if="message" :class="{'alert-success': success, 'alert-danger': !success}" class="alert mt-3">
        {{ message }}
        </div>
        <h1 class="page-title">Sign Up</h1>
        <form @submit.prevent="handleSubmit">
            <div class="form-container">
                <div class="form-group text-left">
                <label for="user_id">User ID</label>
                <input type="text" v-model="user_id" class="form-control" id="user_id" placeholder="Enter UserID" required/>
                </div>
                <div class="form-group text-left">
                <label for="firstName">First Name</label>
                <input type="text" v-model="firstName" class="form-control" id="firstName" placeholder="Enter your First Name" required/>
                </div>
                <div class="form-group text-left">
                <label for="password1">Password</label>
                <input type="password" v-model="password1" class="form-control" id="password1" placeholder="Enter Password" required/>
                </div>
                <div class="form-group text-left">
                <label for="password2">Confirm Password</label>
                <input type="password" v-model="password2" class="form-control" id="password2" placeholder="Confirm Password" required/>
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
            </div>
            </form>
        </div>
    </div>
  </template>
  
  <script>
  import apiService from '@/services/apiService';
  import NavBar from '@/components/Navbar.vue';
  export default {
    name: 'SignUp',
    components: {
    NavBar
  },
    data() {
      return {
        user_id: '',
        firstName: '',
        password1: '',
        password2: '',
        message: '', 
        success: false 
      };
    },
    methods: {
      async handleSubmit() {
        try{
            const result = await apiService.post("/signup", {
                user_id: this.user_id,
                firstName: this.firstName,
                password1: this.password1,
                password2: this.password2
            });
  
            if (result.status == 200) {

                this.message = 'Account created successfully!';
                this.success = true;

                setTimeout(() => {
                this.$router.push('/');
                }, 2000); 
            }
        }   catch(error){
            if (error.response) {
                if (error.response.status === 400) {
                    this.message = 'User already exists';
                } else if (error.response.status === 406) {
                    this.message = 'Passwords don\'t match. Please try again.';
                } else {
                    this.message = 'An error occurred';
                }
                } else {
                this.message = 'Network error';
                }
            }
        }
    },
    mounted() {
      if (sessionStorage.getItem('loggedIn')) {
        this.$router.push('/home');
      }
    }
  };
  </script>
  
  <style scoped>
  .page-wrapper {
  font-family: 'Times New Roman', Times, serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding-top: 80px;
}

.container {
  max-width: 600px;
  margin: 0 auto;
  background-color: #ffffff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.page-title {
  color: #333;
  font-size: 28px;
  margin-bottom: 30px;
  text-align: center;
  font-weight: bold;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 16px;
  color: #333;
}

.form-control {
  border-radius: 4px;
  border: 1px solid #ddd;
  padding: 10px;
  font-size: 16px;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
  color: #fff;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #004085;
}

.alert {
  padding: 15px;
  border-radius: 4px;
  font-size: 16px;
  text-align: center;
}

.alert-success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}
</style>
  