<template>
    <div v-if="showServiceModal" class="modal">
        <div v-if="serviceData">
            <img
                v-if="serviceData.image"
                :src="serviceData.image.filepath"
                :alt="serviceData.image.name"
            />
            <p class="serviceName">{{ serviceData.service_name }}</p>
            <p class="description">{{ serviceData.description }}</p>
            <p class ="price">₹ {{ serviceData.price }}</p>
            <div v-html="Cross" class="cross" @click="closeServiceModal"></div>
        </div>
        <div v-else><p>Loading</p></div>
    </div>
</template>

<script setup>
import Cross from '@/assets/svg/Cross.svg?raw';

const { showServiceModal, serviceData } = defineProps({
    showServiceModal: Boolean,
    serviceData: Object
})

const emit = defineEmits(['closeServiceModal'])

function closeServiceModal() {
    emit('closeServiceModal')
}

</script>

<style scoped>
.modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: min(400px, 90%);
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.8);
    background-color: #1c1b1b;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10000;
}

.serviceName {
    color: #ff5c01;
    text-align: center;
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

.description {
    margin-bottom: 0.2rem;
    color: beige;
}

.price {
    color: green;
    font-weight: bolder;
    font-size: 1rem;
    margin-top: 0.7rem;
}

.cross {
    position: absolute;
    top: 5px;
    right: 5px;
    width: 40px;
    height: 40px;
    cursor: pointer;
}
</style>
