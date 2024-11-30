<script setup>
import axios from 'axios';
import { ref} from 'vue';

// Form data
const formData = ref({
    email: '',
    username: '',
    password: '',
    contact: '',
    pincode: '',
    address: '',
});

// Validation state
const errors = ref({
    email: '',
    username: '',
    password: '',
    contact: '',
    pincode: '',
    address: '',
});

// Validate the form
const validateForm = () => {
    let isValid = true;

    // Clear previous errors
    Object.keys(errors.value).forEach((key) => {
        errors.value[key] = ''
    })

    // Email validation
    if (!formData.value.email) {
        errors.value.email = 'Email is required';
        isValid = false;
        formData.value.email = '';
    } else if (!/\S+@\S+\.\S+/.test(formData.value.email)) {
        errors.value.email = 'Invalid email format';
        isValid = false;
        formData.value.email = '';
    }

    // Username validation
    if (!formData.value.username) {
        errors.value.username = 'Username is required';
        isValid = false;
        formData.value.username = '';
    }

    // Password validation
    if (!formData.value.password){
        errors.value.password = 'Password is required';
        isValid = false;
        formData.value.password = '';
    }
    else if( formData.value.password.length < 3) {
        errors.value.password = 'Password must be at least 4 characters';
        isValid = false;
        formData.value.password = '';
    }

    // Contact number validation
    if (!formData.value.contact) {
        errors.value.contact = 'Contact number is required';
        isValid = false;
        formData.value.contact = '';
    } else if (!/^\d{10}$/.test(formData.value.contact)) {
        errors.value.contact = 'Contact must be a 10-digit number';
        isValid = false;
        formData.value.contact = '';
    }

    // Pincode validation
    if (!formData.value.pincode) {
        errors.value.pincode = 'Pincode is required';
        isValid = false;
        formData.value.pincode = '';
    } else if (!/^\d{6}$/.test(formData.value.pincode)) {
        errors.value.pincode = 'Pincode must be a 6-digit number';
        isValid = false;
        formData.value.pincode = '';
    } 

    // Address validation
    if (!formData.value.address) {
        errors.value.address = 'Address is required';
        isValid = false;
        formData.value.address = '';
    }

    return isValid;
};

// Submit form
const submitForm = async () => {
    if (!validateForm()) {
        addNotification('Please fix the validation errors', 5000);
        return;
    }

    try {
        const response = await axios.post('http://127.0.0.1:5000/customer/signup', formData.value, {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        console.log(response.data);
        addNotification('Customer created successfully!', 3000);
        window.location.href = '/login';
    } catch (error) {
        addNotification('Error occurred. Please try again.', 5000);
    }
};

// Notifications
import NotificationModal from '@/components/NotificationModal.vue';

const notifications = ref([]);

const addNotification = (message, duration) => {
    notifications.value.push({ message, duration });
};
</script>

<template>
    <div>
        <h1 class="heading">CUSTOMER SIGNUP</h1>

        <form @submit.prevent="submitForm" class="form">
            <div>
                <input
                    type="email"
                    v-model="formData.email"
                    :class="{ 'error': errors.email }"
                    :placeholder="errors.email || 'EMAIL ID'"
                />
            </div>
            <div>
                <input
                    type="text"
                    v-model="formData.username"
                    :class="{ 'error': errors.username }"
                    :placeholder="errors.username || 'USERNAME'"
                />
            </div>
            <div>
                <input
                    type="password"
                    v-model="formData.password"
                    :class="{ 'error': errors.password }"
                    :placeholder="errors.password || 'PASSWORD'"
                />
            </div>
            <div>
                <input
                    type="number"
                    v-model="formData.contact"
                    :class="{ 'error': errors.contact }"
                    :placeholder="errors.contact || 'CONTACT'"
                />
            </div>
            <div>
                <input
                    type="number"
                    v-model="formData.pincode"
                    :class="{ 'error': errors.pincode }"
                    :placeholder="errors.pincode || 'PINCODE'"
                />
            </div>
            <div>
                <textarea
                    v-model="formData.address"
                    :class="{ 'error': errors.address }"
                    :placeholder="errors.address || 'ADDRESS.....'"
                    cols="10"
                    rows="3"
                ></textarea>
            </div>
            <button type="submit" class="btn">Create</button>
        </form>

        <div class="signInLine">
            <p>Already have an account?</p>
            <RouterLink :to="{ name: 'login' }" class="signInLink">Sign In</RouterLink>
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
.heading {
    text-align: center;
    font-weight: bolder;
    font-size: 3.5rem;
    margin-top: 1rem;
    margin-bottom: 2rem;
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

.form input,
.form textarea {
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

.form textarea {
    height: 4.5rem;
    padding-top: 0.5rem;
    font-size: 1rem;
    resize: none;
}

input[type="number"] {
    appearance: textfield;   
}

.form input:focus,
textarea:focus {
    border: 3px solid #ff5c01;
    transform: scale(1.05);
    transition: ease-in-out 0.3s;
    background-color: rgba(255, 255, 255, 0.4);
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
    width: 10rem;
    height: 3rem;
    border-radius: 1rem;
    border: none;
    background: #ff5c01;
    color: #fff;
    font-size: 1.5rem;
    font-weight: bolder;
    cursor: pointer;
    transition: ease-in-out 0.3s;
}

.btn:hover {
    background: #ff4500;
    transform: scale(1.1);
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

.signInLink {
    color: #6a94ff;
    font-size: 1.5rem;
    font-weight: bolder;
    text-align: center;
    text-decoration: none;
    margin-left: 10px;
    transition: ease-in-out 0.2s;
}

.signInLink:hover {
    text-decoration: underline;
    transform: scale(1.1);
}
</style>

