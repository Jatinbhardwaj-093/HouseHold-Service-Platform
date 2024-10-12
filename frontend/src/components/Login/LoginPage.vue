<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router'; 
import RoleLogin from './RoleLogin.vue';
import axios from 'axios';

const formData = ref({
    role: '',
    username: '',
    password: ''
});

const router = useRouter(); // Create a router instance

const submitForm = async () => {
    try {
        const response = await axios.post('http://127.0.0.1:5000/login', formData.value, {
            headers: {
                'Content-Type': 'application/json',  
            },
        });

        const token = response.data.token;
        const userRole = formData.value.role; // Assuming the role is selected here
        localStorage.setItem('token', token);
        localStorage.setItem('user_role', userRole); // Store the user role

        // Redirect based on user role
        if (userRole === 'admin') {
            router.push({ name: 'admin' }); // Navigate to Admin Home
        } else if (userRole === 'professional') {
            router.push({ name: 'professional' }); // Navigate to Professional Home
        } else if (userRole === 'customer') {
            router.push({ name: 'customer' }); // Navigate to Customer Home
        }

    } catch (error) {
        console.error('Error:', error.response ? error.response.data : error.message);
    }
};

</script>


<template>
    <h1 class="heading">LOGIN</h1>

    <form class="form" @submit.prevent="submitForm">
        <RoleLogin v-model="formData.role" />
        <div>
            <input type="text" class="username" placeholder="USERNAME" v-model="formData.username" />
        </div>
        <div>
            <input type="password" class="password" placeholder="PASSWORD" v-model="formData.password" />
        </div>
        <button type="submit" class="btn">Login</button>
    </form>

    <div class="signUpLine">
        <p>Don't have an account?</p>
        <RouterLink :to="{ name: 'signup'}">Sign Up</RouterLink>
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
