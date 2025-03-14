import cloudscraper
import json
from typing import Dict, List
import cookie as cookie
def cookie_string_to_jar(cookie_string):
    cookies={}
    for pair in cookie_string.split("; "):
        key, value = pair.split("=", 1)
        cookies[key]=value
    return cookies
def setup_scraper() -> cloudscraper.CloudScraper:
    try:
        scraper = cloudscraper.create_scraper()
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "apollographql-client-name": "talent-web",
            "content-type": "application/json",
            "dnt": "1",
            "cookie": cookie.COOKIE,
            "origin": "https://wellfound.com",
            "priority": "u=1, i",
            "referer": "https://wellfound.com/jobs",
            "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "same-origin",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "x-angellist-dd-client-referrer-resource": "/jobs",
            "x-apollo-operation-name": "JobSearchResultsX",
            "x-apollo-signature": cookie.X_APOLO_SIGNATURE,
            "x-original-referer": "https://wellfound.com/jobs",
            "x-requested-with": "XMLHttpRequest"
        }
        scraper.headers = headers
        # scraper.cookies=cookie_string_to_jar(cookie.COOKIE)
        return scraper
    except Exception as e:
        raise Exception(f"Failed to setup scraper: {str(e)}")

def get_payload() -> Dict:
    return {
        "operationName": "JobSearchResultsX",
        "variables": {
            "filterConfigurationInput": {
                "page": 1,
                "locationTagIds": ["406150"],
                "remoteCompanyLocationTagIds": ["153509"],
                "roleTagIds": ["751460"],
                "equity": {"min": None, "max": None},
                "jobTypes": ["full_time"],
                "remotePreference": "REMOTE_OPEN",
                "salary": {"min": None, "max": None},
                "yearsExperience": {"min": None, "max": None}
            }
        },
        "extensions": {
            "operationId": "tfe/2aeb9d7cc572a94adfe2b888b32e64eb8b7fb77215b168ba4256b08f9a94f37b"
        }
    }

def fetch_job_data(url: str, scraper: cloudscraper.CloudScraper, payload: Dict) -> bytes:
    try:
        response = scraper.post(url, json=payload)
        if response.status_code != 200:
            raise Exception(f"Request failed with status code: {response.status_code}")
        return response.content
    except Exception as e:
        raise Exception(f"Failed to fetch job data: {str(e)}")

def process_job_listings(raw_data: bytes) -> Dict[str, List[Dict]]:
    try:
        data = json.loads(raw_data)
        company_jobs = {}
        
        startups = data["data"]["talent"]["jobSearchResults"]["startups"]["edges"]
        
        for startup in startups:
            startup_node = startup["node"]
            company_name = startup_node["name"]
            company_jobs[company_name] = []
            
            for job in startup_node["highlightedJobListings"]:
                job_info = {
                    "title": job["title"],
                    "job_type": job["jobType"],
                    "compensation": job["compensation"],
                    "equity": job["equity"],
                    "remote": job["remote"],
                    "locations": job["locationNames"],
                    "primary_role": job["primaryRoleTitle"],
                    "description": job["description"],
                    "id": job["id"],
                    "slug": job["slug"]
                }
                company_jobs[company_name].append(job_info)
                
        return company_jobs
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON data: {str(e)}")
    except KeyError as e:
        raise Exception(f"Unexpected data structure: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to process job listings: {str(e)}")

def scrape_jobs() -> Dict[str, List[Dict]]:
    url = "https://wellfound.com/graphql"
    try:
        scraper = setup_scraper()
        payload = get_payload()
        raw_data = fetch_job_data(url, scraper, payload)
        company_jobs = process_job_listings(raw_data)
        
        return company_jobs
        
    except Exception as e:
        raise Exception(f"Job scraping failed: {str(e)}")

def main():
    try:
        jobs_by_company = scrape_jobs()
        print(jobs_by_company)       
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()