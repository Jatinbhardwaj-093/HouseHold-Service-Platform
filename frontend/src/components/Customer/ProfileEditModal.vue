<script setup>
import Cross from '@/assets/svg/Cross.svg?raw'
import Img from '@/assets/svg/Img.svg?raw'

import { ref, watch } from 'vue'
import axios from 'axios'

const token = localStorage.getItem('customerToken')

const emit = defineEmits(['closeProfileEditModal', 'Notification', 'error'])

const closeProfileEditModal = () => {
    emit('closeProfileEditModal')
}

const { profileData } = defineProps({
    profileData: Object
})

const customer = ref({
    email: '',
    username: '',
    password: '',
    contact: null,
    pincode: null,
    address: '',
    ImgFilePath: null,
    image_name: ''
})

const imageFile = ref(null)

watch(
    () => profileData,
    (newVal) => {
        if (newVal) {
            customer.value = {
                email: newVal.email,
                username: newVal.username,
                password: newVal.password,
                contact: newVal.contact,
                pincode: newVal.pincode,
                address: newVal.address,
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
        customer.value.ImgFilePath = reader.result // For preview
    }
}

// Validation state
const errors = ref({
    email: '',
    username: '',
    password: '',
    contact: '',
    pincode: '',
    address: ''
})

// Validate the form
const validateForm = () => {
    let isValid = true

    // Clear previous errors
    Object.keys(errors.value).forEach((key) => {
        errors.value[key] = ''
    })

    // Email validation
    if (!customer.value.email) {
        errors.value.email = 'Email is required'
        isValid = false
        customer.value.email = ''
    } else if (!/\S+@\S+\.\S+/.test(customer.value.email)) {
        errors.value.email = 'Invalid email format'
        isValid = false
        customer.value.email = ''
    }

    // Username validation
    if (!customer.value.username) {
        errors.value.username = 'Username is required'
        isValid = false
        customer.value.username = ''
    }

    // Password validation
    if (customer.value.password && customer.value.password.length < 3) {
        errors.value.password = 'Password must be at least 4 characters'
        isValid = false
        customer.value.password = ''
    }

    // Contact number validation
    if (!customer.value.contact) {
        errors.value.contact = 'Contact number is required'
        isValid = false
        customer.value.contact = ''
    } else if (!/^\d{10}$/.test(customer.value.contact)) {
        errors.value.contact = 'Contact must be a 10-digit number'
        isValid = false
        customer.value.contact = ''
    }

    // Pincode validation
    if (!customer.value.pincode) {
        errors.value.pincode = 'Pincode is required'
        isValid = false
        customer.value.pincode = ''
    } else if (!/^\d{6}$/.test(customer.value.pincode)) {
        errors.value.pincode = 'Pincode must be a 6-digit number'
        isValid = false
        customer.value.pincode = ''
    }

    // Address validation
    if (!customer.value.address) {
        errors.value.address = 'Address is required'
        isValid = false
        customer.value.address = ''
    }

    return isValid
}

const submitForm = async () => {
    if (!validateForm()) {
        return
    }
    const formData = new FormData()
    formData.append('email', customer.value.email)
    formData.append('username', customer.value.username)
    formData.append('password', customer.value.password)
    formData.append('contact', customer.value.contact)
    formData.append('pincode', customer.value.pincode)
    formData.append('address', customer.value.address)

    if (imageFile.value) {
        formData.append('image', imageFile.value)
    }

    try {
        await axios.put('http://127.0.0.1:5000/customer/profile', formData, {
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
                <div v-if="customer.ImgFilePath" class="image-preview">
                    <img :src="customer.ImgFilePath" alt="Image Preview" />
                </div>
                <div class="image-preview" v-else-if="customer.image_name">
                    <img
                        :src="'http://127.0.0.1:5000/static/customers_imgs/' + customer.image_name"
                        alt="Image Preview"
                    />
                </div>
                <p v-else v-html="Img"></p>
            </div>
            <label for="email" class="label">Email Id</label>
            <input
                type="email"
                class="email"
                v-model="customer.email"
                id="email"
                :placeholder="errors.email"
                :class="{ error: errors.email }"
            />
            <label for="username" class="label">Username</label>
            <input
                type="text"
                class="username"
                v-model="customer.username"
                id="username"
                :placeholder="errors.username"
                :class="{ error: errors.username }"
            />
            <label for="password" class="label">Password</label>
            <input
                type="password"
                class="password"
                v-model="customer.password"
                id="password"
                :placeholder="errors.password"
                :class="{ error: errors.password }"
            />
            <label for="contact" class="label">Contact</label>
            <input
                type="number"
                class="contact"
                v-model="customer.contact"
                id="contact"
                :placeholder="errors.contact"
                :class="{ error: errors.contact }"
            />
            <label for="pincode" class="label">Pincode</label>
            <input
                type="number"
                class="pincode"
                v-model="customer.pincode"
                id="pincode"
                :placeholder="errors.pincode"
                :class="{ error: errors.pincode }"
            />
            <label for="address" class="label">Address</label>
            <textarea
                v-model="customer.address"
                class="address"
                id="address"
                :placeholder="errors.address"
                :class="{ error: errors.address }"
            ></textarea>
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
.contact {
    grid-area: input4;
}
.label:nth-child(10) {
    grid-area: label5;
}
.pincode {
    grid-area: input5;
}
.label:nth-child(12) {
    grid-area: label6;
}
.address {
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

.form input,
.form textarea {
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

.form textarea {
    height: 4rem;
    resize: none;
}

.form input::placeholder,
textarea::placeholder {
    font-size: .75rem;
}

.form input:focus::placeholder,
textarea:focus::placeholder {
    color: transparent;
}

.form input.error,
.form textarea.error {
    border: 3px solid #ff6b6b;
    background-color: rgba(255, 107, 107, 0.1);
}

.form input.error:focus,
.form textarea.error:focus {
    border: 3px solid #ff5c01;
    transform: scale(1.05);
    transition: ease-in-out 0.3s;
    background-color: rgba(255, 255, 255, 0.4);
}

.form input.error::placeholder,
.form textarea.error::placeholder {
    color: #ff6b6b;
}

.form input.error:focus::placeholder,
textarea.error:focus::placeholder {
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
