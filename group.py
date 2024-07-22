from utils import VIEW, TOTAL, TG
from utils import bold, italic, mono, empty
from utils import difference_in_time, sum_of_time, edit_time_period

class Group:
    def __init__(self, num:str, inline:str) -> None:
        self.__num = num
        self.__LINE = inline

        self.__ON_PAIRS = []
        self.create_on_pairs()

        self.__OFF_PAIRS = []
        self.create_off_pairs()

    def get_num(self) -> int:
        return int(self.__num)

    def create_on_pairs(self):
        if "-" in self.__LINE:
            for elem in self.__LINE.split("-"):
                if "+" in elem:
                    self.__ON_PAIRS.append(elem)

    def create_off_pairs(self):
        if "+" in self.__LINE:
            for elem in self.__LINE.split("+"):
                if "-" in elem:
                    self.__OFF_PAIRS.append(elem)

    def show_num(self, tg:TG):
        result = f"Група #{self.__num}:"
        if tg is TG.TRUE:
            result = bold(result)
        print(result)        

    def show_inline(self, tg:TG, on_of_emoji:list):
        result = f"{self.__LINE}"
        if tg is TG.TRUE:
            result = mono(result)
        result = result.replace("-", on_of_emoji[0])
        result = result.replace("+", on_of_emoji[1])
        # FIXME delete it if you don't need minutes as period
        result = result.replace(":00", "")
        result = edit_time_period(result)
        print(result)     

    def show_only_off_hours(self, tg:TG, off_emoji:str):
        result = '\n'.join(self.__OFF_PAIRS)
        if tg is TG.TRUE:
            result = mono(result)
        result = result.replace("-", off_emoji)
        result = edit_time_period(result)
        print(result) 

    def show_only_on_hours(self, tg:TG, on_emoji:str):
        result = '\n'.join(self.__ON_PAIRS)
        if tg is TG.TRUE:
            result = mono(result)
        result = result.replace("+", on_emoji)
        result = edit_time_period(result)
        print(result)

    def get_total_on_light(self) ->str:
        result = None
        for pair in self.__ON_PAIRS:
            t1, t2 = pair.split("+")
            diff = difference_in_time(t1.split(":"), t2.split(":"))
            if result is None:
                result = diff
            else:
                result = sum_of_time(result, diff)
        return ":".join(result)

    def show_total_on_light(self, tg:TG, on_emoji:str):
        hours, minutes = self.get_total_on_light().split(":")
        result = f"{hours} годин"
        if not (minutes == "00"):
            result += f" {minutes[1] if minutes.startswith('0') else minutes} хвилин"
        result = f"({on_emoji}{result}{on_emoji})"
        if tg is TG.TRUE:
            result = italic(result)
        print(result)
        print()

    def get_total_off_light(self) ->str:
        result = None
        for pair in self.__OFF_PAIRS:
            t1, t2 = pair.split("-")
            diff = difference_in_time(t1.split(":"), t2.split(":"))
            if result is None:
                result = diff
            else:
                result = sum_of_time(result, diff)
        return ":".join(result)

    def show_total_off_light(self, tg:TG, off_emoji:str):
        hours, minutes = self.get_total_off_light().split(":")
        result = f"{hours} годин"
        if not (minutes == "00"):
            result += f" {minutes[1] if minutes.startswith('0') else minutes} хвилин"
        result = f"({off_emoji}{result}{off_emoji})"
        if tg is TG.TRUE:
            result = italic(result)
        print(result) 
        print()

    def show(self, view:VIEW, total:TOTAL, tg:TG, on_of_emoji:list):
        self.show_num(tg=tg)
        
        match view:
            case VIEW.INLINE:
                self.show_inline(tg=tg, on_of_emoji=on_of_emoji)
            case VIEW.ON_PAIRS:
                self.show_only_on_hours(tg=tg, on_emoji=on_of_emoji[1])
            case VIEW.OFF_PAIRS:
                self.show_only_off_hours(tg=tg, off_emoji=on_of_emoji[0])

        match total:
            case TOTAL.ON:
                self.show_total_on_light(tg=tg, on_emoji=on_of_emoji[1])
            case TOTAL.OFF:
                self.show_total_off_light(tg=tg, off_emoji=on_of_emoji[0])
            case TOTAL.NONE:
                print()


            