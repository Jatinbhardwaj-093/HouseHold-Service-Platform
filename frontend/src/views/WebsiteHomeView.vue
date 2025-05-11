<script setup>
// Import required components and reactive data
import { ref } from 'vue'

// Services offered
const services = ref([
    { name: 'Cleaning', icon: '🧹', description: 'Professional home cleaning services' },
    { name: 'Plumbing', icon: '🔧', description: 'Expert plumbing repair and installation' },
    { name: 'Electrical', icon: '⚡', description: 'Electrical repairs and installations' },
    { name: 'Gardening', icon: '🌱', description: 'Lawn care and gardening services' }
])
</script>

<template>
    <div class="home-container">
        <!-- Navigation Bar -->
        <nav class="navbar">
            <div class="logo">
                <span class="logo-icon">🏠</span>
                <span class="logo-text">HomeServe</span>
            </div>
            <div class="nav-buttons">
                <RouterLink :to="{ name: 'login' }"
                    ><button class="nav-btn login">Login</button></RouterLink
                >
                <RouterLink :to="{ name: 'signup' }"
                    ><button class="nav-btn signup">Sign Up</button></RouterLink
                >
            </div>
        </nav>

        <!-- Hero Banner -->
        <section class="hero-banner">
            <div class="hero-content">
                <h1>Expert Home Services<br />On Demand</h1>
                <p>Professional, reliable, and affordable home services at your doorstep</p>
                <RouterLink :to="{ name: 'signup' }"
                    ><button class="cta-button">Get Started</button></RouterLink
                >
            </div>
            <div class="overlay"></div>
        </section>

        <!-- Services Section -->
        <section class="services-section">
            <div class="section-header">
                <h2>Our Services</h2>
                <p>Find the right service for all your home needs</p>
            </div>

            <div class="services-grid">
                <div v-for="(service, index) in services" :key="index" class="service-card">
                    <div class="service-icon">{{ service.icon }}</div>
                    <h3>{{ service.name }}</h3>
                    <p>{{ service.description }}</p>
                    <button class="book-now">Book Now</button>
                </div>
            </div>
        </section>

        <!-- How It Works -->
        <section class="how-it-works">
            <div class="section-header">
                <h2>How It Works</h2>
                <p>Book a service in 3 simple steps</p>
            </div>

            <div class="steps-container">
                <div class="step">
                    <div class="step-number">1</div>
                    <h3>Choose a Service</h3>
                    <p>Browse through our range of home services</p>
                </div>
                <div class="step-arrow">→</div>
                <div class="step">
                    <div class="step-number">2</div>
                    <h3>Book Appointment</h3>
                    <p>Select a convenient date and time</p>
                </div>
                <div class="step-arrow">→</div>
                <div class="step">
                    <div class="step-number">3</div>
                    <h3>Service Delivered</h3>
                    <p>Our professionals will handle the rest</p>
                </div>
            </div>
        </section>

        <!-- Trust Section -->
        <section class="trust-section">
            <div class="trust-content">
                <h2>Why Choose Us</h2>
                <div class="trust-points">
                    <div class="trust-point">
                        <span class="trust-icon">✓</span>
                        <div>
                            <h3>Verified Professionals</h3>
                            <p>All our service providers are thoroughly vetted</p>
                        </div>
                    </div>
                    <div class="trust-point">
                        <span class="trust-icon">✓</span>
                        <div>
                            <h3>Quality Guaranteed</h3>
                            <p>Satisfaction guaranteed or we'll make it right</p>
                        </div>
                    </div>
                    <div class="trust-point">
                        <span class="trust-icon">✓</span>
                        <div>
                            <h3>Transparent Pricing</h3>
                            <p>No hidden costs or surprise fees</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="footer">
            <div class="footer-content">
                <p>&copy; .... HomeServe. All rights reserved.</p>
                <div class="footer-links">
                    <a href="#">About Us</a>
                    <a href="#">Contact</a>
                    <a href="#">Terms of Service</a>
                    <a href="#">Privacy Policy</a>
                </div>
            </div>
        </footer>
    </div>
