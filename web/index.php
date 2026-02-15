<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fiberhome HG6145F1 Password Generator</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <script src="script.js" defer></script>
</head>

<body>
    <div class="container">
        <h1>Fiberhome Generator</h1>
        <div class="subtitle">Secure Password Tool for HG6145F1</div>

        <form id="generateForm" class="form-group">
            <div class="input-group">
                <input type="text" id="macInput" name="mac" placeholder="AA:BB:CC:DD:EE:FF" autocomplete="off"
                    maxlength="17">
                <button type="button" id="detectBtn" class="detect-btn" title="Auto-Detect Router MAC">
                    &nbsp; Detect &nbsp;
                </button>
            </div>
            <button type="submit" style="margin-top: 10px;">Generate Password</button>
        </form>

        <div id="resultContainer" class="result-container">
            <div class="result-label">Generated Password</div>
            <div id="resultValue" class="result-value"></div>
            <div class="result-label" style="font-size: 0.7rem; margin-top: 5px;">(Click to Copy)</div>
        </div>

        <div id="errorMsg" class="error-msg"></div>

        <div class="history-section">
            <div class="history-title">Recent Generations</div>
            <ul id="historyList" class="history-list">
                <!-- Populated by JS -->
            </ul>
        </div>
    </div>
</body>

</html>