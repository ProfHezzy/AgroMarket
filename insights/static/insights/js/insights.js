// Insights Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    initializeCharts();
    initializeFilters();
    initializeExportFunctions();
    initializeRealTimeUpdates();
});

// Global chart instances
let charts = {
    priceChart: null,
    salesChart: null,
    categoryChart: null,
    sparklines: []
};

function initializeDashboard() {
    // Animate dashboard elements on load
    const elements = document.querySelectorAll('.stat-card, .chart-container, .sidebar-card');
    elements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            element.style.transition = 'all 0.6s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize responsive handlers
    initializeResponsiveHandlers();
}

function initializeCharts() {
    // Price Trends Chart
    const priceCtx = document.getElementById('price-trends-chart');
    if (priceCtx) {
        charts.priceChart = new Chart(priceCtx.getContext('2d'), {
            type: 'line',
            data: {
                labels: generateDateLabels(30),
                datasets: [{
                    label: 'Average Price',
                    data: generateMockPriceData(30),
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#10b981',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6
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
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        borderColor: '#10b981',
                        borderWidth: 1,
                        cornerRadius: 8,
                        displayColors: false,
                        callbacks: {
                            label: function(context) {
                                return `Price: $${context.parsed.y.toFixed(2)}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#6b7280'
                        }
                    },
                    y: {
                        beginAtZero: false,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            color: '#6b7280',
                            callback: function(value) {
                                return '$' + value.toFixed(2);
                            }
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                animation: {
                    duration: 2000,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }

    // Sales Volume Chart
    const salesCtx = document.getElementById('sales-volume-chart');
    if (salesCtx) {
        charts.salesChart = new Chart(salesCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: generateDateLabels(30),
                datasets: [{
                    label: 'Sales Volume',
                    data: generateMockSalesData(30),
                    backgroundColor: '#3b82f6',
                    borderColor: '#2563eb',
                    borderWidth: 1,
                    borderRadius: 4,
                    borderSkipped: false
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
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        borderColor: '#3b82f6',
                        borderWidth: 1,
                        cornerRadius: 8,
                        displayColors: false,
                        callbacks: {
                            label: function(context) {
                                return `Sales: ${context.parsed.y} units`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#6b7280'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            color: '#6b7280'
                        }
                    }
                },
                animation: {
                    duration: 2000,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }

    // Category Distribution Chart
    const categoryCtx = document.getElementById('category-pie-chart');
    if (categoryCtx) {
        charts.categoryChart = new Chart(categoryCtx.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Fresh Produce', 'Grains', 'Dairy', 'Equipment', 'Seeds', 'Organic'],
                datasets: [{
                    data: [35, 25, 15, 10, 8, 7],
                    backgroundColor: [
                        '#10b981', '#3b82f6', '#f59e0b', '#ef4444', 
                        '#8b5cf6', '#06b6d4'
                    ],
                    borderColor: '#ffffff',
                    borderWidth: 3,
                    hoverBorderWidth: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '60%',
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        cornerRadius: 8,
                        displayColors: true,
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${label}: ${percentage}%`;
                            }
                        }
                    }
                },
                animation: {
                    animateRotate: true,
                    duration: 2000,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }

    // Initialize sparkline charts
    initializeSparklines();
}

function initializeSparklines() {
    const sparklineElements = document.querySelectorAll('.trend-sparkline');
    
    sparklineElements.forEach((canvas, index) => {
        const ctx = canvas.getContext('2d');
        const data = generateSparklineData();
        
        const sparklineChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map((_, i) => i),
                datasets: [{
                    data: data,
                    borderColor: data[data.length - 1] > data[0] ? '#10b981' : '#ef4444',
                    borderWidth: 2,
                    pointRadius: 0,
                    pointHoverRadius: 0,
                    tension: 0.4
                }]
            },
            options: {
                responsive: false,
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                },
                scales: {
                    x: { display: false },
                    y: { display: false }
                },
                elements: {
                    point: { radius: 0 }
                },
                animation: {
                    duration: 1000,
                    delay: index * 100
                }
            }
        });
        
        charts.sparklines.push(sparklineChart);
    });
}

