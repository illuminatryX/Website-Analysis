import requests
import re
import ssl
import socket
import datetime
from bs4 import BeautifulSoup

# Function to fetch SSL certificate information
def get_ssl_info(domain):
    ssl_info = {}
    try:
        # Establish a connection to the server
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()

        # Extract SSL certificate information
        ssl_info['ssl_issuer'] = dict(x[0] for x in cert['issuer'])['organizationName']
        ssl_info['ssl_subject'] = dict(x[0] for x in cert['subject'])['commonName']
        ssl_info['ssl_not_before'] = cert['notBefore']
        ssl_info['ssl_not_after'] = cert['notAfter']
        ssl_info['ssl_protocol'] = ssock.version()
    except Exception as e:
        print(f"Error fetching SSL information: {e}")
    return ssl_info

# Function to calculate percentage of images, videos, and text
def calculate_percentage(html_content):
    total_size = len(html_content)
    soup = BeautifulSoup(html_content, 'html.parser')

    # Calculate image percentage
    images = soup.find_all('img')
    img_size = sum([len(str(img)) for img in images])
    image_percentage = (img_size / total_size) * 100 if total_size else 0

    # Calculate video percentage
    videos = soup.find_all('video')
    video_size = sum([len(str(video)) for video in videos])
    video_percentage = (video_size / total_size) * 100 if total_size else 0

    # Calculate text percentage
    text = soup.get_text()
    text_size = len(text)
    text_percentage = (text_size / total_size) * 100 if total_size else 0

    return image_percentage, video_percentage, text_percentage

# URL of the website you want to scrape
url = 'https://www.thequantumloom.xyz'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract metadata using BeautifulSoup
    indexing_status_tag = soup.find('meta', attrs={'name': 'robots'})
    indexing_status = indexing_status_tag['content'] if indexing_status_tag else 'Not Available'

    # Page load time
    page_load_time_tag = soup.find('span', class_='page-load-time')
    page_load_time = page_load_time_tag.text.strip() if page_load_time_tag else 'Not Available'

    # Background color
    body_tag = soup.find('body')
    background_color = body_tag.get('bgcolor', 'Not Available')

    # Extract font face (example assumes inline CSS or style tags)
    styles = soup.find_all('style')
    font_faces = []
    for style in styles:
        font_faces.extend(re.findall(r'font-family:\s*([^;]+);', style.get_text(), re.IGNORECASE))
    most_used_font_face = max(set(font_faces), key=font_faces.count) if font_faces else 'Not Available'

    # Calculate image, video, and text percentages
    image_percentage, video_percentage, text_percentage = calculate_percentage(html_content)

    # Internal and external links
    internal_links = len([link for link in soup.find_all('a', href=True) if url in link['href']])
    external_links = len([link for link in soup.find_all('a', href=True) if url not in link['href']])

    # Extract domain
    domain = url.split('//')[-1].split('/')[0]

    # Fetch SSL information
    ssl_info = get_ssl_info(domain)

    # Print or process the extracted data
    print(f'URL: {url}')
    print(f'Indexing Status: {indexing_status}')
    print(f'Page Load Time: {page_load_time}')
    print(f'Background Color: {background_color}')
    print(f'Most Used Font Face: {most_used_font_face}')
    print(f'Image Percentage: {image_percentage:.2f}%')
    print(f'Video Percentage: {video_percentage:.2f}%')
    print(f'Text Percentage: {text_percentage:.2f}%')
    print(f'Internal Links: {internal_links}')
    print(f'External Links: {external_links}')
    print(f'Domain: {domain}')
    print(f'SSL Issuer: {ssl_info.get("ssl_issuer", "Not Available")}')
    print(f'SSL Subject: {ssl_info.get("ssl_subject", "Not Available")}')
    print(f'SSL Not Before: {ssl_info.get("ssl_not_before", "Not Available")}')
    print(f'SSL Not After: {ssl_info.get("ssl_not_after", "Not Available")}')
    print(f'Secure Protocol: {ssl_info.get("ssl_protocol", "Not Available")}')

else:
    print(f'Failed to retrieve the page. Status code: {response.status_code}')
