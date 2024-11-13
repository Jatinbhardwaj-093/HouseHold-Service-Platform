<script setup>
import axios from 'axios';
import { ref, onMounted, computed } from 'vue';
import Review from '@/assets/svg/Review.svg?raw';
import ReviewModal from './ReviewModal.vue';

const token = localStorage.getItem('token');

const requests = ref([]);

// Fetch requests from the API
const fetchRequests = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5000/professional/service/requests/history', {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        requests.value = response.data;
    } catch (error) {
        console.error(error);
    }
};

const completedRequests = computed(() => {
    return requests.value.filter(request => request.professionalStatus === 'completed');
});

const rejectedRequests = computed(() => {
    return requests.value.filter(request => request.professionalStatus === 'rejected');
});

onMounted(() => {
    fetchRequests();
});

// Review of Completed Request
const showModalReview = ref(false);
const reviewData = ref({
    customerName: '',
    review: '',
    rating: 0
});

const ModalReview = (request) => {
    showModalReview.value = true;
    reviewData.value.customerName = request.customerName;
    reviewData.value.review = request.review;
    reviewData.value.rating = request.rating;
};

</script>

<template>
    <div>
        <div class="grid">
            <!-- Completed Requests Table -->
            <div class="table1">
                <h1>Completed Requests</h1>
                <table v-if="completedRequests.length > 0">
                    <thead>
                        <tr class="headrow">
                            <th>S.No</th>
                            <th>Customer</th>
                            <th>Contact</th>
                            <th style="width: 30%;">Address</th>
                            <th>Pincode</th>
                            <th>Date Of Request</th>
                            <th>Date Of Completion</th>
                            <th>Review</th>
                            <th>Rating</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(request, index) in completedRequests" :key="request.id">
                            <td>{{ index + 1 }}</td>
                            <td>{{ request.customerName }}</td>
                            <td>{{ request.customerContact }}</td>
                            <td>{{ request.customerAddress }}</td>
                            <td>{{ request.customerPincode }}</td>
                            <td>{{ new Date(request.requestDate).toISOString().slice(0, 10) }}</td>
                            <td>{{ new Date(request.completionDate).toISOString().slice(0, 10) }}</td>
                            <td v-if="request.reviewed === 'yes'">
                                <p class="review" v-html="Review" @click="ModalReview(request)"></p>
                            </td>
                            <td v-else></td>
                            <td>{{ request.rating }}</td>
                        </tr>
                    </tbody>
                </table>
                <img v-else class="emptyMessage" src="@/assets/images/empty-box.png" alt="NO Data">
            </div>

            <!-- Rejected Requests Table -->
            <div class="table2">
                <h1>Rejected Requests</h1>
                <table v-if="rejectedRequests.length > 0">
                    <thead>
                        <tr class="headrow">
                            <th>S.No</th>
                            <th>Customer</th>
                            <th style="width: 40%;">Address</th>
                            <th>Pincode</th>
                            <th>Date Of Request</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(request, index) in rejectedRequests" :key="request.id">
                            <td>{{ index + 1 }}</td>
                            <td>{{ request.customerName }}</td>
                            <td>{{ request.customerAddress }}</td>
                            <td>{{ request.customerPincode }}</td>
                            <td>{{ new Date(request.requestDate).toISOString().slice(0, 10) }}</td>
                            <td class="rejected">Rejected</td>
                        </tr>
                    </tbody>
                </table>
                <img v-else class="emptyMessage" src="@/assets/images/empty-box.png" alt="NO Data">
            </div>
        </div>

        <ReviewModal class="modal" v-if="showModalReview" :ReviewData="reviewData" @closeModal="showModalReview = false" />
    </div>
</template>


<style scoped>

.modal{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 10000;
}

.grid{
    display: grid;
    grid-template-rows: 1fr 1fr;
    grid-row-gap: 1rem;
    height: 80vh;
    width: 95vw;
    margin: auto;
    
}

.grid > div{
    overflow: auto;
    scrollbar-width: none;
    background-color: rgba(255, 255, 255, 0.06);
    box-shadow: 5px 5px 10px rgb(0, 0, 0);
    border-radius: 1rem;
    padding: 1rem;
}

h1{
    text-align: center;
    color: #fff;
    font-size: 2rem;    
    font-weight: bolder;
    margin-bottom: 1rem;
}
table{
    width: 100%;
    border: none;
    border-collapse: separate; 
    border-spacing: 0; 
    border-radius: 0.5rem; 
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

.review{
    margin: auto;
    height: 25px;
    width: 25px;
    cursor: pointer;
}

.emptyMessage{
    height: 180px;
    width: 180px;
    display: block;
    margin: auto;
    margin-top: 2rem;

}
</style>