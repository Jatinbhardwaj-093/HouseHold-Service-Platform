<script setup></script>

<template>
    <div>
        <div class="container">
            <div class="searchBar">
                <input type="text" class="search" placeholder="Search by customer name" />
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
                        <th>S.No</th>
                        <th>Service ID</th>
                        <th>Professional</th>
                        <th>Customer</th>
                        <th>P - Pin Code</th>
                        <th>C - Pin Code</th>
                        <th>Validity</th>
                        <th></th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>1</td>
                        <td>Jatin Slith</td>
                        <td>Plumber</td>
                        <td>4 Years</td>
                        <td>110023</td>
                        <td>5</td>
                        <td>Ok</td>
                        <td><button>Flag</button></td>
                        <td><button>Delete</button></td>
                    </tr>
                    <tr>
                        <td>1</td>
                        <td>2</td>
                        <td>3</td>
                        <td>4</td>
                        <td>5</td>
                        <td>5</td>
                        <td>Flagged</td>
                        <td><button>UnFlag</button></td>
                        <td><button>Delete</button></td>
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
    text-align: center;
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
</style>
