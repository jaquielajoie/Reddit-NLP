from Social_Scraper import q, db
from time import strftime, time
from Social_Scraper.Web_Server.Reddit.PostReader import PostReader
#from Social_Scraper.Web_Server.DBModels_Reddit import DBNode
from Social_Scraper.Web_Server.Network.Network import Network
from Social_Scraper.Web_Server.Network.Node import Node
from Social_Scraper.Web_Server.Network.Edge import Edge

class Tasker:
    def __init__(self, func_name, args):
        self.args = args
        self.response = self.add_task(func_name=func_name)

    def add_task(self, func_name):
        jobs = q.jobs
        func = getattr(self, f'task_{func_name}')
        task = q.enqueue(func, kwargs=self.args)

        q_len = len(q)
        message = f'Task {func_name} with {self.args} queued at {task.enqueued_at.strftime("%a %d %b %Y %H:%M")} || {q_len} tasks in the queue...'
        return message

    def task_postreader(self, subreddit_name, number_of_posts, comment_limit):
        sub_name = str(subreddit_name)
        pr = PostReader(sub_name=sub_name)
        count = int(number_of_posts)
        comment_limit = int(comment_limit)

        pr.set_topic_list(['trump', 'republican', 'republicans', 'biden', 'democrat', 'democrats'])
        #subreddit = DBSubreddit(subreddit_name=subreddit_name,number_of_posts=number_of_posts,comment_limit=comment_limit,create_date=datetime.now())
        #db.session.add(subreddit)
        #db.session.commit()
        ret_val = pr.collect_posts(count=count, comment_limit=comment_limit, threshold=0.8)
        return ret_val

    def task_draw_network_new(self, top_node):
        network_node = db.session.query(DBNode).filter(DBNode.identifier.in_((top_node,''))).first()
        print(network_node)
        subreddit_nodes = db.session.query(DBNode).filter(DBNode.parent_id.in_((network_node.id,''))).all()
        print(subreddit_nodes)

        for node in subreddit_nodes:
            post_nodes = db.session.query(DBNode).filter(DBNode.parent_id.in_((node.id,''))).all()
            print(node.description)

            for post in post_nodes:
                print('hello')
                print(post.description)

    def task_draw_network(self, top_node):
        nodes = DBNode.query.all()
        nodes.reverse()
        #stmt = ['top_node', 'next']
        #seen_nodes = []
        seen_parents = []
        seen_idens = []

        id_identifiers = [('id','identifier')]
        ns = []

        network = Network(name=top_node)
        for node in nodes:
            #if node.id not in seen_nodes: seen_nodes.append(node.id)
            if node.identifier not in seen_idens:
                seen_idens.append(node.identifier)
                n = Node(identifier=node.identifier,description=node.description,type=type(node), db_id=node.id ,parent_id=node.parent_id)
                ns.append(n)
                if node.parent_id not in seen_parents: seen_parents.append(node.parent_id)
            id_identifiers.append((node.id,node.identifier))





        #ns.reverse() #1 to 1 creation with id_identifiers
        #id_identifiers.reverse() #get the most recent entries in the database for each identifier :)

        #current_iden = ''
        unique_idens = []
        id_identifiers.pop(0) #get rid of first value

        while id_identifiers:
            print(unique_idens)
            child_id, child_iden = id_identifiers.pop(0)

            '''
            Get only unique node id's - could be problematic for cross sites
            '''
            if child_iden not in unique_idens:
                unique_idens.append(child_iden)
            else:
                continue

        for child_n in ns:
            for iden in unique_idens:
                if child_n.identifier == iden:
                    print(child_n.identifier)
                    for parent_id in seen_parents:
                        if child_n.parent_id == parent_id:
                            for parent_n in ns:
                                if parent_n.db_id == parent_id:
                                    print('get teh parent node object')
                                    edge = Edge(sender=parent_n,receiver=child_n,weight=1,type=type(Edge), save_to_db=True)
                                    network.add_edge(edge)
                                    network.show_graph()






                #n = ns[i]
                #if n.identifier == iden:
                    #print(n)



        #
            #print(node.identifier)
            #sleep(1)
        #return nodes
