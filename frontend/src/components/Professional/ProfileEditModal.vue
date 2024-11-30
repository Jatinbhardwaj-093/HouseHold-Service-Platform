<script setup>
import Cross from '@/assets/svg/Cross.svg?raw'
import Img from '@/assets/svg/Img.svg?raw'

import { ref, watch } from 'vue'
import axios from 'axios'
const token = localStorage.getItem('professionalToken')

const emit = defineEmits(['closeProfileEditModal', 'Notification', 'error'])

const closeProfileEditModal = () => {
    emit('closeProfileEditModal')
}

const { profileData } = defineProps({
    profileData: Object
})

const professional = ref({
    email: '',
    username: '',
    password: '',
    contact: null,
    experience: null,
    pincode: null,
    image_name: '',
    ImgFilePath: null
})

const imageFile = ref(null)

watch(
    () => profileData,
    (newVal) => {
        if (newVal) {
            professional.value = {
                email: newVal.email,
                username: newVal.username,
                password: newVal.password,
                contact: newVal.contact,
                experience: newVal.experience,
                pincode: newVal.pincode,
                image_name: newVal.image_name
            }
        }
    },
    { immediate: true }
)

const imgPath = (event) => {
    const file = event.target.files[0]

    if (!file) {
        return
    }

    imageFile.value = file // Store the file for FormData

    const reader = new FileReader()
    reader.readAsDataURL(file)

    reader.onload = () => {
        professional.value.ImgFilePath = reader.result // For preview
    }
}

const validationErrors = ref({
    email: '',
    username: '',
    password: '',
    experience: '',
    contact: '',
    pincode: ''
})

const validateForm = () => {
    let isValid = true

    // Clear previous errors
    Object.keys(validationErrors.value).forEach((key) => {
        validationErrors.value[key] = ''
    })

    // Email validation
    if (!professional.value.email) {
        validationErrors.value.email = 'Email is required.'
        isValid = false
        professional.value.email = ''
    } else if (!/\S+@\S+\.\S+/.test(professional.value.email)) {
        validationErrors.value.email = 'Enter a valid email address.'
        isValid = false
        professional.value.email = ''
    }

    // Username validation
    if (!professional.value.username) {
        validationErrors.value.username = 'Username is required.'
        isValid = false
        professional.value.username = ''
    }

    // Password validation
    if (professional.value.password && professional.value.password.length < 3) {
        validationErrors.value.password = 'Password must be at least 6 characters.'
        isValid = false
        professional.value.password = ''
    }

    // Experience validation
    if (professional.value.experience === null || professional.value.experience === '') {
        validationErrors.value.experience = 'Experience is required.'
        isValid = false
        professional.value.experience = ''
    } else if (isNaN(professional.value.experience) || professional.value.experience < 0) {
        validationErrors.value.experience = 'Experience must be a positive number.'
        isValid = false
        professional.value.experience = null
    } else if (professional.value.experience > 45) {
        validationErrors.value.experience = 'Experience must be less than 45 years.'
        isValid = false
        professional.value.experience = null
    }

    // Contact validation
    if (professional.value.contact === null || professional.value.contact === '') {
        validationErrors.value.contact = 'Contact number is required.'
        isValid = false
        professional.value.contact = null
    } else if (!/^\d{10}$/.test(professional.value.contact)) {
        validationErrors.value.contact = 'Enter a valid 10-digit contact number.'
        isValid = false
        professional.value.contact = null
    }

    // Pincode validation
    if (professional.value.pincode === null || professional.value.pincode === '') {
        validationErrors.value.pincode = 'Pincode is required.'
        isValid = false
        professional.value.pincode = null
    } else if (!/^\d{6}$/.test(professional.value.pincode)) {
        validationErrors.value.pincode = 'Enter a valid 6-digit pincode.'
        isValid = false
        professional.value.pincode = null
    }

    return isValid
}

