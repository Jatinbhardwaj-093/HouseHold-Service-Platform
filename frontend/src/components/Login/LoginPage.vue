<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import RoleLogin from './RoleLogin.vue'
import axios from 'axios'

const formData = ref({
    role: '',
    username: '',
    password: ''
})

const router = useRouter() // Create a router instance

const submitForm = async () => {
    const { role, username } = formData.value;

    if (!role || !username) {
        addNotification('Please provide valid role and username.', 5000);
        return;
    }

    try {
        // Fetch condition only if the role is not admin
        let condition = {};
        if (role !== 'admin') {
            const conditionResponse = await axios.get(
                `http://127.0.0.1:5000/condition/${role}/${username}`
            );
            condition = conditionResponse.data;

            // Check conditions for roles other than admin
            if (condition.flag === 'yes') {
                addNotification('Currently you are not allowed to login', 5000);
                return;
            }

            if (role === 'professional' && condition.verify === 'no') {
                addNotification('Currently your file is under verification! Please wait.', 5000);
                return;
            }
        }

        // Proceed to login
        const loginResponse = await axios.post(
            'http://127.0.0.1:5000/login',
            formData.value,
            { headers: { 'Content-Type': 'application/json' } }
        );

        // Store the token based on user role in local storage
        const token = loginResponse.data.token;
        if (role === 'admin') {
            localStorage.setItem('adminToken', token);
        } else if (role === 'professional') {
            localStorage.setItem('professionalToken', token);
        } else if (role === 'customer') {
            localStorage.setItem('customerToken', token);
        }

        // Redirect based on user role
        if (role === 'admin') {
            router.push({ name: 'admin' });
        } else if (role === 'professional') {
            router.push({ name: 'professional' });
        } else if (role === 'customer') {
            router.push({ name: 'customer' });
        }
    } catch (error) {
        console.error(error);
        if (error.response?.data?.message) {
            addNotification(error.response.data.message, 5000);
        } else {
            addNotification('Login failed. Please check your credentials.', 5000);
        }
    }
};


//Notification
import NotificationModal from '../NotificationModal.vue'

const notifications = ref([])

const addNotification = (message, duration) => {
    notifications.value.push({ message, duration })
}
</script>

<template>
    <div>
        <h1 class="heading">LOGIN</h1>

        <form class="form" @submit.prevent="submitForm">
            <RoleLogin v-model="formData.role" />
            <div>
                <input
                    type="text"
                    class="username"
                    placeholder="USERNAME"
                    v-model="formData.username"
                />
            </div>
            <div>
                <input
                    type="password"
                    class="password"
                    placeholder="PASSWORD"
                    v-model="formData.password"
                />
            </div>
            <button type="submit" class="btn">Login</button>
        </form>

        <div class="signUpLine">
            <p>Don't have an account?</p>
            <RouterLink :to="{ name: 'signup' }">Sign Up</RouterLink>
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
    font-size: 3.5rem;
    margin-top: 1.5rem;
    margin-bottom: 3rem;
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

.form input {
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

.form input:focus {
    border: 3px solid #ff5c01;
    transform: scale(1.05);
    transition: ease-in-out 0.5;
    background-color: rgba(255, 255, 255, 0.4);
}

.form input:focus::placeholder {
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

.signUpLine {
    display: flex;
    align-items: center;
    justify-content: center;

    margin: auto;
    margin-bottom: 1rem;
}

.signUpLine p {
    color: #ff5c01;
    font-size: 1.5rem;
    font-weight: bolder;
    font-style: italic;
    text-align: center;
}

.signUpLine a {
    color: #6a94ff;
    font-size: 1.5rem;
    font-weight: bolder;
    text-align: center;
    text-decoration: none;
    margin-left: 10px;
}

.signUpLine a:hover {
    text-decoration: underline;
    transform: scale(1.1);
    transition: ease-in-out 0.2s;
}
</style>
