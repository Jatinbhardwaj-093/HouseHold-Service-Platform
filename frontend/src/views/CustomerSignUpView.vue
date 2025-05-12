<script setup>
import axios from 'axios'
import { ref } from 'vue'

// Form data
const formData = ref({
    email: '',
    username: '',
    password: '',
    contact: '',
    pincode: '',
    address: ''
})

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
    if (!formData.value.email) {
        errors.value.email = 'Email is required'
        isValid = false
        formData.value.email = ''
    } else if (!/\S+@\S+\.\S+/.test(formData.value.email)) {
        errors.value.email = 'Invalid email format'
        isValid = false
        formData.value.email = ''
    }

    // Username validation
    if (!formData.value.username) {
        errors.value.username = 'Username is required'
        isValid = false
        formData.value.username = ''
    }

    // Password validation
    if (!formData.value.password) {
        errors.value.password = 'Password is required'
        isValid = false
        formData.value.password = ''
    } else if (formData.value.password.length < 3) {
        errors.value.password = 'Password must be at least 4 characters'
        isValid = false
        formData.value.password = ''
    }

    // Contact number validation
    if (!formData.value.contact) {
        errors.value.contact = 'Contact number is required'
        isValid = false
        formData.value.contact = ''
    } else if (!/^\d{10}$/.test(formData.value.contact)) {
        errors.value.contact = 'Contact must be a 10-digit number'
        isValid = false
        formData.value.contact = ''
    }

    // Pincode validation
    if (!formData.value.pincode) {
        errors.value.pincode = 'Pincode is required'
        isValid = false
        formData.value.pincode = ''
    } else if (!/^\d{6}$/.test(formData.value.pincode)) {
        errors.value.pincode = 'Pincode must be a 6-digit number'
        isValid = false
        formData.value.pincode = ''
    }

    // Address validation
    if (!formData.value.address) {
        errors.value.address = 'Address is required'
        isValid = false
        formData.value.address = ''
    }

    return isValid
}

// Submit form
const submitForm = async () => {
    if (!validateForm()) {
        addNotification('Please fix the validation errors', 5000)
        return
    }

    try {
        const response = await axios.post('http://127.0.0.1:5000/customer/signup', formData.value, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
        console.log(response.data)
        addNotification('Customer created successfully!', 3000)
        window.location.href = '/login'
    } catch (error) {
        addNotification('Error occurred. Please try again.', 5000)
    }
}

// Notifications
import NotificationModal from '@/components/NotificationModal.vue'

const notifications = ref([])

const addNotification = (message, duration) => {
    notifications.value.push({ message, duration })
}
</script>

<template>
    <div class="customer-signup-container">
        <div class="signup-wrapper">
            <h1 class="heading">Create Customer Account</h1>

            <div class="form-container">
                <div class="form-description">
                    <h2>Join Our Community</h2>
                    <p>
                        Sign up to discover reliable home services from verified professionals in
                        your area.
                    </p>
                    <div class="benefits">
                        <div class="benefit-item">
                            <span class="benefit-icon">✓</span>
                            <span>Verified professionals</span>
                        </div>
                        <div class="benefit-item">
                            <span class="benefit-icon">✓</span>
                            <span>Quick service booking</span>
                        </div>
                        <div class="benefit-item">
                            <span class="benefit-icon">✓</span>
                            <span>Secure payments</span>
                        </div>
                    </div>
                </div>

                <form @submit.prevent="submitForm" class="form">
                    <div class="form-fields">
                        <div class="input-group">
                            <label for="email">Email Address</label>
                            <input
                                id="email"
                                type="email"
                                v-model="formData.email"
                                :class="{ error: errors.email }"
                                placeholder="Enter your email"
                            />
                            <span class="error-message" v-if="errors.email">{{
                                errors.email
                            }}</span>
                        </div>

                        <div class="input-group">
                            <label for="username">Username</label>
                            <input
                                id="username"
                                type="text"
                                v-model="formData.username"
                                :class="{ error: errors.username }"
                                placeholder="Choose a username"
                            />
                            <span class="error-message" v-if="errors.username">{{
                                errors.username
                            }}</span>
                        </div>

                        <div class="input-group">
                            <label for="password">Password</label>
                            <input
                                id="password"
                                type="password"
                                v-model="formData.password"
                                :class="{ error: errors.password }"
                                placeholder="Create a password"
                            />
                            <span class="error-message" v-if="errors.password">{{
                                errors.password
                            }}</span>
                        </div>

                        <div class="input-group">
                            <label for="contact">Contact Number</label>
                            <input
                                id="contact"
                                type="number"
                                v-model="formData.contact"
                                :class="{ error: errors.contact }"
                                placeholder="Your phone number"
                            />
                            <span class="error-message" v-if="errors.contact">{{
                                errors.contact
                            }}</span>
                        </div>

                        <div class="input-group">
                            <label for="pincode">Pincode</label>
                            <input
                                id="pincode"
                                type="number"
                                v-model="formData.pincode"
                                :class="{ error: errors.pincode }"
                                placeholder="Your area pincode"
                            />
                            <span class="error-message" v-if="errors.pincode">{{
                                errors.pincode
                            }}</span>
                        </div>

                        <div class="input-group address-group">
                            <label for="address">Address</label>
                            <textarea
                                id="address"
                                v-model="formData.address"
                                :class="{ error: errors.address }"
                                placeholder="Enter your full address"
                                rows="3"
                            ></textarea>
                            <span class="error-message" v-if="errors.address">{{
                                errors.address
                            }}</span>
                        </div>
                    </div>

                    <button type="submit" class="btn">
                        <span class="btn-text">Create Account</span>
                        <span class="btn-icon">→</span>
                    </button>
                </form>
            </div>

            <div class="signInLine">
                <p>Already have an account?</p>
                <RouterLink :to="{ name: 'login' }" class="signInLink">Sign In</RouterLink>
            </div>
        </div>

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
.customer-signup-container {
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
    font-size: 1.2rem;
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

.form textarea {
    height: 4.5rem;
    padding-top: 0.5rem;
    font-size: 1rem;
    resize: none;
}

input[type='number'] {
    appearance: textfield;
}

.form-fields {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 25px;
    width: 100%;
}

.input-group {
    position: relative;
    margin-bottom: 10px;
}

.input-group label {
    display: block;
    font-size: 0.95rem;
    font-weight: 500;
    color: #e0e0e0;
    margin-bottom: 6px;
    margin-left: 5px;
}

.address-group {
    grid-column: 1 / -1; /* Make address field span full width */
}

.form input,
.form textarea {
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

.form input:focus,
textarea:focus {
    border: 2px solid #ff5c01;
    background-color: rgba(30, 30, 30, 0.7);
    box-shadow: 0 0 20px rgba(255, 92, 1, 0.25);
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

.form textarea {
    height: 100px;
    padding-top: 0.8rem;
    resize: none;
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

.error-message {
    color: #ff6b6b;
    font-size: 0.85rem;
    margin-top: 4px;
    display: block;
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

.signInLink {
    color: #ff5c01;
    font-size: 1rem;
    font-weight: 600;
    text-decoration: none;
    margin-left: 10px;
    position: relative;
    padding-bottom: 2px;
}

.signInLink::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 2px;
    background-color: #ff5c01;
    transition: width 0.3s ease;
}

.signInLink:hover::after {
    width: 100%;
}

.signInLink:hover {
    text-shadow: 0 0 8px rgba(255, 92, 1, 0.5);
}
</style>
