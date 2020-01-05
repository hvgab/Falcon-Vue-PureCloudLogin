<template>
  <div class="box">
    <div class="card">
      <button type="button" name="button" v-on:click="cookieprinter">Print Cookies</button>
    </div>
    <div class="card">
      <code>{{ cookies }}</code>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Brace from 'vue-bulma-brace'
export default {
  components: {
    Brace
  },
  name: 'CookiePrinter',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      cookies: '',
      code: ''
    }
  },
  methods: {
    cookieprinter: function () {
      axios.get('http://localhost:5000/cookieprinter', {withCredentials: true})
        .then(response => {
          console.log('success')
          console.log(response.data)
          console.log(response.data.cookies)
          console.log(response.data.session)
          this.cookies = response.data
          this.code = response.data
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
