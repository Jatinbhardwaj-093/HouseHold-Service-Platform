<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import BarChart from '@/components/Charts/BarChart.vue'
import PieChart from '../Charts/PieChart.vue'

//Main Api call to fetch data
const token = localStorage.getItem('customerToken')
const fetchChartData = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5000/customer/statistics', {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })
        const data = response.data.AskedServices

        barChartData.value = {
            labels: data.map((service) => service.name),
            datasets: [
                {
                    label: data.map((service) => service.name),
                    backgroundColor: [
                        'rgba(255, 90, 1, 0.8)',
                        'rgba(255, 90, 1, 0.6)',
                        'rgba(255, 90, 1, 0.4)',
                        'rgba(255, 90, 1, 0.2)',
                        'rgba(255, 90, 1)'
                    ],
                    borderColor: 'rgba(255, 90, 1)',
                    borderWidth: 2,
                    data: data.map((service) => service.requestCount)
                }
            ]
        }

        const serviceStatus = response.data.ServiceStatus
        const Labels = Object.keys(serviceStatus)
        const val = Object.values(serviceStatus)
        pieChartData.value = {
            labels: Labels,
            datasets: [
                {
                    label: 'Service Requests',
                    backgroundColor: ['rgba(255, 90, 1, 0.8)', '#252424', 'rgba(255,255,255,0.4)'],
                    data: val
                }
            ]
        }
    } catch (error) {
        console.error('Error fetching data:', error)
    }
}

onMounted(() => {
    fetchChartData()
})

// Bar Chart(Different type of service requests)
const barChartData = ref({
    labels: [],
    datasets: [
        {
            label: 'Service Requests',
            backgroundColor: [
                'rgba(255, 90, 1, 0.8)',
                'rgba(255, 90, 1, 0.6)',
                'rgba(255, 90, 1, 0.4)',
                'rgba(255, 90, 1, 0.4)',
                'rgba(255, 90, 1, 0.4)'
            ],
            data: []
        }
    ]
})

const barChartOptions = ref({
    responsive: true,
    maintainAspectRatio: false,
    barThickness: 100,
    scales: {
        x: {
            grid: {
                display: true,
                color: 'rgba(255, 99, 132, 0.4)',
                lineWidth: 1
            },
            ticks: {
                color: 'white',
                font: {
                    size: 16
                }
            }
            
        },
        y: {
            grid: {
                display: true,
                color: 'rgba(54, 162, 235, 0.4)',
                lineWidth: 1
            },
            ticks: {
                color: 'white',
                font: {
                    size: 16
                }
            }
        }
    },
    plugins: {
        legend: {
            display: false,
            position: 'top',
            labels: {
                display: false,
                color: 'white',
                font: {
                    size: 16,
                    wieght: 800
                }
            }
        },
        title: {
            display: true,
            text: 'Services Requests',
            color: 'white',
            font: {
                size: 30,
                wieght: 800
            }
        }
    }
})

// Pie Chart(Current state of service requests)
const pieChartData = ref({
    labels: [],
    datasets: [
        {
            label: 'Service Requests',
            backgroundColor: ['rgba(255, 90, 1, 0.8)', '#252424'],
            borderWidth: 2.5,
            borderColor: 'black',
            data: []
        }
    ]
})

const pieChartOptions = ref({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: true,
            position: 'top',
            labels: {
                color: 'white',
                font: {
                    size: 16,
                    wieght: 800
                }
            }
        },
        title: {
            display: true,
            text: 'Services Status',
            color: 'white',
            font: {
                size: 30,
                wieght: 800
            },
            textAlign: 'center'
        }
    }
})
</script>

<template>
    <div class="grid">
        <BarChart class="bar-chart" :chartData="barChartData" :chartOptions="barChartOptions" />
        <PieChart class="pie-chart" :chartData="pieChartData" :chartOptions="pieChartOptions" />
    </div>
</template>

<style scoped>
.grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 1rem;
    height: 80vh;
    width: 95vw;
    margin: auto;
    justify-items: center;
    align-items: center;
    color: rgba(255, 90, 1, 0.8);
}

.bar-chart,
.pie-chart {
    height: 100%;
    width: 100%;
}
</style>
