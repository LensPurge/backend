from google.cloud import bigquery
from google.api_core.exceptions import BadRequest
import os 
from . import sql_templates as t
import threading
import time
from .lens_cacher import LensCacher

class BigQueryHandler:
    ID_PLACEHOLDER = "XXXIDXXX"
    ADDR_PLACEHOLDER = "XXXADDRXXX"
    TIMESTAMP_PLACEHODLER = "XXXTIMESTAMPXXX"#"2023-03-05" y, m, d    
    
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]  =r"C:\Users\Demo\git\eth_global\backend\bigquery\minimalens-f0f35b81ae0f.json"
        #os.environ["GOOGLE_APPLICATION_CREDENTIALS"]  ="/home/pbbecker/backend/bigquery/py/minimalens-f0f35b81ae0f.json"
        time_ = time.time()
        self.client = bigquery.Client()
        print(time.time() -time_)
        self.cacher = LensCacher()

    def run(self, addr, timestamp):

        id =  self.get_profile_id(addr)
        #addr = self.get_addr(id) #done 
        if self.cacher.is_saved(id, timestamp):
            return self.cacher.get_saved(id,timestamp)

        self.following = self.get_followers(addr) # done: ids of the followers

        # collection_thread = threading.Thread(target= self.get_collections, args  =(addr,timestamp))
        # collection_thread.start()
        #collections = self.get_collections(addr, timestamp)#done: ids of profiles of collections you got
        self.get_collections(addr, timestamp)#done: ids of profiles of collections you got

        # comment_thread = threading.Thread(target= self.get_comments, args  =(id, timestamp))
        # comment_thread.start()
        #comments = self.get_comments(id, timestamp) #done: ids of profiles you commented on
        self.get_comments(id, timestamp) #done: ids of profiles you commented on

        # reactions_thread = threading.Thread(target= self.get_reactions, args  =(id, timestamp))
        # reactions_thread.start()
        #reactions = self.get_reactions(id, timestamp) # done: ids of profiles you reacted on
        self.get_reactions(id, timestamp) # done: ids of profiles you reacted on

        # mirrors_comments_thread = threading.Thread(target= self.get_mirrors_comments, args  =(id, timestamp))
        # mirrors_comments_thread.start()
        #mirrors_comments = self.get_mirrors_comments(id, timestamp)#done: profiles where you mirrored a comment
        self.get_mirrors_comments(id, timestamp)#done: profiles where you mirrored a comment
        
        # mirrors_posts_thread = threading.Thread(target= self.get_mirrors_posts, args  =(id, timestamp))
        # mirrors_posts_thread.start()
        #mirrors_posts = self.get_mirrors_posts(id,timestamp)#done: profiles where you mirrored a post
        self.get_mirrors_posts(id,timestamp)#done: profiles where you mirrored a post

      
        # collection_thread.join()
        # comment_thread.join()
        # reactions_thread.join()
        # mirrors_comments_thread.join()
        # mirrors_posts_thread.join()


        mapping_factor = [
            (self.collections,"collections", 1),
            (self.comments, "comments",1),
            (self.reactions, "reactions",1),
            (self.mirrors_comments, "mirrors_comments",1),
            (self.mirrors_posts, "mirrors_posts",1),
        ]

        scores = self.calculate_scores(mapping_factor)

        #now we have scores of the ones we interacted with. 
        #Now add the ones, which we didn not interacted with.
        following_but_no_interaction = list(set(self.following) - set(scores.keys()))
        profile_infos =  self.get_profile_infos(following_but_no_interaction)


        self.cacher.add_log(profile_infos, id, timestamp)
        return profile_infos


    def calculate_scores(self,mapping_factor):
        scores = {}
        for ids, type,factor in mapping_factor:
            for id_tuple in ids:
                id = id_tuple[0]
                id_timestamp = id_tuple[1]
                if id in self.following: #only people which we follow
                    
                    if id in scores: 
                        if type in scores[id]:
                            scores[id][type]["score"] +=1
                            if scores[id][type]["last_interaction"] < id_timestamp:
                                scores[id][type]["last_interaction"] = id_timestamp
                        else:
                            scores[id] = {
                            type:{
                                "score":1,
                                "last_interaction": id_timestamp
                            }
                        }
                    else:
                        scores[id] = {
                            type:{
                                "score":1,
                                "last_interaction": id_timestamp
                            }
                        }

        return scores
        

    def query(self, query):
        #client = bigquery.Client()
        return self.client.query(query)  # Make an API request.
    
    def get_addr(self, profile_id):
        result =  self.get_query_with_profile_id("address",profile_id )
        for row in result: return row["owned_by"]

    def get_profile_id(self, addr):
        result =  self.get_query_with_address("profile", addr)
        for row in result: return row["profile_id"]

    def get_profile_infos(self, ids):
        try:
            ids_copy = ids.copy()
            template = t.PROFILE_INFOS
            if len(ids) == 1:
                ids = "('" + str(ids[0]) +"')"
            else:
                ids = str(tuple(ids))
            template = template.replace(self.ID_PLACEHOLDER, ids)
            result = self.query(template)

            nft_adresses = self.get_nft_addr(ids_copy)

            infos = {
                row["profile_id"]:{
                    "img_link" : self.format_profile_link(row["profile_picture_s3_url"]),
                    "handle": row["handle"],
                    "name": row["name"],
                    "nft_addr": nft_adresses[row["profile_id"]]
                    } 
                for row in result
            }
            return infos
        except BadRequest as e:
            return {}
    
    def format_profile_link(self, url):
        if url is None:
            return None
        if url.startswith("ipfs://"):
            url = url.replace("ipfs://", "https://ipfs.io/ipfs/")
        if url.startswith("https://ipfs.infura.io/ipfs/"):
            url = url.replace("https://ipfs.infura.io/ipfs/", "https://ipfs.io/ipfs/")
        return url

    def get_followers(self,addr):
        try:
            result =  self.get_query_with_address("followers", addr)
            ids_following = [row["follow_profile_id"] for row in result]
            return ids_following
        except BadRequest as e:
            return []
        

    def get_collections(self, addr, timestamp):
        try:
            result =  self.get_query_with_address("collections", addr, timestamp)
            pub_ids_of_collections = [(row["publication_id"], row["block_timestamp"]) for row in result]
            #profile id is the first part of publication id
            profile_ids_of_collection = [(x.split("-")[0], y) for x, y in pub_ids_of_collections]
            self.collections =  profile_ids_of_collection
        except BadRequest as e:
            self.collections = []

    def get_comments(self, profile_id, timestamp):
        try:
            result =  self.get_query_with_profile_id("comments",profile_id, timestamp )
            profile_ids_you_commented_on = [(row["profile_id"], row["block_timestamp"]) for row in result]
            self.comments =  profile_ids_you_commented_on
        except BadRequest as e:
            self.comments = []

    def get_reactions(self, profile_id, timestamp):
        try:
            result =  self.get_query_with_profile_id("reactions",profile_id, timestamp )
            publication_ids_you_reacted_on = [(row["publication_id"], row["action_at"]) for row in result]
            #profile id is the first part of publication id
            profile_ids_you_reacted_on = [(x.split("-")[0],y) for x,y in publication_ids_you_reacted_on]
            self.reactions =  profile_ids_you_reacted_on
        except BadRequest as e:
            self.reactions = []

    def get_mirrors_comments(self, profile_id, timestamp):
        try:
            result =  self.get_query_with_profile_id("mirrors_comments_sub",profile_id, timestamp )
            comment_ids = [row["is_related_to_comment"] for row in result]
            if comment_ids == []:
                self.mirrors_comments = []
                return
            if len(comment_ids )==1:
                comment_ids = "(" + str(comment_ids[0]) + ")"
            else:
                comment_ids = str(tuple(comment_ids))
            timestamps = [row["block_timestamp"] for row in result]

            comment_ids_and_timestamps = [(a,b) for a,b in zip(comment_ids, timestamps)]

            result =  self.get_query_with_profile_id("mirrors_comments",comment_ids, timestamp )
            profiles_which_comments_the_id_mirrored=[row["comment_by_profile_id"] for row in result]
            comment_ids_2 = [row["comment_id"] for row in result]
            if comment_ids_2 == []:
                self.mirrors_comments = []
                return 

            comment_ids_and_profile_ids = [(a,b) for a,b in zip(comment_ids_2, profiles_which_comments_the_id_mirrored)]

            profile_ids_and_timestamps = self.match_tuples(comment_ids_and_profile_ids, comment_ids_and_timestamps)

            self.mirrors_comments =  profile_ids_and_timestamps
        except Exception as e:
            self.mirrors_comments =[]
    
    def get_mirrors_posts(self, profile_id, timestamp):
        try:
            result =  self.get_query_with_profile_id("mirrors_posts_sub",profile_id, timestamp )
            post_ids = [row["is_related_to_post"] for row in result]
            if post_ids == []:
                self.mirrors_posts = []
                return 
            post_ids = str(tuple(post_ids))
            timestamps = [row["block_timestamp"] for row in result]

            post_ids_and_timestamps = [(a,b) for a,b in zip(post_ids, timestamps)]


            result =  self.get_query_with_profile_id("mirrors_posts",post_ids, timestamp )
            profiles_which_posts_the_id_mirrored=[row["profile_id"] for row in result]
            post_ids_2 = [row["post_id"] for row in result]
            if post_ids_2 ==[]:
                self.mirrors_posts = []
                return 

            post_ids_and_profile_ids = [(a,b) for a,b in zip(post_ids_2, profiles_which_posts_the_id_mirrored)]

            profile_ids_and_timestamps = self.match_tuples(post_ids_and_profile_ids, post_ids_and_timestamps)

            self.mirrors_posts =  profile_ids_and_timestamps
        except BadRequest as e:
            self.mirrors_posts = []
    
    def get_nft_addr(self, ids):
        try:
            if len(ids) == 1:
                ids = "('" + str(ids[0]) +"')"
            else:
                ids = str(tuple(ids))
            result =  self.get_query_with_profile_id("nft_addr", ids)
            profile_ids_and_nft_adrrs = {row["profile_id"]: row["follow_nft_address"] for row in result}
            return profile_ids_and_nft_adrrs
            
        except BadRequest as e:
            self.collections = []

    def match_tuples(self, t1, t2):
        #t1 = [('a1','b1')]
        #t2 = [('a1','c1')]
        #return [(b1,c1)]
        result = []
        t2_dict = {t[0]: t[1] for t in t2}
        for t in t1:
            if t[0] in t2_dict:
                result.append((t[1], t2_dict[t[0]]))
        return result


    def get_query_with_profile_id(self, template_type, profile_id, timestamp = None):
        
        templates = {
            "mirrors_comments":t.MIRRORS_COMMENT,
            "mirrors_comments_sub": t.MIRRORS_COMMENT_SUB,
            "mirrors_posts": t.MIRRORS_POSTS,
            "mirrors_posts_sub": t.MIRRORS_POSTS_SUB,
            "reactions": t.REACTIONS,
            "comments": t.COMMENT,
            "address": t.ADDRESS,
            "nft_addr": t.NFT_ADDR,
        }

        if template_type not in templates:
            raise ValueError(f"wrong template type handed over: {template_type}")
        
        print(f"Fetching {template_type}...", flush= True)
        
        template = templates[template_type]

        curr_query = template
        curr_query = curr_query.replace(self.ID_PLACEHOLDER, profile_id)
        if timestamp:
            curr_query = curr_query.replace(self.TIMESTAMP_PLACEHODLER, timestamp)

        result = self.query(curr_query)

        return result

    def get_query_with_address(self, template_type, address, timestamp = None):
        
        templates = {
            "collections":t.COLLECTIONS,
            "followers":t.FOLLOWERS,
            "profile": t.PROFILE
        }

        if template_type not in templates:
            raise ValueError(f"wrong template type handed over: {template_type}")
        
        print(f"Fetching {template_type}...", flush = True)
        
        template = templates[template_type]

        curr_query = template
        curr_query = curr_query.replace(self.ADDR_PLACEHOLDER, address)
        if timestamp:
            curr_query = curr_query.replace(self.TIMESTAMP_PLACEHODLER, timestamp)

        result = self.query(curr_query)

        return result
