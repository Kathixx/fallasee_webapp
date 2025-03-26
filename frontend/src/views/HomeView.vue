<script setup>
</script>

<template>
  <main>
    <div>
      <h1>Hello Aylin, Maren & Parya, this is our webapp! Wuhuu!</h1>
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