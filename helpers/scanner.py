import socket
import json
import datetime

# Function to scan ports on a single IP address
def scan_ports(ip, ports, timeout=1):
    open_ports = {}
    closed_ports = {}
    filtered_ports = {}
    port_time = {}
    start_time = datetime.datetime.now()                            # Start time for scanning all ports

    # Loop through the list of ports and scan each one
    for port in ports:
        port = int(port)
        start_time_port = datetime.datetime.now()                   # Start time for scanning the port
        print(f"Scanning {ip}:{port}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            result = sock.connect_ex((ip, port))                    # Connect to the port and get the result
            try:
                service_name = socket.getservbyport(port)           # Get the service name for the port
            except OSError:
                service_name = "Unknown"                            # If the service name is not found, set it to "Unknown"

            if result == 0:
                open_ports[port] = service_name                     # If the port is open, add it to the open_ports dictionary
            elif result == socket.errno.ECONNREFUSED:
                closed_ports[port] = service_name                   # If the port is closed, add it to the closed_ports dictionary
            else:
                filtered_ports[port] = service_name                 # If the port is filtered, add it to the filtered_ports dictionary

        except socket.timeout:
            # If the connection times out, add the port to the filtered_ports dictionary
            filtered_ports[port] = socket.getservbyport(port) if port in socket.getservbyport(port) else "Unknown"
        except Exception as e:
            #  If an error occurs, add the port to the filtered_ports dictionary
            print(f"Error scanning port {port}: {str(e)}")
            filtered_ports[port] = "Unknown"
        sock.close()
        end_time_port = datetime.datetime.now()                     # End time for scanning the port
        elapsed_time_port = (end_time_port - start_time_port).total_seconds()       # Calculate the elapsed time for scanning the port
        port_time[port] = elapsed_time_port                          # Add the elapsed time to the port_time dictionary
    end_time = datetime.datetime.now()                              # End time for scanning all ports

    # Return the scan results as a dictionary
    return {
        "ip": ip,
        "open_ports": open_ports,
        "open_ports_count": len(open_ports),
        "closed_ports": closed_ports,
        "closed_ports_count": len(closed_ports),
        "filtered_ports": filtered_ports,
        "filtered_ports_count": len(filtered_ports),
        "start_time": start_time.strftime("%Y:%m:%d:%H:%M:%S.%f"),
        "end_time": end_time.strftime("%Y:%m:%d:%H:%M:%S.%f"),
        "elapsed_time": (end_time - start_time).total_seconds(),
        "ports": [
            {
                "port_no": str(port),
                "status": "open" if port in open_ports else "closed" if port in closed_ports else "filtered",
                "service": open_ports[port] if port in open_ports else closed_ports[port] if port in closed_ports else "Unknown",
                "time": port_time[port] if port in port_time else "N/A"
            }
            for port in ports
        ]
    }

# Function to scan multiple IP addresses
def scan_multiple_ips(ips, ports, name):
    result = {name: []}
    for ip in ips:
        scan_result = scan_ports(ip, ports)
        result[name].append(scan_result)
    return result

# Main function to scan multiple IP addresses and ports. Use it for testing purposes
if __name__ == "__main__":
    # Define IP addresses and ports to scan
    ips_to_scan = ["192.168.0.189", "192.168.0.184"]
    # ips_to_scan = ["127.0.0.1"]

    ports_to_scan = [21, 53, 80, 443, 22, 8080, 16000, 345, 5000]  # Example list of ports to scan

    # Perform scanning and generate JSON report
    scan_results = scan_multiple_ips(ips_to_scan, ports_to_scan, "ScanResults")

    # Output the result to a JSON file
    with open("scan_results.json", "w") as json_file:
        json.dump(scan_results, json_file, indent=4)
    print("Scanning completed. Results saved to 'scan_results.json'.")