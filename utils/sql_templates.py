REACTIONS = """SELECT 
reactions.publication_id,reactions.action_at 
FROM 
`lens-public-data.mumbai.public_publication_reaction_records` as reactions
WHERE
reactions.actioned_by_profile_id = "XXXIDXXX"
AND
reactions.action_at > "XXXTIMESTAMPXXX"
"""

COMMENT ="""SELECT
post.profile_id, comment.block_timestamp
FROM 
`lens-public-data.mumbai.public_post_comment` as comment, `lens-public-data.mumbai.public_profile_post` as post
WHERE
comment.post_id = post.post_id
AND
comment.comment_by_profile_id = "XXXIDXXX"
AND
comment.block_timestamp > "XXXTIMESTAMPXXX"
"""

MIRRORS_POSTS = """SELECT 
post.profile_id,post.post_id

FROM
`lens-public-data.mumbai.public_profile_post` as post
where 
post.post_id IN XXXIDXXX
"""
MIRRORS_POSTS_SUB = """SELECT 
post.is_related_to_post, block_timestamp
FROM 
`lens-public-data.mumbai.public_profile_post` as post
WHERE 
(
  post.is_related_to_post IS NOT NULL
)
AND 
post.profile_id = "XXXIDXXX"
AND
block_timestamp > "XXXTIMESTAMPXXX"
"""
MIRRORS_COMMENT = """SELECT 
comment.comment_by_profile_id, comment.comment_id

FROM
`lens-public-data.mumbai.public_post_comment` as comment
where 
comment.comment_id IN XXXIDXXX
"""
MIRRORS_COMMENT_SUB =  """SELECT 
post.is_related_to_comment, post.block_timestamp
FROM 
`lens-public-data.mumbai.public_profile_post` as post
WHERE 
(
  post.is_related_to_comment IS NOT NULL
)
AND 
post.profile_id = "XXXIDXXX"
AND
post.block_timestamp > "XXXTIMESTAMPXXX"
"""

COLLECTIONS = """SELECT 
publication_id, block_timestamp
FROM 
`lens-public-data.mumbai.public_publication_collect_module_collected_records`

WHERE 
collected_by = "XXXADDRXXX"
AND
block_timestamp > "XXXTIMESTAMPXXX"
"""

FOLLOWERS = """SELECT 
follow_profile_id
FROM 
`lens-public-data.mumbai.public_follower`

WHERE 
address = "XXXADDRXXX"
"""  
ADDRESS = """SELECT owned_by
FROM 
`lens-public-data.mumbai.public_profile`

WHERE 
profile_id = "XXXIDXXX"
"""

PROFILE = """SELECT 
profile_id
FROM 
`lens-public-data.mumbai.public_profile`
WHERE 
owned_by = "XXXADDRXXX"
"""

PROFILE_INFOS = """SELECT 
profile_picture_s3_url, handle, name, profile_id
FROM 
`lens-public-data.mumbai.public_profile`
WHERE 
profile_id IN XXXIDXXX
"""

NFT_ADDR = """SELECT 
follow_nft_address, profile_id
FROM
`lens-public-data.mumbai.public_profile_follow_nft`
where profile_id IN XXXIDXXX
"""