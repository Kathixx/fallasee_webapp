<script setup>
import FallacyShort from '../components/FallacyShort.vue'
</script>

<template>
  <main>
    <div class="row" id="detector">
      <div class="col-8 offset-2">
        <p>FallaSee can detect logical fallacies in a sentence or argument. Just write your sentence or argument in the field below.</p>
        <textarea v-model="sentence" placeholder="Type your sentence here (max. 200 words)" ></textarea>
      </div>
      <div class="col-8 offset-2 button">
        <button @click="pushFallacy(sentence)">
          detect fallacy
        </button>
      </div>
      <div class="row prediction">
        <div class="col-md-8 offset-2" v-if="sentence_to_predict" >
          <div class="sentence">
            <h4> Sentence to predict:</h4>
            <div class="wrapper" >
              <p>{{ sentence_to_predict }}</p>
            </div>
          </div>
          <div class="result" v-if="predictionReady">
            <FallacyShort :label=first_pred :proba=first_proba :number_fa=1 ></FallacyShort>
            <FallacyShort :label=second_pred :proba=second_proba :number_fa=2 ></FallacyShort>
          </div>
          <div class="result" v-else>
            <h2>Loading ...</h2>
          </div>
        </div>
        <div class="col-8 offset-2 fallacy-list" v-if="list.length >0">
          <div class="heading">
            <h2> Previous results</h2>
            <button @click="clearLocalStorage" >  
              clear list
            </button>
          </div>
          <div class="table header">
            <div class="col-6">Sentence to predict</div>
            <div class="col-2">Results</div>
            <div class="col-2">Confidence</div>
            <div class="col-2">Probability</div>
          </div>
          <div class="table" v-for="(value, key) in list">
            <div class="col-6">{{value.sentence}}</div>
            <div class="col-2">{{value.first_label}}</div>
            <div class="col-2">{{value.first_confidence}}</div>
            <div class="col-2">{{value.first_proba}}</div>
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
      first_pred: null,
      first_label: null,
      first_proba: null,
      first_confidence: null,
      second_pred: null,
      second_label: null,
      second_proba: null,
      second_confidence : null,
      sentence : '',
      sentence_to_predict : null,
      data: '',
      list: [],
      newEntry : {},
      predictionReady : false
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
   async getPrediction () {
    await axios.get('http://localhost:5000/predict').then(
        result => {
          console.log("get Prediction:", result.data)
          this.first_pred = result.data.first_pred
          this.first_label = result.data.first_label
          this.first_proba = result.data.first_proba
          this.second_pred = result.data.second_pred
          this.second_label = result.data.second_label
          this.second_proba = result.data.second_proba
        },
        error => {
          console.error(error)
        }
      )
    },
    calculate(proba) {
      let proba_hundred = proba * 100
      return proba_hundred.toFixed(2) + ' %'
    },
    getConfidence(proba) {
      
      if (proba > 0.9){
        confidence = 'pretty sure'
        this.first_confidence = confidence
        return confidence
      }
      else if (proba > 70) {
        confidence = 'very sure'
        this.first_confidence = confidence
        return confidence
      }
      else if (proba > 50) {
        confidence = 'sure'
        this.first_confidence = confidence
        return confidence
      }
      else if (proba > 30 ) {
        confidence = 'little sure'
        this.first_confidence = confidence
        return confidence
      }
      else {
        confidence = 'not sure'
        this.first_confidence = confidence
        return confidence
      }
      
    },
    setFallacyToLocalStorage(JSONdata, sentence){
      if (localStorage.getItem("FallacyList") != null) {
        this.data = localStorage.getItem('FallacyList')
        console.log('found local storage:', this.data)
        this.list = JSON.parse(this.data)
      } 
      console.log('JSONdata', JSONdata)
      let newEntry = {
        'sentence': this.sentence,
        'first_label': JSONdata.first_label,
        'first_proba': this.calculate(JSONdata.first_proba),
        'first_confidence': this.getConfidence(JSONdata.first_proba),
        'second_label': JSONdata.second_label,
        'second_proba': JSONdata.second_proba,
      }
      this.list.push(newEntry)
      localStorage.setItem('FallacyList', JSON.stringify(this.list))
      console.log('Set local storage:', this.list)
      console.log('Get local storage:', localStorage.getItem('FallacyList'))
    },
    async pushFallacy () {
      this.predictionReady = false
      this.sentence_to_predict = this.sentence
      // this.setFallacyToLocalStorage(this.fallacy)
      await axios.post('http://localhost:5000/predict',
        { txt: this.sentence }, 
      )
      .then(res => {
        this.getPrediction()
        this.predictionReady = true
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