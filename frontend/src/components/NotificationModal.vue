<template>
    <div
        class="notification"
        :class="{ show: isVisible, error: isError }"
        @click="closeNotification"
    >
        {{ message }}
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
    message: String,
    type: { type: String, default: 'success' }, 
    duration: { type: Number, default: 3000 }
})

const emit = defineEmits(['close'])

const isVisible = ref(false)
const isError = ref(props.type === 'error')

onMounted(() => {
    setTimeout(() => {
        isVisible.value = true
    }, 50) 

    setTimeout(() => {
        isVisible.value = false
        setTimeout(() => emit('close'), 2000) 
    }, props.duration)
})

const closeNotification = () => {
    isVisible.value = false
    setTimeout(() => emit('close'), 2000)
}
</script>

<style scoped>
.notification {
    position: fixed;
    top: 3%;
    left: 50%;
    background-color: #1e1e1e;
    height: 5rem;
    width: 50vw;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.5rem;
    font-weight: bolder;
    transform: translateX(-50%);
    color: white;
    padding: 1rem;
    border-radius: 1rem;
    box-shadow: 0 8px 15px rgb(0, 0, 0);
    opacity: 0;
    transition: all 1.3s ease-in-out;
    pointer-events: none;
    z-index: 9999;
}

.notification.show {
    opacity: 1;
}

.notification.error {
    background-color: #d31919cf;
    outline: 10px solid #ff0000;
}
</style>
