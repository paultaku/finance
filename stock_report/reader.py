# from google_client.sheets import google_sheets
# from google_client.drive import google_drive
from pprint import pprint
from stock_report.abstract import abstract_report

class reader(abstract_report):

    def __init__(self, stock_number):
        self.stock_number = stock_number
        abstract = super(abstract_report, self)
    #     self.target_folder = 'Taiwan Index Stock'
    #
    #     scope = [
    #         'https://www.googleapis.com/auth/spreadsheets',
    #         'https://www.googleapis.com/auth/drive'
    #     ]
    #     # google sheet client
    #     self.sheet_client = google_sheets(scope, path='./client_secret.json')
    #     # google drive client
    #     self.drive_client = google_drive(scope, path='./client_secret.json')

    # def _get_target_sheet(self):
    #     return self.drive_client.find_target_sheet(self.stock_number)
    #
    # def _get_target_folder(self):
    #     return super(abstract_report, self)._get_target_folder()


    def execute(self, *args, **kwargs):
        tab_title = 'Daily'
        folder = self._get_target_folder()
        sheet = self._get_target_sheet()
        pprint(sheet)
        if sheet is None:
            sheet = self.drive_client.add_new_sheet(name=self.stock_number, parent=folder)

        # get target via google sheet API
        target = self.sheet_client.get(spreadsheetId=sheet['id'])
        sheet_prop = self.sheet_client.find_sheet_by_name(spreadsheet_properties=target, sheet_name=tab_title)

        if len(sheet_prop) == 0:
            sheet_prop = self.sheet_client.addSheet(spreadsheetId=sheet['id'], body={
                'properties': {
                    'index': 0,
                    'title': tab_title,
                    'gridProperties': {
                        'rowCount': len(kwargs['data']),
                        'columnCount': 9
                    }
                },
            })

        sheet_data = self.sheet_client.read(
            spreadsheetId=sheet['id'],
            ranges=self.get_grids_rangs(
                columnCount=sheet_prop[0]['properties']['gridProperties']['columnCount'],
                rowCount=sheet_prop[0]['properties']['gridProperties']['rowCount']
            ),
            valueRenderOption='UNFORMATTED_VALUE',
            dateTimeRenderOption='FORMATTED_STRING'
        )
        existing_data = self.get_daily_data(data=sheet_data)
        return list(map(lambda row: row[0], existing_data)) if existing_data is not None else []
