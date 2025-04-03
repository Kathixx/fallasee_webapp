<script setup>
import data from '../assets/definitions.json'
import { defineProps, ref, watch, onMounted } from 'vue'

const props = defineProps({
    label: Number
})

const definition = ref(null)
const title = ref(null)

function getDef(label) {
    console.log('getDef!')
    data.definitions.forEach((child) => {
        const id = child.id
        if (id === label) {
            definition.value = child.explanation
            title.value = child.fallacy
        }
    })
}

watch(
    () => props.label, 
    (newLabel) => {
        getDef(newLabel) 
    },
    { immediate: true } 
)

onMounted(() => {
    getDef(props.label) 
})

</script>

<template>
    <div class="row">
        <div class="col-2">
            <div class="symbol"></div>
        </div>
        <div class="col-10">
            <h2>{{title}}</h2>
            <p>{{ definition }}</p>
            <RouterLink to="/logical_fallacies">More about fallacies</RouterLink>
        </div>
    </div>
</template>

<style scoped>
.row {
    margin: 2em 0px;
}
.symbol{
    background-color: var(--yellow);
    width: 100px;
    height: 100px;
    border-radius: 20px;
}
</style>

<script>


// export default {
//   data() {
//     return{
//       definition:null,
//       title: null
//     }
//   },
//   methods: {
//     getDef(label) {
//         data.definitions.forEach((child)=>{
//             const id = child.id
//             if(id == label){
//                 this.definition = child.explanation
//                 this.title = child.fallacy
//             }
//         })
//     }
//   },
//   mounted() {
//     this.getDef(props.label)
//   }
// }
</script>