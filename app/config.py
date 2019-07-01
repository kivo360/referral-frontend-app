from decouple import config


DB_URL = config("SQLDATABASE")
REDISHOST = config("REDISHOST")
REDISPORT = config("REDISPORT")
TESTDB = config("SQLTEMP")
MAILGUNPASS = config("MAILGUNPASSWORD")
MAILGUNAPI = config("MAILGUNAPI")
STRIPEKEY = config("STRIPEKEY")
REWARDS = {
    'first': [
        {
            "name": "Tier 1 - Starter",
            "number": 10,
            "description": "You'll be able to get the 1st week free",
            "benefits": [
                'benefit1',
                'benefit2',
                'benefit3',
                'benefit4'
            ] 
        },
        {
            "name": "Tier 1 - Middle",
            "number": 25,
            "description": "You'll be able to get the 2 weeks free. Very good",
            "benefits": [
                'benefit1',
                'benefit2',
                'benefit3',
                'benefit4'
            ]
        },
        {
            "name": "Tier 1 - Pro",
            "number": 100,
            "description": "For this you'll be able to get the first month free.",
            "benefits": [
                'benefit1',
                'benefit2',
                'benefit3',
                'benefit4'
            ]
        }
    ],
    'second': [
        {
            "name": "Tier 2 - Starter",
            "number": 40,
            "description": "Get your first month free! (5%) life long discount if you hit Tier-1 Pro.",
            "benefits": [
                'benefit1',
                'benefit2',
                'benefit3',
                'benefit4'
            ] 
        },
        {
            "name": "Tier 2 - Middle",
            "number": 150,
            "description": "Get your first 2 months free! (5%) life long discount included.",
            "benefits": [
                'benefit1',
                'benefit2',
                'benefit3',
                'benefit4'
            ] 
        },
        {
            "name": "Tier 2 - Pro",
            "number": 300,
            "description": "Get your first 3 months free! (5%) life long discount and 20 FNG tokens included upon launch.",
            "benefits": [
                'benefit1',
                'benefit2',
                'benefit3',
                'benefit4'
            ] 
        }
    ],
    'third': [
        {
            "name": "Tier 3 - Starter",
            "number": 120,
            "description": "Get your first 2 months free! (10%) life long discount included.",
            "benefits": [
                'benefit1',
                'benefit2',
                'benefit3',
                'benefit4'
            ] 
        },
        {
            "name": "Tier 3 - Middle",
            "number": 450,
            "description": "Get your first 6 months free! (15%) life long discount and 100 FNG tokens included upon launch.",
            "benefits": [
                'benefit1',
                'benefit2',
                'benefit3',
                'benefit4'
            ] 
        },
        {
            "name": "Tier 3 - Pro",
            "number": 900,
            "description": "Get your first year free! (20%) life long discount and 150 FNG tokens included upon launch.",
            "benefits": [
                'benefit1',
                'benefit2',
                'benefit3',
                'benefit4'
            ] 
        }
    ]
}