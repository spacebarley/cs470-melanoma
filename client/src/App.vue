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
    <div v-if="testComplete && melanomaProbability < 30">
      <h2>Thankfully the mole does not seems to be melanoma.</h2>
    </div>
    <div v-else-if="testComplete && melanomaProbability < 60">
      <h2>It is possible that the picture contains melanoma. It is recommended to seek detailed examination at a medical center.</h2>
    </div>
    <div v-else-if="testComplete && melanomaProbability < 100">
      <h2>It is very likely that the mole is melanoma. It is recommended to have a detailed examination at a medical center immediately.</h2>
    </div>
    <div v-if="testComplete" id="melanoma-info">
      <h2>Know more about melanoma</h2>
      <div>
        <p><b>Q. Why detecting melanoma early is important?</b></p>
        <p>A. melanoma is more dangerous because of its ability to spread to other organs more rapidly if it is not treated at an early stage.<br/>5-year survival rate for patients in the U.S. whose melanoma is detected early. The survival rate drops to 65% if the disease reaches the lymph nodes and 25% if it spreads to distant organs.</p>
      </div>
      <div>
        <p><b>Q. What is signs for melanoma?</b></p>
        <p>A. Remember <b>ABCDE</b>. 
        <p>A is for Asymmetry. Most melanomas are asymmetrical. </p>
        <div class="melanoma-info-picture">
          <img src="./assets/info/melanoma_1_Asymmetry-340x240.png" style="width:auto; max-width:600px">
          <p>A is for Asymmetry</p>
        </div>
        <p>B is for Border. Melanoma borders are tend to be uneven and may have scalloped or notched edges. Common moles tend to have smoother, more even borders.</p>
        <div class="melanoma-info-picture">
          <img src="./assets/info/melanoma_2_Border-340x240.png" style="width:auto; max-width:600px">
          <p>B is for Border</p>
        </div>
        <p>C is for Color. Multiple colors are a warning sign. While benign moles are usually a single shade of brown, a melanoma may have different shades of brown, tan or black. As it grows, the colors red, white or blue may also appear.</p>
        <div class="melanoma-info-picture">
          <img src="./assets/info/melanoma_3_Color-340x240.png" style="width:auto; max-width:600px">
          <p>C is for Color</p>
        </div>
        <p>D is for Diameter or Dark. It is idial to detect a melanoma when it is small. if lesion is same or larger than a 6mm, It is warning sign. Also look for moles that darker than others is important.</p>
        <div class="melanoma-info-picture">
          <img src="./assets/info/melanoma_4_Diameter-336x240.png" style="width:auto; max-width:600px">
          <p>D is for Diameter or Dark</p>
        </div>
        <p>E is for Evolving. Any change on your mole such as size, shape, color or elevation, and any new symptom in it such as bleeding, itching or crusting may be a warning sign of melanoma.</p>
      </div>
      <div>
        <p><b>Q. How can I recognize melanoma in early stage?</b></p>
        <p>A. There is starategy called <b>Ugly Duckling</b>. While most normal moles on your body is similar to other moles, melanoma stand out like ugly ducklings in comparison. It means comparing any suspicous mole to surrounding moles to determine whether it looks different from its neighbors.</p>
        <div>
          <img src="./assets/info/uglyducklings.jpg" style="width:auto; max-width:600px">
        </div>
      </div>
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
      melanomaProbability: -1,
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
          this.melanomaProbability = probability
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

#melanoma-info {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
  max-width: 600px;
  margin: auto;
}

.melanoma-info-picture {
  text-align: center;
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
