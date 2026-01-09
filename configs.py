# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01


from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", "27686895"))
    API_HASH = getenv("API_HASH", "0e996bd3891969ec5dfebf8bb3e39e94")
    BOT_TOKEN = getenv("BOT_TOKEN", "8358355530:AAGX5QEJb18nlL-ChozYdYb7OMFpyXj8GDA")
    # Your Force Subscribe Channel Id Below 
    CHID = int(getenv("CHID", "-1003375459241")) # Make Bot Admin In This Channel
    # Admin Or Owner Id Below
    SUDO = list(map(int, getenv("SUDO", "1246987713").split()))
    MONGO_URI = getenv("MONGO_URI", "mongodb+srv://anihubyt:xG92SHTUX4Cd7BcA@cluster0.qv5tu12.mongodb.net/?appName=Cluster0")
    
cfg = Config()

# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01
