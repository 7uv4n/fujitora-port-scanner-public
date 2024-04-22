def expand_ip_range(ip_range_str):
    import ipaddress

    def expand_single_ip(ip):
        try:
            ipaddress.ip_address(ip)
            return [ip]
        except ValueError:
            pass
        
        parts = ip.split('.')
        if '-' in parts[-1]:
            base_ip = '.'.join(parts[:-1])
            start, end = map(int, parts[-1].split('-'))
            return [f"{base_ip}.{i}" for i in range(start, end + 1)]
        else:
            return [ip]

    # Split input string by comma and strip spaces
    ip_ranges = [range_part.strip() for range_part in ip_range_str.split(',')]

    # Expand each part of the IP range string
    expanded_ips = []
    for ip_range in ip_ranges:
        expanded_ips.extend(expand_single_ip(ip_range))

    return expanded_ips

def expand_ranges(input_str):
    def expand_range(range_str):
        parts = range_str.split('-')
        if len(parts) == 1:
            return [int(parts[0])]  # Single port number
        elif len(parts) == 2:
            start, end = map(int, parts)
            return list(range(start, end + 1))  # Range of port numbers
        else:
            raise ValueError("Invalid range format")

    # Split input string by comma and strip spaces
    ranges = [range_part.strip() for range_part in input_str.split(',')]

    # Expand each part of the input string
    expanded_values = []
    for range_item in ranges:
        if '-' in range_item:
            expanded_values.extend(expand_range(range_item))
        else:
            expanded_values.append(int(range_item))

    return expanded_values

# # Test examples
# print(expand_ranges('80-85'))          # Output: [80, 81, 82, 83, 84, 85]
# print(expand_ranges('79,30,60-65'))    # Output: [79, 30, 60, 61, 62, 63, 64, 65]


# # Test examples
# print(expand_ip_range('127.0.0.1, 127.0.0.2'))  # Output: ['127.0.0.1', '127.0.0.2']
# print(expand_ip_range('192.1.1.1-3'))            # Output: ['192.1.1.1', '192.1.1.2', '192.1.1.3']


