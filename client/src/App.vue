<template>
  <div id="app">
    <v-app>
      <v-main>
        <v-container>
          <img src="./assets/logo.png" style="width:auto; max-width:150px; margin-bottom:15px;">
          <h1>{{ msg }}</h1>
          <div style="margin-top:3rem; margin-bottom:2rem;">
            <image-uploader
              :preview="true"
              outputFormat="blob"
              :className="['fileinput', { 'fileinput--loaded' : selectedFile != undefined }]"
              capture="environment"
              accept="image/*"
              @input="setImage"
            >
              <label for="fileInput" slot="upload-label">
                <figure>
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="32"
                    height="32"
                    viewBox="0 0 32 32"
                  >
                    <path
                      class="path1"
                      d="M9.5 19c0 3.59 2.91 6.5 6.5 6.5s6.5-2.91 6.5-6.5-2.91-6.5-6.5-6.5-6.5 2.91-6.5 6.5zM30 8h-7c-0.5-2-1-4-3-4h-8c-2 0-2.5 2-3 4h-7c-1.1 0-2 0.9-2 2v18c0 1.1 0.9 2 2 2h28c1.1 0 2-0.9 2-2v-18c0-1.1-0.9-2-2-2zM16 27.875c-4.902 0-8.875-3.973-8.875-8.875s3.973-8.875 8.875-8.875c4.902 0 8.875 3.973 8.875 8.875s-3.973 8.875-8.875 8.875zM30 14h-4v-2h4v2z"
                    ></path>
                  </svg>
                </figure>
                <span class="upload-caption">{{
                  selectedFile != undefined ? "Replace" : "Click to upload"
                }}</span>
              </label>
            </image-uploader>
          </div>
          <v-btn
            color="primary"
            rounded
            v-if="selectedFile"
            @click="onClickRequest"
          >
            Request
          </v-btn>

          <div v-if="testComplete" style="margin-top:20px; margin-bottom:5px;">
            <h3>Melanoma probability : </h3><h1><strong>{{melanomaResult}}</strong></h1>
          </div>
          <div v-if="testComplete && melanomaProbability < 30">
            <h1 style="color:green">The mole does not seem to be melanoma.</h1>
          </div>
          <div v-else-if="testComplete && melanomaProbability < 60">
            <h1 style="color:orange">It is possible that the picture contains melanoma.<br>We recommend you to have a detailed examination later.</h1>
          </div>
          <div v-else-if="testComplete && melanomaProbability < 100">
            <h1 style="color:red">It is very likely that the mole is melanoma.<br>We strongly recommend you to have a detailed examination immediately.</h1>
          </div>
          <div v-if="testComplete" id="melanoma-info" style="margin-top:35px;">
            <h2 style="color:gray">Know more about melanoma</h2>
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
          <div style="height:100px;">
          </div>
        </v-container>
      </v-main>
    </v-app>
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
    setImage(input) {
      this.selectedFile = input
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
  margin-top: 40px;
}

#fileInput {
  display: none;
  margin: 20px;
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

</style>
