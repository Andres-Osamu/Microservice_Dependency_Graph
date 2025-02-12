# Import functions from the cleaner module
# - removeFluff: Filters out non-data-containing events (e.g., non-response events).
from .cleaner import removeFluff

# Import functions from the sql_matcher module
# - matchResponseSQL: Matches response events with SQL events.
from .sql_matcher import matchResponseSQL

# Import functions from the pubsub_matcher module
# - matchPubSub: Matches published events (RabbitMQ) with response events.
from .pubsub_matcher import matchPubSub

# Import functions from the cross_matcher module
# - domainKnowledgeEventAnalysis: Cross-references events and resolves potential matches.
from .cross_matcher import domainKnowledgeEventAnalysis

# Define the public API of the module
# This list specifies which functions are exposed when using `from event_correlation import *`
# - removeFluff: Function to clean and filter events.
# - matchResponseSQL: Function to match response events with SQL events.
# - matchPubSub: Function to match published events with response events.
# - domainKnowledgeEventAnalysis: Function to analyze and resolve event matches using domain knowledge.
__all__ = [
    "removeFluff",
    "matchResponseSQL",
    "matchPubSub",
    "domainKnowledgeEventAnalysis",
]