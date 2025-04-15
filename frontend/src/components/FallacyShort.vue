<script setup>
import data from '../assets/definitions.json'
import { defineProps, ref, watch, onMounted } from 'vue'

const props = defineProps({
    label: Number,
    proba : Number,
    confidence: String
})

const definition = ref(null)
const title = ref(null)
const confidence = ref(null)
const probability = ref(null)
const isAdHominem = ref(false)
const isAuthority = ref(false)
const isEmotion = ref(false)
const isDilemma = ref(false)
const isSlope = ref(false)
const isNone = ref(false)
const icon = ref(null)
const isNotConfident = ref(false)

function getDef(label, proba, conf) {
    isAdHominem.value = false
    isAuthority.value = false
    isEmotion.value = false
    isDilemma.value = false
    isSlope.value = false
    isNone.value = false
    isNotConfident.value = false
    console.log('getDef!', label, proba, conf)
    data.definitions.forEach((child) => {
        const id = child.id
        if (id === label) {
            definition.value = child.explanation
            confidence.value = conf
            console.log("get icon:", child.image_url)
            title.value = child.fallacy
            let proba_hundred = proba * 100
            let proba_string = proba_hundred.toFixed(2) + ' %'
            probability.value = proba_string
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
        isNone.value = true
    }
    if(label == 5) {
        isSlope.value = true
    }
    if (label == 6) {
        isNotConfident.value = true
    }
    console.log('isNotConfidence: ', isNotConfident.value, 'confidence: ', confidence.value, 'isNone: ', isNone.value)

}

function imageUrl() {
    return icon.value
    // return new URL(`../assets/images/${icon.value}`, import.meta.url).href;
}



watch(
    () => props.label, 
    (newLabel) => {
        getDef(newLabel, props.proba, props.confidence) 
        console.log('watch:', props.label, props.proba, props.confidence)
    },
    { immediate: true } 
)


onMounted(() => {
    getDef(props.label, props.proba, props.confidence)
    console.log('mounted:', props.label, props.proba, props.confidence)
})

</script>

<template>
    <div class="row fallacy-short">
        <div class="col-2">
            <div class="symbol" :class="{'ad_hominem': isAdHominem, 'authority': isAuthority, 'emotion': isEmotion, 'dilemma': isDilemma, 'slope': isSlope, 'none' :isNone, 'notConfident': isNotConfident }">
                <img :src="imageUrl()">
            </div>
        </div>
        <div class="col-10">
            <h2>{{title}}</h2>
            <p v-if="!isNotConfident && confidence != 'chance' && !isNone">I'm <span class="bold">{{ confidence }}</span> in your sentence is the fallacy: {{title}}.</p>
            <p v-if="!isNotConfident && confidence != 'chance' && isNone">I'm <span class="bold">{{ confidence }}</span> in your sentence is no fallacy.</p>
            <p v-if = "confidence === 'chance'">There might be a chance that your text also contains the fallacy {{ title }}.</p>
            <p>{{ definition }}</p>
            <div class ="fallacy-short-bottom" v-if="!isNotConfident">
                <RouterLink to="/logical-fallacies">More about fallacies</RouterLink>
                <p class="bold">Probability: {{probability}}</p>
            </div>
        </div>
        
    </div>
</template>

<style scoped>

</style>



<script>

</script>