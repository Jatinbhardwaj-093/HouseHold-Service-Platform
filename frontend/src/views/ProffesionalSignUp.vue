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
    pincode: null
})

const validationErrors = ref({
    email: '',
    username: '',
    password: '',
    serviceType: '',
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
    if (!formData.value.email) {
        validationErrors.value.email = 'Email is required.'
        isValid = false
        formData.value.email = ''
    } else if (!/\S+@\S+\.\S+/.test(formData.value.email)) {
        validationErrors.value.email = 'Enter a valid email address.'
        isValid = false
        formData.value.email = ''
    }

    // Username validation
    if (!formData.value.username) {
        validationErrors.value.username = 'Username is required.'
        isValid = false
        formData.value.username = ''
    }

    // Password validation
    if (!formData.value.password) {
        validationErrors.value.password = 'Password is required.'
        isValid = false
        formData.value.password = ''
    } else if (formData.value.password.length < 3) {
        validationErrors.value.password = 'Password must be at least 4 characters.'
        isValid = false
        formData.value.password = ''
    }

    // Service Type validation
    if (!formData.value.serviceType) {
        validationErrors.value.serviceType = 'Please select a service type.'
        isValid = false
        formData.value.serviceType = ''
    }

    // Experience validation
    if (formData.value.experience === null || formData.value.experience === '') {
        validationErrors.value.experience = 'Experience is required.'
        isValid = false
        formData.value.experience = ''
    } else if (isNaN(formData.value.experience) || formData.value.experience < 0) {
        validationErrors.value.experience = 'Experience must be a positive number.'
        isValid = false
        formData.value.experience = null
    } else if (formData.value.experience > 45) {
        validationErrors.value.experience = 'Experience must be less than 45 years.'
        isValid = false
        formData.value.experience = null
    }

    // Contact validation
    if (formData.value.contact === null || formData.value.contact === '') {
        validationErrors.value.contact = 'Contact number is required.'
        isValid = false
        formData.value.contact = null
    } else if (!/^\d{10}$/.test(formData.value.contact)) {
        validationErrors.value.contact = 'Enter a valid 10-digit contact number.'
        isValid = false
        formData.value.contact = null
    }

    // Pincode validation
    if (formData.value.pincode === null || formData.value.pincode === '') {
        validationErrors.value.pincode = 'Pincode is required.'
        isValid = false
        formData.value.pincode = null
    } else if (!/^\d{6}$/.test(formData.value.pincode)) {
        validationErrors.value.pincode = 'Enter a valid 6-digit pincode.'
        isValid = false
        formData.value.pincode = null
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
                    'Content-Type': 'application/json'
                }
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
                'Content-Type': 'application/json'
            }
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
    <div class="professional-signup-container">
        <div class="signup-wrapper">
            <h1 class="heading">Join as a Professional</h1>

            <div class="form-container">
                <div class="form-description">
                    <h2>Offer Your Services</h2>
                    <p>
                        Join our network of skilled professionals and grow your business by
                        connecting with customers in need of your expertise.
                    </p>
                    <div class="benefits">
                        <div class="benefit-item">
                            <span class="benefit-icon">💼</span>
                            <span>Grow your business</span>
                        </div>
                        <div class="benefit-item">
                            <span class="benefit-icon">📅</span>
                            <span>Flexible scheduling</span>
                        </div>
                        <div class="benefit-item">
                            <span class="benefit-icon">💰</span>
                            <span>Competitive earnings</span>
                        </div>
                    </div>
                </div>

                <form class="form" @submit.prevent="submitForm">
                    <div class="form-fields">
                        <div class="input-group">
                            <label for="email">Email Address</label>
                            <input
                                id="email"
                                type="email"
                                v-model="formData.email"
                                :class="{ error: validationErrors.email }"
                                :placeholder="validationErrors.email || 'Enter your email'"
                            />
                            <span class="error-message" v-if="validationErrors.email">{{
                                validationErrors.email
                            }}</span>
                        </div>

                        <div class="input-group">
                            <label for="username">Username</label>
                            <input
                                id="username"
                                type="text"
                                v-model="formData.username"
                                :class="{ error: validationErrors.username }"
                                :placeholder="validationErrors.username || 'Choose a username'"
                            />
                            <span class="error-message" v-if="validationErrors.username">{{
                                validationErrors.username
                            }}</span>
                        </div>

                        <div class="input-group">
                            <label for="password">Password</label>
                            <input
                                id="password"
                                type="password"
                                v-model="formData.password"
                                :class="{ error: validationErrors.password }"
                                :placeholder="validationErrors.password || 'Create a password'"
                            />
                            <span class="error-message" v-if="validationErrors.password">{{
                                validationErrors.password
                            }}</span>
                        </div>

                        <div class="input-group">
                            <label for="serviceType">Service Type</label>
                            <div class="service-type-wrapper">
                                <input
                                    id="serviceType"
                                    type="text"
                                    v-model="formData.serviceType"
                                    :class="{ error: validationErrors.serviceType }"
                                    :placeholder="
                                        validationErrors.serviceType || 'Select your service type'
                                    "
                                    @click="toggleModal"
                                    readonly
                                />
                                <span class="select-icon">▼</span>
                            </div>
                            <span class="error-message" v-if="validationErrors.serviceType">{{
                                validationErrors.serviceType
                            }}</span>
                        </div>

                        <div class="input-group">
                            <label for="experience">Experience (years)</label>
                            <input
                                id="experience"
                                type="text"
                                v-model="formData.experience"
                                :class="{ error: validationErrors.experience }"
                                :placeholder="validationErrors.experience || 'Years of experience'"
                            />
                            <span class="error-message" v-if="validationErrors.experience">{{
                                validationErrors.experience
                            }}</span>
                        </div>

                        <div class="input-group">
                            <label for="contact">Contact Number</label>
                            <input
                                id="contact"
                                type="number"
                                v-model="formData.contact"
                                :class="{ error: validationErrors.contact }"
                                :placeholder="validationErrors.contact || 'Your phone number'"
                            />
                            <span class="error-message" v-if="validationErrors.contact">{{
                                validationErrors.contact
                            }}</span>
                        </div>

                        <div class="input-group">
                            <label for="pincode">Pincode</label>
                            <input
                                id="pincode"
                                type="number"
                                v-model="formData.pincode"
                                :class="{ error: validationErrors.pincode }"
                                :placeholder="validationErrors.pincode || 'Your area pincode'"
                            />
                            <span class="error-message" v-if="validationErrors.pincode">{{
                                validationErrors.pincode
                            }}</span>
                        </div>
                    </div>

                    <button class="btn" type="submit">
                        <span class="btn-text">Create Account</span>
                        <span class="btn-icon">→</span>
                    </button>
                </form>
            </div>

            <div class="signInLine">
                <p>Already have an account?</p>
                <RouterLink :to="{ name: 'login' }" class="signInLink">Login</RouterLink>
            </div>
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
.professional-signup-container {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #000;
    padding: 20px;
    background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.9)),
        url('@/components/assets/images/webHomePage.png');
    background-size: cover;
    background-position: center;
}

