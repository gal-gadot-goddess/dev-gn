"""
Threads Upload Module for dev-gn
Uploads video to tmpfiles.org, then publishes via Meta Threads API.
Skips cleanly if THREADS_ACCESS_TOKEN or THREADS_USER_ID is not configured.
"""

import os
import requests
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def upload_to_threads(video_path, text):
    access_token = os.getenv('THREADS_ACCESS_TOKEN')
    user_id = os.getenv('THREADS_USER_ID')

    if not access_token or not user_id:
        print("[threads] ℹ️ Skipping Threads upload: credentials not configured.")
        return {'status': 'skipped', 'reason': 'Missing credentials', 'platform': 'threads'}

    video_path_obj = Path(video_path)
    if not video_path_obj.exists():
        raise FileNotFoundError(f"[threads] Video file not found: {video_path}")

    text_limited = text[:500] if len(text) > 500 else text

    try:
        with open(video_path_obj, 'rb') as video_file:
            files = {'file': ('video.mp4', video_file, 'video/mp4')}
            temp_response = requests.post(
                'https://tmpfiles.org/api/v1/upload',
                files=files,
                timeout=180
            )

        if temp_response.status_code != 200:
            raise Exception("tmpfiles.org upload failed")

        temp_data = temp_response.json()
        temp_url = temp_data.get('data', {}).get('url', '')
        video_url = temp_url.replace('tmpfiles.org/', 'tmpfiles.org/dl/').replace('http://', 'https://')

        container_url = f"https://graph.threads.net/v1.0/{user_id}/threads"
        container_params = {
            'media_type': 'VIDEO',
            'video_url': video_url,
            'text': text_limited,
            'access_token': access_token
        }
        container_response = requests.post(container_url, params=container_params, timeout=60)
        if container_response.status_code != 200:
            raise Exception(f"Container failed: {container_response.text}")

        container_id = container_response.json().get('id')

        # Poll status
        status_url = f"https://graph.threads.net/v1.0/{container_id}"
        for _ in range(12):
            time.sleep(10)
            status_data = requests.get(status_url, params={'fields': 'status', 'access_token': access_token}, timeout=30).json()
            if status_data.get('status') == 'FINISHED':
                break

        # Publish
        pub_url = f"https://graph.threads.net/v1.0/{user_id}/threads_publish"
        pub_res = requests.post(pub_url, params={'creation_id': container_id, 'access_token': access_token}, timeout=60)
        if pub_res.status_code == 200:
            return {'id': pub_res.json().get('id'), 'platform': 'threads', 'status': 'success'}
        return {'status': 'failed', 'error': pub_res.text}

    except Exception as e:
        print(f"[threads] ⚠️ Threads upload note: {e}")
        return {'status': 'skipped', 'reason': str(e), 'platform': 'threads'}
