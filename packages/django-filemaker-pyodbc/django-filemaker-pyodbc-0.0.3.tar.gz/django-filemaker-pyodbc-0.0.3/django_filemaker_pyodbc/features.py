from django.db.backends.base.features import BaseDatabaseFeatures

class FilemakerDatabaseFeatures(BaseDatabaseFeatures):
    supports_transactions = True
