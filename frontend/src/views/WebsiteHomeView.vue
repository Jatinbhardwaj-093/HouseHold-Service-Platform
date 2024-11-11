<script setup>

</script>


<template>
    <div>
        <h1 class="heading">Welcome to Home Service App</h1>
        <router-link :to="{name: 'login'}" class="btn">Login</router-link>
        <router-link :to="{name: 'signup'}" class="btn">Sign UP</router-link>
    </div>
</template>

<style scoped>

.heading {
    text-align: center;
    font-weight: bolder;
    font-size: 3.5rem;
    margin-top: 1.5rem;
    margin-bottom: 3rem;
    font-weight: bolder;
    font-style: italic;
    color: #FF5C01;
}

.btn{
    font-size: 1.5rem;
    padding: .5rem;
    border-radius: .5rem;
    border: none;
    cursor: pointer;
    background-color: #FF5C01;
    color: white;
    margin: 0.5rem;
    text-decoration: none;
}

</style>