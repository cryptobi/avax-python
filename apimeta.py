# ava-python : A Python implementation of the AVA API
# Author: https://github.com/zefonseca/
# License MIT

api_meta = {
    "metrics": { 
        "endpoint": "{}/ext/metrics",  # metrics endpoint
    },
    "avm": { 
        "endpoint": "{}/ext/bc/X",  # x-chain endpoint
    },
    "timestamp": { 
        "endpoint": "{}/ext/timestamp",  # timestamp endpoint
    }, 
    "platform": { 
        "endpoint": "{}/ext/bc/P",  # p-chain endpoint
    },    
    "keystore": { 
        "endpoint": "{}/ext/keystore",  # keystore endpoint
    },    
    "admin": { 
        "endpoint": "{}/ext/admin",  # admin endpoint
    },    
    "ipcs": { 
        "endpoint": "{}/ext/ipcs",  # ipcs endpoint
    },    
    "health": { 
        "endpoint": "{}/ext/health",  # health endpoint
    },    
    "evm": { 
        "endpoint": "{}/ext/bc/C/rpc",  # ethereum endpoint
    },    
    "ws": { 
        "endpoint": "{}/ext/bc/C/ws",  # websocket ethereum endpoint
    },    
    "info": { 
        "endpoint": "{}/ext/info",  # info API endpoint
    }
}