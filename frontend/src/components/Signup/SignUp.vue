<script setup>
import { RouterLink } from 'vue-router';

</script>


<template>
    <div>
        <h1 class="heading">SIGN UP</h1>
        <div class="container">
            <RouterLink class="customerSignUp" :to="{ name : 'customer-signup'}" > CUSTOMER/USER </RouterLink>
            
            <RouterLink class="professionalSignUp" :to="{ name : 'proffessional-signup'}">SERVICE PROFFESIONAL</RouterLink>


            <div class="signInLine">
                <p>Already have an account? </p>
                <RouterLink :to="{ name : 'login'}">Sign In</RouterLink>
            </div>
        </div>

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

.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: auto;
    margin-bottom: 1rem;
}

.customerSignUp ,
.professionalSignUp{
    min-width: 350px;
    color: white;
    font-size: 1.5rem;
    font-weight: bolder;
    font-style: italic;
    text-align: center;
    background-image: linear-gradient(to right, #FF5C01 10%, #9D3C06);
    border: none;
    padding: 1.5rem;
    border-radius: 1rem;
    margin-bottom: 2rem;
    cursor: pointer;
    text-decoration: none;
}

.customerSignUp button:hover,
.professionalSignUp button:hover {
    transform: scale(1.04);
    transition: ease-in 0.3s;
}

.signInLine {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: auto;
    margin-bottom: 1rem;
}

.signInLine p {
    color: #FF5C01;
    font-size: 1.5rem;
    font-weight: bolder;
    font-style: italic;
    text-align: center;

}

.signInLine a {
    color: #6A94FF;
    font-size: 1.5rem;
    font-weight: bolder;
    text-align: center;
    text-decoration: none;
    margin-left: 10px;

}

.signInLine a:hover {
    text-decoration: underline;
    transform: scale(1.1);
    transition: ease-in-out 0.2s;
}
</style>