<script setup>
import { onMounted, ref, computed } from 'vue'
import axios from 'axios'
import Search from '@/assets/svg/Search.svg?raw'
import Verification from '@/assets/svg/Verification.svg?raw'
import Flag from '@/assets/svg/Flag.svg?raw'
import MenuDot from '@/assets/svg/MenuDot.svg?raw'
import NoImg from '@/assets/svg/NoImg.svg?raw'
import Cross from '@/assets/svg/Cross.svg?raw'

const detailsRef = ref([])
const token = localStorage.getItem('adminToken')

onMounted(() => {
    document.addEventListener('click', (event) => {
        detailsRef.value.forEach((detail) => {
            if (!detail.contains(event.target)) {
                detail.removeAttribute('open')
            }
        })
        if (showMenu.value && !event.target.closest('.menu-button')) {
            showMenu.value = null
        }
        if (showFilterDropdown.value && !event.target.closest('.filter-container')) {
            showFilterDropdown.value = false
        }
    })
})

const professional = ref([])
const fetchProfessional = async () => {
    try {
        const response = await axios.get(`http://127.0.0.1:5000/admin/professional`, {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })
        professional.value = response.data
    } catch (error) {
        addNotification('Failed to fetch professionals. Please try again.', 5000)
    }
}

// Search and filter state
const searchTerm = ref('')
const showUnverifiedOnly = ref(false)
const filterType = ref('name')
const filterOptions = ['name', 'experience', 'profession']
const showFilterDropdown = ref(false)

// Computed property for filtering professionals
const filteredProfessionals = computed(() => {
    let result = professional.value

    if (showUnverifiedOnly.value) {
        result = result.filter((p) => p.verify === 'no')
    }

    if (searchTerm.value) {
        if (filterType.value === 'name') {
            result = result.filter((p) =>
                p.username.toLowerCase().includes(searchTerm.value.toLowerCase())
            )
        } else if (filterType.value === 'experience') {
            result = result.filter((p) => p.experience >= parseInt(searchTerm.value))
        } else if (filterType.value === 'profession') {
            result = result.filter((p) =>
                p.serviceName.toLowerCase().includes(searchTerm.value.toLowerCase())
            )
        }
    }

    return result
})

// Toggle unverified filter
const toggleUnverifiedFilter = () => {
    showUnverifiedOnly.value = !showUnverifiedOnly.value
}

// Flag, verify, and delete operations
const flagProfessional = async (professional_id, professional_name, flag_condition) => {
    try {
        await axios.put(
            `http://127.0.0.1:5000/admin/professional/${professional_id}/flag`,
            {},
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            }
        )
        fetchProfessional()
        if (flag_condition == 'no') {
            addNotification(`Professional ${professional_name} flagged successfully!`)
        } else {
            addNotification(`Professional ${professional_name} unflagged successfully!`)
        }
    } catch (error) {
        addNotification('Failed to flag professional. Please try again.', 5000)
    }
}

const verifyProfessional = async (professional_id, professional_name) => {
    try {
        await axios.put(
            `http://127.0.0.1:5000/admin/professional/${professional_id}/verify`,
            {},
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            }
        )
        fetchProfessional()
        addNotification(`Professional ${professional_name} verified successfully!`)
    } catch (error) {
        addNotification('Failed to verify professional. Please try again.', 5000)
    }
}

const deleteProfessional = async (professional_id, professional_name) => {
    try {
        await axios.delete(`http://127.0.0.1:5000/admin/professional/${professional_id}/delete`, {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })
        fetchProfessional()
        addNotification(`Professional ${professional_name} deleted successfully!`)
    } catch (error) {
        addNotification('Failed to delete professional. Please try again.', 5000)
    }
}

const showSidebar = ref(false)
const selectedProfessional = ref(null)
const isClosing = ref(false)

const viewProfessional = (professional) => {
    selectedProfessional.value = professional
    showSidebar.value = true
}

const closeSidebar = () => {
    isClosing.value = true
    setTimeout(() => {
        showSidebar.value = false
        isClosing.value = false
    }, 500) // Match the transition duration
}

const showMenu = ref(null)

const toggleMenu = (professionalId) => {
    showMenu.value = showMenu.value === professionalId ? null : professionalId
}

onMounted(() => {
    fetchProfessional()
})

//Notification
import NotificationModal from '../NotificationModal.vue'

const notifications = ref([])

const addNotification = (message, duration = 3000) => {
    notifications.value.push({ message, duration })
}
</script>

