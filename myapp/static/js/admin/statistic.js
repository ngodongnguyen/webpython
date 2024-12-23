// statistic.js

// Hàm tải dữ liệu thống kê từ server
async function fetchStatisticData(endpoint, params = {}) {
    try {
        const query = new URLSearchParams(params).toString();
        const response = await fetch(endpoint + '?' + query, { method: 'GET' });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching data:', error);
        return null;
    }
}

// Hàm hiển thị biểu đồ
function renderChart(chartId, labels, data, label, backgroundColor) {
    const ctx = document.getElementById(chartId).getContext('2d');
    new Chart(ctx, {
        type: 'bar', // Có thể thay đổi thành 'line', 'pie', 'doughnut', ...
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: backgroundColor || 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function (tooltipItem) {
                            return tooltipItem.raw.toLocaleString() + ' VNĐ';
                        }
                    }
                }
            }
        }
    });
}

// Hàm tải biểu đồ doanh thu theo tháng
async function loadMonthlyRevenueChart() {
    const data = await fetchStatisticData('/api/statistics/revenue', { type: 'month' });
    if (data) {
        const labels = data.map(item => `Tháng ${item.key}`);
        const values = data.map(item => item.value);
        renderChart('monthlyRevenueChart', labels, values, 'Doanh thu theo tháng');
    } else {
        alert('Không thể tải dữ liệu doanh thu.');
    }
}

// Hàm tải bảng kết quả thống kê
async function loadStatisticTable() {
    const data = await fetchStatisticData('/api/statistics/overview');
    if (data) {
        const tableBody = document.getElementById('statisticTableBody');
        tableBody.innerHTML = data.map(item => `
            <tr>
                <td>${item.key}</td>
                <td>${item.value}</td>
            </tr>
        `).join('');
    } else {
        alert('Không thể tải dữ liệu bảng.');
    }
}

// Hàm xử lý sự kiện khi người dùng chọn loại thống kê
document.getElementById('statisticType').addEventListener('change', async (event) => {
    const type = event.target.value;
    if (type === 'revenue') {
        await loadMonthlyRevenueChart();
    }
    // Có thể thêm các loại thống kê khác
});

// Khởi tạo khi tải trang
window.onload = async () => {
    await loadMonthlyRevenueChart(); // Mặc định tải biểu đồ doanh thu
    await loadStatisticTable();     // Tải bảng dữ liệu tổng quan
};
// Thêm hàm này để xử lý khi nhấp vào "Thống Kê"
function loadStatisticPage() {
    console.log("Loading statistic page...");
    fetch('/admin/thongke')
        .then(response => response.text())
        .then(html => {
            console.log("Statistic page loaded successfully");
            document.getElementById('content').innerHTML = html;
        })
        .catch(error => console.error('Error:', error));
}
document.querySelectorAll('.sidebar a').forEach(link => {
    if (window.location.pathname === link.getAttribute('href')) {
        link.classList.add('active');
    }
});
