// Lấy dữ liệu từ JSON
const chartDataScript = document.getElementById('chartDataScript');
const chartData = JSON.parse(chartDataScript.textContent);

console.log("Dữ liệu JSON từ backend:", chartData);

const labels = chartData.labels; // Nhãn các tháng
const tanSuatData = chartData.tanSuat; // Dữ liệu tần suất khám
const doanhThuData = chartData.doanhThu; // Dữ liệu doanh thu
const thuocData = chartData.thuoc; // Dữ liệu tần suất sử dụng thuốc

let currentChart = null; // Biến toàn cục cho biểu đồ hiện tại
const tanSuatCtx = document.getElementById('tanSuatChart').getContext('2d');
const doanhThuCtx = document.getElementById('doanhThuChart').getContext('2d');
const thuocCtx = document.getElementById('thuocChart').getContext('2d');

const chartSelector = document.getElementById('chartSelector');
const yearSelector = document.getElementById('yearSelector');
const monthSelector = document.getElementById('monthSelector');
const monthInput = document.getElementById('monthInput');
const chartTypeSelector = document.getElementById('chartTypeSelector');

// Hàm tạo biểu đồ
function createChart(ctx, type, labels, datasets, removeXLabels = false) {
    console.log("Tạo biểu đồ với các tham số:", { type, labels, datasets });
    return new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false } // Tắt legend
            },
            scales: {
                x: {
                    display: !removeXLabels, // Tắt hoặc bật trục X
                    ticks: {
                        display: !removeXLabels // Tắt hoặc bật nhãn trục X
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Hàm cập nhật biểu đồ
function updateChart(chartType, year, month = 0) {
    if (currentChart) {
        console.log("Hủy biểu đồ cũ...");
        currentChart.destroy(); // Hủy biểu đồ cũ
    }

    const selectedType = chartTypeSelector.value;
    console.log("Đang cập nhật biểu đồ:", { chartType, year, month, selectedType });

    if (chartType === 'tanSuat') {
        const data = tanSuatData[year] || Array(12).fill(0);
        console.log(`Dữ liệu tần suất khám cho năm ${year}:`, data);

        currentChart = createChart(tanSuatCtx, selectedType, labels, [{
            label: `Tần suất khám - ${year}`,
            data: data,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]);
    } else if (chartType === 'doanhThu') {
        const data = doanhThuData[year] || Array(12).fill(0);
        console.log(`Dữ liệu doanh thu cho năm ${year}:`, data);

        currentChart = createChart(doanhThuCtx, selectedType, labels, [{
            label: `Doanh thu - ${year}`,
            data: data,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]);
    } else if (chartType === 'thuoc') {
        const typeForThuoc = selectedType === 'line' ? 'bar' : selectedType; // Không cho phép biểu đồ đường
        const data = thuocData[year] || {};
        let datasets;
        const removeXLabels = true; // Ẩn nhãn dưới cột cho tần suất sử dụng thuốc

        console.log(`Dữ liệu thuốc cho năm ${year}:`, data);

        if (month === 0) {
            // Hiển thị cả năm
            datasets = Object.keys(data).map((thuoc, idx) => ({
                label: thuoc,
                data: data[thuoc],
                backgroundColor: `rgba(${50 + idx * 20}, ${100 + idx * 30}, ${150 + idx * 40}, 0.5)`,
                borderColor: `rgba(${50 + idx * 20}, ${100 + idx * 30}, ${150 + idx * 40}, 1)`,
                borderWidth: 1
            }));
            currentChart = createChart(thuocCtx, typeForThuoc, labels, datasets, removeXLabels);
        } else {
            // Hiển thị theo tháng
            datasets = Object.keys(data).map((thuoc, idx) => ({
                label: thuoc,
                data: [data[thuoc][month - 1] || 0],
                backgroundColor: `rgba(${50 + idx * 20}, ${100 + idx * 30}, ${150 + idx * 40}, 0.5)`,
                borderColor: `rgba(${50 + idx * 20}, ${100 + idx * 30}, ${150 + idx * 40}, 1)`,
                borderWidth: 1
            }));
            currentChart = createChart(thuocCtx, typeForThuoc, [`Tháng ${month}`], datasets, removeXLabels);
        }
    }
}

// Hiển thị biểu đồ theo loại
function toggleChartVisibility(chartType) {
    console.log("Chuyển đổi hiển thị biểu đồ:", chartType);

    document.getElementById('tanSuatChartContainer').style.display = chartType === 'tanSuat' ? 'block' : 'none';
    document.getElementById('doanhThuChartContainer').style.display = chartType === 'doanhThu' ? 'block' : 'none';
    document.getElementById('thuocChartContainer').style.display = chartType === 'thuoc' ? 'block' : 'none';
    monthSelector.style.display = chartType === 'thuoc' ? 'block' : 'none';
}

// Lắng nghe sự kiện thay đổi
chartSelector.addEventListener('change', (e) => {
    const chartType = e.target.value;
    const year = yearSelector.value;
    const month = parseInt(monthInput.value, 10) || 0;
    toggleChartVisibility(chartType);
    updateChart(chartType, year, month);
});

yearSelector.addEventListener('change', () => {
    const chartType = chartSelector.value;
    const year = yearSelector.value;
    const month = parseInt(monthInput.value, 10) || 0;
    updateChart(chartType, year, month);
});

monthInput.addEventListener('change', () => {
    const chartType = chartSelector.value;
    const year = yearSelector.value;
    const month = parseInt(monthInput.value, 10) || 0;
    updateChart(chartType, year, month);
});

chartTypeSelector.addEventListener('change', () => {
    const chartType = chartSelector.value;
    const year = yearSelector.value;
    const month = parseInt(monthInput.value, 10) || 0;
    updateChart(chartType, year, month);
});

// Khởi tạo mặc định
updateChart('tanSuat', '2024');
toggleChartVisibility('tanSuat');
