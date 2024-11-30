<script setup>
import Img from '@/assets/svg/Img.svg?raw'
import Cross from '@/assets/svg/Cross.svg?raw'
import { ref, watch } from 'vue'
import axios from 'axios'

const { showEditModal, serviceToEdit } = defineProps({
    showEditModal: Boolean,
    serviceToEdit: Object 
})

const emit = defineEmits(['closeEditModal'])

const editFormData = ref({
    ImgFilePath: null,
    service_name: '',
    description: '',
    price: null,
    service_id: null,
    image_name: null
});

// Watch the passed data to pre-fill form fields
watch(() => serviceToEdit, (newVal) => {
    if (newVal) {
        editFormData.value = {
            image_name: newVal.image_name,
            service_name: newVal.service_name,
            description: newVal.description,
            price: newVal.price,
            service_id: newVal.service_id
        };
    }
}, { immediate: true });

const imageFile = ref(null)

const imgPath = (event) => {
    const file = event.target.files[0]

    if (!file) {
        return
    }

    imageFile.value = file 
    const reader = new FileReader()
    reader.readAsDataURL(file)

    reader.onload = () => {
        editFormData.value.ImgFilePath = reader.result
    }
}

const submitEditForm = async () => {
    const formData = new FormData()
    formData.append('service_name', editFormData.value.service_name)
    formData.append('description', editFormData.value.description)
    formData.append('price', editFormData.value.price)  

    if (imageFile.value) {
        formData.append('image', imageFile.value)
    }
    try {
        const response = await axios.put(`http://127.0.0.1:5000/admin/service/${editFormData.value.service_id}`, formData, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('adminToken')}`
            }
        })  
        console.log(response.data)
        closeEditModal()
    } catch (error) {
        console.error('Error occurred:', error.response ? error.response.data : error.message)
    }
}

function closeEditModal() {
    emit('closeEditModal')
}
</script>

<template>
    <div v-if="showEditModal" class="modal">
        <form @submit.prevent="submitEditForm">
            <div class="serviceImg">
                <input type="file" class="ImgFilePath" @change="imgPath" accept="image/*" />
                <img v-if="editFormData.ImgFilePath" 
                :src="editFormData.ImgFilePath" 
                alt="Image Preview" 
                class="ImagePreview"/>

                <img v-else-if="editFormData.image_name" 
                :src=" 'http://127.0.0.1:5000/static/services_imgs/' + editFormData.image_name" 
                alt="Image Preview" 
                class="ImagePreview"/>
                
                <p v-else v-html="Img"
                class="ImagePreview"></p>
            </div>
            <input type="text" class="serviceName" placeholder="SERVICE NAME" v-model="editFormData.service_name" />
            <textarea class="serviceDescription" placeholder="DESCRIPTION....."
                v-model="editFormData.description"></textarea>
            <input type="number" class="servicePrice" placeholder="PRICE" v-model="editFormData.price" />
            <button type="submit" class="btn">Edit</button>
        </form>
        <div v-html="Cross" class="cross" @click="closeEditModal"></div>
    </div>
</template>


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
    z-index: 10000;
}

.serviceImg {
    position: relative;
    height: 80px;
    width: 80px;
    background-color: rgb(255, 255, 255);
    border-radius: 1rem;
    margin-bottom: 1rem;
    padding: 0.7rem;
}

.ImagePreview {
    width: 100%;
    height: 100%;
    object-fit: contain;
    border-radius: 1rem;
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
    height: 2rem;
    border-radius: 0.3rem;
    border: none;
    background: #ff5a01d5;
    box-shadow: 2px 5px 20px rgba(0, 0, 0, 0.6);
    color: #fff;
    font-size: 1.25rem;
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
