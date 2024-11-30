<script setup>
import { onMounted, ref, reactive } from 'vue';
import axios from 'axios';
import Review from '@/assets/svg/Review.svg?raw';
import ReviewModal from './ReviewModal.vue';
import BookingModal from './BookingModal.vue';
import MenuDot from '@/assets/svg/MenuDot.svg?raw';

const token = localStorage.getItem('customerToken');
const bookings = ref([]);

// Fetch bookings
const fetchBookings = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5000/customer/service/bookings', {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'  
            }
        });
        bookings.value = response.data;
        // Initialize showMenu for each booking to false (closed menu by default)
        bookings.value.forEach(booking => {
            showMenu[booking.id] = false;  // Initialize menu state per booking
        });
    } catch (error) {
        console.error('Error occurred:', error.response ? error.response.data : error.message);
    }
};

onMounted(() => {
    fetchBookings();
});

// Reschedule Service Request
const reschedule = reactive({});
const info = ref({});

const rescheduleBooking = (bookingId) => {
    reschedule[bookingId] = !reschedule[bookingId];
    info.value = {
        bookingId: bookingId,
        action: 'updateBooking'
    }
};

const closeRescheduleModal = (bookingId) => {
    reschedule[bookingId] = !reschedule[bookingId];
    fetchBookings();
};

// Cancel Service Request
const cancelBooking = async (bookingId) => {
    try {
        await axios.delete(`http://127.0.0.1:5000/customer/service/booking/${bookingId}/delete`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        addNotification('Service cancelled successfully!', 3000);
        fetchBookings();
            
        } catch (error) {
            addNotification('Failed to cancel service. Please try again.', 5000);
        }
};

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
        addNotification('Service marked completed successfully!', 3000);
    } catch (error) {
        addNotification('Failed to mark service as completed. Please try again.', 5000);
    }
};

// Review Modal
const openModal = (bookingId, action) => {
    showModal.value = true;
    booking_id.value = bookingId;
    Action.value = action;
};

const closeModal = () => {
    showModal.value = false;
    booking_id.value = null;
    Action.value = '';
    fetchBookings();
};

const showModal = ref(false);
const booking_id = ref(null);
const Action = ref('');

// Menu to Edit, Delete or Review Request
const showMenu = reactive({}); // Using `reactive` to track changes to the object

const toggleMenu = (bookingId) => {
    showMenu[bookingId] = !showMenu[bookingId]; // Toggle specific booking's menu
};

const handleOptionClick = (bookingId, option) => {
    console.log(`Option selected: ${option}`);
    if (option === 'editReview') {
        openModal(bookingId, option);
    } else if (option === 'deleteReview') {
        deleteReview(bookingId);
    } else if (option === 'edit') {
        rescheduleBooking(bookingId);
    } else if (option === 'delete') {
        cancelBooking(bookingId);
    }

    // Close the menu after selection
    showMenu[bookingId] = false;
};

