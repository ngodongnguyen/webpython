// Lấy dữ liệu từ JSON
const chartDataScript = document.getElementById('chartDataScript');
const chartData = JSON.parse(chartDataScript.textContent);

// Dữ liệu cho biểu đồ
const labels = chartData.labels;
const tanSuatData = chartData.tanSuat;
const doanhThuData = chartData.doanhThu;

// Biến biểu đồ toàn cục
let currentChart = null;
const tanSuatCtx = document.getElementById('tanSuatChart').getContext('2d');
const doanhThuCtx = document.getElementById('doanhThuChart').getContext('2d');

// Hàm tạo biểu đồ
function createChart(ctx, type, labels, data, label) {
    const isPieChart = type === 'pie';
    return new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: isPieChart
                    ? [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ]
                    : 'rgba(54, 162, 235, 0.2)',
                borderColor: isPieChart
                    ? [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ]
                    : 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: null // Hiển thị legend chỉ cho biểu đồ tròn
                }
            },
            scales: isPieChart
                ? {}
                : {
                    y: {
                        beginAtZero: true
                    }
                }
        }
    });
}

// Hàm cập nhật biểu đồ
function updateChart(ctx, type, labels, data, label) {
    // Xóa biểu đồ cũ nếu tồn tại
    if (currentChart) {
        currentChart.destroy();
    }

    // Thêm lớp 'pie' nếu biểu đồ là dạng tròn
    const container = ctx.canvas.parentElement;
    if (type === 'pie') {
        container.classList.add('pie');
    } else {
        container.classList.remove('pie');
    }

    // Tạo biểu đồ mới
    currentChart = createChart(ctx, type, labels, data, label);
}

// Xử lý hiển thị biểu đồ theo lựa chọn dropdown
const chartSelector = document.getElementById('chartSelector');
const chartTypeSelector = document.getElementById('chartTypeSelector');
const tanSuatChartContainer = document.getElementById('tanSuatChartContainer');
const doanhThuChartContainer = document.getElementById('doanhThuChartContainer');

chartSelector.addEventListener('change', (event) => {
    const selectedChart = event.target.value;
    if (selectedChart === 'tanSuatChart') {
        tanSuatChartContainer.style.display = 'block';
        doanhThuChartContainer.style.display = 'none';
        updateChart(tanSuatCtx, chartTypeSelector.value, labels, tanSuatData, 'Tần suất khám');
    } else if (selectedChart === 'doanhThuChart') {
        tanSuatChartContainer.style.display = 'none';
        doanhThuChartContainer.style.display = 'block';
        updateChart(doanhThuCtx, chartTypeSelector.value, labels, doanhThuData, 'Doanh thu');
    }
});

chartTypeSelector.addEventListener('change', (event) => {
    const type = event.target.value;
    if (tanSuatChartContainer.style.display === 'block') {
        updateChart(tanSuatCtx, type, labels, tanSuatData, 'Tần suất khám');
    } else if (doanhThuChartContainer.style.display === 'block') {
        updateChart(doanhThuCtx, type, labels, doanhThuData, 'Doanh thu');
    }
});

// Khởi tạo biểu đồ mặc định
updateChart(tanSuatCtx, 'bar', labels, tanSuatData, 'Tần suất khám');
