import gspread
import datetime

class googlesheetsapi:
    
    def add_data(username, link):
        ss = gspread.service_account('gspreadkey/spotibottybot-f0d1e357e6da.json')
        sh = ss.open('SpotiBottyBot')
        wks = sh.worksheet('Sheet1')

        today = datetime.date.today()
        date = today.strftime("%B %d, %Y")
        str_list = list(filter(None, wks.col_values(1)))
        next_row = str(len(str_list)+1)
        wks.update(f'A{next_row}', username)
        wks.update(f'B{next_row}', date)
        wks.update(f'C{next_row}', link)