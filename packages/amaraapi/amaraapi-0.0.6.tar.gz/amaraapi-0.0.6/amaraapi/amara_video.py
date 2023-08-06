import requests
import time
from .exceptions import AmaraApiException

MAX_TRIES=10


class AmaraVideo:

    def __init__(self, headers, amara_id):
        self.headers = headers
        self.amara_id = amara_id

    def get_subtitles(self, language):

        tries = 0
        ok = False
        url='https://amara.org/api/videos/'+self.amara_id+'/languages/'+language+'/subtitles/?sub_format=srt'
        while not ok and tries < MAX_TRIES:
            print("Trying {} ...".format(url))
            r = requests.get(url, headers=self.headers)
            if r.ok:
                ok = True
                subtitles_obj = r.json()
                #if 'version_number' in subtitles_obj and 'subtitles' in subtitles_obj and subtitles_obj['version_number'] > 1:
                return subtitles_obj
            elif r.status_code == 404:
                print("Not found....")
                return None
            else:
                tries += 1
                waiting_for = 2**tries
                print("Request failed with status {}, waiting for {} seconds".format(r.status_code, waiting_for))
                time.sleep(waiting_for)
        if not ok:
            raise AmaraApiException("Max tries exceeded, could not get subtitles for {}".format(url))

    def get_video_info(self):
        tries = 0
        ok = False
        if not hasattr(self, 'video_info'):
            url='https://amara.org/api/videos/'+self.amara_id+'/'
            print("Trying {} ...".format(url))
            while not ok and tries < MAX_TRIES:
                r =requests.get(url, headers=self.headers)
                if r.ok:
                    ok = True
                    self.video_info = r.json()

                elif r.status_code == 404:
                    print("Not found....")
                    return None
                else:
                    tries += 1
                    waiting_for = 2 ** tries
                    print("Request failed with status {}, waiting for {} seconds".format(r.status_code, waiting_for))
                    time.sleep(waiting_for)
            if not ok:
                raise AmaraApiException("Max tries exceeded, could not get subtitles for {}".format(url))
        return self.video_info

    def get_title(self):
        return self.get_video_info()['title']

    def get_urls(self):
        return self.get_video_info()['all_urls']

    def get_languages(self):
        return self.get_video_info()['languages']

    def get_best_subtitles(self):
        languages = self.get_languages()
        best_subtitle = None
        for language in languages:
            curr_subtitle = self.get_subtitles(language['code'])
            if not best_subtitle or (curr_subtitle and curr_subtitle['version_number'] > best_subtitle['version_number']):
                best_subtitle = curr_subtitle

        if best_subtitle:
            return best_subtitle['subtitles']
        else:
            return None

    def get_actions(self,language_code):
        url = 'https://amara.org/api/videos/'+self.amara_id+'/languages/'+language_code+'/subtitles/actions/'
        r = requests.get(url, headers=self.headers)
        self.actions = r.json()
        return self.actions

    def post_subtitles(self, language_code, subtitles):
        url = 'https://amara.org/api/videos/'+self.amara_id+'/languages/'+language_code+'/subtitles/'
        urldict = dict({'subtitles': subtitles, 'sub_format': 'srt'})
        r = requests.post(url, data=urldict, headers=self.headers)





