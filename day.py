from utils import VIEW, TOTAL, TG
from utils import bold, italic, mono, empty

from group import Group

class Day:
    def __init__(self, name:str, groups:dict):
        self.__name = name
        self.__groups = []
        for group_num, group_pairs in groups.items():
            self.__groups.append(Group(num=group_num, off_pairs=group_pairs))

    def show_day_name(self, tg:TG):
        result = f"Графік на {self.__name}:"
        if tg is TG.TRUE:
            result = bold(result)
        print(result+'\n') 

    def show_groups(self, groups_to_show:list, view:VIEW, total:TOTAL, tg:TG, on_of_emoji:list):
        for group in self.__groups:
            if group.get_num() in groups_to_show:
                group.show(
                    view=view, 
                    total=total, 
                    tg=tg, 
                    on_of_emoji=on_of_emoji
                    )

    def show(self, groups_to_show:list, view:VIEW, total:TOTAL, tg:TG, on_of_emoji:list):
        self.show_day_name(tg=tg)
        self.show_groups(
            groups_to_show=groups_to_show, 
            view=view, 
            total=total, 
            tg=tg,
            on_of_emoji=on_of_emoji
            )