function initializeFilters() {
    const dateRangeSelect = document.getElementById('date-range');
    const categorySelect = document.getElementById('category-filter');
    
    if (dateRangeSelect) {
        dateRangeSelect.addEventListener('change', function() {
            updateDashboard();
        });
    }
    
    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            updateDashboard();
        });
    }
    
    // Initialize search functionality
    const searchInput = document.querySelector('input[placeholder*="Search"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                filterTable(this.value);
            }, 300);
        });
    }
}

function initializeExportFunctions() {
    // Export button handlers
    const exportButtons = document.querySelectorAll('[onclick*="exportData"]');
    exportButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const format = this.textContent.toLowerCase().includes('csv') ? 'csv' : 
                          this.textContent.toLowerCase().includes('pdf') ? 'pdf' : 'json';
            exportData(format);
        });
    });
}

function initializeRealTimeUpdates() {
    // Simulate real-time updates every 30 seconds
    setInterval(() => {
        updateRealTimeData();
    }, 30000);
    
    // Update timestamp
    updateTimestamp();
    setInterval(updateTimestamp, 60000);
}

function initializeTooltips() {
    // Add tooltips to various elements
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function initializeResponsiveHandlers() {
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            resizeCharts();
        }, 250);
    });
}

// Data Generation Functions
function generateDateLabels(days) {
    const labels = [];
    const today = new Date();
    
    for (let i = days - 1; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        labels.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
    }
    
    return labels;
}

function generateMockPriceData(days) {
    const data = [];
    let basePrice = 25;
    
    for (let i = 0; i < days; i++) {
        basePrice += (Math.random() - 0.5) * 3;
        basePrice = Math.max(15, Math.min(40, basePrice));
        data.push(parseFloat(basePrice.toFixed(2)));
    }
    
    return data;
}

function generateMockSalesData(days) {
    const data = [];
    
    for (let i = 0; i < days; i++) {
        const sales = Math.floor(Math.random() * 100) + 20;
        data.push(sales);
    }
    
    return data;
}

function generateSparklineData() {
    const data = [];
    let value = 50;
    
    for (let i = 0; i < 10; i++) {
        value += (Math.random() - 0.5) * 10;
        value = Math.max(20, Math.min(80, value));
        data.push(Math.round(value));
    }
    
    return data;
}

// Dashboard Update Functions
function updateDashboard() {
    const dateRange = document.getElementById('date-range')?.value || '30';
    const category = document.getElementById('category-filter')?.value || '';
    
    showLoadingState();
    
    // Simulate API call
    setTimeout(() => {
        updateChartsWithNewData(dateRange, category);
        updateStatCards();
        hideLoadingState();
        showNotification('Dashboard updated successfully!', 'success');
    }, 1500);
}

function updateChartsWithNewData(dateRange, category) {
    const days = parseInt(dateRange);
    
    // Update price chart
    if (charts.priceChart) {
        charts.priceChart.data.labels = generateDateLabels(days);
        charts.priceChart.data.datasets[0].data = generateMockPriceData(days);
        charts.priceChart.update('active');
    }
    
    // Update sales chart
    if (charts.salesChart) {
        charts.salesChart.data.labels = generateDateLabels(days);
        charts.salesChart.data.datasets[0].data = generateMockSalesData(days);
        charts.salesChart.update('active');
    }
    
    // Update category chart if no specific category is selected
    if (!category && charts.categoryChart) {
        const newData = [
            Math.floor(Math.random() * 40) + 20,
            Math.floor(Math.random() * 30) + 15,
            Math.floor(Math.random() * 20) + 10,
            Math.floor(Math.random() * 15) + 5,
            Math.floor(Math.random() * 12) + 3,
            Math.floor(Math.random() * 10) + 2
        ];
        charts.categoryChart.data.datasets[0].data = newData;
        charts.categoryChart.update('active');
    }
}

