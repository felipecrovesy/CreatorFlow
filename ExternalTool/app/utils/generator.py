
import random
import uuid
from datetime import datetime
from faker import Faker
import names

fake = Faker('pt_BR')

CONTENT_TYPES = [
    'adult', 'sports', 'cooking', 'music', 'gaming', 'fitness', 'travel',
    'fashion', 'education', 'comedy', 'art', 'lifestyle', 'technology',
    'photography', 'beauty'
]

def generate_creator_name() -> str:
    adjectives = ['Sexy', 'Cool', 'Hot', 'Mystic', 'Crazy', 'Sweet', 'Cute', 'Epic',
                  'Funky', 'Charming', 'Wild', 'Glam', 'Vivid', 'Bold', 'Daring',
                  'Fierce', 'Gorgeous', 'Radiant', 'Sassy', 'Trendy']
    names_list = ['Luna', 'Leo', 'Dark', 'Bella', 'Gabi', 'Thor', 'Neko', 'Max', 'Roxy',
                  'Jade', 'Kira', 'Nova', 'Milo', 'Zoe', 'Finn', 'Sky', 'Ace', 'Rex',
                  'Jax', 'Mia', 'Koda', 'Sage', 'Raven', 'Echo', 'Blaze', 'Storm',
                  'Faye', 'Juno', 'Zara', 'Nina', 'Iza']
    numbers = str(random.randint(10, 9999))
    return random.choice(adjectives) + random.choice(names_list) + numbers

def create_user() -> dict:
    now = datetime.utcnow().isoformat() + "Z"
    return {
        "creatorName": generate_creator_name(),
        "realName": names.get_full_name(),
        "clientId": str(uuid.uuid4()),
        "totalFollowers": random.randint(100, 500000),
        "contentType": random.choice(CONTENT_TYPES),
        "revenue": round(random.uniform(100.0, 100000.0), 2),
        "email": fake.email(),
        "documentId": fake.cpf(),
        "isProcessed": False,
        "createdAt": now,
        "updatedAt": now
    }
