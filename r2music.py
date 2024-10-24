import os
import cv2
from flask import Flask, render_template, request, redirect, url_for
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser

# Set up environment variable to skip dotenv
os.environ['FLASK_SKIP_DOTENV'] = '1'

# Spotify setup
CLIENT_ID = '05379b84b9844aa9a8c17c66da1ed8b2'  # Replace with your actual Client ID
CLIENT_SECRET = '75b059e18c0545af9a0e1d684d3b9875'  # Replace with your actual Client Secret
REDIRECT_URI = 'http://localhost:7777/callback'

scope = "user-library-read playlist-modify-public user-read-playback-state user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=scope))

# Map emotions to songspip list
emotion_to_tracks = {
    'happy': [
        {'uri': 'spotify:track:0XgoXio6L2d5tFhIq0K0ty', 'url': 'https://open.spotify.com/track/0XgoXio6L2d5tFhIq0K0ty', 'name': 'Happy Song 1'},
        {'uri': 'spotify:track:60nZcImufyMA1MKQY3dcCH', 'url': 'https://open.spotify.com/track/60nZcImufyMA1MKQY3dcCH', 'name': 'Happy Song 2'},
        {'uri': 'spotify:track:19kHhX6f6EfLU7rcO3RqjO', 'url': 'https://open.spotify.com/track/19kHhX6f6EfLU7rcO3RqjO', 'name': 'Happy Song 3'},
        {'uri': 'spotify:track:5Hroj5K7vLpIG4FNCRIjbP', 'url': 'https://open.spotify.com/track/5Hroj5K7vLpIG4FNCRIjbP', 'name': 'Happy Song 4'},
        {'uri': 'spotify:track:0GRRNKl329iGEvGRXQPj7q', 'url': 'https://open.spotify.com/track/0GRRNKl329iGEvGRXQPj7q', 'name': 'Happy Song 5'},
        {'uri': 'spotify:track:2LNe50dfsa7WaFa7LprfQg?si=c3260d28075e4b18', 'url': 'https://open.spotify.com/track/2LNe50dfsa7WaFa7LprfQg?si=c3260d28075e4b18', 'name': 'Happy Song 6'},
        {'uri': 'spotify:track:4vYOlnNVjEfuac7wqJiPbQ?si=0094fcb80a1b41ec', 'url': 'https://open.spotify.com/track/4vYOlnNVjEfuac7wqJiPbQ?si=0094fcb80a1b41ec', 'name': 'Happy Song 7'},
        {'uri': 'spotify:track:1XvOEvWtfa879Wk1wKHZ1M?si=811fdea6d797464f', 'url': 'https://open.spotify.com/track/1XvOEvWtfa879Wk1wKHZ1M?si=811fdea6d797464f', 'name': 'Happy Song 8'},
        {'uri': 'spotify:track:3zkvkUnWZ1SfqcdNcqotJT', 'url': 'https://open.spotify.com/track/3zkvkUnWZ1SfqcdNcqotJT', 'name': 'Happy Song 9'},
        {'uri': 'spotify:track:4vYOlnNVjEfuac7wqJiPbQ', 'url': 'https://open.spotify.com/track/4vYOlnNVjEfuac7wqJiPbQ', 'name': 'Happy Song 10'},
        {'uri': 'spotify:track:4DPLka2ZhnPdHzzci7vX1n', 'url': 'https://open.spotify.com/track/4DPLka2ZhnPdHzzci7vX1n', 'name': 'Happy Song 11'},
        {'uri': 'spotify:track:4126keCXZXzCRtmcuPcBWw', 'url': 'https://open.spotify.com/track/4126keCXZXzCRtmcuPcBWw', 'name': 'Happy Song 12'},
        {'uri': 'spotify:track:6JV2JOEocMgcZxYSZelKcc', 'url': 'https://open.spotify.com/track/6JV2JOEocMgcZxYSZelKcc', 'name': 'Happy Song 13'},
        {'uri': 'spotify:track:05wIrZSwuaVWhcv5FfqeH0', 'url': 'https://open.spotify.com/track/05wIrZSwuaVWhcv5FfqeH0', 'name': 'Happy Song 14'},
        {'uri': 'spotify:track:2A6jI1szK1aFzSK8i4ceq5', 'url': 'https://open.spotify.com/track/2A6jI1szK1aFzSK8i4ceq5', 'name': 'Happy Song 15'},
        {'uri': 'spotify:track:3lOpUMMUskknPD3dJR2MkT', 'url': 'https://open.spotify.com/track/3lOpUMMUskknPD3dJR2MkT', 'name': 'Happy Song 16'},
        {'uri': 'spotify:track:56v8WEnGzLByGsDAXDiv4d', 'url': 'https://open.spotify.com/track/56v8WEnGzLByGsDAXDiv4d', 'name': 'Happy Song 17'},
        {'uri': 'spotify:track:4QtFRUFS7BVi3OHUfmt2dP', 'url': 'https://open.spotify.com/track/4QtFRUFS7BVi3OHUfmt2dP', 'name': 'Happy Song 18'},
        {'uri': 'spotify:track:2EFk8PEXvVglkAOI3IOTAw', 'url': 'https://open.spotify.com/track/2EFk8PEXvVglkAOI3IOTAw', 'name': 'Happy Song 19'},
        {'uri': 'spotify:track:7gcMKL3lnDxsp4bIXyv6Zk', 'url': 'https://open.spotify.com/track/7gcMKL3lnDxsp4bIXyv6Zk', 'name': 'Happy Song 20'}
    ],

    'sad': [
        {'uri': 'spotify:track:1Y84d8A6RpteKamrSWGQ04', 'url': 'https://open.spotify.com/track/1Y84d8A6RpteKamrSWGQ04', 'name': 'Sad Song 1'},
        {'uri': 'spotify:track:2fhOljbX79loRcdl47SFye', 'url': 'https://open.spotify.com/track/2fhOljbX79loRcdl47SFye', 'name': 'Sad Song 2'},
        {'uri': 'spotify:track:0ZaN8nowyYANp4vWTLfAZs', 'url': 'https://open.spotify.com/track/0ZaN8nowyYANp4vWTLfAZs', 'name': 'Sad Song 3'},
        {'uri': 'spotify:track:6n4ayixQF0Qc5EBjKrgBrh', 'url': 'https://open.spotify.com/track/6n4ayixQF0Qc5EBjKrgBrh', 'name': 'Sad Song 4'},
        {'uri': 'spotify:track:73BpzXbQ2wdMayh1urk3p5', 'url': 'https://open.spotify.com/track/73BpzXbQ2wdMayh1urk3p5', 'name': 'Sad Song 5'},
        {'uri': 'spotify:track:4gDzUzSgwhXuGXNGuBQVVm', 'url': 'https://open.spotify.com/track/4gDzUzSgwhXuGXNGuBQVVm', 'name': 'Sad Song 6'},
        {'uri': 'spotify:track:752ZFsGMUthS2TqdXppvWl', 'url': 'https://open.spotify.com/track/752ZFsGMUthS2TqdXppvWl', 'name': 'Sad Song 7'},
        {'uri': 'https://open.spotify.com/track/7LVHVU3tWfcxj5aiPFEW4Q', 'url': 'https://open.spotify.com/track/7LVHVU3tWfcxj5aiPFEW4Q', 'name': 'Sad Song 8'},
        {'uri': 'spotify:track:3bNv3VuUOKgrf5hu3YcuRo', 'url': 'https://open.spotify.com/track/3bNv3VuUOKgrf5hu3YcuRo', 'name': 'Sad Song 9'},
        {'uri': 'spotify:track:1VdZ0vKfR5jneCmWIUAMxK', 'url': 'https://open.spotify.com/track/1VdZ0vKfR5jneCmWIUAMxK', 'name': 'Sad Song 10'},
        {'uri': 'spotify:track:2ndWbjiiNBEOrlfToKlABE', 'url': 'https://open.spotify.com/track/2ndWbjiiNBEOrlfToKlABE', 'name': 'Sad Song 11'},
        {'uri': 'spotify:track:7onjRqhbRtJWMhkuT9XopO', 'url': 'https://open.spotify.com/track/7onjRqhbRtJWMhkuT9XopO', 'name': 'Sad Song 12'},
        {'uri': 'spotify:track:7KTlvOc9yjSv9p1f2rkJ6I', 'url': 'https://open.spotify.com/track/7KTlvOc9yjSv9p1f2rkJ6I', 'name': 'Sad Song 13'},
        {'uri': 'spotify:track:https://open.spotify.com/track/1l2pTuZmdz0dgbaBjL4vJD', 'url': 'https://open.spotify.com/track/1l2pTuZmdz0dgbaBjL4vJD', 'name': 'Sad Song 14'},
        {'uri': 'spotify:track:08MFgEQeVLF37EyZ7jcwLc', 'url': 'https://open.spotify.com/track/08MFgEQeVLF37EyZ7jcwLc', 'name': 'Sad Song 15'},
        {'uri': 'spotify:track:1Fid2jjqsHViMX6xNH70hE', 'url': 'https://open.spotify.com/track/1Fid2jjqsHViMX6xNH70hE', 'name': 'Sad Song 16'},
        {'uri': 'spotify:track:5ysqI7Q5QfZOKistxWCAp1', 'url': 'https://open.spotify.com/track/5ysqI7Q5QfZOKistxWCAp1', 'name': 'Sad Song 17'},
        {'uri': 'spotify:track:5hiQSNo6jQbQ2m2gBZs7bU', 'url': 'https://open.spotify.com/track/5hiQSNo6jQbQ2m2gBZs7bU', 'name': 'Sad Song 18'},
        {'uri': 'spotify:track:6qqNVTkY8uBg9cP3Jd7DAH', 'url': 'https://open.spotify.com/artist/6qqNVTkY8uBg9cP3Jd7DAH', 'name': 'Sad Song 19'},
        {'uri': 'spotify:track:6wf7Yu7cxBSPrRlWeSeK0Q', 'url': 'https://open.spotify.com/track/6wf7Yu7cxBSPrRlWeSeK0Q', 'name': 'Sad Song 20'}

    ],
    'angry': [
        {'uri': 'spotify:track:1IT0WQk5J8NsaeII8ktdlZ', 'url': 'https://open.spotify.com/track/1IT0WQk5J8NsaeII8ktdlZ', 'name': 'Angry Song 1'},
        {'uri': 'spotify:track:285pBltuF7vW8TeWk8hdRR', 'url': 'https://open.spotify.com/track/285pBltuF7vW8TeWk8hdRR', 'name': 'Angry Song 2'},
        {'uri': 'spotify:track:3FUS56gKr9mVBmzvlnodlh', 'url': 'https://open.spotify.com/track/3FUS56gKr9mVBmzvlnodlh', 'name': 'Angry Song 3'},
        {'uri': 'spotify:track:7kCPZBztxoo8QbmiWs5fku', 'url': 'https://open.spotify.com/track/7kCPZBztxoo8QbmiWs5fku', 'name': 'Angry Song 4'},
        {'uri': 'spotify:track:4rjTi6f0ZtmDw8Uc3MFE6M', 'url': 'https://open.spotify.com/track/4rjTi6f0ZtmDw8Uc3MFE6M', 'name': 'Angry Song 5'},
        {'uri': 'spotify:track:6aNhF17w3I25xxLmX8bM8r', 'url': 'https://open.spotify.com/track/6aNhF17w3I25xxLmX8bM8r', 'name': 'Angry Song 6'},
        {'uri': 'spotify:track:2yYX7KbfWZrezWVW1vN3iz?si=92acfc2ec60f463b', 'url': 'https://open.spotify.com/track/2yYX7KbfWZrezWVW1vN3iz?si=92acfc2ec60f463b', 'name': 'Angry Song 7'},
        {'uri': 'spotify:track:0UqDHyajhOTknbgj1IjuNM?si=0c393a5a28624aa4', 'url': 'https://open.spotify.com/track/0UqDHyajhOTknbgj1IjuNM?si=0c393a5a28624aa4', 'name': 'Angry Song 8'},
        {'uri': 'spotify:track:0WSa1sucoNRcEeULlZVQXj?si=f89ef9d602204381', 'url': 'https://open.spotify.com/track/0WSa1sucoNRcEeULlZVQXj?si=f89ef9d602204381', 'name': 'Angry Song 9'},
        {'uri': 'spotify:track:4bJygwUKrRgq1stlNXcgMg?si=991cd6bb90f74776', 'url': 'https://open.spotify.com/track/4bJygwUKrRgq1stlNXcgMg?si=991cd6bb90f74776', 'name': 'Angry Song 10'},
        {'uri': 'spotify:track:2yYX7KbfWZrezWVW1vN3iz?si=c2e1adcb14394a97', 'url': 'https://open.spotify.com/track/2yYX7KbfWZrezWVW1vN3iz?si=c2e1adcb14394a97', 'name': 'Angry Song 11'},
        {'uri': 'spotify:track:2KGdxXnW10v0nTXay9AElG', 'url': 'https://open.spotify.com/track/2KGdxXnW10v0nTXay9AElG', 'name': 'Angry Song 12'}
    ],
    'surprise': [
        {'uri': 'spotify:track:4rlQza35DE4Prh5yonxnCs', 'url': 'https://open.spotify.com/track/4rlQza35DE4Prh5yonxnCs', 'name': 'Surprise Song 1'},
        {'uri': 'spotify:track:5p3xMIHQ6YoAIaSgZeOkNa?si=5f8bcc4a8e6c4e25', 'url': 'https://open.spotify.com/track/5p3xMIHQ6YoAIaSgZeOkNa?si=5f8bcc4a8e6c4e25', 'name': 'Surprise Song 2'},
        {'uri': 'spotify:track:5rkhImAE9y8vHwWPjfkx61?si=1b50b8d8da4541c8', 'url': 'https://open.spotify.com/track/5rkhImAE9y8vHwWPjfkx61?si=1b50b8d8da4541c8', 'name': 'Surprise Song 3'},
        {'uri': 'spotify:track:40cAclLDpkh2M8GGmIpVoM', 'url': 'https://open.spotify.com/track/40cAclLDpkh2M8GGmIpVoM', 'name': 'Surprise Song 4'},
        {'uri': 'spotify:track:2xizRhme7pYeITbH1NLLGt?si=8b7fc8c1fb0b498b', 'url': 'https://open.spotify.com/track/2xizRhme7pYeITbH1NLLGt?si=8b7fc8c1fb0b498b', 'name': 'Surprise Song 5'},
        {'uri': 'spotify:track:3By9jCy6b4dv5XnlhvIWwx?si=5a32fa5a8fb84397', 'url': 'https://open.spotify.com/track/3By9jCy6b4dv5XnlhvIWwx?si=5a32fa5a8fb84397', 'name': 'Surprise Song 6'},
        {'uri': 'spotify:track:4kjZGzoruRTzapDQA6H3Hj?si=0b087b6124074ae6', 'url': 'https://open.spotify.com/track/4kjZGzoruRTzapDQA6H3Hj?si=0b087b6124074ae6', 'name': 'Surprise Song 7'},
        {'uri': 'spotify:track:5rkhImAE9y8vHwWPjfkx61?si=1b50b8d8da4541c8', 'url': 'https://open.spotify.com/track/5rkhImAE9y8vHwWPjfkx61?si=1b50b8d8da4541c8', 'name': 'Surprise Song 8'},
        {'uri': 'spotify:track:2HoqbEOXgbDSLZ5XCePEXt?si=ddf5eebd043946a4', 'url': 'https://open.spotify.com/track/2HoqbEOXgbDSLZ5XCePEXt?si=ddf5eebd043946a4', 'name': 'Surprise Song 9'},
        {'uri': 'spotify:track:3hwuHzRicnu6Ji9i1JLzor?si=c35c92c86dab4696', 'url': 'https://open.spotify.com/track/3hwuHzRicnu6Ji9i1JLzor?si=c35c92c86dab4696', 'name': 'Surprise Song 10'},
        {'uri': 'spotify:track:1WBagB7FdOlxUpYTG9XVik?si=1233e062015c44f1', 'url': 'https://open.spotify.com/track/1WBagB7FdOlxUpYTG9XVik?si=1233e062015c44f1', 'name': 'Surprise Song 11'},
        {'uri': 'spotify:track:4AFsRbaLKRWo3dDtjDFA2V?si=0dd68c1c2ec64754', 'url': 'https://open.spotify.com/track/4AFsRbaLKRWo3dDtjDFA2V?si=0dd68c1c2ec64754', 'name': 'Surprise Song 12'},
        {'uri': 'spotify:track:26EM9sZnQkLLQxixGd88KE?si=b9f15825a0fc49d7', 'url': 'https://open.spotify.com/track/26EM9sZnQkLLQxixGd88KE?si=b9f15825a0fc49d7', 'name': 'Surprise Song 13'},
        {'uri': 'spotify:track:2ihCaVdNZmnHZWt0fvAM7B?si=9ff2376625204295', 'url': 'https://open.spotify.com/track/2ihCaVdNZmnHZWt0fvAM7B?si=9ff2376625204295', 'name': 'Surprise Song 14'},
        {'uri': 'spotify:track:3dI59jLoFMjMAyUAyRZnkE?si=df79f83fdb794368', 'url': 'https://open.spotify.com/track/3dI59jLoFMjMAyUAyRZnkE?si=df79f83fdb794368', 'name': 'Surprise Song 15'}
    ],
    'neutral': [
        {'uri': 'spotify:track:3J2WUEn6oFN8eDPZov7w9I', 'url': 'https://open.spotify.com/track/3J2WUEn6oFN8eDPZov7w9I', 'name': 'Neutral Song 1'},
        {'uri': 'spotify:track:1Yk0cQdMLx5RzzFTYwmuld', 'url': 'https://open.spotify.com/track/1Yk0cQdMLx5RzzFTYwmuld', 'name': 'Neutral Song 2'},
        {'uri': 'spotify:track:2nbMCBBmKc3B6A30jYPmpD?si=8f34d1f9dc4a4d0a', 'url': 'https://open.spotify.com/track/2nbMCBBmKc3B6A30jYPmpD?si=8f34d1f9dc4a4d0a', 'name': 'Neutral Song 3'},
        {'uri': 'spotify:track:2L5WJA8XcCnczIVhujMNcZ?si=07f44c7ea8834a18', 'url': 'https://open.spotify.com/track/2L5WJA8XcCnczIVhujMNcZ?si=07f44c7ea8834a18', 'name': 'Neutral Song 4'},
        {'uri': 'spotify:track:53PCccWVUMrahgaRvpIcXf?si=61db41e91490413f', 'url': 'https://open.spotify.com/track/53PCccWVUMrahgaRvpIcXf?si=61db41e91490413f', 'name': 'Neutral Song 5'},
        {'uri': 'spotify:5NdezYYKee6x3Q321GcGka?si=964f2a1d9681401a', 'url': 'https://open.spotify.com/track/5NdezYYKee6x3Q321GcGka?si=964f2a1d9681401a', 'name': 'Neutral Song 6'},
        {'uri': 'spotify:track:2EM3z870MwvKASPO23MeUB?si=4306394808504d66', 'url': 'https://open.spotify.com/track/2EM3z870MwvKASPO23MeUB?si=4306394808504d66', 'name': 'Neutral Song 7'},
        {'uri': 'spotify:track:2agBDIr9MYDUducQPC1sFU?si=312b44f24d324862', 'url': 'https://open.spotify.com/track/2agBDIr9MYDUducQPC1sFU?si=312b44f24d324862', 'name': 'Neutral Song 8'},
        {'uri': 'spotify:track:76AyhBEQaq3QrjnFTiqEnm?si=61c76115fb3f49a3', 'url': 'https://open.spotify.com/track/76AyhBEQaq3QrjnFTiqEnm?si=61c76115fb3f49a3', 'name': 'Neutral Song 9'},
        {'uri': 'spotify:track:1b9bGEtNOmiMD5gq7dGrxn?si=bbc32ae28f6c49f3', 'url': 'https://open.spotify.com/track/1b9bGEtNOmiMD5gq7dGrxn?si=bbc32ae28f6c49f3', 'name': 'Neutral Song 10'},
        {'uri': 'spotify:track:6qUjY7JsuQYxn99qfOAQyB?si=fafef73daf264dfd', 'url': 'https://open.spotify.com/track/6qUjY7JsuQYxn99qfOAQyB?si=fafef73daf264dfd', 'name': 'Neutral Song 11'},
        {'uri': 'spotify:track:29U7stRjqHU6rMiS8BfaI9?si=b58b79eef94c4fa7', 'url': 'https://open.spotify.com/track/29U7stRjqHU6rMiS8BfaI9?si=b58b79eef94c4fa7', 'name': 'Neutral Song 12'},
        {'uri': 'spotify:track:5jgFfDIR6FR0gvlA56Nakr?si=1ddba909723f442d', 'url': 'https://open.spotify.com/track/5jgFfDIR6FR0gvlA56Nakr?si=1ddba909723f442d', 'name': 'Neutral Song 13'},
        {'uri': 'spotify:track:1qzvzPfqzpNQ01ZBOEkVlf?si=d9a28c4bcc9d4e05', 'url': 'https://open.spotify.com/track/1qzvzPfqzpNQ01ZBOEkVlf?si=d9a28c4bcc9d4e05', 'name': 'Neutral Song 14'},
        {'uri': 'spotify:track:01aVuBzov1TL2iCNhwkguC?si=2591b1543c794dd9', 'url': 'https://open.spotify.com/track/01aVuBzov1TL2iCNhwkguC?si=2591b1543c794dd9', 'name': 'Neutral Song 15'},
        {'uri': 'spotify:track:1bSGr3yVE0tBBhyUqlrBkx', 'url': 'https://open.spotify.com/track/1bSGr3yVE0tBBhyUqlrBkx', 'name': 'Neutral Song 16'},
        {'uri': 'spotify:track:6dGnYIeXmHdcikdzNNDMm2?si=3c63edba0c654342', 'url': 'https://open.spotify.com/track/6dGnYIeXmHdcikdzNNDMm2?si=3c63edba0c654342','name': 'Neutral Song 17'},
        {'uri': 'spotify:track:76AyhBEQaq3QrjnFTiqEnm?si=61c76115fb3f49a3', 'url': 'https://open.spotify.com/track/76AyhBEQaq3QrjnFTiqEnm?si=61c76115fb3f49a3', 'name': 'Neutral Song 18'},
        {'uri': 'spotify:track:5CUQnKjA6nlteCnxMKsjIu?si=00547ece18244cbc', 'url': 'https://open.spotify.com/track/5CUQnKjA6nlteCnxMKsjIu?si=00547ece18244cbc', 'name': 'Neutral Song 19'},
        {'uri': 'spotify:track:3Srw8isgDzmYsgwDi4MtbD?si=3f47a818aeaa4add', 'url': 'https://open.spotify.com/track/3Srw8isgDzmYsgwDi4MtbD?si=3f47a818aeaa4add', 'name': 'Neutral Song 20'}
    ]
}

r2music = Flask(__name__)

@r2music.route('/')
def index():
    return render_template('index.html')

@r2music.route('/capture', methods=['POST'])
def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Unable to open camera", 500

    ret, frame = cap.read()
    if not ret:
        return "Failed to capture image", 500

    cv2.imwrite("captured_image.jpg", frame)
    cap.release()
    cv2.destroyAllWindows()

    try:
        img = cv2.imread("captured_image.jpg")
        results = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)

        if results:
            if isinstance(results, list) and len(results) > 0:
                emotion = results[0]['dominant_emotion']

                if emotion in emotion_to_tracks:
                    tracks = emotion_to_tracks[emotion]
                    return render_template('song_selection.html', emotion=emotion, tracks=tracks)
                else:
                    return "No track found for this emotion", 404
            else:
                return "No emotions detected in the results", 404
        else:
            return "No emotion detected", 404
    except Exception as e:
        return f"Error: {str(e)}", 500

@r2music.route('/play', methods=['POST'])
def play_song():
    selected_track_url = request.form.get('track_url')
    if selected_track_url:
        webbrowser.open(selected_track_url)
        return redirect(url_for('index'))
    return "No track selected", 400

if __name__ == '__main__':
    r2music.run(debug=True)



def app():
    return None