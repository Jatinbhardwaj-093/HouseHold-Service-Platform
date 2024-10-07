<template>
    <div class="optionBlock">
        <div ref="customSelect" class="custom-select" @click="toggleDropdown">
            <div class="selected-option">{{ selectedText }}</div>
            <ul class="options-list" v-show="isOpen">
                <li v-for="(option, index) in options" :key="index" class="option" @click="selectOption(option)">
                    {{ option.label }}
                </li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const options = [
    { label: 'Customer', value: 'customer' },
    { label: 'Professional', value: 'professional' },
    { label: 'Admin', value: 'admin' }
]

const selectedText = ref('Select Role')
const selectedValue = ref(null)
const isOpen = ref(false)

const customSelect = ref(null)

const toggleDropdown = () => {
    isOpen.value = !isOpen.value
}

const selectOption = (option) => {
    selectedText.value = option.label
    selectedValue.value = option.value
    isOpen.value = false
}

// Close dropdown when clicking outside
const closeDropdown = (e) => {
    if (customSelect.value && !customSelect.value.contains(e.target)) {
        isOpen.value = false
    }
}

onMounted(() => {
    document.addEventListener('click', closeDropdown)
})
</script>

<style scoped>
/* Role Option Block */
.optionBlock {
    display: inline-block;
    width: clamp(20rem, 25vw + 10rem, 50rem);
    margin-bottom: 1rem;
}

.custom-select {
    position: relative;
    border-radius: 1rem;
    height: 3rem;
    background-color: rgba(255, 255, 255, 0.2);
    box-shadow: 5px 5px 25px rgba(0, 0, 0, 0.6);
    padding: 0.65rem 1rem 0.5rem;
    font-size: 1.5rem;
    color: rgba(255, 255, 255, 0.6);
    font-weight: bolder;
    font-style: italic;
    cursor: pointer;
    user-select: none;
}

.selected-option {
    display: block;
    padding-left: 1.5rem;
}

.options-list {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.95);
    color: rgba(255, 255, 255, 0.6);
    border-radius: 0.5rem;
    padding: 0;
    margin: 0;
    list-style: none;
    z-index: 10;
}

.option {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    cursor: pointer;
    transition: background-color 0.2s;
}

.option:hover {
    background-color: rgba(107, 107, 107, 0.4);
}

.option:last-child {
    border: none;
}

.custom-select.open .options-list {
    display: block;
}

.custom-select.open .selected-option {
    color: white;
}
</style>