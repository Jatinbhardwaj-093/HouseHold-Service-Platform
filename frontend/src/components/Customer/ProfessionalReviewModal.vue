<script setup>
import Cross from '@/assets/svg/Cross.svg?raw'
import { ref,onMounted } from 'vue'
import axios from 'axios'

const { professionalId } = defineProps({
    professionalId: Number
})

const token = localStorage.getItem('token')
const Data = ref([])

onMounted(() => {
    axios
        .get(`http://127.0.0.1:5000/customer/professional/${professionalId}/reviews`, {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })
        .then((response) => {
            Data.value = response.data
        })
})
</script>

<template>
    <div>
        <div class="reviewContainer">
            <h1>Reviews</h1>
            <div @click="$emit('close')" class="cross">
                <p  v-html="Cross"></p>
            </div>
            <table v-if="Data.length > 0">
                <thead>
                    <tr class="headrow">
                        <th>Customer</th>
                        <th style="width: 70%">Review</th>
                        <th>Rating</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="review in Data" :key="review.id">
                        <td>{{ review.customerName }}</td>
                        <td>{{ review.review }}</td>
                        <td>{{ review.rating }}</td>
                    </tr>
                </tbody>
            </table>
            <img v-else class="emptyMessage" src="@/assets/images/empty-box.png" alt="">
        </div>
    </div>
</template>

<style scoped>
.reviewContainer {
    position: relative;
    width: 40vw;
    height: 60vh;
    padding: 1rem;
    gap: 1rem;
    background-color: #3c3c3c;
    border-radius: 1rem;
    box-shadow: 2px 5px 20px rgba(0, 0, 0, 0.6);
    overflow: auto;
    scrollbar-width: thin;
    margin: auto;
}

.cross {
    position: absolute;
    top: 5px;
    right: 5px;
    width: 50px;
    height: 50px;
    cursor: pointer;
}

h1 {
    color: #f65901;
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

table {
    width: 95%;
    margin: auto;
    padding: 0.2rem;
    overflow: hidden;
}

table {
    width: 100%;
    border: none;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 1rem;
    margin: auto;
    overflow: hidden;
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
    background-color: #282727;
}

.headrow {
    color: white;
    background-color: hsla(21, 100%, 50%, 0.85);
}

tr {
    color: #f5f5dc;
    background-color: #2b2828;
}

tr:last-child {
    border-bottom: none;
}

.emptyMessage {
    display: block;
    margin: auto;
    height: 300px;
    width: 300px;
}

</style>
