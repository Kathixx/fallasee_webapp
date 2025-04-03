<script setup>
  import Fallacy from '../components/Fallacy.vue'
</script>

<template>
  <main>
    <div class="row" id="detector">
      <div class="col-8 offset-2">
        <p>Fallacify can detect logical fallacies in a sentence or argument. Just write your sentence or argument in the field below.</p>
        <textarea v-model="sentence" placeholder="Type your sentence here" ></textarea>
      </div>
      <div class="col-8 offset-2 button">
        <button @click="pushFallacy(sentence)">
          Detect Fallacy
        </button>
      </div>
      <div class="row prediction">
        <div class="col-md-8 offset-2">
          <p> You wanted to detect a logical fallacy in this sentence/argument:</p>
          <p style="font-family: 'Montserrat-Bold';">{{ sentence_to_predict }}</p>
          <p>This is your result:</p>
          <p style="font-family: 'Montserrat-Bold';">{{ ordinal_label }} {{ fallacy_label }}</p>
          <p> Fallacy List</p>
          <li v-for="(value, key) in list" :key = "id">
            sentence: {{value.sentence}} || detected fallacy: {{ value.label}} || probability: {{ value.proba}}
          </li>
          <button @click="clearLocalStorage">
            Clear Fallacy List
          </button>
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
      ordinal_label: 'number',
      fallacy_label: 'label',
      sentence : '',
      sentence_to_predict : '',
      data: '',
      list: [],
      newEntry : {}
    }
  },
  created () {
    this.getLocalStorage()
  },
  methods: {
    getLocalStorage(){
      if (localStorage.getItem("FallacyList") != null) {
        this.data = localStorage.getItem('FallacyList')
        console.log('found local storage:', this.data)
        this.list = JSON.parse(this.data)
      } 
    },
    clearLocalStorage() {
      localStorage.clear()
      this.list = []
    },
    getPrediction () {
      // , withCredentials: true
      axios({ method: 'GET', url: 'http://localhost:5000/predict' }).then(
        result => {
          console.log("get Prediction:", result.data)
          this.ordinal_label = result.data.result
          this.fallacy_label = result.data.fallacy_label
        },
        error => {
          console.error(error)
        }
      )},
    setFallacyToLocalStorage(JSONdata, sentence){
      if (localStorage.getItem("FallacyList") != null) {
        this.data = localStorage.getItem('FallacyList')
        console.log('found local storage:', this.data)
        this.list = JSON.parse(this.data)
      } 
      this.newEntry = {
        'id': Math.random(),
        'sentence': sentence,
        'label': JSONdata.fallacy,
        'proba': "tbd"
      }
      this.list.push(this.newEntry)
      localStorage.setItem('FallacyList', JSON.stringify(this.list))
      console.log('Set local storage:', this.list)
      console.log('Get local storage:', localStorage.getItem('FallacyList'))
    },
    pushFallacy () {
      this.sentence_to_predict = this.sentence
      // this.setFallacyToLocalStorage(this.fallacy)
      axios.post('http://localhost:5000/predict',
        { txt: this.sentence }, 
        // { withCredentials: true }
      )
      .then(res => {
        this.fallacy = ''
        this.getPrediction()
        console.log("push Fallacy res:", res)
        this.setFallacyToLocalStorage(res.data, this.sentence)
      })
      .catch(err => {
        console.log(err)
      })
    },
  }
  
}
</script>