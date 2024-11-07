<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Logout from '@/assets/svg/Logout.svg?raw'
import ProfileModal from '@/components/Customer/ProfileModal.vue'
import ProfileEditModal from './ProfileEditModal.vue'
import axios from 'axios'

const token = localStorage.getItem('token')

const profileModal = ref(false) 
const customer = ref({
            'email': '',
            'username': '',
            'password': '',
            'contact': null,
            'pincode': null,
            'address': ''
        })

// Getting customer details

axios.get('http://127.0.0.1:5000/customer/', {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
    .then((response) => {
        customer.value = response.data.customer
    })
    .catch((error) => {
        console.error(error)
    })


// Profile Modal
const showModal = (event) => {
    event.stopPropagation() 
    profileModal.value = true 
}

const closeModal = () => {

    profileModal.value = false 
}

const handleClickOutside = (event) => {
    const modal = document.querySelector('.modal-content')
    
    if (modal && !modal.contains(event.target) && profileModal.value) {
        closeModal()
    }
}

onMounted(() => {
    document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
})

// Profile Edit Modal

const profileEditModal = ref(false)

const openEditModal = () => {
    profileModal.value = false
    profileEditModal.value = true
}

const closeEditModal = () => {
    profileEditModal.value = false
}

</script>

<template>
    <div>
        <div class="navbar" :class="{ 'blur-background': profileModal || profileEditModal }">
            <div class="customerDetail">
                <div @click="showModal" class="img"></div>
                <div class="customerName">{{ customer.username }}</div>
            </div>
            <div class="menu">
                <div class="home" @click="$router.push({ name: 'customer' })">Home</div>
                <div class="service" @click="$router.push({ name: 'customer-services' })">Service</div>
                <div class="stats">Statistics</div>
            </div>
            <div class="logout" v-html="Logout"></div>
        </div>

        <!-- Modal -->
        <ProfileModal v-if="profileModal" class="modal-content" @close="closeModal" @openProfileEditModal="openEditModal" />

        <!-- Edit Modal -->
        <ProfileEditModal v-if="profileEditModal" class="editModal-content" @closeProfileEditModal="closeEditModal"
        :profileData="customer" />
    </div>
</template>

<style scoped>

.blur-background {
    filter: blur(5px);
    transition: filter 0.3s ease;
}

.navbar {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    height: 10vh;
    background-color: hsla(21, 100%, 50%, 0.8);
    margin: 1rem;
    margin-right: 1rem;
    padding: 1rem;
    border-radius: 1rem;
    box-shadow: 8px 8px 25px rgba(0, 0, 0, 0.8);
}

.customerDetail {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 0.7rem;
}

.img {
    height: 3rem;
    width: 3rem;
    background-color: #ece3e3;
    border-radius: 50%;
    box-shadow: 2px 2px 15px rgba(0, 0, 0, 0.6);
}

.customerName {
    color: #fff;
    font-size: 1.5rem;
    font-weight: bolder;
    font-style: italic;
    padding-top: 1rem;
}

.menu {
    display: flex;
    flex-direction: row;
    gap: 1.5rem;
    color: #fff;
    margin-top: 0.5rem;
}

.home,
.service,
.stats {
    font-size: 1.5rem;
    font-weight: bolder;
    cursor: pointer;
}

.home:hover,
.service:hover,
.stats:hover {
    transform: scale(1.1);
    transition: ease-in-out 0.2s;
}

.logout {
    height: 40px;
    width: 40px;
    cursor: pointer;
    z-index: 1000000;
}

</style>
