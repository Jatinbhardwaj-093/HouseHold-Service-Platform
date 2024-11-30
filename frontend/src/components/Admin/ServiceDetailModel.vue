<template>
    <div v-if="showServiceModal" class="modal">
        <div v-if="serviceData">
            <div class="serviceImageHolder">
                <img
                    v-if="serviceData.image_name"
                    :src=" 'http://127.0.0.1:5000/static/services_imgs/' + serviceData.image_name"
                    :alt="serviceData.image_name"
                class="imagePreview"
                />
                <p v-else v-html="Img" lass="imagePreview"></p>
            </div>
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
import Img from '@/assets/svg/Img.svg?raw'

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

.serviceImageHolder {
    margin: auto;
    height: 130px;
    width: 130px;
    background-color: rgb(255, 255, 255);
    border-radius: 1rem;
    margin-bottom: 1rem;
    padding: 0.7rem;

}

.imagePreview {
    width: 100%;
    height: 100%;
    object-fit: contain;
}
.serviceName {
    color: #ff5c01;
    font-size: 2rem;
    margin-bottom: 1rem;
}

.description {
    margin-bottom: 0.2rem;
    color: beige;
}

.price {
    color: rgb(6, 176, 6);
    font-weight: bolder;
    font-size: 1.25rem;
    margin-top: 1rem;
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
