<script setup>
import Cross from '../../assets/svg/Cross.svg?raw'
</script>


<template>
    <div>
        <div class="container">
        <div class="serviceName"><h1>Service Name</h1></div>
        <div class="description">Description</div>
        <div class="serviceDescription">This service provide best care and tidy solution for home cleaning and servicing. Negotiation on price can be done by the customer.</div>
        <div class="servicePrice">Price: ₹100000</div>
        <div v-html="Cross" class="cross"></div>
    </div>
    </div>
</template>


<style scoped>

.container{
    position: relative;
    color: white;
    width: min(400px,90%);
    margin: auto;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow:  5px 5px 10px rgba(0, 0, 0, 0.6);
    background-color: #000000;
}

.serviceName{
    color: #FF5C01;
    text-align: center;
    margin-bottom: 1rem;
}

.description{
    margin-bottom: 0.2rem;
}

.serviceDescription{
    font-size: 0.5rem;
    margin-bottom: 0.7rem;
}

.cross{
    position: absolute;
    top: 5px;
    right: 5px;
    width: 40px;
    height: 40px;
    cursor: pointer;
}
</style>