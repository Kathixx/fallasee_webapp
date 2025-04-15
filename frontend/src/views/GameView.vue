<script setup>

</script>

<template>
  <main>
    <div class="gameResultWrapper">
      <div class="gameResult" :class="[show ? 'start' : 'displayNone']">
       {{ result }}
      </div>
    </div>
    <div class="col-12 introduction">
      <p>Points: {{ points }} | Round: {{ round }}</p>
      <div class=" row gameWrapper">
        <p>{{ txt }}</p>
      </div>
      <div class="row gameButtons">
        <h3>{{ moderation }}</h3>
        <div class=" col-2 buttonWrapper adHominem">
          <div class="choices">
            <div class="circleWrapper" v-if="user_adHominem">
              <span class="user"><p>YOU</p></span>
            </div>
            <div class="circleWrapper" v-if="ai_adHominem">
              <span class="ai"><p>AI</p></span>
            </div>
          </div>
          <button :class="{'right' : btn_adHominem, 'disabled': isDisabled}" @click="check('adHominem')"  >Ad Hominem</button>
        </div>
        <div class=" col-2 buttonWrapper authority">
          <div class="choices">
            <div class="circleWrapper" v-if="user_authority">
              <span class="user"><p>YOU</p></span>
            </div>
            <div class="circleWrapper" v-if="ai_authority">
              <span class="ai"><p>AI</p></span>
            </div>
          </div>
          <button :class="{'right' : btn_authority, 'disabled': isDisabled}" @click="check('authority')"  >Appeal To Authority</button>
        </div>
        <div class=" col-2 buttonWrapper emotion">
          <div class="choices">
            <div class="circleWrapper" v-if="user_emotion">
              <span class="user"><p>YOU</p></span>
            </div>
            <div class="circleWrapper" v-if="ai_emotion">
              <span class="ai"><p>AI</p></span>
            </div>
          </div>
          <button :class="{'right' : btn_emotion, 'disabled': isDisabled}" @click="check('emotion')" >Appeal To Emotion</button>
        </div>
        <div class=" col-2 buttonWrapper dilemma">
          <div class="choices">
            <div class="circleWrapper" v-if="user_dilemma">
              <span class="user"><p>YOU</p></span>
            </div>
            <div class="circleWrapper" v-if="ai_dilemma">
              <span class="ai"><p>AI</p></span>
            </div>
          </div>
          <button :class="{'right' : btn_dilemma, 'disabled': isDisabled}" @click="check('dilemma')" >False Dilemma</button>
        </div>
        <div class=" col-2 buttonWrapper slope"> 
          <div class="choices">
            <div class="circleWrapper" v-if="user_slope">
              <span class="user"><p>YOU</p></span>
            </div>
            <div class="circleWrapper" v-if="ai_slope">
              <span class="ai"><p>AI</p></span>
            </div>
          </div>
          <button :class="{'right' : btn_slope, 'disabled': isDisabled}" @click="check('slope')" >Slippery Slope</button>
        </div>
        <div class=" col-2 buttonWrapper none">
          <div class="choices">
            <div class="circleWrapper" v-if="user_none">
              <span class="user"><p>YOU</p></span>
            </div>
            <div class="circleWrapper" v-if="ai_none">
              <span class="ai"><p>AI</p></span>
            </div>
          </div>
          <button :class="{'right' : btn_none, 'disabled': isDisabled}" @click="check('none')" >No Fallacy</button>
        </div>
      </div>
      <div class="row next">
        <button @click="nextRound()" >Next</button>
      </div>
    </div>
  </main>
</template>

<script>
import axios from 'axios'

axios.defaults.withCredentials = true; 

import data from '../assets/definitions.json'
const delay = ms => new Promise(res => setTimeout(res, ms));

