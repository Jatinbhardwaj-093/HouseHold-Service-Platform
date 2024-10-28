<script setup>
import Cross from '@/assets/svg/Cross.svg?raw'
import { ref, watch } from 'vue'
import axios from 'axios'

const token = localStorage.getItem('token')

const emit = defineEmits(['closeProfileEditModal'])

const closeProfileEditModal = () => {
    emit('closeProfileEditModal')
}

const { profileData } = defineProps({
    profileData: Object
})

const customer = ref({
    email: '',
    username: '',
    password: '',
    contact: null,
    pincode: null,
    address: ''
})

watch(
    () => profileData,
    (newVal) => {
        if (newVal) {
            customer.value = {
                email: newVal.email,
                username: newVal.username,
                password: newVal.password,
                contact: newVal.contact,
                pincode: newVal.pincode,
                address: newVal.address
            }
        }
    },
    { immediate: true }
)

const submitForm = async () => {
    try {
        const response = await axios.put('http://127.0.0.1:5000/customer/profile', customer.value, {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })
        console.log(response.data)
        closeProfileEditModal()
    } catch (error) {
        console.error('Error occurred:', error.response ? error.response.data : error.message)
    }
}
</script>


<template>
    <div class="editModal-content">
        <form class="form" @submit.prevent="submitForm">
            <p class="profilePic"></p>
            <label for="email" class="label">Email Id</label>
            <input type="email" class="email" v-model="customer.email" id="email" />
            <label for="username" class="label">Username</label>
            <input type="text" class="username" v-model="customer.username" id="username" />
            <label for="password" class="label">Password</label>
            <input type="password" class="password" v-model="customer.password" id="password" />
            <label for="contact" class="label">Contact</label>
            <input type="number" class="contact" v-model="customer.contact" id="contact" />
            <label for="pincode" class="label">Pincode</label>
            <input type="number" class="pincode" v-model="customer.pincode" id="pincode" />
            <label for="address" class="label">Address</label>
            <textarea v-model="customer.address" class="address" cols="10" rows="3" id="address"></textarea>
            <button type="submit" class="btn">Edit</button>
        </form>
        <div v-html="Cross" class="cross" @click="closeProfileEditModal"></div>
    </div>
</template>

<style scoped>
.editModal-content {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 30rem;
    padding: 2.5rem;
    background-color: #161414;
    border-radius: 1rem;
    box-shadow: 2px 5px 20px rgba(202, 122, 82, 0.6);
    z-index: 10000;
}

.form {
    display: grid;
    grid-template-columns: 1fr 5fr;
    grid-template-areas:
        "profilePic profilePic"
        "label1 input1"
        "label2 input2"
        "label3 input3"
        "label4 input4"
        "label5 input5"
        "label6 input6"
        "btn btn";
    gap: 0.5rem;
}

.profilePic {
    grid-area: profilePic;
    justify-self: center;
    align-self: center;
    width: 6rem;
    height: 6rem;
    border-radius: 50%;
    margin-bottom: 1.5rem;
    background-color: #d9d9d9;
    box-shadow: 2px 5px 20px rgba(236, 103, 14, 0.6);
}

.label:nth-child(2) { grid-area: label1; }
.email { grid-area: input1; }
.label:nth-child(4) { grid-area: label2; }
.username { grid-area: input2; }
.label:nth-child(6) { grid-area: label3; }
.password { grid-area: input3; }
.label:nth-child(8) { grid-area: label4; }
.contact { grid-area: input4; }
.label:nth-child(10) { grid-area: label5; }
.pincode { grid-area: input5; }
.label:nth-child(12) { grid-area: label6; }
.address { grid-area: input6; }

.cross {
    position: absolute;
    top: 10px;
    right: 10px;
    height: 40px;
    width: 40px;
    cursor: pointer;
}

.form label {
    color: bisque;
    font-size: 1.2rem;
    font-weight: bolder;
    font-style: italic;
    margin-right: 0.5rem;
}

.form input,
.form textarea {
    margin: auto;
    height: 2rem;
    outline: none;
    color: white;
    border-radius: 0.5rem;
    border: none;
    padding: 0.5rem;
    padding-left: 1.2rem;
    font-size: 1rem;
    font-weight: bolder;
    font-style: italic;
    background-color: rgba(255, 255, 255, 0.2);
    box-shadow: 6px 8px 25px rgba(0, 0, 0, 0.8);
}

.form input[type="number"] {
    appearance: textfield;
}

.form textarea {
    height: 4rem;
    resize: none;
    width: 65%;
}

.btn {
    grid-area: btn;
    justify-self: center;
    margin-top: 1rem;
    width: 5rem;
    height: 1.7rem;
    border-radius: 0.3rem;
    border: none;
    background: #ff5c01;
    box-shadow: 2px 5px 20px rgba(0, 0, 0, 0.6);
    color: #fff;
    font-size: 1rem;
    font-weight: bolder;
    cursor: pointer;
}

</style>
