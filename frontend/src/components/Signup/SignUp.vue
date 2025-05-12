<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
    <div class="signup-container">
        <div class="signup-wrapper">
            <h1 class="heading">SIGN UP</h1>
            <div class="container">
                <div class="signup-options">
                    <RouterLink class="customerSignUp" :to="{ name: 'customer-signup' }">
                        <div class="option-card">
                            <div class="option-icon">👤</div>
                            <h2 class="option-title">Customer</h2>
                            <p class="option-description">Sign up as a service user to find and book professional services for your home</p>
                        </div>
                    </RouterLink>

                    <RouterLink class="professionalSignUp" :to="{ name: 'proffessional-signup' }">
                        <div class="option-card">
                            <div class="option-icon">🛠️</div>
                            <h2 class="option-title">Professional</h2>
                            <p class="option-description">Join as a service professional to offer your skills and grow your business</p>
                        </div>
                    </RouterLink>
                </div>

                <div class="signInLine">
                    <p>Already have an account?</p>
                    <RouterLink :to="{ name: 'login' }">Sign In</RouterLink>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.signup-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: #000;
    padding: 20px;
    background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.9)),
        url('../assets/images/webHomePage.png');
    background-size: cover;
    background-position: center;
}

.signup-wrapper {
    width: 100%;
    max-width: 900px; /* Increased width to accommodate the container */
    padding: 40px 20px;
    border-radius: 20px;
    background-color: rgba(34, 33, 33, 0.7);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(0, 0, 0, 0.1);
}

.icon {
    margin-right: 10px;
    font-size: 1.5rem;
}

.heading {
    text-align: center;
    font-weight: bolder;
    font-size: 3.5rem;
    margin-top: 2rem;
    margin-bottom: 3rem;
    font-style: italic;
    color: #ff5c01;
    text-shadow: 0 2px 5px rgba(255, 92, 1, 0.3);
    letter-spacing: 1px;
}

.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: auto;
    margin-bottom: 3rem;
    padding: 3rem 2rem;
    border-radius: 15px;
    max-width: 800px; /* Increased width to accommodate side-by-side cards */
    width: 100%;
}

.signup-options {
    display: flex;
    justify-content: center;
    flex-direction: row; /* Ensure items are in a row */
    flex-wrap: nowrap; /* Prevent wrapping */
    gap: 2rem;
    width: 100%;
    margin-bottom: 2.5rem;
}

.customerSignUp,
.professionalSignUp {
    text-decoration: none;
    flex: 1;
    width: calc(50% - 1rem); /* Each takes half the width minus gap */
    min-width: 240px;
    transition: all 0.3s ease;
}

.option-card {
    background: rgba(37, 37, 37, 0.7);
    border: 2px solid rgba(255, 92, 1, 0.2);
    border-radius: 15px;
    padding: 2rem 1.5rem;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    box-shadow: 0 8px 20px rgba(255, 92, 1, 0.2);
    transition: all 0.4s ease;
}

.option-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #ff5c01, #ff8f01);
    width: 80px;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    box-shadow: 0 5px 15px rgba(255, 92, 1, 0.3);
}

.option-title {
    color: #ff5c01;
    font-size: 1.8rem;
    margin-bottom: 1rem;
    font-weight: 600;
}

.option-description {
    color: #ddd;
    text-align: center;
    font-size: 1rem;
    line-height: 1.5;
    flex-grow: 1; /* Allow description to expand */
}

.customerSignUp:hover .option-card,
.professionalSignUp:hover .option-card {
    transform: translateY(-10px);
    box-shadow: 0 15px 35px rgba(255, 92, 1, 0.5);
    border-color: rgba(255, 92, 1, 0.6);
    background: rgba(47, 47, 47, 0.8);
}

.signInLine {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: auto;
    margin-top: 0.5rem;
    padding: 15px;
    border-radius: 8px;
    background-color: rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 92, 1, 0.1);
    width: 100%;
    max-width: 350px;
}

.signInLine p {
    color: #ccc;
    font-size: 1.2rem;
    font-weight: 500;
    text-align: center;
}

.signInLine a {
    color: #ff5c01;
    font-size: 1.2rem;
    font-weight: 600;
    text-align: center;
    text-decoration: none;
    margin-left: 10px;
    position: relative;
    padding-bottom: 2px;
}

.signInLine a::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 2px;
    background-color: #ff5c01;
    transition: width 0.3s ease;
}

.signInLine a:hover::after {
    width: 100%;
}

.signInLine a:hover {
    text-shadow: 0 0 8px rgba(255, 92, 1, 0.5);
    transition: all 0.3s ease;
}

/* Media query for smaller screens */
@media screen and (max-width: 768px) {
    .signup-options {
        flex-direction: column;
        align-items: center;
    }
    
    .customerSignUp,
    .professionalSignUp {
        width: 100%;
        max-width: 400px;
    }

    .option-card {
        min-height: 280px;
    }
    
    .heading {
        font-size: 2.8rem;
        margin-bottom: 2rem;
    }
}
</style>
