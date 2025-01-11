<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import Search from '@/assets/svg/Search.svg?raw'

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

onMounted(() => {
    fetchCustomers()
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
const filteredCustomers = computed(() => {
    return search.value
        ? customers.value.filter((customer) =>
              customer.username.toLowerCase().includes(search.value.toLowerCase())
          )
        : customers.value
})

//Notification
import NotificationModal from '../NotificationModal.vue'

const notifications = ref([])

const addNotification = (message, duration) => {
    notifications.value.push({ message, duration })
}
</script>

<template>
    <div>
        <div class="container">
            <div class="searchBar">
                <input
                    type="text"
                    class="search"
                    placeholder="Search by customer name"
                    v-model="search"
                />
                <div class="searchBtn" v-html="Search"></div>
            </div>
            <div v-if="filteredCustomers.length > 0" class="card-container">
                <div v-for="customer in filteredCustomers" :key="customer.id" class="card">
                    <div class="card-header">
                        <p class="username">{{ customer.username }}</p>
                    </div>
                    <div class="card-body">
                        <p><strong>Address:</strong> {{ customer.address }}</p>
                        <p><strong>Email:</strong> {{ customer.email }}</p>
                        <p><strong>Contact:</strong> {{ customer.contact }}</p>
                        <p><strong>Pincode:</strong> {{ customer.pincode }}</p>
                        <p>
                            <strong>Status:</strong>
                            <span v-if="customer.flag == 'yes'">Flagged</span>
                            <span v-else>OK</span>
                        </p>
                    </div>
                    <div class="card-footer">
                        <div class="footer-divider">
                            <div>
                                <button @click="flagCustomer(customer)">
                                    {{ customer.flag == 'no' ? 'Flag' : 'Unflag' }}
                                </button>
                            </div>
                            <div>
                                <button @click="deleteCustomer(customer.id, customer.username)">
                                    Delete
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <img
                v-else
                class="emptyMessage"
                src="@/assets/images/empty-box.png"
                alt="No customers found"
            />
        </div>
        <NotificationModal
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

.searchBtn {
    height: 30px;
    width: 30px;
    cursor: pointer;
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
    align-items: center;
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

.emptyMessage {
    height: 250px;
    width: 250px;
    display: block;
    margin: auto;
    margin-top: 2rem;
}
</style>
