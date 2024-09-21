import requests
import re
import ssl
import datetime

# Function to fetch SSL certificate information
def get_ssl_info(url):
    ssl_info = {}
    try:
        cert = ssl.get_server_certificate((url, 443))
        x509 = ssl.load_certificate(ssl.PEM, cert)
        ssl_info['ssl_certificate'] = cert.decode('utf-8')
        ssl_info['ssl_protocol'] = ssl.PROTOCOL_SSLv23
        ssl_info['ssl_issuer'] = x509.get_issuer().organizationName
        ssl_info['ssl_subject'] = x509.get_subject().commonName
        ssl_info['ssl_not_before'] = datetime.datetime.strptime(x509.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ').strftime('%Y-%m-%d %H:%M:%S')
        ssl_info['ssl_not_after'] = datetime.datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ').strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"Error fetching SSL information: {e}")
    return ssl_info

# URL of the website you want to scrape
url = 'https://www.thequantumloom.xyz'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract response content as text
    html_content = response.text

    # Extract specific data based on your requirements using regex
    indexing_status = re.search(r'<meta\s+name="robots"\s+content="([^"]*)"', html_content)
    indexing_status = indexing_status.group(1) if indexing_status else ''

    page_load_time = re.search(r'<span\s+class="page-load-time">([^<]*)</span>', html_content)
    page_load_time = page_load_time.group(1).strip() if page_load_time else ''

    background_color = re.search(r'<body\s+bgcolor="([^"]*)"', html_content)
    background_color = background_color.group(1) if background_color else ''

    most_used_font_face = ''  # Implement logic to find most used font face
    image_percentage = ''  # Implement logic to calculate image percentage
    video_percentage = ''  # Implement logic to calculate video percentage
    text_percentage = ''  # Implement logic to calculate text percentage
    internal_links = len(re.findall(r'<a\s+href="([^"]*)"', html_content))  # Example of counting internal links
    external_links = 0  # Example, set to 0 for simplicity
    domain = url.split('//')[-1].split('/')[0]  # Extract domain from URL

    # Fetch SSL information
    ssl_info = get_ssl_info(domain)

    # Print or process the extracted data
    print(f'URL: {url}')
    print(f'Indexing Status: {indexing_status}')
    print(f'Page Load Time: {page_load_time}')
    print(f'Background Color: {background_color}')
    print(f'Most Used Font Face: {most_used_font_face}')
    print(f'Image Percentage: {image_percentage}')
    print(f'Video Percentage: {video_percentage}')
    print(f'Text Percentage: {text_percentage}')
    print(f'Internal Links: {internal_links}')
    print(f'External Links: {external_links}')
    print(f'Domain: {domain}')
    print(f'SSL Certificate: {ssl_info.get("ssl_certificate", "")}')
    print(f'Secure Protocol: {ssl_info.get("ssl_protocol", "")}')
    print(f'SSL Issuer: {ssl_info.get("ssl_issuer", "")}')
    print(f'SSL Subject: {ssl_info.get("ssl_subject", "")}')
    print(f'SSL Not Before: {ssl_info.get("ssl_not_before", "")}')
    print(f'SSL Not After: {ssl_info.get("ssl_not_after", "")}')

    # You can continue to extract other elements similarly
else:
    print(f'Failed to retrieve the page. Status code: {response.status_code}')
