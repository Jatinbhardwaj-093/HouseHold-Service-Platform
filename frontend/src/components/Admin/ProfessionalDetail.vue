<script setup>
import { onMounted, ref } from 'vue'

// Create a reference to track the details elements
const detailsRef = ref([])

// Use onMounted to set up the click listener when the component is mounted
onMounted(() => {
    document.addEventListener('click', (event) => {
        detailsRef.value.forEach((detail) => {
            if (!detail.contains(event.target)) {
                detail.removeAttribute('open') // Close the <details> element
            }
        })
    })
})
</script>

<template>
    <div>
        <div class="container">
            <div class="searchBar">
                <input type="text" class="search" placeholder="Service Name" />
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
            <table>
                <thead>
                    <tr class="headrow">
                        <th style="width: 1%"></th>
                        <th>S.No</th>
                        <th>Professinal</th>
                        <th>Service</th>
                        <th>Experience</th>
                        <th>Pincode</th>
                        <th>Rating</th>
                        <th>Verification</th>
                        <th style="width: 5%"></th>
                        <th style="width: 2%"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="yellow"
                                class="bi bi-flag-fill" viewBox="0 0 16 16">
                                <path
                                    d="M14.778.085A.5.5 0 0 1 15 .5V8a.5.5 0 0 1-.314.464L14.5 8l.186.464-.003.001-.006.003-.023.009a12 12 0 0 1-.397.15c-.264.095-.631.223-1.047.35-.816.252-1.879.523-2.71.523-.847 0-1.548-.28-2.158-.525l-.028-.01C7.68 8.71 7.14 8.5 6.5 8.5c-.7 0-1.638.23-2.437.477A20 20 0 0 0 3 9.342V15.5a.5.5 0 0 1-1 0V.5a.5.5 0 0 1 1 0v.282c.226-.079.496-.17.79-.26C4.606.272 5.67 0 6.5 0c.84 0 1.524.277 2.121.519l.043.018C9.286.788 9.828 1 10.5 1c.7 0 1.638-.23 2.437-.477a20 20 0 0 0 1.349-.476l.019-.007.004-.002h.001" />
                            </svg>
                        </td>
                        <td>1</td>
                        <td>Jatin Slith</td>
                        <td>Plumber</td>
                        <td>4 Years</td>
                        <td>110023</td>
                        <td>5</td>
                        <td class="verified">Verified</td>
                        <td>
                            <div class="option">
                                <button class="unverifyBtn">Unverify</button>
                            </div>
                        </td>
                        <td>
                            <details>
                                <summary>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                        class="bi bi-three-dots-vertical" viewBox="0 0 16 16">
                                        <path
                                            d="M9.5 13a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0m0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0m0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0" />
                                    </svg>
                                </summary>
                                <ul>
                                    <li>Falg</li>
                                    <li>Delete</li>
                                </ul>
                            </details>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<style scoped>
.container {
    width: 95%;
    height: 100vh;
    margin: auto;
    border-radius: 1rem;
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.6);
    background-color: #3c3c3c;
    overflow-y: hidden;
    overflow-x: scroll;
    scrollbar-width: thin;
}

.searchBar {
    display: flex;
    justify-content: space-between;
    background-color: black;
    box-shadow: 5px 5px 10px rgb(0, 0, 0);
    border-radius: 0.5rem;
    padding: 0.5rem;
    margin: 2rem;
    width: min(100%, 800px);
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

table {
    width: 98%;
    border: none;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 0.5rem;
    overflow: hidden;
    margin: auto;
}

th,
td {
    padding: 4px;
    text-align: start;
    border-bottom: 1px solid #f5f5dc;
}

tr:last-child td {
    border-bottom: none;
}

tr:nth-child(even) {
    background-color: #2f2c2c;
}

.headrow {
    color: white;
    background-color: hsla(21, 100%, 50%, 0.85);
}

tr {
    color: #f5f5dc;
    background-color: #3c3c3c;
}

.option {
    display: flex;
    gap: 5px;
    justify-content: center;
    align-items: center;
}

button {
    border: none;
    border-radius: 0.2rem;
    width: 4rem;
    color: white;
    cursor: pointer;
}

td svg {
    height: 20px;
    width: 20px;
}

svg {
    height: 30px;
    width: 30px;
    cursor: pointer;
}

button {
    background-color: #1e1e1e;
    color: #fe772e;
    padding: 3px;
    text-align: center;
}

details summary svg {
    background-color: #2c2b2b;
    padding: 2px;
    border-radius: 2px;
    height: 25px;
    width: 25px;
}

details summary svg:hover {
    outline: #832f01 2px solid;
}

details {
    position: relative;
}

details ul {
    position: absolute;
    top: -100%;
    right: 110%;
    list-style: none;
    width: max-content;
    background-color: #4f4f4f;
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
    background-color: #832f01;
}

.bi .bi-flag-fiil {
    color: yellow;
    background-color: yellow;
}
</style>
