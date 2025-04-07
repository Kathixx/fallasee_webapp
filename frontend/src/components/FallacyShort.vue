<script setup>
import data from '../assets/definitions.json'
import { defineProps, ref, watch, onMounted } from 'vue'

const props = defineProps({
    label: Number,
    proba : Number,
    number_fa: Number
})

const definition = ref(null)
const title = ref(null)
const probability = ref(null)
const number_fa = ref(null)

function getDef(label, proba, number) {
    console.log('getDef!', label, proba, number)
    data.definitions.forEach((child) => {
        const id = child.id
        if (id === label) {
            definition.value = child.explanation
            title.value = child.fallacy
            let proba_hundred = proba * 100
            let proba_string = proba_hundred.toFixed(2) + ' %'
            probability.value = proba_string
            number_fa.value = number
        }
    })
}

watch(
    () => props.label, 
    (newLabel) => {
        getDef(newLabel, props.proba, props.number_fa) 
        console.log('watch:', props.label, props.proba, props.number_fa)
    },
    { immediate: true } 
)

onMounted(() => {
    getDef(props.label, props.proba, props.number_fa)
    console.log('mounted:', props.label, props.proba, props.number_fa)
})

</script>

<template>
    <div class="row fallacy-short">
        <div class="col-2">
            <div class="symbol"></div>
        </div>
        <div class="col-10">
            <h4>0{{number_fa}} prediction</h4>
            <h2>{{title}}</h2>
            <p>{{ definition }}</p>
            <div class ="fallacy-short-bottom">
                <RouterLink to="/">More about fallacies</RouterLink>
                <p class="bold">Probability: {{probability}}</p>
            </div>
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