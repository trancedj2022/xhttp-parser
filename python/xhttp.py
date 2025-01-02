import base64
import os
import requests

def is_base64_encoded(content):
    """
    Checks if the provided content is Base64 encoded.

    :param content: Content to check.
    :return: True if the content is Base64 encoded, False otherwise.
    """
    try:
        # Try to decode and check if re-encoding gives the same result
        return base64.b64encode(base64.b64decode(content)).decode() == content.strip()
    except Exception:
        return False

def decode_base64_content(content):
    """
    Decodes Base64 encoded content.

    :param content: Base64 encoded content.
    :return: Decoded content.
    """
    return base64.b64decode(content).decode()

def filter_vless_xhttp(content):
    """
    Filters lines starting with "vless://" and containing "xhttp".

    :param content: Input content as a string.
    :return: Filtered lines as a list of strings.
    """
    filtered_lines = []
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("vless://") and "xhttp" in line:
            filtered_lines.append(line)
    return filtered_lines

def process_subscription_links(links):
    """
    Processes multiple subscription links, handling both plain and Base64-encoded content.

    :param links: List of file paths or URLs containing subscription links.
    :return: List of filtered VLESS configs containing "xhttp".
    """
    all_filtered_configs = []

    for link in links:
        try:
            if link.startswith("http://") or link.startswith("https://"):
                response = requests.get(link)
                response.raise_for_status()
                content = response.text.strip()
            elif os.path.isfile(link):
                with open(link, 'r') as file:
                    content = file.read().strip()
            else:
                print(f"Skipping invalid link or file path: {link}")
                continue

            if is_base64_encoded(content):
                try:
                    content = decode_base64_content(content)
                except Exception as e:
                    print(f"Failed to decode Base64 content in {link}: {e}")
                    continue

            filtered_configs = filter_vless_xhttp(content)

            if filtered_configs:
                print(f"Successfully parsed {len(filtered_configs)} configs from {link}")
            else:
                print(f"No valid configs found in {link}")

            all_filtered_configs.extend(filtered_configs)
        except Exception as e:
            print(f"Error processing {link}: {e}")

    return all_filtered_configs

# Subscription links
subscription_links = [
                "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Config%20list1.txt",
                "https://raw.githubusercontent.com/barry-far/V2ray-Configs/refs/heads/main/Sub1.txt",
                "https://raw.githubusercontent.com/lagzian/SS-Collector/refs/heads/main/reality.txt",
                "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/layers/ipv4",
                "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/layers/ipv6",
                "https://raw.githubusercontent.com/M-logique/Proxies/refs/heads/main/proxies/tvc/configshub.txt",
                "https://raw.githubusercontent.com/NRi94/a1/refs/heads/main/svmes.txt",
                "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/refs/heads/main/configtg.txt"
]

output_file = "output/xhttp.txt"

filtered_configs = process_subscription_links(subscription_links)

# Write the filtered configs to an output file
with open(output_file, 'w') as outfile:
    outfile.write('\n'.join(filtered_configs))

print(f"Filtered configs saved to {output_file}")
