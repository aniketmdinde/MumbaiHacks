// Sample data
const months = ['January', 'February', 'March', 'April', 'May'];
const savingsData = [200, 300, 400, 500, 600];
const incomeData = [1000, 2000, 1500, 1800, 2200];
const expensesData = [800, 1700, 1100, 1300, 2000];
const expensesSummaryData = [200, 100, 300, 400, 500];
const futurePaymentsData = [1200, 1300, 1250, 1400, 1500];

// Savings chart
const savingsChart = new Chart(document.getElementById('savingsChart'), {
    type: 'line',
    data: {
        labels: months,
        datasets: [{ 
            data: savingsData,
            label: "Savings",
            borderColor: "#6474e5", // updated color
            fill: false
        }]
    }
});

// Load balance chart
const balanceChart = new Chart(document.getElementById('balanceChart'), {
    type: 'bar',
    data: {
        labels: months,
        datasets: [
            {
                data: incomeData,
                label: "Income",
                backgroundColor: "#6474e5", // updated color
                stack: 'Stack 0',
            },
            {
                data: expensesData,
                label: "Expenses",
                backgroundColor: "#9aa4ec", // updated color
                stack: 'Stack 0',
            }
        ]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                stacked: true
            }
        },
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        let label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        if (context.parsed.y !== null) {
                            label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(context.parsed.y);
                        }
                        // calculate percentage difference
                        if(context.datasetIndex === 1){
                            const income = context.raw;
                            const expense = context.chart.data.datasets[0].data[context.dataIndex];
                            const difference = ((income - expense) / income) * 100;
                            label += ' (' + difference.toFixed(2) + '% difference)';
                        }
                        return label;
                    }
                }
            }
        }
    }
});

// Expenses summary chart
const expensesChart = new Chart(document.getElementById('expensesChart'), {
    type: 'pie',
    data: {
        labels: ["Rent", "Groceries", "Transport", "Subscriptions", "Others"],
        datasets: [{
            data: expensesSummaryData,
            backgroundColor: ["#6474e5", "#9aa4ec", "#d4f7ff", "#ffffff", "#f4a4a4"] // updated colors
        }]
    },
    options: {
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        let label = context.label || '';
                        if (label) {
                            label += ': ';
                        }
                        if (context.parsed !== null) {
                            let total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                            let value = context.chart.data.datasets[0].data[context.dataIndex];
                            let percentage = ((value / total) * 100).toFixed(2) + "%";
                            label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value) + ' (' + percentage + ')';
                        }
                        return label;
                    }
                }
            }
        }
    }
});

// Future payments prediction chart
const futurePaymentsChart = new Chart(document.getElementById('futurePaymentsChart'), {
    type: 'line',
    data: {
        labels: months,
        datasets: [{ 
            data: futurePaymentsData,
            label: "Future Payments",
            borderColor: "#6474e5", // updated color
            fill: false
        }]
    }
});