function updateStatCards() {
    const statCards = document.querySelectorAll('.stat-card');
    
    statCards.forEach(card => {
        const valueElement = card.querySelector('.text-2xl');
        if (valueElement) {
            const currentValue = valueElement.textContent;
            let newValue;
            
            if (currentValue.includes('$')) {
                newValue = '$' + (Math.random() * 100 + 50).toFixed(2);
            } else {
                newValue = Math.floor(Math.random() * 1000 + 100).toString();
            }
            
            animateValue(valueElement, currentValue, newValue);
        }
    });
}

function updateRealTimeData() {
    // Update sparklines
    charts.sparklines.forEach(chart => {
        const newData = generateSparklineData();
        chart.data.datasets[0].data = newData;
        chart.data.datasets[0].borderColor = newData[newData.length - 1] > newData[0] ? '#10b981' : '#ef4444';
        chart.update('none');
    });
    
    // Update trend indicators
    updateTrendIndicators();
}

function updateTrendIndicators() {
    const trendItems = document.querySelectorAll('.trend-indicator');
    
    trendItems.forEach(item => {
        const change = (Math.random() - 0.5) * 20;
        const percentage = Math.abs(change).toFixed(1);
        const icon = item.querySelector('i');
        const span = item.querySelector('span');
        
        if (change > 0) {
            item.className = 'trend-indicator up';
            icon.className = 'fas fa-arrow-up';
            span.textContent = `+${percentage}%`;
        } else if (change < -5) {
            item.className = 'trend-indicator down';
            icon.className = 'fas fa-arrow-down';
            span.textContent = `-${percentage}%`;
        } else {
            item.className = 'trend-indicator stable';
            icon.className = 'fas fa-arrow-right';
            span.textContent = `${percentage}%`;
        }
    });
}

// Chart Type Switching
function updateChart(chartType, newType) {
    const buttons = document.querySelectorAll('.chart-type-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.closest('.chart-type-btn').classList.add('active');
    
    if (chartType === 'price' && charts.priceChart) {
        charts.priceChart.config.type = newType;
        charts.priceChart.update();
    } else if (chartType === 'sales' && charts.salesChart) {
        charts.salesChart.config.type = newType;
        charts.salesChart.update();
    }
}

// Export Functions
function exportData(format = 'csv') {
    showNotification(`Preparing ${format.toUpperCase()} export...`, 'info');
    
    const data = collectDashboardData();
    
    setTimeout(() => {
        if (format === 'csv') {
            downloadCSV(data);
        } else if (format === 'pdf') {
            generatePDFReport(data);
        } else {
            downloadJSON(data);
        }
        
        showNotification(`${format.toUpperCase()} export completed!`, 'success');
    }, 2000);
}

function collectDashboardData() {
    return {
        timestamp: new Date().toISOString(),
        priceData: charts.priceChart?.data || null,
        salesData: charts.salesChart?.data || null,
        categoryData: charts.categoryChart?.data || null,
        filters: {
            dateRange: document.getElementById('date-range')?.value,
            category: document.getElementById('category-filter')?.value
        }
    };
}

function downloadCSV(data) {
    const csv = convertToCSV(data);
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `agromarket-insights-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
}

function downloadJSON(data) {
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `agromarket-insights-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    window.URL.revokeObjectURL(url);
}

function generatePDFReport(data) {
    // This would integrate with a PDF library like jsPDF
    showNotification('PDF generation feature coming soon!', 'info');
}

function convertToCSV(data) {
    let csv = 'Date,Price,Sales Volume\n';
    
    if (data.priceData && data.salesData) {
        const labels = data.priceData.labels || [];
        const prices = data.priceData.datasets[0]?.data || [];
        const sales = data.salesData.datasets[0]?.data || [];
        
        for (let i = 0; i < labels.length; i++) {
            csv += `${labels[i]},${prices[i] || 0},${sales[i] || 0}\n`;
        }
    }
    
    return csv;
}

// Table Functions
function filterTable(searchTerm) {
    const rows = document.querySelectorAll('.table-row');
    const term = searchTerm.toLowerCase();
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        if (text.includes(term)) {
            row.style.display = '';
            row.style.animation = 'fadeIn 0.3s ease';
        } else {
            row.style.display = 'none';
        }
    });
}