export default {
  data() {
    return{
      points: 0,
      round: 0,
      txt : '',
      solution : '',
      prediction: '',
      isDisabled : false,
      btn_adHominem: false,
      btn_authority: false,
      btn_emotion: false,
      btn_dilemma: false,
      btn_slope: false,
      btn_none: false,
      user_adHominem : false,
      user_authority : false,
      user_emotion : false,
      user_dilemma : false,
      user_none : false,
      user_slope : false,
      ai_adHominem : false,
      ai_authority : false,
      ai_emotion : false,
      ai_dilemma : false,
      ai_none : false,
      ai_slope : false,
      moderation : 'Choose the right fallacy',
      result: '',
      show: false
    }
  },
  created(){
    this.getRandom()
  },
  methods: {
    async getRandom(){
      let random = Math.floor(Math.random() *data.game.length);
      this.txt = data.game[random].example
      this.solution = data.game[random].label
      await axios.post('http://localhost:5000/predict',
        { txt: this.txt }, 
      )
      .then(res => {
        this.prediction = this.getPrediction(res.data)
        console.log('Set prediction:' ,this.prediction)
      })
      .catch(err => {
        console.log(err)
      })
    },
    check(user) {
      this.setClasses(user)
      let current_result = ''
      if(user == this.solution) {
        this.points = this.points +1
        current_result = '+1'
        if (this.prediction != user) {
          this.points = this.points +1
          current_result = '+2'
        }
      }
      else current_result = ':/'
      this.result = current_result
    },
    nextRound() {
      this.round = this.round + 1
      this.reset()
      this.getRandom()
    },
    getPrediction (data) {
      let predictions = this.setPredictionArray(data)
      let max = Math.max.apply(null, predictions)
      let position = predictions.indexOf(max)
      return this.getLabel(position)
    },
    getLabel(fallacy) {
      if(fallacy == 0) { return 'adHominem'}
      if(fallacy == 1) { return 'authority'}
      if(fallacy == 2) { return 'emotion'}
      if(fallacy == 3) { return 'dilemma'}
      if(fallacy == 4) { return 'none'}
      if(fallacy == 5) { return 'slope'}
    },
    setPredictionArray(json_result) {
      let predictions = []
      for (var key in json_result){
        var value = json_result[key];
        predictions.push(value)
      }
      return predictions
    },
    async setClasses(user) {
      this.isDisabled = true
      this.moderation = 'You have chosen:'
      // User Icon
      if(user == 'adHominem') { this.user_adHominem = true}
      if(user == 'authority') { this.user_authority = true}
      if(user == 'emotion') { this.user_emotion = true}
      if(user == 'dilemma') { this.user_dilemma = true}
      if(user == 'none') { this.user_none = true}
      if(user == 'slope') { this.user_slope = true}
      await delay(1000);
      this.moderation = 'The AI has predicted...'
      let random = Math.floor((Math.random() * 1000)+1000);
      await delay(random);
      // AI Icon
      if(this.prediction == 'adHominem') { this.ai_adHominem = true}
      if(this.prediction == 'authority') { this.ai_authority = true}
      if(this.prediction == 'emotion') { this.ai_emotion = true}
      if(this.prediction == 'dilemma') { this.ai_dilemma = true}
      if(this.prediction == 'none') { this.ai_none = true}
      if(this.prediction == 'slope') { this.ai_slope = true}
      this.moderation = 'The correct answer is...'
      await delay(1000);
      // Button
      if(this.solution == 'adHominem') { this.btn_adHominem = true}
      if(this.solution == 'authority') { this.btn_authority = true}
      if(this.solution == 'emotion') { this.btn_emotion = true}
      if(this.solution == 'dilemma') { this.btn_dilemma = true}
      if(this.solution == 'none') { this.btn_none = true}
      if(this.solution == 'slope') { this.btn_slope = true}
      this.show = true
    },
    reset(){
      this.isDisabled = false,
      this.btn_adHominem =false,
      this.btn_authority =false,
      this.btn_emotion =false,
      this.btn_dilemma =false,
      this.btn_slope =false,
      this.btn_none =false,
      this.user_adHominem  =false,
      this.user_authority  =false,
      this.user_emotion  =false,
      this.user_dilemma  =false,
      this.user_none  =false,
      this.user_slope  =false,
      this.ai_adHominem  =false,
      this.ai_authority  =false,
      this.ai_emotion  =false,
      this.ai_dilemma  =false,
      this.ai_none  =false,
      this.ai_slope  =false,
      this.result = ''
      this.show = false
    },
    
  }
}

</script>