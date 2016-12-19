
class Error(Exception): pass

class DiskError(Error): pass
class StateError(Error): pass
class TableError(Error): pass

class NoVaultFileError(DiskError): pass
class BadVaultFilePermissionsError(DiskError): pass
class VaultFileAlreadyExistsError(DiskError): pass

class NoTableLoadedError(StateError): pass
class TableAlreadyLoadedError(StateError): pass

class RequiresEmptyTableError(TableError): pass
class RequiresLockedTableError(TableError): pass
class RequiresUnlockedTableError(TableError): pass
class RequiresTableWithPasswordError(TableError): pass
