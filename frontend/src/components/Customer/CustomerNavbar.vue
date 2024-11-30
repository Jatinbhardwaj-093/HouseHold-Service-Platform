<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import Logout from '@/assets/svg/Logout.svg?raw'
import DefaultProfile from '@/assets/svg/DefaultProfile.svg?raw'
import ProfileModal from '@/components/Customer/ProfileModal.vue'
import ProfileEditModal from './ProfileEditModal.vue'
import axios from 'axios'

const router = useRouter()
const token = localStorage.getItem('customerToken')

const profileModal = ref(false) 
const customer = ref({})

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

//Logout
const logout = async () => {
    try {
        await axios.post('http://127.0.0.1:5000/customer/logout',{},{
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
        ); 
    } catch (error) {
        console.error('Error during logout:', error);
    } finally {
        localStorage.removeItem('customerToken');
        router.push({ path: '/login' });
    }
};


// Notification Modal
import NotificationModal from '../NotificationModal.vue'

const notifications = ref([])   

const addNotification = (message, duration = 3000) => {
    notifications.value.push({ message, duration })
}
</script>

<template>
    <div>
        <div class="navbar" :class="{ 'blur-background': profileModal || profileEditModal }">
            <div class="customerDetail">
                <div class="img" @click="showModal">
                    <img v-if="customer.image_name"
                        :src="'http://127.0.0.1:5000/static/customers_imgs/' + customer.image_name"
                        alt="Profile Image" 
                        class="profile-img"
                    />
                    <p v-else v-html="DefaultProfile" class="profile-img"></p>
                </div>
                <div class="customerName">{{ customer.username }}</div>
            </div>
            <div class="menu">
                <div class="home" @click="$router.push({ name: 'customer' })">Home</div>
                <div class="service" @click="$router.push({ name: 'customer-services' })">Service</div>
                <div class="stats" @click="$router.push({ name: 'customer-statistics' })">Statistics</div>
            </div>
            <div class="logout" v-html="Logout" @click="logout"></div>
        </div>

        <!-- Modal -->
        <ProfileModal v-if="profileModal" 
        class="modal-content" 
        @close="closeModal" 
        @openProfileEditModal="openEditModal" />

        <!-- Edit Modal -->
        <ProfileEditModal v-if="profileEditModal" 
        class="editModal-content" 
        @closeProfileEditModal="closeEditModal"
        @Notification="addNotification('Profile updated successfully!', 3000)"
        @error="addNotification('Error updating profile', 3000)"
        :profileData="customer" />

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
    height: 3.2rem;
    width: 3.2rem;
    background-color: #ece3e3;
    border-radius: 50%;
    padding: 5px;
    box-shadow: 2px 2px 15px rgba(0, 0, 0, 0.6);

}

.profile-img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    overflow: hidden;
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
