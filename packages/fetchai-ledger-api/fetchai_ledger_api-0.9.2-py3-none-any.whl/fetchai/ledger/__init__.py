# Ledger version that this API is compatible with
__version__ = '0.9.2'
# This API is compatible with ledgers that meet all the requirements listed here:
__compatible__ = ['<0.11.0', '>=0.8.0-alpha']


class IncompatibleLedgerVersion(Exception):
    pass
