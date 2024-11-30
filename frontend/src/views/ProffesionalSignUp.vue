<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios'
import ServiceChoiceModal from '@/components/Professional/ServiceChoiceModel.vue'
import NotificationModal from '@/components/NotificationModal.vue'

const formData = ref({
    email: '',
    username: '',
    password: '',
    serviceType: '',
    experience: null,
    contact: null,
    pincode: null,
})

const validationErrors = ref({
    email: '',
    username: '',
    password: '',
    serviceType: '',
    experience: '',
    contact: '',
    pincode: '',
})

const validateForm = () => {
    let isValid = true

    // Clear previous errors
    Object.keys(validationErrors.value).forEach((key) => {
        validationErrors.value[key] = ''
    })

    // Email validation
    if (!formData.value.email) {
        validationErrors.value.email = 'Email is required.'
        isValid = false
        formData.value.email=''
    } else if (!/\S+@\S+\.\S+/.test(formData.value.email)) {
        validationErrors.value.email = 'Enter a valid email address.'
        isValid = false
        formData.value.email=''
    }

    // Username validation
    if (!formData.value.username) {
        validationErrors.value.username = 'Username is required.'
        isValid = false
        formData.value.username=''
    }

    // Password validation
    if (!formData.value.password) {
        validationErrors.value.password = 'Password is required.'
        isValid = false
        formData.value.password=''
    } else if (formData.value.password.length < 3) {
        validationErrors.value.password = 'Password must be at least 4 characters.'
        isValid = false
        formData.value.password=''
    }

    // Service Type validation
    if (!formData.value.serviceType) {
        validationErrors.value.serviceType = 'Please select a service type.'
        isValid = false
        formData.value.serviceType=''
    }

    // Experience validation
    if (formData.value.experience === null || formData.value.experience === '') {
        validationErrors.value.experience = 'Experience is required.'
        isValid = false
        formData.value.experience=''
    } else if (isNaN(formData.value.experience) || formData.value.experience < 0) {
        validationErrors.value.experience = 'Experience must be a positive number.'
        isValid = false
        formData.value.experience=null
    } else if (formData.value.experience >45) {
        validationErrors.value.experience = 'Experience must be less than 45 years.'
        isValid = false
        formData.value.experience=null
    }

    // Contact validation
    if (formData.value.contact === null || formData.value.contact === '') {
        validationErrors.value.contact = 'Contact number is required.'
        isValid = false
        formData.value.contact=null
    } else if (!/^\d{10}$/.test(formData.value.contact)) {
        validationErrors.value.contact = 'Enter a valid 10-digit contact number.'
        isValid = false
        formData.value.contact=null
    }

    // Pincode validation
    if (formData.value.pincode === null || formData.value.pincode === '') {
        validationErrors.value.pincode = 'Pincode is required.'
        isValid = false
        formData.value.pincode=null
    } else if (!/^\d{6}$/.test(formData.value.pincode)) {
        validationErrors.value.pincode = 'Enter a valid 6-digit pincode.'
        isValid = false
        formData.value.pincode=null
    }

    return isValid
}

const submitForm = async () => {
    if (!validateForm()) return

    try {
        const response = await axios.post(
            'http://127.0.0.1:5000/professional/signup',
            formData.value,
            {
                headers: {
                    'Content-Type': 'application/json',
                },
            }
        )
        console.log(response.data)
        addNotification('Professional created successfully!', 3000)
        window.location.href = '/login'
    } catch (error) {
        addNotification('Error occurred. Please try again.', 5000)
    }
}

// Professional Service Choice
const showModal = ref(false)
const Services = ref([])
const modalRef = ref(null) // Reference to the modal element

const fetchServices = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5000/professional/services', {
            headers: {
                'Content-Type': 'application/json',
            },
        })
        Services.value = response.data
        console.log(Services.value)
    } catch (error) {
        console.error('Error occurred:', error.response ? error.response.data : error.message)
    }
}

const toggleModal = async () => {
    if (!Services.value.length) {
        await fetchServices()
    }
    showModal.value = !showModal.value
}

const handleClickOutside = (event) => {
    if (
        modalRef.value?.$refs?.modalContainer &&
        !modalRef.value.$refs.modalContainer.contains(event.target)
    ) {
        showModal.value = false
    }
}

onMounted(() => {
    document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
    document.removeEventListener('click', handleClickOutside)
})

const handleServiceSelect = (service) => {
    formData.value.serviceType = service.name
    showModal.value = false
}

//Notification
const notifications = ref([])

const addNotification = (message, duration) => {
    notifications.value.push({ message, duration })
}
</script>

