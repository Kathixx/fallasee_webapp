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
        <button @click="predict">
          Detect Fallacy
        </button>
      </div>
      <div class="row prediction">
        <div class="col-md-8 offset-2">
          <Fallacy></Fallacy>
        </div>
      </div>
    </div>
  </main>
</template>

<!-- https://heartbeat.comet.ml/deploying-a-text-classification-model-using-flask-and-vue-js-25b9aa7ff048 -->
<!-- <script>
import axios from 'axios'

export default {
  data () {
    return {
      textClassify: [],
      id: '',
      taskname: '',
      isEdit: false
    }
  },
  mounted () {
    this.getTasks()
  },
  methods: {
    getTasks () {
      axios({ method: 'GET', url: '/api/tasks' }).then(
        result => {
          console.log(result.data)
          this.textClassify = result.data
        },
        error => {
          console.error(error)
        }
      )
    },
    addNewTask () {
      axios.post('/api/task',
        { title: this.taskname })
        .then(res => {
          this.taskname = ''
          this.getTasks()
          console.log(res)
        }
        .catch(err => {
          console.log(err)
        })
      }
    }
}
</script> -->