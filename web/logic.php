<?php
// logic.php - Core logic isolated
function mac_to_pass($mac)
{
    // 1. Validate format
    if (!preg_match('/^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$/', $mac)) {
        return "";
    }

    $UPPER = "ACDFGHJMNPRSTUWXY";
    $LOWER = "abcdfghjkmpstuwxy";
    $DIGIT = "2345679";
    $SYMBOL = "!@$&%";

    // MD5 hashing
    $hash = md5($mac . "AEJLY"); // PHP md5 returns 32 hex chars by default

    $vals = [];
    // Process first 20 hex chars
    for ($i = 0; $i < 20; $i++) {
        $c = $hash[$i];
        if ($c >= '0' && $c <= '9') {
            $vals[] = ord($c) - ord('0');
        } elseif ($c >= 'a' && $c <= 'f') {
            $vals[] = ord($c) - ord('a') + 10;
        } elseif ($c >= 'A' && $c <= 'F') {
            $vals[] = ord($c) - ord('A') + 10;
        } else {
            $vals[] = 0;
        }
    }

    // Initialize password array
    $password = array_fill(0, 16, '');

    for ($i = 0; $i < 16; $i++) {
        $v = $vals[$i];
        $case_type = $v % 4;

        if ($case_type == 0) {
            $password[$i] = $UPPER[($v * 2) % 17];
        } elseif ($case_type == 1) {
            $password[$i] = $LOWER[($v * 2 + 1) % 17];
        } elseif ($case_type == 2) {
            // PHP string access is 0-indexed.
            // Python: DIGIT[6 - (v % 7)]
            $password[$i] = $DIGIT[6 - ($v % 7)];
        } elseif ($case_type == 3) {
            // Python: SYMBOL[4 - (v % 5)]
            $password[$i] = $SYMBOL[4 - ($v % 5)];
        }
    }

    // Step 4: enforce all character classes
    $p0 = ($vals[16] + 1) % 16;
    $p1 = ($vals[17] + 1) % 16;
    while ($p1 == $p0) {
        $p1 = ($p1 + 1) % 16;
    }

    $p2 = ($vals[18] + 1) % 16;
    while ($p2 == $p0 || $p2 == $p1) {
        $p2 = ($p2 + 1) % 16;
    }

    $p3 = ($vals[19] + 1) % 16;
    while ($p3 == $p0 || $p3 == $p1 || $p3 == $p2) {
        $p3 = ($p3 + 1) % 16;
    }

    $password[$p0] = $UPPER[($vals[16] * 2) % 17];
    $password[$p1] = $LOWER[($vals[17] * 2 + 1) % 17];
    $password[$p2] = $DIGIT[6 - ($vals[18] % 7)];
    $password[$p3] = $SYMBOL[4 - ($vals[19] % 5)];

    return implode('', $password);
}
?>