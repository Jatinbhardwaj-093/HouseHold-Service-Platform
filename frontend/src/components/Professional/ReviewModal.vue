<script setup>
import FillStar from '@/assets/svg/FillStar.svg?raw'
import Cross from '@/assets/svg/Cross.svg?raw'

const { ReviewData} = defineProps({
    ReviewData: Object
})


</script>

<template>
    <div>
        <div class="container">
            <h1>{{ ReviewData.customerName }}</h1>
            <p class="review">{{ ReviewData.review }}</p>
            <div class="rating">
                <p class="star-icon" v-for="i in ReviewData.rating" :key="i">
                    <span  v-html="FillStar"></span>
                </p>
            </div>
            <div class="cross">
                <p @click="$emit('closeModal')" v-html="Cross"></p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.container {
    position: relative;
    height: 50vh;
    width: 45vw;
    background-color: #333;
    color: white;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 6px 8px 25px rgba(0, 0, 0, 0.8);

}

h1 {
    font-size: 2.5rem;
    font-weight: bolder;
    color: orange;
    text-align: center;
}

.review {
    font-size: 1.25rem;
    margin: 1.2rem;
    height: 20vh;
    overflow: auto;
}

.rating{
    display: flex;
    align-items: end;
    gap: 0.5rem;
    justify-content: center;
}

.star-icon {
    height: 50px;
    width: 50px;
    
}

.cross {
    position: absolute;
    top: 3%;
    left: 88%;
    height: 50px;
    width: 50px;
    cursor: pointer;
}
</style>