.signup-wrapper {
    width: 100%;
    max-width: 1000px;
    padding: 40px 20px;
    border-radius: 20px;
    background-color: rgba(10, 10, 10, 0.8);
    box-shadow: 0 20px 50px rgba(255, 92, 1, 0.25);
    border: 1px solid rgba(255, 92, 1, 0.2);
    backdrop-filter: blur(10px);
}

.heading {
    text-align: center;
    font-size: 3.2rem;
    margin-top: 0.5rem;
    margin-bottom: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ff5c01, #ff8f01);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 1px;
}

.form-container {
    display: flex;
    flex-direction: row;
    gap: 30px;
    margin: 0 auto 2rem;
}

@media (max-width: 900px) {
    .form-container {
        flex-direction: column;
    }
}

.form-description {
    flex: 1;
    padding: 2rem;
    background-color: rgba(30, 30, 30, 0.7);
    border-radius: 15px;
    border: 1px solid rgba(255, 92, 1, 0.2);
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.form-description h2 {
    font-size: 1.8rem;
    color: #ff5c01;
    margin-bottom: 1rem;
    font-weight: 600;
}

.form-description p {
    color: #ddd;
    font-size: 1.1rem;
    line-height: 1.6;
    margin-bottom: 2rem;
}

.benefits {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.benefit-item {
    display: flex;
    align-items: center;
    color: #e0e0e0;
    font-size: 1.1rem;
}

.benefit-icon {
    font-size: 1.5rem;
    margin-right: 15px;
    background: rgba(255, 92, 1, 0.2);
    padding: 8px;
    border-radius: 50%;
}

.form {
    flex: 1.5;
    display: flex;
    flex-direction: column;
    padding: 0;
}

.form-fields {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 25px;
}

.input-group {
    position: relative;
    margin-bottom: 5px;
}

.input-group label {
    display: block;
    font-size: 0.95rem;
    font-weight: 500;
    color: #e0e0e0;
    margin-bottom: 6px;
    margin-left: 5px;
}

.service-type-wrapper {
    position: relative;
}

.select-icon {
    position: absolute;
    right: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: #ff5c01;
    font-size: 0.8rem;
    pointer-events: none;
}

.form input {
    width: 100%;
    height: 3.2rem;
    outline: none;
    color: white;
    border-radius: 12px;
    border: 1px solid rgba(255, 92, 1, 0.3);
    padding: 0.8rem 1rem;
    font-size: 1rem;
    font-weight: 400;
    background-color: rgba(20, 20, 20, 0.6);
    box-shadow:
        inset 0 2px 8px rgba(0, 0, 0, 0.3),
        0 0 15px rgba(255, 92, 1, 0.1);
    transition: all 0.3s ease;
}

input[type='number'] {
    appearance: textfield;
    -moz-appearance: textfield;
}

input[readonly] {
    cursor: pointer;
    background-color: rgba(30, 30, 30, 0.7);
}

.form input:focus {
    border: 2px solid #ff5c01;
    background-color: rgba(30, 30, 30, 0.7);
    box-shadow: 0 0 20px rgba(255, 92, 1, 0.25);
}

.form input:focus::placeholder {
    color: rgba(255, 255, 255, 0.3);
}

.error-message {
    color: #ff6b6b;
    font-size: 0.85rem;
    margin-top: 4px;
    display: block;
}

.form input.error,
.form textarea.error {
    border: 2px solid #ff6b6b;
    background-color: rgba(255, 107, 107, 0.08);
}

.form input.error:focus {
    border: 2px solid #ff5c01;
    background-color: rgba(30, 30, 30, 0.7);
}

.form input.error::placeholder {
    color: rgba(255, 107, 107, 0.7);
}

.btn {
    width: 100%;
    height: 3.5rem;
    border-radius: 12px;
    border: none;
    background: linear-gradient(135deg, #ff5c01, #ff8f01);
    color: #fff;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    margin-top: 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 8px 20px rgba(255, 92, 1, 0.3);
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}

.btn-text {
    margin-right: 10px;
}

.btn-icon {
    opacity: 0;
    transform: translateX(-10px);
    transition: all 0.3s ease;
}

.btn:before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: 0.5s;
}

.btn:hover:before {
    left: 100%;
}

.btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(255, 92, 1, 0.5);
}

.btn:hover .btn-icon {
    opacity: 1;
    transform: translateX(0);
}

.signInLine {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 2rem auto 1rem;
    padding: 15px;
    background-color: rgba(30, 30, 30, 0.7);
    border-radius: 10px;
    max-width: 400px;
    border: 1px solid rgba(255, 92, 1, 0.1);
}

.signInLine p {
    color: #ddd;
    font-size: 1rem;
    font-weight: 500;
}

.signInLine a {
    color: #ff5c01;
    font-size: 1rem;
    font-weight: 600;
    text-decoration: none;
    margin-left: 10px;
    position: relative;
    padding-bottom: 2px;
}

.signInLine a::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 2px;
    background-color: #ff5c01;
    transition: width 0.3s ease;
}

.signInLine a:hover::after {
    width: 100%;
}

.signInLine a:hover {
    text-shadow: 0 0 8px rgba(255, 92, 1, 0.5);
}

.Modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}
</style>
