import gspread
import datetime

class googlesheetsapi:
    
    def add_data(first_name, username, link):
        ss = gspread.service_account('gspreadkey/spotibottybot-356716-2207c2abbd40.json')
        sh = ss.open('SpotiBottyBot')
        wks = sh.worksheet('Sheet1')

        today = datetime.date.today()
        date = today.strftime("%B %d, %Y")
        str_list = list(filter(None, wks.col_values(1)))
        next_row = str(len(str_list)+1)
        wks.update(f'A{next_row}', first_name)
        wks.update(f'B{next_row}', username)
        wks.update(f'C{next_row}', date)
        wks.update(f'D{next_row}', link)