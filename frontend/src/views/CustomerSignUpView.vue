<script setup> 
import axios from 'axios';
import { ref } from 'vue';


const formData = ref({
    email: '',
    username: '',
    password: '',
    contact: null,
    pincode: null,
    address: ''
});

const submitForm = async () => {
    try {
        const response = await axios.post('http://127.0.0.1:5000/customer/signup', formData.value, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        console.log(response.data);
        alert("Customer created successfully");
        window.location.href = '/login';
    } catch (error) {
        console.error('Error occurred:', error.response ? error.response.data : error.message);
    }
};


</script>

<template>
    <div>
        <h1 class="heading">CUSTOMER SIGNUP</h1>

    <form @submit.prevent="submitForm" class="form">
        <div>
            <input type="email" class="email" v-model="formData.email" placeholder="EMAIL ID">
        </div>
        <div>
            <input type="text" class="username" v-model="formData.username" placeholder="USERNAME">
        </div>
        <div>
            <input type="password" class="password" v-model="formData.password" placeholder="PASSWORD">
        </div>
        <div>
            <input type="number" class="contact" v-model="formData.contact" placeholder="CONTACT">
        </div>
        <div>
            <input type="number" class="pincode" v-model="formData.pincode" placeholder="PINCODE">
        </div>
        <div>
            <textarea v-model="formData.address" class="address" cols="10" rows="3" placeholder="ADDRESS....."></textarea>
        </div>
        <button type="submit" class="btn">Create</button>
    </form>

    <div class="signInLine">
        <p>Already have an account?</p>
        <RouterLink :to="{ name: 'login'}" class="signInLink">Sign In</RouterLink>
    </div>
    </div>
</template>

<style scoped>
.heading{
    text-align: center;
    font-weight: bolder;
    font-size: 3.5rem;
    margin-top: 1rem;
    margin-bottom: 2rem;
    font-weight: bolder;
    font-style: italic;
    color: #FF5C01;
}
.form{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: auto;
    margin-bottom: 1rem;
}

.form input, .form textarea{
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
    background-color: rgba(255, 255, 255, 0.2) ;     
    box-shadow: 6px 8px 25px rgba(0, 0, 0, 0.8) ;
}

.form textarea{
    height: 4.5rem;
    padding-top: 0.5rem;
    font-size: 1rem;
}

.pincode, .contact{
    appearance: textfield;
}

.form input:focus{
    border: 3px solid #FF5C01;
    transform: scale(1.05);
    transition: ease-in-out 0.5;
    background-color: rgba(255, 255, 255, 0.4);
}


.form input:focus::placeholder , .form textarea:focus::placeholder{
    color: transparent; 
}

.btn{
    width: 10rem;
    height: 3rem;
    border-radius: 1rem;
    border: none;
    background: #FF5C01;
    color: #fff;
    font-size: 1.5rem;
    font-weight: bolder;
    cursor: pointer;
}

.signInLine{
    display: flex;
    align-items: center;
    justify-content: center;
    margin: auto;
    margin-bottom: 1rem;
}
.signInLine p{
    color: #FF5C01;
    font-size: 1.5rem;
    font-weight: bolder;
    font-style: italic;
    text-align: center;

}
.signInLink{
    color: #6A94FF;
    font-size: 1.5rem;
    font-weight: bolder;
    text-align: center;
    text-decoration: none;
    margin-left: 10px;
    
}

.signInLink:hover{
    text-decoration: underline;
    transform: scale(1.1);
    transition: ease-in-out 0.2s;
}


</style>