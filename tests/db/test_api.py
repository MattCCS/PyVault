
import unittest

from pyvault.db import api
from pyvault.db import errors


TEST_CONFIG_NAME = "test_config.json"
TEST_KEY = b"test"
TEST_KEY_2 = b"test2"


class TestAPI_01_None(unittest.TestCase):

    def test_none_can_change_settings(self):
        self.assertIsNone(api.use_settings(TEST_CONFIG_NAME))

    def test_none_cant_load(self):
        with self.assertRaises(errors.NoVaultFileError):
            api.load_table()

    def test_none_cant_save(self):
        with self.assertRaises(errors.NoTableLoadedError):
            api.save_table(overwrite=True)

    def test_none_cant_close(self):
        with self.assertRaises(errors.NoTableLoadedError):
            api.close_table()

    def test_none_cant_reset_password(self):
        with self.assertRaises(errors.NoTableLoadedError):
            api.reset_password(TEST_KEY, TEST_KEY_2)

    def test_none_cant_check_password(self):
        with self.assertRaises(errors.NoTableLoadedError):
            api.check_password(TEST_KEY)

    def test_none_cant_decrypt(self):
        with self.assertRaises(errors.NoTableLoadedError):
            api.decrypt(TEST_KEY)

    def test_none_cant_encrypt(self):
        with self.assertRaises(errors.NoTableLoadedError):
            api.encrypt(TEST_KEY)

    def test_none_cant_add_encrypted_entry(self):
        with self.assertRaises(errors.NoTableLoadedError):
            api.add_encrypted_entry(TEST_KEY, None)

    def test_none_cant_add_derived_entry(self):
        with self.assertRaises(errors.NoTableLoadedError):
            api.add_derived_entry(TEST_KEY, None)

    def test_none_cant_show_entry(self):
        with self.assertRaises(errors.NoTableLoadedError):
            api.show_entry(TEST_KEY, None)

    def test_none_cant_list_entries(self):
        with self.assertRaises(errors.NoTableLoadedError):
            api.list_entries()

    def test_none_cant_edit_entry(self):
        with self.assertRaises(errors.NoTableLoadedError):
            api.edit_entry(TEST_KEY, None, None)

    def test_none_cant_delete_entry(self):
        with self.assertRaises(errors.NoTableLoadedError):
            api.delete_entry(TEST_KEY, None)


class TestAPI_02_NoneToDisk(unittest.TestCase):

    def setUp(self):
        api.use_settings(TEST_CONFIG_NAME)

    def test_none_can_create_and_delete(self):
        self.assertEqual(api.create_table(), {})
        self.assertIsNone(api.delete_table())
        with self.assertRaises(errors.NoVaultFileError):
            api.delete_table()


class TestAPI_03_Disk(unittest.TestCase):

    def setUp(self):
        api.use_settings(TEST_CONFIG_NAME)
        api.create_table()

    def tearDown(self):
        api.delete_table()

    def test_disk_can_change_settings(self):
        self.assertIsNone(api.use_settings(TEST_CONFIG_NAME))


class TestAPI_04_DiskToEmpty(unittest.TestCase):

    def setUp(self):
        api.use_settings(TEST_CONFIG_NAME)
        api.create_table()

    def tearDown(self):
        api.delete_table()

    def test_disk_can_load(self):
        self.assertIsNotNone(api.load_table())


class TestAPI_05_Empty(unittest.TestCase):

    def setUp(self):
        api.use_settings(TEST_CONFIG_NAME)
        api.create_table()
        api.load_table()

    def tearDown(self):
        api.delete_table()

    def test_empty_cant_change_settings(self):
        with self.assertRaises(errors.TableAlreadyLoadedError):
            api.use_settings(TEST_CONFIG_NAME)

    def test_empty_cant_create(self):
        with self.assertRaises(errors.VaultFileAlreadyExistsError):
            api.create_table()

    def test_empty_cant_load(self):
        with self.assertRaises(errors.TableAlreadyLoadedError):
            api.load_table()

    def test_empty_can_save(self):
        self.assertEqual(api.save_table(overwrite=True), {})

    def test_empty_can_close(self):
        self.assertIsNone(api.close_table())

    def test_empty_cant_reset_password(self):
        with self.assertRaises(errors.RequiresTableWithPasswordError):
            api.reset_password(TEST_KEY, TEST_KEY_2)

    def test_empty_cant_check_password(self):
        with self.assertRaises(errors.RequiresTableWithPasswordError):
            api.check_password(TEST_KEY)

    def test_empty_cant_decrypt(self):
        with self.assertRaises(errors.RequiresLockedTableError):
            api.decrypt(TEST_KEY)

    def test_empty_cant_encrypt(self):
        with self.assertRaises(errors.RequiresUnlockedTableError):
            api.encrypt(TEST_KEY)

    def test_empty_cant_add_encrypted_entry(self):
        with self.assertRaises(errors.RequiresUnlockedTableError):
            api.add_encrypted_entry(TEST_KEY, None)

    def test_empty_cant_add_derived_entry(self):
        with self.assertRaises(errors.RequiresUnlockedTableError):
            api.add_derived_entry(TEST_KEY, None)

    def test_empty_cant_show_entry(self):
        with self.assertRaises(errors.RequiresUnlockedTableError):
            api.show_entry(TEST_KEY, None)

    def test_empty_cant_list_entries(self):
        with self.assertRaises(errors.RequiresUnlockedTableError):
            api.list_entries()

    def test_empty_cant_edit_entry(self):
        with self.assertRaises(errors.RequiresUnlockedTableError):
            api.edit_entry(TEST_KEY, None, None)

    def test_empty_cant_delete_entry(self):
        with self.assertRaises(errors.RequiresUnlockedTableError):
            api.delete_entry(TEST_KEY, None)


