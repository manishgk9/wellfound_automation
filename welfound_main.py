import requests
import os
from dotenv import load_dotenv
load_dotenv()
def cookie_string_to_jar(cookie_string):
    cookies={}
    for pair in cookie_string.split("; "):
        key, value = pair.split("=", 1)
        cookies[key]=value
    return cookies


def post_jobs(url:str):
    payload={
    "operationName": "CreateJobListing",
    "variables": {
        "input": {
            "allowInternationalApplicants": False,
            "allowRelocation": True,
            "equityMax": 2.5,
            "equityMin": 2,
            "filterRemote": True,
            "filterRequiresSponsorship": False,
            "jobListingAcceptedRemoteLocationIds": [],
            "locationIds": [
                "152433"
            ],
            "noEquity": False,
            "remote": False,
            "salaryMax": 10,
            "salaryMin": 0.9,
            "skillIds": [
                "14780",
                "17237"
            ],
            "relocationAssistance": False,
            "remoteConfigWfhFlexible": True,
            "remoteConfigHiringTimeZoneIds": [],
            "remoteConfigKind": "ONSITE",
            "currencyCode": "GBP",
            "description": "this mobile developer position by manish upcomming projects",
            "jobType": "cofounder",
            "live": False,
            "primaryRoleId": "14739",
            "recruitingContactId": "19317249",
            "remoteConfigCollaborationEndAt": "",
            "remoteConfigCollaborationStartAt": "",
            "remoteConfigCollaborationTimeZoneId": None,
            "remotePolicy": None,
            "startupSize": "SIZE_11_50",
            "subscriberIds": [],
            "taggedCoworkerIds": [],
            "title": "Juniar ai developer",
            "yearsExperienceMin": 2,
            "startupId": "10444826",
            "onboarding": False
        }
    },
    "extensions": {
        "operationId": "tfe/cc2cf6b4a7c89640532b2f1dcbc7af2c753197766cdc57ccca0e9980f1e962b0"
        }
    }
    headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,ko;q=0.6",
    "apollographql-client-name": "talent-web",
    "content-type": "application/json",
    "cookie": os.getenv("COOKIE_STRING"),
    "origin": "https://wellfound.com",
    "priority": "u=1, i",
    "referer": "https://wellfound.com/recruit/jobs/new",
    "sec-ch-device-memory": "4",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    "sec-ch-ua-arch": "x86",
    "sec-ch-ua-full-version-list": '"Chromium";v="134.0.6998.35", "Not:A-Brand";v="24.0.0.0", "Google Chrome";v="134.0.6998.35"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "same-origin",
    "sec-fetch-site": "same-origin",
    # "dnt":"1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "x-angellist-dd-client-referrer-resource": "/recruit/jobs/new",
    "x-apollo-operation-name": "CreateJobListing",
    "x-apollo-signature":os.getenv("X_APOLO_SIGNATURE"),
    "x-original-referer": "https://wellfound.com/login",
    "x-requested-with": "XMLHttpRequest"
    }
    session=requests.Session()
    
    try:
        response=session.post(url,json=payload,headers=headers)
        if response.status_code==200:
            print(f'status code is {response.status_code} got and data is {response.content}')
        else:
            print(f'status code is {response.status_code} got and data is {response.text}')
    except Exception as e:
        print(f"Error is found {e}")
        
print(post_jobs("https://wellfound.com/graphql"))
# https://wellfound.com/recruit/jobs/{job_id}

# import asyncio
# import cloudscraper
# import os
# # from typing import Optional

