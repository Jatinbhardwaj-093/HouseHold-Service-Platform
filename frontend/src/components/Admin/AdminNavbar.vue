<script setup>
import Logout from '@/assets/svg/Logout.svg?raw';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter()
//Logout
const logout = async () => {
    try {
        await axios.post('http://127.0.0.1:5000/admin/logout',{},{
            headers: {
                Authorization: `Bearer ${localStorage.getItem('adminToken')}`
            }
        });
    } catch (error) {
        console.error('Error during logout:', error);
    } finally {
        localStorage.removeItem('adminToken');
        router.push({ path: '/login' });
    }
};

</script>


<template>
    <div>
        <div class="navbar">
        <div><router-link class="home" :to="{ name: 'admin' }">Home</router-link></div>
        <div ><router-link class="professional" :to="{ name: 'professional-detail' }">Professional</router-link></div>
        <div><router-link class="customer" :to="{name: 'customer-detail'}">Customer</router-link></div>
        <div><router-link class="ongoing" :to="{name: 'ongoing-service'}">Ongoing Services</router-link></div>
        <div><router-link class="Statistics" :to="{name: 'admin-statistics'}">Statistics </router-link></div>
        <div v-html="Logout" class="logout" @click="logout"></div>
    </div>
    </div>
</template>


<style scoped>
.navbar{
    width: 95%;
    margin: auto;
    margin-top: 0.7rem;
    display: flex;
    justify-content: start;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    border-radius: 1rem;
    background-color: rgba(255, 90, 1, 0.8);
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.6);
}

.home, .professional, .customer, .ongoing, .Statistics{
    text-decoration: none;
    cursor: pointer;
    color: #fff;
    font-size: 1.2rem;
    font-weight: bolder;
}

.navbar > div{
    cursor: pointer;
    color: #fff;
    font-size: 1.2rem;
    font-weight: bolder;
}

.navbar > div:hover{
    transform: scale(1.1);
    transition: ease-in-out 0.2s;
}

.logout {
    height: 35px;
    width: 36px;
    margin-left: auto;
    vertical-align: middle;
}
</style>