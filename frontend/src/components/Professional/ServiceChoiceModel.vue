<script setup>
import NoImg from '@/assets/svg/NoImg.svg?raw'

const { showModal, ServiceData } = defineProps({
    showModal: Boolean,
    ServiceData: Array
})

const emit = defineEmits(['closeServiceChoiceModal']);

const selectService = (service) => {
    emit('closeServiceChoiceModal', service);
};

</script>

<template>
    <div v-if="showModal">
        <div class="container">
            <h2>Available Profession</h2>
            <div class="blocks">
                <div 
                    class="block" 
                    v-for="service in ServiceData" 
                    :key="service.id"
                    @click="selectService(service)"
                >
                    <img v-if="service.image" :src="service.image.filepath" alt="Service Image" />
                    <div v-else class="serviceImgHolder">
                        <p v-html="NoImg"></p>
                    </div>
                    <p class="serviceName">{{ service.name }}</p>
                    <p class="price">₹ {{ service.price }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}
</style>
<style scoped>
.container {
    width: 40vw;
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow: hidden;
    justify-content: center;
    margin: auto;
    margin: 1rem;
    background-color: #3c3c3c;
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.6);
    border-radius: 1rem;
    padding: 1rem;
}

h2 {
    color: white;
}

.blocks {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 0.5rem;
}

.block {
    background-color: black;
    width: 100px;
    height: 100px;
    border-radius: 0.5rem;
    box-shadow: 2px 5px 20px rgba(0, 0, 0, 0.6);
    padding-top: 5px;
    padding-left: 10px;
    display: flex;
    flex-direction: column;
    align-items: start;
    justify-content: center;
    gap: 3px;
}

.serviceName {
    color: #fff;
    font-size: 1rem;
    font-weight: bolder;
    font-style: italic;
}

.price {
    color: #10b80d;
    font-size: 0.7rem;
    
}

img, .serviceImgHolder {
    margin-bottom: 4px;
    margin-left: 20px;
    border-radius: 5px;

    height: 40px;
    width: 40px;
    background-color: bisque;
}
</style>
