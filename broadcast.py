from day import Day
from utils import clear_console
from utils import get_current_time, italic, UPDATE_EMOJI, DISK_EMOJI
from utils import VIEW, TOTAL, TG

class Broadcast:
    def __init__(self, posts:dict, is_online:bool):
        self.__days = []
        self.__is_online = is_online
        self.__update_time = get_current_time()
        for post_day, post_groups in posts.items():
            self.__days.append(Day(name=post_day, groups=post_groups))

    def get_last_day(self) -> Day:
        return self.__days[-1]

    def show_last_day(self, groups_to_show:list, view:VIEW, total:TOTAL, tg:TG, on_of_emoji:list):
        self.get_last_day().show(
            groups_to_show=groups_to_show, 
            view=view, 
            total=total, 
            tg=tg,
            on_of_emoji=on_of_emoji
            )
    
    def show_all_days(self):
        for day in self.__days:
            day.show()

    def show_update_time(self, tg:TG):
        result = f"{DISK_EMOJI}{self.__update_time}{DISK_EMOJI}"
        if tg is TG.TRUE:
            result = f"{italic(result)}"
        if self.__is_online:
          result = result.replace(DISK_EMOJI, UPDATE_EMOJI)
        print(result+"\n")

    def show(self, 
                groups_to_show:list, 
                view:VIEW, 
                total:TOTAL, 
                tg:TG, 
                on_of_emoji:list
                ):
        clear_console()
        self.show_last_day(
            groups_to_show=groups_to_show, 
            view=view, 
            total=total, 
            tg=tg,
            on_of_emoji=on_of_emoji
            )
        
        self.show_update_time(tg=tg)
        
