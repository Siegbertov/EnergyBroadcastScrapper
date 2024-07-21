# EnergyBroadcastScrapper

### SETTINGS:

**S_SHOW_MODE = MODE.ORDER_R**
 - MODE.FULL : _(shows all groups)_
 - MODE.ORDER : _(shows group one by one)_
 - MODE.ORDER_R : _(shows -||- in reversed order)_

**S_GROUPS_TO_SHOW** = [1, 2, 3, 4, 5, 6]
 - [1, 2, 3, 4, 5, 6] : _(all possible groups)_

**S_VIEW = VIEW.INLINE**   
 - INLINE : _(shows one line for each group)_
 - ON_PAIRS : _(shows only ON pairs)_
 - OFF_PAIRS : _(shows obly OFF pairs)_

**S_TOTAL = TOTAL.ON**     
 - NONE : _(doesn't show any total)_
 - ON : _(shows total hours of ON)_
 - OFF : _(shows total hours of OFF)_
   - (TODO: create ON_OFF and OFF_ON)

**S_TG = TG.TRUE**        
 - TRUE : _(edit text for Telegram)_
 - FALSE : _(doesn't edit text)_

OFFS = ["🪫", "🔴", "🟥", "🔻", "🌚","🌑"]

ONS =  ["🔋", "🟢", "🟩", "⚡️", "🌝", "🌕"]

**S_OFF_EMOJI** = OFFS[0]
- _(choose index of OFF_emoji)_
- _(yiu can add your own emoji)_

**S_ON_EMOJI** = ONS[0]
- _(choose index of ON_emoji)_
- _(yiu can add your own emoji)_


**S_ON_OFF_EMOJI** = [S_OFF_EMOJI, S_ON_EMOJI]