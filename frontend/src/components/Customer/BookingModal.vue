<script setup>
import axios from 'axios'
import { ref } from 'vue'

const props = defineProps({
    scheduleInfo: {
        type: Object,
        required: true
    }
})

const emits = defineEmits(['close', 'notification', 'error', 'Reschedule_notification', 'Reschedule_error'])
const token = localStorage.getItem('customerToken')

const serviceDate = ref('')

const servicebooking = async () => {
    try {
        if (props.scheduleInfo.action === 'createBooking') {
            try {
            await axios.post(
                `http://127.0.0.1:5000/customer/service/${props.scheduleInfo.serviceId}/booking`,
                {
                    professionalId: props.scheduleInfo.professionalId,
                    serviceDate: serviceDate.value
                },
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                }
            )
            emits('notification')
            } catch (error) {
                emits('error')
            }
        } else if (props.scheduleInfo.action === 'updateBooking') {
            try {
                
                await axios.put(
                    `http://127.0.0.1:5000/customer/service/booking/${props.scheduleInfo.bookingId}/reschedule`,
                    {
                        serviceDate: serviceDate.value
                    },
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                            'Content-Type': 'application/json'
                        }
                    }
                )
                emits('Reschedule_notification')
            } catch (error) {
                emits('Reschedule_error')
            }
            }
        emits('close')
    } catch (error) {
        console.error('Error occurred:', error.response ? error.response.data : error.message)
    }
}
</script>

<template>
    <div class="bookingModal">
        <div>
            <label for="servicedate">Schedule Date</label>
            <input
                type="date"
                class="servicedate"
                id="servicedate"
                v-model="serviceDate"
                name="servicedate"
            />
        </div>
        <div class="btn">
            <button @click="servicebooking" class="bookingBtn">Book</button>
            <button
                @click="$emit('close')"
                style="background-color: tomato; margin-left: 15px"
                class="bookingBtn"
            >
                Cancel
            </button>
        </div>
    </div>
</template>

<style scoped>

.bookingModal {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.7rem;
    width: 12rem;
    background-color: black;
    box-shadow: 5px 5px 10px rgb(0, 0, 0);
    border-radius: 1rem;
    padding: 1rem;
    margin: auto;
}

.servicedate {
    color: black;
    font-weight: bolder;
    padding: 3px;
    text-align: center;
    width: 10rem;
}

label {
    color: #f5f5f5;
    font-size: 0.8rem;
}

.bookingBtn {
    width: 4rem;
    border-radius: 0.5rem;
    background-color: #6a94ff;
    border: none;
    padding: 0.2rem;
}
</style>
