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
          <div class="result" v-if="predictionReady" v-for="(value, key) in resultList">
            <FallacyShort :label=value.fallacy :proba=value.proba ></FallacyShort>
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
            <div class="col-2">Result</div>
            <div class="col-2">Confidence</div>
            <div class="col-2">Probability</div>
          </div>
          <div class="table" v-for="(value, key) in list">
            <div class="col-6">{{value.sentence}}</div>
            <div class="col-2">{{value.label}}</div>
            <div class="col-2">{{value.confidence}}</div>
            <div class="col-2">{{value.proba}}</div>
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
      resultList: [],
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
    setPredictionArray(json_result) {
      let predictions = []
      for (var key in json_result){
        var value = json_result[key];
        predictions.push(value)
      }
      return predictions
    },
    async getPrediction () {
      await axios.get('http://localhost:5000/predict').then(
        result => {
          console.log("get Prediction:", result.data)
          this.resultList = []
          let predictions = this.setPredictionArray(result.data)
          let max = Math.max.apply(null, predictions)
          let position = predictions.indexOf(max)
          if (max >= 0.9) {
            let item = {'fallacy': position, 'proba':max}
            this.resultList.push(item)
            console.log('show only one fallacy', max)
          }
          else {
            let item = {'fallacy': position, 'proba':max}
            this.resultList.push(item)
            let currentPreds = predictions
            currentPreds.splice(position, 1)
            let max2 =  Math.max.apply(null, currentPreds)
            let position2 = predictions.indexOf(max2)
            let item2 = {'fallacy': position2, 'proba':max2}
            this.resultList.push(item2)
            console.log('show more fallacies:', max, max2)
          }
          console.log('resultList:', this.resultList)
          this.predictionReady = true
          this.setFallacyToLocalStorage(position, max, this.sentence)
          this.sentence = ''
          // // this.first_pred = result.data.first_pred
          // // this.first_label = result.data.first_label
          // // this.first_proba = result.data.first_proba
          // // this.second_pred = result.data.second_pred
          // // this.second_label = result.data.second_label
          // // this.second_proba = result.data.second_proba
          // this.first_pred = 'fd'
          // this.first_label = 'fd'
          // this.first_proba = 0
          // this.second_pred = 'fd'
          // this.second_label = 'fd'
          // this.second_proba = 0
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
    getLabel(fallacy) {
      if(fallacy == 0) { return 'Ad Hominem'}
      if(fallacy == 1) { return 'Appeal to Authority'}
      if(fallacy == 2) { return 'Appeal to Emotion'}
      if(fallacy == 3) { return 'False Dilemma'}
      if(fallacy == 4) { return 'Slippery Slope'}
      if(fallacy == 5) { return 'No Fallacy'}},
    getConfidence(proba) {
      let confidence
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
    setFallacyToLocalStorage(fallacy, proba, sentence){
      if (localStorage.getItem("FallacyList") != null) {
        this.data = localStorage.getItem('FallacyList')
        console.log('found local storage:', this.data)
        this.list = JSON.parse(this.data)
      } 
      let newEntry = {
        'sentence': sentence,
        'label': this.getLabel(fallacy),
        'proba': this.calculate(proba),
        'confidence': this.getConfidence(proba),

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
      })
      .catch(err => {
        console.log(err)
      })
    },
  }
  
}
</script>