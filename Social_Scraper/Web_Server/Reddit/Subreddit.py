from Social_Scraper.Web_Server.Network.Node import Node

class Subreddit(Node):
    def __init__(self, sub_name, description):
        super().__init__(identifier=sub_name, description=description, type=str(self))
        self.sub_name = sub_name
        self.description = description
        self.type = type
        self.url = f'https://www.reddit.com/r/{sub_name}'
