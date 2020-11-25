<template>
  <div id="app">
    <img src="./assets/logo.png" style="width:auto; max-width:150px">
    <h1>{{ msg }}</h1>
    <h2>Upload Image</h2>
    <input ref="file" name="file" type="file" accept="image/*" :disabled="selectedFile" @change="onFileChange">
    <button type="button" v-if="selectedFile" @click="removeImage">Remove image</button><br>
    <img id="inputImage" style="width:auto; max-width:300px"><br>
    <button type="button" class="btn btn-yellow" v-if="selectedFile" @click="onClickRequest">Request</button>
    <div v-if="testComplete">
      <h2>Melanoma probability : {{melanomaResult}}</h2>
    </div>
  </div>
</template>

<script>
import { melanoma } from '~/api/index'

export default {
  name: 'app',
  data () {
    return {
      msg: 'Welcome to CS470 Melanoma',
      selectedFile: undefined,
      melanomaResult: '',
      testComplete: false,
    }
  },
  methods: {
    onFileChange(e) {
      this.selectedFile = this.$refs.file.files[0];
      var fr = new FileReader()
      fr.onload = function () {
        document.getElementById('inputImage').src = fr.result;
      }
      fr.readAsDataURL(this.selectedFile)
    },

    removeImage() {
      this.selectedFile = undefined
      document.getElementById("inputImage").src = ''
      this.testComplete = false
    },

    onClickRequest() {
      this.requestHandler()
    },

    requestHandler() {
      melanoma.request(this.selectedFile)
        .then(response => {
          let probability = parseFloat(response.data.melanoma_probability) * 100
          probability = probability.toFixed(1)
          this.melanomaResult = `${probability}%`
          this.testComplete = true
        })
        .catch(error => {
          console.log(error)
        })
    },
  }
}
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

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

@mixin button-bg($bg) {
  background: $bg;
  &:hover {
    background:darken($bg,8%);
    transition: all 0.3s ease;
  }
  &:active {
    background:darken($bg,25%);
  } 
}

.btn {
  color:white;
  text-decoration:none;
  padding:5px 10px;
  border-radius:3px;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  font-size:2em;
  border: none;
}

.btn-yellow{
   @include button-bg(#f1c40f);
}
</style>
