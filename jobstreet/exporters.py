from scrapy.conf import settings
from scrapy.contrib.exporter import CsvItemExporter


class FixCsvItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        newline = settings.get('CSV_NEWLINE', '')
        kwargs['newline'] = newline
        super(FixCsvItemExporter, self).__init__(*args, **kwargs)