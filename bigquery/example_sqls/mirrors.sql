SELECT 

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
profile_id = "0x15"