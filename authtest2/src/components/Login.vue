<template>
  <div class="box">
    <div class="card">
      <button type="button" name="button" v-on:click="login_purecloud">Log in with Purecloud</button>
      <a :href="'https://login.mypurecloud.ie/oauth/authorize?client_id=' + PCP_CLIENT_ID + '&response_type=code&redirect_uri=http://localhost:5000/oauth/callback'">Login with Purecloud</a>

    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Login',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      PCP_CLIENT_ID: process.env.PCP_CLIENT_ID
    }
  },
  methods: {
    login_purecloud: function () {
      axios.get('http://localhost:5000/oauth/purecloud/login')
        .then(response => {
          console.log('success')
          console.log(response.data)
          this.$router.push(response.data.redirect_to)
        })
        .catch(error => {
          console.log('error')
          console.log(error)
          console.log(error.response)
          console.log(error.response.data)
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
