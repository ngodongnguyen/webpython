document.getElementById('login').addEventListener('click', function (event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    })
        .then(response => {
            console.log('Response Status:', response.status);
            return response.json().catch(() => {
                throw new Error('Không thể parse JSON từ server');
            });
        })
        .then(data => {
            console.log('Response Data:', data); // Log dữ liệu trả về
            if (data.redirect) {
                window.location.href = data.redirect;
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Lỗi:', error);
            alert('Đã xảy ra lỗi. Vui lòng thử lại.');
        });
});