class TestAPI_06_EmptyToLocked(unittest.TestCase):

    def setUp(self):
        api.use_settings(TEST_CONFIG_NAME)
        api.create_table()
        api.load_table()

    def tearDown(self):
        api.delete_table(TEST_KEY)

    def test_empty_set_password(self):
        self.assertIsNotNone(api.set_password(TEST_KEY))


class TestAPI_07_Locked(unittest.TestCase):

    def setUp(self):
        api.use_settings(TEST_CONFIG_NAME)
        api.create_table()
        api.load_table()
        api.set_password(TEST_KEY)

    def tearDown(self):
        api.delete_table(TEST_KEY)

    def test_locked_cant_change_settings(self):
        with self.assertRaises(errors.TableAlreadyLoadedError):
            api.use_settings(TEST_CONFIG_NAME)

    def test_locked_cant_create(self):
        with self.assertRaises(errors.VaultFileAlreadyExistsError):
            api.create_table()

    def test_locked_cant_load(self):
        with self.assertRaises(errors.TableAlreadyLoadedError):
            api.load_table()

    def test_locked_can_save(self):
        self.assertIsNotNone(api.save_table(overwrite=True))

    def test_locked_can_close(self):
        self.assertIsNone(api.close_table())

    def test_locked_can_check_password(self):
        self.assertIsNone(api.check_password(TEST_KEY))

    def test_locked_cant_encrypt(self):
        with self.assertRaises(errors.RequiresUnlockedTableError):
            api.encrypt(TEST_KEY)

    def test_locked_cant_add_encrypted_entry(self):
        with self.assertRaises(errors.RequiresUnlockedTableError):
            api.add_encrypted_entry(TEST_KEY, None)

    def test_locked_cant_add_derived_entry(self):
        with self.assertRaises(errors.RequiresUnlockedTableError):
            api.add_derived_entry(TEST_KEY, None)

    def test_locked_cant_show_entry(self):
        with self.assertRaises(errors.RequiresUnlockedTableError):
            api.show_entry(TEST_KEY, None)

    def test_locked_cant_list_entries(self):
        with self.assertRaises(errors.RequiresUnlockedTableError):
            api.list_entries()

    def test_locked_cant_edit_entry(self):
        with self.assertRaises(errors.RequiresUnlockedTableError):
            api.edit_entry(TEST_KEY, None, None)

    def test_locked_cant_delete_entry(self):
        with self.assertRaises(errors.RequiresUnlockedTableError):
            api.delete_entry(TEST_KEY, None)


class TestAPI_08_LockedToLocked(unittest.TestCase):

    def setUp(self):
        api.use_settings(TEST_CONFIG_NAME)
        api.create_table()
        api.load_table()
        api.set_password(TEST_KEY)

    def tearDown(self):
        api.delete_table(TEST_KEY_2)

    def test_locked_can_reset_password(self):
        self.assertIsNone(api.reset_password(TEST_KEY, TEST_KEY_2))
        self.assertIsNone(api.check_password(TEST_KEY_2))


class TestAPI_09_LockedToUnlocked(unittest.TestCase):

    def setUp(self):
        api.use_settings(TEST_CONFIG_NAME)
        api.create_table()
        api.load_table()
        api.set_password(TEST_KEY)

    def tearDown(self):
        api.delete_table(TEST_KEY)

    def test_locked_can_decrypt(self):
        self.assertIsNotNone(api.decrypt(TEST_KEY))


class TestAPI_10_Unlocked(unittest.TestCase):

    def setUp(self):
        api.use_settings(TEST_CONFIG_NAME)
        api.create_table()
        api.load_table()
        api.set_password(TEST_KEY)
        api.decrypt(TEST_KEY)

    def tearDown(self):
        api.delete_table(TEST_KEY)
