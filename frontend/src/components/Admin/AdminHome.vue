<script setup>
import { ref, onMounted } from 'vue';

const data = ref(null);
const error = ref(null);

onMounted(() => {
    const token = localStorage.getItem('token');
    const userRole = localStorage.getItem('user_role');

    if (!token || userRole !== 'admin') {
        window.location.href = '/'; // Redirect to login if no token or not admin
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
            data.value = fetchedData; // Store fetched data
        })
        .catch(err => {
            error.value = 'Error: ' + err.message; // Set error message
        });
    }
});
</script>


<template>
    <div class="container">
        <div class="top">
            <div class="searchBar">
                <input type="text" class="search" placeholder="Service Name">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                    <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                    <g id="SVGRepo_iconCarrier">
                        <path
                            d="M11 6C13.7614 6 16 8.23858 16 11M16.6588 16.6549L21 21M19 11C19 15.4183 15.4183 19 11 19C6.58172 19 3 15.4183 3 11C3 6.58172 6.58172 3 11 3C15.4183 3 19 6.58172 19 11Z"
                            stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
                    </g>
                </svg>
            </div>
            <div class="createNewBtn">Create New +</div>
        </div>
        <div class="blocks">
            <div class="block">
                <!-- <img src="/service icon/water-supply.png" class="serviceImg" alt=""> -->
                <div class="serviceName">
                    <p>Plumber</p>
                    <details>
                        <summary>
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                class="bi bi-three-dots-vertical" viewBox="0 0 16 16">
                                <path
                                    d="M9.5 13a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0m0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0m0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0" />
                            </svg>
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
    </div>
</template>



<style scoped>
.top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 3rem;
}

.container {
    overflow: scroll;
    scrollbar-width: thin;
    width: 95%;
    height: 90vh;
    margin: auto;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.6);
    background-color: #3C3C3C;
}

.searchBar {
    display: flex;
    justify-content: space-between;
    background-color: black;
    box-shadow: 5px 5px 10px rgb(0, 0, 0);
    border-radius: 0.5rem;
    padding: 0.5rem;
    width: 70%;
}

input {
    display: inline;
    background-color: transparent;
    border: none;
    outline: none;
    color: white;
    font-size: 1.5rem;
    vertical-align: middle;
    padding-left: 1rem;
}

input:focus::placeholder {
    color: transparent;
}

svg {
    width: 30px;
    height: 30px;
    cursor: pointer;
    vertical-align: middle;
}

.createNewBtn {
    height: 2.5rem;
    width: 10rem;
    cursor: pointer;
    text-align: center;
    font-size: 1.2rem;
    font-weight: bold;
    color: white;
    border-radius: 0.5rem;
    padding: 0.5rem;
    background-image: linear-gradient(to right, #E95401, #832F01);
    overflow: hidden;
}

.blocks {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 1rem;
}

.block {
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

.serviceName {
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

img {
    width: 50px;
    height: 50px;
    text-align: center;
}

details summary svg {
    background-color: #2c2b2b;
    padding: 2px;
    border-radius: 2px;
    width: 20px;
    height: 20px;
}

details summary svg:hover {
    outline: #832F01 2px solid;
}


details {
    position: relative;
}

details ul {
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

details ul li {
    text-align: start;
    cursor: pointer;
    padding: 2px 15px;
}

details ul li:hover {
    background-color: #424242;
    border-radius: 0.2rem;
    color: white;
}

details summary {
    list-style-type: none;
}

details[open] summary svg {
    background-color: #832F01;
}
</style>