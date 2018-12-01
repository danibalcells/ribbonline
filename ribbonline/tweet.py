import dateparser

from . import constants
from .util import has_emoji


class Tweet(object):

    def __init__(self, raw_data):
        # self.raw_data = raw_data
        self.id = raw_data['id']
        self.text = raw_data['html']
        self.username = raw_data['fullname']
        self.user_description = ''  # For now
        #  self.user_id = raw_data['user']['id']
        # self.date = dateparser.parse(raw_data['created_at'].replace('+0000 ',''))
    
    @property
    def text_has_ribbon(self):
        return has_emoji(self.text, constants.EMOJI_RIBBON)
    
    @property
    def username_has_ribbon(self):
        return has_emoji(self.username, constants.EMOJI_RIBBON)
    
    @property
    def user_description_has_ribbon(self):
        return has_emoji(self.user_description, constants.EMOJI_RIBBON)
    
    @property
    def text_has_flag(self):
        return has_emoji(self.text, constants.EMOJI_FLAG)
    
    @property
    def username_has_flag(self):
        return has_emoji(self.username, constants.EMOJI_FLAG)
    
    @property
    def user_description_has_flag(self):
        return has_emoji(self.user_description, constants.EMOJI_FLAG)