<template>
    <div>
        <h1 class="heading">SERVICE PROFESSIONAL SIGNUP</h1>

        <form class="form" @submit.prevent="submitForm">
            <div>
                <input
                    type="email"
                    v-model="formData.email"
                    :class="{ 'error': validationErrors.email }"
                    :placeholder=" validationErrors.email || 'EMAIL ID'"
                />
            </div>
            <div>
                <input
                    type="text"
                    v-model="formData.username"
                    :class="{ 'error': validationErrors.username }"
                    :placeholder=" validationErrors.username || 'USERNAME'"
                />
            </div>
            <div>
                <input
                    type="password"
                    v-model="formData.password"
                    :class="{ 'error': validationErrors.password }"
                    :placeholder=" validationErrors.password || 'PASSWORD'"
                />
            </div>
            <div>
                <input
                    type="text"
                    v-model="formData.serviceType"
                    :class="{ 'error': validationErrors.serviceType }"
                    :placeholder=" validationErrors.serviceType || 'SERVICE TYPE'"
                    @click="toggleModal"
                />
            </div>
            <div>
                <input
                    type="text"
                    v-model="formData.experience"
                    :class="{ 'error': validationErrors.experience }"
                    :placeholder=" validationErrors.experience || 'EXPERIENCE'"
                />
            </div>
            <div>
                <input
                    type="number"
                    v-model="formData.contact"
                    :class="{ 'error': validationErrors.contact }"
                    :placeholder=" validationErrors.contact || 'CONTACT NUMBER'"
                />
            </div>
            <div>
                <input
                    type="number"
                    v-model="formData.pincode"
                    :class="{ 'error': validationErrors.pincode }"
                    :placeholder=" validationErrors.pincode || 'PINCODE'"
                />
            </div>

            <button class="btn" type="submit">Register</button>
        </form>

        <div class="signInLine">
            <p>Already have an account?</p>
            <RouterLink :to="{ name: 'login' }" class="signInLink">Login</RouterLink>
        </div>

        <!-- Service Choice Modal -->
        <ServiceChoiceModal
            ref="modalRef"
            class="Modal"
            :ServiceData="Services"
            :showModal="showModal"
            @CloseServiceChoiceModal="handleServiceSelect"
        />

        <!-- Notification Modal -->
        <NotificationModal
            v-for="(notification, index) in notifications"
            :key="index"
            :message="notification.message"
            :duration="notification.duration"
            @close="notifications.splice(index, 1)"
        />
    </div>
</template>


<style scoped>
.Modal {
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

.serviceType {
    position: relative;
}

.heading {
    text-align: center;
    font-weight: bolder;
    font-size: 3.5rem;
    margin-top: 1rem;
    margin-bottom: 2rem;
    font-weight: bolder;
    font-style: italic;
    color: #ff5c01;
}
.form {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: auto;
    margin-bottom: 1rem;
}

.form input{
    width: clamp(20rem, 25vw + 10rem, 50rem);
    height: 3rem;
    outline: none;
    color: white;
    border-radius: 1rem;
    border: none;
    padding: 1rem;
    padding-left: 2.25rem;
    font-size: 1.5rem;
    font-weight: bolder;
    font-style: italic;
    margin-bottom: 1rem;
    background-color: rgba(255, 255, 255, 0.2);
    box-shadow: 6px 8px 25px rgba(0, 0, 0, 0.8);
}

input[type='number'] {
    appearance: textfield;
}

.form input:focus {
    border: 3px solid #ff5c01;
    transform: scale(1.05);
    transition: ease-in-out 0.5;
    background-color: rgba(255, 255, 255, 0.4);
}

.form input:focus::placeholder {
    color: transparent;
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
    color: #ff6b6b;
}

.form input.error:focus::placeholder{
    color: transparent;
}

.btn {
    width: 10rem;
    height: 3rem;
    border-radius: 1rem;
    border: none;
    background: #ff5c01;
    color: #fff;
    font-size: 1.5rem;
    font-weight: bolder;
    cursor: pointer;
}

.signInLine {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: auto;
    margin-bottom: 1rem;
}
.signInLine p {
    color: #ff5c01;
    font-size: 1.5rem;
    font-weight: bolder;
    font-style: italic;
    text-align: center;
}
.signInLine a {
    color: #6a94ff;
    font-size: 1.5rem;
    font-weight: bolder;
    text-align: center;
    text-decoration: none;
    margin-left: 10px;
}

.signInLine a:hover {
    text-decoration: underline;
    transform: scale(1.1);
    transition: ease-in-out 0.2s;
}
</style>
