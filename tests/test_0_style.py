import unittest
import os
import pep8

PACKAGES = ['scrappers', 'server']


class TestCodingStyle(unittest.TestCase):
    def test_pep8_conformance(self):
        """Test that we conform to PEP8."""
        project_dir = os.path.abspath(os.curdir)
        pep8style = pep8.StyleGuide(config_file=os.path.join(project_dir, '.pep8'))
        files_to_check = [os.path.join(project_dir, f) for f in os.listdir(project_dir) if f.endswith('.py')]
        for part in [os.path.join(project_dir, part) for part in PACKAGES]:
            for root, dirs, files in os.walk(part):
                files_to_check.extend([os.path.join(root, file) for file in files if file.endswith('.py')])
        result = pep8style.check_files(files_to_check)
        self.assertEqual(result.total_errors, 0, "Found code style errors (and warnings)")
