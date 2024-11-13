<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const token = localStorage.getItem('token');
const newRequests = ref([]);
const ongoingRequests = ref([]);

const fetchbookings = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5000/professional/service/requests', {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        
        })
        newRequests.value = response.data.newRequests;
        ongoingRequests.value = response.data.ongoingRequests;
    }
    catch (error) {
        console.error('Error occurred:', error.response ? error.response.data : error.message);
    }
}

onMounted(() => {
    fetchbookings();
})

const newRequestResponse = async (requestId, status) => {
    try {
        await axios.put(
            `http://127.0.0.1:5000/professional/service/request/${requestId}`,
            { professionalStatus: status },
            {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            }
        )
        fetchbookings();
    } catch (error) {
        console.error('Error occurred:', error.response ? error.response.data : error.message);
    }
}

const markComplete = async (requestId) => {
    const completionDate = new Date().toISOString().slice(0, 10);
    try {
        await axios.put(
            `http://127.0.0.1:5000/professional/service/request/${requestId}/complete`,
            { completionDate: completionDate },
            {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            }
        )
        fetchbookings();
    }
    catch (error) {
        console.error('Error occurred:', error.response ? error.response.data : error.message);
    }
}

</script>


<template>
    <div>
        <div class="grid">
        <div class="table1">
            <h1>New Requests</h1>
            <table v-if="newRequests.length > 0">
                <thead>
                <tr class="headrow">
                    <th>S.No</th>
                    <th>Customer</th>
                    <th>Contact</th>
                    <th style="width: 30%;">Address</th>
                    <th>Pincode</th>
                    <th>Date Of Request</th>
                    <th>Action</th>
                    
                </tr>
                </thead>

                <tbody>
                <tr v-for="(request, index) in newRequests" :key="request.id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ request.customerName }}</td>
                    <td>{{ request.customerContact }}</td>
                    <td>{{ request.customerAddress }}</td>
                    <td>{{ request.customerPincode }}</td>
                    <td>{{ new Date(request.requestDate).toISOString().slice(0, 10) }}</td>
                    <td v-if="request.professionalStatus == 'pending'"><div class="option">
                        <button class="acceptBtn" @click="newRequestResponse(request.id, 'accepted')">Accept</button>
                        <button class="rejectBtn" @click="newRequestResponse(request.id , 'rejected')">Reject</button>
                    </div></td>
                    <td v-else><p v-html="request.professionalStatus=='accepted'?'Accepted':'Rejected'"></p></td>
                </tr>
                </tbody>
            </table>
            <img v-else class="emptyMessage" src="@/assets/images/empty-box.png" alt="No Data">
        </div>
        <div class="table2">
            <h1>Ongoing Requests</h1>
            <table v-if="ongoingRequests.length > 0">
                <thead>
                <tr class="headrow">
                    <th>S.No</th>
                    <th>Customer</th>
                    <th>Contact</th>
                    <th style="width: 30%;">Address</th>
                    <th>Pincode</th>
                    <th>Date Of Request</th>
                    <th>Customer Status</th>
                    <th>Action</th>
                </tr>
                </thead>

                <tbody>
                <tr v-for="(request, index) in ongoingRequests" :key="request.id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ request.customerName }}</td>
                    <td>{{ request.customerContact }}</td>
                    <td>{{ request.customerAddress }}</td>
                    <td>{{ request.customerPincode }}</td>
                    <td>{{ new Date(request.requestDate).toISOString().slice(0, 10) }}</td>
                    <td>{{ request.customerStatus }}</td>
                    
                    <td><div class="option">
                        <button class="closeBtn" @click="markComplete(request.id)">Mark Complete</button>
                    </div></td>
                </tr>
                </tbody>
            </table> 
            <img v-else class="emptyMessage" src="@/assets/images/empty-box.png" alt="No Data">
        </div>
    </div>
    </div>
</template>

<style scoped>
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

.option{
    display: flex;
    gap: 5px;
    justify-content: center;
    align-items: center;
}

.closeBtn{
background-color: #6A94FF;
border: none;
color: #f5f5dc;
padding: 5px;
border-radius: 5px;
text-align: center;
}

button {
    border: none;
    border-radius: 0.25rem;
    width: 5rem;
    font-size: 1rem;
    cursor: pointer;
    background-color: #1e1e1e;
    color: #fe772e;
    padding: 3px;
    text-align: center;
}

.emptyMessage{
    height: 180px;
    width: 180px;
    display: block;
    margin: auto;
    margin-top: 2rem;

}


</style>