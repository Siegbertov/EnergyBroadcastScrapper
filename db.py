import sqlite3
from test import scrapper

class DBHandler:
    def __init__(self, db_filename: str|None = None) -> None:
        if db_filename is None:
            self.__connection = sqlite3.connect(':memory:')
        elif db_filename.endswith('.db'):
            self.__connection = sqlite3.connect(db_filename)
        else:
            print(f"{db_filename} should end <.db>")
        self.__cursor = self.__connection.cursor()
        self.__create_table()

    def __create_table(self) -> None:
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS days (
                                day_name text,
                                first_g text,
                                second_g text,
                                third_g text,
                                fouth_g text,
                                fifth_g text,
                                sixth_g text
                            )""")

    def is_day_in_db(self, day_name:str) -> bool:
        return bool (self.__cursor.execute(f"SELECT * FROM days WHERE day_name= :day_name", {'day_name':day_name}).fetchone())

    def get_all_data(self) -> list:
        return self.__cursor.execute(f"SELECT * FROM days").fetchall()

    def get_day(self, day_name:str) -> tuple:
        return self.__cursor.execute(f"SELECT * FROM days WHERE day_name=:day_name", {'day_name':day_name}).fetchone()

    def update_day(self, day_name:str, groups:dict):
        with self.__connection:
            if self.is_day_in_db(day_name):
                self.__cursor.execute(
                    """UPDATE days SET first_g=:first_g, second_g=:second_g, third_g=:third_g,
                    fouth_g=:fouth_g, fifth_g=:fifth_g, sixth_g=:sixth_g WHERE day_name=:day_name""",
                    {'day_name': day_name, 'first_g': groups['1'], 'second_g': groups['2'], 'third_g': groups['3'], 
                    'fouth_g': groups['4'], 'fifth_g': groups['5'], 'sixth_g': groups['6']}
                                    )
                                       
            else:
                self.__cursor.execute(
                    f"INSERT INTO days VALUES (:day_name, :first_g, :second_g, :third_g, :fouth_g, :fifth_g, :sixth_g)", 
                    {'day_name': day_name, 'first_g': groups['1'], 'second_g': groups['2'], 'third_g': groups['3'], 
                    'fouth_g': groups['4'], 'fifth_g': groups['5'], 'sixth_g': groups['6']}
                                    )                          


def main():
    LINK = "https://t.me/s/ternopiloblenerho"
    DAY_MONTH_RAW = r"(\d+) (\w+),"
    GROUP_RAW = r"(\d\d:\d\d)-(\d\d:\d\d)\s+(\d)\s+\w+"

    db_h = DBHandler()

    days = scrapper(
                    link=LINK,
                    day_month_r=DAY_MONTH_RAW,
                    group_r=GROUP_RAW
                    )   
    for day_name, groups in days.items():
        db_h.update_day(day_name=day_name, groups=groups)

    # for db_day in db_h.get_all_data():
    #     print(db_day)
    #     print()

    print(db_h.get_day(day_name="28 липня"))
    db_h.update_day(day_name="28 липня", groups={"1":"a", "2":"b", "3":"c", "4":"d", "5":"e", "6":"f"})
    print(db_h.get_day(day_name="28 липня"))
    
if __name__ == "__main__":
    main()