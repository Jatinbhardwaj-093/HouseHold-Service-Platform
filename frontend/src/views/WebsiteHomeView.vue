<script setup>

</script>


<template>
    <div>
        <h1 class="heading" id="typewriter">Welcome to Home Service Application</h1>
        <div class="imageHolder">
            <img class="homeImage" src="../assets/images/websiteHomePage.jpg" alt="">
        </div>
        <div class="button">
            <RouterLink class="box" :to="{ name : 'login'}"><button class="btn">Login</button></RouterLink>
            <RouterLink class="box" :to="{ name : 'signup'}"><button class="btn">Sign Up</button></RouterLink>
        </div>
    </div>
</template>

<style scoped>
@keyframes typewriter {
    from {
        width: 0;
    }
    to {
        width: 100%;
    }
}

@keyframes blinkCursor {
    from {
        border-right-color: rgba(255, 92, 1, 1);
    }
    to {
        border-right-color: transparent;
    }
}

.heading {
    text-align: center;
    font-weight: bolder;
    font-size: 3.5rem;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    font-style: italic;
    color: #FF5C01;
    overflow: hidden;
    white-space: nowrap;
    border-right: 4px solid #FF5C01;
    animation: typewriter 3s steps(30, end), blinkCursor 0.5s step-end infinite;
}


.imageHolder {
    height: 420px;
    width: 600px;
    padding: 1rem;
    margin: auto;
    border-radius: 2rem;
}

.homeImage {
    height: 100%;
    width: 100%;
    border-radius: 2rem;
}

.button{
    display: flex;
    justify-content: center;
    margin-top: 1rem;
}

.btn {
    width: 15rem;
    font-size: 2rem;
    padding: .25rem;
    border-radius: .75rem;
    border: none;
    cursor: pointer;
    background-color: #FF5C01;
    color: white;
    margin: 1rem;
    text-decoration: none;
}

.btn:hover {
    transform: scale(1.05);
    transition: ease-in-out 0.5;
}
</style>