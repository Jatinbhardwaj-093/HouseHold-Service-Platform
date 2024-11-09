<script setup>
import Cross from '@/assets/svg/Cross.svg?raw';
import UnfillStar from '@/assets/svg/UnfillStar.svg?raw';
import FillStar from '@/assets/svg/FillStar.svg?raw';

import { ref } from 'vue';
import axios from 'axios';

const { bookingId,action } = defineProps({
    bookingId: Number,
    action: String
});

const response = ref({
    review: '',
    rating: 0
});

const emit = defineEmits(['closeModal']);

const submitReview = async () => {
    
    if (action === 'createReview') {
        await axios.post(`http://127.0.0.1:5000/customer/service/${bookingId}/review/create`, response.value, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json'
            }
        });
    } else if (action === 'editReview') {
        await axios.put(`http://127.0.0.1:5000/customer/service/${bookingId}/review/update`, response.value, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json'
            }
        });
    }
    
    emit('closeModal');
};


const stars = ref([false, false, false, false, false]);


const updateRating = (index) => {
    response.value.rating = index + 1;
    stars.value = stars.value.map((_, i) => i <= index);
};

</script>

<template>
    <div>
        <div class="reviewingContainer">
            <h1>Review</h1>
            <textarea v-model="response.review" placeholder="Write a review...."></textarea>
            <p class="rating">Rate Our Service</p>
            <div class="ratingStar">
                <p
                    v-for="(star, index) in stars"
                    :key="index"
                    @click="updateRating(index)"
                    v-html="star ? FillStar : UnfillStar"
                    class="star-icon"
                ></p>
            </div>
            <button @click="submitReview">Submit</button>
            <div class="cross">
                <p @click="$emit('closeModal')" v-html="Cross"></p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.reviewingContainer {
    position: absolute;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    width: 30rem;
    background-color: #292929;
    box-shadow: 5px 5px 10px rgb(0, 0, 0);
    border-radius: 1rem;
    padding: 1rem;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

h1 {
    text-align: center;
    font-weight: bolder;
    font-size: 2rem;
    color: #FF5C01;
}

textarea {
    width: 20rem;
    height: 10rem;
    padding: 0.5rem;
    border-radius: 0.5rem;
    border: none;
    background-color: #1c1c1c;
    color: white;
    padding: 1rem;
    outline: none;
    resize: none;
    scrollbar-width: none;
}

textarea:focus::placeholder {
    color: transparent;
}

button {
    width: 7rem;
    height: 2rem;
    font-size: 1rem;
    background-color: #6A94FF;
    color: white;
    padding: 0.2rem;
    border-radius: 0.5rem;
    border: none;
    cursor: pointer;
}

.cross {
    position: absolute;
    top: 10px;
    right: 10px;
    cursor: pointer;
}

.cross p {
    height: 50px;
    width: 50px;
}

.rating {
    text-align: start;
    color: #FF5C01;
    font-size: 1.5rem;
}

.ratingStar {
    display: flex;
    gap: 0.5rem;
}

.star-icon {
    height: 35px;
    width: 35px;
    cursor: pointer;
}
</style>