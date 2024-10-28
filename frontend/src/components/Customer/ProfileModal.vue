<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const profile = ref(null) 
const token = localStorage.getItem('token')



onMounted(() => {
    axios.get('http://127.0.0.1:5000/customer/profile', {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
    .then((response) => {
        profile.value = response.data 
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
                <div class="profilePic"></div>
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
    top: 15%;
    left: 1%;
    width: max(45%, 350px);
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
    width: 3.5rem;
    height: 3.5rem;
    border-radius: 50%;
    margin-top: 1rem;
    background-color: #d9d9d9;
    box-shadow: 5px 5px 25px rgb(0, 0, 0);
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
    margin-bottom: 5px;
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