// Delete Review
const deleteReview = async (bookingId) => {
    try {
        await axios.delete(`http://127.0.0.1:5000/customer/service/${bookingId}/review/delete`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        addNotification('Review deleted successfully!', 3000);
        fetchBookings();
    } catch (err) {
        addNotification('Failed to delete review. Please try again.', 5000);
    }
}

// Notification
import NotificationModal from '../NotificationModal.vue';

const notifications = ref([]);

const addNotification = (message, duration) => {
    notifications.value.push({ message, duration });
};
</script>

<template>
    <div>
        <div class="bookingContainer">
            <h1>BOOKING</h1>
            <table v-if="bookings.length > 0">
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
                        <th></th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="(booking, index) in bookings" :key="booking.id">
                        <td>{{ index + 1 }}</td>
                        <td>{{ booking.serviceName }}</td>
                        <td>{{ booking.professionalName }}</td>
                        <td>{{ new Date(booking.requestDate).toISOString().slice(0, 10) }}</td>
                        <td v-if="booking.completionDate">{{ new Date(booking.completionDate).toISOString().slice(0, 10) }}</td>
                        <td v-else>....</td>
                        <td v-if="booking.professionalStatus=='accepted' || booking.professionalStatus=='completed'">Accepted</td>
                        <td v-else-if="booking.professionalStatus=='rejected'">Rejected</td>
                        <td v-else>Pending</td>
                        <td v-if="booking.completionDate">Completed</td>
                        <td v-else>....</td>

                        <!-- action button to mark service as completed -->
                        <td v-if="(booking.professionalStatus=='accepted' || booking.professionalStatus=='completed') 
                            && booking.customerStatus!='completed' ">
                            <button class="closeBtn" @click="closeBooking(booking.id)" type="submit">Close</button>
                        </td>
                        <td v-else-if="booking.customerStatus=='completed'">Completed</td>
                        <td v-else></td>

                        <!-- review button -->
                        <td v-if="booking.customerStatus=='completed' && booking.reviewed=='no'">
                            <p @click="openModal(booking.id,'createReview')" class="review" v-html="Review"></p>
                        </td>
                        <td v-else></td>

                        <!-- Menu Button -->
                        <td>
                            <p v-html="MenuDot" @click="toggleMenu(booking.id)" class="menu"></p>
                            <div v-if="showMenu[booking.id]" class="dropdown-menu">
                                <p v-if="booking.completionDate==null" @click="handleOptionClick(booking.id,'edit')">Edit</p>
                                <p v-if="booking.professionalStatus=='pending'" @click="handleOptionClick(booking.id,'delete')">Delete</p>
                                <p v-if="booking.reviewed=='yes'" @click="handleOptionClick(booking.id,'editReview')">Edit Review</p>
                                <p v-if="booking.reviewed=='yes'" @click="handleOptionClick(booking.id,'deleteReview')">Delete Review</p>
                            </div>
                            <BookingModal v-if="reschedule[booking.id]" 
                            class="rescheduleBookingModal"
                            :scheduleInfo="info" 
                            @close="closeRescheduleModal(booking.id)" 
                            @Reschedule_notification="addNotification('Service rescheduled successfully!', 3000)"
                            @Reschedule_error="addNotification('Error rescheduling service', 3000)"
                            />
                        </td>
                    </tr>
                </tbody>
            </table>
            <img v-else class="emptyMessage" src="@/assets/images/empty-box.png" alt="NO Data">
        </div>
        <!-- Review Modal -->
        <ReviewModal v-if="showModal" 
        :bookingId="booking_id" 
        :action="Action" 
        @closeModal="closeModal"
        @notification="addNotification('Review added successfully!', 3000)" 
        @error="addNotification('Error adding review', 3000)"
        @update_notification="addNotification('Review updated successfully!', 3000)"
        @update_error="addNotification('Error updating review', 3000)"
        />

        <!-- Notification Modal -->
        <NotificationModal v-for="notification in notifications" 
        :key="notification.message" 
        :message="notification.message" 
        :duration="notification.duration" />
    </div>
</template>

<style scoped>

.rescheduleBookingModal {
    position: absolute;
    margin-top: 5px;
    left: 80%;
    z-index: 10000;
}

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

.menu{
    width: 30px;
    height: 30px;
    cursor: pointer;
    background-color: #242424;
    padding: 5px;
    border-radius: 5px;
}

.dropdown-menu {
    position: absolute;
    background-color: rgb(18, 17, 17);
    border: 1px solid #ddd;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    border-radius: 4px;
    margin-top: 5px;
    z-index: 1000;
    width: 80px;
}

.dropdown-menu p {
    margin: 0;
    padding: 5px;
    cursor: pointer;
    color: white;
}

.dropdown-menu p:hover {
    background-color: #383535;
}

.emptyMessage{
    height: 250px;
    width: 250px;
    display: block;
    margin: auto;
    margin-top: 4rem;

}

</style>