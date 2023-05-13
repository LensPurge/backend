wallet_ID_Yogi = "0x3A5bd1E37b099aE3386D13947b6a90d97675e5e3"

from utils.big_query_handler import BigQueryHandler

handler = BigQueryHandler()
timestamp = "2023-05-01 09:00:00"

resp = handler.run(wallet_ID_Yogi, timestamp)

print("hi")