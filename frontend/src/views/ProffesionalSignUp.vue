<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import axios from 'axios';
import ServiceChoiceModel from '@/components/Professional/ServiceChoiceModel.vue';

const formData = ref({
    email: '',
    username: '',
    password: '',
    serviceType: '',
    experience: null,
    contact: null,
    pincode: null
});

const submitForm = async () => {
    try {
        const response = await axios.post(
            'http://127.0.0.1:5000/professional/signup',
            formData.value,
            {
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        );
        console.log(response.data);
        alert('Professional created successfully');
        window.location.href = '/login';
    } catch (error) {
        console.error('Error occurred:', error.response ? error.response.data : error.message);
    }
};

// Professional Service Choice
const showModal = ref(false);
const Services = ref([]);
const modalRef = ref(null); // Reference to the modal element

const fetchServices = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5000/professional/services', {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        Services.value = response.data;
        console.log(Services.value);
    } catch (error) {
        console.error('Error occurred:', error.response ? error.response.data : error.message);
    }
};

const toggleModal = async () => {
    if (!Services.value.length) {
        await fetchServices();
    }
    showModal.value = !showModal.value;
};

const handleClickOutside = (event) => {
    if (modalRef.value?.$refs?.modalContainer && !modalRef.value.$refs.modalContainer.contains(event.target)) {
        showModal.value = false;
    }
};

onMounted(() => {
    document.addEventListener('click', handleClickOutside);
});

onBeforeUnmount(() => {
    document.removeEventListener('click', handleClickOutside);
});

const handleServiceSelect = (service) => {
    formData.value.serviceType = service.name;
    showModal.value = false;
};

</script>

<template>
    <div>
        <h1 class="heading">SERVICE PROFESSIONAL SIGNUP</h1>

        <form class="form" @submit.prevent="submitForm">
            <div>
                <input type="email" class="email" v-model="formData.email" placeholder="EMAIL" />
            </div>
            <div>
                <input
                    type="text"
                    class="username"
                    v-model="formData.username"
                    placeholder="USERNAME"
                />
            </div>
            <div>
                <input
                    type="password"
                    class="password"
                    v-model="formData.password"
                    placeholder="PASSWORD"
                />
            </div>
            <div>
                <input
                    type="text"
                    class="serviceType"
                    v-model="formData.serviceType"
                    placeholder="SERVICE TYPE"
                    @click="toggleModal"
                />
            </div>
            <div>
                <input
                    type="text"
                    class="experience"
                    v-model="formData.experience"
                    placeholder="EXPERIENCE"
                />
            </div>
            <div>
                <input
                    type="number"
                    class="contact"
                    v-model="formData.contact"
                    placeholder="CONTACT"
                />
            </div>
            <div>
                <input
                    type="number"
                    class="pincode"
                    v-model="formData.pincode"
                    placeholder="PINCODE"
                />
            </div>

            <button type="submit" class="btn">Register</button>
        </form>

        <div class="signInLine">
            <p>Already have an account?</p>
            <RouterLink :to="{ name: 'login' }" class="signInLink">Sign In</RouterLink>
        </div>

        <ServiceChoiceModel ref="modalRef" :ServiceData="Services" :showModal="showModal" class="Modal" @closeServiceChoiceModal="handleServiceSelect"/>
    </div>
</template>


<style scoped>
.Modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.serviceType {
    position: relative;
}

.heading {
    text-align: center;
    font-weight: bolder;
    font-size: 3.5rem;
    margin-top: 1rem;
    margin-bottom: 2rem;
    font-weight: bolder;
    font-style: italic;
    color: #ff5c01;
}
.form {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: auto;
    margin-bottom: 1rem;
}

.form input,
.form textarea {
    width: clamp(20rem, 25vw + 10rem, 50rem);
    height: 2.25rem;
    outline: none;
    color: white;
    border-radius: 1rem;
    border: none;
    padding: 1rem;
    padding-left: 2.25rem;
    font-size: 1.5rem;
    font-weight: bolder;
    font-style: italic;
    margin-bottom: 1rem;
    background-color: rgba(255, 255, 255, 0.2);
    box-shadow: 6px 8px 25px rgba(0, 0, 0, 0.8);
}

.form textarea {
    height: 4.5rem;
    padding-top: 0.5rem;
    font-size: 1rem;
}

input[type='number'] {
    appearance: textfield;
}

.form input:focus {
    border: 3px solid #ff5c01;
    transform: scale(1.05);
    transition: ease-in-out 0.5;
    background-color: rgba(255, 255, 255, 0.4);
}

.form input:focus::placeholder,
.form textarea:focus::placeholder {
    color: transparent;
}

.btn {
    width: 10rem;
    height: 3rem;
    border-radius: 1rem;
    border: none;
    background: #ff5c01;
    color: #fff;
    font-size: 1.5rem;
    font-weight: bolder;
    cursor: pointer;
}

.signInLine {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: auto;
    margin-bottom: 1rem;
}
.signInLine p {
    color: #ff5c01;
    font-size: 1.5rem;
    font-weight: bolder;
    font-style: italic;
    text-align: center;
}
.signInLine a {
    color: #6a94ff;
    font-size: 1.5rem;
    font-weight: bolder;
    text-align: center;
    text-decoration: none;
    margin-left: 10px;
}

.signInLine a:hover {
    text-decoration: underline;
    transform: scale(1.1);
    transition: ease-in-out 0.2s;
}
</style>
