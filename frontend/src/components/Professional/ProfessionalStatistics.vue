<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import BarChart from '@/components/Charts/BarChart.vue'
import PieChart from '../Charts/PieChart.vue'
import LineChart from '../Charts/LineChart.vue'

const token = localStorage.getItem('professionalToken')

// Main api call function
const fetchData = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5000/professional/statistics', {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })
        const DifferentPincode = response.data.DifferentPincode
        console.log(DifferentPincode)
        barChartData.value = {
            labels: DifferentPincode.map((pincode) => pincode.pincode),
            datasets: [
                {
                    label: DifferentPincode.map((pincode) => pincode.pincode),
                    data: DifferentPincode.map((pincode) => pincode.requestCount),
                    backgroundColor: [
                        'rgba(255, 90, 1, 0.8)',
                        'rgba(255, 90, 1, 0.6)',
                        'rgba(255, 90, 1, 0.4)',
                        'rgba(255, 90, 1, 0.2)',
                        'rgba(255, 90, 1)'
                    ],
                    borderColor: 'rgba(255, 90, 1)',
                    borderWidth: 2
                }
            ]
        }

        const ServiceStatus = response.data.ServiceStatus
        const Labels = Object.keys(ServiceStatus)
        const val = Object.values(ServiceStatus)
        pieChartData.value = {
            labels: Labels,
            datasets: [
                {
                    label: 'Service Requests',
                    backgroundColor: ['rgba(255, 90, 1, 0.8)', '#252424', 'rgba(255,255,255,0.4)'],
                    data: val,
                    borderColor: 'rgba(0, 0, 0)',
                    borderWidth: 2
                }
            ]
        }

        const RequestDates = response.data.requestDates
        lineChartData.value = {
            labels: Object.keys(RequestDates),
            datasets: [
                {
                    labels: 'Sales',
                    data: Object.values(RequestDates),
                    backgroundColor: 'rgba(255, 90, 1, 1)',
                    borderColor: 'rgba(255, 90, 1, 1)',
                    borderWidth: 2,
                    tension: 0.4
                }
            ]
        }
    } catch (error) {
        console.error(error)
    }
}

onMounted(() => {
    fetchData()
})
// Bar chart data(Different area(pincode) of requests)
const barChartData = ref({
    labels: [],
    datasets: [
        {
            label: 'Service Requests',
            backgroundColor: '#f87979',
            data: []
        }
    ]
})

const barChartOptions = ref({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: false
        },
        title: {
            display: true,
            text: 'Service requests from different area',
            color: 'white',
            font: {
                size: 16,
                wieght: 800
            }
        }
    },
    barThickness: 50,
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
                    size: 10
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
                    size: 10
                }
            }
        }
    }
})

// Pie chart data(Current state of service requests)
const pieChartData = ref({
    labels: [],
    datasets: [
        {
            label: 'Service Requests',
            backgroundColor: ['#f87979', '#f87979'],
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
                    size: 14,
                    wieght: 800
                }
            }
        },
        title: {
            display: true,
            text: 'Current state of service requests',
            color: 'white',
            font: {
                size: 16,
                wieght: 800
            },
            textAlign: 'center'
        }
    }
})

// Line chart data
const lineChartData = ref({
    labels: [],
    datasets: [
        {
            label: 'Sales',
            data: [],
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderWidth: 2,
            tension: 0.4
        }
    ]
})

const lineChartOptions = ref({
    responsive: true,
    maintainAspectRatio: false,
    layouts:{
        margin: {
            bottom: 20,
        }
    },
    plugins: {
        legend: {
            display: false
        },
        title: {
            display: true,
            text: 'Requests per day',
            color: 'white',
            font: {
                size: 28,
                wieght: 800
            }
        }
    },
    scales: {
        x: {
            ticks: {
                color: 'white'
            },
            grid: {
                display: true,
                color: 'rgba(0,0,0,0.2)',
                lineWidth: 1
            },
            beginAtZero: true
        },
        y: {
            ticks: {
                color: 'white'
            },
            grid: {
                display: true,
                color: 'rgba(0,0,0,0.2)',
                lineWidth: 1
            },
            beginAtZero: true
        }
    }
})
</script>

<template>
    <div class="grid">
        <BarChart class="bar-chart" :chartData="barChartData" :chartOptions="barChartOptions" />
        <PieChart class="pie-chart" :chartData="pieChartData" :chartOptions="pieChartOptions" />
        <LineChart
            class="line-chart"
            :chartData="lineChartData"
            :chart-options="lineChartOptions"
        />
    </div>
</template>

<style scoped>
.grid {
    display: grid;
    grid-template-areas:
        'pie-chart line-chart'
        'bar-chart line-chart';
    grid-template-columns: 1fr 2fr;
    grid-template-rows: 270px 350px;
    gap: 1rem;
    height: 80vh;
    width: 95vw;
    margin: auto;
    justify-items: center;
    align-items: center;
}

.bar-chart {
    grid-area: bar-chart;
    height: 100%;
    width: 100%;
}

.pie-chart {
    grid-area: pie-chart;
    height: 100%;
    width: 100%;
}

.line-chart {
    grid-area: line-chart;
    height: 100%;
    width: 100%;
}
</style>
