<template>
    <div class="container">
        <div class="top">
            <div class="searchBar">
                <input type="text" class="search" placeholder="Service Name">
                <div class="searchBtn" v-html="Search"></div>
            </div>
            <div class="createNewBtn" @click="showModal = true">Create New +</div>
        </div>

        <div class="blocks">
            <div class="block">
                <div class="serviceName">
                    <p>Plumber</p>
                    <details>
                        <summary>
                            <p class="menuDot" v-html="MenuDot"></p>
                        </summary>
                        <ul>
                            <li>View</li>
                            <li>Edit</li>
                            <li>Delete</li>
                        </ul>
                    </details>
                </div>
            </div>
        </div>

        <Modal :showModal="showModal" @closeModal="showModal = false" />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Modal from './ServiceCreateModel.vue';
import Search from '@/assets/svg/Search.svg?raw';
import MenuDot from '@/assets/svg/MenuDot.svg?raw';

const showModal = ref(false);
const data = ref(null);
const error = ref(null);

onMounted(() => {
    const token = localStorage.getItem('token');
    const userRole = localStorage.getItem('user_role');

    if (!token || userRole !== 'admin') {
        window.location.href = '/';
    } else {
        fetch('/admin/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(fetchedData => {
                data.value = fetchedData; 
            })
            .catch(err => {
                error.value = 'Error: ' + err.message; 
            });
    }
});
</script>

<style scoped>

.container{
    overflow: scroll;
    scrollbar-width: thin;
    width: 95%;
    height: 100vh;
    margin: auto;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow:  5px 5px 10px rgba(0, 0, 0, 0.6);
    background-color: #3C3C3C;
}

.top{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

.searchBar{
    display: flex;
    justify-content: space-between;
    background-color: black;
    box-shadow: 5px 5px 10px rgb(42, 42, 42);
    border-radius: 0.5rem;
    padding: 0.5rem;
    width: max(70%);
}

.searchBtn{
    width: 30px;
    height: 30px;
    cursor: pointer;
    vertical-align: middle;
}

input{
    background-color: transparent;
    border: none;
    outline: none;
    color: white;
    font-size: 1.5rem;
    vertical-align: middle;
    padding-left: 1rem;
}

input:focus::placeholder{
    color: transparent;
}


.createNewBtn{
    width: 10rem;
    cursor: pointer;
    text-align: center;
    font-size: 1.25rem;
    font-weight: bold;
    color: white;
    border-radius: 0.5rem;
    padding: 0.6rem;
    background-image: linear-gradient( to right,#E95401,#832F01 );
    overflow: hidden;
}

.blocks{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 1rem;
}

.block{
    position: relative;
    background-color: black;
    width: 100px;
    height: 100px;
    border-radius: 0.5rem;
    box-shadow: 2px 5px 20px rgba(0, 0, 0, 0.6);
    padding: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 5px;
}

.serviceName{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    width: 100%;
    text-align: center;
    color: #fff;
    font-size: 1rem;
    font-weight: bolder;
}

img{
    width: 50px;
    height: 50px;
    text-align: center;
}

details summary .menuDot{
    background-color: #2c2b2b;
    padding: 2px;
    border-radius: 2px;
    width: 20px;
    height: 20px;
}

details summary .menuDot:hover{
    outline: #832F01 2px solid;
}


details{
    position: relative;
}

details ul{
    position: absolute;
    top: -200%;
    left: 150%; 
    list-style: none;
    width: max-content;
    background-color: #4F4F4F;
    color: white;
    border-radius: 0.2rem;
    z-index: 100;
}

details ul li{
    text-align: start;
    cursor: pointer;
    padding: 2px 15px;
}

details ul li:hover{
    background-color: #424242;
    border-radius: 0.2rem;
    color: white;
}

details summary{
    list-style-type: none;
}

details[open] summary .menuDot{
    background-color: #832F01;
}

</style>