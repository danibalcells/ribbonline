class DailyOpinionSplit(object):
    
    def __init__(self, date, tweet_collection):
        self.date = date
        self.tweet_collection = tweet_collection
        self.text_has_ribbon = \
            self.tweet_collection.text_has_ribbon.length
        self.username_has_ribbon = \
            self.tweet_collection.username_has_ribbon.length
        self.user_description_has_ribbon = \
            self.tweet_collection.user_description_has_ribbon.length
        self.text_has_flag = \
            self.tweet_collection.text_has_flag.length
        self.username_has_flag = \
            self.tweet_collection.username_has_flag.length
        self.user_description_has_flag = \
            self.tweet_collection.user_description_has_flag.length
        self.neutral = (self.tweet_collection.length - 
                        self.text_has_ribbon - 
                        self.username_has_ribbon -
                        self.user_description_has_ribbon -
                        self.text_has_flag -
                        self.username_has_flag -
                        self.user_description_has_flag)
    
    @property
    def list(self):
        return [
            self.text_has_ribbon,
            self.username_has_ribbon,
            self.user_description_has_ribbon,
            self.neutral,
            self.user_description_has_flag,
            self.username_has_flag,
            self.text_has_flag,
        ]
