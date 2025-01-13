<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import Search from '@/assets/svg/Search.svg?raw'
import Download from '@/assets/svg/Download.svg?raw'
import Filter from '@/assets/svg/Filter.svg?raw'
import Calendar from '@/assets/svg/Calendar.svg?raw' // Add this new import

const token = localStorage.getItem('adminToken')
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
const showFilter = ref(false)
const filterBy = ref('serviceName') // 'serviceName', 'date', 'customerPincode', or 'professionalPincode'
const dateRange = ref({
    start: '',
    end: ''
})
const showDateFilter = ref(false) // Add this new ref

const searchPlaceholder = computed(() => {
    switch (filterBy.value) {
        case 'serviceName':
            return 'Search by service name'
        case 'customerPincode':
            return 'Search by customer pincode'
        case 'professionalPincode':
            return 'Search by professional pincode'
        default:
            return 'Search'
    }
})

const filteredServices = computed(() => {
    let filtered = OngoingServices.value

    if (search.value) {
        if (filterBy.value === 'serviceName') {
            filtered = filtered.filter((service) =>
                service.serviceName.toLowerCase().includes(search.value.toLowerCase())
            )
        } else if (filterBy.value === 'customerPincode') {
            filtered = filtered.filter((service) =>
                service.customerPincode.toLowerCase().includes(search.value.toLowerCase())
            )
        } else if (filterBy.value === 'professionalPincode') {
            filtered = filtered.filter((service) =>
                service.professionalPincode.toLowerCase().includes(search.value.toLowerCase())
            )
        }
    }

    if (filterBy.value === 'date' && dateRange.value.start && dateRange.value.end) {
        filtered = filtered.filter((service) => {
            const serviceDate = new Date(service.requestDate).getTime()
            const start = new Date(dateRange.value.start).getTime()
            const end = new Date(dateRange.value.end).getTime()
            return serviceDate >= start && serviceDate <= end
        })
    }

    return filtered
})

// Add click-outside directive
const vClickOutside = {
    mounted(el, binding) {
        el._clickOutside = (event) => {
            // Don't trigger if clicking inside the element or its children
            if (!el.contains(event.target)) {
                binding.value(event)
            }
        }
        document.addEventListener('click', el._clickOutside, true)
    },
    unmounted(el) {
        document.removeEventListener('click', el._clickOutside, true)
    }
}

const toggleFilter = (event) => {
    event.stopPropagation()
    showFilter.value = !showFilter.value
    showDateFilter.value = false
    filterBy.value = 'serviceName' // Set filterBy to 'serviceName' when opening filter
}

const toggleDateFilter = (event) => {
    event.stopPropagation()
    showDateFilter.value = !showDateFilter.value
    showFilter.value = false
    filterBy.value = 'date' // Set filterBy to 'date' when opening date filter
}

const closeDropdowns = () => {
    showFilter.value = false
    showDateFilter.value = false
}

// Pagination
const currentPage = ref(1)
const itemsPerPage = 15
const paginatedServices = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage
    const end = start + itemsPerPage
    return filteredServices.value.slice(start, end)
})

const totalPages = computed(() => {
    return Math.ceil(filteredServices.value.length / itemsPerPage)
})

const nextPage = () => {
    if (currentPage.value < totalPages.value) {
        currentPage.value++
    }
}

const prevPage = () => {
    if (currentPage.value > 1) {
        currentPage.value--
    }
}

// Download CSV
const errorMessage = ref('')
const downloadCsv = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5000/admin/download-csv', {
            headers: {
                Authorization: `Bearer ${token}`
            },
            responseType: 'blob'
        })
        const blob = new Blob([response.data], { type: 'text/csv' })
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = 'completed_services.csv'
        link.click()
    } catch (error) {
        if (error.response && error.response.data.error) {
            errorMessage.value = error.response.data.error
        } else {
            errorMessage.value = 'An error occurred while downloading the file.'
        }
        console.error('Error downloading CSV:', error)
    }
}

// Modify clearDateFilter to also close the dropdown
const clearDateFilter = () => {
    dateRange.value = {
        start: '',
        end: ''
    }
    showDateFilter.value = false
    filterBy.value = 'serviceName'
}

const clearFilters = () => {
    search.value = ''
    showFilter.value = false
    showDateFilter.value = false
    filterBy.value = 'serviceName'
    dateRange.value = {
        start: '',
        end: ''
    }
}
</script>

