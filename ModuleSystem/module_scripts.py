# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from ID_animations import *
from ID_troops import *
from ID_factions import *
from module_troops import *

from module_scripts_ai import *

####################################################################################################################
# scripts is a list of script records.
# Each script record contns the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################


# added subfactions (mtarini)
def set_item_faction():
	command_list = []
	for i_troop in xrange(1,len(troops) ):
		r = 0
		#for i_item in troops[i_troop][7]: 
		for j in range(0,len(subfaction_data) ):
			if troops[i_troop][1].find(subfaction_data[j][2])!=-1: # if there is, e.g.  "Lossarnach" in the name
				r = subfaction_data[j][0]
				command_list.append((troop_set_slot, "trp_"+troops[i_troop][0], slot_troop_subfaction, r))
		#print troops[i_troop][0]
		for i_item in troops[i_troop][7]:   
			command_list.append((item_get_slot , ":valA",i_item, slot_item_faction))
			command_list.append((val_or, ":valA",1 << troops[i_troop][6]))       
			command_list.append((item_set_slot, i_item, slot_item_faction,":valA"))
			command_list.append((item_get_slot, ":valB",i_item, slot_item_subfaction))
			command_list.append((val_or, ":valB",1 << r ))
			command_list.append((item_set_slot, i_item, slot_item_subfaction,":valB"))
	return command_list [:]


# party player icons (mtarini)
# for each faction: icon-mounted, icon-on-foot (melee), icon-on-foot (ranged)
faction_player_icons = [
    ("fac_gondor"  ,"icon_knight_gondor", "icon_footman_gondor", "icon_ithilien_ranger"),
    ("fac_rohan"   ,"icon_knight_rohan", "icon_player", "icon_player"),
    ("fac_isengard","icon_wargrider_run", "icon_uruk_isengard", "icon_uruk_isengard"), # assuming uruk orc (not uruk or evil man). Evil men will be deatl separately
    ("fac_mordor"  ,"icon_wargrider_furshield_run", "icon_uruk", "icon_uruk"),         # same thing
    ("fac_harad"   ,"icon_harad_horseman", "icon_player", "icon_player"),       
    ("fac_rhun"    ,"icon_easterling_horseman", "icon_player", "icon_player"),
    ("fac_khand"   ,"icon_easterling_horseman", "icon_player", "icon_player"),
    ("fac_umbar"   ,"icon_umbar_captain", "icon_umbar_corsair", "icon_umbar_corsair"),
    ("fac_lorien"  ,"icon_knight_rivendell", "icon_lorien_elf_b", "icon_lorien_elf_a"),
    ("fac_imladris","icon_lamedon_horseman", "icon_mirkwood_elf", "icon_mirkwood_elf"),
    ("fac_woodelf" ,"icon_player_horseman", "icon_mirkwood_elf", "icon_mirkwood_elf"),
    ("fac_moria"   ,"icon_wargrider_furshield_run", "icon_orc", "icon_orc"),
    ("fac_guldur"  ,"icon_wargrider_furshield_run", "icon_orc", "icon_orc"),
#    ("fac_northmen","icon_player_horseman", "icon_player", "icon_player"),
    ("fac_gundabad","icon_wargrider_furshield_run", "icon_orc", "icon_orc"),
    ("fac_dale"    ,"icon_player_horseman", "icon_player", "icon_player"),
    ("fac_dwarf"   ,"icon_player_horseman", "icon_dwarf",  "icon_dwarf"),
    ("fac_dunland" ,"icon_dunland_captain", "icon_dunlander", "icon_dunlander"),
    ("fac_beorn"   ,"icon_player_horseman", "icon_player", "icon_player"),

]
  
scripts = [
# script_init_player_map_icons
############################# TLD player icon (mtarini)
# party player icons (mtarini)
  ("init_player_map_icons",[
	# defaults
  	(assign, "$g_player_icon_mounted", "icon_player_horseman"),
	(assign, "$g_player_icon_foot_melee", "icon_player"),
	(assign, "$g_player_icon_foot_archer","icon_player"),

	(assign, ":fac","$players_kingdom"),
	(troop_get_type, ":race","$g_player_troop"),

	(try_begin),
		(eq,0,1),
]+concatenate_scripts([
	(else_try),
		(eq, ":fac", faction_player_icons[y][0]),
		(assign, "$g_player_icon_mounted",    faction_player_icons[y][1]),
		(assign, "$g_player_icon_foot_melee", faction_player_icons[y][2]),
		(assign, "$g_player_icon_foot_archer",faction_player_icons[y][3]),
]for y in range(len(faction_player_icons)) ) +[
	(try_end),
	# fix mordor and isengard NON orcs
	(try_begin),
		(neg|is_between, ":race", tf_orc_begin, tf_orc_end),
		(try_begin),
			(eq, ":fac", "fac_mordor"),
			(assign, "$g_player_icon_mounted", "icon_mordor_captain"),
			(assign, "$g_player_icon_foot_melee", "icon_player"),
			(assign, "$g_player_icon_foot_archer","icon_player"),
		(try_end),
		(try_begin),
			(eq, ":fac", "fac_isengard"),
			(assign, "$g_player_icon_mounted", "icon_isengard_captain"),
			(assign, "$g_player_icon_foot_melee", "icon_player"),
			(assign, "$g_player_icon_foot_archer","icon_player"),
		(try_end),		
	(try_end),
	# fix mordor and isengard orcs NON uruk (non mounted only)
	(try_begin),
		(eq, ":race", tf_orc),
		(try_begin),
			(eq, ":fac", "fac_mordor"),
			(assign, "$g_player_icon_foot_melee", "icon_orc"),
			(assign, "$g_player_icon_foot_archer","icon_orc"),
		(try_end),
		(try_begin),
			(eq, ":fac", "fac_isengard"),
			(assign, "$g_player_icon_foot_melee", "icon_orc_isengard"),
			(assign, "$g_player_icon_foot_archer","icon_orc_isengard"),
		(try_end),		
	(try_end),	
		
  ]
  ),

# script_determine_what_player_looks_like  
  # no input. Call me when player can have changed look
  ("determine_what_player_looks_like", [
    (troop_get_type, ":race","$g_player_troop"),
	(try_begin),
		(is_between, ":race", tf_orc_begin, tf_orc_end),
		(assign, "$player_looks_like_an_orc",1),
	(else_try),
		(assign, "$player_looks_like_an_orc",0),
	(try_end),
  ]
  ),

#############################  TLD PLAYER REWARD SYSTEM --- SCRIPTS   (mtarini)  #############################?#
# script_player_meets_party 
  # PlayerRewardSystem: call this when enetring a city, or meeting a party, so that player's "gold" will update    (mtarini)
  # param1: encountered party
  ("player_meets_party",[

    #MV: old code: didn't work too well, should have detected "territory", not opposing party faction
	# (try_begin),
	  # (store_script_param_1, ":party"),
	  # (store_faction_of_party, ":fac", ":party"),
	  # (is_between, ":fac", kingdoms_begin, kingdoms_end),
	  # (neq, "$ambient_faction", ":fac"), # no need to swap anything, already right
	  # (store_relation, reg0, "fac_player_faction", ":fac"),
      # (ge, reg0, 0), # only with non-enemies	
	  # (call_script, "script_set_ambient_faction", ":fac"),
	# (try_end),
    
    (store_script_param_1, ":party"),
    
    (assign, ":closest_faction", -1),
    (try_begin),
      # check if visiting a friendly town, to optimize code
      (is_between, ":party", centers_begin, centers_end),
      (store_faction_of_party, ":center_faction", ":party"),
      (store_relation, ":relation", ":center_faction", "$players_kingdom"),
      (ge, ":relation", 0),
      (assign, ":closest_faction", ":center_faction"),
    (else_try),
      # find closest friendly active center to determine in whose "territory" is the main party
      (assign, ":mindist", 100000),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (store_relation, ":relation", ":center_faction", "$players_kingdom"),
        (ge, ":relation", 0), # friendly center found
        (store_distance_to_party_from_party, ":dist", "p_main_party", ":center_no"),
        (lt, ":dist", ":mindist"),
        (assign, ":mindist", ":dist"),
        (assign, ":closest_faction", ":center_faction"),
      (try_end),
      (try_begin),
        (eq, ":closest_faction", -1), #all friendly factions defeated, the player is his own faction :)
        (assign, ":closest_faction", "$players_kingdom"),
      (try_end),
    (try_end),
      
    (try_begin),
      (neq, "$ambient_faction", ":closest_faction"), # no need to swap anything, already right
      (call_script, "script_set_ambient_faction", ":closest_faction"),
    (try_end),

  ]),

# script_add_faction_respoint  
  # PlayerRewardSystem:  adds / removes (if neg) some respoints (parameter2) to a given faction (parameter1)  (mtarini)
  ("add_faction_respoint",[
	(store_script_param_1, ":fac"),
	(store_script_param_2, ":diff"),
	(store_mul,  ":diff_neg",  ":diff", -1), # diff = - diff
	(try_begin), (eq, "$ambient_faction", ":fac"), 
		# just rise player gold 
		(set_show_messages, 0),
		(try_begin),(gt, ":diff", 0),
			(troop_add_gold, "$g_player_troop", ":diff"),
		(else_try),
			(troop_remove_gold, "$g_player_troop", ":diff_neg"),
		(try_end),
		(set_show_messages, 1),
	(else_try), 
		# rise res. points of that faction
		(faction_get_slot,  ":rp", ":fac", slot_faction_respoint),
		(store_add,":rp",":rp",":diff"),
		(faction_set_slot, ":fac", slot_faction_respoint, ":rp"),
	(try_end),
	
	(str_store_faction_name, s10, ":fac"),
	(try_begin),(gt, ":diff", 0),
		(assign, reg10, ":diff"),
		(display_message, "@You gain {reg10} Resource Pts. of {s10}."),
	(else_try),(gt, ":diff_neg", 0),
		(assign, reg10, ":diff_neg"),
		(display_message, "@You used {reg10} Resource Pts. of {s10}."),
	(try_end),
  ]),
  
# script_update_respoint
  # PlayerRewardSystem, update_respoint script: makes sure that respoints of active faction reflect current "gold"(no params)  (mtarini)
  ("update_respoint",[
	(store_troop_gold, ":cur_gold", "$g_player_troop"),
	(faction_set_slot, "$ambient_faction", slot_faction_respoint, ":cur_gold"),
  ]),
  
# script_reward_system_init
  # PlayerRewardSystem: init (mtarini)
  ("reward_system_init",[
	(try_for_range, ":fac", kingdoms_begin, kingdoms_end),
		(try_begin),
			(eq,"$players_kingdom", ":fac"),
			(store_troop_gold, ":gold_player", "$g_player_troop"),
			(faction_set_slot,  ":fac", slot_faction_influence, 1),
			(faction_set_slot,  ":fac", slot_faction_rank     , 100),
			(faction_set_slot,  ":fac", slot_faction_respoint , ":gold_player"),
			(assign, "$ambient_faction", ":fac"),
		(else_try),
			(faction_set_slot,  ":fac", slot_faction_influence, 0),
			(faction_set_slot,  ":fac", slot_faction_rank     , 0),
			(faction_set_slot,  ":fac", slot_faction_respoint , 0),
		(try_end),
	(try_end),
	#(str_store_faction_name,s3,"$players_kingdom"),(store_troop_gold, reg3, "$g_player_troop"),
	#(display_message, "@debug: player has faction '{s3}' and {reg3} gold"),
	#]+concatenate_scripts([
	#	(store_set_slot, faction_init[y][0], slot_faction_influence, 0),
	#	(store_set_slot, faction_init[y][0], slot_faction_rank, 0),
	#	(store_set_slot, faction_init[y][0], slot_faction_respoint, 0),
	#]for y in range(len(faction_init)) ) +[
  ]),

# script_set_ambient_faction
  # PlayerRewardSystem, script: stores current gold to appropriate faction's respoint, and resoruce point of a parameter faction to current gold  (mtarini)
  # param1: new current faction
  ("set_ambient_faction",[
    (try_begin),
      (store_script_param_1, ":fac"),
	  (store_troop_gold, ":old_gold", "$g_player_troop"),
	  (faction_get_slot, ":new_gold",  ":fac", slot_faction_respoint),
	  (faction_set_slot, "$ambient_faction", slot_faction_respoint, ":old_gold"),
	
	  (neq, "$ambient_faction", ":fac"), # no need to swap, already right
	  (assign, "$ambient_faction", ":fac"),	
	
	  (set_show_messages, 0),
	  (try_begin),
        (gt, ":old_gold", ":new_gold"),
		(store_sub, ":diff", ":old_gold", ":new_gold"),
		(troop_remove_gold, "$g_player_troop", ":diff"),
	  (else_try),
		(store_sub, ":diff", ":new_gold", ":old_gold"),
		(troop_add_gold, "$g_player_troop", ":diff"),
	  (try_end),
	  (set_show_messages, 1),

	#(str_store_faction_name, s10, "$ambient_faction"),			
	#(display_message, "@info: now using Resource Pts. of {s10}." ),
	(try_end),
  ]),

# script_rank_income_to_player
 # PlayerRewardSystem: rank_income (mtarini)
 # gives to player the income of his rank
  ("rank_income_to_player",[
	(try_for_range, ":fac", kingdoms_begin, kingdoms_end),
		(faction_get_slot, ":rank", ":fac", slot_faction_rank ),
		(val_div, ":rank", 100), 
		(gt, ":rank", 0),
		(call_script, "script_get_rank_title", ":fac"),
		(display_message, "@{s24}:"),

		(store_mul, ":income", ":rank", ":rank"), 
		(store_mul, ":rank10", ":rank", 10), 
		(val_mul, ":income", 5),  #  ( rank^2 *5 +rank * 10) =  0,  15 , 30, 55, 90 , 135, 190, 255, ... per day.
		(val_add, ":income", ":rank10"),
		
		(call_script, "script_add_faction_respoint", ":fac", ":income"),
	(try_end),
  ]),
  
# script_get_own_rank_title 
  # PlayerRewardSystem, script: stores in s24 title of a faction, rank, career  (mtarini)
  # param1: faction
  # param2: rank 
  # param3: career variant (e.g. ranger vs knight) TODO
  # output: string 24
  # THIS IS JUST A STUB!!!! TODO: make rank names for all factions!
  ("get_own_rank_title",[
	(store_script_param_1, ":fac"),
	(store_script_param_2, ":rank"),
	(str_store_faction_name, s5, ":fac"),
	(store_div, reg10,":rank", 100),
	(try_begin),
		(ge, reg10, 9), (str_store_string, s24, "@Grandmaster Knight of {s5} (rank {reg10})"),
	(else_try),
		(ge, reg10, 8), (str_store_string, s24, "@Master Knight of {s5}"),
	(else_try),
		(ge, reg10, 7), (str_store_string, s24, "@Veteran Knight of {s5}"),
	(else_try),
		(ge, reg10, 6), (str_store_string, s24, "@Knight of {s5}"),
	(else_try),
		(ge, reg10, 5), (str_store_string, s24, "@Commander of {s5}"),
	(else_try),
		(ge, reg10, 4), (str_store_string, s24, "@Sergeant of {s5}"),
	(else_try),
		(ge, reg10, 3), (str_store_string, s24, "@Veteran of {s5}"),
	(else_try),
		(ge, reg10, 2), (str_store_string, s24, "@Soldier of {s5}"),
	(else_try),
		(ge, reg10, 1), (str_store_string, s24, "@Recruit of {s5}"),
	(else_try),
		(str_store_string, s24, "@Unknown to {s5}"),
	(end_try),
  ]),

# script_get_allied_rank_title
  # PlayerRewardSystem, script: stores in s24 title of a faction, rank, career  (mtarini)
  # param1: faction
  # param2: rank 
  # output: string 24
  # THIS IS JUST A STUB!!!! TODO: make rank allied names for all factions!
  ("get_allied_rank_title",[
	(store_script_param_1, ":fac"),
	(store_script_param_2, ":rank"),
	(str_store_faction_name, s5, ":fac"),
	(store_div, reg10,":rank", 100),
	(try_begin),
		(ge, reg10, 9), (str_store_string, s24, "@Great Hope of {s5} (rank {reg10})"),
	(else_try),
		(ge, reg10, 8), (str_store_string, s24, "@Hope of {s5}"),
	(else_try),
		(ge, reg10, 7), (str_store_string, s24, "@Great Friend of {s5}"),
	(else_try),
		(ge, reg10, 6), (str_store_string, s24, "@Dearest friend of {s5}"),
	(else_try),
		(ge, reg10, 5), (str_store_string, s24, "@Admired friend of {s5}"),
	(else_try),
		(ge, reg10, 4), (str_store_string, s24, "@Trusted friend of {s5}"),
	(else_try),
		(ge, reg10, 3), (str_store_string, s24, "@Friend of {s5}"),
	(else_try),
		(ge, reg10, 2), (str_store_string, s24, "@Familiar to {s5}"),
	(else_try),
		(ge, reg10, 1), (str_store_string, s24, "@Known to {s5}"),
	(else_try),
		              (str_store_string, s24, "@Stranger to {s5}"),
	(end_try),
  ]),

# script_get_rank_title  
  ("get_rank_title",[
	(store_script_param_1, ":fac"),
	(faction_get_slot, ":rank", ":fac", slot_faction_rank ),
	(try_begin),
		(eq, ":fac", "$players_kingdom"),
		(call_script, "script_get_own_rank_title", ":fac", ":rank"),
	(else_try),
		(call_script, "script_get_allied_rank_title", ":fac", ":rank"),
	(try_end),
  ]),

# script_new_rank_attained
("new_rank_attained",
    [ (store_script_param_1, ":fac"),
	  (play_sound, "snd_gong"),
	  (call_script, "script_get_rank_title", ":fac"),
	  (str_store_troop_name, s10, "trp_player"),
	  (display_message, "@You are now {s10}, {s24}", color_good_news),
	]
  ),
  
# script_increase_rank 
  ("increase_rank",
    [ # gain rank (need 100 points to advance)
      (store_script_param_1, ":fac"),
      (store_script_param_2, ":difference"),
	  (faction_get_slot, ":val", ":fac", slot_faction_rank),
	  (store_div, ":old", ":val", 100),
	  (val_add, ":val", ":difference"),
	  (store_div, ":new", ":val", 100),
	  (faction_set_slot, ":fac", slot_faction_rank,  ":val"),
	  
	  # gain 1/10 influence
	  (faction_get_slot, ":val", ":fac", slot_faction_influence),
	  (store_div, ":inf_dif", ":difference", 10),
	  (val_add, ":val", ":inf_dif"),
	  (faction_set_slot, ":fac", slot_faction_influence,  ":val"),

	  # display message
	  # (store_mod, reg10, ":difference", 100),(store_div, reg11, ":difference", 100),
	  # (try_begin), (lt, reg10, 10), (str_store_string, s10, "@.0"), (else_try), (str_store_string, s10, "@."), (try_end),
	  (str_store_faction_name, s11, ":fac"),
	  (assign, reg11, ":difference"),
	  (assign, reg12, ":inf_dif"),
	  (display_message, "@Earned {reg11} rank points and {reg12} influence with {s11}.", color_good_news),
	  
	  # rank increased?
	  (try_begin),
		(neq, ":old", ":new"),
		(call_script, "script_new_rank_attained", ":fac"),
	  (try_end),
 	]
  ),

# script_find_closest_enemy_town_or_host  
# input: faction f,  party x
# output: reg0 = closest party to x enemy of f, but friend of player, reg1 = its distance
("find_closest_enemy_town_or_host",[
	(store_script_param, ":fac", 1),
	(store_script_param, ":target", 2),
	(assign, ":mindist", 100000),
	(assign, ":res", -1),
    (try_for_parties, ":party"),
       (party_is_active, ":party"),
       
       (this_or_next|party_slot_eq, ":party", slot_party_type, spt_kingdom_hero_party),  # its a host
       (this_or_next|party_slot_eq, ":party", slot_party_type, spt_kingdom_hero_alone),  # or a lone hero
	   (is_between, ":party", towns_begin, towns_end),  #or a town
       
	   (store_faction_of_party, ":pfac", ":party"),
	   (store_relation, ":relation", ":pfac", ":fac"),
	   (lt, ":relation", 0), # it's an enemy...
	   
	   (store_relation, ":relation", ":pfac", "$players_kingdom"),
	   (ge, ":relation", 0), # and it's your friend
 
       (store_distance_to_party_from_party, ":dist", ":party", ":target"),
       (lt, ":dist", ":mindist"),
	   (assign, ":mindist", ":dist"),
	   (assign, ":res", ":party"),
     (try_end),
	 (assign, reg0, ":res"),
	 (assign, reg1, ":dist"),
     ]),
	 
	 

  # script_npc_get_troop_wage  (mtarini)
  #  called from module system to calculate troop wages for npc parties.
  # Input: param1: troop_id
  # Output: reg0: weekly wage
  ("npc_get_troop_wage",
    [ (store_script_param_1, ":troop_id"),
	  (call_script, "script_game_get_troop_wage", ":troop_id",0)
  ]),
  
  # script_game_get_join_cost  (mtarini)
  # This script is called from the game engine for calculating troop join cost.
  # Input:   param1: troop_id,
  # Output: reg0: join cost
  ("game_get_join_cost",
  [ (store_script_param_1, ":troop_id"),
	(call_script, "script_game_get_troop_wage", ":troop_id",0),
	(val_mul, reg0, 3), # to join, twice than day upkeep x 3
	(set_trigger_result, reg0),
  ]),
  
# script_get_troop_disband_cost
  # Call this script to know how much the player earns if he sends this troop home  (mtarini)
  # Input:   param1: troop_id,  
  # Input:   param2: 0 = auto, 1 = perfect helath  2 =  wounded
  # Input:   param3: 0 = sent home from map,   1 = given to city,    2 = given to host
  # Output: reg15: leave cost
  ("get_troop_disband_cost",
  [	    (store_script_param_1, ":troop_id"),
		(store_script_param_2, ":opt"),
		(store_script_param,   ":origin", 3),
		
		# determine if troop is wounded
		(assign, ":wounded",0),
		(try_begin),(eq,":opt",0), # auto check if wounded
			(try_begin),
			  (call_script, "script_cf_is_troop_in_party_wounded", ":troop_id", "p_main_party"),
			  (assign, ":wounded",1),
			(try_end),
		(else_try),  (eq,":opt",2), # assume it is wounded
			(assign, ":wounded",1),
		(try_end),

		(assign, ":perc", 80), # base: 80 percent
		(try_begin),(eq,":origin",0), (assign, ":perc", 70), (try_end), # from map: 70%
		(try_begin),(eq,":origin",1), (assign, ":perc", 80), (try_end), # to city garrison: 80%
		(try_begin),(eq,":origin",2), (assign, ":perc", 90), (try_end), # to war party: 90%
		(try_begin),(eq,":wounded",1),(val_sub,":perc", 30), (try_end), # if wounded: -30%
		
		(call_script, "script_game_get_join_cost", ":troop_id"),
		(val_mul, reg0, ":perc"), 
		(store_div, reg15, reg0, 100), # when this troop leaves, you gain  $ join_cost * perc/100  
  ]),
 
  # script_get_party_disband_cost 
  # Call this script to know how much the player earns if this entire party is disbanded (mtarini)
  # Input:   param1: party_id,  
  # Input:   param2: 0 = sent home from map,   1 = given to city    2 = given to host
  # Output: reg0: leave cost of party  
  ("get_party_disband_cost",
  [	(store_script_param_1, ":party_id"),
	(store_script_param_2, ":origin"),
	(party_get_num_companion_stacks, ":num_stacks", ":party_id"),
	(assign, ":tot", 0),
	(try_for_range, ":i", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",  ":party_id", ":i"),
        (party_stack_get_size, ":n_ok", ":party_id", ":i"),
        (party_stack_get_num_wounded, ":n_wounded", ":party_id", ":i"),
		(val_sub, ":n_ok", ":n_wounded"),
		
        (call_script, "script_get_troop_disband_cost", ":stack_troop",1,":origin"),
        (val_mul, reg15, ":n_ok"),
        (val_add, ":tot", reg15),
		
        (call_script, "script_get_troop_disband_cost", ":stack_troop",2,":origin"),
        (val_mul, reg15, ":n_wounded"),
        (val_add, ":tot", reg15),
    (try_end),
    (assign, reg0, ":tot"),
  ]),

# script_game_get_troop_wage  
  # This script is called from the game engine for calculating troop wages.  (mod by mtarini)
  # Input: param1: troop_id, param2: party-id
  # Output: reg0: weekly wage
  ("game_get_troop_wage",
    [ (store_script_param_1, ":troop_id"),
      (store_script_param_2, ":unused"), #party id
      
	  (store_character_level, ":troop_level", ":troop_id"),
      (assign, ":wage", ":troop_level"),
      (val_add, ":wage", 3),
      (val_mul, ":wage", ":wage"),
      (val_div, ":wage", 25),

	  (troop_get_type, reg13, ":troop_id"),
	  (try_begin), (eq, reg13, tf_troll),
		(val_add, ":wage", 5),
		(val_mul, ":wage", 27),# trolls cost x 27
	  (try_end),
	  
      (try_begin), #mounted troops cost 50% more than the normal cost
        (troop_is_mounted, ":troop_id"),
        (val_mul, ":wage", 150),
        (val_div, ":wage", 100),
      (try_end),
       
	  (try_begin), #mounted troops cost 50% more than the normal cost
		(troop_is_hero,":troop_id"), # no upkeep for heros! (player included)
		(assign, reg0, 0),
      (try_end),
	  
      (assign, reg0, ":wage"),
      (set_trigger_result, reg0),
  ]),
  
  # script_game_get_total_wage  (mod by mtarini)
  # This script is called from the game engine for calculating total wage of the player party which is shown at the party window.
  # Input: none
  # Output: reg0: weekly wage
  ("game_get_total_wage",
    [ (assign, ":total_wage", 0),
      (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
        (party_stack_get_size, ":stack_size", "p_main_party", ":i_stack"),
        (call_script, "script_game_get_troop_wage", ":stack_troop",0),
        (val_mul, reg0, ":stack_size"),
        (val_add, ":total_wage", reg0),
      (try_end),
      (assign, reg0, ":total_wage"),
      (set_trigger_result, reg0),
  ]),

  # script_compute_wage_per_faction  (mtarini)
  # Input: arg1 = faction
  # Output: reg4 = weekly wage per faction (player has to pay)
  ("compute_wage_per_faction",
  [ (store_script_param_1, ":fac"),
	(assign, ":party", "p_main_party"),
	(assign, ":spending",  0), # for this faction
	(party_get_num_companion_stacks, ":num_stacks","p_main_party"),
	
	(try_for_range, ":i", 0, ":num_stacks"),
		(party_stack_get_size, ":stack_size",":party",":i"),
		(party_stack_get_troop_id, ":stack_troop",":party",":i"),

		(store_troop_faction, ":fac_troop", ":stack_troop"),
		(eq,":fac_troop",":fac"),
		
		(call_script, "script_game_get_troop_wage", ":stack_troop",0 ),
		(assign, ":cur_wage", reg0),
		(val_mul, ":cur_wage", ":stack_size"),
						
		(val_add, ":spending", ":cur_wage"),
	(end_try),  # end of for each stack
	(assign, reg4, ":spending"),
  ]
  ),
  
  # script_make_player_pay_upkeep  (mtarini)
  # no input, no output
  ("make_player_pay_upkeep",
   [(call_script, "script_update_respoint"), # make sure respoint are up-to-date (with current gold)
	(assign, ":party", "p_main_party"), # pay only for player party (no garrisons, for now)
	(party_get_num_companion_stacks, ":num_stacks",":party"),
	
	(assign, ":n_tot_unpaid_troops",  0), # for all factions
	(assign, ":tot_spending",  0), # for all factions
	(str_clear, s10 ), # list of unpaid faction
	
	(display_message, "@Troop upkeep:"),

	(try_for_range, ":fac", kingdoms_begin, kingdoms_end),
		(faction_get_slot, ":allowance",  ":fac", slot_faction_respoint),
		
		(assign, ":spending",  0), # for this faction
		(assign, ":n_unpaid_troops",  0), # for this faction
		
		(try_for_range_backwards, ":i", 0, ":num_stacks"),
			(party_stack_get_size, ":stack_size",":party",":i"),
			(party_stack_get_troop_id, ":stack_troop",":party",":i"),

			(store_troop_faction, ":fac_troop", ":stack_troop"),
			(eq,":fac_troop",":fac"),
			
			(call_script, "script_game_get_troop_wage", ":stack_troop",0 ),
			(assign, ":cur_wage", reg0),
			(val_mul, ":cur_wage", ":stack_size"),		
			
			# up to 50% discont, if spent time indoor
			(store_sub, ":total_payment", 8, "$g_cur_week_half_daily_wage_payments"), #between 0 and 4
			(val_mul, ":cur_wage", ":total_payment"),
		
			(val_div, ":cur_wage", 8),
		
			(try_begin), (ge,  ":allowance",":cur_wage"), 
				# CAN afford
				(val_add, ":spending", ":cur_wage"),
				(val_add, ":tot_spending", ":cur_wage"),
				(val_sub, ":allowance",":cur_wage"), 
				(troop_set_slot, ":stack_troop", slot_troop_upkeep_not_paid, 0),
			(else_try),
				# CAN'T afford
				(val_add, ":n_unpaid_troops", ":stack_size"),
				(troop_set_slot, ":stack_troop", slot_troop_upkeep_not_paid, 1),
			(end_try),
			
		(end_try),  # end of for each stack

		(try_begin),(gt,  ":n_unpaid_troops", 0 ), 
		    (assign, reg12, ":n_unpaid_troops"),
			(str_store_faction_name,s11,":fac"),
			(try_begin), (gt, ":n_tot_unpaid_troops", 0),  #  not first time
				(str_store_string, s10, "@{s11} and {s10}"), 
				(str_store_string, s12, "@their"), 
			(else_try),
				(str_store_string, s10, "@{s11}"),
				(str_store_string, s12, "@its"), 
			(end_try),
			(assign, ":n_unpaid_troops", ":stack_size" ), # for this faction
		(end_try),
		
		(val_add, ":n_tot_unpaid_troops", ":n_unpaid_troops"),
		
		(gt,  ":spending", 0),
		(store_mul, reg10, ":spending", -1),
		(call_script, "script_add_faction_respoint", ":fac", reg10),
			
	(end_try),  # end of for each faction

	(try_begin),(eq,  ":tot_spending", 0 ),(eq,  ":n_tot_unpaid_troops", 0 ), 
		(display_message, "@[no upkeep costs]"),
	(end_try),
	(try_begin),(gt, ":n_tot_unpaid_troops", 0),
		(display_message, "@Short of Resource Points!!", color_bad_news),
		(display_message, "@{s10} will soon reassign some of {s12} troops away from your party!", color_bad_news),
	(end_try),
	
	(assign, "$g_cur_week_half_daily_wage_payments", 0), # reset "rest in city" discount
   ]),
	
	
	# script_make_unpaid_troop_go  (mtarini)
    #  No input, no output. Just makes the "unpaid" troops of player party leave the party, if you still don't have the money
	("make_unpaid_troop_go",
    [
	(call_script, "script_update_respoint"), # make sure respoint are up-to-date (with current gold)
	(assign, ":party", "p_main_party"), 
	(party_get_num_companion_stacks, ":num_stacks",":party"),
	
	(assign, ":tot_spending",  0), # for all factions
	(str_clear, s12 ), # list of unpaid faction

	(try_for_range, ":fac", kingdoms_begin, kingdoms_end),
		(faction_get_slot, ":allowance",  ":fac", slot_faction_respoint),
		
		(assign, ":spending",  0), # for this faction
		
		#(assign, ":n_tot_left",  0), # for this factions
		(assign,  ":msg_shown", 0),
		
		(try_for_range_backwards, ":i", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop",":party",":i"),  
			(ge, ":stack_troop", 0),
			(troop_slot_eq, ":stack_troop", slot_troop_upkeep_not_paid, 1), # the upkeep of these guys wasn't paid
			(store_troop_faction, ":fac_troop", ":stack_troop"),(eq,":fac_troop",":fac"),  # and they are of the right faction
			(troop_set_slot, ":stack_troop", slot_troop_upkeep_not_paid, 0),

			(party_stack_get_size, ":stack_size",":party",":i"),
			(party_stack_get_num_wounded, ":stack_wounded",":party",":i"),
			

			(call_script, "script_game_get_troop_wage", ":stack_troop",0 ), (assign, ":wage", reg0),
			(call_script, "script_get_troop_disband_cost", ":stack_troop",1 ,0 ), (assign, ":gain_ok", reg15),
			(call_script, "script_get_troop_disband_cost", ":stack_troop",2 ,0 ), (assign, ":gain_ko", reg15),

			# up to 50% discount, if spent time indoor
			(store_sub, ":total_payment", 8, "$g_cur_week_half_daily_wage_payments"), #between 0 and 4
			(val_mul, ":wage", ":total_payment"),
			(val_div, ":wage", 8),
			
			(assign, ":n_left",  0), # for his stack

			(try_for_range, ":unused", 0, ":stack_size"), # for each troop in stack
			
				(try_begin), (ge,  ":allowance",":wage"), 
					# CAN afford: stays. Pay wage
					(val_add, ":spending", ":wage"),
					(val_add, ":tot_spending", ":wage"),
					(val_sub, ":allowance",":wage"), 
				(else_try),
					# CAN'T afford: leaves. Gain premium.
					(assign, ":gain", ":gain_ok"),
					(try_begin), (gt, ":stack_wounded", 0),  # if wounded, gain less money
						(val_sub, ":stack_wounded", 1),
						(assign, ":gain", ":gain_ko"),
					(end_try),
					(val_sub, ":spending", ":gain"),  # gain RP
					(val_sub, ":tot_spending", ":gain"), # gain RP
					(val_add, ":allowance",":gain"), # gain RP
					(val_add, ":n_left",  1), 
					#(val_add, ":n_tot_left",  1), 
				(end_try),
			(try_end), # end of a stack
			
			(gt, ":n_left", 0),
			(try_begin),(eq, ":msg_shown", 0),
				(str_store_faction_name,s11,":fac"),
				(display_message, "@Superior orders from {s11} to reassign troops:", color_bad_news),
				(assign,  ":msg_shown", 1), # only once
			(end_try),
			
			(str_store_troop_name_by_count,s10,":stack_troop", ":n_left"),
			(assign, reg12, ":n_left"),
			
			(display_message, "@{reg12} {s10} left the party!", color_bad_news),
			(party_remove_members, ":party", ":stack_troop", ":n_left"),
		(end_try),  # end of for all stacks
		
		(neq,  ":spending", 0),
		(store_mul, reg10, ":spending", -1),
		(call_script, "script_add_faction_respoint", ":fac", reg10),
		
	(end_try),  # end of for each faction


	]),
	
#############################  TLD PLAYER REWARD SYSTEM --- SCRIPTS  END  (mtarini)  #############################?#
#script_cf_is_troop_in_party_wounded 
  #is a regular troop wounded inside a party?  (mtarini)
  # INPUT: arg1 = faction_no, arg2 = owner_troop_no
  #OUTPUT: nothing (can fail)
  ("cf_is_troop_in_party_wounded",
    [ (store_script_param, ":troop", 1),
      (store_script_param, ":party", 2),
	  (assign, ":yes", 0), 
      (party_get_num_companion_stacks, ":num_stacks", ":party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", ":party", ":i_stack"),
        (eq, ":stack_troop", ":troop"),
		(party_stack_get_num_wounded,":nw",":party",":i_stack"),
		(gt, ":nw", 1), # if there are wounded
        (assign, ":yes", 1), # then yes
      (try_end),
	  (eq, ":yes", 1), # fails if not wounded
   ]),
   
#script_cf_is_troop_in_party_not_wounded 
   # as above, but the opposite
   ("cf_is_troop_in_party_not_wounded",
    [
      (store_script_param, ":troop", 1),
      (store_script_param, ":party", 2),
	  (assign, ":yes", 0), 
      (party_get_num_companion_stacks, ":num_stacks", ":party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", ":party", ":i_stack"),
        (eq, ":stack_troop", ":troop"),
		(party_stack_get_num_wounded,":nw",":party",":i_stack"),
		(gt, ":nw", 1), # if there are wounded
        (assign, ":yes", 1), # then yes
      (try_end),
	  (eq, ":yes", 0), # fails if not wounded   ]),
	]),  

#script_store_troop_king_in_s15    
# get a troop (param1) and return how player will refer to that troop's king  (mtarini)
("store_troop_king_in_s15",[
	(store_script_param_1, ":troop"),
	(store_troop_faction, ":fac", ":troop"),
	
	(try_begin), (eq, ":fac", "fac_gondor"),
		(str_store_string, s15,"@the Steward"),
	(else_try),
		(try_begin),(eq, ":fac", "$players_kingdom"),
			(str_store_string, s13,"@our"),
		(else_try),
			(str_store_string, s13,"@your"),
		(try_end),
		(try_begin),(faction_slot_eq, ":fac", slot_faction_side, faction_side_good ),
			(str_store_string, s15,"@{s13} King"),
		(else_try),
			(str_store_string, s15,"@{s13} Master"),
		(try_end), 
	(try_end),
  
]),
 
 
 
 #############################  TLD FANGORN SCRIPTS   (mtarini)  #############################?#
#script_fangorn_deal_damage
  # script: deal 'fangorn damage' to a party (abstact attack by ents):  (mtarini)
  #  INPUT: party to deal damage
  #  OUTPUT: reg0 killed troops. reg1 = wonded troops. reg2 = wounded player (1 or 0)
  ("fangorn_deal_damage", 
  [(store_script_param_1, ":party"),
   (assign,":killed",0),
   (assign,":wounded",0),
   (assign,":leader_wounded",0),
   (try_begin),
     (store_random_in_range, reg0,0,100),
     (lt, reg0, "$g_fangorn_rope_pulled"), # if fangorn rope is not pulled enough, get away with this 
     (party_get_num_companion_stacks, ":num_stacks",":party"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),

         (party_stack_get_troop_id, ":stack_troop",":party",":i_stack"),
         (party_stack_get_size, ":stack_size",":party",":i_stack"),

         (assign, reg0, ":stack_size"),
          #(display_message,"@DEBUG: processing a stack of {reg0} troops"),

         (try_for_range, ":i",0,":stack_size"),
          (store_random_in_range, reg0,0,5), (eq, reg0, 2),  # kill 1 in 5
           (try_begin),
             (store_random_in_range, reg0,0,2), (this_or_next|eq, reg0, 0),  # wound 1 in 2 just wounded (and all heros)
             (troop_is_hero,":stack_troop"),
             (neg|troop_is_wounded,":stack_troop"),
             (party_wound_members,":party",":stack_troop",1),
             (try_begin),
                (troop_is_hero,":stack_troop"),
                (troop_set_health,":stack_troop",0), # heroes  (including player) gets 0 health
             (try_end),
             (try_begin),
                (eq, ":i",0),
                (val_add,":leader_wounded",1),
             (else_try),
                (val_add,":wounded",1),
             (try_end),
           (else_try),
             (party_remove_members,":party",":stack_troop",1),
             (val_add,":killed",reg0),
           (try_end),
         (try_end),         
     (try_end),
   (try_end),
   (assign, reg0, ":killed"),
   (assign, reg1, ":wounded"),
   (assign, reg2, ":leader_wounded"),
  ]),

#script_after_fangorn_damage_to_player 
  # script: after_fangorn_damage_to_player:  (mtarini)
  ("after_fangorn_damage_to_player",
   [ (try_begin),
       (this_or_next|gt,reg0,0),
       (gt,reg1,0),
       (display_message,"@Fangorn claimed {reg0} killed and {reg1} wounded among your troops!", color_bad_news),
     (try_end),
     (try_begin),
       (eq,reg2,1),
       (display_message,"@You were wounded in Fangorn!", color_bad_news),
     (try_end),
   
     (assign, ":player_victim", reg2),
     (store_add, ":troop_victims", reg1,reg0), # killed + wounded victims
     
     (try_begin),  
       (eq, ":player_victim",  1),
       (eq, ":troop_victims", 0), 
       (jump_to_menu, "mnu_fangorn_killed_player_only"),
     (else_try),
       (eq, ":player_victim",  0),
       (gt, ":troop_victims", 0), 
       (jump_to_menu, "mnu_fangorn_killed_troop_only"),
     (else_try),
       (eq, ":player_victim",  1),
       (gt, ":troop_victims", 0), 
       (jump_to_menu, "mnu_fangorn_killed_troop_and_player"),
     (else_try),
       (change_screen_map), # no victims at all
     (try_end),
   ]
  ),
 
#script_party_is_in_fangorn
  # Script: is this party curretnly inside fangorn?   (mtarini)
  #    INPUT: party to test
  #    OUTPUT: reg0  = 1 if yes
  ("party_is_in_fangorn",
   [
    (set_fixed_point_multiplier, 100),
    (store_script_param_1, ":party"),
    (party_get_position, pos1, ":party"),
    (party_get_position, pos2, "p_fangorn_center"),
    (get_distance_between_positions, ":dist", pos1, pos2),
    (party_get_current_terrain, ":terrain_type", ":party"),
# (assign, reg0, ":dist"),
# (assign, reg1, ":terrain_type"),
# (display_message,"@Distance from Fangorn: {reg0}, terrain: {reg1}"),
    
    (try_begin),
      (lt, ":dist", 2500), #MV: was 3200
      (this_or_next|eq, ":terrain_type", rt_steppe_forest),
      (this_or_next|eq, ":terrain_type", rt_forest),
      (eq, ":terrain_type", rt_snow_forest),
      (assign, reg0, 1),
    (else_try),
      (assign, reg0, 0),
    (try_end),
   ]
  ),
  
#script_fangorn_fight_ents
  # Script: start a battle with wandering ents  (mtarini)
  ("fangorn_fight_ents",[
        #(assign, ":ent_troop", "trp_ent"), # should be ents!
        (jump_to_scene, "scn_random_scene_plain_forest"),
        (call_script, "script_setup_random_scene"),
        (set_jump_mission,"mt_fangorn_battle"),
        (modify_visitors_at_site, "scn_random_scene_plain_forest"),
        (reset_visitors),
        (set_party_battle_mode),
        #(store_random_in_range,":n_ents1",1,5),
        #(store_random_in_range,":n_ents2",1,5),
        #(store_add,":n_ents",":n_ents1",":n_ents2"), # 2d5 ents!  
        #(set_visitor, 3, ":ent_troop"),
        #(set_visitor, 2, ":ent_troop"),
        #(set_visitors, 3, ":ent_troop", ":n_ents2"),
        #(set_visitors, 16, ":ent_troop", ":n_ents2"),
        #(set_visitors, 17, ":ent_troop", ":n_ents2"),
        #(set_visitors, 0, ":ent_troop", ":n_ents2"),
        #(set_visitors, 1, ":ent_troop", ":n_ents2"),
        #(set_visitors, 2, "trp_farmer", "$qst_eliminate_bandits_infesting_village_num_villagers"),
        (set_battle_advantage, 0),
        (assign, "$g_battle_result", 0),
        #(set_jump_mission,"mt_fangorn_battle"),
        #(display_message,"@You lead the exploration inside Fangorn forest..."),
        (assign, "$g_next_menu", "mnu_fangorn_battle_debrief"),        
        (jump_to_menu, "mnu_battle_debrief"),
        (assign, "$g_mt_mode", vba_normal),
        (assign, "$cant_leave_encounter", 1),
        (change_screen_mission),
  ]),

  #############################  TLD FANGORN SCRIPTS  END ##############################
  
  
  
  ######################################################################################
  ##############################  GAME START MEGASCRIPT  ###############################
  ######################################################################################
  
  #script_game_start:
  # This script is called when a new game is started
  # INPUT: none
  ("game_start",
   [  (assign, "$g_fangorn_rope_pulled", 0),
	  #(assign, "$g_ent_seen", 0),
	  (assign, "$g_ent_water_ever_drunk", 0),
	  (assign, "$g_ent_water_taking_effect", 0),
      (faction_set_slot, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
      (assign, "$g_player_luck", 200),
      (troop_set_slot, "trp_player", slot_troop_occupation, slto_kingdom_hero),
      (troop_set_slot, "trp_player", slot_troop_prisoner_of_party, -1),
      (try_for_range, ":cur_troop", kingdom_heroes_begin, kingdom_heroes_end),
        (troop_set_slot, ":cur_troop", slot_troop_prisoner_of_party, -1),
        (troop_set_slot, ":cur_troop", slot_troop_custom_banner_flag_type, -1),
        (troop_set_slot, ":cur_troop", slot_troop_custom_banner_map_flag_type, -1),
      (try_end),
      (troop_set_slot, "trp_player", slot_troop_custom_banner_flag_type, -1),
      (troop_set_slot, "trp_player", slot_troop_custom_banner_map_flag_type, -1),
      #Assigning global constant
      (call_script, "script_store_average_center_value_per_faction"),

      (troop_set_slot, "trp_player", slot_troop_custom_banner_bg_color_1, 0xFFFFFFFF),
      (troop_set_slot, "trp_player", slot_troop_custom_banner_bg_color_2, 0xFFFFFFFF),
      (troop_set_slot, "trp_player", slot_troop_custom_banner_charge_color_1, 0xFFFFFFFF),
      (troop_set_slot, "trp_player", slot_troop_custom_banner_charge_color_2, 0xFFFFFFFF),
      (troop_set_slot, "trp_player", slot_troop_custom_banner_charge_color_3, 0xFFFFFFFF),
      (troop_set_slot, "trp_player", slot_troop_custom_banner_charge_color_4, 0xFFFFFFFF),
	  
	  (troop_set_type, "trp_gondor_lord" , 16),  # test!!!


    # TLD: Initialize faction rank
    (troop_set_slot, "trp_player", slot_troop_faction_rank, stfr_rank_mask+stfr_position_mask+stfr_equipments_permit),
#Setting background colors for banners
	  ]+[ (troop_set_slot, "trp_banner_background_color_array", x,  color_list[x])  for x in range(len(color_list)) ]+[
 
      (str_store_troop_name, s5, "trp_player"),
      (party_set_name, "p_main_party", s5),
      (call_script, "script_update_party_creation_random_limits"),
# Reseting player party icon
      (assign, "$g_player_party_icon", -1),
# Setting food bonuses
      (item_set_slot, "itm_smoked_fish", slot_item_food_bonus, 5),
      (item_set_slot, "itm_dried_meat", slot_item_food_bonus, 5),
      (item_set_slot, "itm_cattle_meat", slot_item_food_bonus, 7),
      (item_set_slot, "itm_human_meat", slot_item_food_bonus, 6),
	  (item_set_slot, "itm_lembas", slot_item_food_bonus, 10),

#NPC companion changes begin
      (call_script, "script_initialize_npcs"),
      (assign, "$disable_npc_complaints", 0), #MV: back to 0
#NPC companion changes end

# Setting book intelligence requirements
      #(item_set_slot, "itm_book_tactics", slot_item_intelligence_requirement, 9),
      #(item_set_slot, "itm_book_wound_treatment_reference", slot_item_intelligence_requirement, 10),
      
# Setting the random town sequence:
      (store_sub, ":num_towns", towns_end, towns_begin),
      (assign, ":num_iterations", ":num_towns"),
      (try_for_range, ":cur_town_no", 0, ":num_towns"),
        (troop_set_slot, "trp_random_town_sequence", ":cur_town_no", -1),
      (try_end),
      (assign, ":cur_town_no", 0),
      (try_for_range, ":unused", 0, ":num_iterations"),
        (store_random_in_range, ":random_no", 0, ":num_towns"),
        (assign, ":is_unique", 1),
        (try_for_range, ":cur_town_no_2", 0, ":num_towns"),
          (troop_slot_eq, "trp_random_town_sequence", ":cur_town_no_2", ":random_no"),
          (assign, ":is_unique", 0),
        (try_end),
        (try_begin),
          (eq, ":is_unique", 1),
          (troop_set_slot, "trp_random_town_sequence", ":cur_town_no", ":random_no"),
          (val_add, ":cur_town_no", 1),
        (else_try),
          (val_add, ":num_iterations", 1),
        (try_end),
      (try_end),
	  
# item faction slots
    (call_script,"script_set_item_faction"),	  

# culture troop slots
	  ]+[
      (faction_set_slot, faction_init[x][0], slot_faction_tier_1_troop,  faction_init[x][4][0])  for x in range(len(faction_init)) ]+[
      (faction_set_slot, faction_init[x][0], slot_faction_tier_2_troop,  faction_init[x][4][1])  for x in range(len(faction_init)) ]+[
      (faction_set_slot, faction_init[x][0], slot_faction_tier_3_troop,  faction_init[x][4][2])  for x in range(len(faction_init)) ]+[
      (faction_set_slot, faction_init[x][0], slot_faction_tier_4_troop,  faction_init[x][4][3])  for x in range(len(faction_init)) ]+[
      (faction_set_slot, faction_init[x][0], slot_faction_tier_5_troop,  faction_init[x][4][4])  for x in range(len(faction_init)) ]+[      
# Faction init from data in module_constants.py
# War system (foxyman)
      (faction_set_slot, faction_init[x][0], slot_faction_strength        , faction_init[x][1])     for x in range(len(faction_init)) ]+[
      (faction_set_slot, faction_init[x][0], slot_faction_culture         , faction_init[x][2])     for x in range(len(faction_init)) ]+[
      (faction_set_slot, faction_init[x][0], slot_faction_leader          , faction_init[x][3])     for x in range(len(faction_init)) ]+[
      (faction_set_slot, faction_init[x][0], slot_faction_tier_1_troop    , faction_init[x][4][0])  for x in range(len(faction_init)) ]+[
      (faction_set_slot, faction_init[x][0], slot_faction_tier_2_troop    , faction_init[x][4][1])  for x in range(len(faction_init)) ]+[
      (faction_set_slot, faction_init[x][0], slot_faction_tier_3_troop    , faction_init[x][4][2])  for x in range(len(faction_init)) ]+[
      (faction_set_slot, faction_init[x][0], slot_faction_tier_4_troop    , faction_init[x][4][3])  for x in range(len(faction_init)) ]+[
      (faction_set_slot, faction_init[x][0], slot_faction_tier_5_troop    , faction_init[x][4][4])  for x in range(len(faction_init)) ]+[
      (faction_set_slot, faction_init[x][0], slot_faction_reinforcements_a, faction_init[x][5][0])  for x in range(len(faction_init)) ]+[
      (faction_set_slot, faction_init[x][0], slot_faction_reinforcements_b, faction_init[x][5][1])  for x in range(len(faction_init)) ]+[
      (faction_set_slot, faction_init[x][0], slot_faction_reinforcements_c, faction_init[x][5][2])  for x in range(len(faction_init)) ]+[
	  (faction_set_slot, faction_init[x][0], slot_faction_prisoner_train  , faction_init[x][5][3])  for x in range(len(faction_init)) ]+[
	  (faction_set_slot, faction_init[x][0], slot_faction_party_map_banner, faction_init[x][7])     for x in range(len(faction_init)) ]+[
# troop slots
      (faction_set_slot, faction_init[x][0], slot_faction_deserter_troop    , faction_init[x][8][0]) for x in range(len(faction_init)) ]+[
      (faction_set_slot, faction_init[x][0], slot_faction_guard_troop       , faction_init[x][8][1]) for x in range(len(faction_init)) ]+[
      (faction_set_slot, faction_init[x][0], slot_faction_messenger_troop   , faction_init[x][8][2]) for x in range(len(faction_init)) ]+[
      (faction_set_slot, faction_init[x][0], slot_faction_prison_guard_troop, faction_init[x][8][3]) for x in range(len(faction_init)) ]+[
      (faction_set_slot, faction_init[x][0], slot_faction_castle_guard_troop, faction_init[x][8][4]) for x in range(len(faction_init)) ]+[

	  (faction_set_slot, faction_init[x][0], slot_faction_capital           , faction_init[x][9])    for x in range(len(faction_init)) ]+[
	  (faction_set_slot, faction_init[x][0], slot_faction_side              , faction_init[x][10])   for x in range(len(faction_init)) ]+[
	  (faction_set_slot, faction_init[x][0], slot_faction_home_theater      , faction_init[x][11])   for x in range(len(faction_init)) ]+[
	  (faction_set_slot, faction_init[x][0], slot_faction_advance_camp      , faction_init[x][12])   for x in range(len(faction_init)) ]+[
# rumors in shops and tavers
	  (faction_set_slot, faction_strings[x][0], slot_faction_rumors_begin   , faction_strings[x][1])    for x in range(len(faction_init)) ]+[
	  (faction_set_slot, faction_strings[x][0], slot_faction_rumors_end     , faction_strings[x][2])    for x in range(len(faction_init)) ]+[
# ambient sounds
	  (faction_set_slot, faction_strings[x][0], slot_faction_ambient_sound_day   , faction_strings[x][3])    for x in range(len(faction_init)) ]+[
	  (faction_set_slot, faction_strings[x][0], slot_faction_ambient_sound_always, faction_strings[x][4])    for x in range(len(faction_init)) ]+[

# fixed faction info      
	  (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
	    (faction_get_slot, ":king", ":faction", slot_faction_leader),
        (faction_set_slot, ":faction", slot_faction_marshall, ":king"),
        
		(faction_get_slot,":strength",":faction",slot_faction_strength),
        (faction_set_slot,":faction",slot_faction_strength_tmp,":strength"),
        
	    (faction_get_slot, ":theater", ":faction", slot_faction_home_theater),
        (faction_set_slot, ":faction", slot_faction_active_theater, ":theater"),
      (try_end),
      (faction_set_slot, "fac_player_supporters_faction", slot_faction_marshall, "trp_player"),

# Towns:
      (try_for_range, ":item_no", trade_goods_begin, trade_goods_end),
        (store_sub, ":offset", ":item_no", trade_goods_begin),
        (val_add, ":offset", slot_town_trade_good_prices_begin),
        (try_for_range, ":center_no", centers_begin, centers_end),
          (party_set_slot, ":center_no", ":offset", average_price_factor),
        (try_end),
      (try_end),

# setting up trade and messenger routes
	  ]+concatenate_scripts([
      [
      (call_script, "script_set_trade_route_between_centers", routes_list[x][0], routes_list[x][y]) for y in range (len(routes_list[x]))
      ] for x in range(len(routes_list))
     ])+[
      (call_script, "script_center_change_trade_good_production", "p_town_minas_tirith", "itm_tools", 110, 0),
      (call_script, "script_center_change_trade_good_production", "p_town_pelargir", "itm_smoked_fish", 130, 0),
      (call_script, "script_center_change_trade_good_production", "p_town_linhir", "itm_tools", 120, 0),
      (call_script, "script_center_change_trade_good_production", "p_town_dol_amroth", "itm_tools", 130, 0),
      (call_script, "script_center_change_trade_good_production", "p_town_edhellond", "itm_tools", 80, 0),
      (call_script, "script_center_change_trade_good_production", "p_town_lossarnach", "itm_tools", 130, 0),
      (call_script, "script_center_change_trade_good_production", "p_town_tarnost", "itm_tools", 140, 0),
      (call_script, "script_center_change_trade_good_production", "p_town_tarnost", "itm_smoked_fish", 110, 0),
      (call_script, "script_center_change_trade_good_production", "p_town_erech", "itm_tools", 130, 0),
      (call_script, "script_center_change_trade_good_production", "p_town_pinnath_gelin", "itm_tools", 135, 0),
      (call_script, "script_center_change_trade_good_production", "p_town_aldburg", "itm_tools", 86, 0),
      (call_script, "script_center_change_trade_good_production", "p_town_edoras", "itm_tools", 130, 0),
      (call_script, "script_center_change_trade_good_production", "p_town_hornburg", "itm_tools", 140, 0),
      (call_script, "script_center_change_trade_good_production", "p_town_east_emnet", "itm_dried_meat", 120, 0),
      (call_script, "script_center_change_trade_good_production", "p_town_westfold", "itm_tools", 120, 0),
      (call_script, "script_center_change_trade_good_production", "p_town_west_emnet", "itm_tools", 100, 0),
      (call_script, "script_center_change_trade_good_production", "p_town_eastfold", "itm_tools", 100, 0),
      (call_script, "script_center_change_trade_good_production", "p_town_morannon", "itm_tools", 100, 0),
      (call_script, "script_center_change_trade_good_production", "p_town_minas_morgul", "itm_tools", 125, 0),

      (try_for_range, ":unused", 0, 1),
        (call_script, "script_average_trade_good_productions"),
      (try_end),
      (call_script, "script_normalize_trade_good_productions"),

# Centers init from data in module_constants.py
        ]+[
        (party_set_slot, center_list[x][0], slot_town_center          , center_list[x][1][0]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_town_castle          , center_list[x][1][1]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_town_prison          , center_list[x][1][2]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_town_tavern          , center_list[x][1][3]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_town_arena           , center_list[x][1][4]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_town_elder           , center_list[x][2][3]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_town_barman          , center_list[x][2][0]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_town_weaponsmith     , center_list[x][2][1]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_town_armorer         , center_list[x][2][1]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_town_merchant        , center_list[x][2][2]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_town_horse_merchant  , center_list[x][2][2]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_town_reinf_pt        , center_list[x][2][4]) for x in range(len(center_list)) ]+[
#walker types
        (party_set_slot, center_list[x][0], slot_center_walker_0_troop, center_list[x][2][6]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_center_walker_1_troop, center_list[x][2][7]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_center_walker_2_troop, center_list[x][2][8]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_center_walker_3_troop, center_list[x][2][9]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_center_walker_4_troop, center_list[x][2][6]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_center_walker_5_troop, center_list[x][2][7]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_center_walker_6_troop, center_list[x][2][8]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_center_walker_7_troop, center_list[x][2][9]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_center_walker_8_troop, center_list[x][2][6]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_center_walker_9_troop, center_list[x][2][7]) for x in range(len(center_list)) ]+[
		(party_set_banner_icon,             center_list[x][0],          center_list[x][3][0]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_center_strength_income,    center_list[x][6]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_center_garrison_limit,     center_list[x][7]) for x in range(len(center_list)) ]+[
        (party_set_slot, center_list[x][0], slot_center_destroy_on_capture, center_list[x][8]) for x in range(len(center_list)) ]+[
#item abundancy in center shops
        (troop_set_slot, center_list[x][2][2], slot_troop_shop_horses  ,center_list[x][4][0] ) for x in range(len(center_list)) ]+[
        (troop_set_slot, center_list[x][2][1], slot_troop_shop_1h      ,center_list[x][4][1] ) for x in range(len(center_list)) ]+[
        (troop_set_slot, center_list[x][2][1], slot_troop_shop_2h      ,center_list[x][4][2] ) for x in range(len(center_list)) ]+[
        (troop_set_slot, center_list[x][2][1], slot_troop_shop_pole    ,center_list[x][4][3] ) for x in range(len(center_list)) ]+[
        (troop_set_slot, center_list[x][2][1], slot_troop_shop_arrows  ,center_list[x][4][4] ) for x in range(len(center_list)) ]+[
        (troop_set_slot, center_list[x][2][1], slot_troop_shop_bolts   ,center_list[x][4][5] ) for x in range(len(center_list)) ]+[
        (troop_set_slot, center_list[x][2][1], slot_troop_shop_shield  ,center_list[x][4][6] ) for x in range(len(center_list)) ]+[
        (troop_set_slot, center_list[x][2][1], slot_troop_shop_bow     ,center_list[x][4][7] ) for x in range(len(center_list)) ]+[
        (troop_set_slot, center_list[x][2][1], slot_troop_shop_crossbow,center_list[x][4][8] ) for x in range(len(center_list)) ]+[
        (troop_set_slot, center_list[x][2][1], slot_troop_shop_thrown  ,center_list[x][4][9] ) for x in range(len(center_list)) ]+[
        (troop_set_slot, center_list[x][2][2], slot_troop_shop_goods   ,center_list[x][4][10]) for x in range(len(center_list)) ]+[
        (troop_set_slot, center_list[x][2][1], slot_troop_shop_head    ,center_list[x][4][11]) for x in range(len(center_list)) ]+[
        (troop_set_slot, center_list[x][2][1], slot_troop_shop_body    ,center_list[x][4][12]) for x in range(len(center_list)) ]+[
        (troop_set_slot, center_list[x][2][1], slot_troop_shop_foot    ,center_list[x][4][13]) for x in range(len(center_list)) ]+[
        (troop_set_slot, center_list[x][2][1], slot_troop_shop_hand    ,center_list[x][4][14]) for x in range(len(center_list)) ]+[
        (troop_set_slot, center_list[x][2][1], slot_troop_shop_gold    ,center_list[x][4][15]) for x in range(len(center_list)) ]+[
        (troop_set_slot, center_list[x][2][2], slot_troop_shop_gold    ,center_list[x][4][15]) for x in range(len(center_list)) ]+[
# give centers to lords
        (call_script, "script_give_center_to_lord", center_list[x][0], center_list[x][2][5], 0) for x in range(len(center_list)) ]+[ 
# center fixed info filling
      (try_for_range, ":town_no", towns_begin, towns_end),
        (party_set_slot, ":town_no", slot_party_type, spt_town),
        (party_set_slot, ":town_no", slot_town_walls, "scn_town_walls"),
        (party_set_slot, ":town_no", slot_town_store, "scn_town_store"),
        (party_set_slot, ":town_no", slot_town_alley, "scn_town_alley"),
        (party_set_slot, ":town_no", slot_town_mercs, "p_town_merc_1"),
      (try_end),

# Centers spawns init from ws_party_spawns_list in module_constants.py      
        ]+[
        (party_set_slot, ws_party_spawns_list[x][0], slot_center_spawn_scouts,  ws_party_spawns_list[x][1]) for x in range(len(ws_party_spawns_list)) ]+[
        (party_set_slot, ws_party_spawns_list[x][0], slot_center_spawn_raiders, ws_party_spawns_list[x][2]) for x in range(len(ws_party_spawns_list)) ]+[
        (party_set_slot, ws_party_spawns_list[x][0], slot_center_spawn_patrol,  ws_party_spawns_list[x][3]) for x in range(len(ws_party_spawns_list)) ]+[
        (party_set_slot, ws_party_spawns_list[x][0], slot_center_spawn_caravan, ws_party_spawns_list[x][4]) for x in range(len(ws_party_spawns_list)) ]+[
# disable some evil centers at start
]+[   (disable_party, centers_disabled_at_start[x]) for x in range(len(centers_disabled_at_start)) ]+[

      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_set_slot, ":center_no", slot_center_last_spotted_enemy, -1),
        (party_set_slot, ":center_no", slot_center_is_besieged_by, -1),
        (party_set_slot, ":center_no", slot_center_last_taken_by_troop, -1),
        #Assigning random prosperity
        (store_random_in_range, ":random_prosperity_adder", -25, 15),
        (call_script, "script_get_center_ideal_prosperity", ":center_no"),
        (assign, ":prosperity", reg0),
        (val_add, ":prosperity", ":random_prosperity_adder"),
        (try_begin),
          (party_slot_eq, ":center_no", slot_party_type, spt_town),
          (val_add, ":prosperity", 20),
        (try_end),
        (val_clamp, ":prosperity", 0, 100),
        (party_set_slot, ":center_no", slot_town_prosperity, ":prosperity"),
      (try_end),
	  
	  (try_for_range, ":town_no", centers_begin, centers_end),
	  	(store_faction_of_party, ":faction", ":town_no"),
		(faction_get_slot, ":tmp",":faction", slot_faction_reinforcements_a),
		(party_set_slot, ":town_no", slot_town_reinforcements_a, ":tmp"),
		(faction_get_slot, ":tmp",":faction", slot_faction_reinforcements_b),
		(party_set_slot, ":town_no", slot_town_reinforcements_b, ":tmp"),
		(faction_get_slot, ":tmp",":faction", slot_faction_reinforcements_c),
		(party_set_slot, ":town_no", slot_town_reinforcements_c, ":tmp"),
    # set center theater according to faction theater - never changes except for advance camps
        (faction_get_slot, ":tmp", ":faction", slot_faction_home_theater),
		(party_set_slot, ":town_no", slot_center_theater, ":tmp"),
    # victory points value on capture/destruction
		(party_set_slot, ":town_no", slot_party_victory_value, ws_center_vp),
	# ambient sounds for centers from faction defaults
        (faction_get_slot, ":tmp", ":faction", slot_faction_ambient_sound_day),
		(party_set_slot, ":town_no", slot_center_ambient_sound_day, ":tmp"),
        (faction_get_slot, ":tmp", ":faction", slot_faction_ambient_sound_always),
		(party_set_slot, ":town_no", slot_center_ambient_sound_always, ":tmp"),
      (try_end),
	  
	  ]+[
      (party_set_slot, subfaction_data[x][1], slot_town_reinforcements_a, subfaction_data[x][4][0])  for x in range(len(subfaction_data)) ]+[
      (party_set_slot, subfaction_data[x][1], slot_town_reinforcements_b, subfaction_data[x][4][1])  for x in range(len(subfaction_data)) ]+[
      (party_set_slot, subfaction_data[x][1], slot_town_reinforcements_c, subfaction_data[x][4][2])  for x in range(len(subfaction_data)) ]+[
	  
	  (party_add_members, subfaction_data[x][1], subfaction_data[x][5][y],1)  for x in range(len(subfaction_data)) for y in range(len(subfaction_data[x][5])) ]+[
# specific centers ambient sounds
      (party_set_slot, center_sounds[x][0], slot_center_ambient_sound_day   , center_sounds[x][1])  for x in range(len(center_sounds)) ]+[
      (party_set_slot, center_sounds[x][0], slot_center_ambient_sound_always, center_sounds[x][2])  for x in range(len(center_sounds)) ]+[

	  ]+[


      #Initialize walkers
      (try_for_range, ":center_no", centers_begin, centers_end),
        (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
                     (party_slot_eq, ":center_no", slot_party_type, spt_village),
        (try_for_range, ":walker_no", 0, num_town_walkers),
          (call_script, "script_center_set_walker_to_type", ":center_no", ":walker_no", walkert_default),
        (try_end),
      (try_end),

# TLD banner assignment		
# assign main faction banners to lords
      ]+[
	   (troop_set_slot, faction_init[x][3], slot_troop_banner_scene_prop, faction_init[x][6]) for x in range(len(faction_init)) ]+[   
      
     (try_for_range, ":kingdom_hero", kingdom_heroes_begin, kingdom_heroes_end),
        (troop_add_gold,":kingdom_hero",100000),
        (store_troop_faction, ":kingdom_hero_faction", ":kingdom_hero"),
	# other heroes get banners like lords, except Rohan (which will be overwritten later)
	    (faction_get_slot,":kingdom_leader",":kingdom_hero_faction",slot_faction_leader),
		(troop_get_slot, ":banner_id", ":kingdom_leader", slot_troop_banner_scene_prop),
		(troop_set_slot, ":kingdom_hero", slot_troop_banner_scene_prop, ":banner_id"),

        (store_character_level, ":level", ":kingdom_hero"),
        (store_mul, ":renown", ":level", ":level"),
        (val_div, ":renown", 2),
        (try_begin),
          (faction_slot_eq, ":kingdom_hero_faction", slot_faction_leader, ":kingdom_hero"),
          (troop_set_slot, ":kingdom_hero", slot_troop_loyalty, 100),
          (store_random_in_range, ":random_renown", 250, 400),
        (else_try),
          (store_random_in_range, ":random_loyalty", 50, 100),
          (troop_set_slot, ":kingdom_hero", slot_troop_loyalty, ":random_loyalty"),
          (store_random_in_range, ":random_renown", 100, 200),
        (try_end),
        (val_add, ":renown", ":random_renown"),
        (troop_set_slot, ":kingdom_hero", slot_troop_renown, ":renown"),
        (store_random_in_range, ":random_readiness", 0, 100),
        (troop_set_slot, ":kingdom_hero", slot_troop_readiness_to_join_army, ":random_readiness"),
        (troop_set_slot, ":kingdom_hero", slot_troop_readiness_to_follow_orders, 100),
        (troop_set_slot, ":kingdom_hero", slot_troop_player_order_state, spai_undefined),
        (troop_set_slot, ":kingdom_hero", slot_troop_player_order_object, -1),
      (try_end),
# Rohan lord banners
    (assign, ":rohan_banner_id", "spr_banner_f01"), #first rohan banner in a list
    (try_for_range, ":rohan_hero", "trp_knight_1_9", "trp_knight_1_15"),
		(troop_set_slot, ":rohan_hero", slot_troop_banner_scene_prop, ":rohan_banner_id"),
		(val_add,":rohan_banner_id",1),
	(try_end),
	
      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_faction_of_party, ":original_faction", ":center_no"),
        (faction_get_slot, ":culture", ":original_faction", slot_faction_culture),
        (party_set_slot, ":center_no", slot_center_culture,  ":culture"),
        (party_set_slot, ":center_no", slot_center_original_faction,  ":original_faction"),
        (party_set_slot, ":center_no", slot_center_ex_faction,  ":original_faction"),
		# TLD center guards
		(faction_get_slot, ":troop", ":original_faction", slot_faction_guard_troop),
        (party_set_slot, ":center_no", slot_town_guard_troop,  ":troop"),
		(faction_get_slot, ":troop", ":original_faction", slot_faction_prison_guard_troop),
        (party_set_slot, ":center_no", slot_town_prison_guard_troop,  ":troop"),
		(faction_get_slot, ":troop", ":original_faction", slot_faction_castle_guard_troop),
        (party_set_slot, ":center_no", slot_town_castle_guard_troop,  ":troop"),
      (try_end),
	# TLD specific center guards
      ]+concatenate_scripts([[
      (party_set_slot, subfaction_data[x][1], slot_town_guard_troop          , subfaction_data[x][3][0]) ,
      (party_set_slot, subfaction_data[x][1], slot_town_prison_guard_troop   , subfaction_data[x][3][1]) ,
      (party_set_slot, subfaction_data[x][1], slot_town_castle_guard_troop   , subfaction_data[x][3][2]) ,
	  (party_set_slot, subfaction_data[x][1],slot_party_subfaction    , subfaction_data[x][0]),
	  (party_get_slot, ":weaponsmith",      subfaction_data[x][1]    , slot_town_weaponsmith),
	  (troop_set_slot, ":weaponsmith",      slot_troop_subfaction    , subfaction_data[x][0]),
	  ]   for x in range(len(subfaction_data)) ])+[
	
	  (party_set_slot, "p_town_minas_tirith", slot_town_castle_guard_troop,  "trp_steward_guard"), # minas tirith exception
      (call_script, "script_update_village_market_towns"),

      (try_for_range, ":troop_id", kingdom_heroes_begin, kingdom_heroes_end),
        (try_begin),
          (store_troop_faction, ":faction_id", ":troop_id"),
          (is_between, ":faction_id", kingdoms_begin, kingdoms_end),
          (troop_set_slot, ":troop_id", slot_troop_original_faction, ":faction_id"),
          (try_begin),
            (is_between, ":troop_id", pretenders_begin, pretenders_end),
            (faction_set_slot, ":faction_id", slot_faction_has_rebellion_chance, 1),
          (else_try),
            (troop_set_slot, ":troop_id", slot_troop_occupation, slto_kingdom_hero),
          (try_end),
        (try_end),
        (assign, ":initial_wealth", 60000),
        (try_begin),
          (store_troop_faction, ":faction", ":troop_id"),
          (faction_slot_eq, ":faction", slot_faction_leader, ":troop_id"),
          (assign, ":initial_wealth", 200000),
        (try_end),
        (troop_set_slot, ":troop_id", slot_troop_wealth, ":initial_wealth"),
      (try_end),

	  # assign volunteer partis to towns (mtarini)
	  (try_for_parties, ":town"), 
		(party_set_slot,":town", slot_town_volunteer_pt, -1),
	  (try_end),

      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),#add town garrisons
        #Add initial center wealth
        (assign, ":initial_wealth", 20000),
        (try_begin),
          (is_between, ":center_no", towns_begin, towns_end),
          (val_mul, ":initial_wealth", 2),
        (try_end),
        (party_set_slot, ":center_no", slot_town_wealth, ":initial_wealth"),
      
        (assign, ":garrison_strength", 13), 
        (try_begin),
          (party_slot_eq, ":center_no", slot_party_type, spt_town),
          (assign, ":garrison_strength", 20), 
        (try_end),
        (try_begin), # TLD: capitals get more
          (store_faction_of_party, ":center_faction", ":center_no"),
          (faction_slot_eq, ":center_faction", slot_faction_capital, ":center_no"),
          (assign, ":garrison_strength", 30), 
        (try_end),
        (party_get_slot, ":garrison_limit", ":center_no", slot_center_garrison_limit),
        (try_for_range, ":unused", 0, ":garrison_strength"),
          (call_script, "script_cf_reinforce_party", ":center_no"),
          (try_begin), #TLD: don't go overboard
            (party_get_num_companions, ":garrison_size", ":center_no"),
            (le, ":garrison_limit", ":garrison_size"),
            (assign, ":garrison_strength", 0),
          (try_end),
        (try_end),
        (try_for_range, ":unused", 0, 2),
          (call_script, "script_maybe_someone_volunteers_in_town", ":center_no"),
        (try_end),
        ## ADD some XP initially
        #(store_div, ":xp_amount", ":garrison_strength", 8),
        #(val_add, ":xp_amount", 4),
        #(try_for_range, ":unused", 0, ":xp_amount"),
        #  (store_random_in_range, ":xp", 7000, 9000),
        #  (party_upgrade_with_xp, ":center_no", ":xp", 0),
        #(try_end),

        #Fill town food stores upto 1/2 the limit
        (call_script, "script_center_get_food_store_limit", ":center_no"),
        (assign,  ":food_store_limit", reg0),
        (val_div, ":food_store_limit", 2),
        (party_set_slot, ":center_no", slot_party_food_store, ":food_store_limit"),
      (try_end),

# spawn lords in random places, TLD
	  (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
	    (faction_get_slot, ":king", ":faction", slot_faction_leader),
        (faction_set_slot, ":faction", slot_faction_marshall, ":king"),
        
		(faction_get_slot,":strength",":faction",slot_faction_strength),
        (faction_set_slot,":faction",slot_faction_strength_tmp,":strength"),      
      (try_end),
# spawn kings in capitals, TLD
    ]+concatenate_scripts([
	  [
	  (call_script, "script_create_kingdom_hero_party", faction_init[x][3], faction_init[x][9]),
	  (party_attach_to_party, "$pout_party", faction_init[x][9])
	  ]  for x in range(len(faction_init)) 
	])+[
# spawn other specific location lords

      (call_script, "script_create_kingdom_hero_party", "trp_knight_1_3", "p_town_dol_amroth"),
      (party_attach_to_party, "$pout_party", "p_town_dol_amroth"),
# spawn lords in random places, TLD
      (try_for_range, ":hero", kingdom_heroes_begin, kingdom_heroes_end),
        (troop_slot_eq, ":hero", slot_troop_leaded_party, 0),
	    (store_troop_faction, ":faction", ":hero"),
        (call_script,"script_cf_select_random_town_with_faction", ":faction"),
		(assign,":center",reg0),
        (call_script, "script_create_kingdom_hero_party", ":hero", ":center"),
        (party_attach_to_party, "$pout_party", ":center"),
        (party_set_slot, ":center", slot_town_player_odds, 1000),  
      (try_end),
	  

      (try_for_range, ":unused", 0, 8),
        (call_script, "script_spawn_bandits"),
      (try_end),

      (set_spawn_radius, 50),
      (try_for_range, ":unused", 0, 25),
        (spawn_around_party,"p_main_party","pt_looters"),
      (try_end),

      (try_for_range, ":unused", 0, 6),
        (call_script, "script_update_trade_good_prices"),
      (try_end),
      
      (call_script, "script_assign_lords_to_empty_centers"),

      (call_script, "script_update_mercenary_units_of_towns"),
      #(call_script, "script_update_companion_candidates_in_taverns"),
      (call_script, "script_update_ransom_brokers"),
      (call_script, "script_update_tavern_travelers"),
      (call_script, "script_update_tavern_minstels"),

#      (try_for_range, ":village_no", villages_begin, villages_end),
#        (call_script, "script_update_volunteer_troops_in_village", ":village_no"),
#      (try_end),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (call_script, "script_update_faction_notes", ":faction_no"),
        (store_random_in_range, ":random_no", -60, 0),
        (faction_set_slot, ":faction_no", slot_faction_ai_last_offensive_time, ":random_no"),
      (try_end),
      #(display_message,"@TEST HERE"),
	  (try_for_range, ":cur_troop", kingdom_heroes_begin, kingdom_heroes_end),
        (call_script, "script_update_troop_notes", ":cur_troop"),
      (try_end),
      (call_script, "script_update_troop_notes", "trp_player"),
      (try_for_range, ":cur_center", centers_begin, centers_end),
        (call_script, "script_update_center_notes", ":cur_center"),
      (try_end),

      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (call_script, "script_faction_recalculate_strength", ":faction_no"),
      (try_end),

      (call_script, "script_get_player_party_morale_values"),
      (party_set_morale, "p_main_party", reg0),
	  
	   # PlayerRewardSystem: end
    ]),    


  # script script_maybe_someone_volunteers_in_town (mtarini)
  ("maybe_someone_volunteers_in_town",[
   (store_script_param_1, ":town"),
   (party_get_slot, ":volunteers", ":town", slot_town_volunteer_pt ),
   (try_begin),
	(store_faction_of_party, ":fac", ":town"), # friendly towns only
	(store_relation, ":rel", ":fac", "fac_player_faction"),
 	(ge, ":rel", 0),

	(try_begin),
		(gt,  ":volunteers", -1),
		(neg|party_is_active, ":volunteers"), # depleted
		(assign,  ":volunteers", -1),
	(try_end),
	(try_begin),
		(lt,  ":volunteers", 0),
		(spawn_around_party, ":town"),
		(assign,":volunteers", reg0),
		(party_attach_to_party,":volunteers", ":town"),
		(party_set_slot, ":town", slot_town_volunteer_pt, ":volunteers" ),
		(party_set_name, ":volunteers", "@_+_"),
		(party_set_flags, ":volunteers",pf_no_label),
		(party_set_ai_behavior, ":volunteers",ai_bhvr_hold),
	(try_end),
	(store_faction_of_party, ":fac", ":town"),
	
	# compute ideal number of volunteers in r10
	(store_party_size, ":to_add", ":town"),(val_div, ":to_add", 20), #   base: [num-garrisons] / 20
	(faction_get_slot, reg12, ":fac", slot_faction_rank), (val_div, reg12, 100), (val_mul, reg12, 1), (val_add, ":to_add", reg12), #  + rank
	(store_skill_level, reg13, "skl_leadership", "trp_player"), (val_div, reg13, 2), (val_add, ":to_add", reg13),   # +leadership / 2
	
	# compute how many soldiers to add to volunteers
	(store_party_size, reg11, ":volunteers"),
	(val_sub, ":to_add", reg11), # how many troops to add to volunteer (in theory)
	(val_add, ":to_add", 2), (val_div, ":to_add",3), # fill 1/3 of the gap per time
	(store_random_in_range, reg15, 0, 5), (val_add, reg15, -2), (val_add, ":to_add", reg15), # plus random -2 .. +2

	(try_begin),
		(gt, ":to_add", 0), # add volunteers!
		(try_for_range, ":unused", 0, ":to_add"),
			# select three potential volunteers
			(call_script, "script_cf_party_select_random_regular_troop", ":town"),(assign,":vol0", reg0),  # can fail
			(call_script, "script_cf_party_select_random_regular_troop", ":town"),(assign,":vol1", reg0),  # can fail
			(call_script, "script_cf_party_select_random_regular_troop", ":town"),(assign,":vol2", reg0),  # can fail
			# select lower in grade
			(store_character_level, ":lvl0", ":vol0"),
			(store_character_level, ":lvl1", ":vol1"),
			(store_character_level, ":lvl2", ":vol2"),
			(try_begin), (lt, ":lvl1",":lvl0"), (assign,":vol0",":vol1"),(assign,":lvl0",":lvl1"),  (try_end),
			(try_begin), (store_random_in_range, ":tmp", 1,101), (le, ":tmp", 66),
			   (lt, ":lvl2",":lvl0"), (assign,":vol0",":vol2"),(try_end), 
			# move the guy from garrison to volunteers
			(party_remove_members_wounded_first, ":town", ":vol0", 1),
			(party_add_members, ":volunteers", ":vol0", 1),
		(try_end),
	(else_try),
		(lt, ":to_add", 0), # remove volunteers!
		(val_mul, ":to_add", -1),
		(try_for_range, ":unused", 0, ":to_add"),
			(call_script, "script_cf_party_select_random_regular_troop", ":volunteers"),(assign,":guy", reg0),  # can fail
			(party_remove_members_wounded_first, ":volunteers", ":guy", 1),
			(party_add_members, ":town", ":guy", 1),
		(try_end),
	(try_end),
   (try_end),

	
  ]),
 
  # script_troll_hit  (just a test)
  #  called by troll weapon hitting 
  ("troll_hit", [ (display_message,"@DEBUG: Troll hit!!!"),]),
  

  # script_game_event_party_encounter:
  # This script is called from the game engine whenever player party encounters another party or a battle on the world map
  # INPUT:
  # param1: encountered_party
  # param2: second encountered_party (if this was a battle
  ("game_event_party_encounter",
   [
       (store_script_param_1, "$g_encountered_party"),
       (store_script_param_2, "$g_encountered_party_2"),# encountered_party2 is set when we come across a battle or siege, otherwise it's a negative value
	   (call_script, "script_player_meets_party","$g_encountered_party"),  # to set resource points (mtarini)
#       (store_encountered_party, "$g_encountered_party"),
#       (store_encountered_party2,"$g_encountered_party_2"), # encountered_party2 is set when we come across a battle or siege, otherwise it's a minus value
       (store_faction_of_party, "$g_encountered_party_faction","$g_encountered_party"),
       (store_relation, "$g_encountered_party_relation", "$g_encountered_party_faction", "fac_player_faction"),
       (party_get_slot, "$g_encountered_party_type", "$g_encountered_party", slot_party_type),
       (party_get_template_id,"$g_encountered_party_template","$g_encountered_party"),
#       (try_begin),
#         (gt, "$g_encountered_party_2", 0),
#         (store_faction_of_party, "$g_encountered_party_2_faction","$g_encountered_party_2"),
#         (store_relation, "$g_encountered_party_2_relation", "$g_encountered_party_2_faction", "fac_player_faction"),
#         (party_get_template_id,"$g_encountered_party_2_template","$g_encountered_party_2"),
#       (else_try),
#         (assign, "$g_encountered_party_2_faction",-1),
#         (assign, "$g_encountered_party_2_relation", 0),
#         (assign,"$g_encountered_party_2_template", -1),
#       (try_end),

#NPC companion changes begin
       (call_script, "script_party_count_fit_regulars", "p_main_party"),
       (assign, "$playerparty_prebattle_regulars", reg0),

       (assign, "$g_last_rest_center", -1),
       (assign, "$talk_context", 0),
       (assign,"$g_player_surrenders",0),
       (assign,"$g_enemy_surrenders",0),
       (assign, "$g_leave_encounter",0),
       (assign, "$g_engaged_enemy", 0),

       (try_begin),
         (neg|is_between, "$g_encountered_party", centers_begin, centers_end),
         (rest_for_hours, 0), #stop waiting
       (try_end),

       (assign, "$new_encounter", 1), #check this in the menu.
       (try_begin),
         (lt, "$g_encountered_party_2",0), #Normal encounter. Not battle or siege.
         (try_begin),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
           (jump_to_menu, "mnu_castle_outside"),
         (else_try),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
           (jump_to_menu, "mnu_castle_outside"),
         (else_try),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_ship),
           (jump_to_menu, "mnu_ship_reembark"),
         (else_try),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
           (jump_to_menu, "mnu_village"),
         (else_try),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_cattle_herd),
           (jump_to_menu, "mnu_cattle_herd"),
         (else_try),
           (eq, "$g_encountered_party", "p_zendar"),
           (jump_to_menu, "mnu_zendar"),
         (else_try),
           (eq, "$g_encountered_party", "p_salt_mine"),
           (jump_to_menu, "mnu_salt_mine"),
         (else_try),
           (eq, "$g_encountered_party", "p_four_ways_inn"),
           (jump_to_menu, "mnu_four_ways_inn"),
         (else_try),
           (eq, "$g_encountered_party", "p_test_scene"),
           (jump_to_menu, "mnu_test_scene"),
         (else_try),
           (eq, "$g_encountered_party", "p_battlefields"),
           (jump_to_menu, "mnu_battlefields"),
         (else_try),
           (eq, "$g_encountered_party", "p_training_ground"),
           (jump_to_menu, "mnu_tutorial"),
         (else_try),
           (eq, "$g_encountered_party", "p_camp_bandits"),
           (jump_to_menu, "mnu_camp"),
         (else_try),
           (eq, "$g_encountered_party_template", "pt_ruins"), #TLD ruins
           (jump_to_menu, "mnu_ruins"),
         (else_try),
           (jump_to_menu, "mnu_simple_encounter"),
         (try_end),
       (else_try), #Battle or siege
         (try_begin),
           (this_or_next|party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
           (try_begin),
             (eq, "$auto_enter_town", "$g_encountered_party"),
             (jump_to_menu, "mnu_town"),
           (else_try),
             (eq, "$auto_besiege_town", "$g_encountered_party"),
             (jump_to_menu, "mnu_besiegers_camp_with_allies"),
           (else_try),
             (jump_to_menu, "mnu_join_siege_outside"),
           (try_end),
         (else_try),
           (jump_to_menu, "mnu_pre_join"),
         (try_end),
       (try_end),
       (assign,"$auto_enter_town",0),
       (assign,"$auto_besiege_town",0),
      ]),

  #script_game_event_simulate_battle:
  # This script is called whenever the game simulates the battle between two parties on the map.
  # INPUT:
  # param1: Defender Party
  # param2: Attacker Party
  ("game_event_simulate_battle",
    [
       (store_script_param_1, ":root_defender_party"),
       (store_script_param_2, ":root_attacker_party"),

       (try_begin),
         (this_or_next|neg|party_is_active,":root_defender_party"),
         (neg|party_is_active,":root_attacker_party"),
         (set_trigger_result, 1),
       (else_try),
         (store_faction_of_party, ":defender_faction", ":root_defender_party"),
         (store_faction_of_party, ":attacker_faction", ":root_attacker_party"),
         (neq, ":defender_faction", "fac_player_faction"),
         (neq, ":attacker_faction", "fac_player_faction"),
         (store_relation, ":reln", ":defender_faction", ":attacker_faction"),
         (ge, ":reln", 0),
         (set_trigger_result, 1),
       (else_try),
         (assign, ":trigger_result", 0),

         (try_begin),
           (this_or_next|eq, "$g_battle_simulation_cancel_for_party", ":root_defender_party"),
           (eq, "$g_battle_simulation_cancel_for_party", ":root_attacker_party"),
           (assign, "$g_battle_simulation_cancel_for_party", -1),
           (assign, "$auto_enter_town", "$g_battle_simulation_auto_enter_town_after_battle"),
           (assign, ":trigger_result", 1),
         (else_try),
           (try_begin),
             (this_or_next|party_slot_eq, ":root_defender_party", slot_party_retreat_flag, 1),
             (party_slot_eq, ":root_attacker_party", slot_party_retreat_flag, 1),
             (assign, ":trigger_result", 1), #End battle!
           (try_end),
           (party_set_slot, ":root_attacker_party", slot_party_retreat_flag, 0),

  ##         (assign, ":cancel_attack", 0),

           (party_collect_attachments_to_party, ":root_defender_party", "p_collective_ally"),
           (party_collect_attachments_to_party, ":root_attacker_party", "p_collective_enemy"),

 #          (call_script, "script_party_count_fit_for_battle", "p_collective_ally"),
           (call_script, "script_party_calculate_strength", "p_collective_ally", 0),
           (assign, ":defender_strength", reg0),
#           (call_script, "script_party_count_fit_for_battle", "p_collective_enemy"),
           (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
           (assign, ":attacker_strength", reg0),

           (store_div, ":defender_strength", ":defender_strength", 20),
           (val_min, ":defender_strength", 50),
           (val_max, ":defender_strength", 1),
           (store_div, ":attacker_strength", ":attacker_strength", 20),
           (val_min, ":attacker_strength", 50),
           (val_add, ":attacker_strength", 1),
           (try_begin),
             #For sieges increase attacker casualties and reduce defender casualties.
             (this_or_next|party_slot_eq, ":root_defender_party", slot_party_type, spt_castle),
             (party_slot_eq, ":root_defender_party", slot_party_type, spt_town),
             (val_mul, ":defender_strength", 3),
             (val_div, ":defender_strength", 2),
             (val_div, ":attacker_strength", 2),
           (try_end),

           (try_begin),
# WTF, night in TLD is primary WAR TIME =)! GA
#             (neg|is_currently_night), #Don't fight at night
             (inflict_casualties_to_party_group, ":root_attacker_party", ":defender_strength", "p_temp_casualties"),
             (party_collect_attachments_to_party, ":root_attacker_party", "p_collective_enemy"),
           (try_end),
           (call_script, "script_party_count_fit_for_battle", "p_collective_enemy", 0),
           (assign, ":new_attacker_strength", reg0),

           (try_begin),
             (gt, ":new_attacker_strength", 0),
# WTF, night in TLD is primary WAR TIME =)! GA
#             (neg|is_currently_night), #Don't fight at night
             (inflict_casualties_to_party_group, ":root_defender_party", ":attacker_strength", "p_temp_casualties"),
             (party_collect_attachments_to_party, ":root_defender_party", "p_collective_ally"),
           (try_end),
           (call_script, "script_party_count_fit_for_battle", "p_collective_ally", 0),
           (assign, ":new_defender_strength", reg0),

           (try_begin),
             (this_or_next|eq, ":new_attacker_strength", 0),
             (eq, ":new_defender_strength", 0),
    # Battle concluded! determine winner
             (try_begin),
               (eq, ":new_attacker_strength", 0),
               (eq, ":new_defender_strength", 0),
               (assign, ":root_winner_party", -1),
               (assign, ":root_defeated_party", -1),
               (assign, ":collective_casualties", -1),
             (else_try),
               (eq, ":new_attacker_strength", 0),
               (assign, ":root_winner_party",   ":root_defender_party"),
               (assign, ":root_defeated_party", ":root_attacker_party"),
               (assign, ":collective_casualties",    "p_collective_enemy"),
             (else_try),
               (assign, ":root_winner_party", ":root_attacker_party"),
               (assign, ":root_defeated_party",  ":root_defender_party"),
               (assign, ":collective_casualties",  "p_collective_ally"),
             (try_end),

             (try_begin),
               (ge, ":root_winner_party", 0),
               (call_script, "script_get_nonempty_party_in_group", ":root_winner_party"),
               (assign, ":nonempty_winner_party", reg0),
               (store_faction_of_party, ":faction_receiving_prisoners", ":nonempty_winner_party"),
               (store_faction_of_party, ":defeated_faction", ":root_defeated_party"),
             (else_try),
               (assign, ":nonempty_winner_party", -1),
             (try_end),

             (try_begin),
                (ge, ":collective_casualties", 0),
                (party_clear, "p_temp_party"),
                (assign, "$g_move_heroes", 1), 
                (call_script, "script_party_add_party_prisoners", "p_temp_party", ":collective_casualties"),
                (call_script, "script_party_prisoners_add_party_companions", "p_temp_party", ":collective_casualties"),
             (try_end),

             (try_begin),
               (ge, ":collective_casualties", 0),
               (party_get_num_companion_stacks, ":num_stacks", ":collective_casualties"),
             (else_try),
               (assign, ":num_stacks", 0),
             (try_end),
             (try_for_range, ":troop_iterator", 0, ":num_stacks"),
               (party_stack_get_troop_id, ":cur_troop_id", ":collective_casualties", ":troop_iterator"),
               (troop_is_hero, ":cur_troop_id"),
               (call_script, "script_remove_troop_from_prison", ":cur_troop_id"),
               (troop_set_slot, ":cur_troop_id", slot_troop_leaded_party, -1),
               (store_random_in_range, ":rand", 0, 100),
               (str_store_troop_name_link, s1, ":cur_troop_id"),
               (str_store_faction_name_link, s2, ":faction_receiving_prisoners"),
               (store_troop_faction, ":defeated_troop_faction", ":cur_troop_id"),
               (str_store_faction_name_link, s3, ":defeated_troop_faction"),
               (try_begin),
                 (ge, ":rand", hero_escape_after_defeat_chance),
                 (party_stack_get_troop_id, ":leader_troop_id", ":nonempty_winner_party", 0),
                 (is_between, ":leader_troop_id", kingdom_heroes_begin, kingdom_heroes_end), #disable non-kingdom parties capturing enemy lords
#                 (party_add_prisoners, ":nonempty_winner_party", ":cur_troop_id", 1), #TLD: lords captured will later be moved to prisoner train
                 (gt, reg0, 0),
                 #(troop_set_slot, ":cur_troop_id", slot_troop_is_prisoner, 1),
                 (troop_set_slot, ":cur_troop_id", slot_troop_prisoner_of_party, ":nonempty_winner_party"),
                 (display_log_message, "str_hero_taken_prisoner"),
               (else_try),
                 (party_remove_members, "p_temp_party", ":cur_troop_id", 1), #TLD: lords captured will later be moved to prisoner train
                 (try_begin),
                   (store_relation, ":rel", "$players_kingdom", ":defeated_troop_faction"),
                   (lt, ":rel", 0),
                   (assign, ":news_color", color_good_news),
                 (else_try),
                   (assign, ":news_color", color_bad_news),
                 (try_end),
                 (display_message,"@{s1} of {s3} was defeated in battle but managed to escape.", ":news_color"),
               (try_end),
               (try_begin),
                 (store_troop_faction, ":cur_troop_faction", ":cur_troop_id"),
                 (faction_slot_eq, ":cur_troop_faction", slot_faction_marshall, ":cur_troop_id"),
                 #Marshall is defeated, refresh ai.
                 (assign, "$g_recalculate_ais", 1),
               (try_end),
             (try_end),
             (try_begin),
               (ge, ":collective_casualties", 0),
               (party_get_num_prisoner_stacks, ":num_stacks", ":collective_casualties"),
             (else_try),
               (assign, ":num_stacks", 0),
             (try_end),
             (try_for_range, ":troop_iterator", 0, ":num_stacks"),
               (party_prisoner_stack_get_troop_id, ":cur_troop_id", ":collective_casualties", ":troop_iterator"),
               (troop_is_hero, ":cur_troop_id"),
               (call_script, "script_remove_troop_from_prison", ":cur_troop_id"),
               (store_troop_faction, ":cur_troop_faction", ":cur_troop_id"),
               (str_store_troop_name_link, s1, ":cur_troop_id"),
               (str_store_faction_name_link, s2, ":faction_receiving_prisoners"),
               (str_store_faction_name_link, s3, ":cur_troop_faction"),
               (display_log_message,"str_hero_freed"),
             (try_end),

             (try_begin),
                    # TLD: spawn prisoner train
                    (store_party_size, ":size", "p_temp_party"),
                    (gt, ":size", 0),
                    (try_begin),
                        (store_party_size, ":size", "p_temp_party"),
                        (store_party_size_wo_prisoners, ":comps", "p_temp_party"),
                        (val_sub, ":size", ":comps"),
                        (gt, ":size", 0),
                        (is_between, ":faction_receiving_prisoners", kingdoms_begin, kingdoms_end),
                        (faction_get_slot, ":prisoner_train_pt", ":faction_receiving_prisoners", slot_faction_prisoner_train),
                        (neq, ":prisoner_train_pt", -1),
                        (set_spawn_radius, 1),
                        (spawn_around_party, ":nonempty_winner_party", ":prisoner_train_pt"),
                        (assign, ":prisoner_train", reg0),
                        (party_set_faction, ":prisoner_train", ":faction_receiving_prisoners"),
                        (party_set_slot, ":prisoner_train", slot_party_victory_value, ws_p_train_vp),
                        (party_set_slot, ":prisoner_train", slot_party_type, spt_prisoner_train),
                        (assign, "$g_move_heroes", 0), #MV set to 0, lords escape
                        (call_script, "script_party_prisoners_add_party_prisoners", ":prisoner_train", "p_temp_party"),
                        (call_script, "script_party_remove_all_prisoners", "p_temp_party"),
                        (call_script, "script_find_random_nearby_friendly_town", ":prisoner_train", 1),
#                        (str_store_faction_name, s1, ":faction_receiving_prisoners"),
#                        (party_set_name, ":prisoner_train", "@{s1} Prisoner Train"),
                        (party_set_slot, ":prisoner_train", slot_party_ai_state, spai_undefined),
                        (party_set_ai_behavior, ":prisoner_train", ai_bhvr_travel_to_party),
                        (party_set_ai_object, ":prisoner_train", reg0),
                        (party_set_flags, ":prisoner_train", pf_default_behavior, 0),
                    (try_end),
                    (distribute_party_among_party_group, "p_temp_party", ":root_winner_party"), 
                # TLD: spawn prisoner train end
             (try_end),
             
             (call_script, "script_clear_party_group", ":root_defeated_party", ":faction_receiving_prisoners"),
             (assign, ":trigger_result", 1), #End battle!

             #Center captured
             (try_begin),
               (ge, ":collective_casualties", 0),
               (party_get_slot, ":cur_party_type", ":root_defeated_party", slot_party_type),
               (this_or_next|eq, ":cur_party_type", spt_town),
               (eq, ":cur_party_type", spt_castle),

               (assign, "$g_recalculate_ais", 1),

               (store_faction_of_party, ":winner_faction", ":root_winner_party"),
               (store_faction_of_party, ":defeated_faction", ":root_defeated_party"),

               (str_store_party_name, s1, ":root_defeated_party"),
               (str_store_faction_name, s2, ":winner_faction"),
               (str_store_faction_name, s3, ":defeated_faction"),
               (try_begin),
                 (store_relation, ":rel", "$players_kingdom", ":winner_faction"),
                 (gt, ":rel", 0),
                 (assign, ":news_color", color_good_news),
               (else_try),
                 (assign, ":news_color", color_bad_news),
               (try_end),
               (try_begin),
                 (party_slot_eq, ":root_defeated_party", slot_center_destroy_on_capture, 1),
                 (display_log_message, "@{s2} have razed {s1}!", ":news_color"),
               (else_try),
                 (display_log_message, "str_center_captured", ":news_color"),
               (try_end),

               (try_begin),
                    (eq, "$g_encountered_party", ":root_defeated_party"),
  ##                  (display_message, "@Player participation in siege called from g_encountered_party"),
                    (call_script, "script_add_log_entry", logent_player_participated_in_siege, "trp_player",  "$g_encountered_party", 0, "$g_encountered_party_faction"),
               (try_end),
  ##             (try_begin),
  ##                  (eq, "$g_encountered_party_2", ":root_defeated_party"),
  ##                  (display_message, "@Player participation in siege called from game_event_simulate_battle thanks to g_encountered_party"),
  ##             (try_end),
  ##             (try_begin),
  ##                  (eq, "$g_enemy_party", ":root_defeated_party"),
  ##                  (display_message, "@Player participation in siege called from game_event_simulate_battle thanks to g_encountered_party"),
  ##             (try_end),


               (try_begin),
                 (party_get_num_companion_stacks, ":num_stacks", ":root_winner_party"),
                 (gt, ":num_stacks", 0),
                 (party_stack_get_troop_id, ":leader_troop_no", ":root_winner_party", 0),
                 (is_between, ":leader_troop_no", kingdom_heroes_begin, kingdom_heroes_end),
                 (party_set_slot, ":root_defeated_party", slot_center_last_taken_by_troop, ":leader_troop_no"),
               (else_try),
                 (party_set_slot, ":root_defeated_party", slot_center_last_taken_by_troop, -1),
               (try_end),

               (call_script, "script_lift_siege", ":root_defeated_party", 0),
               (try_begin), #TLD: if center destroyable, disable it, otherwise proceed as normal
                 (party_slot_eq, ":root_defeated_party", slot_center_destroy_on_capture, 1),
                 (call_script, "script_destroy_center", ":root_defeated_party"),
               (else_try),
                 (call_script, "script_give_center_to_faction", ":root_defeated_party", ":winner_faction"),
                 (try_begin),
                   (eq, ":defeated_faction", "fac_player_supporters_faction"),
                   (call_script, "script_add_notification_menu", "mnu_notification_center_lost", ":root_defeated_party", ":winner_faction"),
                 (try_end),
                 #Reduce prosperity of the center by 5
                 (call_script, "script_change_center_prosperity", ":root_defeated_party", -5),
                 (call_script, "script_order_best_besieger_party_to_guard_center", ":root_defeated_party", ":winner_faction"),
                 (call_script, "script_cf_reinforce_party", ":root_defeated_party"),
                 (call_script, "script_cf_reinforce_party", ":root_defeated_party"),
               (try_end),
             (try_end),
           (try_end),

           #ADD XP
           (try_begin),
             (party_slot_eq, ":root_attacker_party", slot_party_type, spt_kingdom_hero_party),
             (store_random_in_range, ":random_num",0, 100),
             (lt, ":random_num", 25),
             (gt, ":new_attacker_strength", 0),
             (call_script, "script_upgrade_hero_party", ":root_attacker_party", 1000),
           (try_end),
           (try_begin),
             (party_slot_eq, ":root_defender_party", slot_party_type, spt_kingdom_hero_party),
             (store_random_in_range, ":random_num",0, 100),
             (lt, ":random_num", 25),
             (gt, ":new_defender_strength", 0),
             (call_script, "script_upgrade_hero_party", ":root_defender_party", 1000),
           (try_end),

           (store_random_in_range, ":random_num", 0, 100),
           (try_begin),
             (lt, ":random_num", 10),
  ##           (this_or_next|lt, ":random_num", 10),
  ##           (eq, ":cancel_attack", 1),
             (assign, ":trigger_result", 1), #End battle!
           (try_end),
         (try_end),
         (set_trigger_result, ":trigger_result"),
       (try_end),
  ]),

  #script_game_event_battle_end:
  # This script is called whenever the game ends the battle between two parties on the map.
  # INPUT:
  # param1: Defender Party
  # param2: Attacker Party
  ("game_event_battle_end",
    [
##       (store_script_param_1, ":root_defender_party"),
##       (store_script_param_2, ":root_attacker_party"),
      #Fixing deleted heroes
      (try_for_range, ":cur_troop", kingdom_heroes_begin, kingdom_heroes_end),
        (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
        (troop_get_slot, ":cur_prisoner_of_party", ":cur_troop", slot_troop_prisoner_of_party),
        (try_begin),
          (ge, ":cur_party", 0),
          (assign, ":continue", 0),
          (try_begin),
            (neg|party_is_active, ":cur_party"),
            (assign, ":continue", 1),
          (else_try),
            (party_count_companions_of_type, ":amount", ":cur_party", ":cur_troop"),
            (le, ":amount", 0),
            (assign, ":continue", 1),
          (try_end),
          (eq, ":continue", 1),
          (try_begin),
            (eq, "$cheat_mode", 1),
            (str_store_troop_name, s1, ":cur_troop"),
            (display_message, "@DEBUG: {s1} no longer leads a party."),
          (try_end),
          (troop_set_slot, ":cur_troop", slot_troop_leaded_party, -1),
        (try_end),
        (try_begin),
          (ge, ":cur_prisoner_of_party", 0),
          (assign, ":continue", 0),
          (try_begin),
            (neg|party_is_active, ":cur_prisoner_of_party"),
            (assign, ":continue", 1),
          (else_try),
            (party_count_prisoners_of_type, ":amount", ":cur_prisoner_of_party", ":cur_troop"),
            (le, ":amount", 0),
            (assign, ":continue", 1),
          (try_end),
          (eq, ":continue", 1),
          (try_begin),
            (eq, "$cheat_mode", 1),
            (str_store_troop_name, s1, ":cur_troop"),
            (display_message, "@DEBUG: {s1} is no longer a prisoner."),
          (try_end),
          (call_script, "script_remove_troop_from_prison", ":cur_troop"),
          #searching player
          (try_begin),
            (party_count_prisoners_of_type, ":amount", "p_main_party", ":cur_troop"),
            (gt, ":amount", 0),
            (troop_set_slot, ":cur_troop", slot_troop_prisoner_of_party, "p_main_party"),
            (assign, ":continue", 0),
            (try_begin),
              (eq, "$cheat_mode", 1),
              (str_store_troop_name, s1, ":cur_troop"),
              (display_message, "@DEBUG: {s1} is now a prisoner of player."),
            (try_end),
          (try_end),
          (eq, ":continue", 1),
          #searching kingdom heroes
          (try_for_range, ":cur_troop_2", kingdom_heroes_begin, kingdom_heroes_end),
            (eq, ":continue", 1),
            (troop_get_slot, ":cur_prisoner_of_party_2", ":cur_troop_2", slot_troop_leaded_party),
            (party_is_active, ":cur_prisoner_of_party_2"),
            (party_count_prisoners_of_type, ":amount", ":cur_prisoner_of_party_2", ":cur_troop"),
            (gt, ":amount", 0),
            (troop_set_slot, ":cur_troop", slot_troop_prisoner_of_party, ":cur_prisoner_of_party_2"),
            (assign, ":continue", 0),
            (try_begin),
              (eq, "$cheat_mode", 1),
              (str_store_troop_name, s1, ":cur_troop"),
              (str_store_party_name, s2, ":cur_prisoner_of_party_2"),
              (display_message, "@DEBUG: {s1} is now a prisoner of {s2}."),
            (try_end),
          (try_end),
          #searching walled centers
          (try_for_range, ":cur_prisoner_of_party_2", walled_centers_begin, walled_centers_end),
            (eq, ":continue", 1),
            (party_count_prisoners_of_type, ":amount", ":cur_prisoner_of_party_2", ":cur_troop"),
            (gt, ":amount", 0),
            (troop_set_slot, ":cur_troop", slot_troop_prisoner_of_party, ":cur_prisoner_of_party_2"),
            (assign, ":continue", 0),
            (try_begin),
              (eq, "$cheat_mode", 1),
              (str_store_troop_name, s1, ":cur_troop"),
              (str_store_party_name, s2, ":cur_prisoner_of_party_2"),
              (display_message, "@DEBUG: {s1} is now a prisoner of {s2}."),
            (try_end),
          (try_end),
        (try_end),
      (try_end),
  ]),
  
  #script_order_best_besieger_party_to_guard_center:
  # INPUT:
  # param1: defeated_center, param2: winner_faction
  # OUTPUT:
  # none
  ("order_best_besieger_party_to_guard_center",
    [
      (store_script_param, ":defeated_center", 1),
      (store_script_param, ":winner_faction", 2),
      (assign, ":best_party", -1),
      (assign, ":best_party_strength", 0),
      (try_for_range, ":kingdom_hero", kingdom_heroes_begin, kingdom_heroes_end),
        (troop_get_slot, ":kingdom_hero_party", ":kingdom_hero", slot_troop_leaded_party),
        (gt, ":kingdom_hero_party", 0),
        (store_distance_to_party_from_party, ":dist", ":kingdom_hero_party", ":defeated_center"),
        (lt, ":dist", 5),
        (store_faction_of_party, ":kingdom_hero_party_faction", ":kingdom_hero_party"),
        (eq, ":winner_faction", ":kingdom_hero_party_faction"),
        #If marshall has captured the castle, then do not leave him behind.
        (neg|faction_slot_eq, ":winner_faction", slot_faction_marshall, ":kingdom_hero"),
        (assign, ":has_besiege_ai", 0),
        (try_begin),
          (party_slot_eq, ":kingdom_hero_party", slot_party_ai_state, spai_besieging_center),
          (party_slot_eq, ":kingdom_hero_party", slot_party_ai_object, ":defeated_center"),
          (assign, ":has_besiege_ai", 1),
        (else_try),
          (party_slot_eq, ":kingdom_hero_party", slot_party_ai_state, spai_accompanying_army),
          (party_get_slot, ":kingdom_hero_party_commander_party", ":kingdom_hero_party", slot_party_commander_party),
          (party_slot_eq, ":kingdom_hero_party_commander_party", slot_party_ai_state, spai_besieging_center),
          (party_slot_eq, ":kingdom_hero_party_commander_party", slot_party_ai_object, ":defeated_center"),
          (assign, ":has_besiege_ai", 1),
        (try_end),
        (eq, ":has_besiege_ai", 1),
        (party_get_slot, ":kingdom_hero_party_strength", ":kingdom_hero_party", slot_party_cached_strength),#recently calculated
        (gt, ":kingdom_hero_party_strength", ":best_party_strength"),
        (assign, ":best_party_strength", ":kingdom_hero_party_strength"),
        (assign, ":best_party", ":kingdom_hero_party"),
      (try_end),
      (try_begin),
        (gt, ":best_party", 0),
        (call_script, "script_party_set_ai_state", ":best_party", spai_holding_center, ":defeated_center"),
        (party_set_slot, ":best_party", slot_party_commander_party, -1),
        (party_set_flags, ":best_party", pf_default_behavior, 1),
      (try_end),
      ]),

  #script_game_get_item_buy_price_factor:
  # This script is called from the game engine for calculating the buying price of any item.
  # INPUT:
  # param1: item_kind_id
  # OUTPUT:
  # trigger_result and reg0 = price_factor
  ("game_get_item_buy_price_factor",
    [
      (store_script_param_1, ":item_kind_id"),
      (assign, ":price_factor", 100),

      (call_script, "script_get_trade_penalty", ":item_kind_id"),
      (assign, ":trade_penalty", reg0),

      (try_begin),
        (is_between, "$g_encountered_party", centers_begin, centers_end),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
        (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
        (party_get_slot, ":price_factor", "$g_encountered_party", ":item_slot_no"),
        (val_mul, ":price_factor", 100), #normalize price factor to range 0..100
        (val_div, ":price_factor", average_price_factor),
      (try_end),
      
      (store_add, ":penalty_factor", 100, ":trade_penalty"),
      
      (val_mul, ":price_factor", ":penalty_factor"),
      (val_div, ":price_factor", 100),

      (assign, reg0, ":price_factor"),
      (set_trigger_result, reg0),
  ]),
  
  #script_game_get_item_sell_price_factor:
  # This script is called from the game engine for calculating the selling price of any item.
  # INPUT:
  # param1: item_kind_id
  # OUTPUT:
  # trigger_result and reg0 = price_factor
  ("game_get_item_sell_price_factor",
    [
      (store_script_param_1, ":item_kind_id"),
      (assign, ":price_factor", 100),

      (call_script, "script_get_trade_penalty", ":item_kind_id"),
      (assign, ":trade_penalty", reg0),

      (try_begin),
        (is_between, "$g_encountered_party", centers_begin, centers_end),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
        (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
        (party_get_slot, ":price_factor", "$g_encountered_party", ":item_slot_no"),
        (val_mul, ":price_factor", 100),#normalize price factor to range 0..100
        (val_div, ":price_factor", average_price_factor),
      (else_try),
        #increase trade penalty while selling
        (val_mul, ":trade_penalty", 4),
      (try_end),
      
      
      (store_add, ":penalty_divisor", 100, ":trade_penalty"),
      
      (val_mul, ":price_factor", 100),
      (val_div, ":price_factor", ":penalty_divisor"),
      
      (assign, reg0, ":price_factor"),
      (set_trigger_result, reg0),
  ]),
  
  # script_get_trade_penalty
  # Input: param1 troop_id,
  # Output: reg0
  ("get_trade_penalty",
    [ (store_script_param_1, ":item_kind_id"),
      (assign, ":penalty",0),
      
      (party_get_skill_level, ":trade_skill", "p_main_party", skl_trade),
      (try_begin),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (assign, ":penalty",20),
        (store_mul, ":skill_bonus", ":trade_skill", 1),
        (val_sub, ":penalty", ":skill_bonus"),
      (else_try),
        (assign, ":penalty",100),
        (store_mul, ":skill_bonus", ":trade_skill", 5),
        (val_sub, ":penalty", ":skill_bonus"),
      (try_end),

      (assign, ":penalty_multiplier", 1000),
##       # Apply penalty if player is hostile to merchants faction
##      (store_relation, ":merchants_reln", "fac_merchants", "fac_player_supporters_faction"),
##      (try_begin),
##        (lt, ":merchants_reln", 0),
##        (store_sub, ":merchants_reln_dif", 10, ":merchants_reln"),
##        (store_mul, ":merchants_relation_penalty", ":merchants_reln_dif", 20),
##        (val_add, ":penalty_multiplier", ":merchants_relation_penalty"),
##      (try_end),

       # Apply penalty if player is on bad terms with the town
      (try_begin),
        (is_between, "$g_encountered_party", centers_begin, centers_end),
        (party_get_slot, ":center_relation", "$g_encountered_party", slot_center_player_relation),
        (store_mul, ":center_relation_penalty", ":center_relation", -3),
        (val_add, ":penalty_multiplier", ":center_relation_penalty"),
        (try_begin),
          (lt, ":center_relation", 0),
          (store_sub, ":center_penalty_multiplier", 100, ":center_relation"),
          (val_mul, ":penalty_multiplier", ":center_penalty_multiplier"),
          (val_div, ":penalty_multiplier", 100),
        (try_end),
      (try_end),

       # Apply penalty if player is on bad terms with the merchant (not currently used)
      (call_script, "script_troop_get_player_relation", "$g_talk_troop"),
      (assign, ":troop_reln", reg0),
      #(troop_get_slot, ":troop_reln", "$g_talk_troop", slot_troop_player_relation),
      (try_begin),
        (lt, ":troop_reln", 0),
        (store_sub, ":troop_reln_dif", 0, ":troop_reln"),
        (store_mul, ":troop_relation_penalty", ":troop_reln_dif", 20),
        (val_add, ":penalty_multiplier", ":troop_relation_penalty"),
      (try_end),
      
      (val_mul, ":penalty",  ":penalty_multiplier"),
      (val_div, ":penalty", 1000),
      (val_max, ":penalty", 1),
      (assign, reg0, ":penalty"),
  ]),
  
  #script_game_event_buy_item:
  # This script is called from the game engine when player buys an item.
  # INPUT: param1: item_kind_id
  ("game_event_buy_item",
    [
      (store_script_param_1, ":item_kind_id"),
      (store_script_param_2, ":reclaim_mode"),
      (try_begin),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
        (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
        (party_get_slot, ":multiplier", "$g_encountered_party", ":item_slot_no"),
        (try_begin),
          (eq, ":reclaim_mode", 0),
          (val_add, ":multiplier", 10),
        (else_try),
          (val_add, ":multiplier", 15),
        (try_end),
        (val_min, ":multiplier", maximum_price_factor),
        (party_set_slot, "$g_encountered_party", ":item_slot_no", ":multiplier"),
      (try_end),
  ]),
  
  #script_game_event_sell_item:
  # This script is called from the game engine when player sells an item.
  # INPUT: param1: item_kind_id
  ("game_event_sell_item",
    [
      (store_script_param_1, ":item_kind_id"),
      (store_script_param_2, ":return_mode"),
      (try_begin),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
        (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
        (party_get_slot, ":multiplier", "$g_encountered_party", ":item_slot_no"),
        (try_begin),
          (eq, ":return_mode", 0),
          (val_sub, ":multiplier", 15),
        (else_try),
          (val_sub, ":multiplier", 10),
        (try_end),
        (val_max, ":multiplier", minimum_price_factor),
        (party_set_slot, "$g_encountered_party", ":item_slot_no", ":multiplier"),
      (try_end),
  ]),
  


  # script_game_get_prisoner_price
  # This script is called from the game engine for calculating prisoner price
  # Input:
  # param1: troop_id,
  # Output: reg0
  ("game_get_prisoner_price",
    [
      (store_script_param_1, ":troop_id"),
      (assign, reg0, 50),
      (try_begin),
        #(is_between, "$g_talk_troop", ransom_brokers_begin, ransom_brokers_end),
        (store_character_level, ":troop_level", ":troop_id"),
        (assign, ":ransom_amount", ":troop_level"),
        (val_add, ":ransom_amount", 10), 
        (val_mul, ":ransom_amount", ":ransom_amount"),
        (val_div, ":ransom_amount", 6),
        (assign, reg0, ":ransom_amount"),
      (try_end),
      (set_trigger_result, reg0),
  ]),


  # script_game_check_prisoner_can_be_sold
  # This script is called from the game engine for checking if a given troop can be sold.
  # Input: 
  # param1: troop_id,
  # Output: reg0: 1= can be sold; 0= cannot be sold.
  ("game_check_prisoner_can_be_sold",
    [
      (store_script_param_1, ":troop_id"),
      (assign, reg0, 0),
      (try_begin),
        (neg|troop_is_hero, ":troop_id"),
        (assign, reg0, 1),
      (try_end),
      (set_trigger_result, reg0),
  ]),

  #script_game_event_detect_party:
  # This script is called from the game engine when player party inspects another party.
  # INPUT: param1: Party-id
  ("game_event_detect_party",
    [
        (store_script_param_1, ":party_id"),
        (try_begin),
          (party_slot_eq, ":party_id", slot_party_type, spt_kingdom_hero_party),
          (party_stack_get_troop_id, ":leader", ":party_id", 0),
          (is_between, ":leader", kingdom_heroes_begin, kingdom_heroes_end),
          (call_script, "script_update_troop_location_notes", ":leader", 0),
        (else_try),
          (is_between, ":party_id", walled_centers_begin, walled_centers_end),
          (party_get_num_attached_parties, ":num_attached_parties",  ":party_id"),
          (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
            (party_get_attached_party_with_rank, ":attached_party", ":party_id", ":attached_party_rank"),
            (party_stack_get_troop_id, ":leader", ":attached_party", 0),
            (is_between, ":leader", kingdom_heroes_begin, kingdom_heroes_end),
            (call_script, "script_update_troop_location_notes", ":leader", 0),
          (try_end),
        (try_end),
  ]),

  #script_game_event_undetect_party:
  # This script is called from the game engine when player party inspects another party.
  # INPUT: param1: Party-id
  ("game_event_undetect_party",
    [
        (store_script_param_1, ":party_id"),
        (try_begin),
          (party_slot_eq, ":party_id", slot_party_type, spt_kingdom_hero_party),
          (party_stack_get_troop_id, ":leader", ":party_id", 0),
          (is_between, ":leader", kingdom_heroes_begin, kingdom_heroes_end),
          (call_script, "script_update_troop_location_notes", ":leader", 0),
        (try_end),
  ]),

  #script_game_get_statistics_line:
  # This script is called from the game engine when statistics page is opened.
  # INPUT:
  # param1: line_no
  ("game_get_statistics_line",
    [
      (store_script_param_1, ":line_no"),
      (try_begin),
        (eq, ":line_no", 0),
        (get_player_agent_kill_count, reg1),
		(str_store_string, s1, "str_number_of_troops_killed_reg1"),
        (set_result_string, s1),
      (else_try),
        (eq, ":line_no", 1),
        (get_player_agent_kill_count, reg1, 1),
        (str_store_string, s1, "str_number_of_troops_wounded_reg1"),
        (set_result_string, s1),
      (else_try),
        (eq, ":line_no", 2),
        (get_player_agent_own_troop_kill_count, reg1),
        (str_store_string, s1, "str_number_of_own_troops_killed_reg1"),
        (set_result_string, s1),
      (else_try),
        (eq, ":line_no", 3),
        (get_player_agent_own_troop_kill_count, reg1, 1),
        (str_store_string, s1, "str_number_of_own_troops_wounded_reg1"),
        (set_result_string, s1),
      (else_try),
        (eq, ":line_no", 4), # test!!
        (get_player_agent_own_troop_kill_count, reg1, 1),
		(str_store_string, s1, "@Hey it seems that more stuff can be put here!!! (on multiple lines too) -- mtarini"),
        (set_result_string, s1),
      (else_try),
        (eq, ":line_no", 5), # test!!
        (get_player_agent_own_troop_kill_count, reg1, 1),
		(str_store_string, s1, "@So let's think of something worth keeping track of!"),
        (set_result_string, s1),
     (try_end),
  ]),

  #script_game_get_date_text:
  # This script is called from the game engine when the date needs to be displayed.
  # INPUT: arg1 = number of days passed since the beginning of the game
  # OUTPUT: result string = date
  # TLD: used Steward's Reckoning!!! -- mtarini
  ("game_get_date_text",
    [
      (store_script_param_2, ":num_hours"),
      (store_div, ":num_days", ":num_hours", 24),
      (store_add, ":cur_day", ":num_days", 15),
      (assign, ":cur_month", 7),
      (assign, ":cur_year", 3018), # -- osgiliat conquered by mordor in 3018 -- mtarini
      (assign, ":try_range", 99999),
      (try_for_range, ":unused", 0, ":try_range"),
        (try_begin),
		   # the 5 "one day months"
          (this_or_next|eq, ":cur_month", 1),
          (this_or_next|eq, ":cur_month", 5),
          (this_or_next|eq, ":cur_month", 9),
          (this_or_next|eq, ":cur_month",13),
          (eq,              ":cur_month",17),
          (assign, ":month_day_limit", 1),
        (else_try),
		  # normal othor months have 30 days
          (assign, ":month_day_limit", 30),
        (try_end),
        (try_begin),
          (gt, ":cur_day", ":month_day_limit"),
          (val_sub, ":cur_day", ":month_day_limit"),
          (val_add, ":cur_month", 1),
          (try_begin),
            (gt, ":cur_month", 17),
            (val_sub, ":cur_month", 17),
            (val_add, ":cur_year", 1),
          (try_end),
        (else_try),
          (assign, ":try_range", 0),
        (try_end),
      (try_end),
      (assign, reg1, ":cur_day"),
      (assign, reg2, ":cur_year"),
      (try_begin),(eq, ":cur_month", 1), (str_store_string, s1,   "str_calendar_spec_day_1"),
      (else_try) ,(eq, ":cur_month", 2), (str_store_string, s1, "str_january_reg1_reg2"),
      (else_try) ,(eq, ":cur_month", 3), (str_store_string, s1, "str_february_reg1_reg2"),
      (else_try) ,(eq, ":cur_month", 4), (str_store_string, s1, "str_march_reg1_reg2"),
      (else_try) ,(eq, ":cur_month", 5), (str_store_string, s1,   "str_calendar_spec_day_2"),
      (else_try) ,(eq, ":cur_month", 6), (str_store_string, s1, "str_april_reg1_reg2"),
      (else_try) ,(eq, ":cur_month", 7), (str_store_string, s1, "str_may_reg1_reg2"),
      (else_try) ,(eq, ":cur_month", 8), (str_store_string, s1, "str_june_reg1_reg2"),
      (else_try) ,(eq, ":cur_month", 9), (str_store_string, s1,   "str_calendar_spec_day_3"),
      (else_try) ,(eq, ":cur_month",10), (str_store_string, s1, "str_july_reg1_reg2"),
      (else_try) ,(eq, ":cur_month",11), (str_store_string, s1, "str_august_reg1_reg2"),
      (else_try) ,(eq, ":cur_month",12), (str_store_string, s1, "str_september_reg1_reg2"),
      (else_try) ,(eq, ":cur_month",13), (str_store_string, s1,   "str_calendar_spec_day_4"),
      (else_try) ,(eq, ":cur_month",14), (str_store_string, s1, "str_october_reg1_reg2"),
      (else_try) ,(eq, ":cur_month",15), (str_store_string, s1, "str_november_reg1_reg2"),
      (else_try) ,(eq, ":cur_month",16), (str_store_string, s1, "str_december_reg1_reg2"),
      (else_try) ,(eq, ":cur_month",17), (str_store_string, s1,   "str_calendar_spec_day_5"),
      (try_end),
      (set_result_string, s1),
    ]),  
  
  #script_game_get_money_text:
  # This script is called from the game engine when an amount of money needs to be displayed.
  # INPUT: arg1 = amount in units
  # OUTPUT: result string = money in text
  ("game_get_money_text",
    [ 
	  (store_script_param_1, ":amount"),
	  (str_store_faction_name, s2, "$ambient_faction"),
      (try_begin),
        (eq, ":amount", 1),
		(str_store_string, s1, "@1 Res.Pts ({s2})"),
        #(str_store_string, s1, "str_1_denar"),
      (else_try),
        (assign, reg1, ":amount"),
		(str_store_string, s1, "@{reg1} Res.Pts ({s2})"),
        #(str_store_string, s1, "str_reg1_denars"),
      (try_end),
      (set_result_string, s1),
  ]),

  #script_game_get_party_companion_limit:
  # This script is called from the game engine when the companion limit is needed for a party.
  # INPUT: arg1 = none
  # OUTPUT: reg0 = companion_limit
  ("game_get_party_companion_limit",
    [
      (assign, ":troop_no", "trp_player"),

      (assign, ":limit", 10),
      (store_skill_level, ":skill", "skl_leadership", ":troop_no"),
      (store_attribute_level, ":charisma", ":troop_no", ca_charisma),
      (val_mul, ":skill", 5),
      (val_add, ":limit", ":skill"),
      (val_add, ":limit", ":charisma"),

      (troop_get_slot, ":troop_renown", ":troop_no", slot_troop_renown),
      (store_div, ":renown_bonus", ":troop_renown", 25),
      (val_add, ":limit", ":renown_bonus"),

      (assign, reg0, ":limit"),
      (set_trigger_result, reg0),
  ]),


  ##  
  # script_get_party_tot_join_cost (mtarini)
  # Input: arg1 = party_no
  # Output: reg0 = total 
  ("get_party_total_join_cost",
    [
      (store_script_param_1, ":party_no"),
      (assign, ":total", 0),
      (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
        (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
        (call_script, "script_game_get_join_cost", ":stack_troop",0),
        (val_mul, reg0, ":stack_size"),
        (val_add, ":total", reg0),
      (try_end),
      (assign, reg0, ":total"),
      
	]),
	
  ##  
  # script_get_party_min_join_cost (mtarini)
  # Input: arg1 = party_no
  # Output: reg0 = returns party with minimal cost
  ("get_party_min_join_cost",
    [
      (store_script_param_1, ":party_no"),
      (assign, ":res", 9999999),
      (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
        (call_script, "script_game_get_join_cost", ":stack_troop",0),
        (val_min, ":res", reg0),
      (try_end),
      (assign, reg0, ":res"),
	]),
	
  ##  
  # script_get_party_max_ranking_slot(mtarini)
  # Input: arg1 = party_no
  # Output: reg0 = returns party slot with max cost
  ("get_party_max_ranking_slot",
    [
      (store_script_param_1, ":party_no"),
	  (assign, ":res", 0),
	  (assign, ":max", 0),
      (store_faction_of_party, ":pfac", ":party_no"),
      (party_get_slot, ":psubfac", ":party_no", slot_party_subfaction),
      (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
		(store_character_level, ":lvl", ":stack_troop"),
		(store_troop_faction, ":fac",  ":stack_troop"),
		(troop_get_slot, ":subfac", ":stack_troop", slot_troop_subfaction),
		(try_begin), (eq, ":fac", ":pfac"), (val_add,  ":lvl", 20), (try_end),  # bonus for same faction
		(try_begin), (eq, ":subfac", ":psubfac"), (val_add,  ":lvl", 20), (try_end), # bonus for same subfaction
		(try_begin),
			(lt, ":max", ":lvl"),
			(assign, ":max", ":lvl"),
			(assign, ":res", ":i_stack"),
		(try_end),
      (try_end),
      (assign, reg0, ":res"),
      
	]),

  ##  
  # script_party_split_by_faction (mtarini)
  # Input: arg1 = party_A, retains only the player and troops of given faction, except heroes
  # Input: arg2 = party_B, receives the rest, old A = new A + new B
  # Input: arg3 = faction
  ("party_split_by_faction",
    [
      (store_script_param_1, ":partyA"),
      (store_script_param_2, ":partyB"),
      (store_script_param, ":fac", 3),
      (party_get_num_companion_stacks, ":num_stacks", ":partyA"),
	  (party_clear, ":partyB"),
	  
      (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", ":partyA", ":i_stack"),
        (store_troop_faction, ":fac_t", ":stack_troop"),
		(this_or_next|troop_is_hero, ":stack_troop"),
		(neq, ":fac_t", ":fac"),
		(neq,  ":stack_troop", "$g_player_troop"), # player stays in A
        (party_stack_get_size,  ":stack_size",":partyA",":i_stack"),
        (party_remove_members, ":partyA", ":stack_troop",  ":stack_size"),
		(party_add_members, ":partyB", ":stack_troop",  ":stack_size"),
      (try_end),
	]),
	
  #script_game_reset_player_party_name:
  # This script is called from the game engine when the player name is changed.
  # INPUT: none
  # OUTPUT: none
  ("game_reset_player_party_name",
    [(str_store_troop_name, s5, "trp_player"),
     (party_set_name, "p_main_party", s5),
     ]),
  
  # script_party_get_ideal_size @used for NPC parties.
  # Input: arg1 = party_no
  # Output: reg0: ideal size 
  ("party_get_ideal_size",
    [ (store_script_param_1, ":party_no"),
      (assign, ":limit", 30),
      (try_begin),
        (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
        (party_stack_get_troop_id, ":party_leader", ":party_no", 0),
        (store_faction_of_party, ":faction_id", ":party_no"),
        (assign, ":limit", 10),

        (store_skill_level, ":skill", "skl_leadership", ":party_leader"),
        (store_attribute_level, ":charisma", ":party_leader", ca_charisma),
        (val_mul, ":skill", 5),
        (val_add, ":limit", ":skill"),
        (val_add, ":limit", ":charisma"),

        (troop_get_slot, ":troop_renown", ":party_leader", slot_troop_renown),
        (store_div, ":renown_bonus", ":troop_renown", 25),
        (val_add, ":limit", ":renown_bonus"),

        (try_begin),
          (faction_slot_eq, ":faction_id", slot_faction_leader, ":party_leader"),
          (val_add, ":limit", 100),
        (try_end),
      (try_end),
      (store_character_level, ":level", "trp_player"), #increase limits a little bit as the game progresses.
      (store_add, ":level_factor", 90, ":level"),
      (val_mul, ":limit", ":level_factor"),
      (val_div, ":limit", 90),
      (assign, reg0, ":limit"),
  ]),


  #script_game_get_party_prisoner_limit:
  # This script is called from the game engine when the prisoner limit is needed for a party.
  # INPUT: arg1 = party_no
  # OUTPUT: reg0 = prisoner_limit
  ("game_get_party_prisoner_limit",
    [
#      (store_script_param_1, ":party_no"),
      (assign, ":troop_no", "trp_player"),

      (assign, ":limit", 0),
      (store_skill_level, ":skill", "skl_prisoner_management", ":troop_no"),
      (store_mul, ":limit", ":skill", 5),
      (assign, reg0, ":limit"),
      (set_trigger_result, reg0),
  ]),

  #script_game_get_item_extra_text:
  # This script is called from the game engine when an item's properties are displayed.
  # INPUT: arg1 = item_no, arg2 = extra_text_id (this can be between 0-7 (7 included)), arg3 = item_modifier
  # OUTPUT: result_string = item extra text, trigger_result = text color (0 for default)
  ("game_get_item_extra_text",
    [ (store_script_param, ":item_no", 1),
      (store_script_param, ":extra_text_id", 2),
      (store_script_param, ":item_modifier", 3),
	  #(item_get_type,":itp", ":item_no"),
      (try_begin),
		(eq,":item_no","itm_rohan_saddle"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Riding Skill"),(try_end),
		(try_begin),(eq, ":extra_text_id", 1),(set_result_string, "@+1 to Horse Archery"),(try_end),
        (set_trigger_result, 0xFFEEDD),
      (else_try),
		(eq,":item_no","itm_map"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Pathfinding"),(try_end),
        (set_trigger_result, 0xFFEEDD),
      (else_try),
		(eq,":item_no","itm_orc_brew"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+5 to Wound Treatement"),(set_trigger_result, 0xFFEEDD),(try_end),
		#(try_begin),(eq, ":extra_text_id", 1),(set_result_string, "@Not Used"),(set_trigger_result, 0xAAAAAA),(try_end),
		#(try_begin),(eq, ":extra_text_id", 2),(set_result_string, "@Camp Menu"),(set_trigger_result, 0xAAAAAA),(try_end),
      (else_try),
		(eq,":item_no","itm_ent_water"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@Use from"),(try_end),
		(try_begin),(eq, ":extra_text_id", 1),(set_result_string, "@Camp Menu"),(try_end),
        (set_trigger_result, 0xAAAAAA),
      (else_try),
		#(store_and,reg20,":itp", itp_food), (neq, reg20,0),
		#(eq,":itp", itp_food), 
        (is_between, ":item_no", food_begin, food_end),
        (try_begin),
          (eq, ":extra_text_id", 0),
          (assign, ":continue", 1),
          (try_begin),
            (eq, ":item_no", "itm_cattle_meat"),
            (eq, ":item_modifier", imod_rotten),
            (assign, ":continue", 0),
          (try_end),
          (eq, ":continue", 1),
          (item_get_slot, ":food_bonus", ":item_no", slot_item_food_bonus),
          (assign, reg1, ":food_bonus"),
          (set_result_string, "@+{reg1} to party morale"),
          (set_trigger_result, 0x4444FF),
        (try_end),
      (try_end),
	  # debug item faction label, GA
		#(try_begin),
        #  (eq, ":extra_text_id", 4),
        #  (item_get_slot,reg1,":item_no",slot_item_subfaction),
        #  (set_result_string, "@[debug:{reg1}]"),
		#(try_end),
  ]),

  #script_game_on_disembark:
  # This script is called from the game engine when the player reaches the shore with a ship.
  # INPUT: pos0 = disembark position
  ("game_on_disembark",
   [(question_box,"@Do you want to disembark?"),
#   (jump_to_menu, "mnu_disembark"),
  ]),


  #script_game_context_menu_get_buttons:
  # This script is called from the game engine when the player clicks the right mouse button over a party on the map.
  # INPUT: arg1 = party_no
  # OUTPUT: none, fills the menu buttons
  ("game_context_menu_get_buttons",
   [(store_script_param, ":party_no", 1),
    (try_begin),
      (neq, ":party_no", "p_main_party"),
      (context_menu_add_item, "@Move here", cmenu_move),
    (try_end),
    (try_begin),
      (is_between, ":party_no", centers_begin, centers_end),
      (context_menu_add_item, "@View notes", 1),
    (else_try),
      (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
      (gt, ":num_stacks", 0),
      (party_stack_get_troop_id, ":troop_no", ":party_no", 0),
      (is_between, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
      (context_menu_add_item, "@View notes", 2),
    (try_end),
    #MV debug stuff
    (try_begin),
      (eq, cheat_switch, 1),
      (call_script, "script_party_calculate_strength", ":party_no", 0),
      (context_menu_add_item, "@Debug str: {reg0}", 3),
    (try_end),
  ]),

  #script_game_event_context_menu_button_clicked:
  # This script is called from the game engine when the player clicks on a button at the right mouse menu.
  # INPUT: arg1 = party_no, arg2 = button_value
  # OUTPUT: none
  ("game_event_context_menu_button_clicked",
   [(store_script_param, ":party_no", 1),
    (store_script_param, ":button_value", 2),
    (try_begin),
      (eq, ":button_value", 1),
      (change_screen_notes, 3, ":party_no"),
    (else_try),
      (eq, ":button_value", 2),
      (party_stack_get_troop_id, ":troop_no", ":party_no", 0),
      (change_screen_notes, 1, ":troop_no"),
    (try_end),
  ]),

  #script_game_get_skill_modifier_for_troop
  # This script is called from the game engine when a skill's modifiers are needed  
  #  Mtarini: added magic item effects
  # INPUT: arg1 = troop_no, arg2 = skill_no
  # OUTPUT: trigger_result = modifier_value
  ("game_get_skill_modifier_for_troop",
   [(store_script_param, ":troop_no", 1),
    (store_script_param, ":skill_no", 2),
    (assign, ":modifier_value", 0),
    (try_begin),
   	  (eq, ":skill_no", "skl_pathfinding"),
	  (call_script, "script_get_troop_item_amount", ":troop_no", "itm_map"),
	  (gt, reg0, 0),
      (val_add, ":modifier_value", 1),
	(else_try),
  	  (eq, ":skill_no", "skl_wound_treatment"),
	  (eq, ":troop_no", "trp_player"), # player only uses brew
	  (call_script, "script_get_troop_item_amount", ":troop_no", "itm_orc_brew"),
	  (gt, reg0, 0),
      (val_add, ":modifier_value", 5),	
	(else_try),
  	  (this_or_next|eq, ":skill_no", "skl_riding"),
  	  (eq, ":skill_no", "skl_horse_archery"),
	  (call_script, "script_get_troop_item_amount", ":troop_no", "itm_rohan_saddle"),
	  (gt, reg0, 0),
      (val_add, ":modifier_value", 1),
#    (else_try),
#      (eq, ":skill_no", "skl_trainer"),
#      (call_script, "script_get_troop_item_amount", ":troop_no", "itm_book_training_reference"),
#      (gt, reg0, 0),
#      (val_add, ":modifier_value", 1),
#    (else_try),
#      (eq, ":skill_no", "skl_surgery"),
#      (call_script, "script_get_troop_item_amount", ":troop_no", "itm_book_surgery_reference"),
#      (gt, reg0, 0),
#      (val_add, ":modifier_value", 1),
    (try_end),
    (set_trigger_result, ":modifier_value"),
    ]),

# Note to modders: Uncomment these if you'd like to use the following.
  
##  #script_game_check_party_sees_party
##  # This script is called from the game engine when a party is inside the range of another party
##  # INPUT: arg1 = party_no_seer, arg2 = party_no_seen
##  # OUTPUT: trigger_result = true or false (1 = true, 0 = false)
##  ("game_check_party_sees_party",
##   [
##     (store_script_param, ":party_no_seer", 1),
##     (store_script_param, ":party_no_seen", 2),
##     (set_trigger_result, 1),
##    ]),
##
##  #script_game_get_party_speed_multiplier
##  # This script is called from the game engine when a skill's modifiers are needed
##  # INPUT: arg1 = party_no
##  # OUTPUT: trigger_result = multiplier (scaled by 100, meaning that giving 100 as the trigger result does not change the party speed)
##  ("game_get_party_speed_multiplier",
##   [
##     (store_script_param, ":party_no", 1),
##     (set_trigger_result, 100),
##    ]),
  


  #script_setup_talk_info
  # INPUT: $g_talk_troop, $g_talk_troop_relation
  ("setup_talk_info",
    [
      (talk_info_set_relation_bar, "$g_talk_troop_relation"),
      (str_store_troop_name, s61, "$g_talk_troop"),
      (str_store_string, s61, "@ {s61}"),
      (assign, reg1, "$g_talk_troop_relation"),
      (str_store_string, s62, "str_relation_reg1"),
      (talk_info_set_line, 0, s61),
      (talk_info_set_line, 1, s62),
      (call_script, "script_describe_relation_to_s63", "$g_talk_troop_relation"),
      (talk_info_set_line, 3, s63),
  ]),

#NPC companion changes begin
  #script_setup_talk_info_companions
  ("setup_talk_info_companions",
    [
      (call_script, "script_npc_morale", "$g_talk_troop"),
      (assign, ":troop_morale", reg0),

      (talk_info_set_relation_bar, ":troop_morale"),

      (str_store_troop_name, s61, "$g_talk_troop"),
      (str_store_string, s61, "@ {s61}"),
      (assign, reg1, ":troop_morale"),
      (str_store_string, s62, "str_morale_reg1"),
      (talk_info_set_line, 0, s61),
      (talk_info_set_line, 1, s62),
      (talk_info_set_line, 3, s63),
  ]),
#NPC companion changes end

  #script_update_party_creation_random_limits
  # INPUT: none
  ("update_party_creation_random_limits",
    [
      (store_character_level, ":player_level", "trp_player"),
      (store_mul, ":upper_limit", ":player_level", 3),
      (val_add, ":upper_limit", 25),
      (val_min, ":upper_limit", 100),
      (set_party_creation_random_limits, 0, ":upper_limit"),
      (assign, reg0, ":upper_limit"),
  ]),

  #script_set_trade_route_between_centers
  # INPUT:
  # param1: center_no_1
  # param1: center_no_2
  ("set_trade_route_between_centers",
    [(store_script_param, ":center_no_1", 1),
     (store_script_param, ":center_no_2", 2),
     (assign, ":center_1_added", 0),
     (assign, ":center_2_added", 0),
     (try_for_range, ":cur_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
       (try_begin),
         (eq, ":center_1_added", 0),
         (party_slot_eq, ":center_no_1", ":cur_slot", 0),
         (party_set_slot, ":center_no_1", ":cur_slot", ":center_no_2"),
         (assign, ":center_1_added", 1),
       (try_end),
       (try_begin),
         (eq, ":center_2_added", 0),
         (party_slot_eq, ":center_no_2", ":cur_slot", 0),
         (party_set_slot, ":center_no_2", ":cur_slot", ":center_no_1"),
         (assign, ":center_2_added", 1),
       (try_end),
     (try_end),
     (try_begin),
       (eq, ":center_1_added", 0),
       (str_store_party_name, s1, ":center_no_1"),
       (display_message, "@ERROR: More than 15 trade routes are given for {s1}."),
     (try_end),
     (try_begin),
       (eq, ":center_2_added", 0),
       (str_store_party_name, s1, ":center_no_2"),
       (display_message, "@ERROR: More than 15 trade routes are given for {s1}."),
     (try_end),
     ]),

  #script_center_change_trade_good_production
  # INPUT:
  # param1: center_no
  # param2: item_id
  # param3: production_rate (should be between -100 (for net consumption) and 100 (for net production)
  # param4: randomness (between 0-100)
  ("center_change_trade_good_production",
    [
      (store_script_param, ":center_no", 1),
      (store_script_param, ":item_no", 2),
      (store_script_param, ":production_rate", 3),
#      (val_mul, ":production_rate", 5),
      (store_script_param, ":randomness", 4),
      (store_random_in_range, ":random_num", 0, ":randomness"),
      (store_random_in_range, ":random_sign", 0, 2),
      (try_begin),
        (eq, ":random_sign", 0),
        (val_add, ":production_rate", ":random_num"),
      (else_try),
        (val_sub, ":production_rate", ":random_num"),
      (try_end),
      (val_sub, ":item_no", trade_goods_begin),
      (val_add, ":item_no", slot_town_trade_good_productions_begin),

      (party_get_slot, ":old_production_rate", ":center_no", ":item_no"),
      (val_add, ":production_rate", ":old_production_rate"),
      (party_set_slot, ":center_no", ":item_no", ":production_rate"),
  ]),
  
  #script_average_trade_good_productions
  # INPUT: none
  ("average_trade_good_productions",
    [
      (store_sub, ":item_to_slot", slot_town_trade_good_productions_begin, trade_goods_begin),
#      (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
      (try_for_range, ":center_no", towns_begin, towns_end),
        (this_or_next|is_between, ":center_no", towns_begin, towns_end),
        (is_between, ":center_no", villages_begin, villages_end),
        (try_for_range, ":other_center", centers_begin, centers_end),
          (party_is_active, ":other_center"), #TLD
          (this_or_next|is_between, ":center_no", towns_begin, towns_end),
          (is_between, ":center_no", villages_begin, villages_end),
          (neq, ":other_center", ":center_no"),
          (store_distance_to_party_from_party, ":cur_distance", ":center_no", ":other_center"),
          (lt, ":cur_distance", 110),
          (store_sub, ":dist_factor", 110, ":cur_distance"),
          (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
            (store_add, ":cur_good_slot", ":cur_good", ":item_to_slot"),
            (party_get_slot, ":center_production", ":center_no", ":cur_good_slot"),
            (party_get_slot, ":other_center_production", ":other_center", ":cur_good_slot"),
            (store_sub, ":prod_dif", ":center_production", ":other_center_production"),
            (gt, ":prod_dif", 0),
            (store_mul, ":prod_dif_change", ":prod_dif", 1),
##            (try_begin),
##              (is_between, ":center_no", towns_begin, towns_end),
##              (is_between, ":other_center", towns_begin, towns_end),
##              (val_mul, ":cur_distance", 2),
##            (try_end),
            (val_mul ,":prod_dif_change", ":dist_factor"),
            (val_div ,":prod_dif_change", 110),
            (val_add, ":other_center_production", ":prod_dif_change"),
            (party_set_slot, ":other_center", ":cur_good_slot", ":other_center_production"),
          (try_end),
        (try_end),
      (try_end),
  ]),
  
  #script_normalize_trade_good_productions
  # INPUT: none
  ("normalize_trade_good_productions",
    [
      (store_sub, ":item_to_slot", slot_town_trade_good_productions_begin, trade_goods_begin),
      (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
        (assign, ":total_production", 0),
        (assign, ":num_centers", 0),
        (store_add, ":cur_good_slot", ":cur_good", ":item_to_slot"),
        (try_for_range, ":center_no", centers_begin, centers_end),
          (party_is_active, ":center_no"), #TLD
          (val_add, ":num_centers", 1),
          (try_begin),
            (is_between, ":center_no", towns_begin, towns_end), #each town is weighted as 5 villages...
            (val_add, ":num_centers", 4), 
          (try_end),
          (party_get_slot, ":center_production", ":center_no", ":cur_good_slot"),
          (val_add, ":total_production", ":center_production"),
        (try_end),
        (store_div, ":new_production_difference", ":total_production", ":num_centers"),
        (neq, ":new_production_difference", 0),
        (try_for_range, ":center_no", centers_begin, centers_end),
          (party_is_active, ":center_no"), #TLD
          (this_or_next|is_between, ":center_no", towns_begin, towns_end),
          (is_between, ":center_no", villages_begin, villages_end),
          (party_get_slot, ":center_production", ":center_no", ":cur_good_slot"),
          (val_sub, ":center_production", ":new_production_difference"),
          (party_set_slot, ":center_no", ":cur_good_slot", ":center_production"),
        (try_end),
      (try_end),
  ]),
  
  #script_update_trade_good_prices
  # INPUT: none
  ("update_trade_good_prices",
    [
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
        (this_or_next|is_between, ":center_no", towns_begin, towns_end),
        (is_between, ":center_no", villages_begin, villages_end),
        (call_script, "script_update_trade_good_price_for_party", ":center_no"),
      (try_end),
#      (call_script, "script_update_trade_good_price_for_party", "p_zendar"),
#      (call_script, "script_update_trade_good_price_for_party", "p_salt_mine"),
#      (call_script, "script_update_trade_good_price_for_party", "p_four_ways_inn"),
  ]),

  #script_update_trade_good_price_for_party
  # INPUT: arg1 = party_no
  ("update_trade_good_price_for_party",
    [
      (store_script_param, ":center_no", 1),
      (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
        (store_sub, ":cur_good_slot", ":cur_good", trade_goods_begin),
        (val_add, ":cur_good_slot", slot_town_trade_good_productions_begin),
        (store_sub, ":cur_good_price_slot", ":cur_good", trade_goods_begin),
        (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
        (party_get_slot, ":production", ":center_no", ":cur_good_slot"),
        (party_get_slot, ":cur_price", ":center_no", ":cur_good_price_slot"),
        (try_begin),
          (lt, ":production", 0), #demand is greater than supply
          (store_mul, ":change_factor", ":production", -3), #price will be increased by his factor
        (else_try),
          (store_mul, ":change_factor", ":production", 3), #price will be decreased by this factor
        (try_end),
#        (val_mul, ":change_factor", 2),
        (store_random_in_range, ":random_change", 0, ":change_factor"),
        (try_begin),
          (lt, ":production", 0), #demand is greater than supply
          (val_add, ":cur_price", ":random_change"),
        (else_try),
          (val_sub, ":cur_price", ":random_change"),
        (try_end),
        #Move price towards average by 2%...
        (store_sub, ":price_difference", ":cur_price", average_price_factor),
        (val_mul, ":price_difference", 97),
        (val_div, ":price_difference", 100),
        (store_add, ":new_price", average_price_factor, ":price_difference"),
        (val_clamp, ":new_price", minimum_price_factor, maximum_price_factor),
        (party_set_slot, ":center_no", ":cur_good_price_slot", ":new_price"),
      (try_end),
  ]),  
  
  #script_do_merchant_town_trade
  # INPUT: arg1 = party_no (of the merchant), arg2 = center_no
  ("do_merchant_town_trade",
    [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":center_no"),
      (call_script, "script_do_party_center_trade", ":party_no", ":center_no", 20), #change prices by 20%
      
      (assign, ":total_change", reg0),
      #Adding the earnings to the wealth (maximum changed price is the earning)
      (val_div, ":total_change", 2),
      (str_store_party_name, s1, ":party_no"),
      (str_store_party_name, s2, ":center_no"),
      (assign, reg1, ":total_change"),
##      (try_begin),
##        (eq, "$cheat_mode", 1),
##        (display_message, "@Merchant {s1} traded with {s2} and earned {reg1} denars."),
##      (try_end),

      #Adding tax revenue to the center
      (party_get_slot, ":accumulated_tariffs", ":center_no", slot_center_accumulated_tariffs),
      (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
      (store_add, ":tax_gain", ":prosperity", 10),
      (val_mul, ":tax_gain", ":total_change"),
      (val_div, ":tax_gain", 2200), #(10 + prosperity) / 110 * 5% of the merchant's revenue.
      (val_add, ":accumulated_tariffs", ":tax_gain"),
      (party_set_slot, ":center_no", slot_center_accumulated_tariffs, ":accumulated_tariffs"),
      
#      (try_begin),
#        (is_between, ":center_no", towns_begin, towns_end),
#        (party_get_slot, ":merchant",":center_no",slot_town_merchant),
#        (gt, ":merchant", 0),
#        (store_mul, ":merchant_profit", ":total_change", 1),
#        (val_div, ":merchant_profit", 2),
#        (troop_add_gold, ":merchant", ":merchant_profit"),
#      (try_end),

      #Adding 1 to center prosperity
      (try_begin),
        (store_random_in_range, ":rand", 0, 100),
        (lt, ":rand", 35),
        (call_script, "script_change_center_prosperity", ":center_no", 1),
      (try_end),
      
  ]),
  
  #script_party_calculate_regular_strength:
  # INPUT:
  # param1: Party-id
  ("party_calculate_regular_strength",
    [
      (store_script_param_1, ":party"), #Party_id
      
      (assign, reg(0),0),
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party",":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (store_character_level, ":stack_strength", ":stack_troop"),
        (val_add, ":stack_strength", 12),
        (val_mul, ":stack_strength", ":stack_strength"),
        (val_div, ":stack_strength", 100),
        (party_stack_get_size, ":stack_size",":party",":i_stack"),
        (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
        (val_sub, ":stack_size", ":num_wounded"),
        (val_mul, ":stack_strength", ":stack_size"),
        (val_add,reg(0), ":stack_strength"),
      (try_end),
  ]),
  
  
  
  
  #script_party_calculate_strength:
  # INPUT: arg1 = party_id, arg2 = exclude leader
  # OUTPUT: reg0 = strength
  ("party_calculate_strength",
    [
      (store_script_param_1, ":party"), #Party_id
      (store_script_param_2, ":exclude_leader"), #Party_id
      
      (assign, reg(0),0),
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, ":first_stack", 0),
      (try_begin),
        (neq, ":exclude_leader", 0),
        (assign, ":first_stack", 1),
      (try_end),
      (try_for_range, ":i_stack", ":first_stack", ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":party",":i_stack"),
        (store_character_level, ":stack_strength", ":stack_troop"),
        (val_add, ":stack_strength", 12),
        (val_mul, ":stack_strength", ":stack_strength"),
        (val_div, ":stack_strength", 100),
        (try_begin),
          (neg|troop_is_hero, ":stack_troop"),
          (party_stack_get_size, ":stack_size",":party",":i_stack"),
          (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
          (val_sub, ":stack_size", ":num_wounded"),
          (val_mul, ":stack_strength", ":stack_size"),
        (else_try),
          (troop_is_wounded, ":stack_troop"), #hero...
          (assign,":stack_strength",0),
        (try_end),
        (val_add,reg(0), ":stack_strength"),
      (try_end),
      (party_set_slot, ":party", slot_party_cached_strength, reg(0)),
  ]),


  #script_loot_player_items:
  # INPUT: arg1 = enemy_party_no
  # Output: none
  ("loot_player_items",
    [
      (store_script_param, ":enemy_party_no", 1),
      
      (troop_get_inventory_capacity, ":inv_cap", "trp_player"),
      (try_for_range, ":i_slot", 0, ":inv_cap"),
        (troop_get_inventory_slot, ":item_id", "trp_player", ":i_slot"),
        (ge, ":item_id", 0),
        (troop_get_inventory_slot_modifier, ":item_modifier", "trp_player", ":i_slot"),
# all items looted with max probability. No easy life :) GA
#        (try_begin),
#          (is_between, ":item_id", trade_goods_begin, trade_goods_end),
          (assign, ":randomness", 20),
#        (else_try),
#          (is_between, ":item_id", horses_begin, horses_end),
#          (assign, ":randomness", 15),
#        (else_try),
#          (this_or_next|is_between, ":item_id", weapons_begin, weapons_end),
#          (is_between, ":item_id", ranged_weapons_begin, ranged_weapons_end),
#          (assign, ":randomness", 5),
#        (else_try),
#          (this_or_next|is_between, ":item_id", armors_begin, armors_end),
#          (is_between, ":item_id", shields_begin, shields_end),
#          (assign, ":randomness", 5),
#        (try_end),
        (store_random_in_range, ":random_no", 0, 100),
        (lt, ":random_no", ":randomness"),
        (troop_remove_item, "trp_player", ":item_id"),

        (try_begin),
          (gt, ":enemy_party_no", 0),
          (party_get_slot, ":cur_loot_slot", ":enemy_party_no", slot_party_next_looted_item_slot),
          (val_add, ":cur_loot_slot", slot_party_looted_item_1),
          (party_set_slot, ":enemy_party_no", ":cur_loot_slot", ":item_id"),
          (val_sub, ":cur_loot_slot", slot_party_looted_item_1),
          (val_add, ":cur_loot_slot", slot_party_looted_item_1_modifier),
          (party_set_slot, ":enemy_party_no", ":cur_loot_slot", ":item_modifier"),
          (val_sub, ":cur_loot_slot", slot_party_looted_item_1_modifier),
          (val_add, ":cur_loot_slot", 1),
          (val_mod, ":cur_loot_slot", num_party_loot_slots),
          (party_set_slot, ":enemy_party_no", slot_party_next_looted_item_slot, ":cur_loot_slot"),
        (try_end),
      (try_end),
      (store_troop_gold, ":cur_gold", "trp_player"),
      (store_div, ":max_lost", ":cur_gold", 4),
      (store_div, ":min_lost", ":cur_gold", 10),
      (store_random_in_range, ":lost_gold", ":min_lost", ":max_lost"),
      (troop_remove_gold, "trp_player", ":lost_gold"),
      ]),

  
  #script_party_calculate_loot:
  # INPUT: param1: Party-id
  # Returns num looted items in reg(0)
  ("party_calculate_loot",
    [
      (store_script_param_1, ":enemy_party"), #Enemy Party_id
      
	  (call_script,"script_get_faction_mask","$players_kingdom"),(assign,":faction_mask",reg30),
	  
      (call_script, "script_calculate_main_party_shares"),(assign, ":num_player_party_shares", reg0),
      #      (assign, ":num_ally_shares", reg1),
      #      (store_add, ":num_shares",  ":num_player_party_shares", ":num_ally_shares"),
      
      #Calculate player loot probability
      #      (assign, ":loot_probability", 100),
      #      (val_mul, ":loot_probability", 10),
      #      (val_div, ":loot_probability", ":num_shares"),

	  (assign, ":can_steal", 1),  # can steal objects of own faction or , of no faction
	  (try_begin), (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good), (assign, ":can_steal", 0),(try_end), # good guys don't steal
      # Loot the defeated party
      (store_mul, ":loot_probability", player_loot_share, 3),
      (val_mul, ":loot_probability", "$g_strength_contribution_of_player"),
      (party_get_skill_level, ":player_party_looting", "p_main_party", "skl_looting"),
      (val_add, ":player_party_looting", 10),
      (val_mul, ":loot_probability", ":player_party_looting"),
      (val_div, ":loot_probability", 10),
      (val_div, ":loot_probability", ":num_player_party_shares"),

	  (assign, ":dest", "trp_temp_troop"), (try_begin),(eq,"$g_crossdressing_activated", 0),(assign, ":dest", "trp_temp_troop_2"),(try_end),
	  (troop_clear_inventory,"trp_temp_troop_2"),
	  (troop_clear_inventory,"trp_temp_troop"),

      (party_get_num_companion_stacks, ":num_stacks",":enemy_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":enemy_party",":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size, ":stack_size",":enemy_party",":i_stack"),
        (try_for_range, ":unused", 0, ":stack_size"),
          (troop_loot_troop,":dest",":stack_troop",":loot_probability"),
        (try_end),
      (try_end),

	  # substitute forbidden items  with "metal scraps" 
	  (try_begin),
		(eq,"$g_crossdressing_activated", 0),
		(troop_get_inventory_capacity, ":inv_cap", "trp_temp_troop_2"),
		
		(try_for_range, ":i_slot", 0, ":inv_cap"),
			(troop_get_inventory_slot, ":item_id", "trp_temp_troop_2", ":i_slot"),
			(ge, ":item_id", 0),
			(try_begin),
				(item_get_type, ":it", ":item_id"),
				(eq, ":it", itp_type_horse),
				(try_begin),
					(troop_get_type, ":race","$g_player_troop"),
					(is_between, ":race", tf_orc_begin, tf_orc_end), # orcs:
					(try_begin),
						(is_between, ":item_id", item_warg_begin , item_warg_end),
						(troop_add_item, "trp_temp_troop", ":item_id"), # keep any warg
					(else_try),
						(troop_add_item, "trp_temp_troop", "itm_horse_meat"), # turn any horse in meat
					(try_end),
				(else_try),
					# non orcs: 
					(try_begin),
						(is_between, ":item_id", item_warg_begin , item_warg_end), # trash any warg
					(else_try),
						(troop_add_item, "trp_temp_troop", ":item_id"), # keep any horse
					(try_end),
				(try_end),
			(else_try),
				(eq, ":can_steal", 1), # if can steal...
				(item_get_slot, reg10,  ":item_id", slot_item_faction),
				(store_and, reg11, reg10, ":faction_mask"),
				(this_or_next|eq, reg10, 0), # can steal objects with no faction
				(neq, reg11, 0), # can steal objects of player's faction
				# don't replace item
				(troop_add_item, "trp_temp_troop", ":item_id"),
			(else_try),
				# replace item with scrap
				(store_random_in_range, ":rand", 0, 100), (ge, ":rand", 75),
				(store_item_value, ":val", ":item_id"),
				(try_begin), (ge,":val",150), (troop_add_item, "trp_temp_troop", "itm_metal_scraps_good"),
				(else_try), (ge,":val",30), (troop_add_item, "trp_temp_troop", "itm_metal_scraps_medium"),
				(else_try), (ge,":val",5), (troop_add_item, "trp_temp_troop", "itm_metal_scraps_bad"),
				(try_end),
			(try_end),	  
		(try_end),	  
      (try_end),	  
	  
	  # adding any special loot from party "looted item" slots (item that where stolen by the party)
      (try_for_range, ":i_loot", 0, num_party_loot_slots),
        (store_add, ":cur_loot_slot", ":i_loot", slot_party_looted_item_1),
        (party_get_slot, ":item_no", "$g_enemy_party", ":cur_loot_slot"),
        (gt, ":item_no", 0),
        (party_set_slot, "$g_enemy_party", ":cur_loot_slot", 0),
        (val_sub, ":cur_loot_slot", slot_party_looted_item_1),
        (val_add, ":cur_loot_slot", slot_party_looted_item_1_modifier),
        (party_get_slot, ":item_modifier", "$g_enemy_party", ":cur_loot_slot"),
        (troop_add_item, "trp_temp_troop", ":item_no", ":item_modifier"),
      (try_end),
      (party_set_slot, "$g_enemy_party", slot_party_next_looted_item_slot, 0),

	  # put "goods" in loot if it was a caravan (or farmers)
      (assign, ":num_looted_items",0),
      (try_begin),
        (this_or_next|party_slot_eq, "$g_enemy_party", slot_party_type, spt_kingdom_caravan),
        (party_slot_eq, "$g_enemy_party", slot_party_type, spt_village_farmer),
        (store_mul, ":plunder_amount", player_loot_share, 30),
        (val_mul, ":plunder_amount", "$g_strength_contribution_of_player"),
        (val_div, ":plunder_amount", 100),
        (val_div, ":plunder_amount", ":num_player_party_shares"),
        (try_begin),
          (party_slot_eq, "$g_enemy_party", slot_party_type, spt_kingdom_caravan),
		   #  (val_clamp, ":plunder_amount", 1, 50),
          (reset_item_probabilities, 100),
          (assign, ":range_min", trade_goods_begin),
          (assign, ":range_max", trade_goods_end),
        (else_try),
          (val_div, ":plunder_amount", 5),
		  #(val_clamp, ":plunder_amount", 1, 10),
          (reset_item_probabilities, 1),
          (assign, ":range_min", normal_food_begin),
          (assign, ":range_max", food_end),
        (try_end),
        (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
        (try_for_range, ":cur_goods", ":range_min", ":range_max"),
          (store_add, ":cur_price_slot", ":cur_goods", ":item_to_price_slot"),
          (party_get_slot, ":cur_price", "$g_enemy_party", ":cur_price_slot"),
          (assign, ":cur_probability", 100),
          (val_mul, ":cur_probability", average_price_factor),
          (val_div, ":cur_probability", ":cur_price"),
          (val_mul, ":cur_probability", average_price_factor),
          (val_div, ":cur_probability", ":cur_price"),
          (val_mul, ":cur_probability", average_price_factor),
          (val_div, ":cur_probability", ":cur_price"),
          #(assign, reg0, ":cur_probability"),
          (set_item_probability_in_merchandise, ":cur_goods", ":cur_probability"),
        (try_end),
        (troop_add_merchandise, "trp_temp_troop", itp_type_goods, ":plunder_amount"),
        #(assign, reg5, ":plunder_amount"),
        (val_add, ":num_looted_items", ":plunder_amount"),
      (try_end),
      	  
	  # count how many objects were accumulated in total
      (troop_get_inventory_capacity, ":inv_cap", "trp_temp_troop"),
      (try_for_range, ":i_slot", 0, ":inv_cap"),
        (troop_get_inventory_slot, ":item_id", "trp_temp_troop", ":i_slot"),
        (ge, ":item_id", 0),
        (val_add, ":num_looted_items",1),
      (try_end),

      (assign, reg0, ":num_looted_items"),
  ]),
  
  #script_calculate_main_party_shares:
  # Returns number of player party shares in reg0
  ("calculate_main_party_shares",
    [
      (assign, ":num_player_party_shares",player_loot_share),
      # Add shares for player's party
      (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
      (try_for_range, ":i_stack", 1, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop","p_main_party",":i_stack"),
        (try_begin),
          (neg|troop_is_hero, ":stack_troop"),
          (party_stack_get_size, ":stack_size","p_main_party",":i_stack"),
          (val_add, ":num_player_party_shares", ":stack_size"),
        (else_try),
          (val_add, ":num_player_party_shares", hero_loot_share),
        (try_end),
      (try_end),
      
      (assign, reg0, ":num_player_party_shares"),
  ]),
  
  #script_party_give_xp_and_gold:
  # INPUT: param1: destroyed Party-id
  # calculates and gives player paty's share of gold and xp.
  ("party_give_xp_and_gold",
    [
      (store_script_param_1, ":enemy_party"), #Party_id
      
      (call_script, "script_calculate_main_party_shares"),
      (assign, ":num_player_party_shares", reg0),
      
      #      (assign, ":num_ally_shares", reg1),
      #     (store_add, ":num_total_shares",  ":num_player_party_shares", ":num_ally_shares"),
      
      (assign, ":total_gain", 0),
      (party_get_num_companion_stacks, ":num_stacks",":enemy_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":enemy_party",":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size, ":stack_size",":enemy_party",":i_stack"),
        (store_character_level, ":level", ":stack_troop"),
        (store_add, ":gain", ":level", 10),
        (val_mul, ":gain", ":gain"),
        (val_div, ":gain", 10),
        (store_mul, ":stack_gain", ":gain", ":stack_size"),
        (val_add, ":total_gain", ":stack_gain"),
      (try_end),
      
      (val_mul, ":total_gain", "$g_strength_contribution_of_player"),
      (val_div, ":total_gain", 100),
      (val_min, ":total_gain", 40000), #eliminate negative results
      #      (store_mul, ":player_party_xp_gain", ":total_gain", ":num_player_party_shares"),
      #      (val_div, ":player_party_xp_gain", ":num_total_shares"),
      (assign, ":player_party_xp_gain", ":total_gain"),
      
      (store_random_in_range, ":r", 50, 100),
      (val_mul, ":player_party_xp_gain", ":r"),
      (val_div, ":player_party_xp_gain", 100),
      
      (party_add_xp, "p_main_party", ":player_party_xp_gain"),
      
      (store_mul, ":player_gold_gain", ":total_gain", player_loot_share),
      (val_min, ":player_gold_gain", 60000), #eliminate negative results
      (store_random_in_range, ":r", 50, 100),
      (val_mul, ":player_gold_gain", ":r"),
      (val_div, ":player_gold_gain", 100),
      (val_div, ":player_gold_gain", ":num_player_party_shares"),
      
      #add gold now
      (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop","p_main_party",":i_stack"),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (call_script, "script_troop_add_gold", ":stack_troop", ":player_gold_gain"),
        (try_end),
      (try_end),
   #Add morale
      (assign, ":morale_gain", ":total_gain"),
      (val_div, ":morale_gain", ":num_player_party_shares"),
      (call_script, "script_change_player_party_morale", ":morale_gain"),
  ]),
  
  
  #script_setup_troop_meeting:
  # INPUT: param1: troop_id with which meeting will be made, param2: troop_dna (optional)
  ("setup_troop_meeting",
    [
      (store_script_param_1, ":meeting_troop"),
      (store_script_param_2, ":troop_dna"),
      (modify_visitors_at_site,"scn_conversation_scene"),(reset_visitors),
      (set_visitor,0,"trp_player"),
      #       (party_stack_get_troop_dna,":troop_dna",":meeting_party",0),
      (set_visitor,17,":meeting_troop",":troop_dna"),
      (set_jump_mission,"mt_conversation_encounter"),
      (jump_to_scene,"scn_conversation_scene"),
      (change_screen_map_conversation, ":meeting_troop"),
  ]),
  
  #script_setup_party_meeting:
  # INPUT: param1: Party-id with which meeting will be made.
  ("setup_party_meeting",
    [
      (store_script_param_1, ":meeting_party"),
      (try_begin),
        (lt, "$g_encountered_party_relation", 0), #hostile
#        (call_script, "script_music_set_situation_with_culture", mtf_sit_encounter_hostile),
      (try_end),
      (modify_visitors_at_site,"scn_conversation_scene"),(reset_visitors),
      (set_visitor,0,"trp_player"),
      (party_stack_get_troop_id, ":meeting_troop",":meeting_party",0),
      (party_stack_get_troop_dna,":troop_dna",":meeting_party",0),
      (set_visitor,17,":meeting_troop",":troop_dna"),
      (set_jump_mission,"mt_conversation_encounter"),
      (jump_to_scene,"scn_conversation_scene"),
      (change_screen_map_conversation, ":meeting_troop"),
  ]),
  
  #script_party_remove_all_companions:
  # INPUT:
  # param1: Party-id from which  companions will be removed.
  # "$g_move_heroes" : controls if heroes will also be removed.
  ("party_remove_all_companions",
    [ (store_script_param_1, ":party"), #Source Party_id
      (party_get_num_companion_stacks, ":num_companion_stacks",":party"),
      (try_for_range_backwards, ":stack_no", 0, ":num_companion_stacks"),
        (party_stack_get_troop_id,   ":stack_troop",":party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_stack_get_size,  ":stack_size",":party",":stack_no"),
        (party_remove_members, ":party", ":stack_troop",  ":stack_size"),
      (try_end),
  ]),
  
  #script_party_remove_all_prisoners:
  # INPUT: param1: Party-id from which  prisoners will be removed.
  # "$g_move_heroes" : controls if heroes will also be removed.
  ("party_remove_all_prisoners",
    [ (store_script_param_1, ":party"), #Source Party_id
      (party_get_num_prisoner_stacks, ":num_prisoner_stacks",":party"),
      (try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
        (party_prisoner_stack_get_troop_id,   ":stack_troop",":party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_prisoner_stack_get_size, ":stack_size",":party",":stack_no"),
        (party_remove_prisoners, ":party", ":stack_troop", ":stack_size"),
      (try_end),
  ]),
  
  #script_party_add_party_companions:
  # INPUT: param1: Party-id to add the second part, param2: Party-id which will be added to the first one.
  # "$g_move_heroes" : controls if heroes will also be added.
  ("party_add_party_companions",
    [
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_get_num_companion_stacks, ":num_stacks",":source_party"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":source_party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_stack_get_size,         ":stack_size",":source_party",":stack_no"),
        (party_add_members, ":target_party", ":stack_troop", ":stack_size"),
        (party_stack_get_num_wounded, ":num_wounded", ":source_party", ":stack_no"),
        (party_wound_members, ":target_party", ":stack_troop", ":num_wounded"),
      (try_end),
  ]),
  
  #script_party_add_party_prisoners:
  # INPUT: param1: Party-id to add the second party, param2: Party-id which will be added to the first one.
  # "$g_move_heroes" : controls if heroes will also be added.
  ("party_add_party_prisoners",
    [
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_get_num_prisoner_stacks, ":num_stacks",":source_party"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id,     ":stack_troop",":source_party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_prisoner_stack_get_size,         ":stack_size",":source_party",":stack_no"),
        (party_add_members, ":target_party", ":stack_troop", ":stack_size"),
      (try_end),
  ]),
  
  #script_party_prisoners_add_party_companions:
  # INPUT: param1: Party-id to add the second part, param2: Party-id which will be added to the first one.
  # "$g_move_heroes" : controls if heroes will also be added.
  ("party_prisoners_add_party_companions",
    [
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_get_num_companion_stacks, ":num_stacks",":source_party"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":source_party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (troop_get_type,":race",":stack_troop"),
        (neg|eq,":race",tf_orc),        ## TLD good guys finish all orcs, evil guys finish all elves, GA
        (neg|eq,":race",tf_uruk),
        (neg|eq,":race",tf_urukhai),
        (neg|eq,":race",tf_troll),
        (neg|eq,":race",tf_lorien),
        (neg|eq,":race",tf_imladris),
        (neg|eq,":race",tf_woodelf),
        (party_stack_get_size, ":stack_size",":source_party",":stack_no"),
        (party_add_prisoners, ":target_party", ":stack_troop", ":stack_size"),
      (try_end),
  ]),
  
  #script_party_prisoners_add_party_prisoners:
  # INPUT: param1: Party-id to add the second part, param2: Party-id which will be added to the first one.
  # "$g_move_heroes" : controls if heroes will also be added.
  ("party_prisoners_add_party_prisoners",
    [
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_get_num_prisoner_stacks, ":num_stacks",":source_party"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id,     ":stack_troop",":source_party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_prisoner_stack_get_size,         ":stack_size",":source_party",":stack_no"),
        (party_add_prisoners, ":target_party", ":stack_troop", ":stack_size"),
      (try_end),
  ]),
  
  # script_party_add_party:
  # INPUT: param1: Party-id to add the second part, param2: Party-id which will be added to the first one.
  # "$g_move_heroes" : controls if heroes will also be added.
  ("party_add_party",
    [ (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (call_script, "script_party_add_party_companions",          ":target_party", ":source_party"),
      (call_script, "script_party_prisoners_add_party_prisoners", ":target_party", ":source_party"),
  ]),
  
  #script_party_copy:
  # INPUT: param1: Party-id to copy the second party, param2: Party-id which will be copied to the first one.
  ("party_copy",
    [ (assign, "$g_move_heroes", 1),
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_clear, ":target_party"),
	  (store_faction_of_party, reg10, ":source_party"),
	  (party_set_faction, ":target_party", reg10),
      (call_script, "script_party_add_party", ":target_party", ":source_party"),
  ]),
  
  
  #script_clear_party_group:
  # INPUT: param1: Party-id of the root of the group.
  #        param2: winner faction
  # This script will clear the root party and all parties attached to it recursively.
  ("clear_party_group",
    [ (store_script_param_1, ":root_party"),
      (store_script_param_2, ":winner_faction"),
	  (try_begin),
        (ge, ":root_party", 0), #MV fix for script errors
  #TLD assign faction strength penalties for party destruction, GA
        (store_faction_of_party, ":faction", ":root_party"),
	    (try_begin),
	      (is_between, ":faction", kingdoms_begin, kingdoms_end),
	      (faction_get_slot,":strength",":faction",slot_faction_strength_tmp),
	      (party_get_slot,":party_value", ":root_party",slot_party_victory_value),
	    #(party_get_slot,":party_type", ":root_party",slot_party_type),
#	    (try_begin),
#	      (eq,":party_type",spt_kingdom_hero_party), #hosts dying decrease faction strength unconditionally 
		  (val_sub, ":strength", ":party_value"),
          #debug stuff
          (faction_get_slot, ":debug_loss", ":faction", slot_faction_debug_str_loss),
		  (val_add, ":debug_loss", ":party_value"),
          (faction_set_slot, ":faction", slot_faction_debug_str_loss, ":debug_loss"),
#	    (else_try),
#		  (store_div,":s0",":strength",1000),
#		  (store_sub,":s",":strength",":party_value"),
#		  (val_div,":s",1000),
#		  (eq,":s0",":s"),
#		    (val_sub, ":strength",":party_value"),   # lesser parties dying can't shift faction strength through threshold
#	    (try_end),
	      (faction_set_slot,":faction",slot_faction_strength_tmp,":strength"),  # new strength stored in tmp slot to be processed in a trigger every 2h
          # add half victory points to the winner faction
          (try_begin),
            (is_between, ":winner_faction", kingdoms_begin, kingdoms_end),
            (faction_get_slot,":winner_strength",":winner_faction",slot_faction_strength_tmp),
		    (store_div, ":win_value", ":party_value", 2), #this formula could be balanced after playtesting
		    (val_add, ":winner_strength", ":win_value"),
	        (faction_set_slot,":winner_faction",slot_faction_strength_tmp,":winner_strength"),
            #debug stuff
            (faction_get_slot, ":debug_gain", ":winner_faction", slot_faction_debug_str_gain),
		    (val_add, ":debug_gain", ":win_value"),
            (faction_set_slot, ":winner_faction", slot_faction_debug_str_gain, ":debug_gain"),
          (try_end),
          #debug
          (try_begin),
            (eq, cheat_switch, 1),
	        (assign,reg0,":party_value"),
	        (assign,reg1,":strength"),
	        (assign,reg2,":win_value"),
	        (assign,reg3,":winner_strength"),
	        (str_store_faction_name,s1,":faction"),
	        (str_store_faction_name,s2,":winner_faction"),
            (try_begin),
              (is_between, ":winner_faction", kingdoms_begin, kingdoms_end),
	          #(display_message,"@DEBUG: {s1} strength -{reg0} to {reg1}, {s2} strength +{reg2} to {reg3}."), #mvdebug
            (else_try),
	          #(display_message,"@DEBUG: {s1} strength -{reg0} to {reg1}, defeat by {s2}."), #mvdebug
            (try_end),
          (try_end),
	    (try_end),
#end TLD

        (party_clear, ":root_party"),
        (party_get_num_attached_parties, ":num_attached_parties", ":root_party"),
        (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
          (party_get_attached_party_with_rank, ":attached_party", ":root_party", ":attached_party_rank"),
          (call_script, "script_clear_party_group", ":attached_party", ":winner_faction"),
        (try_end),
      
	  (try_end),
  ]),
  
  #script_get_nonempty_party_in_group:
  # INPUT: param1: Party-id of the root of the group.
  # OUTPUT: reg0: nonempy party-id
  ("get_nonempty_party_in_group",
    [ (store_script_param_1, ":party_no"),
      (party_get_num_companion_stacks, ":num_companion_stacks", ":party_no"),
      (try_begin),
        (gt, ":num_companion_stacks", 0),
        (assign, reg0, ":party_no"),
      (else_try),
        (assign, reg0, -1),
        
        (party_get_num_attached_parties, ":num_attached_parties", ":party_no"),
        (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
          (lt, reg0, 0),
          (party_get_attached_party_with_rank, ":attached_party", ":party_no", ":attached_party_rank"),
          (call_script, "script_get_nonempty_party_in_group", ":attached_party"),
        (try_end),
      (try_end),
  ]),
  
  #script_collect_prisoners_from_empty_parties:
  # INPUT: param1: Party-id of the root of the group, param2: Party to collect prisoners in.
  # make sure collection party is cleared before calling this.
  ("collect_prisoners_from_empty_parties",
    [ (store_script_param_1, ":party_no"),
      (store_script_param_2, ":collection_party"),
      
      (party_get_num_companions, ":num_companions", ":party_no"),
      (try_begin),
        (eq, ":num_companions", 0), #party is empty (has no companions). Collect its prisoners.
        (party_get_num_prisoner_stacks, ":num_stacks",":party_no"),
        (try_for_range, ":stack_no", 0, ":num_stacks"),
          (party_prisoner_stack_get_troop_id,     ":stack_troop",":party_no",":stack_no"),
          (troop_is_hero, ":stack_troop"),
          (party_add_members, ":collection_party", ":stack_troop", 1),
        (try_end),
      (try_end),
      (party_get_num_attached_parties, ":num_attached_parties", ":party_no"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":party_no", ":attached_party_rank"),
        (call_script, "script_collect_prisoners_from_empty_parties", ":attached_party", ":collection_party"),
      (try_end),
  ]),
  
  #script_print_casualties_to_s0:
  # INPUT: param1: Party_id, param2: 0 = use new line, 1 = use comma
  #OUTPUT: string register 0.
  ("print_casualties_to_s0",
    [(store_script_param, ":party_no", 1),
     (store_script_param, ":use_comma", 2),
     (str_clear, s0),
     (assign, ":total_reported", 0),
     (assign, ":total_wounded", 0),
     (assign, ":total_killed", 0),
     (party_get_num_companion_stacks, ":num_stacks",":party_no"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
       (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
       (party_stack_get_num_wounded, ":num_wounded",":party_no",":i_stack"),
       (store_sub, ":num_killed", ":stack_size", ":num_wounded"),
       (val_add, ":total_killed", ":num_killed"),
       (val_add, ":total_wounded", ":num_wounded"),
       (try_begin),
         (this_or_next|gt, ":num_killed", 0),
         (gt, ":num_wounded", 0),
         (store_add, reg3, ":num_killed", ":num_wounded"),
         (str_store_troop_name_by_count, s1, ":stack_troop", reg3),
         (try_begin),
           (troop_is_hero, ":stack_troop"),
           (assign, reg3, 0),
         (try_end),
         (try_begin),
           (gt, ":num_killed", 0),
           (gt, ":num_wounded", 0),
           (assign, reg4, ":num_killed"),
           (assign, reg5, ":num_wounded"),
           (str_store_string, s2, "@{reg4} killed, {reg5} wounded"),
         (else_try),
           (gt, ":num_killed", 0),
           (str_store_string, s2, "@killed"),
         (else_try),
           (str_store_string, s2, "@wounded"),
         (try_end),
         (try_begin),
           (eq, ":use_comma", 1),
           (try_begin),
             (eq, ":total_reported", 0),
             (str_store_string, s0, "@{reg3?{reg3}:} {s1} ({s2})"),
           (else_try),
             (str_store_string, s0, "@{s0}, {reg3?{reg3}:} {s1} ({s2})"),
           (try_end),
         (else_try),
           (str_store_string, s0, "@{s0}^{reg3?{reg3}:} {s1} ({s2})"),
         (try_end),
         (val_add, ":total_reported", 1),
       (try_end),
     (try_end),

     (try_begin),
       (this_or_next|gt, ":total_killed", 0),
       (gt, ":total_wounded", 0),
       (store_add, reg3, ":total_killed", ":total_wounded"),
       (try_begin),
         (gt, ":total_killed", 0),
         (gt, ":total_wounded", 0),
         (assign, reg4, ":total_killed"),
         (assign, reg5, ":total_wounded"),
         (str_store_string, s2, "@{reg4} killed, {reg5} wounded"),
       (else_try),
         (gt, ":total_killed", 0),
         (str_store_string, s2, "@killed"),
       (else_try),
         (str_store_string, s2, "@wounded"),
       (try_end),
       (str_store_string, s0, "@{s0}^TOTAL: {reg3} ({s2})"),
     (else_try),
       (try_begin),
         (eq, ":use_comma", 1),
         (str_store_string, s0, "@None"),
       (else_try),
         (str_store_string, s0, "@^None"),
       (try_end),
     (try_end),
  ]),

  #script_write_fit_party_members_to_stack_selection
  # INPUT: param1: party_no, exclude_leader
  #OUTPUT: trp_stack_selection_amounts slots (slot 0 = number of stacks, 1 = number of men fit, 2..n = stack sizes (fit))
  # trp_stack_selection_ids slots (2..n = stack troops)
  ("write_fit_party_members_to_stack_selection",
   [ (store_script_param, ":party_no", 1),
     (store_script_param, ":exclude_leader", 2),
     (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
     (assign, ":slot_index", 2),
     (assign, ":total_fit", 0),
     (try_for_range, ":stack_index", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop", ":party_no", ":stack_index"),
       (assign, ":num_fit", 0),
       (try_begin),
         (troop_is_hero, ":stack_troop"),
         (try_begin),
           (neg|troop_is_wounded, ":stack_troop"),
           (this_or_next|eq, ":exclude_leader", 0),
           (neq, ":stack_index", 0),
           (assign, ":num_fit",1),
         (try_end),
       (else_try),
         (party_stack_get_size, ":num_fit", ":party_no", ":stack_index"),
         (party_stack_get_num_wounded, ":num_wounded", ":party_no", ":stack_index"),
         (val_sub, ":num_fit", ":num_wounded"),
       (try_end),
       (try_begin),
         (gt, ":num_fit", 0),
         (troop_set_slot, "trp_stack_selection_amounts", ":slot_index", ":num_fit"),
         (troop_set_slot, "trp_stack_selection_ids", ":slot_index", ":stack_troop"),
         (val_add, ":slot_index", 1),
       (try_end),
       (val_add, ":total_fit", ":num_fit"),
     (try_end),
     (val_sub, ":slot_index", 2),
     (troop_set_slot, "trp_stack_selection_amounts", 0, ":slot_index"),
     (troop_set_slot, "trp_stack_selection_amounts", 1, ":total_fit"),
    ]),

  #script_remove_fit_party_member_from_stack_selection
  # INPUT: param1: slot_index
  #OUTPUT: reg0 = troop_no
  # trp_stack_selection_amounts slots (slot 0 = number of stacks, 1 = number of men fit, 2..n = stack sizes (fit))
  # trp_stack_selection_ids slots (2..n = stack troops)
  ("remove_fit_party_member_from_stack_selection",
   [ (store_script_param, ":slot_index", 1),
     (val_add, ":slot_index", 2),
     (troop_get_slot, ":amount", "trp_stack_selection_amounts", ":slot_index"),
     (troop_get_slot, ":troop_no", "trp_stack_selection_ids", ":slot_index"),
     (val_sub, ":amount", 1),
     (troop_set_slot, "trp_stack_selection_amounts", ":slot_index", ":amount"),
     (troop_get_slot, ":total_amount", "trp_stack_selection_amounts", 1),
     (val_sub, ":total_amount", 1),
     (troop_set_slot, "trp_stack_selection_amounts", 1, ":total_amount"),
     (try_begin),
       (le, ":amount", 0),
       (troop_get_slot, ":num_slots", "trp_stack_selection_amounts", 0),
       (store_add, ":end_cond", ":num_slots", 2),
       (store_add, ":begin_cond", ":slot_index", 1),
       (try_for_range, ":index", ":begin_cond", ":end_cond"),
         (store_sub, ":prev_index", ":index", 1),
         (troop_get_slot, ":value", "trp_stack_selection_amounts", ":index"),
         (troop_set_slot, "trp_stack_selection_amounts", ":prev_index", ":value"),
         (troop_get_slot, ":value", "trp_stack_selection_ids", ":index"),
         (troop_set_slot, "trp_stack_selection_ids", ":prev_index", ":value"),
       (try_end),
       (val_sub, ":num_slots", 1),
       (troop_set_slot, "trp_stack_selection_amounts", 0, ":num_slots"),
     (try_end),
     (assign, reg0, ":troop_no"),
    ]),

  #script_remove_random_fit_party_member_from_stack_selection
  #OUTPUT: reg0 = troop_no
  # trp_stack_selection_amounts slots (slot 0 = number of stacks, 1 = number of men fit, 2..n = stack sizes (fit))
  # trp_stack_selection_ids slots (2..n = stack troops)
  ("remove_random_fit_party_member_from_stack_selection",
   [
     (troop_get_slot, ":total_amount", "trp_stack_selection_amounts", 1),
     (store_random_in_range, ":random_troop", 0, ":total_amount"),
     (troop_get_slot, ":num_slots", "trp_stack_selection_amounts", 0),
     (store_add, ":end_cond", ":num_slots", 2),
     (try_for_range, ":index", 2, ":end_cond"),
       (troop_get_slot, ":amount", "trp_stack_selection_amounts", ":index"),
       (val_sub, ":random_troop", ":amount"),
       (lt, ":random_troop", 0),
       (assign, ":end_cond", 0),
       (store_sub, ":slot_index", ":index", 2),
     (try_end),
     (call_script, "script_remove_fit_party_member_from_stack_selection", ":slot_index"),
    ]),


  #script_cf_training_ground_sub_routine_for_training_result
  # INPUT: arg1: troop_id, arg2: stack_no, arg3: troop_count, arg4: xp_ratio_to_add
  ("cf_training_ground_sub_routine_for_training_result", []),


##  #script_cf_print_troop_name_with_stack_index_to_s0
##  # INPUT:
##  # param1: stack_index
##  
##  #OUTPUT:
##  # string register 0.
##  ("cf_print_troop_name_with_stack_index_to_s0",
##   [
##     (store_script_param_1, ":stack_index"),
##     (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
##     (lt, ":stack_index", ":num_stacks"),
##     (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":stack_index"),
##     (str_store_troop_name, s0, ":stack_troop"),
##    ]),

  #script_print_troop_owned_centers_in_numbers_to_s0
  # INPUT:
  # param1: troop_no
  #OUTPUT:
  # string register 0.
  ("print_troop_owned_centers_in_numbers_to_s0",
   [
     (store_script_param_1, ":troop_no"),
     (str_store_string, s0, "@nothing"),
     (assign, ":owned_towns", 0),
     (assign, ":owned_castles", 0),
     (assign, ":owned_villages", 0),
     (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
       (party_is_active, ":cur_center"), #TLD
       (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
       (try_begin),
         (party_slot_eq, ":cur_center", slot_party_type, spt_town),
         (val_add, ":owned_towns", 1),
       (else_try),
         (party_slot_eq, ":cur_center", slot_party_type, spt_castle),
         (val_add, ":owned_castles", 1),
       (else_try),
         (val_add, ":owned_villages", 1),
       (try_end),
     (try_end),
     (assign, ":num_types", 0),
     (try_begin),
       (gt, ":owned_villages", 0),
       (assign, reg0, ":owned_villages"),
       (store_sub, reg1, reg0, 1),
       (str_store_string, s0, "@{reg0} village{reg1?s:}"),
       (val_add, ":num_types", 1),
     (try_end),
     (try_begin),
       (gt, ":owned_castles", 0),
       (assign, reg0, ":owned_castles"),
       (store_sub, reg1, reg0, 1),
       (try_begin),
         (eq, ":num_types", 0),
         (str_store_string, s0, "@{reg0} castle{reg1?s:}"),
       (else_try),
         (str_store_string, s0, "@{reg0} castle{reg1?s:} and {s0}"),
       (try_end),
       (val_add, ":num_types", 1),
     (try_end),
     (try_begin),
       (gt, ":owned_towns", 0),
       (assign, reg0, ":owned_towns"),
       (store_sub, reg1, reg0, 1),
       (try_begin),
         (eq, ":num_types", 0),
         (str_store_string, s0, "@{reg0} town{reg1?s:}"),
       (else_try),
         (eq, ":num_types", 1),
         (str_store_string, s0, "@{reg0} town{reg1?s:} and {s0}"),
       (else_try),
         (str_store_string, s0, "@{reg0} town{reg1?s:}, {s0}"),
       (try_end),
     (try_end),
     (store_add, reg0, ":owned_villages", ":owned_castles"),
     (val_add, reg0, ":owned_towns"),
     ]),

  #script_get_random_melee_training_weapon
  # INPUT: none
  # OUTPUT: reg0 = weapon_1, reg1 = weapon_2
  ("get_random_melee_training_weapon",
   [
     (assign, ":weapon_1", -1),
     (assign, ":weapon_2", -1),
     (store_random_in_range, ":random_no", 0, 3),
     (try_begin),
       (eq, ":random_no", 0),
     (else_try),
       (eq, ":random_no", 1),
     (else_try),
     (try_end),
     (assign, reg0, ":weapon_1"),
     (assign, reg1, ":weapon_2"),
     ]),
 
  #script_party_count_fit_regulars:
  # Returns the number of unwounded regular companions in a party
  # INPUT: param1: Party-id
  ("party_count_fit_regulars",
    [
      (store_script_param_1, ":party"), #Party_id
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, reg0, 0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":party",":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size,         ":stack_size",":party",":i_stack"),
        (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
        (val_sub, ":stack_size", ":num_wounded"),
        (val_add, reg0, ":stack_size"),
      (try_end),
  ]),
  
  #script_party_count_fit_for_battle:
  # Returns the number of unwounded companions in a party
  # INPUT: param1: Party-id
  # OUTPUT: reg0 = result
  ("party_count_fit_for_battle",
    [
      (store_script_param_1, ":party"), #Party_id
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, reg0, 0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":party",":i_stack"),
        (assign, ":num_fit",0),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
#          (store_troop_health, ":troop_hp", ":stack_troop"),
          (try_begin),
            (neg|troop_is_wounded, ":stack_troop"),
#            (ge,  ":troop_hp", 20),
            (assign, ":num_fit",1),
          (try_end),
        (else_try),
          (party_stack_get_size,         ":num_fit",":party",":i_stack"),
          (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
          (val_sub, ":num_fit", ":num_wounded"),
        (try_end),
        (val_add, reg0, ":num_fit"),
      (try_end),
  ]),


  #script_party_count_members_with_full_health
  # Returns the number of unwounded regulars, and heroes other than player with 100% hitpoints in a party
  # INPUT: param1: Party-id
  # OUTPUT: reg0 = result
  ("party_count_members_with_full_health",
    [
      (store_script_param_1, ":party"), #Party_id
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, reg0, 0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":party",":i_stack"),
        (assign, ":num_fit",0),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (neq, ":stack_troop", "trp_player"),
          (store_troop_health, ":troop_hp", ":stack_troop"),
          (try_begin),
            (ge,  ":troop_hp", 80),
            (assign, ":num_fit",1),
          (try_end),
        (else_try),
          (party_stack_get_size,         ":num_fit",":party",":i_stack"),
          (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
          (val_sub, ":num_fit", ":num_wounded"),
          (val_max, ":num_fit", 0),
        (try_end),
        (val_add, reg0, ":num_fit"),
      (try_end),
  ]),
  
  ("party_count_wounded",
    [
      (store_script_param_1, ":party"), #Party_id
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, reg0, 0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":party",":i_stack"),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (store_troop_health, ":troop_hp", ":stack_troop"),
          (try_begin),
            (le,  ":troop_hp", 99),
            (val_add, reg0,5), # heros count for 5
          (try_end),
        (else_try),
          (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
          (val_add, reg0, ":num_wounded"),
        (try_end),
      (try_end),
  ]),

 
  ##  ("get_fit_stack_with_rank",
  ##    [
  ##      (store_script_param_1, ":party"), #Party_id
  ##      (store_script_param_2, ":rank"), #Rank
  ##      (party_get_num_companion_stacks, ":num_stacks",":party"),
  ##      (assign, reg0, -1),
  ##      (assign, ":num_total", 0),
  ##      (try_for_range, ":i_stack", 0, ":num_stacks"),
  ##        (eq, reg(0), -1), #continue only if we haven't found the result yet.
  ##        (party_stack_get_troop_id,     ":stack_troop",":party",":i_stack"),
  ##        (assign, ":num_fit",0),
  ##        (try_begin),
  ##          (troop_is_hero, ":stack_troop"),
  ##          (store_troop_health, ":troop_hp", ":stack_troop"),
  ##          (try_begin),
  ##            (ge,  ":troop_hp", 20),
  ##            (assign, ":num_fit",1),
  ##          (try_end),
  ##        (else_try),
  ##          (party_stack_get_size,         ":num_fit",":party",":i_stack"),
  ##          (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
  ##          (val_sub, ":num_fit", ":num_wounded"),
  ##        (try_end),
  ##        (val_add, ":num_total", ":num_fit"),
  ##        (try_begin),
  ##          (lt, ":rank", ":num_total"),
  ##          (assign, reg(0), ":i_stack"),
  ##        (try_end),
  ##      (try_end),
  ##  ]),
  
  #script_get_stack_with_rank:
  # Returns the stack no, containing unwounded regular companions with rank rank.
  # INPUT: param1: Party-id, param2: rank
  ("get_stack_with_rank",
    [
      (store_script_param_1, ":party"), #Party_id
      (store_script_param_2, ":rank"), #Rank
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, reg(0), -1),
      (assign, ":num_total", 0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (eq, reg(0), -1), #continue only if we haven't found the result yet.
        (party_stack_get_troop_id,     ":stack_troop",":party",":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size,         ":stack_size",":party",":i_stack"),
        (party_stack_get_num_wounded,  ":num_wounded",":party",":i_stack"),
        (val_sub, ":stack_size", ":num_wounded"),
        (val_add, ":num_total", ":stack_size"),
        (try_begin),
          (lt, ":rank", ":num_total"),
          (assign, reg(0), ":i_stack"),
        (try_end),
      (try_end),
  ]),
  
  #script_inflict_casualties_to_party:
  # INPUT: param1: Party-id, param2: number of rounds
  #OUTPUT:
  # This script doesn't return a value but populates the parties p_temp_wounded and p_temp_killed with the wounded and killed.
  #Example:
  #  (script_inflict_casualties_to_party, "_p_main_party" ,50), - simulates 50 rounds of casualties to main_party.
  ("inflict_casualties_to_party",
    [
      (party_clear, "p_temp_casualties"),
      (store_script_param_1, ":party"), #Party_id
      (call_script, "script_party_count_fit_regulars", ":party"),
      (assign, ":num_fit", reg(0)), #reg(47) = number of fit regulars.
      (store_script_param_2, ":num_attack_rounds"), #number of attacks
      (try_for_range, ":unused", 0, ":num_attack_rounds"),
        (gt, ":num_fit", 0),
        (store_random_in_range, ":attacked_troop_rank", 0 , ":num_fit"), #attack troop with rank reg(46)
        (assign, reg1, ":attacked_troop_rank"),
        (call_script, "script_get_stack_with_rank", ":party", ":attacked_troop_rank"),
        (assign, ":attacked_stack", reg(0)), #reg(53) = stack no to attack.
        (party_stack_get_troop_id,     ":attacked_troop",":party",":attacked_stack"),
        (store_character_level, ":troop_toughness", ":attacked_troop"),
        (val_add, ":troop_toughness", 5),  #troop-toughness = level + 5
        (assign, ":casualty_chance", 10000),
        (val_div, ":casualty_chance", ":troop_toughness"), #dying chance
        (try_begin),
          (store_random_in_range, ":rand_num", 0 ,10000),
          (lt, ":rand_num", ":casualty_chance"), #check chance to be a casualty
          (store_random_in_range, ":rand_num2", 0, 2), #check if this troop will be wounded or killed
          (try_begin),
            (troop_is_hero,":attacked_troop"), #currently troop can't be a hero, but no harm in keeping this.
            (store_troop_health, ":troop_hp",":attacked_troop"),
            (val_sub, ":troop_hp", 45),
            (val_max, ":troop_hp", 1),
            (troop_set_health, ":attacked_troop", ":troop_hp"),
          (else_try),
            (lt, ":rand_num2", 1), #wounded
            (party_add_members, "p_temp_casualties", ":attacked_troop", 1),
            (party_wound_members, "p_temp_casualties", ":attacked_troop", 1),
            (party_wound_members, ":party", ":attacked_troop", 1),
          (else_try), #killed
            (party_add_members, "p_temp_casualties", ":attacked_troop", 1),
            (party_remove_members, ":party", ":attacked_troop", 1),
          (try_end),
          (val_sub, ":num_fit", 1), #adjust number of fit regulars.
        (try_end),
      (try_end),
  ]),
  
  
  #script_move_members_with_ratio:
  # INPUT: param1: Source Party-id, param2: Target Party-id
  # pin_number = ratio of members to move, multiplied by 1000
  #OUTPUT:
  # This script doesn't return a value but moves some of the members of source party to target party according to the given ratio.
  ("move_members_with_ratio",
    [
      (store_script_param_1, ":source_party"), #Source Party_id
      (store_script_param_2, ":target_party"), #Target Party_id
      (party_get_num_prisoner_stacks, ":num_stacks",":source_party"),
      (try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id,     ":stack_troop",":source_party",":stack_no"),
        (party_prisoner_stack_get_size,    ":stack_size",":source_party",":stack_no"),
        (store_mul, ":number_to_move",":stack_size","$pin_number"),
        (val_div, ":number_to_move", 1000),
        (party_remove_prisoners, ":source_party", ":stack_troop", ":number_to_move"),
        (assign, ":number_moved", reg0),
        (party_add_prisoners, ":target_party", ":stack_troop", ":number_moved"),
      (try_end),
      (party_get_num_companion_stacks, ":num_stacks",":source_party"),
      (try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":source_party",":stack_no"),
        (party_stack_get_size,    ":stack_size",":source_party",":stack_no"),
        (store_mul, ":number_to_move",":stack_size","$pin_number"),
        (val_div, ":number_to_move", 1000),
        (party_remove_members, ":source_party", ":stack_troop", ":number_to_move"),
        (assign, ":number_moved", reg0),
        (party_add_members, ":target_party", ":stack_troop", ":number_moved"),
      (try_end),
  ]),
  
  
  # script_count_parties_of_faction_and_party_type:
  # counts number of active parties with a template and faction.
  # Input: arg1 = faction_no, arg2 = party_type
  # Output: reg0 = count
  ("count_parties_of_faction_and_party_type",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":party_type"),
      (assign, reg0, 0),
      (try_for_parties, ":party_no"),
        (party_is_active, ":party_no"),
        (party_slot_eq, ":party_no", slot_party_type, ":party_type"),
        (store_faction_of_party, ":cur_faction", ":party_no"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, reg0, 1),
      (try_end),
  ]),

  #script_select_random_town:
  # This script selects a random town in range [towns_begin, towns_end)
  #OUTPUT: reg0: id of the selected random town
 # ("select_random_town",
   # [
     # (assign, ":num_towns", towns_end),
     # (val_sub,":num_towns", towns_begin),
     # (store_random, ":random_town", ":num_towns"),
     # (val_add,":random_town", towns_begin),
     # (assign, reg0, ":random_town"),
 # ]),
  
 # ("select_random_spawn_point",
   # [
     # (assign, reg(20), spawn_points_end),
     # (val_sub,reg(20), spawn_points_begin),
     # (store_random, reg(21), reg(20)),
     # (val_add,reg(21), spawn_points_begin),
     # (assign, "$pout_town", reg(21)),
# ]),

  #script_cf_select_random_town_with_faction:
  # This script selects a random town in range [towns_begin, towns_end)
  # such that faction of the town is equal to given_faction
  # INPUT: arg1 = faction_no
  #OUTPUT: reg0 = town_no, this script may return false if there is no matching town.
  ("cf_select_random_town_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      # First count num matching spawn points
      (assign, ":no_towns", 0),
      (try_for_range,":cur_town", towns_begin, towns_end),
        (party_is_active, ":cur_town"), #TLD: don't consider disabled parties
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_towns", 1),
      (try_end),
      (gt, ":no_towns", 0), #Fail if there are no towns
      (store_random_in_range, ":random_town", 0, ":no_towns"),
      (assign, ":no_towns", 0),
      (try_for_range,":cur_town", towns_begin, towns_end),
        (party_is_active, ":cur_town"), #TLD: don't consider disabled parties
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_towns", 1),
        (gt, ":no_towns", ":random_town"),
        (assign, ":result", ":cur_town"),
      (try_end),
      (assign, reg0, ":result"),
  ]),

  #script_cf_select_random_village_with_faction:
  # This script selects a random village in range [villages_begin, villages_end)
  # such that faction of the village is equal to given_faction
  # INPUT: arg1 = faction_no
  #OUTPUT: reg0 = village_no, This script may return false if there is no matching village.
  ("cf_select_random_village_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      # First count num matching spawn points
      (assign, ":no_villages", 0),
      (try_for_range,":cur_village", villages_begin, villages_end),
        (store_faction_of_party, ":cur_faction", ":cur_village"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_villages", 1),
      (try_end),
      (gt, ":no_villages", 0), #Fail if there are no villages
      (store_random_in_range, ":random_village", 0, ":no_villages"),
      (assign, ":no_villages", 0),
      (try_for_range,":cur_village", villages_begin, villages_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_village"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_villages", 1),
        (gt, ":no_villages", ":random_village"),
        (assign, ":result", ":cur_village"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
  
  #script_cf_select_random_walled_center_with_faction:
  # This script selects a random center in range [centers_begin, centers_end)
  # such that faction of the town is equal to given_faction
  # INPUT: arg1 = faction_no, arg2 = preferred_center_no
  #OUTPUT: reg0 = town_no, This script may return false if there is no matching town.
  ("cf_select_random_walled_center_with_faction",
    [
      (store_script_param, ":faction_no", 1),
      (store_script_param, ":preferred_center_no", 2),
      (assign, ":result", -1),
      # First count num matching spawn points
      (assign, ":no_centers", 0),
      (try_for_range,":cur_center", walled_centers_begin, walled_centers_end),
        (party_is_active, ":cur_center"), #TLD
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_centers", 1),
        (eq, ":cur_center", ":preferred_center_no"),
        (val_add, ":no_centers", 99),
      (try_end),
      (gt, ":no_centers", 0), #Fail if there are no centers
      (store_random_in_range, ":random_center", 0, ":no_centers"),
      (try_for_range,":cur_center", walled_centers_begin, walled_centers_end),
        (party_is_active, ":cur_center"), #TLD
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (val_sub, ":random_center", 1),
        (try_begin),
          (eq, ":cur_center", ":preferred_center_no"),
          (val_sub, ":random_center", 99),
        (try_end),
        (lt, ":random_center", 0),
        (assign, ":result", ":cur_center"),
      (try_end),
      (assign, reg0, ":result"),
  ]),

  #script_cf_select_random_walled_center_with_faction_and_owner_priority_no_siege:
  # INPUT: arg1 = faction_no, arg2 = owner_troop_no
  #OUTPUT:
  # This script may return false if there is no matching town.
  # reg0 = center_no (Can fail)
  ("cf_select_random_walled_center_with_faction_and_owner_priority_no_siege",
    [
      (store_script_param, ":faction_no", 1),
      (store_script_param, ":troop_no", 2),
      #This script is used only to spawn lords, so make sure they spawn in their home theater
      (faction_get_slot, ":home_theater", ":faction_no", slot_faction_home_theater), #TLD
      (assign, ":result", -1),
      (assign, ":no_centers", 0),
      (try_for_range,":cur_center", walled_centers_begin, walled_centers_end),
        (party_is_active, ":cur_center"), #TLD
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_theater, ":home_theater"), #TLD
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_add, ":no_centers", 1),
        (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
        (val_add, ":no_centers", 1000),
      (try_end),
      (gt, ":no_centers", 0), #Fail if there are no centers
      (store_random_in_range, ":random_center", 0, ":no_centers"),
      (try_for_range,":cur_center", walled_centers_begin, walled_centers_end),
        (party_is_active, ":cur_center"), #TLD
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_theater, ":home_theater"), #TLD
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_sub, ":random_center", 1),
        (try_begin),
          (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
          (val_sub, ":random_center", 1000),
        (try_end),
        (lt, ":random_center", 0),
        (assign, ":result", ":cur_center"),
      (try_end),
      (assign, reg0, ":result"),
  ]),

  #script_cf_select_random_walled_center_with_faction_and_less_strength_priority:
  # This script selects a random center in range [centers_begin, centers_end)
  # such that faction of the town is equal to given_faction
  # INPUT: arg1 = faction_no, arg2 = preferred_center_no
  #OUTPUT: reg0 = town_no, This script may return false if there is no matching town.
  ("cf_select_random_walled_center_with_faction_and_less_strength_priority",
    [
      (store_script_param, ":faction_no", 1),
      (store_script_param, ":preferred_center_no", 2),
      (assign, ":result", -1),

#TLD begin
      (faction_get_slot, ":faction_theater", ":faction_no", slot_faction_active_theater),
      # TLD: First try to find a center in the active theater, if that fails, go anywhere as normal
      # Note: this script is only used when lords decide where to go next
      # First count num matching spawn points
      (assign, ":no_centers", 0),
      (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
        (party_is_active, ":cur_center"), #TLD
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_theater, ":faction_theater"), #TLD
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_add, ":no_centers", 1),
        (try_begin),
          (eq, ":cur_center", ":preferred_center_no"),
          (val_add, ":no_centers", 99),
        (try_end),
      (try_end),
      (gt, ":no_centers", 0), #Fail if there are no centers
      (store_random_in_range, ":random_center", 0, ":no_centers"),
      (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
        (party_is_active, ":cur_center"), #TLD
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_theater, ":faction_theater"), #TLD
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_sub, ":random_center", 1),
        (try_begin),
          (eq, ":cur_center", ":preferred_center_no"),
          (val_sub, ":random_center", 99),
        (try_end),
        (lt, ":random_center", 0),
        (assign, ":result", ":cur_center"),
      (try_end),
      
#TLD end

      # First count num matching spawn points
      (assign, ":no_centers", 0),
      (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
        (party_is_active, ":cur_center"), #TLD
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_add, ":no_centers", 1),
        (try_begin),
          (eq, ":cur_center", ":preferred_center_no"),
          (val_add, ":no_centers", 99),
        (try_end),
##        (call_script, "script_party_calculate_regular_strength", ":cur_center"),
##        (assign, ":strength", reg0),
##        (lt, ":strength", 80),
##        (store_sub, ":strength", 100, ":strength"),
##        (val_div, ":strength", 20),
##        (val_add, ":no_centers", ":strength"),
      (try_end),
      (gt, ":no_centers", 0), #Fail if there are no centers
      (store_random_in_range, ":random_center", 0, ":no_centers"),
      (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
        (party_is_active, ":cur_center"), #TLD
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_sub, ":random_center", 1),
        (try_begin),
          (eq, ":cur_center", ":preferred_center_no"),
          (val_sub, ":random_center", 99),
        (try_end),
##        (try_begin),
##          (call_script, "script_party_calculate_regular_strength", ":cur_center"),
##          (assign, ":strength", reg0),
##          (lt, ":strength", 80),
##          (store_sub, ":strength", 100, ":strength"),
##          (val_div, ":strength", 20),
##          (val_sub, ":random_center", ":strength"),
##        (try_end),
        (lt, ":random_center", 0),
        (assign, ":result", ":cur_center"),
      (try_end),
      (assign, reg0, ":result"),
  ]),

  
  #script_cf_select_random_town_at_peace_with_faction:
  # This script selects a random town in range [towns_begin, towns_end)
  # such that faction of the town is friendly to given_faction
  # INPUT: arg1 = faction_no
  #OUTPUT: reg0 = town_no, this script may return false if there is no matching town.
  ("cf_select_random_town_at_peace_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      # First count num matching towns
      (assign, ":no_towns", 0),
      (try_for_range,":cur_town", towns_begin, towns_end),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation,":reln", ":cur_faction", ":faction_no"),
        (ge, ":reln", 0),
        (val_add, ":no_towns", 1),
      (try_end),
      (gt, ":no_towns", 0), #Fail if there are no towns
      (store_random_in_range, ":random_town", 0, ":no_towns"),
      (assign, ":no_towns", 0),
      (try_for_range,":cur_town", towns_begin, towns_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation,":reln", ":cur_faction", ":faction_no"),
        (ge, ":reln", 0),
        (val_add, ":no_towns", 1),
        (gt, ":no_towns", ":random_town"),
        (assign, ":result", ":cur_town"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
  
  #script_cf_select_random_town_at_peace_with_faction_in_trade_route
  # INPUT: arg1 = town_no, arg2 = faction_no
  #OUTPUT: reg0 = town_no, this script may return false if there is no matching town.
  ("cf_select_random_town_at_peace_with_faction_in_trade_route",
    [
      (store_script_param, ":town_no", 1),
      (store_script_param, ":faction_no", 2),
      (assign, ":result", -1),
      (assign, ":no_towns", 0),
      (try_for_range, ":cur_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
        (party_get_slot, ":cur_town", ":town_no", ":cur_slot"),
        (gt, ":cur_town", 0),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation, ":reln", ":cur_faction", ":faction_no"),
        (ge, ":reln", 0),
        (val_add, ":no_towns", 1),
      (try_end),
      (gt, ":no_towns", 0), #Fail if there are no towns
      (store_random_in_range, ":random_town", 0, ":no_towns"),
      (try_for_range, ":cur_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
        (eq, ":result", -1),
        (party_get_slot, ":cur_town", ":town_no", ":cur_slot"),
        (gt, ":cur_town", 0),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation, ":reln", ":cur_faction", ":faction_no"),
        (ge, ":reln", 0),
        (val_sub, ":random_town", 1),
        (lt, ":random_town", 0),
        (assign, ":result", ":cur_town"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
  
  ##  ("cf_select_faction_spawn_point",
  ##    [
  ##      # First count num matching spawn points
  ##      (assign, reg(24), 0),
  ##      (try_for_range,reg(25), spawn_points_begin, spawn_points_end),
  ##        (store_faction_of_party, reg(23), reg(25)),
  ##        (eq, reg(23), "$pin_faction"),
  ##        (val_add, reg(24), 1),
  ##      (end_try,0),
  ##      # reg4 now holds num towns of this faction.
  ##      (gt, reg(24), 0), #Fail if there are no towns
  ##      (store_random, reg(26), reg(24)),
  ##
  ##      (assign, reg(24), 0), # reg24 = num points of this faction.
  ##      (try_for_range,reg(25), spawn_points_begin, spawn_points_end),
  ##        (store_faction_of_party, reg(23), reg(25)),
  ##        (eq, reg(23), "$pin_faction"),
  ##        (try_begin,0),
  ##          (eq, reg(24), reg(26)),
  ##          (assign, "$pout_town", reg(25)), # result is this town
  ##        (end_try,0),
  ##        (val_add, reg(24), 1),
  ##      (end_try,0),
  ##  ]),
  
  #script_spawn_party_at_random_town:
  # This script selects a random town in range [towns_begin, towns_end)
  # such that faction of the town is equal to given_faction
  # and spawns a new party there.
  # INPUT:
  # $pin_faction: given_faction
  # $pin_party_template: given_party_template
  
  #OUTPUT:
  # This script may return false if party cannot be spawned.
  # $pout_party: id of the spawned party
  ##  ("spawn_party_at_random_town",
  ##    [
  ##      (call_script,"script_select_random_spawn_point"),
  ##      (set_spawn_radius,1),
  ##      (spawn_around_party,"$pout_town","$pin_party_template"),
  ##      (assign, "$pout_party", reg(0)),
  ##  ]),
  
  #script_cf_spawn_party_at_faction_town:
  # This script selects a random town in range [towns_begin, towns_end)
  # such that faction of the town is equal to given_faction
  # and spawns a new party there.
  # INPUT:
  # $pin_faction: given_faction
  # $pin_party_template: given_party_template
  
  #OUTPUT:
  # This script may return false if party cannot be spawned.
  # $pout_party: id of the spawned party
  ##  ("cf_spawn_party_at_faction_town",
  ##    [
  ##      (call_script,"script_cf_select_faction_spawn_point"),
  ##      (set_spawn_radius,1),
  ##      (spawn_around_party,"$pout_town","$pin_party_template"),
  ##      (assign, "$pout_party", reg(0)),
  ##  ]),
  
  #script_spawn_party_at_random_town_if_below_limit:
  # This script checks if number of parties
  # of specified template is less than limit,
  # If so, it selects a random town in range [towns_begin, towns_end)
  # and spawns a new party there.
  # INPUT:
  # $pin_party_template: given_party_template
  # $pin_limit: limit value
  
  #OUTPUT:
  # $pout_party: id of the spawned party
  # $pout_town: id of the selected faction town
  # Note:
  # This script may return false if number of parties
  # of specified template is greater or equal to limit,
  # or if party cannot be spawned.
##  ("cf_spawn_party_at_random_town_if_below_limit",
##    [
##      (store_num_parties_of_template, reg(22), "$pin_party_template"),
##      (lt,reg(22),"$pin_limit"), #check if we are below limit.
##      (call_script,"script_select_random_spawn_point"),
##      (set_spawn_radius,1),
##      (spawn_around_party,"$pout_town","$pin_party_template"),
##      (assign, "$pout_party", reg(0)),
##  ]),
  
  ##  #script_spawn_party_at_faction_town_if_below_limit:
  ##  # This script checks if number of parties
  ##  # of specified template is less than limit,
  ##  # If so, it selects a random town in range [towns_begin, towns_end)
  ##  # such that faction of the town is equal to given_faction
  ##  # and spawns a new party there.
  ##  # INPUT:
  ##  # $pin_faction: given_faction
  ##  # $pin_party_template: given_party_template
  ##  # $pin_limit: limit value
  ##
   #OUTPUT:
   # $pout_party: id of the spawned party
   # $pout_town: id of the selected faction town
   # Note:
   # This script may return false if number of parties
   # of specified template is greater or equal to limit,
   # or if party cannot be spawned.
   # ("cf_spawn_party_at_faction_town_if_below_limit",
     # [
       # (store_num_parties_of_template, reg(22), "$pin_party_template"),
       # (lt,reg(22),"$pin_limit"), #check if we are below limit.
       # (call_script,"script_cf_select_faction_spawn_point"),
       # (set_spawn_radius,1),
       # (spawn_around_party,"$pout_town","$pin_party_template"),
       # (assign, "$pout_party", reg(0)),
   # ]),

  # script_shuffle_troop_slots:
  # Shuffles a range of slots of a given troop.
  # Used for exploiting a troop as an array.
  # INPUT: arg1 = troop_no, arg2 = slot_begin, arg3 = slot_end
  ("shuffle_troop_slots",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":slots_begin", 2),
      (store_script_param, ":slots_end", 3),
      (try_for_range, ":cur_slot_no", ":slots_begin", ":slots_end"),
        (store_random_in_range, ":random_slot_no", ":slots_begin", ":slots_end"), #reg(58) = random slot. Now exchange slots reg(57) and reg(58)
        (troop_get_slot, ":cur_slot_value", ":troop_no", ":cur_slot_no"), #temporarily store the value in slot reg(57) in reg(59)
        (troop_get_slot, ":random_slot_value", ":troop_no", ":random_slot_no"), #temporarily store the value in slot reg(58) in reg(60)
        (troop_set_slot, ":troop_no", ":cur_slot_no", ":random_slot_value"), # Now exchange the two...
        (troop_set_slot, ":troop_no", ":random_slot_no", ":cur_slot_value"),
      (try_end),
  ]),
  
  # script_get_random_quest
  # INPUT: arg1 = troop_no (of the troop in conversation), arg2 = min_importance (of the quest)
  #OUTPUT: reg0 = quest_no (the slots of the quest will be filled after calling this script)
  ("get_random_quest",
    [
      (store_script_param_1, ":giver_troop"),
      
      (store_character_level, ":player_level", "trp_player"),
      (store_troop_faction, ":giver_faction_no", ":giver_troop"),
      
      (troop_get_slot, ":giver_party_no", ":giver_troop", slot_troop_leaded_party),
      (troop_get_slot, ":giver_reputation", ":giver_troop", slot_lord_reputation_type),
      
      (assign, ":giver_center_no", -1),
      (try_begin),
        (gt, ":giver_party_no", 0),
        (party_get_attached_to, ":giver_center_no", ":giver_party_no"),
      (else_try),
        (is_between, "$g_encountered_party", centers_begin, centers_end),
        (assign, ":giver_center_no", "$g_encountered_party"),
      (try_end),
      
      (try_begin),
        (troop_slot_eq, ":giver_troop", slot_troop_occupation, slto_kingdom_hero),
        (try_begin),
          (ge, "$g_talk_troop_faction_relation", 0),
          (assign, ":quests_begin", lord_quests_begin),
          (assign, ":quests_end", lord_quests_end),
        (else_try),
          (assign, ":quests_begin", enemy_lord_quests_begin),
          (assign, ":quests_end", enemy_lord_quests_end),
        (try_end),
      (else_try),
        (is_between, ":giver_troop", village_elders_begin, village_elders_end),
        (assign, ":quests_begin", village_elder_quests_begin),
        (assign, ":quests_end", village_elder_quests_end),
      (else_try),
        (is_between, ":giver_troop", mayors_begin, mayors_end),
        (assign, ":quests_begin", mayor_quests_begin),
        (assign, ":quests_end", mayor_quests_end),
      (else_try),
        (assign, ":quests_begin", lady_quests_begin),
        (assign, ":quests_end", lady_quests_end),
      (try_end),
      (assign, ":result", -1),
      (try_for_range, ":unused", 0, 20), #Repeat trial twenty times
        (eq, ":result", -1),
        (assign, ":quest_target_troop", -1),
        (assign, ":quest_target_center", -1),
        (assign, ":quest_target_faction", -1),
        (assign, ":quest_object_faction", -1),
        (assign, ":quest_object_troop", -1),
        (assign, ":quest_object_center", -1),
        (assign, ":quest_target_party", -1),
        (assign, ":quest_target_party_template", -1),
        (assign, ":quest_target_amount", -1),
        (assign, ":quest_target_dna", -1),
        (assign, ":quest_target_item", -1),
        (assign, ":quest_importance", 1),
        (assign, ":quest_xp_reward", 0),
        (assign, ":quest_gold_reward", 0),
        (assign, ":quest_convince_value", 0),
        (assign, ":quest_expiration_days", 0),
        (assign, ":quest_dont_give_again_period", 0),

        (store_random_in_range, ":quest_no", ":quests_begin", ":quests_end"),
#      Remove this when test is done
#       (assign, ":quest_no", "qst_investigate_fangorn"),
#MV removed, please don't put test code that breaks other code into SVN -      (assign, ":quest_no", "qst_find_lost_spears"),
#(assign, ":quest_no", "qst_rescue_prisoners"), #MV debug
#      Remove this when test is done end
        (neg|check_quest_active,":quest_no"),
        (neg|quest_slot_ge, ":quest_no", slot_quest_dont_give_again_remaining_days, 1),
         (try_begin),
          # Saruman wants Fangorn to be investigated
##          (eq, ":quest_no", "qst_investigate_fangorn"),
      (eq, ":quest_no", "qst_find_lost_spears"),
          (try_begin),
            #(eq, ":giver_troop", trp_isengard_lord),  # only saruman gives this quest
			#(ge, ":player_level", 4),
            (assign, ":quest_expiration_days", 40),
            (assign, ":quest_dont_give_again_period", 200),
			(assign, ":quest_importance", 2),
            (assign, ":quest_xp_reward", 100),
			(assign, ":quest_gold_reward", 500),
            (assign, ":result", ":quest_no"),
          (try_end),
        (else_try),
          # Village Elder quests
          (eq, ":quest_no", "qst_deliver_grain"),
          (try_begin),
            (is_between, ":giver_center_no", villages_begin, villages_end),
            #The quest giver is the village elder
            (call_script, "script_get_troop_item_amount", ":giver_troop", "itm_grain"),
            (eq, reg0, 0),
            (neg|party_slot_ge, ":giver_center_no", slot_town_prosperity, 40),
            (assign, ":quest_target_center", ":giver_center_no"),
            (store_random_in_range, ":quest_target_amount", 4, 8),
            (assign, ":quest_expiration_days", 30),
            (assign, ":quest_dont_give_again_period", 20),
            (assign, ":result", ":quest_no"),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_deliver_cattle"),
          (try_begin),
            (is_between, ":giver_center_no", villages_begin, villages_end),
            #The quest giver is the village elder
            (party_get_slot, ":num_cattle", ":giver_center_no", slot_village_number_of_cattle),
            (lt, ":num_cattle", 50),
            (assign, ":quest_target_center", ":giver_center_no"),
            (store_random_in_range, ":quest_target_amount", 5, 10),
            (assign, ":quest_expiration_days", 30),
            (assign, ":quest_dont_give_again_period", 20),
            (assign, ":result", ":quest_no"),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_train_peasants_against_bandits"),
          (try_begin),
            (is_between, ":giver_center_no", villages_begin, villages_end),
            #The quest giver is the village elder
            (store_skill_level, ":player_trainer", "skl_trainer", "trp_player"),
            (gt, ":player_trainer", 0),
            (store_random_in_range, ":quest_target_amount", 5, 8),
            (assign, ":quest_target_center", ":giver_center_no"),
            (assign, ":quest_expiration_days", 20),
            (assign, ":quest_dont_give_again_period", 40),
            (assign, ":result", ":quest_no"),
          (try_end),
        (else_try),
          # Mayor quests
          (eq, ":quest_no", "qst_escort_merchant_caravan"),
          (is_between, ":giver_center_no", centers_begin, centers_end),
          (store_random_party_in_range, ":quest_target_center", towns_begin, towns_end),
          (store_distance_to_party_from_party, ":dist", ":giver_center_no",":quest_target_center"),
          (assign, ":quest_gold_reward", ":dist"),
          (val_add, ":quest_gold_reward", 25),
          (val_mul, ":quest_gold_reward", 25),
          (val_div, ":quest_gold_reward", 20),
          (store_random_in_range, ":quest_target_amount", 6, 12),
          (assign, "$escort_merchant_caravan_mode", 0),
          (assign, ":result", ":quest_no"),
        (else_try),
          (eq, ":quest_no", "qst_deliver_wine"),
          (is_between, ":giver_center_no", centers_begin, centers_end),
          (store_random_party_in_range, ":quest_target_center", towns_begin, towns_end),
          (store_random_in_range, ":random_no", 0, 2),
          (try_begin),
            (eq, ":random_no", 0),
            (assign, ":quest_target_item", "itm_quest_wine"),
          (else_try),
            (assign, ":quest_target_item", "itm_quest_ale"),
          (try_end),
          (store_random_in_range, ":quest_target_amount", 6, 12),
          (store_distance_to_party_from_party, ":dist", ":giver_center_no",":quest_target_center"),
          (assign, ":quest_gold_reward", ":dist"),
          (val_add, ":quest_gold_reward", 2),
          (assign, ":multiplier", 5),
          (val_add, ":multiplier", ":quest_target_amount"),
          (val_mul, ":quest_gold_reward", ":multiplier"),
          (val_div, ":quest_gold_reward", 100),
          (val_mul, ":quest_gold_reward", 10),
          (store_item_value,"$qst_deliver_wine_debt",":quest_target_item"),
          (val_mul,"$qst_deliver_wine_debt",":quest_target_amount"),
          (val_mul,"$qst_deliver_wine_debt", 6),
          (val_div,"$qst_deliver_wine_debt",5),
          (assign, ":quest_expiration_days", 7),
          (assign, ":quest_dont_give_again_period", 20),
          (assign, ":result", ":quest_no"),
        (else_try),
          (eq, ":quest_no", "qst_troublesome_bandits"),
          (is_between, ":giver_center_no", centers_begin, centers_end),
          (store_character_level, ":quest_gold_reward", "trp_player"),
          (val_add, ":quest_gold_reward", 20),
          (val_mul, ":quest_gold_reward", 35),
          (val_div, ":quest_gold_reward",100),
          (val_mul, ":quest_gold_reward", 10),
          (assign, ":quest_expiration_days", 30),
          (assign, ":quest_dont_give_again_period", 30),
          (assign, ":result", ":quest_no"),
        (else_try),
          (eq, ":quest_no", "qst_kidnapped_girl"),
          (is_between, ":giver_center_no", centers_begin, centers_end),
          (store_random_in_range, ":quest_target_center", villages_begin, villages_end),
          (store_character_level, ":quest_target_amount"),
          (val_add, ":quest_target_amount", 15),
          (store_distance_to_party_from_party, ":dist", ":giver_center_no", ":quest_target_center"),
          (val_add, ":dist", 15),
          (val_mul, ":dist", 2),
          (val_mul, ":quest_target_amount", ":dist"),
          (val_div, ":quest_target_amount",100),
          (val_mul, ":quest_target_amount",10),
          (assign, ":quest_gold_reward", ":quest_target_amount"),
          (val_div, ":quest_gold_reward", 40),
          (val_mul, ":quest_gold_reward", 10),
          (assign, ":quest_dont_give_again_period", 30),
          (assign, ":result", ":quest_no"),
        (else_try),
          (eq, ":quest_no", "qst_move_cattle_herd"),
          (is_between, ":giver_center_no", centers_begin, centers_end),
          (call_script, "script_cf_select_random_town_at_peace_with_faction", ":giver_faction_no"),
          (neq, ":giver_center_no", reg0),
          (assign, ":quest_target_center", reg0),
          (store_distance_to_party_from_party, ":dist",":giver_center_no",":quest_target_center"),
          (assign, ":quest_gold_reward", ":dist"),
          (val_add, ":quest_gold_reward", 25),
          (val_mul, ":quest_gold_reward", 50),
          (val_div, ":quest_gold_reward", 20),
          (assign, ":quest_expiration_days", 20),
          (assign, ":quest_dont_give_again_period", 20),
          (assign, ":result", ":quest_no"),
        (else_try),
          (eq, ":quest_no", "qst_persuade_lords_to_make_peace"),
          (is_between, ":giver_center_no", centers_begin, centers_end),
          (store_faction_of_party, ":cur_object_faction", ":giver_center_no"),
          (call_script, "script_cf_faction_get_random_enemy_faction", ":cur_object_faction"),
          (assign, ":cur_target_faction", reg0),
          (call_script, "script_cf_get_random_lord_except_king_with_faction", ":cur_object_faction"),
          (assign, ":cur_object_troop", reg0),
          (call_script, "script_cf_get_random_lord_except_king_with_faction", ":cur_target_faction"),
          (assign, ":quest_target_troop", reg0),
          (assign, ":quest_object_troop", ":cur_object_troop"),
          (assign, ":quest_target_faction", ":cur_target_faction"),
          (assign, ":quest_object_faction", ":cur_object_faction"),
          (assign, ":quest_gold_reward", 12000),
          (assign, ":quest_convince_value", 7000),
          (assign, ":quest_expiration_days", 30),
          (assign, ":quest_dont_give_again_period", 100),
          (assign, ":result", ":quest_no"),
        (else_try),
          (eq, ":quest_no", "qst_deal_with_looters"),
          (is_between, ":player_level", 0, 15),
          (is_between, ":giver_center_no", centers_begin, centers_end),
          (store_faction_of_party, ":cur_object_faction", ":giver_center_no"),
          (store_num_parties_destroyed_by_player, ":num_looters_destroyed", "pt_looters"),
          (party_template_set_slot,"pt_looters",slot_party_template_num_killed,":num_looters_destroyed"),
          (quest_set_slot,"$random_merchant_quest_no",slot_quest_current_state,0),
          (quest_set_slot,"$random_merchant_quest_no",slot_quest_target_party_template,"pt_looters"),
          (assign, ":quest_gold_reward", 500),
          (assign, ":quest_xp_reward", 500),
          (assign, ":quest_expiration_days", 20),
          (assign, ":quest_dont_give_again_period", 30),
          (assign, ":result", ":quest_no"),
        (else_try),
          (eq, ":quest_no", "qst_deal_with_night_bandits"),
          (is_between, ":player_level", 0, 15),
          (is_between, ":giver_center_no", centers_begin, centers_end),
          (party_slot_ge, ":giver_center_no", slot_center_has_bandits, 1),
          (assign, ":quest_target_center", ":giver_center_no"),
          (assign, ":quest_expiration_days", 4),
          (assign, ":quest_dont_give_again_period", 15),
          (assign, ":result", ":quest_no"),
        (else_try),
          # Lady quests
          (eq, ":quest_no", "qst_rescue_lord_by_replace"),
          (try_begin),
            (ge, "$g_talk_troop_faction_relation", 0),
            (is_between, ":player_level", 5, 25),
            (troop_get_slot, ":cur_target_troop", ":giver_troop", slot_troop_father),
            (try_begin),
              (eq, ":cur_target_troop", 0),
              (troop_get_slot, ":cur_target_troop", ":giver_troop", slot_troop_spouse),
            (try_end),
            #(troop_slot_eq, ":cur_target_troop", slot_troop_is_prisoner, 1),#Skip if the lady's father/husband is not in prison
            (troop_slot_ge, ":cur_target_troop", slot_troop_prisoner_of_party, 0),
            (call_script, "script_search_troop_prisoner_of_party", ":cur_target_troop"),
            (assign, ":cur_target_center", reg0),
            (is_between, ":cur_target_center", towns_begin, towns_end),#Skip if he is not in a town
            (assign, ":quest_target_center", ":cur_target_center"),
            (assign, ":quest_target_troop", ":cur_target_troop"),
            (assign, ":quest_expiration_days", 30),
            (assign, ":quest_dont_give_again_period", 73),
            (assign, ":result", ":quest_no"),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_deliver_message_to_prisoner_lord"),
          (try_begin),
            (ge, "$g_talk_troop_faction_relation", 0),
            (is_between, ":player_level", 5, 25),
            (troop_get_slot, ":cur_target_troop", ":giver_troop", slot_troop_father),
            (try_begin),
              (eq, ":cur_target_troop", 0),
              (troop_get_slot, ":cur_target_troop", ":giver_troop", slot_troop_spouse),
            (try_end),
            #(troop_slot_eq, ":cur_target_troop", slot_troop_is_prisoner, 1),#Skip if the lady's father/husband is not in prison
            (troop_slot_ge, ":cur_target_troop", slot_troop_prisoner_of_party, 0),
            (call_script, "script_search_troop_prisoner_of_party", ":cur_target_troop"),
            (assign, ":cur_target_center", reg0),
            (is_between, ":cur_target_center", towns_begin, towns_end),#Skip if he is not in a town
            (assign, ":quest_target_center", ":cur_target_center"),
            (assign, ":quest_target_troop", ":cur_target_troop"),
            (assign, ":quest_expiration_days", 30),
            (assign, ":quest_dont_give_again_period", 30),
            (assign, ":result", ":quest_no"),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_duel_for_lady"),
          (try_begin),
            (ge, "$g_talk_troop_faction_relation", 0),
            (ge, ":player_level", 10),
            (call_script, "script_cf_troop_get_random_enemy_troop_with_occupation", ":giver_troop", slto_kingdom_hero),#Can fail
            (assign, ":cur_target_troop", reg0),
            (neg|troop_slot_eq, ":giver_troop", slot_troop_spouse, ":cur_target_troop"), #must not be in the family
            (neg|troop_slot_eq, ":giver_troop", slot_troop_father, ":cur_target_troop"),
            #(troop_slot_eq, ":cur_target_troop", slot_troop_is_prisoner, 0),
            (neg|troop_slot_ge, ":cur_target_troop", slot_troop_prisoner_of_party, 0),
            (troop_slot_ge, ":cur_target_troop", slot_troop_leaded_party, 0),
            (neg|troop_slot_eq, ":cur_target_troop", slot_lord_reputation_type, lrep_goodnatured),
            (neg|troop_slot_eq, ":cur_target_troop", slot_lord_reputation_type, lrep_upstanding),
            (assign, ":quest_target_troop", ":cur_target_troop"),
            (assign, ":quest_expiration_days", 30),
            (assign, ":quest_dont_give_again_period", 50),
            (assign, ":result", ":quest_no"),
          (try_end),
          # Enemy Lord Quests
        (else_try),
          (eq, ":quest_no", "qst_lend_surgeon"),
          (try_begin),
            (eq, "$g_defending_against_siege", 0),#Skip if the center is under siege (because of resting)
            (neq, ":giver_reputation", lrep_quarrelsome),
            (neq, ":giver_reputation", lrep_debauched),
            (assign, ":max_surgery_level", 0),
            (assign, ":best_surgeon", -1),
            (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
            (try_for_range, ":i_stack", 1, ":num_stacks"),
              (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
              (troop_is_hero, ":stack_troop"),
              (store_skill_level, ":cur_surgery_skill", skl_surgery, ":stack_troop"),
              (gt, ":cur_surgery_skill", ":max_surgery_level"),
              (assign, ":max_surgery_level", ":cur_surgery_skill"),
              (assign, ":best_surgeon", ":stack_troop"),
            (try_end),
            
            (store_character_level, ":cur_level", "trp_player"),
            (assign, ":required_skill", 5),
            (val_div, ":cur_level", 10),
            (val_add, ":required_skill", ":cur_level"),
            (ge, ":max_surgery_level", ":required_skill"), #Skip if party skill level is less than the required value
            
            (assign, ":quest_object_troop", ":best_surgeon"),
            (assign, ":quest_importance", 1),
            (assign, ":quest_xp_reward", 10),
            (assign, ":quest_gold_reward", 10),
            (assign, ":quest_dont_give_again_period", 50),
            (assign, ":result", ":quest_no"),
          (try_end),
          # Lord Quests
        (else_try),
          (eq, ":quest_no", "qst_meet_spy_in_enemy_town"),
          (try_begin),
            (eq, "$players_kingdom", ":giver_faction_no"),
            (neq, ":giver_reputation", lrep_goodnatured),
            (call_script, "script_troop_get_player_relation", ":giver_troop"),
            (assign, ":giver_relation", reg0),
            (gt, ":giver_relation", 3),
            (call_script, "script_cf_faction_get_random_enemy_faction", ":giver_faction_no"),
            (assign, ":enemy_faction", reg0),
            (store_relation, ":reln", ":enemy_faction", "fac_player_supporters_faction"),
            (lt, ":reln", 0),
            (call_script, "script_cf_select_random_town_with_faction", ":enemy_faction"),
            (assign, ":cur_target_center", reg0),
            #Just to make sure that there is a free walker
            (call_script, "script_cf_center_get_free_walker", ":cur_target_center"),
            (assign, ":quest_target_center", ":cur_target_center"),
            (store_random_in_range, ":quest_target_amount", secret_signs_begin, secret_signs_end),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_gold_reward", 500),
            (assign, ":quest_expiration_days", 30),
            (assign, ":quest_dont_give_again_period", 50),
            (quest_set_slot, "qst_meet_spy_in_enemy_town", slot_quest_gold_reward, 500),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_raid_caravan_to_start_war"),
          (try_begin),
            (eq, "$players_kingdom", ":giver_faction_no"),
            (this_or_next|eq, ":giver_reputation", lrep_cunning),
            (this_or_next|eq, ":giver_reputation", lrep_quarrelsome),
            (             eq, ":giver_reputation", lrep_debauched),
            (gt, ":player_level", 10),
            (neg|faction_slot_eq, ":giver_faction_no", slot_faction_leader, ":giver_troop"),#Can not take the quest from the king
            (call_script, "script_cf_faction_get_random_friendly_faction", ":giver_faction_no"),#Can fail
            (assign, ":quest_target_faction", reg0),
            (store_troop_faction, ":quest_object_faction", ":giver_troop"),
            (assign, ":quest_target_party_template", "pt_kingdom_caravan_party"),
            (assign, ":quest_target_amount", 2),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_expiration_days", 30),
            (assign, ":quest_dont_give_again_period", 100),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_deliver_message"),
          (try_begin),
            (ge, "$g_talk_troop_faction_relation", 0),
            (lt, ":player_level", 20),
            (call_script, "script_cf_get_random_lord_in_a_center_with_faction", ":giver_faction_no"),#Can fail
            (assign, ":cur_target_troop", reg0),
            (neq, ":cur_target_troop", ":giver_troop"),#Skip himself
            (call_script, "script_get_troop_attached_party", ":cur_target_troop"),
            (assign, ":cur_target_center", reg0),#cur_target_center will definitely be a valid center
            (neq,":giver_center_no", ":cur_target_center"),#Skip current center

            (assign, ":quest_target_center", ":cur_target_center"),
            (assign, ":quest_target_troop", ":cur_target_troop"),
            (assign, ":quest_xp_reward", 30),
            (assign, ":quest_gold_reward", 40),
            (assign, ":result", ":quest_no"),
      
            (assign, ":quest_expiration_days", 30),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_escort_lady"),
          (try_begin),
            (ge, "$g_talk_troop_faction_relation", 0),
            (ge, ":player_level", 10),
            (troop_get_slot, ":cur_object_troop", ":giver_troop", slot_troop_daughter),
            (store_random_in_range, ":random_no", 0, 2),
            (try_begin),
              (this_or_next|eq,  ":cur_object_troop", 0),
              (eq, ":random_no", 0),
              (troop_get_slot, ":cur_object_troop_2", ":giver_troop", slot_troop_spouse),
              (gt, ":cur_object_troop_2", 0),
              (assign, ":cur_object_troop", ":cur_object_troop_2"),
            (try_end),
            (gt, ":cur_object_troop", 0),#Skip lords without a lady
            (troop_get_type, ":cur_troop_gender", ":cur_object_troop"),
            (eq, ":cur_troop_gender", 1),#Skip if it is not female
            (gt, ":giver_center_no", 0),#Skip if lord is outside the center
            (troop_slot_eq, ":cur_object_troop", slot_troop_cur_center, ":giver_center_no"),#Skip if the lady is not at the same center
            (call_script, "script_cf_select_random_town_with_faction", ":giver_faction_no"),#Can fail
            (assign, ":cur_target_center", reg0),
            (neq, ":cur_target_center", ":giver_center_no"),
            (hero_can_join),#Skip if player has no available slots

            (assign, ":quest_object_troop", ":cur_object_troop"),
            (assign, ":quest_target_center", ":cur_target_center"),
            (assign, ":quest_expiration_days", 20),
            (assign, ":quest_dont_give_again_period", 30),
            (assign, ":result", ":quest_no"),
          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_hunt_down_raiders"),
##          (try_begin),
##            (gt, ":player_level", 10),
##            (faction_slot_eq, ":giver_faction_no", slot_faction_leader, ":giver_troop"),
##            (call_script, "script_cf_select_random_town_with_faction", ":giver_faction_no"),#Can fail
##            (assign, ":cur_object_center", reg0),
##            (neq, ":cur_object_center", ":giver_center_no"),#Skip current center
##            (call_script, "script_get_random_enemy_center", ":giver_party_no"),
##            (assign, ":cur_target_center", reg0),
##            (ge, ":cur_target_center", 0),
##            (store_faction_of_party, ":cur_target_faction", ":cur_target_center"),
##            (is_between,  ":cur_target_faction", kingdoms_begin, kingdoms_end),
##
##            (assign, ":quest_object_center", ":cur_object_center"),
##            (assign, ":quest_target_center", ":cur_target_center"),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 1500),
##            (assign, ":quest_gold_reward", 1000),
##            (assign, ":result", ":quest_no"),
##          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_bring_back_deserters"),
##          (try_begin),
##            (gt, ":player_level", 5),
##            (faction_get_slot, ":cur_target_party_template", ":giver_faction_no", slot_faction_deserter_party_template),
##            (faction_get_slot, ":cur_target_troop", ":giver_faction_no", slot_faction_deserter_troop),
##            (gt, ":cur_target_party_template", 0),#Skip factions with no deserter party templates
##            (store_num_parties_of_template, ":num_deserters", ":cur_target_party_template"),
##            (ge, ":num_deserters", 2),#Skip if there are less than 2 active deserter parties
##
##            (assign, ":quest_target_troop", ":cur_target_troop"),
##            (assign, ":quest_target_party_template", ":cur_target_party_template"),
##            (assign, ":quest_target_amount", 5),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 500),
##            (assign, ":quest_gold_reward", 300),
##            (assign, ":result", ":quest_no"),
##          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_deliver_supply_to_center_under_siege"),
##          (try_begin),
##            (gt, ":player_level", 10),
##            (gt, ":giver_center_no", 0),#Skip if lord is outside the center
##            (call_script, "script_cf_get_random_siege_location_with_faction", ":giver_faction_no"),#Can fail
##            (assign, ":quest_target_center", reg0),
##            (assign, ":quest_target_amount", 10),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 500),
##            (assign, ":quest_gold_reward", 300),
##            (assign, ":result", ":quest_no"),
##          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_rescue_lady_under_siege"),
##          (try_begin),
##            (gt, ":player_level", 15),
##            (troop_get_slot, ":cur_object_troop", ":giver_troop", slot_troop_daughter),
##            (store_random_in_range, ":random_no", 0, 2),
##            (try_begin),
##              (this_or_next|eq,  ":cur_object_troop", 0),
##              (eq, ":random_no", 0),
##              (troop_get_slot, ":cur_object_troop_2", ":giver_troop", slot_troop_spouse),
##              (gt, ":cur_object_troop_2", 0),
##              (assign, ":cur_object_troop", ":cur_object_troop_2"),
##            (try_end),
##            (gt, ":cur_object_troop", 0),#Skip lords without a lady
##            (troop_get_type, ":cur_troop_gender", ":cur_object_troop"),
##            (eq, ":cur_troop_gender", 1),#Skip if lady is not female
##            (troop_get_slot, ":cur_target_center", ":cur_object_troop", slot_troop_cur_center),
##            (is_between, ":cur_target_center", centers_begin, centers_end),#Skip if she is not in a center
##            (neq,":giver_center_no", ":cur_target_center"),#Skip current center
##            (call_script, "script_cf_get_random_siege_location_with_faction", ":giver_faction_no"),#Can fail
##            (assign, ":cur_target_center", reg0),
##            (troop_set_slot, ":cur_object_troop", slot_troop_cur_center, ":cur_target_center"),#Move lady to the siege location
##            (assign, ":quest_object_troop", ":cur_object_troop"),
##            (assign, ":quest_target_center", ":cur_target_center"),
##            (assign, ":quest_target_troop", ":giver_troop"),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 200),
##            (assign, ":quest_gold_reward", 750),
##            (assign, ":result", ":quest_no"),
##          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_deliver_message_to_lover"),
##          (try_begin),
##            (is_between, ":player_level", 5, 30),
##            (troop_get_slot, ":cur_target_troop", ":giver_troop", slot_troop_lover),
##            (gt, ":cur_target_troop", 0),#Skip lords without a lover
##            (troop_get_slot, ":cur_target_center", ":cur_target_troop", slot_troop_cur_center),
##            (is_between, ":cur_target_center", centers_begin, centers_end),#Skip if she is not in a center
##            (neq,":giver_center_no", ":cur_target_center"),#Skip current center
##            (assign, ":quest_target_troop", ":cur_target_troop"),
##            (assign, ":quest_target_center", ":cur_target_center"),
##            (assign, ":result", ":quest_no"),
##          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_bring_reinforcements_to_siege"),
##          (try_begin),
##            (gt, ":player_level", 10),
##            (call_script, "script_cf_get_random_siege_location_with_attacker_faction", ":giver_faction_no"),#Can fail
##            (assign, ":cur_target_center", reg0),
##            (store_random_in_range, ":random_no", 5, 11),
##            (troops_can_join, ":random_no"),#Skip if the player doesn't have enough room
##            (call_script, "script_cf_get_number_of_random_troops_from_party", ":giver_party_no", ":random_no"),#Can fail
##            (assign, ":cur_object_troop", reg0),
##            (party_get_battle_opponent, ":cur_target_party", ":cur_target_center"),
##            (party_get_num_companion_stacks, ":num_stacks", ":cur_target_party"),
##            (gt, ":num_stacks", 0),#Skip if the besieger party has no troops
##            (party_stack_get_troop_id, ":cur_target_troop", ":cur_target_party", 0),
##            (troop_is_hero, ":cur_target_troop"),#Skip if the besieger party has no heroes
##            (neq, ":cur_target_troop", ":giver_troop"),#Skip if the quest giver is the same troop
##            (assign, ":quest_target_troop", ":cur_target_troop"),
##            (assign, ":quest_object_troop", ":cur_object_troop"),
##            (assign, ":quest_target_party", ":cur_target_party"),
##            (assign, ":quest_target_center", ":cur_target_center"),
##            (assign, ":quest_target_amount", ":random_no"),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 400),
##            (assign, ":quest_gold_reward", 200),
##            (assign, ":result", ":quest_no"),
##          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_deliver_message_to_enemy_lord"),
          (try_begin),
            (ge, "$g_talk_troop_faction_relation", 0),
            (is_between, ":player_level", 5,25),
            (call_script, "script_cf_get_random_lord_from_another_faction_in_a_center", ":giver_faction_no"),#Can fail
            (assign, ":cur_target_troop", reg0),
            (call_script, "script_get_troop_attached_party", ":cur_target_troop"),
            (assign, ":quest_target_center", reg0),#quest_target_center will definitely be a valid center
            (assign, ":quest_target_troop", ":cur_target_troop"),
            (assign, ":quest_importance", 1),
            (assign, ":quest_xp_reward", 200),
            (assign, ":quest_gold_reward", 0),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_expiration_days", 40),
          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_bring_prisoners_to_enemy"),
##          (try_begin),
##            (gt, ":player_level", 10),
##            (is_between, ":giver_center_no", centers_begin, centers_end),#Skip if the quest giver is not at a center
##            (store_random_in_range, ":random_no", 5, 11),
##            (troops_can_join_as_prisoner, ":random_no"),#Skip if the player doesn't have enough room
##            (call_script, "script_get_random_enemy_town", ":giver_center_no"),
##            (assign, ":cur_target_center", reg0),
##            (ge, ":cur_target_center", 0),#Skip if there are no enemy towns
##            (store_faction_of_party, ":cur_target_faction", ":cur_target_center"),
##            (faction_get_slot, ":cur_object_troop", ":cur_target_faction", slot_faction_tier_5_troop),
##            (assign, ":quest_target_center", ":cur_target_center"),
##            (assign, ":quest_object_troop", ":cur_object_troop"),
##            (assign, ":quest_target_amount", ":random_no"),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 300),
##            (assign, ":quest_gold_reward", 200),
##            (assign, ":result", ":quest_no"),
##          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_deal_with_bandits_at_lords_village"),
          (try_begin),
            (neq, ":giver_reputation", lrep_debauched),
            (neq, ":giver_reputation", lrep_quarrelsome),
            (ge, "$g_talk_troop_faction_relation", 0),
            (assign, ":end_cond", villages_end),
            (assign, ":cur_target_center", -1),
            (try_for_range, ":cur_village", villages_begin, ":end_cond"),
              (party_slot_eq, ":cur_village", slot_town_lord, ":giver_troop"),
              (party_slot_eq, ":cur_village", slot_village_infested_by_bandits, 1),
              (assign, ":cur_target_center", ":cur_village"),
              (assign, ":end_cond", 0),
            (try_end),
            (ge, ":cur_target_center", 0),
            (neg|check_quest_active, "qst_eliminate_bandits_infesting_village"),
            (assign, ":quest_target_center", ":cur_target_center"),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_expiration_days", 30),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_raise_troops"),
          (try_begin),
            (neq, ":giver_reputation", lrep_martial),
            (neq, ":giver_faction_no", "fac_player_supporters_faction"), #we need tier_1_troop a valid value
            (ge, "$g_talk_troop_faction_relation", 0),
            (store_character_level, ":cur_level", "trp_player"),
            (gt, ":cur_level", 5),
            (troop_slot_ge, "trp_player", slot_troop_renown, 100),
             
            (store_random_in_range, ":quest_target_amount", 5, 8),
            (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
            (le, ":quest_target_amount", ":free_capacity"),
            (faction_get_slot, ":quest_object_troop", ":giver_faction_no", slot_faction_tier_1_troop),
            (store_random_in_range, ":level_up", 20, 40),
            (val_add, ":level_up", ":cur_level"),
            (val_div, ":level_up", 10),

            (store_mul, ":quest_gold_reward", ":quest_target_amount", 10),

            (assign, ":quest_target_troop", ":quest_object_troop"),
            (try_for_range, ":unused", 0, ":level_up"),
              (troop_get_upgrade_troop, ":level_up_troop", ":quest_target_troop", 0),
              (gt, ":level_up_troop", 0),
              (assign, ":quest_target_troop", ":level_up_troop"),
              (val_mul, ":quest_gold_reward", ":quest_gold_reward", 7),
              (val_div, ":quest_gold_reward", ":quest_gold_reward", 4),
            (try_end),
      
##            (try_begin),
##              (ge, ":cur_level", 15),
##              (faction_get_slot, ":cur_target_troop", ":giver_faction_no", slot_faction_tier_5_troop),
##              (assign, ":quest_gold_reward", 300),
##            (else_try),
##              (faction_get_slot, ":cur_target_troop", ":giver_faction_no", slot_faction_tier_4_troop),
##              (assign, ":quest_gold_reward", 150),
##            (try_end),
##            (gt, ":cur_target_troop", 0),
            (assign, ":quest_xp_reward", ":quest_gold_reward"),
            (val_mul, ":quest_xp_reward", 3),
            (val_div, ":quest_xp_reward", 10),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_expiration_days", 120),
            (assign, ":quest_dont_give_again_period", 15),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_collect_taxes"),
          (try_begin),
            (neq, ":giver_reputation", lrep_goodnatured),
            (neq, ":giver_reputation", lrep_upstanding),
            (ge, "$g_talk_troop_faction_relation", 0),
            (call_script, "script_cf_troop_get_random_leaded_town_or_village_except_center", ":giver_troop", ":giver_center_no"),
            (assign, ":quest_target_center", reg0),
            (assign, ":quest_importance", 1),
            (assign, ":quest_gold_reward", 0),
            (assign, ":quest_xp_reward", 100),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_expiration_days", 50),
            (assign, ":quest_dont_give_again_period", 20),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_hunt_down_fugitive"),
          (try_begin),
            (ge, "$g_talk_troop_faction_relation", 0),
            (call_script, "script_cf_select_random_village_with_faction", ":giver_faction_no"),
            (assign, ":quest_target_center", reg0),
            (store_random_in_range, ":quest_target_dna", 0, 1000000),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_expiration_days", 30),
            (assign, ":quest_dont_give_again_period", 30),
          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_capture_messenger"),
##          (try_begin),
##            (call_script, "script_cf_faction_get_random_enemy_faction", ":giver_faction_no"),
##            (assign, ":cur_target_faction", reg0),
##            (faction_get_slot, ":cur_target_troop", ":cur_target_faction", slot_faction_messenger_troop),
##            (gt, ":cur_target_troop", 0),#Checking the validiy of cur_target_troop
##            (store_num_parties_destroyed_by_player, ":quest_target_amount", "pt_messenger_party"),
##
##            (assign, ":quest_target_troop", ":cur_target_troop"),
##            (assign, ":quest_target_party_template", ":cur_target_party_template"),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 700),
##            (assign, ":quest_gold_reward", 400),
##            (assign, ":result", ":quest_no"),
##          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_kill_local_merchant"),
          (try_begin),
            (this_or_next|eq, ":giver_reputation", lrep_quarrelsome),
            (this_or_next|eq, ":giver_reputation", lrep_cunning),
            (             eq, ":giver_reputation", lrep_debauched),
            (neg|faction_slot_eq, ":giver_faction_no", slot_faction_leader, ":giver_troop"),#Can not take the quest from the king
            (ge, "$g_talk_troop_faction_relation", 0),
            (gt, ":player_level", 5),
            (is_between, ":giver_center_no", towns_begin, towns_end),
            (assign, ":quest_importance", 1),
            (assign, ":quest_xp_reward", 300),
            (assign, ":quest_gold_reward", 1000),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_expiration_days", 10),
            (assign, ":quest_dont_give_again_period", 30),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_bring_back_runaway_serfs"),
          (try_begin),
            (neq, ":giver_reputation", lrep_goodnatured),
            (neq, ":giver_reputation", lrep_upstanding),
            (ge, "$g_talk_troop_faction_relation", 0),
            (ge, ":player_level", 5),
            (gt, ":giver_center_no", 0),#Skip if lord is outside the center
            (eq, "$g_defending_against_siege", 0),#Skip if the center is under siege (because of resting)
      
            (assign, ":cur_object_center", -1),
            (try_for_range, ":cur_village", villages_begin, villages_end),
              (party_slot_eq, ":cur_village", slot_town_lord, ":giver_troop"),
              (store_distance_to_party_from_party, ":dist", ":cur_village", ":giver_center_no"),
              (lt, ":dist", 25),
              (assign, ":cur_object_center", ":cur_village"),
            (try_end),
            (ge, ":cur_object_center", 0),#Skip if the quest giver is not the owner of any villages around the center
            (call_script, "script_cf_select_random_town_with_faction", ":giver_faction_no"),
            (assign, ":cur_target_center", reg0),
            (neq, ":cur_target_center", ":giver_center_no"),#Skip current center
            (store_distance_to_party_from_party, ":dist", ":cur_target_center", ":giver_center_no"),
            (ge, ":dist", 20),
            (assign, ":quest_target_party_template", "pt_runaway_serfs"),
            (assign, ":quest_object_center", ":cur_object_center"),
            (assign, ":quest_target_center", ":cur_target_center"),
            (assign, ":quest_importance", 1),
            (assign, ":quest_xp_reward", 200),
            (assign, ":quest_gold_reward", 150),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_expiration_days", 30),
            (assign, ":quest_dont_give_again_period", 20),
            (assign, "$qst_bring_back_runaway_serfs_num_parties_returned", 0),
            (assign, "$qst_bring_back_runaway_serfs_num_parties_fleed", 0),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_follow_spy"),
          (try_begin),
            (ge, "$g_talk_troop_faction_relation", 0),
            (neq, ":giver_reputation", lrep_goodnatured),
            (party_get_skill_level, ":tracking_skill", "p_main_party", "skl_tracking"),
            (ge, ":tracking_skill", 2),
            (ge, ":player_level", 10),
            (eq, "$g_defending_against_siege", 0), #Skip if the center is under siege (because of resting)
            (gt, ":giver_party_no", 0), #Skip if the quest giver doesn't have a party
            (gt, ":giver_center_no", 0), #skip if the quest giver is not in a center
            (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town), #skip if we are not in a town.
            (party_get_position, pos2, "p_main_party"),
            (assign, ":min_distance", 99999),
            (try_for_range, ":unused_2", 0, 10),
              (call_script, "script_cf_get_random_enemy_center", ":giver_party_no"),
              (assign, ":random_object_center", reg0),
              (party_get_position, pos3, ":random_object_center"),
              (map_get_random_position_around_position, pos4, pos3, 6),
              (get_distance_between_positions, ":cur_distance", pos2, pos4),
              (lt, ":cur_distance", ":min_distance"),
              (assign, ":min_distance", ":cur_distance"),
              (assign, ":cur_object_center", ":random_object_center"),
              (copy_position, pos63, pos4), #Do not change pos63 until quest is accepted
            (try_end),
            (gt, ":cur_object_center", 0), #Skip if there are no enemy centers

            (assign, ":quest_object_center", ":cur_object_center"),
            (assign, ":quest_dont_give_again_period", 50),
            (assign, ":result", ":quest_no"),
            (assign, "$qst_follow_spy_run_away", 0),
            (assign, "$qst_follow_spy_meeting_state", 0),
            (assign, "$qst_follow_spy_meeting_counter", 0),
            (assign, "$qst_follow_spy_spy_back_in_town", 0),
            (assign, "$qst_follow_spy_partner_back_in_town", 0),
            (assign, "$qst_follow_spy_no_active_parties", 0),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_capture_enemy_hero"),
          (try_begin),
            (eq, "$players_kingdom", ":giver_faction_no"),
            (neg|faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
            (ge, ":player_level", 15),
            (call_script, "script_cf_faction_get_random_enemy_faction", ":giver_faction_no"),#Can fail
            (assign, ":quest_target_faction", reg0),
            (assign, ":quest_expiration_days", 30),
            (assign, ":quest_dont_give_again_period", 80),
            (assign, ":quest_gold_reward", 2000),
            (assign, ":result", ":quest_no"),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_lend_companion"),
          (try_begin),
            (ge, "$g_talk_troop_faction_relation", 0),
            (assign, ":total_heroes", 0),
            (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
            (try_for_range, ":i_stack", 0, ":num_stacks"),
              (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
              (troop_is_hero, ":stack_troop"),
              (is_between, ":stack_troop", companions_begin, companions_end),
              (store_character_level, ":stack_level", ":stack_troop"),
              (ge, ":stack_level", 15),
              (assign, ":is_quest_hero", 0),
              (try_for_range, ":i_quest", 0, all_quests_end),
                (check_quest_active, ":i_quest"),
                (this_or_next|quest_slot_eq, ":i_quest", slot_quest_target_troop, ":stack_troop"),
                (quest_slot_eq, ":i_quest", slot_quest_object_troop, ":stack_troop"),
                (assign, ":is_quest_hero", 1),
              (try_end),
              (eq, ":is_quest_hero", 0),
              (val_add, ":total_heroes", 1),
            (try_end),
            (gt, ":total_heroes", 0),#Skip if party has no eligible heroes
            (store_random_in_range, ":random_hero", 0, ":total_heroes"),
            (assign, ":total_heroes", 0),
            (assign, ":cur_target_troop", -1),
            (try_for_range, ":i_stack", 0, ":num_stacks"),
              (eq, ":cur_target_troop", -1),
              (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
              (troop_is_hero, ":stack_troop"),
              (neq, ":stack_troop", "trp_player"),
              (store_character_level, ":stack_level", ":stack_troop"),
              (ge, ":stack_level", 15),
              (assign, ":is_quest_hero", 0),
              (try_for_range, ":i_quest", 0, all_quests_end),
                (check_quest_active, ":i_quest"),
                (this_or_next|quest_slot_eq, ":i_quest", slot_quest_target_troop, ":stack_troop"),
                (quest_slot_eq, ":i_quest", slot_quest_object_troop, ":stack_troop"),
                (assign, ":is_quest_hero", 1),
              (try_end),
              (eq, ":is_quest_hero", 0),
              (val_add, ":total_heroes", 1),
              (gt, ":total_heroes", ":random_hero"),
              (assign, ":cur_target_troop", ":stack_troop"),
            (try_end),
            (assign, ":quest_target_troop", ":cur_target_troop"),
            (store_current_day, ":quest_target_amount"),
            (val_add, ":quest_target_amount", 8),

            (assign, ":quest_importance", 1),
            (assign, ":quest_xp_reward", 300),
            (assign, ":quest_gold_reward", 400),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_dont_give_again_period", 30),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_collect_debt"),
          (try_begin),
            (ge, "$g_talk_troop_faction_relation", 0),
          # Find a vassal (within the same kingdom?) 
            (call_script, "script_cf_get_random_lord_in_a_center_with_faction", ":giver_faction_no"),#Can fail
            (assign, ":quest_target_troop", reg0),
            (neq, ":quest_target_troop", ":giver_troop"),#Skip himself
            (call_script, "script_get_troop_attached_party", ":quest_target_troop"),
            (assign, ":quest_target_center", reg0),#cur_target_center will definitely be a valid center
            (neq,":giver_center_no", ":quest_target_center"),#Skip current center

            (assign, ":quest_xp_reward", 30),
            (assign, ":quest_gold_reward", 40),
            (assign, ":result", ":quest_no"),
            (store_random_in_range, ":quest_target_amount", 6, 9),
            (val_mul, ":quest_target_amount", 500),
            (store_div, ":quest_convince_value", ":quest_target_amount", 5),
            (assign, ":quest_expiration_days", 90),
            (assign, ":quest_dont_give_again_period", 20),
          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_capture_conspirators"),
##          (try_begin),
##            (eq, 1,0), #TODO: disable this for now
##            (ge, ":player_level", 10),
##            (is_between, ":giver_center_no", towns_begin, towns_end),#Skip if quest giver's center is not a town
##            (party_slot_eq, ":giver_center_no", slot_town_lord, ":giver_troop"),#Skip if the current center is not ruled by the quest giver
##            (call_script, "script_cf_get_random_kingdom_hero", ":giver_faction_no"),#Can fail
##
##            (assign, ":quest_target_troop", reg0),
##            (assign, ":quest_target_center", ":giver_center_no"),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 10),
##            (assign, ":quest_gold_reward", 10),
##            (assign, ":result", ":quest_no"),
##            (store_character_level, ":cur_level"),
##            (val_div, ":cur_level", 5),
##            (val_max, ":cur_level", 3),
##            (store_add, ":max_parties", 4, ":cur_level"),
##            (store_random_in_range, "$qst_capture_conspirators_num_parties_to_spawn", 4, ":max_parties"),
##            (assign, "$qst_capture_conspirators_num_troops_to_capture", 0),
##            (assign, "$qst_capture_conspirators_num_parties_spawned", 0),
##            (assign, "$qst_capture_conspirators_leave_meeting_counter", 0),
##            (assign, "$qst_capture_conspirators_party_1", 0),
##            (assign, "$qst_capture_conspirators_party_2", 0),
##            (assign, "$qst_capture_conspirators_party_3", 0),
##            (assign, "$qst_capture_conspirators_party_4", 0),
##            (assign, "$qst_capture_conspirators_party_5", 0),
##            (assign, "$qst_capture_conspirators_party_6", 0),
##            (assign, "$qst_capture_conspirators_party_7", 0),
##          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_defend_nobles_against_peasants"),
##          (try_begin),
##            (eq, 1,0), #TODO: disable this for now
##            (ge, ":player_level", 10),
##            (is_between, ":giver_center_no", towns_begin, towns_end),#Skip if quest giver's center is not a town
##            (party_slot_eq, ":giver_center_no", slot_town_lord, ":giver_troop"),#Skip if the current center is not ruled by the quest giver
##
##            (assign, ":quest_target_center", ":giver_center_no"),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 10),
##            (assign, ":quest_gold_reward", 10),
##            (assign, ":result", ":quest_no"),
##            (store_character_level, ":cur_level"),
##            (val_div, ":cur_level", 5),
##            (val_max, ":cur_level", 4),
##            (store_add, ":max_parties", 4, ":cur_level"),
##            (store_random_in_range, "$qst_defend_nobles_against_peasants_num_peasant_parties_to_spawn", 4, ":cur_level"),
##            (store_random_in_range, "$qst_defend_nobles_against_peasants_num_noble_parties_to_spawn", 4, ":cur_level"),
##            (assign, "$qst_defend_nobles_against_peasants_num_nobles_to_save", 0),
##            (assign, "$qst_defend_nobles_against_peasants_num_nobles_saved", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_1", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_2", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_3", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_4", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_5", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_6", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_7", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_8", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_1", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_2", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_3", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_4", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_5", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_6", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_7", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_8", 0),
##          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_incriminate_loyal_commander"),
          (try_begin),
            (neq, ":giver_reputation", lrep_upstanding),
            (neq, ":giver_reputation", lrep_goodnatured),
            (eq, "$players_kingdom", ":giver_faction_no"),
            (ge, ":player_level", 10),
            (faction_slot_eq, ":giver_faction_no", slot_faction_leader, ":giver_troop"),
            (assign, ":try_times", 1),
            (assign, ":found", 0),
            (try_for_range, ":unused", 0, ":try_times"),
              (call_script, "script_cf_faction_get_random_enemy_faction", ":giver_faction_no"),#Can fail
              (assign, ":cur_target_faction", reg0),

              (faction_get_slot, ":cur_target_troop", ":cur_target_faction", slot_faction_leader),
              (assign, ":num_centerless_heroes", 0),
              (try_for_range, ":cur_kingdom_hero", kingdom_heroes_begin, kingdom_heroes_end),
                (troop_slot_eq, ":cur_kingdom_hero", slot_troop_occupation, slto_kingdom_hero),
                #(troop_slot_eq, ":cur_kingdom_hero", slot_troop_is_prisoner, 0),
                (neg|troop_slot_ge, ":cur_kingdom_hero", slot_troop_prisoner_of_party, 0),
                (neq, ":cur_target_troop", ":cur_kingdom_hero"),
                (store_troop_faction, ":cur_kingdom_hero_faction", ":cur_kingdom_hero"),
                (eq, ":cur_target_faction", ":cur_kingdom_hero_faction"),
##                (call_script, "script_get_number_of_hero_centers", ":cur_kingdom_hero"),
##                (eq, reg0, 0),
                (val_add, ":num_centerless_heroes", 1),
              (try_end),
              (gt, ":num_centerless_heroes", 0),
              (assign, ":cur_object_troop", -1),
              (store_random_in_range, ":random_kingdom_hero", 0, ":num_centerless_heroes"),
              (try_for_range, ":cur_kingdom_hero", kingdom_heroes_begin, kingdom_heroes_end),
                (eq, ":cur_object_troop", -1),
                (troop_slot_eq, ":cur_kingdom_hero", slot_troop_occupation, slto_kingdom_hero),
                (neq, ":cur_target_troop", ":cur_kingdom_hero"),
                (store_troop_faction, ":cur_kingdom_hero_faction", ":cur_kingdom_hero"),
                (eq, ":cur_target_faction", ":cur_kingdom_hero_faction"),
##                (call_script, "script_get_number_of_hero_centers", ":cur_kingdom_hero"),
##                (eq, reg0, 0),
                (val_sub, ":random_kingdom_hero", 1),
                (lt, ":random_kingdom_hero", 0),
                (assign, ":cur_object_troop", ":cur_kingdom_hero"),
              (try_end),

              (assign, ":cur_target_center", -1),
              (call_script, "script_get_troop_attached_party", ":cur_target_troop"),
              (is_between, reg0, towns_begin, towns_end),
              (party_slot_eq, reg0, slot_town_lord, ":cur_target_troop"),
              (assign, ":cur_target_center", reg0),

              (assign, ":try_times", -1),#Exit the second loop
              (assign, ":found", 1),
            (try_end),
            (eq, ":found", 1),

            (assign, "$incriminate_quest_sacrificed_troop", 0),

            (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
            (try_for_range, ":i_stack", 1, ":num_stacks"),
              (eq ,"$incriminate_quest_sacrificed_troop", 0),
              (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
              (neg|troop_is_hero, ":stack_troop"),
              (store_character_level, ":stack_troop_level", ":stack_troop"),
              (ge, ":stack_troop_level", 25),
              (assign, "$incriminate_quest_sacrificed_troop", ":stack_troop"),
            (try_end),
            (gt, "$incriminate_quest_sacrificed_troop", 0),

            (assign, ":quest_target_troop", ":cur_target_troop"),
            (assign, ":quest_object_troop", ":cur_object_troop"),
            (assign, ":quest_target_center", ":cur_target_center"),
            (assign, ":quest_target_faction", ":cur_target_faction"),

            (assign, ":quest_importance", 1),
            (assign, ":quest_xp_reward", 700),
            (assign, ":quest_gold_reward", 1000),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_expiration_days", 30),
            (assign, ":quest_dont_give_again_period", 180),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_capture_prisoners"),
          (try_begin),
            (eq, "$players_kingdom", ":giver_faction_no"),
            (call_script, "script_cf_faction_get_random_enemy_faction", ":giver_faction_no"),#Can fail
            (assign, ":cur_target_faction", reg0),
            (store_add, ":max_tier_no", slot_faction_tier_5_troop, 1),
            (store_random_in_range, ":random_tier_no", slot_faction_tier_2_troop, ":max_tier_no"),
            (faction_get_slot, ":cur_target_troop", ":cur_target_faction", ":random_tier_no"),
            (gt, ":cur_target_troop", 0),
            (store_random_in_range, ":quest_target_amount", 3, 7),
            (assign, ":quest_target_troop", ":cur_target_troop"),
            (assign, ":quest_target_faction", ":cur_target_faction"),
            (assign, ":quest_importance", 1),
            (store_character_level, ":quest_gold_reward", ":cur_target_troop"),
            (val_add, ":quest_gold_reward", 5),
            (val_mul, ":quest_gold_reward", ":quest_gold_reward"),
            (val_div, ":quest_gold_reward", 5),
            (val_mul, ":quest_gold_reward", ":quest_target_amount"),
            (assign, ":quest_xp_reward", ":quest_gold_reward"),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_expiration_days", 90),
            (assign, ":quest_dont_give_again_period", 20),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_rescue_prisoners"),
          (try_begin),
            (store_character_level, ":quest_target_amount", "trp_player"),
            (val_clamp, ":quest_target_amount", 5, 21),
            (assign, ":quest_importance", 1),
            (store_mul, ":quest_gold_reward", ":quest_target_amount", 20),
            (assign, ":quest_xp_reward", ":quest_gold_reward"),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_expiration_days", 60),
            (assign, ":quest_dont_give_again_period", 20),
          (try_end),
        (try_end),
      (try_end),
      (try_begin),
        (neq, ":result", -1),
        
        (try_begin),
          (ge, ":quest_target_center", 0),
          (store_faction_of_party, ":quest_target_faction", ":quest_target_center"),
        (try_end),
        
        (quest_set_slot, ":result", slot_quest_target_troop, ":quest_target_troop"),
        (quest_set_slot, ":result", slot_quest_target_center, ":quest_target_center"),
        (quest_set_slot, ":result", slot_quest_object_troop, ":quest_object_troop"),
        (quest_set_slot, ":result", slot_quest_target_faction, ":quest_target_faction"),
        (quest_set_slot, ":result", slot_quest_object_faction, ":quest_object_faction"),
        (quest_set_slot, ":result", slot_quest_object_center, ":quest_object_center"),
        (quest_set_slot, ":result", slot_quest_target_party, ":quest_target_party"),
        (quest_set_slot, ":result", slot_quest_target_party_template, ":quest_target_party_template"),
        (quest_set_slot, ":result", slot_quest_target_amount, ":quest_target_amount"),
        (quest_set_slot, ":result", slot_quest_importance, ":quest_importance"),
        (quest_set_slot, ":result", slot_quest_xp_reward, ":quest_xp_reward"),
        (quest_set_slot, ":result", slot_quest_gold_reward, ":quest_gold_reward"),
        (quest_set_slot, ":result", slot_quest_convince_value, ":quest_convince_value"),
        (quest_set_slot, ":result", slot_quest_expiration_days, ":quest_expiration_days"),
        (quest_set_slot, ":result", slot_quest_dont_give_again_period, ":quest_dont_give_again_period"),
        (quest_set_slot, ":result", slot_quest_current_state, 0),
        (quest_set_slot, ":result", slot_quest_giver_troop, ":giver_troop"),
        (quest_set_slot, ":result", slot_quest_giver_center, ":giver_center_no"),
        (quest_set_slot, ":result", slot_quest_target_dna, ":quest_target_dna"),
        (quest_set_slot, ":result", slot_quest_target_item, ":quest_target_item"),
      (try_end),
      
      (assign, reg0, ":result"),
  ]),
  
  # script_cf_get_random_enemy_center_within_range
  # INPUT: arg1 = party_no, arg2 = range (in kms)
  #OUTPUT: reg0 = center_no
  ("cf_get_random_enemy_center_within_range",
    [
      (store_script_param, ":party_no", 1),
      (store_script_param, ":range", 2),

      (assign, ":num_centers", 0),
      (store_faction_of_party, ":faction_no", ":party_no"),
      (try_for_range, ":cur_center", centers_begin, centers_end),
        (party_is_active, ":cur_center"), #TLD
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (lt, ":cur_relation", 0),
        (store_distance_to_party_from_party, ":dist", ":party_no", ":cur_center"),
        (le, ":dist", ":range"),
        (val_add, ":num_centers", 1),
      (try_end),
      (gt, ":num_centers", 0),
      (store_random_in_range, ":random_center", 0, ":num_centers"),
      (assign, ":end_cond", centers_end),
      (try_for_range, ":cur_center", centers_begin, ":end_cond"),
        (party_is_active, ":cur_center"), #TLD
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (lt, ":cur_relation", 0),
        (store_distance_to_party_from_party, ":dist", ":party_no", ":cur_center"),
        (le, ":dist", ":range"),
        (val_sub, ":random_center", 1),
        (lt, ":random_center", 0),
        (assign, ":result", ":cur_center"),
        (assign, ":end_cond", 0),#break
      (try_end),
      (assign, reg0, ":result"),
  ]),
  
  # script_cf_faction_get_random_enemy_faction
  # INPUT: arg1 = faction_no
  #OUTPUT: reg0 = faction_no (Can fail)
  ("cf_faction_get_random_enemy_faction",
    [
      (store_script_param_1, ":faction_no"),
      
      (assign, ":result", -1),
      (assign, ":count_factions", 0),
      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (le, ":cur_relation", -1),
        (val_add, ":count_factions", 1),
      (try_end),
      (store_random_in_range,":random_faction",0,":count_factions"),
      (assign, ":count_factions", 0),
      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (eq, ":result", -1),
        (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (le, ":cur_relation", -1),
        (val_add, ":count_factions", 1),
        (gt, ":count_factions", ":random_faction"),
        (assign, ":result", ":cur_faction"),
      (try_end),
      
      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ]),

  # script_cf_faction_get_random_friendly_faction
  # INPUT: arg1 = faction_no
  #OUTPUT: reg0 = faction_no (Can fail)
  ("cf_faction_get_random_friendly_faction",
    [
      (store_script_param_1, ":faction_no"),
      
      (assign, ":result", -1),
      (assign, ":count_factions", 0),
      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
        (neq, ":cur_faction", ":faction_no"),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (ge, ":cur_relation", 0),
        (val_add, ":count_factions", 1),
      (try_end),
      (store_random_in_range,":random_faction",0,":count_factions"),
      (assign, ":count_factions", 0),
      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (eq, ":result", -1),
        (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
        (neq, ":cur_faction", ":faction_no"),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (ge, ":cur_relation", 0),
        (val_add, ":count_factions", 1),
        (gt, ":count_factions", ":random_faction"),
        (assign, ":result", ":cur_faction"),
      (try_end),
      
      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ]),  
  
  # script_cf_troop_get_random_enemy_troop_with_occupation
  # Input: arg1 = troop_no,
  # Output: reg0 = enemy_troop_no (Can fail)
  ("cf_troop_get_random_enemy_troop_with_occupation",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":occupation"),
      
      (assign, ":result", -1),
      (assign, ":count_enemies", 0),
      (try_for_range, ":cur_slot", slot_troop_enemies_begin, slot_troop_enemies_end),
        (troop_get_slot, ":cur_enemy", ":troop_no", ":cur_slot"),
        (gt, ":cur_enemy", 0),
        (troop_slot_eq, ":cur_enemy", slot_troop_occupation, ":occupation"),
        (val_add, ":count_enemies", 1),
      (try_end),
      (store_random_in_range,":random_enemy",0,":count_enemies"),
      (assign, ":count_enemies", 0),
      (try_for_range, ":cur_slot", slot_troop_enemies_begin, slot_troop_enemies_end),
        (eq, ":result", -1),
        (troop_get_slot, ":cur_enemy", ":troop_no", ":cur_slot"),
        (gt, ":cur_enemy", 0),
        (troop_slot_eq, ":cur_enemy", slot_troop_occupation, ":occupation"),
        (val_add, ":count_enemies", 1),
        (gt, ":count_enemies", ":random_enemy"),
        (assign, ":result", ":cur_enemy"),
      (try_end),
      
      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ]),
  
  
##  # script_cf_troop_get_random_enemy_troop_as_a_town_lord
##  # Input: arg1 = troop_no
##  # Output: reg0 = enemy_troop_no (Can fail)
##  ("cf_troop_get_random_enemy_troop_as_a_town_lord",
##    [
##      (store_script_param_1, ":troop_no"),
##      
##      (assign, ":result", -1),
##      (assign, ":count_enemies", 0),
##      (try_for_range, ":cur_slot", slot_troop_enemies_begin, slot_troop_enemies_end),
##        (troop_get_slot, ":cur_enemy", ":troop_no", ":cur_slot"),
##        (gt, ":cur_enemy", 0),
##        (troop_slot_eq, ":cur_enemy", slot_troop_occupation, slto_kingdom_hero),
##        (call_script, "script_get_number_of_hero_centers", ":cur_enemy"),
##        (gt, reg0, 0),
##        (val_add, ":count_enemies", 1),
##      (try_end),
##      (store_random_in_range,":random_enemy",0,":count_enemies"),
##      (assign, ":count_enemies", 0),
##      (try_for_range, ":cur_slot", slot_troop_enemies_begin, slot_troop_enemies_end),
##        (eq, ":result", -1),
##        (troop_get_slot, ":cur_enemy", ":troop_no", ":cur_slot"),
##        (gt, ":cur_enemy", 0),
##        (troop_slot_eq, ":cur_enemy", slot_troop_occupation, slto_kingdom_hero),
##        (call_script, "script_get_number_of_hero_centers", ":cur_enemy"),
##        (gt, reg0, 0),
##        (val_add, ":count_enemies", 1),
##        (gt, ":count_enemies", ":random_enemy"),
##        (assign, ":result", ":cur_enemy"),
##      (try_end),
##      (neq, ":result", -1),
##      (assign, reg0, ":result"),
##  ]),
  
  
  ##  # script_cf_get_random_enemy_with_valid_slot
  ##  # Input: arg1 = faction_no, arg2 = slot_no
  ##  # Output: reg0 = faction_no (Can fail)
  ##  ("cf_get_random_enemy_with_valid_slot",
  ##    [
  ##      (store_script_param_1, ":faction_no"),
  ##      (store_script_param_2, ":slot_no"),
  ##
  ##      (assign, ":result", -1),
  ##      (assign, ":count_factions", 0),
  ##      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
  ##        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
  ##        (le, ":cur_relation", -10),
  ##        (faction_get_slot, ":cur_value", ":cur_faction", ":slot_no"),
  ##        (gt, ":cur_value", 0),#Checking validity
  ##        (val_add, ":count_factions", 1),
  ##      (try_end),
  ##      (store_random_in_range,":random_faction",0,":count_factions"),
  ##      (assign, ":count_factions", 0),
  ##      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
  ##        (eq, ":result", -1),
  ##        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
  ##        (le, ":cur_relation", -10),
  ##        (faction_get_slot, ":cur_value", ":cur_faction", ":slot_no"),
  ##        (gt, ":cur_value", 0),#Checking validity
  ##        (val_add, ":count_factions", 1),
  ##        (gt, ":count_factions", ":random_faction"),
  ##        (assign, ":result", ":cur_faction"),
  ##      (try_end),
  ##
  ##      (neq, ":result", -1),
  ##      (assign, reg0, ":result"),
  ##  ]),
  
  
##  # script_cf_get_random_kingdom_hero
##  # Input: arg1 = faction_no
##  # Output: reg0 = troop_no (Can fail)
##  ("cf_get_random_kingdom_hero",
##    [
##      (store_script_param_1, ":faction_no"),
##      (assign, ":count_heroes", 0),
##      (try_for_range, ":center_no", centers_begin, centers_end),
##        (store_faction_of_party, ":cur_faction", ":center_no"),
##        (eq, ":cur_faction", ":faction_no"),
##        (party_get_slot, ":cur_lord", ":center_no", slot_town_lord),
##        (is_between, ":cur_lord", heroes_begin, heroes_end),
##        (val_add, ":count_heroes", 1),
##      (try_end),
##      (store_random_in_range, ":random_hero", 0, ":count_heroes"),
##      (assign, ":result", -1),
##      (assign, ":count_heroes", 0),
##      (try_for_range, ":center_no", centers_begin, centers_end),
##        (eq, ":result", -1),
##        (store_faction_of_party, ":cur_faction", ":center_no"),
##        (eq, ":cur_faction", ":faction_no"),
##        (party_get_slot, ":cur_lord", ":center_no", slot_town_lord),
##        (is_between, ":cur_lord", heroes_begin, heroes_end),
##        (val_add, ":count_heroes", 1),
##        (lt, ":random_hero", ":count_heroes"),
##        (assign, ":result", ":cur_lord"),
##      (try_end),
##      (neq, ":result", -1),
##      (assign, reg0, ":result"),
##  ]),
  
  
  # script_cf_get_random_kingdom_hero_as_lover
  # Input: arg1 = troop_no (of the lady)
  # Output: reg0 = troop_no (of the hero) (Can fail)
  ("cf_get_random_kingdom_hero_as_lover",
    [
      #      (store_script_param_1, ":cur_lady"),
      
      
      #      (troop_get_slot, ":cur_father", ":cur_lady", slot_troop_father),
      #      (troop_get_slot, ":fathers_rank", ":cur_father", slot_troop_kingdom_rank),
      (assign, ":result", -1),
      (assign, ":count_heroes", 0),
      (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
        (troop_slot_eq, ":troop_no", slot_troop_lover, 0),
        (troop_slot_eq, ":troop_no", slot_troop_spouse, 0),
        #        (troop_get_slot, ":cur_rank", ":troop_no", slot_troop_kingdom_rank),
        #        (lt, ":cur_rank", ":fathers_rank"), # Only heroes with lower ranks may be the lovers of the daughters
        (val_add, ":count_heroes", 1),
      (try_end),
      (store_random_in_range,":random_hero",0,":count_heroes"),
      (assign, ":count_heroes", 0),
      (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
        (eq, ":result", -1),
        (troop_slot_eq, ":troop_no", slot_troop_lover, 0),
        (troop_slot_eq, ":troop_no", slot_troop_spouse, 0),
        #        (troop_get_slot, ":cur_rank", ":troop_no", slot_troop_kingdom_rank),
        #        (lt, ":cur_rank", ":fathers_rank"), # Only heroes with lower ranks may be the lovers of the daughters
        (val_add, ":count_heroes", 1),
        (gt, ":count_heroes", ":random_hero"),
        (assign, ":result", ":troop_no"),
      (try_end),
      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ]),
  
  
##  # script_cf_get_random_siege_location_with_faction
##  # Input: arg1 = faction_no
##  # Output: reg0 = center_no, Can Fail!
##  ("cf_get_random_siege_location_with_faction",
##    [
##      (store_script_param_1, ":faction_no"),
##      (assign, ":result", -1),
##      (assign, ":count_sieges", 0),
##      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
##        (party_get_battle_opponent, ":besieger_party", ":center_no"),
##        (gt, ":besieger_party", 0),
##        (store_faction_of_party, ":cur_faction_no", ":center_no"),
##        (eq, ":cur_faction_no", ":faction_no"),
##        (val_add, ":count_sieges", 1),
##      (try_end),
##      (store_random_in_range,":random_center",0,":count_sieges"),
##      (assign, ":count_sieges", 0),
##      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
##        (eq, ":result", -1),
##        (party_get_battle_opponent, ":besieger_party", ":center_no"),
##        (gt, ":besieger_party", 0),
##        (store_faction_of_party, ":cur_faction_no", ":center_no"),
##        (eq, ":cur_faction_no", ":faction_no"),
##        (val_add, ":count_sieges", 1),
##        (gt, ":count_sieges", ":random_center"),
##        (assign, ":result", ":center_no"),
##      (try_end),
##      (neq, ":result", -1),
##      (assign, reg0, ":result"),
##  ]),
  
##  # script_cf_get_random_siege_location_with_attacker_faction
##  # Input: arg1 = faction_no
##  # Output: reg0 = center_no, Can Fail!
##  ("cf_get_random_siege_location_with_attacker_faction",
##    [
##      (store_script_param_1, ":faction_no"),
##      (assign, ":result", -1),
##      (assign, ":count_sieges", 0),
##      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
##        (party_get_battle_opponent, ":besieger_party", ":center_no"),
##        (gt, ":besieger_party", 0),
##        (store_faction_of_party, ":cur_faction_no", ":besieger_party"),
##        (eq, ":cur_faction_no", ":faction_no"),
##        (val_add, ":count_sieges", 1),
##      (try_end),
##      (store_random_in_range,":random_center",0,":count_sieges"),
##      (assign, ":count_sieges", 0),
##      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
##        (eq, ":result", -1),
##        (party_get_battle_opponent, ":besieger_party", ":center_no"),
##        (gt, ":besieger_party", 0),
##        (store_faction_of_party, ":cur_faction_no", ":besieger_party"),
##        (eq, ":cur_faction_no", ":faction_no"),
##        (val_add, ":count_sieges", 1),
##        (gt, ":count_sieges", ":random_center"),
##        (assign, ":result", ":center_no"),
##      (try_end),
##      (neq, ":result", -1),
##      (assign, reg0, ":result"),
##  ]),
  
  
  
##  # script_cf_get_number_of_random_troops_from_party
##  # Input: arg1 = party_no, arg2 = number of troops to remove
##  # Output: reg0 = troop_no, Can fail if there are no slots having the required number of units!
##  ("cf_get_number_of_random_troops_from_party",
##    [
##      (store_script_param_1, ":party_no"),
##      (store_script_param_2, ":no_to_remove"),
##      
##      (assign, ":result", -1),
##      (assign, ":count_stacks", 0),
##      
##      (party_get_num_companion_stacks, ":num_stacks",":party_no"),
##      (try_for_range, ":i_stack", 0, ":num_stacks"),
##        (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
##        (party_stack_get_num_wounded, ":num_wounded",":party_no",":i_stack"),
##        (val_sub, ":stack_size", ":num_wounded"),
##        (ge, ":stack_size", ":no_to_remove"),
##        (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
##        (neg|troop_is_hero, ":stack_troop"),
##        (val_add, ":count_stacks", 1),
##      (try_end),
##      (store_random_in_range,":random_stack",0,":count_stacks"),
##      (assign, ":count_stacks", 0),
##      (try_for_range, ":i_stack", 0, ":num_stacks"),
##        (eq, ":result", -1),
##        (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
##        (party_stack_get_num_wounded, ":num_wounded",":party_no",":i_stack"),
##        (val_sub, ":stack_size", ":num_wounded"),
##        (ge, ":stack_size", ":no_to_remove"),
##        (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
##        (neg|troop_is_hero, ":stack_troop"),
##        (val_add, ":count_stacks", 1),
##        (gt, ":count_stacks", ":random_stack"),
##        (assign, ":result", ":stack_troop"),
##      (try_end),
##      
##      (neq, ":result", -1),
##      (assign, reg0, ":result"),
##  ]),
  
  
  
  
  # script_cf_get_random_lord_in_a_center_with_faction
  # INPUT: arg1 = faction_no
  #OUTPUT: reg0 = troop_no, Can Fail!
  ("cf_get_random_lord_in_a_center_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (eq, ":faction_no", ":lord_faction_no"),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (party_get_attached_to, ":lord_attachment", ":lord_party"),
        (is_between, ":lord_attachment", centers_begin, centers_end), #is troop in a center?
        (val_add, ":count_lords", 1),
      (try_end),
      (store_random_in_range, ":random_lord", 0, ":count_lords"),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (eq, ":result", -1),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (eq, ":faction_no", ":lord_faction_no"),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (party_get_attached_to, ":lord_attachment", ":lord_party"),
        (is_between, ":lord_attachment", centers_begin, centers_end), #is troop in a center?
        (val_add, ":count_lords", 1),
        (lt, ":random_lord", ":count_lords"),
        (assign, ":result", ":lord_no"),
      (try_end),
      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ]),

  # script_cf_get_random_lord_except_king_with_faction
  # Input: arg1 = faction_no
  # Output: reg0 = troop_no, Can Fail!
  ("cf_get_random_lord_except_king_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (eq, ":faction_no", ":lord_faction_no"),
        (neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":lord_no"),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (val_add, ":count_lords", 1),
      (try_end),
      (store_random_in_range, ":random_lord", 0, ":count_lords"),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (eq, ":result", -1),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (eq, ":faction_no", ":lord_faction_no"),
        (neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":lord_no"),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (val_add, ":count_lords", 1),
        (lt, ":random_lord", ":count_lords"),
        (assign, ":result", ":lord_no"),
      (try_end),
      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ]),
  
  
  # script_cf_get_random_lord_from_another_faction_in_a_center
  # Input: arg1 = faction_no
  # Output: reg0 = troop_no, Can Fail!
  ("cf_get_random_lord_from_another_faction_in_a_center",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (neq, ":lord_faction_no", ":faction_no"),
        (store_relation, ":our_relation", ":lord_faction_no", "fac_player_supporters_faction"),
        (store_relation, ":lord_relation", ":lord_faction_no", ":faction_no"),
        (lt, ":lord_relation", 0),
        (ge, ":our_relation", 0),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (party_get_attached_to, ":lord_attachment", ":lord_party"),
        (is_between, ":lord_attachment", centers_begin, centers_end), #is troop in a center?
        (val_add, ":count_lords", 1),
      (try_end),
      (store_random_in_range, ":random_lord", 0, ":count_lords"),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (eq, ":result", -1),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (neq, ":lord_faction_no", ":faction_no"),
        (store_relation, ":our_relation", ":lord_faction_no", "fac_player_supporters_faction"),
        (store_relation, ":lord_relation", ":lord_faction_no", ":faction_no"),
        (lt, ":lord_relation", 0),
        (ge, ":our_relation", 0),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (party_get_attached_to, ":lord_attachment", ":lord_party"),
        (is_between, ":lord_attachment", centers_begin, centers_end), #is troop in a center?
        (val_add, ":count_lords", 1),
        (lt, ":random_lord", ":count_lords"),
        (assign, ":result", ":lord_no"),
      (try_end),
      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ]),
  
  # script_get_closest_walled_center
  # Input: arg1 = party_no
  # Output: reg0 = center_no (closest)
  ("get_closest_walled_center",
    [
      (store_script_param_1, ":party_no"),
      (assign, ":min_distance", 9999999),
      (assign, reg0, -1),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (party_is_active, ":center_no"), #TLD
        (store_distance_to_party_from_party, ":party_distance", ":party_no", ":center_no"),
        (lt, ":party_distance", ":min_distance"),
        (assign, ":min_distance", ":party_distance"),
        (assign, reg0, ":center_no"),
      (try_end),
  ]),  
  
  # script_get_closest_center
  # Input: arg1 = party_no
  # Output: reg0 = center_no (closest)
  ("get_closest_center",
    [
      (store_script_param_1, ":party_no"),
      (assign, ":min_distance", 9999999),
      (assign, reg0, -1),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
        (store_distance_to_party_from_party, ":party_distance", ":party_no", ":center_no"),
        (lt, ":party_distance", ":min_distance"),
        (assign, ":min_distance", ":party_distance"),
        (assign, reg0, ":center_no"),
      (try_end),
  ]),
  
  
  # script_get_closest_center_of_faction
  # Input: arg1 = party_no, arg2 = kingdom_no
  # Output: reg0 = center_no (closest)
  ("get_closest_center_of_faction",
    [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":kingdom_no"),
      (assign, ":min_distance", 99999),
      (assign, ":result", -1),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
        (store_faction_of_party, ":faction_no", ":center_no"),
        (eq, ":faction_no", ":kingdom_no"),
        (store_distance_to_party_from_party, ":party_distance", ":party_no", ":center_no"),
        (lt, ":party_distance", ":min_distance"),
        (assign, ":min_distance", ":party_distance"),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
  
  # script_get_closest_walled_center_of_faction
  # Input: arg1 = party_no, arg2 = kingdom_no
  # Output: reg0 = center_no (closest)
  ("get_closest_walled_center_of_faction",
    [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":kingdom_no"),
      (assign, ":min_distance", 99999),
      (assign, ":result", -1),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (party_is_active, ":center_no"), #TLD
        (store_faction_of_party, ":faction_no", ":center_no"),
        (eq, ":faction_no", ":kingdom_no"),
        (store_distance_to_party_from_party, ":party_distance", ":party_no", ":center_no"),
        (lt, ":party_distance", ":min_distance"),
        (assign, ":min_distance", ":party_distance"),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
  
  
##  # script_get_closest_town_of_faction
##  # Input: arg1 = party_no, arg2 = kingdom_no
##  # Output: reg0 = center_no (closest)
##  ("get_closest_town_of_faction",
##    [
##      (store_script_param_1, ":party_no"),
##      (store_script_param_2, ":kingdom_no"),
##      (assign, ":min_distance", 9999999),
##      (assign, ":result", -1),
##      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
##        (store_faction_of_party, ":faction_no", ":center_no"),
##        (eq, ":faction_no", ":kingdom_no"),
##        (party_slot_eq, ":center_no", slot_party_type, spt_town),
##        (store_distance_to_party_from_party, ":party_distance", ":party_no", ":center_no"),
##        (lt, ":party_distance", ":min_distance"),
##        (assign, ":min_distance", ":party_distance"),
##        (assign, ":result", ":center_no"),
##      (try_end),
##      (assign, reg0, ":result"),
##  ]),

  
  # script_let_nearby_parties_join_current_battle
  # Input: arg1 = besiege_mode, arg2 = dont_add_friends
  # Output: none
  ("let_nearby_parties_join_current_battle",
    [
      (store_script_param, ":besiege_mode", 1),
      (store_script_param, ":dont_add_friends", 2),
      (assign, ":join_distance", 5),
      (try_begin),
        (is_currently_night),
        (assign, ":join_distance", 3),
      (try_end),
      (try_for_parties, ":party_no"),
        (party_is_active, ":party_no"), # Warband fix
        (party_get_battle_opponent, ":opponent",":party_no"),
        (lt, ":opponent", 0), #party is not itself involved in a battle
        (party_get_attached_to, ":attached_to",":party_no"),
        (lt, ":attached_to", 0), #party is not attached to another party
        (get_party_ai_behavior, ":behavior", ":party_no"),
        (neq, ":behavior", ai_bhvr_in_town),

      
        (store_distance_to_party_from_party, ":distance", ":party_no", "p_main_party"),
        (lt, ":distance", ":join_distance"),

        (store_faction_of_party, ":faction_no", ":party_no"),
        (store_faction_of_party, ":enemy_faction", "$g_enemy_party"),
        (try_begin),
          (eq, ":faction_no", "fac_player_supporters_faction"),
          (assign, ":reln_with_player", 100),
        (else_try),
          (store_relation, ":reln_with_player", ":faction_no", "fac_player_supporters_faction"),
        (try_end),
        (try_begin),
          (eq, ":faction_no", ":enemy_faction"),
          (assign, ":reln_with_enemy", 100),
        (else_try),
          (store_relation, ":reln_with_enemy", ":faction_no", ":enemy_faction"),
        (try_end),

        (assign, ":enemy_side", 1),
        (try_begin),
          (neq, "$g_enemy_party", "$g_encountered_party"),
          (assign, ":enemy_side", 2),
        (try_end),

        (try_begin),
          (eq, ":besiege_mode", 0),
          (lt, ":reln_with_player", 0),
          (gt, ":reln_with_enemy", 0),
          (party_get_slot, ":party_type", ":party_no"),
          #(eq, ":party_type", spt_kingdom_hero_party), #TLD: all parties can join
          (neq, ":party_type", spt_town), #...except towns

          (get_party_ai_behavior, ":ai_bhvr", ":party_no"),
          (neq, ":ai_bhvr", ai_bhvr_avoid_party),
          (party_quick_attach_to_current_battle, ":party_no", ":enemy_side"), #attach as enemy
          (str_store_party_name, s1, ":party_no"),
          (display_message, "str_s1_joined_battle_enemy", color_bad_news),
        (else_try),
          (eq, ":dont_add_friends", 0),
          (gt, ":reln_with_player", 0),
          (lt, ":reln_with_enemy", 0),
          (assign, ":do_join", 1),
          (try_begin),
            (eq, ":besiege_mode", 1),
            (assign, ":do_join", 0),
            (eq, ":faction_no", "$players_kingdom"),
            (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
            (assign, ":do_join", 1),
          (try_end),
          (eq, ":do_join", 1),
          (party_get_slot, ":party_type", ":party_no"),
          #(eq, ":party_type", spt_kingdom_hero_party), #TLD: all parties can join
          (neq, ":party_type", spt_town), #...except towns

          #MV commented out personal relations
          #(party_stack_get_troop_id, ":leader", ":party_no", 0),
   #       (troop_get_slot, ":player_relation", ":leader", slot_troop_player_relation),
          #(call_script, "script_troop_get_player_relation", ":leader"),
          #(assign, ":player_relation", reg0),
          #(ge, ":player_relation", 0),
          (party_quick_attach_to_current_battle, ":party_no", 0), #attach as friend
          (str_store_party_name, s1, ":party_no"),
          (display_message, "str_s1_joined_battle_friend", color_good_news),
        (try_end),
      (try_end),
  ]),
    
  # script_party_wound_all_members_aux
  # Input: arg1 = party_no
  ("party_wound_all_members_aux",
    [
      (store_script_param_1, ":party_no"),
      
      (party_get_num_companion_stacks, ":num_stacks",":party_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
        (try_begin),
          (neg|troop_is_hero, ":stack_troop"),
          (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
          (party_wound_members, ":party_no", ":stack_troop", ":stack_size"),
        (else_try),
          (troop_set_health, ":stack_troop", 0),
        (try_end),
      (try_end),
      (party_get_num_attached_parties, ":num_attached_parties", ":party_no"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":party_no", ":attached_party_rank"),
        (call_script, "script_party_wound_all_members_aux", ":attached_party"),
      (try_end),
      
  ]),
  
  # script_party_wound_all_members. identical to script_party_wound_all_members_aux
  # Input: arg1 = party_no
  ("party_wound_all_members",
    [ (store_script_param_1, ":party_no"),
      (call_script, "script_party_wound_all_members_aux", ":party_no"),
  ]),
  
  
  
  # script_calculate_battle_advantage
  # Output: reg0 = battle advantage
  ("calculate_battle_advantage",
    [
      (call_script, "script_party_count_fit_for_battle", "p_collective_friends"),
      (assign, ":friend_count", reg(0)),
      
      (party_get_skill_level, ":player_party_tactics",  "p_main_party", skl_tactics),
      (party_get_skill_level, ":ally_party_tactics",  "p_collective_friends", skl_tactics),
      (val_max, ":player_party_tactics", ":ally_party_tactics"),
     
      (call_script, "script_party_count_fit_for_battle", "p_collective_enemy"),
      (assign, ":enemy_count", reg(0)),

  ## TLD, total number of combatants, needed for random scene generation, GA
	  (store_add, "$number_of_combatants", ":friend_count",":enemy_count"),
	  
      (party_get_skill_level, ":enemy_party_tactics",  "p_collective_enemy", skl_tactics),
      
      (val_add, ":friend_count", 1),
      (val_add, ":enemy_count", 1),
      
      (try_begin),
        (ge, ":friend_count", ":enemy_count"),
        (val_mul, ":friend_count", 100),
        (store_div, ":ratio", ":friend_count", ":enemy_count"),
        (store_sub, ":raw_advantage", ":ratio", 100),
      (else_try),
        (val_mul, ":enemy_count", 100),
        (store_div, ":ratio", ":enemy_count", ":friend_count"),
        (store_sub, ":raw_advantage", 100, ":ratio"),
      (try_end),
      (val_mul, ":raw_advantage", 2),
      
      (val_mul, ":player_party_tactics", 30),
      (val_mul, ":enemy_party_tactics", 30),
      (val_add, ":raw_advantage", ":player_party_tactics"),
      (val_sub, ":raw_advantage", ":enemy_party_tactics"),
      (val_div, ":raw_advantage", 100),
      
      
      (assign, reg0, ":raw_advantage"),
      (display_message, "@Battle Advantage = {reg0}.", 0xFFFFFFFF),
  ]),
  
  
  # script_cf_check_enemies_nearby
  # Input: none
  # Output: none, fails when enemies are nearby
  ("cf_check_enemies_nearby",
    [
      (get_player_agent_no, ":player_agent"),
      (agent_is_alive, ":player_agent"),
      (agent_get_position, pos1, ":player_agent"),
      (assign, ":result", 0),
      (set_fixed_point_multiplier, 100),
      (try_for_agents,":cur_agent"),
        (neq, ":cur_agent", ":player_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (neg|agent_is_ally, ":cur_agent"),
        (agent_get_position, pos2, ":cur_agent"),
        (get_distance_between_positions, ":cur_distance", pos1, pos2),
        (le, ":cur_distance", 1500), #15 meters
        (assign, ":result", 1),
      (try_end),
      (eq, ":result", 0),
  ]),
  
  # script_get_heroes_attached_to_center_aux
  # For internal use only
  ("get_heroes_attached_to_center_aux",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (party_get_num_companion_stacks, ":num_stacks",":center_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":center_no",":i_stack"),
        (troop_is_hero, ":stack_troop"),
        (party_add_members, ":party_no_to_collect_heroes", ":stack_troop", 1),
      (try_end),
      (party_get_num_attached_parties, ":num_attached_parties", ":center_no"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":center_no", ":attached_party_rank"),
        (call_script, "script_get_heroes_attached_to_center_aux", ":attached_party", ":party_no_to_collect_heroes"),
      (try_end),
  ]),
  
  # script_get_heroes_attached_to_center
  # Input: arg1 = center_no, arg2 = party_no_to_collect_heroes
  # Output: none, adds heroes to the party_no_to_collect_heroes party
  ("get_heroes_attached_to_center",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (party_clear, ":party_no_to_collect_heroes"),
      (call_script, "script_get_heroes_attached_to_center_aux", ":center_no", ":party_no_to_collect_heroes"),

#rebellion changes begin -Arma
     (try_for_range, ":pretender", pretenders_begin, pretenders_end),
        (neq, ":pretender", "$supported_pretender"),
        (troop_slot_eq, ":pretender", slot_troop_cur_center, ":center_no"),
        (party_add_members, ":party_no_to_collect_heroes", ":pretender", 1),
     (try_end),

#     (try_for_range, ":rebel_faction", rebel_factions_begin, rebel_factions_end),
#        (faction_slot_eq, ":rebel_faction", slot_faction_state, sfs_inactive_rebellion),
#        (faction_slot_eq, ":rebel_faction", slot_faction_inactive_leader_location, ":center_no"),
#        (faction_get_slot, ":pretender", ":rebel_faction", slot_faction_leader),
#        (party_add_members, ":party_no_to_collect_heroes", ":pretender", 1),
#     (try_end),
#rebellion changes end


  ]),
  
  
  # script_get_heroes_attached_to_center_as_prisoner_aux
  # For internal use only
  ("get_heroes_attached_to_center_as_prisoner_aux",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (party_get_num_prisoner_stacks, ":num_stacks",":center_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id, ":stack_troop",":center_no",":i_stack"),
        (troop_is_hero, ":stack_troop"),
        (party_add_members, ":party_no_to_collect_heroes", ":stack_troop", 1),
      (try_end),
      (party_get_num_attached_parties, ":num_attached_parties", ":center_no"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":center_no", ":attached_party_rank"),
        (call_script, "script_get_heroes_attached_to_center_as_prisoner_aux", ":attached_party", ":party_no_to_collect_heroes"),
      (try_end),
  ]),
  
  
  # script_get_heroes_attached_to_center_as_prisoner
  # Input: arg1 = center_no, arg2 = party_no_to_collect_heroes
  # Output: none, adds heroes to the party_no_to_collect_heroes party
  ("get_heroes_attached_to_center_as_prisoner",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (party_clear, ":party_no_to_collect_heroes"),
      (call_script, "script_get_heroes_attached_to_center_as_prisoner_aux", ":center_no", ":party_no_to_collect_heroes"),
  ]),
  
##  
##  # script_cf_get_party_leader
##  # Input: arg1 = party_no
##  # Output: reg0 = troop_no of the leader (Can fail)
##  ("cf_get_party_leader",
##    [
##      (store_script_param_1, ":party_no"),
##      
##      (party_get_num_companion_stacks, ":num_stacks",":party_no"),
##      (gt, ":num_stacks", 0),
##      (party_stack_get_troop_id, ":stack_troop", ":party_no", 0),
##      (troop_is_hero, ":stack_troop"),
##      (assign, reg0, ":stack_troop"),
##  ]),
  
  # script_give_center_to_faction
  # Input: arg1 = center_no, arg2 = faction
  ("give_center_to_faction",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":faction_no"),
      (try_begin),
        (check_quest_active, "qst_join_siege_with_army"),
        (quest_slot_eq, "qst_join_siege_with_army", slot_quest_target_center, ":center_no"),
        (call_script, "script_abort_quest", "qst_join_siege_with_army", 0),
        #Reactivating follow army quest
        (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
        (str_store_troop_name_link, s9, ":faction_marshall"),
        (setup_quest_text, "qst_follow_army"),
        (str_store_string, s2, "@{s9} wants you to resume following his army until further notice."),
        (call_script, "script_start_quest", "qst_follow_army", ":faction_marshall"),
        #(assign, "$g_player_follow_army_warnings", 0),
      (try_end),
      (store_faction_of_party, ":old_faction", ":center_no"),
      (call_script, "script_give_center_to_faction_aux", ":center_no", ":faction_no"),
      (call_script, "script_update_village_market_towns"),

      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (call_script, "script_faction_recalculate_strength", ":cur_faction"),
      (try_end),
      (assign, "$g_recalculate_ais", 1),

      (call_script, "script_activate_deactivate_player_faction", ":old_faction"),
      (try_begin),
        (eq, ":faction_no", "fac_player_supporters_faction"),
        (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
        (call_script, "script_give_center_to_lord", ":center_no", "trp_player", 0),
        (try_for_range, ":cur_village", villages_begin, villages_end),
          (store_faction_of_party, ":cur_village_faction", ":cur_village"),
          (eq, ":cur_village_faction", "fac_player_supporters_faction"),
          (neg|party_slot_eq, ":cur_village", slot_town_lord, "trp_player"),
          (call_script, "script_give_center_to_lord", ":cur_village", "trp_player", 0),
        (try_end),
      (try_end),
      ]),
  
  # script_give_center_to_faction_aux
  # Input: arg1 = center_no, arg2 = faction
  ("give_center_to_faction_aux",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":faction_no"),

      (store_faction_of_party, ":old_faction", ":center_no"),
      (party_set_slot, ":center_no", slot_center_ex_faction, ":old_faction"),
      (party_set_faction, ":center_no", ":faction_no"),

      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_village),
        (party_get_slot, ":farmer_party", ":center_no", slot_village_farmer_party),
        (gt, ":farmer_party", 0),
        (party_is_active, ":farmer_party"),
        (party_set_faction, ":farmer_party", ":faction_no"),
      (try_end),

      (party_get_slot, ":old_town_lord", ":center_no", slot_town_lord),
      
      #TLD changes: give captured centers to kings, place faction banner
      (faction_get_slot, ":king", ":faction_no", slot_faction_leader),
      (party_set_slot, ":center_no", slot_town_lord, ":king"),
	  (faction_get_slot,":faction_banner",":faction_no",slot_faction_party_map_banner),
      (party_set_banner_icon, ":center_no", ":faction_banner"),
      #TLD: change NPCs and walkers - since I'm lazy, I'll just give them clones of the faction capital NPCs and walkers
      (faction_get_slot, ":capital", ":faction_no", slot_faction_capital),
      (party_get_slot, ":value", ":capital", slot_town_elder),
      (party_set_slot, ":center_no", slot_town_elder, ":value"),
      (party_get_slot, ":value", ":capital", slot_town_barman),
      (party_set_slot, ":center_no", slot_town_barman, ":value"),
      (party_get_slot, ":value", ":capital", slot_town_weaponsmith),
      (party_set_slot, ":center_no", slot_town_weaponsmith, ":value"),
      (party_get_slot, ":value", ":capital", slot_town_armorer),
      (party_set_slot, ":center_no", slot_town_armorer, ":value"),
      (party_get_slot, ":value", ":capital", slot_town_merchant),
      (party_set_slot, ":center_no", slot_town_merchant, ":value"),
      (party_get_slot, ":value", ":capital", slot_town_horse_merchant),
      (party_set_slot, ":center_no", slot_town_horse_merchant, ":value"),
      (party_get_slot, ":value", ":capital", slot_town_reinf_pt),
      (party_set_slot, ":center_no", slot_town_reinf_pt, ":value"),
      (party_get_slot, ":value", ":capital", slot_center_walker_0_troop),
      (party_set_slot, ":center_no", slot_center_walker_0_troop, ":value"),
      (party_get_slot, ":value", ":capital", slot_center_walker_1_troop),
      (party_set_slot, ":center_no", slot_center_walker_1_troop, ":value"),
      (party_get_slot, ":value", ":capital", slot_center_walker_2_troop),
      (party_set_slot, ":center_no", slot_center_walker_2_troop, ":value"),
      (party_get_slot, ":value", ":capital", slot_center_walker_3_troop),
      (party_set_slot, ":center_no", slot_center_walker_3_troop, ":value"),
      (party_get_slot, ":value", ":capital", slot_center_walker_4_troop),
      (party_set_slot, ":center_no", slot_center_walker_4_troop, ":value"),
      (party_get_slot, ":value", ":capital", slot_center_walker_5_troop),
      (party_set_slot, ":center_no", slot_center_walker_5_troop, ":value"),
      (party_get_slot, ":value", ":capital", slot_center_walker_6_troop),
      (party_set_slot, ":center_no", slot_center_walker_6_troop, ":value"),
      (party_get_slot, ":value", ":capital", slot_center_walker_7_troop),
      (party_set_slot, ":center_no", slot_center_walker_7_troop, ":value"),
      (party_get_slot, ":value", ":capital", slot_center_walker_8_troop),
      (party_set_slot, ":center_no", slot_center_walker_8_troop, ":value"),
      (party_get_slot, ":value", ":capital", slot_center_walker_9_troop),
      (party_set_slot, ":center_no", slot_center_walker_9_troop, ":value"),
      (faction_get_slot, ":value", ":faction_no", slot_faction_guard_troop),
      (party_set_slot, ":center_no", slot_town_guard_troop, ":value"),
      (faction_get_slot, ":value", ":faction_no", slot_faction_prison_guard_troop),
      (party_set_slot, ":center_no", slot_town_prison_guard_troop, ":value"),
      (faction_get_slot, ":value", ":faction_no", slot_faction_castle_guard_troop),
      (party_set_slot, ":center_no", slot_town_castle_guard_troop, ":value"),
      
      # Change center spawns to be the same as for faction advance camps, only if there was such a spawn before
      (faction_get_slot, ":adv_camp", ":faction_no", slot_faction_advance_camp),
      (try_begin),
        (party_get_slot, ":old_value", ":center_no", slot_center_spawn_scouts),
        (gt, ":old_value", 0),
        (party_get_slot, ":value", ":adv_camp", slot_center_spawn_scouts),
        (party_set_slot, ":center_no", slot_center_spawn_scouts, ":value"),
      (try_end),
      (try_begin),
        (party_get_slot, ":old_value", ":center_no", slot_center_spawn_raiders),
        (gt, ":old_value", 0),
        (party_get_slot, ":value", ":adv_camp", slot_center_spawn_raiders),
        (party_set_slot, ":center_no", slot_center_spawn_raiders, ":value"),
      (try_end),
      (try_begin),
        (party_get_slot, ":old_value", ":center_no", slot_center_spawn_patrol),
        (gt, ":old_value", 0),
        (party_get_slot, ":value", ":adv_camp", slot_center_spawn_patrol),
        (party_set_slot, ":center_no", slot_center_spawn_patrol, ":value"),
      (try_end),
      (try_begin),
        (party_get_slot, ":old_value", ":center_no", slot_center_spawn_caravan),
        (gt, ":old_value", 0),
        (party_get_slot, ":value", ":adv_camp", slot_center_spawn_caravan),
        (party_set_slot, ":center_no", slot_center_spawn_caravan, ":value"),
      (try_end),
      
      #reduce income to 5 if non-zero
      (party_get_slot, ":strength_income", ":center_no", slot_center_strength_income),
      (val_min, ":strength_income", str_income_low),
      (party_set_slot, ":center_no", slot_center_strength_income, ":strength_income"),
      
      #TLD: old faction loses faction strength
      # (faction_get_slot,":strength",":old_faction",slot_faction_strength_tmp),
      # (val_sub, ":strength", ws_center_vp),
      # (faction_set_slot,":old_faction",slot_faction_strength_tmp,":strength"),
      # #debug stuff
      # (faction_get_slot, ":debug_loss", ":old_faction", slot_faction_debug_str_loss),
      # (val_add, ":debug_loss", ws_center_vp),
      # (faction_set_slot, ":old_faction", slot_faction_debug_str_loss, ":debug_loss"),
      # #TLD: conquering faction gains faction strength
      # (faction_get_slot,":winner_strength",":faction_no",slot_faction_strength_tmp),
      # (store_div, ":win_value", ws_center_vp, 2), #this formula could be balanced after playtesting
      # (val_add, ":winner_strength", ":win_value"),
      # (faction_set_slot,":faction_no",slot_faction_strength_tmp,":winner_strength"),
      # #debug stuff
      # (faction_get_slot, ":debug_gain", ":faction_no", slot_faction_debug_str_gain),
      # (val_add, ":debug_gain", ":win_value"),
      # (faction_set_slot, ":faction_no", slot_faction_debug_str_gain, ":debug_gain"),
      # #debug
      # (try_begin),
        # (eq, cheat_switch, 1),
        # (assign,reg0,ws_center_vp),
        # (assign,reg1,":strength"),
        # (assign,reg2,":win_value"),
        # (assign,reg3,":winner_strength"),
        # (str_store_faction_name,s1,":old_faction"),
        # (str_store_faction_name,s2,":faction_no"),
        # (str_store_party_name,s3,":center_no"),
        # (display_message,"@DEBUG: {s3} captured: {s1} strength -{reg0} to {reg1}, {s2} strength +{reg2} to {reg3}."),
      # (try_end),

      (call_script, "script_update_faction_notes", ":old_faction"),
      (call_script, "script_update_faction_notes", ":faction_no"),
      (call_script, "script_update_center_notes", ":center_no"),
      (call_script, "script_update_troop_notes", ":king"), # TLD
      (try_begin),
        (ge, ":old_town_lord", 0),
        (call_script, "script_update_troop_notes", ":old_town_lord"),
      (try_end),

      (try_for_range, ":other_center", centers_begin, centers_end),
        (party_is_active, ":other_center"), #TLD
        (party_slot_eq, ":other_center", slot_village_bound_center, ":center_no"),
        (call_script, "script_give_center_to_faction_aux", ":other_center", ":faction_no"),
      (try_end),
  ]),
  
  # script_change_troop_faction
  # Input: arg1 = troop_no, arg2 = faction
  ("change_troop_faction",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":faction_no"),
      (try_begin),
        #Reactivating inactive or defeated faction
        (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
        (neg|faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (faction_set_slot, ":faction_no", slot_faction_state, sfs_active),
        (call_script, "script_store_average_center_value_per_faction"),
      (try_end),

      (troop_set_faction, ":troop_no", ":faction_no"),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (party_is_active, ":center_no"), #TLD
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (party_set_faction, ":center_no", ":faction_no"),
        (try_for_range, ":village_no", villages_begin, villages_end),
          (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),
          (party_set_faction, ":village_no", ":faction_no"),
          (party_get_slot, ":farmer_party_no", ":village_no", slot_village_farmer_party),
          (try_begin),
            (gt, ":farmer_party_no", 0),
            (party_is_active, ":farmer_party_no"),
            (party_set_faction, ":farmer_party_no", ":faction_no"),
          (try_end),
          (try_begin),
            (party_get_slot, ":old_town_lord", ":village_no", slot_town_lord),
            (neq, ":old_town_lord", ":troop_no"),
            (party_set_slot, ":village_no", slot_town_lord, stl_unassigned),
          (try_end),
        (try_end),
      (try_end),
      (try_for_range, ":village_no", villages_begin, villages_end),
        (party_slot_eq, ":village_no", slot_town_lord, ":troop_no"),
        (store_faction_of_party, ":village_faction", ":village_no"),
        (try_begin),
          (neq, ":village_faction", ":faction_no"),
          (party_set_slot, ":village_no", slot_town_lord, stl_unassigned),
        (try_end),
      (try_end),
      (try_begin),
        (troop_get_slot, ":leaded_party", ":troop_no", slot_troop_leaded_party),
        (ge, ":leaded_party", 0),
        (party_set_faction, ":leaded_party", ":faction_no"),
        (party_get_num_prisoner_stacks, ":num_stacks", ":leaded_party"),
        (try_for_range_backwards, ":troop_iterator", 0, ":num_stacks"),
          (party_prisoner_stack_get_troop_id, ":cur_troop_id", ":leaded_party", ":troop_iterator"),
          (store_troop_faction, ":cur_faction", ":cur_troop_id"),
          (troop_is_hero, ":cur_troop_id"),
          (eq, ":cur_faction", ":faction_no"),
          (call_script, "script_remove_troop_from_prison", ":cur_troop_id"),
          (party_remove_prisoners, ":leaded_party", ":cur_troop_id", 1),
        (try_end),
      (try_end),
      (call_script, "script_update_all_notes"),

      (call_script, "script_update_village_market_towns"),
      (assign, "$g_recalculate_ais", 1),
      ]),


  # script_give_center_to_lord
  # Input: arg1 = center_no, arg2 = lord_troop, arg3 = add_garrison_to_center
  ("give_center_to_lord",
    [
      (store_script_param, ":center_no", 1),
      (store_script_param, ":lord_troop_id", 2),
      (store_script_param, ":add_garrison", 3),

      (party_get_slot, ":old_lord_troop_id", ":center_no", slot_town_lord),
      
      (store_troop_faction, ":lord_troop_faction", ":lord_troop_id"),
      (try_begin),
        (eq, ":lord_troop_id", "trp_player"),
        (gt, "$players_kingdom", 0),
        (party_set_faction, ":center_no", "$players_kingdom"),
      (else_try),
        (eq, ":lord_troop_id", "trp_player"),
        (le, "$players_kingdom", 0),
        (party_set_faction, ":center_no", "fac_player_supporters_faction"),
      (else_try),
        (party_set_faction, ":center_no", ":lord_troop_faction"),
      (try_end),
      (party_set_slot, ":center_no", slot_town_lord, ":lord_troop_id"),

      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_village),
        (party_get_slot, ":farmer_party_no", ":center_no", slot_village_farmer_party),
        (gt, ":farmer_party_no", 0),
        (party_is_active, ":farmer_party_no"),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (party_set_faction, ":farmer_party_no", ":center_faction"),
      (try_end),

      (try_begin),
        (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
        (party_slot_eq, ":center_no", slot_party_type, spt_castle),
#normal_banner_begin
#       (troop_get_slot, ":cur_banner", ":lord_troop_id", slot_troop_banner_scene_prop),
#        (gt, ":cur_banner", 0),
#        (val_sub, ":cur_banner", banner_scene_props_begin),
#        (val_add, ":cur_banner", banner_map_icons_begin),
#        (party_set_banner_icon, ":center_no", ":cur_banner"),
# custom_banner_begin
#        (troop_get_slot, ":flag_icon", ":lord_troop_id", slot_troop_custom_banner_map_flag_type),
#        (ge, ":flag_icon", 0),
#        (val_add, ":flag_icon", custom_banner_map_icons_begin),
#        (party_set_banner_icon, ":center_no", ":flag_icon"),
      (try_end),

      (try_begin),
        (eq, ":lord_troop_id", "trp_player"),
        (neq, ":old_lord_troop_id", "trp_player"),
        (party_get_slot, ":center_relation", ":center_no", slot_center_player_relation),
        (is_between, ":center_relation", -4, 5),
        (call_script, "script_change_player_relation_with_center", ":center_no", 5),
        (gt, ":old_lord_troop_id", 0),
        (call_script, "script_change_player_relation_with_troop", ":old_lord_troop_id", -25),
      (try_end),

      (call_script, "script_update_troop_notes", ":lord_troop_id"),
      (call_script, "script_update_center_notes", ":center_no"),
      (call_script, "script_update_faction_notes", ":lord_troop_faction"),
      (try_begin),
        (ge, ":old_lord_troop_id", 0),
        (call_script, "script_update_troop_notes", ":old_lord_troop_id"),
        (store_troop_faction, ":old_lord_troop_faction", ":old_lord_troop_id"),
        (call_script, "script_update_faction_notes", ":old_lord_troop_faction"),
      (try_end),

      (try_begin),
        (eq, ":add_garrison", 1),
        (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
        (party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (assign, ":garrison_strength", 3), 
        (try_begin),
          (party_slot_eq, ":center_no", slot_party_type, spt_town),
          (assign, ":garrison_strength", 9),
        (try_end),
        (try_for_range, ":unused", 0, ":garrison_strength"),
          (call_script, "script_cf_reinforce_party", ":center_no"),
        (try_end),
        ## ADD some XP initially
        (try_for_range, ":unused", 0, 7),
          (store_random_in_range, ":xp", 1500, 2000),
          (party_upgrade_with_xp, ":center_no", ":xp", 0),
        (try_end),
      (try_end),

      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (try_for_range, ":cur_village", villages_begin, villages_end),
          (party_slot_eq, ":cur_village", slot_village_bound_center, ":center_no"),
          (call_script, "script_give_center_to_lord", ":cur_village", ":lord_troop_id", 0),
        (try_end),
      (try_end),
  ]),
  
  # script_get_number_of_hero_centers
  # Input: arg1 = troop_no
  # Output: reg0 = number of centers that are ruled by the hero
  ("get_number_of_hero_centers",
    [
      (store_script_param_1, ":troop_no"),
      (assign, ":result", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (val_add, ":result", 1),
      (try_end),
      (assign, reg0, ":result"),
  ]),
  
  
  ##  # script_cf_get_new_center_leader_chance_for_troop
  ##  # Input: arg1 = troop_no
  ##  # Output: reg0 = chance of the troop to rule a new center
  ##  ("cf_get_new_center_leader_chance_for_troop",
  ##    [
  ##      (store_script_param_1, ":troop_no"),
  ##      (troop_get_slot, ":troop_rank", ":troop_no", slot_troop_kingdom_rank),
  ##      (try_begin),
  ##        (eq, ":troop_rank", 4),
  ##        (assign, ":troop_chance", 1000),
  ##      (else_try),
  ##        (eq, ":troop_rank", 3),
  ##        (assign, ":troop_chance", 800),
  ##      (else_try),
  ##        (eq, ":troop_rank", 2),
  ##        (assign, ":troop_chance", 400),
  ##      (else_try),
  ##        (eq, ":troop_rank", 1),
  ##        (assign, ":troop_chance", 100),
  ##      (else_try),
  ##        (assign, ":troop_chance", 10),
  ##      (try_end),
  ##
  ##      (call_script, "script_get_number_of_hero_centers", ":troop_no"),
  ##      (assign, ":number_of_hero_centers", reg0),
  ##      (try_begin),
  ##        (gt, ":number_of_hero_centers", 0),
  ##        (val_mul, ":number_of_hero_centers", 2),
  ##        (val_mul, ":number_of_hero_centers", ":number_of_hero_centers"),
  ##        (val_div, ":troop_chance", ":number_of_hero_centers"),
  ##      (try_end),
  ##      (assign, reg0, ":troop_chance"),
  ##      (eq, reg0, 0),
  ##      (assign, reg0, 1),
  ##  ]),
  
  
##  # script_select_kingdom_hero_for_new_center
##  # Input: arg1 = faction_no
##  # Output: reg0 = troop_no as the new leader
##  ("select_kingdom_hero_for_new_center",
##    [
##      (store_script_param_1, ":kingdom"),
##      
##      (assign, ":min_num_centers", -1),
##      (assign, ":min_num_centers_troop", -1),
##      
##      (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
##        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
##        (store_troop_faction, ":troop_faction", ":troop_no"),
##        (eq, ":troop_faction", ":kingdom"),
##        (call_script, "script_get_number_of_hero_centers", ":troop_no"),
##        (assign, ":num_centers", reg0),
##        (try_begin),
##          (lt, ":num_centers", ":min_num_centers"),
##          (assign, ":min_num_centers", ":num_centers"),
##          (assign, ":min_num_centers_troop", ":troop_no"),
##        (try_end),
##      (try_end),
##      (assign, reg0, ":min_num_centers_troop"),
##  ]),
  
  
  # script_cf_get_random_enemy_center
  # Input: arg1 = party_no
  # Output: reg0 = center_no
  ("cf_get_random_enemy_center",
    [
      (store_script_param_1, ":party_no"),
      
      (assign, ":result", -1),
      (assign, ":total_enemy_centers", 0),
      (store_faction_of_party, ":party_faction", ":party_no"),
      
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
        (store_faction_of_party, ":center_faction", ":center_no"),
        (store_relation, ":party_relation", ":center_faction", ":party_faction"),
        (lt, ":party_relation", 0),
        (val_add, ":total_enemy_centers", 1),
      (try_end),

      (gt, ":total_enemy_centers", 0),
      (store_random_in_range, ":random_center", 0, ":total_enemy_centers"),
      (assign, ":total_enemy_centers", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
        (eq, ":result", -1),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (store_relation, ":party_relation", ":center_faction", ":party_faction"),
        (lt, ":party_relation", 0),
        (val_sub, ":random_center", 1),
        (lt, ":random_center", 0),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
  
  
##  # script_get_random_enemy_town
##  # Input: arg1 = party_no
##  # Output: reg0 = center_no
##  ("get_random_enemy_town",
##    [
##      (store_script_param_1, ":party_no"),
##      
##      (assign, ":result", -1),
##      (assign, ":total_enemy_centers", 0),
##      (store_faction_of_party, ":party_faction", ":party_no"),
##      
##      (try_for_range, ":center_no", towns_begin, towns_end),
##        (store_faction_of_party, ":center_faction", ":center_no"),
##        (neq, ":center_faction", ":party_faction"),
##        (val_add, ":total_enemy_centers", 1),
##      (try_end),
##      
##      (try_begin),
##        (eq, ":total_enemy_centers", 0),
##      (else_try),
##        (store_random_in_range, ":random_center", 0, ":total_enemy_centers"),
##        (assign, ":total_enemy_centers", 0),
##        (try_for_range, ":center_no", towns_begin, towns_end),
##          (eq, ":result", -1),
##          (store_faction_of_party, ":center_faction", ":center_no"),
##          (neq, ":center_faction", ":party_faction"),
##          (store_relation, ":party_relation", ":center_faction", ":party_faction"),
##          (le, ":party_relation", -10),
##          (val_add, ":total_enemy_centers", 1),
##          (lt, ":random_center", ":total_enemy_centers"),
##          (assign, ":result", ":center_no"),
##        (try_end),
##      (try_end),
##      (assign, reg0, ":result"),
##  ]),
  
  
  
  # script_find_travel_location
  # Input: arg1 = center_no
  # Output: reg0 = new_center_no (to travel within the same faction)
  ("find_travel_location",
    [
      (store_script_param_1, ":center_no"),
      (store_faction_of_party, ":faction_no", ":center_no"),
      (assign, ":total_weight", 0),
      (try_for_range, ":cur_center_no", centers_begin, centers_end),
        (party_is_active, ":cur_center_no"), #TLD
        (neq, ":center_no", ":cur_center_no"),
        (store_faction_of_party, ":center_faction_no", ":cur_center_no"),
        (eq, ":faction_no", ":center_faction_no"),
        
        (store_distance_to_party_from_party, ":cur_distance", ":center_no", ":cur_center_no"),
        (val_add, ":cur_distance", 1),
        
        (assign, ":new_weight", 100000),
        (val_div, ":new_weight", ":cur_distance"),
        (val_add, ":total_weight", ":new_weight"),
      (try_end),
      
      (assign, reg0, -1),
      
      (try_begin),
        (eq, ":total_weight", 0),
      (else_try),
        (store_random_in_range, ":random_weight", 0 , ":total_weight"),
        (assign, ":total_weight", 0),
        (assign, ":done", 0),
        (try_for_range, ":cur_center_no", centers_begin, centers_end),
          (party_is_active, ":cur_center_no"), #TLD
          (eq, ":done", 0),
          (neq, ":center_no", ":cur_center_no"),
          (store_faction_of_party, ":center_faction_no", ":cur_center_no"),
          (eq, ":faction_no", ":center_faction_no"),
          
          (store_distance_to_party_from_party, ":cur_distance", ":center_no", ":cur_center_no"),
          (val_add, ":cur_distance", 1),
          
          (assign, ":new_weight", 100000),
          (val_div, ":new_weight", ":cur_distance"),
          (val_add, ":total_weight", ":new_weight"),
          (lt, ":random_weight", ":total_weight"),
          (assign, reg0, ":cur_center_no"),
          (assign, ":done", 1),
        (try_end),
      (try_end),
  ]),
  
  
  # script_get_relation_between_parties
  # Input: arg1 = party_no_1, arg2 = party_no_2
  # Output: reg0 = relation between parties
  ("get_relation_between_parties",
    [
      (store_script_param_1, ":party_no_1"),
      (store_script_param_2, ":party_no_2"),
      
      (store_faction_of_party, ":party_no_1_faction", ":party_no_1"),
      (store_faction_of_party, ":party_no_2_faction", ":party_no_2"),
      (try_begin),
        (eq, ":party_no_1_faction", ":party_no_2_faction"),
        (assign, reg0, 100),
      (else_try),
        (store_relation, ":relation", ":party_no_1_faction", ":party_no_2_faction"),
        (assign, reg0, ":relation"),
      (try_end),
  ]),
  
  
  
  
  # script_cf_reinforce_party
  # Input: arg1 = party_no,
  # Output: none
  # Adds reinforcement to party according to its type and faction
  ("cf_reinforce_party",
    [
      (store_script_param_1, ":party_no"),
      
      (store_faction_of_party, ":party_faction", ":party_no"),
      #(party_get_slot, ":party_type",":party_no", slot_party_type),

      (try_begin),
        (eq, ":party_faction", "fac_player_supporters_faction"),
        (party_get_slot, ":town_lord", ":party_no", slot_town_lord),
        (try_begin),
          (gt, ":town_lord", 0),
          (troop_get_slot, ":party_faction", ":town_lord", slot_troop_original_faction),
        (else_try),
          (party_get_slot, ":party_faction", ":party_no", slot_center_original_faction),
        (try_end),
      (try_end),
      
      (faction_get_slot, ":party_template_a", ":party_faction", slot_faction_reinforcements_a),
      (faction_get_slot, ":party_template_b", ":party_faction", slot_faction_reinforcements_b),
      (faction_get_slot, ":party_template_c", ":party_faction", slot_faction_reinforcements_c),

	  # special minas - MV: commented out, looks unfinished
      # (party_get_slot, ":party_template_a", ":party_no", slot_town_reinforcements_a),
      # (party_get_slot, ":party_template_b", ":party_no", slot_town_reinforcements_b),
      # (party_get_slot, ":party_template_c", ":party_no", slot_town_reinforcements_c),

      (store_random_in_range, ":rand", 0, 100), # A, B, or C

	  (assign, ":bonus", 0 ), 
	  #(MV: did) uncomment the following block to make a 6% of mixing between gondor subfactions
	  (try_begin), 
	  	(eq, ":party_faction", "fac_gondor"), # only in gondor....
		(store_random_in_range, ":rand2", 0, 100), (le, ":rand2", 8), # 8% of times...
		(try_begin),
			#non regular Gondor parties gets a regular reinforement...
			(neg|party_slot_eq, ":party_no", slot_party_subfaction, 0), 
			(faction_get_slot, ":party_template_a", ":party_faction", slot_faction_reinforcements_a),
			(faction_get_slot, ":party_template_b", ":party_faction", slot_faction_reinforcements_b),
			(faction_get_slot, ":party_template_c", ":party_faction", slot_faction_reinforcements_c),
		(else_try),
			#regular Gondor parties gets a subfaction reinforement...
			(store_random_in_range, ":bonus", 1, len(subfaction_data)+1 ),
			(val_mul, ":bonus", 3), 
		(try_end),
		(val_mul,":rand",75),(val_div,":rand",100),  # but cannot pick "C"
	  (try_end),

      (assign, ":party_template", 0),
      (try_begin),
        (lt, ":rand", 55),
        (store_add, ":party_template", ":party_template_a", ":bonus"),
      (else_try),
        (lt, ":rand", 80),
        (store_add, ":party_template", ":party_template_b", ":bonus"),
      (else_try),
        (store_add, ":party_template", ":party_template_c", ":bonus"),
      (try_end),
	  (try_begin),
		(eq, ":party_no", "p_town_minas_tirith"), # special minas tirith rule,,,
		(store_random_in_range, ":rand2", 0, 100), (le, ":rand2", 20), # 20% of times...
		(assign, ":party_template", "pt_gondor_reinf_d"),
	  (try_end),
      
      (try_begin),
        (gt, ":party_template", 0),
        (party_is_active, ":party_no"), #TLD
        (party_add_template, ":party_no", ":party_template"),
      (try_end),
  ]),
  
  # script_hire_men_to_kingdom_hero_party
  # [Old TLD change: Hiring troops based on nearby town wealth instead of hero wealth]
  # New TLD change: Hiring troops based only on current and ideal party size
  # Input: arg1 = troop_no (hero of the party)
  # Output: none
  ("hire_men_to_kingdom_hero_party",
    [ (store_script_param_1, ":troop_no"),
      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
        # (call_script, "script_find_random_nearby_friendly_town", ":party_no", 0),
        # (assign, ":nearby_center", reg0),
        # (party_get_slot, ":cur_wealth", ":nearby_center", slot_town_wealth),
      # (assign, ":hiring_budget", ":cur_wealth"),
      # (val_mul, ":hiring_budget", 4),
      # (val_div, ":hiring_budget", 5),
      (assign, ":num_rounds", 1),
    
      (call_script, "script_party_get_ideal_size", ":party_no"),
      (assign, ":ideal_size", reg0),
#      (display_message, "@DEBUG: Host ideal size: {reg0}", debug_color),
      (store_mul, ":ideal_top_size", ":ideal_size", 3),
      (val_div, ":ideal_top_size", 2),
    
      (party_get_num_companions, ":party_size", ":party_no"),
      (try_for_range, ":unused", 0 , ":num_rounds"),
        (try_begin),
          (lt, ":party_size", ":ideal_size"),
#          (gt, ":hiring_budget", reinforcement_cost),
          (gt, ":party_no", 0),
          (call_script, "script_cf_reinforce_party", ":party_no"),
#          (val_sub, ":cur_wealth", reinforcement_cost),
#          (party_set_slot, ":nearby_center", slot_town_wealth, ":cur_wealth"), # TLD: wealth change to town
        (else_try),
          (gt, ":party_size", ":ideal_top_size"),
          (store_troop_faction, ":troop_faction", ":troop_no"),
          (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
          (assign, ":total_regulars", 0),
          (assign, ":total_regular_levels", 0),
          (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
            (neg|troop_is_hero, ":stack_troop"),
            (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
            (store_character_level, ":stack_level", ":stack_troop"),
            (store_troop_faction, ":stack_faction", ":stack_troop"),
            (try_begin),
              (eq, ":troop_faction", ":stack_faction"),
              (val_mul, ":stack_level", 3), #reducing the chance of the faction troops' removal
            (try_end),
            (val_mul, ":stack_level", ":stack_size"),
            (val_add, ":total_regulars", ":stack_size"),
            (val_add, ":total_regular_levels", ":stack_level"),
          (try_end),
          (gt, ":total_regulars", 0),
          (store_div, ":average_level", ":total_regular_levels", ":total_regulars"),
          (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
            (neg|troop_is_hero, ":stack_troop"),
            (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
            (store_character_level, ":stack_level", ":stack_troop"),
            (store_troop_faction, ":stack_faction", ":stack_troop"),
            (try_begin),
              (eq, ":troop_faction", ":stack_faction"),
              (val_mul, ":stack_level", 3),
            (try_end),
            (store_sub, ":level_dif", ":average_level", ":stack_level"),
            (val_div, ":level_dif", 3),
            (store_add, ":prune_chance", 10, ":level_dif"),
            (gt, ":prune_chance", 0),
            (call_script, "script_get_percentage_with_randomized_round", ":stack_size", ":prune_chance"),
            (gt, reg0, 0),
            (party_remove_members, ":party_no", ":stack_troop", reg0),
          (try_end),
        (try_end),
      (try_end),
#MV test code begin
# (try_begin),
  # (eq, cheat_switch, 1),
  # (store_troop_faction, ":faction_no", ":troop_no"),
  # (this_or_next|eq, ":faction_no", "fac_gondor"),
  # (eq, ":faction_no", "fac_mordor"),
  # (assign, reg1, ":party_size"),
  # (assign, reg2, ":ideal_size"),
  # (str_store_troop_name, s1, ":troop_no"),
  # (party_get_num_companions, reg3, ":party_no"),
  # (display_message, "@DEBUG: {s1} reinforces, current:{reg1} ideal:{reg2} new:{reg3}.", 0x30FFC8),
# (try_end),
#MV test code end
  ]),

  # script_find_random_nearby_friendly_town
  # TLD script
  # Input: arg1 = party_no, from where to find town; arg2 = include castles
  # Output: reg0 = center party no
  ("find_random_nearby_friendly_town", [
    (store_script_param, ":party_no", 1),
    (store_script_param, ":c_castles", 2),
    (store_faction_of_party, ":party_faction", ":party_no"),
    (assign, ":min_dis", 10000000),
    (assign, reg0, -1),
    (try_for_parties, ":party"),
        (this_or_next|party_slot_eq, ":party", slot_party_type, spt_town),
        (neq, ":c_castles", 0),
        (this_or_next|party_slot_eq, ":party", slot_party_type, spt_town),
        (party_slot_eq, ":party", slot_party_type, spt_castle),
        (store_faction_of_party, ":faction", ":party"),
        (eq, ":faction", ":party_faction"),
        (store_distance_to_party_from_party, ":dis", ":party", ":party_no"),
        (store_random_in_range, ":rand", 0, ":min_dis"),
        (this_or_next|gt, ":rand", ":dis"),
        (eq, reg0, -1),
        (assign, reg0, ":party"),
        (assign, ":min_dis", ":dis"),
    (try_end),
    ]
  ),

  # script_get_percentage_with_randomized_round
  # Input: arg1 = value, arg2 = percentage
  # Output: none
  ("get_percentage_with_randomized_round",
    [
      (store_script_param, ":value", 1),
      (store_script_param, ":percentage", 2),

      (store_mul, ":result", ":value", ":percentage"),
      (val_div, ":result", 100),
      (store_mul, ":used_amount", ":result", 100),
      (val_div, ":used_amount", ":percentage"),
      (store_sub, ":left_amount", ":value", ":used_amount"),
      (try_begin),
        (gt, ":left_amount", 0),
        (store_mul, ":chance", ":left_amount", ":percentage"),
        (store_random_in_range, ":random_no", 0, 100),
        (lt, ":random_no", ":chance"),
        (val_add, ":result", 1),
      (try_end),
      (assign, reg0, ":result"),
      ]),
  
  # script_cf_create_merchant_party
  # Input: arg1 = troop_no,
  # Output: $pout_party = party_no
##  ("cf_create_merchant_party",
##    [
##      (store_script_param_1, ":troop_no"),
##      (store_troop_faction, ":troop_faction", ":troop_no"),
##      
##      (call_script, "script_cf_select_random_town_at_peace_with_faction", ":troop_faction"),
##      (assign, ":center_no", reg0),
##      
##      (assign, "$pout_party", -1),
##      (set_spawn_radius,0),
##      (spawn_around_party,":center_no", "pt_merchant_party"),
##      (assign, "$pout_party", reg0),
##      
##      (party_set_faction, "$pout_party", ":troop_faction"),
##      (party_set_slot, "$pout_party", slot_party_type, spt_merchant_caravan),
##      (party_set_slot, "$pout_party", slot_party_ai_state, spai_undefined),
##      (troop_set_slot, ":troop_no", slot_troop_leaded_party, "$pout_party"),
##      (party_add_leader, "$pout_party", ":troop_no"),
##      (str_store_troop_name, s5, ":troop_no"),
##      (party_set_name, "$pout_party", "str_s5_s_caravan"),
##      (party_set_ai_behavior, "$pout_party", ai_bhvr_travel_to_party),
##      (party_set_ai_object, "$pout_party", ":center_no"),
##      (party_set_flags, "$pout_party", pf_default_behavior, 0),
##      (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
##      (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
##        (store_add, ":cur_goods_price_slot", ":cur_goods", ":item_to_price_slot"),
##        (party_set_slot, "$pout_party", ":cur_goods_price_slot", average_price_factor),
##      (try_end),
##      (troop_set_slot, ":troop_no", slot_troop_wealth, 2000),
##  ]),

  # script_create_cattle_herd
  # Input: arg1 = center_no, arg2 = amount (0 = default)
  # Output: reg0 = party_no
  ("create_cattle_herd",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":amount"),
      
      (assign, ":herd_party", -1),
      (set_spawn_radius,1),

      (spawn_around_party,":center_no", "pt_cattle_herd"),
      (assign, ":herd_party", reg0),
      (party_get_position, pos1, ":center_no"),
      (call_script, "script_map_get_random_position_around_position_within_range", 1, 2),
      (party_set_position, ":herd_party", pos2),

      (party_set_slot, ":herd_party", slot_party_type, spt_cattle_herd),
      (party_set_slot, ":herd_party", slot_party_ai_state, spai_undefined),
      (party_set_ai_behavior, ":herd_party", ai_bhvr_hold),

      (party_set_slot, ":herd_party", slot_party_commander_party, -1), #we need this because 0 is player's party!

      (try_begin),
        (gt, ":amount", 0),
        (party_clear, ":herd_party"),
        (party_add_members, ":herd_party", "trp_cattle", ":amount"),
      (try_end),
      
      (assign, reg0, ":herd_party"),
  ]),

  #script_buy_cattle_from_village
  # Input: arg1 = village_no, arg2 = amount, arg3 = single_cost
  # Output: reg0 = party_no
  ("buy_cattle_from_village",
    [
      (store_script_param, ":village_no", 1),
      (store_script_param, ":amount", 2),
      (store_script_param, ":single_cost", 3),

      #Changing price of the cattle
      (try_for_range, ":unused", 0, ":amount"),
        (call_script, "script_game_event_buy_item", "itm_cattle_meat", 0),
        (call_script, "script_game_event_buy_item", "itm_cattle_meat", 0),
      (try_end),

      (party_get_slot, ":num_cattle", ":village_no", slot_village_number_of_cattle),
      (val_sub, ":num_cattle", ":amount"),
      (party_set_slot, ":village_no", slot_village_number_of_cattle, ":num_cattle"),
      (store_mul, ":cost", ":single_cost", ":amount"),
      (troop_remove_gold, "trp_player", ":cost"),

      (assign, ":continue", 1),
      (try_for_parties, ":cur_party"),
        (eq, ":continue", 1),
        (party_slot_eq, ":cur_party", slot_party_type, spt_cattle_herd),
        (store_distance_to_party_from_party, ":dist", ":village_no", ":cur_party"),
        (lt, ":dist", 6),
        (assign, ":subcontinue", 1),
        (try_begin),
          (check_quest_active, "qst_move_cattle_herd"),
          (quest_slot_eq, "qst_move_cattle_herd", slot_quest_target_party, ":cur_party"),
          (assign, ":subcontinue", 0),
        (try_end),
        (eq, ":subcontinue", 1),
        (party_add_members, ":cur_party", "trp_cattle", ":amount"),
        (assign, ":continue", 0),
        (assign, reg0, ":cur_party"),
      (try_end),
      (try_begin),
        (eq, ":continue", 1),
        (call_script, "script_create_cattle_herd", ":village_no", ":amount"),
      (try_end),
  ]),

  #script_kill_cattle_from_herd
  # Input: arg1 = party_no, arg2 = amount
  # Output: none (fills trp_temp_troop's inventory)
  ("kill_cattle_from_herd",
    [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":amount"),

      (troop_clear_inventory, "trp_temp_troop"),
      (store_mul, ":meat_amount", ":amount", 2),
      (troop_add_items, "trp_temp_troop", "itm_cattle_meat", ":meat_amount"),

      (troop_get_inventory_capacity, ":inv_size", "trp_temp_troop"),
      (try_for_range, ":i_slot", 0, ":inv_size"),
        (troop_get_inventory_slot, ":item_id", "trp_temp_troop", ":i_slot"),
        (eq, ":item_id", "itm_cattle_meat"),
        (troop_set_inventory_slot_modifier, "trp_temp_troop", ":i_slot", imod_fresh),
      (try_end),

      (party_get_num_companions, ":num_cattle", ":party_no"),
      (try_begin),
        (ge, ":amount", ":num_cattle"),
        (remove_party, ":party_no"),
      (else_try),
        (party_remove_members, ":party_no", "trp_cattle", ":amount"),
      (try_end),
      ]),
  
 
  # script_get_troop_attached_party
  # Input: arg1 = troop_no
  # Output: reg0 = party_no (-1 if troop's party is not attached to a party)
  ("get_troop_attached_party",
    [
      (store_script_param_1, ":troop_no"),
      
      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (assign, ":attached_party_no", -1),
      (try_begin),
        (ge, ":party_no", 0),
        (party_get_attached_to, ":attached_party_no", ":party_no"),
      (try_end),
      (assign, reg0, ":attached_party_no"),
  ]),


  # script_center_get_food_consumption
  # Input: arg1 = center_no
  # Output: reg0: food consumption (1 food item counts as 100 units)
  ("center_get_food_consumption",
    [
      (store_script_param_1, ":center_no"),
      (assign, ":food_consumption", 0),
      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_town),
        (assign, ":food_consumption", 500),
      (else_try),
        (party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (assign, ":food_consumption", 50),
      (try_end),
      (assign, reg0, ":food_consumption"),
  ]),
  
  # script_center_get_food_store_limit
  # Input: arg1 = center_no
  # Output: reg0: food consumption (1 food item counts as 100 units)
  ("center_get_food_store_limit",
    [
      (store_script_param_1, ":center_no"),
      (assign, ":food_store_limit", 0),
      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_town),
        (assign, ":food_store_limit", 50000),
      (else_try),
        (party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (assign, ":food_store_limit", 1500),
      (try_end),
      (assign, reg0, ":food_store_limit"),
  ]),

  # script_refresh_village_merchant_inventory
  # Input: arg1 = village_no
  # Output: none
  ("refresh_village_merchant_inventory",
    [
      (store_script_param_1, ":village_no"),
      (party_get_slot, ":merchant_troop", ":village_no", slot_town_elder),
      (reset_item_probabilities,0),
      (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
      (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
        (store_add, ":cur_price_slot", ":cur_goods", ":item_to_price_slot"),
        (party_get_slot, ":cur_price", ":village_no", ":cur_price_slot"),
        (assign, ":cur_probability", 100),
        (val_mul, ":cur_probability", average_price_factor),
        (val_div, ":cur_probability", ":cur_price"),
        (val_mul, ":cur_probability", average_price_factor),
        (val_div, ":cur_probability", ":cur_price"),
        (val_mul, ":cur_probability", average_price_factor),
        (val_div, ":cur_probability", ":cur_price"),
        (val_mul, ":cur_probability", average_price_factor),
        (val_div, ":cur_probability", ":cur_price"),
        (set_item_probability_in_merchandise, ":cur_goods", ":cur_probability"),
      (try_end),
#      (set_item_probability_in_merchandise, "itm_spice", 0),
#      (set_item_probability_in_merchandise, "itm_velvet", 0),
      (troop_add_merchandise, ":merchant_troop", itp_type_goods, 3),
      (troop_ensure_inventory_space, ":merchant_troop", 80),

      #Adding 1 prosperity to the village while reducing each 3000 gold from the elder
      (store_troop_gold, ":gold",":merchant_troop"),
      (try_begin),
        (gt, ":gold", 3500),
        (store_div, ":prosperity_added", ":gold", 3000),
        (store_mul, ":gold_removed", ":prosperity_added", 3000),
        (troop_remove_gold, ":merchant_troop", ":gold_removed"),
        (call_script, "script_change_center_prosperity", ":village_no", ":prosperity_added"),
      (try_end),
  ]),

  # script_refresh_village_defenders
  # Input: arg1 = village_no
  # Output: none
  ("refresh_village_defenders",
    [
      (store_script_param_1, ":village_no"),

      (assign, ":ideal_size", 50),
      (try_begin),
        (party_get_num_companions, ":party_size", ":village_no"),
        (lt, ":party_size", ":ideal_size"),
        (party_add_template, ":village_no", "pt_village_defenders"),
      (try_end),
  ]),

  # script_village_set_state
  # Input: arg1 = center_no arg2:new_state
  # Output: reg0: food consumption (1 food item counts as 100 units)
  ("village_set_state",
    [
      (store_script_param_1, ":village_no"),
      (store_script_param_2, ":new_state"),
#      (party_get_slot, ":old_state", ":village_no", slot_village_state),
      (try_begin),
        (eq, ":new_state", 0),
        (party_set_extra_text, ":village_no", "str_empty_string"),
        (party_set_slot, ":village_no", slot_village_raided_by, -1),
      (else_try),
        (eq, ":new_state", svs_being_raided),
        (party_set_extra_text, ":village_no", "@(Being Raided)"),
      (else_try),
        (eq, ":new_state", svs_looted),
        (party_set_extra_text, ":village_no", "@(Looted)"),
        (party_set_slot, ":village_no", slot_village_raided_by, -1),
        (call_script, "script_change_center_prosperity", ":village_no", -30),
      (else_try),
        (eq, ":new_state", svs_under_siege),
        (party_set_extra_text, ":village_no", "@(Under Siege)"),
      (try_end),
      (party_set_slot, ":village_no", slot_village_state, ":new_state"),
  ]),


  # script_process_village_raids
  # Input: none
  # Output: none
  # called from triggers every two hours
  ("process_village_raids",
    [
       (try_for_range, ":village_no", villages_begin, villages_end),
         (party_get_slot, ":village_raid_progress", ":village_no", slot_village_raid_progress),
         (try_begin),
           (party_slot_eq, ":village_no", slot_village_state, 0), #village is normal
           (val_sub, ":village_raid_progress", 5),
           (val_max, ":village_raid_progress", 0),
           (party_set_slot, ":village_no", slot_village_raid_progress, ":village_raid_progress"),
         (else_try),
           (party_slot_eq, ":village_no", slot_village_state, svs_being_raided), #village is being raided
       # End raid unless there is an enemy party nearby
           (assign, ":raid_ended", 1),
           (party_get_slot, ":raider_party", ":village_no", slot_village_raided_by),
           (try_begin),
             (ge, ":raider_party", 0),
             (party_is_active, ":raider_party"),
             (this_or_next|neq, ":raider_party", "p_main_party"),
             (eq, "$g_player_is_captive", 0),
             (store_distance_to_party_from_party, ":distance", ":village_no", ":raider_party"),
             (lt, ":distance", raid_distance),
             (assign, ":raid_ended", 0),
           (try_end),
           (try_begin),
             (eq, ":raid_ended", 1),
             (call_script, "script_village_set_state",  ":village_no", 0), #clear raid flag
             (party_set_slot, ":village_no", slot_village_smoke_added, 0),
             (party_clear_particle_systems, ":village_no"),
           (else_try),
             (assign, ":raid_progress_increase", 11),
             (party_get_slot, ":thug_party", ":village_no", slot_village_raided_by),
             (try_begin),
               (party_get_skill_level, ":looting_skill", ":thug_party", "skl_looting"),
               (val_add, ":raid_progress_increase", ":looting_skill"),
             (try_end),
             (try_begin),
               (party_slot_eq, ":village_no", slot_center_has_watch_tower, 1),
               (val_mul, ":raid_progress_increase", 75),
               (val_div, ":raid_progress_increase", 100),
             (try_end),
             (val_add, ":village_raid_progress", ":raid_progress_increase"),
             (party_set_slot, ":village_no", slot_village_raid_progress, ":village_raid_progress"),
             (try_begin),
               (ge, ":village_raid_progress", 50),
               (party_slot_eq, ":village_no", slot_village_smoke_added, 0),
               (party_add_particle_system, ":village_no", "psys_map_village_fire"),
               (party_add_particle_system, ":village_no", "psys_map_village_fire_smoke"),
#               (party_set_icon, ":village_no", "icon_village_burnt_a"), # TLD icons economy, GA
               (party_set_slot, ":village_no", slot_village_smoke_added, 1),
             (try_end),
             (try_begin),
               (gt, ":village_raid_progress", 100),
               (str_store_party_name_link, s1, ":village_no"),
               (party_stack_get_troop_id, ":raid_leader", ":thug_party"),
               (ge, ":raid_leader", 0),
               (str_store_party_name, s2, ":thug_party"),
               (display_log_message, "@The village of {s1} has been looted by {s2}."),
               (call_script, "script_village_set_state",  ":village_no", svs_looted),
               (party_set_slot, ":village_no", slot_village_raid_progress, 0),
               (party_set_slot, ":village_no", slot_village_recover_progress, 0),
               (try_begin),
                 (store_faction_of_party, ":village_faction", ":village_no"),
                 (this_or_next|party_slot_eq, ":village_no", slot_town_lord, "trp_player"),
                 (eq, ":village_faction", "fac_player_supporters_faction"),
                 (call_script, "script_add_notification_menu", "mnu_notification_village_raided", ":village_no", ":raid_leader"),
               (try_end),
               (call_script, "script_add_log_entry", logent_village_raided, ":raid_leader",  ":village_no", -1, -1),
             (try_end),
           (try_end),
         (else_try),
           (party_slot_eq, ":village_no", slot_village_state, svs_looted), #village is looted
           (party_get_slot, ":recover_progress", ":village_no", slot_village_recover_progress),
           (val_add, ":recover_progress", 1),
           (party_set_slot, ":village_no", slot_village_recover_progress, ":recover_progress"), #village looted
           (try_begin),
             (ge, ":recover_progress", 10),
             (party_slot_eq, ":village_no", slot_village_smoke_added, 1),
             (party_clear_particle_systems, ":village_no"),
             (party_add_particle_system, ":village_no", "psys_map_village_looted_smoke"),
             (party_set_slot, ":village_no", slot_village_smoke_added, 2),
           (try_end),
           (try_begin),
             (gt, ":recover_progress", 50),
             (party_slot_eq, ":village_no", slot_village_smoke_added, 2),
             (party_clear_particle_systems, ":village_no"),
             (party_set_slot, ":village_no", slot_village_smoke_added, 3),
#             (party_set_icon, ":village_no", "icon_village_deserted_a"), # TLD icons economy, GA
           (try_end),
           (try_begin),
             (gt, ":recover_progress", 100),
             (call_script, "script_village_set_state",  ":village_no", 0),#village back to normal
             (party_set_slot, ":village_no", slot_village_recover_progress, 0),
             (party_clear_particle_systems, ":village_no"),
             (party_set_slot, ":village_no", slot_village_smoke_added, 0),
             (party_set_icon, ":village_no", "icon_village_a"),
           (try_end),
         (try_end),
       (try_end),
  ]),

 
  # script_process_sieges
  # Input: none
  # Output: none
  #called from triggers
  ("process_sieges",
    [
       (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
         (party_is_active, ":center_no"), #TLD
         #Reducing siege hardness every day by 20
         (party_get_slot, ":siege_hardness", ":center_no", slot_center_siege_hardness),
         (val_sub, ":siege_hardness", 20),
         (val_max, ":siege_hardness", 0),
         (party_set_slot, ":center_no", slot_center_siege_hardness, ":siege_hardness"),
       
         (party_get_slot, ":town_food_store", ":center_no", slot_party_food_store),
         (call_script, "script_center_get_food_store_limit", ":center_no"),
         (assign, ":food_store_limit", reg0),
         (try_begin),
           (party_get_slot, ":besieger_party", ":center_no", slot_center_is_besieged_by),
           (ge, ":besieger_party", 0), #town is under siege
       
           #Reduce prosperity of besieged center by -1 with a 33% chance every day.
           (try_begin),
             (store_random_in_range, ":random_no", 0, 3),
             (eq, ":random_no", 0),
             (call_script, "script_change_center_prosperity", ":center_no", -1),
           (try_end),

           (store_faction_of_party, ":center_faction", ":center_no"),
        # Lift siege unless there is an enemy party nearby
           (assign, ":siege_lifted", 0),
           (try_begin),
             (try_begin),
               (neg|party_is_active, ":besieger_party"),
               (assign, ":siege_lifted", 1),
             (else_try),
               (store_distance_to_party_from_party, ":besieger_distance", ":center_no", ":besieger_party"),
               (gt, ":besieger_distance", 5),
               (assign, ":siege_lifted", 1),
             (else_try), #MV: possibly redundant code
               (store_faction_of_party, ":besieger_faction", ":besieger_party"),
               (store_relation, ":reln", ":besieger_faction", ":center_faction"),
               (gt, ":reln", 0), #MV: if center changed hands
               (assign, ":siege_lifted", 1),
             (try_end),
             (eq, ":siege_lifted", 1),
             (try_for_range, ":enemy_hero", kingdom_heroes_begin, kingdom_heroes_end),
               (troop_slot_eq, ":enemy_hero", slot_troop_occupation, slto_kingdom_hero),
               (troop_get_slot, ":enemy_party", ":enemy_hero", slot_troop_leaded_party),
               (ge, ":enemy_party", 0),
               (party_is_active, ":enemy_party"),
               (store_faction_of_party, ":party_faction", ":enemy_party"),
               (store_relation, ":reln", ":party_faction", ":center_faction"),
               (lt, ":reln", 0),
               (store_distance_to_party_from_party, ":distance", ":center_no", ":enemy_party"),
               (lt, ":distance", 4),
               (assign, ":besieger_party", ":enemy_party"),
               (party_set_slot, ":center_no", slot_center_is_besieged_by, ":enemy_party"),
               (assign, ":siege_lifted", 0),
             (try_end),
           (try_end),
           (try_begin),
             (eq, ":siege_lifted", 1),
             (call_script, "script_lift_siege", ":center_no", 1),
           (else_try),
             (call_script, "script_center_get_food_consumption", ":center_no"),
             (assign, ":food_consumption", reg0),
             (val_sub, ":town_food_store", ":food_consumption"), # reduce food only under siege???
             (try_begin),
               (le, ":town_food_store", 0), #town is starving
               (store_random_in_range, ":r", 0, 100),
               (lt, ":r", 10), 
               (call_script, "script_party_wound_all_members", ":center_no"), # town falls with 10% chance if starving
             (try_end),
           (try_end),
         (else_try),
           #town is not under siege...
           (val_add, ":town_food_store", 30), #add 30 food (significant for castles only.
         (try_end),

         (val_min, ":town_food_store", ":food_store_limit"),
         (val_max, ":town_food_store", 0),
         (party_set_slot, ":center_no", slot_party_food_store, ":town_food_store"),
       (try_end),
  ]),

  # script_lift_siege
  # Input: arg1 = center_no, arg2 = display_message
  # Output: none
  #called from triggers
  ("lift_siege",
    [
      (store_script_param, ":center_no", 1),
      (store_script_param, ":display_message", 2),
      (party_set_slot, ":center_no", slot_center_is_besieged_by, -1), #clear siege
      (call_script, "script_village_set_state",  ":center_no", 0), #clear siege flag
      (try_begin),
        (eq, ":center_no", "$g_player_besiege_town"),
        (assign, "$g_siege_method", 0), #remove siege progress
      (try_end),
      (try_begin),
        (eq, ":display_message", 1),
        (str_store_party_name_link, s3, ":center_no"),
        (try_begin),
          (store_faction_of_party, ":faction", ":center_no"),
          (store_relation, ":rel", "$players_kingdom", ":faction"),
          (gt, ":rel", 0),
          (assign, ":news_color", color_good_news),
        (else_try),
          (assign, ":news_color", color_bad_news),
        (try_end),
        (display_message, "@{s3} is no longer under siege.", ":news_color"),
      (try_end),
      ]),


  # script_process_alarms
  # Input: none
  # Output: none
  #called from triggers
  ("process_alarms",
    [(try_for_range, ":center_no", centers_begin, centers_end),
       (party_set_slot, ":center_no", slot_center_last_spotted_enemy, -1),
     (try_end),
     (assign, ":spotting_range", 2),
     (try_begin),
       (is_currently_night),
       (assign, ":spotting_range", 1),
     (try_end),
     (try_begin),
       (party_slot_eq, ":center_no", slot_center_has_watch_tower, 1),
       (val_mul, ":spotting_range", 2),
     (try_end),
     (try_for_parties, ":party_no"),
       (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
       (neg|party_is_in_any_town, ":party_no"),
       (store_faction_of_party, ":party_faction", ":party_no"),
       (try_for_range, ":center_no", centers_begin, centers_end),
         (party_is_active, ":center_no"), #TLD
         (store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),
         (le, ":distance", ":spotting_range"),
         (store_faction_of_party, ":center_faction", ":center_no"),
         (store_relation, ":reln", ":center_faction", ":party_faction"),
         (lt, ":reln", 0),
         (party_set_slot, ":center_no", slot_center_last_spotted_enemy, ":party_no"), 
       (try_end),
     (try_end),
     (try_for_range, ":center_no", centers_begin, centers_end),
       (party_is_active, ":center_no"), #TLD
       (store_faction_of_party, ":center_faction", ":center_no"),
       (this_or_next|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
       (eq, ":center_faction", "$players_kingdom"),
       (party_get_slot, ":enemy_party", ":center_no", slot_center_last_spotted_enemy),
       (ge, ":enemy_party", 0),
       (store_distance_to_party_from_party, ":dist", "p_main_party", ":center_no"),
       (assign, ":has_messenger", 0),
       (try_begin),
         (this_or_next|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
         (eq, ":center_faction", "fac_player_supporters_faction"),
         (party_slot_eq, ":center_no", slot_center_has_messenger_post, 1),
         (assign, ":has_messenger", 1),
       (try_end),
       (this_or_next|lt, ":dist", 30),
       (eq, ":has_messenger", 1),
       (str_store_party_name_link, s1, ":center_no"),
       (display_message, "@Enemies spotted near {s1}."),
     (try_end),
     ]),

  # script_select_faction_marshall
  # Input: arg1: faction_no
  # Output: none
  #called from triggers
  ("select_faction_marshall",
   [
     (store_script_param_1, ":faction_no"),
     (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
     (faction_get_slot, ":old_faction_marshall", ":faction_no", slot_faction_marshall),
     (assign, ":total_renown", 0),
     (try_for_range, ":loop_var", "trp_kingdom_heroes_including_player_begin", kingdom_heroes_end),
       (assign, ":cur_troop", ":loop_var"),
       (assign, ":continue", 0),
       (try_begin),
         (eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
         (assign, ":cur_troop", "trp_player"),
         (try_begin),
           (eq, ":faction_no", "$players_kingdom"),
           (assign, ":continue", 1),
         (try_end),
       (else_try),
         (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
         (store_troop_faction, ":cur_faction", ":cur_troop"),
         (eq, ":cur_faction", ":faction_no"),
         (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
         (gt, ":cur_party", 0),
         (party_is_active, ":cur_party"),
         (call_script, "script_party_count_fit_for_battle", ":cur_party"),
         (assign, ":party_fit_for_battle", reg0),
         (call_script, "script_party_get_ideal_size", ":cur_party"),
         (assign, ":ideal_size", reg0),
         (store_mul, ":relative_strength", ":party_fit_for_battle", 100),
         (val_div, ":relative_strength", ":ideal_size"),
         (ge, ":relative_strength", 25),
         (assign, ":continue", 1),
       (try_end),
       (eq, ":continue", 1),
       (troop_get_slot, ":renown", ":cur_troop", slot_troop_renown),
       (try_begin),
         (eq, ":cur_troop", "trp_player"),
         (neq, ":old_faction_marshall", "trp_player"),
         (assign, ":renown", 0),
       (try_end),
       (try_begin),
         (eq, ":cur_troop", ":faction_leader"),
         (val_mul, ":renown", 3),
         (val_div, ":renown", 4),
       (try_end),
       (try_begin),
         (eq, ":cur_troop", ":old_faction_marshall"),
         (val_mul, ":renown", 1000),
       (try_end),
       (val_add, ":total_renown", ":renown"),
     (try_end),
     (assign, ":result", -1),
     (try_begin),
       (gt, ":total_renown", 0),
       (store_random_in_range, ":random_renown", 0, ":total_renown"),
       (try_for_range, ":loop_var", "trp_kingdom_heroes_including_player_begin", kingdom_heroes_end),
         (eq, ":result", -1),
         (assign, ":cur_troop", ":loop_var"),
         (assign, ":continue", 0),
         (try_begin),
           (eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
           (assign, ":cur_troop", "trp_player"),
           (try_begin),
             (eq, ":faction_no", "$players_kingdom"),
             (assign, ":continue", 1),
           (try_end),
         (else_try),
           (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
           (store_troop_faction, ":cur_faction", ":cur_troop"),
           (eq, ":cur_faction", ":faction_no"),
           (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
           (gt, ":cur_party", 0),
           (party_is_active, ":cur_party"),
           (call_script, "script_party_count_fit_for_battle", ":cur_party"),
           (assign, ":party_fit_for_battle", reg0),
           (call_script, "script_party_get_ideal_size", ":cur_party"),
           (assign, ":ideal_size", reg0),
           (store_mul, ":relative_strength", ":party_fit_for_battle", 100),
           (val_div, ":relative_strength", ":ideal_size"),
           (ge, ":relative_strength", 25),
           (assign, ":continue", 1),
         (try_end),
         (eq, ":continue", 1),
         (troop_get_slot, ":renown", ":cur_troop", slot_troop_renown),
         (try_begin),
           (eq, ":cur_troop", "trp_player"),
           (neq, ":old_faction_marshall", "trp_player"),
           (assign, ":renown", 0),
         (try_end),
         (try_begin),
           (eq, ":cur_troop", ":faction_leader"),
           (val_mul, ":renown", 3),
           (val_div, ":renown", 4),
         (try_end),
         (try_begin),
           (eq, ":cur_troop", ":old_faction_marshall"),
           (val_mul, ":renown", 1000),
         (try_end),
         (val_sub, ":random_renown", ":renown"),
         (lt, ":random_renown", 0),
         (assign, ":result", ":cur_troop"),
       (try_end),
     (try_end),
     (try_begin),
       (eq, "$cheat_mode", 1),
       (ge, ":result", 0),
       (str_store_troop_name, s1, ":result"),
       (str_store_faction_name, s2, ":faction_no"),
       (display_message, "@{s1} is chosen as the marshall of {s2}."),
     (try_end),
     (assign, reg0, ":result"),
     ]),

  # script_get_center_faction_relation_including_player
  # Input: arg1: center_no, arg2: target_faction_no
  # Output: reg0: relation
  #called from triggers
  ("get_center_faction_relation_including_player",
   [
     (store_script_param, ":center_no", 1),
     (store_script_param, ":target_faction_no", 2),
     (store_faction_of_party, ":center_faction", ":center_no"),
     (store_relation, ":reln", ":center_faction", ":target_faction_no"),
     (try_begin),
       (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
       (store_relation, ":reln", "fac_player_supporters_faction", ":target_faction_no"),
     (try_end),
     (assign, reg0, ":reln"),
     ]),
  
  # script_check_and_finish_active_army_quests_for_faction
  # Input: faction_no
  # Output: none
  ("check_and_finish_active_army_quests_for_faction",
   [
     (store_script_param_1, ":faction_no"),
     (try_begin),
       (eq, "$players_kingdom", ":faction_no"),
       (try_begin),
         (check_quest_active, "qst_report_to_army"),
         (call_script, "script_cancel_quest", "qst_report_to_army"),
       (try_end),
       (assign, ":one_active", 0),
       (try_for_range, ":quest_no", army_quests_begin, army_quests_end),
         (check_quest_active, ":quest_no"),
         (call_script, "script_cancel_quest", ":quest_no"),
         (assign, ":one_active", 1),
       (try_end),
       (try_begin),
         (check_quest_active, "qst_follow_army"),
         (assign, ":one_active", 1),
         (call_script, "script_end_quest", "qst_follow_army"),
       (try_end),
       (eq, ":one_active", 1),
       (faction_get_slot, ":last_offensive_time", ":faction_no", slot_faction_ai_last_offensive_time),
       (store_current_hours, ":cur_hours"),
       (store_sub, ":total_time_served", ":cur_hours", ":last_offensive_time"),
       (store_mul, ":xp_reward", ":total_time_served", 5),
       (val_div, ":xp_reward", 50),
       (val_mul, ":xp_reward", 50),
       (val_add, ":xp_reward", 50),
       (add_xp_as_reward, ":xp_reward"),
     (try_end),
    ]),
  
    # script_troop_get_player_relation
    # Input: arg1 = troop_no
    # Output: reg0 = effective relation (modified by troop reputation, honor, etc.)
    ("troop_get_player_relation",
      [
        (store_script_param_1, ":troop_no"),
        (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
        (troop_get_slot, ":effective_relation", ":troop_no", slot_troop_player_relation),
        (assign, ":honor_bonus", 0),
        (try_begin),
          (eq,  ":reputation", lrep_quarrelsome),
          (val_add, ":effective_relation", -3),
        (try_end),
        (try_begin),
          (ge, "$player_honor", 0),
          (try_begin),
            (this_or_next|eq,  ":reputation", lrep_upstanding),
            (             eq,  ":reputation", lrep_goodnatured),
            (store_div, ":honor_bonus", "$player_honor", 3),
          (try_end),
        (try_end),
        (try_begin),
          (lt, "$player_honor", 0),
          (try_begin),
            (this_or_next|eq,  ":reputation", lrep_upstanding),
            (             eq,  ":reputation", lrep_goodnatured),
            (store_div, ":honor_bonus", "$player_honor", 3),
          (else_try),
            (eq,  ":reputation", lrep_martial),
            (store_div, ":honor_bonus", "$player_honor", 5),
          (try_end),
        (try_end),
        (val_add, ":effective_relation", ":honor_bonus"),
        (assign, reg0, ":effective_relation"),
    ]),
  
  # script_change_troop_renown
  # Input: arg1 = troop_no, arg2 = relation difference
  ("change_troop_renown",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":renown_change"),
      
      (troop_get_slot, ":old_renown", ":troop_no", slot_troop_renown),
      (store_add, ":new_renown", ":old_renown", ":renown_change"),
      (val_max, ":new_renown", 0),
      (troop_set_slot, ":troop_no", slot_troop_renown, ":new_renown"),

      (try_begin),
        (eq, ":troop_no", "trp_player"),
        (str_store_troop_name, s1, ":troop_no"),
        (assign, reg12, ":renown_change"),
        (val_abs, reg12),
        (try_begin),
         (gt, ":renown_change", 0),
         (display_message, "@You gained {reg12} renown.", color_good_news),
        (else_try),
          (lt, ":renown_change", 0),
          (display_message, "@You lose {reg12} renown.", color_bad_news),
        (try_end),
      (try_end),
      (call_script, "script_update_troop_notes", ":troop_no"),
  ]),
  
  
  # script_change_player_relation_with_troop
  # Input: arg1 = troop_no, arg2 = relation difference
  ("change_player_relation_with_troop",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":difference"),

      (try_begin),
        (neq, ":troop_no", "trp_player"),
        (neg|is_between, ":troop_no", soldiers_begin, soldiers_end),
        (neq, ":difference", 0),
        (call_script, "script_troop_get_player_relation", ":troop_no"),
        (assign, ":old_effective_relation", reg0),
        (troop_get_slot, ":player_relation", ":troop_no", slot_troop_player_relation),
        (val_add, ":player_relation", ":difference"),
        (val_clamp, ":player_relation", -100, 101),
        (try_begin),
          (troop_set_slot, ":troop_no", slot_troop_player_relation, ":player_relation"),
          
          (str_store_troop_name_link, s1, ":troop_no"),
          (call_script, "script_troop_get_player_relation", ":troop_no"),
          (assign, ":new_effective_relation", reg0),
          (neq, ":old_effective_relation", ":new_effective_relation"),
          (assign, reg1, ":old_effective_relation"),
          (assign, reg2, ":new_effective_relation"),
          (try_begin),
            (gt, ":difference", 0),
            (display_message, "str_troop_relation_increased", color_good_news),
          (else_try),
            (lt, ":difference", 0),
            (display_message, "str_troop_relation_detoriated", color_bad_news),
          (try_end),
          (try_begin),
            (eq, ":troop_no", "$g_talk_troop"),
            (assign, "$g_talk_troop_relation", ":new_effective_relation"),
            (call_script, "script_setup_talk_info"),
          (try_end),
          (call_script, "script_update_troop_notes", ":troop_no"),
        (try_end),
      (try_end),
  ]),

  # script_change_player_relation_with_center
  # Input: arg1 = party_no, arg2 = relation difference
  ("change_player_relation_with_center",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":difference"),
      
      (party_get_slot, ":player_relation", ":center_no", slot_center_player_relation),
      (assign, reg1, ":player_relation"),
      (val_add, ":player_relation", ":difference"),
      (val_clamp, ":player_relation", -100, 100),
      (assign, reg2, ":player_relation"),
      (party_set_slot, ":center_no", slot_center_player_relation, ":player_relation"),
      
      (str_store_party_name_link, s1, ":center_no"),
      (try_begin),
        (gt, ":difference", 0),
        (display_message, "@Your relation with {s1} has improved.", color_good_news),
      (else_try),
        (lt, ":difference", 0),
        (display_message, "@Your relation with {s1} has deteriorated."),
      (try_end),
      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_village),
        (call_script, "script_update_volunteer_troops_in_village", ":center_no"),
      (try_end),
      
      (try_begin),
        (this_or_next|is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
        (is_between, "$g_talk_troop", mayors_begin, mayors_end),
        (assign, "$g_talk_troop_relation", ":player_relation"),
        (call_script, "script_setup_talk_info"),
      (try_end),
  ]),
  
  
  # script_change_player_relation_with_faction
  # Input: arg1 = faction_no, arg2 = relation difference
  ("change_player_relation_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":difference"),
      
      (store_relation, ":player_relation", ":faction_no", "fac_player_supporters_faction"),
      (assign, reg1, ":player_relation"),
      (val_add, ":player_relation", ":difference"),
      (assign, reg2, ":player_relation"),
      (set_relation, ":faction_no", "fac_player_faction", ":player_relation"),
      (set_relation, ":faction_no", "fac_player_supporters_faction", ":player_relation"),
      
      (str_store_faction_name_link, s1, ":faction_no"),
      (try_begin),
        (gt, ":difference", 0),
        (display_message, "str_faction_relation_increased", color_good_news),
      (else_try),
        (lt, ":difference", 0),
        (display_message, "str_faction_relation_detoriated", color_bad_news),
      (try_end),
      (call_script, "script_update_all_notes"),
      ]),

  # script_set_player_relation_with_faction
  # Input: arg1 = faction_no, arg2 = relation
  ("set_player_relation_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":relation"),
      
      (store_relation, ":player_relation", ":faction_no", "fac_player_supporters_faction"),
      (store_sub, ":reln_dif", ":relation", ":player_relation"),
      (call_script, "script_change_player_relation_with_faction", ":faction_no", ":reln_dif"),
      ]),


  # script_cf_get_random_active_faction_except_player_faction_and_faction
  # Input: arg1 = except_faction_no
  # Output: reg0 = random_faction
  ("cf_get_random_active_faction_except_player_faction_and_faction",
    [
      (store_script_param_1, ":except_faction_no"),
      (assign, ":num_factions", 0),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (neq, ":faction_no", ":except_faction_no"),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (val_add, ":num_factions", 1),
      (try_end),
      (gt, ":num_factions", 0),
      (assign, ":selected_faction", -1),
      (store_random_in_range, ":random_faction", 0, ":num_factions"),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (ge, ":random_faction", 0),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (neq, ":faction_no", ":except_faction_no"),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (val_sub, ":random_faction", 1),
        (lt, ":random_faction", 0),
        (assign, ":selected_faction", ":faction_no"),
      (try_end),
      (assign, reg0, ":selected_faction"),
  ]),

  # script_make_kingdom_hostile_to_player
  # Input: arg1 = faction_no, arg2 = relation difference
  # Output: none
  ("make_kingdom_hostile_to_player",
    [
      (store_script_param_1, ":kingdom_no"),
      (store_script_param_2, ":difference"),

      (try_begin),
        (lt, ":difference", 0),
        (store_relation, ":player_relation", ":kingdom_no", "fac_player_supporters_faction"),
        (val_min, ":player_relation", 0),
        (val_add, ":player_relation", ":difference"),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_no", ":player_relation"),
      (try_end),
  ]),
  
  # script_change_player_honor
  # Input: arg1 = honor difference
  # Output: none
  ("change_player_honor",
    [
      (store_script_param_1, ":honor_dif"),
      (val_add, "$player_honor", ":honor_dif"),
      (try_begin),
        (gt, ":honor_dif", 0),
        (display_message, "@You gain honour.", color_good_news),
      (else_try),
        (lt, ":honor_dif", 0),
        (display_message, "@You lose honour.", color_bad_news),
      (try_end),

##      (val_mul, ":honor_dif", 1000),
##      (assign, ":temp_honor", 0),
##      (assign, ":num_nonlinear_steps", 10),
##      (try_begin),
##        (gt, "$player_honor", 0),
##        (lt, ":honor_dif", 0),
##        (assign, ":num_nonlinear_steps", 0),
##      (else_try),
##        (lt, "$player_honor", 0),
##        (gt, ":honor_dif", 0),
##        (assign, ":num_nonlinear_steps", 3),
##      (try_end),
##      
##      (try_begin),
##        (ge, "$player_honor", 0),
##        (assign, ":temp_honor", "$player_honor"),
##      (else_try),
##        (val_sub, ":temp_honor", "$player_honor"),
##      (try_end),
##      (try_for_range, ":unused",0,":num_nonlinear_steps"),
##        (ge, ":temp_honor", 10000),
##        (val_div, ":temp_honor", 2),
##        (val_div, ":honor_dif", 2),
##      (try_end),
##      (val_add, "$player_honor", ":honor_dif"),
  ]),

  # script_change_player_party_morale
  # Input: arg1 = morale difference
  # Output: none
  ("change_player_party_morale",
    [
      (store_script_param_1, ":morale_dif"),
      (party_get_morale, ":cur_morale", "p_main_party"),
      (store_add, ":new_morale", ":cur_morale", ":morale_dif"),
      (val_clamp, ":new_morale", 0, 100),
      (party_set_morale, "p_main_party", ":new_morale"),
      (try_begin),
        (lt, ":new_morale", ":cur_morale"),
        (store_sub, reg1, ":cur_morale", ":new_morale"),
        (display_message, "str_party_lost_morale", color_bad_news),
      (else_try),
        (gt, ":new_morale", ":cur_morale"),
        (store_sub, reg1, ":new_morale", ":cur_morale"),
        (display_message, "str_party_gained_morale", color_good_news),
      (try_end),
  ]),

  # script_cf_player_has_item_without_modifier
  # Input: arg1 = item_id, arg2 = modifier
  # Output: none (can_fail)
  ("cf_player_has_item_without_modifier",
    [
      (store_script_param, ":item_id", 1),
      (store_script_param, ":modifier", 2),
      (player_has_item, ":item_id"),
      #checking if any of the meat is not rotten
      (assign, ":has_without_modifier", 0),
      (troop_get_inventory_capacity, ":inv_size", "trp_player"),
      (try_for_range, ":i_slot", 0, ":inv_size"),
        (troop_get_inventory_slot, ":cur_item", "trp_player", ":i_slot"),
        (eq, ":cur_item", ":item_id"),
        (troop_get_inventory_slot_modifier, ":cur_modifier", "trp_player", ":i_slot"),
        (neq, ":cur_modifier", ":modifier"),
        (assign, ":has_without_modifier", 1),
        (assign, ":inv_size", 0), #break
      (try_end),
      (eq, ":has_without_modifier", 1),
  ]),

  # script_get_player_party_morale_values
  # Output: reg0 = player_party_morale_target
  ("get_player_party_morale_values",
    [
      (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
      (assign, ":num_men", 0),
      (try_for_range, ":i_stack", 1, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (val_add, ":num_men", 3),
        (else_try),
          (party_stack_get_size, ":stack_size","p_main_party",":i_stack"),
          (val_add, ":num_men", ":stack_size"),
        (try_end),
      (try_end),
      (assign, "$g_player_party_morale_modifier_party_size", ":num_men"),
    
      (store_skill_level, ":player_leadership", "skl_leadership", "trp_player"),
      (store_mul, "$g_player_party_morale_modifier_leadership", ":player_leadership", 7),
      (assign, ":new_morale", "$g_player_party_morale_modifier_leadership"),
      (val_sub, ":new_morale", "$g_player_party_morale_modifier_party_size"),
      (val_add, ":new_morale", 50),

      (assign, "$g_player_party_morale_modifier_food", 0),
      (try_for_range, ":cur_edible", food_begin, food_end),
        (call_script, "script_cf_player_has_item_without_modifier", ":cur_edible", imod_rotten),
        (item_get_slot, ":food_bonus", ":cur_edible", slot_item_food_bonus),
        (val_add, "$g_player_party_morale_modifier_food", ":food_bonus"),
      (try_end),
      (val_add, ":new_morale", "$g_player_party_morale_modifier_food"),

      (try_begin),
        (eq, "$g_player_party_morale_modifier_food", 0),
        (assign, "$g_player_party_morale_modifier_no_food", 30),
        (val_sub, ":new_morale", "$g_player_party_morale_modifier_no_food"),
      (else_try),
        (assign, "$g_player_party_morale_modifier_no_food", 0),
      (try_end),

	  # TLD: nothing for this
      #(assign, "$g_player_party_morale_modifier_debt", 0),
      #(try_begin),
      #  (gt, "$g_player_debt_to_party_members", 0),
      #  (call_script, "script_calculate_player_faction_wage"),
      #  (assign, ":total_wages", reg0),
      #  (store_mul, "$g_player_party_morale_modifier_debt", "$g_player_debt_to_party_members", 10),
      #  (val_div, "$g_player_party_morale_modifier_debt", ":total_wages"),
      #  (val_clamp, "$g_player_party_morale_modifier_debt", 1, 31),
      #  (val_sub, ":new_morale", "$g_player_party_morale_modifier_debt"),
      #(try_end),

      (val_clamp, ":new_morale", 0, 100),
      (assign, reg0, ":new_morale"),
      ]),
  
  # script_diplomacy_start_war_between_kingdoms
  # Input: arg1 = kingdom_1, arg2 = kingdom_2, arg3 = initializing_war_peace_cond
  # Output: none
  ("diplomacy_start_war_between_kingdoms", #sets relations between two kingdoms and their vassals.
    [
      (store_script_param, ":kingdom_a", 1),
      (store_script_param, ":kingdom_b", 2),
      (store_script_param, ":initializing_war_peace_cond", 3),
      
      (store_relation, ":relation", ":kingdom_a", ":kingdom_b"),
      (val_min, ":relation", -10),
      (val_add, ":relation", -30),
      (set_relation, ":kingdom_a", ":kingdom_b", ":relation"),

      (try_begin),
        (eq, "$players_kingdom", ":kingdom_a"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_b"),
        (val_min, ":relation", -30),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_b", ":relation"),
      (else_try),
        (eq, "$players_kingdom", ":kingdom_b"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_a"),
        (val_min, ":relation", -30),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_a", ":relation"),
      (try_end),

      (try_begin),
        (eq, ":initializing_war_peace_cond", 1),
        (try_begin),
          (store_random_in_range, ":random_no", 0, 2),
          (this_or_next|eq, ":kingdom_a", "fac_player_supporters_faction"),
          (eq, ":random_no", 0),
          (assign, ":local_temp", ":kingdom_a"),
          (assign, ":kingdom_a", ":kingdom_b"),
          (assign, ":kingdom_b", ":local_temp"),
        (try_end),
        (str_store_faction_name_link, s1, ":kingdom_a"),
        (str_store_faction_name_link, s2, ":kingdom_b"),
        (display_log_message, "@{s1} has declared war against {s2}."),

        (call_script, "script_add_notification_menu", "mnu_notification_war_declared", ":kingdom_a", ":kingdom_b"),

        (call_script, "script_update_faction_notes", ":kingdom_a"),
        (call_script, "script_update_faction_notes", ":kingdom_b"),
        (assign, "$g_recalculate_ais", 1),
      (try_end),
  ]),
  
  # script_event_kingdom_make_peace_with_kingdom
  # Input: arg1 = source_kingdom, arg2 = target_kingdom
  # Output: none
  ("event_kingdom_make_peace_with_kingdom",
    [
      (store_script_param_1, ":source_kingdom"),
      (store_script_param_2, ":target_kingdom"),
      (try_begin),
        (check_quest_active, "qst_capture_prisoners"),
        (try_begin),
          (eq, "$players_kingdom", ":source_kingdom"),
          (quest_slot_eq, "qst_capture_prisoners", slot_quest_target_faction, ":target_kingdom"),
          (call_script, "script_cancel_quest", "qst_capture_prisoners"),
        (else_try),
          (eq, "$players_kingdom", ":target_kingdom"),
          (quest_slot_eq, "qst_capture_prisoners", slot_quest_target_faction, ":source_kingdom"),
          (call_script, "script_cancel_quest", "qst_capture_prisoners"),
        (try_end),
      (try_end),
  ]),

# script_exchange_prisoners_between_factions
# Input: arg1 = faction_no_1, arg2 = faction_no_2
  ("exchange_prisoners_between_factions",
   [
       (store_script_param_1, ":faction_no_1"),
       (store_script_param_2, ":faction_no_2"),
       (assign, ":faction_no_3", -1),
       (assign, ":faction_no_4", -1),
       (try_begin),
         (this_or_next|eq, "$players_kingdom", ":faction_no_1"),
         (eq, "$players_kingdom", ":faction_no_2"),
         (assign, ":faction_no_3", "fac_player_faction"),
         (assign, ":faction_no_4", "fac_player_supporters_faction"),
       (try_end),

       (try_for_parties, ":party_no"),
         (store_faction_of_party, ":party_faction", ":party_no"),
         (this_or_next|eq, ":party_faction", ":faction_no_1"),
         (this_or_next|eq, ":party_faction", ":faction_no_2"),
         (this_or_next|eq, ":party_faction", ":faction_no_3"),
         (eq, ":party_faction", ":faction_no_4"),
         (party_get_num_prisoner_stacks, ":num_stacks", ":party_no"),
         (try_for_range_backwards, ":troop_iterator", 0, ":num_stacks"),
           (party_prisoner_stack_get_troop_id, ":cur_troop_id", ":party_no", ":troop_iterator"),
           (store_troop_faction, ":cur_faction", ":cur_troop_id"),
           (this_or_next|eq, ":cur_faction", ":faction_no_1"),
           (this_or_next|eq, ":cur_faction", ":faction_no_2"),
           (this_or_next|eq, ":cur_faction", ":faction_no_3"),
           (eq, ":cur_faction", ":faction_no_4"),
           (try_begin),
             (troop_is_hero, ":cur_troop_id"),
             (call_script, "script_remove_troop_from_prison", ":cur_troop_id"),
           (try_end),
           (party_prisoner_stack_get_size, ":stack_size", ":party_no", ":troop_iterator"),
           (party_remove_prisoners, ":party_no", ":cur_troop_id", ":stack_size"),
         (try_end),
       (try_end),
    ]),

  # script_add_notification_menu
  # Input: arg1 = menu_no, arg2 = menu_var_1, arg3 = menu_var_2
  # Output: none
  ("add_notification_menu",
    [
      (store_script_param, ":menu_no", 1),
      (store_script_param, ":menu_var_1", 2),
      (store_script_param, ":menu_var_2", 3),
      (assign, ":end_cond", 1),
      (try_for_range, ":cur_slot", 0, ":end_cond"),
        (try_begin),
          (troop_slot_ge, "trp_notification_menu_types", ":cur_slot", 1),
          (val_add, ":end_cond", 1),
        (else_try),
          (troop_set_slot, "trp_notification_menu_types", ":cur_slot", ":menu_no"),
          (troop_set_slot, "trp_notification_menu_var1", ":cur_slot", ":menu_var_1"),
          (troop_set_slot, "trp_notification_menu_var2", ":cur_slot", ":menu_var_2"),
        (try_end),
      (try_end),
      ]),
  
  # script_finish_quest
  # Input: arg1 = quest_no, arg2 = finish_percentage
  # Output: none
  ("finish_quest",
    [
      (store_script_param_1, ":quest_no"),
      (store_script_param_2, ":finish_percentage"),
      
      (quest_get_slot, ":quest_giver", ":quest_no", slot_quest_giver_troop),
      (quest_get_slot, ":quest_importance", ":quest_no", slot_quest_importance),
      (quest_get_slot, ":quest_xp_reward", ":quest_no", slot_quest_xp_reward),
      (quest_get_slot, ":quest_gold_reward", ":quest_no", slot_quest_gold_reward),
      
      (try_begin),
        (lt, ":finish_percentage", 100),
        (val_mul, ":quest_xp_reward", ":finish_percentage"),
        (val_div, ":quest_xp_reward", 100),
        (val_mul, ":quest_gold_reward", ":finish_percentage"),
        (val_div, ":quest_gold_reward", 100),
        #Changing the relation factor. Negative relation if less than 75% of the quest is finished.
        #Positive relation if more than 75% of the quest is finished.
        (assign, ":importance_multiplier", ":finish_percentage"),
        (val_sub, ":importance_multiplier", 75),
        (val_mul, ":quest_importance", ":importance_multiplier"),
        (val_div, ":quest_importance", 100),
      (else_try),
        (val_div, ":quest_importance", 4),
        (val_add, ":quest_importance", 1),
        (call_script, "script_change_player_relation_with_troop", ":quest_giver", ":quest_importance"),
      (try_end),
      
      (add_xp_as_reward, ":quest_xp_reward"),
      (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
      (call_script, "script_end_quest", ":quest_no"),
  ]),
  
  
  # script_get_information_about_troops_position
  # Input: arg1 = troop_no, arg2 = time (0 if present tense, 1 if past tense)
  # Output: s1 = String, reg0 = knows-or-not
  ("get_information_about_troops_position",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, reg3),
      (troop_get_type, reg4, ":troop_no"),
      (str_store_troop_name, s2, ":troop_no"),
      
      (assign, ":found", 0),
      (troop_get_slot, ":center_no", ":troop_no", slot_troop_cur_center),
      (try_begin),
        (gt, ":center_no", 0),
        (is_between, ":center_no", centers_begin, centers_end),
        (str_store_party_name_link, s3, ":center_no"),
        (str_store_string, s1, "@{s2} {reg3?was:is currently} at {s3}."),
        (assign, ":found", 1),
      (else_try),
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
        (gt, ":party_no", 0),
        (call_script, "script_get_troop_attached_party", ":troop_no"),
        (assign, ":center_no", reg0),
        (try_begin),
          (is_between, ":center_no", centers_begin, centers_end),
          (str_store_party_name_link, s3, ":center_no"),
          (str_store_string, s1, "@{s2} {reg3?was:is currently} at {s3}."),
          (assign, ":found", 1),
        (else_try),
          (get_party_ai_behavior, ":ai_behavior", ":party_no"),
          (eq, ":ai_behavior", ai_bhvr_travel_to_party),
          (get_party_ai_object, ":ai_object", ":party_no"),
          (is_between, ":ai_object", centers_begin, centers_end),
          (call_script, "script_get_closest_center", ":party_no"),
          (str_store_party_name_link, s4, reg0),
          (str_store_party_name_link, s3, ":ai_object"),
          (str_store_string, s1, "@{s2} {reg3?was:is} travelling to {s3} and {reg4?she:he} {reg3?was:should be} close to {s4}{reg3?: at the moment}."),
          (assign, ":found", 1),
        (else_try),
          (call_script, "script_get_closest_center", ":party_no"),
          (str_store_party_name_link, s3, reg0),
          (str_store_string, s1, "@{s2} {reg3?was:is} in wilderness and {reg4?she:he} {reg3?was:should be} close to {s3}{reg3?: at the moment}."),
          (assign, ":found", 1),
        (try_end),
      (else_try),
        #(troop_slot_ge, ":troop_no", slot_troop_is_prisoner, 1),
        (troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
        (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
          (party_is_active, ":center_no"), #TLD
          (party_count_prisoners_of_type, ":num_prisoners", ":center_no", ":troop_no"),
          (gt, ":num_prisoners", 0),
          (assign, ":found", 1),
          (str_store_party_name_link, s3, ":center_no"),
          (str_store_string, s1, "@{s2} {reg3?was:is} being held captive at {s3}."),
        (try_end),
        (try_begin),
          (eq, ":found", 0),
          (str_store_string, s1, "@{s2} {reg3?was:has been} taken captive by {reg4?her:his} enemies."),
          (assign, ":found", 1),
        (try_end),
      (try_end),
      (try_begin),
        (eq, ":found", 0),
        (str_store_string, s1, "@{reg3?{s2}'s location was unknown:I don't know where {s2} is}."),
      (try_end),
      (assign, reg0, ":found"),
  ]),

  # script_recruit_troop_as_companion
  # Input: arg1 = troop_no,
  # Output: none
  ("recruit_troop_as_companion",
    [ (store_script_param_1, ":troop_no"),
      (troop_set_slot, ":troop_no", slot_troop_occupation, slto_player_companion),
      #(troop_set_slot, ":troop_no", slot_troop_cur_center, -1),
      (troop_set_auto_equip, ":troop_no",0),
      (party_add_members, "p_main_party", ":troop_no", 1),
      (str_store_troop_name, s6, ":troop_no"),
      (display_message, "@{s6} has joined your party"),
  ]),
  

  # script_setup_random_scene
  # Input: arg1 = center_no, arg2 = mission_template_no
  # Output: none
  ("setup_random_scene",
    [(party_get_current_terrain, ":terrain_type", "p_main_party"),
     (assign, ":scene_to_use", 0),
	
# check if near small fords
	 (try_for_range,":ford","p_ford_cerin_dolen","p_ford_moria2"),
	    (store_distance_to_party_from_party,":dist","p_main_party",":ford"),
	    (lt,":dist",3), (assign,":scene_to_use","scn_battle_scene_plain_01"), #placeholder scenes
	 (try_end),

# check if near large fords
  (try_begin),
     (eq,":scene_to_use",0),
	 (try_for_range,":ford","p_ford_cair_andros1","p_ford_cerin_dolen"),
	   (store_distance_to_party_from_party,":dist","p_main_party",":ford"),
	   (lt,":dist",3), (assign,":scene_to_use","scn_battle_scene_plain_02"), #placeholder scenes
	 (try_end),
  (try_end),
  
# check if near Gondor towns (farms and fields scenes)

# check if in Lorien (elven forest scenes)

# check if in Fangorn (Fangorn forest scenes)

# checks depleted, completely random terrain generated
  (try_begin),
     (eq,":scene_to_use",0),	
     (assign, ":scene_to_use", "scn_random_scene_plain"),
  #  player party temporary relocation to map Z=0, anti-crazy-hills. GA
     (assign,"$relocated",1),
	 (party_relocate_near_party,"p_pointer_player","p_main_party",0), #remember original player location
     
	 (try_begin),
        (store_random_in_range, ":radius", 1, 5), # radius around base terrain Z=0 position for seed generation
        
		(this_or_next|eq, ":terrain_type", rt_steppe),
        (this_or_next|eq, ":terrain_type", rt_plain ),
        (this_or_next|eq, ":terrain_type", rt_snow  ),
        (             eq, ":terrain_type", rt_desert),
#        (store_random_in_range, ":terrain", 0, 4), #randomness off
        (try_begin),
		   (eq, ":terrain_type", rt_steppe),
		   (assign, ":scene_to_use", "scn_random_scene_steppe"),           (display_message,"@SCENE: steppe"),
		   (party_relocate_near_party,"p_main_party", "p_pointer_z_0_steppe",":radius"),
        (else_try),
		   (eq, ":terrain_type", rt_plain),
		   (assign, ":scene_to_use", "scn_random_scene_plain" ),           (display_message,"@SCENE: plain"),
		   (party_relocate_near_party,"p_main_party", "p_pointer_z_0_plain" ,":radius"),
        (else_try),
		   (eq, ":terrain_type", rt_snow),
		   (assign, ":scene_to_use", "scn_random_scene_snow"  ),           (display_message,"@SCENE: snow"),
		   (party_relocate_near_party,"p_main_party", "p_pointer_z_0_snow"  ,":radius"),
        (else_try),
		   (eq, ":terrain_type", rt_desert),
		   (assign, ":scene_to_use", "scn_random_scene_desert"),           (display_message,"@SCENE: desert"),
		   (party_relocate_near_party,"p_main_party", "p_pointer_z_0_desert",":radius"),
        (try_end),
	# get number of combatants (calculated in script_calculate_battle_advantage) and use small scene if too few. GA
	    (try_begin), 
	       (lt,"$number_of_combatants",70),
	       (val_add,":scene_to_use",1),     # small scene variations right after standard ones in module_scenes
		   (display_message,"@small scene used"),
	    (try_end),
	  
	  (else_try),  # forest types randomly mashed for generation testing purposes, forests always small, for fps. GA
        (this_or_next|eq, ":terrain_type", rt_steppe_forest),
        (this_or_next|eq, ":terrain_type", rt_forest       ),
        (this_or_next|eq, ":terrain_type", rt_snow_forest  ),
        (             eq, ":terrain_type", rt_desert_forest),

#        (store_random_in_range, ":terrain", 0, 4),
        (try_begin),
		   (eq, ":terrain_type", rt_steppe_forest),
		   (assign, ":scene_to_use", "scn_random_scene_steppe_forest"),            (display_message,"@SCENE: steppe forest"),
		   (party_relocate_near_party,"p_main_party", "p_pointer_z_0_steppe_forest",":radius"),
        (else_try),
		   (eq, ":terrain_type", rt_forest),
		   (assign, ":scene_to_use", "scn_random_scene_plain_forest" ),            (display_message,"@SCENE: plain forest" ),
		   (party_relocate_near_party,"p_main_party", "p_pointer_z_0_plain_forest" ,":radius"),
        (else_try),
		   (eq, ":terrain_type", rt_snow_forest),
		   (assign, ":scene_to_use", "scn_random_scene_snow_forest"  ),            (display_message,"@SCENE: snow forest"  ),
		   (party_relocate_near_party,"p_main_party", "p_pointer_z_0_snow_forest"  ,":radius"),
        (else_try),
		   (eq, ":terrain_type", rt_desert_forest),
		   (assign, ":scene_to_use", "scn_random_scene_desert_forest"),            (display_message,"@SCENE: desert forest"),
		   (party_relocate_near_party,"p_main_party", "p_pointer_z_0_desert_forest",":radius"),
        (try_end),
      (try_end),
  (try_end),
  
      (jump_to_scene,":scene_to_use"),
  ]),

  # script_enter_dungeon
  # Input: arg1 = center_no, arg2 = mission_template_no
  # Output: none
  ("enter_dungeon",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":mission_template_no"),
      
      (set_jump_mission,":mission_template_no"),
      (party_get_slot, ":dungeon_scene", ":center_no", slot_town_prison),
      
      (modify_visitors_at_site,":dungeon_scene"),(reset_visitors),
      (assign, ":cur_pos", 16),
      (call_script, "script_get_heroes_attached_to_center_as_prisoner", ":center_no", "p_temp_party"),
      (party_get_num_companion_stacks, ":num_stacks","p_temp_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop","p_temp_party",":i_stack"),
        (lt, ":cur_pos", 32), # spawn up to entry point 32
        (set_visitor, ":cur_pos", ":stack_troop"),
        (val_add,":cur_pos", 1),
      (try_end),
      
      (set_jump_entry, 0),
      (jump_to_scene,":dungeon_scene"),
      (scene_set_slot, ":dungeon_scene", slot_scene_visited, 1),
      (change_screen_mission),
  ]),
  
  # script_enter_court
  # Input: arg1 = center_no
  # Output: none
  ("enter_court",
    [
      (store_script_param_1, ":center_no"),
      
      (assign, "$talk_context", tc_court_talk),
      
      (set_jump_mission,"mt_visit_town_castle"),
      (party_get_slot, ":castle_scene", ":center_no", slot_town_castle),
      (modify_visitors_at_site,":castle_scene"),
      (reset_visitors),
      #Adding guards
#      (store_faction_of_party, ":center_faction", ":center_no"),
#      (faction_get_slot, ":guard_troop", ":center_faction", slot_faction_guard_troop),
# center specific guards in TLD
      (party_get_slot, ":guard_troop", ":center_no", slot_town_castle_guard_troop),
##########
      (try_begin),
        (le, ":guard_troop", 0),
        (assign, ":guard_troop", "trp_guard_of_the_fountain_court"),
      (try_end),
      (set_visitor, 6, ":guard_troop"),
      (set_visitor, 7, ":guard_troop"),

      (assign, ":cur_pos", 16),
      (call_script, "script_get_heroes_attached_to_center", ":center_no", "p_temp_party"),
      (party_get_num_companion_stacks, ":num_stacks","p_temp_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop","p_temp_party",":i_stack"),
        (lt, ":cur_pos", 32), # spawn up to entry point 32
        (set_visitor, ":cur_pos", ":stack_troop"),
        (val_add,":cur_pos", 1),
      (try_end),
      (try_for_range, ":cur_troop", heroes_begin, heroes_end),
        (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_lady),
        (troop_slot_eq, ":cur_troop", slot_troop_cur_center, ":center_no"),
        (lt, ":cur_pos", 32), # spawn up to entry point 32
        (set_visitor, ":cur_pos", ":cur_troop"),
        (val_add,":cur_pos", 1),
      (try_end),
      #TLD NPC companions
      (val_max, ":cur_pos", 17), #if no one else in court, skip 16 (could be a throne)
      (try_for_range, ":cur_troop", companions_begin, companions_end),
        (troop_slot_eq, ":cur_troop", slot_troop_cur_center, ":center_no"),
        (neg|main_party_has_troop, ":cur_troop"), #not already hired
        (store_faction_of_party, ":center_faction", ":center_no"),
        (store_troop_faction, ":troop_faction", ":cur_troop"),
        (store_relation, ":rel", ":center_faction", ":troop_faction"),
        (ge, ":rel", 0), #only spawn if friendly center
        (lt, ":cur_pos", 32), # spawn up to entry point 32, can have multiple companions in a single town castle
        (set_visitor, ":cur_pos", ":cur_troop"),
        (val_add,":cur_pos", 1),
      (try_end),
      (jump_to_scene,":castle_scene"),
      (scene_set_slot, ":castle_scene", slot_scene_visited, 1),
      (change_screen_mission),
  ]),


  # script_find_high_ground_around_pos1
  # Input: pos1 should hold center_position_no
  #        arg1: team_no
  #        arg2: search_radius (in meters)
  # Output: pos52 contains highest ground within <search_radius> meters of team leader
  # Destroys position registers: pos10, pos11, pos15
  ("find_high_ground_around_pos1",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":search_radius", 2),
      (val_mul, ":search_radius", 100),
      (get_scene_boundaries, pos10,pos11),
      (team_get_leader, ":ai_leader", ":team_no"),
      (agent_get_position, pos1, ":ai_leader"),
      (set_fixed_point_multiplier, 100),
      (position_get_x, ":o_x", pos1),
      (position_get_y, ":o_y", pos1),
      (store_sub, ":min_x", ":o_x", ":search_radius"),
      (store_sub, ":min_y", ":o_y", ":search_radius"),
      (store_add, ":max_x", ":o_x", ":search_radius"),
      (store_add, ":max_y", ":o_y", ":search_radius"),
      (position_get_x, ":scene_min_x", pos10),
      (position_get_x, ":scene_max_x", pos11),
      (position_get_y, ":scene_min_y", pos10),
      (position_get_y, ":scene_max_y", pos11),
      (val_max, ":min_x", ":scene_min_x"),
      (val_max, ":min_y", ":scene_min_y"),
      (val_min, ":max_x", ":scene_max_x"),
      (val_min, ":max_y", ":scene_max_y"),
      
      (store_div, ":min_x_meters", ":min_x", 100),
      (store_div, ":min_y_meters", ":min_y", 100),
      (store_div, ":max_x_meters", ":max_x", 100),
      (store_div, ":max_y_meters", ":max_y", 100),
      
      (assign, ":highest_pos_z", -10000),
      (copy_position, pos52, pos1),
      (init_position, pos15),
      
      (try_for_range, ":i_x", ":min_x_meters", ":max_x_meters"),
        (store_mul, ":i_x_cm", ":i_x", 100),
        (try_for_range, ":i_y", ":min_y_meters", ":max_y_meters"),
          (store_mul, ":i_y_cm", ":i_y", 100),
          (position_set_x, pos15, ":i_x_cm"),
          (position_set_y, pos15, ":i_y_cm"),
          (position_set_z, pos15, 10000),
          (position_set_z_to_ground_level, pos15),
          (position_get_z, ":cur_pos_z", pos15),
          (try_begin),
            (gt, ":cur_pos_z", ":highest_pos_z"),
            (copy_position, pos52, pos15),
            (assign, ":highest_pos_z", ":cur_pos_z"),
          (try_end),
        (try_end),
      (try_end),
  ]),
  
  # script_select_battle_tactic
  # Input: none
  # Output: none
  ("select_battle_tactic",
    [
      (assign, "$ai_team_1_battle_tactic", 0),
      (get_player_agent_no, ":player_agent"),
      (agent_get_team, ":player_team", ":player_agent"),
      (try_begin),
        (num_active_teams_le, 2),
        (try_begin),
          (eq, ":player_team", 0),
          (assign, "$ai_team_1", 1),
        (else_try),
          (assign, "$ai_team_1", 0),
        (try_end),
        (assign, "$ai_team_2", -1),
      (else_try),
        (try_begin),
          (eq, ":player_team", 0),
          (assign, "$ai_team_1", 1),
        (else_try),
          (assign, "$ai_team_1", 0),
        (try_end),
        (store_add, "$ai_team_2", ":player_team", 2),
      (try_end),
      (call_script, "script_select_battle_tactic_aux", "$ai_team_1"),
      (assign, "$ai_team_1_battle_tactic", reg0),
      (try_begin),
        (ge, "$ai_team_2", 0),
        (call_script, "script_select_battle_tactic_aux", "$ai_team_2"),
        (assign, "$ai_team_2_battle_tactic", reg0),
      (try_end),
  ]),

  # script_select_battle_tactic_aux
  # Input: team_no
  # Output: battle_tactic
  ("select_battle_tactic_aux",
    [
      (store_script_param, ":team_no", 1),
      (assign, ":battle_tactic", 0),
      (assign, ":defense_not_an_option", 0),
      (get_player_agent_no, ":player_agent"),
      (agent_get_team, ":player_team", ":player_agent"),
      (try_begin),
        (eq, "$cant_leave_encounter", 1),
        (teams_are_enemies, ":team_no", ":player_team"),
        (assign, ":defense_not_an_option", 1),
      (try_end),
      (call_script, "script_team_get_class_percentages", ":team_no", 0),
      #      (assign, ":ai_perc_infantry", reg0),
      (assign, ":ai_perc_archers",  reg1),
      (assign, ":ai_perc_cavalry",  reg2),
      (call_script, "script_team_get_class_percentages", ":team_no", 1),#enemies of the ai_team
      #      (assign, ":enemy_perc_infantry", reg0),
      #      (assign, ":enemy_perc_archers",  reg1),
      #      (assign, ":enemy_perc_cavalry",  reg2),

      (store_random_in_range, ":rand", 0, 100),      
      (try_begin),
        (this_or_next|lt, ":rand", 20),
        (assign, ":continue", 0),
        (try_begin),
          (teams_are_enemies, ":team_no", ":player_team"),
          (party_slot_eq, "$g_enemy_party", slot_party_type, spt_kingdom_hero_party),
          (assign, ":continue", 1),
        (else_try),
          (neg|teams_are_enemies, ":team_no", ":player_team"),
          (gt, "$g_ally_party", 0),
          (party_slot_eq, "$g_ally_party", slot_party_type, spt_kingdom_hero_party),
          (assign, ":continue", 1),
        (try_end),
        (eq, ":continue", 1),
        (try_begin),
          (eq, ":defense_not_an_option", 0),
          (gt, ":ai_perc_archers", 50),
          (lt, ":ai_perc_cavalry", 35),
          (assign, ":battle_tactic", btactic_hold),
        (else_try),
          (lt, ":rand", 80),
          (assign, ":battle_tactic", btactic_follow_leader),
        (try_end),
      (try_end),
      (assign, reg0, ":battle_tactic"),
  ]),
  
  # script_battle_tactic_init
  # Input: none
  # Output: none
  ("battle_tactic_init",
    [
      (call_script, "script_battle_tactic_init_aux", "$ai_team_1", "$ai_team_1_battle_tactic"),
      (try_begin),
        (ge, "$ai_team_2", 0),
        (call_script, "script_battle_tactic_init_aux", "$ai_team_2", "$ai_team_2_battle_tactic"),
      (try_end),
  ]),

  # script_battle_tactic_init_aux
  # Input: team_no, battle_tactic
  # Output: none
  ("battle_tactic_init_aux",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":battle_tactic", 2),
      (team_get_leader, ":ai_leader", ":team_no"),
      (try_begin),
        (eq, ":battle_tactic", btactic_hold),
        (agent_get_position, pos1, ":ai_leader"),
        (call_script, "script_find_high_ground_around_pos1", ":team_no", 30),
        (copy_position, pos1, pos52),
        (call_script, "script_find_high_ground_around_pos1", ":team_no", 30), # call again just in case we are not at peak point.
        (copy_position, pos1, pos52),
        (call_script, "script_find_high_ground_around_pos1", ":team_no", 30), # call again just in case we are not at peak point.
        (team_give_order, ":team_no", grc_everyone, mordr_hold),
        (team_set_order_position, ":team_no", grc_everyone, pos52),
        (team_give_order, ":team_no", grc_archers, mordr_advance),
        (team_give_order, ":team_no", grc_archers, mordr_advance),
      (else_try),
        (eq, ":battle_tactic", btactic_follow_leader),
        (team_get_leader, ":ai_leader", ":team_no"),
        (agent_set_speed_limit, ":ai_leader", 8),
        (agent_get_position, pos60, ":ai_leader"),
        (team_give_order, ":team_no", grc_everyone, mordr_hold),
        (team_set_order_position, ":team_no", grc_everyone, pos60),
      (try_end),
  ]),
  
  # script_battle_tactic_apply
  # Input: none
  # Output: none
  ("battle_tactic_apply",
    [
      (call_script, "script_battle_tactic_apply_aux", "$ai_team_1", "$ai_team_1_battle_tactic"),
      (assign, "$ai_team_1_battle_tactic", reg0),
      (try_begin),
        (ge, "$ai_team_2", 0),
        (call_script, "script_battle_tactic_apply_aux", "$ai_team_2", "$ai_team_2_battle_tactic"),
        (assign, "$ai_team_2_battle_tactic", reg0),
      (try_end),
  ]),

  # script_battle_tactic_apply_aux
  # Input: team_no, battle_tactic
  # Output: battle_tactic
  ("battle_tactic_apply_aux",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":battle_tactic", 2),
      (store_mission_timer_a, ":mission_time"),
      (try_begin),
        (eq, ":battle_tactic", btactic_hold),
        (copy_position, pos1, pos52),
        (call_script, "script_get_closest3_distance_of_enemies_at_pos1", ":team_no", 1),
        (assign, ":avg_dist", reg0),
        (assign, ":min_dist", reg1),
        (try_begin),
          (this_or_next|lt, ":min_dist", 1000),
          (lt, ":avg_dist", 4000),
          (assign, ":battle_tactic", 0),
          (team_give_order, ":team_no", grc_everyone, mordr_charge),
        (try_end),
      (else_try),
        (eq, ":battle_tactic", btactic_follow_leader),
        (team_get_leader, ":ai_leader", ":team_no"),
        (agent_set_speed_limit, ":ai_leader", 9),
        (call_script, "script_team_get_average_position_of_enemies", ":team_no"),
        (copy_position, pos60, pos0),
        (agent_get_position, pos61, ":ai_leader"),
        (position_transform_position_to_local, pos62, pos61, pos60), #pos62 = vector to enemy w.r.t leader
        (position_normalize_origin, ":distance_to_enemy", pos62),
        (convert_from_fixed_point, ":distance_to_enemy"),
        (assign, reg17, ":distance_to_enemy"),
        (position_get_x, ":dir_x", pos62),
        (position_get_y, ":dir_y", pos62),
        (val_mul, ":dir_x", 23),
        (val_mul, ":dir_y", 23), #move 23 meters
        (position_set_x, pos62, ":dir_x"),
        (position_set_y, pos62, ":dir_y"),
      
        (position_transform_position_to_parent, pos63, pos61, pos62), #pos63 is 23m away from leader in the direction of the enemy.
        (position_set_z_to_ground_level, pos63),
      
        (team_give_order, ":team_no", grc_everyone, mordr_hold),
        (team_set_order_position, ":team_no", grc_everyone, pos63),
#        (team_give_order, ":team_no", grc_everyone, mordr_follow),
        (agent_get_position, pos1, ":ai_leader"),
#        (call_script, "script_get_closest3_distance_of_enemies_at_pos1", ":team_no"),
#        (assign, ":avg_dist", reg0),
#        (assign, ":min_dist", reg1),
        (try_begin),
          (lt, ":distance_to_enemy", 50),
          (ge, ":mission_time", 30),
          (assign, ":battle_tactic", 0),
          (team_give_order, ":team_no", grc_everyone, mordr_charge),
          (agent_set_speed_limit, ":ai_leader", 60),
        (try_end),
      (try_end),
      
      (try_begin), # charge everyone after a while
        (neq, ":battle_tactic", 0),
        (ge, ":mission_time", 300),
        (assign, ":battle_tactic", 0),
        (team_give_order, ":team_no", grc_everyone, mordr_charge),
        (team_get_leader, ":ai_leader", ":team_no"),
        (agent_set_speed_limit, ":ai_leader", 60),
      (try_end),
      (assign, reg0, ":battle_tactic"),
  ]),

##  # script_siege_defender_tactic_apply
##  # Input: none
##  # Output: none
##  ("siege_defender_tactic_apply",
##    [
##      (try_begin),
##        (eq, "$defender_team", 1),
##        (ge, "$belfry_positioned", 2),
##        
##        (assign, ":enemy_too_weak", 0),
##        (try_begin),
##          (ge, "$attacker_reinforcement_stage", 2),
##          (call_script, "script_calculate_team_strength", "$defender_team"),
##          (assign, ":defender_strength", reg0),
##          (call_script, "script_calculate_team_strength", "$attacker_team"),
##          (assign, ":attacker_strength", reg0),
##          (store_mul, ":attacker_strength_multiplied", ":attacker_strength", 2),
##          (ge, ":defender_strength", ":attacker_strength_multiplied"),
##          (assign, ":enemy_too_weak", 1),
##        (try_end),
##        
##        (try_begin),
##          (eq, ":enemy_too_weak", 1),
##          (neq, "$ai_battle_tactic", btactic_charge),
##          (assign, "$ai_battle_tactic", btactic_charge),
##          (team_give_order, "$defender_team", grc_infantry, mordr_charge),
##        (else_try),
##          (neq, "$ai_battle_tactic", btactic_charge),
##          (neq, "$ai_battle_tactic", btactic_hold),
##          (assign, "$ai_battle_tactic", btactic_hold),
##          (team_give_order, "$defender_team", grc_infantry, mordr_hold),
##          (team_give_order, "$defender_team", grc_heroes, mordr_hold),
##          (entry_point_get_position,pos1,10),
##          (team_set_order_position, "$defender_team", grc_infantry, pos1),
##          (team_set_order_position, "$defender_team", grc_heroes, pos1),
##        (try_end),
##      (try_end),
##  ]),
  
  
  # script_team_get_class_percentages
  # Input: arg1: team_no, arg2: try for team's enemies
  # Output: reg0: percentage infantry, reg1: percentage archers, reg2: percentage cavalry
  ("team_get_class_percentages",
    [
      (assign, ":num_infantry", 0),
      (assign, ":num_archers", 0),
      (assign, ":num_cavalry", 0),
      (assign, ":num_total", 0),
      (store_script_param, ":team_no", 1),
      (store_script_param, ":negate", 2),
      (try_for_agents,":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_get_team, ":agent_team", ":cur_agent"),
        (assign, ":continue", 0),
        (try_begin),
          (eq, ":negate", 1),
          (teams_are_enemies, ":agent_team", ":team_no"),
          (assign, ":continue", 1),
        (else_try),
          (eq, ":agent_team", ":team_no"),
          (assign, ":continue", 1),
        (try_end),
        (eq, ":continue", 1),
        (val_add, ":num_total", 1),
        (agent_get_class, ":agent_class", ":cur_agent"),
        (try_begin),
          (eq, ":agent_class", grc_infantry),
          (val_add,  ":num_infantry", 1),
        (else_try),
          (eq, ":agent_class", grc_archers),
          (val_add,  ":num_archers", 1),
        (else_try),
          (eq, ":agent_class", grc_cavalry),
          (val_add,  ":num_cavalry", 1),
        (try_end),
      (try_end),
      (try_begin),
        (eq,  ":num_total", 0),
        (assign,  ":num_total", 1),
      (try_end),
      (store_mul, ":perc_infantry",":num_infantry",100),
      (val_div, ":perc_infantry",":num_total"),
      (store_mul, ":perc_archers",":num_archers",100),
      (val_div, ":perc_archers",":num_total"),
      (store_mul, ":perc_cavalry",":num_cavalry",100),
      (val_div, ":perc_cavalry",":num_total"),
      (assign, reg0, ":perc_infantry"),
      (assign, reg1, ":perc_archers"),
      (assign, reg2, ":perc_cavalry"),
  ]),
  
  # script_get_closest3_distance_of_enemies_at_pos1
  # Input: arg1: team_no, pos1
  # Output: reg0: distance in cms.
  ("get_closest3_distance_of_enemies_at_pos1",
    [
      (assign, ":min_distance_1", 100000),
      (assign, ":min_distance_2", 100000),
      (assign, ":min_distance_3", 100000),
      
      (store_script_param, ":team_no", 1),
      (try_for_agents,":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_get_team, ":agent_team", ":cur_agent"),
        (teams_are_enemies, ":agent_team", ":team_no"),
       
        (agent_get_position, pos2, ":cur_agent"),
        (get_distance_between_positions,":cur_dist",pos2,pos1),
        (try_begin),
          (lt, ":cur_dist", ":min_distance_1"),
          (assign, ":min_distance_3", ":min_distance_2"),
          (assign, ":min_distance_2", ":min_distance_1"),
          (assign, ":min_distance_1", ":cur_dist"),
        (else_try),
          (lt, ":cur_dist", ":min_distance_2"),
          (assign, ":min_distance_3", ":min_distance_2"),
          (assign, ":min_distance_2", ":cur_dist"),
        (else_try),
          (lt, ":cur_dist", ":min_distance_3"),
          (assign, ":min_distance_3", ":cur_dist"),
        (try_end),
      (try_end),
      
      (assign, ":total_distance", 0),
      (assign, ":total_count", 0),
      (try_begin),
        (lt, ":min_distance_1", 100000),
        (val_add, ":total_distance", ":min_distance_1"),
        (val_add, ":total_count", 1),
      (try_end),
      (try_begin),
        (lt, ":min_distance_2", 100000),
        (val_add, ":total_distance", ":min_distance_2"),
        (val_add, ":total_count", 1),
      (try_end),
      (try_begin),
        (lt, ":min_distance_3", 100000),
        (val_add, ":total_distance", ":min_distance_3"),
        (val_add, ":total_count", 1),
      (try_end),
      (assign, ":average_distance", 100000),
      (try_begin),
        (gt, ":total_count", 0),
        (store_div, ":average_distance", ":total_distance", ":total_count"),
      (try_end),
      (assign, reg0, ":average_distance"),
      (assign, reg1, ":min_distance_1"),
      (assign, reg2, ":min_distance_2"),
      (assign, reg3, ":min_distance_3"),
  ]),

  # script_team_get_average_position_of_enemies
  # Input: arg1: team_no, 
  # Output: pos0: average position.
  ("team_get_average_position_of_enemies",
    [
      (store_script_param_1, ":team_no"),
      (init_position, pos0),
      (assign, ":num_enemies", 0),
      (assign, ":accum_x", 0),
      (assign, ":accum_y", 0),
      (assign, ":accum_z", 0),
      (try_for_agents,":enemy_agent"),
        (agent_is_alive, ":enemy_agent"),
        (agent_is_human, ":enemy_agent"),
        (agent_get_team, ":enemy_team", ":enemy_agent"),
        (teams_are_enemies, ":team_no", ":enemy_team"),
      
        (agent_get_position, pos62, ":enemy_agent"),
      
        (position_get_x, ":x", pos62),
        (position_get_y, ":y", pos62),
        (position_get_z, ":z", pos62),
      
        (val_add, ":accum_x", ":x"),
        (val_add, ":accum_y", ":y"),
        (val_add, ":accum_z", ":z"),
        (val_add, ":num_enemies", 1),
      (try_end),
      (store_div, ":average_x", ":accum_x", ":num_enemies"),
      (store_div, ":average_y", ":accum_y", ":num_enemies"),
      (store_div, ":average_z", ":accum_z", ":num_enemies"),

      (position_set_x, pos0, ":average_x"),
      (position_set_y, pos0, ":average_y"),
      (position_set_z, pos0, ":average_z"),
      (assign, reg0, ":num_enemies"),
  ]),
  
  # script_search_troop_prisoner_of_party
  # Input: arg1 = troop_no
  # Output: reg0 = party_no (-1 if troop is not a prisoner.)
  ("search_troop_prisoner_of_party",
    [
      (store_script_param_1, ":troop_no"),
      (assign, ":prisoner_of", -1),
      (try_for_parties, ":party_no"),
        (eq,  ":prisoner_of", -1),
        (this_or_next|eq, ":party_no", "p_main_party"),
        (ge, ":party_no", centers_begin),
        (party_count_prisoners_of_type, ":troop_found", ":party_no", ":troop_no"),
        (gt, ":troop_found", 0),
        (assign, ":prisoner_of", ":party_no"),
      (try_end),
      (assign, reg0, ":prisoner_of"),
  ]),
  
  
##  # script_clear_last_quest
##  # Input: arg1 = troop_no
##  ("clear_last_quest",
##    [
##      (store_script_param_1, ":troop_no"),
##      
##      (troop_set_slot, ":troop_no",slot_troop_last_quest, 0),
##      (troop_set_slot, ":troop_no",slot_troop_last_quest_betrayed, 0)
##  ]),
  
  # script_change_debt_to_troop
  # Input: arg1 = troop_no, arg2 = new debt amount
  # Output: none
  ("change_debt_to_troop",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":new_debt"),
      
      (troop_get_slot, ":cur_debt", ":troop_no", slot_troop_player_debt),
      (assign, reg1, ":cur_debt"),
      (val_add, ":cur_debt", ":new_debt"),
      (assign, reg2, ":cur_debt"),
      (troop_set_slot, ":troop_no", slot_troop_player_debt, ":cur_debt"),
      (str_store_troop_name_link, s1, ":troop_no"),
      (display_message, "@You now owe {reg2} denars to {s1}."),
  ]),
  
  # script_abort_quest
  # Input: arg1 = quest_no, arg2 = apply relation penalty
  # Output: none
  ("abort_quest",
    [
      (store_script_param_1, ":quest_no"),
      (store_script_param_2, ":abort_type"), #0=aborted by event, 1=abort by talking 2=abort by expire

      (assign, ":quest_return_penalty", -1),
      (assign, ":quest_expire_penalty", -2),
      
#      (quest_get_slot, ":quest_object_troop", ":quest_no", slot_quest_object_troop),
      (try_begin),
        (this_or_next|eq, ":quest_no", "qst_deliver_message"),
        (eq, ":quest_no", "qst_deliver_message_to_enemy_lord"),
        (assign, ":quest_return_penalty", -2),
        (assign, ":quest_expire_penalty", -3),
      (else_try),
        (eq, ":quest_no", "qst_escort_lady"),
        (quest_get_slot, ":quest_object_troop", "qst_escort_lady", slot_quest_object_troop),
        (party_remove_members, "p_main_party", ":quest_object_troop", 1),
        (assign, ":quest_return_penalty", -2),
        (assign, ":quest_expire_penalty", -3),
##      (else_try),
##        (eq, ":quest_no", "qst_rescue_lady_under_siege"),
##        (party_remove_members, "p_main_party", ":quest_object_troop", 1),
##      (else_try),
##        (eq, ":quest_no", "qst_deliver_message_to_lover"),
##      (else_try),
##        (eq, ":quest_no", "qst_bring_prisoners_to_enemy"),
##        (try_begin),
##          (check_quest_succeeded, ":quest_no"),
##          (quest_get_slot, ":quest_target_amount", ":quest_no", slot_quest_target_amount),
##          (quest_get_slot, ":quest_object_troop", ":quest_no", slot_quest_object_troop),
##          (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
##          (call_script, "script_game_get_join_cost", ":quest_object_troop"),
##          (assign, ":reward", reg0),
##          (val_mul, ":reward", ":quest_target_amount"),
##          (val_div, ":reward", 2),
##        (else_try),
##          (quest_get_slot, ":reward", ":quest_no", slot_quest_target_amount),
##        (try_end),
##        (call_script, "script_change_debt_to_troop", ":quest_giver_troop", ":reward"),
##      (else_try),
##        (eq, ":quest_no", "qst_bring_reinforcements_to_siege"),
##        (quest_get_slot, ":quest_target_amount", ":quest_no", slot_quest_target_amount),
##        (quest_get_slot, ":quest_object_troop", ":quest_no", slot_quest_object_troop),
##        (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
##        (call_script, "script_game_get_join_cost", ":quest_object_troop"),
##        (assign, ":reward", reg0),
##        (val_mul, ":reward", ":quest_target_amount"),
##        (val_mul, ":reward", 2),
##        (call_script, "script_change_debt_to_troop", ":quest_giver_troop", ":reward"),
##      (else_try),
##        (eq, ":quest_no", "qst_deliver_supply_to_center_under_siege"),
##        (quest_get_slot, ":quest_target_amount", ":quest_no", slot_quest_target_amount),
##        (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
##        (store_item_value, ":reward", "itm_siege_supply"),
##        (val_mul, ":reward", ":quest_target_amount"),
##        (call_script, "script_change_debt_to_troop", ":quest_giver_troop", ":reward"),
      (else_try),
        (eq, ":quest_no", "qst_raise_troops"),
        (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
        (call_script, "script_change_debt_to_troop", ":quest_giver_troop", 100),
        (assign, ":quest_return_penalty", -4),
        (assign, ":quest_expire_penalty", -5),
      (else_try),
        (eq, ":quest_no", "qst_deal_with_looters"),
        (try_for_parties, ":cur_party_no"),
          (party_get_template_id, ":cur_party_template", ":cur_party_no"),
          (eq, ":cur_party_template", "pt_looters"),
          (party_set_flags, ":cur_party_no", pf_quest_party, 0),
        (try_end),
        (assign, ":quest_return_penalty", -4),
        (assign, ":quest_expire_penalty", -5),
      (else_try),
        (eq, ":quest_no", "qst_deal_with_bandits_at_lords_village"),
        (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
        (call_script, "script_change_debt_to_troop", ":quest_giver_troop", 200),
        (assign, ":quest_return_penalty", -5),
        (assign, ":quest_expire_penalty", -6),
      (else_try),
        (eq, ":quest_no", "qst_collect_taxes"),
        (quest_get_slot, ":gold_reward", ":quest_no", slot_quest_gold_reward),
        (quest_set_slot, ":quest_no", slot_quest_gold_reward, 0),
        (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
        (call_script, "script_change_debt_to_troop", ":quest_giver_troop", ":gold_reward"),
        (assign, ":quest_return_penalty", -4),
        (assign, ":quest_expire_penalty", -6),
##      (else_try),
##        (eq, ":quest_no", "qst_capture_messenger"),
##      (else_try),
##        (eq, ":quest_no", "qst_bring_back_deserters"),
      (else_try),
        (eq, ":quest_no", "qst_hunt_down_fugitive"),
        (assign, ":quest_return_penalty", -3),
        (assign, ":quest_expire_penalty", -4),
      (else_try),
        (eq, ":quest_no", "qst_kill_local_merchant"),
      (else_try),
        (eq, ":quest_no", "qst_bring_back_runaway_serfs"),
        (assign, ":quest_return_penalty", -1),
        (assign, ":quest_expire_penalty", -1),
      (else_try),
        (eq, ":quest_no", "qst_lend_companion"),
      (else_try),
        (eq, ":quest_no", "qst_collect_debt"),
        (try_begin),
          (quest_slot_eq, "qst_collect_debt", slot_quest_current_state, 1), #debt collected but not delivered
          (quest_get_slot, ":debt", "qst_collect_debt", slot_quest_target_amount),
          (quest_get_slot, ":quest_giver", "qst_collect_debt", slot_quest_giver_troop),
          (call_script, "script_change_debt_to_troop", ":quest_giver", ":debt"),
          (assign, ":quest_return_penalty", -3),
          (assign, ":quest_expire_penalty", -6),
        (else_try),
          (assign, ":quest_return_penalty", -3),
          (assign, ":quest_expire_penalty", -4),
        (try_end),
      (else_try),
        (eq, ":quest_no", "qst_deal_with_bandits_at_lords_village"),
        (assign, ":quest_return_penalty", -6),
        (assign, ":quest_expire_penalty", -6),
      (else_try),
        (eq, ":quest_no", "qst_raid_caravan_to_start_war"),
        (assign, ":quest_return_penalty", -10),
        (assign, ":quest_expire_penalty", -13),
      (else_try),
        (eq, ":quest_no", "qst_persuade_lords_to_make_peace"),
        (assign, ":quest_return_penalty", -10),
        (assign, ":quest_expire_penalty", -13),
      (else_try),
        (eq, ":quest_no", "qst_deal_with_night_bandits"),
        (assign, ":quest_return_penalty", -1),
        (assign, ":quest_expire_penalty", -1),
      
      (else_try),
        (eq, ":quest_no", "qst_follow_spy"),
        (assign, ":quest_return_penalty", -2),
        (assign, ":quest_expire_penalty", -3),
        (try_begin),
          (party_is_active, "$qst_follow_spy_spy_party"),
          (remove_party, "$qst_follow_spy_spy_party"),
        (try_end),
        (try_begin),
          (party_is_active, "$qst_follow_spy_spy_partners_party"),
          (remove_party, "$qst_follow_spy_spy_partners_party"),
        (try_end),
      (else_try),
        (eq, ":quest_no", "qst_capture_enemy_hero"),
        (assign, ":quest_return_penalty", -3),
        (assign, ":quest_expire_penalty", -4),
##      (else_try),
##        (eq, ":quest_no", "qst_lend_companion"),
##        (quest_get_slot, ":quest_target_troop", "qst_lend_companion", slot_quest_target_troop),
##        (party_add_members, "p_main_party", ":quest_target_troop", 1),
##      (else_try),
##        (eq, ":quest_no", "qst_capture_conspirators"),
##      (else_try),
##        (eq, ":quest_no", "qst_defend_nobles_against_peasants"),
      (else_try),
        (eq, ":quest_no", "qst_incriminate_loyal_commander"),
        (assign, ":quest_return_penalty", -5),
        (assign, ":quest_expire_penalty", -6),
##      (else_try),
##        (eq, ":quest_no", "qst_hunt_down_raiders"),
##      (else_try),
##        (eq, ":quest_no", "qst_capture_prisoners"),
##        #Enemy lord quests
      (else_try),
        (eq, ":quest_no", "qst_lend_surgeon"),

        #Kingdom lady quests
      (else_try),
        (eq, ":quest_no", "qst_rescue_lord_by_replace"),
        (assign, ":quest_return_penalty", -1),
        (assign, ":quest_expire_penalty", -1),
      (else_try),
        (eq, ":quest_no", "qst_deliver_message_to_prisoner_lord"),
        (assign, ":quest_return_penalty", 0),
        (assign, ":quest_expire_penalty", -1),
      (else_try),
        (eq, ":quest_no", "qst_duel_for_lady"),
        (assign, ":quest_return_penalty", -1),
        (assign, ":quest_expire_penalty", -1),
      
      #Kingdom Army quests
      (else_try),
        (eq, ":quest_no", "qst_follow_army"),
        (assign, ":quest_return_penalty", -4),
        (assign, ":quest_expire_penalty", -5),
      (else_try),
        (eq, ":quest_no", "qst_deliver_cattle_to_army"),
        (assign, ":quest_return_penalty", -1),
        (assign, ":quest_expire_penalty", -2),
      (else_try),
        (eq, ":quest_no", "qst_join_siege_with_army"),
        (assign, ":quest_return_penalty", -1),
        (assign, ":quest_expire_penalty", -2),
      (else_try),
        (eq, ":quest_no", "qst_scout_waypoints"),
        (assign, ":quest_return_penalty", -1),
        (assign, ":quest_expire_penalty", -2),
      
      #Village Elder quests
      (else_try),
        (eq, ":quest_no", "qst_deliver_grain"),
        (assign, ":quest_return_penalty", -6),
        (assign, ":quest_expire_penalty", -7),
      (else_try),
        (eq, ":quest_no", "qst_deliver_cattle"),
        (assign, ":quest_return_penalty", -3),
        (assign, ":quest_expire_penalty", -4),
      (else_try),
        (eq, ":quest_no", "qst_train_peasants_against_bandits"),
        (assign, ":quest_return_penalty", -4),
        (assign, ":quest_expire_penalty", -5),

      #Mayor quests
      (else_try),
        (eq, ":quest_no", "qst_deliver_wine"),
        (assign, ":quest_return_penalty", -1),
        (assign, ":quest_expire_penalty", -3),
        (val_add, "$debt_to_merchants_guild", "$qst_deliver_wine_debt"),
      (else_try),
        (eq, ":quest_no", "qst_move_cattle_herd"),
        (assign, ":quest_return_penalty", -1),
        (assign, ":quest_expire_penalty", -3),
      (else_try),
        (eq, ":quest_no", "qst_escort_merchant_caravan"),
        (assign, ":quest_return_penalty", -1),
        (assign, ":quest_expire_penalty", -3),
      (else_try),
        (eq, ":quest_no", "qst_troublesome_bandits"),
        (assign, ":quest_return_penalty", -1),
        (assign, ":quest_expire_penalty", -2),
      #Other quests
      (else_try),
        (eq, ":quest_no", "qst_join_faction"),
        (assign, ":quest_return_penalty", -3),
        (assign, ":quest_expire_penalty", -3),
        (try_begin),
          (call_script, "script_get_number_of_hero_centers", "trp_player"),
          (gt, reg0, 0),
          (call_script, "script_change_player_relation_with_faction", "$g_invite_faction", -10),
        (try_end),
        (assign, "$g_invite_faction", 0),
        (assign, "$g_invite_faction_lord", 0),
        (assign, "$g_invite_offered_center", 0),
      (else_try),
        (eq, ":quest_no", "qst_eliminate_bandits_infesting_village"),
        (assign, ":quest_return_penalty", -3),
        (assign, ":quest_expire_penalty", -3),
      (try_end),
      (try_begin),
        (gt, ":abort_type", 0),
        (quest_get_slot, ":quest_giver", ":quest_no", slot_quest_giver_troop),
        (assign, ":relation_penalty", ":quest_return_penalty"),
        (try_begin),
          (eq, ":abort_type", 2),
          (assign, ":relation_penalty", ":quest_expire_penalty"),
        (try_end),
        (try_begin),
          (this_or_next|is_between, ":quest_giver", village_elders_begin, village_elders_end),
          (is_between, ":quest_giver", mayors_begin, mayors_end),
          (quest_get_slot, ":quest_giver_center", ":quest_no", slot_quest_giver_center),
          (call_script, "script_change_player_relation_with_center", ":quest_giver_center", ":relation_penalty"),
        (else_try),
          (call_script, "script_change_player_relation_with_troop", ":quest_giver", ":relation_penalty"),
        (try_end),
      (try_end),
      (fail_quest, ":quest_no"),
#NPC companion changes begin
      (try_begin),
        (gt, ":abort_type", 0),
        (call_script, "script_objectionable_action", tmt_honest, "str_fail_quest"),
      (try_end),
#NPC companion changes end
      (call_script, "script_end_quest", ":quest_no"),
  ]),
  
  
##  # script_event_center_captured
##  # Input: arg1 = center_no, arg2 = old_faction_no
##  # Output: none
##  ("event_center_captured",
##    [
##      #      (store_script_param_1, ":center_no"),
##      #       (store_script_param_2, ":old_faction_no"),
##      #       (store_faction_of_party, ":faction_no"),
##      
##      (try_begin),
##        (check_quest_active, "qst_deliver_message"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_escort_lady"),
##        (quest_slot_eq, "qst_escort_lady", slot_quest_target_center, ":center_no"),
##        (call_script, "script_abort_quest", "qst_escort_lady"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_rescue_lady_under_siege"),
##        (quest_slot_eq, "qst_rescue_lady_under_siege", slot_quest_target_center, ":center_no"),
##        (quest_slot_eq, "qst_rescue_lady_under_siege", slot_quest_current_state, 0),
##        (call_script, "script_abort_quest", "qst_rescue_lady_under_siege", 1),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_deliver_message_to_lover"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_deliver_message_to_enemy_lord"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_bring_prisoners_to_enemy"),
##        (quest_slot_eq, "qst_bring_prisoners_to_enemy", slot_quest_target_center, ":center_no"),
##        (neg|check_quest_succeeded, "qst_bring_prisoners_to_enemy"),
##        (call_script, "script_abort_quest", "qst_bring_prisoners_to_enemy"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_bring_reinforcements_to_siege"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_deliver_supply_to_center_under_siege"),
##        (quest_slot_eq, "qst_deliver_supply_to_center_under_siege", slot_quest_target_center, ":center_no"),
##        (call_script, "script_abort_quest", "qst_deliver_supply_to_center_under_siege", 1),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_raise_troops"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_capture_messenger"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_bring_back_deserters"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_kill_local_merchant"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_bring_back_runaway_serfs"),
##        (quest_slot_eq, "qst_bring_back_runaway_serfs", slot_quest_object_center, ":center_no"),
##        (neg|check_quest_succeeded, "qst_bring_back_runaway_serfs"),
##        (neg|check_quest_failed, "qst_bring_back_runaway_serfs"),
##        (call_script, "script_abort_quest", "qst_bring_back_runaway_serfs"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_follow_spy"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_capture_enemy_hero"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_lend_companion"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_capture_conspirators"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_defend_nobles_against_peasants"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_incriminate_loyal_commander"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_hunt_down_raiders"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_capture_prisoners"),
##      (try_end),
##      #Enemy lord quests
##      (try_begin),
##        (check_quest_active, "qst_lend_surgeon"),
##      (try_end),
##      #Kingdom lady quests
##      (try_begin),
##        (check_quest_active, "qst_rescue_lord_by_replace"),
##        (quest_get_slot, ":quest_target_troop", "qst_rescue_lord_by_replace", slot_quest_target_troop),
##        (troop_slot_eq, ":quest_target_troop", slot_troop_is_prisoner, 0),
##        (neg|check_quest_succeeded, "qst_rescue_lord_by_replace"),
##        (call_script, "script_abort_quest", "qst_rescue_lord_by_replace"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_deliver_message_to_prisoner_lord"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_duel_for_lady"),
##      (try_end),
##  ]),

  # script_cf_is_quest_troop
  # Input: arg1 = troop_no
  # Output: none (can fail)
  ("cf_is_quest_troop",
    [
      (store_script_param_1, ":troop_no"),
      (assign, ":is_quest_troop", 0),
      (try_for_range, ":cur_quest", all_quests_begin, all_quests_end),
        (check_quest_active, ":cur_quest"),
        (quest_get_slot, ":quest_troop_1", ":cur_quest", slot_quest_target_troop),
        (quest_get_slot, ":quest_troop_2", ":cur_quest", slot_quest_object_troop),
        (quest_get_slot, ":quest_troop_3", ":cur_quest", slot_quest_giver_troop),
        (this_or_next|eq, ":quest_troop_1", ":troop_no"),
        (this_or_next|eq, ":quest_troop_2", ":troop_no"),
        (eq, ":quest_troop_3", ":troop_no"),
        (assign, ":is_quest_troop", 1),
      (try_end),
      (eq, ":is_quest_troop", 1),
  ]),

##  # script_calculate_team_strength
##  # Input: arg1 = team_no
##  # Output: strength
##  ("calculate_team_strength",
##    [
##      (store_script_param_1, ":team_no"),
##      (assign, ":total_strength", 0),
##      (try_for_agents, ":cur_agent"),
##        (agent_get_team, ":agent_team", ":cur_agent"),
##        (eq, ":team_no", ":agent_team"),
##        (agent_is_human, ":cur_agent"),
##        (agent_is_alive, ":cur_agent"),
##        
##        (agent_get_troop_id, ":cur_troop", ":cur_agent"),
##        (store_character_level, ":cur_level", ":cur_troop"),
##        (val_add, ":cur_level", 5),
##        (try_begin),
##          (troop_is_hero, ":cur_troop"),
##          (val_add, ":cur_level", 5),
##        (try_end),
##        (val_add, ":total_strength", ":cur_level"),
##      (try_end),
##      (assign, reg0, ":total_strength"),
##  ]),

  # script_check_friendly_kills
  # Input: none
  # Output: none (changes the morale of the player's party)
  ("check_friendly_kills",
    [(get_player_agent_own_troop_kill_count, ":count"),
     (try_begin),
       (neq, "$g_player_current_own_troop_kills", ":count"),
       (val_sub, ":count", "$g_player_current_own_troop_kills"),
       (val_add, "$g_player_current_own_troop_kills", ":count"),
       (val_mul, ":count", -1),
       (call_script, "script_change_player_party_morale", ":count"),
     (try_end),
   ]),

  # script_simulate_retreat
  # Input: arg1 = players_side_damage, arg2 = enemy_side_damage, s5 = title_string
  # Output: none
  ("simulate_retreat",
    [
      (call_script, "script_music_set_situation_with_culture", mtf_sit_killed),
      (set_show_messages, 0),
      (store_script_param, ":players_side_damage", 1),
      (store_script_param, ":enemy_side_damage", 2),

      (assign, ":players_side_strength", 0),
      (assign, ":enemy_side_strength", 0),
      
      (assign, ":do_calculate", 1),
      (try_begin),
        (try_for_agents, ":cur_agent"),
          (agent_is_human, ":cur_agent"),
          (agent_is_alive, ":cur_agent"),
          (agent_set_slot, ":cur_agent", slot_agent_is_alive_before_retreat, 1),#needed for simulation

          (agent_get_troop_id, ":cur_troop", ":cur_agent"),
          (store_character_level, ":cur_level", ":cur_troop"),
          (val_add, ":cur_level", 5),
          (try_begin),
            (troop_is_hero, ":cur_troop"),
            (val_add, ":cur_level", 5),
          (try_end),
          (try_begin),
            (agent_is_ally, ":cur_agent"),
            (val_add, ":players_side_strength", ":cur_level"),
          (else_try),
            (val_add, ":enemy_side_strength", ":cur_level"),
          (try_end),
        (try_end),
        (eq, "$pin_player_fallen", 0),
        (lt, ":enemy_side_strength", ":players_side_strength"),
        (assign, ":do_calculate", 0),
      (try_end),
      
      (try_begin),
        (eq, ":do_calculate", 1),
        
        (assign, "$g_last_mission_player_damage", 0),
        (party_clear, "p_temp_party"),
        (party_clear, "p_temp_party_2"),
        (call_script, "script_simulate_battle_with_agents_aux", 0, ":players_side_damage"),
        (call_script, "script_simulate_battle_with_agents_aux", 1, ":enemy_side_damage"),
        
        (assign, ":display_casualties", 0),
        
        (try_begin),
          (gt, "$g_last_mission_player_damage", 0),
          (assign, ":display_casualties", 1),
          (assign, reg1, "$g_last_mission_player_damage"),
          (str_store_string, s12, "str_casualty_display_hp"),
        (else_try),
          (str_clear, s12),
        (try_end),
        
        (call_script, "script_print_casualties_to_s0", "p_temp_party", 1),
        (try_begin),
          (party_get_num_companion_stacks, ":num_stacks", "p_temp_party"),
          (gt, ":num_stacks", 0),
          (assign, ":display_casualties", 1),
        (try_end),
        (str_store_string_reg, s10, s0),
        
        (call_script, "script_print_casualties_to_s0", "p_temp_party_2", 1),
        (try_begin),
          (party_get_num_companion_stacks, ":num_stacks", "p_temp_party_2"),
          (gt, ":num_stacks", 0),
          (assign, ":display_casualties", 1),
        (try_end),
        (str_store_string_reg, s11, s0),
        (try_begin),
          (eq, ":display_casualties", 1),
          (dialog_box,"str_casualty_display", s5),
        (try_end),
      (try_end),
      (set_show_messages, 1),

      #Calculating morale penalty (can be between 0-30)
      (assign, ":ally_casualties", 0),
      (assign, ":enemy_casualties", 0),
      (assign, ":total_allies", 0),
      
      (try_for_agents, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (try_begin),
          (agent_is_ally, ":cur_agent"),
          (val_add, ":total_allies", 1),
          (try_begin),
            (neg|agent_is_alive, ":cur_agent"),
            (val_add, ":ally_casualties", 1),
          (try_end),
        (else_try),
          (neg|agent_is_alive, ":cur_agent"),
          (val_add, ":enemy_casualties", 1),
        (try_end),
      (try_end),
      (store_add, ":total_casualties", ":ally_casualties", ":enemy_casualties"),
      (try_begin),
        (gt, ":total_casualties", 0),
        (store_mul, ":morale_adder", ":ally_casualties", 100),
        (val_div, ":morale_adder", ":total_casualties"),
        (val_mul, ":morale_adder", ":ally_casualties"),
        (val_div, ":morale_adder", ":total_allies"),
        (val_mul, ":morale_adder", -30),
        (val_div, ":morale_adder", 100),
        (call_script, "script_change_player_party_morale", ":morale_adder"),
      (try_end),
  ]),

  
  
  # script_simulate_battle_with_agents_aux
  # For internal use only
  # Input: arg1 = attacker_side (0 = ally, 1 = enemy), arg2 = damage amount
  # Output: none
  ("simulate_battle_with_agents_aux",
    [
      (store_script_param_1, ":attacker_side"),
      (store_script_param_2, ":damage"),
      
      (get_player_agent_no, ":player_agent"),
      (try_for_agents, ":cur_agent"),
        (neq, ":player_agent", ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        #do not check agent_is_alive, check slot_agent_is_alive_before_retreat instead, so that dead agents can still hit enemies
        (agent_slot_eq, ":cur_agent", slot_agent_is_alive_before_retreat, 1),
        (try_begin),
          (agent_is_ally, ":cur_agent"),
          (assign, ":cur_agents_side", 0),
        (else_try),
          (assign, ":cur_agents_side", 1),
        (try_end),
        (eq, ":cur_agents_side", ":attacker_side"),
        (agent_get_position, pos2, ":cur_agent"),
        (assign, ":closest_agent", -1),
        (assign, ":min_distance", 100000),
        (try_for_agents, ":cur_agent_2"),
          (agent_is_human, ":cur_agent_2"),
          (agent_is_alive, ":cur_agent_2"),
          (try_begin),
            (agent_is_ally, ":cur_agent_2"),
            (assign, ":cur_agents_side_2", 0),
          (else_try),
            (assign, ":cur_agents_side_2", 1),
          (try_end),
          (this_or_next|neq, ":cur_agent_2", ":player_agent"),
          (eq, "$pin_player_fallen", 0),
          (neq, ":attacker_side", ":cur_agents_side_2"),
          (agent_get_position, pos3, ":cur_agent_2"),
          (get_distance_between_positions, ":cur_distance", pos2, pos3),
          (lt, ":cur_distance", ":min_distance"),
          (assign, ":min_distance", ":cur_distance"),
          (assign, ":closest_agent", ":cur_agent_2"),
        (try_end),
        (ge, ":closest_agent", 0),
        #Fight
        (agent_get_class, ":agent_class", ":cur_agent"),
        (assign, ":agents_speed", 1),
        (assign, ":agents_additional_hit", 0),
        (try_begin),
          (eq, ":agent_class", grc_archers),
          (assign, ":agents_additional_hit", 2),
        (else_try),
          (eq, ":agent_class", grc_cavalry),
          (assign, ":agents_speed", 2),
        (try_end),
        (agent_get_class, ":agent_class", ":closest_agent"),
        (assign, ":agents_speed_2", 1),
        (try_begin),
          (eq, ":agent_class", grc_cavalry),
          (assign, ":agents_speed_2", 2),
        (try_end),
        (assign, ":agents_hit", 18000),
        (val_add, ":min_distance", 3000),
        (val_div, ":agents_hit", ":min_distance"),
        (val_mul, ":agents_hit", 2),# max 10, min 2 hits within 150 meters
        
        (val_mul, ":agents_hit", ":agents_speed"),
        (val_div, ":agents_hit", ":agents_speed_2"),
        (val_add, ":agents_hit", ":agents_additional_hit"),
        
        (assign, ":cur_damage", ":damage"),
        (agent_get_troop_id, ":closest_troop", ":closest_agent"),
        (agent_get_troop_id, ":cur_troop", ":cur_agent"),
        (store_character_level, ":closest_level", ":closest_troop"),
        (store_character_level, ":cur_level", ":cur_troop"),
        (store_sub, ":level_dif", ":cur_level", ":closest_level"),
        (val_div, ":level_dif", 5),
        (val_add, ":cur_damage", ":level_dif"),
        
        (try_begin),
          (eq, ":closest_agent", ":player_agent"),
          (val_div, ":cur_damage", 2),
          (store_agent_hit_points, ":init_player_hit_points", ":player_agent", 1),
        (try_end),
        
        (try_for_range, ":unused", 0, ":agents_hit"),
          (store_random_in_range, ":random_damage", 0, 100),
          (lt, ":random_damage", ":cur_damage"),
          (agent_deliver_damage_to_agent, ":cur_agent", ":closest_agent"),
        (try_end),
        
        (try_begin),
          (eq, ":closest_agent", ":player_agent"),
          (store_agent_hit_points, ":final_player_hit_points", ":player_agent", 1),
          (store_sub, ":hit_points_difference", ":init_player_hit_points", ":final_player_hit_points"),
          (val_add, "$g_last_mission_player_damage", ":hit_points_difference"),
        (try_end),
        
        (neg|agent_is_alive, ":closest_agent"),
        (try_begin),
          (eq, ":attacker_side", 1),
          (party_add_members, "p_temp_party", ":closest_troop", 1),
          (try_begin),
            (agent_is_wounded, ":closest_agent"),
            (party_wound_members, "p_temp_party", ":closest_troop", 1),
          (try_end),
        (else_try),
          (party_add_members, "p_temp_party_2", ":closest_troop", 1),
          (try_begin),
            (agent_is_wounded, ":closest_agent"),
            (party_wound_members, "p_temp_party_2", ":closest_troop", 1),
          (try_end),
        (try_end),
      (try_end),
  ]),
  
  
  # script_map_get_random_position_around_position_within_range
  # Input: arg1 = minimum_distance in km, arg2 = maximum_distance in km, pos1 = origin position
  # Output: pos2 = result position
  ("map_get_random_position_around_position_within_range",
    [
      (store_script_param_1, ":min_distance"),
      (store_script_param_2, ":max_distance"),
      (val_mul, ":min_distance", 100),
      (assign, ":continue", 1),
      (try_for_range, ":unused", 0, 20),
        (eq, ":continue", 1),
        (map_get_random_position_around_position, pos2, pos1, ":max_distance"),
        (get_distance_between_positions, ":distance", pos2, pos1),
        (ge, ":distance", ":min_distance"),
        (assign, ":continue", 0),
      (try_end),
  ]),
  
  
  # script_get_number_of_unclaimed_centers_by_player
  # Input: none
  # Output: reg0 = number of unclaimed centers, reg1 = last unclaimed center_no
  ("get_number_of_unclaimed_centers_by_player",
    [
      (assign, ":unclaimed_centers", 0),
      (assign, reg1, -1),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
        (store_faction_of_party, ":faction_no", ":center_no"),
        (eq, ":faction_no", "fac_player_supporters_faction"),
        (party_slot_eq, ":center_no", slot_town_claimed_by_player, 0),
        (party_get_num_companion_stacks, ":num_stacks", ":center_no"),
        (ge, ":num_stacks", 1), #castle is garrisoned
        (assign, reg1, ":center_no"),
        (val_add, ":unclaimed_centers", 1),
      (try_end),
      (assign, reg0, ":unclaimed_centers"),
  ]),
  
  # script_troop_count_number_of_enemy_troops
  # Input: arg1 = troop_no
  # Output: reg0 = number_of_enemy_troops
  ("troop_count_number_of_enemy_troops",
    [
      (store_script_param_1, ":troop_no"),
      (assign, ":enemy_count", 0),
      (try_for_range, ":i_enemy_slot", slot_troop_enemies_begin, slot_troop_enemies_end),
        (troop_slot_ge, ":troop_no", ":i_enemy_slot", 1),
        (val_add, ":enemy_count", 1),
      (try_end),
      (assign, reg0, ":enemy_count"),
  ]),
  
  
  # script_cf_troop_check_troop_is_enemy
  # Input: arg1 = troop_no, arg2 = checked_troop_no
  # Output: none (Can fail)
  ("cf_troop_check_troop_is_enemy",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":checked_troop_no"),
      (assign, ":result", 0),
      (try_for_range, ":i_enemy_slot", slot_troop_enemies_begin, slot_troop_enemies_end),
        (troop_slot_eq, ":troop_no", ":i_enemy_slot", ":checked_troop_no"),
        (assign, ":result", 1),
      (try_end),
      (eq, ":result", 1),
  ]),
  
  
  # script_troop_get_leaded_center_with_index
  # Input: arg1 = troop_no, arg2 = center index within range between zero and the number of centers that troop owns
  # Output: reg0 = center_no
  ("troop_get_leaded_center_with_index",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":random_center"),
      (assign, ":result", -1),
      (assign, ":center_count", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
        (eq, ":result", -1),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (val_add, ":center_count", 1),
        (gt, ":center_count", ":random_center"),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
  
  # script_cf_troop_get_random_leaded_walled_center_with_less_strength_priority
  # Input: arg1 = troop_no, arg2 = preferred_center_no
  # Output: reg0 = center_no (Can fail)
  ("cf_troop_get_random_leaded_walled_center_with_less_strength_priority",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":preferred_center_no", 2),

      (assign, ":num_centers", 0),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (party_is_active, ":center_no"), #TLD
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1),
        (val_add, ":num_centers", 1),
        (try_begin),
          (eq, ":center_no", ":preferred_center_no"),
          (val_add, ":num_centers", 99),
        (try_end),
##        (call_script, "script_party_calculate_regular_strength", ":center_no"),
##        (assign, ":strength", reg0),
##        (lt, ":strength", 80),
##        (store_sub, ":strength", 100, ":strength"),
##        (val_div, ":strength", 20),
##        (val_add, ":num_centers", ":strength"),
      (try_end),
      (gt, ":num_centers", 0),
      (store_random_in_range, ":random_center", 0, ":num_centers"),
      (assign, ":result", -1),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (party_is_active, ":center_no"), #TLD
        (eq, ":result", -1),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1),
        (val_sub, ":random_center", 1),
        (try_begin),
          (eq, ":center_no", ":preferred_center_no"),
          (val_sub, ":random_center", 99),
        (try_end),
##        (try_begin),
##          (call_script, "script_party_calculate_regular_strength", ":center_no"),
##          (assign, ":strength", reg0),
##          (lt, ":strength", 80),
##          (store_sub, ":strength", 100, ":strength"),
##          (val_div, ":strength", 20),
##          (val_sub, ":random_center", ":strength"),
##        (try_end),
        (lt, ":random_center", 0),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
  ]),

  # script_cf_troop_get_random_leaded_town_or_village_except_center
  # Input: arg1 = troop_no, arg2 = except_center_no
  # Output: reg0 = center_no (Can fail)
  ("cf_troop_get_random_leaded_town_or_village_except_center",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":except_center_no"),

      (assign, ":num_centers", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
        (neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (neq, ":center_no", ":except_center_no"),
        (val_add, ":num_centers", 1),
      (try_end),

      (gt, ":num_centers", 0),
      (store_random_in_range, ":random_center", 0, ":num_centers"),
      (assign, ":end_cond", centers_end),
      (try_for_range, ":center_no", centers_begin, ":end_cond"),
        (party_is_active, ":center_no"), #TLD
        (neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (neq, ":center_no", ":except_center_no"),
        (val_sub, ":random_center", 1),
        (lt, ":random_center", 0),
        (assign, ":target_center", ":center_no"),
        (assign, ":end_cond", 0),
      (try_end),
      (assign, reg0, ":target_center"),
  ]),

  # script_troop_write_owned_centers_to_s2
  # Input: arg1 = troop_no
  ("troop_write_owned_centers_to_s2",
    [
      (store_script_param_1, ":troop_no"),
      
      (call_script, "script_get_number_of_hero_centers", ":troop_no"),
      (assign, ":no_centers", reg0),
      
      (str_store_troop_name, s5, ":troop_no"),
      
      (try_begin),
        (gt, ":no_centers", 1),
        (try_for_range, ":i_center", 1, ":no_centers"),
          (call_script, "script_troop_get_leaded_center_with_index", ":troop_no", ":i_center"),
          (str_store_party_name_link, s50, reg0),
          (try_begin),
            (eq, ":i_center", 1),
            (call_script, "script_troop_get_leaded_center_with_index", ":troop_no", 0),
            (str_store_party_name_link, s51, reg0),
            (str_store_string, s51, "str_s50_and_s51"),
          (else_try),
            (str_store_string, s51, "str_s50_comma_s51"),
          (try_end),
        (try_end),
        (str_store_string, s2, "str_s5_is_the_ruler_of_s51"),
      (else_try),
        (eq, ":no_centers", 1),
        (call_script, "script_troop_get_leaded_center_with_index", ":troop_no", 0),
        (str_store_party_name_link, s51, reg0),
        (str_store_string, s2, "str_s5_is_the_ruler_of_s51"),
      (else_try),
        (store_troop_faction, ":faction_no", ":troop_no"),
        (str_store_faction_name_link, s6, ":faction_no"),
        (str_store_string, s2, "str_s5_is_a_nobleman_of_s6"),
      (try_end),
  ]),
  
  # script_troop_write_family_relations_to_s1
  # Input: arg1 = troop_no
  ("troop_write_family_relations_to_s1",
    [
      (store_script_param_1, ":troop_no"),
      (assign, ":num_family", 0),
      (try_for_range, ":slot_no", slot_troop_family_begin, slot_troop_family_end),
        (troop_slot_ge, ":troop_no", ":slot_no", 1),
        (val_add, ":num_family", 1),
      (try_end),
      
      (troop_get_type, ":gender", ":troop_no"),
      (try_begin),
        (eq, ":gender", 1),
        (str_store_string, s5, "str_she"),
      (else_try),
        (str_store_string, s5, "str_he"),
      (try_end),
      
      (try_begin),
        (gt, ":num_family", 1),
        (try_for_range, ":i_family", 1, ":num_family"),
          (call_script, "script_write_family_relation_as_s3s_s2_to_s4", ":troop_no", ":i_family"),
          (str_store_string_reg, s50, s4),
          (try_begin),
            (eq, ":i_family", 1),
            (call_script, "script_write_family_relation_as_s3s_s2_to_s4", ":troop_no", 0),
            (str_store_string_reg, s51, s4),
            (str_store_string, s51, "str_s50_and_s51"),
          (else_try),
            (str_store_string, s51, "str_s50_comma_s51"),
          (try_end),
        (try_end),
        (str_store_string, s1, "str_s5_is_s51"),
      (else_try),
        (eq, ":num_family", 1),
        (call_script, "script_write_family_relation_as_s3s_s2_to_s4", ":troop_no", 0),
        (str_store_string_reg, s51, s4),
        (str_store_string, s1, "str_s5_is_s51"),
      (else_try),
        (str_store_string, s1, "str_blank_string"),
      (try_end),
  ]),
  
  # script_write_family_relation_as_s3s_s2_to_s4
  # Inputs: arg1 = troop_no, arg2 = family_no (valid slot no after slot_troop_family_begin)
  # Outputs: s50 = s3s_s2 text
  ("write_family_relation_as_s3s_s2_to_s4",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":family_no"),
      (troop_get_type, ":gender", ":troop_no"),
      (assign, ":slot_no", slot_troop_family_begin),
      (try_for_range, ":unused", slot_troop_family_begin, slot_troop_family_end),
        (this_or_next|gt, ":family_no", 0),
        (troop_slot_eq, ":troop_no", ":slot_no", 0),
        (try_begin),
          (troop_slot_ge, ":troop_no", ":slot_no", 1),
          (val_sub, ":family_no", 1),
        (try_end),
        (val_add, ":slot_no", 1),
      (try_end),
      (try_begin),
        (eq, ":slot_no", slot_troop_spouse),
        (try_begin),
          (eq, ":gender", 0),
          (str_store_string, s2, "str_husband"),
        (else_try),
          (str_store_string, s2, "str_wife"),
        (try_end),
      (else_try),
        (this_or_next|eq, ":slot_no", slot_troop_son),
        (eq, ":slot_no", slot_troop_daughter),
        (try_begin),
          (eq, ":gender", 0),
          (str_store_string, s2, "str_father"),
        (else_try),
          (str_store_string, s2, "str_mother"),
        (try_end),
      (else_try),
        (this_or_next|eq, ":slot_no", slot_troop_father),
        (eq, ":slot_no", slot_troop_mother),
        (try_begin),
          (eq, ":gender", 0),
          (str_store_string, s2, "str_son"),
        (else_try),
          (str_store_string, s2, "str_daughter"),
        (try_end),
      (else_try),
        (eq, ":slot_no", slot_troop_sibling),
        (try_begin),
          (eq, ":gender", 0),
          (str_store_string, s2, "str_brother"),
        (else_try),
          (str_store_string, s2, "str_sister"),
        (try_end),
      (try_end),
      (troop_get_slot, ":cur_family", ":troop_no", ":slot_no"),
      (str_store_troop_name_link, s3, ":cur_family"),
      (str_store_string, s4, "str_s3s_s2"),
  ]),
  
  
  # script_complete_family_relations
  ("complete_family_relations",
    [
      #Completing family relations
      (try_for_range, ":troop_id", heroes_begin, heroes_end),
        (troop_get_type, ":troop_gender", ":troop_id"),
        (try_begin),
          (troop_get_slot, ":cur_spouse", ":troop_id", slot_troop_spouse),
          (gt, ":cur_spouse", 0),
          (troop_set_slot, ":cur_spouse", slot_troop_spouse, ":troop_id"),
          #Adding children from troop to new spouse
          (troop_get_slot, ":cur_daughter", ":troop_id", slot_troop_daughter),
          (troop_get_slot, ":cur_son", ":troop_id", slot_troop_son),
          (try_begin),
            (gt, ":cur_daughter", 0),
            (troop_set_slot, ":cur_spouse", slot_troop_daughter, ":cur_daughter"),
          (try_end),
          (try_begin),
            (gt, ":cur_son", 0),
            (troop_set_slot, ":cur_spouse", slot_troop_son, ":cur_son"),
          (try_end),
          #Adding children from new spouse to troop
          (troop_get_slot, ":cur_daughter", ":cur_spouse", slot_troop_daughter),
          (troop_get_slot, ":cur_son", ":cur_spouse", slot_troop_son),
          (try_begin),
            (gt, ":cur_daughter", 0),
            (troop_set_slot, ":troop_id", slot_troop_daughter, ":cur_daughter"),
          (try_end),
          (try_begin),
            (gt, ":cur_son", 0),
            (troop_set_slot, ":troop_id", slot_troop_son, ":cur_son"),
          (try_end),
        (try_end),
        (try_begin),
          (troop_get_slot, ":cur_sibling", ":troop_id", slot_troop_sibling),
          (gt, ":cur_sibling", 0),
          (troop_set_slot, ":cur_sibling", slot_troop_sibling, ":troop_id"),
          #Adding parents from troop to new sibling
          (troop_get_slot, ":cur_mother", ":troop_id", slot_troop_mother),
          (troop_get_slot, ":cur_father", ":troop_id", slot_troop_father),
          (try_begin),
            (gt, ":cur_mother", 0),
            (troop_set_slot, ":cur_sibling", slot_troop_mother, ":cur_mother"),
          (try_end),
          (try_begin),
            (gt, ":cur_father", 0),
            (troop_set_slot, ":cur_sibling", slot_troop_father, ":cur_father"),
          (try_end),
          #Adding parents from new sibling to troop
          (troop_get_slot, ":cur_mother", ":cur_sibling", slot_troop_mother),
          (troop_get_slot, ":cur_father", ":cur_sibling", slot_troop_father),
          (try_begin),
            (gt, ":cur_mother", 0),
            (troop_set_slot, ":troop_id", slot_troop_mother, ":cur_mother"),
          (try_end),
          (try_begin),
            (gt, ":cur_father", 0),
            (troop_set_slot, ":troop_id", slot_troop_father, ":cur_father"),
          (try_end),
        (try_end),
        (try_begin),
          (troop_get_slot, ":cur_child", ":troop_id", slot_troop_son),
          (gt, ":cur_child", 0),
          (try_begin),
            (eq, ":troop_gender", 0),
            (troop_set_slot, ":cur_child", slot_troop_father, ":troop_id"),
          (else_try),
            (troop_set_slot, ":cur_child", slot_troop_mother, ":troop_id"),
          (try_end),
          #Adding mother/father and sibling from troop to new son
          (troop_get_slot, ":cur_mother_father", ":troop_id", slot_troop_spouse),
          (troop_get_slot, ":cur_sibling", ":troop_id", slot_troop_daughter),
          (try_begin),
            (gt, ":cur_mother_father", 0),
            (try_begin),
              (eq, ":troop_gender", 1),
              (troop_set_slot, ":cur_child", slot_troop_father, ":cur_mother_father"),
            (else_try),
              (troop_set_slot, ":cur_child", slot_troop_mother, ":cur_mother_father"),
            (try_end),
          (try_end),
          (try_begin),
            (gt, ":cur_sibling", 0),
            (troop_set_slot, ":cur_child", slot_troop_sibling, ":cur_sibling"),
          (try_end),
          #Adding son/daughter and spouse from new son to troop
          (try_begin),
            (eq, ":troop_gender", 0),
            (troop_get_slot, ":cur_spouse", ":cur_child", slot_troop_mother),
          (else_try),
            (troop_get_slot, ":cur_spouse", ":cur_child", slot_troop_father),
          (try_end),
          (troop_get_slot, ":cur_daughter", ":cur_child", slot_troop_sibling),
          (try_begin),
            (gt, ":cur_spouse", 0),
            (troop_set_slot, ":troop_id", slot_troop_spouse, ":cur_spouse"),
          (try_end),
          (try_begin),
            (gt, ":cur_daughter", 0),
            (troop_set_slot, ":troop_id", slot_troop_daughter, ":cur_daughter"),
          (try_end),
        (try_end),
        (try_begin),
          (troop_get_slot, ":cur_child", ":troop_id", slot_troop_daughter),
          (gt, ":cur_child", 0),
          (try_begin),
            (eq, ":troop_gender", 0),
            (troop_set_slot, ":cur_child", slot_troop_father, ":troop_id"),
          (else_try),
            (troop_set_slot, ":cur_child", slot_troop_mother, ":troop_id"),
          (try_end),
          #Adding mother/father and sibling from troop to new daughter
          (troop_get_slot, ":cur_mother_father", ":troop_id", slot_troop_spouse),
          (troop_get_slot, ":cur_sibling", ":troop_id", slot_troop_son),
          (try_begin),
            (gt, ":cur_mother_father", 0),
            (try_begin),
              (eq, ":troop_gender", 1),
              (troop_set_slot, ":cur_child", slot_troop_father, ":cur_mother_father"),
            (else_try),
              (troop_set_slot, ":cur_child", slot_troop_mother, ":cur_mother_father"),
            (try_end),
          (try_end),
          (try_begin),
            (gt, ":cur_sibling", 0),
            (troop_set_slot, ":cur_child", slot_troop_sibling, ":cur_sibling"),
          (try_end),
          #Adding son/daughter and spouse from new daughter to troop
          (try_begin),
            (eq, ":troop_gender", 0),
            (troop_get_slot, ":cur_spouse", ":cur_child", slot_troop_mother),
          (else_try),
            (troop_get_slot, ":cur_spouse", ":cur_child", slot_troop_father),
          (try_end),
          (troop_get_slot, ":cur_son", ":cur_child", slot_troop_sibling),
          (try_begin),
            (gt, ":cur_spouse", 0),
            (troop_set_slot, ":troop_id", slot_troop_spouse, ":cur_spouse"),
          (try_end),
          (try_begin),
            (gt, ":cur_son", 0),
            (troop_set_slot, ":troop_id", slot_troop_son, ":cur_son"),
          (try_end),
        (try_end),
        (try_begin),
          (troop_get_slot, ":cur_father", ":troop_id", slot_troop_father),
          (gt, ":cur_father", 0),
          (try_begin),
            (eq, ":troop_gender", 0),
            (troop_set_slot, ":cur_father", slot_troop_son, ":troop_id"),
          (else_try),
            (troop_set_slot, ":cur_father", slot_troop_daughter, ":troop_id"),
          (try_end),
          #Adding son/daughter and spouse from troop to new father
          (troop_get_slot, ":cur_spouse", ":troop_id", slot_troop_mother),
          (troop_get_slot, ":cur_son_daughter", ":troop_id", slot_troop_sibling),
          (try_begin),
            (gt, ":cur_spouse", 0),
            (troop_set_slot, ":cur_father", slot_troop_spouse, ":cur_spouse"),
          (try_end),
          (try_begin),
            (gt, ":cur_son_daughter", 0),
            (try_begin),
              (eq, ":troop_gender", 0),
              (troop_set_slot, ":cur_father", slot_troop_daughter, ":cur_son_daughter"),
            (else_try),
              (troop_set_slot, ":cur_father", slot_troop_son, ":cur_son_daughter"),
            (try_end),
          (try_end),
          #Adding mother/father and sibling from new father to troop
          (try_begin),
            (eq, ":troop_gender", 0),
            (troop_get_slot, ":cur_sibling", ":cur_father", slot_troop_daughter),
          (else_try),
            (troop_get_slot, ":cur_sibling", ":cur_father", slot_troop_son),
          (try_end),
          (troop_get_slot, ":cur_mother", ":cur_father", slot_troop_spouse),
          (try_begin),
            (gt, ":cur_sibling", 0),
            (troop_set_slot, ":troop_id", slot_troop_sibling, ":cur_sibling"),
          (try_end),
          (try_begin),
            (gt, ":cur_mother", 0),
            (troop_set_slot, ":troop_id", slot_troop_mother, ":cur_mother"),
          (try_end),
        (try_end),
        (try_begin),
          (troop_get_slot, ":cur_mother", ":troop_id", slot_troop_mother),
          (gt, ":cur_mother", 0),
          (try_begin),
            (eq, ":troop_gender", 0),
            (troop_set_slot, ":cur_mother", slot_troop_son, ":troop_id"),
          (else_try),
            (troop_set_slot, ":cur_mother", slot_troop_daughter, ":troop_id"),
          (try_end),
          #Adding son/daughter and spouse from troop to new mother
          (troop_get_slot, ":cur_spouse", ":troop_id", slot_troop_father),
          (troop_get_slot, ":cur_son_daughter", ":troop_id", slot_troop_sibling),
          (try_begin),
            (gt, ":cur_spouse", 0),
            (troop_set_slot, ":cur_mother", slot_troop_spouse, ":cur_spouse"),
          (try_end),
          (try_begin),
            (gt, ":cur_son_daughter", 0),
            (try_begin),
              (eq, ":troop_gender", 0),
              (troop_set_slot, ":cur_mother", slot_troop_daughter, ":cur_son_daughter"),
            (else_try),
              (troop_set_slot, ":cur_mother", slot_troop_son, ":cur_son_daughter"),
            (try_end),
          (try_end),
          #Adding mother/father and sibling from new mother to troop
          (try_begin),
            (eq, ":troop_gender", 0),
            (troop_get_slot, ":cur_sibling", ":cur_mother", slot_troop_daughter),
          (else_try),
            (troop_get_slot, ":cur_sibling", ":cur_mother", slot_troop_son),
          (try_end),
          (troop_get_slot, ":cur_father", ":cur_mother", slot_troop_spouse),
          (try_begin),
            (gt, ":cur_sibling", 0),
            (troop_set_slot, ":troop_id", slot_troop_sibling, ":cur_sibling"),
          (try_end),
          (try_begin),
            (gt, ":cur_father", 0),
            (troop_set_slot, ":troop_id", slot_troop_father, ":cur_father"),
          (try_end),
        (try_end),
      (try_end),
  ]),
  
  # script_collect_friendly_parties
  # Fills the party p_collective_friends with the members of parties attached to main_party and ally_party_no
  ("collect_friendly_parties",
    [
      (party_collect_attachments_to_party, "p_main_party", "p_collective_friends"),
      (try_begin),
        (gt, "$g_ally_party", 0),
        (party_collect_attachments_to_party, "$g_ally_party", "p_temp_party"),
        (assign, "$g_move_heroes", 1),
        (call_script, "script_party_add_party", "p_collective_friends", "p_temp_party"),
      (try_end),
  ]),

  # script_encounter_calculate_fit
  # Input: arg1 = troop_no
  # Output: none
  ("encounter_calculate_fit",
    [
#      (assign, "$g_enemy_fit_for_battle_old",  "$g_enemy_fit_for_battle"),
#      (assign, "$g_friend_fit_for_battle_old", "$g_friend_fit_for_battle"),
#      (assign, "$g_main_party_fit_for_battle_old", "$g_main_party_fit_for_battle"),
      (call_script, "script_party_count_fit_for_battle", "p_main_party"),
 #     (assign, "$g_main_party_fit_for_battle", reg(0)),
      (call_script, "script_collect_friendly_parties"),
      (call_script, "script_party_count_fit_for_battle", "p_collective_friends"),
      (assign, "$g_friend_fit_for_battle", reg(0)),

      (party_clear, "p_collective_ally"),
      (try_begin),
        (gt, "$g_ally_party", 0),
        (party_is_active, "$g_ally_party"),
        (party_collect_attachments_to_party, "$g_ally_party", "p_collective_ally"),
#        (call_script, "script_party_count_fit_for_battle", "p_collective_ally"),
#        (val_add, "$g_friend_fit_for_battle", reg(0)),
      (try_end),

      (party_clear, "p_collective_enemy"),
      (try_begin),
        (party_is_active, "$g_enemy_party"),
        (party_collect_attachments_to_party, "$g_enemy_party", "p_collective_enemy"),
      (try_end),
      (call_script, "script_party_count_fit_for_battle", "p_collective_enemy"),
      (assign, "$g_enemy_fit_for_battle", reg(0)),
      (assign, reg11, "$g_enemy_fit_for_battle"),
      (assign, reg10, "$g_friend_fit_for_battle"),
  ]),
  
  # script_encounter_init_variables
  # Input: arg1 = troop_no
  # Output: none
  ("encounter_init_variables",
    [
      (assign, "$capture_screen_shown", 0),
      (assign, "$loot_screen_shown", 0),
      (assign, "$thanked_by_ally_leader", 0),
      (assign, "$g_battle_result", 0),
      (assign, "$cant_leave_encounter", 0),
      (assign, "$cant_talk_to_enemy", 0),
      (assign, "$last_defeated_hero", 0),
      (assign, "$last_freed_hero", 0),

      (call_script, "script_encounter_calculate_fit"),
      (call_script, "script_party_copy", "p_main_party_backup", "p_main_party"),
      (call_script, "script_party_calculate_strength", "p_main_party", 0),
      (assign, "$g_starting_strength_main_party", reg0),
      (call_script, "script_party_copy", "p_encountered_party_backup", "p_collective_enemy"),
      (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
      (assign, "$g_starting_strength_enemy_party", reg0),
#      (assign, "$g_starting_strength_ally_party", 0),
      (assign, "$g_strength_contribution_of_player", 100),

      (call_script, "script_party_copy", "p_collective_friends_backup", "p_collective_friends"),
      (call_script, "script_party_calculate_strength", "p_collective_friends", 0),
      (assign, "$g_starting_strength_friends", reg0),

      (store_mul, "$g_strength_contribution_of_player","$g_starting_strength_main_party", 100), # reduce contribution if we are helping someone.
      (val_div, "$g_strength_contribution_of_player","$g_starting_strength_friends"),

#      (try_begin),
#        (gt, "$g_ally_party", 0),
#        (call_script, "script_party_copy", "p_ally_party_backup", "p_collective_ally"),
#        (call_script, "script_party_calculate_strength", "p_collective_ally"),
#        (assign, "$g_starting_strength_ally_party", reg0),
#        (store_add, ":starting_strength_factor_combined","$g_starting_strength_ally_party","$g_starting_strength_main_party"),
#         (store_mul, "$g_strength_contribution_of_player","$g_starting_strength_main_party", 80), #reduce contribution if we are helping someone.
#        (val_div, "$g_strength_contribution_of_player",":starting_strength_factor_combined"),
#      (try_end),
  ]),
  
#script_party_vote_race
	# each party member "votes" his race,. Votes go in reg15 and reg16 -- mtarini
    ("party_vote_race",
    [
      (store_script_param_1, ":party"), #Party_id
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_size, ":n",":party",":i_stack"),
		(party_stack_get_troop_id, ":tr",":party",":i_stack"),
        (try_begin),(eq, ":tr", "trp_player"),
			(val_mul, ":n", 8), # player "vote" counts for 8!
		(try_end),
		(troop_get_type,":race",":tr"),
		(try_begin),(is_between, ":race", tf_orc_begin, tf_orc_end),
			(val_add, reg15, ":n"),
		(else_try), 
			(val_add, reg16, ":n"),
			(try_begin),(eq, ":race", tf_dwarf),
				(val_add, reg18, ":n"),
			(else_try), 
				(val_add, reg19, ":n"),
			(else_try), (is_between, ":race", tf_elf_begin, tf_elf_end),
				(val_add, reg17, ":n"),
			(try_end),
		(try_end),
      (try_end),
  ]),

  
#script_calculate_battleside_races
  # compute with rache each battle is (mtarini)
  # $player_side_race_group = humanoids or orchoids
  # $player_side_race = humanoids or orchoids
  ("calculate_battleside_races", [
	(assign, reg15, 0), # humanoids
	(assign, reg16, 0), # orcoids
	(assign, reg17, 0), # humans
	(assign, reg18, 0), # dwarves
	(assign, reg19, 0), # elves
	(call_script, "script_party_vote_race", "p_main_party"),
	(call_script, "script_party_vote_race", "p_collective_friends"),
	(try_begin), (gt, reg15, reg16),
		(assign, "$player_side_race_group", tf_orc),
	(else_try), 
		(assign, "$player_side_race_group", tf_male),
		(try_begin), (gt, reg19, reg18),(gt, reg19, reg17),
			(assign, "$player_side_race", tf_elf_begin),
		(else_try), (gt, reg18, reg17),
			(assign, "$player_side_race", tf_dwarf),
		(else_try), 
			(assign, "$player_side_race", tf_male),
		(try_end),
	(try_end),
	(assign, reg15, 0), # humanoids 
	(assign, reg16, 0), # orcoids
	(assign, reg17, 0), # humans
	(assign, reg18, 0), # dwarves
	(assign, reg19, 0), # elves
	(call_script, "script_party_vote_race", "p_collective_enemy"),
	(try_begin), (gt, reg15, reg16),
		(assign, "$enemy_side_race_group", tf_orc),
	(else_try), 
		(assign, "$enemy_side_race_group", tf_male),
		
		(try_begin), (gt, reg19, reg18),(gt, reg19, reg17),
			(assign, "$enemy_side_race", tf_elf_begin),
		(else_try), (gt, reg18, reg17),
			(assign, "$enemy_side_race", tf_dwarf),
		(else_try), 
			(assign, "$enemy_side_race", tf_male),
		(try_end),

	(try_end),
   
   ] ),

  # script_calculate_renown_value
  # Input: arg1 = troop_no
  # Output: fills $battle_renown_value
  ("calculate_renown_value",
   [
      (call_script, "script_party_calculate_strength", "p_main_party", 0),
      (assign, ":main_party_strength", reg0),
      (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
      (assign, ":enemy_strength", reg0),
      (call_script, "script_party_calculate_strength", "p_collective_friends", 0),
      (assign, ":friends_strength", reg0),

      (val_add, ":friends_strength", 1),
      (store_mul, ":enemy_strength_ratio", ":enemy_strength", 100),
      (val_div, ":enemy_strength_ratio", ":friends_strength"),

      (assign, ":renown_val", ":enemy_strength"),
      (val_mul, ":renown_val", ":enemy_strength_ratio"),
      (val_div, ":renown_val", 100),

      (val_mul, ":renown_val", ":main_party_strength"),
      (val_div, ":renown_val",":friends_strength"),

      (store_div, "$battle_renown_value", ":renown_val", 5),
      (val_min, "$battle_renown_value", 2500),
      (convert_to_fixed_point, "$battle_renown_value"),
      (store_sqrt, "$battle_renown_value", "$battle_renown_value"),
      (convert_from_fixed_point, "$battle_renown_value"),
      (assign, reg8, "$battle_renown_value"),
      (display_message, "@Renown value for this battle is {reg8}.",0xFFFFFFFF),
  ]),
       

  
  # script_get_first_agent_with_troop_id
  # Input: arg1 = troop_no
  # Output: agent_id
  ("cf_get_first_agent_with_troop_id",
    [
      (store_script_param_1, ":troop_no"),
      #      (store_script_param_2, ":agent_no_to_begin_searching_after"),
      (assign, ":result", -1),
      (try_for_agents, ":cur_agent"),
        (eq, ":result", -1),
        ##        (try_begin),
        ##          (eq, ":cur_agent", ":agent_no_to_begin_searching_after"),
        ##          (assign, ":agent_no_to_begin_searching_after", -1),
        ##        (try_end),
        ##        (eq, ":agent_no_to_begin_searching_after", -1),
        (agent_get_troop_id, ":cur_troop_no", ":cur_agent"),
        (eq, ":cur_troop_no", ":troop_no"),
        (assign, ":result", ":cur_agent"),
      (try_end),
      (assign, reg0, ":result"),
      (neq, reg0, -1),
  ]),
  
  
  # script_cf_team_get_average_position_of_agents_with_type_to_pos1
  # Input: arg1 = team_no, arg2 = class_no (grc_everyone, grc_infantry, grc_cavalry, grc_archers, grc_heroes)
  # Output: none, pos1 = average_position (0,0,0 if there are no matching agents)
  ("cf_team_get_average_position_of_agents_with_type_to_pos1",
    [
      (store_script_param_1, ":team_no"),
      (store_script_param_2, ":class_no"),
      (assign, ":total_pos_x", 0),
      (assign, ":total_pos_y", 0),
      (assign, ":total_pos_z", 0),
      (assign, ":num_agents", 0),
      (set_fixed_point_multiplier, 100),
      (try_for_agents, ":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_get_team, ":cur_team_no", ":cur_agent"),
        (eq, ":cur_team_no", ":team_no"),
        (agent_get_class, ":cur_class_no", ":cur_agent"),
        (this_or_next|eq, ":class_no", grc_everyone),
        (eq, ":class_no", ":cur_class_no"),
        (agent_get_position, pos1, ":cur_agent"),
        (position_get_x, ":cur_pos_x", pos1),
        (val_add, ":total_pos_x", ":cur_pos_x"),
        (position_get_y, ":cur_pos_y", pos1),
        (val_add, ":total_pos_y", ":cur_pos_y"),
        (position_get_z, ":cur_pos_z", pos1),
        (val_add, ":total_pos_z", ":cur_pos_z"),
        (val_add, ":num_agents", 1),
      (try_end),
      (gt, ":num_agents", 1),
      (val_div, ":total_pos_x", ":num_agents"),
      (val_div, ":total_pos_y", ":num_agents"),
      (val_div, ":total_pos_z", ":num_agents"),
      (init_position, pos1),
      (position_move_x, pos1, ":total_pos_x"),
      (position_move_y, pos1, ":total_pos_y"),
      (position_move_z, pos1, ":total_pos_z"),
  ]),
  
  # script_cf_turn_windmill_fans
  # Input: arg1 = instance_no (none = 0)
  # Output: none
  ("cf_turn_windmill_fans",
    [(store_script_param_1, ":instance_no"),
      (scene_prop_get_instance, ":windmill_fan_object", "spr_windmill_fan_turning", ":instance_no"),
      (ge, ":windmill_fan_object", 0),
      (prop_instance_get_position, pos1, ":windmill_fan_object"),
      (position_rotate_y, pos1, 10),
      (prop_instance_animate_to_position, ":windmill_fan_object", pos1, 100),
      (val_add, ":instance_no", 1),
      (call_script, "script_cf_turn_windmill_fans", ":instance_no"),
  ]),
  
  # script_print_party_members
  # Input: arg1 = party_no
  # Output: s51 = output string. "noone" if the party is empty
  ("print_party_members",
    [(store_script_param_1, ":party_no"),
      (party_get_num_companion_stacks, ":num_stacks",":party_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
        (troop_is_hero, ":stack_troop"),
        (try_begin),
          (eq, ":i_stack", 0),
          (str_store_troop_name, s51, ":stack_troop"),
        (try_end),
        (str_store_troop_name, s50, ":stack_troop"),
        (try_begin),
          (eq, ":i_stack", 1),
          (str_store_string, s51, "str_s50_and_s51"),
        (else_try),
          (gt, ":i_stack", 1),
          (str_store_string, s51, "str_s50_comma_s51"),
        (try_end),
      (try_end),
      (try_begin),
        (eq, ":num_stacks", 0),
        (str_store_string, s51, "str_noone"),
      (try_end),
  ]),

  # script_round_value
  # Input: arg1 = value
  # Output: reg0 = rounded_value
  ("round_value",
    [ (store_script_param_1, ":value"),
      (try_begin),
        (lt, ":value", 100),
        (neq, ":value", 0),
        (val_add, ":value", 5),
        (val_div, ":value", 10),
        (val_mul, ":value", 10),
        (try_begin),
          (eq, ":value", 0),
          (assign, ":value", 5),
        (try_end),
      (else_try),
        (lt, ":value", 300),
        (val_add, ":value", 25),
        (val_div, ":value", 50),
        (val_mul, ":value", 50),
      (else_try),
        (val_add, ":value", 50),
        (val_div, ":value", 100),
        (val_mul, ":value", 100),
      (try_end),
      (assign, reg0, ":value"),
  ]),
  
  
##  # script_print_productions_above_or_below_50
##  # Input: arg1 = center_no, arg2 = sign of the production, 1 if produced goods, -1 if consumed goods
##  # Output: s51 = output string. "nothing" if there are no productions above or below 50
##  ("print_productions_above_or_below_50",
##    [(store_script_param_1, ":center_no"),
##      (store_script_param_2, ":sign"),
##      (store_sub, ":item_to_slot", slot_town_trade_good_productions_begin, trade_goods_begin),
##      (assign, ":cur_print_index", 0),
##      (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
##        (store_add, ":cur_good_slot", ":cur_goods", ":item_to_slot"),
##        (party_get_slot, ":cur_production", ":center_no", ":cur_good_slot"),
##        (val_mul, ":cur_production", ":sign"),
##        (ge, ":cur_production", 50),
##        (try_begin),
##          (eq, ":cur_print_index", 0),
##          (str_store_item_name, s51, ":cur_goods"),
##        (try_end),
##        (str_store_item_name, s50, ":cur_goods"),
##        (try_begin),
##          (eq, ":cur_print_index", 1),
##          (str_store_string, s51, "str_s50_and_s51"),
##        (else_try),
##          (gt, ":cur_print_index", 1),
##          (str_store_string, s51, "str_s50_comma_s51"),
##        (try_end),
##        (val_add, ":cur_print_index", 1),
##      (try_end),
##      (try_begin),
##        (eq, ":cur_print_index", 0),
##        (str_store_string, s51, "str_nothing"),
##      (try_end),
##  ]),
  
  # script_change_banners_and_chest
  # Input: none
  # Output: none
  ("change_banners_and_chest",
    [(party_get_slot, ":cur_leader", "$g_encountered_party", slot_town_lord),
     (try_begin),
       (ge, ":cur_leader", 0),
#normal_banner_begin
       (troop_get_slot, ":troop_banner_object", ":cur_leader", slot_troop_banner_scene_prop),
       (gt, ":troop_banner_object", 0),
       (replace_scene_props, banner_scene_props_begin, ":troop_banner_object"),
     (else_try),
       (replace_scene_props, banner_scene_props_begin, "spr_empty"),
#custom_banner_begin
#       (troop_get_slot, ":flag_spr", ":cur_leader", slot_troop_custom_banner_flag_type),
#       (ge, ":flag_spr", 0),
#       (val_add, ":flag_spr", custom_banner_flag_scene_props_begin),
#       (replace_scene_props, banner_scene_props_begin, ":flag_spr"),
#     (else_try),
#       (replace_scene_props, banner_scene_props_begin, "spr_empty"),
     (try_end),
     (try_begin),
       (neq, ":cur_leader", "trp_player"),
       (replace_scene_props, "spr_player_chest", "spr_locked_player_chest"),
     (try_end),
     ]),

  # script_remove_siege_objects
  ("remove_siege_objects",
    [ (replace_scene_props, "spr_battlement_a_destroyed", "spr_battlement_a"),
#      (replace_scene_props, "spr_snowy_castle_battlement_a_destroyed", "spr_snowy_castle_battlement_a"),
      (replace_scene_props, "spr_castle_e_battlement_a_destroyed", "spr_castle_e_battlement_a"),
      (replace_scene_props, "spr_castle_battlement_a_destroyed", "spr_castle_battlement_a"),
      (replace_scene_props, "spr_castle_battlement_b_destroyed", "spr_castle_battlement_b"),
      (replace_scene_props, "spr_earth_wall_a2", "spr_earth_wall_a"),
      (replace_scene_props, "spr_earth_wall_b2", "spr_earth_wall_b"),
      (replace_scene_props, "spr_belfry_platform_b", "spr_empty"),
      (replace_scene_props, "spr_belfry_platform_a", "spr_empty"),
      (replace_scene_props, "spr_belfry_a", "spr_empty"),
      (replace_scene_props, "spr_belfry_wheel", "spr_empty"),
      (replace_scene_props, "spr_siege_ladder_12m", "spr_empty"),
      (replace_scene_props, "spr_siege_ladder_14m", "spr_empty"),
      (replace_scene_props, "spr_mangonel", "spr_empty"),
      (replace_scene_props, "spr_trebuchet_old", "spr_empty"),
      (replace_scene_props, "spr_trebuchet_new", "spr_empty"),
      (replace_scene_props, "spr_stone_ball", "spr_empty"),
      (replace_scene_props, "spr_Village_fire_big", "spr_empty"),
      ]),

  # script_describe_relation_to_s63
  # Input: arg1 = relation (-100 .. 100)
  # Output: none
  ("describe_relation_to_s63",
    [(store_script_param_1, ":relation"),
      (store_add, ":normalized_relation", ":relation", 100),
      (val_add, ":normalized_relation", 5),
      (store_div, ":str_offset", ":normalized_relation", 10),
      (val_clamp, ":str_offset", 0, 20),
      (store_add, ":str_id", "str_relation_mnus_100",  ":str_offset"),
      (str_store_string, s63, ":str_id"),
  ]),
  
  # script_describe_center_relation_to_s3
  # Input: arg1 = relation (-100 .. 100)
  # Output: none
  ("describe_center_relation_to_s3",
    [(store_script_param_1, ":relation"),
      (store_add, ":normalized_relation", ":relation", 100),
      (val_add, ":normalized_relation", 5),
      (store_div, ":str_offset", ":normalized_relation", 10),
      (val_clamp, ":str_offset", 0, 20),
      (store_add, ":str_id", "str_center_relation_mnus_100",  ":str_offset"),
      (str_store_string, s3, ":str_id"),
  ]),

  # script_center_ambiance_sounds
  # to be called every two seconds. TODO for TLD centers
  ("center_ambiance_sounds",
    [   #(assign, ":sound_1", -1),
        #(assign, ":sound_2", -1),
        #(assign, ":sound_3", -1),
        #(assign, ":sound_4", -1),
        #(assign, ":sound_5", -1),
        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
          (try_begin),
            (neg|is_currently_night),
        #    (assign, ":sound_3", "snd_distant_dog_bark"),
        #    (assign, ":sound_3", "snd_distant_chicken"),
          (else_try),
        #    (assign, ":sound_1", "snd_distant_dog_bark"),
        #    (assign, ":sound_2", "snd_distant_owl"),
          (try_end),
        (else_try),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (try_begin),
            (neg|is_currently_night),
        #    (assign, ":sound_1", "snd_distant_carpenter"),
        #    (assign, ":sound_2", "snd_distant_blacksmith"),
        #    (assign, ":sound_3", "snd_distant_dog_bark"),
          (else_try),
        #    (assign, ":sound_1", "snd_distant_dog_bark"),
          (try_end),
        (try_end),
        (try_begin),
        #  (store_random_in_range, ":r", 0, 7),

        #  (try_begin),(eq, ":r", 1),(ge, ":sound_1", 0),(play_sound, ":sound_1"),
        #  (else_try) ,(eq, ":r", 2),(ge, ":sound_2", 0),(play_sound, ":sound_2"),
        #  (else_try) ,(eq, ":r", 3),(ge, ":sound_3", 0),(play_sound, ":sound_3"),
        #  (else_try) ,(eq, ":r", 4),(ge, ":sound_4", 0),(play_sound, ":sound_4"),
        #  (else_try) ,(eq, ":r", 5),(ge, ":sound_5", 0),(play_sound, ":sound_5"),
        #  (try_end),
        (try_end),
  ]),

  # script_center_set_walker_to_type
  # Input: arg1 = center_no, arg2 = walker_no, arg3 = walker_type, 
  # Output: none
  ("center_set_walker_to_type",
   [
       (store_script_param, ":center_no", 1),
       (store_script_param, ":walker_no", 2),
       (store_script_param, ":walker_type", 3),
       (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
       (party_set_slot, ":center_no", ":type_slot", ":walker_type"),
#       (try_begin),
#         (party_slot_eq, ":center_no", slot_party_type, spt_village),
#         (store_random_in_range, ":walker_troop_id", village_walkers_begin, village_walkers_end),
#       (else_try),
#         (store_random_in_range, ":walker_troop_id", town_walkers_begin, town_walkers_end),
#       (try_end),
       (party_get_slot, ":walker_troop_id", ":center_no", slot_center_walker_0_troop),
       (try_begin),
         (eq,":walker_type",walkert_spy),
         (assign,":original_walker",":walker_troop_id"),
         (val_add,":walker_troop_id",4), # select spy troop id

         # restore spy inventory
         (try_for_range,":item_no","itm_horse_meat","itm_one_handed_war_axe_a"),
            (store_item_kind_count,":num_items",":item_no",":original_walker"),
            (ge,":num_items",1),
            (store_item_kind_count,":num_items",":item_no",":walker_troop_id"),
            (lt,":num_items",1),
            (troop_add_items,":walker_troop_id",":item_no",1),
         (try_end),
         # determine spy recognition item
         (store_random_in_range,":spy_item_type",itp_type_head_armor,itp_type_hand_armor),
         (assign,":num",0),
         (try_for_range,":item_no","itm_horse_meat","itm_one_handed_war_axe_a"),
            (store_item_kind_count,":num_items",":item_no",":walker_troop_id"),
            (ge,":num_items",1),
            (item_get_type, ":itp", ":item_no"),
            (eq,":itp",":spy_item_type"),
            (val_add,":num",1),
            (troop_remove_items,":walker_troop_id",":item_no",":num_items"),
         (try_end),
         (store_random_in_range,":random_item",0,":num"),
         (assign,":num",-1),
         (try_for_range,":item_no","itm_horse_meat","itm_one_handed_war_axe_a"),
            (store_item_kind_count,":num_items",":item_no",":original_walker"),
            (ge,":num_items",1),
            (item_get_type, ":itp", ":item_no"),
            (eq,":itp",":spy_item_type"),
            (val_add,":num",1),
            (eq,":num",":random_item"),
            (troop_add_items,":walker_troop_id",":item_no",1),
            (assign,":spy_item",":item_no"),
         (try_end),
         (assign,"$spy_item_worn",":spy_item"),
         (assign,"$spy_quest_troop",":walker_troop_id"),
         (troop_equip_items,":walker_troop_id"),
       (try_end),
#       (store_add, ":troop_slot", slot_center_walker_0_troop, ":walker_no"),
#       (party_set_slot, ":center_no", ":troop_slot", ":walker_troop_id"),
       (store_random_in_range, ":walker_dna", 0, 1000000),
       (store_add, ":dna_slot", slot_center_walker_0_dna, ":walker_no"),
       (party_set_slot, ":center_no", ":dna_slot", ":walker_dna"),
     ]),

  # script_cf_center_get_free_walker
  # Input: arg1 = center_no
  # Output: reg0 = walker no (can fail)
  ("cf_center_get_free_walker",
   [
       (store_script_param, ":center_no", 1),
       (assign, ":num_free_walkers", 0),
       (try_for_range, ":walker_no", 0, num_town_walkers),
         (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
         (party_slot_eq, ":center_no", ":type_slot", walkert_default),
         (val_add, ":num_free_walkers", 1),
       (try_end),
       (gt, ":num_free_walkers", 0),
       (assign, reg0, -1),
       (store_random_in_range, ":random_rank", 0, ":num_free_walkers"),
       (try_for_range, ":walker_no", 0, num_town_walkers),
         (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
         (party_slot_eq, ":center_no", ":type_slot", walkert_default),
         (val_sub, ":num_free_walkers", 1),
         (eq, ":num_free_walkers", ":random_rank"),
         (assign, reg0, ":walker_no"),
       (try_end),
     ]),
    
  # script_center_remove_walker_type_from_walkers
  # Input: arg1 = center_no, arg2 = walker_type, 
  # Output: reg0 = 1 if comment found, 0 otherwise; s61 will contain comment string if found
  ("center_remove_walker_type_from_walkers",
   [
       (store_script_param, ":center_no", 1),
       (store_script_param, ":walker_type", 2),
       (try_for_range, ":walker_no", 0, num_town_walkers),
         (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
         (party_slot_eq, ":center_no", ":type_slot", ":walker_type"),
         (call_script, "script_center_set_walker_to_type", ":center_no", ":walker_no", walkert_default),
       (try_end),
     ]),
  
  # script_init_town_walkers
  ("init_town_walkers",
    [(try_begin),
       (eq, "$town_nighttime", 0),
       (try_for_range, ":walker_no", 0, num_town_walkers),
         (store_add, ":troop_slot", slot_center_walker_0_troop, ":walker_no"),
         (party_get_slot, ":walker_troop_id", "$current_town", ":troop_slot"),
         (gt, ":walker_troop_id", 0),
         (store_add, ":entry_no", town_walker_entries_start, ":walker_no"),
         (set_visitor, ":entry_no", ":walker_troop_id"),
       (try_end),
##       (try_for_range, ":cur_walker", 0, 8),
##         (try_begin),
##           (lt, ":cur_walker", ":num_walkers"),
##           (store_random_in_range, ":walker_troop", town_walkers_begin, town_walkers_end),
##         (else_try),
##           (assign, ":walker_troop", -1),
##         (try_end),
##         (try_begin),
##           (eq, ":cur_walker", 0),
##           (assign, reg0, ":walker_troop"),
##         (else_try),
##           (eq, ":cur_walker", 1),
##           (assign, reg1, ":walker_troop"),
##         (else_try),
##           (eq, ":cur_walker", 2),
##           (assign, reg2, ":walker_troop"),
##         (else_try),
##           (eq, ":cur_walker", 3),
##           (assign, reg3, ":walker_troop"),
##         (else_try),
##           (eq, ":cur_walker", 4),
##           (assign, reg4, ":walker_troop"),
##         (else_try),
##           (eq, ":cur_walker", 5),
##           (assign, reg5, ":walker_troop"),
##         (else_try),
##           (eq, ":cur_walker", 6),
##           (assign, reg6, ":walker_troop"),
##         (else_try),
##           (eq, ":cur_walker", 7),
##           (assign, reg7, ":walker_troop"),
##         (try_end),
##       (try_end),
##       (shuffle_range, 0, 8),
##       (set_visitor, 32, reg0),
##       (set_visitor, 33, reg1),
##       (set_visitor, 34, reg2),
##       (set_visitor, 35, reg3),
##       (set_visitor, 36, reg4),
##       (set_visitor, 37, reg5),
##       (set_visitor, 38, reg6),
##       (set_visitor, 39, reg7),
##     (try_end),
  ]),

  # script_cf_enter_center_location_bandit_check
  ("cf_enter_center_location_bandit_check",
    [
      (neq, "$town_nighttime", 0),
      (party_slot_ge, "$current_town", slot_center_has_bandits, 1),
      (eq, "$g_defending_against_siege", 0),#Skip if the center is under siege (because of resting)
      (eq, "$sneaked_into_town", 0),#Skip if sneaked
      (try_begin),
        (party_slot_eq, "$current_town", slot_party_type, spt_village),
        (party_get_slot, ":cur_scene", "$current_town", slot_castle_exterior),
      (else_try),
        (party_get_slot, ":cur_scene", "$current_town", slot_town_center),
      (try_end),
      (modify_visitors_at_site, ":cur_scene"),
      (reset_visitors),
      (party_get_slot, ":bandit_troop", "$current_town", slot_center_has_bandits),
      (store_character_level, ":level", "trp_player"),

      (set_jump_mission, "mt_bandits_at_night"),
      (try_begin),
        (party_slot_eq, "$current_town", slot_party_type, spt_village),
        (assign, ":spawn_amount", 2),
        (store_div, ":level_fac",  ":level", 10),
        (val_add, ":spawn_amount", ":level_fac"),
        (try_for_range, ":unused", 0, 3),
          (gt, ":level", 10),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", ":level"),
          (val_add, ":spawn_amount", 1),
        (try_end),
        (set_visitors, 4, ":bandit_troop", ":spawn_amount"),
        (assign, "$num_center_bandits", ":spawn_amount"),
        (set_jump_entry, 2),
      (else_try),
        (assign, ":spawn_amount", 1),
        (assign, "$num_center_bandits", 0),
        (try_begin),
          (gt, ":level", 15),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", ":level"),
          (assign, ":spawn_amount", 2),
        (try_end),
        (val_add, "$num_center_bandits",  ":spawn_amount"),
        (set_visitors, 11, ":bandit_troop", ":spawn_amount"),
        (assign, ":spawn_amount", 1),
        (try_begin),
          (gt, ":level", 20),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", ":level"),
          (assign, ":spawn_amount", 2),
        (try_end),
        (set_visitors, 27, ":bandit_troop", ":spawn_amount"),
        (val_add, "$num_center_bandits",  ":spawn_amount"),
        (try_begin),
          (gt, ":level", 9),
          (assign, ":spawn_amount", 1),
          (try_begin),
            (gt, ":level", 25),
            (store_random_in_range, ":random_no", 0, 100),
            (lt, ":random_no", ":level"),
            (assign, ":spawn_amount", 2),
          (try_end),
          (set_visitors, 28, ":bandit_troop", ":spawn_amount"),
          (val_add, "$num_center_bandits",  ":spawn_amount"),
        (try_end),
        (assign, "$town_entered", 1),
        (assign, "$all_doors_locked", 1),
      (try_end),

      (display_message, "@You have run into a trap!", 0xFFFF2222),
      (display_message, "@You are attacked by a group of bandits!", 0xFFFF2222),

      (jump_to_scene, ":cur_scene"),
      (change_screen_mission),
      ]),
  
  # script_init_town_agent
  ("init_town_agent",
    [
      (store_script_param, ":agent_no", 1),
      (agent_get_troop_id, ":troop_no", ":agent_no"),
      (set_fixed_point_multiplier, 100),
      (assign, ":stand_animation", -1),
      (try_begin),
        (this_or_next|is_between, ":troop_no", armor_merchants_begin, armor_merchants_end),
        (is_between, ":troop_no", weapon_merchants_begin, weapon_merchants_end),
        (try_begin),
          (troop_get_type, ":cur_troop_gender", ":troop_no"),
          (eq, ":cur_troop_gender", 0),
          (agent_set_animation, ":agent_no", "anim_stand_townguard"),
        (else_try),
          (agent_set_animation, ":agent_no", "anim_stand_townguard"),
        (end_try),
      (else_try),
        (eq, ":troop_no", "trp_gondor_lord" ),
        (assign, ":stand_animation", "anim_sit_on_trone"), # mtarini: let sire denethor sit.
      (else_try),
        (is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
        (assign, ":stand_animation", "anim_stand_lady"),
      (else_try),
        (is_between, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
        (assign, ":stand_animation", "anim_stand_lord"),
      (else_try),
        (is_between, ":troop_no", soldiers_begin, soldiers_end),
        (assign, ":stand_animation", "anim_stand_townguard"),
      (try_end),
      (try_begin),
        (ge, ":stand_animation", 0),
        (agent_set_stand_animation, ":agent_no", ":stand_animation"),
        (agent_set_animation, ":agent_no", ":stand_animation"),
        (store_random_in_range, ":random_no", 0, 100),
        (agent_set_animation_progress, ":agent_no", ":random_no"),
      (try_end),
      ]),

  # script_init_town_walker_agents
  ("init_town_walker_agents",
    [(assign, ":num_walkers", 0),
     (try_for_agents, ":cur_agent"),
#       (agent_get_troop_id, ":cur_troop", ":cur_agent"),
#       (is_between, ":cur_troop", walkers_begin, walkers_end),
	   (agent_get_entry_no, ":entry", ":cur_agent"),
	   (is_between, ":entry",town_walker_entries_start,40),
       (val_add, ":num_walkers", 1),
       (agent_get_position, pos1, ":cur_agent"),
       (try_for_range, ":i_e_p", 9, 40),#Entry points
         (entry_point_get_position, pos2, ":i_e_p"),
         (get_distance_between_positions, ":distance", pos1, pos2),
         (lt, ":distance", 200),
         (agent_set_slot, ":cur_agent", 0, ":i_e_p"),
       (try_end),
       (call_script, "script_set_town_walker_destination", ":cur_agent"),
     (try_end),
  ]),

  # script_agent_get_town_walker_details
  # This script assumes this is one of town walkers. 
  # Input: agent_id
  # Output: reg0: town_walker_type, reg1: town_walker_dna
  ("agent_get_town_walker_details",
    [(store_script_param, ":agent_no", 1),
     (agent_get_entry_no, ":entry_no", ":agent_no"),
     (store_sub, ":walker_no", ":entry_no", town_walker_entries_start),

     (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
     (party_get_slot, ":walker_type", "$current_town", ":type_slot"),
     (store_add, ":dna_slot", slot_center_walker_0_dna,  ":walker_no"),
     (party_get_slot, ":walker_dna", "$current_town", ":dna_slot"),
     (assign, reg0, ":walker_type"),
     (assign, reg1, ":walker_dna"),
     (assign, reg2, ":walker_no"),
  ]),

  
  # script_tick_town_walkers
  ("tick_town_walkers",
    [(try_for_agents, ":cur_agent"),
#       (agent_get_troop_id, ":cur_troop", ":cur_agent"),
#       (is_between, ":cur_troop", walkers_begin, walkers_end),
       (agent_get_entry_no, ":entry", ":cur_agent"),
	   (is_between, ":entry",town_walker_entries_start,40),
       (agent_get_slot, ":target_entry_point", ":cur_agent", 0),
       (entry_point_get_position, pos1, ":target_entry_point"),
       (try_begin),
         (lt, ":target_entry_point", town_walker_entries_start),
         (init_position, pos2),
         (position_set_y, pos2, 250),
         (position_transform_position_to_parent, pos1, pos1, pos2),
       (try_end),
       (agent_get_position, pos2, ":cur_agent"),
       (get_distance_between_positions, ":distance", pos1, pos2),
       (lt, ":distance", 400),
       (assign, ":random_no", 0),
       (try_begin),
         (lt, ":target_entry_point", town_walker_entries_start),
         (store_random_in_range, ":random_no", 0, 100),
       (try_end),
       (lt, ":random_no", 20),
       (call_script, "script_set_town_walker_destination", ":cur_agent"),
     (try_end),
  ]),

  # script_set_town_walker_destination
  # Input: arg1 = agent_no
  ("set_town_walker_destination",
    [(store_script_param_1, ":agent_no"),
     (assign, reg0, 9),
     (assign, reg1, 10),
     (assign, reg2, 12),
     (assign, reg3, 32),
     (assign, reg4, 33),
     (assign, reg5, 34),
     (assign, reg6, 35),
     (assign, reg7, 36),
     (assign, reg8, 37),
     (assign, reg9, 38),
     (assign, reg10, 39),
     (try_for_agents, ":cur_agent"),
#       (agent_get_troop_id, ":cur_troop", ":cur_agent"),
#       (is_between, ":cur_troop", walkers_begin, walkers_end),
       (agent_get_entry_no, ":entry", ":cur_agent"),
	   (is_between, ":entry",town_walker_entries_start,40),
       (agent_get_slot, ":target_entry_point", ":cur_agent", 0),

       (try_begin),(eq, ":target_entry_point", 9),(assign, reg0, 0),
       (else_try) ,(eq, ":target_entry_point",10),(assign, reg1, 0),
       (else_try) ,(eq, ":target_entry_point",12),(assign, reg2, 0),
       (else_try) ,(eq, ":target_entry_point",32),(assign, reg3, 0),
       (else_try) ,(eq, ":target_entry_point",33),(assign, reg4, 0),
       (else_try) ,(eq, ":target_entry_point",34),(assign, reg5, 0),
       (else_try) ,(eq, ":target_entry_point",35),(assign, reg6, 0),
       (else_try) ,(eq, ":target_entry_point",36),(assign, reg7, 0),
       (else_try) ,(eq, ":target_entry_point",37),(assign, reg8, 0),
       (else_try) ,(eq, ":target_entry_point",38),(assign, reg9, 0),
       (else_try) ,(eq, ":target_entry_point",39),(assign,reg10, 0),
       (try_end),
     (try_end),
     (assign, ":try_limit", 100),
     (assign, ":target_entry_point", 0),
     (try_for_range, ":unused", 0, ":try_limit"),
       (shuffle_range, 0, 11),
       (gt, reg0, 0),
       (assign, ":target_entry_point", reg0),
       (assign, ":try_limit", 0),
     (try_end),
     (try_begin),
       (gt, ":target_entry_point", 0),
       (agent_set_slot, ":agent_no", 0, ":target_entry_point"),
       (entry_point_get_position, pos1, ":target_entry_point"),
       (try_begin),
         (lt, ":target_entry_point", town_walker_entries_start),
         (init_position, pos2),
         (position_set_y, pos2, 250),
         (position_transform_position_to_parent, pos1, pos1, pos2),
       (try_end),
       (agent_set_scripted_destination, ":agent_no", pos1, 0),
       (agent_set_speed_limit, ":agent_no", 5),
     (try_end),
  ]),

  # script_town_init_doors
  # Input: door_state (-1 = closed, 1 = open, 0 = use $town_nighttime)
  # Output: none (required for siege mission templates)
  ("town_init_doors",
   [(store_script_param, ":door_state", 1),
    (try_begin),
      (assign, ":continue", 0),
      (try_begin),
        (eq, ":door_state", 1),
        (assign, ":continue", 1),
      (else_try),
        (eq, ":door_state", 0),
        (eq, "$town_nighttime", 0),
        (assign, ":continue", 1),
      (try_end),
      (eq, ":continue", 1),# open doors
      (assign, ":end_cond", 1),
      (try_for_range, ":i_instance", 0, ":end_cond"),
        (scene_prop_get_instance, ":object", "spr_towngate_door_left", ":i_instance"),
        (ge, ":object", 0),
        (val_add, ":end_cond", 1),
        (prop_instance_get_position, pos1, ":object"),
        (position_rotate_z, pos1, -100),
        (prop_instance_animate_to_position, ":object", pos1, 1),
      (try_end),
      (assign, ":end_cond", 1),
      (try_for_range, ":i_instance", 0, ":end_cond"),
        (scene_prop_get_instance, ":object", "spr_towngate_rectangle_door_left", ":i_instance"),
        (ge, ":object", 0),
        (val_add, ":end_cond", 1),
        (prop_instance_get_position, pos1, ":object"),
        (position_rotate_z, pos1, -80),
        (prop_instance_animate_to_position, ":object", pos1, 1),
      (try_end),
      (assign, ":end_cond", 1),
      (try_for_range, ":i_instance", 0, ":end_cond"),
        (scene_prop_get_instance, ":object", "spr_towngate_door_right", ":i_instance"),
        (ge, ":object", 0),
        (val_add, ":end_cond", 1),
        (prop_instance_get_position, pos1, ":object"),
        (position_rotate_z, pos1, 100),
        (prop_instance_animate_to_position, ":object", pos1, 1),
      (try_end),
      (assign, ":end_cond", 1),
      (try_for_range, ":i_instance", 0, ":end_cond"),
        (scene_prop_get_instance, ":object", "spr_towngate_rectangle_door_right", ":i_instance"),
        (ge, ":object", 0),
        (val_add, ":end_cond", 1),
        (prop_instance_get_position, pos1, ":object"),
        (position_rotate_z, pos1, 80),
        (prop_instance_animate_to_position, ":object", pos1, 1),
      (try_end),
    (try_end),
  ]),

  # script_siege_init_ai_and_belfry
  # Output: none (required for siege mission templates)
  ("siege_init_ai_and_belfry",
   [(assign, "$cur_belfry_pos", 50),
    (assign, ":cur_belfry_object_pos", slot_scene_belfry_props_begin),
    (store_current_scene, ":cur_scene"),
    #Collecting belfry objects
    (try_for_range, ":i_belfry_instance", 0, 3),
      (scene_prop_get_instance, ":belfry_object", "spr_belfry_a", ":i_belfry_instance"),
      (ge, ":belfry_object", 0),
      (scene_set_slot, ":cur_scene", ":cur_belfry_object_pos", ":belfry_object"),
      (val_add, ":cur_belfry_object_pos", 1),
    (try_end),
    (try_for_range, ":i_belfry_instance", 0, 3),
      (scene_prop_get_instance, ":belfry_object", "spr_belfry_platform_a", ":i_belfry_instance"),
      (ge, ":belfry_object", 0),
      (scene_set_slot, ":cur_scene", ":cur_belfry_object_pos", ":belfry_object"),
      (val_add, ":cur_belfry_object_pos", 1),
    (try_end),
    (try_for_range, ":i_belfry_instance", 0, 3),
      (scene_prop_get_instance, ":belfry_object", "spr_belfry_platform_b", ":i_belfry_instance"),
      (ge, ":belfry_object", 0),
      (scene_set_slot, ":cur_scene", ":cur_belfry_object_pos", ":belfry_object"),
      (val_add, ":cur_belfry_object_pos", 1),
    (try_end),
    (assign, "$belfry_rotating_objects_begin", ":cur_belfry_object_pos"),
    (try_for_range, ":i_belfry_instance", 0, 5),
      (scene_prop_get_instance, ":belfry_object", "spr_belfry_wheel", ":i_belfry_instance"),
      (ge, ":belfry_object", 0),
      (scene_set_slot, ":cur_scene", ":cur_belfry_object_pos", ":belfry_object"),
      (val_add, ":cur_belfry_object_pos", 1),
    (try_end),
    (assign, "$last_belfry_object_pos", ":cur_belfry_object_pos"),

    #Lifting up the platform  at the beginning
    (scene_prop_get_instance, ":belfry_object_to_rotate", "spr_belfry_platform_a", 0),
    
    #Moving the belfry objects to their starting position
    (entry_point_get_position,pos1,55),
    (entry_point_get_position,pos3,50),
    (try_for_range, ":i_belfry_object_pos", slot_scene_belfry_props_begin, "$last_belfry_object_pos"),
      (assign, ":pos_no", pos_belfry_begin),
      (val_add, ":pos_no", ":i_belfry_object_pos"),
      (val_sub, ":pos_no", slot_scene_belfry_props_begin),
      (scene_get_slot, ":cur_belfry_object", ":cur_scene", ":i_belfry_object_pos"),
      (prop_instance_get_position, pos2, ":cur_belfry_object"),
      (try_begin),
        (eq, ":cur_belfry_object", ":belfry_object_to_rotate"),
        (position_rotate_x, pos2, 90),
      (try_end),
      (position_transform_position_to_local, ":pos_no", pos1, pos2),
      (position_transform_position_to_parent, pos4, pos3, ":pos_no"),
      (prop_instance_animate_to_position, ":cur_belfry_object", pos4, 1),
    (try_end),
    (assign, "$belfry_positioned", 0),
    (assign, "$belfry_num_slots_positioned", 0),
    (assign, "$belfry_num_men_pushing", 0),
  ]),

  # script_cf_siege_move_belfry
  # Output: none (required for siege mission templates)
  ("cf_siege_move_belfry",
   [(neq, "$last_belfry_object_pos", slot_scene_belfry_props_begin),
    (entry_point_get_position,pos1,50),
    (entry_point_get_position,pos4,55),
    (get_distance_between_positions, ":total_distance", pos4, pos1),
    (store_current_scene, ":cur_scene"),
    (scene_get_slot, ":first_belfry_object", ":cur_scene", slot_scene_belfry_props_begin),
    (prop_instance_get_position, pos2, ":first_belfry_object"),
    (entry_point_get_position,pos1,"$cur_belfry_pos"),
    (position_transform_position_to_parent, pos3, pos1, pos_belfry_begin),
    (position_transform_position_to_parent, pos5, pos4, pos_belfry_begin),
    (get_distance_between_positions, ":cur_distance", pos2, pos3),
    (get_distance_between_positions, ":distance_left", pos2, pos5),
    (try_begin),
      (le, ":cur_distance", 10),
      (val_add, "$cur_belfry_pos", 1),
      (entry_point_get_position,pos1,"$cur_belfry_pos"),
      (position_transform_position_to_parent, pos3, pos1, pos_belfry_begin),
      (get_distance_between_positions, ":cur_distance", pos2, pos3),
    (try_end),
    (neq, "$cur_belfry_pos", 50),

    (assign, ":base_speed", 20),
    (store_div, ":slow_range", ":total_distance", 60),
    (store_sub, ":distance_moved", ":total_distance", ":distance_left"),

    (try_begin),
      (lt, ":distance_moved", ":slow_range"),
      (store_mul, ":base_speed", ":distance_moved", -60),
      (val_div, ":base_speed", ":slow_range"),
      (val_add, ":base_speed", 80),
    (else_try),
      (lt, ":distance_left", ":slow_range"),
      (store_mul, ":base_speed", ":distance_left", -60),
      (val_div, ":base_speed", ":slow_range"),
      (val_add, ":base_speed", 80),
    (try_end),
    (store_mul, ":belfry_speed", ":cur_distance", ":base_speed"),
    (try_begin),
      (eq, "$belfry_num_men_pushing", 0),
      (assign, ":belfry_speed", 1000000),
    (else_try),
      (val_div, ":belfry_speed", "$belfry_num_men_pushing"),
    (try_end),

    (try_begin),
      (le, "$cur_belfry_pos", 55),
      (init_position, pos3),
      (position_rotate_x, pos3, ":distance_moved"),
      (scene_get_slot, ":base_belfry_object", ":cur_scene", slot_scene_belfry_props_begin),
      (prop_instance_get_position, pos4, ":base_belfry_object"),
      (entry_point_get_position,pos1,"$cur_belfry_pos"),
      (try_for_range, ":i_belfry_object_pos", slot_scene_belfry_props_begin, "$last_belfry_object_pos"),
        (scene_get_slot, ":cur_belfry_object", ":cur_scene", ":i_belfry_object_pos"),
        (try_begin),
          (ge, ":i_belfry_object_pos", "$belfry_rotating_objects_begin"),
          (prop_instance_get_starting_position, pos5, ":base_belfry_object"),
          (prop_instance_get_starting_position, pos6, ":cur_belfry_object"),
          (position_transform_position_to_local, pos7, pos5, pos6),
          (position_transform_position_to_parent, pos5, pos4, pos7),
          (position_transform_position_to_parent, pos6, pos5, pos3),
          (prop_instance_set_position, ":cur_belfry_object", pos6),
        (else_try),
          (assign, ":pos_no", pos_belfry_begin),
          (val_add, ":pos_no", ":i_belfry_object_pos"),
          (val_sub, ":pos_no", slot_scene_belfry_props_begin),
          (position_transform_position_to_parent, pos2, pos1, ":pos_no"),
          (prop_instance_animate_to_position, ":cur_belfry_object", pos2, ":belfry_speed"),
        (try_end),
      (try_end),
    (try_end),
    (gt, "$cur_belfry_pos", 55),
    (assign, "$belfry_positioned", 1),
  ]),

  # script_cf_siege_rotate_belfry_platform
  # Input: none
  # Output: none (required for siege mission templates)
  ("cf_siege_rotate_belfry_platform",
   [(eq, "$belfry_positioned", 1),
    (scene_prop_get_instance, ":belfry_object", "spr_belfry_platform_a", 0),
    (prop_instance_get_position, pos1, ":belfry_object"),
    (position_rotate_x, pos1, -90),
    (prop_instance_animate_to_position, ":belfry_object", pos1, 400),
    (assign, "$belfry_positioned", 2),
  ]),

  # script_cf_siege_assign_men_to_belfry
  # Output: none (required for siege mission templates)
  ("cf_siege_assign_men_to_belfry",
   [
    (store_mission_timer_a, ":cur_seconds"),
    (neq, "$last_belfry_object_pos", slot_scene_belfry_props_begin),
    (assign, ":end_trigger", 0),
    (try_begin),
      (lt, "$belfry_positioned", 3),
      (get_player_agent_no, ":player_agent"),
      (store_current_scene, ":cur_scene"),
      (scene_get_slot, ":first_belfry_object", ":cur_scene", slot_scene_belfry_props_begin),
      (prop_instance_get_position, pos2, ":first_belfry_object"),
      (assign, ":slot_1_positioned", 0),
      (assign, ":slot_2_positioned", 0),
      (assign, ":slot_3_positioned", 0),
      (assign, ":slot_4_positioned", 0),
      (assign, ":slot_5_positioned", 0),
      (assign, ":slot_6_positioned", 0),
      (assign, "$belfry_num_slots_positioned", 0),
      (assign, "$belfry_num_men_pushing", 0),
      (try_for_agents, ":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (try_begin),
          (agent_get_slot, ":x_pos", ":cur_agent", slot_agent_target_x_pos),
          (neq, ":x_pos", 0),
          (agent_get_slot, ":y_pos", ":cur_agent", slot_agent_target_y_pos),
          (try_begin),
            (eq, ":x_pos", -600),
            (try_begin),
              (eq, ":y_pos", 0),
              (assign, ":slot_1_positioned", 1),
            (else_try),
              (eq, ":y_pos", -200),
              (assign, ":slot_2_positioned", 1),
            (else_try),
              (assign, ":slot_3_positioned", 1),
            (try_end),
          (else_try),
            (try_begin),
              (eq, ":y_pos", 0),
              (assign, ":slot_4_positioned", 1),
            (else_try),
              (eq, ":y_pos", -200),
              (assign, ":slot_5_positioned", 1),
            (else_try),
              (assign, ":slot_6_positioned", 1),
            (try_end),
          (try_end),
          (val_add, "$belfry_num_slots_positioned", 1),
          (init_position, pos1),
          (position_move_x, pos1, ":x_pos"),
          (position_move_y, pos1, ":y_pos"),
          (init_position, pos3),
          (position_move_x, pos3, ":x_pos"),
          (position_move_y, pos3, -1000),
          (position_transform_position_to_parent, pos4, pos2, pos1),
          (position_transform_position_to_parent, pos5, pos2, pos3),
          (agent_get_position, pos6, ":cur_agent"),
          (get_distance_between_positions, ":target_distance", pos6, pos4),
          (get_distance_between_positions, ":waypoint_distance", pos6, pos5),
          (try_begin),
            (this_or_next|lt, ":target_distance", ":waypoint_distance"),
            (lt, ":waypoint_distance", 600),
            (agent_set_scripted_destination, ":cur_agent", pos4, 1),
          (else_try),
            (agent_set_scripted_destination, ":cur_agent", pos5, 1),
          (try_end),
          (try_begin),
            (le, ":target_distance", 300),
            (val_add, "$belfry_num_men_pushing", 1),
          (try_end),
        (else_try),
          (agent_get_team, ":cur_agent_team", ":cur_agent"),
          (this_or_next|eq, "$attacker_team", ":cur_agent_team"),
          (             eq, "$attacker_team_2", ":cur_agent_team"),
          (try_begin),
            (gt, ":cur_seconds", 20),
            (agent_get_position, pos1, ":cur_agent"),
            (agent_set_scripted_destination, ":cur_agent", pos1, 0),
          (else_try),
            (try_begin),
              (team_get_movement_order, ":order1", "$attacker_team", grc_infantry),
              (team_get_movement_order, ":order2", "$attacker_team", grc_cavalry),
              (team_get_movement_order, ":order3", "$attacker_team", grc_archers),
              (this_or_next|neq, ":order1", mordr_stand_ground),
              (this_or_next|neq, ":order2", mordr_stand_ground),
              (neq, ":order3", mordr_stand_ground),
              (set_show_messages, 0),
              (team_give_order, "$attacker_team", grc_everyone, mordr_stand_ground),
              (set_show_messages, 1),
            (try_end),
          (try_end),
        (try_end),
      (try_end),
      (try_begin),
        (lt, "$belfry_num_slots_positioned", 6),
        (try_for_agents, ":cur_agent"),
          (agent_is_alive, ":cur_agent"),
          (agent_get_team, ":cur_agent_team", ":cur_agent"),
          (this_or_next|eq, "$attacker_team", ":cur_agent_team"),
          (             eq, "$attacker_team_2", ":cur_agent_team"),
          (neq, ":player_agent", ":cur_agent"),
          (agent_get_class, ":agent_class", ":cur_agent"),
          (this_or_next|eq, ":agent_class", grc_infantry),
          (eq, ":agent_class", grc_cavalry),
          (agent_get_slot, ":x_pos", ":cur_agent", 1),
          (eq, ":x_pos", 0),
          (assign, ":y_pos", 0),
          (try_begin),
            (eq, ":slot_1_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", 0),
            (val_add, ":slot_1_positioned", 1),
          (else_try),
            (eq, ":slot_2_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", -200),
            (val_add, ":slot_2_positioned", 1),
          (else_try),
            (eq, ":slot_3_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", -400),
            (val_add, ":slot_3_positioned", 1),
          (else_try),
            (eq, ":slot_4_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", 0),
            (val_add, ":slot_4_positioned", 1),
          (else_try),
            (eq, ":slot_5_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", -200),
            (val_add, ":slot_5_positioned", 1),
          (else_try),
            (eq, ":slot_6_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", -400),
            (val_add, ":slot_6_positioned", 1),
          (try_end),
          (val_add, "$belfry_num_slots_positioned", 1),
          (agent_set_slot, ":cur_agent", 1, ":x_pos"),
          (agent_set_slot, ":cur_agent", 2, ":y_pos"),
        (try_end),
      (try_end),
      (try_begin),
        (store_mission_timer_a, ":cur_timer"),
        (gt, ":cur_timer", 20),
        (lt, "$belfry_num_slots_positioned", 6),
        (try_for_agents, ":cur_agent"),
          (agent_is_alive, ":cur_agent"),
          (agent_get_team, ":cur_agent_team", ":cur_agent"),
          (this_or_next|eq, "$attacker_team", ":cur_agent_team"),
          (             eq, "$attacker_team_2", ":cur_agent_team"),
          (neq, ":player_agent", ":cur_agent"),
          (agent_get_slot, ":x_pos", ":cur_agent", 1),
          (eq, ":x_pos", 0),
          (assign, ":y_pos", 0),
          (try_begin),
            (eq, ":slot_1_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", 0),
            (val_add, ":slot_1_positioned", 1),
          (else_try),
            (eq, ":slot_2_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", -200),
            (val_add, ":slot_2_positioned", 1),
          (else_try),
            (eq, ":slot_3_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", -400),
            (val_add, ":slot_3_positioned", 1),
          (else_try),
            (eq, ":slot_4_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", 0),
            (val_add, ":slot_4_positioned", 1),
          (else_try),
            (eq, ":slot_5_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", -200),
            (val_add, ":slot_5_positioned", 1),
          (else_try),
            (eq, ":slot_6_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", -400),
            (val_add, ":slot_6_positioned", 1),
          (try_end),
          (val_add, "$belfry_num_slots_positioned", 1),
          (agent_set_slot, ":cur_agent", 1, ":x_pos"),
          (agent_set_slot, ":cur_agent", 2, ":y_pos"),
        (try_end),
      (try_end),
    (else_try),
      (assign, ":end_trigger", 1),
      (try_for_agents, ":cur_agent"),
        (agent_clear_scripted_mode, ":cur_agent"),
      (try_end),
      (set_show_messages, 0),
      (team_give_order, "$attacker_team", grc_everyone, mordr_charge),
      (set_show_messages, 1),
    (try_end),
    (eq, ":end_trigger", 1),
  ]),

  # script_siege_move_archers_to_archer_positions
  ("siege_move_archers_to_archer_positions",
   [
     (try_for_agents, ":agent_no"),
       (agent_is_alive, ":agent_no"),
       (agent_slot_eq, ":agent_no", slot_agent_is_not_reinforcement, 0),
       (agent_is_defender, ":agent_no"),
       (agent_get_class, ":agent_class", ":agent_no"),
       (agent_get_troop_id, ":agent_troop", ":agent_no"),
       (eq, ":agent_class", grc_archers),
       (try_begin),
         (agent_slot_eq, ":agent_no", slot_agent_target_entry_point, 0),
         (store_random_in_range, ":random_entry_point", 40, 44),
         (agent_set_slot, ":agent_no", slot_agent_target_entry_point, ":random_entry_point"),
       (try_end),
       (try_begin),
         (agent_get_position, pos0, ":agent_no"),
         (entry_point_get_position, pos1, ":random_entry_point"),
         (get_distance_between_positions, ":dist", pos0, pos1),
         (lt, ":dist", 300),
         (agent_clear_scripted_mode, ":agent_no"),
         (agent_set_slot, ":agent_no", slot_agent_is_in_scripted_mode, 0),
         (agent_set_slot, ":agent_no", slot_agent_is_not_reinforcement, 1),
         (str_store_troop_name, s1, ":agent_troop"),
         (assign, reg0, ":agent_no"),
#         (display_message, "@{s1} ({reg0}) reached pos"),
       (else_try),
         (agent_get_simple_behavior, ":agent_sb", ":agent_no"),
         (agent_get_combat_state, ":agent_cs", ":agent_no"),
         (this_or_next|eq, ":agent_sb", aisb_ranged),
         (eq, ":agent_sb", aisb_go_to_pos),#scripted mode
         (eq, ":agent_cs", 7), # 7 = no visible targets (state for ranged units)
         (try_begin),
           (agent_slot_eq, ":agent_no", slot_agent_is_in_scripted_mode, 0),
           (agent_set_scripted_destination, ":agent_no", pos1, 0),
           (agent_set_slot, ":agent_no", slot_agent_is_in_scripted_mode, 1),
           (str_store_troop_name, s1, ":agent_troop"),
           (assign, reg0, ":agent_no"),
#           (display_message, "@{s1} ({reg0}) moving to pos"),
         (try_end),
       (else_try),
         (try_begin),
           (agent_slot_eq, ":agent_no", slot_agent_is_in_scripted_mode, 1),
           (agent_clear_scripted_mode, ":agent_no"),
           (agent_set_slot, ":agent_no", slot_agent_is_in_scripted_mode, 0),
           (str_store_troop_name, s1, ":agent_troop"),
           (assign, reg0, ":agent_no"),
#           (display_message, "@{s1} ({reg0}) seeing target or changed mode"),
         (try_end),
       (try_end),
     (try_end),
     ]),

  # script_store_movement_order_name_to_s1
  # Input: arg1 = team_no, arg2 = class_no
  # Output: s1 = order_name
  ("store_movement_order_name_to_s1",
   [(store_script_param_1, ":team_no"),
    (store_script_param_2, ":class_no"),
    (team_get_movement_order, ":cur_order", ":team_no", ":class_no"),

    (try_begin),(eq, ":cur_order", mordr_hold        ),(str_store_string, s1, "@Holding"),
    (else_try) ,(eq, ":cur_order", mordr_follow      ),(str_store_string, s1, "@Following"),
    (else_try) ,(eq, ":cur_order", mordr_charge      ),(str_store_string, s1, "@Charging"),
    (else_try) ,(eq, ":cur_order", mordr_advance     ),(str_store_string, s1, "@Advancing"),
    (else_try) ,(eq, ":cur_order", mordr_fall_back   ),(str_store_string, s1, "@Falling Back"),
    (else_try) ,(eq, ":cur_order", mordr_stand_closer),(str_store_string, s1, "@Standing Closer"),
    (else_try) ,(eq, ":cur_order", mordr_spread_out  ),(str_store_string, s1, "@Spreading Out"),
    (else_try) ,(eq, ":cur_order", mordr_stand_ground),(str_store_string, s1, "@Standing"),
    (else_try) ,                                       (str_store_string, s1, "@N/A"),
    (try_end),
  ]),

  # script_store_riding_order_name_to_s1
  # Input: arg1 = team_no, arg2 = class_no
  # Output: s1 = order_name
  ("store_riding_order_name_to_s1",
   [(store_script_param_1, ":team_no"),
    (store_script_param_2, ":class_no"),
    (team_get_riding_order, ":cur_order", ":team_no", ":class_no"),
    (try_begin),
      (eq, ":cur_order", rordr_free),
      (str_store_string, s1, "@Free"),
    (else_try),
      (eq, ":cur_order", rordr_mount),
      (str_store_string, s1, "@Mount"),
    (else_try),
      (eq, ":cur_order", rordr_dismount),
      (str_store_string, s1, "@Dismount"),
    (else_try),
      (str_store_string, s1, "@N/A"),
    (try_end),
  ]),

  # script_store_weapon_usage_order_name_to_s1
  # Input: arg1 = team_no, arg2 = class_no
  # Output: s1 = order_name
  ("store_weapon_usage_order_name_to_s1",
   [(store_script_param_1, ":team_no"),
    (store_script_param_2, ":class_no"),
    (team_get_weapon_usage_order, ":cur_order", ":team_no", ":class_no"),
    (team_get_hold_fire_order, ":cur_hold_fire", ":team_no", ":class_no"),
    (try_begin),
      (eq, ":cur_order", wordr_use_any_weapon),
      (eq, ":cur_hold_fire", aordr_fire_at_will),
      (str_store_string, s1, "@Any Weapon"),
    (else_try),
      (eq, ":cur_order", wordr_use_blunt_weapons),
      (eq, ":cur_hold_fire", aordr_fire_at_will),
      (str_store_string, s1, "@Blunt Weapons"),
    (else_try),
      (eq, ":cur_order", wordr_use_any_weapon),
      (eq, ":cur_hold_fire", aordr_hold_your_fire),
      (str_store_string, s1, "str_hold_fire"),
    (else_try),
      (eq, ":cur_order", wordr_use_blunt_weapons),
      (eq, ":cur_hold_fire", aordr_hold_your_fire),
      (str_store_string, s1, "str_blunt_hold_fire"),
    (else_try),
      (str_store_string, s1, "@N/A"),
    (try_end),
  ]),

  # script_team_give_order_from_order_panel
  # Input: arg1 = leader_agent_no, arg2 = class_no
  # Output: none
  ("team_give_order_from_order_panel",
   [(store_script_param_1, ":leader_agent_no"),
    (store_script_param_2, ":order"),
    (agent_get_team, ":team_no", ":leader_agent_no"),
    (set_show_messages, 0),
    (try_begin),
      (eq, "$g_formation_infantry_selected", 1),
      (team_give_order, ":team_no", grc_infantry, ":order"),
    (try_end),
    (try_begin),
      (eq, "$g_formation_archers_selected", 1),
      (team_give_order, ":team_no", grc_archers, ":order"),
    (try_end),
    (try_begin),
      (eq, "$g_formation_cavalry_selected", 1),
      (team_give_order, ":team_no", grc_cavalry, ":order"),
    (try_end),

    (try_begin),
      (eq, ":order", mordr_hold),
      (agent_get_position, pos1, ":leader_agent_no"),
      (try_begin),
        (eq, "$g_formation_infantry_selected", 1),
        (team_set_order_position, ":team_no", grc_infantry, pos1),
      (try_end),
      (try_begin),
        (eq, "$g_formation_archers_selected", 1),
        (team_set_order_position, ":team_no", grc_archers, pos1),
      (try_end),
      (try_begin),
        (eq, "$g_formation_cavalry_selected", 1),
        (team_set_order_position, ":team_no", grc_cavalry, pos1),
      (try_end),
    (try_end),
    (set_show_messages, 1),
  ]),  


  # script_update_order_panel
  # Input: arg1 = team_no
  # Output: none
  ("update_order_panel",
   [(store_script_param_1, ":team_no"),
    (set_fixed_point_multiplier, 1000),

    (assign, ":old_is_infantry_listening", 0),
    (try_begin),
      (class_is_listening_order, ":team_no", grc_infantry),
      (assign, ":old_is_infantry_listening", 1),
    (try_end),
    (assign, ":old_is_archers_listening", 0),
    (try_begin),
      (class_is_listening_order, ":team_no", grc_archers),
      (assign, ":old_is_archers_listening", 1),
    (try_end),
    (assign, ":old_is_cavalry_listening", 0),
    (try_begin),
      (class_is_listening_order, ":team_no", grc_cavalry),
      (assign, ":old_is_cavalry_listening", 1),
    (try_end),

    (call_script, "script_store_movement_order_name_to_s1", ":team_no", grc_infantry),
    (overlay_set_text, "$g_presentation_infantry_movement", s1),
    (call_script, "script_store_riding_order_name_to_s1", ":team_no", grc_infantry),
    (overlay_set_text, "$g_presentation_infantry_riding", s1),
    (call_script, "script_store_weapon_usage_order_name_to_s1", ":team_no", grc_infantry),
    (overlay_set_text, "$g_presentation_infantry_weapon_usage", s1),
    (call_script, "script_store_movement_order_name_to_s1", ":team_no", grc_archers),
    (overlay_set_text, "$g_presentation_archers_movement", s1),
    (call_script, "script_store_riding_order_name_to_s1", ":team_no", grc_archers),
    (overlay_set_text, "$g_presentation_archers_riding", s1),
    (call_script, "script_store_weapon_usage_order_name_to_s1", ":team_no", grc_archers),
    (overlay_set_text, "$g_presentation_archers_weapon_usage", s1),
    (call_script, "script_store_movement_order_name_to_s1", ":team_no", grc_cavalry),
    (overlay_set_text, "$g_presentation_cavalry_movement", s1),
    (call_script, "script_store_riding_order_name_to_s1", ":team_no", grc_cavalry),
    (overlay_set_text, "$g_presentation_cavalry_riding", s1),
    (call_script, "script_store_weapon_usage_order_name_to_s1", ":team_no", grc_cavalry),
    (overlay_set_text, "$g_presentation_cavalry_weapon_usage", s1),

    (try_begin),
      (eq, ":old_is_infantry_listening", 1),
      (eq, ":old_is_archers_listening", 1),
      (eq, ":old_is_cavalry_listening", 1),
      (team_set_order_listener, ":team_no", grc_everyone),
    (else_try),
      (eq, ":old_is_infantry_listening", 1),
      (team_set_order_listener, ":team_no", grc_infantry),
    (else_try),
      (eq, ":old_is_archers_listening", 1),
      (team_set_order_listener, ":team_no", grc_archers),
    (else_try),
      (eq, ":old_is_cavalry_listening", 1),
      (team_set_order_listener, ":team_no", grc_cavalry),
    (try_end),

    (position_set_y, pos1, 660),
    (position_set_x, pos1, 250),
    (overlay_set_position, "$g_presentation_infantry_movement", pos1),
    (position_set_x, pos1, 400),
    (overlay_set_position, "$g_presentation_infantry_riding", pos1),
    (position_set_x, pos1, 550),
    (overlay_set_position, "$g_presentation_infantry_weapon_usage", pos1),

    (position_set_y, pos1, 620),
    (position_set_x, pos1, 250),
    (overlay_set_position, "$g_presentation_archers_movement", pos1),
    (position_set_x, pos1, 400),
    (overlay_set_position, "$g_presentation_archers_riding", pos1),
    (position_set_x, pos1, 550),
    (overlay_set_position, "$g_presentation_archers_weapon_usage", pos1),

    (position_set_y, pos1, 580),
    (position_set_x, pos1, 250),
    (overlay_set_position, "$g_presentation_cavalry_movement", pos1),
    (position_set_x, pos1, 400),
    (overlay_set_position, "$g_presentation_cavalry_riding", pos1),
    (position_set_x, pos1, 550),
    (overlay_set_position, "$g_presentation_cavalry_weapon_usage", pos1),
  ]),


  # script_update_agent_position_on_map
  # Input: arg1 = agent_no, pos2 = map_size_pos
  # Output: none
  ("update_agent_position_on_map",
   [(store_script_param_1, ":agent_no"),
    (agent_get_slot, ":agent_overlay", ":agent_no", slot_agent_map_overlay_id),

    (get_player_agent_no, ":player_agent"),
    (try_begin),
      (le, ":agent_overlay", 0),
      (set_fixed_point_multiplier, 1000),
      (try_begin),
        (eq, ":agent_no", ":player_agent"),
        (create_mesh_overlay, reg1, "mesh_player_dot"),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 500),
        (overlay_set_size, reg1, pos1),
      (else_try),
        (create_mesh_overlay, reg1, "mesh_white_dot"),
        (position_set_x, pos1, 200),
        (position_set_y, pos1, 200),
        (overlay_set_size, reg1, pos1),
      (try_end),
      (overlay_set_alpha, reg1, 0x88),
      (agent_set_slot, ":agent_no", slot_agent_map_overlay_id, reg1),
      (assign, ":agent_overlay", reg1),
    (try_end),

    (try_begin),
      (neq, ":agent_no", ":player_agent"),
      (agent_get_party_id, ":agent_party", ":agent_no"),
      (try_begin),
        (eq, ":agent_party", "p_main_party"),
        (agent_get_class, ":agent_class", ":agent_no"),
        (try_begin),
          (eq, ":agent_class", grc_archers),
          (overlay_set_color, ":agent_overlay", 0x34c6e4),
        (else_try),
          (eq, ":agent_class", grc_cavalry),
          (overlay_set_color, ":agent_overlay", 0x569619),
       (else_try),
          #grc_infantry
          (overlay_set_color, ":agent_overlay", 0x8d5220),
        (try_end),
      (else_try),
        (agent_is_ally, ":agent_no"),
        (overlay_set_color, ":agent_overlay", 0x5555FF),
      (else_try),
        (overlay_set_color, ":agent_overlay", 0xFF0000),
      (try_end),
    (try_end),

    (try_begin),
      (eq, ":agent_no", ":player_agent"),
      (agent_get_look_position, pos1, ":agent_no"),
      (position_get_rotation_around_z, ":rot", pos1),
      (init_position, pos10),
      (position_rotate_z, pos10, ":rot"),
      (overlay_set_mesh_rotation, ":agent_overlay", pos10),
      (call_script, "script_convert_3d_pos_to_map_pos"),
    (else_try),
      (agent_get_position, pos1, ":agent_no"),
      (call_script, "script_convert_3d_pos_to_map_pos"),
    (try_end),
    (overlay_set_position, ":agent_overlay", pos0),
  ]),

  # script_convert_3d_pos_to_map_pos
  # Input: pos1 = 3d_pos, pos2 = map_size_pos
  # Output: pos0 = map_pos
  ("convert_3d_pos_to_map_pos",
   [(set_fixed_point_multiplier, 1000),
    (position_transform_position_to_local, pos3, pos2, pos1),
    (position_get_x, ":agent_x_pos", pos3),
    (position_get_y, ":agent_y_pos", pos3),
    (val_div, ":agent_x_pos", "$g_battle_map_scale"),
    (val_div, ":agent_y_pos", "$g_battle_map_scale"),
    (set_fixed_point_multiplier, 1000),
    (store_sub, ":map_x", 980, "$g_battle_map_width"),
    (store_sub, ":map_y", 730, "$g_battle_map_height"),
    (val_add, ":agent_x_pos", ":map_x"),
    (val_add, ":agent_y_pos", ":map_y"),
    (position_set_x, pos0, ":agent_x_pos"),
    (position_set_y, pos0, ":agent_y_pos"),
  ]),

  # script_update_order_flags_on_map
  # Input: none
  # Output: none
  ("update_order_flags_on_map",
   [(set_fixed_point_multiplier, 1000),
    (get_player_agent_no, ":player_agent"),
    (agent_get_team, ":player_team", ":player_agent"),

    (assign, ":old_is_infantry_listening", 0),
    (try_begin),
      (class_is_listening_order, ":player_team", grc_infantry),
      (assign, ":old_is_infantry_listening", 1),
    (try_end),
    (assign, ":old_is_archers_listening", 0),
    (try_begin),
      (class_is_listening_order, ":player_team", grc_archers),
      (assign, ":old_is_archers_listening", 1),
    (try_end),
    (assign, ":old_is_cavalry_listening", 0),
    (try_begin),
      (class_is_listening_order, ":player_team", grc_cavalry),
      (assign, ":old_is_cavalry_listening", 1),
    (try_end),

    (get_scene_boundaries, pos2, pos3),

    (team_get_movement_order, ":cur_order", ":player_team", grc_infantry),
    (try_begin),
      (eq, ":cur_order", mordr_hold),
      (team_get_order_position, pos1, ":player_team", grc_infantry),
      (call_script, "script_convert_3d_pos_to_map_pos"),
      (overlay_set_alpha, "$g_battle_map_infantry_order_flag", 0xFF),
      (overlay_set_position, "$g_battle_map_infantry_order_flag", pos0),
    (else_try),
      (overlay_set_alpha, "$g_battle_map_infantry_order_flag", 0),
    (try_end),
    (team_get_movement_order, ":cur_order", ":player_team", grc_archers),
    (try_begin),
      (eq, ":cur_order", mordr_hold),
      (team_get_order_position, pos1, ":player_team", grc_archers),
      (call_script, "script_convert_3d_pos_to_map_pos"),
      (overlay_set_alpha, "$g_battle_map_archers_order_flag", 0xFF),
      (overlay_set_position, "$g_battle_map_archers_order_flag", pos0),
    (else_try),
      (overlay_set_alpha, "$g_battle_map_archers_order_flag", 0),
    (try_end),
    (team_get_movement_order, ":cur_order", ":player_team", grc_cavalry),
    (try_begin),
      (eq, ":cur_order", mordr_hold),
      (team_get_order_position, pos1, ":player_team", grc_cavalry),
      (call_script, "script_convert_3d_pos_to_map_pos"),
      (overlay_set_alpha, "$g_battle_map_cavalry_order_flag", 0xFF),
      (overlay_set_position, "$g_battle_map_cavalry_order_flag", pos0),
    (else_try),
      (overlay_set_alpha, "$g_battle_map_cavalry_order_flag", 0),
    (try_end),

    (try_begin),
      (eq, ":old_is_infantry_listening", 1),
      (eq, ":old_is_archers_listening" , 1),
      (eq, ":old_is_cavalry_listening" , 1),
      (team_set_order_listener, ":player_team", grc_everyone),
    (else_try),
      (eq, ":old_is_infantry_listening", 1),
      (team_set_order_listener, ":player_team", grc_infantry),
    (else_try),
      (eq, ":old_is_archers_listening", 1),
      (team_set_order_listener, ":player_team", grc_archers),
    (else_try),
      (eq, ":old_is_cavalry_listening", 1),
      (team_set_order_listener, ":player_team", grc_cavalry),
    (try_end),
  ]),

  # script_update_order_panel_checked_classes
  ("update_order_panel_checked_classes",
   [(get_player_agent_no, ":player_agent"),
    (agent_get_team, ":player_team", ":player_agent"),

    (try_begin),
      (class_is_listening_order, ":player_team", grc_infantry),
      (overlay_set_val, "$g_presentation_obj_4", 1),
      (assign, "$g_formation_infantry_selected", 1),
      (overlay_animate_to_alpha, "$g_presentation_obj_1", 250, 0x44),
    (else_try),
      (overlay_set_val, "$g_presentation_obj_4", 0),
      (assign, "$g_formation_infantry_selected", 0),
      (overlay_animate_to_alpha, "$g_presentation_obj_1", 250, 0),
    (try_end),
    (try_begin),
      (class_is_listening_order, ":player_team", grc_archers),
      (overlay_set_val, "$g_presentation_obj_5", 1),
      (assign, "$g_formation_archers_selected", 1),
      (overlay_animate_to_alpha, "$g_presentation_obj_2", 250, 0x44),
    (else_try),
      (overlay_set_val, "$g_presentation_obj_5", 0),
      (assign, "$g_formation_archers_selected", 0),
      (overlay_animate_to_alpha, "$g_presentation_obj_2", 250, 0),
    (try_end),
    (try_begin),
      (class_is_listening_order, ":player_team", grc_cavalry),
      (overlay_set_val, "$g_presentation_obj_6", 1),
      (assign, "$g_formation_cavalry_selected", 1),
      (overlay_animate_to_alpha, "$g_presentation_obj_3", 250, 0x44),
    (else_try),
      (overlay_set_val, "$g_presentation_obj_6", 0),
      (assign, "$g_formation_cavalry_selected", 0),
      (overlay_animate_to_alpha, "$g_presentation_obj_3", 250, 0),
    (try_end),
  ]),

  # script_update_order_panel_statistics_and_map
  ("update_order_panel_statistics_and_map", #TODO: Call this in every battle mission template, once per second
   [(set_fixed_point_multiplier, 1000),
    (assign, ":num_us_ready_infantry", 0),
    (assign, ":num_us_ready_archers", 0),
    (assign, ":num_us_ready_cavalry", 0),
    (assign, ":num_us_wounded_infantry", 0),
    (assign, ":num_us_wounded_archers", 0),
    (assign, ":num_us_wounded_cavalry", 0),
    (assign, ":num_us_dead_infantry", 0),
    (assign, ":num_us_dead_archers", 0),
    (assign, ":num_us_dead_cavalry", 0),
    (assign, ":num_allies_ready_men", 0),
    (assign, ":num_allies_wounded_men", 0),
    (assign, ":num_allies_dead_men", 0),
    (assign, ":num_enemies_ready_men", 0),
    (assign, ":num_enemies_wounded_men", 0),
    (assign, ":num_enemies_dead_men", 0),

    (get_player_agent_no, ":player_agent"),
    (agent_get_team, ":player_team", ":player_agent"),

    (assign, ":old_is_infantry_listening", 0),
    (try_begin),
      (class_is_listening_order, ":player_team", grc_infantry),
      (assign, ":old_is_infantry_listening", 1),
    (try_end),
    (assign, ":old_is_archers_listening", 0),
    (try_begin),
      (class_is_listening_order, ":player_team", grc_archers),
      (assign, ":old_is_archers_listening", 1),
    (try_end),
    (assign, ":old_is_cavalry_listening", 0),
    (try_begin),
      (class_is_listening_order, ":player_team", grc_cavalry),
      (assign, ":old_is_cavalry_listening", 1),
    (try_end),

    (get_scene_boundaries, pos2, pos3),

    (try_for_agents,":cur_agent"),
      (agent_is_human, ":cur_agent"),
      (agent_get_class, ":agent_class", ":cur_agent"),
      (agent_get_party_id, ":agent_party", ":cur_agent"),
      (agent_get_slot, ":agent_overlay", ":cur_agent", slot_agent_map_overlay_id),
      (try_begin),
        (eq, ":agent_party", "p_main_party"),
        (try_begin),
          (agent_is_alive, ":cur_agent"),
          (call_script, "script_update_agent_position_on_map", ":cur_agent"),
          
          (try_begin),
            (eq, ":agent_class", grc_archers),
            (val_add, ":num_us_ready_archers", 1),
          (else_try),
            (eq, ":agent_class", grc_cavalry),
            (val_add, ":num_us_ready_cavalry", 1),
          (else_try),
            #infantry
            (val_add, ":num_us_ready_infantry", 1),
          (try_end),
        (else_try),
          (overlay_set_alpha, ":agent_overlay", 0),
          (agent_is_wounded, ":cur_agent"),
          (try_begin),
            (eq, ":agent_class", grc_archers),
            (val_add, ":num_us_wounded_archers", 1),
          (else_try),
            (eq, ":agent_class", grc_cavalry),
            (val_add, ":num_us_wounded_cavalry", 1),
          (else_try),
            #infantry
            (val_add, ":num_us_wounded_infantry", 1),
          (try_end),
        (else_try),
          (try_begin),
            (eq, ":agent_class", grc_archers),
            (val_add, ":num_us_dead_archers", 1),
          (else_try),
            (eq, ":agent_class", grc_cavalry),
            (val_add, ":num_us_dead_cavalry", 1),
          (else_try),
            #infantry
            (val_add, ":num_us_dead_infantry", 1),
          (try_end),
        (try_end),
      (else_try),
        (agent_is_ally, ":cur_agent"),
        (try_begin),
          (agent_is_alive, ":cur_agent"),
          (call_script, "script_update_agent_position_on_map", ":cur_agent"),
          (val_add, ":num_allies_ready_men", 1),
        (else_try),
          (overlay_set_alpha, ":agent_overlay", 0),
          (agent_is_wounded, ":cur_agent"),
          (val_add, ":num_allies_wounded_men", 1),
        (else_try),
          (val_add, ":num_allies_dead_men", 1),
        (try_end),
      (else_try),
        (try_begin),
          (agent_is_alive, ":cur_agent"),
          (call_script, "script_update_agent_position_on_map", ":cur_agent"),
          (val_add, ":num_enemies_ready_men", 1),
        (else_try),
          (overlay_set_alpha, ":agent_overlay", 0),
          (agent_is_wounded, ":cur_agent"),
          (val_add, ":num_enemies_wounded_men", 1),
        (else_try),
          (val_add, ":num_enemies_dead_men", 1),
        (try_end),
      (try_end),
    (try_end),
    (assign, reg1, ":num_us_ready_infantry"),
    (assign, reg2, ":num_us_ready_archers"),
    (assign, reg3, ":num_us_ready_cavalry"),
    (store_add, ":num_us_ready_men", ":num_us_ready_infantry", ":num_us_ready_archers"),
    (val_add, ":num_us_ready_men", ":num_us_ready_cavalry"),
    (store_add, ":num_us_wounded_men", ":num_us_wounded_infantry", ":num_us_wounded_archers"),
    (val_add, ":num_us_wounded_men", ":num_us_wounded_cavalry"),
    (store_add, ":num_us_dead_men", ":num_us_dead_infantry", ":num_us_dead_archers"),
    (val_add, ":num_us_dead_men", ":num_us_dead_cavalry"),
    (assign, reg4, ":num_us_ready_men"),
    (assign, reg5, ":num_us_wounded_men"),
    (assign, reg6, ":num_us_dead_men"),
    (assign, reg7, ":num_allies_ready_men"),
    (assign, reg8, ":num_allies_wounded_men"),
    (assign, reg9, ":num_allies_dead_men"),
    (assign, reg10, ":num_enemies_ready_men"),
    (assign, reg11, ":num_enemies_wounded_men"),
    (assign, reg12, ":num_enemies_dead_men"),
    (overlay_set_text, "$g_presentation_obj_7", "@Infantry ({reg1})"),
    (overlay_set_text, "$g_presentation_obj_8", "@Archers ({reg2})"),
    (overlay_set_text, "$g_presentation_obj_9", "@Cavalry ({reg3})"),
    (overlay_set_text, "$g_battle_us_ready", "@{reg4}"),
    (overlay_set_text, "$g_battle_us_wounded", "@{reg5}"),
    (overlay_set_text, "$g_battle_us_dead", "@{reg6}"),
    (overlay_set_text, "$g_battle_allies_ready", "@{reg7}"),
    (overlay_set_text, "$g_battle_allies_wounded", "@{reg8}"),
    (overlay_set_text, "$g_battle_allies_dead", "@{reg9}"),
    (overlay_set_text, "$g_battle_enemies_ready", "@{reg10}"),
    (overlay_set_text, "$g_battle_enemies_wounded", "@{reg11}"),
    (overlay_set_text, "$g_battle_enemies_dead", "@{reg12}"),

    (assign, ":stat_position_x", 100),
    (assign, ":stat_position_y", 100),
    (val_add, ":stat_position_x", 150),
    (val_add, ":stat_position_y", 80),
    (position_set_x, pos1, ":stat_position_x"),
    (position_set_y, pos1, ":stat_position_y"),
    (overlay_set_position, "$g_battle_us_ready", pos1),
    (val_add, ":stat_position_x", 150),
    (position_set_x, pos1, ":stat_position_x"),
    (overlay_set_position, "$g_battle_us_wounded", pos1),
    (val_add, ":stat_position_x", 150),
    (position_set_x, pos1, ":stat_position_x"),
    (overlay_set_position, "$g_battle_us_dead", pos1),
    (val_add, ":stat_position_x", -300),
    (val_add, ":stat_position_y", -40),
    (position_set_x, pos1, ":stat_position_x"),
    (position_set_y, pos1, ":stat_position_y"),
    (overlay_set_position, "$g_battle_allies_ready", pos1),
    (val_add, ":stat_position_x", 150),
    (position_set_x, pos1, ":stat_position_x"),
    (overlay_set_position, "$g_battle_allies_wounded", pos1),
    (val_add, ":stat_position_x", 150),
    (position_set_x, pos1, ":stat_position_x"),
    (overlay_set_position, "$g_battle_allies_dead", pos1),
    (val_add, ":stat_position_x", -300),
    (val_add, ":stat_position_y", -40),
    (position_set_x, pos1, ":stat_position_x"),
    (position_set_y, pos1, ":stat_position_y"),
    (overlay_set_position, "$g_battle_enemies_ready", pos1),
    (val_add, ":stat_position_x", 150),
    (position_set_x, pos1, ":stat_position_x"),
    (overlay_set_position, "$g_battle_enemies_wounded", pos1),
    (val_add, ":stat_position_x", 150),
    (position_set_x, pos1, ":stat_position_x"),
    (overlay_set_position, "$g_battle_enemies_dead", pos1),

    (call_script, "script_update_order_flags_on_map"),

    (try_begin),
      (eq, ":old_is_infantry_listening", 1),
      (eq, ":old_is_archers_listening", 1),
      (eq, ":old_is_cavalry_listening", 1),
      (team_set_order_listener, ":player_team", grc_everyone),
    (else_try),
      (eq, ":old_is_infantry_listening", 1),
      (team_set_order_listener, ":player_team", grc_infantry),
    (else_try),
      (eq, ":old_is_archers_listening", 1),
      (team_set_order_listener, ":player_team", grc_archers),
    (else_try),
      (eq, ":old_is_cavalry_listening", 1),
      (team_set_order_listener, ":player_team", grc_cavalry),
    (try_end),
  ]),


  # script_consume_food
  # Input: arg1: order of the food to be consumed
  # Output: none
  ("consume_food",
   [(store_script_param, ":selected_food", 1),
    (troop_get_inventory_capacity, ":capacity", "trp_player"),
    (try_for_range, ":cur_slot", 0, ":capacity"),
      (troop_get_inventory_slot, ":cur_item", "trp_player", ":cur_slot"),
      (is_between, ":cur_item", food_begin, food_end),
      (troop_get_inventory_slot_modifier, ":item_modifier", "trp_player", ":cur_slot"),
      (neq, ":item_modifier", imod_rotten),
      (item_slot_eq, ":cur_item", slot_item_is_checked, 0),
      (item_set_slot, ":cur_item", slot_item_is_checked, 1),
      (val_sub, ":selected_food", 1),
      (lt, ":selected_food", 0),
      (assign, ":capacity", 0),
      (troop_inventory_slot_get_item_amount, ":cur_amount", "trp_player", ":cur_slot"),
      (val_sub, ":cur_amount", 1),
      (troop_inventory_slot_set_item_amount, "trp_player", ":cur_slot", ":cur_amount"),
    (try_end),
    ]),
	
   # script_consume_orc_brew-- mtarini
  # Input: arg1: how much
  # Output: none
   ("consume_orc_brew",
   [
    (store_script_param, ":howmuch", 1),
    (troop_get_inventory_capacity, ":capacity", "trp_player"),
    (try_for_range, ":cur_slot", 0, ":capacity"),
      (troop_get_inventory_slot, ":cur_item", "trp_player", ":cur_slot"),
      (eq, ":cur_item", "itm_orc_brew"),
	  (assign, ":capacity", 0), # stop loops
      (troop_inventory_slot_get_item_amount, ":cur_amount", "trp_player", ":cur_slot"),
      (val_sub, ":cur_amount", ":howmuch"),
	  (try_begin), 
	     (le, ":cur_amount", 0),
		 (display_message, "@Orc brew finished!"),
	  (try_end), 
      (troop_inventory_slot_set_item_amount, "trp_player", ":cur_slot", ":cur_amount"),
    (try_end),
    ]),

  # script_calculate_troop_score_for_center
  # Input: arg1 = troop_no, arg2 = center_no
  # Output: reg0 = score
  ("calculate_troop_score_for_center",
   [(store_script_param, ":troop_no", 1),
    (store_script_param, ":center_no", 2),
    (assign, ":num_center_points", 1),
    (try_for_range, ":cur_center", centers_begin, centers_end),
      (party_is_active, ":cur_center"), #TLD
      (assign, ":center_owned", 0),
      (try_begin),
        (eq, ":troop_no", "trp_player"),
        (party_slot_eq, ":cur_center", slot_town_lord, stl_reserved_for_player),
        (assign, ":center_owned", 1),
      (try_end),
      (this_or_next|party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
      (eq, ":center_owned", 1),
      (try_begin),
        (party_slot_eq, ":cur_center", slot_party_type, spt_town),
        (val_add, ":num_center_points", 4),
      (else_try),
        (party_slot_eq, ":cur_center", slot_party_type, spt_castle),
        (val_add, ":num_center_points", 2),
      (else_try),
        (val_add, ":num_center_points", 1),
      (try_end),
    (try_end),
    (troop_get_slot, ":troop_renown", ":troop_no", slot_troop_renown),
    (store_add, ":score", 500, ":troop_renown"),
    (val_div, ":score", ":num_center_points"),
    (store_random_in_range, ":random", 50, 100),
    (val_mul, ":score", ":random"),
    (try_begin),
      (party_slot_eq, ":center_no", slot_center_last_taken_by_troop, ":troop_no"),
      (val_mul, ":score", 3),
      (val_div, ":score", 2),
    (try_end),
    (try_begin),
      (eq, ":troop_no", "trp_player"),
      (faction_get_slot, ":faction_leader", "$players_kingdom"),
      (call_script, "script_troop_get_player_relation", ":faction_leader"),
      (assign, ":leader_relation", reg0),
      #(troop_get_slot, ":leader_relation", ":faction_leader", slot_troop_player_relation),
      (val_mul, ":leader_relation", 2),
      (val_add, ":score", ":leader_relation"),
    (try_end),
    (assign, reg0, ":score"),
    ]),
  
  # script_assign_lords_to_empty_centers
  ("assign_lords_to_empty_centers",
   [(try_for_range, ":cur_center", centers_begin, centers_end),
      (party_is_active, ":cur_center"), #TLD
      (party_get_slot, ":center_lord", ":cur_center", slot_town_lord),
      (this_or_next|eq, ":center_lord", stl_unassigned),
      (eq, ":center_lord", stl_rejected_by_player),
    
      (store_faction_of_party, ":center_faction", ":cur_center"),
      (is_between, ":center_faction", kingdoms_begin, kingdoms_end),
      (neg|faction_slot_eq, ":center_faction", slot_faction_leader, "trp_player"),

      (assign, ":best_lord", -1),
      (assign, ":best_lord_score", -1),
      (try_begin),
        (eq, ":center_lord", stl_unassigned),
        (try_begin),
          (eq, "$players_kingdom", ":center_faction"),
          (eq, "$player_has_homage", 1),
          (assign, ":best_lord", stl_reserved_for_player),
          (call_script, "script_calculate_troop_score_for_center", "trp_player", ":cur_center"),
          (assign, ":best_lord_score", reg0),
        (try_end),
      (try_end),
    
      (try_for_range, ":cur_troop", kingdom_heroes_begin, kingdom_heroes_end),
        (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
        (store_troop_faction, ":troop_faction", ":cur_troop"),
        (eq, ":troop_faction", ":center_faction"),

        (call_script, "script_calculate_troop_score_for_center", ":cur_troop", ":cur_center"),
        (assign, ":score", reg0),

        (gt, ":score", ":best_lord_score"),
        (assign, ":best_lord_score", ":score"),
        (assign, ":best_lord", ":cur_troop"),
      (try_end),
      (try_begin),
        (ge, ":best_lord", 0),
        (call_script, "script_give_center_to_lord", ":cur_center", ":best_lord", 1),
      (else_try),
        (eq, ":best_lord", stl_reserved_for_player),
        (party_set_slot, ":cur_center", slot_town_lord, stl_reserved_for_player),
        (try_begin),
          (party_slot_eq, ":cur_center", slot_party_type, spt_castle),
          (try_for_range, ":cur_village", villages_begin, villages_end),
            (party_slot_eq, ":cur_village", slot_village_bound_center, ":cur_center"),
            (party_set_slot, ":cur_village", slot_town_lord, stl_reserved_for_player),
          (try_end),
        (try_end),
      (try_end),
    (try_end),
    ]),


  # script_create_village_farmer_party
  # Input: arg1 = village_no
  # Output: reg0 = party_no
  ("create_village_farmer_party",
   [(store_script_param, ":village_no", 1),
    (party_get_slot, ":town_no", ":village_no", slot_village_market_town),
    
    (store_faction_of_party, ":party_faction", ":town_no"),
    (set_spawn_radius, 0),
    (spawn_around_party, ":village_no", "pt_village_farmers"),
    (assign, ":new_party", reg0),
      
    (party_set_faction, ":new_party", ":party_faction"),
    (party_set_slot, ":new_party", slot_party_home_center, ":village_no"),
    (party_set_slot, ":new_party", slot_party_type, spt_village_farmer),
    (party_set_slot, ":new_party", slot_party_ai_state, spai_trading_with_town),
    (party_set_slot, ":new_party", slot_party_ai_object, ":town_no"),
    (party_set_ai_behavior, ":new_party", ai_bhvr_travel_to_party),
    (party_set_ai_object, ":new_party", ":town_no"),
    (party_set_flags, ":new_party", pf_default_behavior, 0),
    (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
    (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
      (store_add, ":cur_good_price_slot", ":cur_goods", ":item_to_price_slot"),
      (party_get_slot, ":cur_village_price", ":village_no", ":cur_good_price_slot"),
      (party_set_slot, ":new_party", ":cur_good_price_slot", ":cur_village_price"),
    (try_end),
    (assign, reg0, ":new_party"),
    ]),

  #script_do_party_center_trade
  # INPUT: arg1 = party_no, arg2 = center_no, arg3 = percentage_change_in_center
  # OUTPUT: reg0 = total_change
  ("do_party_center_trade",
    [
      (store_script_param, ":party_no", 1),
      (store_script_param, ":center_no", 2),
      (store_script_param, ":percentage_change", 3),
      (assign, ":total_change", 0),
      (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
      (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
        (store_add, ":cur_good_price_slot", ":cur_good", ":item_to_price_slot"),
        (party_get_slot, ":cur_merchant_price", ":party_no", ":cur_good_price_slot"),
        (party_get_slot, ":cur_center_price", ":center_no", ":cur_good_price_slot"),
        (store_sub, ":price_dif", ":cur_merchant_price", ":cur_center_price"),
        (assign, ":cur_change", ":price_dif"),
        (val_abs, ":cur_change"),
        (val_add, ":total_change", ":cur_change"),
        (val_mul, ":cur_change", ":percentage_change"),
        (val_div, ":cur_change", 100),
        (try_begin),
          (lt, ":price_dif", 0),
          (val_mul, ":cur_change", -1),
        (try_end),
        (val_add, ":cur_center_price", ":cur_change"),
        (party_set_slot, ":center_no", ":cur_good_price_slot", ":cur_center_price"),
        (party_set_slot, ":party_no", ":cur_good_price_slot", ":cur_center_price"),
      (try_end),
      (assign, reg0, ":total_change"),
  ]),

  # script to start the game as one... troop -- mtarini
  # (copys that troop stats, items, factions, race, etc, into player)
  ("start_as_one",[
    (store_script_param, ":troop", 1),
	(assign, "$player_current_troop_type", ":troop"),
	# copy faction
    (store_troop_faction, ":fac", ":troop"),
	(call_script, "script_player_join_faction", ":fac"),
    (troop_get_slot, "$players_subkingdom",":troop", slot_troop_subfaction), # subfaction
	# copy race
	(troop_get_type,":race",":troop"),
	(troop_set_type,"trp_player",":race"),
	# copy items
	(troop_clear_inventory, "trp_player"),
	(troop_get_inventory_capacity, ":inv_cap", ":troop"),
    (try_for_range, ":i_slot", 0, ":inv_cap"),
        (troop_get_inventory_slot, ":item_id", ":troop", ":i_slot"),
        (ge, ":item_id", 0),
		(item_get_type,  ":t", ":item_id"),
        (troop_get_inventory_slot_modifier, ":item_modifier", ":troop", ":i_slot"),
		(troop_get_inventory_slot, ":prev_item", "trp_player", ":item_id"),
		(try_begin), # only one item per type! (one armor, one weapon,,,)
			(store_random_in_range, ":die_roll", 0, 100), 
			(lt|this_or_next, ":prev_item", 0), # if first item of that type...
			(lt, ":die_roll", 50), # 50% of time, replace old item with new item 
			(troop_set_inventory_slot, "trp_player", ":t",":item_id"),
			(troop_set_inventory_slot_modifier,  "trp_player", ":t",":item_modifier",),
		(try_end),
	(try_end),
	# copy stats: attrib
    (try_for_range, ":i", 0, 4),
	  (store_attribute_level, ":x",":troop",":i"),
	  (troop_raise_attribute,  "trp_player",":i",-1000), 	  
	  (troop_raise_attribute,  "trp_player",":i",":x"), 
	  #(assign, reg10, ":x"),(assign, reg11, ":i"),(display_message, "@Rising skill {reg11} to {reg10}"),
	(end_try),
	# copy stats: skills
    (try_for_range, ":i", 0, 38 ),
	  (store_skill_level, ":x", ":i", ":troop"),
	  (troop_raise_skill,  "trp_player",":i",-1000), 	  
	  (troop_raise_skill,  "trp_player",":i",":x"), 
	(end_try),
	# copy stats: proficienceis
    (try_for_range, ":i", 0, 6),
	  (store_proficiency_level, ":x", ":i", ":troop"),
	  (troop_raise_proficiency,  "trp_player",":i",-1000), 	  
	  #(val_div, ":x", 4), # weapon proficiencies are too high!
	  #(val_min, ":x", 60),
	  (troop_raise_proficiency,  "trp_player",":i",":x"), 
	(end_try),
  ]),

  #script_player_join_faction
  # INPUT: arg1 = faction_no
  # OUTPUT: none
  ("player_join_faction",
    [
      (store_script_param, ":faction_no", 1),
      (assign,"$players_kingdom",":faction_no"),
      (faction_set_slot, "fac_player_supporters_faction", slot_faction_ai_state, sfai_default),
      (assign, "$players_oath_renounced_against_kingdom", 0),
      (try_for_range,":other_kingdom",kingdoms_begin,kingdoms_end),
        (faction_slot_eq, ":other_kingdom", slot_faction_state, sfs_active),
        (neq, ":other_kingdom", "fac_player_supporters_faction"),
        (try_begin),
          (neq, ":other_kingdom", ":faction_no"),
          (store_relation, ":other_kingdom_reln", ":other_kingdom", ":faction_no"),
        (else_try),
          (store_relation, ":other_kingdom_reln", "fac_player_supporters_faction", ":other_kingdom"),
          (val_max, ":other_kingdom_reln", 50), #TLD
        (try_end),
        (call_script, "script_set_player_relation_with_faction", ":other_kingdom", ":other_kingdom_reln"),
      (try_end),
      (try_for_range, ":cur_center", centers_begin, centers_end),
        (party_is_active, ":cur_center"), #TLD
        #Give center to kingdom if player is the owner
        (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
        (party_set_faction, ":cur_center", ":faction_no"),
      (try_end),
      (try_for_range, ":quest_no", lord_quests_begin, lord_quests_end),
        (check_quest_active, ":quest_no"),
        (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
        (store_troop_faction, ":quest_giver_faction", ":quest_giver_troop"),
        (store_relation, ":quest_giver_faction_relation", "fac_player_supporters_faction", ":quest_giver_faction"),
        (lt, ":quest_giver_faction_relation", 0),
        (call_script, "script_abort_quest", ":quest_no", 0),
      (try_end),
      (try_begin),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (faction_set_slot, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
        (faction_set_slot, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
      (try_end),
      (call_script, "script_store_average_center_value_per_faction"),
      (call_script, "script_update_all_notes"),
      (assign, "$g_recalculate_ais", 1),
      ]),

  #script_player_leave_faction
  # INPUT: arg1 = give_back_fiefs
  # OUTPUT: none
  ("player_leave_faction",
    [
      (store_script_param, ":give_back_fiefs", 1),
      (call_script, "script_check_and_finish_active_army_quests_for_faction", "$players_kingdom"),
      (assign, ":old_kingdom", "$players_kingdom"),
      (assign, ":old_has_homage", "$player_has_homage"),
      (assign, "$players_kingdom", 0),
      (assign, "$player_has_homage", 0),
      (try_begin),
        (neq, ":give_back_fiefs", 0),
        (try_for_range, ":cur_center", centers_begin, centers_end),
          (party_is_active, ":cur_center"), #TLD
          (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
          (call_script, "script_give_center_to_faction", ":cur_center", ":old_kingdom"),
        (try_end),
      (else_try),
        (try_for_range, ":cur_center", centers_begin, centers_end),
          (party_is_active, ":cur_center"), #TLD
          (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
          (call_script, "script_give_center_to_faction", ":cur_center", "fac_player_supporters_faction"),
        (try_end),
        (try_for_range, ":cur_center", villages_begin, villages_end),
          (party_get_slot, ":cur_bound_center", ":cur_center", slot_village_bound_center),
          (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
          (neg|party_slot_eq, ":cur_bound_center", slot_town_lord, "trp_player"),
          (call_script, "script_give_center_to_faction", ":cur_center", ":old_kingdom"),
        (try_end),
        (store_relation, ":reln", "fac_player_supporters_faction", ":old_kingdom"),
        (store_sub, ":req_dif", -40, ":reln"),
        (call_script, "script_change_player_relation_with_faction", ":old_kingdom", ":req_dif"),
      (try_end),
      (try_begin),
        (eq, ":old_has_homage", 1),
        (faction_get_slot, ":faction_leader", ":old_kingdom", slot_faction_leader),
        (call_script, "script_change_player_relation_with_troop", ":faction_leader", -20),
      (try_end),
      (call_script, "script_update_all_notes"),
      (assign, "$g_recalculate_ais", 1),
      ]),


  #script_activate_deactivate_player_faction
  # INPUT: arg1 = last_interaction_with_faction
  # OUTPUT: none
  ("activate_deactivate_player_faction",
    [
      (store_script_param, ":last_interaction_with_faction", 1),
      (try_begin),
        (assign, ":has_center", 0),
        (try_for_range, ":cur_center", centers_begin, centers_end),
          (party_is_active, ":cur_center"), #TLD
          (store_faction_of_party, ":cur_center_faction", ":cur_center"),
          (eq, ":cur_center_faction", "fac_player_supporters_faction"),
          (assign, ":has_center", 1),
        (try_end),
        (try_begin),
          (eq, ":has_center", 1),
          (neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
          (faction_set_slot, "fac_player_supporters_faction", slot_faction_state, sfs_active),
          (faction_set_slot, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
          (str_store_faction_name, s1, ":last_interaction_with_faction"),
          (faction_set_name, "fac_player_supporters_faction", "@{s1} Rebels"),
          (faction_set_color, "fac_player_supporters_faction", 0xAAAAAA),
          (assign, "$players_kingdom", "fac_player_supporters_faction"),
          (assign, "$g_player_banner_granted", 1),
          (call_script, "script_store_average_center_value_per_faction"),
          (call_script, "script_update_all_notes"),
          (call_script, "script_add_notification_menu", "mnu_notification_player_faction_active", 0, 0),
        (else_try),
          (eq, ":has_center", 0),
          (faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
          (le, "$supported_pretender", 0),
          (faction_set_slot, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
          (faction_set_slot, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
          (assign, "$players_kingdom", 0),
          (assign, "$players_oath_renounced_against_kingdom", 0),
          (call_script, "script_store_average_center_value_per_faction"),
          (call_script, "script_update_all_notes"),
          (call_script, "script_add_notification_menu", "mnu_notification_player_faction_deactive", 0, 0),
        (try_end),
      (try_end),
      ]),



  #script_agent_reassign_team
  # INPUT: arg1 = agent_no
  # OUTPUT: none
  ("agent_reassign_team",
    [
      (store_script_param, ":agent_no", 1),
      (get_player_agent_no, ":player_agent"),
      (try_begin),
        (ge, ":player_agent", 0),
        (agent_is_human, ":agent_no"),
        (agent_is_ally, ":agent_no"),
        (agent_get_party_id, ":party_no", ":agent_no"),
        (neq, ":party_no", "p_main_party"),
        (assign, ":continue", 1),
        (store_faction_of_party, ":party_faction", ":party_no"),
        (try_begin),
          (eq, ":party_faction", "$players_kingdom"),
          (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
          (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
          (assign, ":continue", 0),
        (else_try),
          (party_stack_get_troop_id, ":leader_troop_id", ":party_no", 0),
          (neg|is_between, ":leader_troop_id", kingdom_heroes_begin, kingdom_heroes_end),
          (assign, ":continue", 0),
        (try_end),
        (eq, ":continue", 1),
        (agent_get_team, ":player_team", ":player_agent"),
        (val_add, ":player_team", 2),
        (agent_set_team, ":agent_no", ":player_team"),
      (try_end),
      ]),

  #script_start_quest
  # INPUT: arg1 = quest_no, arg2 = giver_troop_no, s2 = description_text
  # OUTPUT: none
  ("start_quest",
    [(store_script_param, ":quest_no", 1),
     (store_script_param, ":giver_troop_no", 2),
     (try_begin),
       (is_between, ":giver_troop_no", kingdom_heroes_begin, kingdom_heroes_end),
       (str_store_troop_name_link, s62, ":giver_troop_no"),
     (else_try),
       (str_store_troop_name, s62, ":giver_troop_no"),
     (try_end),
     (str_store_string, s63, "@Given by: {s62}"),
     (store_current_hours, ":cur_hours"),
     (str_store_date, s60, ":cur_hours"),
     (str_store_string, s60, "@Given on: {s60}"),
     (add_quest_note_from_sreg, ":quest_no", 0, s60, 0),
     (add_quest_note_from_sreg, ":quest_no", 1, s63, 0),
     (add_quest_note_from_sreg, ":quest_no", 2, s2, 0),

     (try_begin),
       (quest_slot_ge, ":quest_no", slot_quest_expiration_days, 1),
       (quest_get_slot, reg0, ":quest_no", slot_quest_expiration_days),
       (add_quest_note_from_sreg, ":quest_no", 7, "@You have {reg0} days to finish this quest.", 0),
     (try_end),

     #Adding dont_give_again_for_days value
     (try_begin),
       (quest_slot_ge, ":quest_no", slot_quest_dont_give_again_period, 1),
       (quest_get_slot, ":dont_give_again_period", ":quest_no", slot_quest_dont_give_again_period),
       (quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days, ":dont_give_again_period"),
     (try_end),
     (start_quest, ":quest_no", ":giver_troop_no"),
     (display_message, "str_quest_log_updated"),
     ]),

  #script_conclude_quest
  # INPUT: arg1 = quest_no
  # OUTPUT: none
  ("conclude_quest",
    [(store_script_param, ":quest_no", 1),
     (conclude_quest, ":quest_no"),
     (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
     (str_store_troop_name, s59, ":quest_giver_troop"),
     (add_quest_note_from_sreg, ":quest_no", 7, "@This quest has been concluded. Talk to {s59} to finish it.", 0),
     ]),

  #script_succeed_quest
  # INPUT: arg1 = quest_no
  # OUTPUT: none
  ("succeed_quest",
    [(store_script_param, ":quest_no", 1),
     (succeed_quest, ":quest_no"),
     (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
     (str_store_troop_name, s59, ":quest_giver_troop"),
     (add_quest_note_from_sreg, ":quest_no", 7, "@This quest has been successfully completed. Talk to {s59} to claim your reward.", 0),
     ]),

  #script_fail_quest
  # INPUT: arg1 = quest_no
  # OUTPUT: none
  ("fail_quest",
    [(store_script_param, ":quest_no", 1),
     (fail_quest, ":quest_no"),
     (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
     (str_store_troop_name, s59, ":quest_giver_troop"),
     (add_quest_note_from_sreg, ":quest_no", 7, "@This quest has failed. Talk to {s59} to explain the situation.", 0),
     ]),

  #script_report_quest_troop_positions
  # INPUT: arg1 = quest_no, arg2 = troop_no, arg3 = note_index
  # OUTPUT: none
  ("report_quest_troop_positions",
    [(store_script_param, ":quest_no", 1),
     (store_script_param, ":troop_no", 2),
     (store_script_param, ":note_index", 3),
     (call_script, "script_get_information_about_troops_position", ":troop_no", 1),
     (str_store_string, s5, "@At the time quest was given:^{s1}"),
     (add_quest_note_from_sreg, ":quest_no", ":note_index", s5, 1),
     (call_script, "script_update_troop_location_notes", ":troop_no", 1),
     ]),
   
  #script_end_quest
  # INPUT: arg1 = quest_no
  # OUTPUT: none
  ("end_quest",
    [(store_script_param, ":quest_no", 1),
     (str_clear, s1),
     (add_quest_note_from_sreg, ":quest_no", 0, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 1, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 2, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 3, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 4, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 5, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 6, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 7, s1, 0),
     (try_begin),
       (neg|check_quest_failed, ":quest_no"),
       (val_add, "$g_total_quests_completed", 1),
     (try_end),
     (complete_quest, ":quest_no"),
     (try_begin),
       (is_between, ":quest_no", mayor_quests_begin, mayor_quests_end),
       (assign, "$merchant_quest_last_offerer", -1),
       (assign, "$merchant_offered_quest", -1),
     (try_end),
     ]),

  #script_cancel_quest
  # INPUT: arg1 = quest_no
  # OUTPUT: none
  ("cancel_quest",
    [(store_script_param, ":quest_no", 1),
     (str_clear, s1),
     (add_quest_note_from_sreg, ":quest_no", 0, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 1, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 2, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 3, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 4, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 5, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 6, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 7, s1, 0),
     (cancel_quest, ":quest_no"),
     (try_begin),
       (is_between, ":quest_no", mayor_quests_begin, mayor_quests_end),
       (assign, "$merchant_quest_last_offerer", -1),
       (assign, "$merchant_offered_quest", -1),
     (try_end),
    ]),

##  #script_get_available_mercenary_troop_and_amount_of_center
##  # INPUT: arg1 = center_no
##  # OUTPUT: reg0 = mercenary_troop_type, reg1 = amount
##  ("get_available_mercenary_troop_and_amount_of_center",
##    [(store_script_param, ":center_no", 1),
##     (party_get_slot, ":mercenary_troop", ":center_no", slot_center_mercenary_troop_type),
##     (party_get_slot, ":mercenary_amount", ":center_no", slot_center_mercenary_troop_amount),
##     (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
##     (val_min, ":mercenary_amount", ":free_capacity"),
##     (store_troop_gold, ":cur_gold", "trp_player"),
##     (call_script, "script_game_get_join_cost", ":mercenary_troop"),
##     (assign, ":join_cost", reg0),
##     (try_begin),
##       (gt, ":join_cost", 0),
##       (val_div, ":cur_gold", ":join_cost"),
##       (val_min, ":mercenary_amount", ":cur_gold"),
##     (try_end),
##     (assign, reg0, ":mercenary_troop"),
##     (assign, reg1, ":mercenary_amount"),
##     ]),
##

  #script_update_village_market_towns
  ("update_village_market_towns",
    [(try_for_range, ":cur_village", villages_begin, villages_end),
       (store_faction_of_party, ":village_faction", ":cur_village"),
       (assign, ":min_dist", 999999),
       (assign, ":min_dist_town", -1),
       (try_for_range, ":cur_town", towns_begin, towns_end),
         (store_faction_of_party, ":town_faction", ":cur_town"),
         (eq, ":town_faction", ":village_faction"),
         (store_distance_to_party_from_party, ":cur_dist", ":cur_village", ":cur_town"),
         (lt, ":cur_dist", ":min_dist"),
         (assign, ":min_dist", ":cur_dist"),
         (assign, ":min_dist_town", ":cur_town"),
       (try_end),
       (gt, ":min_dist_town", -1),
       (party_set_slot, ":cur_village", slot_village_market_town, ":min_dist_town"),
     (try_end),
     ]),

  #script_update_mercenary_units_of_towns
  ("update_mercenary_units_of_towns",
    [(try_for_range, ":town_no", towns_begin, towns_end),
      (store_random_in_range, ":troop_no", mercenary_troops_begin, mercenary_troops_end),
      (party_set_slot, ":town_no", slot_center_mercenary_troop_type, ":troop_no"),
      (store_random_in_range, ":amount", 3, 8),
      (party_set_slot, ":town_no", slot_center_mercenary_troop_amount, ":amount"),
    (try_end),
     ]),
     
  #script_update_volunteer_troops_in_village
  # INPUT: arg1 = center_no
  ("update_volunteer_troops_in_village",
    [  (store_script_param, ":center_no", 1),
       (party_get_slot, ":player_relation", ":center_no", slot_center_player_relation),
       (party_get_slot, ":center_culture", ":center_no", slot_center_culture),
       (faction_get_slot, ":volunteer_troop", ":center_culture", slot_faction_tier_1_troop),
       (assign, ":volunteer_troop_tier", 1),
       (store_div, ":tier_upgrades", ":player_relation", 10),
       (try_for_range, ":unused", 0, ":tier_upgrades"),
         (store_random_in_range, ":random_no", 0, 100),
         (lt, ":random_no", 10),
         (store_random_in_range, ":random_no", 0, 2),
         (troop_get_upgrade_troop, ":upgrade_troop_no", ":volunteer_troop", ":random_no"),
         (try_begin),
           (le, ":upgrade_troop_no", 0),
           (troop_get_upgrade_troop, ":upgrade_troop_no", ":volunteer_troop", 0),
         (try_end),
         (gt, ":upgrade_troop_no", 0),
         (val_add, ":volunteer_troop_tier", 1),
         (assign, ":volunteer_troop", ":upgrade_troop_no"),
       (try_end),
       
       (assign, ":upper_limit", 7),
       (try_begin),
         (ge, ":player_relation", 5),
         (assign, ":upper_limit", ":player_relation"),
         (val_div, ":upper_limit", 2),
         (val_add, ":upper_limit", 10),
       (else_try),
         (lt, ":player_relation", 0),
         (assign, ":upper_limit", 0),
       (try_end),

       (val_mul, ":upper_limit", 3),   
       (store_add, ":amount_random_divider", 2, ":volunteer_troop_tier"),
       (val_div, ":upper_limit", ":amount_random_divider"),
       
       (store_random_in_range, ":amount", 0, ":upper_limit"),
       (party_set_slot, ":center_no", slot_center_volunteer_troop_type, ":volunteer_troop"),
       (party_set_slot, ":center_no", slot_center_volunteer_troop_amount, ":amount"),
     ]),

  #script_update_npc_volunteer_troops_in_village
  # INPUT: arg1 = center_no
  ("update_npc_volunteer_troops_in_village",
    [
       (store_script_param, ":center_no", 1),
       (party_get_slot, ":center_culture", ":center_no", slot_center_culture),
       (faction_get_slot, ":volunteer_troop", ":center_culture", slot_faction_tier_1_troop),
       (assign, ":volunteer_troop_tier", 1),
       (try_for_range, ":unused", 0, 5),
         (store_random_in_range, ":random_no", 0, 100),
         (lt, ":random_no", 10),
         (store_random_in_range, ":random_no", 0, 2),
         (troop_get_upgrade_troop, ":upgrade_troop_no", ":volunteer_troop", ":random_no"),
         (try_begin),
           (le, ":upgrade_troop_no", 0),
           (troop_get_upgrade_troop, ":upgrade_troop_no", ":volunteer_troop", 0),
         (try_end),
         (gt, ":upgrade_troop_no", 0),
         (val_add, ":volunteer_troop_tier", 1),
         (assign, ":volunteer_troop", ":upgrade_troop_no"),
       (try_end),
       
       (assign, ":upper_limit", 12),
       
       (store_add, ":amount_random_divider", 2, ":volunteer_troop_tier"),
       (val_div, ":upper_limit", ":amount_random_divider"),
       
       (store_random_in_range, ":amount", 0, ":upper_limit"),
       (party_set_slot, ":center_no", slot_center_npc_volunteer_troop_type, ":volunteer_troop"),
       (party_set_slot, ":center_no", slot_center_npc_volunteer_troop_amount, ":amount"),
     ]),

  #script_update_companion_candidates_in_taverns - not used in TLD
  ("update_companion_candidates_in_taverns",
    [  (try_for_range, ":troop_no", companions_begin, companions_end),
         (troop_set_slot, ":troop_no", slot_troop_cur_center, -1),
         (troop_slot_eq, ":troop_no", slot_troop_occupation, 0),
         (store_random_in_range, ":town_no", towns_begin, towns_end),
         (try_begin),
           (neg|troop_slot_eq, ":troop_no", slot_troop_home, ":town_no"),
           (neg|troop_slot_eq, ":troop_no", slot_troop_first_encountered, ":town_no"),
           (troop_set_slot, ":troop_no", slot_troop_cur_center, ":town_no"),
           (try_begin),
             (eq, "$cheat_mode", 1),
             (str_store_troop_name, 4, ":troop_no"),
             (str_store_party_name, 5, ":town_no"),     
             (display_message, "@{s4} is in {s5}"),
           (try_end),
         (try_end),
       (try_end),
     ]),

  #script_update_ransom_brokers
  ("update_ransom_brokers",
    [(try_for_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_ransom_broker, 0),
     (try_end),
     
     (try_for_range, ":troop_no", ransom_brokers_begin, ransom_brokers_end),
       (store_random_in_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_ransom_broker, ":troop_no"),
     (try_end),
     (party_set_slot,"p_town_pelargir",slot_center_ransom_broker,"trp_ramun_the_slave_trader"),
     ]),

  #script_update_tavern_travelers
  ("update_tavern_travelers",
    [(try_for_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_tavern_traveler, 0),
     (try_end),
     
     (try_for_range, ":troop_no", tavern_travelers_begin, tavern_travelers_end),
       (store_random_in_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_tavern_traveler, ":troop_no"),
       (assign, ":end_cond", 15),
       (try_for_range, ":unused", 0, ":end_cond"),
         (store_random_in_range, ":info_faction", kingdoms_begin, kingdoms_end),
         (faction_slot_eq, ":info_faction", slot_faction_state, sfs_active),
         (neq, ":info_faction", "$players_kingdom"),
         (neq, ":info_faction", "fac_player_supporters_faction"),
         (party_set_slot, ":town_no", slot_center_traveler_info_faction, ":info_faction"),
         (assign, ":end_cond", 0),
       (try_end),
     (try_end),
     ]),

  #script_update_villages_infested_by_bandits
  ("update_villages_infested_by_bandits",
    [(try_for_range, ":village_no", villages_begin, villages_end),
       (try_begin),
         (check_quest_active, "qst_eliminate_bandits_infesting_village"),
         (quest_slot_eq, "qst_eliminate_bandits_infesting_village", slot_quest_target_center, ":village_no"),
         (quest_get_slot, ":cur_state", "qst_eliminate_bandits_infesting_village", slot_quest_current_state),
         (val_add, ":cur_state", 1),
         (try_begin),
           (lt, ":cur_state", 3),
           (quest_set_slot, "qst_eliminate_bandits_infesting_village", slot_quest_current_state, ":cur_state"),
         (else_try),
           (party_set_slot, ":village_no", slot_village_infested_by_bandits, 0),
           (call_script, "script_abort_quest", "qst_eliminate_bandits_infesting_village", 2),
         (try_end),
       (else_try),
         (check_quest_active, "qst_deal_with_bandits_at_lords_village"),
         (quest_slot_eq, "qst_deal_with_bandits_at_lords_village", slot_quest_target_center, ":village_no"),
         (quest_get_slot, ":cur_state", "qst_deal_with_bandits_at_lords_village", slot_quest_current_state),
         (val_add, ":cur_state", 1),
         (try_begin),
           (lt, ":cur_state", 3),
           (quest_set_slot, "qst_deal_with_bandits_at_lords_village", slot_quest_current_state, ":cur_state"),
         (else_try),
           (party_set_slot, ":village_no", slot_village_infested_by_bandits, 0),
           (call_script, "script_abort_quest", "qst_deal_with_bandits_at_lords_village", 2),
         (try_end),
       (else_try),
         (party_set_slot, ":village_no", slot_village_infested_by_bandits, 0),
         (store_random_in_range, ":random_no", 0, 100),
         (lt, ":random_no", 3),
         (store_random_in_range, ":random_no", 0, 3),
         (try_begin),
           (eq, ":random_no", 0),
           (assign, ":bandit_troop", "trp_bandit"),
         (else_try),
           (eq, ":random_no", 1),
           (assign, ":bandit_troop", "trp_mountain_bandit"),
         (else_try),
           (assign, ":bandit_troop", "trp_forest_bandit"),
         (try_end),
         (party_set_slot, ":village_no", slot_village_infested_by_bandits, ":bandit_troop"),
         #Reduce prosperity of the village by 3
         (call_script, "script_change_center_prosperity", ":village_no", -3),
         (try_begin),
           (eq, "$cheat_mode", 1),
           (str_store_party_name, s1, ":village_no"),
           (display_message, "@{s1} is infested by bandits."),
         (try_end),
       (try_end),
     (try_end),
     ]),

     
  #script_update_tavern_minstels
  ("update_tavern_minstels",
    [(try_for_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_tavern_minstrel, 0),
     (try_end),
     
     (try_for_range, ":troop_no", tavern_minstrels_begin, tavern_minstrels_end),
       (store_random_in_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_tavern_minstrel, ":troop_no"),
     (try_end),
     ]),
 
  #script_update_faction_notes
  # INPUT: faction_no
  ("update_faction_notes",
    [(store_script_param, ":faction_no", 1),
     (try_begin),
       (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
       (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
       (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
       (str_store_faction_name, s5, ":faction_no"),
       (str_store_troop_name_link, s6, ":faction_leader"),
       (assign, ":num_centers", 0),
       (str_store_string, s8, "@no holdings"),
       (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
         (party_is_active, ":cur_center"), #TLD
         (store_faction_of_party, ":center_faction", ":cur_center"),
         (eq, ":center_faction", ":faction_no"),
         (try_begin),
           (eq, ":num_centers", 0),
           (str_store_party_name_link, s8, ":cur_center"),
         (else_try),
           (eq, ":num_centers", 1),
           (str_store_party_name_link, s7, ":cur_center"),
           (str_store_string, s8, "@{s7} and {s8}"),
         (else_try),
           (str_store_party_name_link, s7, ":cur_center"),
           (str_store_string, s8, "@{s7}, {s8}"),
         (try_end),
         (val_add, ":num_centers", 1),
       (try_end),
       (assign, ":num_members", 0),
       (str_store_string, s10, "@noone"),
       (try_for_range_backwards, ":loop_var", "trp_kingdom_heroes_including_player_begin", kingdom_heroes_end),
         (assign, ":cur_troop", ":loop_var"),
         (try_begin),
           (eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
           (assign, ":cur_troop", "trp_player"),
           (assign, ":troop_faction", "$players_kingdom"),
         (else_try),
           (store_troop_faction, ":troop_faction", ":cur_troop"),
         (try_end),
         (eq, ":troop_faction", ":faction_no"),
         (neq, ":cur_troop", ":faction_leader"),
         (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
         (try_begin),
           (eq, ":num_members", 0),
           (str_store_troop_name_link, s10, ":cur_troop"),
         (else_try),
           (eq, ":num_members", 1),
           (str_store_troop_name_link, s9, ":cur_troop"),
           (str_store_string, s10, "@{s9} and {s10}"),
         (else_try),
           (str_store_troop_name_link, s9, ":cur_troop"),
           (str_store_string, s10, "@{s9}, {s10}"),
         (try_end),
         (val_add, ":num_members", 1),
       (try_end),
       (str_store_string, s12, "@no one"),
       (assign, ":num_enemies", 0),
       (try_for_range_backwards, ":cur_faction", kingdoms_begin, kingdoms_end),
         (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
         (store_relation, ":cur_relation", ":cur_faction", ":faction_no"),
         (lt, ":cur_relation", 0),
         (try_begin),
           (eq, ":num_enemies", 0),
           (str_store_faction_name_link, s12, ":cur_faction"),
         (else_try),
           (eq, ":num_enemies", 1),
           (str_store_faction_name_link, s11, ":cur_faction"),
           (str_store_string, s12, "@{s11} and {s12}"),
         (else_try),
           (str_store_faction_name_link, s11, ":cur_faction"),
           (str_store_string, s12, "@{s11}, {s12}"),
         (try_end),
         (val_add, ":num_enemies", 1),
       (try_end),
       (add_faction_note_from_sreg, ":faction_no", 0, "@{s5} is ruled by {s6}.^It controls {s8}.^Its commanders are {s10}.^{s5} is at war with {s12}.", 0),
     (else_try),
       (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
       (faction_slot_eq, ":faction_no", slot_faction_state, sfs_defeated),
       (str_store_faction_name, s5, ":faction_no"),
       (add_faction_note_from_sreg, ":faction_no", 0, "@{s5} has been defeated!", 0),
       (str_clear, s1),
       (add_faction_note_from_sreg, ":faction_no", 1, s1, 0),
     (else_try),
       (str_clear, s1),
       (add_faction_note_from_sreg, ":faction_no", 0, s1, 0),
       (add_faction_note_from_sreg, ":faction_no", 1, s1, 0),
     (try_end),
#MV: show faction leader banner instead of (non-existent) faction pic
#     (try_begin),
#       (is_between, ":faction_no", "fac_gondor", kingdoms_end), #Excluding player kingdom
#       (add_faction_note_tableau_mesh, ":faction_no", "tableau_faction_note_mesh"),
#     (else_try),
       (add_faction_note_tableau_mesh, ":faction_no", "tableau_faction_note_mesh_banner"),
#     (try_end),
     ]),

  #script_update_faction_traveler_notes
  # INPUT: faction_no
  ("update_faction_traveler_notes",
    [(store_script_param, ":faction_no", 1),
     (assign, ":total_men", 0),
     (try_for_parties, ":cur_party"),
       (store_faction_of_party, ":center_faction", ":cur_party"),
       (eq, ":center_faction", ":faction_no"),
       (party_get_num_companions, ":num_men", ":cur_party"),
       (val_add, ":total_men", ":num_men"),
     (try_end),
     (str_store_faction_name, s5, ":faction_no"),
     (assign, reg1, ":total_men"),
     (add_faction_note_from_sreg, ":faction_no", 1, "@{s5} has a strength of {reg1} men in total.", 1),
     ]),


  #script_update_troop_notes
  # INPUT: troop_no
  ("update_troop_notes",
    [(store_script_param, ":troop_no", 1),
     (str_store_troop_name, s54, ":troop_no"),
     (try_begin),
       (eq, ":troop_no", "trp_player"),
       (this_or_next|eq, "$player_has_homage", 1),
       (             eq, "$players_kingdom", "fac_player_supporters_faction"),
       (assign, ":troop_faction", "$players_kingdom"),
     (else_try),
       (store_troop_faction, ":troop_faction", ":troop_no"),
     (try_end),
     (try_begin),
       (neq, ":troop_no", "trp_player"),
       (neg|is_between, ":troop_faction", kingdoms_begin, kingdoms_end),
       (str_clear, s54),
       (add_troop_note_from_sreg, ":troop_no", 0, s54, 0),
       (add_troop_note_from_sreg, ":troop_no", 1, s54, 0),
       (add_troop_note_from_sreg, ":troop_no", 2, s54, 0),
     (else_try),
       (is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
       (str_clear, s54),
       (add_troop_note_from_sreg, ":troop_no", 0, s54, 0),
       (add_troop_note_from_sreg, ":troop_no", 1, s54, 0),
       (add_troop_note_from_sreg, ":troop_no", 2, s54, 0),
     (else_try),
       (is_between, ":troop_no", pretenders_begin, pretenders_end),
       (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
       (neq, ":troop_no", "$supported_pretender"),
       (troop_get_slot, ":orig_faction", ":troop_no", slot_troop_original_faction),
       (try_begin),
         (faction_slot_eq, ":orig_faction", slot_faction_state, sfs_active),
         (faction_slot_eq, ":orig_faction", slot_faction_has_rebellion_chance, 1),
         (str_store_faction_name_link, s56, ":orig_faction"),
         (add_troop_note_from_sreg, ":troop_no", 0, "@{s54} is a claimant to the throne of {s56}.", 0),
         (add_troop_note_tableau_mesh, ":troop_no", "tableau_troop_note_mesh"),
       (else_try),
         (str_clear, s54),
         (add_troop_note_from_sreg, ":troop_no", 0, s54, 0),
         (add_troop_note_from_sreg, ":troop_no", 1, s54, 0),
         (add_troop_note_from_sreg, ":troop_no", 2, s54, 0),
       (try_end),
     (else_try),
       (faction_get_slot, ":faction_leader", ":troop_faction", slot_faction_leader),
       (str_store_troop_name_link, s55, ":faction_leader"),
       (str_store_faction_name_link, s56, ":troop_faction"),
       (assign, reg4, 0),
       (assign, reg6, 0),
       (try_begin),
         (eq, ":troop_faction", "fac_player_faction"),
         (assign, reg6, 1),
       (else_try),
         (eq, ":faction_leader", ":troop_no"),
         (assign, reg4, 1),
       (try_end),
       (assign, ":num_centers", 0),
       (str_store_string, s58, "@no holdings"),
       (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
         (party_is_active, ":cur_center"), #TLD
         (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
         (try_begin),
           (eq, ":num_centers", 0),
           (str_store_party_name_link, s58, ":cur_center"),
         (else_try),
           (eq, ":num_centers", 1),
           (str_store_party_name_link, s57, ":cur_center"),
           (str_store_string, s58, "@{s57} and {s58}"),
         (else_try),
           (str_store_party_name_link, s57, ":cur_center"),
           (str_store_string, s58, "@{s57}, {s58}"),
         (try_end),
         (val_add, ":num_centers", 1),
       (try_end),
       (troop_get_type, reg3, ":troop_no"),
       (try_begin),
         (gt, reg3, 1), #MV: non-humans are male
         (assign, reg3, 0),
       (try_end),
       (troop_get_slot, reg5, ":troop_no", slot_troop_renown),
       (str_clear, s59),
       (try_begin),
#         (troop_get_slot, ":relation", ":troop_no", slot_troop_player_relation),
         (call_script, "script_troop_get_player_relation", ":troop_no"),
         (assign, ":relation", reg0),
         (store_add, ":normalized_relation", ":relation", 100),
         (val_add, ":normalized_relation", 5),
         (store_div, ":str_offset", ":normalized_relation", 10),
         (val_clamp, ":str_offset", 0, 20),
         (store_add, ":str_id", "str_relation_mnus_100_ns",  ":str_offset"),
         (neq, ":str_id", "str_relation_plus_0_ns"),
         (str_store_string, s60, "@{reg3?She:He}"),
         (str_store_string, s59, ":str_id"),
         (str_store_string, s59, "@^{s59}"),
       (try_end),
       (assign, reg9, ":num_centers"),
       (add_troop_note_from_sreg, ":troop_no", 0, "@{reg6?:{reg4?{s54} is the ruler of {s56}.^:{s54} serves {s55} of {s56}.^}}Renown: {reg5}.{reg9?^{reg3?She:He} is the {reg3?lady:lord} of {s58}.:}{s59}", 0),
       (add_troop_note_tableau_mesh, ":troop_no", "tableau_troop_note_mesh"),
     (try_end),
     ]),

  #script_update_troop_location_notes
  # INPUT: troop_no
  ("update_troop_location_notes",
    [(store_script_param, ":troop_no", 1),
     (store_script_param, ":see_or_hear", 2),
     (call_script, "script_get_information_about_troops_position", ":troop_no", 1),
     (try_begin),
       (neq, reg0, 0),
       (troop_get_type, reg1, ":troop_no"),
       (try_begin),
         (gt, reg1, 1), #MV: non-humans are male
         (assign, reg1, 0),
       (try_end),
       (try_begin),
         (eq, ":see_or_hear", 0),
         (add_troop_note_from_sreg, ":troop_no", 2, "@The last time you saw {reg1?her:him}, {s1}", 1),
       (else_try),
         (add_troop_note_from_sreg, ":troop_no", 2, "@The last time you heard about {reg1?her:him}, {s1}", 1),
       (try_end),
     (try_end),
     ]),

  #script_update_center_notes
  # INPUT: center_no
  ("update_center_notes",
    [(store_script_param, ":center_no", 1),

     (party_get_slot, ":lord_troop", ":center_no", slot_town_lord),
     (try_begin),
       (ge, ":lord_troop", 0),
       (store_troop_faction, ":lord_faction", ":lord_troop"),
       (faction_slot_eq, ":lord_faction", slot_faction_state, sfs_active), #TLD
       (str_store_troop_name_link, s1, ":lord_troop"),
       (try_begin),
         (eq, ":lord_troop", "trp_player"),
         (gt, "$players_kingdom", 0),
         (str_store_faction_name_link, s2, "$players_kingdom"),
       (else_try),
         (str_store_faction_name_link, s2, ":lord_faction"),
       (try_end),
       (str_store_party_name, s50, ":center_no"),
       (try_begin),
         (party_slot_eq, ":center_no", slot_party_type, spt_town),
         (str_store_string, s51, "@The town of {s50}"),
       (else_try),
         (party_slot_eq, ":center_no", slot_party_type, spt_village),
         (party_get_slot, ":bound_center", ":center_no", slot_village_bound_center),
         (str_store_party_name_link, s52, ":bound_center"),
         (str_store_string, s51, "@The village of {s50} near {s52}"),
       (else_try),
         (str_store_string, s51, "@{s50}"),
       (try_end),
       (str_store_string, s2, "@{s50} belongs to {s1} of {s2}.^"), #TLD: was s51
     (else_try),
       (str_clear, s2),
     (try_end),
     (try_begin),
       (is_between, ":center_no", villages_begin, villages_end),
     (else_try),
       (eq, 0, 1), #TLD: no villages
       (assign, ":num_villages", 0),
       (try_for_range_backwards, ":village_no", villages_begin, villages_end),
         (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),
         (try_begin),
           (eq, ":num_villages", 0),
           (str_store_party_name_link, s8, ":village_no"),
         (else_try),
           (eq, ":num_villages", 1),
           (str_store_party_name_link, s7, ":village_no"),
           (str_store_string, s8, "@{s7} and {s8}"),
         (else_try),
           (str_store_party_name_link, s7, ":village_no"),
           (str_store_string, s8, "@{s7}, {s8}"),
         (try_end),
         (val_add, ":num_villages", 1),
       (try_end),
       (try_begin),
         (eq, ":num_villages", 0),
         (str_store_string, s2, "@{s2}It has no villages.^"),
       (else_try),
         (store_sub, reg0, ":num_villages", 1),
         (str_store_string, s2, "@{s2}{reg0?Its villages are:Its village is} {s8}.^"),
       (try_end),
     (try_end),
     (call_script, "script_get_prosperity_text_to_s50", ":center_no"),
     (try_begin), #TLD: if party is disabled, clear all text so there will be no wiki entry
       (neg|party_is_active, ":center_no"),
       (str_clear, s2),
     (try_end),
     (add_party_note_from_sreg, ":center_no", 0, "@{s2}", 0), #TLD: no prosperity
     #(add_party_note_from_sreg, ":center_no", 0, "@{s2}Its prosperity is: {s50}", 0),
     (add_party_note_tableau_mesh, ":center_no", "tableau_center_note_mesh"),
     ]),
      

  #script_update_center_recon_notes
  # INPUT: center_no
  # OUTPUT: none
  ("update_center_recon_notes",
    [(store_script_param, ":center_no", 1),
     (try_begin),
       (this_or_next|is_between, ":center_no", towns_begin, towns_end),
       (is_between, ":center_no", castles_begin, castles_end),
       (party_get_slot, ":center_food_store", ":center_no", slot_party_food_store),
       (call_script, "script_center_get_food_consumption", ":center_no"),
       (assign, ":food_consumption", reg0),
       (store_div, reg6, ":center_food_store", ":food_consumption"),
       (party_collect_attachments_to_party, ":center_no", "p_collective_ally"),
       (party_get_num_companions, reg5, "p_collective_ally"),
       (add_party_note_from_sreg, ":center_no", 1, "@Current garrison consists of {reg5} men.^Has food stock for {reg6} days.", 1),
     (try_end),
     ]),
  
  #script_update_all_notes
  ("update_all_notes",
    [ (call_script, "script_update_troop_notes", "trp_player"),
      (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
        (call_script, "script_update_troop_notes", ":troop_no"),
      (try_end),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
        (call_script, "script_update_center_notes", ":center_no"),
      (try_end),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (call_script, "script_update_faction_notes", ":faction_no"),
      (try_end),
     ]),


  #script_shield_item_set_banner
  # INPUT: agent_no
  # OUTPUT: none
  ("shield_item_set_banner",
    [  (store_script_param, ":tableau_no",1),
       (store_script_param, ":agent_no", 2),
       (store_script_param, ":troop_no", 3),
       (assign, ":banner_troop", -1),
       (assign, ":banner_mesh", "mesh_banners_default_b"),
       (try_begin),
         (lt, ":agent_no", 0),
         (try_begin),
           (ge, ":troop_no", 0),
           (this_or_next|troop_slot_ge, ":troop_no", slot_troop_banner_scene_prop, 1),
           (             eq, ":troop_no", "trp_player"),
           (assign, ":banner_troop", ":troop_no"),
         (else_try),
           (is_between, ":troop_no", companions_begin, companions_end),
           (assign, ":banner_troop", "trp_player"),
         (else_try),
           (assign, ":banner_mesh", "mesh_banners_default_a"),
         (try_end),
       (else_try),
         (agent_get_troop_id, ":troop_id", ":agent_no"),
         (this_or_next|troop_slot_ge,  ":troop_id", slot_troop_banner_scene_prop, 1),
         (             eq, ":troop_no", "trp_player"),
         (assign, ":banner_troop", ":troop_id"),
       (else_try),
         (agent_get_party_id, ":agent_party", ":agent_no"),
         (try_begin),
           (lt, ":agent_party", 0),
           (is_between, ":troop_id", companions_begin, companions_end),
           (main_party_has_troop, ":troop_id"),
           (assign, ":agent_party", "p_main_party"),
         (try_end),
         (ge, ":agent_party", 0),
         (party_get_template_id, ":party_template", ":agent_party"),
         (try_begin),
           (eq, ":party_template", "pt_deserters"),
           (assign, ":banner_mesh", "mesh_banners_default_c"),
         (else_try),
           (is_between, ":agent_party", centers_begin, centers_end),
           (party_get_slot, ":town_lord", "$g_encountered_party", slot_town_lord),
           (ge, ":town_lord", 0),
           (assign, ":banner_troop", ":town_lord"),
         (else_try),
           (this_or_next|party_slot_eq, ":agent_party", slot_party_type, spt_kingdom_hero_party),
           (             eq, ":agent_party", "p_main_party"),
           (party_get_num_companion_stacks, ":num_stacks", ":agent_party"),
           (gt, ":num_stacks", 0),
           (party_stack_get_troop_id, ":leader_troop_id", ":agent_party", 0),
           (this_or_next|troop_slot_ge,  ":leader_troop_id", slot_troop_banner_scene_prop, 1),
           (             eq, ":leader_troop_id", "trp_player"),
           (assign, ":banner_troop", ":leader_troop_id"),
         (try_end),
       (else_try), #Check if we are in a tavern
         (eq, "$talk_context", tc_tavern_talk),
         (neq, ":troop_no", "trp_player"),
         (assign, ":banner_mesh", "mesh_banners_default_d"),
       (else_try), #can't find party, this can be a town guard
         (neq, ":troop_no", "trp_player"),
         (is_between, "$g_encountered_party", walled_centers_begin, walled_centers_end),
         (party_get_slot, ":town_lord", "$g_encountered_party", slot_town_lord),
         (ge, ":town_lord", 0),
         (assign, ":banner_troop", ":town_lord"),
       (try_end),
	   
       (try_begin),
         (ge, ":banner_troop", 0),
         (try_begin),
           (neg|troop_slot_ge, ":banner_troop", slot_troop_banner_scene_prop, 1),
           (assign, ":banner_mesh", "mesh_banners_default_b"),
         (else_try), 
           (troop_get_slot, ":banner_spr", ":banner_troop", slot_troop_banner_scene_prop),
           (store_add, ":banner_scene_props_end", banner_scene_props_end_minus_one, 1),
           (is_between, ":banner_spr", banner_scene_props_begin, ":banner_scene_props_end"),
           (val_sub, ":banner_spr", banner_scene_props_begin),
           (store_add, ":banner_mesh", ":banner_spr", arms_meshes_begin),
         (try_end),
       (try_end),
       (cur_item_set_tableau_material, ":tableau_no", ":banner_mesh"),
     ]),

##  #script_shield_item_set_banner
##  # INPUT: agent_no
##  # OUTPUT: none
##  ("shield_item_set_banner",
##    [
##       (store_script_param, ":tableau_no",1),
##       (store_script_param, ":agent_no", 2),
##       (store_script_param, ":troop_no", 3),
##       (assign, ":banner_troop", -1),
##       (try_begin),
##         (lt, ":agent_no", 0),
##         (try_begin),
##           (ge, ":troop_no", 0),
##           (troop_slot_ge, ":troop_no", slot_troop_banner_scene_prop, 0),
##           (assign, ":banner_troop", ":troop_no"),
##         (else_try),
##           (assign, ":banner_troop", -2),
##         (try_end),
##       (else_try),
##         (agent_get_troop_id, ":troop_id", ":agent_no"),
##         (troop_slot_ge,  ":troop_id", slot_troop_custom_banner_flag_type, 0),
##         (assign, ":banner_troop", ":troop_id"),
##       (else_try),
##         (agent_get_party_id, ":agent_party", ":agent_no"),
##         (try_begin),
##           (lt, ":agent_party", 0),
##           (is_between, ":troop_id", companions_begin, companions_end),
##           (main_party_has_troop, ":troop_id"),
##           (assign, ":agent_party", "p_main_party"),
##         (try_end),
##         (ge, ":agent_party", 0),
##         (party_get_template_id, ":party_template", ":agent_party"),
##         (try_begin),
##           (eq, ":party_template", "pt_deserters"),
##           (assign, ":banner_troop", -3),
##         (else_try),
##           (is_between, ":agent_party", centers_begin, centers_end),
##           (party_get_slot, ":town_lord", "$g_encountered_party", slot_town_lord),
##           (ge, ":town_lord", 0),
##           (assign, ":banner_troop", ":town_lord"),
##         (else_try),
##           (this_or_next|party_slot_eq, ":agent_party", slot_party_type, spt_kingdom_hero_party),
##           (             eq, ":agent_party", "p_main_party"),
##           (party_get_num_companion_stacks, ":num_stacks", ":agent_party"),
##           (gt, ":num_stacks", 0),
##           (party_stack_get_troop_id, ":leader_troop_id", ":agent_party", 0),
##           (troop_slot_ge,  ":leader_troop_id", slot_troop_banner_scene_prop, 1),
##           (assign, ":banner_troop", ":leader_troop_id"),
##         (try_end),
##       (else_try), #Check if we are in a tavern
##         (eq, "$talk_context", tc_tavern_talk),
##         (neq, ":troop_no", "trp_player"),
##         (assign, ":banner_troop", -4),
##       (else_try), #can't find party, this can be a town guard
##         (neq, ":troop_no", "trp_player"),
##         (is_between, "$g_encountered_party", walled_centers_begin, walled_centers_end),
##         (party_get_slot, ":town_lord", "$g_encountered_party", slot_town_lord),
##         (ge, ":town_lord", 0),
##         (assign, ":banner_troop", ":town_lord"),
##       (try_end),
##       (cur_item_set_tableau_material, ":tableau_no", ":banner_troop"),
##     ]),

  #script_add_troop_to_cur_tableau
  # INPUT: troop_no
  # OUTPUT: none
  ("add_troop_to_cur_tableau",
    [  (store_script_param, ":troop_no",1),

       (set_fixed_point_multiplier, 100),
       (assign, ":banner_mesh", -1),
       (troop_get_slot, ":banner_spr", ":troop_no", slot_troop_banner_scene_prop),
       (store_add, ":banner_scene_props_end", banner_scene_props_end_minus_one, 1),
       (try_begin),
         (is_between, ":banner_spr", banner_scene_props_begin, ":banner_scene_props_end"),
         (val_sub, ":banner_spr", banner_scene_props_begin),
         (store_add, ":banner_mesh", ":banner_spr", banner_meshes_begin),
       (try_end),

       (cur_tableau_clear_override_items),
       
#       (cur_tableau_set_override_flags, af_override_fullhelm),
       (cur_tableau_set_override_flags, af_override_head|af_override_weapons),
       
       (init_position, pos2),
       (cur_tableau_set_camera_parameters, 1, 6, 6, 10, 10000),

       (init_position, pos5),
       (assign, ":eye_height", 162),
       (store_mul, ":camera_distance", ":troop_no", 87323),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 139),
       (store_mul, ":camera_yaw", ":troop_no", 124337),
       (val_mod, ":camera_yaw", 50),
       (val_add, ":camera_yaw", -25),
       (store_mul, ":camera_pitch", ":troop_no", 98123),
       (val_mod, ":camera_pitch", 20),
       (val_add, ":camera_pitch", -14),
       (assign, ":animation", anim_stand_man),
       
##       (troop_get_inventory_slot, ":horse_item", ":troop_no", ek_horse),
##       (try_begin),
##         (gt, ":horse_item", 0),
##         (assign, ":eye_height", 210),
##         (cur_tableau_add_horse, ":horse_item", pos2, anim_horse_stand, 0),
##         (assign, ":animation", anim_ride_0),
##         (position_set_z, pos5, 125),
##         (try_begin),
##           (is_between, ":camera_yaw", -10, 10), #make sure horse head doesn't obstruct face.
##           (val_min, ":camera_pitch", -5),
##         (try_end),
##       (try_end),
       (position_set_z, pos5, ":eye_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

       (try_begin),
         (ge, ":banner_mesh", 0),

         (init_position, pos1),
         (position_set_z, pos1, -1500),
         (position_set_x, pos1, 265),
         (position_set_y, pos1, 400),
         (position_transform_position_to_parent, pos3, pos5, pos1),
         (cur_tableau_add_mesh, ":banner_mesh", pos3, 400, 0),
       (try_end),
       (cur_tableau_add_troop, ":troop_no", pos2, ":animation" , 0),

       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30), 
       (position_rotate_x, pos8, -60), 
       (cur_tableau_add_sun_light, pos8, 175,150,125),
     ]),

  #script_add_troop_to_cur_tableau_for_character
  # INPUT: troop_no
  # OUTPUT: none
  ("add_troop_to_cur_tableau_for_character",
    [
       (store_script_param, ":troop_no",1),

       (set_fixed_point_multiplier, 100),

       (cur_tableau_clear_override_items),
       (cur_tableau_set_override_flags, af_override_fullhelm),
##       (cur_tableau_set_override_flags, af_override_head|af_override_weapons),
       
       (init_position, pos2),
       (cur_tableau_set_camera_parameters, 1, 4, 8, 10, 10000),

       (init_position, pos5),
       (assign, ":cam_height", 150),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 360),
       (assign, ":camera_yaw", -15),
       (assign, ":camera_pitch", -18),
       (assign, ":animation", anim_stand_man),
       
       (position_set_z, pos5, ":cam_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

       (try_begin),
         (troop_is_hero, ":troop_no"),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", -1),
       (else_try),
         (store_mul, ":random_seed", ":troop_no", 126233),
         (val_mod, ":random_seed", 1000),
         (val_add, ":random_seed", 1),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", ":random_seed"),
       (try_end),
       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30), 
       (position_rotate_x, pos8, -60), 
       (cur_tableau_add_sun_light, pos8, 175,150,125),
     ]),

  #script_add_troop_to_cur_tableau_for_inventory
  # INPUT: troop_no
  # OUTPUT: none
  ("add_troop_to_cur_tableau_for_inventory",
    [
       (store_script_param, ":troop_no",1),
       (store_mod, ":side", ":troop_no", 4), #side flag is inside troop_no value
       (val_div, ":troop_no", 4), #removing the flag bit
       (val_mul, ":side", 90), #to degrees

       (set_fixed_point_multiplier, 100),

       (cur_tableau_clear_override_items),
       
       (init_position, pos2),
       (position_rotate_z, pos2, ":side"),
       (cur_tableau_set_camera_parameters, 1, 4, 6, 10, 10000),

       (init_position, pos5),
       (assign, ":cam_height", 105),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 380),
       (assign, ":camera_yaw", -15),
       (assign, ":camera_pitch", -18),
       (assign, ":animation", anim_stand_man),
       
       (position_set_z, pos5, ":cam_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

       (try_begin),
         (troop_is_hero, ":troop_no"),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", -1),
       (else_try),
         (store_mul, ":random_seed", ":troop_no", 126233),
         (val_mod, ":random_seed", 1000),
         (val_add, ":random_seed", 1),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", ":random_seed"),
       (try_end),
       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30), 
       (position_rotate_x, pos8, -60), 
       (cur_tableau_add_sun_light, pos8, 175,150,125),
     ]),
  
  #script_add_troop_to_cur_tableau_for_party
  # INPUT: troop_no
  # OUTPUT: none
  ("add_troop_to_cur_tableau_for_party",
    [
       (store_script_param, ":troop_no",1),
       (store_mod, ":hide_weapons", ":troop_no", 2), #hide_weapons flag is inside troop_no value
       (val_div, ":troop_no", 2), #removing the flag bit

       (set_fixed_point_multiplier, 100),

       (cur_tableau_clear_override_items),
       (try_begin),
         (eq, ":hide_weapons", 1),
         (cur_tableau_set_override_flags, af_override_fullhelm|af_override_head|af_override_weapons),
       (try_end),
       
       (init_position, pos2),
       (cur_tableau_set_camera_parameters, 1, 6, 6, 10, 10000),

       (init_position, pos5),
       (assign, ":cam_height", 105),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 450),
       (assign, ":camera_yaw", 15),
       (assign, ":camera_pitch", -18),
       (assign, ":animation", anim_stand_man),
       
       (troop_get_inventory_slot, ":horse_item", ":troop_no", ek_horse),
       (try_begin),
         (gt, ":horse_item", 0),
         (eq, ":hide_weapons", 0),
         (cur_tableau_add_horse, ":horse_item", pos2, "anim_horse_stand", 0),
         (assign, ":animation", "anim_ride_0"),
         (assign, ":camera_yaw", 23),
         (assign, ":cam_height", 150),
         (assign, ":camera_distance", 550),
       (try_end),
       (position_set_z, pos5, ":cam_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

       (try_begin),
         (troop_is_hero, ":troop_no"),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", -1),
       (else_try),
         (store_mul, ":random_seed", ":troop_no", 126233),
         (val_mod, ":random_seed", 1000),
         (val_add, ":random_seed", 1),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", ":random_seed"),
       (try_end),
       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30), 
       (position_rotate_x, pos8, -60), 
       (cur_tableau_add_sun_light, pos8, 175,150,125),
     ]),

  #script_get_prosperity_text_to_s50
  # INPUT: center_no
  # OUTPUT: none
  ("get_prosperity_text_to_s50",
    [(store_script_param, ":center_no", 1),
     (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
     (val_div, ":prosperity", 20),
	 
     (try_begin),(eq, ":prosperity", 0),(str_store_string, s50, "@Very Poor"),
     (else_try) ,(eq, ":prosperity", 1),(str_store_string, s50, "@Poor"),
     (else_try) ,(eq, ":prosperity", 2),(str_store_string, s50, "@Average"),
     (else_try) ,(eq, ":prosperity", 3),(str_store_string, s50, "@Rich"),
     (else_try) ,                       (str_store_string, s50, "@Very Rich"),
     (try_end),
    ]),

  #script_spawn_bandits
  # INPUT: none
  # OUTPUT: none
  ("spawn_bandits",
    [(set_spawn_radius,1),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_mountain_bandits"),
       (lt,":num_parties",14),
       (store_random,":spawn_point",num_mountain_bandit_spawn_points),
       (val_add,":spawn_point","p_mountain_bandit_spawn_point"),
       (spawn_around_party,":spawn_point","pt_mountain_bandits"),
        (party_set_slot, reg0, slot_party_type, spt_bandit), # Added by foxyman, TLD
     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_forest_bandits"),
       (lt,":num_parties",14),
       (store_random,":spawn_point",num_mountain_bandit_spawn_points),
       (val_add,":spawn_point","p_forest_bandit_spawn_point"),
       (spawn_around_party,":spawn_point","pt_forest_bandits"),
     (party_set_slot, reg0, slot_party_type, spt_bandit), # Added by foxyman, TLD
     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_sea_raiders"),
       (lt,":num_parties",14),
       (store_random,":spawn_point",num_sea_raider_spawn_points),
       (val_add,":spawn_point","p_sea_raider_spawn_point_1"),
       (spawn_around_party,":spawn_point","pt_sea_raiders"),
     (party_set_slot, reg0, slot_party_type, spt_bandit), # Added by foxyman, TLD
     (try_end),
##TLD TEST PARTIES
#     (try_begin),
#       (store_num_parties_of_template, ":num_parties", "pt_gondor_war_party"),
#       (lt,":num_parties",3),
#       (store_random,":spawn_point",num_sea_raider_spawn_points),
#       (val_add,":spawn_point","p_mordor_gondor"),
#       (spawn_around_party,":spawn_point","pt_gondor_war_party"),
#     (try_end),
#     (try_begin),
#       (store_num_parties_of_template, ":num_parties", "pt_gondor_war_party"),
#       (lt,":num_parties",3),
#       (store_random,":spawn_point",num_sea_raider_spawn_points),
#       (val_add,":spawn_point","p_harad_gondor"),
#       (spawn_around_party,":spawn_point","pt_gondor_war_party"),
#     (try_end),
#     
#     (try_begin),
#       (store_num_parties_of_template, ":num_parties", "pt_gondor_allies_war_party"),
#       (lt,":num_parties",2),
#       (store_random,":spawn_point",num_sea_raider_spawn_points),
#       (val_add,":spawn_point","p_gondor_test"),
#       (spawn_around_party,":spawn_point","pt_gondor_allies_war_party"),
#     (try_end),     
#     
#     (try_begin),
#       (store_num_parties_of_template, ":num_parties", "pt_rohan_war_party"),
#       (lt,":num_parties",3),
#       (store_random,":spawn_point",num_sea_raider_spawn_points),
#       (val_add,":spawn_point","p_gondor_test"),
#       (spawn_around_party,":spawn_point","pt_rohan_war_party"),
#     (try_end),     
#     (try_begin),
#       (store_num_parties_of_template, ":num_parties", "pt_rohan_war_party"),
#       (lt,":num_parties",2),
#       (store_random,":spawn_point",num_sea_raider_spawn_points),
#       (val_add,":spawn_point","p_isen_rohan"),
#       (spawn_around_party,":spawn_point","pt_rohan_war_party"),
#     (try_end),    
#     
#     (try_begin),
#       (store_num_parties_of_template, ":num_parties", "pt_lorien_war_party"),
#       (lt,":num_parties",2),
#       (store_random,":spawn_point",num_sea_raider_spawn_points),
#       (val_add,":spawn_point","p_gondor_test"),
#       (spawn_around_party,":spawn_point","pt_lorien_war_party"),
#     (try_end),          
#     (try_begin),
#       (store_num_parties_of_template, ":num_parties", "pt_woodelf_war_party"),
#       (lt,":num_parties",2),
#       (store_random,":spawn_point",num_sea_raider_spawn_points),
#       (val_add,":spawn_point","p_gondor_test"),
#       (spawn_around_party,":spawn_point","pt_woodelf_war_party"),
#     (try_end),          
#     (try_begin),
#       (store_num_parties_of_template, ":num_parties", "pt_imladris_war_party"),
#       (lt,":num_parties",2),
#       (store_random,":spawn_point",num_sea_raider_spawn_points),
#       (val_add,":spawn_point","p_gondor_test"),
#       (spawn_around_party,":spawn_point","pt_imladris_war_party"),
#     (try_end),          
#     (try_begin),
#       (store_num_parties_of_template, ":num_parties", "pt_dunedain_war_party"),
#       (lt,":num_parties",2),
#       (store_random,":spawn_point",num_sea_raider_spawn_points),
#       (val_add,":spawn_point","p_gondor_test"),
#       (spawn_around_party,":spawn_point","pt_dunedain_war_party"),
#     (try_end),          
#     (try_begin),
#       (store_num_parties_of_template, ":num_parties", "pt_northmen_war_party"),
#       (lt,":num_parties",2),
#       (store_random,":spawn_point",num_sea_raider_spawn_points),
#       (val_add,":spawn_point","p_gondor_test"),
#       (spawn_around_party,":spawn_point","pt_northmen_war_party"),
#     (try_end),          
#     (try_begin),
#       (store_num_parties_of_template, ":num_parties", "pt_dwarf_war_party"),
#       (lt,":num_parties",2),
#       (store_random,":spawn_point",num_sea_raider_spawn_points),
#       (val_add,":spawn_point","p_gondor_allies_test"),
#       (spawn_around_party,":spawn_point","pt_dwarf_war_party"),
#     (try_end),          
#
##evil parties spawn     
#     (try_begin),
#       (store_num_parties_of_template, ":num_parties", "pt_mordor_war_party"),
#       (lt,":num_parties",2),
#       (store_random,":spawn_point",num_sea_raider_spawn_points),
#       (val_add,":spawn_point","p_mordor_gondor"),
#       (spawn_around_party,":spawn_point","pt_mordor_war_party"),
#     (try_end),
#     # (try_begin),
#       # (store_num_parties_of_template, ":num_parties", "pt_isengard_war_party"),
#       # (lt,":num_parties",2),
#       # (store_random,":spawn_point",num_sea_raider_spawn_points),
#       # (val_add,":spawn_point","p_mordor_test"),
#       # (spawn_around_party,":spawn_point","pt_isengard_war_party"),
#     # (try_end),
#     (try_begin),
#       (store_num_parties_of_template, ":num_parties", "pt_isengard_war_party"),
#       (lt,":num_parties",2),
#       (store_random,":spawn_point",num_sea_raider_spawn_points),
#       (val_add,":spawn_point","p_isen_rohan"),
#       (spawn_around_party,":spawn_point","pt_isengard_war_party"),
#     (try_end),     
#     (try_begin),
#       (store_num_parties_of_template, ":num_parties", "pt_harad_war_party"),
#       (lt,":num_parties",2),
#       (store_random,":spawn_point",num_sea_raider_spawn_points),
#       (val_add,":spawn_point","p_harad_gondor"),
#       (spawn_around_party,":spawn_point","pt_harad_war_party"),
#     (try_end),   
#     (try_begin),
#       (store_num_parties_of_template, ":num_parties", "pt_rhun_war_party"),
#       (lt,":num_parties",2),
#       (store_random,":spawn_point",num_sea_raider_spawn_points),
#       (val_add,":spawn_point","p_harad_gondor"),
#       (spawn_around_party,":spawn_point","pt_rhun_war_party"),
#     (try_end),  
#     (try_begin),
#       (store_num_parties_of_template, ":num_parties", "pt_dunland_war_party"),
#       (lt,":num_parties",2),
#       (store_random,":spawn_point",num_sea_raider_spawn_points),
#       (val_add,":spawn_point","p_mordor_test"),
#       (spawn_around_party,":spawn_point","pt_dunland_war_party"),
#     (try_end),     (try_begin),
#       (store_num_parties_of_template, ":num_parties", "pt_khand_war_party"),
#       (lt,":num_parties",2),
#       (store_random,":spawn_point",num_sea_raider_spawn_points),
#       (val_add,":spawn_point","p_mordor_test"),
#       (spawn_around_party,":spawn_point","pt_khand_war_party"),
#     (try_end),     (try_begin),
#       (store_num_parties_of_template, ":num_parties", "pt_corsair_war_party"),
#       (lt,":num_parties",2),
#       (store_random,":spawn_point",num_sea_raider_spawn_points),
#       (val_add,":spawn_point","p_mordor_test"),
#       (spawn_around_party,":spawn_point","pt_corsair_war_party"),
#     (try_end),     (try_begin),
#       (store_num_parties_of_template, ":num_parties", "pt_moria_war_party"),
#       (lt,":num_parties",2),
#       (store_random,":spawn_point",num_sea_raider_spawn_points),
#       (val_add,":spawn_point","p_mordor_test"),
#       (spawn_around_party,":spawn_point","pt_moria_war_party"),
#     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_steppe_bandits"),
       (lt,":num_parties",14),
       (store_random,":spawn_point",num_steppe_bandit_spawn_points),
       (val_add,":spawn_point","p_steppe_bandit_spawn_point"),
       (spawn_around_party,":spawn_point","pt_steppe_bandits"),
     (party_set_slot, reg0, slot_party_type, spt_bandit), # Added by foxyman, TLD
     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_looters"),
       (lt,":num_parties",23),
       (store_random_in_range,":spawn_point",villages_begin,villages_end), #spawn looters twice to have lots of them at the beginning
       (spawn_around_party,":spawn_point","pt_looters"),
       (party_set_slot, reg0, slot_party_type, spt_bandit), # Added by foxyman, TLD
       (assign, ":spawned_party_id", reg0),
       (try_begin),
         (check_quest_active, "qst_deal_with_looters"),
         (party_set_flags, ":spawned_party_id", pf_quest_party, 1),
       (else_try),
         (party_set_flags, ":spawned_party_id", pf_quest_party, 0),
       (try_end),
     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_deserters"),
       (lt,":num_parties",15),
       (set_spawn_radius, 4),
       (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
         (store_random_in_range, ":random_no", 0, 100),
         (lt, ":random_no", 5),
         (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
         (store_troop_faction, ":troop_faction", ":troop_no"),
         (neq, ":troop_faction", "fac_player_supporters_faction"),
         (gt, ":party_no", 0),
         (neg|party_is_in_any_town, ":party_no"),
         (faction_get_slot, ":tier_1_troop", ":troop_faction", slot_faction_deserter_troop),
         (try_begin), # only evil factions have deserters, good ones have -1 for deserter troop
           (ge, ":tier_1_troop", 0),		 
##           (party_get_attached_to, ":attached_party_no", ":party_no"),
##           (lt, ":attached_party_no", 0),#in wilderness
           (spawn_around_party, ":party_no", "pt_deserters"),
           (party_set_slot, reg0, slot_party_type, spt_bandit), # Added by foxyman, TLD
           (assign, ":new_party", reg0),
           (store_character_level, ":level", "trp_player"),
           (store_mul, ":max_number_to_add", ":level", 2),
           (val_add, ":max_number_to_add", 11),
           (store_random_in_range, ":number_to_add", 10, ":max_number_to_add"),
           (party_add_members, ":new_party", ":tier_1_troop", ":number_to_add"),
           (store_random_in_range, ":random_no", 1, 4),
           (try_for_range, ":unused", 0, ":random_no"),
             (party_upgrade_with_xp, ":new_party", 1000000, 0),
           (try_end),
		 (try_end),
##         (str_store_party_name, s1, ":party_no"),
##         (call_script, "script_get_closest_center", ":party_no"),
##         (try_begin),
##           (gt, reg0, 0),
##           (str_store_party_name, s2, reg0),
##         (else_try),
##           (str_store_string, s2, "@unknown place"),
##         (try_end),
##         (assign, reg1, ":number_to_add"),
##         (display_message, "@{reg1} Deserters spawned from {s1}, near {s2}."),
       (try_end),
     (try_end),
     ]),

  #script_count_mission_casualties_from_agents
  # INPUT: none
  # OUTPUT: none
  ("count_mission_casualties_from_agents",
    [(party_clear, "p_player_casualties"),
     (party_clear, "p_enemy_casualties"),
     (party_clear, "p_ally_casualties"),
     (assign, "$any_allies_at_the_last_battle", 0),
     (try_for_agents, ":cur_agent"),
       (agent_is_human, ":cur_agent"),
       (agent_get_party_id, ":agent_party", ":cur_agent"),
       (try_begin),
         (neq, ":agent_party", "p_main_party"),
         (agent_is_ally, ":cur_agent"),
         (assign, "$any_allies_at_the_last_battle", 1),
       (try_end),
       (neg|agent_is_alive, ":cur_agent"),
       (agent_get_troop_id, ":agent_troop_id", ":cur_agent"),
       (try_begin),
         (eq, ":agent_party", "p_main_party"),
         (party_add_members, "p_player_casualties", ":agent_troop_id", 1),
         (try_begin),
           (agent_is_wounded, ":cur_agent"),
           (party_wound_members, "p_player_casualties", ":agent_troop_id", 1),
         (try_end),
       (else_try),
         (agent_is_ally, ":cur_agent"),
         (party_add_members, "p_ally_casualties", ":agent_troop_id", 1),
         (try_begin),
           (agent_is_wounded, ":cur_agent"),
           (party_wound_members, "p_ally_casualties", ":agent_troop_id", 1),
         (try_end),
       (else_try),
         (party_add_members, "p_enemy_casualties", ":agent_troop_id", 1),
         (try_begin),
           (agent_is_wounded, ":cur_agent"),
           (party_wound_members, "p_enemy_casualties", ":agent_troop_id", 1),
         (try_end),
       (try_end),
     (try_end),
     ]),

  #script_get_max_skill_of_player_party
  # INPUT: arg1 = skill_no
  # OUTPUT: reg0 = max_skill, reg1 = skill_owner_troop_no
  ("get_max_skill_of_player_party",
    [(store_script_param, ":skill_no", 1),
     (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
     (store_skill_level, ":max_skill", ":skill_no", "trp_player"),
     (assign, ":skill_owner", "trp_player"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
       (troop_is_hero, ":stack_troop"),
       (neg|troop_is_wounded, ":stack_troop"),
       (store_skill_level, ":cur_skill", ":skill_no", ":stack_troop"),
       (gt, ":cur_skill", ":max_skill"),
       (assign, ":max_skill", ":cur_skill"),
       (assign, ":skill_owner", ":stack_troop"),
     (try_end),
     (assign, reg0, ":max_skill"),
     (assign, reg1, ":skill_owner"),
     ]),

  #script_upgrade_hero_party
  # INPUT: arg1 = party_id, arg2 = xp_amount
  ("upgrade_hero_party",
    [(store_script_param, ":party_no", 1),
     (store_script_param, ":xp_amount", 2),
     (party_upgrade_with_xp, ":party_no", ":xp_amount", 0),
     ]),

  #script_get_improvement_details
  # INPUT: arg1 = improvement
  # OUTPUT: reg0 = base_cost
  ("get_improvement_details",
    [(store_script_param, ":improvement_no", 1),
     (try_begin),
       (eq, ":improvement_no", slot_center_has_manor),
       (str_store_string, s0, "@Manor"),
       (str_store_string, s1, "@A manor lets you rest at the village and pay your troops half wages while you rest."),
       (assign, reg0, 8000),
     (else_try),
       (eq, ":improvement_no", slot_center_has_fish_pond),
       (str_store_string, s0, "@Mill"),
       (str_store_string, s1, "@A mill increases village prosperity by 5%."),
       (assign, reg0, 6000),
     (else_try),
       (eq, ":improvement_no", slot_center_has_watch_tower),
       (str_store_string, s0, "@Watch Tower"),
       (str_store_string, s1, "@A watch tower lets the villagers raise alarm earlier. The time it takes for enemies to loot the village increases by 25%."),
       (assign, reg0, 5000),
     (else_try),
       (eq, ":improvement_no", slot_center_has_school),
       (str_store_string, s0, "@School"),
       (str_store_string, s1, "@A shool increases the loyality of the villagers to you by +1 every month."),
       (assign, reg0, 9000),
     (else_try),
       (eq, ":improvement_no", slot_center_has_messenger_post),
       (str_store_string, s0, "@Messenger Post"),
       (str_store_string, s1, "@A messenger post lets the inhabitants send you a message whenever enemies are nearby, even if you are far away from here."),
       (assign, reg0, 4000),
     (else_try),
       (eq, ":improvement_no", slot_center_has_prisoner_tower),
       (str_store_string, s0, "@Prison Tower"),
       (str_store_string, s1, "@A prison tower reduces the chance of captives held here running away successfully."),
       (assign, reg0, 7000),
     (try_end),
     ]),
  
  #script_cf_troop_agent_is_alive
  # INPUT: arg1 = troop_id
  ("cf_troop_agent_is_alive",
    [(store_script_param, ":troop_no", 1),
     (assign, ":alive_count", 0),
     (try_for_agents, ":cur_agent"),
       (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
       (eq, ":troop_no", ":cur_agent_troop"),
       (agent_is_alive, ":cur_agent"),
       (val_add, ":alive_count", 1),
     (try_end),
     (gt, ":alive_count", 0),
     ]),

  #script_cf_village_recruit_volunteers_cond
  # INPUT: none
  # OUTPUT: none
  ("cf_village_recruit_volunteers_cond",
    [(neg|party_slot_eq, "$current_town", slot_village_state, svs_looted),
     (neg|party_slot_eq, "$current_town", slot_village_state, svs_being_raided),
     (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
     (store_faction_of_party, ":village_faction", "$current_town"),
     (party_get_slot, ":center_relation", "$current_town", slot_center_player_relation),
     (store_relation, ":village_faction_relation", ":village_faction", "fac_player_faction"),
     (ge, ":center_relation", 0),
     (this_or_next|ge, ":center_relation", 5),
     (this_or_next|eq, ":village_faction", "$players_kingdom"),
     (this_or_next|ge, ":village_faction_relation", 0),
     (this_or_next|eq, ":village_faction", "$supported_pretender_old_faction"),
     (             eq, "$players_kingdom", 0),
     (party_slot_ge, "$current_town", slot_center_volunteer_troop_amount, 0),
     (party_slot_ge, "$current_town", slot_center_volunteer_troop_type, 1),
     (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
     (ge, ":free_capacity", 1),
     ]),

  #script_village_recruit_volunteers_recruit
  # INPUT: none
  # OUTPUT: none
  ("village_recruit_volunteers_recruit",
    [(party_get_slot, ":volunteer_troop", "$current_town", slot_center_volunteer_troop_type),
     (party_get_slot, ":volunteer_amount", "$current_town", slot_center_volunteer_troop_amount),
     (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
     (val_min, ":volunteer_amount", ":free_capacity"),
     (store_troop_gold, ":gold", "trp_player"),
     (store_div, ":gold_capacity", ":gold", 10),#10 denars per man
     (val_min, ":volunteer_amount", ":gold_capacity"),
     (party_add_members, "p_main_party", ":volunteer_troop", ":volunteer_amount"),
     (party_set_slot, "$current_town", slot_center_volunteer_troop_amount, -1),
     (store_mul, ":cost", ":volunteer_amount", 10),#10 denars per man
     (troop_remove_gold, "trp_player", ":cost"),
     ]),

  #script_get_troop_item_amount
  # INPUT: arg1 = troop_no, arg2 = item_no
  # OUTPUT: reg0 = item_amount
  ("get_troop_item_amount",
    [(store_script_param, ":troop_no", 1),
     (store_script_param, ":item_no", 2),
     (troop_get_inventory_capacity, ":inv_cap", ":troop_no"),
     (assign, ":count", 0),
     (try_for_range, ":i_slot", 0, ":inv_cap"),
       (troop_get_inventory_slot, ":cur_item", ":troop_no", ":i_slot"),
       (eq, ":cur_item", ":item_no"),
       (val_add, ":count", 1),
     (try_end),
     (assign, reg0, ":count"),
     ]),

  #script_get_name_from_dna_to_s50
  # INPUT: arg1 = dna
  # OUTPUT: s50 = name
  ("get_name_from_dna_to_s50",
    [(store_script_param, ":dna", 1),
     (store_sub, ":num_names", names_end, names_begin),
     (store_sub, ":num_surnames", surnames_end, surnames_begin),
     (assign, ":selected_name", ":dna"),
     (val_mod, ":selected_name", ":num_names"),
     (assign, ":selected_surname", ":dna"),
     (val_div, ":selected_surname", ":num_names"),
     (val_mod, ":selected_surname", ":num_surnames"),
     (val_add, ":selected_name", names_begin),
     (val_add, ":selected_surname", surnames_begin),
     (str_store_string, s50, ":selected_name"),
     (str_store_string, s50, ":selected_surname"),
     ]),
     
  #script_change_center_prosperity
  # INPUT: arg1 = center_no, arg2 = difference
  # OUTPUT: none
  ("change_center_prosperity",
    [(store_script_param, ":center_no", 1),
     (store_script_param, ":difference", 2),
     (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
     (store_add, ":new_prosperity", ":prosperity", ":difference"),
     (val_clamp, ":new_prosperity", 0, 100),
     (store_div, ":old_state", ":prosperity", 20),
     (store_div, ":new_state", ":new_prosperity", 20),
     (try_begin),
       (neq, ":old_state", ":new_state"),
       (str_store_party_name_link, s2, ":center_no"),
       (call_script, "script_get_prosperity_text_to_s50", ":center_no"),
       (str_store_string, s3, s50),
       (party_set_slot, ":center_no", slot_town_prosperity, ":new_prosperity"),
       (call_script, "script_get_prosperity_text_to_s50", ":center_no"),
       (str_store_string, s4, s50),
       (display_message, "@Prosperity of {s2} has changed from {s3} to {s4}."),
       (call_script, "script_update_center_notes", ":center_no"),
     (else_try),
       (party_set_slot, ":center_no", slot_town_prosperity, ":new_prosperity"),
     (try_end),
     ]),

  #script_get_center_ideal_prosperity
  # INPUT: arg1 = center_no
  # OUTPUT: reg0 = ideal_prosperity
  ("get_center_ideal_prosperity",
    [(store_script_param, ":center_no", 1),
     (assign, ":ideal", 40),
     (try_begin),
       (is_between, ":center_no", villages_begin, villages_end),
       (try_begin),
         (party_slot_eq, ":center_no", slot_center_has_fish_pond, 1),
         (val_add, ":ideal", 5),
       (try_end),
       (party_get_slot, ":land_quality", ":center_no", slot_village_land_quality),
       (val_mul, ":land_quality", 3),
       (val_add, ":ideal", ":land_quality"),
       (party_get_slot, ":num_cattle", ":center_no", slot_village_number_of_cattle),
       (val_div, ":num_cattle", 20),
       (val_add, ":ideal", ":num_cattle"),
     (else_try),
       (try_for_range, ":village_no", villages_begin, villages_end),
         (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),
         (party_get_slot, ":prosperity", ":village_no", slot_town_prosperity),
         (val_div, ":prosperity", 20),
         (val_add, ":ideal", ":prosperity"),
       (try_end),
     (try_end),
     (assign, reg0, ":ideal"),
     ]),

  #script_get_poorest_village_of_faction
  # INPUT: arg1 = center_no
  # OUTPUT: reg0 = ideal_prosperity
  ("get_poorest_village_of_faction",
    [(store_script_param, ":faction_no", 1),
     (assign, ":min_prosperity_village", -1),
     (assign, ":min_prosperity", 101),
     (try_for_range, ":village_no", villages_begin, villages_end),
       (store_faction_of_party, ":village_faction", ":village_no"),
       (eq, ":village_faction", ":faction_no"),
       (party_get_slot, ":prosperity", ":village_no", slot_town_prosperity),
       (lt, ":prosperity", ":min_prosperity"),
       (assign, ":min_prosperity", ":prosperity"),
       (assign, ":min_prosperity_village", ":village_no"),
     (try_end),
     (assign, reg0, ":min_prosperity_village"),
     ]),

  #script_troop_add_gold
  # INPUT: arg1 = troop_no, arg2 = amount
  # OUTPUT: none
  ("troop_add_gold",
    [(store_script_param, ":troop_no", 1),
     (store_script_param, ":amount", 2),
     (troop_add_gold, ":troop_no", ":amount"),
     (try_begin),
       (eq, ":troop_no", "trp_player"),
       #(play_sound, "snd_money_received"),
     (try_end),
     ]),     

#NPC companion changes begin
  ("initialize_npcs",
    [
# set strings
#good companions
        # Mablung
        (troop_set_slot, "trp_npc1", slot_troop_morality_type, tmt_egalitarian),
        (troop_set_slot, "trp_npc1", slot_troop_morality_value, 3),
        (troop_set_slot, "trp_npc1", slot_troop_2ary_morality_type, tmt_honest),
        (troop_set_slot, "trp_npc1", slot_troop_2ary_morality_value, 2),
        (troop_set_slot, "trp_npc1", slot_troop_personalityclash_object, "trp_npc9"), #Gulm/none
        (troop_set_slot, "trp_npc1", slot_troop_personalityclash2_object, "trp_npc10"),  #Durgash/none
        (troop_set_slot, "trp_npc1", slot_troop_personalitymatch_object, "trp_npc6"),  #Luevanna
        (troop_set_slot, "trp_npc1", slot_troop_home, "p_town_west_osgiliath"),
        (troop_set_slot, "trp_npc1", slot_troop_payment_request, 2000),
        (troop_set_slot, "trp_npc1", slot_troop_cur_center, "p_town_henneth_annun"),  #TLD
        (troop_set_slot, "trp_npc1", slot_troop_rank_request, 3),  #TLD

        # Cirdil
        (troop_set_slot, "trp_npc2", slot_troop_morality_type, tmt_egalitarian),
        (troop_set_slot, "trp_npc2", slot_troop_morality_value, 2),  
        (troop_set_slot, "trp_npc2", slot_troop_2ary_morality_type, -1),  
        (troop_set_slot, "trp_npc2", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc2", slot_troop_personalityclash_object, "trp_npc9"), #Gulm/none
        (troop_set_slot, "trp_npc2", slot_troop_personalityclash2_object, "trp_npc10"),  #Durgash/none
        (troop_set_slot, "trp_npc2", slot_troop_personalitymatch_object, "trp_npc1"),  #Mablung
        (troop_set_slot, "trp_npc2", slot_troop_home, "p_town_minas_morgul"),
        (troop_set_slot, "trp_npc2", slot_troop_payment_request, 100), 
        (troop_set_slot, "trp_npc2", slot_troop_cur_center, "p_town_minas_tirith"),  #TLD
        (troop_set_slot, "trp_npc2", slot_troop_rank_request, 0),  #TLD

        # Ulfas
        (troop_set_slot, "trp_npc3", slot_troop_morality_type, tmt_aristocratic),
        (troop_set_slot, "trp_npc3", slot_troop_morality_value, 4),  
        (troop_set_slot, "trp_npc3", slot_troop_2ary_morality_type, -1), 
        (troop_set_slot, "trp_npc3", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc3", slot_troop_personalityclash_object, "trp_npc1"), #Mablung
        (troop_set_slot, "trp_npc3", slot_troop_personalityclash2_object, "trp_npc10"),  #Durgash/none
        (troop_set_slot, "trp_npc3", slot_troop_personalitymatch_object, "trp_npc4"),  #G�lmyn�
        (troop_set_slot, "trp_npc3", slot_troop_home, "p_ford_fangorn"),
        (troop_set_slot, "trp_npc3", slot_troop_payment_request, 1200), 
        (troop_set_slot, "trp_npc3", slot_troop_cur_center, "p_town_west_emnet"),  #TLD
        (troop_set_slot, "trp_npc3", slot_troop_rank_request, 1),  #TLD

        # G�lmyn�
        (troop_set_slot, "trp_npc4", slot_troop_morality_type, tmt_aristocratic),
        (troop_set_slot, "trp_npc4", slot_troop_morality_value, -1),  
        (troop_set_slot, "trp_npc4", slot_troop_2ary_morality_type, tmt_honest), 
        (troop_set_slot, "trp_npc4", slot_troop_2ary_morality_value, 1),
        (troop_set_slot, "trp_npc4", slot_troop_personalityclash_object, "trp_npc9"), #Gulm/none
        (troop_set_slot, "trp_npc4", slot_troop_personalityclash2_object, "trp_npc10"),  #Durgash/none
        (troop_set_slot, "trp_npc4", slot_troop_personalitymatch_object, "trp_npc8"),  #Faniul
        (troop_set_slot, "trp_npc4", slot_troop_home, "p_ford_brown_lands"), #Field of Celebrant ford
        (troop_set_slot, "trp_npc4", slot_troop_payment_request, 3000), 
        (troop_set_slot, "trp_npc4", slot_troop_cur_center, "p_town_edoras"),  #TLD
        (troop_set_slot, "trp_npc4", slot_troop_rank_request, 4),  #TLD

        # Glorfindel
        (troop_set_slot, "trp_npc5", slot_troop_morality_type, tmt_honest),
        (troop_set_slot, "trp_npc5", slot_troop_morality_value, 3),
        (troop_set_slot, "trp_npc5", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc5", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc5", slot_troop_personalityclash_object, "trp_npc9"), #Gulm/none
        (troop_set_slot, "trp_npc5", slot_troop_personalityclash2_object, "trp_npc10"),  #Durgash/none
        (troop_set_slot, "trp_npc5", slot_troop_personalitymatch_object, "trp_npc9"),  #Gulm/none
        (troop_set_slot, "trp_npc5", slot_troop_home, "p_town_isengard"),
        (troop_set_slot, "trp_npc5", slot_troop_payment_request, 5000),
        (troop_set_slot, "trp_npc5", slot_troop_cur_center, "p_town_caras_galadhon"),  #TLD
        (troop_set_slot, "trp_npc5", slot_troop_rank_request, 7),  #TLD

        # Luevanna
        (troop_set_slot, "trp_npc6", slot_troop_morality_type, -1),
        (troop_set_slot, "trp_npc6", slot_troop_morality_value, 0),
        (troop_set_slot, "trp_npc6", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc6", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc6", slot_troop_personalityclash_object, "trp_npc7"), #K�li
        (troop_set_slot, "trp_npc6", slot_troop_personalityclash2_object, "trp_npc10"),  #Durgash/none
        (troop_set_slot, "trp_npc6", slot_troop_personalitymatch_object, "trp_npc5"),  #Glorfindel
        (troop_set_slot, "trp_npc6", slot_troop_home, "p_town_dol_guldur"),
        (troop_set_slot, "trp_npc6", slot_troop_payment_request, 0),
        (troop_set_slot, "trp_npc6", slot_troop_cur_center, "p_town_thranduils_halls"),  #TLD
        (troop_set_slot, "trp_npc6", slot_troop_rank_request, 0),  #TLD

        # K�li
        (troop_set_slot, "trp_npc7", slot_troop_morality_type, tmt_aristocratic),
        (troop_set_slot, "trp_npc7", slot_troop_morality_value, 3),
        (troop_set_slot, "trp_npc7", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc7", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc7", slot_troop_personalityclash_object, "trp_npc5"), #Glorfindel
        (troop_set_slot, "trp_npc7", slot_troop_personalityclash2_object, "trp_npc6"),  #Luevanna
        (troop_set_slot, "trp_npc7", slot_troop_personalitymatch_object, "trp_npc8"),  #Faniul
        (troop_set_slot, "trp_npc7", slot_troop_home, "p_town_moria"),
        (troop_set_slot, "trp_npc7", slot_troop_payment_request, 800),
        (troop_set_slot, "trp_npc7", slot_troop_cur_center, "p_town_erebor"),  #TLD
        (troop_set_slot, "trp_npc7", slot_troop_rank_request, 1),  #TLD

        # Faniul
        (troop_set_slot, "trp_npc8", slot_troop_morality_type, tmt_egalitarian),
        (troop_set_slot, "trp_npc8", slot_troop_morality_value, 4),
        (troop_set_slot, "trp_npc8", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc8", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc8", slot_troop_personalityclash_object, "trp_npc3"), #Ulfas
        (troop_set_slot, "trp_npc8", slot_troop_personalityclash2_object, "trp_npc10"),  #Durgash/none
        (troop_set_slot, "trp_npc8", slot_troop_personalitymatch_object, "trp_npc7"),  #K�li
        (troop_set_slot, "trp_npc8", slot_troop_home, "p_town_beorn_house"),
        (troop_set_slot, "trp_npc8", slot_troop_payment_request, 300),
        (troop_set_slot, "trp_npc8", slot_troop_cur_center, "p_town_dale"),  #TLD
        (troop_set_slot, "trp_npc8", slot_troop_rank_request, 0),  #TLD

#evil companions
        # Gulm
        (troop_set_slot, "trp_npc9", slot_troop_morality_type, -1),
        (troop_set_slot, "trp_npc9", slot_troop_morality_value, 0),
        (troop_set_slot, "trp_npc9", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc9", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc9", slot_troop_personalityclash_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc9", slot_troop_personalityclash2_object, "trp_npc2"), #Cirdil/none
        (troop_set_slot, "trp_npc9", slot_troop_personalitymatch_object, "trp_npc1"),  #Mablung/none
        (troop_set_slot, "trp_npc9", slot_troop_home, -1), #no "home" speeches
        (troop_set_slot, "trp_npc9", slot_troop_payment_request, 2000),
        (troop_set_slot, "trp_npc9", slot_troop_cur_center, "p_town_urukhai_h_camp"),  #TLD
        (troop_set_slot, "trp_npc9", slot_troop_rank_request, 3),  #TLD

        # Durgash
        (troop_set_slot, "trp_npc10", slot_troop_morality_type, -1),
        (troop_set_slot, "trp_npc10", slot_troop_morality_value, 0),
        (troop_set_slot, "trp_npc10", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc10", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc10", slot_troop_personalityclash_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc10", slot_troop_personalityclash2_object, "trp_npc2"), #Cirdil/none
        (troop_set_slot, "trp_npc10", slot_troop_personalitymatch_object, "trp_npc1"),  #Mablung/none
        (troop_set_slot, "trp_npc10", slot_troop_home, -1),
        (troop_set_slot, "trp_npc10", slot_troop_payment_request, 800),
        (troop_set_slot, "trp_npc10", slot_troop_cur_center, "p_town_isengard"),  #TLD
        (troop_set_slot, "trp_npc10", slot_troop_rank_request, 1),  #TLD

        # Ufthak
        (troop_set_slot, "trp_npc11", slot_troop_morality_type, -1),
        (troop_set_slot, "trp_npc11", slot_troop_morality_value, 0),
        (troop_set_slot, "trp_npc11", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc11", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc11", slot_troop_personalityclash_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc11", slot_troop_personalityclash2_object, "trp_npc2"), #Cirdil/none
        (troop_set_slot, "trp_npc11", slot_troop_personalitymatch_object, "trp_npc1"),  #Mablung/none
        (troop_set_slot, "trp_npc11", slot_troop_home, -1),
        (troop_set_slot, "trp_npc11", slot_troop_payment_request, 100),
        (troop_set_slot, "trp_npc11", slot_troop_cur_center, "p_town_cirith_ungol"),  #TLD
        (troop_set_slot, "trp_npc11", slot_troop_rank_request, 0),  #TLD

        # Gorbag
        (troop_set_slot, "trp_npc12", slot_troop_morality_type, -1),
        (troop_set_slot, "trp_npc12", slot_troop_morality_value, 0),
        (troop_set_slot, "trp_npc12", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc12", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc12", slot_troop_personalityclash_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc12", slot_troop_personalityclash2_object, "trp_npc2"), #Cirdil/none
        (troop_set_slot, "trp_npc12", slot_troop_personalitymatch_object, "trp_npc1"),  #Mablung/none
        (troop_set_slot, "trp_npc12", slot_troop_home, -1),
        (troop_set_slot, "trp_npc12", slot_troop_payment_request, 1800),
        (troop_set_slot, "trp_npc12", slot_troop_cur_center, "p_town_minas_morgul"),  #TLD
        (troop_set_slot, "trp_npc12", slot_troop_rank_request, 3),  #TLD

        # Badhark�n
        (troop_set_slot, "trp_npc13", slot_troop_morality_type, -1),
        (troop_set_slot, "trp_npc13", slot_troop_morality_value, 0),
        (troop_set_slot, "trp_npc13", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc13", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc13", slot_troop_personalityclash_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc13", slot_troop_personalityclash2_object, "trp_npc2"), #Cirdil/none
        (troop_set_slot, "trp_npc13", slot_troop_personalitymatch_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc13", slot_troop_home, -1),
        (troop_set_slot, "trp_npc13", slot_troop_payment_request, 4000),
        (troop_set_slot, "trp_npc13", slot_troop_cur_center, "p_town_harad_camp"),  #TLD
        (troop_set_slot, "trp_npc13", slot_troop_rank_request, 5),  #TLD

        # Fuldimir
        (troop_set_slot, "trp_npc14", slot_troop_morality_type, -1),
        (troop_set_slot, "trp_npc14", slot_troop_morality_value, 0),
        (troop_set_slot, "trp_npc14", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc14", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc14", slot_troop_personalityclash_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc14", slot_troop_personalityclash2_object, "trp_npc2"), #Cirdil/none
        (troop_set_slot, "trp_npc14", slot_troop_personalitymatch_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc14", slot_troop_home, -1),
        (troop_set_slot, "trp_npc14", slot_troop_payment_request, 300),
        (troop_set_slot, "trp_npc14", slot_troop_cur_center, "p_town_umbar_camp"),  #TLD
        (troop_set_slot, "trp_npc14", slot_troop_rank_request, 0),  #TLD

        # Bolzog
        (troop_set_slot, "trp_npc15", slot_troop_morality_type, -1),
        (troop_set_slot, "trp_npc15", slot_troop_morality_value, 0),
        (troop_set_slot, "trp_npc15", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc15", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc15", slot_troop_personalityclash_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc15", slot_troop_personalityclash2_object, "trp_npc2"), #Cirdil/none
        (troop_set_slot, "trp_npc15", slot_troop_personalitymatch_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc15", slot_troop_home, -1),
        (troop_set_slot, "trp_npc15", slot_troop_payment_request, 500),
        (troop_set_slot, "trp_npc15", slot_troop_cur_center, "p_town_moria"),  #TLD
        (troop_set_slot, "trp_npc15", slot_troop_rank_request, 1),  #TLD

        # Varfang
        (troop_set_slot, "trp_npc16", slot_troop_morality_type, -1),
        (troop_set_slot, "trp_npc16", slot_troop_morality_value, 0),
        (troop_set_slot, "trp_npc16", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc16", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc16", slot_troop_personalityclash_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc16", slot_troop_personalityclash2_object, "trp_npc2"), #Cirdil/none
        (troop_set_slot, "trp_npc16", slot_troop_personalitymatch_object, "trp_npc1"),  #Mablung/none
        (troop_set_slot, "trp_npc16", slot_troop_home, -1),
        (troop_set_slot, "trp_npc16", slot_troop_payment_request, 1200),
        (troop_set_slot, "trp_npc16", slot_troop_cur_center, "p_town_north_rhun_camp"),  #TLD
        (troop_set_slot, "trp_npc16", slot_troop_rank_request, 2),  #TLD

#additional companions        
        # D�mborn
        (troop_set_slot, "trp_npc17", slot_troop_morality_type, -1),
        (troop_set_slot, "trp_npc17", slot_troop_morality_value, 0), 
        (troop_set_slot, "trp_npc17", slot_troop_2ary_morality_type, -1), 
        (troop_set_slot, "trp_npc17", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc17", slot_troop_personalityclash_object, "trp_npc9"), #Gulm/none
        (troop_set_slot, "trp_npc17", slot_troop_personalityclash2_object, "trp_npc10"),  #Durgash/none
        (troop_set_slot, "trp_npc17", slot_troop_personalitymatch_object, "trp_npc6"),  #Luevanna
        (troop_set_slot, "trp_npc17", slot_troop_home, "p_town_cerin_dolen"),
        (troop_set_slot, "trp_npc17", slot_troop_payment_request, 400),
        (troop_set_slot, "trp_npc17", slot_troop_cur_center, "p_town_woodsmen_village"),  #TLD
        (troop_set_slot, "trp_npc17", slot_troop_rank_request, 0),  #TLD

        (store_sub, "$number_of_npc_slots", slot_troop_strings_end, slot_troop_intro), # 131-101=30 strings per NPC 
        (store_sub, ":total_companions", companions_end, companions_begin),
        (try_begin),
          (store_sub, reg1, "str_companion_strings_end", "str_npc1_intro"), #total actual strings
          (store_mul, reg2, "$number_of_npc_slots", ":total_companions"), #total strings needed
          (neq, reg1, reg2),
          (display_message, "@ERROR: Companion strings actual/needed: {reg1}/{reg2}", 0xFFFF2222),
        (try_end),
        
        (try_for_range, ":npc", companions_begin, companions_end),
            (try_for_range, ":slot_addition", 0, "$number_of_npc_slots"),
                (store_add, ":slot", ":slot_addition", slot_troop_intro),
                
                (store_mul, ":string_addition", ":slot_addition", ":total_companions"), #MV: was 16
                (store_add, ":string", "str_npc1_intro", ":string_addition"), 
                (val_add, ":string", ":npc"),
                (val_sub, ":string", companions_begin),

                (troop_set_slot, ":npc", ":slot", ":string"),
            (try_end),
        (try_end),
#Troop commentary changes begin
        (try_for_range, ":lord", "trp_knight_1_1", "trp_heroes_end"),
            (store_random_in_range, ":reputation", 0, 8),
            (try_begin),
                (eq, ":reputation", 0),
                (assign, ":reputation", 1),
            (try_end),
            (troop_set_slot, ":lord", slot_lord_reputation_type, ":reputation"),
        (try_end),
#Troop commentary changes end

#Post 0907 changes begin
        (call_script, "script_add_log_entry", logent_game_start, "trp_player", -1, -1, -1),
#Post 0907 changes end

#Rebellion changes begin
        (troop_set_slot, "trp_kingdom_1_pretender", slot_troop_original_faction, "fac_gondor"),
        (troop_set_slot, "trp_kingdom_2_pretender", slot_troop_original_faction, "fac_rohan"),
        (troop_set_slot, "trp_kingdom_3_pretender", slot_troop_original_faction, "fac_isengard"),
        (troop_set_slot, "trp_kingdom_4_pretender", slot_troop_original_faction, "fac_mordor"),
        (troop_set_slot, "trp_kingdom_5_pretender", slot_troop_original_faction, "fac_harad"),

        (troop_set_slot, "trp_kingdom_1_pretender", slot_troop_support_base,     "p_town_dol_amroth"), #suno
        (troop_set_slot, "trp_kingdom_2_pretender", slot_troop_support_base,     "p_town_edoras"), #curaw
        (troop_set_slot, "trp_kingdom_3_pretender", slot_troop_support_base,     "p_town_minas_morgul"), #town_18
        (troop_set_slot, "trp_kingdom_4_pretender", slot_troop_support_base,     "p_town_hornburg"), #wercheg
        (troop_set_slot, "trp_kingdom_5_pretender", slot_troop_support_base,     "p_town_linhir"), #veluca
        (try_for_range, ":pretender", pretenders_begin, pretenders_end),
            (troop_set_slot, ":pretender", slot_lord_reputation_type, lrep_none),
        (try_end),
#Rebellion changes end
     ]),

  ("objectionable_action",
    [
        (store_script_param_1, ":action_type"),
        (store_script_param_2, ":action_string"),

#        (str_store_string, 12, ":action_string"),
#        (display_message, "@Objectionable action check: {s12}"),

        (assign, ":grievance_minimum", -2),
        (assign, ":npc_last_displayed", 0),
        (try_for_range, ":npc", companions_begin, companions_end),
            (main_party_has_troop, ":npc"),

###Primary morality check
            (try_begin),
                (troop_slot_eq, ":npc", slot_troop_morality_type, ":action_type"),
                (troop_get_slot, ":value", ":npc", slot_troop_morality_value),
                (try_begin),
                    (troop_slot_eq, ":npc", slot_troop_morality_state, tms_acknowledged),
# npc is betrayed, major penalty to player honor and morale
                    (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                    (val_mul, ":value", 2),
                    (val_add, ":grievance", ":value"),
                    (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),
                (else_try),
                    (this_or_next|troop_slot_eq, ":npc", slot_troop_morality_state, tms_dismissed),
                        (eq, "$disable_npc_complaints", 1),
# npc is quietly disappointed
                    (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                    (val_add, ":grievance", ":value"),
                    (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),
                (else_try),
# npc raises the issue for the first time
                    (troop_slot_eq, ":npc", slot_troop_morality_state, tms_no_problem),
                    (gt, ":value", ":grievance_minimum"),
                    (assign, "$npc_with_grievance", ":npc"),
                    (assign, "$npc_grievance_string", ":action_string"),
                    (assign, "$npc_grievance_slot", slot_troop_morality_state),
                    (assign, ":grievance_minimum", ":value"),
                    (assign, "$npc_praise_not_complaint", 0),
                    (try_begin),
                        (lt, ":value", 0),
                        (assign, "$npc_praise_not_complaint", 1),
                    (try_end),
                (try_end),



###Secondary morality check
            (else_try),
                (troop_slot_eq, ":npc", slot_troop_2ary_morality_type, ":action_type"),
                (troop_get_slot, ":value", ":npc", slot_troop_2ary_morality_value),
                (try_begin),
                    (troop_slot_eq, ":npc", slot_troop_2ary_morality_state, tms_acknowledged),
# npc is betrayed, major penalty to player honor and morale
                    (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                    (val_mul, ":value", 2),
                    (val_add, ":grievance", ":value"),
                    (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),
                (else_try),
                    (this_or_next|troop_slot_eq, ":npc", slot_troop_2ary_morality_state, tms_dismissed),
                        (eq, "$disable_npc_complaints", 1),
# npc is quietly disappointed
                    (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                    (val_add, ":grievance", ":value"),
                    (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),
                (else_try),
# npc raises the issue for the first time
                    (troop_slot_eq, ":npc", slot_troop_2ary_morality_state, tms_no_problem),
                    (gt, ":value", ":grievance_minimum"),
                    (assign, "$npc_with_grievance", ":npc"),
                    (assign, "$npc_grievance_string", ":action_string"),
                    (assign, "$npc_grievance_slot", slot_troop_2ary_morality_state),
                    (assign, ":grievance_minimum", ":value"),
                    (assign, "$npc_praise_not_complaint", 0),
                    (try_begin),
                        (lt, ":value", 0),
                        (assign, "$npc_praise_not_complaint", 1),
                    (try_end),
                (try_end),
            (try_end),

            (try_begin),
                (gt, "$npc_with_grievance", 0),
                (eq, "$npc_praise_not_complaint", 0),
                (neq, "$npc_with_grievance", ":npc_last_displayed"),                
                (str_store_troop_name, 4, "$npc_with_grievance"),
                (display_message, "@{s4} looks upset."),
                (assign, ":npc_last_displayed", "$npc_with_grievance"),
            (try_end),

        (try_end),        


     ]),


  ("post_battle_personality_clash_check",
[
#            (display_message, "@Post-victory personality clash check"),
            (try_for_range, ":npc", companions_begin, companions_end),
                (eq, "$disable_npc_complaints", 0),

                (main_party_has_troop, ":npc"),
                (neg|troop_is_wounded, ":npc"),

                (troop_get_slot, ":other_npc", ":npc", slot_troop_personalityclash2_object),
                (main_party_has_troop, ":other_npc"),
                (neg|troop_is_wounded, ":other_npc"),

#                (store_random_in_range, ":random", 0, 3),
                (try_begin),
                    (troop_slot_eq, ":npc", slot_troop_personalityclash2_state, 0),
                    (try_begin),
#                        (eq, ":random", 0),
                        (assign, "$npc_with_personality_clash_2", ":npc"),
                    (try_end),
                (try_end),

            (try_end),

            (try_for_range, ":npc", companions_begin, companions_end),
                (troop_slot_eq, ":npc", slot_troop_personalitymatch_state, 0),
                (eq, "$disable_npc_complaints", 0),
                (main_party_has_troop, ":npc"),
                (neg|troop_is_wounded, ":npc"),
                (troop_get_slot, ":other_npc", ":npc", slot_troop_personalitymatch_object),
                (main_party_has_troop, ":other_npc"),
                (neg|troop_is_wounded, ":other_npc"),
                (assign, "$npc_with_personality_match", ":npc"),
            (try_end),


            (try_begin),
                (gt, "$npc_with_personality_clash_2", 0),
                (assign, "$npc_map_talk_context", slot_troop_personalityclash2_state),
                (start_map_conversation, "$npc_with_personality_clash_2"),
            (else_try),
                (gt, "$npc_with_personality_match", 0),
                (assign, "$npc_map_talk_context", slot_troop_personalitymatch_state),
                (start_map_conversation, "$npc_with_personality_match"),
            (try_end),


     ]),

  #script_event_player_defeated_enemy_party
  # INPUT: none
  # OUTPUT: none
  ("event_player_defeated_enemy_party",
    [(try_begin),
       (check_quest_active, "qst_raid_caravan_to_start_war"),
       (neg|check_quest_concluded, "qst_raid_caravan_to_start_war"),
       (party_slot_eq, "$g_enemy_party", slot_party_type, spt_kingdom_caravan),
       (store_faction_of_party, ":enemy_faction", "$g_enemy_party"),
       (quest_slot_eq, "qst_raid_caravan_to_start_war", slot_quest_target_faction, ":enemy_faction"),
       (quest_get_slot, ":cur_state", "qst_raid_caravan_to_start_war", slot_quest_current_state),
       (quest_get_slot, ":quest_target_amount", "qst_raid_caravan_to_start_war", slot_quest_target_amount),
       (val_add, ":cur_state", 1),
       (quest_set_slot, "qst_raid_caravan_to_start_war", slot_quest_current_state, ":cur_state"),
       (try_begin),
         (ge, ":cur_state", ":quest_target_amount"),
         #(quest_get_slot, ":quest_target_faction", "qst_raid_caravan_to_start_war", slot_quest_target_faction),
         #(quest_get_slot, ":quest_giver_troop", "qst_raid_caravan_to_start_war", slot_quest_giver_troop),
         #(store_troop_faction, ":quest_giver_faction", ":quest_giver_troop"),
         #(call_script, "script_diplomacy_start_war_between_kingdoms", ":quest_target_faction", ":quest_giver_faction", 1),
         (call_script, "script_succeed_quest", "qst_raid_caravan_to_start_war"),
       (try_end),
     (try_end),

     ]),

  #script_event_player_captured_as_prisoner
  # INPUT: none
  # OUTPUT: none
  ("event_player_captured_as_prisoner",
    [
        (try_begin),
          (check_quest_active, "qst_raid_caravan_to_start_war"),
          (neg|check_quest_concluded, "qst_raid_caravan_to_start_war"),
          (quest_get_slot, ":quest_target_faction", "qst_raid_caravan_to_start_war", slot_quest_target_faction),
          (store_faction_of_party, ":capturer_faction", "$capturer_party"),
          (eq, ":quest_target_faction", ":capturer_faction"),
          (call_script, "script_fail_quest", "qst_raid_caravan_to_start_war"),
        (try_end),
        #Removing followers of the player
        (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
          (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
          (gt, ":party_no", 0),
          (party_slot_eq, ":party_no", slot_party_commander_party, "p_main_party"),
          (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
          (party_set_slot, ":party_no", slot_party_commander_party, -1),
          (assign, "$g_recalculate_ais", 1),
        (try_end),
     ]),


#NPC morale both returns a string and reg0 as the morale value
  ("npc_morale",
[       (store_script_param_1, ":npc"),

        (troop_get_slot, ":morality_grievances", ":npc", slot_troop_morality_penalties),
        (troop_get_slot, ":personality_grievances", ":npc", slot_troop_personalityclash_penalties),
        (party_get_morale, ":party_morale", "p_main_party"),

        (store_sub, ":troop_morale", ":party_morale", ":morality_grievances"),
        (val_sub, ":troop_morale", ":personality_grievances"),
        (val_add, ":troop_morale", 50),

        (assign, reg8, ":troop_morale"),
        (val_mul, ":troop_morale", 3),
        (val_div, ":troop_morale", 4),
        (val_clamp, ":troop_morale", 0, 100),

        (assign, reg5, ":party_morale"),
        (assign, reg6, ":morality_grievances"),
        (assign, reg7, ":personality_grievances"),
        (assign, reg9, ":troop_morale"),

#        (str_store_troop_name, s11, ":npc"),
#        (display_message, "@{s11}'s morale = PM{reg5} + 50 - MG{reg6} - PG{reg7} = {reg8} x 0.75 = {reg9}"),

        (try_begin),(lt, ":morality_grievances", 3),(str_store_string, 7, "str_happy"),
        (else_try) ,(lt, ":morality_grievances",15),(str_store_string, 7, "str_content"),
        (else_try) ,(lt, ":morality_grievances",30),(str_store_string, 7, "str_concerned"),
        (else_try) ,(lt, ":morality_grievances",45),(str_store_string, 7, "str_not_happy"),
        (else_try) ,                                (str_store_string, 7, "str_miserable"),
        (try_end),

        (try_begin),(lt, ":personality_grievances", 3),(str_store_string, 6, "str_happy"),
        (else_try) ,(lt, ":personality_grievances",15),(str_store_string, 6, "str_content"),
        (else_try) ,(lt, ":personality_grievances",30),(str_store_string, 6, "str_concerned"),
        (else_try) ,(lt, ":personality_grievances",45),(str_store_string, 6, "str_not_happy"),
        (else_try) ,                                   (str_store_string, 6, "str_miserable"),
        (try_end),

        (try_begin),(gt,":troop_morale",80),(str_store_string,8, "str_happy"    ),(str_store_string, 63, "str_bar_enthusiastic"),
        (else_try) ,(gt,":troop_morale",60),(str_store_string,8, "str_content"  ),(str_store_string, 63, "str_bar_content"),
        (else_try) ,(gt,":troop_morale",40),(str_store_string,8, "str_concerned"),(str_store_string, 63, "str_bar_weary"),
        (else_try) ,(gt,":troop_morale",20),(str_store_string,8, "str_not_happy"),(str_store_string, 63, "str_bar_disgruntled"),
        (else_try) ,                        (str_store_string,8, "str_miserable"),(str_store_string, 63, "str_bar_miserable"),
        (try_end),

        (str_store_string, 21, "str_npc_morale_report"),
        (assign, reg0, ":troop_morale"),
     ]),
#NPC morale both returns a string and reg0 as the morale value
#
  ("retire_companion",
[   (store_script_param_1, ":npc"),
    (store_script_param_2, ":length"),

    (remove_member_from_party, ":npc", "p_main_party"),
    (troop_set_slot, ":npc", slot_troop_personalityclash_penalties, 0),
    (troop_set_slot, ":npc", slot_troop_morality_penalties, 0),
    (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
    (store_add, ":return_renown", ":renown", ":length"),
    (troop_set_slot, ":npc", slot_troop_occupation, slto_retirement),
    (troop_set_slot, ":npc", slot_troop_return_renown, ":return_renown"),
    ]),
#NPC companion changes end

  #script_reduce_companion_morale_for_clash
  #script_calculate_ransom_amount_for_troop
  # INPUT: arg1 = troop_no for companion1 arg2 = troop_no for companion2 arg3 = slot_for_clash_state
  # slot_for_clash_state means: 1=give full penalty to companion1; 2=give full penalty to companion2; 3=give penalty equally
  ("reduce_companion_morale_for_clash",
   [
    (store_script_param, ":companion_1", 1),
    (store_script_param, ":companion_2", 2),
    (store_script_param, ":slot_for_clash_state", 3),

    (troop_get_slot, ":clash_state", ":companion_1", ":slot_for_clash_state"),
    (troop_get_slot, ":grievance_1", ":companion_1", slot_troop_personalityclash_penalties),
    (troop_get_slot, ":grievance_2", ":companion_2", slot_troop_personalityclash_penalties),
    (try_begin),
      (eq, ":clash_state", pclash_penalty_to_self),
      (val_add, ":grievance_1", 5),
    (else_try),
      (eq, ":clash_state", pclash_penalty_to_other),
      (val_add, ":grievance_2", 5),
    (else_try),
      (eq, ":clash_state", pclash_penalty_to_both),
      (val_add, ":grievance_1", 3),
      (val_add, ":grievance_2", 3),
    (try_end),
    (troop_set_slot, ":companion_1", slot_troop_personalityclash_penalties, ":grievance_1"),
    (troop_set_slot, ":companion_2", slot_troop_personalityclash_penalties, ":grievance_2"),
    ]),

#Hunting scripts end

  #script_calculate_ransom_amount_for_troop
  # INPUT: arg1 = troop_no
  # OUTPUT: reg0 = ransom_amount
  ("calculate_ransom_amount_for_troop",
    [(store_script_param, ":troop_no", 1),
     (store_troop_faction, ":faction_no", ":troop_no"),
     (assign, ":ransom_amount", 400),
     (try_begin),
       (faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_no"),
       (val_add, ":ransom_amount", 4000),
     (try_end),

     (assign, ":num_center_points", 0),
     (try_for_range, ":cur_center", centers_begin, centers_end),
       (party_is_active, ":cur_center"), #TLD
       (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
       (try_begin),
         (party_slot_eq, ":cur_center", slot_party_type, spt_town),
         (val_add, ":num_center_points", 4),
       (else_try),
         (party_slot_eq, ":cur_center", slot_party_type, spt_castle),
         (val_add, ":num_center_points", 2),
       (else_try),
         (val_add, ":num_center_points", 1),
       (try_end),
     (try_end),
     (val_mul, ":num_center_points", 500),
     (val_add, ":ransom_amount", ":num_center_points"),
     (troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
     (val_mul, ":renown", 2),
     (val_add, ":ransom_amount", ":renown"),
     (store_mul, ":ransom_max_amount", ":ransom_amount", 3),
     (val_div, ":ransom_max_amount", 2),
     (store_random_in_range, ":random_ransom_amount", ":ransom_amount", ":ransom_max_amount"),
     (val_div, ":random_ransom_amount", 100),
     (val_mul, ":random_ransom_amount", 100),
     (assign, reg0, ":random_ransom_amount"),
     ]),  



  # script_cf_check_hero_can_escape_from_player
  # Input: arg1 = troop_no
  # Output: none (can fail)
  ("cf_check_hero_can_escape_from_player",
    [   (store_script_param_1, ":troop_no"),
        (assign, ":quest_target", 0),
        (try_begin),
          (check_quest_active, "qst_persuade_lords_to_make_peace"),
          (this_or_next|quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, ":troop_no"),
          (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, ":troop_no"),
          (assign, ":quest_target", 1),
        (try_end),
        (eq, ":quest_target", 0),
        (store_random_in_range, ":rand", 0, 100),
        (lt, ":rand", hero_escape_after_defeat_chance),
    ]),

  # script_cf_party_remove_random_regular_troop
  # Input: arg1 = party_no
  # Output: troop_id that has been removed (can fail)
  ("cf_party_remove_random_regular_troop",
    [(store_script_param_1, ":party_no"),
     (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
     (assign, ":num_troops", 0),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (neg|troop_is_hero, ":stack_troop"),
       (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
       (val_add, ":num_troops", ":stack_size"),
     (try_end),
     (assign, reg0, -1),
     (gt, ":num_troops", 0),
     (store_random_in_range, ":random_troop", 0, ":num_troops"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (neg|troop_is_hero, ":stack_troop"),
       (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
       (val_sub, ":random_troop", ":stack_size"),
       (lt, ":random_troop", 0),
       (assign, ":num_stacks", 0), #break
       (party_remove_members, ":party_no", ":stack_troop", 1),
       (assign, reg0, ":stack_troop"),
     (try_end),
     ]),
	 
  # script_cf_party_select_random_regular_troop
  # Input: arg1 = party_no
  # Output: troop_id that has been removed (can fail)
  ("cf_party_select_random_regular_troop",
    [(store_script_param_1, ":party_no"),
     (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
     (assign, ":num_troops", 0),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (neg|troop_is_hero, ":stack_troop"),
       (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
       (val_add, ":num_troops", ":stack_size"),
     (try_end),
     (assign, reg0, -1),
     (gt, ":num_troops", 0),
     (store_random_in_range, ":random_troop", 0, ":num_troops"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (neg|troop_is_hero, ":stack_troop"),
       (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
       (val_sub, ":random_troop", ":stack_size"),
       (lt, ":random_troop", 0),
       (assign, ":num_stacks", 0), #break
       (assign, reg0, ":stack_troop"),
     (try_end),
     ]),


  # script_place_player_banner_near_inventory
  # Input: none
  # Output: none
  ("place_player_banner_near_inventory",
    [
        #normal_banner_begin
        (troop_get_slot, ":troop_banner_object", "trp_player", slot_troop_banner_scene_prop),
        #custom_banner_begin
#        (troop_get_slot, ":flag_spr", "trp_player", slot_troop_custom_banner_flag_type),
     (try_begin),
        #normal_banner_begin
       (gt, ":troop_banner_object", 0),
       (scene_prop_get_instance, ":flag_object", ":troop_banner_object", 0),
        #custom_banner_begin
#       (ge, ":flag_spr", 0),
#       (val_add, ":flag_spr", custom_banner_flag_scene_props_begin),
#       (scene_prop_get_instance, ":flag_object", ":flag_spr", 0),
       (try_begin),
         (ge, ":flag_object", 0),
         (get_player_agent_no, ":player_agent"),
         (agent_get_look_position, pos1, ":player_agent"),
         (position_move_y, pos1, -500),
         (position_rotate_z, pos1, 180),
         (position_set_z_to_ground_level, pos1),
         (position_move_z, pos1, 300),
         (prop_instance_set_position, ":flag_object", pos1),
       (try_end),
       (scene_prop_get_instance, ":pole_object", "spr_banner_pole", 0),
       (try_begin),
         (ge, ":pole_object", 0),
         (position_move_z, pos1, -320),
         (prop_instance_set_position, ":pole_object", pos1),
       (try_end),
     (else_try),
       (init_position, pos1),
       (position_move_z, pos1, -1000000),
       (scene_prop_get_instance, ":flag_object", banner_scene_props_begin, 0),
       (try_begin),
         (ge, ":flag_object", 0),
         (prop_instance_set_position, ":flag_object", pos1),
       (try_end),
       (scene_prop_get_instance, ":pole_object", "spr_banner_pole", 0),
       (try_begin),
         (ge, ":pole_object", 0),
         (prop_instance_set_position, ":pole_object", pos1),
       (try_end),
     (try_end),
     ]),

  # script_place_player_banner_near_inventory_bms
  # Input: none
  # Output: none
  ("place_player_banner_near_inventory_bms",
    [           #normal_banner_begin
        (troop_get_slot, ":troop_banner_object", "trp_player", slot_troop_banner_scene_prop),
                #custom_banner_begin
#      (troop_get_slot, ":flag_spr", "trp_player", slot_troop_custom_banner_flag_type),
     (try_begin),
                #normal_banner_begin
       (gt, ":troop_banner_object", 0),
       (replace_scene_props, banner_scene_props_begin, ":troop_banner_object"),
                #custom_banner_begin
#       (ge, ":flag_spr", 0),
#       (val_add, ":flag_spr", custom_banner_flag_scene_props_begin),
#       (replace_scene_props, banner_scene_props_begin, ":flag_spr"),
     (try_end),
     ]),
  
  # script_stay_captive_for_hours
  # Input: arg1 = num_hours
  # Output: none
  ("stay_captive_for_hours",
    [(store_script_param, ":num_hours", 1),
     (store_current_hours, ":cur_hours"),
     (val_add, ":cur_hours", ":num_hours"),
     (val_max, "$g_check_autos_at_hour", ":cur_hours"),
     (val_add, ":num_hours", 1),
     (rest_for_hours, ":num_hours", 0, 0),
     ]),

  # script_set_parties_around_player_ignore_player
  # Input: arg1 = ignore_range, arg2 = num_hours_to_ignore
  # Output: none
  ("set_parties_around_player_ignore_player",
    [(store_script_param, ":ignore_range", 1),
     (store_script_param, ":num_hours", 2),
     (try_for_parties, ":party_no"),
       (party_is_active, ":party_no"),
       (store_distance_to_party_from_party, ":dist", "p_main_party", ":party_no"),
       (lt, ":dist", ":ignore_range"),
       (party_ignore_player, ":party_no", ":num_hours"),
     (try_end),
     ]),

  # script_randomly_make_prisoner_heroes_escape_from_party
  # Input: arg1 = party_no, arg2 = escape_chance_mul_1000
  # Output: none
  ("randomly_make_prisoner_heroes_escape_from_party",
    [(store_script_param, ":party_no", 1),
     (store_script_param, ":escape_chance", 2),
     (assign, ":quest_troop_1", -1),
     (assign, ":quest_troop_2", -1),
     (try_begin),
       (check_quest_active, "qst_rescue_lord_by_replace"),
       (quest_get_slot, ":quest_troop_1", "qst_rescue_lord_by_replace", slot_quest_target_troop),
     (try_end),
     (try_begin),
       (check_quest_active, "qst_deliver_message_to_prisoner_lord"),
       (quest_get_slot, ":quest_troop_2", "qst_deliver_message_to_prisoner_lord", slot_quest_target_troop),
     (try_end),
     (party_get_num_prisoner_stacks, ":num_stacks", ":party_no"),
     (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
       (party_prisoner_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (troop_is_hero, ":stack_troop"),
       (neq, ":stack_troop", ":quest_troop_1"),
       (neq, ":stack_troop", ":quest_troop_2"),
       (troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
       (store_random_in_range, ":random_no", 0, 1000),
       (lt, ":random_no", ":escape_chance"),
       (party_remove_prisoners, ":party_no", ":stack_troop", 1),
       (call_script, "script_remove_troop_from_prison", ":stack_troop"),
       (str_store_troop_name_link, s1, ":stack_troop"),
       (try_begin),
         (eq, ":party_no", "p_main_party"),
         (str_store_string, s2, "@your party"),
       (else_try),
         (str_store_party_name, s2, ":party_no"),
       (try_end),
       (assign, reg0, 0),
       (try_begin),
         (this_or_next|eq, ":party_no", "p_main_party"),
         (party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
         (assign, reg0, 1),
       (try_end),
       (store_troop_faction, ":troop_faction", ":stack_troop"),
       (str_store_faction_name_link, s3, ":troop_faction"),
       (display_message, "@{reg0?One of your prisoners, :}{s1} of {s3} has escaped from captivity!"),
     (try_end),
     ]),

  # script_calculate_amount_of_cattle_can_be_stolen
  # Input: arg1 = village_no
  # Output: reg0 = max_amount
  ("calculate_amount_of_cattle_can_be_stolen",
    [
      (store_script_param, ":village_no", 1),
      (call_script, "script_get_max_skill_of_player_party", "skl_looting"),
      (assign, ":max_skill", reg0),
      (store_mul, ":can_steal", ":max_skill", 2),
      (call_script, "script_party_count_fit_for_battle", "p_main_party"),
      (store_add, ":num_men_effect", reg0, 10),
      (val_div, ":num_men_effect", 10),
      (val_add, ":can_steal", ":num_men_effect"),
      (party_get_slot, ":num_cattle", ":village_no", slot_village_number_of_cattle),
      (val_min, ":can_steal", ":num_cattle"),
      (assign, reg0, ":can_steal"),
     ]),


  # script_draw_banner_to_region
  # Input: arg1 = troop_no, arg2 = center_pos_x, arg3 = center_pos_y, arg4 = width, arg5 = height, arg6 = stretch_width, arg7 = stretch_height, arg8 = default_scale, arg9 = max_charge_scale, arg10 = drawn_item_type
  # drawn_item_type is 0 for banners, 1 for shields, 2 for heater shield, 3 for armor
  # arguments will be used as fixed point values
  # Output: none
  ("draw_banner_to_region",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":center_pos_x", 2),
      (store_script_param, ":center_pos_y", 3),
      (store_script_param, ":width", 4),
      (store_script_param, ":height", 5),
      (store_script_param, ":stretch_width", 6),
      (store_script_param, ":stretch_height", 7),
      (store_script_param, ":default_scale", 8),
      (store_script_param, ":max_charge_scale", 9),
      (store_script_param, ":drawn_item_type", 10),

      (troop_get_slot, ":bg_type", ":troop_no", slot_troop_custom_banner_bg_type),
      (val_add, ":bg_type", custom_banner_backgrounds_begin),
      (troop_get_slot, ":bg_color_1", ":troop_no", slot_troop_custom_banner_bg_color_1),
      (troop_get_slot, ":bg_color_2", ":troop_no", slot_troop_custom_banner_bg_color_2),
      (troop_get_slot, ":num_charges", ":troop_no", slot_troop_custom_banner_num_charges),
      (troop_get_slot, ":positioning", ":troop_no", slot_troop_custom_banner_positioning),
      (call_script, "script_get_troop_custom_banner_num_positionings", ":troop_no"),
      (assign, ":num_positionings", reg0),
      (val_mod, ":positioning", ":num_positionings"),

      (init_position, pos2),
      (position_set_x, pos2, ":width"),
      (position_set_y, pos2, ":height"),
      (assign, ":default_value", 1),
      (convert_to_fixed_point, ":default_value"),
      (position_set_z, pos2, ":default_value"),

      (init_position, pos1),
      (position_set_x, pos1, ":center_pos_x"),
      (position_set_y, pos1, ":center_pos_y"),
      (position_move_z, pos1, -20),

      (init_position, pos3),
      (position_set_x, pos3, ":default_scale"),
      (position_set_y, pos3, ":default_scale"),
      (position_set_z, pos3, ":default_value"),

      (try_begin),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_bg"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg01"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg02"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg03"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg08"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg09"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg10"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg11"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg12"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg13"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg16"),
        (eq, ":bg_type", "mesh_custom_banner_fg17"),
        (cur_tableau_add_mesh_with_scale_and_vertex_color, ":bg_type", pos1, pos2, 0, ":bg_color_1"),
      (else_try),
        (cur_tableau_add_mesh_with_scale_and_vertex_color, ":bg_type", pos1, pos3, 0, ":bg_color_1"),
      (try_end),
      (position_move_z, pos1, -20),
      (position_move_x, pos2, ":width"),
      (position_move_y, pos2, ":height"),
      (cur_tableau_add_mesh_with_scale_and_vertex_color, "mesh_custom_banner_bg", pos1, pos2, 0, ":bg_color_2"),
      
      (assign, ":charge_stretch", ":stretch_width"),
      (val_min, ":charge_stretch", ":stretch_height"),
      (val_min, ":charge_stretch", ":max_charge_scale"),
      (call_script, "script_get_custom_banner_charge_type_position_scale_color", "trp_player", ":positioning"),

      (try_begin),
        (this_or_next|eq, ":drawn_item_type", 2), #heater shield
        (eq, ":drawn_item_type", 3), #armor
        (assign, ":change_center_pos", 0),
        (try_begin),
          (eq, ":num_charges", 1),
          (assign, ":change_center_pos", 1),
        (else_try),
          (eq, ":num_charges", 2),
          (eq, ":positioning", 1),
          (assign, ":change_center_pos", 1),
        (else_try),
          (eq, ":num_charges", 3),
          (eq, ":positioning", 1),
          (assign, ":change_center_pos", 1),
        (try_end),
        (try_begin),
          (eq, ":change_center_pos", 1),
          (val_add, ":center_pos_y", 30),
        (try_end),
      (try_end),
      
      (try_begin),
        (ge, ":num_charges", 1),
        (val_mul, reg1, ":charge_stretch"),
        (val_div, reg1, 10000),
        (position_get_x, ":x", pos0),
        (position_get_y, ":y", pos0),
        (val_mul, ":x", ":stretch_width"),
        (val_mul, ":y", ":stretch_height"),
        (val_div, ":x", 10000),
        (val_div, ":y", 10000),
        (val_add, ":x", ":center_pos_x"),
        (val_add, ":y", ":center_pos_y"),
        (position_set_x, pos0, ":x"),
        (position_set_y, pos0, ":y"),
        (assign, ":scale_value", reg1),
        (convert_to_fixed_point, ":scale_value"),
        (store_mul, ":scale_value_inverse", ":scale_value", -1),
        (init_position, pos4),
        (position_set_x, pos4, ":scale_value"),
        (position_set_y, pos4, ":scale_value"),
        (position_set_z, pos4, ":scale_value"),
        (store_div, ":orientation", reg0, 256), #orientation flags
        (try_begin),
          (this_or_next|eq, ":orientation", 1),
          (eq, ":orientation", 3),
          (position_set_x, pos4, ":scale_value_inverse"),
        (try_end),
        (try_begin),
          (this_or_next|eq, ":orientation", 2),
          (eq, ":orientation", 3),
          (position_set_y, pos4, ":scale_value_inverse"),
        (try_end),
        (val_mod, reg0, 256), #remove orientation flags
        (cur_tableau_add_mesh_with_scale_and_vertex_color, reg0, pos0, pos4, 0, reg2),
      (try_end),
      (try_begin),
        (ge, ":num_charges", 2),
        (val_mul, reg4, ":charge_stretch"),
        (val_div, reg4, 10000),
        (position_get_x, ":x", pos1),
        (position_get_y, ":y", pos1),
        (val_mul, ":x", ":stretch_width"),
        (val_mul, ":y", ":stretch_height"),
        (val_div, ":x", 10000),
        (val_div, ":y", 10000),
        (val_add, ":x", ":center_pos_x"),
        (val_add, ":y", ":center_pos_y"),
        (position_set_x, pos1, ":x"),
        (position_set_y, pos1, ":y"),

        (assign, ":scale_value", reg4),
        (convert_to_fixed_point, ":scale_value"),
        (store_mul, ":scale_value_inverse", ":scale_value", -1),
        (init_position, pos4),
        (position_set_x, pos4, ":scale_value"),
        (position_set_y, pos4, ":scale_value"),
        (position_set_z, pos4, ":scale_value"),
        (store_div, ":orientation", reg3, 256), #orientation flags
        (try_begin),
          (this_or_next|eq, ":orientation", 1),
          (eq, ":orientation", 3),
          (position_set_x, pos4, ":scale_value_inverse"),
        (try_end),
        (try_begin),
          (this_or_next|eq, ":orientation", 2),
          (eq, ":orientation", 3),
          (position_set_y, pos4, ":scale_value_inverse"),
        (try_end),
        (val_mod, reg3, 256), #remove orientation flags

        (cur_tableau_add_mesh_with_scale_and_vertex_color, reg3, pos1, pos4, 0, reg5),
      (try_end),
      (try_begin),
        (ge, ":num_charges", 3),
        (val_mul, reg7, ":charge_stretch"),
        (val_div, reg7, 10000),
        (position_get_x, ":x", pos2),
        (position_get_y, ":y", pos2),
        (val_mul, ":x", ":stretch_width"),
        (val_mul, ":y", ":stretch_height"),
        (val_div, ":x", 10000),
        (val_div, ":y", 10000),
        (val_add, ":x", ":center_pos_x"),
        (val_add, ":y", ":center_pos_y"),
        (position_set_x, pos2, ":x"),
        (position_set_y, pos2, ":y"),

        (assign, ":scale_value", reg7),
        (convert_to_fixed_point, ":scale_value"),
        (store_mul, ":scale_value_inverse", ":scale_value", -1),
        (init_position, pos4),
        (position_set_x, pos4, ":scale_value"),
        (position_set_y, pos4, ":scale_value"),
        (position_set_z, pos4, ":scale_value"),
        (store_div, ":orientation", reg6, 256), #orientation flags
        (try_begin),
          (this_or_next|eq, ":orientation", 1),
          (eq, ":orientation", 3),
          (position_set_x, pos4, ":scale_value_inverse"),
        (try_end),
        (try_begin),
          (this_or_next|eq, ":orientation", 2),
          (eq, ":orientation", 3),
          (position_set_y, pos4, ":scale_value_inverse"),
        (try_end),
        (val_mod, reg6, 256), #remove orientation flags

        (cur_tableau_add_mesh_with_scale_and_vertex_color, reg6, pos2, pos4, 0, reg8),
      (try_end),
      (try_begin),
        (ge, ":num_charges", 4),
        (val_mul, reg10, ":charge_stretch"),
        (val_div, reg10, 10000),
        (position_get_x, ":x", pos3),
        (position_get_y, ":y", pos3),
        (val_mul, ":x", ":stretch_width"),
        (val_mul, ":y", ":stretch_height"),
        (val_div, ":x", 10000),
        (val_div, ":y", 10000),
        (val_add, ":x", ":center_pos_x"),
        (val_add, ":y", ":center_pos_y"),
        (position_set_x, pos3, ":x"),
        (position_set_y, pos3, ":y"),

        (assign, ":scale_value", reg10),
        (convert_to_fixed_point, ":scale_value"),
        (store_mul, ":scale_value_inverse", ":scale_value", -1),
        (init_position, pos4),
        (position_set_x, pos4, ":scale_value"),
        (position_set_y, pos4, ":scale_value"),
        (position_set_z, pos4, ":scale_value"),
        (store_div, ":orientation", reg9, 256), #orientation flags
        (try_begin),
          (this_or_next|eq, ":orientation", 1),
          (eq, ":orientation", 3),
          (position_set_x, pos4, ":scale_value_inverse"),
        (try_end),
        (try_begin),
          (this_or_next|eq, ":orientation", 2),
          (eq, ":orientation", 3),
          (position_set_y, pos4, ":scale_value_inverse"),
        (try_end),
        (val_mod, reg9, 256), #remove orientation flags

        (cur_tableau_add_mesh_with_scale_and_vertex_color, reg9, pos3, pos4, 0, reg11),
      (try_end),
     ]),

  # script_get_troop_custom_banner_num_positionings
  # Input: arg1 = troop_no
  # Output: reg0 = num_positionings
  ("get_troop_custom_banner_num_positionings",
    [
      (store_script_param, ":troop_no", 1),
      (troop_get_slot, ":num_charges", ":troop_no", slot_troop_custom_banner_num_charges),
      (try_begin),
        (eq, ":num_charges", 1),
        (assign, ":num_positionings", 2),
      (else_try),
        (eq, ":num_charges", 2),
        (assign, ":num_positionings", 4),
      (else_try),
        (eq, ":num_charges", 3),
        (assign, ":num_positionings", 6),
      (else_try),
        (assign, ":num_positionings", 2),
      (try_end),
      (assign, reg0, ":num_positionings"),
     ]),

  # script_get_custom_banner_charge_type_position_scale_color
  # Input: arg1 = troop_no, arg2 = positioning_index
  # Output: reg0 = type_1
  #         reg1 = scale_1
  #         reg2 = color_1
  #         reg3 = type_2
  #         reg4 = scale_2
  #         reg5 = color_2
  #         reg6 = type_3
  #         reg7 = scale_3
  #         reg8 = color_3
  #         reg9 = type_4
  #         reg10 = scale_4
  #         reg11 = color_4
  ("get_custom_banner_charge_type_position_scale_color",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":positioning", 2),
      (troop_get_slot, ":num_charges", ":troop_no", slot_troop_custom_banner_num_charges),
      (init_position, pos0),
      (init_position, pos1),
      (init_position, pos2),
      (init_position, pos3),

      (troop_get_slot, reg0, ":troop_no", slot_troop_custom_banner_charge_type_1),
      (val_add, reg0, custom_banner_charges_begin),
      (troop_get_slot, reg2, ":troop_no", slot_troop_custom_banner_charge_color_1),
      (troop_get_slot, reg3, ":troop_no", slot_troop_custom_banner_charge_type_2),
      (val_add, reg3, custom_banner_charges_begin),
      (troop_get_slot, reg5, ":troop_no", slot_troop_custom_banner_charge_color_2),
      (troop_get_slot, reg6, ":troop_no", slot_troop_custom_banner_charge_type_3),
      (val_add, reg6, custom_banner_charges_begin),
      (troop_get_slot, reg8, ":troop_no", slot_troop_custom_banner_charge_color_3),
      (troop_get_slot, reg9, ":troop_no", slot_troop_custom_banner_charge_type_4),
      (val_add, reg9, custom_banner_charges_begin),
      (troop_get_slot, reg11, ":troop_no", slot_troop_custom_banner_charge_color_4),

      (try_begin),
        (eq, ":num_charges", 1),
        (try_begin),
          (eq, ":positioning", 0),
          (assign, reg1, 100),
        (else_try),
          (assign, reg1, 50),
        (try_end),
      (else_try),
        (eq, ":num_charges", 2),
        (try_begin),
          (eq, ":positioning", 0),
          (position_set_y, pos0, 25),
          (position_set_y, pos1, -25),
          (assign, reg1, 40),
          (assign, reg4, 40),
        (else_try),
          (eq, ":positioning", 1),
          (position_set_x, pos0, -25),
          (position_set_x, pos1, 25),
          (assign, reg1, 40),
          (assign, reg4, 40),
        (else_try),
          (eq, ":positioning", 2),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, 25),
          (position_set_x, pos1, 25),
          (position_set_y, pos1, -25),
          (assign, reg1, 50),
          (assign, reg4, 50),
        (else_try),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, -25),
          (position_set_x, pos1, 25),
          (position_set_y, pos1, 25),
          (assign, reg1, 50),
          (assign, reg4, 50),
        (try_end),
      (else_try),
        (eq, ":num_charges", 3),
        (try_begin),
          (eq, ":positioning", 0),
          (position_set_y, pos0, 33),
          (position_set_y, pos2, -33),
          (assign, reg1, 30),
          (assign, reg4, 30),
          (assign, reg7, 30),
        (else_try),
          (eq, ":positioning", 1),
          (position_set_x, pos0, -33),
          (position_set_x, pos2, 33),
          (assign, reg1, 30),
          (assign, reg4, 30),
          (assign, reg7, 30),
        (else_try),
          (eq, ":positioning", 2),
          (position_set_x, pos0, -30),
          (position_set_y, pos0, 30),
          (position_set_x, pos2, 30),
          (position_set_y, pos2, -30),
          (assign, reg1, 35),
          (assign, reg4, 35),
          (assign, reg7, 35),
        (else_try),
          (eq, ":positioning", 3),
          (position_set_x, pos0, -30),
          (position_set_y, pos0, -30),
          (position_set_x, pos2, 30),
          (position_set_y, pos2, 30),
          (assign, reg1, 35),
          (assign, reg4, 35),
          (assign, reg7, 35),
        (else_try),
          (eq, ":positioning", 4),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, -25),
          (position_set_y, pos1, 25),
          (position_set_x, pos2, 25),
          (position_set_y, pos2, -25),
          (assign, reg1, 50),
          (assign, reg4, 50),
          (assign, reg7, 50),
        (else_try),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, 25),
          (position_set_y, pos1, -25),
          (position_set_x, pos2, 25),
          (position_set_y, pos2, 25),
          (assign, reg1, 50),
          (assign, reg4, 50),
          (assign, reg7, 50),
        (try_end),
      (else_try),
        (try_begin),
          (eq, ":positioning", 0),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, 25),
          (position_set_x, pos1, 25),
          (position_set_y, pos1, 25),
          (position_set_x, pos2, -25),
          (position_set_y, pos2, -25),
          (position_set_x, pos3, 25),
          (position_set_y, pos3, -25),
          (assign, reg1, 50),
          (assign, reg4, 50),
          (assign, reg7, 50),
          (assign, reg10, 50),
        (else_try),
          (position_set_y, pos0, 30),
          (position_set_x, pos1, -30),
          (position_set_x, pos2, 30),
          (position_set_y, pos3, -30),
          (assign, reg1, 35),
          (assign, reg4, 35),
          (assign, reg7, 35),
          (assign, reg10, 35),
        (try_end),
      (try_end),
     ]),

  # script_get_random_custom_banner
  # Input: arg1 = troop_no
  # Output: none
  ("get_random_custom_banner",
    [
      (store_script_param, ":troop_no", 1),
      (store_random_in_range, ":num_charges", 1, 5),
      (troop_set_slot, ":troop_no", slot_troop_custom_banner_num_charges, ":num_charges"),
      (store_random_in_range, ":random_color_index", 0, 42),
      (call_script, "script_get_custom_banner_color_from_index", ":random_color_index"),
      (assign, ":color_1", reg0),
      (troop_set_slot, ":troop_no", slot_troop_custom_banner_bg_color_1, ":color_1"),
      (assign, ":end_cond", 1),
      (try_for_range, ":unused", 0, ":end_cond"),
        (store_random_in_range, ":random_color_index", 0, 42),
        (call_script, "script_get_custom_banner_color_from_index", ":random_color_index"),
        (assign, ":color_2", reg0),
        (try_begin),
          (call_script, "script_cf_check_color_visibility", ":color_1", ":color_2"),
          (troop_set_slot, ":troop_no", slot_troop_custom_banner_bg_color_2, ":color_2"),
        (else_try),
          (val_add, ":end_cond", 1),
        (try_end),
      (try_end),
      (assign, ":end_cond", 4),
      (assign, ":cur_charge", 0),
      (try_for_range, ":unused", 0, ":end_cond"),
        (store_random_in_range, ":random_color_index", 0, 42),
        (call_script, "script_get_custom_banner_color_from_index", ":random_color_index"),
        (assign, ":charge_color", reg0),
        (try_begin),
          (call_script, "script_cf_check_color_visibility", ":charge_color", ":color_1"),
          (call_script, "script_cf_check_color_visibility", ":charge_color", ":color_2"),
          (store_add, ":cur_slot", ":cur_charge", slot_troop_custom_banner_charge_color_1),
          (troop_set_slot, ":troop_no", ":cur_slot", ":charge_color"),
          (store_random_in_range, ":random_charge", custom_banner_charges_begin, custom_banner_charges_end),
          (val_sub, ":random_charge", custom_banner_charges_begin),
          (store_add, ":cur_slot", ":cur_charge", slot_troop_custom_banner_charge_type_1),
          (troop_set_slot, ":troop_no", ":cur_slot", ":random_charge"),
          (val_add, ":cur_charge", 1),
        (else_try),
          (val_add, ":end_cond", 1),
        (try_end),
      (try_end),
      (store_random_in_range, ":random_bg", custom_banner_backgrounds_begin, custom_banner_backgrounds_end),
      (val_sub, ":random_bg", custom_banner_backgrounds_begin),
      (troop_set_slot, ":troop_no", slot_troop_custom_banner_bg_type, ":random_bg"),
      (store_random_in_range, ":random_flag", custom_banner_flag_types_begin, custom_banner_flag_types_end),
      (val_sub, ":random_flag", custom_banner_flag_types_begin),
      (troop_set_slot, ":troop_no", slot_troop_custom_banner_flag_type, ":random_flag"),
      (store_random_in_range, ":random_positioning", 0, 4),
      (troop_set_slot, ":troop_no", slot_troop_custom_banner_positioning, ":random_positioning"),
     ]),

  # script_get_custom_banner_color_from_index
  # Input: arg1 = color_index
  # Output: reg0 = color
  ("get_custom_banner_color_from_index",
    [
      (store_script_param, ":color_index", 1),

      (assign, ":cur_color", 0xFF000000), (assign, ":red", 0x00),(assign, ":green", 0x00),(assign, ":blue", 0x00),
      (store_mod, ":mod_i_color", ":color_index", 7),
      (try_begin),(eq, ":mod_i_color", 0),                                                (assign, ":blue", 0xFF),
      (else_try) ,(eq, ":mod_i_color", 1),(assign, ":red", 0xEE),
      (else_try) ,(eq, ":mod_i_color", 2),(assign, ":red", 0xFB),(assign, ":green", 0xAC),
      (else_try) ,(eq, ":mod_i_color", 3),(assign, ":red", 0x5F),                         (assign, ":blue", 0xFF),
      (else_try) ,(eq, ":mod_i_color", 4),(assign, ":red", 0x05),(assign, ":green", 0x44),
      (else_try) ,(eq, ":mod_i_color", 5),(assign, ":red", 0xEE),(assign, ":green", 0xEE),(assign, ":blue", 0xEE),
      (else_try) ,                        (assign, ":red", 0x22),(assign, ":green", 0x22),(assign, ":blue", 0x22),
      (try_end),

      (store_div, ":cur_tone", ":color_index", 7),
      (store_sub, ":cur_tone", 8, ":cur_tone"),
      (val_mul, ":red"  , ":cur_tone"),(val_div, ":red"  , 8),
      (val_mul, ":green", ":cur_tone"),(val_div, ":green", 8),
      (val_mul, ":blue" , ":cur_tone"),(val_div, ":blue" , 8),
      (val_mul, ":green", 0x100),
      (val_mul, ":red", 0x10000),
      (val_add, ":cur_color", ":blue"),
      (val_add, ":cur_color", ":green"),
      (val_add, ":cur_color", ":red"),
      (assign, reg0, ":cur_color"),
     ]),

  # script_cf_check_color_visibility
  # Input: arg1 = color_1, arg2 = color_2
  # Output: none
  ("cf_check_color_visibility",
    [
      (store_script_param, ":color_1", 1),
      (store_script_param, ":color_2", 2),
      (store_mod, ":blue_1", ":color_1", 256),
      (store_div, ":green_1", ":color_1", 256),
      (val_mod, ":green_1", 256),
      (store_div, ":red_1", ":color_1", 256 * 256),
      (val_mod, ":red_1", 256),
      (store_mod, ":blue_2", ":color_2", 256),
      (store_div, ":green_2", ":color_2", 256),
      (val_mod, ":green_2", 256),
      (store_div, ":red_2", ":color_2", 256 * 256),
      (val_mod, ":red_2", 256),
      (store_sub, ":red_dif", ":red_1", ":red_2"),
      (val_abs, ":red_dif"),
      (store_sub, ":green_dif", ":green_1", ":green_2"),
      (val_abs, ":green_dif"),
      (store_sub, ":blue_dif", ":blue_1", ":blue_2"),
      (val_abs, ":blue_dif"),
      (assign, ":max_dif", 0),
      (val_max, ":max_dif", ":red_dif"),
      (val_max, ":max_dif", ":green_dif"),
      (val_max, ":max_dif", ":blue_dif"),
      (ge, ":max_dif", 64),
     ]),
  
  # script_get_next_active_kingdom
  # Input: arg1 = faction_no
  # Output: reg0 = faction_no (does not choose player faction)
  ("get_next_active_kingdom",
    [
      (store_script_param, ":faction_no", 1),
      (assign, ":end_cond", kingdoms_end),
      (try_for_range, ":unused", kingdoms_begin, ":end_cond"),
        (val_add, ":faction_no", 1),
        (try_begin),
          (ge, ":faction_no", kingdoms_end),
          (assign, ":faction_no", kingdoms_begin),
        (try_end),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (assign, ":end_cond", 0),
      (try_end),
      (assign, reg0, ":faction_no"),
     ]),

  # script_store_average_center_value_per_faction
  # Input: none
  # Output: none (sets $g_average_center_value_per_faction)
  ("store_average_center_value_per_faction",
    [
      (store_sub, ":num_towns", towns_end, towns_begin),
      (store_sub, ":num_castles", castles_end, castles_begin),
      (assign, ":num_factions", 0),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (val_add, ":num_factions", 1),
      (try_end),
      (val_max, ":num_factions", 1),
      (store_mul, "$g_average_center_value_per_faction", ":num_towns", 2),
      (val_add, "$g_average_center_value_per_faction", ":num_castles"),
      (val_mul, "$g_average_center_value_per_faction", 10),
      (val_div, "$g_average_center_value_per_faction", ":num_factions"),
     ]),

  # script_remove_cattles_if_herd_is_close_to_party
  # Input: arg1 = party_no, arg2 = maximum_number_of_cattles_required
  # Output: reg0 = number_of_cattles_removed
  ("remove_cattles_if_herd_is_close_to_party",
    [
      (store_script_param, ":party_no", 1),
      (store_script_param, ":max_req", 2),
      (assign, ":cur_req", ":max_req"),
      (try_for_parties, ":cur_party"),
        (gt, ":cur_req", 0),
        (party_slot_eq, ":cur_party", slot_party_type, spt_cattle_herd),
        (store_distance_to_party_from_party, ":dist", ":cur_party", ":party_no"),
        (lt, ":dist", 3),
        #Do not use the quest herd
        (assign, ":subcontinue", 1),
        (try_begin),
          (check_quest_active, "qst_move_cattle_herd"),
          (quest_slot_eq, "qst_move_cattle_herd", slot_quest_target_party, ":cur_party"),
          (assign, ":subcontinue", 0),
        (try_end),
        (eq, ":subcontinue", 1),
        (party_count_companions_of_type, ":num_cattle", ":cur_party", "trp_cattle"),
        (try_begin),
          (le, ":num_cattle", ":cur_req"),
          (assign, ":num_added", ":num_cattle"),
          (remove_party, ":cur_party"),
        (else_try),
          (assign, ":num_added", ":cur_req"),
          (party_remove_members, ":cur_party", "trp_cattle", ":cur_req"),
        (try_end),
        (val_sub, ":cur_req", ":num_added"),
        (try_begin),
          (party_slot_eq, ":party_no", slot_party_type, spt_village),
          (party_get_slot, ":village_cattle_amount", ":party_no", slot_village_number_of_cattle),
          (val_add, ":village_cattle_amount", ":num_added"),
          (party_set_slot, ":party_no", slot_village_number_of_cattle, ":village_cattle_amount"),
        (try_end),
        (assign, reg3, ":num_added"),
        (str_store_party_name_link, s1, ":party_no"),
        (display_message, "@You brought {reg3} heads of cattle to {s1}."),
      (try_end),
      (store_sub, reg0, ":max_req", ":cur_req"),
     ]),  

  # script_get_rumor_to_s61
  # Input: rumor_id
  # Output: reg0 = 1 if rumor found, 0 otherwise; s61 will contain rumor string if found
  ("get_rumor_to_s61",
    [
     (store_script_param, ":base_rumor_id", 1), # the script returns the same rumor for the same rumor id, so that one cannot hear all rumors by
                                                # speaking to a single person.

     (store_current_hours, ":cur_hours"),
     (store_div, ":cur_day", ":cur_hours", 24),
     (assign, ":rumor_found", 0),
     (assign, ":num_tries", 3),
     (try_for_range, ":try_no", 0, ":num_tries"),
       (store_mul, ":rumor_id", ":try_no", 6781),
       (val_add, ":rumor_id", ":base_rumor_id"),
       (store_mod, ":rumor_type", ":rumor_id", 7),
       (val_add, ":rumor_id", ":cur_hours"),
       (try_begin),
         (eq,  ":rumor_type", 0),
         (try_begin),
           (store_sub, ":range", towns_end, towns_begin),
           (store_mod, ":random_center", ":rumor_id", ":range"),
           (val_add, ":random_center", towns_begin),
           (party_slot_ge, ":random_center", slot_town_has_tournament, 1),
           (neq, ":random_center", "$current_town"),
           (str_store_party_name, s62, ":random_center"),
           (str_store_string, s61, "@I heard that there will be a tournament in {s62} soon."),
           (assign, ":rumor_found", 1),
         (try_end),
       (else_try),
         (eq,  ":rumor_type", 1),
         (try_begin),
           (store_sub, ":range", kingdom_heroes_end, kingdom_heroes_begin),
           (store_mod, ":random_hero", ":rumor_id", ":range"),
           (val_add, ":random_hero", kingdom_heroes_begin),
           (troop_get_slot, ":personality", ":random_hero", slot_lord_reputation_type),
           (gt, ":personality", 0),
           (store_add, ":rumor_string", ":personality", "str_gossip_about_character_default"),
           (str_store_troop_name, s6, ":random_hero"),
           (str_store_string, s61, ":rumor_string"),
           (assign, ":rumor_found", 1),
         (try_end),
       (else_try),
         (eq,  ":rumor_type", 2),
         (try_begin),
           (store_sub, ":range", trade_goods_end, trade_goods_begin),
           (store_add, ":random_trade_good", ":rumor_id", ":cur_day"),
           (store_mod, ":random_trade_good", ":random_trade_good", ":range"),
           (store_add, ":random_trade_good_slot", ":random_trade_good", slot_town_trade_good_prices_begin),
           (val_add, ":random_trade_good", trade_goods_begin),
           (store_mul, ":min_price", average_price_factor, 3),
           (val_div, ":min_price", 4),
           (assign, ":min_price_center", -1),
           (try_for_range, ":sub_try_no", 0, 10),
             (store_sub, ":range", towns_end, towns_begin),
             (store_add, ":center_rumor_id", ":rumor_id", ":sub_try_no"),
             (store_mod, ":random_center", ":center_rumor_id", ":range"),
             (val_add, ":random_center", towns_begin),
             (neq, ":random_center", "$g_encountered_party"),
             (party_get_slot, ":cur_price", ":random_center", ":random_trade_good_slot"),
             (lt, ":cur_price", ":min_price"),
             (assign, ":min_price", ":cur_price"),
             (assign, ":min_price_center", ":random_center"),
           (try_end),
           (ge, ":min_price_center", 0),
           (str_store_item_name, s62, ":random_trade_good"),
           (str_store_party_name, s63, ":min_price_center"),
           (str_store_string, s61, "@I heard that one can buy {s62} very cheap at {s63}."),
           (assign, ":rumor_found", 1),
         (try_end),
       (else_try),
         (eq,  ":rumor_type", 3),
         (try_begin),
           (store_sub, ":range", trade_goods_end, trade_goods_begin),
           (store_add, ":random_trade_good", ":rumor_id", ":cur_day"),
           (store_mod, ":random_trade_good", ":random_trade_good", ":range"),
           (store_add, ":random_trade_good_slot", ":random_trade_good", slot_town_trade_good_prices_begin),
           (val_add, ":random_trade_good", trade_goods_begin),
           (store_mul, ":max_price", average_price_factor, 5),
           (val_div, ":max_price", 4),
           (assign, ":max_price_center", -1),
           (try_for_range, ":sub_try_no", 0, 10),
             (store_sub, ":range", towns_end, towns_begin),
             (store_add, ":center_rumor_id", ":rumor_id", ":sub_try_no"),
             (store_mod, ":random_center", ":center_rumor_id", ":range"),
             (val_add, ":random_center", towns_begin),
             (neq, ":random_center", "$g_encountered_party"),
             (party_get_slot, ":cur_price", ":random_center", ":random_trade_good_slot"),
             (gt, ":cur_price", ":max_price"),
             (assign, ":max_price", ":cur_price"),
             (assign, ":max_price_center", ":random_center"),
           (try_end),
           (ge, ":max_price_center", 0),
           (str_store_item_name, s62, ":random_trade_good"),
           (str_store_party_name, s63, ":max_price_center"),
           (str_store_string, s61, "@I heard that they pay a very high price for {s62} at {s63}."),
           (assign, ":rumor_found", 1),
         (try_end),
       (try_end),
       (try_begin),
         (gt, ":rumor_found", 0),
         (assign, ":num_tries", 0),
       (try_end),
     (try_end),
     (assign, reg0, ":rumor_found"),
     ]),

  ("lord_comment_to_s43",
    [(store_script_param, ":lord", 1),
     (store_script_param, ":default_string", 2),

    (troop_get_slot,":reputation", ":lord", slot_lord_reputation_type),
    (val_add,":reputation", ":default_string"),
    (str_store_string,43,":reputation"),
]),
  
#Troop Commentaries begin
  
  # script_add_log_entry
  # Input: arg1 = entry_type, arg2 = event_actor, arg3 = center_object, arg4 = troop_object, arg5 = faction_object
  # Output: none
  ("add_log_entry",
    [(store_script_param, ":entry_type", 1),
     (store_script_param, ":actor", 2),
     (store_script_param, ":center_object", 3),
     (store_script_param, ":troop_object", 4),
     (store_script_param, ":faction_object", 5),
     (assign, ":center_object_lord", -1),
     (assign, ":center_object_faction", -1),
     (assign, ":troop_object_faction", -1),
     (try_begin),
       (gt, ":center_object", 0),
       (party_get_slot, ":center_object_lord", ":center_object", slot_town_lord),
       (store_faction_of_party, ":center_object_faction", ":center_object"),
     (try_end),
     (try_begin),
       (ge, ":troop_object", 0),
       (store_troop_faction, ":troop_object_faction", ":troop_object"),
     (try_end),

     (val_add, "$num_log_entries", 1),
     
     (store_current_hours, ":entry_time"),
     (troop_set_slot, "trp_log_array_entry_type",            "$num_log_entries", ":entry_type"),
     (troop_set_slot, "trp_log_array_entry_time",            "$num_log_entries", ":entry_time"),
     (troop_set_slot, "trp_log_array_actor",                 "$num_log_entries", ":actor"),
     (troop_set_slot, "trp_log_array_center_object",         "$num_log_entries", ":center_object"),
     (troop_set_slot, "trp_log_array_center_object_lord",    "$num_log_entries", ":center_object_lord"),
     (troop_set_slot, "trp_log_array_center_object_faction", "$num_log_entries", ":center_object_faction"),
     (troop_set_slot, "trp_log_array_troop_object",          "$num_log_entries", ":troop_object"),
     (troop_set_slot, "trp_log_array_troop_object_faction",  "$num_log_entries", ":troop_object_faction"),
     (troop_set_slot, "trp_log_array_faction_object",        "$num_log_entries", ":faction_object"),

     (try_begin),
       (eq, "$cheat_mode", 1),
       (assign, reg3, "$num_log_entries"), 
       (assign, reg4, ":entry_type"),
       (display_message, "@Log entry {reg3}: type {reg4}"), 
       (try_begin),
          (gt, ":center_object", 0),
          (str_store_party_name, s4, ":center_object"),
          (display_message, "@Center: {s4}"), 
       (try_end),      
       (try_begin),
          (gt, ":troop_object", 0),
          (str_store_troop_name, s4, ":troop_object"),
          (display_message, "@Troop: {s4}"), 
       (try_end),      
       (try_begin),
          (gt, ":center_object_lord", 0),
          (str_store_troop_name, s4, ":center_object_lord"),
          (display_message, "@Lord: {s4}"), 
       (try_end),
     (try_end),


     (try_begin),
       (this_or_next|gt, "$g_ally_party", 0),
       (eq, ":entry_type", logent_player_participated_in_siege),
       (try_begin),
         (eq, "$cheat_mode", 1),
         (display_message, "@Ally party is present"),
       (try_end),
       (try_for_range, ":hero", kingdom_heroes_begin, kingdom_heroes_end),
         (party_count_companions_of_type, ":hero_present", "p_collective_friends", ":hero"),
         (gt, ":hero_present", 0),
         (troop_set_slot, ":hero", slot_troop_present_at_event, "$num_log_entries"),
#         (store_sub, ":skip_up_to_here", "$num_log_entries", 1),
#         (troop_set_slot, ":hero", slot_troop_last_comment_slot, ":skip_up_to_here"),
         (try_begin),
           (eq, "$cheat_mode", 1),
           (str_store_troop_name, 4, ":hero"),
           (display_message, "@{s4} is present at event"),
         (try_end),
       (try_end),
     (try_end),
     ]),

  
  # script_get_relevant_comment_for_log_entry
  # Input: arg1 = log_entry_no, 
  # Output: reg0 = comment_id; reg1 = relevance
  # Notes: 50 is the default relevance.
  # A comment with relevance less than 30 will always be skipped.
  # A comment with relevance 75 or more will never be skipped.
  # A comment with relevance 50 has about 50% chance to be skipped.
  # If there is more than one comment that is not skipped, the system will randomize their relevance values, and then choose the highest one.
  # Also note that the relevance of events decreases as time passes. After three months, relevance reduces to 50%, after 6 months, 25%, etc...
  ("get_relevant_comment_for_log_entry",
    [(store_script_param, ":log_entry_no", 1),
     
     (troop_get_slot, ":entry_type",            "trp_log_array_entry_type",            ":log_entry_no"),
     (troop_get_slot, ":entry_time",            "trp_log_array_entry_time",            ":log_entry_no"),
     (troop_get_slot, ":actor",                 "trp_log_array_actor",                 ":log_entry_no"),
##     (troop_get_slot, ":center_object",         "trp_log_array_center_object",         ":log_entry_no"),
     (troop_get_slot, ":center_object_lord",    "trp_log_array_center_object_lord",    ":log_entry_no"),
     (troop_get_slot, ":center_object_faction", "trp_log_array_center_object_faction", ":log_entry_no"),
     (troop_get_slot, ":troop_object",          "trp_log_array_troop_object",          ":log_entry_no"),
     (troop_get_slot, ":troop_object_faction",  "trp_log_array_troop_object_faction",  ":log_entry_no"),
     (troop_get_slot, ":faction_object",        "trp_log_array_faction_object",        ":log_entry_no"),

     (assign, ":relevance", 0),
     (assign, ":comment", -1), 
     (assign, ":suggested_relation_change", 0),

     (troop_get_slot, ":reputation", "$g_talk_troop", slot_lord_reputation_type),
     (store_current_hours, ":current_time"),
     (store_sub, ":entry_hours_elapsed", ":current_time", ":entry_time"),

#Post 0907 changes begin
     (assign, ":players_kingdom_relation", 0), ##the below is so that lords will not congratulate player on attacking neutrals
     (try_begin),
       (eq, "$cheat_mode", 1),
       (try_begin),
         (assign, reg5, ":log_entry_no"),
         (assign, reg6, ":entry_type"),
         (assign, reg8, ":entry_time"),

         (gt, "$players_kingdom", 0),
         (try_begin),
            (gt, ":troop_object_faction", 0),
            (store_relation, ":players_kingdom_relation", "$players_kingdom", ":troop_object_faction"),
            (assign, reg7, ":players_kingdom_relation"),
            (display_message, "@Event #{reg5}, type {reg6}, time {reg8}: player's kingdom relation to troop object = {reg7}"),
         (else_try),
            (gt, ":center_object_faction", 0),
            (store_relation, ":players_kingdom_relation", "$players_kingdom", ":center_object_faction"),
            (assign, reg7, ":players_kingdom_relation"),
            (display_message, "@Event #{reg5}, type {reg6}, time {reg8}: player's kingdom relation to center object faction = {reg7}"),
         (else_try),
            (gt, ":faction_object", 0),
            (store_relation, ":players_kingdom_relation", "$players_kingdom", ":faction_object"),
            (assign, reg7, ":players_kingdom_relation"),

            (display_message, "@Event #{reg5}, type {reg6}, time {reg8}: player's kingdom relation to faction object = {reg7}"),
         (else_try),
            (display_message, "@Event #{reg5}, type {reg6}, time {reg8}. No relevant kingdom relation"),
         (try_end),
       (else_try),
         (display_message, "@Event #{reg5}, type {reg6}, time {reg8}. Player unaffiliated"),
       (try_end),
     (try_end),

     (try_begin),
       (eq, ":entry_type", logent_game_start),
       (eq, "$g_talk_troop_met", 0),
       (is_between, "$g_talk_troop_faction_relation", -5, 5),
       (is_between, "$g_talk_troop_relation", -5, 5),

       (assign, ":relevance", 25),
       (troop_get_slot, ":plyr_renown", "trp_player", slot_troop_renown),
#normal_banner_begin
       (troop_get_slot, ":banner", "trp_player", slot_troop_banner_scene_prop),
#custom_banner_begin
#       (troop_get_slot, ":banner", "trp_player", slot_troop_custom_banner_flag_type),
       (store_random_in_range, ":renown_check", 100, 200),
       (try_begin),
          (eq, ":reputation", lrep_none),
          (gt, "$players_kingdom", 0),
          (assign, ":comment", "str_comment_intro_liege_affiliated"),
       (else_try),
          (gt, ":plyr_renown", ":renown_check"), 
          (assign, ":comment", "str_comment_intro_famous_liege"),
          (val_add, ":comment", ":reputation"),
       (else_try),
#normal_banner_begin
          (gt, ":banner", 0), 
#custom_banner_begin
#          (ge, ":banner", 0), 
          (assign, ":comment", "str_comment_intro_noble_liege"),
          (val_add, ":comment", ":reputation"),
       (else_try),
          (assign, ":comment", "str_comment_intro_common_liege"),
          (val_add, ":comment", ":reputation"),
       (try_end),
#Post 0907 changes end

     (else_try),
       (eq, ":entry_type", logent_village_raided),
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":center_object_lord", "$g_talk_troop"),
         (assign, ":relevance", 200),
         (assign, ":suggested_relation_change", -1),
         (assign, ":comment", "str_comment_you_raided_my_village_default"),
         (try_begin),
            (lt, "$g_talk_troop_faction_relation", -5),
            (this_or_next|eq, ":reputation", lrep_goodnatured),
                (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_you_raided_my_village_enemy_benevolent"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -5),
            (this_or_next|eq, ":reputation", lrep_cunning),
                (eq, ":reputation", lrep_selfrighteous),
            (assign, ":comment", "str_comment_you_raided_my_village_enemy_coldblooded"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_raided_my_village_enemy_spiteful"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -5),
            (assign, ":comment", "str_comment_you_raided_my_village_enemy"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_raided_my_village_unfriendly_spiteful"),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (assign, ":comment", "str_comment_you_raided_my_village_friendly"),
         (try_end),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_village_extorted),
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":center_object_lord", "$g_talk_troop"),
         (assign, ":relevance", 30),
         (assign, ":suggested_relation_change", -1),
         (assign, ":comment", "str_comment_you_robbed_my_village_default"),
         (try_begin),
            (lt, "$g_talk_troop_faction_relation", -5),
            (this_or_next|eq, ":reputation", lrep_cunning),
                (eq, ":reputation", lrep_selfrighteous),
            (assign, ":comment", "str_comment_you_robbed_my_village_enemy_coldblooded"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -5),
            (assign, ":comment", "str_comment_you_robbed_my_village_enemy"),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_robbed_my_village_friendly_spiteful"),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (assign, ":comment", "str_comment_you_robbed_my_village_friendly"),
         (try_end),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_caravan_accosted),
       (eq, ":actor", "trp_player"),
       (eq, ":faction_object", "$g_talk_troop_faction"),
       (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
       (assign, ":relevance", 30),
       (assign, ":suggested_relation_change", -1),
       (assign, ":comment", "str_comment_you_accosted_my_caravan_default"),
       (try_begin),
            (lt, "$g_talk_troop_faction_relation", -5),
            (assign, ":comment", "str_comment_you_accosted_my_caravan_enemy"),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_helped_peasants),
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":center_object_lord", "$g_talk_troop"),
         (assign, ":relevance", 40),
         (assign, ":suggested_relation_change", 0),
         (try_begin),
            (this_or_next|eq, ":reputation", lrep_goodnatured),
                (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_you_helped_villagers_benevolent"),
            (assign, ":suggested_relation_change", 1),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_helped_villagers_friendly_cruel"),
            (assign, ":suggested_relation_change", -1),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_helped_villagers_unfriendly_spiteful"),
            (assign, ":suggested_relation_change", -1),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (assign, ":comment", "str_comment_you_helped_villagers_friendly"),
         (else_try),
            (this_or_next|eq, ":reputation", lrep_selfrighteous),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_helped_villagers_cruel"),
            (assign, ":suggested_relation_change", -1),
         (else_try),
             (assign, ":comment", "str_comment_you_helped_villagers_default"),
         (try_end),
       (try_end),

###Combat events
     (else_try),
       (eq, ":entry_type", logent_castle_captured_by_player),
       (try_begin),
         (eq, ":center_object_lord", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_captured_my_castle_enemy_spiteful"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":center_object_lord", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_captured_my_castle_enemy_chivalrous"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":center_object_lord", "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_captured_my_castle_enemy"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_captured_a_castle_allied_spiteful"),
         (assign, ":relevance", 75),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (gt, "$g_talk_troop_relation", 5),
         (assign, ":comment", "str_comment_you_captured_a_castle_allied_friendly"),
         (assign, ":relevance", 75),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_captured_a_castle_allied_unfriendly_spiteful"),
         (assign, ":relevance", 75),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (assign, ":comment", "str_comment_you_captured_a_castle_allied_unfriendly"),
         (assign, ":relevance", 75),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (assign, ":comment", "str_comment_you_captured_a_castle_allied"),
         (assign, ":relevance", 75),
       (try_end),

#Post 0907 changes begin
     (else_try),
       (this_or_next|eq, ":entry_type", logent_lord_defeated_by_player),
            (eq, ":entry_type", logent_lord_helped_by_player),
       (troop_slot_eq, "$g_talk_troop", slot_troop_present_at_event, ":log_entry_no"),
       (try_begin),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_defeated_a_lord_unfriendly_spiteful"),
           (assign, ":relevance", 150),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (assign, ":comment", "str_comment_we_defeated_a_lord_unfriendly"),
           (assign, ":relevance", 150),
       (else_try),
           (this_or_next|eq, ":reputation", lrep_selfrighteous),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_defeated_a_lord_cruel"),
           (assign, ":relevance", 150),
       (else_try),
           (eq, ":reputation", lrep_quarrelsome),        
           (assign, ":comment", "str_comment_we_defeated_a_lord_cruel"),
           (assign, ":relevance", 150),
       (else_try),
           (eq, ":reputation", lrep_upstanding),
           (assign, ":comment", "str_comment_we_defeated_a_lord_upstanding"),
           (assign, ":relevance", 150),
       (else_try),
           (assign, ":comment", "str_comment_we_defeated_a_lord_default"),
           (assign, ":relevance", 150),
       (try_end),


     (else_try),
       (this_or_next|eq, ":entry_type", logent_castle_captured_by_player),
            (eq, ":entry_type", logent_player_participated_in_siege),
       (troop_slot_eq, "$g_talk_troop", slot_troop_present_at_event, ":log_entry_no"),
       (try_begin),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_fought_in_siege_unfriendly_spiteful"),
           (assign, ":relevance", 150),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (assign, ":comment", "str_comment_we_fought_in_siege_unfriendly"),
           (assign, ":relevance", 150),
       (else_try),
           (this_or_next|eq, ":reputation", lrep_selfrighteous),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_fought_in_siege_cruel"),
           (assign, ":relevance", 150),
       (else_try),
           (eq, ":reputation", lrep_quarrelsome),        
           (assign, ":comment", "str_comment_we_fought_in_siege_quarrelsome"),
           (assign, ":relevance", 150),
       (else_try),
           (eq, ":reputation", lrep_upstanding),
           (assign, ":comment", "str_comment_we_fought_in_siege_upstanding"),
           (assign, ":relevance", 150),
       (else_try),
           (assign, ":comment", "str_comment_we_fought_in_siege_default"),
           (assign, ":relevance", 150),
       (try_end),


     (else_try),
       (eq, ":entry_type", logent_player_participated_in_major_battle),
       (troop_slot_eq, "$g_talk_troop", slot_troop_present_at_event, ":log_entry_no"),
       (try_begin),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_fought_in_major_battle_unfriendly_spiteful"),
           (assign, ":relevance", 150),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (assign, ":comment", "str_comment_we_fought_in_major_battle_unfriendly"),
           (assign, ":relevance", 150),
       (else_try),
           (this_or_next|eq, ":reputation", lrep_selfrighteous),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_fought_in_major_battle_cruel"),
           (assign, ":relevance", 150),
       (else_try),
           (eq, ":reputation", lrep_quarrelsome),        
           (assign, ":comment", "str_comment_we_fought_in_major_battle_cruel"),
           (assign, ":relevance", 150),
       (else_try),
           (eq, ":reputation", lrep_upstanding),
           (assign, ":comment", "str_comment_we_fought_in_major_battle_upstanding"),
           (assign, ":relevance", 150),
       (else_try),
           (assign, ":comment", "str_comment_we_fought_in_major_battle_default"),
           (assign, ":relevance", 150),
       (try_end),


#Post 0907 changes end

     (else_try),
       (eq, ":entry_type", logent_lord_defeated_by_player),
       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_defeated_me_enemy_chivalrous"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_debauched),
             (eq, ":reputation", lrep_quarrelsome),
         (assign, ":comment", "str_comment_you_defeated_me_enemy_spiteful"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_defeated_me_enemy"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_upstanding),
             (eq, ":reputation", lrep_cunning),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_pragmatic"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_chivalrous"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_spiteful"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (faction_slot_eq, "$players_kingdom", slot_faction_leader, "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_liege"),
         (assign, ":relevance", 70),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_unfriendly_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_upstanding),
             (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_unfriendly_chivalrous"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied"),
         (assign, ":relevance", 65),
       (try_end),


     (else_try),
       (eq, ":entry_type", logent_lord_defeated_by_player),
       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_defeated_me_enemy_chivalrous"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_debauched),
             (eq, ":reputation", lrep_quarrelsome),
         (assign, ":comment", "str_comment_you_defeated_me_enemy_spiteful"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_defeated_me_enemy"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_upstanding),
             (eq, ":reputation", lrep_cunning),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_pragmatic"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_chivalrous"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_spiteful"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (faction_slot_eq, "$players_kingdom", slot_faction_leader, "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_liege"),
         (assign, ":relevance", 70),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_unfriendly_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_upstanding),
             (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_unfriendly_chivalrous"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied"),
         (assign, ":relevance", 65),
       (try_end),

#Post 0907 changes begin
     (else_try),
       (eq, ":entry_type", logent_lord_helped_by_player),
       (neq, ":troop_object", "$g_talk_troop"),
       (eq, ":troop_object_faction", "$g_talk_troop_faction"),
       (try_begin),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_upstanding),
             (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_you_helped_my_ally_unfriendly_chivalrous"),
         (assign, ":relevance", 65),
         (assign, ":suggested_relation_change", 2),
       (else_try),
         (lt, "$g_talk_troop_relation", -5),
         (assign, ":comment", "str_comment_you_helped_my_ally_unfriendly"),
         (assign, ":relevance", 0),
       (else_try),
         (eq, ":reputation", lrep_none),
         (assign, ":comment", "str_comment_you_helped_my_ally_liege"),
         (assign, ":relevance", 65),
         (assign, ":suggested_relation_change", 3),
       (else_try),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_helped_my_ally_unfriendly_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_helped_my_ally_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_upstanding),
         (assign, ":comment", "str_comment_you_helped_my_ally_chivalrous"),
         (assign, ":relevance", 65),
         (assign, ":suggested_relation_change", 2),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_helped_my_ally_default"),
       (try_end),

#Post 0907 changes begin
     (else_try),
       (eq, ":entry_type", logent_player_defeated_by_lord),
       (troop_slot_eq, "$g_talk_troop", slot_troop_present_at_event, ":log_entry_no"),
       (try_begin),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_were_defeated_unfriendly_spiteful"),
           (assign, ":relevance", 150),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (assign, ":comment", "str_comment_we_were_defeated_unfriendly"),
           (assign, ":relevance", 150),
       (else_try),
           (this_or_next|eq, ":reputation", lrep_selfrighteous),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_were_defeated_cruel"),
           (assign, ":relevance", 150),
       (else_try),
           (assign, ":comment", "str_comment_we_were_defeated_default"),
           (assign, ":relevance", 150),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_player_defeated_by_lord),
       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_I_defeated_you_enemy_spiteful"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_I_defeated_you_enemy_chivalrous"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_goodnatured),
                (eq, ":reputation", lrep_upstanding),
         (assign, ":comment", "str_comment_I_defeated_you_enemy_benevolent"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_selfrighteous),
             (eq, ":reputation", lrep_cunning),
         (assign, ":comment", "str_comment_I_defeated_you_enemy_coldblooded"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_I_defeated_you_enemy"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_I_defeated_you_enemy"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
         (gt, "$g_talk_troop_relation", 5),
         (assign, ":comment", "str_comment_you_were_defeated_allied_friendly_spiteful"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_selfrighteous),
                (eq, ":reputation", lrep_debauched),
         (lt, "$g_talk_troop_relation", -5),
         (assign, ":comment", "str_comment_you_were_defeated_allied_unfriendly_cruel"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
         (le, "$g_talk_troop_relation", 5),
         (assign, ":comment", "str_comment_you_were_defeated_allied_spiteful"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (eq, ":reputation", lrep_selfrighteous),
         (assign, ":comment", "str_comment_you_were_defeated_allied_pitiless"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (eq, ":reputation", lrep_upstanding),
         (lt, "$g_talk_troop_relation", -15),
         (assign, ":comment", "str_comment_you_were_defeated_allied_unfriendly_upstanding"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, "$g_talk_troop_relation", -10),
         (assign, ":comment", "str_comment_you_were_defeated_allied_unfriendly"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (assign, ":comment", "str_comment_you_were_defeated_allied"),
         (assign, ":relevance", 65),
       (try_end),
#Post 0907 changes end

#Post 0907 changes begin
     (else_try),
       (eq, ":entry_type", logent_player_retreated_from_lord),
       (troop_slot_eq, "$g_talk_troop", slot_troop_present_at_event, ":log_entry_no"),
       (try_begin),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_you_abandoned_us_unfriendly_spiteful"),
           (assign, ":relevance", 150),
           (assign, ":suggested_relation_change", -5),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (eq, ":reputation", lrep_selfrighteous),        
           (assign, ":comment", "str_comment_you_abandoned_us_unfriendly_pitiless"),
           (assign, ":relevance", 150),
           (assign, ":suggested_relation_change", -5),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_you_abandoned_us_spiteful"),
           (assign, ":suggested_relation_change", -5),
       (else_try),
           (eq, ":reputation", lrep_martial),
           (assign, ":comment", "str_comment_you_abandoned_us_chivalrous"),
           (assign, ":relevance", 150),
           (assign, ":suggested_relation_change", -2),
       (else_try),
           (this_or_next|eq, ":reputation", lrep_upstanding),
               (eq, ":reputation", lrep_goodnatured),        
           (assign, ":comment", "str_comment_you_abandoned_us_benefitofdoubt"),
           (assign, ":relevance", 150),
           (assign, ":suggested_relation_change", -1),
       (else_try),
           (assign, ":comment", "str_comment_you_abandoned_us_default"),
           (assign, ":relevance", 150),
           (assign, ":suggested_relation_change", -2),
       (try_end),


#Post 0907 changes end

     (else_try),
       (this_or_next|eq, ":entry_type", logent_player_retreated_from_lord),
            (eq, ":entry_type", logent_player_retreated_from_lord_cowardly),
       (eq, ":troop_object", "$g_talk_troop"),
       (try_begin),
         (eq, "$cheat_mode", 1),
         (assign, reg7, ":entry_hours_elapsed"),
         (display_message, "@Elapsed hours: {reg7}"),
       (try_end),
       (gt, ":entry_hours_elapsed", 2),
       (try_begin),
         (this_or_next|eq, ":reputation", lrep_selfrighteous),
                (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_ran_from_me_enemy_spiteful"),
         (assign, ":relevance", 25),
       (else_try),
         (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_you_ran_from_me_enemy_chivalrous"),
         (assign, ":relevance", 25),
       (else_try),
         (this_or_next|eq, ":reputation", lrep_goodnatured),
                (eq, ":reputation", lrep_upstanding),
         (assign, ":comment", "str_comment_you_ran_from_me_enemy_benevolent"),
         (assign, ":relevance", 25),
       (else_try),
         (eq, ":reputation", lrep_cunning),
         (assign, ":comment", "str_comment_you_ran_from_me_enemy_coldblooded"),
         (assign, ":relevance", 25),
       (else_try),
         (assign, ":comment", "str_comment_you_ran_from_me_enemy"),
         (assign, ":relevance", 25),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_player_retreated_from_lord_cowardly),
       (try_begin),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (neq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_relation", 5),
         (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_you_ran_from_foe_allied_chivalrous"),
         (assign, ":relevance", 80),
         (assign, ":suggested_relation_change", -3),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (neq, ":troop_object", "$g_talk_troop"),
         (eq, ":reputation", lrep_upstanding),
         (assign, ":comment", "str_comment_you_ran_from_foe_allied_upstanding"),
         (assign, ":relevance", 80),
         (assign, ":suggested_relation_change", -1),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (neq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_relation", 5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_ran_from_foe_allied_spiteful"),
         (assign, ":relevance", 80),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_lord_defeated_but_let_go_by_player),
       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_let_me_go_spiteful"),
         (assign, ":relevance", 300),
         (assign, ":suggested_relation_change", -15),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (ge, "$g_talk_troop_faction_relation", 0),
         (assign, ":comment", "str_comment_you_let_me_go_default"),
         (assign, ":relevance", 300),
         (assign, ":suggested_relation_change", 2),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_faction_relation", 0),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_upstanding),
         (assign, ":suggested_relation_change", 5),
         (assign, ":relevance", 300),
         (assign, ":comment", "str_comment_you_let_me_go_enemy_chivalrous"),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_faction_relation", 0),
         (this_or_next|eq, ":reputation", lrep_selfrighteous),
             (eq, ":reputation", lrep_cunning),
         (assign, ":relevance", 300),
         (assign, ":comment", "str_comment_you_let_me_go_enemy_coldblooded"),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_faction_relation", 0),
         (assign, ":relevance", 300),
         (assign, ":comment", "str_comment_you_let_me_go_enemy"),
         (assign, ":suggested_relation_change", 1),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (neq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_let_go_a_lord_allied_chivalrous"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (neq, ":troop_object", "$g_talk_troop"),
         (eq, ":reputation", lrep_upstanding),
         (assign, ":comment", "str_comment_you_let_go_a_lord_allied_upstanding"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (neq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_cunning),
             (eq, ":reputation", lrep_selfrighteous),
         (assign, ":comment", "str_comment_you_let_go_a_lord_allied_coldblooded"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (neq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_let_go_a_lord_allied_unfriendly_spiteful"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (neq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_let_go_a_lord_allied"),
         (assign, ":relevance", 80),
       (try_end),

#Internal faction relations

     (else_try),
       (eq, ":entry_type", logent_pledged_allegiance),
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":faction_object", "$g_talk_troop_faction"),
         (neq, ":troop_object", "$g_talk_troop"),
         (assign, ":relevance", 200),
         (try_begin),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_martial),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_martial_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_martial),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_martial"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_quarrelsome),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_quarrelsome_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_quarrelsome),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_quarrelsome"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_selfrighteous),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_selfrighteous_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_selfrighteous),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_selfrighteous"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_cunning),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_cunning_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_cunning),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_cunning"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_debauched_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_debauched"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_goodnatured),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_goodnatured_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_goodnatured),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_goodnatured"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_upstanding_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_upstanding"),
         (try_end),
       (try_end),


     (else_try),
       (eq, ":entry_type", logent_fief_granted_village),
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":faction_object", "$g_talk_troop_faction"),
         (neq, ":troop_object", "$g_talk_troop"),
         (eq, ":faction_object", "$players_kingdom"),
         (assign, ":relevance", 110),
         (try_begin),
            (gt, "$g_talk_troop_relation", 5),
            (this_or_next|eq, ":reputation", lrep_selfrighteous),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_friendly_cruel"),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_cunning),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_friendly_cynical"),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_friendly"),
         (else_try),
            (is_between, "$g_talk_troop_relation", -5, 5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_spiteful"),
            (assign, ":suggested_relation_change", -2),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_unfriendly_upstanding"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_unfriendly_spiteful"),
         (else_try),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied"),
         (try_end),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_renounced_allegiance),
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":faction_object", "$g_talk_troop_faction"),
         (neq, ":troop_object", "$g_talk_troop"),
         (try_begin),
           (ge, "$g_talk_troop_faction_relation", 0),
           (neq, "$g_talk_troop_faction", "$players_kingdom"),
           (assign, ":relevance", 180),
           (try_begin),
             (gt, "$g_talk_troop_relation", 5),
             (assign, ":comment", "str_comment_you_renounced_your_alliegance_friendly"),
           (else_try),
             (ge, "$g_talk_troop_relation", 0),
             (eq, ":reputation", lrep_goodnatured),
             (assign, ":comment", "str_comment_you_renounced_your_alliegance_friendly"),
           (try_end),
         (else_try),
           (lt, "$g_talk_troop_faction_relation", 0),
           (assign, ":relevance", 300),
           (try_begin),
              (ge, "$g_talk_troop_relation", 0),
              (this_or_next|eq, ":reputation", lrep_selfrighteous),
                  (eq, ":reputation", lrep_debauched),
              (assign, ":comment", "str_comment_you_renounced_your_alliegance_unfriendly_moralizing"),
           (else_try),
              (gt, "$g_talk_troop_relation", 5),
              (this_or_next|eq, ":reputation", lrep_goodnatured),
                (eq, ":reputation", lrep_upstanding),
              (assign, ":comment", "str_comment_you_renounced_your_alliegance_enemy_friendly"),
           (else_try),
              (gt, "$g_talk_troop_relation", 5),
              (assign, ":comment", "str_comment_you_renounced_your_alliegance_enemy"),
           (else_try),
              (is_between, "$g_talk_troop_relation", -5, 5),
              (this_or_next|eq, ":reputation", lrep_quarrelsome),
                  (eq, ":reputation", lrep_debauched),
              (assign, ":comment", "str_comment_you_renounced_your_alliegance_unfriendly_spiteful"),
              (assign, ":suggested_relation_change", -2),
           (else_try),
              (lt, "$g_talk_troop_relation", -5),
              (this_or_next|eq, ":reputation", lrep_quarrelsome),
              (this_or_next|eq, ":reputation", lrep_selfrighteous),
                (eq, ":reputation", lrep_debauched),
              (assign, ":comment", "str_comment_you_renounced_your_alliegance_unfriendly_spiteful"),
           (else_try),
              (assign, ":comment", "str_comment_you_renounced_your_alliegance_default"),
           (try_end),
         (try_end),
       (try_end),

     (try_end),
     (assign, reg0, ":comment"),
     (assign, reg1, ":relevance"),
     (assign, reg2, ":suggested_relation_change"),
     ]),

  # script_get_relevant_comment_to_s42
  # Input: none
  # Output: reg0 = 1 if comment found, 0 otherwise; s61 will contain comment string if found
  ("get_relevant_comment_to_s42",
    [(troop_get_slot, ":reputation", "$g_talk_troop", slot_lord_reputation_type),
     (try_begin),
       (eq, "$cheat_mode", 1),
       (store_add, ":rep_string", ":reputation", "str_personality_archetypes"),
       (str_store_string, s15, ":rep_string"),
       (display_message, "@Reputation type: {s15}"),
     (try_end),
      
     (assign, ":highest_score_so_far", 50),
     (assign, ":best_comment_so_far", -1),
     (assign, ":comment_found", 0),
     (assign, ":best_log_entry", -1),
     (assign, ":comment_relation_change", 0),
     (store_current_hours, ":current_time"),

#prevents multiple comments in conversations in same hour

#     (troop_get_slot, ":talk_troop_last_comment_time", "$g_talk_troop", slot_troop_last_comment_time),
#"$num_log_entries should also be set to one, not zero. This is included in the initialize npcs script, although could be moved to game_start
     (troop_get_slot, ":talk_troop_last_comment_slot", "$g_talk_troop", slot_troop_last_comment_slot),
     (troop_set_slot, "$g_talk_troop", slot_troop_last_comment_slot, "$num_log_entries"),

     (store_add, ":log_entries_plus_one", "$num_log_entries", 1),
     (try_for_range, ":log_entry_no", 1, ":log_entries_plus_one"),
#      It should be log entries plus one, so that the try_ sequence does not stop short of the last log entry
#      $Num_log_entries is now the number of the last log entry, which begins at "1" rather than "0"
#      This is so that (le, ":log_entry_no", ":talk_troop_last_comment_slot") works properly
     
       (troop_get_slot, ":entry_time",           "trp_log_array_entry_time",           ":log_entry_no"),
#      (val_max, ":entry_time", 1), #This is needed for pre-game events to be commented upon, if hours are used rather than the order of events
       (store_sub, ":entry_hours_elapsed", ":current_time", ":entry_time"),
       (try_begin),
         (le, ":log_entry_no", ":talk_troop_last_comment_slot"),
#         (le, ":entry_time", ":talk_troop_last_comment_time"),
         (try_begin),
           (eq, ":log_entry_no", ":talk_troop_last_comment_slot"),
           (eq, "$cheat_mode", 1),
           (assign, reg5, ":log_entry_no"),
           (display_message, "@Entries up to #{reg5} skipped"),
         (try_end),
#       I suggest using the log entry number as opposed to time so that events in the same hour can be commented upon
#       This feels more natural, for example, if there are other lords in the court when the player pledges allegiance     
       (else_try),
#         (le, ":entry_hours_elapsed", 3), #don't comment on really fresh events 
#       (else_try),
         (call_script, "script_get_relevant_comment_for_log_entry", ":log_entry_no"),
         (gt, reg1, 10),
         (assign, ":score", reg1),
         (assign, ":comment", reg0),
         (store_random_in_range, ":rand", 70, 140),
         (val_mul, ":score", ":rand"),
         (store_add, ":entry_time_score", ":entry_hours_elapsed", 500), #approx. one month 
         (val_mul, ":score", 1000),
         (val_div, ":score", ":entry_time_score"), ###Relevance decreases over time - halved after one month, one-third after two, etc
         (try_begin),
           (gt, ":score", ":highest_score_so_far"),
           (assign, ":highest_score_so_far", ":score"),
           (assign, ":best_comment_so_far",  ":comment"),
           (assign, ":best_log_entry", ":log_entry_no"),
           (assign, ":comment_relation_change", reg2),
         (try_end),
       (try_end),
     (try_end),

     (try_begin),
       (gt, ":best_comment_so_far", 0),
       (assign, ":comment_found", 1), #comment found print it to s61 now. 
       (troop_get_slot, ":actor",                 "trp_log_array_actor",                 ":best_log_entry"),
       (troop_get_slot, ":center_object",         "trp_log_array_center_object",         ":best_log_entry"),
       (troop_get_slot, ":center_object_lord",    "trp_log_array_center_object_lord",    ":best_log_entry"),
       (troop_get_slot, ":center_object_faction", "trp_log_array_center_object_faction", ":best_log_entry"),
       (troop_get_slot, ":troop_object",          "trp_log_array_troop_object",          ":best_log_entry"),
       (troop_get_slot, ":troop_object_faction",  "trp_log_array_troop_object_faction",  ":best_log_entry"),
       (troop_get_slot, ":faction_object",        "trp_log_array_faction_object",        ":best_log_entry"),
       (try_begin),
         (ge, ":actor", 0),
         (str_store_troop_name,   s50, ":actor"),
       (try_end),
       (try_begin),
         (ge, ":center_object", 0),
         (str_store_party_name,   s51, ":center_object"),
       (try_end),
       (try_begin),
         (ge, ":center_object_lord", 0),
         (str_store_troop_name,   s52, ":center_object_lord"),
       (try_end),
       (try_begin),
         (ge, ":center_object_faction", 0),
         (str_store_faction_name, s53, ":center_object_faction"),
       (try_end),
       (try_begin),
         (ge, ":troop_object", 0),
         (str_store_troop_name,   s54, ":troop_object"),
       (try_end),
       (try_begin),
         (ge, ":troop_object_faction", 0),
         (str_store_faction_name, s55, ":troop_object_faction"),
       (try_end),
       (try_begin),
         (ge, ":faction_object", 0),
         (str_store_faction_name, s56, ":faction_object"),
       (try_end),
       (str_store_string, s42, ":best_comment_so_far"),
     (try_end),
     
     (assign, reg0, ":comment_found"),
     (assign, "$log_comment_relation_change", ":comment_relation_change"),
     ]),

#Troop Commentaries end

#Rebellion changes begin
  ("find_rival_from_faction",
    [
     (store_script_param, ":source_lord", 1),
     (store_script_param, ":target_faction", 2),

     (assign, ":rival", 0),
     (troop_get_slot, ":source_reputation", ":source_lord", slot_lord_reputation_type),

     (try_for_range, ":target_lord", kingdom_heroes_begin, kingdom_heroes_end),
         (store_troop_faction, ":test_faction", ":target_lord"),
         (eq, ":test_faction", ":target_faction"),
         (troop_get_slot, ":target_reputation", ":target_lord", slot_lord_reputation_type),
         (try_begin),
             (eq, ":source_reputation", lrep_martial),
             (eq, ":target_reputation", lrep_martial),
             (assign, ":rival", ":target_lord"),
         (else_try),
             (eq, ":source_reputation", lrep_debauched),
             (eq, ":target_reputation", lrep_upstanding),
             (assign, ":rival", ":target_lord"),
         (else_try),
             (eq, ":source_reputation", lrep_selfrighteous),
             (eq, ":target_reputation", lrep_goodnatured),
             (assign, ":rival", ":target_lord"),
         (else_try),
             (eq, ":source_reputation", lrep_cunning),
             (eq, ":target_reputation", lrep_quarrelsome),
             (assign, ":rival", ":target_lord"),
         (else_try),
             (eq, ":source_reputation", lrep_quarrelsome),
             (eq, ":target_reputation", lrep_cunning),
             (assign, ":rival", ":target_lord"),
         (else_try),
             (eq, ":source_reputation", lrep_goodnatured),
             (eq, ":target_reputation", lrep_selfrighteous),
             (assign, ":rival", ":target_lord"),
         (else_try),
             (eq, ":source_reputation", lrep_upstanding),
             (eq, ":target_reputation", lrep_debauched),
             (assign, ":rival", ":target_lord"),
         (try_end),
     (try_end),

     (assign, reg0, ":rival"),
]),


  ("rebellion_arguments",
    [
     (store_script_param, ":lord", 1),
     (store_script_param, ":argument", 2),

     (assign, ":argument_value", 0),
     (troop_get_slot, ":reputation", ":lord", slot_lord_reputation_type),
     (try_begin),
         (eq, ":reputation", lrep_martial),
         (try_begin),(eq, ":argument", argument_claim  ),(assign, ":argument_value", 30),
         (else_try) ,(eq, ":argument", argument_ruler  ),(assign, ":argument_value", 10),
         (else_try) ,(eq, ":argument", argument_benefit),(assign, ":argument_value",-20),
         (else_try) ,(eq, ":argument", argument_victory),(assign, ":argument_value",-30),
         (try_end),
     (else_try),
         (eq, ":reputation", lrep_quarrelsome),
         (try_begin),(eq, ":argument", argument_claim  ),(assign, ":argument_value",-20),
         (else_try) ,(eq, ":argument", argument_ruler  ),(assign, ":argument_value",-30),
         (else_try) ,(eq, ":argument", argument_benefit),(assign, ":argument_value", 30),
         (else_try) ,(eq, ":argument", argument_victory),(assign, ":argument_value", 10),
         (try_end),
     (else_try),
         (eq, ":reputation", lrep_selfrighteous),
         (try_begin),(eq, ":argument", argument_claim  ),(assign, ":argument_value",-20),
         (else_try) ,(eq, ":argument", argument_ruler  ),(assign, ":argument_value",-30),
         (else_try) ,(eq, ":argument", argument_benefit),(assign, ":argument_value", 20),
         (else_try) ,(eq, ":argument", argument_victory),(assign, ":argument_value", 20),
         (try_end),
	 (else_try),
         (eq, ":reputation", lrep_cunning),
         (try_begin),(eq, ":argument", argument_claim  ),(assign, ":argument_value",-30),
         (else_try) ,(eq, ":argument", argument_ruler  ),(assign, ":argument_value", 20),
         (else_try) ,(eq, ":argument", argument_benefit),(assign, ":argument_value",-20),
         (else_try) ,(eq, ":argument", argument_victory),(assign, ":argument_value", 20),
         (try_end),
     (else_try),
         (eq, ":reputation", lrep_debauched),
         (try_begin),(eq, ":argument", argument_claim  ),(assign, ":argument_value",-20),
         (else_try) ,(eq, ":argument", argument_ruler  ),(assign, ":argument_value",-20),
         (else_try) ,(eq, ":argument", argument_benefit),(assign, ":argument_value", 20),
         (else_try) ,(eq, ":argument", argument_victory),(assign, ":argument_value", 10),
         (try_end),
     (else_try),
         (eq, ":reputation", lrep_goodnatured),
         (try_begin),(eq, ":argument", argument_claim  ),(assign, ":argument_value", 10),
         (else_try) ,(eq, ":argument", argument_ruler  ),(assign, ":argument_value", 20),
         (else_try) ,(eq, ":argument", argument_benefit),(assign, ":argument_value",-15),
         (else_try) ,(eq, ":argument", argument_victory),(assign, ":argument_value",-25),
         (try_end),
     (else_try),
         (eq, ":reputation", lrep_upstanding),
         (try_begin),(eq, ":argument", argument_claim  ),(assign, ":argument_value", 10),
         (else_try) ,(eq, ":argument", argument_ruler  ),(assign, ":argument_value",  0),
         (else_try) ,(eq, ":argument", argument_benefit),(assign, ":argument_value",-40),
         (else_try) ,(eq, ":argument", argument_victory),(assign, ":argument_value", 10),
         (try_end),
     (try_end),
     (assign, reg0, ":argument_value"),
]),

#Rebellion changes end

  # script_get_culture_with_party_faction_for_music
  # Input: arg1 = party_no
  # Output: reg0 = culture
  ("get_culture_with_party_faction_for_music",
    [
      (store_script_param, ":party_no", 1),
      (store_faction_of_party, ":faction_no", ":party_no"),
      (try_begin),
        (this_or_next|eq, ":faction_no", "fac_player_faction"),
        (eq, ":faction_no", "fac_player_supporters_faction"),
        (assign, ":faction_no", "$players_kingdom"),
      (try_end),
      (try_begin),
        (is_between, ":party_no", centers_begin, centers_end),
        (this_or_next|eq, ":faction_no", "fac_player_supporters_faction"),
        (neg|is_between, ":faction_no", kingdoms_begin, kingdoms_end),
        (party_get_slot, ":faction_no", ":party_no", slot_center_original_faction),
      (try_end),
      (try_begin),
        (eq, ":faction_no", "fac_gondor"),
        (assign, ":result", mtf_culture_1),
      (else_try),
        (eq, ":faction_no", "fac_rohan"),
        (assign, ":result", mtf_culture_2),
      (else_try),
        (eq, ":faction_no", "fac_isengard"),
        (assign, ":result", mtf_culture_3),
      (else_try),
        (eq, ":faction_no", "fac_mordor"),
        (assign, ":result", mtf_culture_4),
      (else_try),
        (eq, ":faction_no", "fac_harad"),
        (assign, ":result", mtf_culture_5),
      (else_try),
        (eq, ":faction_no", "fac_rhun"),
        (assign, ":result", mtf_culture_6),
      # (else_try),
        # (eq, ":faction_no", "fac_khand"),
        # (assign, ":result", mtf_culture_7),
      # (else_try),
        # (eq, ":faction_no", "fac_umbar"),
        # (assign, ":result", mtf_culture_8),
      # (else_try),
        # (eq, ":faction_no", "fac_lorien"),
        # (assign, ":result", mtf_culture_9),
      # (else_try),
        # (eq, ":faction_no", "fac_imladris"),
        # (assign, ":result", mtf_culture_10),
      # (else_try),
        # (eq, ":faction_no", "fac_woodelf"),
        # (assign, ":result", mtf_culture_11),
      # (else_try),
        # (eq, ":faction_no", "fac_moria"),
        # (assign, ":result", mtf_culture_12),
      # (else_try),
        # (eq, ":faction_no", "fac_guldur"),
        # (assign, ":result", mtf_culture_13),
      # (else_try),
        # (eq, ":faction_no", "fac_northmen"),
        # (assign, ":result", mtf_culture_14),
      # (else_try),
        # (eq, ":faction_no", "fac_gundabad"),
        # (assign, ":result", mtf_culture_15),
      # (else_try),
        # (eq, ":faction_no", "fac_dale"),
        # (assign, ":result", mtf_culture_16),
      # (else_try),
        # (eq, ":faction_no", "fac_dwarf"),
        # (assign, ":result", mtf_culture_17),
      # (else_try),
        # (eq, ":faction_no", "fac_dunland"),
        # (assign, ":result", mtf_culture_18),
      (else_try),
        (this_or_next|eq, ":faction_no", "fac_outlaws"),
#        (this_or_next|eq, ":faction_no", "fac_peasant_rebels"),
        (this_or_next|eq, ":faction_no", "fac_deserters"),
        (this_or_next|eq, ":faction_no", "fac_mountain_bandits"),
        (eq, ":faction_no", "fac_forest_bandits"),
        (assign, ":result", mtf_culture_6),
      (else_try),
        (assign, ":result", 0), #no culture, including player with no bindings to another kingdom
      (try_end),
      (assign, reg0, ":result"),
     ]),

  # script_music_set_situation_with_culture
  # Input: arg1 = music_situation
  ("music_set_situation_with_culture",
    [ (store_script_param, ":situation", 1),
      (assign, ":culture", 0), #no culture
      (try_begin),
        (this_or_next|eq, ":situation", mtf_sit_town),
        (this_or_next|eq, ":situation", mtf_sit_day),
        (this_or_next|eq, ":situation", mtf_sit_night),
        (this_or_next|eq, ":situation", mtf_sit_town_infiltrate),
        (eq, ":situation", mtf_sit_encounter_hostile),
        (call_script, "script_get_culture_with_party_faction_for_music", "$g_encountered_party"),
        (val_or, ":culture", reg0),
      (else_try),
        (this_or_next|eq, ":situation", mtf_sit_ambushed),
        (eq, ":situation", mtf_sit_fight),
        (call_script, "script_get_culture_with_party_faction_for_music", "$g_encountered_party"),
        (val_or, ":culture", reg0),
        (call_script, "script_get_culture_with_party_faction_for_music", "p_main_party"),
        (val_or, ":culture", reg0),
        (call_script, "script_get_closest_center", "p_main_party"),
        (call_script, "script_get_culture_with_party_faction_for_music", reg0),
        (val_or, ":culture", reg0),
      (else_try),
        (eq, ":situation", mtf_sit_travel),
        (call_script, "script_get_culture_with_party_faction_for_music", "p_main_party"),
        (val_or, ":culture", reg0),
        (call_script, "script_get_closest_center", "p_main_party"),
        (call_script, "script_get_culture_with_party_faction_for_music", reg0),
        (val_or, ":culture", reg0),
      (else_try),
        (eq, ":situation", mtf_sit_victorious),
        (call_script, "script_get_culture_with_party_faction_for_music", "p_main_party"),
        (val_or, ":culture", reg0),
      (else_try),
        (eq, ":situation", mtf_sit_killed),
        (call_script, "script_get_culture_with_party_faction_for_music", "$g_encountered_party"),
        (val_or, ":culture", reg0),
      (try_end),
      (try_begin),
        (this_or_next|eq, ":situation", mtf_sit_town),
        (eq, ":situation", mtf_sit_day),
        (try_begin),
          (is_currently_night),
          (assign, ":situation", mtf_sit_night),
        (try_end),
      (try_end),
      (music_set_situation, ":situation"),
      (music_set_culture, ":culture"),
     ]),

  
  # script_combat_music_set_situation_with_culture
  ("combat_music_set_situation_with_culture",
    [ (assign, ":situation", mtf_sit_fight),
      (assign, ":num_allies", 0),
      (assign, ":num_enemies", 0),
      (try_for_agents, ":agent_no"),
        (agent_is_alive, ":agent_no"),
        (agent_is_human, ":agent_no"),
        (agent_get_troop_id, ":agent_troop_id", ":agent_no"),
        (store_character_level, ":troop_level", ":agent_troop_id"),
        (val_add,  ":troop_level", 10),
        (val_mul, ":troop_level", ":troop_level"),
        (try_begin),
          (agent_is_ally, ":agent_no"),
          (val_add, ":num_allies", ":troop_level"),
        (else_try),
          (val_add, ":num_enemies", ":troop_level"),
        (try_end),
      (try_end),
      (val_mul, ":num_allies", 4), #play ambushed music if we are 2 times outnumbered.
      (val_div, ":num_allies", 3),
      (try_begin),
        (lt, ":num_allies", ":num_enemies"),
        (assign, ":situation", mtf_sit_ambushed),
      (try_end),
      (call_script, "script_music_set_situation_with_culture", ":situation"),
     ]),

  # script_play_victorious_sound
  # Input: none
  # Output: none
  ("play_victorious_sound",
   [  (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
#      (play_cue_track, "track_victorious_neutral_1"),
#      (play_track, "track_victorious_neutral_1", 1),
     ]),
  
  # script_set_items_for_tournament
  # Input: arg1 = horse_chance, arg2 = lance_chance (with horse only), arg3 = sword_chance, arg4 = axe_chance, arg5 = bow_chance (without horse only), arg6 = javelin_chance (with horse only), arg7 = mounted_bow_chance (with horse only), arg8 = crossbow_sword_chance, arg9 = armor_item_begin, arg10 = helm_item_begin
  # Output: none (sets mt_arena_melee_fight items)
  ("set_items_for_tournament",
    [
      (store_script_param, ":horse_chance", 1),
      (store_script_param, ":lance_chance", 2),
      (store_script_param, ":sword_chance", 3),
      (store_script_param, ":axe_chance", 4),
      (store_script_param, ":bow_chance", 5),
      (store_script_param, ":javelin_chance", 6),
      (store_script_param, ":mounted_bow_chance", 7),
      (store_script_param, ":crossbow_sword_chance", 8),
      (store_script_param, ":armor_item_begin", 9),
      (store_script_param, ":helm_item_begin", 10),
      (store_add, ":total_chance", ":sword_chance", ":axe_chance"),
      (val_add, ":total_chance", ":crossbow_sword_chance"),
      (try_for_range, ":i_ep", 0, 32),
        (mission_tpl_entry_clear_override_items, "mt_arena_melee_fight", ":i_ep"),
        (assign, ":has_horse", 0),
        (store_div, ":cur_team", ":i_ep", 8),
        (try_begin),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", ":horse_chance"),
          (assign, ":has_horse", 1),
        (try_end),
        (try_begin),
          (eq, ":has_horse", 1),
          (store_add, ":cur_total_chance", ":total_chance", ":lance_chance"),
          (val_add, ":cur_total_chance", ":javelin_chance"),
          (val_add, ":cur_total_chance", ":mounted_bow_chance"),
        (else_try),
          (store_add, ":cur_total_chance", ":total_chance", ":bow_chance"),
        (try_end),
        (store_random_in_range, ":random_no", 0, ":cur_total_chance"),
        (try_begin),
          (val_sub, ":random_no", ":sword_chance"),
          (lt, ":random_no", 0),
          (try_begin),
            (store_random_in_range, ":sub_random_no", 0, 100),
            (lt, ":sub_random_no", 50),
#            (mission_tpl_entry_add_override_item, "mt_arena_melee_fight", ":i_ep", "itm_practice_shield"),
          (else_try),
          (try_end),
        (else_try),
          (val_sub, ":random_no", ":axe_chance"),
          (lt, ":random_no", 0),
#         (mission_tpl_entry_add_override_item, "mt_arena_melee_fight", ":i_ep", "itm_practice_shield"),
        (else_try),
          (val_sub, ":random_no", ":crossbow_sword_chance"),
          (lt, ":random_no", 0),
        (else_try),
          (eq, ":has_horse", 0),
          (val_sub, ":random_no", ":bow_chance"),
          (lt, ":random_no", 0),
        (else_try),
          (eq, ":has_horse", 1),
          (val_sub, ":random_no", ":lance_chance"),
          (lt, ":random_no", 0),
#          (mission_tpl_entry_add_override_item, "mt_arena_melee_fight", ":i_ep", "itm_practice_shield"),
        (else_try),
          (eq, ":has_horse", 1),
          (val_sub, ":random_no", ":javelin_chance"),
          (lt, ":random_no", 0),
#          (mission_tpl_entry_add_override_item, "mt_arena_melee_fight", ":i_ep", "itm_practice_shield"),
        (else_try),
          (eq, ":has_horse", 1),
          (val_sub, ":random_no", ":mounted_bow_chance"),
          (lt, ":random_no", 0),
          #(mission_tpl_entry_add_override_item, "mt_arena_melee_fight", ":i_ep", "itm_practice_bow"),
          #(mission_tpl_entry_add_override_item, "mt_arena_melee_fight", ":i_ep", "itm_practice_arrows"),
        (try_end),
        (try_begin),
          (ge, ":armor_item_begin", 0),
          (store_add, ":cur_armor_item", ":armor_item_begin", ":cur_team"),
          (mission_tpl_entry_add_override_item, "mt_arena_melee_fight", ":i_ep", ":cur_armor_item"),
        (try_end),
        (try_begin),
          (ge, ":helm_item_begin", 0),
          (store_add, ":cur_helm_item", ":helm_item_begin", ":cur_team"),
          (mission_tpl_entry_add_override_item, "mt_arena_melee_fight", ":i_ep", ":cur_helm_item"),
        (try_end),
      (try_end),
     ]),

  
  # script_custom_battle_end
  # Input: none
  # Output: none
  ("custom_battle_end",
    [ (assign, "$g_custom_battle_team1_death_count", 0),
      (assign, "$g_custom_battle_team2_death_count", 0),
      (try_for_agents, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (neg|agent_is_alive, ":cur_agent"),
        (agent_get_team, ":cur_team", ":cur_agent"),
        (try_begin),
          (eq, ":cur_team", 0),
          (val_add, "$g_custom_battle_team1_death_count", 1),
        (else_try),
          (val_add, "$g_custom_battle_team2_death_count", 1),
        (try_end),
      (try_end),
      ]),  

  # script_remove_troop_from_prison
  # Input: troop_no
  # Output: none
  ("remove_troop_from_prison",
    [ (store_script_param, ":troop_no", 1),
      (troop_set_slot, ":troop_no", slot_troop_prisoner_of_party, -1),
      (try_begin),
        (check_quest_active, "qst_rescue_lord_by_replace"),
        (quest_slot_eq, "qst_rescue_lord_by_replace", slot_quest_target_troop, ":troop_no"),
        (call_script, "script_cancel_quest", "qst_rescue_lord_by_replace"),
      (try_end),
      (try_begin),
        (check_quest_active, "qst_deliver_message_to_prisoner_lord"),
        (quest_slot_eq, "qst_deliver_message_to_prisoner_lord", slot_quest_target_troop, ":troop_no"),
        (call_script, "script_cancel_quest", "qst_deliver_message_to_prisoner_lord"),
      (try_end),
    ]),  

	
  # script_TLD_troop_banner_slot_init 
  # run at the start of the game
  ("TLD_troop_banner_slot_init",
  [ (troop_set_slot, "trp_woodsman_of_lossarnach",               slot_troop_banner_scene_prop, "mesh_banner_e02"),
    (troop_set_slot, "trp_axeman_of_lossarnach",       slot_troop_banner_scene_prop, "mesh_banner_e03"),
    (troop_set_slot, "trp_axemaster_of_lossarnach",        slot_troop_banner_scene_prop, "mesh_banner_e04"),
    (troop_set_slot, "trp_clansman_of_lamedon",             slot_troop_banner_scene_prop, "mesh_banner_e09"),
    (troop_set_slot, "trp_footman_of_lamedon",        slot_troop_banner_scene_prop, "mesh_banner_e10"),
    (troop_set_slot, "trp_veteran_of_lamedon",           slot_troop_banner_scene_prop, "mesh_banner_e11"),
    (troop_set_slot, "trp_warrior_of_pinnath_gelin",        slot_troop_banner_scene_prop, "mesh_banner_e05"),
    (troop_set_slot, "trp_veteran_warrior_of_pinnath_gelin",slot_troop_banner_scene_prop, "mesh_banner_e06"),
    (troop_set_slot, "trp_champion_of_pinnath_gelin",       slot_troop_banner_scene_prop, "mesh_banner_e07"),
    ## BRV does not have shields
    (troop_set_slot, "trp_dol_amroth_youth",                slot_troop_banner_scene_prop, "mesh_banner_e16"),
    (troop_set_slot, "trp_squire_of_dol_amroth",            slot_troop_banner_scene_prop, "mesh_banner_e17"),
    (troop_set_slot, "trp_veteran_squire_of_dol_amroth",    slot_troop_banner_scene_prop, "mesh_banner_e17"),
    (troop_set_slot, "trp_knight_of_dol_amroth",            slot_troop_banner_scene_prop, "mesh_banner_e18"),
    (troop_set_slot, "trp_veteran_knight_of_dol_amroth",    slot_troop_banner_scene_prop, "mesh_banner_e18"),
    (troop_set_slot, "trp_swan_knight_of_dol_amroth",       slot_troop_banner_scene_prop, "mesh_banner_e18"),
#    (display_message,"@DEBUG: banner slots assigned for Gondor troops!"),
  ]),

  #script_TLD_shield_item_set_banner, by GA
  # INPUT: agent_no
  ("TLD_shield_item_set_banner",
  [ (store_script_param, ":tableau_no",1),
    (store_script_param, ":agent_no", 2),
    (store_script_param, ":troop_no", 3),
#    (assign, ":banner_troop", -1),
    (assign, ":banner_mesh", "mesh_banners_default_b"),
    (try_begin),
        (neq,":agent_no",-1),
#        (agent_get_party_id,":party",":agent_no"),
        (try_begin),
            (is_between,":troop_no","trp_rhun_tribesman","trp_rhun_veteran_swift_horseman"),# Rhun randomized heraldry
            (store_random_in_range,":banner_mesh","mesh_circular_8mosaic1","mesh_circular_8mosaic10"),                                            
        (else_try),
            (is_between,":troop_no","trp_harad_desert_warrior","trp_black_serpent_horse_archer"),# Harad randomized heraldry
            (store_random_in_range,":banner_mesh",275,300),                                            
        #(else_try),
            #(eq,"$player_universal_banner",1),                # indicator for the ability to set player's own banner
            #(eq,":party",":player_party"),
            #(troop_get_slot,":banner_mesh","trp_player",slot_troop_banner_scene_prop),
        (try_end),
    (try_end),
    (cur_item_set_tableau_material, ":tableau_no",":banner_mesh"),
    ]),

  # script_TLD_initialize_civilian_clothes
  ("TLD_initialize_civilian_clothes", 
    [
    (store_script_param, ":tableau_no", 1),
    #(store_script_param, ":agent_no", 2),
    (store_script_param, ":troop_no", 3),
    (store_troop_faction, ":fac", ":troop_no"),
    (val_sub, ":fac", kingdoms_begin),
    (try_begin),
        ]+concatenate_scripts([
            [
            (eq, ":fac", x),
            (try_begin),
            ]+concatenate_scripts([
                [
                (eq, ":tableau_no", fac_tableau_list[x][z][0]),
                (store_random_in_range, ":rand", 0, len(fac_tableau_list[x][z][1])),
                (try_begin),
                ]+concatenate_scripts([
                    [
                    (eq, ":rand", y),
                    (cur_item_set_tableau_material, ":tableau_no", fac_tableau_list[x][z][1][y]),
                (else_try),
                    ] for y in range(len(fac_tableau_list[x][z][1]))
                ])+[
                (try_end),
            (else_try),
                ] for z in range(len(fac_tableau_list[x]))
            ])+[
            (try_end),
        (else_try),
            ] for x in range(len(fac_tableau_list))
        ])+[
    (try_end),
    ]
  ),

  # script_set_item_faction
  ("set_item_faction",  set_item_faction()), 
 
  # script_get_faction_mask
  # INPUT: faction
  #OUTPUT: reg30 faction mask
  ("get_faction_mask",  [
   (store_script_param_1, ":faction"),
   (assign,reg30,1),
   (try_for_range,":unused",0,":faction"),
      (val_mul,reg30,2),
   (try_end),
   ]),
   
  # script_fill_camp_chests
  # INPUT: faction
  # fills camp chests with items used by this faction
  ("fill_camp_chests",  [
   (store_script_param_1, ":faction"),
   (call_script,"script_get_faction_mask",":faction"),
   (assign,":fm",reg30),
   
   (troop_clear_inventory,"trp_camp_chest_faction"),
   (troop_clear_inventory,"trp_camp_chest_none"),
   (troop_ensure_inventory_space,"trp_camp_chest_faction",70),
   (troop_ensure_inventory_space,"trp_camp_chest_none",70),
   
   (store_add,":last_item_plus_one","itm_witchking_helmet",1),
   (try_for_range,":item","itm_no_item",":last_item_plus_one"),
      (item_get_slot,":item_faction_mask",":item",slot_item_faction),
#	  (assign,":ii",":item_faction_mask"),
      (try_begin),
        (eq,":item_faction_mask",0),
		  (troop_add_item,"trp_camp_chest_none",":item",0),
	  (else_try),
	    (val_and,":item_faction_mask",":fm"),
        (try_begin),
		  (neq,":item_faction_mask",0),
		    (troop_add_item,"trp_camp_chest_faction",":item",0),
		(try_end),
      (try_end),
   (try_end),

 ]),

# script_fill_merchants_CHEAT
# fills smiths across the land with faction stuff
("fill_merchants_cheat",  [
  (set_merchandise_modifier_quality,150),
  (try_for_range,":cur_merchant",weapon_merchants_begin,weapon_merchants_end),
    (reset_item_probabilities,100),     
    (troop_clear_inventory,":cur_merchant"),
	(store_troop_faction,":faction",":cur_merchant"),
    (call_script,"script_get_faction_mask",":faction"),(assign, ":fac_mask", reg30),
	(troop_get_slot,":subfaction",":cur_merchant",slot_troop_subfaction),
    (call_script,"script_get_faction_mask",":subfaction"),(assign, ":subfac_mask", reg30),
    (try_for_range,":item","itm_no_item","itm_witchking_helmet"),
      (item_get_slot,":item_faction_mask",":item",slot_item_faction),
      (val_and,":item_faction_mask",":fac_mask"),
      (item_get_slot,":item_subfaction_mask",":item",slot_item_subfaction),
      (val_and,":item_subfaction_mask",":subfac_mask"),
      (try_begin),
		(neq,":item_faction_mask",0),(neq,":item_subfaction_mask",0),(troop_add_item,":cur_merchant",":item",0),
	  (try_end),
   (try_end),
  (try_end),
]),


    ######################################
    # TLD faction ranks
    #
    # script_cf_get_soldiers
    # Used by faction rank sys to get troops of rank
    # Input: none
    # Output: none
    ("cf_get_soldiers",
    [
        (assign, "$g_move_heroes", 0),
        (assign, ":successful", 0),
#       (call_script, "script_party_remove_all_companions", "p_main_party"),
        (try_begin),
            (troop_get_slot,":faction_rank","trp_player",slot_troop_faction_rank),
            (store_and, ":pos", ":faction_rank", stfr_position_mask),
            (val_div, ":pos", stfr_position_unit),
            (store_and, ":rank", ":faction_rank", stfr_rank_mask),
            (val_div, ":rank", stfr_rank_unit),
        ]+concatenate_scripts([
            [
            (store_add, ":kd", kd, kingdoms_begin),
            (eq, ":kd", "$players_kingdom"),
            (try_begin),
            ]+concatenate_scripts([
                [
                (eq, ":rank", rnk),
                (try_begin),
                ]+concatenate_scripts([
                    [
                    (eq, ":pos", pos),
                    (try_begin),
                        (call_script, "script_game_get_party_companion_limit"),
                        (store_party_size_wo_prisoners, ":size", "p_main_party"),
                        (val_add, ":size", sum([tld_faction_ranks[kd][rnk][2][pos][tfr_soldiers_pos][stck][1] for stck in range(len(tld_faction_ranks[kd][rnk][2][pos][tfr_soldiers_pos]))])),
                        (le, ":size", reg0),
                        (assign, ":successful", 1),
                    ]+[
                    (party_add_members, "p_main_party", tld_faction_ranks[kd][rnk][2][pos][tfr_soldiers_pos][stck][0],
                                                        tld_faction_ranks[kd][rnk][2][pos][tfr_soldiers_pos][stck][1]) \
                        for stck in range(len(tld_faction_ranks[kd][rnk][2][pos][tfr_soldiers_pos]))
                    ]+[
                    (else_try),
                        (display_message, "@You company cannot take more men", 0xffff1493),
                    (try_end),
                (else_try),
                    ] for pos in range(len(tld_faction_ranks[kd][rnk][2]))
                ])+[
                (try_end),
            (else_try),
                ] for rnk in range(len(tld_faction_ranks[kd]))
            ])+[
            (try_end),        
        (else_try),
            ] for kd in range(len(tld_faction_ranks))
        ])+[
        (try_end),
        (eq, ":successful", 1),
    ]),

    # script_cf_get_supplies
    # Used by faction rank sys to get supplies of rank
    # Input: none
    # Output: none
    ("cf_get_supplies",
    [
        (store_free_inventory_capacity,":capacity", "trp_player"),
        (assign, ":continue", 0),
        (try_begin),
            (troop_get_slot,":faction_rank","trp_player",slot_troop_faction_rank),
            (store_and, ":pos", ":faction_rank", stfr_position_mask),
            (val_div, ":pos", stfr_position_unit),
            (store_and, ":rank", ":faction_rank", stfr_rank_mask),
            (val_div, ":rank", stfr_rank_unit),
        ]+concatenate_scripts([
            [
            (store_add, ":kd", kd, kingdoms_begin),
            (eq, ":kd", "$players_kingdom"),
            (try_begin),
            ]+concatenate_scripts([
                [
                (eq, ":rank", rnk),
                (try_begin),
                ]+concatenate_scripts([
                    [
                    (eq, ":pos", pos),
                    (try_begin),
                        (ge, ":capacity", sum(tld_faction_ranks[kd][rnk][2][pos][tfr_supplies_pos][stck][1] \
                        for stck in range(len(tld_faction_ranks[kd][rnk][2][pos][tfr_supplies_pos])))),
                        ]+[
                        (troop_add_items, "p_main_party", tld_faction_ranks[kd][rnk][2][pos][tfr_supplies_pos][stck][0],
                                                            tld_faction_ranks[kd][rnk][2][pos][tfr_supplies_pos][stck][1]) \
                            for stck in range(len(tld_faction_ranks[kd][rnk][2][pos][tfr_supplies_pos]))
                        ]+[
                        (assign, ":continue", 1),
                    (else_try),
                        (display_message, "@You inventory doesn't have enough space.", 0xffff1493),                    
                    (try_end),
                (else_try),
                    ] for pos in range(len(tld_faction_ranks[kd][rnk][2]))
                ])+[
                (try_end),
            (else_try),
                ] for rnk in range(len(tld_faction_ranks[kd]))
            ])+[
            (try_end),        
        (else_try),
            ] for kd in range(len(tld_faction_ranks))
        ])+[
        (try_end),
        (neq, ":continue", 0),
    ]),
    
    # script_cf_get_equipments
    # Used by faction rank sys to get equipments of rank
    # Input: none
    # Output: none
    ("cf_get_equipments",
    [
        (store_free_inventory_capacity,":capacity", "trp_player"),
        (assign, ":continue", 0),
        (try_begin),
            (troop_get_slot,":faction_rank","trp_player",slot_troop_faction_rank),
            (store_and, ":pos", ":faction_rank", stfr_position_mask),
            (val_div, ":pos", stfr_position_unit),
            (store_and, ":rank", ":faction_rank", stfr_rank_mask),
            (val_div, ":rank", stfr_rank_unit),
        ]+concatenate_scripts([
            [
            (store_add, ":kd", kd, kingdoms_begin),
            (eq, ":kd", "$players_kingdom"),
            (try_begin),
            ]+concatenate_scripts([
                [
                (eq, ":rank", rnk),
                (try_begin),
                ]+concatenate_scripts([
                    [
                    (eq, ":pos", pos),
                    (try_begin),
                        (ge, ":capacity", sum([tld_faction_ranks[kd][rnk][2][pos][tfr_equipments_pos][stck][1] \
                            for stck in range(len(tld_faction_ranks[kd][rnk][2][pos][tfr_equipments_pos]))])),
                        ]+[
                        (troop_add_items, "p_main_party", tld_faction_ranks[kd][rnk][2][pos][tfr_equipments_pos][stck][0],
                                                            tld_faction_ranks[kd][rnk][2][pos][tfr_equipments_pos][stck][1]) \
                            for stck in range(len(tld_faction_ranks[kd][rnk][2][pos][tfr_equipments_pos]))
                        ]+[
                        (assign, ":continue", 1),
                    (else_try),
                        (display_message, "@You inventory doesn't have enough space.", 0xffff1493),                    
                    (try_end),
                (else_try),
                    ] for pos in range(len(tld_faction_ranks[kd][rnk][2]))
                ])+[
                (try_end),
            (else_try),
                ] for rnk in range(len(tld_faction_ranks[kd]))
            ])+[
            (try_end),        
        (else_try),
            ] for kd in range(len(tld_faction_ranks))
        ])+[
        (try_end),
        (neq, ":continue", 0),    
    ]),

    ############# Condition scripts
    
    # script_cf_can_be_captain_of_the_eorl_guard
    # Input: none
    # Output: none
    # Fail if player fail the criterion to be captain of eorl guard
    ("cf_can_be_captain_of_the_eorl_guard", [
        (store_proficiency_level, ":onehanded", "trp_player", wpt_one_handed_weapon),
        (store_proficiency_level, ":polearm", "trp_player", wpt_polearm),
        (ge, ":onehanded", ":polearm"),
        ]
    ),
    
    # script_cf_can_be_captain_of_the_brego_guard
    # Input: none
    # Output: none
    # Fail if player fail the criterion to be captain of eorl guard
    ("cf_can_be_captain_of_the_brego_guard", [
        (store_proficiency_level, ":onehanded", "trp_player", wpt_one_handed_weapon),
        (store_proficiency_level, ":polearm", "trp_player", wpt_polearm),
        (lt, ":onehanded", ":polearm"),
        ]
    ),
    
    #
    # TLD faction ranks end
    ######################################

 # scripts for gondor tableau shields, by GA
 # Input: tableau, agent, troop
 # Output: none
  ("TLD_gondor_round_shield_banner",
  [ (store_script_param, ":tableau_no",1),(store_script_param, ":agent_no", 2),(store_script_param, ":tr", 3),
    (assign, ":bm", "mesh_banner_e08"), #default tableau black
    (try_begin),(neq,":agent_no",-1),
      (try_begin),(is_between,":tr","trp_blackroot_vale_archer"   ,"trp_dol_amroth_youth"        ),(assign, ":bm", "mesh_banner_e02"),
      (else_try) ,(is_between,":tr","trp_warrior_of_pinnath_gelin","trp_dol_amroth_youth"        ),(assign, ":bm", "mesh_banner_e05"),
      (else_try) ,(is_between,":tr","trp_clansman_of_lamedon"     ,"trp_warrior_of_pinnath_gelin"),(assign, ":bm", "mesh_banner_e09"),
      (else_try) ,(is_between,":tr","trp_pelargir_watchman"       ,"trp_clansman_of_lamedon"     ),(assign, ":bm", "mesh_banner_e12"),
      (else_try) ,(is_between,":tr","trp_dol_amroth_youth"        ,"trp_lothlorien_scout"        ),(assign, ":bm", "mesh_banner_e16"),
      (else_try) ,(is_between,":tr","trp_woodsman_of_lossarnach"  ,"trp_vet_axeman_of_lossarnach"),(assign, ":bm", "mesh_banner_e19"),
      (else_try) ,(is_between,":tr","trp_vet_axeman_of_lossarnach","trp_axemaster_of_lossarnach" ),(assign, ":bm", "mesh_banner_e20"),
      (else_try) ,(is_between,":tr","trp_axemaster_of_lossarnach" ,"trp_pelargir_watchman"       ),(assign, ":bm", "mesh_banner_e21"),
	  (else_try) ,(troop_get_slot,":b",":tr",slot_troop_banner_scene_prop),(neq,":b",0),(assign,":bm",":b"), # for other troops get mesh from banner slot
	  (try_end),
    (try_end),
    (cur_item_set_tableau_material, ":tableau_no",":bm"),
  ]),

  ("TLD_gondor_kite_shield_banner",
  [ (store_script_param, ":tableau_no",1),(store_script_param, ":agent_no", 2),(store_script_param, ":tr", 3),
    (assign, ":bm", "mesh_banner_e08"), #default tableau black
    (try_begin),(neq,":agent_no",-1),
      (try_begin),(is_between,":tr","trp_blackroot_vale_archer"   ,"trp_dol_amroth_youth"     ),(assign, ":bm", "mesh_banner_e04"),
      (else_try) ,(is_between,":tr","trp_warrior_of_pinnath_gelin","trp_blackroot_vale_archer"),(assign, ":bm", "mesh_banner_e07"),
      (else_try) ,(is_between,":tr","trp_clansman_of_lamedon"  ,"trp_warrior_of_pinnath_gelin"),(assign, ":bm", "mesh_banner_e11"),
      (else_try) ,(is_between,":tr","trp_pelargir_watchman"         ,"trp_clansman_of_lamedon"),(assign, ":bm", "mesh_banner_e14"),
      (else_try) ,(is_between,":tr","trp_dol_amroth_youth"    ,"trp_swan_knight_of_dol_amroth"),(assign, ":bm", "mesh_banner_e17"),
      (else_try) ,(is_between,":tr","trp_swan_knight_of_dol_amroth"    ,"trp_lothlorien_scout"),(assign, ":bm", "mesh_banner_e18"),
	  (else_try) ,(troop_get_slot,":b",":tr",slot_troop_banner_scene_prop),(neq,":b",0),(assign,":bm",":b"), # for other troops get mesh from banner slot
	  (try_end),
    (try_end),
    (cur_item_set_tableau_material, ":tableau_no",":bm"),
  ]),
	
  ("TLD_gondor_tower_shield_banner",
  [ (store_script_param, ":tableau_no",1),(store_script_param, ":agent_no", 2),(store_script_param, ":tr", 3),
    (assign, ":bm", "mesh_banner_e08"), #default tableau black
    (try_begin),(neq,":agent_no",-1),
      (try_begin),(is_between,":tr","trp_blackroot_vale_archer"   ,"trp_dol_amroth_youth"        ),(assign, ":bm", "mesh_banner_e03"),
      (else_try) ,(is_between,":tr","trp_warrior_of_pinnath_gelin","trp_blackroot_vale_archer"   ),(assign, ":bm", "mesh_banner_e06"),
      (else_try) ,(is_between,":tr","trp_clansman_of_lamedon"     ,"trp_warrior_of_pinnath_gelin"),(assign, ":bm", "mesh_banner_e10"),
	  (else_try) ,(troop_get_slot,":b",":tr",slot_troop_banner_scene_prop),(neq,":b",0),(assign,":bm",":b"), # for other troops get mesh from banner slot
	  (try_end),
    (try_end),
    (cur_item_set_tableau_material, ":tableau_no",":bm"),
  ]),

  ("TLD_gondor_square_shield_banner",
  [ (store_script_param, ":tableau_no",1),(store_script_param, ":agent_no", 2),(store_script_param, ":tr", 3),
    (assign, ":bm", "mesh_banner_e08"), #default tableau black
    (try_begin),(neq,":agent_no",-1),
      (try_begin),(is_between,":tr","trp_pelargir_watchman","trp_clansman_of_lamedon"),(assign, ":bm", "mesh_banner_e13"),
      (else_try) ,(is_between,":tr","trp_steward_guard"    ,"trp_ranger_of_ithilien" ),(assign, ":bm", "mesh_banner_e15"),
	  (try_end),
    (try_end),
    (cur_item_set_tableau_material, ":tableau_no",":bm"),
  ]),
	
	
]

scripts += ai_scripts