const submitForm = async () => {
    if (!validateForm()) {
        return
    }

    const formData = new FormData()

    formData.append('email', professional.value.email)
    formData.append('username', professional.value.username)
    formData.append('password', professional.value.password)
    formData.append('contact', professional.value.contact)
    formData.append('experience', professional.value.experience)
    formData.append('pincode', professional.value.pincode)

    if (imageFile.value) {
        formData.append('image', imageFile.value)
    }
    try {
        await axios.put('http://127.0.0.1:5000/professional/profile', formData, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        closeProfileEditModal()
        emit('Notification')
    } catch (error) {
        emit('error')
    }
}
</script>

<template>
    <div class="editModal-content">
        <form class="form" @submit.prevent="submitForm">
            <div class="profilePic">
                <input type="file" class="ImgFilePath" @change="imgPath" accept="image/*" />
                <div v-if="professional.ImgFilePath" class="image-preview">
                    <img :src="professional.ImgFilePath" alt="Image Preview" />
                </div>
                <div class="image-preview" v-else-if="professional.image_name">
                    <img
                        :src="
                            'http://127.0.0.1:5000/static/professionals_imgs/' +
                            professional.image_name
                        "
                        alt="Image Preview"
                    />
                </div>
                <p v-else v-html="Img"></p>
            </div>
            <label for="email" class="label">Email Id</label>
            <input
                type="email"
                class="email"
                v-model="professional.email"
                id="email"
                :class="{ error: validationErrors.email }"
                :placeholder="validationErrors.email"
            />

            <label for="username" class="label">Username</label>
            <input
                type="text"
                class="username"
                v-model="professional.username"
                id="username"
                :placeholder="validationErrors.username"
                :class="{ error: validationErrors.username }"
            />

            <label for="password" class="label">Password</label>
            <input
                type="password"
                class="password"
                v-model="professional.password"
                id="password"
                :placeholder="validationErrors.password"
                :class="{ error: validationErrors.password }"
            />

            <label for="experience" class="label">Experience</label>
            <input
                type="text"
                class="experience"
                v-model="professional.experience"
                id="experience"
                :placeholder="validationErrors.experience"
                :class="{ error: validationErrors.experience }"
            />

            <label for="contact" class="label">Contact</label>
            <input
                type="number"
                class="contact"
                v-model="professional.contact"
                id="contact"
                :placeholder="validationErrors.contact"
                :class="{ error: validationErrors.contact }"
            />

            <label for="pincode" class="label">Pincode</label>
            <input
                type="number"
                class="pincode"
                v-model="professional.pincode"
                id="pincode"
                :placeholder="validationErrors.pincode"
                :class="{ error: validationErrors.pincode }"
            />

            <button type="submit" class="btn">Edit</button>
        </form>
        <div v-html="Cross" class="cross" @click="closeProfileEditModal"></div>
    </div>
</template>

<style scoped>
.editModal-content {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 30rem;
    padding: 1.5rem;
    background-color: #161414;
    border-radius: 1rem;
    box-shadow: 2px 5px 20px rgba(151, 150, 149, 0.6);
    z-index: 10000;
}

.form {
    display: grid;
    grid-template-columns: 1fr 5fr;
    grid-template-areas:
        'profilePic profilePic'
        'label1 input1'
        'label2 input2'
        'label3 input3'
        'label4 input4'
        'label5 input5'
        'label6 input6'
        'btn btn';
    gap: 0.5rem;
}

.profilePic {
    position: relative;
    grid-area: profilePic;
    justify-self: center;
    align-self: center;
    width: 6.5rem;
    height: 6.5rem;
    border-radius: 1rem;
    padding: 0.5rem;
    margin-bottom: 1.5rem;
    background-color: #423d3d;
    box-shadow: 0px 3px 15px rgba(236, 103, 14, 0.6);
}

.profilePic .ImgFilePath {
    position: absolute;
    top: 0;
    left: 0;
    opacity: 0;
    width: 100%;
    height: 100%;
    cursor: pointer;
}

.profilePic .image-preview img {
    height: 100%;
    width: 100%;
    object-fit: contain;
    overflow: hidden;
}

.label:nth-child(2) {
    grid-area: label1;
}
.email {
    grid-area: input1;
}
.label:nth-child(4) {
    grid-area: label2;
}
.username {
    grid-area: input2;
}
.label:nth-child(6) {
    grid-area: label3;
}
.password {
    grid-area: input3;
}
.label:nth-child(8) {
    grid-area: label4;
}
.experience {
    grid-area: input4;
}
.label:nth-child(10) {
    grid-area: label5;
}
.contact {
    grid-area: input5;
}
.label:nth-child(12) {
    grid-area: label6;
}
.pincode {
    grid-area: input6;
}

.cross {
    position: absolute;
    top: 10px;
    right: 10px;
    height: 55px;
    width: 55px;
    cursor: pointer;
}

.form label {
    color: bisque;
    font-size: 1.2rem;
    font-weight: bolder;
    font-style: italic;
    margin-right: 0.5rem;
}

.form input {
    width: 80%;
    margin: auto;
    height: 2rem;
    outline: none;
    color: white;
    border-radius: 0.5rem;
    border: none;
    padding: 0.5rem;
    padding-left: 1.2rem;
    font-size: 1rem;
    font-weight: bolder;
    font-style: italic;
    background-color: rgba(255, 255, 255, 0.2);
    box-shadow: 6px 8px 25px rgba(0, 0, 0, 0.8);
}

.form input[type='number'] {
    appearance: textfield;
}

.form input.error,
.form textarea.error {
    border: 3px solid #ff6b6b;
    background-color: rgba(255, 107, 107, 0.1); 
}

.form input.error:focus {
    border: 3px solid #ff5c01;
    transform: scale(1.05);
    transition: ease-in-out 0.3s;
    background-color: rgba(255, 255, 255, 0.4);
}

.form input.error::placeholder {
    font-size: 0.75rem;
    color: #ff6b6b;
}

.form input.error:focus::placeholder{
    color: transparent;
}

.btn {
    grid-area: btn;
    justify-self: center;
    margin-top: 1rem;
    width: 6rem;
    height: 2rem;
    border-radius: 0.3rem;
    border: none;
    background: #ff5c01;
    box-shadow: 2px 5px 20px rgba(0, 0, 0, 0.6);
    color: #fff;
    font-size: 1.25rem;
    font-weight: bolder;
    cursor: pointer;
}
</style>
