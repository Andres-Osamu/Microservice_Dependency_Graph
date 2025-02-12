# Import functions from the extractor module
# - extractDomainKnowledge: Extracts domain knowledge from event models.
from .extractor import extractDomainKnowledge

# Import functions from the filter module
# - filterDkUnique: Filters domain knowledge to ensure unique attributes.
# - filterDkCorpus: Filters domain knowledge to create a synonym dictionary.
from .filter import filterDkUnique, filterDkCorpus

# Import functions from the analyzer module
# - combineDKs: Combines domain knowledge from multiple sources.
# - removeDkConflicts: Resolves attribute naming conflicts in domain knowledge.
from .analyzer import combineDKs, removeDkConflicts

# Define the public API of the module
# This list specifies which functions are exposed when using `from knowledge_processing import *`
# - extractDomainKnowledge: Function to extract domain knowledge.
# - filterDkUnique: Function to filter domain knowledge for unique attributes.
# - filterDkCorpus: Function to filter domain knowledge for synonyms.
# - combineDKs: Function to combine domain knowledge from multiple sources.
# - removeDkConflicts: Function to resolve attribute naming conflicts.
__all__ = [
    "extractDomainKnowledge",
    "filterDkUnique",
    "filterDkCorpus",
    "combineDKs",
    "removeDkConflicts",
]