# async def post_jobs(url: str, max_retries: int = 3):
#     payload = {
#         "operationName": "CreateJobListing",
#         "variables": {
#             "input": {
#                 "allowInternationalApplicants": False,
#                 "allowRelocation": True,
#                 "equityMax": 2.5,
#                 "equityMin": 2,
#                 "filterRemote": True,
#                 "filterRequiresSponsorship": False,
#                 "jobListingAcceptedRemoteLocationIds": [],
#                 "locationIds": ["152433"],
#                 "noEquity": False,
#                 "remote": False,
#                 "salaryMax": 10,
#                 "salaryMin": 0.9,
#                 "skillIds": ["14780", "17237"],
#                 "relocationAssistance": False,
#                 "remoteConfigWfhFlexible": True,
#                 "remoteConfigHiringTimeZoneIds": [],
#                 "remoteConfigKind": "ONSITE",
#                 "currencyCode": "GBP",
#                 "description": "this osm post for mobile developer created by manish ahir for upcomming projects",
#                 "jobType": "cofounder",
#                 "live": False,
#                 "primaryRoleId": "14739",
#                 "recruitingContactId": "19317249",
#                 "remoteConfigCollaborationEndAt": "",
#                 "remoteConfigCollaborationStartAt": "",
#                 "remoteConfigCollaborationTimeZoneId": None,
#                 "remotePolicy": None,
#                 "startupSize": "SIZE_11_50",
#                 "subscriberIds": [],
#                 "taggedCoworkerIds": [],
#                 "title": "FullStack Position by manish",
#                 "yearsExperienceMin": 2,
#                 "startupId": "10444826",
#                 "onboarding": False
#             }
#         },
#         "extensions": {
#             "operationId": "tfe/cc2cf6b4a7c89640532b2f1dcbc7af2c753197766cdc57ccca0e9980f1e962b0"
#         }
#     }

#     headers = {
#         "accept": "*/*",
#         "accept-encoding": "gzip, deflate, br, zstd",
#         "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,ko;q=0.6",
#         "apollographql-client-name": "talent-web",
#         "content-type": "application/json",
#         "cookie": os.getenv("COOKIE_STRING"),
#         "origin": "https://wellfound.com",
#         "priority": "u=1, i",
#         "referer": "https://wellfound.com/recruit/jobs/new",
#         "sec-ch-device-memory": "4",
#         "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
#         "sec-ch-ua-arch": "x86",
#         "sec-ch-ua-full-version-list": '"Chromium";v="134.0.6998.35", "Not:A-Brand";v="24.0.0.0", "Google Chrome";v="134.0.6998.35"',
#         "sec-ch-ua-mobile": "?0",
#         "sec-ch-ua-model": "",
#         "sec-ch-ua-platform": '"Windows"',
#         "sec-fetch-dest": "empty",
#         "sec-fetch-mode": "same-origin",
#         "sec-fetch-site": "same-origin",
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
#         "x-angellist-dd-client-referrer-resource": "/recruit/jobs/new",
#         "x-apollo-operation-name": "CreateJobListing",
#         "x-apollo-signature": os.getenv("X_APOLO_SIGNATURE"),
#         "x-original-referer": "https://wellfound.com/login",
#         "x-requested-with": "XMLHttpRequest"
#     }

#     def sync_post(scraper, url, payload, headers):
#         try:
#             response = scraper.post(url, json=payload, headers=headers)
#             return {
#                 "status": response.status_code,
#                 "content": response.content if response.status_code == 200 else response.text
#             }
#         except Exception as e:
#             return {"status": None, "error": str(e)}

#     scraper = cloudscraper.create_scraper()

#     for attempt in range(max_retries):
#         try:
#             result = await asyncio.to_thread(sync_post, scraper, url, payload, headers)
            
#             status_code = result["status"]
#             if status_code == 200:
#                 print(f'status code is {status_code} got and data is {result["content"]}')
#                 return result
#             else:
#                 print(f'status code is {status_code} got and data is {result["content"]}')
#                 if attempt == max_retries - 1:
#                     return result
                
#         except Exception as e:
#             print(f"Attempt {attempt + 1} failed with error: {e}")
#             if attempt == max_retries - 1:
#                 print(f"Max retries ({max_retries}) reached. Giving up.")
#                 return {"status": None, "error": str(e)}
        
#         await asyncio.sleep(1) 
#     return None  

# async def main():
#     result = await post_jobs("https://wellfound.com/graphql")
#     print(f"Final result: {result}")

# if __name__ == "__main__":
#     asyncio.run(main())