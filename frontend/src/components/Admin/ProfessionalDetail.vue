<script setup>
import { onMounted, ref, computed } from 'vue'
import axios from 'axios'
import Search from '@/assets/svg/Search.svg?raw'
import Verification from '@/assets/svg/Verification.svg?raw'

const detailsRef = ref([])
const token = localStorage.getItem('adminToken')

onMounted(() => {
    document.addEventListener('click', (event) => {
        detailsRef.value.forEach((detail) => {
            if (!detail.contains(event.target)) {
                detail.removeAttribute('open')
            }
        })
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

// Computed property for filtering professionals
const filteredProfessionals = computed(() => {
    let result = professional.value

    if (showUnverifiedOnly.value) {
        result = result.filter((p) => p.verify === 'no')
    }

    if (searchTerm.value) {
        result = result.filter((p) =>
            p.username.toLowerCase().includes(searchTerm.value.toLowerCase())
        )
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
    <div>
        <div class="container">
            <div class="header">
                <div class="searchBar">
                    <input
                        type="text"
                        class="search"
                        placeholder="Search by professional name"
                        v-model="searchTerm"
                    />
                    <p class="searchBtn" v-html="Search"></p>
                </div>
                <div @click="toggleUnverifiedFilter" class="btn">
                    <p v-html="Verification" class="VerificationBtn"></p>
                    <p>Verify</p>
                </div>
            </div>
            <div v-if="filteredProfessionals.length > 0" class="card-container">
                <div v-for="prof in filteredProfessionals" :key="prof.professionalId" class="card">
                    <div class="card-header">
                        <p class="username">{{ prof.username }}</p>
                        <div v-if="prof.verify == 'yes'" class="verification-badge">
                            <p v-html="Verification" style="height: 15px; width: 15px"></p>
                            <p style="color: rgb(82, 149, 231); font-weight: 600">Verified</p>
                        </div>
                    </div>
                    <div class="card-body">
                        <p><strong>Service:</strong> {{ prof.serviceName }}</p>
                        <p><strong>Email:</strong> {{ prof.email }}</p>
                        <p><strong>Experience:</strong> {{ prof.experience }} Years</p>
                        <p><strong>Pincode:</strong> {{ prof.pincode }}</p>
                        <p><strong>Rating:</strong> {{ prof.rating }}</p>
                        <p>
                            <strong>Status:</strong>
                            <span v-if="prof.verify == 'no'">Not Verified</span>
                            <span v-else-if="prof.flag == 'yes'">Flagged</span>
                            <span v-else>OK</span>
                        </p>
                    </div>
                    <div class="card-footer">
                        <div class="footer-divider">
                            <div>
                                <button
                                    v-if="prof.verify == 'no'"
                                    @click="verifyProfessional(prof.professionalId, prof.username)"
                                >
                                    Verify
                                </button>
                            </div>
                            <div>
                                <button
                                    style="margin-right: 5px"
                                    v-if="prof.verify == 'yes'"
                                    @click="
                                        flagProfessional(
                                            prof.professionalId,
                                            prof.username,
                                            prof.flag
                                        )
                                    "
                                >
                                    {{ prof.flag == 'no' ? 'Flag' : 'Unflag' }}
                                </button>
                                <button
                                    @click="deleteProfessional(prof.professionalId, prof.username)"
                                >
                                    Delete
                                </button>
                            </div>
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
.container {
    width: 95%;
    height: 80vh;
    margin: auto;
    border-radius: 1rem;
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.6);
    background-color: #3c3c3c;
    overflow: auto;
    scrollbar-width: thin;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 2rem;
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

.card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: center;
}

.card {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 0.5rem;
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.6);
    padding: 1rem;
    width: 300px;
    color: #f5f5dc;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: end;
}

.username {
    font-size: 2rem;
    font-weight: 600;
    color: #fe772e;
}

.card-body p {
    margin: 0.5rem 0;
}

.card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
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

button {
    border: none;
    border-radius: 0.2rem;
    width: 4rem;
    color: white;
    cursor: pointer;
    background-color: #1e1e1e;
    color: #fe772e;
    padding: 3px;
    text-align: center;
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
</style>
