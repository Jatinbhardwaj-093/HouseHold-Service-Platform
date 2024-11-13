<script setup>
import Cross from '@/assets/svg/Cross.svg?raw'
import FillStar from '@/assets/svg/FillStar.svg?raw'

const { ServiceData } = defineProps({
    ServiceData: Object
})

</script>

<template>
    <div>
        <div class="descriptionContainer">
            <div class="serviceName">
                <p>{{ ServiceData.serviceName }}</p>
            </div>
            <div class="serviceDetail">
                <p>ID: {{ ServiceData.id }}</p>
                <p>Name: {{ ServiceData.professionalName }}</p>
                <p>+91 {{ ServiceData.contact }}</p>
                <p>Price: ₹ {{ ServiceData.price }}</p>
            </div>
            <div class="serviceDescription">
                <p class="descriptionHead">Description:</p>
                <p>{{ ServiceData.description }}</p>
            </div>
            <div class="rating">
                <p>Rating:</p>
                <p class="star-icon" v-for="i in 5" :key="i"><span v-html="FillStar"></span></p>
            </div>

            <div class="cross" @click="$emit('close')">
                <p v-html="Cross"></p>
            </div>
        </div>
    </div>
</template>

<style scoped>

.descriptionContainer {
    position: relative;
    width: 50vw;
    height: 50vh;
    display: grid;
    grid-template-columns: 0.8fr 1fr;
    grid-template-rows: 70px 1fr 70px;
    grid-template-areas:
        'heading heading'
        'detail description'
        'rating rating';
    gap: 0.7rem;
    background-color: #161414;
    box-shadow: 5px 5px 10px rgb(0, 0, 0);
    border-radius: 1rem;
    margin: auto;
}

.cross {
    position: absolute;
    right: 5px;
    top: 5px;
    width: 50px;
    height: 50px;
    cursor: pointer;
}

.serviceName {
    grid-area: heading;
    text-align: center;
    font-size: 3rem;
    color: #ff5c01;
    font-weight: bolder;
    font-weight: bolder;
    margin-top: 1rem;
    margin-bottom: 1rem;
}

.serviceDetail {
    grid-area: detail;
    text-align: start;
    font-size: 1.25rem;
    color: white;
    font-weight: bolder;
    padding: 2rem;
    padding-bottom: 0.5rem;
}
.serviceDetail p {
    margin: 4px;
}

.serviceDescription {
    grid-area: description;
    text-align: start;
    font-size: 1rem;
    color: white;
    font-weight: bolder;
    font-style: italic;
    padding: 2rem;
    padding-bottom: 0.5rem;
}

.descriptionHead {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}

.rating {
    grid-area: rating;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    gap: 0.25rem;
    font-size: 1rem;
    color: white;
    font-weight: bolder;
    font-style: italic;
}

.rating p {
    font-size: 1.5rem;
}

.star-icon {
    height: 25px;
    width: 25px;
}

</style>