<template>
    <div class="main-container">
        <transition name="sidebar">
            <div class="sidebar" v-if="showSidebar && !isClosing">
                <p v-html="Cross" @click="closeSidebar" style="width: 30px; height: 30px;"></p>
                <div v-if="selectedProfessional">
                    <img 
                        v-if="selectedProfessional.image_name"
                        :src="
                            'http://127.0.0.1:5000/static/professionals_imgs/' +
                            selectedProfessional.image_name
                        "
                        alt="Professional Image"
                        class="imagePreview sidebar-detail"
                    />
                    <p class="sidebar-detail" v-else v-html="NoImg"></p>
                    <p class="sidebar-detail"><strong class="sidebar-detail-tags">Name:</strong> {{ selectedProfessional.username }}</p>
                    <p class="sidebar-detail"><strong class="sidebar-detail-tags">Service:</strong> {{ selectedProfessional.serviceName }}</p>
                    <p class="sidebar-detail"><strong class="sidebar-detail-tags">Email:</strong> {{ selectedProfessional.email }}</p>
                    <p class="sidebar-detail"><strong class="sidebar-detail-tags">Experience:</strong> {{ selectedProfessional.experience }} Years</p>
                    <p class="sidebar-detail"><strong class="sidebar-detail-tags">Pincode:</strong> {{ selectedProfessional.pincode }}</p>
                    <p class="sidebar-detail"><strong class="sidebar-detail-tags">Rating:</strong> {{ selectedProfessional.rating }}</p>
                    <p class="sidebar-detail">
                        <strong class="sidebar-detail-tags">Status:</strong>
                        <span v-if="selectedProfessional.verify == 'no'">Not Verified</span>
                        <span v-else-if="selectedProfessional.flag == 'yes'">Flagged</span>
                        <span v-else>OK</span>
                    </p>
                </div>
            </div>
        </transition>
        <div class="container">
            <div class="header">
                <div class="search-section"> 
                    <div class="searchBar">
                        <input
                            type="text"
                            class="search"
                            :placeholder="`Search by ${filterType}`"
                            v-model="searchTerm"
                        />
                        <p class="searchBtn" v-html="Search"></p>
                    </div>
                    <div class="filter-container">
                        <button class="filter-btn" @click="showFilterDropdown = !showFilterDropdown">
                            {{ filterType.charAt(0).toUpperCase() + filterType.slice(1) }}
                        </button>
                        <ul v-if="showFilterDropdown" class="filter-dropdown">
                            <li v-for="option in filterOptions" :key="option" @click="filterType = option; showFilterDropdown = false">
                                {{ option.charAt(0).toUpperCase() + option.slice(1) }}
                            </li>
                        </ul>
                    </div>
                </div>
                <div @click="toggleUnverifiedFilter" class="btn">
                    <p v-html="Verification" class="VerificationBtn"></p>
                    <p>Verify</p>
                </div>
            </div>
            <div v-if="filteredProfessionals.length > 0" class="card-container">
                <div v-for="prof in filteredProfessionals" :key="prof.professionalId" class="card">
                    <div class="image-holder">
                        <img
                            v-if="prof.image_name"
                            :src="'http://127.0.0.1:5000/static/professionals_imgs/' + prof.image_name"
                            alt="Professional Image"
                            class="imagePreview"
                        />
                        <p v-else v-html="NoImg" class="noImagePreview"></p>
                    </div>
                    <div class="divider"></div>
                    <div class="card-body">
                        <div class="verified">
                            <p v-if="prof.verify == 'yes'" v-html="Verification" style="height: 20px; width: 20px;" ></p>
                            <p v-if="prof.flag == 'yes'" v-html="Flag" style="height: 20px; width: 20px;"></p>
                            <p class="username">{{ prof.username }}</p>
                        </div>
                        <div class="menu-button">
                            <button @click="toggleMenu(prof.professionalId)" class="menu-btn">
                                <p v-html="MenuDot" style="height: 80%; width: 80%; margin-left: 3px; margin-bottom: 5px;"></p>
                            </button>
                            <ul v-if="showMenu === prof.professionalId" class="menu-list">
                                <li @click="viewProfessional(prof)">View</li>
                                <li
                                    @click="verifyProfessional(prof.professionalId, prof.username)"
                                    v-if="prof.verify == 'no'"
                                >
                                    Verify
                                </li>
                                <li
                                    @click="
                                        flagProfessional(
                                            prof.professionalId,
                                            prof.username,
                                            prof.flag
                                        )
                                    "
                                    v-else
                                >
                                    {{ prof.flag == 'no' ? 'Flag' : 'Unflag' }}
                                </li>
                                <li @click="deleteProfessional(prof.professionalId, prof.username)">
                                    Delete
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            <img
                class="emptyMessage"
                v-else
                src="@/assets/images/empty-box.png"
                alt="No professionals found"
            />
        </div>
        <NotificationModal
            class="notification-modal"
            v-for="(notification, index) in notifications"
            :key="index"
            :message="notification.message"
            :duration="notification.duration"
            @close="notifications.splice(index, 1)"
        />
    </div>
</template>

<style scoped>
.main-container {
    display: flex;
    width: 98%;
    margin: auto;
    overflow: hidden; /* Remove scrolling from main-container */
    gap: .5rem;
}

