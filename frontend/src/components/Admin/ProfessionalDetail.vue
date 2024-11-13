<script setup>
import { onMounted, ref, computed } from 'vue'
import axios from 'axios'
import Search from '@/assets/svg/Search.svg?raw'

const detailsRef = ref([])

// Listen for clicks outside of details elements to close them
onMounted(() => {
    document.addEventListener('click', (event) => {
        detailsRef.value.forEach((detail) => {
            if (!detail.contains(event.target)) {
                detail.removeAttribute('open')
            }
        })
    })
})

// Token for authorization
const token = localStorage.getItem('token')

// Fetch professionals data
const professional = ref([])
const fetchProfessional = async () => {
    try {
        const response = await axios.get(`http://127.0.0.1:5000/admin/professional`, {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });
        professional.value = response.data;
    } catch (error) {
        console.error('Failed to fetch professional:', error);
    }
}

// Search functionality
const searchTerm = ref('') // Reactive variable for search input
const filteredProfessionals = computed(() => {
    if (!searchTerm.value) return professional.value
    return professional.value.filter(p => 
        p.username.toLowerCase().includes(searchTerm.value.toLowerCase())
    )
})

onMounted(() => {
    fetchProfessional()
})

// Flag, verify, and delete operations for professionals
const flagProfessional = async (professional_id) => {
    try {
        await axios.put(`http://127.0.0.1:5000/admin/professional/${professional_id}/flag`, {}, {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });
        fetchProfessional()
    } catch (error) {
        console.error('Failed to flag professional:', error);
    }
}

const verifyProfessional = async (professional_id) => {
    try {
        await axios.put(`http://127.0.0.1:5000/admin/professional/${professional_id}/verify`, {}, {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });
        fetchProfessional()
    } catch (error) {
        console.error('Failed to verify professional:', error);
    }
}

const deleteProfessional = async (professional_id) => {
    try {
        await axios.delete(`http://127.0.0.1:5000/admin/professional/${professional_id}/delete`, {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });
        fetchProfessional()
    } catch (error) {
        console.error('Failed to delete professional:', error);
    }
}
</script>

<template>
    <div>
        <div class="container">
            <div class="searchBar">
                <input 
                    type="text" 
                    class="search" 
                    placeholder="Search by professional name" 
                    v-model="searchTerm" />
                <p class="searchBtn" v-html="Search"></p>
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
                            <button @click="verifyProfessional(prof.professionalId)">Verify</button>
                        </td>
                        <td v-else style="color: rgb(82, 149, 231); font-weight: 600">Verified</td>
                        <td v-if="prof.verify == 'yes'">
                            <button @click="flagProfessional(prof.professionalId)">
                                {{ prof.flag == 'no' ? 'Flag' : 'Unflag' }}
                            </button>
                        </td>
                        <td>
                            <button @click="deleteProfessional(prof.professionalId)">Delete</button>
                        </td>
                    </tr>
                </tbody>
            </table>
            <img class="emptyMessage" v-else src="@/assets/images/empty-box.png" alt="No professionals found">
        </div>
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
    overflow:auto;
    scrollbar-width: thin;
}

.searchBar {
    display: flex;
    justify-content: start;
    background-color: black;
    box-shadow: 5px 5px 10px rgb(0, 0, 0);
    border-radius: 0.5rem;
    padding: 0.5rem;
    margin: 2rem;
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

.searchBtn {
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

.emptyMessage{
    height: 250px;
    width: 250px;
    display: block;
    margin: auto;
    margin-top: 2rem;
}
</style>
