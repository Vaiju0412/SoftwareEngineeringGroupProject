<template>
  <div>
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
            integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh"
            crossorigin="anonymous"/>
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
            crossorigin="anonymous"/>
    </head>
    <nav class="navbar navbar-expand-lg navbar-dark bg-info fixed-top">
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbar">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbar">
        <div class="navbar-nav">
          <a v-if="isUser" class="nav-item nav-link text-dark" @click="userHome">
            <i class="fa fa-home"></i>
          </a>
          <a v-if="isAdmin" class="nav-item nav-link text-dark" @click="home">
            <i class="fa fa-home"></i>
          </a>
          <a v-if="!isLoggedIn" class = "nav-item nav-link text-dark" @click="login"><i class = "fa fa-home"></i></a>
        </div>
        <div class="navbar-nav ml-auto">
          <a v-if="isUser" class="nav-item nav-link text-dark" @click="myBooks">MyBooks</a>
          <a v-if="isUser" class="nav-item nav-link text-dark" @click="userStats">Stats</a>
          <a v-if="isAdmin" class="nav-item nav-link text-dark" @click="requests">Requests</a>
          <a v-if="isAdmin" class="nav-item nav-link text-dark" @click="adminStats">Stats</a>
          <a v-if="isLoggedIn" class="nav-item nav-link text-dark" @click="logout">Logout</a>
          <a v-if="!isLoggedIn" class="nav-item nav-link text-dark" @click="admin">Admin</a>
          <a v-if="!isLoggedIn" class="nav-item nav-link text-dark" @click="SignUp">Sign Up</a>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'NavBar',
  computed: {
    isLoggedIn() {
      return !!sessionStorage.getItem('loggedIn');
    },
    isUser() {
      return sessionStorage.getItem('role') === 'user';
    },
    isAdmin() {
      return sessionStorage.getItem('role') === 'admin';
    }
  },
  methods: {
    logout() {
      sessionStorage.clear();
      this.$router.push('/');
    },
    admin() {
      this.$router.push('/admin');
    },
    myBooks() {
      this.$router.push('/myBooks');
    },
    userStats() {
      this.$router.push('/userStats');
    },
    requests() {
      this.$router.push('/viewRequest');
    },
    adminStats() {
      this.$router.push('/libStats');
    },
    userHome() {
      this.$router.push('/userHome');
    },
    home() {
      this.$router.push('/home');
    },
    SignUp() {
      this.$router.push('/sign-up');
    },
    login() {
      this.$router.push('/');
    },
  }
};
</script>

<style>
.navbar {
  background-color: #3b5998; /* Facebook blue */
  padding: 16px;
  font-family: 'Times New Roman', Times, serif;
}

.navbar ul {
  list-style-type: none;
  padding: 0;
  display: flex;
  justify-content: space-around;
}

.navbar li {
  display: inline;
}

.navbar a {
  color: white !important;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 4px;
  transition: font-weight 0.3s ease;
  cursor: pointer; /* Change cursor to pointer */
}

.navbar a:hover {
  font-weight: bold;
}

.navbar .fa {
  font-size: 18px;
}

.text-dark {
  color: white !important;
}
</style>
