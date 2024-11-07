<script setup>
import axios from 'axios';
import { defineProps, defineEmits, ref } from 'vue';

const props = defineProps({
    showModal: Boolean,
    scheduleInfo: {
        type: Object,
        required: true
    }
});

const emits = defineEmits(['close']); 
const token = localStorage.getItem('token');


const serviceDate = ref('');

const servicebooking = async () => {
    try {
        const response = await axios.post(
            `http://127.0.0.1:5000/customer/service/${props.scheduleInfo.serviceId}/booking`,
            {
                professionalId: props.scheduleInfo.professionalId,
                serviceDate: serviceDate.value 
            },
            {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            }
        );
        console.log(response.data);
        emits('close');
    } catch (error) {
        console.error('Error occurred:', error.response ? error.response.data : error.message);
    }
};
</script>

<template>
    <div v-if="showModal" class="bookingContainer">
        <div>
            <label for="servicedate">Schedule Date</label>
            <input type="date" class="servicedate" id="servicedate" v-model="serviceDate" name="servicedate">
        </div>
        <div class="btn">
        <button @click="servicebooking" class="bookingBtn">Book</button>
        <button @click="$emit('close')" style="background-color: tomato; margin-left: 15px;" class="bookingBtn" >Cancel</button>
        </div>
    </div>
</template>


<style scoped>
.bookingContainer{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.7rem;
    width: 12rem;
    background-color: black;
    box-shadow: 5px 5px 10px rgb(0, 0, 0);
    border-radius: 1rem;
    padding: 1rem;
    margin: auto;
}


.servicedate{
    color: black; 
    font-weight: bolder;
    padding: 3px;
    text-align: center;
    width: 10rem;
}

label{
    color: #F5F5F5;
    font-size: 0.8rem;
}

.bookingBtn{

    width: 4rem;
    border-radius: 0.5rem;
    background-color: #6A94FF;
    border: none;
    padding: 0.2rem;
}
</style>