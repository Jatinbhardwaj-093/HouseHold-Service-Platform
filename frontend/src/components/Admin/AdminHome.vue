<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import Modal from './ServiceCreateModel.vue';
import ServiceModal from './ServiceDetailModel.vue';
import EditModal from './ServiceEditModel.vue';
import Search from '@/assets/svg/Search.svg?raw';
import MenuDot from '@/assets/svg/MenuDot.svg?raw';
import NoImg from '@/assets/svg/NoImg.svg?raw';

// State management
const showModal = ref(false);              // For the "Create New" modal
const showServiceModal = ref(false);       // For the "View Service" modal
const showEditModal = ref(false);          // For the "Edit Service" modal
const servicesData = ref([]);              // List of all services fetched from backend
const selectedService = ref(null);         // Service data for viewing in detail modal
const editServiceData = ref({              // Pre-filled data for the edit service modal
    service_name: '',
    description: '',
    price: '',
    service_id: null,
    image: null
});

const error = ref(null);

// Fetch all services
onMounted(async () => {
    const token = localStorage.getItem('token');
    const userRole = localStorage.getItem('user_role');

    if (!token || userRole !== 'admin') {
        window.location.href = '/';
    } else {
        await fetchServices();  
    }
});

//Serch service by name
const searchServiceName = ref('');

const searchServices = () => {
    searchServiceName.value = searchServiceName.value.toLowerCase(); 
};

const filteredServicesData = computed(() => {
    if (searchServiceName.value) {
        return servicesData.value.filter(service =>
            service.name.toLowerCase()==searchServiceName.value
        );
    }
    return servicesData.value;  
});

// View service details
const viewService = async (serviceId) => {
    const token = localStorage.getItem('token');
    try {
        const response = await axios.get(`http://127.0.0.1:5000/admin/service/${serviceId}`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        selectedService.value = response.data;  
        showServiceModal.value = true;         
    } catch (err) {
        error.value = 'Error: ' + (err.response ? err.response.data : err.message);
    }
};

// Edit service
const openEditModal = (service) => {
    editServiceData.value = {
        service_name: service.name,
        description: service.description,
        price: service.price,
        service_id: service.id,   
        ImageFilePath: service.image
    };
    showEditModal.value = true;
};

// Delete service 
const deleteService = async (serviceId) => {
    const token = localStorage.getItem('token');
    try {
        await axios.delete(`http://127.0.0.1:5000/admin/service/${serviceId}`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        alert('Service deleted successfully');
        await fetchServices(); 
    } catch (err) {
        error.value = 'Error: ' + (err.response ? err.response.data : err.message);
    }
};

// Refresh servicesData after edit or delete
const fetchServices = async () => {
    const token = localStorage.getItem('token');
    try {
        const response = await axios.get('http://127.0.0.1:5000/admin/', {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });
        servicesData.value = response.data; 
    } catch (error) {
        console.error('Failed to fetch services:', error);
    }
};

</script>

<template>
    <div class="container">
        <div class="top">
            <div class="searchBar">
                <input type="text" class="search" placeholder="Service Name" v-model="searchServiceName">
                <div class="searchBtn" v-html="Search" @click="searchServices"></div>
            </div>
            <div class="createNewBtn" @click="showModal = true">Create New +</div>
        </div>

        <div class="blocks">
            <div class="block" v-for="service in filteredServicesData" :key="service.id">
                <img v-if="service.image" :src="service.image.filepath"/>
                <div v-else class="serviceImgHolder"><p v-html="NoImg"></p></div>
                <div class="serviceName">
                    <p>{{ service.name }}</p>
                    <details>
                        <summary>
                            <p class="menuDot" v-html="MenuDot"></p>
                        </summary>
                        <ul>
                            <li @click="viewService(service.id)">View</li>
                            <li @click="openEditModal(service)">Edit</li>
                            <li @click="deleteService(service.id)">Delete</li>
                        </ul>
                    </details>
                </div>
            </div>
        </div>

        <!-- Modal Components -->
        <Modal :showModal="showModal" @closeModal="showModal = false" />
        <ServiceModal :showServiceModal="showServiceModal" :serviceData="selectedService" @closeServiceModal="showServiceModal = false" />
        <EditModal :showEditModal="showEditModal" :serviceToEdit="editServiceData" @closeEditModal="showEditModal = false" />
    </div>
</template>


<style scoped>
.container {
    overflow: auto;
    scrollbar-width: thin;
    width: 95%;
    height: 80vh;
    margin: auto;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.6);
    background-color: #3c3c3c;
}

.top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

.searchBar {
    display: flex;
    justify-content: start;
    background-color: black;
    box-shadow: 5px 5px 10px rgb(42, 42, 42);
    border-radius: 0.5rem;
    padding: 0.5rem;
    width: max(70%);
}

.searchBtn {
    width: 30px;
    height: 30px;
    cursor: pointer;
    vertical-align: middle;
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

.createNewBtn {
    width: 10rem;
    cursor: pointer;
    text-align: center;
    font-size: 1.25rem;
    font-weight: bold;
    color: white;
    border-radius: 0.5rem;
    padding: 0.6rem;
    background-image: linear-gradient(to right, #e95401, #832f01);
    overflow: hidden;
}

.blocks {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 1rem;
}

.block {
    position: relative;
    background-color: black;
    width: 120px;
    height: 120px;
    border-radius: 0.5rem;
    box-shadow: 2px 5px 20px rgba(0, 0, 0, 0.6);
    padding: 5px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 5px;
}

.serviceName {
    display: flex;
    justify-content: center;
    align-items: end;
    gap: 10px;
    width: 100%;
    text-align: center;
    color: #fff;
    font-size: 1rem;
    font-weight: bolder;
}

img {
    width: 50px;
    height: 50px;
    object-fit: cover;
    border-radius: 0.25rem;
}

.serviceImgHolder {
    width: 90px;
    height: 70px;
    background-color: antiquewhite;
    border-radius: 0.25rem;
}

.serviceImgHolder p {
    width: 70px;
    height: 40px;
    margin: auto;
}

details summary .menuDot {
    background-color: #2c2b2b;
    padding: 2px;
    border-radius: 2px;
    width: 20px;
    height: 20px;
}

details summary .menuDot:hover {
    outline: #832f01 2px solid;
}

details {
    position: relative;
}

details ul {
    position: absolute;
    top: -200%;
    left: 170%;
    list-style: none;
    background-color: #4f4f4f;
    color: white;
    border-radius: 0.2rem;
    z-index: 2;
    padding-left: 0px;
}

details ul li {
    text-align: start;
    cursor: pointer;
    padding: 2px 10px;
}

details ul li:hover {
    background-color: #424242;
    border-radius: 0.2rem;
    color: white;
}

details summary {
    list-style-type: none;
}

details[open] summary .menuDot {
    background-color: #832f01;
}
</style>