<template>
    <div @click="closeDropdowns">
        <div class="container" @click.stop>
            <div class="header">
                <div class="searchContainer">
                    <div class="searchBar">
                        <input type="text" class="searchInput" :placeholder="searchPlaceholder" v-model="search" />
                        <p class="searchBtn" v-html="Search"></p>
                    </div>
                    <div class="filterButtons">
                        <div class="filterContainer">
                            <button class="filterBtn" @click.stop="toggleFilter" v-html="Filter"></button>
                            <div class="filterDropdown" v-if="showFilter" @click.stop>
                                <div class="filterOptions">
                                    <label>
                                        <input type="radio" v-model="filterBy" value="serviceName">
                                        Service Name
                                    </label>
                                    <label>
                                        <input type="radio" v-model="filterBy" value="customerPincode">
                                        Customer Pincode
                                    </label>
                                    <label>
                                        <input type="radio" v-model="filterBy" value="professionalPincode">
                                        Professional Pincode
                                    </label>
                                </div>
                                <button class="clearBtn" @click="clearFilters">Clear Filter</button>
                            </div>
                        </div>
                        <div class="dateFilterContainer">
                            <button class="filterBtn dateFilterBtn" @click.stop="toggleDateFilter" v-html="Calendar"></button>
                            <div class="dateFilterDropdown" v-if="showDateFilter" @click.stop>
                                <div class="dateInputs">
                                    <div class="dateField">
                                        <label>Start Date:</label>
                                        <input type="date" v-model="dateRange.start">
                                    </div>
                                    <div class="dateField">
                                        <label>End Date:</label>
                                        <input type="date" v-model="dateRange.end">
                                    </div>
                                </div>
                                <button class="clearBtn" @click="clearDateFilter">Clear Dates</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="exportCSV">
                    <button @click="downloadCsv" class="btn">
                        <span>Export CSV</span>
                        <p class="downloadBtn" v-html="Download"></p>
                    </button>
                </div>
            </div>
            <div class="content">
                <table v-if="paginatedServices.length > 0">
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
                        <tr v-for="(service, index) in paginatedServices" :key="service.BookingId">
                            <td>{{ (currentPage - 1) * itemsPerPage + index + 1 }}</td>
                            <td>{{ service.serviceName }}</td>
                            <td>{{ service.professionalName }}</td>
                            <td>{{ service.customerName }}</td>
                            <td>{{ service.professionalPincode }}</td>
                            <td>{{ service.customerPincode }}</td>

                            <td v-if="service.completionDate">Completed</td>
                            <td v-else-if="service.professionalStatus == 'accepted'">Assigned</td>
                            <td v-else-if="service.professionalStatus == 'rejected'">Rejected</td>
                            <td v-else>Pending...</td>

                            <td>{{ new Date(service.requestDate).toISOString().slice(0, 10) }}</td>

                            <td v-if="service.completionDate">
                                {{ new Date(service.completionDate).toISOString().slice(0, 10) }}
                            </td>
                            <td v-else>...</td>
                        </tr>
                    </tbody>
                </table>
                <div v-else class="emptyMessage">
                    <img src="@/assets/images/empty-box.png" alt="No ongoing services found" />
                </div>
            </div>
            <div class="pagination" v-if="totalPages > 1">
                <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
                <span>Page {{ currentPage }} of {{ totalPages }}</span>
                <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
            </div>
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
    overflow: hidden;
    scrollbar-width: thin;
    display: flex;
    flex-direction: column;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.searchContainer {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2rem;
}

.filterButtons {
    display: flex;
    gap: 1rem;
    align-items: center;
}

.filterContainer {
    position: relative;
}

.filterBtn {
    background-color: #6b6b6b;
    border: none;
    border-radius: 0.5rem;
    padding: 0.7rem;
    height: 53px;
    width: 53px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

.filterBtn :deep(svg) {
    height: 100%;
    width: 100%;
    fill: white;
}

.filterDropdown {
    position: absolute;
    top: 100%;
    right: 0;
    background-color: #2f2c2c;
    border-radius: 0.5rem;
    padding: 1rem;
    margin-top: 0.5rem;
    min-width: 150px;
    box-shadow: 2px 2px 5px rgba(0, 0, 0);
    z-index: 1000;
}

.filterOptions {
    display: flex;
    flex-direction: column;
    align-items: start;
    justify-content: center;
    gap: 0.5rem;
    color: #f5f5dc;
}

.filterOptions label {
    display: flex;
    align-items: center;
    justify-content: start;
    gap: 0.5rem;
    align-items: center;

}

.dateInputs {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-top: 0.5rem;
}

.dateInputs input {
    padding: 0.5rem;
    border-radius: 0.3rem;
    background-color: #3c3c3c;
    border: 1px solid #fe772e;
    color: #f5f5dc;
    width: 100%;
    font-size: 1rem;
}

.clearBtn {
    margin-top: 1rem;
    background-color: #fe772e;
    color: white;
    border: none;
    border-radius: 0.3rem;
    padding: 0.5rem;
    width: 100%;
    cursor: pointer;
}

.searchBar {
    display: flex;
    justify-content: start;
    background-color: black;
    box-shadow: 5px 5px 10px rgb(0, 0, 0);
    border-radius: 0.5rem;
    padding: 0.5rem;
    margin-right: 1rem;
    width: 550px;
}

.searchInput {
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

.content {
    flex: 1;
    overflow: auto;
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

.searchBtn,
.downloadBtn {
    height: 35px;
    width: 35px;
    cursor: pointer;
}

.exportCSV {
    margin: 2rem;
}

.btn {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    width: 12rem;
    font-size: 1.25rem;
    background-color: hsla(201, 87%, 35%, 0.85);
    color: #f5f5dc;
    border: none;
    border-radius: 0.5rem;
    padding: 0.5rem;
    cursor: pointer;
}

.emptyMessage {
    height: 250px;
    width: 250px;
    display: block;
    margin: auto;
    margin-top: 2rem;
}

.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    margin: 1rem 0;
}

.pagination button {
    background-color: #1e1e1e;
    color: #fe772e;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 0.2rem;
    cursor: pointer;
}

.pagination span {
    color: #f5f5dc;
}

.dateFilterContainer {
    position: relative;
}

.dateFilterBtn {
    background-color: #6b6b6b;
}

.dateFilterDropdown {
    position: absolute;
    top: 100%;
    right: 0;
    background-color: #2f2c2c;
    border-radius: 0.5rem;
    padding: 1rem;
    margin-top: 0.5rem;
    min-width: 250px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    z-index: 1000;
}

.dateInputs {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

/* Remove the dateRangeContainer styles as we don't need them anymore */
.dateRangeContainer {
    display: none;
}

.searchContainer {
    margin-top: 1rem;
}
</style>
