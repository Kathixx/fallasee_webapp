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
const isAdHominem = ref(false)
const isAuthority = ref(false)
const isEmotion = ref(false)
const isDilemma = ref(false)
const isSlope = ref(false)
const isNone = ref(false)
const icon = ref(null)

function getDef(label, proba, number) {
    isAdHominem.value = false
    isAuthority.value = false
    isEmotion.value = false
    isDilemma.value = false
    isSlope.value = false
    isNone.value = false
    console.log('getDef!', label, proba, number)
    data.definitions.forEach((child) => {
        const id = child.id
        if (id === label) {
            definition.value = child.explanation
            console.log("get icon:", child.image_url)
            title.value = child.fallacy
            let proba_hundred = proba * 100
            let proba_string = proba_hundred.toFixed(2) + ' %'
            probability.value = proba_string
            number_fa.value = number
            icon.value = child.image_url
        }
    })
    if(label == 0) {
        isAdHominem.value = true
    }
    if(label == 1) {
        isAuthority.value = true
    }
    if(label == 2) {
        isEmotion.value = true
    }
    if(label == 3) {
        isDilemma.value = true
    }
    if(label == 4) {
        isSlope.value = true
    }
    if(label == 5) {
        isNone.value = true
    }
}

function imageUrl() {
    return icon.value
    // return new URL(`../assets/images/${icon.value}`, import.meta.url).href;
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
            <div class="symbol" :class="{'ad_hominem': isAdHominem, 'authority': isAuthority, 'emotion': isEmotion, 'dilemma': isDilemma, 'slope': isSlope, 'none' :isNone }">
                <img :src="imageUrl()">
            </div>
        </div>
        <div class="col-10">
            <h4>0{{number_fa}} prediction</h4>
            <h2>{{title}}</h2>
            <p>{{ definition }}</p>
            <div class ="fallacy-short-bottom">
                <RouterLink to="/logical-fallacies">More about fallacies</RouterLink>
                <p class="bold">Probability: {{probability}}</p>
            </div>
        </div>
        
    </div>
</template>

<style scoped>

</style>



<script>
// import data from '../assets/definitions.json'

// export default {
//     props: ['label', 'proba', 'number_fa'],
//     setup(props) {
//         // setup() receives props as the first argument.
//         console.log(props.label)
//         onMounted(()=> {
//             this.getDef(props.label, props.proba, props.number_fa)
//             console.log('mounted:', label, proba, number_fa)
//         })
//     },
//     data() {
//         return{
//         definition:null,
//         title: null,
//         icon: null,
//         probability: null,
//         number: null
//         }
//     },
//     // props: {
//     //     label: {
//     //     type: Number,
//     //     required: true
//     //     },
//     //     proba: {
//     //         type: Number,
//     //         required: true
//     //     },
//     //     number_fa: {
//     //         type: Number,
//     //         required: true
//     //     }
//     // },
//     watch: {
//         label(newLabel, oldLabel) {
//             getDef(newLabel, props.proba, props.number_fa) 
//             console.log('watch:', props.label, props.proba, props.number_fa)
//         }
//     },  
//     methods: {
//         getDef(label, proba, number) {
//             console.log('getDef!', label, proba, number)
//             data.definitions.forEach((child) => {
//                 let id = child.id
//                 if (id === label) {
//                     this.definition = child.explanation
//                     console.log("get icon:", child.image_url)
//                     this.title = child.fallacy
//                     let proba_hundred = proba * 100
//                     let proba_string = proba_hundred.toFixed(2) + ' %'
//                     this.probability = proba_string
//                     this.number = number
//                     this.icon = child.image_url
//                 }
//             })
//         },
//         imageUrl(){
//             return new URL(`../assets/images/${this.icon}`, import.meta.url).href;
//         }
//     },
//     computed() {
//         this.imageUrl()
//     }
// }

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