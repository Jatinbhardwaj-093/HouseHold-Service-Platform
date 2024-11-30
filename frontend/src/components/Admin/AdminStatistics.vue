<script setup>
import { ref,onMounted } from 'vue';
import axios from 'axios';
import BarChart from '@/components/Charts/BarChart.vue';
import PieChart from '../Charts/PieChart.vue';
import LineChart from '../Charts/LineChart.vue';

const token = localStorage.getItem('adminToken')

// Main Api call to fetch data
const fetchData = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5000/admin/statistics', {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });
        console.log(response.data)
        const ServiceStatus = response.data.serviceStatus;
        barChartData.value = {
            labels: Object.keys(ServiceStatus),
            datasets: [
                {
                    label: 'Service Requests',
                    backgroundColor: ['rgba(255, 90, 1, 0.8)','rgba(255, 90, 1, 0.6)','rgba(255, 90, 1, 0.4)','rgba(255, 90, 1, 0.4)','rgba(255, 90, 1, 0.4)'],
                    data: Object.values(ServiceStatus),
                    borderColor: 'rgba(255, 90, 1)',
                    borderWidth: 2
                }
            ]
        }

        const ratioOfUsers = response.data.ratioOfUsers;

        pieChartData.value = {
            labels: Object.keys(ratioOfUsers),
            datasets: [
                {
                    label: 'Users',
                    backgroundColor: ['rgba(255, 90, 1, 0.8)', '#252424'],
                    data: Object.values(ratioOfUsers),
                    borderColor: 'rgba(0, 0, 0)',
                    borderWidth: 2
                }
            ]
        }

        const requestsOnDay = response.data.requestsOnDay 

        lineChartData.value = {
            labels: Object.keys(requestsOnDay),
            datasets: [
                {
                    label: 'Service Requests',
                    backgroundColor: 'rgba(255, 90, 1, 1)',
                    borderColor: 'rgba(255, 90, 0.6)',
                    borderWidth: 2,
                    data: Object.values(requestsOnDay),
                    tension: 0.5
                }
            ]
        }

        const completionOnDay = response.data.completionOnDay

        doubleLineChartData.value = {
            labels: Array.from(new Set([...Object.keys(requestsOnDay), ...Object.keys(completionOnDay)])),
            datasets: [
                {
                    label: 'Requested',
                    backgroundColor: 'rgba(255, 90, 1, 1)',
                    borderColor: 'rgba(255, 90, 0.6)',
                    borderWidth:2,
                    data: Object.values(requestsOnDay),
                    tension: 0.5
                },
                {
                    label: 'Completed Requests',
                    backgroundColor: 'white',
                    data: Object.values(completionOnDay),
                    borderColor: 'rgba(255,255,255,0.6)',
                    borderWidth:2,
                    tension: 0.5
                }
            ]
        }

    } catch (error) {
        console.error('Failed to fetch data:', error);
}
}

onMounted(() => {
    fetchData();
})

// Bar chart data(Stats of requests)
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
            text: 'Requests per service',
            color: 'white',
            font: {
                size: 20,
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

// Pie chart data(Customer, Professional in platform)
const pieChartData = ref({
    labels: [],
    datasets: [
        {
            label: 'Users',
            backgroundColor: ['#f87979', '#f87979'],
            data: [],
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
            text: 'Users in platform',
            color: 'white',
            font: {
                size: 20,
                wieght: 800
            },
            textAlign: 'center'
        }
    }
})


// Line chart data(Stats of requests)
const lineChartData = ref({
    labels: [],
    datasets: [
        {
            label: 'Service Requests',
            backgroundColor: '#f87979',
            data: []
        }
    ]
})

const lineChartOptions = ref({
    responsive: true,
    maintainAspectRatio: false,
    layout:{
        padding: {
            left: 20,
            right: 20,
            top: 20,
            bottom: 20
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

// Double line chart data(Everyday requests and completion)
const doubleLineChartData = ref({
    labels: [],
    datasets: [
        {
            label: 'Service Requests',
            backgroundColor: '#f87979',
            data: []
        },
        {
            label: 'Service Completion',
            backgroundColor: '#f87979',
            data: []
        }
    ]
})

const doubleLineChartOptions = ref({
    responsive: true,
    maintainAspectRatio: false,
    layout:{
        padding: {
            left: 20,
            right: 20,
            top: 20,
            bottom: 20
        }
    },
    plugins: {
        legend: {
            display: false
        },
        title: {
            display: true,
            text: 'Requests vs Completion Services',
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
        <LineChart class="line-chart" :chartData="lineChartData" :chartOptions="lineChartOptions" />
        <LineChart class="double-line-chart" :chartData="doubleLineChartData" :chartOptions="doubleLineChartOptions" />
    </div>
</template>

<style scoped>
.grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr 1fr 1fr 1fr;
    grid-template-areas:
        'bar-chart pie-chart'
        'line-chart line-chart'
        'line-chart line-chart'
        'double-line-chart double-line-chart'
        'double-line-chart double-line-chart';
    gap: 1rem;
    width: 90vw;
    margin: auto;
    justify-items: center;
    align-items: center;
    color: rgba(255, 90, 1, 0.8);
}

.bar-chart , .pie-chart ,.line-chart, .double-line-chart {
    height: 100%;
    width: 100%;
}
.bar-chart{ grid-area: bar-chart;}
.pie-chart{ grid-area: pie-chart;}
.line-chart{ grid-area: line-chart;}
.double-line-chart{ grid-area: double-line-chart;}

</style>