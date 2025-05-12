<template>
    <div ref="customSelect" class="optionBlock" @click="toggleDropdown">
        <div class="role-icon">👥</div>
        <div class="selected-option">{{ selectedText }}</div>
        <ul class="options-list" v-show="isOpen">
            <li
                v-for="(option, index) in options"
                :key="index"
                class="option"
                @click="selectOption(option)"
            >
                {{ option.label }}
            </li>
        </ul>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
    modelValue: String
})
const emit = defineEmits(['update:modelValue'])

const options = [
    { label: 'Customer', value: 'customer' },
    { label: 'Professional', value: 'professional' },
    { label: 'Admin', value: 'admin' }
]

const selectedText = ref('Select Role')
const isOpen = ref(false)
const customSelect = ref(null)

// methods to close and open option menu
const toggleDropdown = () => {
    isOpen.value = !isOpen.value
}

const selectOption = (option) => {
    selectedText.value = option.label
    emit('update:modelValue', option.value) // Emit the selected value to the parent
    closeDropdown()
}

// Close dropdown when clicking outside
const closeDropdown = (e) => {
    if (
        customSelect.value &&
        customSelect.value.contains &&
        !customSelect.value.contains(e.target)
    ) {
        isOpen.value = false
    }
}

// When component mounts, close dropdown on outside click
onMounted(() => {
    document.addEventListener('click', closeDropdown)
})

// Watch for changes to modelValue to sync selected text
watch(
    () => props.modelValue,
    (newValue) => {
        const selectedOption = options.find((option) => option.value === newValue)
        selectedText.value = selectedOption ? selectedOption.label : 'Select Role'
    },
    { immediate: true }
)
</script>

<style scoped>
.optionBlock {
    position: relative;
    width: 100%;
    margin-bottom: 1rem;
    border-radius: 12px;
    height: 3.5rem;
    background-color: rgba(10, 10, 10, 0.6);
    border: 1px solid rgba(255, 92, 1, 0.3);
    box-shadow:
        inset 0 2px 8px rgba(0, 0, 0, 0.3),
        0 0 15px rgba(255, 92, 1, 0.1);
    padding: 0.85rem 1rem 0.5rem;
    font-size: 1.1rem;
    color: rgba(255, 255, 255, 0.8);
    font-weight: 500;
    cursor: pointer;
    user-select: none;
    display: flex;
    align-items: center;
    transition: all 0.3s ease;
}

.role-icon {
    font-size: 1.2rem;
    color: #ff5c01;
    margin-right: 10px;
    margin-left: 5px;
}

.selected-option {
    font-weight: 500;
    position: relative;
    flex-grow: 1;
}

.selected-option::after {
    content: '▼';
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 0.8rem;
    color: #ff5c01;
    transition: transform 0.3s ease;
}

.optionBlock:hover .selected-option::after {
    color: #ff8f01;
}

.options-list {
    position: absolute;
    width: 100%;
    left: 0;
    top: 110%;
    background-color: rgba(30, 30, 30, 0.95);
    color: rgba(255, 255, 255, 0.8);
    border-radius: 12px;
    padding: 0.5rem 0;
    margin: 0;
    list-style: none;
    z-index: 10;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 92, 1, 0.2);
    overflow: hidden;
}

.option {
    padding: 0.75rem 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
}

.option:hover {
    background-color: rgba(255, 92, 1, 0.15);
    color: #fff;
    padding-left: 2rem;
}

.option:last-child {
    border: none;
}

.optionBlock:focus,
.optionBlock:hover {
    border-color: rgba(255, 92, 1, 0.6);
    background-color: rgba(20, 20, 20, 0.7);
    box-shadow: 0 0 20px rgba(255, 92, 1, 0.25);
}

/* Animation for the dropdown arrow when open */
.optionBlock:has(.options-list:not([style*='display: none'])) .selected-option::after {
    transform: translateY(-50%) rotate(180deg);
}
</style>
