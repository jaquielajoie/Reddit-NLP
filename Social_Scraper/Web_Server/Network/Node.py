from Social_Scraper import db
#from Social_Scraper.Web_Server.DBModels_Reddit import DBNode
from datetime import datetime

class Node:
    def __init__(self, identifier, description, type, parent_id=None):
        self.identifier = identifier
        self.description = description
        self.type = type
        self.parent_id = parent_id
        #self.rtrn_node = self.save_to_db()
        #self.mongo_id = self.rtrn_node._id

    def get_id(self):
        #if str(type(self)) == "<class 'Reddit_User.Reddit_User'>":
            #return str('Username: ' + self.identifier)
        '''
        if str(type(self)) == "<class 'Reddit_Post.JokePost'>":
            return str(self.description)


        if str(type(self)) == "<class 'Reddit_Comment.Reddit_Comment'>":
            return str(self.description)

        '''
        return str(self.identifier)
    def get_description(self):
        return str(self.description)

    def save_to_db(self):
        attr = {}
        attr['identifer'] = self.identifier
        attr['description'] = self.description
        attr['type'] = self.type
        attr['parent_id'] = self.parent_id
        nodes = db.nodes
        rtrn_node = nodes.insert({
            'node_data': attr
        })
        return rtrn_node

        '''
        node = DBNode(identifier=str(self.identifier),description=str(self.description),date_created=datetime.now())
        db.session.add(node)
        db.session.commit()
        '''