.container {
    width: 95%;
    margin:auto;
    height: 85vh;
    border-radius: 1rem;
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.6);
    background-color: #3c3c3c;
    scrollbar-width: thin;
    overflow: auto;
    padding-bottom: 4rem;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 2rem;
}

.search-section {
    display: flex;
    width: min(100%, 850px);
    gap: 1rem;
}

.searchBar {
    display: flex;
    justify-content: start;
    background-color: black;
    box-shadow: 5px 5px 10px rgb(0, 0, 0);
    border-radius: 0.5rem;
    padding: 0.5rem;
    width: min(100%, 750px);

}

input {
    width: 95%;
    background-color: transparent;
    border: none;
    outline: none;
    color: white;
    font-size: 1.5rem;
    vertical-align: middle;
    padding-left: 1rem;
}

.searchBtn,
.VerificationBtn {
    height: 35px;
    width: 35px;
}

input:focus::placeholder {
    color: transparent;
}

.filter-container {
    position: relative;
}

.filter-btn {
    background-color: rgba(255, 90, 1, 0.8);
    box-shadow: 5px 5px 5px #2c2b2b;
    border: none;
    border-radius: .5rem;
    width: 8rem;
    color: #f5f5dc;
    cursor: pointer;
    font-size: 1rem;
    padding: 1rem;
}

.filter-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    background: #2c2b2b;
    border-radius: .5rem;
    list-style: none;
    padding: 0;
    width: 8rem; /* Changed from width: inherit */
    margin: .5rem 0; /* Changed from margin: .5rem auto */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.6);
    z-index: 100;
}

.filter-dropdown li {
    padding: 0.5rem 1rem;
    cursor: pointer;
    color: #f5f5dc;
}

.filter-dropdown li:hover {
    background: #3c3c3c;
}

.card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: center;
}

.card {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 0.5rem;
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.6);
    padding: 1rem;
    padding-bottom: 0;
    width: 300px;
    color: #f5f5dc;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.card-body {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}

.username {
    font-size: 1.5rem;
    font-weight: 600;
    color: #fe772e;
    margin: 0.5rem 0;
}

.divider {
    width: 100%;
    height: 1px;
    background-color: #6b6a6a;
}

.card-body p {
    margin: 0.5rem 0;
}

.verified {
    display: flex;
    align-items: center;
    gap: 5px;
}

.card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.footer-divider {
    display: flex;
    justify-content: space-between;
    width: 100%;
}

.verification-badge {
    display: flex;
    align-items: center;
    gap: 2px;
    margin-bottom: 8px;
}

.btn {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    width: 10rem;
    font-size: 1.5rem;
    background-color: hsla(210, 6%, 7%, 0.85);
    color: #f5f5dc;
    border: none;
    border-radius: 0.5rem;
    padding: 0.75rem;
    cursor: pointer;
}

.emptyMessage {
    height: 250px;
    width: 250px;
    display: block;
    margin: auto;
    margin-top: 2rem;
}

.menu-button {
    position: relative;
}

.menu-btn {
    background-color: #2c2b2b;
    border: none;
    border-radius: 5px;
    height: 2rem;
    width: 2rem;
    vertical-align: middle;
    text-align: center;
    cursor: pointer;
}

.menu-list {
    position: absolute;
    right: 150%;
    bottom: 50%;
    background: #2c2b2b;
    list-style: none;
    padding: 0;
    margin: 0;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.6);
    z-index: 100;
}

.menu-list li {
    padding: 0.5rem 1rem;
    cursor: pointer;
    color: #f5f5dc;
}

.menu-list li:hover {
    background: #3c3c3c;
}

.sidebar {
    width: 30%;
    height: 85vh;
    background: #2c2b2b;
    border-radius: 1rem;
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.6);
    padding: 1rem;
    overflow-y: auto;
    color: #f5f5dc;
    transition: transform .5s ease-in-out, opacity .5s ease-in-out;
}

/* Animation for the sidebar opening */
.sidebar-enter-active,
.sidebar-leave-active {
    transition: transform .5s ease-in-out, opacity .5s ease-in-out;
}

.sidebar-enter-from {
    transform: translateX(-100%);
    opacity: 0;
}

.sidebar-enter-to {
    transform: translateX(0);
    opacity: 1;
}

.sidebar-leave-from {
    transform: translateX(0);
    opacity: 1;
}

.sidebar-leave-to {
    transform: translateX(-100%);
    opacity: 0;
}

.sidebar-detail{
    margin-bottom: .5rem;
}

.sidebar-detail-tags {
    font-weight: 600;
    margin-right: 0.5rem;
    color: #fe772e;
    font-size: 1.25rem;
}


.image-holder {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #3c3c3c;
    border-radius: 2rem;
    width: 15rem;
    height: 10rem;
    padding: 0.5rem;
    margin-bottom: 1rem;
}

.imagePreview {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.noImagePreview {
    width: 70%;
    height: 70%;
    margin-bottom: 3rem;
    object-fit: contain;
}
</style>
