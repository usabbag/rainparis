let chart = null;
let currentArrondissement = null;

// Fetch and display weather data
async function fetchWeather(arrondissement) {
    const loading = document.getElementById('loading');
    const content = document.getElementById('content');

    loading.style.display = 'block';
    content.style.display = 'none';
    currentArrondissement = arrondissement;

    try {
        const response = await fetch(`/api/weather/${arrondissement}`);
        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        // Update UI
        document.getElementById('location-name').textContent = getArrondissementName(arrondissement);
        document.getElementById('temp-value').textContent = Math.round(data.temperature);
        document.getElementById('rain-summary').textContent = data.summary;

        // Update chart
        updateChart(data.chart_data);

        // Update last updated time
        document.getElementById('last-updated').textContent = 'Updated just now';

        // Show content
        loading.style.display = 'none';
        content.style.display = 'block';

    } catch (error) {
        console.error('Error fetching weather:', error);
        loading.textContent = 'Failed to load weather data';
    }
}

// Update precipitation chart
function updateChart(chartData) {
    const ctx = document.getElementById('precipitation-chart').getContext('2d');

    // Extract labels and data
    const labels = chartData.map(d => d.time);
    const precipitation = chartData.map(d => d.precipitation);

    // Destroy existing chart if it exists
    if (chart) {
        chart.destroy();
    }

    // Create gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, 200);
    gradient.addColorStop(0, 'rgba(96, 165, 250, 0.3)');
    gradient.addColorStop(1, 'rgba(96, 165, 250, 0.0)');

    // Create new chart
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Precipitation',
                data: precipitation,
                borderColor: '#60a5fa',
                backgroundColor: gradient,
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                pointHoverRadius: 4,
                pointHoverBackgroundColor: '#60a5fa',
                pointHoverBorderColor: 'white',
                pointHoverBorderWidth: 2,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.9)',
                    padding: 12,
                    cornerRadius: 8,
                    titleFont: {
                        size: 13,
                        weight: '500'
                    },
                    bodyFont: {
                        size: 14,
                        weight: '600'
                    },
                    titleColor: '#8b9dc3',
                    bodyColor: '#ffffff',
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderWidth: 1,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            return context.parsed.y.toFixed(2) + ' mm/hr';
                        }
                    }
                }
            },
            scales: {
                x: {
                    display: true,
                    grid: {
                        display: false
                    },
                    ticks: {
                        maxRotation: 0,
                        autoSkip: true,
                        maxTicksLimit: 6,
                        color: '#6b7f9f',
                        font: {
                            size: 12
                        }
                    }
                },
                y: {
                    display: true,
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#6b7f9f',
                        font: {
                            size: 12
                        },
                        callback: function(value) {
                            return value.toFixed(1);
                        }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

// Get arrondissement name from button
function getArrondissementName(num) {
    const button = document.querySelector(`[data-arr="${num}"]`);
    if (button) {
        const number = button.querySelector('.arr-number').textContent;
        const name = button.querySelector('.arr-name').textContent;
        if (num == 0) {
            return `${number} - ${name}`;
        }
        return `${number} - ${name}`;
    }
    const postalCode = num == 0 ? '75000' : `750${num.toString().padStart(2, '0')}`;
    return `${postalCode}`;
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Add click handlers to all arrondissement buttons
    const buttons = document.querySelectorAll('.arr-button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const arr = this.getAttribute('data-arr');
            fetchWeather(arr);
        });
    });

    // Load default weather for Paris overall on page load
    fetchWeather(0);
});
