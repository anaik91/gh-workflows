import sys
from time import sleep
import argparse
import requests

def _has_active_workers(auth_token,owner,repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runners"
    headers = {
        "Authorization" : f"Bearer {auth_token}",
        "Accept" : "application/vnd.github+json"
    }
    r = requests.get(url,headers=headers)
    print(r.status_code)
    if r.status_code != 200:
        print("Error Unable to list Self hosted runners")
        print(f"Error : {r.text}")
        sys.exit(1)
    worker_info=r.json()
    if worker_info['total_count'] > 0 :
        if worker_info['runners'][0]['status'] == 'online':
            return True,worker_info
    else:
        return False,None

def wait_for_worker(auth_token,owner,repo):
    retry = 0
    retry_count = 30
    sleep_time = 15
    while retry < retry_count:
        worker_status,worker_info=_has_active_workers(auth_token,owner,repo)
        if worker_status:
            print(f"Active Runner Detected : {worker_info['runners'][0]['name']}")
            break
        else:
            print('No Active Runner Detected')
            retry+=1
            sleep(sleep_time)

def main():
    parser = argparse.ArgumentParser(description='GH Worker Status Poller')
    parser.add_argument('--auth_token',help='Github Auth Token',required=True)
    parser.add_argument('--repo_owner',help='Github Repo Owner',required=True)
    parser.add_argument('--repo',help='Github repo',required=True)
    args = parser.parse_args()
    wait_for_worker(
        args.auth_token,
        args.repo_owner,
        args.repo
    )

if __name__ == '__main__' :
    main()