<?php
require_once 'db.php';
require_once 'logic.php';

header('Content-Type: application/json');

// Only support POST for generation
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    $mac = isset($input['mac']) ? strtoupper(trim($input['mac'])) : '';

    if (empty($mac)) {
        echo json_encode(['error' => 'MAC address is required']);
        exit;
    }

    $password = mac_to_pass($mac);

    if ($password === "") {
        echo json_encode(['error' => 'Invalid MAC format (expected XX:XX:XX:XX:XX:XX)']);
        exit;
    }

    // Log to DB if connection exists
    if (isset($pdo)) {
        try {
            $stmt = $pdo->prepare("INSERT INTO generated_passwords (mac_address, generated_password) VALUES (:mac, :pass)");
            $stmt->execute(['mac' => $mac, 'pass' => $password]);
        } catch (\PDOException $e) {
            // Log error silently, don not fail the request
            // error_log("DB Error: " . $e->getMessage());
        }
    }

    echo json_encode(['success' => true, 'password' => $password]);
    exit;
}

// Handle GET
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $action = isset($_GET['action']) ? $_GET['action'] : '';

    if ($action === 'detect') {
        // Detect Router/Gateway MAC
        $mac = null;

        // Windows specific detection logic
        if (strtoupper(substr(PHP_OS, 0, 3)) === 'WIN') {
            // Attempt 1: Get ARP table of gateway
            // Find gateway via route print
            // Simpler: Just get the first dynamic entry in ARP table that ends with .1
            // OR regex on `arp -a` output for the first dynamic entry for local subnet

            // Let's get "Default Gateway" from ipconfig
            exec('chcp 65001'); // Force UTF-8 if possible
            exec('ipconfig /all', $output);
            $gateway_ip = '';

            // Basic parsing for gateway
            foreach ($output as $line) {
                // English: "Default Gateway"
                // French: "Passerelle par défaut"
                // German: "Standardgateway"
                // Use regex for IP pattern after "Gateway" or fallback to lines containing " . . . :"
                if (
                    preg_match('/(Default Gateway|Passerelle.*d.*faut|Standardgateway)[ .:]+([0-9.]+)/i', $line, $matches) ||
                    (strpos($line, '0.0.0.0') === false && preg_match('/^[ .]+: ([0-9.]+)/', $line, $matches))
                ) {

                    if (isset($matches[2]) && filter_var($matches[2], FILTER_VALIDATE_IP)) {
                        $gateway_ip = $matches[2];
                        break;
                    }
                }
            }

            // If explicit gateway found, use it. If not, fallback to ARP table scanning.
            exec('arp -a', $arp_output);
            foreach ($arp_output as $line) {
                // Format: IP Address  Physical Address  Type
                // We want dynamic type usually.
                if (preg_match('/([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})/', $line, $matches)) {
                    $found_mac = strtoupper(str_replace('-', ':', $matches[0]));
                    // Ignore broadcast/multicast
                    if ($found_mac === 'FF:FF:FF:FF:FF:FF' || strpos($found_mac, '01:00:5E') === 0)
                        continue;

                    // If we have a gateway IP, match it
                    if ($gateway_ip && strpos($line, $gateway_ip) !== false) {
                        $mac = $found_mac;
                        break;
                    }

                    // Fallback: assume first dynamic entry is the router (most common on home networks)
                    // Or if line contains "dynamic" or "dynamique"
                    if (!$mac && (strpos(strtolower($line), 'dynamic') !== false || strpos(strtolower($line), 'dynamique') !== false)) {
                        $mac = $found_mac;
                        // Wait, don't break immediately, prioritize gateway if found later?
                        // Actually, usually the gateway is the first entry.
                        break;
                    }
                }
            }
        } else { // Linux/Mac
            // `ip neighbor` or `arp -an`
            exec('ip route show | grep default', $route_output);
            // "default via 192.168.1.1 dev eth0"
            if (isset($route_output[0]) && preg_match('/via ([0-9.]+)/', $route_output[0], $matches)) {
                $gateway_ip = $matches[1];
                exec("cat /proc/net/arp | grep '$gateway_ip'", $arp_output);
                if (isset($arp_output[0]) && preg_match('/([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}/', $arp_output[0], $mac_matches)) {
                    $mac = strtoupper($mac_matches[0]);
                }
            }
        }

        if ($mac) {
            echo json_encode(['success' => true, 'mac' => $mac]);
        } else {
            echo json_encode(['error' => 'Could not detect router MAC. Ensure you are on the same network.']);
        }
        exit;
    }

    if (isset($pdo)) {
        try {
            $stmt = $pdo->query("SELECT mac_address, generated_password, created_at FROM generated_passwords ORDER BY created_at DESC LIMIT 10");
            $history = $stmt->fetchAll();
            echo json_encode(['history' => $history]);
        } catch (\PDOException $e) {
            echo json_encode(['history' => []]);
        }
    } else {
        echo json_encode(['history' => []]);
    }
    exit;
}
?>