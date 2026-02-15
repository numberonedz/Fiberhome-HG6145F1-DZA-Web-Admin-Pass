document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('generateForm');
    const macInput = document.getElementById('macInput');
    const resultContainer = document.getElementById('resultContainer');
    const resultValue = document.getElementById('resultValue');
    const errorMsg = document.getElementById('errorMsg');
    const historyList = document.getElementById('historyList');
    const detectBtn = document.getElementById('detectBtn');

    // Auto-detect handler
    detectBtn.addEventListener('click', async () => {
        const originalText = detectBtn.innerHTML;
        detectBtn.innerHTML = '...';
        detectBtn.disabled = true;
        hideError();

        try {
            const response = await fetch('api.php?action=detect');
            const data = await response.json();

            if (data.success && data.mac) {
                macInput.value = data.mac;
                // Optional: Auto-submit? No, let user confirm.
            } else {
                showError(data.error || 'Could not detect MAC.');
            }
        } catch (err) {
            console.error(err);
            showError('Detection failed (network error).');
        } finally {
            detectBtn.innerHTML = originalText;
            detectBtn.disabled = false;
        }
    });

    // Auto-format MAC address input
    macInput.addEventListener('input', (e) => {
        let val = e.target.value.replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
        if (val.length > 12) val = val.substring(0, 12);

        let formatted = '';
        for (let i = 0; i < val.length; i++) {
            if (i > 0 && i % 2 === 0) formatted += ':';
            formatted += val[i];
        }
        e.target.value = formatted;
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const mac = macInput.value;
        if (!mac || mac.length < 17) {
            showError('Please enter a complete MAC address (XX:XX:XX:XX:XX:XX)');
            return;
        }

        try {
            const response = await fetch('api.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mac: mac })
            });

            const data = await response.json();

            if (data.error) {
                showError(data.error);
                resultContainer.style.display = 'none';
            } else {
                hideError();
                showResult(data.password);
                fetchHistory(); // Refresh history
            }
        } catch (err) {
            showError('Server error. Ensure PHP is running.');
            console.error(err);
        }
    });

    function showError(msg) {
        errorMsg.textContent = msg;
        errorMsg.style.display = 'block';
    }

    function hideError() {
        errorMsg.style.display = 'none';
        errorMsg.textContent = '';
    }

    function showResult(password) {
        resultValue.textContent = password;
        resultContainer.style.display = 'block';
        resultContainer.classList.add('fade-in');

        // Copy functionality
        resultValue.onclick = () => {
            navigator.clipboard.writeText(password).then(() => {
                const originalText = resultValue.textContent;
                resultValue.textContent = 'Copied!';
                setTimeout(() => {
                    resultValue.textContent = originalText;
                }, 1000);
            });
        };
    }

    async function fetchHistory() {
        try {
            const response = await fetch('api.php');
            const data = await response.json();

            historyList.innerHTML = '';
            if (data.history && data.history.length > 0) {
                data.history.forEach(item => {
                    const li = document.createElement('li');
                    li.className = 'history-item';
                    li.innerHTML = `
                        <span class="history-mac">${item.mac_address}</span>
                        <span class="history-pass">${item.generated_password}</span>
                    `;
                    historyList.appendChild(li);
                });
            } else {
                historyList.innerHTML = '<li class="history-item" style="color:#666; justify-content:center;">No history yet</li>';
            }
        } catch (err) {
            console.error('Failed to fetch history', err);
        }
    }

    // Initial fetch of history
    fetchHistory();
});