// UI Helper Functions
function showLoadingState() {
    const chartContainers = document.querySelectorAll('.chart-container');
    chartContainers.forEach(container => {
        container.classList.add('chart-loading');
        
        if (!container.querySelector('.loading-overlay')) {
            const overlay = document.createElement('div');
            overlay.className = 'loading-overlay';
            overlay.innerHTML = '<div class="loading-spinner"></div>';
            container.appendChild(overlay);
        }
    });
}

function hideLoadingState() {
    const chartContainers = document.querySelectorAll('.chart-container');
    chartContainers.forEach(container => {
        container.classList.remove('chart-loading');
        const overlay = container.querySelector('.loading-overlay');
        if (overlay) {
            overlay.remove();
        }
    });
}

function animateValue(element, startValue, endValue) {
    const startNum = parseFloat(startValue.replace(/[^0-9.-]+/g, ''));
    const endNum = parseFloat(endValue.replace(/[^0-9.-]+/g, ''));
    const duration = 1000;
    const startTime = performance.now();
    
    function updateValue(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const currentNum = startNum + (endNum - startNum) * easeOutQuart(progress);
        
        if (endValue.includes('$')) {
            element.textContent = '$' + currentNum.toFixed(2);
        } else {
            element.textContent = Math.round(currentNum).toString();
        }
        
        if (progress < 1) {
            requestAnimationFrame(updateValue);
        }
    }
    
    requestAnimationFrame(updateValue);
}

function easeOutQuart(t) {
    return 1 - Math.pow(1 - t, 4);
}

function resizeCharts() {
    Object.values(charts).forEach(chart => {
        if (chart && typeof chart.resize === 'function') {
            chart.resize();
        }
    });
}

function updateTimestamp() {
    const timestampElements = document.querySelectorAll('.last-updated');
    const now = new Date().toLocaleString();
    
    timestampElements.forEach(element => {
        element.textContent = `Last updated: ${now}`;
    });
}

function showTooltip(event) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = event.target.dataset.tooltip;
    tooltip.style.cssText = `
        position: absolute;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 12px;
        z-index: 1000;
        pointer-events: none;
    `;
    
    document.body.appendChild(tooltip);
    
    const rect = event.target.getBoundingClientRect();
    tooltip.style.left = rect.left + rect.width / 2 - tooltip.offsetWidth / 2 + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
    
    event.target._tooltip = tooltip;
}

function hideTooltip(event) {
    if (event.target._tooltip) {
        event.target._tooltip.remove();
        delete event.target._tooltip;
    }
}

function generateReport() {
    showNotification('Generating comprehensive report...', 'info');
    
    setTimeout(() => {
        showNotification('Report generated successfully!', 'success');
        exportData('pdf');
    }, 2000);
}

function shareInsights() {
    if (navigator.share) {
        navigator.share({
            title: 'AgroMarket Insights',
            text: 'Check out these market insights from AgroMarket',
            url: window.location.href
        });
    } else {
        navigator.clipboard.writeText(window.location.href).then(() => {
            showNotification('Link copied to clipboard!', 'success');
        });
    }
}

function showNotification(message, type = 'info') {
    // Use global notification system if available
    if (window.AgroMarket && window.AgroMarket.showNotification) {
        window.AgroMarket.showNotification(message, type);
    } else {
        // Fallback notification
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-sm transform transition-all duration-300 ease-in-out translate-x-full`;
        
        switch (type) {
            case 'success':
                notification.classList.add('bg-green-500', 'text-white');
                break;
            case 'error':
                notification.classList.add('bg-red-500', 'text-white');
                break;
            case 'warning':
                notification.classList.add('bg-yellow-500', 'text-white');
                break;
            default:
                notification.classList.add('bg-blue-500', 'text-white');
        }
        
        notification.innerHTML = `
            <div class="flex items-center justify-between">
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-white hover:text-gray-200">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);
        
        // Auto remove
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 300);
        }, 5000);
    }
}

// Export functions for global use
window.InsightsDashboard = {
    updateChart,
    exportData,
    generateReport,
    shareInsights,
    updateDashboard
};