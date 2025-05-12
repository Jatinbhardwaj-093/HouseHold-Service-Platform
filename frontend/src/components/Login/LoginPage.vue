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
    const { role, username } = formData.value

    if (!role || !username) {
        addNotification('Please provide valid role and username.', 5000)
        return
    }

    try {
        // Fetch condition only if the role is not admin
        let condition = {}
        if (role !== 'admin') {
            const conditionResponse = await axios.get(
                `http://127.0.0.1:5000/condition/${role}/${username}`
            )
            condition = conditionResponse.data

            // Check conditions for roles other than admin
            if (condition.flag === 'yes') {
                addNotification('Currently you are not allowed to login', 5000)
                return
            }

            if (role === 'professional' && condition.verify === 'no') {
                addNotification('Currently your file is under verification! Please wait.', 5000)
                return
            }
        }

        // Proceed to login
        const loginResponse = await axios.post('http://127.0.0.1:5000/login', formData.value, {
            headers: { 'Content-Type': 'application/json' }
        })

        // Store the token based on user role in local storage
        const token = loginResponse.data.token
        if (role === 'admin') {
            localStorage.setItem('adminToken', token)
        } else if (role === 'professional') {
            localStorage.setItem('professionalToken', token)
        } else if (role === 'customer') {
            localStorage.setItem('customerToken', token)
        }

        // Redirect based on user role
        if (role === 'admin') {
            router.push({ name: 'admin' })
        } else if (role === 'professional') {
            router.push({ name: 'professional' })
        } else if (role === 'customer') {
            router.push({ name: 'customer' })
        }
    } catch (error) {
        console.error(error)
        if (error.response?.data?.message) {
            addNotification(error.response.data.message, 5000)
        } else {
            addNotification('Login failed. Please check your credentials.', 5000)
        }
    }
}

//Notification
import NotificationModal from '../NotificationModal.vue'

const notifications = ref([])

const addNotification = (message, duration) => {
    notifications.value.push({ message, duration })
}
</script>

<template>
    <div class="login-container">
        <div class="login-wrapper">
            <h1 class="heading">LOGIN</h1>

            <form class="form" @submit.prevent="submitForm">
                <div class="form-header">
                    <span class="form-subtitle">Welcome Back</span>
                </div>

                <div class="form-group">
                    <RoleLogin v-model="formData.role" />
                </div>

                <div class="form-group">
                    <label class="form-label" for="username">Username</label>
                    <div class="input-icon-wrapper">
                        <span class="input-icon">👤</span>
                        <input
                            id="username"
                            type="text"
                            class="username"
                            placeholder="Enter your username"
                            v-model="formData.username"
                        />
                    </div>
                </div>

                <div class="form-group">
                    <label class="form-label" for="password">Password</label>
                    <div class="input-icon-wrapper">
                        <span class="input-icon">🔒</span>
                        <input
                            id="password"
                            type="password"
                            class="password"
                            placeholder="Enter your password"
                            v-model="formData.password"
                        />
                    </div>
                </div>

                <button type="submit" class="btn">
                    <span class="btn-text">Login</span>
                    <span class="btn-icon">➔</span>
                </button>
            </form>

            <div class="signUpLine">
                <p>Don't have an account?</p>
                <RouterLink :to="{ name: 'signup' }">Sign Up</RouterLink>
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
.login-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: #000;
    padding: 20px;
    background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.9)),
        url('../assets/images/webHomePage.png');
    background-size: cover;
    background-position: center;
    position: relative;
}

.login-container::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at center, transparent 30%, rgba(0, 0, 0, 0.6));
    pointer-events: none;
    z-index: 1;
}

.login-wrapper {
    width: 100%;
    max-width: 700px;
    padding: 40px 20px;
    border-radius: 20px;
    background-color: rgba(33, 32, 32, 0.8);
    backdrop-filter: blur(10px);
    position: relative;
    z-index: 10;
}

