from google.cloud import bigquery
import os 
import sql_templates as t


class BigQueryHandler:
    ID_PLACEHOLDER = "XXXIDXXX"
    ADDR_PLACEHOLDER = "XXXADDRXXX"
    TIMESTAMP_PLACEHODLER = "XXXTIMESTAMPXXX"#"2023-03-05" y, m, d

    TEMPLATES = {
        "mirrors":t.MIRRORS,
        "reactions": t.REACTIONS,
        "comments": t.COMMENT,
        "collection":t.COLLECTIONS
    }
    
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]  =r"C:\Users\Demo\git\eth_global\backend\bigquery\minimalens-f0f35b81ae0f.json"
        self.client = bigquery.Client()

    def query(self):
        return self.client.query(query)  # Make an API request.
    
    def get_addr(self, profile_id):
        pass

    def get_followers(self):
        pass

    def get_collections(self, addr, timestamp):
        self.get_query_with_address("collections", addr, timestamp)

    def get_comments(self, profile_id, timestamp):
        self.get_query_with_profile_id("comments",profile_id, timestamp )

    def get_reactions(self, profile_id, timestamp):
        self.get_query_with_profile_id("reactions",profile_id, timestamp )

    def get_mirrors(self, profile_id, timestamp):
        self.get_query_with_profile_id("mirrors",profile_id, timestamp )

    def get_query_with_profile_id(self, template_type, profile_id, timestamp):
        if template_type not in self.TEMPLATES:
            raise ValueError(f"wrong template type handed over: {template_type}")
        
        template = self.TEMPLATES[template_type]

        curr_query = template
        curr_query = curr_query.replace(self.ID_PLACEHOLDER, profile_id)
        curr_query = curr_query.replace(self.TIMESTAMP_PLACEHODLER, timestamp)

        result = self.query(curr_query)

    def get_query_with_address(self, template_type, address, timestamp):
        if template_type not in self.TEMPLATES:
            raise ValueError(f"wrong template type handed over: {template_type}")
        
        template = self.TEMPLATES[template_type]

        curr_query = template
        curr_query = curr_query.replace(self.ADDR_PLACEHOLDER, address)
        curr_query = curr_query.replace(self.TIMESTAMP_PLACEHODLER, timestamp)

        result = self.query(curr_query)
    
    def logik(self):
         #user identifiziert sich
         #dadurch kriegen wir profile_id und timestamp
         # dann fetchen wir die  4 SQL Tables
         # dann aggregieren pro following profile
         # filterst du die aggregation nach threshhold
         # die werden in ui angezeigt
         # falls gewünscht: api call von diesen followern: unfollow
         pass

# Construct a BigQuery client object.


query = """
    SELECT owned_by
    FROM 
    `lens-public-data.mumbai.public_profile`

    WHERE 
    profile_id = "0x15" 
    
"""


print("The query data:")
for row in query_job:
    # Row values can be accessed by field name or index.
    print(row)