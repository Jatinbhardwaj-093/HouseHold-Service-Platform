<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import Search from '@/assets/svg/Search.svg?raw'
import MenuDot from '@/assets/svg/MenuDot.svg?raw'
import NoImg from '@/assets/svg/NoImg.svg?raw'
import Cross from '@/assets/svg/Cross.svg?raw'
import Flag from '@/assets/svg/Flag.svg?raw'
import UnFlag from '@/assets/svg/UnFlag.svg?raw'
import Filter from '@/assets/svg/Filter.svg?raw'
import Eye from '@/assets/svg/Eye.svg?raw'
import Dustbin from '@/assets/svg/Dustbin.svg?raw'

const detailsRef = ref([])
const token = localStorage.getItem('adminToken')

// Fetch customers
const customers = ref([])
const fetchCustomers = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5000/admin/customers', {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })
        customers.value = response.data
    } catch (err) {
        console.error('Failed to fetch customers:', err)
    }
}

// Add these new filter-related state variables
const filterType = ref('name')
const filterOptions = ['name', 'pincode']
const showFilterDropdown = ref(false)

// Modify the filteredCustomers computed property
const filteredCustomers = computed(() => {
    let result = customers.value

    if (search.value) {
        if (filterType.value === 'name') {
            result = result.filter((customer) =>
                customer.username.toLowerCase().includes(search.value.toLowerCase())
            )
        } else if (filterType.value === 'pincode') {
            result = result.filter((customer) => 
                customer.pincode.toString().startsWith(search.value)
            )
        }
    }

    return result
})

