#from Social_Scraper import db
#from Social_Scraper.Web_Server.DBModels_Reddit import DBNode
from datetime import datetime
from Social_Scraper import db

class Edge:
    def __init__(self, sender, receiver, weight, type, save_to_db=True):

        #self.id = sender.get_id() + '_' + receiver.get_id()
        self.sender = sender
        self.receiver = receiver
        self.weight = weight
        self.type = type
        #What is the parent network? Network -> Sender -> Receiver
        #self.network = network
        if save_to_db: self.save_to_db()
        #self.direction = f'{self.sender.get_id()} to {self.receiver.get_id()} with weight: {self.weight}'

    def get_sender(self):
        return self.sender

    def get_receiver(self):
        return self.receiver

    def description(self):
        return self.receiver.get_description()

    def save_to_db(self):
        #parent_id = self.receiver.mongo_id

        '''
        SEE IF RECEIVER ALREADY EXISTS, if so, update
        '''
        existing_receiver = db.nodes.find({"node_data.identifier": self.receiver.identifier})#.sort(:-1).limit(1)
        if existing_receiver.count() > 0:
            for record in existing_receiver:
                print(record)
                if record['node_data']['mongo_parent_id']:
                    receiver_parent = record['node_data']['mongo_parent_id']
                else:
                    receiver_parent = ''

                if record['node_data']['natural_parent_id']:
                    receiver_natural_parent = record['node_data']['natural_parent_id']
                else:
                    receiver_natural_parent = ''
        else:
            receiver_parent = ''
            receiver_natural_parent = ''

        receiver_attr = {}
        receiver_attr['identifier'] = self.receiver.identifier
        receiver_attr['description'] = self.receiver.description
        receiver_attr['type'] = str(self.receiver.type)
        receiver_attr['mongo_parent_id'] = receiver_parent
        receiver_attr['natural_parent_id'] = receiver_natural_parent
        nodes = db.nodes
        receiver_node = nodes.insert_one({
            'node_data': receiver_attr
        })

        parent_id = receiver_node.inserted_id

        sender_attr = {}
        sender_attr['identifier'] = self.sender.identifier
        sender_attr['description'] = self.sender.description
        sender_attr['type'] = str(self.sender.type)
        sender_attr['mongo_parent_id'] = parent_id
        sender_attr['natural_parent_id'] = self.receiver.identifier
        nodes = db.nodes
        sender_node = nodes.insert_one({
            'node_data': sender_attr
        })


        #get the parent of the parent
        #network_node = DBNode.query.filter_by(identifier=self.network.identifier).first()
        #print(network_node) #where self.network_name = WHERE
        #db.session.add(network_node)
        #db.session.flush()
        '''
        Check if sender is top level node::if receiver is in the db


        receiver_node = DBNode.query.filter_by(identifier=self.receiver.identifier).first()
        if receiver_node is None:
            receiver_id = 0
        else:
            receiver_id = receiver_node.id

        node_sender = DBNode(identifier=str(self.sender.identifier),description=str(self.sender.description),date_created=datetime.now(), parent_id=receiver_node.id)
        db.session.add(node_sender)
        db.session.flush()
        node_receiver = DBNode(identifier=str(self.receiver.identifier),description=str(self.receiver.description),date_created=datetime.now(), parent_id=node_sender.id)
        db.session.add(node_receiver)
        db.session.commit()
        '''