</template>

<style scoped>
/* Global Styles */
.home-container {
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    color: #fff;
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
    background-color: #000;
}

/* Navigation Bar */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 40px;
    background-color: #000;
    border-bottom: 1px solid rgba(255, 92, 1, 0.3);
    box-shadow: 0 2px 10px rgba(255, 92, 1, 0.1);
    position: sticky;
    top: 0;
    z-index: 100;
}

.logo {
    display: flex;
    align-items: center;
    font-weight: bold;
}

.logo-icon {
    font-size: 24px;
    margin-right: 10px;
}

.logo-text {
    font-size: 22px;
    color: #ff5c01;
}

.nav-buttons {
    display: flex;
    gap: 15px;
}

.nav-btn {
    padding: 8px 20px;
    border-radius: 4px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
    font-size: 14px;
}

.login {
    background-color: transparent;
    color: #ff5c01;
    border: 1px solid #ff5c01;
}

.signup {
    background-color: #ff5c01;
    color: white;
}

.nav-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* Hero Banner */
.hero-banner {
    position: relative;
    height: 500px;
    background-image: url('../assets/images/webHomePage.png');
    background-size: cover;
    background-position: center;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    padding-left: 80px;
    color: white;
}

.overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        90deg,
        rgba(0, 0, 0, 0.7) 30%,
        rgba(0, 0, 0, 0.4) 70%,
        rgba(0, 0, 0, 0.1) 100%
    );
    z-index: 1;
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 600px;
}

.hero-banner h1 {
    font-size: 3.2rem;
    font-weight: 800;
    margin-bottom: 20px;
    line-height: 1.2;
}

.hero-banner p {
    font-size: 1.2rem;
    margin-bottom: 30px;
    opacity: 0.9;
}

.cta-button {
    padding: 14px 32px;
    background-color: #ff5c01;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.cta-button:hover {
    background-color: #e54e00;
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

/* Section Styling */
.section-header {
    text-align: center;
    margin-bottom: 50px;
}

.section-header h2 {
    font-size: 2.5rem;
    color: #ff5c01;
    margin-bottom: 10px;
    text-shadow: 0 2px 5px rgba(255, 92, 1, 0.2);
}

.section-header p {
    font-size: 1.1rem;
    color: #ccc;
    max-width: 600px;
    margin: 0 auto;
}

/* Services Section */
.services-section {
    padding: 80px 40px;
    background-color: #111;
    border-top: 1px solid rgba(255, 92, 1, 0.3);
    border-bottom: 1px solid rgba(255, 92, 1, 0.3);
}

.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 30px;
    max-width: 1200px;
    margin: 0 auto;
}

.service-card {
    background-color: #222;
    border-radius: 8px;
    padding: 30px;
    text-align: center;
    border: 1px solid rgba(255, 92, 1, 0.2);
    box-shadow: 0 5px 15px rgba(255, 92, 1, 0.08);
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
}

.service-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 30px rgba(255, 92, 1, 0.15);
    border-color: rgba(255, 92, 1, 0.5);
}

.service-icon {
    font-size: 3.5rem;
    margin-bottom: 20px;
    background: -webkit-linear-gradient(#ff5c01, #ff8f01);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

.service-card h3 {
    font-size: 1.4rem;
    margin-bottom: 10px;
    color: #ff5c01;
}

.service-card p {
    color: #ccc;
    margin-bottom: 20px;
    flex-grow: 1;
}

.book-now {
    padding: 10px;
    background-color: #ff5c01;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
}

.book-now:hover {
    background-color: #e54e00;
}

/* How It Works Section */
.how-it-works {
    padding: 80px 40px;
    background-color: #000;
}

.steps-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    max-width: 1000px;
    margin: 0 auto;
}

.step {
    flex: 1;
    text-align: center;
    padding: 30px 25px;
    background-color: #111;
    border-radius: 8px;
    border: 1px solid rgba(255, 92, 1, 0.2);
    box-shadow: 0 5px 15px rgba(255, 92, 1, 0.08);
    transition: all 0.3s ease;
}

.step:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(255, 92, 1, 0.15);
    border-color: rgba(255, 92, 1, 0.5);
}

