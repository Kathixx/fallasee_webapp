<script setup>
  import FallacyShort from '../components/FallacyShort.vue'
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
        <div class="col-md-8 offset-2" v-if="sentence_to_predict" >
          <h4> Sentence to predict:</h4>
          <div class="wrapper" >
            <p>{{ sentence_to_predict }}</p>
          </div>
          <FallacyShort :label=ordinal_label ></FallacyShort>
        </div>
        <div class="col-8 offset-2 fallacy-list" v-if="list.length >0">
          <div class="heading">
            <h2> Previous detections</h2>
            <button @click="clearLocalStorage" >
              Clear detection list
            </button>
          </div>
          <div class="table header">
            <div class="col-6">Sentence to predict</div>
            <div class="col-3">Fallacy</div>
            <div class="col-3">Probability</div>
          </div>
          <div class="table" v-for="(value, key) in list">
            <div class="col-6">{{value.sentence}}</div>
            <div class="col-3">{{value.label}}</div>
            <div class="col-3">{{value.proba}}</div>
          </div>
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
      ordinal_label: null,
      fallacy_label: null,
      sentence : '',
      sentence_to_predict : null,
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
      let newEntry = {
        'sentence': this.sentence,
        'label': JSONdata.fallacy,
        'proba': "tbd"
      }
      this.list.push(newEntry)
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
        this.getPrediction()
        console.log("push Fallacy res:", res)
        this.setFallacyToLocalStorage(res.data, this.sentence)
        this.sentence = ''
      })
      .catch(err => {
        console.log(err)
      })
    },
  }
  
}
</script>