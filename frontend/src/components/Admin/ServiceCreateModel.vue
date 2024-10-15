<template>
    <div v-if="showModal" class="modal">
        <form @submit.prevent="submitForm">
            <div class="serviceImg">
                <p v-html="Img"></p>
                <input type="file" class="ImgFilePath" @change="imgPath" accept="image/*" />
            </div>
            <input
                type="text"
                class="serviceName"
                placeholder="SERVICE NAME"
                v-model="formData.serviceName"
            />
            <textarea
                class="serviceDescription"
                placeholder="DESCRIPTION....."
                v-model="formData.Description"
            ></textarea>
            <input
                type="number"
                class="servicePrice"
                placeholder="PRICE"
                v-model="formData.servicePrice"
            />
            <button type="submit" class="btn">Add</button>
        </form>
        <div v-html="Cross" class="cross" @click="closeModal"></div>
    </div>
    <div class="modal-background" @click="closeModal"></div>
</template>

<script setup>
import Img from '@/assets/svg/Img.svg?raw'
import Cross from '@/assets/svg/Cross.svg?raw'

import { ref } from 'vue'
import axios from 'axios'

const formData = ref({
    ImgFilePath: null,
    serviceName: '',
    Description: '',
    servicePrice: 0
})

const imgPath = (event) => {
    const file = event.target.files[0]

    if (!file) {
        console.error('No file selected')
        return
    }
    formData.value.ImgFilePath = file

    console.log('File:', file)
}

const submitForm = async () => {
    try {
        const response = await axios.post('http://127.0.0.1:5000/admin/service', formData.value, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
        console.log('Response:', response.data)
    } catch (error) {
        console.error('Error:', error.response ? error.response.data : error.message)
    }
}

const { showModal } = defineProps({
    showModal: Boolean
})

const emit = defineEmits(['closeModal'])

function closeModal() {
    emit('closeModal')
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
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.6);
    background-color: #000000;
    display: flex;
    justify-content: center;
    align-items: center;
}

.modal-background {
    position: absolute;
    /* width: 100%;
    height: 100%; */
    background-color: rgba(0, 0, 0, 0.6);
}

.serviceImg {
    position: relative;
    height: 80px;
    width: 80px;
    background-color: rgb(255, 255, 255);
    border-radius: 1rem;
    margin-bottom: 1rem;
    padding: 1rem;
}

.ImgFilePath {
    position: absolute;
    top: 0;
    left: 0;
    opacity: 0;
    width: 100%;
    height: 100%;
    cursor: pointer;
}

.serviceDescription,
.serviceName,
.servicePrice {
    color: white;
    font-size: 0.9rem;
    appearance: textfield;
}

.serviceDescription {
    height: 6rem;
}

form {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: auto;
    gap: 0.5rem;
    width: 100%;
}

form input,
form textarea {
    outline: none;
    width: 90%;
    height: 2.5rem;
    color: white;
    border-radius: 0.5rem;
    border: none;
    padding: 0.5rem;
    padding-left: 1rem;
    font-weight: bolder;
    background-color: rgba(255, 255, 255, 0.2);
    box-shadow: 6px 8px 25px rgba(0, 0, 0, 0.8);
}

form textarea {
    resize: none;
    scrollbar-width: none;
}

form input:focus,
form textarea:focus {
    border: 3px solid #ff5c01;
    transform: scale(1.05);
    transition: ease-in-out 0.5;
    background-color: rgba(255, 255, 255, 0.4);
}

form input:focus::placeholder,
form textarea:focus::placeholder {
    color: transparent;
}

.btn {
    margin-top: 0.5rem;
    width: 5rem;
    height: 1.7rem;
    border-radius: 0.3rem;
    border: none;
    background: #ff5a01d5;
    box-shadow: 2px 5px 20px rgba(0, 0, 0, 0.6);
    color: #fff;
    font-size: 1rem;
    font-weight: bolder;
    cursor: pointer;
}

.cross {
    position: absolute;
    top: 5px;
    right: 10px;
    width: 40px;
    height: 40px;
    cursor: pointer;
}
</style>
