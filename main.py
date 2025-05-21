import json
from datetime import datetime
from restro_details_scraper import scrape_lieferando

def print_log(message, level="INFO"):
    """Helper function to print formatted log messages"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - {level} - {message}")

cookies = {
    'siteLanguage': 'en',
    'je-auser': '4e1749f7-51d8-43a4-8e18-f4ad3dba233b',
    'deviceLocationPermissionGranted': 'false',
    'je-cookieConsent': 'full',
    'customerCookieConsent': '%5B%7B%22consentTypeId%22%3A103%2C%22consentTypeName%22%3A%22necessary%22%2C%22isAccepted%22%3Atrue%2C%22decisionAt%22%3A%222025-05-20T08%3A27%3A56.0000000%2B00%3A00%22%7D%2C%7B%22consentTypeId%22%3A104%2C%22consentTypeName%22%3A%22functional%22%2C%22isAccepted%22%3Atrue%2C%22decisionAt%22%3A%222025-05-20T08%3A27%3A56.0000000%2B00%3A00%22%7D%2C%7B%22consentTypeId%22%3A105%2C%22consentTypeName%22%3A%22analytical%22%2C%22isAccepted%22%3Atrue%2C%22decisionAt%22%3A%222025-05-20T08%3A27%3A56.0000000%2B00%3A00%22%7D%2C%7B%22consentTypeId%22%3A106%2C%22consentTypeName%22%3A%22personalized%22%2C%22isAccepted%22%3Atrue%2C%22decisionAt%22%3A%222025-05-20T08%3A27%3A56.0000000%2B00%3A00%22%7D%5D',
    '_gcl_au': '1.1.1171915029.1747729677',
    '_ga': 'GA1.1.4e1749f7-51d8-43a4-8e18-f4ad3dba233b',
    '_pin_unauth': 'dWlkPU9HRXpOak00TURVdFltSTFNaTAwWlRKbExXSTRZek10WVRJMVptUXpZalV6WVdZeA',
    '_scid': 'FRkEq8CRc1KVnkrpfn7UBfkuwCm5nTKv',
    '_fbp': 'fb.1.1747729677644.24991599728435861',
    '_tt_enable_cookie': '1',
    '_ttp': '01JVPCWZF86BM2YNQ7RCTWXSDF_.tt.1',
    '_sctr': '1%7C1747679400000',
    'ab.storage.deviceId.f543a405-bc6b-4dfa-b736-f6a0d6884bad': '%7B%22g%22%3A%222719dc6e-77de-5edd-869a-57ace6754c2e%22%2C%22c%22%3A1747729686987%2C%22l%22%3A1747729686987%7D',
    'activeAddress': '%7B%22address%22%3A%7B%22location%22%3A%7B%22lat%22%3A50.969316%2C%22lng%22%3A13.8738134%2C%22locationSlug%22%3A%2201809%22%7D%7D%7D',
    'cookieConsent': 'full',
    'cookieConsent': '%22full%22',
    'jet-sp-customer-ses.5f43': '*',
    '__cf_bm': 'l1eQmysB6BlMo4WJhG.AJQLeO6QSD_Ke2okC8riimlM-1747808492-1.0.1.1-apRMbRjTFEt7YwkEX9LeoAEBFX.RQ4ogglK9tf3JP22Ob0hIdvqT1_ZeeOr.qQ15Ux6oVjN1IJE4xBp.J0NbtZ.3KzjRq5ZNw6LEuWBdOC_TFfHLXcEyIvSoOqRQVvlP',
    '_ga_VJTENYSCXJ': 'GS2.1.sa734e963-749a-4c71-8c07-1bd1a37cfb08$o3$g0$t1747809309$j0$l0$h0',
    'cwSession': '%7B%22id%22%3A%2280a42fcd-5dcb-4845-87f0-63993364db48%22%7D',
    'cf_clearance': 'fPhSecfQt.OCqyXosEjuW95k2JBUpXgDOClKnfhpwuE-1747809593-1.2.1.1-unj09EmL0ZAkyLQXUxq7CAGOMJEyyzpRMDQVcOr5un2gbptvMSuil8RlieozoIRWVQIHhcQ0L8eqnPpNKeoi27uQtcIoHppI_UoT2Jxt9WUsKmhUR_Kb6JQmszPfL8WVX29jM.ryuM9KfHN.3qWFwXUWAZ39DHRoOB6EuzU9JPr1uRk5iyp1yuYH.PQOOapxYSoPvXXcNMo3LOxvTnJrA7blnAn.9Q7S2Vffh9ytLBYLNaDLOstl.8_HUDOPKwPIZNi3b5dIbT4W4Gmh7aElSX.NBgYQL7XWSJVgpUu2gh1JFoU_L5g3muPFgW33Vbpok.pytiKxFWV_bOww7D6BkSS37JwxCq7Syni45tqV4xTK1c5ec8OPLmZ5tOJk5x0R',
    '_ga_4PH28YDTSD': 'GS2.1.s1747807431$o3$g1$t1747809324$j0$l0$h0',
    'jet-sp-customer-id.5f43': '3f0ecb99-c4a7-4e81-8579-e493c533088e.1747729677.3.1747809324.1747748799.a734e963-749a-4c71-8c07-1bd1a37cfb08.10a788bd-ee59-46b6-a3a9-4b154778593d.25c5696d-862f-485e-b277-7f8ace052731.1747807430147.26',
    '_scid_r': 'LZkEq8CRc1KVnkrpfn7UBfkuwCm5nTKvOWbhUg',
    '_uetsid': '5575ea60355411f0bfbcf5e373c5f3a5',
    '_uetvid': '55762000355411f084c0f5d3ccd1bafd',
    'ttcsid_C8LGUFCO0T91FSTH4960': '1747809324750::-u-H9K8Gsn74ZLWNkNvJ.1.1747809324752',
    'ttcsid': '1747809324750::YM8ezG-6_pSEECeS7-is.1.1747809324753',
    '_ScCbts': '%5B%5D',
    '_dd_s': 'aid=8d9181dd-1179-419e-bb58-8871879ccf22&logs=1&id=00c31eff-e98c-4b93-8521-d92ee357365d&created=1747807429009&expire=1747810265764&rum=0',
}

try:
    print_log("Starting restaurant data scraping...")
    
    # Load restaurant links
    with open('restro_links.json', 'r') as file:
        restro_links = json.load(file)
        print_log(f"Loaded {len(restro_links)} restaurant URLs to scrape")

    success_count = 0
    fail_count = 0

    for idx, url in enumerate(restro_links, 1):
        print_log(f"Processing URL {idx}/{len(restro_links)}: {url}")
        
        try:
            result = scrape_lieferando(url, cookies)
            result['url'] = url
            export_save_file_path = './output/' + url.split('/')[-1] + '.json'
            
            if result:
                with open(export_save_file_path, 'w') as json_file:
                    json.dump(result, json_file, indent=4)
                
                print_log(f"Successfully exported data to {export_save_file_path}")
                success_count += 1
            else:
                print_log(f"Failed to scrape data from {url}", level="WARNING")
                fail_count += 1
                
        except Exception as e:
            print_log(f"Error processing {url}: {str(e)}", level="ERROR")
            fail_count += 1
            continue  # Continue with next URL even if one fails

    # Summary
    print_log("Scraping process completed")
    print_log(f"Results: {success_count} succeeded, {fail_count} failed")

except FileNotFoundError:
    print_log("Error: restro_links.json file not found", level="ERROR")
except json.JSONDecodeError:
    print_log("Error: Invalid JSON format in restro_links.json", level="ERROR")
except Exception as e:
    print_log(f"Unexpected error: {str(e)}", level="ERROR")
finally:
    print_log("Script execution finished")