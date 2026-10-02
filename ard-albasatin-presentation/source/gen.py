# -*- coding: utf-8 -*-
import sys, json
import core
from slides_e import *


def build():
    S = []

    def add(f, *a):
        S.append(f(len(S) + 1, *a))
    add(s_cover); add(s_agenda)
    add(s_divider, 2); add(s_idea); add(s_idea2); add(s_importance); add(s_goals)
    add(s_divider, 3); add(s_info); add(s_audience); add(s_platforms)
    add(s_divider, 4); add(s_desc); add(s_problem); add(s_value)
    add(s_divider, 5); add(s_demo); add(s_interests); add(s_needs); add(s_behavior)
    add(s_divider, 6); add(s_comp_id); add(s_comp_sw); add(s_comp_style); add(s_comp_opp)
    add(s_divider, 7); add(s_swot1); add(s_swot2)
    add(s_divider, 8); add(s_goal_main); add(s_goals8); add(s_platwhy); add(s_style1); add(s_style2); add(s_journey)
    add(s_divider, 9); add(s_plan); [add(s_week, k) for k in range(4)]; add(s_dist); add(s_message)
    add(s_divider, None, T(254), 'G')
    add(s_ex1); add(s_ex2); add(s_ex3); add(s_ex4); add(s_ex5); add(s_ex6); add(s_ex7)
    add(s_show1); add(s_show2); add(s_valueex); add(s_adex)
    add(s_pas); add(s_pas_p); add(s_pas_a); add(s_pas_s)
    add(s_persona1); add(s_persona2)
    add(s_close)
    return S


S = build()
core.NTOTAL = len(S)
core.USED.clear()
S = build()
open('deck/deck.html', 'w').write(page(S))
json.dump(sorted(core.USED), open('deck/used.json', 'w'))
print(len(S), 'slides')
