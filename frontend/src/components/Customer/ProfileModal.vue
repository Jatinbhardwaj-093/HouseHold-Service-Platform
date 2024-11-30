<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import DefaultProfile from '@/assets/svg/DefaultProfile.svg?raw'

const profile = ref(null) 
const token = localStorage.getItem('customerToken')

onMounted(() => {
    axios.get('http://127.0.0.1:5000/customer/profile', {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
    .then((response) => {
        profile.value = response.data.customer 
    })
    .catch((error) => {
        console.error(error)
    })
})

const emit = defineEmits(['openProfileEditModal'])

const openEditModal = () => {
    emit('openProfileEditModal') 
}

</script>

<template>
    <div>
        <div class="modal-content" v-if="profile">
            <div class="profileModal">
                <div class="profilePic" @click="showModal">
                    <img v-if="profile.image_name"
                        :src="'http://127.0.0.1:5000/static/customers_imgs/' + profile.image_name"
                        alt="Profile Image" 
                        class="profile-img"
                    />
                    <p v-else v-html="DefaultProfile" class="profile-img"></p>
                </div>
                <div class="detail">
                    <div class="customerName">{{ profile.username }}</div>
                    <div class="contactDetail">
                        <div class="customerContact">+91 {{ profile.contact }}</div>
                        <div class="customerEmail">{{ profile.email }}</div>
                    </div>
                    <div class="addressDetail">
                        <div class="customerAddress">Address: {{ profile.address }}</div>
                        <div class="customerPincode">Pincode: {{ profile.pincode }}</div>
                    </div>
                    <div class="editProfile" @click="openEditModal">Edit Profile</div>
                </div>
            </div>
        </div>
    </div>
</template>


<style scoped>
.modal-content {
    position: absolute;
    top: 14%;
    left: 1%;
    width: max(30%, 400px);
    z-index: 10000;
}

.profileModal {
    display: flex;
    align-items: start;
    justify-content: start;
    padding: 1rem;
    gap: 1rem;
    background-color: #555454;
    border-radius: 1rem;
    box-shadow: 2px 5px 20px rgba(0, 0, 0, 0.6);
}

.profilePic {
    width: 4rem;
    height: 4rem;
    border-radius: 50%;
    margin-top: 1rem;
    padding: 5px;
    background-color: #d9d9d9;
    box-shadow: 5px 5px 25px rgb(0, 0, 0);
}

.profile-img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    overflow: hidden;
}

.customerName {
    font-size: 2rem;
    font-weight: bolder;
    font-style: italic;
    color: #ffffff;
    margin-bottom: .5rem;
}
.customerContact,
.customerEmail,
.customerAddress,
.customerPincode {
    color: #ffffff;
}

.contactDetail {
    margin-bottom: 10px;
}
.addressDetail {
    margin-bottom: 8px;
}

.editProfile {
    border: none;
    color: #428eff;
    font-size: 1rem;
    font-weight: bolder;
    cursor: pointer;
    width: max-content;
}
</style>
