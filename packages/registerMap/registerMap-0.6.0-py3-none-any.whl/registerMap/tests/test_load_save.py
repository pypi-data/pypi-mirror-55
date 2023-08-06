#
# Copyright 2019 Russell Smiley
#
# This file is part of registerMap.
#
# registerMap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# registerMap is distributed in the hope that it will be useful
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with registerMap.  If not, see <http://www.gnu.org/licenses/>.
#

import unittest.mock

# import the top-level module to test that load, save are importable at this level
import registerMap


class TestLoad(unittest.TestCase):
    def test_load(self):
        mock_filename = 'some/file'
        with unittest.mock.patch('registerMap.registerMap.load_yaml_data') as mock_yaml_load, \
                unittest.mock.patch('registerMap.registerMap.RegisterMap.from_yamlData') as \
                        mock_from:
            loaded_map = registerMap.load(mock_filename)

            registermap_instance = mock_from.return_value

            self.assertEqual(loaded_map, registermap_instance)
            mock_from.assert_called_once()

            mock_yaml_load.assert_called_once_with(mock_filename)


class TestSave(unittest.TestCase):
    def test_save(self):
        mock_filename = 'some/file'
        with unittest.mock.patch('registerMap.registerMap.save_yaml_data') as mock_yaml_save:
            mock_map = unittest.mock.create_autospec(registerMap.RegisterMap)

            registerMap.save(mock_filename, mock_map)

            mock_map.to_yamlData.assert_called_once()
            mock_yaml_save.assert_called_once_with(mock_filename, mock_map.to_yamlData.return_value)


if __name__ == '__main__':
    unittest.main()
