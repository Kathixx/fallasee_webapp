<script setup>
  import Fallacy from '../components/Fallacy.vue'
</script>

<template>
  <main>
    <div class="row" id="detector">
      <div class="col-8 offset-2">
        <p>Fallacify can detect logical fallacies in a sentence or argument. Just write your sentence or argument in the field below.</p>
        <textarea v-model="fallacy" placeholder="Type your sentence here" ></textarea>
      </div>
      <div class="col-8 offset-2 button">
        <button @click="pushFallacy(fallacy)">
          Detect Fallacy
        </button>
      </div>
      <div class="row prediction">
        <div class="col-md-8 offset-2">
          <p> You wanted to detect a logical fallacy in this sentence/argument:</p>
          <p style="font-family: 'Montserrat-Bold';">{{ predicted_fallacy }}</p>
          <p>This is your result:</p>
          <p style="font-family: 'Montserrat-Bold';">{{ prediction }} {{ fallacy_label }}</p>
          <!-- <Fallacy></Fallacy> -->
        </div>
      </div>
    </div>
  </main>
</template>

<!-- https://heartbeat.comet.ml/deploying-a-text-classification-model-using-flask-and-vue-js-25b9aa7ff048 -->
<script>
import axios from 'axios'
axios.defaults.withCredentials = true;  // Ensure cookies are sent with requests

export default {
  data () {
    return {
      prediction: 'number',
      fallacy_label: 'label',
      fallacy : '',
      predicted_fallacy : ''
    }
  },
  // mounted () {
  //   this.getTasks()
  // },
  methods: {
    getPrediction () {
      // , withCredentials: true
      axios({ method: 'GET', url: 'http://localhost:5000/predict' }).then(
        result => {
          console.log(result.data)
          this.prediction = result.data.result
          this.fallacy_label = result.data.fallacy_label
        },
        error => {
          console.error(error)
        }
      )},
    pushFallacy () {
      this.predicted_fallacy = this.fallacy
      axios.post('http://localhost:5000/predict',
        { fa: this.fallacy }, 
        // { withCredentials: true }
        )
        .then(res => {
          this.fallacy = ''
          this.getPrediction()
          console.log(res)
        })
        .catch(err => {
          console.log(err)
        })
      }
  }
  
}
</script>