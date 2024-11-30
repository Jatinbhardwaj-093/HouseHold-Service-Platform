<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import DefaultProfile from '@/assets/svg/DefaultProfile.svg?raw'

const profile = ref(null) 
const token = localStorage.getItem('professionalToken')

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
            <div class="profilePic" @click="showModal">
                    <img v-if="profile.image_name"
                        :src="'http://127.0.0.1:5000/static/professionals_imgs/' + profile.image_name"
                        alt="Profile Image" 
                        class="profile-img"
                    />
                    <p v-else v-html="DefaultProfile" class="profile-img"></p>
                </div>
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
    top: 14%;
    left: 1%;
    width: max(30%, 400px);
    color: white;
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
    border: none;
    color: #428eff;
    font-size: 1rem;
    font-weight: bolder;
    cursor: pointer;
    width: max-content;
}

</style>