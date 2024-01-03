CONNECTORS = {}

LOG = {
    "loggers": {"cloudforet": {"level": "DEBUG", "handlers": ["console"]}},
    "filters": {
        "masking": {"rules": {"ExternalAuth.authorize": ["secret_data", "credentials"]}}
    },
}

HANDLERS = {}

ENDPOINTS = {}
