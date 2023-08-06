import unittest

from fetchai.ledger.crypto import Entity
from fetchai.ledger.crypto.genesis import GenesisFile

class EntityTests(unittest.TestCase):
    def test_json_generation(self):
        # Wealth division
        DESIRED_ENTITIES        = 30
        DESIRED_MINERS          = 20
        TOTAL_TOKEN_SUPPLY      = 1000000
        TOKENS_PER_ENTITY       = TOTAL_TOKEN_SUPPLY/DESIRED_ENTITIES
        TOKENS_STAKED_PER_MINER = TOKENS_PER_ENTITY/2

        # System parameters
        MAX_CABINET_SIZE   = 30
        BLOCK_INTERVAL_MS  = 1000
        START_IN_X_SECONDS = 5

        initial_entities = [(Entity(), TOKENS_PER_ENTITY, TOKENS_STAKED_PER_MINER if x < DESIRED_MINERS else 0) for x in range(DESIRED_ENTITIES)]

        genesis_file = GenesisFile(initial_entities, MAX_CABINET_SIZE, START_IN_X_SECONDS, BLOCK_INTERVAL_MS)

        # Check that the structure is correct

        genesis_file.dump_to_file("genesis_file.json")
