from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class pagination:

    current_page = 1
    tracks_name_id = {}
    tracks_name_id_list = []
    stream_list = []
    resolution_list = []
    audio_quality = []
    perrow = 10
    link = None
    messageid = None
    total_tracks = None

    def show_buttons(self):
        self.current_page = 1
        button = []
        button.append([InlineKeyboardButton('--Download All--', f'spdlall:'), InlineKeyboardButton('--Download This Page--', f'spdlpg:')])
        for id, name in self.tracks_name_id[self.current_page - 1].items():
            button.append([InlineKeyboardButton(name, f'trckdl:{id}')])
        next_ = InlineKeyboardButton('>', 'next_')
        last_ = InlineKeyboardButton('>>', 'last_')
        if self.current_page == 1:
            button.append([next_, last_])

        return InlineKeyboardMarkup(button)

    def next_button(self):
        self.current_page += 1
        button = []
        button.append([InlineKeyboardButton('--Download This Page--', f'spdlpg:')])
        for id, name in self.tracks_name_id[self.current_page - 1].items():
            button.append([InlineKeyboardButton(name, f'trckdl:{id}')])
        prev_ = InlineKeyboardButton('<', 'prev_')
        next_ = InlineKeyboardButton('>', 'next_')
        first_ = InlineKeyboardButton('<<', 'first_')
        last_ = InlineKeyboardButton('>>', 'last_')
        if self.current_page == 1:
            button.append([next_, last_])
        elif self.current_page == len(self.tracks_name_id):
            button.append([first_, prev_])
        elif self.current_page > 1:
            button.append([first_, prev_, next_, last_])

        return InlineKeyboardMarkup(button)

    def prev_button(self):
        self.current_page -= 1
        button = []
        button.append([InlineKeyboardButton('--Download This Page--', f'spdlpg:')])
        for id, name in self.tracks_name_id[self.current_page - 1].items():
            button.append([InlineKeyboardButton(name, f'trckdl:{id}')])
        prev_ = InlineKeyboardButton('<', 'prev_')
        next_ = InlineKeyboardButton('>', 'next_')
        first_ = InlineKeyboardButton('<<', 'first_')
        last_ = InlineKeyboardButton('>>', 'last_')
        if self.current_page == 1:
            button.pop(0)
            button.insert(0, [InlineKeyboardButton('--Download All--', f'spdlall:'), InlineKeyboardButton('--Download This Page--', f'spdlpg:')])
            button.append([next_, last_])
        elif self.current_page > 1:
            button.append([first_, prev_, next_, last_])

        return InlineKeyboardMarkup(button)

    def first_button(self):
        self.current_page = 1
        button = []
        button.append([InlineKeyboardButton('--Download All--', f'spdlall:'), InlineKeyboardButton('--Download This Page--', f'spdlpg:')])
        for id, name in self.tracks_name_id[self.current_page - 1].items():
            button.append([InlineKeyboardButton(name, f'trckdl:{id}')])
        next_ = InlineKeyboardButton('>', 'next_')
        last_ = InlineKeyboardButton('>>', 'last_')
        if self.current_page == 1:
            button.append([next_, last_])

        return InlineKeyboardMarkup(button)

    def last_button(self):
        self.current_page = len(self.tracks_name_id)
        button = []
        button.append([InlineKeyboardButton('--Download This Page--', f'spdlpg:')])
        for id, name in self.tracks_name_id[self.current_page - 1].items():
            button.append([InlineKeyboardButton(name, f'trckdl:{id}')])
        prev_ = InlineKeyboardButton('<', 'prev_')
        first_ = InlineKeyboardButton('<<', 'first_')
        if self.current_page == len(self.tracks_name_id):
            button.append([first_, prev_])

        return InlineKeyboardMarkup(button)