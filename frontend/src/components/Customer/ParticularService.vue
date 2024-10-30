<script setup>
import Search from '@/assets/svg/Search.svg?raw';
import Home from '@/assets/svg/Home.svg?raw';
import Description from '@/assets/svg/Description.svg?raw';
import Review from '@/assets/svg/Review.svg?raw';

import { onMounted, ref } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';

const route = useRoute();
const serviceId = route.params.serviceId;
const token = localStorage.getItem('token');
console.log(serviceId);

const serviceData = ref({});

onMounted(async () => {
    try {
        const response = await axios.get(`http://127.0.0.1:5000/customer/service/${serviceId}`, {
            headers: {
                'Authorization': token ? `Bearer ${token}` : ''
            }
        });
        serviceData.value = response.data;
        console.log(response.data);
    } catch (error) {
        console.log('Error fetching service data:', error);
    }
});
</script>



<template>
    <div>
        <div class="homeButton" v-html="Home" @click="$router.push({ name: 'customer' })"></div>
        <p class="heading">{{ serviceData.name }}</p>

        <div class="pincodeSearch">
            <p>Pincode:</p>
            <input type="text" />
            <div class="searchBtn" v-html="Search"></div>
        </div>
        <div class="table">
            <table class="serviceTable">
                <thead>
                    <tr class="headrow">
                        <th>S.No</th>
                        <th>Professinal Name</th>
                        <th>Contact</th>
                        <th>Pincode</th>
                        <th>Rating</th>
                        <th>Price</th>
                        <th></th>
                        <th></th>
                        <th></th>
                    </tr>
                </thead>

                <tbody>
                    <tr>
                        <td>1</td>
                        <td>Rossevelt kumar</td>
                        <td>+91000000000</td>
                        <td>110082</td>
                        <td>4</td>
                        <td>₹10000</td>
                        <td><button class="bookingBtn" type="submit">Book</button></td>
                        <td>
                            <div class="svg" ><p v-html="Description"></p></div>
                            <span class="description">Description</span>
                        </td>
                        <td>
                            <div class="svg" ><p v-html="Review"></p></div>
                            <span class="review">Reviews</span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<style scoped>
.homeButton {
    position: absolute;
    top: 1.3rem;
    left: 1rem;
    width: 50px;
    height: 50px;
    text-align: center;
    background-image: linear-gradient(to bottom, #3c3c3c, #4f4f4f, #656565, #a1a1a1);
    cursor: pointer;
    padding: 0.4rem;
    border-radius: 0.5rem;
}

.homeButton svg {
    width: 30px;
    height: 30px;
    margin-top: 0.25rem;
    text-align: center;
}

.heading {
    width: clamp(20rem, 40vw + 10rem, 50rem);
    text-align: center;
    font-weight: bolder;
    font-size: 2.5rem;
    font-weight: bolder;
    color: white;
    background-image: linear-gradient(to right, #ff5c01, #993701);
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.6);
    border-radius: 0.5rem;
    padding: 0.2rem;
    margin: auto;
    margin-top: 1rem;
}

.pincodeSearch {
    display: flex;
    justify-content: end;
    align-items: center;
    margin: 1rem;
    gap: 0.5rem;
}

.pincodeSearch p {
    color: white;
    font-size: 1.1rem;
}
.pincodeSearch input {
    outline: none;
    color: white;
    border-radius: 0.5rem;
    border: none;
    padding: 0.2rem;
    padding-left: 1rem;
    font-size: 1.1rem;
    background-color: rgba(255, 255, 255, 0.2);
    box-shadow: 6px 8px 25px rgba(0, 0, 0, 0.8);
}

.searchBtn {
    height: 30px;
    width: 30px;
    cursor: pointer;
}

/* table */

.table {
    width: 95%;
    height: clamp(20rem, 50vh + 10rem, 50rem);
    margin: auto;
    margin-top: 1rem;
    padding: 2rem;
    border-radius: 1rem;
    overflow: hidden;
    box-shadow: 6px 8px 25px rgba(0, 0, 0, 0.8);
}

.serviceTable {
    width: 100%;
    border: none;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 0.5rem;
    margin: auto;
    overflow: hidden;
}

.serviceTable th,
td {
    padding: 4px;
    text-align: center;
    border-bottom: 1px solid #f5f5dc;
}
.serviceTable tr:last-child td {
    border-bottom: none;
}

.serviceTable tr:nth-child(even) {
    background-color: #2f2c2c;
}

.serviceTable .headrow {
    color: white;
    background-color: hsla(21, 100%, 50%, 0.85);
}

.serviceTable tr {
    color: #f5f5dc;
    background-color: #3c3c3c;
}

.serviceTable tr:last-child {
    border-bottom: none;
}

.serviceTable .bookingBtn {
    width: 4rem;
    color: white;
    background-color: #6a94ff;
    border-radius: 0.2rem;
    padding: 0.1rem;
    cursor: pointer;
    border: none;
}

.svg {
    height: 25px;
    width: 25px;
    cursor: pointer;
    margin-top: 6px;
}

.serviceTable td {
    position: relative;
}

.review,
.description {
    font-size: 0.8rem;
    visibility: hidden;
    opacity: 0;
    background-color: #030303;
    color: beige;
    text-align: center;
    border-radius: 4px;
    padding: 5px;
    position: absolute;
    bottom: 80%;
    left: -30%;
    transform: translateX(-50%);
    white-space: nowrap;
    z-index: 1;
    transition: opacity 0.3s ease-in-out;
}

td .svg:hover + .review,
td .svg:hover + .description {
    visibility: visible;
    opacity: 1;
}
</style>
