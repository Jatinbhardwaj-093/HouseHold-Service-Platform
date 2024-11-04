<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const profile = ref(null) 
const token = localStorage.getItem('token')

// Fetch profile data on component mount
const fetchProfileData = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5000/professional/profile', {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        profile.value = response.data
    } catch (error) {
        console.error('Error fetching profile:', error.response ? error.response.data : error.message)
    }
}

onMounted(fetchProfileData)

const emit = defineEmits(['openProfileEditModal'])

// Emit event to open the edit modal
const openEditModal = () => {
    emit('openProfileEditModal') 
}
</script>

<template>
    <div v-if="profile" class="modal-content">
        <div class="profileModal">
            <div class="profilePic"></div>
            <div class="detail">
                <div class="professionalName">{{ profile.username }}</div>
                <div class="serviceDetail">
                    <div>Service: {{ profile.serviceType }}</div>
                    <div>Experience: {{ profile.experience }} Years</div>
                </div>
                <div class="Detail">
                    <div>{{ profile.email }}</div>
                    <div>+91 {{ profile.contact }}</div>
                    <div>Pincode: {{ profile.pincode }}</div>
                </div>
                <div class="editProfile" @click="openEditModal">Edit Profile</div>
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
    color: white;
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

.professionalName {
    font-size: 2rem;
    font-weight: bolder;
    font-style: italic;
    margin-bottom: .5rem;
}

.detail{
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.editProfile {
    color: #428eff;
    font-size: 1.5rem;
    font-weight: bolder;
    cursor: pointer;
}

</style>