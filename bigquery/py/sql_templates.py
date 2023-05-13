REACTIONS = """SELECT 
* 
FROM 
`lens-public-data.mumbai.public_publication_reaction_records`
WHERE 
actioned_by_profile_id = "XXXIDXXX"
AND
action_at > "XXXTIMESTAMPXXX"
"""

COMMENT = """SELECT
* 
FROM 
`lens-public-data.mumbai.public_post_comment`
WHERE 
comment_by_profile_id = "XXXIDXXX"
AND
block_timestamp > "XXXTIMESTAMPXXX"
"""

MIRRORS = """SELECT 
*
FROM 
`lens-public-data.mumbai.public_profile_post`
WHERE 
(
  is_related_to_comment IS NOT NULL  
  OR 
  is_related_to_post IS NOT NULL
)
AND 
profile_id = "XXXIDXXX"
AND
block_timestamp > "XXXTIMESTAMPXXX"
"""

COLLECTIONS = """
SELECT 
* 
FROM 
`lens-public-data.mumbai.public_publication_collect_module_collected_records`

WHERE 
collected_by = "XXXADDRXXX"
AND
block_timestamp > "XXXTIMESTAMPXXX"
"""
