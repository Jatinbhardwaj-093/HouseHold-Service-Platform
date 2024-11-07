<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios';
import Review from '@/assets/svg/Review.svg?raw'

const token = localStorage.getItem('token');
const bookings = ref([]);

// fetchBookings
const fetchBookings = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5000/customer/', {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'  
            }
        })
        bookings.value = response.data.service_bookings;
    }
    catch (error) {
        console.error('Error occurred:', error.response ? error.response.data : error.message);
    }
}

// Marking service completed
const closeBooking = async (bookingId) => {
    const currentDate = new Date().toISOString().slice(0, 10);
    try {
        await axios.put(
            `http://127.0.0.1:5000/customer/service/booking/${bookingId}/complete`,
            { completionDate: currentDate },
            {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            }
        );
        fetchBookings();
    } catch (error) {
        console.error('Error occurred:', error.response ? error.response.data : error.message);
    }
}

onMounted(() => {
    fetchBookings();
})
</script>


<template>
    <div>
        <div class="bookingContainer">
        <h1>BOOKING</h1>
        <table>
            <thead>
            <tr class="headrow">
                <th>S.No</th>
                <th>Service</th>
                <th>Professional</th>
                <th>Date of Request</th>
                <th>Date of Completion</th>
                <th>Request Status</th>
                <th>Service Status</th>
                <th>Action</th>
                <th></th>
            </tr>
            </thead>

            <tbody>
            <tr v-for="(booking, index) in bookings" :key="booking.id">
                <td>{{ index + 1 }}</td>
                <td>{{ booking.serviceName }}</td>
                <td>{{ booking.professionalName }}</td>
                <td>{{ new Date(booking.requestDate).toISOString().slice(0, 10) }}</td>
                
                <!-- booking.completionDate -->
                <td v-if="booking.completionDate">{{ new Date(booking.completionDate).toISOString().slice(0, 10) }}</td>
                <td v-else>Pending</td>
                
                <!-- booking request status -->
                <td v-if="booking.professionalStatus=='accepted'||booking.professionalStatus=='completed'">Accepted</td>
                <td v-else>Pending</td>

                <!-- booking service status -->
                <td v-if="booking.completionDate">Completed</td>
                <td v-else>Pending</td>

                <!-- action button to mark service as completed -->
                <td v-if="(booking.professionalStatus=='accepted' || booking.professionalStatus=='completed') 
                    && !booking.customerStatus=='completed' ">
                    <button class="closeBtn" @click="closeBooking(booking.id)" type="submit">Close</button></td>
                <td v-else>Completed</td>

                <!-- review button -->
                <td v-if="booking.customerStatus=='completed'"><p class="review" v-html="Review"></p></td>
                <td v-else></td>
            </tr>
            </tbody>
        </table>
    </div>
    </div>
</template>

<style scoped>
.bookingContainer{
    width: 95%;
    background-color: rgba(255, 255, 255, 0.06);
    box-shadow: 5px 5px 10px rgb(0, 0, 0);
    border-radius: 1rem;
    padding: 1rem;
    margin: auto;

}

h1{
    text-align: center;
    color: #fff;
    font-size: 2.5rem;    
    font-weight: bolder;
    margin-bottom: 1rem;
}


table{
    width: 95%;
    margin: auto;
    padding: .2rem;
    overflow: hidden;
}

table{
    width: 100%;
    border: none;
    border-collapse: separate; 
    border-spacing: 0; 
    border-radius: 1rem; 
    margin: auto;
    overflow: hidden; 
}



th,td{
    padding: 4px;
    text-align: center;
    border-bottom: 1px solid #f5f5dc;
}

tr:last-child td{
    border-bottom: none;
}

tr:nth-child(even) {
    background-color: #2f2c2c;
}

.headrow{
    color: white;
    background-color: hsla(21, 100%, 50%, 0.85);
}

tr{
    color: #f5f5dc;
    background-color: #3C3C3C;
}

tr:last-child{
    border-bottom: none;
}

.closeBtn{
    background-color: #6A94FF;
    border: none;
    border-radius: .2rem;
    width: 3rem;
    color: white;
    cursor: pointer;
}

.review{
    width: 25px;
    height: 25px;
}

</style>