.step-number {
    width: 55px;
    height: 55px;
    background-color: #ff5c01;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0 auto 20px;
    box-shadow: 0 0 15px rgba(255, 92, 1, 0.5);
}

.step h3 {
    font-size: 1.3rem;
    margin-bottom: 10px;
    color: #ff5c01;
}

.step p {
    color: #ccc;
}

.step-arrow {
    font-size: 2.5rem;
    color: #ff5c01;
    text-shadow: 0 0 10px rgba(255, 92, 1, 0.3);
}

/* Trust Section */
.trust-section {
    padding: 80px 40px;
    background-color: #111;
    border-top: 1px solid rgba(255, 92, 1, 0.3);
}

.trust-content {
    max-width: 1000px;
    margin: 0 auto;
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 12px;
    padding: 40px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 92, 1, 0.15);
}

.trust-content h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 50px;
    color: #ff5c01;
    text-shadow: 0 2px 5px rgba(255, 92, 1, 0.2);
}

.trust-points {
    display: flex;
    flex-direction: column;
    gap: 30px;
}

.trust-point {
    display: flex;
    align-items: flex-start;
    gap: 20px;
    padding: 15px;
    border-radius: 8px;
    background-color: rgba(255, 92, 1, 0.05);
    transition: all 0.3s ease;
}

.trust-point:hover {
    background-color: rgba(255, 92, 1, 0.1);
    transform: translateX(5px);
}

.trust-icon {
    width: 45px;
    height: 45px;
    background: linear-gradient(135deg, #ff5c01, #ff8f01);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    font-weight: bold;
    flex-shrink: 0;
    box-shadow: 0 5px 15px rgba(255, 92, 1, 0.3);
}

.trust-point h3 {
    margin-bottom: 8px;
    color: #ff5c01;
    font-size: 1.3rem;
}

.trust-point p {
    color: #ccc;
}

/* Footer */
.footer {
    background-color: #111;
    color: white;
    padding: 40px;
    border-top: 1px solid rgba(255, 92, 1, 0.3);
}

.footer-content {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.footer p {
    color: #999;
}

.footer-links {
    display: flex;
    gap: 30px;
}

.footer a {
    color: #ccc;
    text-decoration: none;
    transition: all 0.3s ease;
    position: relative;
    padding-bottom: 3px;
}

.footer a::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 1px;
    background-color: #ff5c01;
    transition: width 0.3s ease;
}

.footer a:hover {
    color: #ff5c01;
}

.footer a:hover::after {
    width: 100%;
}

/* Responsive Design */
@media (max-width: 992px) {
    .navbar {
        padding: 15px 20px;
    }

    .hero-banner {
        padding-left: 40px;
    }

    .hero-banner h1 {
        font-size: 2.8rem;
    }

    .steps-container {
        flex-direction: column;
        gap: 30px;
    }

    .step-arrow {
        transform: rotate(90deg);
    }

    .footer-content {
        flex-direction: column;
        gap: 20px;
    }
}

@media (max-width: 768px) {
    .hero-banner {
        padding: 0 20px;
        text-align: center;
        justify-content: center;
    }

    .overlay {
        background: linear-gradient(to bottom, rgba(0, 0, 0, 0.7) 0%, rgba(0, 0, 0, 0.6) 100%);
    }

    .services-grid {
        grid-template-columns: 1fr;
        max-width: 400px;
        margin: 0 auto;
    }

    .trust-point {
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
}
</style>
