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
            addNotification('Customer ' + customer.username + ' flagged successfully!',3000)
        } else {
            addNotification('Customer ' + customer.username + ' unflagged successfully!',3000)
        }
        
        await fetchCustomers() 
    } catch (err) {
        console.error('Failed to flag customer:', err)
    }
}

// Delete customer and reload data
const deleteCustomer = async (customerId,customer_name) => {
    try {
        await axios.delete(`http://127.0.0.1:5000/admin/customer/${customerId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })
        await fetchCustomers() 
        addNotification('Customer ' + customer_name + ' deleted successfully!',3000)
    } catch (err) {
        addNotification('Failed to delete' + customer_name + '. Please try again.', 5000)
    }
}

// Search functionality
const search = ref('')
const filteredCustomers = computed(() => {
    return search.value
        ? customers.value.filter(customer => 
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
                <input type="text" class="search" placeholder="Search by customer name" v-model="search" />
                <div class="searchBtn" v-html="Search"></div>
            </div>
            <table v-if="filteredCustomers.length > 0">
                <thead>
                    <tr>
                        <th>S.No</th>
                        <th>Name</th>
                        <th>Address</th>
                        <th>Email</th>
                        <th>Contact</th>
                        <th>Pincode</th>
                        <th>Status</th>
                        <th style="width: 5%;"></th>
                        <th style="width: 8%;"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(customer, index) in filteredCustomers" :key="customer.id">
                        <td>{{ index + 1 }}</td>
                        <td>{{ customer.username }}</td>
                        <td>{{ customer.address }}</td>
                        <td>{{ customer.email }}</td>
                        <td>{{ customer.contact }}</td>
                        <td>{{ customer.pincode }}</td>
                        <td v-if="customer.flag == 'yes' ">Flagged</td>
                        <td v-else>OK</td>
                        <td>
                            <button @click="flagCustomer(customer)" v-if="customer.flag == 'no' ">Flag</button>
                            <button @click="flagCustomer(customer)" v-else>Unflag</button>
                        </td>
                        <td><button @click="deleteCustomer(customer.id, customer.username)">Delete</button></td>
                    </tr>
                </tbody>
            </table>
            <img v-else class="emptyMessage" src="@/assets/images/empty-box.png" alt="No customers found">
        </div>
        <NotificationModal 
        v-for="(notification, index) in notifications" 
        :key="index" 
        :message="notification.message" 
        :duration="notification.duration" 
        @close="notifications.splice(index, 1)"/>
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

thead tr {
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
    height: 30px;
    width: 30px;
    cursor: pointer;
}

button {
    background-color: #1e1e1e;
    color: #fe772e;
    padding: 3px;
    text-align: center;
    border: none;
    border-radius: 0.2rem;
    width: 4rem;
}

.emptyMessage{
    height: 250px;
    width: 250px;
    display: block;
    margin: auto;
    margin-top: 2rem;
}
</style>
