import requests
from bs4 import BeautifulSoup
import json

def get_page_data(url, cookies):
    """Fetch and parse the page data"""
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://www.lieferando.de/",
        "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        "sec-ch-ua-arch": '"x86"',
        "sec-ch-ua-bitness": '"64"',
        "sec-ch-ua-full-version": '"136.0.7103.94"',
        "sec-ch-ua-full-version-list": '"Chromium";v="136.0.7103.94", "Google Chrome";v="136.0.7103.94", "Not.A/Brand";v="99.0.0.0"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": '""',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-platform-version": '"10.0.0"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    }

    try:
        response = requests.get(url, cookies=cookies, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find_all('script')[-1]
        return json.loads(script_tag.text)
    except Exception as e:
        print(f"Error getting page data: {e}")
        return None

def extract_restaurant_data(page_data):
    """Extract restaurant data from the page JSON"""
    try:
        return page_data['props']['appProps']['preloadedState']['menu']['restaurant']
    except KeyError as e:
        print(f"Error extracting restaurant data: {e}")
        return None

def process_menu(restaurant_data):
    """Process the menu data into a clean structure"""
    if not restaurant_data:
        return []
    
    try:
        raw_menu = restaurant_data['cdn']['restaurant']['menus'][0]["categories"]
        items_common = restaurant_data['cdn']['items']
        
        # Map item IDs to their full details
        for section in raw_menu:
            section['items'] = [items_common[item_id] for item_id in section['itemIds']]
        
        # Transform to cleaner structure
        return [
            {
                'category': section['name'],
                'items': [
                    {
                        'name': item['name'],
                        'description': item.get('description', ''),
                        'variations': [
                            {'name': var['name'], 'price': var['basePrice']}
                            for var in item.get('variations', [])
                        ]
                    }
                    for item in section['items']
                ]
            }
            for section in raw_menu
        ]
    except Exception as e:
        print(f"Error processing menu: {e}")
        return []

def get_reviews(restaurant_id):
    """Fetch restaurant reviews"""
    try:
        url = f"https://rest.api.eu-central-1.production.jet-external.com/restaurants/de/{restaurant_id}/reviews"
        response = requests.get(url)
        return response.json() if response.ok else []
    except Exception as e:
        print(f"Error getting reviews: {e}")
        return []

def scrape_lieferando(url, site_cookies):
    """Main scraping function"""
    # Get the initial page data
    page_data = get_page_data(url, site_cookies)
    if not page_data:
        return None
    
    # Extract restaurant data
    restaurant_data = extract_restaurant_data(page_data)
    if not restaurant_data:
        return None
    
    # Build the result dictionary
    cdn = restaurant_data['cdn']['restaurant']
    info = cdn['restaurantInfo']
    
    result = {
        'id': cdn['restaurantId'],
        'name': info['name'],
        'email': info['email'],
        'location': info['location'],
        'phone': info.get('allergenPhoneNumber'),
        'menu': process_menu(restaurant_data),
        'reviews': get_reviews(cdn['restaurantId'])
    }
    
    return result

if __name__ == "__main__":
    url = "https://www.lieferando.de/en/menu/subway-pirna"
    site_cookies = "siteLanguage=en; je-auser=4e1749f7-51d8-43a4-8e18-f4ad3dba233b; deviceLocationPermissionGranted=false; je-cookieConsent=full; customerCookieConsent=%5B%7B%22consentTypeId%22%3A103%2C%22consentTypeName%22%3A%22necessary%22%2C%22isAccepted%22%3Atrue%2C%22decisionAt%22%3A%222025-05-20T08%3A27%3A56.0000000%2B00%3A00%22%7D%2C%7B%22consentTypeId%22%3A104%2C%22consentTypeName%22%3A%22functional%22%2C%22isAccepted%22%3Atrue%2C%22decisionAt%22%3A%222025-05-20T08%3A27%3A56.0000000%2B00%3A00%22%7D%2C%7B%22consentTypeId%22%3A105%2C%22consentTypeName%22%3A%22analytical%22%2C%22isAccepted%22%3Atrue%2C%22decisionAt%22%3A%222025-05-20T08%3A27%3A56.0000000%2B00%3A00%22%7D%2C%7B%22consentTypeId%22%3A106%2C%22consentTypeName%22%3A%22personalized%22%2C%22isAccepted%22%3Atrue%2C%22decisionAt%22%3A%222025-05-20T08%3A27%3A56.0000000%2B00%3A00%22%7D%5D; jet-sp-customer-ses.5f43=*; _gcl_au=1.1.1171915029.1747729677; _ga=GA1.1.4e1749f7-51d8-43a4-8e18-f4ad3dba233b; _pin_unauth=dWlkPU9HRXpOak00TURVdFltSTFNaTAwWlRKbExXSTRZek10WVRJMVptUXpZalV6WVdZeA; _scid=FRkEq8CRc1KVnkrpfn7UBfkuwCm5nTKv; _fbp=fb.1.1747729677644.24991599728435861; _tt_enable_cookie=1; _ttp=01JVPCWZF86BM2YNQ7RCTWXSDF_.tt.1; _sctr=1%7C1747679400000; ab.storage.deviceId.f543a405-bc6b-4dfa-b736-f6a0d6884bad=%7B%22g%22%3A%222719dc6e-77de-5edd-869a-57ace6754c2e%22%2C%22c%22%3A1747729686987%2C%22l%22%3A1747729686987%7D; activeAddress=%7B%22address%22%3A%7B%22location%22%3A%7B%22lat%22%3A50.969316%2C%22lng%22%3A13.8738134%2C%22locationSlug%22%3A%2201809%22%7D%7D%7D; cookieConsent=full; cookieConsent=%22full%22; cwSession=%7B%22id%22%3A%227220f2fa-b5de-49cd-8ea3-d5c4830479fb%22%7D; __cf_bm=.1osnGB7mzVk9hMPo.hTyParWPTdyXV73Ao8bg6KUlQ-1747738549-1.0.1.1-DcWQ75uL6JL2jAk_Y1i6iNfGId4fgLLWfkwXFtMEUXifhbpmw2SQcGAxsduPpZX7j6jiq7hgFpTriVzZTHbluXRCwRGRSBhjunT4m2Rx0Eew3Q.yz4yO4bmh9PAY5P72; _scid_r=EpkEq8CRc1KVnkrpfn7UBfkuwCm5nTKvOWbhVw; ttcsid_C8LGUFCO0T91FSTH4960=1747738284663::hU-r77VXQsIo54uyD_rg.1.1747738284664; ttcsid=1747738284663::sC9DrNZucIVSVIgfdQ1Y.1.1747738284664; _uetsid=5575ea60355411f0bfbcf5e373c5f3a5; _uetvid=55762000355411f084c0f5d3ccd1bafd; _ScCbts=%5B%5D; _dd_s=aid=08c347b2-f2a7-4e11-9235-ecf9288a463b&logs=1&id=38e9d19e-87e9-4eb6-8b68-d6900f106123&created=1747729656554&expire=1747739311898&rum=0; restaurantsView=%7B%22viewType%22%3A%22restaurantsListView%22%2C%22restaurantId%22%3A%2210062823%22%7D; jet-sp-customer-id.5f43=3f0ecb99-c4a7-4e81-8579-e493c533088e.1747729677.1.1747738412..70016a9a-4449-4a43-b573-8863371baa32..48d24624-3e2e-4933-842f-829211c4b8f7.1747729682891.279; _ga_4PH28YDTSD=GS2.1.s1747729676$o1$g1$t1747738411$j0$l0$h0; _ga_VJTENYSCXJ=GS2.1.s70016a9a-4449-4a43-b573-8863371baa32$o1$g1$t1747738411$j0$l0$h0; cf_clearance=odSa0x7OwaKdIcFAMOxkTZiaKhrc5hzrHLeG0dTlilU-1747738691-1.2.1.1-Hcwu1JyU100C66QvIm19Xv0v8ScsIGwGTN_i9fq1QS8yhTJNTvpGHf_3M8rRzxtnAWuAy.YUk.dAakE2GbN2johdqGtnBiTGdBulcqSj8Nce9.2OhEKIND1H.So0IIDhGQoupWM02Dn2_iiomyjMA_enFfj46aiXp_ZbpVQE.x46V5Lk8tepZcir0y8DH_nLq.WtDgyu68gDlfPoulK7dyjWIhTWr0drz_7rlfZ4CZnT3HhzKwk9pooDRRZrDqgigafr6hA8NAU.prxXvmYf2SyazXBHTWPRYF58MH03Bxv.Xxb9oImMcK3j4attqf3yL5CVV.dpfEUMQsrMcMT7lxHGh3g9THFwN5oEqf7UB3Y7I04yXKAdHQRq8fZgJZFG"

    result = scrape_lieferando(url, site_cookies)
    export_save_file_path = './' + url.split('/')[-1] + '.json'
    
    if result:
        with open(export_save_file_path, 'w') as json_file:
            json.dump(result, json_file, indent=4)

        print(f"Data successfully exported to {export_save_file_path}")

    else:
        print("Failed to scrape restaurant data")