import unittest

from seaborn_table.table import main as cli_converter
from test.support import BaseTest, FormatMixin


class FileConversionMixin(FormatMixin):
    def validate_test_condition(self, source):
        dest = self.DEST
        source_file = self.test_data_path('test_file.%s' % source)
        expected_file = self.test_data_path('test_file.%s' % dest)
        result_file = self.test_data_path('_%s'%source, 'test_file.%s' % dest)
        cli_converter(source_file, result_file)
        self.assert_result_file(expected_file, result_file,
                                "Failure converting %s into %s"%(source, dest))
        self.remove_file(result_file)

    def test_html(self):
        raise unittest.SkipTest("reading html has not been implemented")


class FileConversionTestTxt(BaseTest, FileConversionMixin):
    DEST = 'txt'


class FileConversionTestCsv(BaseTest, FileConversionMixin):
    DEST = 'csv'


class FileConversionTestMd(BaseTest, FileConversionMixin):
    DEST = 'md'


class FileConversionTestHtml(BaseTest, FileConversionMixin):
    DEST = 'html'


class FileConversionTestGrid(BaseTest, FileConversionMixin):
    DEST = 'grid'


class FileConversionTestJson(BaseTest, FileConversionMixin):
    DEST = 'json'


class FileConversionTestRst(BaseTest, FileConversionMixin):
    DEST = 'rst'


class FileConversionTestPsql(BaseTest, FileConversionMixin):
    DEST = 'psql'


if __name__ == '__main__':
    unittest.main()