onMounted(() => {
    fetchCustomers()
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

// Flag customer and reload data
const flagCustomer = async (customer) => {
    try {
        await axios.put(
            `http://127.0.0.1:5000/admin/customer/${customer.id}/flag`,
            {},
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            }
        )
        if (customer.flag == 'no') {
            addNotification('Customer ' + customer.username + ' flagged successfully!', 3000)
        } else {
            addNotification('Customer ' + customer.username + ' unflagged successfully!', 3000)
        }

        await fetchCustomers()
    } catch (err) {
        console.error('Failed to flag customer:', err)
    }
}

// Delete customer and reload data
const deleteCustomer = async (customerId, customer_name) => {
    try {
        await axios.delete(`http://127.0.0.1:5000/admin/customer/${customerId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })
        await fetchCustomers()
        addNotification('Customer ' + customer_name + ' deleted successfully!', 3000)
    } catch (err) {
        addNotification('Failed to delete' + customer_name + '. Please try again.', 5000)
    }
}

// Search functionality
const search = ref('')

//Notification
import NotificationModal from '../NotificationModal.vue'

const notifications = ref([])

const addNotification = (message, duration) => {
    notifications.value.push({ message, duration })
}

const showSidebar = ref(false)
const selectedCustomer = ref(null)
const isClosing = ref(false)

const viewCustomer = (customer) => {
    selectedCustomer.value = customer
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

const toggleMenu = (customerId) => {
    showMenu.value = showMenu.value === customerId ? null : customerId
}
</script>

<template>
    <div class="main-container">
        <transition name="sidebar">
            <div class="sidebar" v-if="showSidebar && !isClosing">
                <p v-html="Cross" @click="closeSidebar" style="width: 30px; height: 30px"></p>
                <div v-if="selectedCustomer">
                    <img
                        v-if="selectedCustomer.image_name"
                        :src="
                            'http://127.0.0.1:5000/static/customers_imgs/' +
                            selectedCustomer.image_name
                        "
                        alt="Customer Image"
                        class="imagePreview sidebar-detail"
                    />
                    <p class="sidebar-detail" v-else v-html="NoImg"></p>
                    <p class="sidebar-detail">
                        <strong class="sidebar-detail-tags">Name:</strong>
                        {{ selectedCustomer.username }}
                    </p>
                    <p class="sidebar-detail">
                        <strong class="sidebar-detail-tags">Email:</strong>
                        {{ selectedCustomer.email }}
                    </p>
                    <p class="sidebar-detail">
                        <strong class="sidebar-detail-tags">Phone:</strong>
                        {{ selectedCustomer.phone }}
                    </p>
                    <p class="sidebar-detail">
                        <strong class="sidebar-detail-tags">Address:</strong>
                        {{ selectedCustomer.address }}
                    </p>
                    <p class="sidebar-detail">
                        <strong class="sidebar-detail-tags">Pincode:</strong>
                        {{ selectedCustomer.pincode }}
                    </p>
                    <p class="sidebar-detail">
                        <strong class="sidebar-detail-tags">Status:</strong>
                        <span v-if="selectedCustomer.verify == 'no'">Not Verified</span>
                        <span v-else-if="selectedCustomer.flag == 'yes'">Flagged</span>
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
                            v-model="search"
                        />
                        <p class="searchBtn" v-html="Search"></p>
                    </div>
                    <div class="filter-container">
                        <p v-html="Filter" class="filterBtn"></p>
                        <button class="filter-btn" @click="showFilterDropdown = !showFilterDropdown">
                            {{ filterType.charAt(0).toUpperCase() + filterType.slice(1) }}
                        </button>
                        <ul v-if="showFilterDropdown" class="filter-dropdown">
                            <li
                                v-for="option in filterOptions"
                                :key="option"
                                @click="
                                    filterType = option;
                                    showFilterDropdown = false
                                "
                            >
                                {{ option.charAt(0).toUpperCase() + option.slice(1) }}
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <div v-if="filteredCustomers.length > 0" class="card-container">
                <div v-for="customer in filteredCustomers" :key="customer.id" class="card">
                    <div class="image-holder">
                        <img
                            v-if="customer.image_name"
                            :src="
                                'http://127.0.0.1:5000/static/customers_imgs/' + customer.image_name
                            "
                            alt="Customer Image"
                            class="imagePreview"
                        />
                        <p v-else v-html="NoImg" class="noImagePreview"></p>
                    </div>
                    <div class="divider"></div>
                    <div class="card-body">
                        <div class="verified">
                            <p
                                v-if="customer.flag == 'yes'"
                                v-html="Flag"
                                style="height: 20px; width: 20px"
                            ></p>
                            <p class="username">{{ customer.username }}</p>
                        </div>
                        <div class="menu-button">
                            <button @click="toggleMenu(customer.id)" class="menu-btn">
                                <p
                                    v-html="MenuDot"
                                    style="
                                        height: 80%;
                                        width: 80%;
                                        margin-left: 3px;
                                        margin-bottom: 5px;
                                    "
                                ></p>
                            </button>
                            <ul v-if="showMenu === customer.id" class="menu-list">
                                <li @click="viewCustomer(customer)">
                                    <span v-html="Eye" class="menu-list-icon"></span>
                                    <span>View</span>
                                </li>
                                <li @click="flagCustomer(customer)">
                                    <span v-if="customer.flag == 'no'" v-html="Flag" class="menu-list-icon"></span>
                                    <span v-else v-html="UnFlag" class="menu-list-icon"></span>
                                    <span>
                                        {{ customer.flag == 'no' ? 'Flag' : 'Unflag' }}
                                    </span>
                                </li>
                                <li @click="deleteCustomer(customer.id, customer.username)">
                                    <span v-html="Dustbin" class="menu-list-icon"></span>
                                    <span>Delete</span>
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
                alt="No customers found"
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
    gap: 0.5rem;
}

.container {
    width: 95%;
    margin: auto;
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

.searchBar {
    display: flex;
    justify-content: start;
    background-color: black;
    box-shadow: 5px 5px 10px rgb(0, 0, 0);
    border-radius: 0.5rem;
    padding: 0.5rem;
    width: 650px;
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
    cursor: pointer;
}

.filterBtn {
    height: 30px;
    width: 30px;
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
    right: 120%;
    bottom: 0;
    background: #2c2b2b;
    list-style: none;
    padding: 0;
    margin: 0;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.6);
    z-index: 100;
}

.menu-list li {
    padding: 0.5rem 1rem;
    display: flex;
    align-items: center;
    justify-content: start;
    gap: 5px;
    cursor: pointer;
    color: #f5f5dc;
}

.menu-list-icon {
    height: 20px;
    width: 20px;
}

.menu-list li:hover {
    background: #3c3c3c;
}

.sidebar {
    width: 25%;
    height: 85vh;
    background: #2c2b2b;
    border-radius: 1rem;
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.6);
    padding: 1rem;
    overflow-y: auto;
    color: #f5f5dc;
    transition:
        transform 0.5s ease-in-out,
        opacity 0.5s ease-in-out;
}

/* Animation for the sidebar opening */
.sidebar-enter-active,
.sidebar-leave-active {
    transition:
        transform 0.5s ease-in-out,
        opacity 0.5s ease-in-out;
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

.sidebar-detail {
    margin-bottom: 0.5rem;
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

.search-section {
    display: flex;
    gap: 1rem;
}

.filter-container {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #6b6a6a;
    padding: .5rem;
    border-radius: .5rem;
}
.filter-btn {
    background-color: inherit;
    border: none;
    outline: none;
    color: #f5f5dc;
    cursor: pointer;
    font-size: 1.25rem;
    border-left: #5e5d5d 2px solid;
    margin-left: .5rem;
    padding-left: .5rem;
}

.filter-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    background: #2c2b2b;
    border-radius: 0.5rem;
    list-style: none;
    padding: 0;
    width: 100%;
    margin: 0.5rem 0; /* Changed from margin: 0.5rem auto */
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
</style>
