from broadcast import Broadcast
from utils import scrapper, read_from_json_file, write_to_json_file, clear_console
from utils import VIEW, TOTAL, TG, MODE

JSON_FILENAME = "posts.json"
DB_FILENAME = "broadcast_archive.db"
LINK = "https://t.me/s/ternopiloblenerho"
# DAY_MONTH_RAW = r"(\d+) (\w+), з 00:00 до 24:00" # OLD WAY
DAY_MONTH_RAW = r"(\d+) (\w+),"
GROUP_RAW = r"(\d\d:\d\d)-(\d\d:\d\d)\s+(\d)\s+\w+"


def main():
    IS_ONLINE = False
    POSTS = scrapper(
        link=LINK,
        day_month_r=DAY_MONTH_RAW,
        group_r=GROUP_RAW
    )
    if POSTS:
        IS_ONLINE = True
        write_to_json_file(
            data=POSTS,
            filename=JSON_FILENAME
        )
    POSTS = read_from_json_file(JSON_FILENAME)    
    # ---------------------- SETTINGS 
    OFFS = ["🪫", "🔴", "🟥", "🔻", "🌚", "🌑"]
    ONS =  ["🔋", "🟢", "🟩", "⚡️", "🌝", "🌕"]
    S_OFF_EMOJI = OFFS[0]
    S_ON_EMOJI = ONS[0]
    S_ON_OFF_EMOJI = [S_OFF_EMOJI, S_ON_EMOJI]

    S_GROUPS_TO_SHOW = [1, 2, 3, 4, 5, 6]       # list of numbers from 1 to 6 []

    S_SHOW_MODE = MODE.ORDER_R            # FULL, ORDER, ORDER_R
    S_VIEW = VIEW.INLINE                        # <INLINE, ON_PAIRS, OFF_PAIRS>
    S_TOTAL = TOTAL.ON                         # <NONE, ON, OFF>
    S_TG = TG.TRUE                              # <TRUE, FALSE>
    
    # ----------------------------------
    broadcast = Broadcast(
                      posts=POSTS,
                      is_online=IS_ONLINE,
                      db_filename=DB_FILENAME
                      )
    # showing
    match S_SHOW_MODE:
        case MODE.FULL:
            broadcast.show(
                                        groups_to_show=S_GROUPS_TO_SHOW,
                                        view=S_VIEW,
                                        total=S_TOTAL,
                                        tg=S_TG,
                                        on_of_emoji=S_ON_OFF_EMOJI
                                        )
            input()                                    
        case MODE.ORDER:
            for g_num in S_GROUPS_TO_SHOW:
                broadcast.show(
                                            groups_to_show=[g_num],
                                            view=S_VIEW,
                                            total=S_TOTAL,
                                            tg=S_TG,
                                            on_of_emoji=S_ON_OFF_EMOJI
                                        )
                input()
        case MODE.ORDER_R:
            for g_num in S_GROUPS_TO_SHOW[::-1]:
                broadcast.show(
                                            groups_to_show=[g_num],
                                            view=S_VIEW,
                                            total=S_TOTAL,
                                            tg=S_TG,
                                            on_of_emoji=S_ON_OFF_EMOJI
                                        )
                input()
            
    clear_console()

if __name__ == "__main__":
    main()