.heading {
    text-align: center;
    font-size: 3.5rem;
    margin-top: 0.5rem;
    margin-bottom: 2rem;
    font-weight: 800;
    font-style: italic;
    background: linear-gradient(135deg, #ff5c01, #ff8f01);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 2px 10px rgba(255, 92, 1, 0.3);
    letter-spacing: 2px;
}

.form {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: auto;
    margin-bottom: 2rem;
    background-color: rgba(25, 25, 25, 0.85);
    padding: 3rem 2.5rem;
    border-radius: 15px;
    max-width: 600px;
    border: 1px solid rgba(255, 92, 1, 0.3);
    box-shadow:
        0 15px 35px rgba(255, 92, 1, 0.15),
        inset 0 2px 10px rgba(0, 0, 0, 0.5);
}

.form-header {
    width: 100%;
    text-align: center;
    margin-bottom: 1.5rem;
}

.form-subtitle {
    color: #e0e0e0;
    font-size: 1.4rem;
    font-weight: 300;
    letter-spacing: 0.5px;
}

.form-group {
    width: 100%;
    margin-bottom: 20px;
}

.form-label {
    display: block;
    font-size: 1rem;
    font-weight: 500;
    color: #e0e0e0;
    margin-bottom: 8px;
    margin-left: 5px;
}

.input-icon-wrapper {
    position: relative;
    width: 100%;
}

.input-icon {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.2rem;
    color: #ff5c01;
    z-index: 2;
    transition: all 0.3s;
}

.form input {
    width: 100%;
    height: 3.5rem;
    outline: none;
    color: white;
    border-radius: 12px;
    border: 1px solid rgba(255, 92, 1, 0.3);
    padding: 0.8rem;
    padding-left: 3rem;
    font-size: 1.1rem;
    font-weight: 400;
    background-color: rgba(10, 10, 10, 0.6);
    box-shadow:
        inset 0 2px 8px rgba(0, 0, 0, 0.3),
        0 0 15px rgba(255, 92, 1, 0.1);
    transition: all 0.3s ease;
}

.form input:focus {
    border: 2px solid #ff5c01;
    background-color: rgba(20, 20, 20, 0.7);
    box-shadow: 0 0 20px rgba(255, 92, 1, 0.25);
}

.form input:focus + .input-icon {
    transform: translateY(-50%) scale(1.2);
    color: #ff8f01;
}

.form input:focus::placeholder {
    color: rgba(255, 255, 255, 0.3);
    font-size: 0.9rem;
}

.btn {
    width: 100%;
    height: 3.5rem;
    border-radius: 12px;
    border: none;
    background: linear-gradient(135deg, #ff5c01, #ff8f01);
    color: #fff;
    font-size: 1.2rem;
    font-weight: 600;
    cursor: pointer;
    margin-top: 1.5rem;
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
    font-size: 1.2rem;
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

.signUpLine {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: auto;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    background-color: rgba(17, 17, 17, 0.5);
    padding: 15px;
    border-radius: 8px;
    max-width: 450px;
    border: 1px solid rgba(255, 92, 1, 0.1);
}

.signUpLine p {
    color: #ccc;
    font-size: 1.2rem;
    font-weight: 500;
    text-align: center;
}

.signUpLine a {
    color: #ff5c01;
    font-size: 1.2rem;
    font-weight: 600;
    text-align: center;
    text-decoration: none;
    margin-left: 10px;
    position: relative;
    padding-bottom: 2px;
}

.signUpLine a::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 2px;
    background-color: #ff5c01;
    transition: width 0.3s ease;
}

.signUpLine a:hover::after {
    width: 100%;
}

.signUpLine a:hover {
    text-shadow: 0 0 8px rgba(255, 92, 1, 0.5);
    transition: all 0.3s ease;
}

/* Media query for smaller screens */
@media screen and (max-width: 768px) {
    .heading {
        font-size: 2.8rem;
        margin-bottom: 1.5rem;
    }

    .form {
        padding: 2rem 1.5rem;
    }

    .form-subtitle {
        font-size: 1.2rem;
    }

    .btn {
        height: 3.2rem;
    }

    .signUpLine {
        margin-top: 1rem;
        padding: 12px;
    }
}
</style>
