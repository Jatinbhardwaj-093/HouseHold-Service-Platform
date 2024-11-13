<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import Search from '@/assets/svg/Search.svg?raw'

const token = localStorage.getItem('token')
const OngoingServices = ref([])

const fetchOngoingServices = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5000/admin/ongoingServices', {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })
        OngoingServices.value = response.data
    } catch (err) {
        console.error('Failed to fetch ongoing services:', err)
    }
}

onMounted(() => {
    fetchOngoingServices()
})

// Search bar
const search = ref('')
const filteredServices = computed(() => {
    return search.value
        ? OngoingServices.value.filter(service =>
            service.serviceName.toLowerCase().includes(search.value.toLowerCase())
        )
        : OngoingServices.value
})

</script>

<template>
    <div>
        <div class="container">
            <div class="searchBar">
                <input type="text" class="search" placeholder="Search by service name" v-model="search" />
                <p class="searchBtn" v-html="Search"></p>
            </div>
            <table v-if="filteredServices.length > 0">
                <thead>
                    <tr class="headrow">
                        <th>S.No</th>
                        <th>serviceName</th>
                        <th>Professional</th>
                        <th>Customer</th>
                        <th>P - Pin Code</th>
                        <th>C - Pin Code</th>
                        <th>Status</th>
                        <th>Request Date</th>
                        <th>Completion Date</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(service, index) in filteredServices" :key="service.BookingId">
                        <td>{{ index + 1 }}</td>
                        <td>{{ service.serviceName }}</td>
                        <td>{{ service.professionalName }}</td>
                        <td>{{ service.customerName }}</td>
                        <td>{{ service.professionalPincode }}</td>
                        <td>{{ service.customerPincode }}</td>

                        <td v-if="service.completionDate">Completed</td>
                        <td v-else-if="service.professionalStatus=='accepted'">Assigned</td>
                        <td v-else-if="service.professionalStatus=='rejected'">Rejected</td>
                        <td v-else>Pending...</td>

                        <td>{{ new Date(service.requestDate).toISOString().slice(0, 10) }}</td>

                        <td v-if="service.completionDate">{{ new Date(service.completionDate).toISOString().slice(0, 10) }}</td>
                        <td v-else>...</td>
                    </tr>
                </tbody>
            </table>
            <img v-else class="emptyMessage" src="@/assets/images/empty-box.png" alt="">
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
    overflow: auto;
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
    text-align: center;
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

.searchBtn {
    height: 35px;
    width: 35px;
    cursor: pointer;
}

button {
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
