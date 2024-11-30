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
const flagProfessional = async (professional_id,professional_name,flag_condition) => {
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

const verifyProfessional = async (professional_id,professional_name) => {
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

const deleteProfessional = async (professional_id,professional_name) => {
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
            <table v-if="filteredProfessionals.length > 0">
                <thead>
                    <tr class="headrow">
                        <th style="width: 1%"></th>
                        <th>S.No</th>
                        <th>Professional</th>
                        <th>Service</th>
                        <th>Email</th>
                        <th>Experience</th>
                        <th>Pincode</th>
                        <th>Rating</th>
                        <th>Status</th>
                        <th>Verification</th>
                        <th style="width: 5%"></th>
                        <th style="width: 8%"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(prof, index) in filteredProfessionals" :key="prof.professionalId">
                        <td v-if="prof.flag == 'no'"></td>
                        <td v-else><p v-html="Flag"></p></td>
                        <td>{{ index + 1 }}</td>
                        <td>{{ prof.username }}</td>
                        <td>{{ prof.serviceName }}</td>
                        <td>{{ prof.email }}</td>
                        <td>{{ prof.experience }} Years</td>
                        <td>{{ prof.pincode }}</td>
                        <td>{{ prof.rating }}</td>
                        <td v-if="prof.verify == 'no'">Not Verified</td>
                        <td v-else-if="prof.flag == 'yes'">Flagged</td>
                        <td v-else>OK</td>
                        <td v-if="prof.verify == 'no'">
                            <button @click="verifyProfessional(prof.professionalId, prof.username)">Verify</button>
                        </td>
                        <td v-else style="color: rgb(82, 149, 231); font-weight: 600">Verified</td>
                        <td v-if="prof.verify == 'yes'">
                            <button @click="flagProfessional(prof.professionalId, prof.username, prof.flag)">
                                {{ prof.flag == 'no' ? 'Flag' : 'Unflag' }}
                            </button>
                        </td>
                        <td v-else></td>
                        <td>
                            <button @click="deleteProfessional(prof.professionalId, prof.username)">Delete</button>
                        </td>
                    </tr>
                </tbody>
            </table>
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

table {
    width: 98%;
    border: none;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 0.5rem;
    overflow: hidden;
    margin: auto;
}

th,
td {
    padding: 4px;
    text-align: start;
    border-bottom: 1px solid #f5f5dc;
}

tr:last-child td {
    border-bottom: none;
}

tr:nth-child(even) {
    background-color: #2f2c2c;
}

.headrow {
    color: white;
    background-color: hsla(21, 100%, 50%, 0.85);
}

tr {
    color: #f5f5dc;
    background-color: #3c3c3c;
}

.option {
    display: flex;
    gap: 5px;
    justify-content: center;
    align-items: center;
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
