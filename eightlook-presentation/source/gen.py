import sys
from slides_d import *
def build():
    S=[]; n=0
    def add(f,*a):
        nonlocal n; n+=1; S.append(f(n,*a))
    add(s_cover); add(s_agenda)
    add(s_divider,1); add(s_intro); add(s_goals)
    add(s_divider,2); add(s_info); add(s_products); add(s_target); add(s_platforms)
    add(s_divider,3); add(s_study)
    add(s_divider,4); add(s_aud1); add(s_aud2)
    add(s_divider,5); [add(s_comp,i) for i in range(4)]
    add(s_divider,6); add(s_swot1); add(s_swot2); add(s_growth)
    add(s_divider,7); add(s_goal_main); add(s_goals8); add(s_platwhy); add(s_style); add(s_journey); add(s_chain)
    add(s_divider,8); add(s_plan); [add(s_week,i) for i in range(4)]; add(s_dist); add(s_path)
    add(s_divider,9); add(s_cw1); add(s_cw2); add(s_cw3); add(s_cw4); add(s_cw5); add(s_cw6)
    add(s_divider,10); add(s_ad1); add(s_ad2); add(s_ad3); add(s_ad4); add(s_ad5); add(s_ad6)
    add(s_pers1a); add(s_pers1b); add(s_pers2a); add(s_pers2b)
    add(s_divider,11); add(s_ai)
    add(s_divider,12); add(s_camp); [add(s_msg,i) for i in range(3)]
    add(s_divider,13); add(s_kpi)
    add(s_close)
    return S
S=build()
open('deck/deck.html','w').write(page(S))
print(len(S),'slides')
