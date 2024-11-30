<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import NoImg from '@/assets/svg/NoImg.svg?raw';

// State management
const servicesData = ref([]);           
const error = ref(null);

// Fetch all services
onMounted(async () => {
    const token = localStorage.getItem('customerToken');

    if (!token ) {
        window.location.href = '/'; 
    } else {
        try {
            const response = await axios.get('http://127.0.0.1:5000/customer/services', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            servicesData.value = response.data; 
        } catch (err) {
            error.value = 'Error: ' + (err.response ? err.response.data : err.message); 
        }
    }
});

// View service details
const viewService = async (serviceId) => {
    window.location.href = `/customer/service/${serviceId}`;
}
</script>


<template>
    <div>
        <div class="container">
        <div class="heading">   Services</div>
        <div class="blocks" >
            <div class="block" v-for="service in servicesData" :key="service.id" @dblclick="viewService(service.id)">
                <div class="serviceImageHolder">
                    <img v-if="service.image_name" 
                    :src="`http://127.0.0.1:5000/static/services_imgs/${service.image_name}`" 
                    alt="Service Image" 
                    class="imagePreview" />
                    <p v-else v-html="NoImg" class="imagePreview"></p>
                </div>
                <div class="serviceName">{{ service.name }}</div>
                <div class="servicePrice">₹ {{ service.price }}"</div>
            </div>
        </div>
    </div>
    </div>
</template>

<style scoped>

.container{
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow: hidden;
    justify-content: center;
    margin: auto;
    margin: 1rem;
    background-color: rgba(255, 255, 255, 0.05);
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.6);
    border-radius: 1rem;
    padding: 1rem;
}

.heading{
    width: 10rem;
    text-align: center;
    color: #fff;
    font-size: 2rem;
    font-weight: bolder;
    font-style: italic;
    margin-top: 1rem;
    background-image: linear-gradient(to right, #FF5C01, #993701 70%); 
    border-radius: 0.5rem;
    box-shadow: 2px 5px 20px rgba(0, 0, 0, 0.6);
}

.blocks{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 1rem;
    margin: 1rem;
}

.block{
    background-color: black;
    width: 140px;
    height: 140px;
    border-radius: 1rem;
    box-shadow: 2px 5px 20px rgba(0, 0, 0, 0.6);
    padding: 10px;
}

.block:hover{
    transform: scale(1.1);
    transition: ease-in-out 0.5;
    box-shadow: 1px 2px 10px rgba(255, 119, 0, 0.6);
}

.serviceName{
    color: #fff;
    font-size: 1rem;
    font-weight: bolder;
    white-space: nowrap;
    text-align: start;
    margin-top: 0.25rem;
    margin-bottom: 0.25rem;
    overflow: hidden;
}

.servicePrice{
    color: #3edf4e;
    font-size: .8rem;
    font-weight: bolder;
    text-align: start;
}

.serviceImageHolder {
    margin: auto;
    width: 90px;
    height: 70px;
    padding: 2px;
    margin-top: 3px;
    background-color: antiquewhite;
    border-radius: 0.25rem;
}

.imagePreview {
    width: 100%;
    height: 100%;
    margin: auto;
    object-fit: contain;
    overflow: hidden;
}

</style>