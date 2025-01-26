# examples/basic_agent.py
from gracie import Agent, Topic, KnowledgeConfig

def create_basic_agent():
    """Create a simple agent example"""
    # Initialize agent
    config = KnowledgeConfig(
        enable_faiss=True,
        max_contexts=5
    )
    
    agent = Agent(
        name="BasicAgent",
        knowledge_config=config
    )
    
    # Add basic knowledge
    agent.add_knowledge([
        Topic(
            name="greetings",
            definition="Basic greeting responses",
            facts=[
                "Always be polite",
                "Use appropriate time-based greetings",
                "Remember user names when possible"
            ]
        )
    ])
    
    return agent

# examples/crypto_bot.py
from gracie import Agent, Topic, KnowledgeConfig

def create_crypto_agent():
    """Create a cryptocurrency focused agent"""
    config = KnowledgeConfig(
        enable_faiss=True,
        max_contexts=10
    )
    
    agent = Agent(
        name="CryptoBot",
        knowledge_config=config,
        personality_traits=[
            {"name": "analytical", "strength": 0.8},
            {"name": "cautious", "strength": 0.7}
        ]
    )
    
    # Add crypto knowledge
    agent.add_knowledge([
        Topic(
            name="crypto_basics",
            definition="Basic cryptocurrency concepts",
            facts=[
                "Cryptocurrencies are digital assets",
                "Bitcoin was the first cryptocurrency",
                "Blockchain ensures transparency"
            ]
        ),
        Topic(
            name="trading_basics",
            definition="Basic trading concepts",
            facts=[
                "Never invest more than you can afford to lose",
                "Diversification reduces risk",
                "DYOR - Do Your Own Research"
            ]
        )
    ])
    
    return agent

# examples/custom_knowledge.py
from gracie import Agent, Topic, KnowledgeConfig
import json

def create_custom_agent(knowledge_file: str):
    """Create an agent with custom knowledge"""
    # Load custom knowledge
    with open(knowledge_file, 'r') as f:
        custom_knowledge = json.load(f)
    
    # Initialize agent
    agent = Agent(
        name="CustomAgent",
        knowledge_config=KnowledgeConfig(
            enable_faiss=True,
            max_contexts=15
        )
    )
    
    # Convert and add knowledge
    topics = [
        Topic(
            name=k["name"],
            definition=k["definition"],
            facts=k["facts"]
        )
        for k in custom_knowledge
    ]
    
    agent.add_knowledge(topics)
    return agent

if __name__ == "__main__":
    # Basic agent example
    basic_agent = create_basic_agent()
    print(basic_agent.process_input("Hello!"))
    
    # Crypto agent example
    crypto_agent = create_crypto_agent()
    print(crypto_agent.process_input("What is Bitcoin?"))
    
    # Custom agent example
    custom_agent = create_custom_agent("custom_knowledge.json")
    print(custom_agent.process_input("Tell me what you know"))
