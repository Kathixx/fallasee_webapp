<script setup>
  import Fallacy from '../components/Fallacy.vue'

</script>

<template>
  <main>
    <div class="row" id="fallacy">
      <h1>Logical Fallacies</h1>
      <div v-for="item in definitions" :key ="item.id">
        <Fallacy :title="item.fallacy" :explanation="item.explanation"></Fallacy>
      </div>

    </div>
  </main>
</template>

<!-- https://heartbeat.comet.ml/deploying-a-text-classification-model-using-flask-and-vue-js-25b9aa7ff048 -->
<script>

import data from '../assets/definitions.json'

export default {
  data() {
    return{
      definitions:null
    }
  },
  methods: {
    getAll(){
      this.definitions = data.definitions
    }
  },
  mounted() {
    this.getAll()
  }
}
</script>