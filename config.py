BOOTSTRAP_SERVERS = 'localhost:9092'
TOPIC_NAME = 'website_health'
SITES_TO_MONITOR = ['https://www.emirrisyad.site/', 'https://www.shinjang.site/', 'https://live-collab-api.onrender.com/health',
                    'https://medrec-api.onrender.com/health', 'https://httpstat.us/404'] # Last one tests errors
SLEEP_TIME = 10