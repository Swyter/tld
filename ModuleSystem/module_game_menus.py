﻿from header_common import *
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *

from module_constants import *

from module_info import wb_compile_switch as is_a_wb_cutscene

####################################################################################################################
#  (menu-id, menu-flags, menu_text, mesh-name, [<operations>], [<options>]),
#
#   Each game menu is a tuple that contains the following fields:
#  
#  1) Game-menu id (string): used for referencing game-menus in other files.
#     The prefix menu_ is automatically added before each game-menu-id
#
#  2) Game-menu flags (int). See header_game_menus.py for a list of available flags.
#     You can also specify menu text color here, with the menu_text_color macro
#  3) Game-menu text (string).
#  4) mesh-name (string). Not currently used. Must be the string "none"
#  5) Operations block (list). A list of operations. See header_operations.py for reference.
#     The operations block is executed when the game menu is activated.
#  6) List of Menu options (List).
#     Each menu-option record is a tuple containing the following fields:
#   6.1) Menu-option-id (string) used for referencing game-menus in other files.
#        The prefix mno_ is automatically added before each menu-option.
#   6.2) Conditions block (list). This must be a valid operation block. See header_operations.py for reference. 
#        The conditions are executed for each menu option to decide whether the option will be shown to the player or not.
#   6.3) Menu-option text (string).
#   6.4) Consequences block (list). This must be a valid operation block. See header_operations.py for reference. 
#        The consequences are executed for the menu option that has been selected by the player.
#
# Note: The first Menu is the initial character creation menu.
####################################################################################################################

# just stuff to make search for troop cheat (mtarini)
tmp_menu_steps = 5 # how many entries per meny page
tmp_menu_max_fac = 21
tmp_menu_max_tier = 4
tmp_max_troop = 858 # troop_end

magic_items = [itm_lembas] + [itm_pony] +  [itm_warg_reward] + range(itm_ent_water, itm_witchking_helmet)  # first non magic item

city_menu_color = menu_text_color(0xFF010101)  # city menu text color: black

# code snipped to set city meny background
code_to_set_city_background = [
  (party_get_slot,":mesh","$g_encountered_party",slot_town_menu_background),
  (set_background_mesh, ":mesh"),
 ]

# (a common code snippet that is used twice in the add troop cheat menu... ) -- mtarini
code_to_set_search_string = [
  (set_background_mesh, "mesh_ui_default_menu_window"),
  (try_begin), (ge,"$menu_select_any_troop_search_fac", tmp_menu_max_fac+1), 
	(str_store_string, s10, "@any"), 
  (else_try),
	(str_store_faction_name, s10, "$menu_select_any_troop_search_fac"), 
  (try_end),
  (try_begin)
  ]+concatenate_scripts([[
	(eq,"$menu_select_any_troop_search_race",x),
	(str_store_string, s13, race_names[x]),
  (else_try),
  ]for x in range(len(race_names)) ])+[ 
	(str_store_string, s13, "@any"), 
  (try_end),
  (try_begin), (eq,"$menu_select_any_troop_search_tier", tmp_menu_max_tier+1), 
	(str_store_string, s11, "@any"), 
  (else_try),
	(assign, reg11, "$menu_select_any_troop_search_tier"),
	(str_store_string, s11, "@{reg11}0 - {reg11}9"), 
  (try_end),
  
  (try_begin), (eq,"$menu_select_any_troop_search_hero", 0), 
	(str_store_string, s12, "@Regular troops only"), 
  (else_try),  (eq,"$menu_select_any_troop_search_hero", 1), 
	(str_store_string, s12, "@Heroes only"), 
  (else_try),  
	(str_store_string, s12, "@Regulars and Heroes"), 
  (try_end),
  ]
# just stuff to make search for troop cheat (mtarini)
  
game_menus = [
#This needs to be the first window!!!
( "start_game_1",menu_text_color(0xFF000000)|mnf_disable_all_keys,
    "^^^^^^^^^^What do you fight for?", "none", [
	(set_background_mesh, "mesh_relief01"),
	(set_show_messages,0),
	# item faction slots
	(call_script,"script_set_item_faction"),
	(assign, "$disable_skill_modifiers", 0),
    ],
    [("start_good",[],"the DAWN of a new Era"    ,[(jump_to_menu,"mnu_start_good" ),]),
     ("start_evil",[],"the TWILIGHT of Man"      ,[(jump_to_menu,"mnu_start_evil" ),]),
	 ("spacer"    ,[],"_"  ,[]),
	 ("go_bback"  ,[],"Go Back",[(change_screen_quit              ),]), 
	]+concatenate_scripts([[
	 ("quick"     ,[(eq, cheat_switch, 1),],"[dev: quick start Gondor]",[(call_script,"script_start_as_one","trp_gondor_commoner"),(jump_to_menu,"mnu_start_phase_2" ),]), 
	 ("quick2"    ,[(eq, cheat_switch, 1),],"[dev: quick start Mordor]",[(call_script,"script_start_as_one","trp_uruk_snaga_of_mordor"),(jump_to_menu,"mnu_start_phase_2" ),]), 
	] for ct in range(cheat_switch)])+[	
	]
 ),
#This needs to be the second window!!!
( "start_phase_2",mnf_disable_all_keys,
    "^^^^^______________Middle Earth. A shadow is growing in the East, ^______________and dark things come forth that have long been hidden. ^______________The free peoples prepare for war, the like of which has not been seen for an age. ^______________Men, Elves, Dwarves and Orcs; all will play their part. ^^______________What part, however, remains to be seen... ",
    "none",
   [#(set_background_mesh, "mesh_ui_default_menu_window"),
	(try_begin), (eq,"$start_phase_initialized",0),(assign,"$start_phase_initialized",1), # do this only once
		(set_show_messages,0),
		#(call_script,"script_TLD_troop_banner_slot_init"),
		(call_script,"script_reward_system_init"),
		(call_script,"script_init_player_map_icons"),
		#(call_script,"script_get_player_party_morale_values"), (party_set_morale, "p_main_party", reg0),
		(troop_add_gold, "trp_player", 50),#  add a little money
	# relocate party next to own capital
		(faction_get_slot, reg20, "$players_kingdom", slot_faction_capital),
		(try_for_range, ":i", centers_begin, centers_end),
			(party_is_active, ":i"), 
		    (party_slot_eq, ":i", slot_center_destroyed, 0),
			(gt, "$players_subkingdom", 0), # player has a subfaction
			(store_faction_of_party, reg15, ":i"), (eq, reg15, "$players_kingdom"),
			(party_slot_eq, ":i", slot_party_subfaction, "$players_subkingdom"), # i this is the  capital of the subfaction
			(assign, reg20, ":i"), 
			(assign, ":i", centers_end),  # break
		(try_end),
		(call_script, "script_tld_party_relocate_near_party", "p_main_party", reg20, 5), # MV: was 16km - too far
	
		# initialization of "search troop" menu (only once)  mtarini
		(assign, "$menu_select_any_troop_search_race", len(race_names)),  # any race
		(assign, "$menu_select_any_troop_search_tier", tmp_menu_max_tier+1), # any tier
		(assign, "$menu_select_any_troop_search_fac", "$players_kingdom"), # player's kingdom
		(assign, "$menu_select_any_troop_search_hero", 0),	

		(assign, "$cheat_imposed_quest", -1),	

		(call_script, "script_determine_what_player_looks_like"), # for drawings meshes
		#(set_show_messages,1),
	(try_end),
    (call_script, "script_update_troop_notes", "trp_player"), #MV fixes
    (call_script, "script_update_faction_notes", "$players_kingdom"),
	],
    [ ("go_forth",[],"__________Go forth upon you chosen path...",
       [#(troop_add_item, "trp_player","itm_dried_meat",0),#  free food for everyone
        (call_script, "script_get_player_party_morale_values"),
        (party_set_morale, "p_main_party", reg0),
		(assign, "$recover_after_death_menu", "mnu_recover_after_death_default"),
		# TEMP: a spear for everyone
		#(troop_add_item, "trp_player","itm_rohan_lance_standard",0),
		##   (troop_add_item, "trp_player","itm_horn",0),
		(troop_equip_items, "trp_player"),
        (troop_sort_inventory, "trp_player"),
		#(set_show_messages, 1),
        (change_screen_map), #(change_screen_return),
       ]),
	  ("spacer",[],"_",[]),
	]+concatenate_scripts([[
      ("cheat00",[(eq, cheat_switch, 1),(troop_get_upgrade_troop,":t","$player_current_troop_type",0),(gt,":t",0),(str_store_troop_name,s21,":t"),
	    ],"CHEAT: become a {s21}",[
		(troop_get_upgrade_troop,":t","$player_current_troop_type",0),
	    (call_script,"script_start_as_one",":t"),
		(jump_to_menu,"mnu_start_phase_2" ),
	  ]),
      ("cheat01",[(eq, cheat_switch, 1),(troop_get_upgrade_troop,":t","$player_current_troop_type",1),(gt,":t",0),(str_store_troop_name,s21,":t"),
	    ],"CHEAT: become a  {s21}",[
		(troop_get_upgrade_troop,":t","$player_current_troop_type",1),
	    (call_script,"script_start_as_one",":t"),
		(jump_to_menu,"mnu_start_phase_2" ),
	  ]),
      ("cheat03",[(eq, cheat_switch, 1),(str_store_troop_name_plural,s21,"$player_current_troop_type")],"CHEAT: add 10 {s21} to party",
	  [(party_add_members, "p_main_party", "$player_current_troop_type", 10),	  
	  ]),
	] for ct in range(cheat_switch)])+[	
      #("cheat02",[],"CHEAT!",    ]+concatenate_scripts([[     ] for ct in range(cheat_switch)])+[	
      # [
         #(try_for_range, ":cur_place", scenes_begin, scenes_end),
         #  (scene_set_slot, ":cur_place", slot_scene_visited, 1),
         #(try_end),
         #(call_script, "script_get_player_party_morale_values"),
         #(party_set_morale, "p_main_party", reg0),
       #  ]),
    ]
 ),
# This needs to be the third window!!!  
( "start_game_3",mnf_disable_all_keys,
    "^^^^^^^^Choose your scenario:",
    "none",
    [ #Default banners
      (troop_set_slot, "trp_banner_background_color_array", 126, 0xFF212221),
      (troop_set_slot, "trp_banner_background_color_array", 127, 0xFF212221),
      (troop_set_slot, "trp_banner_background_color_array", 128, 0xFF2E3B10),
      (troop_set_slot, "trp_banner_background_color_array", 129, 0xFF425D7B),
      (troop_set_slot, "trp_banner_background_color_array", 130, 0xFF394608),
	  
	  # initialization (mtarini)
      (assign, "$testbattle_team_a_num", 40),(assign, "$testbattle_team_a_troop", "trp_orc_of_isengard"),
      (assign, "$testbattle_team_b_num", 10),(assign, "$testbattle_team_b_troop", "trp_gondor_swordsmen"),
      (assign, "$menu_select_any_troop_search_race", len(race_names)),  # any race
      (assign, "$menu_select_any_troop_search_tier", tmp_menu_max_tier+1), # any tier
      (assign, "$menu_select_any_troop_search_fac", "fac_gondor"), # player's kingdom
      (assign, "$menu_select_any_troop_search_hero", 0),
      
    # (call_script,"script_TLD_troop_banner_slot_init"), 	  #TLD troops banners
      
    #swy-- added unused merlkir illustration here... it looks cool!
      (set_background_mesh, "mesh_draw_war_starts"),
      
      ],
   [("custom_battle_scenario_1" ,[], "Skirmish, Gondor factions vs Harad",
		[(assign, "$g_custom_battle_scenario", 1),(jump_to_menu, "mnu_custom_battle_2"),]),
	]+concatenate_scripts([[
	("custom_battle_scenario_12",[],"Choose factions for battle",
		[(assign, "$g_custom_battle_scenario",16),(jump_to_menu, "mnu_custom_battle_choose_faction1"),]),
	] for ct in range(cheat_switch)])+[	
	("custom_battle_scenario_3" ,[],"Skirmish, Elves vs Black_Numenoreans",
		[(assign, "$g_custom_battle_scenario", 2),(jump_to_menu, "mnu_custom_battle_2"),]),
	("custom_battle_scenario_4" ,[],"Helms Deep Defense, Rohan vs Isengard",
		[(assign, "$g_custom_battle_scenario", 3),(jump_to_menu, "mnu_custom_battle_2"),]),
	("custom_battle_scenario_5" ,[],"Skirmish, North factions vs Rhun",
		[(assign, "$g_custom_battle_scenario", 4),(jump_to_menu, "mnu_custom_battle_2"),]),
	("custom_battle_scenario_6" ,[(eq, cheat_switch, 1),],"Siege Attack, Orcs vs Dwarves",
		[(assign, "$g_custom_battle_scenario", 5),(jump_to_menu, "mnu_custom_battle_2"),]),
	("custom_battle_scenario_7" ,[],"Ambush, Orcs vs Mirkwood",
		[(assign, "$g_custom_battle_scenario", 6),(jump_to_menu, "mnu_custom_battle_2"),]),
#	("custom_battle_scenario_8",[],"           Attack, Gondor vs Corsairs",
#		[(assign, "$g_custom_battle_scenario", 7),(jump_to_menu, "mnu_custom_battle_2"),]),
#	("custom_battle_scenario_9",[],"Football fun        ",
#		[(assign, "$g_custom_battle_scenario", 8),(jump_to_menu, "mnu_custom_battle_2"),]),

# 	(CppCoder) placeholder, should we want to implement this.
#	("custom_battle_choose" ,[],"____________Build your own battle____________.",
#		[(assign, "$g_custom_battle_scenario", 1),(jump_to_menu, "mnu_custom_battle_2"),]),

	]+concatenate_scripts([[
	("custom_battle_scenario_11",[],"Test Battles (Tune Balancing!)",
		[(jump_to_menu, "mnu_quick_battle_general_test"),]),
	("custom_battle_scenario_10",[],"Scenery test battle",
		[(assign, "$g_custom_battle_scenario", 9),(jump_to_menu, "mnu_custom_battle_2"),]),
	("troll_battle_scenario",[],"Test Troll Battles",
		[(jump_to_menu, "mnu_quick_battle_troll"),]),
	("warg_battle_scenario",[],"Test Warg Battles",
		[(jump_to_menu, "mnu_quick_battle_wargs"),]),
	("choose_scene"             ,[],"** Scene Chooser **",
		[                                         (jump_to_menu, "mnu_choose_scenes_0"),]),
	] for ct in range(cheat_switch)])+[
    ("build_your_own_scene"     ,[],"** Build your own scene for TLD **",
		[                                         (jump_to_menu, "mnu_build_your_scene"),]),
    ("go_back"                  ,[],"Go back",[(change_screen_quit)])]
 ),
# This needs to be the fourth window!!!
( "tutorial",mnf_disable_all_keys,
    "^^TLD has a lot of features unknown to native M&B. Those are described in some non-spoilerish detail in PDF included with the release. For tutorial on basic game mechanics please use Native module",
    "none",
    [(set_background_mesh, "mesh_ui_default_menu_window")],
	[("go_back_dot",[],"Go back.",[(change_screen_quit)])]
 ),
# This needs to be the fifth window!!!  
( "reports",0,
   "^^^{s9}", "none",
   [#(set_background_mesh, "mesh_ui_default_menu_window"),
	# Player Reward System (mtarini)
	(call_script, "script_update_respoint"), # so that current money is registered as res point of appropriate faction
	(faction_get_slot, reg10, "$players_kingdom", slot_faction_rank),
	(faction_get_slot, reg11, "$players_kingdom", slot_faction_influence),
	(faction_get_slot, reg12, "$players_kingdom", slot_faction_respoint ),
	(str_store_faction_name, s16, "$players_kingdom"),
    (call_script, "script_get_faction_rank", "$players_kingdom"),
    (assign, reg13, reg0),
	(call_script, "script_get_own_rank_title_to_s24", "$players_kingdom", reg13),
	(str_store_string, s11, "@{s24} ({reg13})"),  # first title (own faction)
	(str_store_string, s13, "@Influence:^ {reg11} (with {s16})"),  # first inf
	(str_store_string, s15, "@Resource Points:^ {reg12} (in {s16})"),  # first rp

	(try_for_range, ":fac", kingdoms_begin, kingdoms_end),
		(neg|eq,"$players_kingdom", ":fac"),
		(faction_get_slot, reg10, ":fac", slot_faction_rank),
		(faction_get_slot, reg11, ":fac", slot_faction_influence),
		(faction_get_slot, reg12, ":fac", slot_faction_respoint ),
		(str_store_faction_name, s16, ":fac"),
		
		(call_script, "script_get_faction_rank", ":fac"),
		(assign, reg13, reg0),
		(call_script, "script_get_allied_rank_title_to_s24", ":fac", reg13),
		(try_begin), 
			(this_or_next|gt, reg10, 0),(eq, "$ambient_faction", ":fac"), (str_store_string, s11, "@{s11}, {s24} ({reg13})"),  # title
		(try_end),
		(try_begin), 
			(this_or_next|gt, reg11, 0),(eq, "$ambient_faction", ":fac"), (str_store_string, s13, "@{s13}, {reg11} (with {s16})"),  # finf
		(try_end),
		(try_begin), 
			(this_or_next|gt, reg12, 0),(eq, "$ambient_faction", ":fac"), (str_store_string, s15, "@{s15}, {reg12} (in {s16})"),  # first rp
		(try_end),
	(try_end),
	(str_store_troop_name, s10, "$g_player_troop"),
#	(troop_get_slot, reg2, "trp_player", slot_troop_renown),
	(str_store_string, s9, "@-={s10}=-^{s11}.^^{s13}.^^{s15}."),
    ],
    [ 
 ]+concatenate_scripts([[		
	  ("cheat_faction_orders"  ,[(eq,"$cheat_mode",1)],"Cheat: Faction orders."   ,[(jump_to_menu, "mnu_faction_orders"   ),]),
 ] for ct in range(cheat_switch)])+[
      ("view_upkeep_costs"     ,[                    ],"View upkeep costs."       ,[(jump_to_menu, "mnu_upkeep_report" ),]),
      ("view_character_report" ,[                    ],"View character report."   ,[(jump_to_menu, "mnu_character_report" ),]),
      ("view_party_size_report",[                    ],"View party size report."  ,[(jump_to_menu, "mnu_party_size_report"),]),
      ("view_morale_report"    ,[                    ],"View party morale report.",[(jump_to_menu, "mnu_morale_report"    ),]),
#NPC companion changes begin
#      ("view_party_preferences",[],"View party management preferences.", [(jump_to_menu, "mnu_party_preferences"),]),
      ("view_character_report_02" ,[(eq,"$cheat_mode",1)],"NPC status check.",
       [(try_for_range, ":npc", companions_begin, companions_end),
            (main_party_has_troop, ":npc"),
            (str_store_troop_name, s4, ":npc"),
            (troop_get_slot, reg3, ":npc", slot_troop_morality_state),
            (troop_get_slot, reg4, ":npc", slot_troop_2ary_morality_state),
            (troop_get_slot, reg5, ":npc", slot_troop_personalityclash_state),    
            (troop_get_slot, reg6, ":npc", slot_troop_personalityclash2_state),    
            (troop_get_slot, reg7, ":npc", slot_troop_personalitymatch_state),    
            (display_message, "@{s4}: M{reg3}, 2M{reg4}, PC{reg5}, 2PC{reg6}, PM{reg7}"),
        (try_end),
        ]),
#NPC companion changes end
      ("view_faction_strengths_report",[],"View faction strengths report.",[(jump_to_menu, "mnu_faction_strengths_report"),]),
      #("view_faction_relations_report",[],"View faction relations report.",[(jump_to_menu, "mnu_faction_relations_report"),]),
      ("view_traits_report",[],"View traits.",[(jump_to_menu, "mnu_traits_report"),]),
      ("resume_travelling"            ,[],"Resume travelling."            ,[(change_screen_return),]),
    ]
 ),
( "custom_battle_2",mnf_disable_all_keys,
    "^^^^^^{s16}",
    "none",
    [(assign, "$g_battle_result", 0),
     (set_show_messages, 0),
     (troop_clear_inventory, "trp_player"),
     (troop_raise_attribute, "trp_player", ca_strength, -1000),
     (troop_raise_attribute, "trp_player", ca_agility, -1000),
     (troop_raise_skill, "trp_player", skl_shield, -1000),
     (troop_raise_skill, "trp_player", skl_athletics, -1000),
     (troop_raise_skill, "trp_player", skl_riding, -1000),
     (troop_raise_skill, "trp_player", skl_power_strike, -1000),
     (troop_raise_skill, "trp_player", skl_power_throw, -1000),
     (troop_raise_skill, "trp_player", skl_weapon_master, -1000),
     (troop_raise_skill, "trp_player", skl_horse_archery, -1000),
     (troop_raise_skill, "trp_player", skl_ironflesh, -1000),
     (troop_raise_proficiency_linear, "trp_player", wpt_one_handed_weapon, -10000),
     (troop_raise_proficiency_linear, "trp_player", wpt_two_handed_weapon, -10000),
     (troop_raise_proficiency_linear, "trp_player", wpt_polearm, -10000),
     (troop_raise_proficiency_linear, "trp_player", wpt_archery, -10000),
     (troop_raise_proficiency_linear, "trp_player", wpt_crossbow, -10000),
     (troop_raise_proficiency_linear, "trp_player", wpt_throwing, -10000),
     (reset_visitors),

############################################   Scene 1 Start "Gondor factions vs Harad"
     (try_begin),
       (eq, "$g_custom_battle_scenario", 1),
       (assign, "$g_custom_battle_scene", "scn_quick_battle_1"),

       (assign, "$g_player_troop", "trp_knight_1_1"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
       (troop_add_item, "$g_player_troop","itm_gondor_bow",0),
       (troop_add_item, "$g_player_troop","itm_khergit_arrows",0),
       (troop_equip_items, "$g_player_troop"),
     
		(set_visitors, 1, "trp_woodsman_of_lossarnach",				5),
		(set_visitors, 2, "trp_axeman_of_lossarnach",		3),
		(set_visitors, 3, "trp_axemaster_of_lossarnach",		2),
		(set_visitors, 4, "trp_clansman_of_lamedon",			5),
		(set_visitors, 5, "trp_footman_of_lamedon",	3),
		(set_visitors, 6, "trp_veteran_of_lamedon",		2),
		(set_visitors, 7, "trp_pinnath_gelin_plainsman",		5),
		(set_visitors, 8, "trp_pinnath_gelin_spearman",3),
		(set_visitors, 9, "trp_warrior_of_pinnath_gelin",		2),
		(set_visitors, 10, "trp_knight_of_dol_amroth",			5),
		(set_visitors, 11, "trp_veteran_knight_of_dol_amroth",	3),
		(set_visitors, 12, "trp_swan_knight_of_dol_amroth",		2),
#       (set_visitors, 13, "trp_dol_amroth_youth",				5),
#       (set_visitors, 14, "trp_squire_of_dol_amroth",			3),
#       (set_visitors, 15, "trp_veteran_squire_of_dol_amroth",	2),
		(set_visitors, 13, "trp_knight_of_dol_amroth",			5),
		(set_visitors, 14, "trp_veteran_knight_of_dol_amroth",	3),
		(set_visitors, 15, "trp_swan_knight_of_dol_amroth",		2),
#		Enemy
		(set_visitors, 16, "trp_harad_desert_warrior",			3),
		(set_visitors, 17, "trp_harad_desert_warrior",			3),
		(set_visitors, 18, "trp_harondor_scout",		3),
		(set_visitors, 19, "trp_harad_infantry",				3),
		(set_visitors, 20, "trp_harad_veteran_infantry",		3),
		(set_visitors, 21, "trp_harad_tiger_guard",	3),
		(set_visitors, 22, "trp_harad_lion_guard",			3),
		(set_visitors, 23, "trp_harondor_rider",					3),
		(set_visitors, 24, "trp_harondor_light_cavalry",			3),
		(set_visitors, 25, "trp_fang_heavy_cavalry",			3),
		(set_visitors, 26, "trp_harad_skirmisher",					3),
		(set_visitors, 27, "trp_harad_archer",			3),
		(set_visitors, 28, "trp_harad_eagle_guard",			3),
		#(set_visitors, 29, "trp_troll_of_moria",				1),
		(str_store_string, s16, "str_custom_battle_1"),

############################################# "Elves kick ass"
     (else_try),
       (eq, "$g_custom_battle_scenario", 2),
       (assign, "$g_custom_battle_scene", "scn_quick_battle_3"),

       (assign, "$g_player_troop", "trp_knight_3_6"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
     
		(set_visitors, 1, "trp_lothlorien_scout",					3),
		(set_visitors, 2, "trp_lothlorien_veteran_scout",			3),
		(set_visitors, 3, "trp_lothlorien_archer",					3),
		(set_visitors, 4, "trp_lothlorien_veteran_archer",			3),
		(set_visitors, 5, "trp_lothlorien_master_archer",			3),
		(set_visitors, 6, "trp_galadhrim_royal_archer",				3),
		(set_visitors, 7, "trp_galadhrim_royal_marksman",			3),
		(set_visitors, 8, "trp_noldorin_mounted_archer",			3),
		(set_visitors, 9, "trp_lothlorien_infantry",				3),
		(set_visitors, 10, "trp_lothlorien_veteran_infantry",		3),
		(set_visitors, 11, "trp_lothlorien_elite_infantry",			3),
		(set_visitors, 12, "trp_galadhrim_royal_swordsman",			3),
		(set_visitors, 13, "trp_lothlorien_warden",					3),
		(set_visitors, 14, "trp_lothlorien_veteran_warden",			3),
		(set_visitors, 15, "trp_galadhrim_royal_warden",			3),
#		ENEMY
		(set_visitors, 16, "trp_black_numenorean_warrior",			3),
		(set_visitors, 17, "trp_black_numenorean_veteran_warrior",	3),
		(set_visitors, 18, "trp_black_numenorean_champion",			3),
		(set_visitors, 19, "trp_black_numenorean_assassin",			3),
		(set_visitors, 20, "trp_black_numenorean_veteran_horseman",	3),
		(set_visitors, 21, "trp_black_numenorean_horsemaster",		3),
		(set_visitors, 22, "trp_black_numenorean_captain",			2),
		(set_visitors, 23, "trp_black_numenorean_lieutenant",		2),
		(set_visitors, 25, "trp_high_captain_of_mordor",			2),
		(set_visitors, 26, "trp_black_snake_horse_archer",		3),
		(set_visitors, 27, "trp_gold_serpent_horse_archer",		3),
		(str_store_string, s16, "str_custom_battle_2"),

     (else_try),
##########################################   SCENE 4 Start "Helms Deep defence"
       (eq, "$g_custom_battle_scenario", 3),
       (assign, "$g_custom_battle_scene", "scn_quick_battle_4"),

       (assign, "$g_player_troop", "trp_knight_1_9"),
       (set_player_troop, "$g_player_troop"),
     
       (troop_raise_attribute, "$g_player_troop", ca_strength, 12),
       (troop_raise_attribute, "$g_player_troop", ca_agility, 9),
       (troop_raise_skill, "$g_player_troop", skl_shield, 3),
       (troop_raise_skill, "$g_player_troop", skl_athletics, 4),
       (troop_raise_skill, "$g_player_troop", skl_riding, 3),
       (troop_raise_skill, "$g_player_troop", skl_power_strike, 4),
       (troop_raise_skill, "$g_player_troop", skl_power_draw, 5),
       (troop_raise_skill, "$g_player_troop", skl_ironflesh, 6),
       (troop_raise_proficiency_linear, "$g_player_troop", wpt_one_handed_weapon, 200),
       (troop_raise_proficiency_linear, "$g_player_troop", wpt_two_handed_weapon, 200),
       (troop_raise_proficiency_linear, "$g_player_troop", wpt_polearm, 200),
       (troop_raise_proficiency_linear, "$g_player_troop", wpt_archery, 210),
       (troop_raise_proficiency_linear, "$g_player_troop", wpt_throwing, 110),
     
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
       (troop_add_item, "$g_player_troop","itm_strong_bow",0),
       (troop_add_item, "$g_player_troop","itm_khergit_arrows",0),
       (troop_equip_items, "$g_player_troop"),
## US     
		(set_visitors, 1, "trp_dismounted_skirmisher_of_rohan",				3),
		(set_visitors, 2, "trp_dismounted_elite_skirmisher_of_rohan",		3),
		(set_visitors, 3, "trp_dismounted_thengel_guard_of_rohan",			3),
		(set_visitors, 4, "trp_heavy_swordsman_of_rohan",					3),
		(set_visitors, 5, "trp_folcwine_guard_of_rohan",					3),
		(set_visitors, 6, "trp_veteran_footman_of_rohan",					3),
		(set_visitors, 7, "trp_warden_of_methuseld",						3),
		(set_visitors, 8, "trp_dismounted_veteran_skirmisher_of_rohan",		3),
		(set_visitors, 9, "trp_rohan_youth",								3),
		(set_visitors, 10, "trp_guardsman_of_rohan",						3),
		(set_visitors, 11, "trp_footman_of_rohan",							3),
		(set_visitors, 12, "trp_elite_footman_of_rohan",					3),
		(set_visitors, 13, "trp_lothlorien_veteran_archer",					5),
		(set_visitors, 14, "trp_dismounted_veteran_skirmisher_of_rohan",	3),
		(set_visitors, 15, "trp_dismounted_veteran_skirmisher_of_rohan",	3),
		(set_visitors, 40, "trp_dismounted_veteran_skirmisher_of_rohan",	1),
		(set_visitors, 41, "trp_dismounted_veteran_skirmisher_of_rohan",	1),
		(set_visitors, 42, "trp_dismounted_veteran_skirmisher_of_rohan",	1),
		(set_visitors, 43, "trp_dismounted_veteran_skirmisher_of_rohan",	1),
		(set_visitors, 44, "trp_dismounted_veteran_skirmisher_of_rohan",	1),
## ENEMY
		(set_visitors, 16, "trp_uruk_hai_tracker",							3),
		(set_visitors, 17, "trp_large_uruk_hai_tracker",					3),
		(set_visitors, 18, "trp_fighting_uruk_hai_tracker",					3),
		(set_visitors, 19, "trp_fighting_uruk_hai_berserker",				8),
		(set_visitors, 20, "trp_uruk_snaga_of_isengard",					10),
		(set_visitors, 21, "trp_uruk_hai_of_isengard",						10),
		(set_visitors, 22, "trp_large_uruk_hai_of_isengard",				10),
		(set_visitors, 23, "trp_fighting_uruk_hai_warrior",					5),
		(set_visitors, 24, "trp_uruk_hai_pikeman",							10),
		(set_visitors, 25, "trp_fighting_uruk_hai_pikeman",					5),
		(set_visitors, 26, "trp_fighting_uruk_hai_champion",				5),
		(set_visitors, 27, "trp_dunnish_wolf_warrior",						15),
		(set_visitors, 28, "trp_dunnish_warrior",							5),
		(set_visitors, 29, "trp_dunnish_wolf_guard",						5),
		(str_store_string, s16, "str_custom_battle_3"),
     
     (else_try),
##########################################   Scene 5 "Northen guys vs Rhun
       (eq, "$g_custom_battle_scenario", 4),
       (assign, "$g_custom_battle_scene", "scn_quick_battle_5"),

       (assign, "$g_player_troop", "trp_knight_4_11"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
     
## US     
       (set_visitors, 1, "trp_woodmen_youth",				20),
#       (set_visitors, 2, "trp_woodsman_scout",				3),
#		(set_visitors, 1, "trp_laketown_scout",				3),
		(set_visitors, 2, "trp_laketown_bowmen",		3),
		(set_visitors, 3, "trp_laketown_archer",					3),
		(set_visitors, 4, "trp_beorning_vale_man",			3),
		(set_visitors, 5, "trp_beorning_warrior",			3),
#       (set_visitors, 3, "trp_dale_noble",					3),
#       (set_visitors, 4, "trp_dale_squire",				3),   
#       (set_visitors, 5, "trp_dale_mounted_moble",			3),
		(set_visitors, 6, "trp_beorning_tolltacker",				3),
		(set_visitors, 7, "trp_beorning_sentinel",				3),
		(set_visitors, 8, "trp_beorning_warden_of_the_ford",			3),
		(set_visitors, 9, "trp_beorning_carrock_lookout",	3),
		(set_visitors, 10, "trp_beorning_carrock_fighter",	3),
		(set_visitors, 11, "trp_dale_militia",				3),
		(set_visitors, 12, "trp_dale_man_at_arms",			3),
		(set_visitors, 13, "trp_dale_warrior",				3),
		(set_visitors, 14, "trp_dale_veteran_warrior",			3),
		(set_visitors, 15, "trp_dale_marchwarden",			3),
#       (set_visitors, 15, "trp_bardian_master_archer",		3),
##     enemy Rhun
		(set_visitors, 16, "trp_rhun_tribesman",			3),
		(set_visitors, 17, "trp_rhun_horse_scout",			3),
		(set_visitors, 18, "trp_rhun_horse_archer",			3),
		(set_visitors, 19, "trp_rhun_veteran_horse_archer",	3),
		(set_visitors, 20, "trp_fell_balchoth_horse_archer",3),
		(set_visitors, 21, "trp_rhun_swift_horseman",		3),
		(set_visitors, 22, "trp_rhun_veteran_swift_horseman",3),
		(set_visitors, 23, "trp_falcon_horseman",           3),
		(set_visitors, 24, "trp_rhun_tribal_warrior",		3),
		(set_visitors, 25, "trp_rhun_tribal_infantry",		3),
		(set_visitors, 26, "trp_rhun_vet_infantry",			3),
		(set_visitors, 27, "trp_infantry_of_the_ox",		3),
		(set_visitors, 28, "trp_rhun_light_horseman",       3),
		(set_visitors, 29, "trp_rhun_light_cavalry",        3),
		(set_visitors, 30, "trp_rhun_noble_cavalry",        3),
		(set_visitors, 31, "trp_dorwinion_noble_of_rhun",	3),
		(str_store_string, s16, "str_custom_battle_4"),
     
     (else_try),
########################################## MORIA GUNDA VS DWARVES  
       (eq, "$g_custom_battle_scenario", 5),
       (assign, "$g_custom_battle_scene", "scn_quick_battle_7"),

       (assign, "$g_player_troop", "trp_knight_2_1"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor,  0, "$g_player_troop"),

		(set_visitors, 1, "trp_snaga_of_moria",					5),
		(set_visitors, 2, "trp_goblin_of_moria",				5),
		(set_visitors, 3, "trp_large_goblin_of_moria",			5),
		(set_visitors, 4, "trp_fell_goblin_of_moria",			5),
		(set_visitors, 5, "trp_archer_snaga_of_moria",			5),
		(set_visitors, 6, "trp_large_goblin_archer_of_moria",	5),
		(set_visitors, 7, "trp_fell_goblin_archer_of_moria",	5),
		(set_visitors, 8, "trp_goblin_gundabad",				5),
		(set_visitors, 9, "trp_orc_gundabad",					5),
## ENEMY
		(set_visitors, 11, "trp_dwarven_apprentice",		3),
		(set_visitors, 12, "trp_dwarven_warrior",			3),
		(set_visitors, 13, "trp_dwarven_hardened_warrior",	3),
		(set_visitors, 14, "trp_dwarven_spearman",			3),
		(set_visitors, 16, "trp_dwarven_pikeman",			3),
		(set_visitors, 17, "trp_dwarven_halberdier",		3),
		(set_visitors, 18, "trp_dwarven_axeman",			3),
		(set_visitors, 40, "trp_dwarven_expert_axeman",		3),
		(set_visitors, 41, "trp_longbeard_axeman",			3),
		(set_visitors, 42, "trp_dwarven_scout",				2),
		(set_visitors, 43, "trp_dwarven_bowman",			2),
		(set_visitors, 44, "trp_dwarven_archer",			2),
		(set_visitors, 45, "trp_marksman_of_ravenhill",		2),
		(str_store_string, s16, "str_custom_battle_5"),
     (else_try),
########################################## ORCS VS MIRKWOOD  
       (eq, "$g_custom_battle_scenario", 6),
       (assign, "$g_custom_battle_scene", "scn_quick_battle_ambush"),

       (assign, "$g_player_troop", "trp_knight_1_15"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),

		(set_visitors, 1, "trp_orc_fighter_gundabad",				4),
		(set_visitors, 2, "trp_fell_orc_warrior_gundabad",		3),
		(set_visitors, 3, "trp_goblin_bowmen_gundabad",			5),
		(set_visitors, 4, "trp_fell_goblin_of_moria",					3),
		(set_visitors, 5, "trp_bolg_clan_rider",						1),
		(set_visitors, 6, "trp_warg_rider_of_moria",					2),
		(set_visitors, 7, "trp_wolf_rider_of_moria",					2),
		(set_visitors, 8, "trp_goblin_gundabad",					5),
		(set_visitors, 9, "trp_orc_gundabad",						6),
		(set_visitors, 10, "trp_keen_eyed_goblin_archer_gundabad",4),
		(set_visitors, 11, "trp_fell_goblin_archer_gundabad",		2),
		(set_visitors, 12, "trp_goblin_rider_gundabad",			2),
		(set_visitors, 13, "trp_warg_rider_gundabad",				2),
		(set_visitors, 14, "trp_goblin_north_clan_rider",				1),
## ENEMY
		(set_visitors, 16, "trp_greenwood_scout",						3),
		(set_visitors, 17, "trp_greenwood_veteran_scout",				3),
		(set_visitors, 18, "trp_greenwood_archer",						3),
		(set_visitors, 19, "trp_greenwood_veteran_archer",				2),
		(set_visitors, 20, "trp_greenwood_master_archer",				2),
		(set_visitors, 21, "trp_thranduils_royal_marksman",				2),
		(set_visitors, 22, "trp_noldorin_mounted_archer",				2),
		(set_visitors, 23, "trp_rivendell_scout",						2),
		(set_visitors, 24, "trp_rivendell_veteran_scout",				2),
		(set_visitors, 25, "trp_rivendell_sentinel",					2),
		(set_visitors, 26, "trp_greenwood_royal_spearman",				2),
		(set_visitors, 27, "trp_greenwood_veteran_spearman",			2),
		(set_visitors, 28, "trp_greenwood_spearman",					2),
		(str_store_string, s16, "str_custom_battle_6"),
     (else_try),
########################################## GONDOR VS CORSAIRS  
       (eq, "$g_custom_battle_scenario", 7),
       (assign, "$g_custom_battle_scene", "scn_quick_battle_corsair"),

       (assign, "$g_player_troop", "trp_knight_1_1"), #Malvogil
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),

		(set_visitors, 1, "trp_gondor_commoner",				4),
		(set_visitors, 2, "trp_gondor_militiamen",				3),
		(set_visitors, 3, "trp_footmen_of_gondor",				3),
		(set_visitors, 4, "trp_gondor_spearmen",				3),
		(set_visitors, 5, "trp_gondor_veteran_spearmen",		1),
		(set_visitors, 6, "trp_guard_of_the_fountain_court",	2),
		(set_visitors, 7, "trp_ranger_of_ithilien",				2),
		(set_visitors, 8, "trp_gondor_swordsmen",				3),
		(set_visitors, 9, "trp_gondor_veteran_swordsmen",		3),
		(set_visitors, 10, "trp_swordsmen_of_the_tower_guard",	2),
		(set_visitors, 11, "trp_archer_of_the_tower_guard",		2),
		(set_visitors, 12, "trp_bowmen_of_gondor",				2),
		(set_visitors, 13, "trp_archer_of_gondor",				2),
		(set_visitors, 14, "trp_veteran_archer_of_gondor",		1),
## ENEMY
		(set_visitors, 16, "trp_olog_hai",				2),
		(set_visitors, 16, "trp_corsair_youth",					3),
		(set_visitors, 17, "trp_corsair_warrior",				3),
		(set_visitors, 18, "trp_corsair_pikeman",				3),
		(set_visitors, 19, "trp_corsair_veteran_raider",		2),
		(set_visitors, 20, "trp_corsair_night_raider",			2),
		(set_visitors, 21, "trp_militia_of_umbar",				2),
		(set_visitors, 22, "trp_marksman_of_umbar",				2),
		(set_visitors, 23, "trp_veteran_marksman_of_umbar",		2),
		(set_visitors, 24, "trp_master_marksman_of_umbar",		2),
		(set_visitors, 25, "trp_corsair_marauder",				2),
		(set_visitors, 26, "trp_corsair_veteran_marauder",		2),
		(set_visitors, 27, "trp_corsair_elite_marauder",		2),
		(set_visitors, 28, "trp_assassin_of_umbar",				2),
		(str_store_string, s16, "str_custom_battle_7"),
 ]+concatenate_scripts([[
	(else_try),
########################################## FOOTBALL  
       # (eq, "$g_custom_battle_scenario", 8),
       # (assign, "$g_custom_battle_scene", "scn_town_1_arena_football"),

	   # (assign, "$g_player_troop", "trp_knight_1_1"), #Malvogil
       # (set_player_troop, "$g_player_troop"),
	   # (modify_visitors_at_site, "$g_custom_battle_scene"),
       # (set_visitor, 0, "$g_player_troop"),

		# (set_visitors, 1, "trp_gondor_commoner", 1),
		# (set_visitors, 2, "trp_gondor_commoner", 1),
		# (set_visitors, 3, "trp_gondor_commoner", 1),
		# (set_visitors, 4, "trp_gondor_commoner", 1),
		# (set_visitors, 5, "trp_gondor_commoner", 1),
		# (set_visitors, 6, "trp_gondor_commoner", 1),
		
		# (set_visitors, 16, "trp_townsman", 1),
		# (set_visitors, 17, "trp_townsman", 1),
		# (set_visitors, 18, "trp_townsman", 1),
		# (set_visitors, 19, "trp_townsman", 1),
		# (set_visitors, 20, "trp_townsman", 1),
		# (set_visitors, 21, "trp_townsman", 1),
		# (str_store_string, s16, "@They came here after we kicked their asses 5:0 in the first round! Let's do it again."),
      # (else_try),

	    # TROLL TEST
       (eq, "$g_custom_battle_scenario", 10),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign, "$g_player_troop", "trp_gondor_veteran_swordsmen"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
	   (set_visitors, 1, "trp_gondor_veteran_spearmen",		8),
	   (set_visitors, 16, "trp_troll_of_moria",				1),
	   (str_store_string, s16, "@TEST: troll VS infantry"),
     (else_try),
	    # TROLL TEST
       (eq, "$g_custom_battle_scenario", 11),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign, "$g_player_troop", "trp_archer_of_the_tower_guard"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
	   (set_visitors, 1, "trp_veteran_archer_of_gondor",		7),
	   (set_visitors, 16, "trp_troll_of_moria",				1),
	   (set_visitors, 17, "trp_orc_snaga_of_isengard",				1),
	   (str_store_string, s16, "@TEST: troll VS archers"),
	(else_try),
	    # TROLL TEST
       (eq, "$g_custom_battle_scenario", 12),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign, "$g_player_troop", "trp_eorl_guard_of_rohan"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
	   (set_visitors, 1, "trp_elite_rider_of_rohan",		6),
	   (set_visitors, 16, "trp_troll_of_moria",				1),
	   (str_store_string, s16, "@TEST: troll VS chavalry"),
    (else_try),
	    # TROLL TEST
       (eq, "$g_custom_battle_scenario", 13),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign, "$g_player_troop", "trp_elite_lancer_of_rohan"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
	   (set_visitors, 1, "trp_lancer_of_rohan",		6),
	   (set_visitors, 16, "trp_troll_of_moria",				1),
	   (str_store_string, s16, "@TEST: troll VS lancers"),
      (else_try),
	    # TROLL TEST
       (eq, "$g_custom_battle_scenario", 14),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign, "$g_player_troop", "trp_fighting_uruk_hai_berserker"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
	   (set_visitors, 1, "trp_orc_of_isengard",	8),
	   (set_visitors, 2, "trp_troll_of_moria",	1),
	   (set_visitors, 16, "trp_olog_hai",	1),
	   (set_visitors, 17, "trp_orc_of_mordor",	8),
 	   (str_store_string, s16, "@TEST: Troll vs Troll"),
    (else_try),
	    # TROLL TEST 3
       (eq, "$g_custom_battle_scenario", 15),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign, "$g_player_troop", "trp_olog_hai"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 16, "$g_player_troop"),
	   #(set_visitors, 1, "trp_gondor_veteran_swordsmen",				8),
	   (set_visitors, 1, "trp_gondor_veteran_spearmen",		8),
	   (set_visitors, 0, "trp_gondor_veteran_swordsmen",				1),
	   (str_store_string, s16, "@TEST: Troll by player"),
	   (str_store_string, s16, "@TROLL TEST"),
    (else_try),
	    # WARG TEST 1vs1
       (eq, "$g_custom_battle_scenario", 20),
       (assign, "$g_custom_battle_scene", "scn_random_scene_plain_forest"),
       (assign, "$g_player_troop", "trp_archer_of_the_tower_guard"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 4, "$g_player_troop"),
	   (set_visitors, 1, "trp_wolf_rider_of_isengard",				1),
	   (set_visitors, 2, "trp_wolf_rider_of_isengard",				1),
	   (set_visitors, 3, "trp_wolf_rider_of_isengard",				1),
	   (str_store_string, s16, "@TEST: warg test 1 VS 1"),
    (else_try),
	    # WARG TEST 2vs3
       (eq, "$g_custom_battle_scenario", 21),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign, "$g_player_troop", "trp_archer_of_the_tower_guard"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
	   (set_visitors, 2, "trp_veteran_archer_of_gondor",		1),
	   (set_visitors, 16, "trp_wolf_rider_of_isengard",		    3),
	   (set_visitors, 17, "trp_orc_snaga_of_isengard",				1),
	   (str_store_string, s16, "@TEST: warg test 2 VS 3"),
    (else_try),
	    # WARG TEST 12vs8
       (eq, "$g_custom_battle_scenario", 22),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign, "$g_player_troop", "trp_archer_of_the_tower_guard"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
	   (set_visitors, 2, "trp_veteran_archer_of_gondor",		9),
	   (set_visitors, 16, "trp_wolf_rider_of_isengard",		    9),
	   (set_visitors, 17, "trp_orc_snaga_of_isengard",				4),
	   (str_store_string, s16, "@TEST: warg test many VS many"),
    (else_try),
	    # WARG TEST 1vs1
       (eq, "$g_custom_battle_scenario", 23),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign, "$g_player_troop", "trp_wolf_rider_of_isengard"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 17, "$g_player_troop"),
	   (set_visitors, 0, "trp_veteran_archer_of_gondor",		1),
	   (str_store_string, s16, "@TEST: play warg, test 1 VS 1"),
    (else_try),
	    # WARG TEST 2vs3
       (eq, "$g_custom_battle_scenario", 24),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign, "$g_player_troop", "trp_white_hand_rider"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
	   (set_visitors, 2, "trp_wolf_rider_of_isengard",		    2),
	   (set_visitors, 16, "trp_veteran_archer_of_gondor",		2),
	   #(set_visitors, 18, "trp_orc_snaga_of_isengard",				1),
	   (str_store_string, s16, "@TEST: play wargs, test 2 VS 3"),
    (else_try),
	    # WARG TEST 12vs8
       (eq, "$g_custom_battle_scenario", 25),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign, "$g_player_troop", "trp_white_hand_rider"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
	   (set_visitors, 2, "trp_wolf_rider_of_isengard",		    12),
	   (set_visitors, 16, "trp_veteran_archer_of_gondor",		10),
	   #(set_visitors, 18, "trp_orc_snaga_of_isengard",				4),
	   (str_store_string, s16, "@TEST: play wargs, many VS many"),
   (else_try),########################################## TEST SCENE FOR DYNAMIC SCENERY  
		(eq, "$g_custom_battle_scenario", 26),
		#(assign, "$g_custom_battle_scene", "scn_quick_battle_3"),
		#(assign, "$g_custom_battle_scene", "scn_random_scene_plain_small"),
		(assign, "$g_custom_battle_scene", "scn_quick_battle_5"),
		#(modify_visitors_at_site, "$g_custom_battle_scene"),
		#(assign, "$g_player_troop", "$testbattle_team_a_troop"),
		#(set_player_troop, "$g_player_troop"),
		
	   (assign, "$g_player_troop", "trp_knight_3_6"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
	   
		#(set_visitor, 0, "$g_player_troop"),

		
		(set_visitors, 5,"$testbattle_team_a_troop","$testbattle_team_a_num"),
		(set_visitors, 16,"$testbattle_team_b_troop","$testbattle_team_b_num"),
		(str_store_string, s16, "@TEST BATTLE: {reg10} {s10} vs {reg11} {s11}"),
   (else_try),########################################## TEST SCENE FOR DYNAMIC SCENERY  
		(eq, "$g_custom_battle_scenario", 9),
		(assign, "$g_custom_battle_scene", "scn_quick_battle_random"),

		(assign, "$g_player_troop", "trp_knight_1_1"), #Malvogil
		(set_player_troop, "$g_player_troop"),
		(modify_visitors_at_site, "$g_custom_battle_scene"),
	    (set_visitor, 0, "$g_player_troop"),
		
		(store_random_in_range,":gfac",0,9),  ## good faction chosen randomly
		(try_begin),
			(eq,":gfac",0),(assign,":trp_good_min","trp_beorning_vale_man"),(assign,":trp_good_max","trp_beorning_warden_of_the_ford" ),(else_try),
			(eq,":gfac",1),(assign,":trp_good_min","trp_dale_militia"     ),(assign,":trp_good_max","trp_girions_guard_of_dale"       ),(else_try),
			(eq,":gfac",2),(assign,":trp_good_min","trp_dwarven_apprentice"),(assign,":trp_good_max","trp_dwarven_halberdier"         ),(else_try),
			(eq,":gfac",3),(assign,":trp_good_min","trp_woodsman_of_lossarnach"),(assign,":trp_good_max","trp_master_blackroot_vale_archer"),(else_try),
			(eq,":gfac",4),(assign,":trp_good_min","trp_dol_amroth_youth" ),(assign,":trp_good_max","trp_swan_knight_of_dol_amroth"   ),(else_try),
			(eq,":gfac",5),(assign,":trp_good_min","trp_lothlorien_scout" ),(assign,":trp_good_max","trp_galadhrim_royal_warden"      ),(else_try),
			(eq,":gfac",6),(assign,":trp_good_min","trp_greenwood_scout"  ),(assign,":trp_good_max","trp_knight_of_rivendell"         ),(else_try),
			(eq,":gfac",7),(assign,":trp_good_min","trp_dunedain_scout"   ),(assign,":trp_good_max","trp_dunedain_master_ranger"      ),(else_try),
			(eq,":gfac",8),(assign,":trp_good_min","trp_rohan_youth"      ),(assign,":trp_good_max","trp_eorl_guard_of_rohan"         ),
		(try_end),

		(store_random_in_range,":bfac",0,9),  ## bad faction chosen randomly
		(try_begin),
			(eq,":bfac",0),(assign,":trp_bad_min","trp_rhun_tribesman"       ),(assign,":trp_bad_max","trp_dorwinion_noble_of_rhun"    ),(else_try),
			(eq,":bfac",1),(assign,":trp_bad_min","trp_harad_desert_warrior" ),(assign,":trp_bad_max","trp_gold_serpent_horse_archer" ),(else_try),
			(eq,":bfac",2),(assign,":trp_bad_min","trp_dunnish_wildman"      ),(assign,":trp_bad_max","trp_dunnish_chieftan"           ),(else_try),
			(eq,":bfac",3),(assign,":trp_bad_min","trp_easterling_youth"     ),(assign,":trp_bad_max","trp_easterling_elite_skirmisher"),(else_try),
			(eq,":bfac",4),(assign,":trp_bad_min","trp_corsair_youth"        ),(assign,":trp_bad_max","trp_pike_master_of_umbar"       ),(else_try),
			(eq,":bfac",5),(assign,":trp_bad_min","trp_orc_snaga_of_isengard"),(assign,":trp_bad_max","trp_fighting_uruk_hai_pikeman"  ),(else_try),
			(eq,":bfac",6),(assign,":trp_bad_min","trp_orc_snaga_of_mordor"  ),(assign,":trp_bad_max","trp_fell_orc_archer_of_mordor"  ),(else_try),
			(eq,":bfac",7),(assign,":trp_bad_min","trp_wolf_rider_of_moria"  ),(assign,":trp_bad_max","trp_fell_goblin_archer_of_moria"),(else_try),
			(eq,":bfac",8),(assign,":trp_bad_min","trp_goblin_gundabad"      ),(assign,":trp_bad_max","trp_goblin_north_clan_rider"    ),
		(try_end),

		(store_random_in_range,":player_good",0,2),
		(try_begin),
			(eq,":player_good",0),
			(assign,":trp0_min",":trp_bad_min" ),(assign,":trp0_max",":trp_bad_max"),
			(assign,":trp1_min",":trp_good_min"),(assign,":trp1_max",":trp_good_max"),
		(else_try),
			(assign,":trp0_min",":trp_good_min"),(assign,":trp0_max",":trp_good_max"),
			(assign,":trp1_min",":trp_bad_min" ),(assign,":trp1_max",":trp_bad_max"),
		(try_end),

		(try_for_range,":i",1,7),
			(store_random_in_range,":trp",":trp0_min",":trp0_max"),
			(store_random_in_range,":n",3,10),
			(set_visitors, ":i", ":trp", ":n"),
		(try_end),
		(try_for_range,":i",16,22),
			(store_random_in_range,":trp",":trp1_min",":trp1_max"),
			(store_random_in_range,":n",3,10),
			(set_visitors, ":i", ":trp", ":n"),
		(try_end),
		
		(str_store_string, s16, "@TEST SCENE"),
		
    (else_try),########################################## CUSTOM FACTIONS  
		(eq, "$g_custom_battle_scenario", 16),
		(assign, "$g_custom_battle_scene", "scn_random_scene_parade"),

		(assign, "$g_player_troop", "trp_knight_1_1"), #Malvogil
		(set_player_troop, "$g_player_troop"),
		(modify_visitors_at_site, "$g_custom_battle_scene"),
	    (set_visitor, 0, "$g_player_troop"),
		
		# determine player and enemy faction
		(try_begin),(gt,"$cbadvantage",0),(assign,":ally_faction","$faction_good"),(assign,":enemy_faction","$faction_evil"),
         (else_try),                      (assign,":ally_faction","$faction_evil"),(assign,":enemy_faction","$faction_good"),(val_mul,"$cbadvantage",-1),
        (try_end),

		#spawn all ally and enemy faction troops 
		(assign,":ally_n",4),
		(assign,":enemy_n",4),
		(assign,":ally_entry",1),
		(assign,":enemy_entry",30),
		(try_for_range,":troop","trp_mercenaries_end","trp_looter"),
		    (neg|troop_is_hero,":troop"),
			(troop_get_type,":troop_faction",":troop"),
			(neq,":troop_faction",tf_troll), #GA: no trolls on battlefield
            (store_troop_faction,":troop_faction",":troop"),
			(try_begin),
			   (eq,":troop_faction",":ally_faction"),
               (lt,":ally_entry",30),
			      (set_visitors, ":ally_entry", ":troop", ":ally_n"),
			      (val_add,":ally_entry",1),
			(else_try),
			   (eq,":troop_faction",":enemy_faction"),
               (lt,":enemy_entry",60),
			      (set_visitors, ":enemy_entry", ":troop", ":enemy_n"),
			      (val_add,":enemy_entry",1),
		    (try_end),
		(try_end),

		(str_store_string, s16, "@FACTION SHOWOFF"),
 ] for ct in range(cheat_switch)])+[
	(try_end),
	(set_show_messages, 1),
	],
    
    [("custom_battle_go",[],"Start.",
       [(try_begin),(eq, "$g_custom_battle_scenario", 5),(set_jump_mission,"mt_custom_battle_5"),
         (else_try),(eq, "$g_custom_battle_scenario", 3),(set_jump_mission,"mt_custom_battle_HD"),#(rest_for_hours,8,1000,0),
#		 (else_try),(eq, "$g_custom_battle_scenario", 8),(set_jump_mission,"mt_custom_battle_football"),
         (else_try),(eq, "$g_custom_battle_scenario", 9),(set_jump_mission,"mt_custom_battle_dynamic_scene"),
         (else_try),(eq, "$g_custom_battle_scenario",16),(set_jump_mission,"mt_custom_battle_parade"),#(rest_for_hours,12,1000,0),
         (else_try),(eq, "$g_custom_battle_scenario",26),(set_jump_mission,"mt_lead_charge"),#(rest_for_hours,12,1000,0),
	 (else_try),(set_jump_mission,"mt_custom_battle"),
        (try_end),
        (jump_to_menu, "mnu_custom_battle_end"),
        (jump_to_scene,"$g_custom_battle_scene"),
		(change_screen_mission),
       ]),
      ("leave_custom_battle_2",[],"Cancel.", [(jump_to_menu, "mnu_start_game_3"), ]),
    ]
 ),
( "custom_battle_end",mnf_disable_all_keys,
    "^^^^^^The battle is over. {s1} Your side killed {reg5} enemies and lost {reg6} troops over the battle.^You personally slew {reg7} opponents in the fighting.",
    "none",
    [(music_set_situation, 0),
     (assign, reg5, "$g_custom_battle_team2_death_count"),
     (assign, reg6, "$g_custom_battle_team1_death_count"),
     (get_player_agent_kill_count, ":kill_count"),
     (get_player_agent_kill_count, ":wound_count", 1),
     (store_add, reg7, ":kill_count", ":wound_count"),
     (try_begin),
       (eq, "$g_battle_result", 1),
       (str_store_string, s1, "str_battle_won"),
     (else_try),
       (str_store_string, s1, "str_battle_lost"),
     (try_end),
	],

	# (CppCoder) Ease not for only testing but for playing as well.
    	[
		("replay",[],"Play this battle again.",[(assign, "$battle_won", 0),(jump_to_menu, "mnu_custom_battle_2")]),
    		("continue_dot",[],"Continue.",[(try_begin),(eq,"$g_custom_battle_scenario",26),(jump_to_menu, "mnu_quick_battle_general_test"),(else_try),(change_screen_quit),(try_end)]),
   	]
 ),

######################################
#TLD Troll quick battle choser
( "quick_battle_general_test",mnf_disable_all_keys,
    "^^^Current battle: ^team A: {reg10} {s10}^^VS^^ team B: {reg11} {s11}",
    "none",
    [ #(set_background_mesh, "mesh_draw_wild_troll"),
	  (assign, reg10, "$testbattle_team_a_num"),
	  (assign, reg11, "$testbattle_team_b_num"),
	  (str_store_troop_name_by_count, s10, "$testbattle_team_a_troop",reg10),
	  (str_store_troop_name_by_count, s11, "$testbattle_team_b_troop",reg11),
	],
   [
 ]+concatenate_scripts([[
	("tAA",[],"        +5 Team A", [(val_add, "$testbattle_team_a_num", 5),(val_clamp, "$testbattle_team_a_num", 1,101),(jump_to_menu, "mnu_quick_battle_general_test"),]),
	("tAB",[],"        -5 Team A", [(val_sub, "$testbattle_team_a_num", 5),(val_clamp, "$testbattle_team_a_num", 1,101),(jump_to_menu, "mnu_quick_battle_general_test"),]),
	("tAC",[],"        Select Troop A", [
	   (store_troop_faction, "$menu_select_any_troop_search_fac", "$testbattle_team_a_troop"),
	   (troop_get_type, "$menu_select_any_troop_search_race", "$testbattle_team_a_troop"),
	   (assign, "$select_any_troop_nextmenu","mnu_quick_battle_general_test_select_a" ), 
	   (assign, "$select_any_troop_add_selected_troops",0 ), 
	   (jump_to_menu, "mnu_select_any_troop"),
	]),
	#("B",[],"_", []),
	("tBA",[],"        +5 Team B", [(val_add, "$testbattle_team_b_num", 5),(val_clamp, "$testbattle_team_b_num", 1,101),(jump_to_menu, "mnu_quick_battle_general_test"),]),
	("tBB",[],"        -5 Team B", [(val_sub, "$testbattle_team_b_num", 5),(val_clamp, "$testbattle_team_b_num", 1,101),(jump_to_menu, "mnu_quick_battle_general_test"),]),
	("tBC",[],"        Select Troop B", [
	   (store_troop_faction, "$menu_select_any_troop_search_fac", "$testbattle_team_b_troop"),
	   (troop_get_type, "$menu_select_any_troop_search_race", "$testbattle_team_b_troop"),
	   (assign, "$select_any_troop_nextmenu","mnu_quick_battle_general_test_select_b" ), 
	   (assign, "$select_any_troop_add_selected_troops",0 ), 
	   (jump_to_menu, "mnu_select_any_troop"),
	]),
	#("B",[],"_", []),
	("B",[],"         Preset 1", [
	          (assign, "$testbattle_team_b_num", 40),(assign, "$testbattle_team_b_troop", "trp_orc_of_isengard"),
	          (assign, "$testbattle_team_a_num", 10),(assign, "$testbattle_team_a_troop", "trp_gondor_swordsmen")
	]),
	#("B",[],"_", []),
	("F",[],"          START FIGHT!",
		[(assign, "$g_custom_battle_scenario", 26),(jump_to_menu, "mnu_custom_battle_2"),]),
 ] for ct in range(cheat_switch)])+[
    ("dot_go_back",[],".                 Go back",[(jump_to_menu, "mnu_start_game_3"),]),    ]
 ),
( "quick_battle_general_test_select_a",0,"_","none",[
  (try_begin),(ge, "$select_any_troop_result", 0), (assign, "$testbattle_team_a_troop", "$select_any_troop_result"),(try_end),
  (jump_to_menu, "mnu_quick_battle_general_test"),],[],
 ),
( "quick_battle_general_test_select_b",0,"_","none",[
  (try_begin),(ge, "$select_any_troop_result", 0), (assign, "$testbattle_team_b_troop", "$select_any_troop_result"),(try_end),
  (jump_to_menu, "mnu_quick_battle_general_test"),],[],
 ),


#TLD Troll quick battle choser
( "quick_battle_troll",mnf_disable_all_keys,
    "^^^^^^^^Choose your troll scenario:",
    "none",
    [(set_background_mesh, "mesh_draw_wild_troll"),],
   [
 ]+concatenate_scripts([[ 
	("troll_battle_scenario_10",[],"          Test: Troll VS Infantry",
		[(assign, "$g_custom_battle_scenario", 10),(jump_to_menu, "mnu_custom_battle_2"),]),
	("troll_battle_scenario_11",[],"          Test: Troll VS Archers",
		[(assign, "$g_custom_battle_scenario", 11),(jump_to_menu, "mnu_custom_battle_2"),]),
	("troll_battle_scenario_12",[],"          Test: Troll VS Cavalry",
		[(assign, "$g_custom_battle_scenario", 12),(jump_to_menu, "mnu_custom_battle_2"),]),
	("troll_battle_scenario_13",[],"          Test: Troll VS Lancers",
		[(assign, "$g_custom_battle_scenario", 13),(jump_to_menu, "mnu_custom_battle_2"),]),
	("troll_battle_scenario_14",[],"          Test: Troll VS Troll",
		[(assign, "$g_custom_battle_scenario", 14),(jump_to_menu, "mnu_custom_battle_2"),]),
	("troll_battle_scenario_15",[],"          Toy-Test: player controlled Troll",
		[(assign, "$g_custom_battle_scenario", 15),(jump_to_menu, "mnu_custom_battle_2"),]),
 ] for ct in range(cheat_switch)])+[
    ("dot_go_back",[],".                 Go back",[(jump_to_menu, "mnu_start_game_3"),]),    ]
 ),
( "quick_battle_wargs",mnf_disable_all_keys,
    "^^^^^^^^Choose your TEST Warg scenario:",
    "none",
    [(set_background_mesh, "mesh_draw_orc_raiders"),],
   [
 ]+concatenate_scripts([[
	("warg_battle_scenario_10",[],"          Against Wargs: 1 vs 1",
		[(assign, "$g_custom_battle_scenario", 20),(jump_to_menu, "mnu_custom_battle_2"),]),
	("warg_battle_scenario_11",[],"          Against Wargs: 2 vs 3",
		[(assign, "$g_custom_battle_scenario", 21),(jump_to_menu, "mnu_custom_battle_2"),]),
	("warg_battle_scenario_12",[],"          Against Wargs: many vs many",
		[(assign, "$g_custom_battle_scenario", 22),(jump_to_menu, "mnu_custom_battle_2"),]),
	("warg_battle_scenario_10b",[],"          Play Wargs: 1 vs 1",
		[(assign, "$g_custom_battle_scenario", 23),(jump_to_menu, "mnu_custom_battle_2"),]),
	("warg_battle_scenario_11b",[],"          Play Wargs: 2 vs 3",
		[(assign, "$g_custom_battle_scenario", 24),(jump_to_menu, "mnu_custom_battle_2"),]),
	("warg_battle_scenario_12b",[],"          Play Wargs: many vs many",
		[(assign, "$g_custom_battle_scenario", 25),(jump_to_menu, "mnu_custom_battle_2"),]),
 ] for ct in range(cheat_switch)])+[
    ("dot_go_back",[],".                 Go back",[(jump_to_menu, "mnu_start_game_3"),]),    ]
 ),
######################################
#TLD Character creation menus CONTINUE
( "start_good",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^Select your race:", "none",[(set_show_messages,0),],[
  ("start_ma",[],"MAN",                 [(jump_to_menu,"mnu_start_good_man"),]),
  ("start_el",[],"ELF",                 [(jump_to_menu,"mnu_start_good_elf"),]),
  ("start_dw",[],"DWARF",               [(jump_to_menu,"mnu_start_good_dwarf"),]),
  ("spacer"  ,[],"_",[]),  
  ("go_back" ,[],"Go back",[(jump_to_menu, "mnu_start_game_1")]),    ]
 ),
( "start_evil",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^Whom do you Serve?", "none",[],
 [("start_eye"   ,[],"SAURON of Mordor, the Lord of the Rings",   [(jump_to_menu,"mnu_start_eye"),]),
  ("start_hand"  ,[],"SARUMAN of Isengard, the White Hand",       [(jump_to_menu,"mnu_start_hand"),]),
  ("spacer",[],"_",[]),
  ("go_back"     ,[],"Go back",[(jump_to_menu, "mnu_start_game_1")]),    ]
 ),
( "start_eye",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^Your Master is the Lidless Eye^Choose your Race", "none",[],[
 ("start_or"  ,[],"an ORC, serving the Lidless Eye"       ,[(jump_to_menu,"mnu_start_eye_orc"),]),
 ("start_ur"  ,[],"an URUK, the new breed of Orcs"        ,[(call_script,"script_start_as_one","trp_uruk_snaga_of_mordor"),  (jump_to_menu,"mnu_choose_skill"),]),
 ("start_em"  ,[],"a MAN, subjugated by Sauron"           ,[(jump_to_menu,"mnu_start_eye_man"),]),
 ("spacer",[],"_",[]),
 ("go_back"     ,[],"Go back",[(jump_to_menu, "mnu_start_evil")]),    ]
 ),
( "start_hand",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^Your Master is the White Hand^Choose your Race", "none",[],[
 ("start_whor",[],"an ORC, serving the White Hand",          [(jump_to_menu,"mnu_start_hand_orc"),]),
 ("start_isur",[],"an URUK-HAI, bred in Isengard",           [(call_script,"script_start_as_one","trp_uruk_snaga_of_isengard"),(jump_to_menu,"mnu_choose_skill"),]),
 ("start_duma",[],"a MAN of Dunland, the Western Plains",    [(call_script,"script_start_as_one","trp_dunnish_wildman"),       (jump_to_menu,"mnu_choose_gender"),]), #(jump_to_menu,"mnu_choose_skill"),]),
 ("spacer",[],"_",[]),
 ("go_back"     ,[],"Go back",[(jump_to_menu, "mnu_start_evil")]),    ]
 ),
( "start_good_man",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^Select your people:", "none",[(assign, "$last_menu", "mnu_start_good_man")],[
  ("start_go",[],"GONDOR, the Kingdom of the White Tower",[(jump_to_menu,"mnu_start_gondor"),]),
  ("start_ro",[],"ROHAN, the Horse people"               ,[(call_script,"script_start_as_one","trp_rohan_youth"),           (jump_to_menu,"mnu_choose_gender"),]),
  ("start_du",[],"DUNEDAIN, the ancient dynasty of Men"  ,[(call_script,"script_start_as_one","trp_dunedain_scout"),        (jump_to_menu,"mnu_choose_gender"),]),
  ("start_be",[],"BEORNINGS, the Bear people"            ,[(call_script,"script_start_as_one","trp_beorning_vale_man"),     (jump_to_menu,"mnu_choose_gender"),]),
  ("start_da",[],"the northern Kingdom of DALE"          ,[(call_script,"script_start_as_one","trp_dale_militia"),         (jump_to_menu,"mnu_choose_gender"),]),
  ("spacer"  ,[],"_",[]),  
  ("go_back" ,[],"Go back",[(jump_to_menu, "mnu_start_good")]),    ]
 ),
( "start_good_elf",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^which Forest do you live in, Elder?", "none",[(assign, "$last_menu", "mnu_start_good_elf")],[
  ("start_ri", [],"RIVENDELL, of Lord Elrond"            ,[(call_script,"script_start_as_one","trp_rivendell_scout"),      (jump_to_menu,"mnu_choose_gender"),]),
  ("start_lo", [],"LOTHLORIEN, of Lady Galadriel"        ,[(call_script,"script_start_as_one","trp_lothlorien_scout"),     (jump_to_menu,"mnu_choose_gender"),]),
  ("start_mi", [],"MIRKWOOD, land of the Silvan Elves"   ,[(call_script,"script_start_as_one","trp_greenwood_scout"),      (jump_to_menu,"mnu_choose_gender"),]),
  ("spacer" , [],"_",[]),  
  ("go_back", [],"Go back",[(jump_to_menu, "mnu_start_good")]),    ]
 ),
( "start_good_dwarf",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^Select your Lineage:", "none",[(assign, "$last_menu", "mnu_start_good_elf")],[
  ("start_er", [],"a dweller of EREBOR"                  ,[(call_script,"script_start_as_one","trp_dwarven_apprentice"),   (jump_to_menu,"mnu_choose_skill"),]),
  ("start_ih", [],"a miner of the IRON HILLS"            ,[(call_script,"script_start_as_one","trp_iron_hills_miner"),     (jump_to_menu,"mnu_choose_skill"),]),
  ("spacer" , [],"_",[]),  
  ("go_back", [],"Go back",[(jump_to_menu, "mnu_start_good")]),    ]
 ),
( "start_gondor",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^Where are you from, in Gondor?", "none",[(assign, "$last_menu", "mnu_start_gondor")],[
 ("start_mt",[],"MINAS TIRITH, the Capital"                    ,[(jump_to_menu,"mnu_start_gondor_mt"),]),
 ("start_ls",[],"LOSSARNACH, the Fiefdom of the Axemen"        ,[(call_script,"script_start_as_one","trp_woodsman_of_lossarnach"),(jump_to_menu,"mnu_choose_gender"),]),
 ("start_la",[],"LAMEDON, the Fiefdom of the Mountain Clansmen",[(call_script,"script_start_as_one","trp_clansman_of_lamedon"),   (jump_to_menu,"mnu_choose_gender"),]),
 ("start_pg",[],"PINNATH GELIN, the Fiefdom of Green Hills"    ,[(call_script,"script_start_as_one","trp_pinnath_gelin_plainsman"), (jump_to_menu,"mnu_choose_gender"),]),
 ("start_do",[],"DOL AMROTH, the Fiefdom of Swan Knights"      ,[(call_script,"script_start_as_one","trp_dol_amroth_youth"),      (jump_to_menu,"mnu_choose_gender"),]),
 ("start_pe",[],"PELARGIR, the Coastal Fiefdom"                ,[(call_script,"script_start_as_one","trp_pelargir_watchman"), (jump_to_menu,"mnu_choose_gender"),]),
 ("start_bl",[],"BLACKROOT VALE, the Fiefdom of Archers"       ,[(call_script,"script_start_as_one","trp_blackroot_vale_archer"), (jump_to_menu,"mnu_choose_gender"),]),
 ("spacer",[],"_",[]),
 ("go_back"     ,[],"Go back",[(jump_to_menu, "mnu_start_good")]),    ]
 ),
( "start_eye_man",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^Select your people:", "none",[(assign, "$last_menu", "mnu_start_eye_man")],[
 ("start_hr",[],"HARADRIM, the desert people from the South",    [(jump_to_menu,"mnu_start_haradrim"),]),  
 ("start_bn",[],"Black NUMENOREANS, the renegades from the West",[(call_script,"script_start_as_one","trp_black_numenorean_renegade"),(jump_to_menu,"mnu_choose_gender"),]),
 ("start_um",[],"UMBAR, the pirates from the South Seas",        [(call_script,"script_start_as_one","trp_corsair_youth"),            (jump_to_menu,"mnu_choose_gender"),]),
 ("start_rh",[],"RHUN, the barbarians from the East",            [(call_script,"script_start_as_one","trp_rhun_tribesman"),           (jump_to_menu,"mnu_choose_gender"),]),
 ("start_kh",[],"KHAND, the savage people from South-East",      [(call_script,"script_start_as_one","trp_easterling_youth"),         (jump_to_menu,"mnu_choose_gender"),]),
 ("spacer",[],"_",[]),
 ("go_back",[],"Go back",[(jump_to_menu, "mnu_start_eye")]),    ]
 ),
( "start_eye_orc",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^Where do you lurk?", "none",[],[
 ("start_arm",[],"in the armies amassed at MORDOR", [(call_script,"script_start_as_one","trp_orc_snaga_of_mordor"),   (jump_to_menu,"mnu_choose_skill"),]),
 ("start_cav",[],"in the caves of DOL GULDUR",      [(call_script,"script_start_as_one","trp_orc_snaga_of_guldur"),   (jump_to_menu,"mnu_choose_skill"),]),
 ("spacer" ,[],"_"  ,[]),
 ("go_back",[],"Go back",[(jump_to_menu, "mnu_start_eye")]),    ]
 ),
( "start_hand_orc",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^Where do you lurk?", "none",[],[
 ("start_armis",[],"in the Armies amassed at ISENGARD",[(call_script,"script_start_as_one","trp_orc_snaga_of_isengard"),(jump_to_menu,"mnu_choose_skill"),]),
 ("start_minmo",[],"in the Mines of MORIA"            ,[(call_script,"script_start_as_one","trp_snaga_of_moria"),       (jump_to_menu,"mnu_choose_skill"),]),
 ("start_cliff",[],"in the cliffs of Mount GUNDABAD",  [(call_script,"script_start_as_one","trp_goblin_gundabad"),      (jump_to_menu,"mnu_choose_skill"),]),
 ("spacer" ,[],"_",[]),
 ("go_back",[],"Go back",[(jump_to_menu, "mnu_start_hand")]),    ]
 ),
( "start_gondor_mt",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^Select your Lineage", "none",[(assign, "$last_menu", "mnu_start_gondor_mt")],[
 ("start_1_com",[],"Commoner" ,[(call_script,"script_start_as_one","trp_gondor_commoner"),(jump_to_menu,"mnu_choose_gender"),]),
 ("start_2_hib",[],"High-born",[(call_script,"script_start_as_one","trp_gondor_noblemen"),(jump_to_menu,"mnu_choose_gender"),]),
 ("spacer" ,[],"_"        ,[]),
 ("go_back",[],"Go back"  ,[(jump_to_menu, "mnu_start_gondor")]),    ]
 ),
( "start_haradrim",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^You are an Haradrim,^a Man of the Desert.^Select your line", "none",[(assign, "$last_menu", "mnu_start_haradrim")],[
 ("start_1_des",[],"Desert Man",                          [(call_script,"script_start_as_one","trp_harad_desert_warrior"),   (jump_to_menu,"mnu_choose_gender"),]),
 ("start_2_far",[],"Far Harad Tribesman",                 [(call_script,"script_start_as_one","trp_far_harad_tribesman"),    (jump_to_menu,"mnu_choose_gender"),]),
# ("start_3",[],"Harondor Noble",                      [(call_script,"script_start_as_one","trp_harondor_scout"),(jump_to_menu,"mnu_choose_gender"),]),
 ("spacer",[],"_",[]),
 ("go_back",[],"Go back",[(jump_to_menu, "mnu_start_eye_man")]),    ]
 ),
( "choose_gender",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^Your gender?", "none",[],
 [("start_male"  ,[],"Male"   ,[#(assign,"$character_gender",tf_male  ),
    (jump_to_menu,"mnu_choose_skill"),]),
  ("start_female",[],"Female" ,[
    (troop_set_type,"trp_player",tf_female), # override race for females elves and mans
    #(assign,"$character_gender",tf_female), no need
    (jump_to_menu,"mnu_choose_skill"),
  ]),
  ("spacer",[],"_",[]),

  ("go_back"     ,[],"Go back",[(troop_clear_inventory, "trp_player"),(jump_to_menu,"$last_menu")]),    ]
 ),
( "choose_skill",mnf_disable_all_keys|menu_text_color(0xFF0000FF),
 "^^^^^^^^FOR DEVS:^*normally*, at this point^you would go to edit skills^and then face...","none",[
	 (jump_to_menu, "mnu_auto_return"), # comment this line to let devs skip skill/face editing
	],
	[ ("skip",[],"SKIP THAT: let me playtest now",[(jump_to_menu, "mnu_start_phase_2"),]),
	  ("proc",[],"Proceed as normal",[(jump_to_menu, "mnu_auto_return"),])]
 ),
############################################### 
( "auto_return",0,
    "This menu automatically returns to caller.",
    "none",
    [(change_screen_return, 0)],[]
 ),

( "morale_report",0,
   "^^{s1}",
   "none",
   [#(set_background_mesh, "mesh_ui_default_menu_window"),
    (call_script, "script_get_player_party_morale_values"),
    (assign, ":target_morale", reg0),
    (assign, reg1, "$g_player_party_morale_modifier_party_size"),
    (try_begin),(gt, reg1, 0),(str_store_string, s2, "@ -"),
     (else_try),              (str_store_string, s2, "@ "),
    (try_end),

    (assign, reg2, "$g_player_party_morale_modifier_leadership"),
    (try_begin),(gt, reg2, 0),(str_store_string, s3, "@ +"),
     (else_try),              (str_store_string, s3, "@ "),
    (try_end),

    (try_begin),
      (gt, "$g_player_party_morale_modifier_no_food", 0),
      (assign, reg7, "$g_player_party_morale_modifier_no_food"),
      (str_store_string, s5, "@^No food:  -{reg7}"),
    (else_try),
      (str_store_string, s5, "@ "),
    (try_end),
    (assign, reg3, "$g_player_party_morale_modifier_food"),
    (try_begin),(gt, reg3, 0),(str_store_string, s4, "@ +"),
     (else_try),              (str_store_string, s4, "@ "),
    (try_end),
    
    # TLD morale-boosting items (non-cumulative)
    (assign, reg6, 0),
    (str_store_string, s6, "@ "),
    (try_begin),
	  (call_script, "script_get_troop_item_amount", "trp_player", "itm_lembas"),
	  (gt, reg0, 0),
      (assign, reg6, 30),
      (str_store_string, s6, "@ +"),
    (else_try),
	  (call_script, "script_get_troop_item_amount", "trp_player", "itm_cooking_cauldron"),
	  (gt, reg0, 0),
      (assign, reg6, 20),
      (str_store_string, s6, "@ +"),      
    (try_end),

    (party_get_morale, reg5, "p_main_party"),
    (store_sub, reg4, reg5, ":target_morale"),
    (try_begin),(gt, reg4, 0),(str_store_string, s7, "@ +"),
     (else_try),              (str_store_string, s7, "@ "),
    (try_end),
    (str_store_string, s1, "@Current party morale is {reg5}.^Current party morale modifiers are:^^Base morale:  +50^Party size: {s2}{reg1}^Leadership: {s3}{reg2}^Food variety: {s4}{reg3}{s5}^Special items: {s6}{reg6}^Recent events: {s7}{reg4}^TOTAL:  {reg5}"),
    ],
    [("continue",[],"Continue...",[(jump_to_menu, "mnu_reports")])]
 ),
( "faction_orders",0,
   "{s9}", "none",
   [ 
     (set_background_mesh, "mesh_ui_default_menu_window"),
     (str_clear, s9),
     (store_current_hours, ":cur_hours"),
     (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
       (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
       (neq, ":faction_no", "fac_player_supporters_faction"),
       (faction_get_slot, ":faction_ai_state", ":faction_no", slot_faction_ai_state),
       (faction_get_slot, ":faction_ai_object", ":faction_no", slot_faction_ai_object),
       (faction_get_slot, ":faction_marshall", ":faction_no", slot_faction_marshall),
       (faction_get_slot, ":faction_ai_last_offensive_time", ":faction_no", slot_faction_ai_last_offensive_time),
       (faction_get_slot, ":faction_ai_offensive_max_followers", ":faction_no", slot_faction_ai_offensive_max_followers),
       (str_store_faction_name, s10, ":faction_no"),
       (store_sub, reg1, ":cur_hours", ":faction_ai_last_offensive_time"),
       (assign, reg2, ":faction_ai_offensive_max_followers"),
       (try_begin),
         (eq, ":faction_ai_state", sfai_default),
         (str_store_string, s11, "@Defending"),
       (else_try),
         (eq, ":faction_ai_state", sfai_gathering_army),
         (str_store_string, s11, "@Gathering army"),
       (else_try),
         (eq, ":faction_ai_state", sfai_attacking_center),
         (str_store_party_name, s11, ":faction_ai_object"),
         (str_store_string, s11, "@Besieging {s11}"),
       (else_try),
         (eq, ":faction_ai_state", sfai_raiding_village),
         (str_store_party_name, s11, ":faction_ai_object"),
         (str_store_string, s11, "@Raiding {s11}"),
       (else_try),
         (eq, ":faction_ai_state", sfai_attacking_enemy_army),
         (str_store_party_name, s11, ":faction_ai_object"),
         (str_store_string, s11, "@Attacking enemies around {s11}"),
       (try_end),
       (str_store_faction_name, s10, ":faction_no"),
       (try_begin),
         (lt, ":faction_marshall", 0),
         (str_store_string, s12, "@No one"),
       (else_try),
         (str_store_troop_name, s12, ":faction_marshall"),
       (try_end),
       (str_store_string, s9, "@{s9}{s10}^Current state: {s11}^Marshall: {s12}^Since the last offensive: {reg1} hours^Offensive maximum followers: {reg2}^^"),
     (try_end),
     (try_begin),
       (neg|is_between, "$g_cheat_selected_faction", kingdoms_begin, kingdoms_end),
       (call_script, "script_get_next_active_kingdom", kingdoms_end),
       (assign, "$g_cheat_selected_faction", reg0),
     (try_end),
     (str_store_faction_name, s10, "$g_cheat_selected_faction"),
     (str_store_string, s9, "@Selected faction is: {s10}^^{s9}"),
    ],
    [ 
 ]+concatenate_scripts([[	
	("faction_orders_next_faction", [],"Select next faction.",
       [ (call_script, "script_get_next_active_kingdom", "$g_cheat_selected_faction"),
         (assign, "$g_cheat_selected_faction", reg0),
         (jump_to_menu, "mnu_faction_orders"),
        ]),
      ("faction_orders_defend", [],"Force defend.",
       [ (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_state, sfai_default),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_object, -1),
         (jump_to_menu, "mnu_faction_orders"),
        ]),
      ("faction_orders_gather", [],"Force gather army.",
       [ (store_current_hours, ":cur_hours"),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_state, sfai_gathering_army),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_last_offensive_time, ":cur_hours"),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_offensive_max_followers, 1),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_object, -1),
         (jump_to_menu, "mnu_faction_orders"),
        ]),
      ("faction_orders_increase_time", [],"Increase last offensive time by 24 hours.",
       [ (faction_get_slot, ":faction_ai_last_offensive_time", "$g_cheat_selected_faction", slot_faction_ai_last_offensive_time),
         (val_sub, ":faction_ai_last_offensive_time", 24),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_last_offensive_time, ":faction_ai_last_offensive_time"),
         (jump_to_menu, "mnu_faction_orders"),
        ]),
      ("faction_orders_rethink", [],"Force rethink.",
       [ (call_script, "script_init_ai_calculation"),
         (call_script, "script_decide_faction_ai", "$g_cheat_selected_faction"),
         (jump_to_menu, "mnu_faction_orders"),
        ]),
      ("faction_orders_rethink_all", [],"Force rethink for all factions.",
       [ (call_script, "script_recalculate_ais"),
         (jump_to_menu, "mnu_faction_orders"),
        ]),
 ] for ct in range(cheat_switch)])+[
      ("go_back_dot",[],"Go back.",[(jump_to_menu, "mnu_reports"),]),
    ]
 ),
( "character_report",0,
   "^^^^^Party Morale: {reg8}^Party Size Limit: {reg7}^{s5}",
#   "^^^^^Character Renown: {reg5}^Honor Rating: {reg6}^Party Morale: {reg8}^Party Size Limit: {reg7}^{s5}",
   "none",
   [#(set_background_mesh, "mesh_ui_default_menu_window"),

    (call_script, "script_game_get_party_companion_limit"),
    (assign, ":party_size_limit", reg0),
    #(troop_get_slot, ":renown", "trp_player", slot_troop_renown),
    #(assign, reg5, ":renown"),
    #(assign, reg6, "$player_honor"),
    (assign, reg7, ":party_size_limit"),
    (party_get_morale, reg8, "p_main_party"),
	# CppCoder: Injury Report. Feel free to edit/remove/improve. :)
	(eq, 0, 0), # on / off toggle
	(assign, ":str_reg", s1), 
	(assign, ":wounds", 0), #count # of wounds
	(assign, ":wound_mask", 0), #count # of wounds
	(troop_get_slot, ":wound_mask", "trp_player", slot_troop_wound_mask),
	(try_begin),(store_and,":x",":wound_mask",wound_head ),(neq,":x",0),(val_add,":wounds",1),(str_store_string, ":str_reg", "str_wound_head"),(val_add, ":str_reg", 1),(try_end),
	(try_begin),(store_and,":x",":wound_mask",wound_chest),(neq,":x",0),(val_add,":wounds",1),(str_store_string, ":str_reg", "str_wound_chest"),(val_add, ":str_reg", 1),(try_end),
	(try_begin),(store_and,":x",":wound_mask",wound_arm  ),(neq,":x",0),(val_add,":wounds",1),(str_store_string, ":str_reg", "str_wound_arm"),(val_add, ":str_reg", 1),(try_end),
	(try_begin),(store_and,":x",":wound_mask",wound_leg  ),(neq,":x",0),(val_add,":wounds",1),(str_store_string, ":str_reg", "str_wound_leg"),(val_add, ":str_reg", 1),(try_end),
	(str_store_string, s5, "@You are in perfect health."),
        (try_begin),
		(eq, ":wounds", 1),
		(str_store_string, s5, "@You are suffering from {s1}."),
	(else_try),
		(eq, ":wounds", 2),
		(str_store_string, s5, "@You are suffering from {s1} and {s2}."),
	(else_try),
		(eq, ":wounds", 3),
		(str_store_string, s5, "@You are suffering from {s1}, {s2}, and {s3}."),
	(else_try),
		(eq, ":wounds", 4),
		(str_store_string, s5, "@You are suffering from {s1}, {s2}, {s3} and {s4}."),
	(else_try),
		(str_store_string, s5, "@You are in perfect health."),
	(try_end),
   ],
   [("continue",[],"Continue...",[(jump_to_menu, "mnu_reports"),]),]
 ),
( "upkeep_report", 0,
 "{s12}", "none",[ #(set_background_mesh, "mesh_ui_default_menu_window"),
    (assign, reg5, 0),
    (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
      (neq, ":faction_no", "fac_player_supporters_faction"),
  	  (call_script, "script_compute_wage_per_faction", ":faction_no"),
	  (val_add, reg5, reg4),
    (try_end),
    
    (try_begin),
      (gt,reg5,0),
      (str_store_string, s12, "@Weekly upkeep for troops:^{reg5} Resource Points^"),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (call_script, "script_compute_wage_per_faction", ":faction_no"),
        (gt, reg4, 0),
        (str_store_faction_name, s4, ":faction_no"),
        (faction_get_slot, reg5, ":faction_no", slot_faction_respoint),
        (str_store_string, s12, "@{s12}^  {s4}: {reg4} Resource points ({reg5})"),
      (try_end),
	(else_try),
	  (str_store_string, s12, "@No upkeep costs"),
    (try_end),
   ],
   [("continue",[],"Continue...",[(jump_to_menu, "mnu_reports")])]
 ),
( "party_size_report",0,
   "^^^^{s1}", "none",
   [(call_script, "script_game_get_party_companion_limit"),
    (assign, ":party_size_limit", reg0),

    (store_skill_level, ":leadership", "skl_leadership", "trp_player"),
    (val_mul, ":leadership", 5),
    (store_attribute_level, ":charisma", "trp_player", ca_charisma),

    (assign, ":ranks", 0),
    (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
      (call_script, "script_get_faction_rank", ":faction"),
      (val_add, ":ranks", reg0),
      (try_begin),
		(eq, ":faction", "$players_kingdom"),
        (val_add, ":ranks", reg0), # double for home faction
      (try_end),
    (try_end),

    # (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
    # (val_div, ":renown", 25),
    (try_begin),(gt, ":leadership", 0),(str_store_string, s2, "@ +"),
     (else_try),                       (str_store_string, s2, "@ "),
    (try_end),
    (try_begin),(gt, ":charisma", 0),(str_store_string, s3, "@ +"),
     (else_try),                     (str_store_string, s3, "@ "),
    (try_end),
    (try_begin),(gt, ":ranks", 0),(str_store_string, s4, "@ +"),
     (else_try),                   (str_store_string, s4, "@ "),
    (try_end),
    # (try_begin),(gt, ":renown", 0),(str_store_string, s4, "@ +"),
    #  (else_try),                   (str_store_string, s4, "@ "),
    # (try_end),
    (assign, reg5, ":party_size_limit"),
    (assign, reg1, ":leadership"),
    (assign, reg2, ":charisma"),
    (assign, reg3, ":ranks"),
    # (assign, reg3, ":renown"),
    (str_clear, s5),
    (try_begin),
      (neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
      (str_store_string, s5, "@Orc hiring bonus: +2/3 for each orc^"),
    (try_end),
    (str_store_string, s1, "@Current party size limit is {reg5}.^Current party size modifiers are:^^Base size:  +10^Leadership: {s2}{reg1}^Charisma: {s3}{reg2}^Ranks: {s4}{reg3}^{s5}TOTAL:  {reg5}"),
#    (str_store_string, s1, "@Current party size limit is {reg5}.^Current party size modifiers are:^^Base size:  +10^Leadership: {s2}{reg1}^Charisma: {s3}{reg2}^TOTAL:  {reg5}"),
#    (str_store_string, s1, "@Current party size limit is {reg5}.^Current party size modifiers are:^^Base size:  +10^Leadership: {s2}{reg1}^Charisma: {s3}{reg2}^Renown: {s4}{reg3}^TOTAL:  {reg5}"),
    ],
    [("continue",[],"Continue...",[(jump_to_menu, "mnu_reports"),]),]
 ),
( "faction_strengths_report",0,
   "{s1}",
   "none",
   [(str_clear, s2),
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
      (neq, ":cur_kingdom", "fac_player_supporters_faction"),
      (call_script, "script_faction_strength_string_to_s23", ":cur_kingdom"),
      (str_store_faction_name, s4, ":cur_kingdom"),
      (faction_get_slot, reg1, ":cur_kingdom", slot_faction_strength),
      (str_store_string, s2, "@{s2}^_________{s4}: {reg1} ({s23})"),
    (try_end),
    (str_store_string, s1, "@_________Faction strengths report:^{s2}"),
    (assign, reg1, "$g_fac_str_siegable"),
    (str_store_string, s1, "@{s1}^^Factions are normally sieged when below {reg1} strength."),
    ],
    [("continue",[],"Continue...", [(jump_to_menu, "mnu_reports")])]
 ),
# ( "faction_relations_report",0,
   # "{s1}",
   # "none",
   # [(str_clear, s2),
    # (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      # (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
      # (neq, ":cur_kingdom", "fac_player_supporters_faction"),
      # (store_relation, ":cur_relation", "fac_player_supporters_faction", ":cur_kingdom"),
      # (try_begin),(ge, ":cur_relation", 90),(str_store_string, s3, "@Loyal"),
      # (else_try), (ge, ":cur_relation", 80),(str_store_string, s3, "@Devoted"),
      # (else_try), (ge, ":cur_relation", 70),(str_store_string, s3, "@Fond"),
      # (else_try), (ge, ":cur_relation", 60),(str_store_string, s3, "@Gracious"),
      # (else_try), (ge, ":cur_relation", 50),(str_store_string, s3, "@Friendly"),
      # (else_try), (ge, ":cur_relation", 40),(str_store_string, s3, "@Supportive"),
      # (else_try), (ge, ":cur_relation", 30),(str_store_string, s3, "@Favorable"),
      # (else_try), (ge, ":cur_relation", 20),(str_store_string, s3, "@Cooperative"),
      # (else_try), (ge, ":cur_relation", 10),(str_store_string, s3, "@Accepting"),
      # (else_try), (ge, ":cur_relation", 0 ),(str_store_string, s3, "@Indifferent"),
      # (else_try), (ge, ":cur_relation",-10),(str_store_string, s3, "@Suspicious"),
      # (else_try), (ge, ":cur_relation",-20),(str_store_string, s3, "@Grumbling"),
      # (else_try), (ge, ":cur_relation",-30),(str_store_string, s3, "@Hostile"),
      # (else_try), (ge, ":cur_relation",-40),(str_store_string, s3, "@Resentful"),
      # (else_try), (ge, ":cur_relation",-50),(str_store_string, s3, "@Angry"),
      # (else_try), (ge, ":cur_relation",-60),(str_store_string, s3, "@Hateful"),
      # (else_try), (ge, ":cur_relation",-70),(str_store_string, s3, "@Revengeful"),
      # (else_try),                           (str_store_string, s3, "@Vengeful"),
      # (try_end),
      # (str_store_faction_name, s4, ":cur_kingdom"),
      # (assign, reg1, ":cur_relation"),
      # (str_store_string, s2, "@{s2}^{s4}: {reg1} ({s3})"),
    # (try_end),
    # (str_store_string, s1, "@Your relation with the factions are:^{s2}"),
    # ],
    # [("continue",[],"Continue...", [(jump_to_menu, "mnu_reports"),]),
    # ]
 # ),
( "traits_report",0,
   "{s1}",
   "none",
   [(set_background_mesh, "mesh_ui_default_menu_window"),
    (str_clear, s2),
    (try_for_range, ":trait", slot_trait_first, slot_trait_last+1),
      (troop_slot_eq, "trp_traits", ":trait", 1),
      
      # Title string = First title string + 2*(slot-1)
      (store_sub, ":title_string", ":trait", 1),
      (val_add, ":title_string", ":title_string"),
      (val_add, ":title_string", tld_first_trait_string),
      (str_store_string, s5, ":title_string"),
      (val_add, ":title_string", 1),
      (str_store_string, s6, ":title_string"), #description string
    
      (str_store_string, s2, "@{s2}^^{s5}^{s6}"),
    (try_end),
    (str_store_string, s1, "@Traits gained:^{s2}"),
    ],
    [("continue",[],"Continue...", [(jump_to_menu, "mnu_reports")])]
 ),

( "camp",0,
   "^^^^You are in {s1}.{s2}^^What do you want to do?",
   "none",
	[ (assign, "$g_player_icon_state", pis_normal),
	  (call_script,"script_maybe_relocate_player_from_z0"),

	  #(assign, reg0, "$current_player_landmark",), (display_message, "@DEBUG: LANDMARK ID {reg0}"),
	  
	  (str_clear, s2),
	  (try_begin), 
		(call_script, "script_cf_store_landmark_description_in_s17", "$current_player_landmark"),
		(str_store_string,s2,"@^^You are {s17}."), 
	  (try_end),
	  
	  (store_add, reg2, "$current_player_region", str_fullname_region_begin),
	  (str_store_string,s1,reg2),
	  (set_background_mesh, "mesh_ui_default_menu_window"),
    ],[
		("camp_scene"      ,[],"Walk around."  ,[
			(assign, "$number_of_combatants", 1), # use a scene as if a battle with one combatant...
			(call_script, "script_jump_to_random_scene", "$current_player_region", "$current_player_terrain",  "$current_player_landmark"), 
			#    (jump_to_scene, "scn_camp_scene"),
			(change_screen_mission)]),
		("camp_troop"      ,[
		    (party_get_num_companions,reg10,"p_main_party"),(val_sub,reg10,1),
		    (party_get_num_prisoners,reg11,"p_main_party"),
              	    (party_count_prisoners_of_type, ":troll_count", "p_main_party", "trp_troll_of_moria"),(val_sub,reg11,":troll_count"),
              	    (party_count_prisoners_of_type, ":troll_count", "p_main_party", "trp_armoured_troll"),(val_sub,reg11,":troll_count"),
              	    (party_count_prisoners_of_type, ":troll_count", "p_main_party", "trp_olog_hai"),(val_sub,reg11,":troll_count"),
		    (this_or_next|gt,reg10,0),(gt,reg11,0),
			(store_mul, reg12, reg10,reg11),
		],"Review{reg10?_troops:}{reg12?_and:}{reg11?_prisoners:}."  ,[
			(assign, "$number_of_combatants", 1), # use a scene as if a battle with one combatant...
			(call_script, "script_jump_to_random_scene", "$current_player_region", "$current_player_terrain",  "$current_player_landmark"), 
			#    (jump_to_scene, "scn_camp_scene"),
			(set_jump_mission,"mt_review_troops"),
			(change_screen_mission)]),
		("camp_action"     ,[],"Use an object."    ,[(jump_to_menu, "mnu_camp_action")]),

  #TLD - modified rest menu, added chance of being attacked by assasins (Kolba)
		("camp_wait_here",[],"Camp here for some time.",
      [		(store_random_in_range,":r",0,10),#random number
			(try_begin),
				(gt,":r",10),#NEVER! 10% of time we are attacked
				#clearing temporary slots
				(try_for_range,":slot",0,10),
					(troop_set_slot,"trp_temp_array_a",":slot",-1),
				(try_end),
				
				(assign,":slot",0),
				(try_for_range,":faction",kingdoms_begin,kingdoms_end),
					(faction_slot_eq,":faction",slot_faction_state,sfs_active),
					(neq,":faction","fac_player_supporters_faction"),
					(store_relation,":relation",":faction","fac_player_faction"),
					(lt,":relation",0),
					(troop_set_slot,"trp_temp_array_a",":slot",":faction"),#save enemy faction to slot
					(val_add,":slot",1),#continue to next slot
				(try_end),
				
				(gt,":slot",0),#if there are no enemy factions, we are simply sleeping
				(store_random_in_range,":faction_slot",0,":slot"),#choose random slot of enemy faction
				(troop_get_slot,":faction","trp_temp_array_a",":faction_slot"),#get faction number from slot
				
				(troop_set_slot,"trp_temp_array_a",0,":faction"),#saves faction (to use it later, in the battle)
          
				#(call_script, "script_asasins_ambush_setup"), # set scene, it's exported to rego0
				(assign,":scene",scn_khand_camp_center),#save scene to variable
				(modify_visitors_at_site,":scene"),
				(reset_visitors),
				(set_visitor,0,"trp_player"),
				
				(faction_get_slot,":troop",":faction",slot_faction_tier_2_troop),# get troop from faction, you can set other tier
				(try_begin),
					(le,":troop",0),#if there are any problems with troop, it's set to normal bandit
					(assign,":troop","trp_bandit"),
				(try_end),
				(set_visitors,1,":troop",5),
                
                (display_message, "@Assassins in the camp, defend yourself!", 0xFF0000),

				(set_jump_mission,"mt_assasins_attack"), #jump to mission template
				(jump_to_scene,":scene"), #jump to scene
				(change_screen_mission), #run mission
			(else_try),
				(assign,"$g_camp_mode", 1),
				#(assign, "$g_infinite_camping", 0),
				(assign, "$g_player_icon_state", pis_camping),
				(rest_for_hours_interactive, 24 * 365, 5, 1), #rest while attackable
				(change_screen_return),
			(try_end), #end trying
	]),

    ("camp_options",[],"Change TLD options.",[(jump_to_menu, "mnu_game_options")]),
	
 ]+concatenate_scripts([[ 
	#SW - added enable/disable camp cheat menu by ConstantA - http://forums.taleworlds.net/index.php/topic,63142.msg1647442.html#msg1647442
	 ("Cheat_enable",[(eq, cheat_switch, 1),(eq,"$cheat_mode",0)],"Enable cheat/modding options.",[(assign, "$cheat_mode", 1),(jump_to_menu, "mnu_camp")]),
     ("camp_cheat_option", [(eq, cheat_switch, 1),(eq,"$cheat_mode",1)] ,"Cheats  (for development use).",[(jump_to_menu, "mnu_camp_cheat")]),
  ## MadVader test begin
     ("camp_test_madvader",[],"MV Test Menu",[(jump_to_menu, "mnu_camp_mvtest")]),
  ## MadVader test end
     ("camp_test_cppcoder",[],"Cpp Test Menu",[(jump_to_menu, "mnu_camp_cctest")]),
 ] for ct in range(cheat_switch)])+[
     ("resume_travelling",[],"Resume travelling.",[(change_screen_return)]),
    ]
 ),
  

## CppCoder test begin
( "camp_cctest",0,
   "Hurry up and pick something already.",
   "none", [],
  [
     	("camp_cctest_injure",[],"Injure Me",[(call_script,"script_injury_routine", "trp_player")]),

	("camp_cctest_injure_party_heroes", [], "Injure Companions",
	[
		(try_for_range, ":npc", companions_begin, companions_end),
            		(main_party_has_troop, ":npc"),
			(call_script,"script_injury_routine", ":npc"),
        	(try_end),
	]),

    	("camp_cctest_heal",[],"Heal my Injuries. (Does not fix prof. or attributes.)",[(troop_set_slot, "trp_player", slot_troop_wound_mask, 0)]),

     	("camp_cctest_kill_lord",[],"Kill a Random Lord",
	[
		(store_random_in_range, ":cur_troop_id", "trp_knight_1_1", kingdom_heroes_end), #kings and marshals cannot die for now
		(call_script, "script_hero_leader_killed_abstractly", ":cur_troop_id","p_main_party")
	]),

     	("camp_cctest_rout_ally",[],"Add troops to routed allies",
	[
		(store_random_in_range, ":troop_no", "trp_gondor_noblemen", "trp_steward_guard"),
		(party_add_members, "p_routed_allies", ":troop_no", 1),
    		(party_get_num_companions, reg1, "p_routed_allies"),
		(display_message, "@Ally party size: {reg1}", color_good_news),
	]),

     	("camp_cctest_rout_enemy",[],"Add troops to routed enemies",
	[
		(store_random_in_range, ":troop_no", "trp_orc_snaga_of_mordor", "trp_wolf_rider_of_moria"),
		(party_add_members, "p_routed_enemies", ":troop_no", 1),
    		(party_get_num_companions, reg1, "p_routed_enemies"),
		(display_message, "@Enemy party size: {reg1}", color_bad_news),
	]),

     	("camp_cctest_rout_spawn",[],"Spawn routed parties",
	[
		(assign, "$g_spawn_allies_routed", 1),
		(assign, "$g_spawn_enemies_routed", 1),
		(call_script,"script_cf_spawn_routed_parties"),
		(display_message, "@Spawned routed parties!", color_good_news),
	]),		
	

     	("camp_cctest_gain_traits",[],"Get All Traits",
	[
		(try_for_range, ":trait", slot_trait_first, slot_trait_last+1),
			(call_script, "script_gain_trait", ":trait"),
		(try_end),
	]),

     	("camp_cctest_parties",[],"Count Parties",
	[
		(assign, reg0, 0),
		(try_for_parties, ":unused"),
			(val_add, reg0, 1),
		(try_end),
		(display_message, "@Party count: {reg0}"),
	]),

     	("camp_cctest_items",[],"Refactionize Items",[(call_script, "script_set_item_faction")]),
     	("camp_cctest_pos",[],"Print Coords x100",
	[
		(set_fixed_point_multiplier, 100),
		(party_get_position, pos13, "p_main_party"),
       		(position_get_x, reg2, pos13),
      		(position_get_y, reg3, pos13),
      		(display_message, "@Party position ({reg2},{reg3}).", 0x30FFC8),
	]),
     	("camp_cctest_defiled",[],"Add WIP Items",
	[
		(troop_add_item, "trp_player","itm_defiled_armor_gondor"),
		(troop_add_item, "trp_player","itm_defiled_armor_rohan"),
		(troop_add_item, "trp_player","itm_defiled_armor_dale"),
		(troop_add_item, "trp_player","itm_gon_leader_surcoat_cloak"),
	]),

     ("camp_cctest_return",[],"Back to camp menu.",[(jump_to_menu, "mnu_camp")]),
  ]
),

## MadVader test begin
( "camp_mvtest",0,
   "What do you want to test today?",
   "none", [],
  [
 ]+concatenate_scripts([[ 
  ("camp_mvtest_pimp",[],"Pimp me up first!",
    [(troop_raise_attribute, "trp_player",ca_strength,20),
     (troop_raise_attribute, "trp_player",ca_agility,20),
     (troop_raise_attribute, "trp_player",ca_intelligence,20),
     (troop_raise_attribute, "trp_player",ca_charisma,20),
     (troop_raise_proficiency_linear, "trp_player", wpt_one_handed_weapon, 500),
     (troop_raise_proficiency_linear, "trp_player", wpt_two_handed_weapon, 500),
     (troop_raise_proficiency_linear, "trp_player", wpt_polearm, 500),
     (troop_raise_proficiency_linear, "trp_player", wpt_archery, 500),
     (troop_raise_proficiency_linear, "trp_player", wpt_crossbow, 500),
     (troop_raise_proficiency_linear, "trp_player", wpt_throwing, 500),
     (troop_raise_skill, "trp_player",skl_ironflesh,10),
     (troop_raise_skill, "trp_player",skl_power_strike,10),
     (troop_raise_skill, "trp_player",skl_weapon_master,10),
     (troop_raise_skill, "trp_player",skl_athletics,10),
     (troop_raise_skill, "trp_player",skl_power_draw,10),
     (troop_raise_skill, "trp_player",skl_riding,10),
     (troop_raise_skill, "trp_player",skl_spotting,10),
     (troop_raise_skill, "trp_player",skl_prisoner_management,10),
     (troop_raise_skill, "trp_player",skl_tactics,10),
     (troop_raise_skill, "trp_player",skl_inventory_management,10),
     (troop_raise_skill, "trp_player",skl_wound_treatment,10),
     (troop_raise_skill, "trp_player",skl_surgery,10),
     (troop_raise_skill, "trp_player",skl_first_aid,10),
     (troop_raise_skill, "trp_player",skl_pathfinding,10),
     (troop_raise_skill, "trp_player",skl_leadership,10),
     (troop_raise_skill, "trp_player",skl_engineer,10),
     (troop_add_gold, "trp_player", 1000000),
	 (troop_set_health, "trp_player", 100),
     (troop_add_item, "trp_player","itm_gondor_lance",imod_balanced),
     (troop_add_item, "trp_player","itm_gondor_shield_d",imod_reinforced),
     (troop_add_item, "trp_player","itm_gondor_ranger_sword",imod_masterwork),
     (troop_add_item, "trp_player","itm_gondor_hunter",imod_champion),
     (troop_add_item, "trp_player","itm_riv_helm_c",imod_lordly),
     (troop_add_item, "trp_player","itm_gon_tower_knight",imod_lordly),
     (troop_add_item, "trp_player","itm_mail_mittens",imod_lordly),
     (troop_add_item, "trp_player","itm_dol_greaves",imod_lordly),
     (troop_add_items, "trp_player","itm_lembas",3),
     (troop_add_items, "trp_player","itm_map",3),
     (troop_equip_items, "trp_player"),
     (troop_sort_inventory, "trp_player"),
     (display_message, "@You have been pimped up!", 0x30FFC8),
    ]
   ),
   ("camp_mvtest_expwar",[(eq, cheat_switch, 1),(eq,"$tld_war_began",0)],"Start the War!",[(add_xp_to_troop,9000,"trp_player"), (display_message, "@9000 XP added - now wait for the War...", 0x30FFC8),]),
   ("camp_mvtest_evilwar",[(eq, cheat_switch, 1),(eq,"$tld_war_began",1)],"Start the War of Two Towers! (defeat all good factions)",[
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
       (neq, ":cur_kingdom", "fac_player_supporters_faction"),
       (faction_slot_eq, ":cur_kingdom", slot_faction_side, faction_side_good),
       (faction_set_slot,":cur_kingdom",slot_faction_strength_tmp,-1000),
    (try_end),
    (display_message, "@Good factions defeated! Now wait for it...", 0x30FFC8),
   ]),
   ("camp_mvtest_rank",[(eq, cheat_switch, 1),],"Give me local money, rank and influence.",[
    (troop_add_gold, "trp_player", 10000),
    (call_script, "script_increase_rank", "$ambient_faction", 100),
    (faction_get_slot, reg0, "$ambient_faction", slot_faction_rank),
    (faction_get_slot, reg1, "$ambient_faction", slot_faction_influence),
    (val_add, reg1, 100),
    (faction_set_slot, "$ambient_faction", slot_faction_influence, reg1),
    (str_store_faction_name, s1, "$ambient_faction"),
    (display_message, "@{s1} rank points increased to {reg0}, influence to {reg1}!", 0x30FFC8),
   ]),
   # ("camp_mvtest_rankfunc",[],"Test rank functions.",[
    # (try_for_range, ":rank_index", 0, 13),
      # (call_script, "script_get_own_rank_title_to_s24", "$ambient_faction", ":rank_index"),
      # (call_script, "script_get_rank_points_for_rank", ":rank_index"),
      # (assign, reg1, ":rank_index"),
      # (display_message, "@Rank {reg1} ({reg0} points): {s24}", 0x30FFC8),
    # (try_end),
    # (try_for_range, ":something", 0, 25),
      # (store_mul, ":rank_points", ":something", 40),
      # (call_script, "script_get_rank_for_rank_points", ":rank_points"),
      # (assign, reg1, ":rank_points"),
      # (display_message, "@Rank points {reg1}: at rank {reg0}.", 0x30FFC8),
    # (try_end),
   # ]),
   # ("camp_mvtest_goodvictory",[],"Defeat all evil factions!",[
    # (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
       # (neq, ":cur_kingdom", "fac_player_supporters_faction"),
       # (neg|faction_slot_eq, ":cur_kingdom", slot_faction_side, faction_side_good),
       # (faction_set_slot,":cur_kingdom",slot_faction_strength_tmp,-1000),
    # (try_end),
    # (display_message, "@Evil factions defeated! Now wait for it...", 0x30FFC8),
   # ]),
   # ("camp_mvtest_influence",[],"Increase ambient faction influence by 100.",[
    # (faction_get_slot, reg0, "$ambient_faction", slot_faction_influence),
    # (val_add, reg0, 100),
    # (faction_set_slot, "$ambient_faction", slot_faction_influence, reg0),
    # (str_store_faction_name, s1, "$ambient_faction"),
    # (display_message, "@{s1} influence increased to {reg0}!", 0x30FFC8),
   # ]),
   ("camp_mvtest_reinf",[(eq, cheat_switch, 1),],"Reinforce me!",[
    (party_get_num_companions, ":old_size", "p_main_party"),
    (try_for_range, ":unused", 0, 10),
      (call_script, "script_cf_reinforce_party", "p_main_party"),
    (try_end),
    (party_get_num_companions, reg1, "p_main_party"),
    (assign, reg0, ":old_size"),
    (display_message, "@Party size increased from {reg0} to {reg1}!", 0x30FFC8),
   ]),
   # ("camp_mvtest_free_willy",[],"Free all prisoners (for corrupt saves)",[
    # (spawn_around_party, "p_main_party", "pt_looters"),
    # (try_for_parties, ":cur_party"),
      # (party_is_active, ":cur_party"),
      # (party_get_num_prisoner_stacks, ":num_stacks", ":cur_party"),
      # (try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
        # (party_prisoner_stack_get_troop_id,     ":stack_troop",":cur_party",":stack_no"),
        # (party_prisoner_stack_get_size,         ":stack_size",":cur_party",":stack_no"),
        # (party_remove_prisoners, ":cur_party", ":stack_troop", ":stack_size"),
      # (try_end),
    # (try_end),
    # (display_message, "@All prisoners freed!", 0x30FFC8),
   # ]),
   # ("camp_mvtest_save_bug",[],"Create a party (for corrupt saves)",[
    # (spawn_around_party, "p_main_party", "pt_looters"),
    # (display_message, "@Party created, ID={reg0}!", 0x30FFC8),
   # ]),
   # ("camp_mvtest_test_music",[],"Test music path (plays track)",[
    # (play_track, "track_TLD_Map_Day_A", 1),
    # (display_message, "@Playing track - can you hear it?", 0x30FFC8),
   # ]),
   ("camp_mvtest_sieges",[(eq, cheat_switch, 1),],"Test sieges...",[(jump_to_menu, "mnu_mvtest_sieges")]),
   # ("camp_mvtest_trolls",[],"Test trolls in battle.",[
     # (party_add_members, "p_main_party", "trp_troll_of_moria", 3),
     # (set_spawn_radius, 0),
     # (spawn_around_party, "p_main_party", "pt_mordor_war_party"),
     # (assign, ":troll_party", reg0),
     # (party_clear, ":troll_party"),
     # (party_add_members, ":troll_party", "trp_black_numenorean_horsemaster", 3),
     # (party_add_members, ":troll_party", "trp_olog_hai", 3),
     # (party_add_members, ":troll_party", "trp_orc_archer_of_mordor", 10),
     # (party_add_members, ":troll_party", "trp_large_orc_of_mordor", 20),
     # (display_message, "@Mordor party with olog hai spawned!", 0x30FFC8),
   # ]),            
   ("camp_mvtest_legend",[(eq, cheat_switch, 1),],"Enable legendary places.",[
    (enable_party, "p_legend_amonhen"),
    (enable_party, "p_legend_deadmarshes"),
    (enable_party, "p_legend_mirkwood"),
    (enable_party, "p_legend_fangorn"),
    (display_message, "@All four legendary places enabled!", 0x30FFC8),
   ]),
   ("camp_mvtest_intro",[(eq, cheat_switch, 1),],"Test cutscenes...",[(jump_to_menu, "mnu_mvtest_cutscenes"),]),
   # ("camp_mvtest_rewards",[],"Print ambient faction reward items.",[
    # (store_sub, ":faction_index", "$ambient_faction", kingdoms_begin),
    # (try_begin),
        # ]+concatenate_scripts([
            # [
            # (eq, ":faction_index", x),
            # ]+concatenate_scripts([[
                # (assign, ":rank", fac_reward_items_list[x][item_entry][0]),
                # (assign, ":item", fac_reward_items_list[x][item_entry][1]),
                # (assign, ":modifier", fac_reward_items_list[x][item_entry][2]),
                # (assign, reg0, ":rank"),
                # (assign, reg1, ":modifier"),
                # (str_store_item_name, s20, ":item"),
                # (display_message, "@Rank {reg0}: {s20}, mod {reg1}.", 0x30FFC8),
                # ] for item_entry in range(len(fac_reward_items_list[x]))
            # ])+[
         # (else_try),
            # ] for x in range(len(fac_reward_items_list))
        # ])+[
    # (try_end),   
   # ]),
   # ("camp_mvtest_coords",[],"Print party coordinates x100.",[
      # (set_fixed_point_multiplier, 100),
      # (party_get_position, pos13, "p_main_party"),
      # (position_get_x, reg2, pos13),
      # (position_get_y, reg3, pos13),
      # (display_message, "@Party position ({reg2},{reg3}).", 0x30FFC8),
   # ]),
   ("camp_mvtest_facstr",[(eq, cheat_switch, 1),],"View faction strengths.",[(jump_to_menu, "mnu_mvtest_facstr_report")]),
   ("camp_mvtest_killed",[(eq, cheat_switch, 1),],"View faction casualties.",[(jump_to_menu, "mnu_mvtest_faction_casualties")]),
   ("camp_mvtest_facai",[(eq, cheat_switch, 1),],"View faction AI.",[(jump_to_menu, "mnu_mvtest_facai_report")]),
   ("camp_mvtest_towns",[(eq, cheat_switch, 1),],"View center strength income.",[(jump_to_menu, "mnu_mvtest_town_wealth_report")]),
   # ("camp_mvtest_wm",[],"Where is my party?",[
    # (try_begin),
      # (call_script, "script_cf_party_is_south_of_white_mountains", "p_main_party"),
      # (display_message, "@The party is south of the White Mountains.", 0x30FFC8),
    # (else_try),
      # (call_script, "script_cf_party_is_north_of_white_mountains", "p_main_party"),
      # (display_message, "@The party is north of the White Mountains.", 0x30FFC8),
    # (else_try),
      # (display_message, "@The party is east of the White Mountains.", 0x30FFC8),
    # (try_end),
   # ]),
   # ("camp_mvtest_formula",[],"Test line formulas.",[
    # (call_script, "script_get_line_through_parties", "p_town_hornburg", "p_town_minas_tirith"),
    # (display_message, "@Debug: Hornburg-MT line: y = {reg0}/{reg1}*x + {reg2}"),
    # (call_script, "script_get_line_through_parties", "p_town_harad_camp", "p_town_minas_tirith"),
    # (display_message, "@Debug: Harad-MT line: y = {reg0}/{reg1}*x + {reg2}"),
    # (call_script, "script_get_line_through_parties", "p_town_morannon", "p_town_minas_tirith"),
    # (display_message, "@Debug: Morannon-MT line: y = {reg0}/{reg1}*x + {reg2}"),
   # ]),
   ("camp_mvtest_defeat",[(eq, cheat_switch, 1),],"Defeat a faction.",[(jump_to_menu, "mnu_mvtest_destroy_faction")]),
   ("camp_mvtest_advcamps",[(eq, cheat_switch, 1),],"Test advance camps.",[(jump_to_menu, "mnu_mvtest_advcamps")]),
   # ("camp_mvtest_destroy",[],"Destroy Hornburg!",[
     # (assign, ":root_defeated_party", "p_town_hornburg"),
     # (party_set_slot, ":root_defeated_party", slot_center_destroyed, 1), # DESTROY!
     # # disable and replace with ruins
     # (set_spawn_radius, 0),
     # (spawn_around_party, ":root_defeated_party", "pt_ruins"),
     # (assign, ":ruin_party", reg0),
     # #(party_get_icon, ":map_icon", ":root_defeated_party"),
     # #(party_set_icon, ":ruin_party", ":map_icon"),
     # (str_store_party_name, s1, ":root_defeated_party"),
     # (disable_party, ":root_defeated_party"),
     # (party_set_flags, ":ruin_party", pf_is_static|pf_always_visible|pf_hide_defenders|pf_label_medium, 1),
     # (party_set_name, ":ruin_party", "@{s1} ruins"),
     # (display_message, "@Hornburg razed - check map!", 0x30FFC8),
   # ]),
   ("camp_mvtest_wait",[(eq, cheat_switch, 1),],"Fast forward for 30 days.",[
         (assign, "$g_camp_mode", 1),
         (assign, "$g_player_icon_state", pis_camping),
         (rest_for_hours_interactive, 24 * 30, 40), #30 day rest while not attackable with 40x speed
         (change_screen_return),
   ]), 
   # ("camp_mvtest_notes",[],"Update lord locations.",[
     # (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
       # (call_script, "script_update_troop_location_notes", ":troop_no", 0),
     # (try_end),
     # (display_message, "@Lord locations updated - see wiki!", 0x30FFC8),
   # ]),            
   # ("camp_mvtest_rescue",[],"Spawn a party with prisoners.",[
     # (set_spawn_radius, 0),
     # (spawn_around_party, "p_main_party", "pt_looters"),
     # (party_add_prisoners, reg0, "trp_peasant_woman", 10),
     # (display_message, "@Tribal orcs with women spawned!", 0x30FFC8),
   #]),
   # ("camp_mvtest_npcs",[],"Get all good npcs.",[
    # (try_for_range, ":npc", companions_begin, companions_end),
		# (store_troop_faction, ":fac", ":npc"),
		# (faction_slot_eq, ":fac", slot_faction_side, faction_side_good),
		# (party_add_members,"p_main_party",":npc",1),
	# (try_end),
    # (display_message, "@You got them all, pardner!", 0x30FFC8),
   # ]),
 ] for ct in range(cheat_switch)])+[
   ("camp_mvtest_back",[],"Back to camp menu.",[(jump_to_menu, "mnu_camp")])]            
 ),
( "mvtest_destroy_faction",0,
   "Choose a faction to defeat:",
   "none",
   [],
  [("back_test",[],"Back to test menu.", [(jump_to_menu, "mnu_camp_mvtest"),]),]
  +
  concatenate_scripts([[
  (
	"kill_faction",
	[(faction_slot_eq, faction_init[y][0], slot_faction_state, sfs_active),
     (faction_slot_ge, faction_init[y][0], slot_faction_strength_tmp, 0),
     (str_store_faction_name, s10, faction_init[y][0]),],
	"{s10}.",
	[
		(faction_set_slot, faction_init[y][0], slot_faction_strength_tmp, -1000),
        (str_store_faction_name, s10, faction_init[y][0]),
		(display_message, "@{s10} defeated! Now wait for it...", 0x30FFC8),
    ]
  )
  ]for y in range(len(faction_init)) ])      
 ),
( "mvtest_facstr_report",0,
   "{s1}",
   "none",
   [(str_clear, s2),
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
      (neq, ":cur_kingdom", "fac_player_supporters_faction"),
      (call_script, "script_faction_strength_string_to_s23", ":cur_kingdom"),
      (str_store_faction_name, s4, ":cur_kingdom"),
      (faction_get_slot, reg1, ":cur_kingdom", slot_faction_strength),
      (faction_get_slot, reg2, ":cur_kingdom", slot_faction_debug_str_gain),
      (faction_get_slot, reg3, ":cur_kingdom", slot_faction_debug_str_loss),
      (val_sub, reg2, reg3),
      (str_store_string, s2, "@{s2}^{s4}: {reg1} ({s23}) Diff: {reg2}"),
    (try_end),
    (str_store_string, s1, "@Faction strengths report:^{s2}"),
    ],
    [("back_test",[],"Back to test menu.", [(jump_to_menu, "mnu_camp_mvtest"),]),
    ]
 ),
( "mvtest_facai_report",0,
   "{s1}",
   "none",
   [(str_clear, s2),
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (neq, ":cur_kingdom", "fac_player_supporters_faction"),
      (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
      (faction_get_slot, ":faction_ai_state", ":cur_kingdom", slot_faction_ai_state),
      (faction_get_slot, ":faction_ai_object", ":cur_kingdom", slot_faction_ai_object),
      (faction_get_slot, ":faction_theater", ":cur_kingdom", slot_faction_active_theater),
      (faction_get_slot, ":home_theater", ":cur_kingdom", slot_faction_home_theater),
      
	  # calculate number of active hosts
      (assign,":hosts",0),
	  (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end), 
        (store_troop_faction, ":troop_faction_no", ":troop_no"),
        (eq, ":troop_faction_no", ":cur_kingdom"),
		(troop_get_slot, ":party", ":troop_no", slot_troop_leaded_party),
		(gt,":party",0),
		(party_slot_eq, ":party", slot_party_type, spt_kingdom_hero_party),
	    (val_add,":hosts",1),
	  (try_end),
      
      # AI string
      (try_begin),
        (eq, ":faction_ai_state", sfai_default),
        (str_store_string, s11, "@Defending"),
      (else_try),
        (eq, ":faction_ai_state", sfai_gathering_army),
        (str_store_string, s11, "@Gathering army"),
      (else_try),
        (eq, ":faction_ai_state", sfai_attacking_center),
        (str_store_party_name, s11, ":faction_ai_object"),
        (str_store_string, s11, "@Besieging {s11}"),
      (else_try),
        (eq, ":faction_ai_state", sfai_attacking_enemies_around_center),
        (str_store_party_name, s11, ":faction_ai_object"),
        (str_store_string, s11, "@Attacking enemies around {s11}"),
      (else_try),
        (eq, ":faction_ai_state", sfai_attacking_enemy_army),
        (str_store_party_name, s11, ":faction_ai_object"),
        (str_store_string, s11, "@Attacking enemy party {s11}"),
      (else_try),
        (assign, reg3, ":faction_ai_state"), (str_store_string, s11, "@Unknown({reg3})"),
      (try_end),
      
      # theater string
      (try_begin),
        (eq, ":home_theater", theater_SE),
        (str_store_string, s9, "@SE"),
      (else_try),
        (eq, ":home_theater", theater_SW),
        (str_store_string, s9, "@SW"),
      (else_try),
        (eq, ":home_theater", theater_C),
        (str_store_string, s9, "@C"),
      (else_try),
        (eq, ":home_theater", theater_N),
        (str_store_string, s9, "@N"),
      (else_try),
        (str_store_string, s9, "@INVALID"),
      (try_end),
      # theater string
      (try_begin),
        (eq, ":faction_theater", theater_SE),
        (str_store_string, s10, "@SE"),
      (else_try),
        (eq, ":faction_theater", theater_SW),
        (str_store_string, s10, "@SW"),
      (else_try),
        (eq, ":faction_theater", theater_C),
        (str_store_string, s10, "@C"),
      (else_try),
        (eq, ":faction_theater", theater_N),
        (str_store_string, s10, "@N"),
      (else_try),
        (str_store_string, s10, "@INVALID"),
      (try_end),
      
      (str_store_faction_name, s4, ":cur_kingdom"),
      (faction_get_slot, reg1, ":cur_kingdom", slot_faction_strength),
      (assign, reg2, ":hosts"),
      (str_store_string, s2, "@{s2}^{s4}: Th: {s9}-{s10} Str: {reg1} Hosts: {reg2} {s11}"),
    (try_end),
    (str_store_string, s1, "@Faction AI report:^{s2}"),
    ],
    [("details",[],"Detailed faction report...", [(jump_to_menu, "mnu_mvtest_facai_details"),]),
     ("back_mtest",[],"Back to main test menu.", [(jump_to_menu, "mnu_camp_mvtest"),]),
    ]
 ),
( "mvtest_facai_details",0,
   "{s1}",
   "none",
   [
      (try_begin),
	    (neg|is_between, "$g_mvtest_faction", kingdoms_begin, kingdoms_end), #first use?
	    (assign, "$g_mvtest_faction", kingdoms_begin), #gondor
	  (try_end),
        
      (assign, ":cur_kingdom", "$g_mvtest_faction"),
      
      (faction_get_slot, ":faction_ai_state", ":cur_kingdom", slot_faction_ai_state),
      (faction_get_slot, ":faction_ai_object", ":cur_kingdom", slot_faction_ai_object),
      (faction_get_slot, ":faction_theater", ":cur_kingdom", slot_faction_active_theater),
      (faction_get_slot, ":home_theater", ":cur_kingdom", slot_faction_home_theater),
      
	  # calculate number of active hosts
      (assign,":hosts",0),
	  (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end), 
        (store_troop_faction, ":troop_faction_no", ":troop_no"),
        (eq, ":troop_faction_no", ":cur_kingdom"),
		(troop_get_slot, ":party", ":troop_no", slot_troop_leaded_party),
		(gt,":party",0),
		(party_slot_eq, ":party", slot_party_type, spt_kingdom_hero_party),
	    (val_add,":hosts",1),
	  (try_end),
      
      # AI string
      (try_begin),
        (eq, ":faction_ai_state", sfai_default),
        (str_store_string, s11, "@Defending"),
      (else_try),
        (eq, ":faction_ai_state", sfai_gathering_army),
        (str_store_string, s11, "@Gathering army"),
      (else_try),
        (eq, ":faction_ai_state", sfai_attacking_center),
        (str_store_party_name, s11, ":faction_ai_object"),
        (str_store_string, s11, "@Besieging {s11}"),
      (else_try),
        (eq, ":faction_ai_state", sfai_attacking_enemies_around_center),
        (str_store_party_name, s11, ":faction_ai_object"),
        (str_store_string, s11, "@Attacking enemies around {s11}"),
      (else_try),
        (eq, ":faction_ai_state", sfai_attacking_enemy_army),
        (str_store_party_name, s11, ":faction_ai_object"),
        (str_store_string, s11, "@Attacking enemy party {s11}"),
      (else_try),
        (assign, reg3, ":faction_ai_state"), (str_store_string, s11, "@Unknown({reg3})"),
      (try_end),
      
      # theater string
      (try_begin),
        (eq, ":home_theater", theater_SE),
        (str_store_string, s9, "@SE"),
      (else_try),
        (eq, ":home_theater", theater_SW),
        (str_store_string, s9, "@SW"),
      (else_try),
        (eq, ":home_theater", theater_C),
        (str_store_string, s9, "@C"),
      (else_try),
        (eq, ":home_theater", theater_N),
        (str_store_string, s9, "@N"),
      (else_try),
        (str_store_string, s9, "@INVALID"),
      (try_end),
      # theater string
      (try_begin),
        (eq, ":faction_theater", theater_SE),
        (str_store_string, s10, "@SE"),
      (else_try),
        (eq, ":faction_theater", theater_SW),
        (str_store_string, s10, "@SW"),
      (else_try),
        (eq, ":faction_theater", theater_C),
        (str_store_string, s10, "@C"),
      (else_try),
        (eq, ":faction_theater", theater_N),
        (str_store_string, s10, "@N"),
      (else_try),
        (str_store_string, s10, "@INVALID"),
      (try_end),
      
      (str_store_faction_name, s4, ":cur_kingdom"),
      (faction_get_slot, reg1, ":cur_kingdom", slot_faction_strength),
      (assign, reg2, ":hosts"),
      (str_store_string, s1, "@Detailed faction AI report for {s4}:^Theater:{s9}-{s10} Str:{reg1} Hosts:{reg2} {s11}"),
      (try_begin),
        (neg|faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
        (str_store_string, s1, "@Faction defeated!^{s1}"),
      (try_end),
      
	  # AI details for each host
	  (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end), 
        (store_troop_faction, ":troop_faction_no", ":troop_no"),
        (eq, ":troop_faction_no", ":cur_kingdom"),
		(troop_get_slot, ":party", ":troop_no", slot_troop_leaded_party),
		(gt,":party",0),
        
        (str_store_troop_name, s6, ":troop_no"),
        (str_store_party_name, s7, ":party"),
        (str_store_string, s1, "@{s1}^{s6} leads {s7}, "),
        (try_begin),
          (party_slot_eq, ":party", slot_party_type, spt_kingdom_hero_alone),
          (str_store_string, s1, "@{s1}(no host), "),          
        (try_end),
        
        (party_get_slot, ":party_ai_state", ":party", slot_party_ai_state),
        (party_get_slot, ":party_ai_object", ":party", slot_party_ai_object),
        (try_begin),
          (ge, ":party_ai_object", 0),
          (str_store_party_name, s7, ":party_ai_object"),
        (else_try),
          (str_store_string, s7, "@INVALID"),
        (try_end),
        
        # AI string
        (try_begin),(eq, ":party_ai_state", spai_undefined),               (str_store_string, s1, "@{s1}doing nothing"),
         (else_try),(eq, ":party_ai_state", spai_accompanying_army),       (str_store_string, s1, "@{s1}escorting {s7}"),
         (else_try),(eq, ":party_ai_state", spai_besieging_center),        (str_store_string, s1, "@{s1}besieging {s7}"),
         (else_try),(eq, ":party_ai_state", spai_holding_center),          (str_store_string, s1, "@{s1}defending {s7}"),
         (else_try),(eq, ":party_ai_state", spai_patrolling_around_center),(str_store_string, s1, "@{s1}patrolling around {s7}"),
         (else_try),(eq, ":party_ai_state", spai_recruiting_troops),       (str_store_string, s1, "@{s1}recruiting in {s7} - INVALID"),
         (else_try),(eq, ":party_ai_state", spai_raiding_around_center),   (str_store_string, s1, "@{s1}raiding around {s7} - INVALID"),
         (else_try),(eq, ":party_ai_state", spai_engaging_army),           (str_store_string, s1, "@{s1}engaging {s7}"),
         (else_try),(eq, ":party_ai_state", spai_retreating_to_center),    (str_store_string, s1, "@{s1}retreating to {s7}"),
         (else_try),                    (assign, reg3, ":party_ai_state"), (str_store_string, s1, "@{s1}unknown({reg3})"),
        (try_end),
	  (try_end),
    ],
    [("change",[
        (str_store_faction_name, s7, "$g_mvtest_faction"),
      ],
      "Change faction: {s7}",
      [
        (val_add, "$g_mvtest_faction", 1),
        (try_begin),
	      (eq, "$g_mvtest_faction", "fac_player_supporters_faction"),
	      (assign, "$g_mvtest_faction", kingdoms_begin),
	    (try_end),
      ]),
     ("defeat",[],"Set faction strength to -1000 (defeat).", [
       (faction_set_slot,"$g_mvtest_faction",slot_faction_strength_tmp,-1000),
       (display_message, "@Faction defeated! Now wait for it...", 0x30FFC8),]),
     ("dying",[],"Set faction strength to 300 (dying).", [
       (faction_set_slot,"$g_mvtest_faction",slot_faction_strength_tmp,300),
       (display_message, "@Faction almost defeated! Wait for the guardians to spawn...", 0x30FFC8),]),
     ("spent",[],"Set faction strength to 600 (spent).", [
       (faction_set_slot,"$g_mvtest_faction",slot_faction_strength_tmp,600),
       (display_message, "@Faction almost defeated! The AI can go for the capital now...", 0x30FFC8),]),
     ("back_ai",[],"Back to faction AI.", [(jump_to_menu, "mnu_mvtest_facai_report"),]),
    ]
 ),
( "mvtest_faction_casualties",0,
   "{s1}",
   "none",
   [  (try_begin),
	    (neg|is_between, "$g_mvtest_faction", kingdoms_begin, kingdoms_end), #first use?
	    (assign, "$g_mvtest_faction", kingdoms_begin), #gondor
	  (try_end),
        
      (assign, ":total_strength_loss", 0),
      
      (store_current_day, reg1),
      (str_store_faction_name, s4, "$g_mvtest_faction"),
      (str_store_string, s1, "@{s4} spawn losses after {reg1} days^"),
      
      # (assign, ":faction_scouts", 0),
      # (assign, ":faction_raiders", 0),
      # (assign, ":faction_patrol", 0),
      (assign, ":faction_caravan", 0),
      
      # abusing chests as scout, raider, patrol arrays (slot 0: length, slots 1,2,3.. array)
      (troop_set_slot, "trp_bonus_chest_1", 0, 0),
      (troop_set_slot, "trp_bonus_chest_2", 0, 0),
      (troop_set_slot, "trp_bonus_chest_3", 0, 0),
      
      # determine faction spawns (scouts, raiders, patrol, caravan) by looking at center spawns
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
        (store_faction_of_party, ":center_faction", ":center_no"),
        (eq, ":center_faction", "$g_mvtest_faction"),
        #(party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD - not destroyed; not important
        (party_get_slot, ":center_scouts", ":center_no", slot_center_spawn_scouts),
        (party_get_slot, ":center_raiders", ":center_no", slot_center_spawn_raiders),
        (party_get_slot, ":center_patrol", ":center_no", slot_center_spawn_patrol),
        (party_get_slot, ":center_caravan", ":center_no", slot_center_spawn_caravan),
        (try_begin),
          (gt, ":center_scouts", 0),
          (troop_get_slot, ":number_spawns", "trp_bonus_chest_1", 0),
          (store_add, ":number_spawns_plus_one", ":number_spawns", 1),
          (assign, ":scout_found", 0),
          (try_for_range, ":slot", 1, ":number_spawns_plus_one"),
            (troop_slot_eq, "trp_bonus_chest_1", ":slot", ":center_scouts"),
            (assign, ":scout_found", 1),
          (try_end),
          (eq, ":scout_found", 0),
          (troop_set_slot, "trp_bonus_chest_1", 0, ":number_spawns_plus_one"),
          (troop_set_slot, "trp_bonus_chest_1", ":number_spawns_plus_one", ":center_scouts"),
        (try_end),
        (try_begin),
          (gt, ":center_raiders", 0),
          (troop_get_slot, ":number_spawns", "trp_bonus_chest_2", 0),
          (store_add, ":number_spawns_plus_one", ":number_spawns", 1),
          (assign, ":scout_found", 0),
          (try_for_range, ":slot", 1, ":number_spawns_plus_one"),
            (troop_slot_eq, "trp_bonus_chest_2", ":slot", ":center_raiders"),
            (assign, ":scout_found", 1),
          (try_end),
          (eq, ":scout_found", 0),
          (troop_set_slot, "trp_bonus_chest_2", 0, ":number_spawns_plus_one"),
          (troop_set_slot, "trp_bonus_chest_2", ":number_spawns_plus_one", ":center_raiders"),
        (try_end),
        (try_begin),
          (gt, ":center_patrol", 0),
          (troop_get_slot, ":number_spawns", "trp_bonus_chest_3", 0),
          (store_add, ":number_spawns_plus_one", ":number_spawns", 1),
          (assign, ":scout_found", 0),
          (try_for_range, ":slot", 1, ":number_spawns_plus_one"),
            (troop_slot_eq, "trp_bonus_chest_3", ":slot", ":center_patrol"),
            (assign, ":scout_found", 1),
          (try_end),
          (eq, ":scout_found", 0),
          (troop_set_slot, "trp_bonus_chest_3", 0, ":number_spawns_plus_one"),
          (troop_set_slot, "trp_bonus_chest_3", ":number_spawns_plus_one", ":center_patrol"),
        (try_end),
        (try_begin), #one type of caravan, if any
          (eq, ":faction_caravan", 0), (gt, ":center_caravan", 0), (assign, ":faction_caravan", ":center_caravan"),
        (try_end),
	  (try_end),
      
      # Print out the results
      (try_begin),
        (troop_get_slot, ":number_spawns", "trp_bonus_chest_1", 0),
        (gt, ":number_spawns", 0),
        (assign, ":spawns_destroyed", 0),
        (assign, ":spawns_active", 0),
        (store_add, ":number_spawns_plus_one", ":number_spawns", 1),
        (try_for_range, ":slot", 1, ":number_spawns_plus_one"),
          (troop_get_slot, ":spawn", "trp_bonus_chest_1", ":slot"),
          (store_num_parties_destroyed, ":val", ":spawn"),
          (val_add, ":spawns_destroyed", ":val"),
          (store_num_parties_of_template, ":val", ":spawn"),
          (val_add, ":spawns_active", ":val"),
        (try_end),
        (assign, reg1, ":spawns_destroyed"),
        (assign, reg3, ":spawns_active"),
        (store_mul, reg2, reg1, ws_scout_vp), #strength loss
        (str_store_string, s1, "@{s1}^Scouts lost: {reg1} Str loss: {reg2} Active: {reg3}"),
        (val_add, ":total_strength_loss", reg2),
      (try_end),
      (try_begin),
        (troop_get_slot, ":number_spawns", "trp_bonus_chest_2", 0),
        (gt, ":number_spawns", 0),
        (assign, ":spawns_destroyed", 0),
        (assign, ":spawns_active", 0),
        (store_add, ":number_spawns_plus_one", ":number_spawns", 1),
        (try_for_range, ":slot", 1, ":number_spawns_plus_one"),
          (troop_get_slot, ":spawn", "trp_bonus_chest_2", ":slot"),
          (store_num_parties_destroyed, ":val", ":spawn"),
          (val_add, ":spawns_destroyed", ":val"),
          (store_num_parties_of_template, ":val", ":spawn"),
          (val_add, ":spawns_active", ":val"),
        (try_end),
        (assign, reg1, ":spawns_destroyed"),
        (assign, reg3, ":spawns_active"),
        (store_mul, reg2, reg1, ws_raider_vp), #strength loss
        (str_store_string, s1, "@{s1}^Raiders lost: {reg1} Str loss: {reg2} Active: {reg3}"),
        (val_add, ":total_strength_loss", reg2),
      (try_end),
      (try_begin),
        (troop_get_slot, ":number_spawns", "trp_bonus_chest_3", 0),
        (gt, ":number_spawns", 0),
        (assign, ":spawns_destroyed", 0),
        (assign, ":spawns_active", 0),
        (store_add, ":number_spawns_plus_one", ":number_spawns", 1),
        (try_for_range, ":slot", 1, ":number_spawns_plus_one"),
          (troop_get_slot, ":spawn", "trp_bonus_chest_3", ":slot"),
          (store_num_parties_destroyed, ":val", ":spawn"),
          (val_add, ":spawns_destroyed", ":val"),
          (store_num_parties_of_template, ":val", ":spawn"),
          (val_add, ":spawns_active", ":val"),
        (try_end),
        (assign, reg1, ":spawns_destroyed"),
        (assign, reg3, ":spawns_active"),
        (store_mul, reg2, reg1, ws_patrol_vp), #strength loss
        (str_store_string, s1, "@{s1}^Patrols lost: {reg1} Str loss: {reg2} Active: {reg3}"),
        (val_add, ":total_strength_loss", reg2),
      (try_end),
      (try_begin),
        (gt, ":faction_caravan", 0),
        (store_num_parties_destroyed, reg1, ":faction_caravan"),
        (store_mul, reg2, reg1, ws_caravan_vp), #strength loss
        (store_num_parties_of_template, reg3, ":faction_caravan"),
        (str_store_string, s1, "@{s1}^Caravans lost: {reg1} Str loss: {reg2} Active: {reg3}"),
        (val_add, ":total_strength_loss", reg2),
      (try_end),
      (faction_get_slot, ":prisoner_train_pt", "$g_mvtest_faction", slot_faction_prisoner_train),
      (try_begin),
        (gt, ":prisoner_train_pt", 0),
        (store_num_parties_destroyed, reg1, ":prisoner_train_pt"), #note that removed on arrival are also counted here
        (store_mul, reg2, reg1, ws_p_train_vp), #strength loss
        (store_num_parties_of_template, reg3, ":prisoner_train_pt"),
        (str_store_string, s1, "@{s1}^P. trains lost-arrived: {reg1} Strength loss: 0{reg2?-{reg2}:} Active: {reg3}"),
        #(val_add, ":total_strength_loss", reg2),
      (try_end),
      
      (faction_get_slot, reg1, "$g_mvtest_faction", slot_faction_debug_str_gain),
      (str_store_string, s1, "@{s1}^^Total strength gain: {reg1}"),
      (faction_get_slot, reg2, "$g_mvtest_faction", slot_faction_debug_str_loss),
      (str_store_string, s1, "@{s1}^Total strength loss: {reg2}"),
      (assign, reg3, ":total_strength_loss"),
      (str_store_string, s1, "@{s1}^(Strength loss from spawns: {reg3})"),
      (val_sub, reg1, reg2),
      (str_store_string, s1, "@{s1}^Difference: {reg1}"),
    ],
    [("prev_faction",[],
      "Previous faction",
      [
        (try_begin),
	      (eq, "$g_mvtest_faction", kingdoms_begin),
	      (assign, "$g_mvtest_faction", kingdoms_end),
	    (try_end),
        (val_sub, "$g_mvtest_faction", 1),
      ]),
     ("next_faction",[],
      "Next faction",
      [
        (val_add, "$g_mvtest_faction", 1),
        (try_begin),
	      (eq, "$g_mvtest_faction", kingdoms_end),
	      (assign, "$g_mvtest_faction", kingdoms_begin),
	    (try_end),
      ]),
     ("back_mtest",[],"Back to main test menu.", [(jump_to_menu, "mnu_camp_mvtest"),]),
    ]
 ),
( "mvtest_town_wealth_report",0,
   "{s1}",
   "none",
   [  (try_begin),
	    (neg|is_between, "$g_mvtest_faction", kingdoms_begin, kingdoms_end), #first use?
	    (assign, "$g_mvtest_faction", kingdoms_begin), #gondor
	  (try_end),
        
      (assign, ":cur_kingdom", "$g_mvtest_faction"),
      (assign, ":total_income", 0),
      
      (str_store_faction_name, s4, ":cur_kingdom"),
      (str_store_string, s1, "@Daily strength income and garrisons for {s4}"),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
		(party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD
        (store_faction_of_party, ":center_faction", ":center_no"),
        (eq, ":center_faction", ":cur_kingdom"),
        (party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD - not destroyed
        (str_store_party_name, s7, ":center_no"),
        (party_get_slot, reg1, ":center_no", slot_center_strength_income),
        (party_get_slot, reg2, ":center_no", slot_center_garrison_limit),
        (party_get_num_companions, reg3, ":center_no"),
        (party_get_slot, reg4, ":center_no", slot_center_destroy_on_capture),
        (val_add, ":total_income", reg1),
        (str_store_string, s1, "@{s1}^{s7}: {reg1}  Garrison: {reg3}/{reg2}{reg4?: Capturable}"),
	  (try_end),
      (assign, reg1, ":total_income"),
      (str_store_string, s1, "@{s1}^^Total: {reg1}"),
    ],
    [("change",[
        (str_store_faction_name, s7, "$g_mvtest_faction"),
      ],
      "Change faction: {s7}",
      [
        (val_add, "$g_mvtest_faction", 1),
        (try_begin),
	      (eq, "$g_mvtest_faction", "fac_player_supporters_faction"),
	      (assign, "$g_mvtest_faction", kingdoms_begin),
	    (try_end),
      ]),
     ("back_mtest",[],"Back to main test menu.", [(jump_to_menu, "mnu_camp_mvtest"),]),
    ]
 ),
( "mvtest_sieges",0,
   "Test sieges",
   "none",
   [],
    [
 ]+concatenate_scripts([[ 
	("order_siege",[],"Order ambient faction to besiege...", [(jump_to_menu, "mnu_mvtest_order_siege")]),
     ("order_siege_wo",[
        (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_is_active, ":king_party"),
     ],"Order Gothmog to besiege West Osgiliath.",
      [ (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_detach, ":king_party"),
        (party_relocate_near_party, ":king_party", "p_town_west_osgiliath", 0),
        (party_set_slot, "p_town_west_osgiliath", slot_center_is_besieged_by, ":king_party"),
        (call_script, "script_party_set_ai_state", ":king_party", spai_besieging_center, "p_town_west_osgiliath"),
        (party_set_ai_behavior, ":king_party", ai_bhvr_attack_party),
        (party_set_ai_object, ":king_party", "p_town_west_osgiliath"),
        (party_set_flags, ":king_party", pf_default_behavior, 1),
        (party_set_slot, ":king_party", slot_party_ai_substate, 1),
        (display_message, "@Gothmog besieges West Osgiliath!", 0x30FFC8),
        (change_screen_map),
      ]),
	  ("order_siege_erech",[
        (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_is_active, ":king_party"),
     ],"Order Gothmog to besiege Erech.",
      [ (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_detach, ":king_party"),
        (party_relocate_near_party, ":king_party", "p_town_erech", 0),
        (party_set_slot, "p_town_erech", slot_center_is_besieged_by, ":king_party"),
        (call_script, "script_party_set_ai_state", ":king_party", spai_besieging_center, "p_town_erech"),
        (party_set_ai_behavior, ":king_party", ai_bhvr_attack_party),
        (party_set_ai_object, ":king_party", "p_town_erech"),
        (party_set_flags, ":king_party", pf_default_behavior, 1),
        (party_set_slot, ":king_party", slot_party_ai_substate, 1),
        (display_message, "@Gothmog besieges Erech!", 0x30FFC8),
        (change_screen_map),
      ]),
	 ("order_siege_pinnath",[
        (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_is_active, ":king_party"),
     ],"Order Gothmog to besiege Pinnath Gelin.",
      [ (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_detach, ":king_party"),
        (party_relocate_near_party, ":king_party", "p_town_pinnath_gelin", 0),
        (party_set_slot, "p_town_pinnath_gelin", slot_center_is_besieged_by, ":king_party"),
        (call_script, "script_party_set_ai_state", ":king_party", spai_besieging_center, "p_town_pinnath_gelin"),
        (party_set_ai_behavior, ":king_party", ai_bhvr_attack_party),
        (party_set_ai_object, ":king_party", "p_town_pinnath_gelin"),
        (party_set_flags, ":king_party", pf_default_behavior, 1),
        (party_set_slot, ":king_party", slot_party_ai_substate, 1),
        (display_message, "@Gothmog besieges Pinnath Gelin!", 0x30FFC8),
        (change_screen_map),
      ]),
	 ("order_siege_edhellond",[
        (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_is_active, ":king_party"),
     ],"Order Gothmog to besiege Edhellond.",
      [ (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_detach, ":king_party"),
        (party_relocate_near_party, ":king_party", "p_town_edhellond", 0),
        (party_set_slot, "p_town_edhellond", slot_center_is_besieged_by, ":king_party"),
        (call_script, "script_party_set_ai_state", ":king_party", spai_besieging_center, "p_town_edhellond"),
        (party_set_ai_behavior, ":king_party", ai_bhvr_attack_party),
        (party_set_ai_object, ":king_party", "p_town_edhellond"),
        (party_set_flags, ":king_party", pf_default_behavior, 1),
        (party_set_slot, ":king_party", slot_party_ai_substate, 1),
        (display_message, "@Gothmog besieges Edhellond!", 0x30FFC8),
        (change_screen_map),
      ]),
     ("order_siege_candros",[
        (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_is_active, ":king_party"),
     ],"Order Gothmog to besiege Edoras.",
      [ (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_detach, ":king_party"),
        (party_relocate_near_party, ":king_party", "p_town_edoras", 0),
        (party_set_slot, "p_town_edoras", slot_center_is_besieged_by, ":king_party"),
        (call_script, "script_party_set_ai_state", ":king_party", spai_besieging_center, "p_town_edoras"),
        (party_set_ai_behavior, ":king_party", ai_bhvr_attack_party),
        (party_set_ai_object, ":king_party", "p_town_edoras"),
        (party_set_flags, ":king_party", pf_default_behavior, 1),
        (party_set_slot, ":king_party", slot_party_ai_substate, 1),
        (display_message, "@Gothmog besieges Edoras!", 0x30FFC8),
        (change_screen_map),
      ]),
	("order_siege_pelargir",[
        (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_is_active, ":king_party"),
     ],"Order Gothmog to besiege Pelargir.",
      [ (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_detach, ":king_party"),
        (party_relocate_near_party, ":king_party", "p_town_pelargir", 0),
        (party_set_slot, "p_town_pelargir", slot_center_is_besieged_by, ":king_party"),
        (call_script, "script_party_set_ai_state", ":king_party", spai_besieging_center, "p_town_pelargir"),
        (party_set_ai_behavior, ":king_party", ai_bhvr_attack_party),
        (party_set_ai_object, ":king_party", "p_town_pelargir"),
        (party_set_flags, ":king_party", pf_default_behavior, 1),
        (party_set_slot, ":king_party", slot_party_ai_substate, 1),
        (display_message, "@Gothmog besieges Pelargir!", 0x30FFC8),
        (change_screen_map),
      ]),
     ("order_siege_wemnet",[
        (troop_get_slot, ":king_party", "trp_isengard_lord", slot_troop_leaded_party),
        (party_is_active, ":king_party"),
     ],"Order Saruman to besiege Edoras.",
      [
        (troop_get_slot, ":king_party", "trp_isengard_lord", slot_troop_leaded_party),
        (party_detach, ":king_party"),
        (party_relocate_near_party, ":king_party", "p_town_edoras", 0),
        (party_set_slot, "p_town_edoras", slot_center_is_besieged_by, ":king_party"),
        (call_script, "script_party_set_ai_state", ":king_party", spai_besieging_center, "p_town_edoras"),
        (party_set_ai_behavior, ":king_party", ai_bhvr_attack_party),
        (party_set_ai_object, ":king_party", "p_town_edoras"),
        (party_set_flags, ":king_party", pf_default_behavior, 1),
        (party_set_slot, ":king_party", slot_party_ai_substate, 1),
        (display_message, "@Saruman besieges Edoras!", 0x30FFC8),
        (change_screen_map),
      ]),
     ("order_siege_dale",[
        (troop_get_slot, ":king_party", "trp_rhun_lord", slot_troop_leaded_party),
        (party_is_active, ":king_party"),
     ],"Order Partitava to besiege Dale.",
      [
        (troop_get_slot, ":king_party", "trp_rhun_lord", slot_troop_leaded_party),
        (party_detach, ":king_party"),
        (party_relocate_near_party, ":king_party", "p_town_dale", 0),
        (party_set_slot, "p_town_dale", slot_center_is_besieged_by, ":king_party"),
        (call_script, "script_party_set_ai_state", ":king_party", spai_besieging_center, "p_town_dale"),
        (party_set_ai_behavior, ":king_party", ai_bhvr_attack_party),
        (party_set_ai_object, ":king_party", "p_town_dale"),
        (party_set_flags, ":king_party", pf_default_behavior, 1),
        (party_set_slot, ":king_party", slot_party_ai_substate, 1),
        (display_message, "@Partitava besieges Dale!", 0x30FFC8),
        (change_screen_map),
      ]),
 ] for ct in range(cheat_switch)])+[
     ("back_mtest",[],"Back to main test menu.", [(jump_to_menu, "mnu_camp_mvtest"),]),
    ]
 ),
( "mvtest_order_siege",0,
   "Order {s1} to besiege...",
   "none",
   [(str_store_faction_name, s1, "$ambient_faction"),],
   [("back_sieg",[],"Back to siege menu.", [(jump_to_menu, "mnu_mvtest_sieges"),]),]
  +
  concatenate_scripts([[
  (
	"siege_town",
	[(party_is_active, center_list[y][0]),
     (faction_get_slot, ":king", "$ambient_faction", slot_faction_marshall),
     (troop_get_slot, ":king_party", ":king", slot_troop_leaded_party),
     (party_is_active, ":king_party"),
     (store_faction_of_party, ":town_faction", center_list[y][0]),
     (store_relation, ":reln", ":town_faction", "$ambient_faction"),
	 (lt, ":reln", 0),
     (faction_get_slot, ":faction_theater", "$ambient_faction", slot_faction_active_theater),
     (party_slot_eq, center_list[y][0], slot_center_theater, ":faction_theater"),
     (party_slot_eq, center_list[y][0], slot_center_is_besieged_by, -1),
     (str_store_party_name, s10, center_list[y][0]),],
	"{s10}.",
	[
        #order ambient king to besiege
        (faction_get_slot, ":king", "$ambient_faction", slot_faction_marshall),
        (troop_get_slot, ":king_party", ":king", slot_troop_leaded_party),
        (party_detach, ":king_party"),
        (party_relocate_near_party, ":king_party", center_list[y][0], 0),
        (party_set_slot, center_list[y][0], slot_center_is_besieged_by, ":king_party"),
        (call_script, "script_party_set_ai_state", ":king_party", spai_besieging_center, center_list[y][0]),
        (party_set_ai_behavior, ":king_party", ai_bhvr_attack_party),
        (party_set_ai_object, ":king_party", center_list[y][0]),
        (party_set_flags, ":king_party", pf_default_behavior, 1),
        (party_set_slot, ":king_party", slot_party_ai_substate, 1),
        (str_store_party_name, s10, center_list[y][0]),
		(display_message, "@{s10} besieged!", 0x30FFC8),
        (change_screen_map),
    ]
  )
  ]for y in range(len(center_list)) ])      
 ),
( "mvtest_advcamps",0,
   "Test advance camps",
   "none",
   [], [
 ]+concatenate_scripts([[ 
    ("spawnSW",[],"Spawn SW advance camps", [
	  (try_for_range, ":camp_pointer", "p_camplace_N1", "p_ancient_ruins"), # free up campable place
		  (party_set_slot, ":camp_pointer", slot_camp_place_occupied, 0),
	  (try_end),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        #(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (faction_set_slot, ":faction_no", slot_faction_active_theater, theater_SW),
        (faction_get_slot, ":adv_camp", ":faction_no", slot_faction_advance_camp),
        (try_begin),
          (faction_slot_eq, ":faction_no", slot_faction_home_theater, theater_SW),
          (disable_party, ":adv_camp"),
        (else_try),        
          (call_script, "script_get_advcamp_pos_predefined", ":faction_no"), #fills pos1
          (party_set_position, ":adv_camp", pos1),
          (enable_party, ":adv_camp"),
        (try_end),
      (try_end),
      (display_message, "@SW advance camps spawned around a point northwest of East Emnet!", 0x30FFC8),
    ]),
    ("spawnSE",[],"Spawn SE advance camps", [
	  (try_for_range, ":camp_pointer", "p_camplace_N1", "p_ancient_ruins"), # free up campable place
		  (party_set_slot, ":camp_pointer", slot_camp_place_occupied, 0),
	  (try_end),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        #(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (faction_set_slot, ":faction_no", slot_faction_active_theater, theater_SE),
        (faction_get_slot, ":adv_camp", ":faction_no", slot_faction_advance_camp),
        (try_begin),
          (faction_slot_eq, ":faction_no", slot_faction_home_theater, theater_SE),
          (disable_party, ":adv_camp"),
        (else_try),        
          (call_script, "script_get_advcamp_pos_predefined", ":faction_no"), #fills pos1
          (party_set_position, ":adv_camp", pos1),
          (enable_party, ":adv_camp"),
        (try_end),
      (try_end),
      (display_message, "@SE advance camps spawned around a point west of West Osgiliath!", 0x30FFC8),
    ]),
    ("spawnC",[],"Spawn C advance camps", [
	  (try_for_range, ":camp_pointer", "p_camplace_N1", "p_ancient_ruins"), # free up campable place
		  (party_set_slot, ":camp_pointer", slot_camp_place_occupied, 0),
	  (try_end),
	  (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        #(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (faction_set_slot, ":faction_no", slot_faction_active_theater, theater_C),
        (faction_get_slot, ":adv_camp", ":faction_no", slot_faction_advance_camp),
        (try_begin),
          (faction_slot_eq, ":faction_no", slot_faction_home_theater, theater_C),
          (disable_party, ":adv_camp"),
        (else_try),        
          (call_script, "script_get_advcamp_pos_predefined", ":faction_no"), #fills pos1
          (party_set_position, ":adv_camp", pos1),
          (enable_party, ":adv_camp"),
        (try_end),
      (try_end),
      (display_message, "@C advance camps spawned around Cerin Amroth!", 0x30FFC8),
    ]),
    ("spawnN",[],"Spawn N advance camps", [
	  (try_for_range, ":camp_pointer", "p_camplace_N1", "p_ancient_ruins"), # free up campable place
		  (party_set_slot, ":camp_pointer", slot_camp_place_occupied, 0),
	  (try_end),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        #(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (faction_set_slot, ":faction_no", slot_faction_active_theater, theater_N),
        (faction_get_slot, ":adv_camp", ":faction_no", slot_faction_advance_camp),
        (try_begin),
          (faction_slot_eq, ":faction_no", slot_faction_home_theater, theater_N),
          (disable_party, ":adv_camp"),
        (else_try),        
          (call_script, "script_get_advcamp_pos_predefined", ":faction_no"), #fills pos1
          (party_set_position, ":adv_camp", pos1),
          (enable_party, ":adv_camp"),
        (try_end),
      (try_end),
      (display_message, "@N advance camps spawned around Beorn's House!", 0x30FFC8),
    ]),
    ("disable",[],"Remove all advance camps", [
	  (try_for_range, ":camp_pointer", "p_camplace_N1", "p_ancient_ruins"), # free up campable place
		(party_set_slot, ":camp_pointer", slot_camp_place_occupied, 0),
	  (try_end),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        #(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        
        (faction_get_slot, ":home_theater", ":faction_no", slot_faction_home_theater),
        (faction_set_slot, ":faction_no", slot_faction_active_theater, ":home_theater"),
        (faction_get_slot, ":adv_camp", ":faction_no", slot_faction_advance_camp),
        (disable_party, ":adv_camp"),
      (try_end),
      (call_script, "script_update_active_theaters"),
      (display_message, "@Advance camps disabled, theaters restored!", 0x30FFC8),
    ]),
    ("movespawnSW",[],"Move SW theater center and spawn camps there", [
      (party_get_position, pos13, "p_main_party"),
      (party_set_position, "p_theater_sw_center", pos13),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        #(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (faction_set_slot, ":faction_no", slot_faction_active_theater, theater_SW),
        (faction_get_slot, ":adv_camp", ":faction_no", slot_faction_advance_camp),
        (try_begin),
          (faction_slot_eq, ":faction_no", slot_faction_home_theater, theater_SW),
          (disable_party, ":adv_camp"),
		  (try_for_range, ":camp_pointer", "p_camplace_N1", "p_ancient_ruins"), # free up campable place
		      (store_distance_to_party_from_party,":dist", ":adv_camp", ":camp_pointer"),
		      (le, ":dist",1),
		      (party_set_slot, ":camp_pointer", slot_camp_place_occupied, 0),
		  (try_end),
        (else_try),        
          (call_script, "script_get_advcamp_pos_predefined", ":faction_no"), #fills pos1
          (party_set_position, ":adv_camp", pos1),
          (enable_party, ":adv_camp"),
        (try_end),
      (try_end),
      (set_fixed_point_multiplier, 1000),
      (position_get_x, reg2, pos13),
      (position_get_y, reg3, pos13),
      (display_message, "@SW advance camps spawned around {reg2},{reg3}!", 0x30FFC8),
    ]),
    ("movespawnSE",[],"Move SE theater center and spawn camps there", [
      (party_get_position, pos13, "p_main_party"),
      (party_set_position, "p_theater_se_center", pos13),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        #(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (faction_set_slot, ":faction_no", slot_faction_active_theater, theater_SE),
        (faction_get_slot, ":adv_camp", ":faction_no", slot_faction_advance_camp),
        (try_begin),
          (faction_slot_eq, ":faction_no", slot_faction_home_theater, theater_SE),
          (disable_party, ":adv_camp"),
		  (try_for_range, ":camp_pointer", "p_camplace_N1", "p_ancient_ruins"), # free up campable place
		      (store_distance_to_party_from_party,":dist", ":adv_camp", ":camp_pointer"),
		      (le, ":dist",1),
		      (party_set_slot, ":camp_pointer", slot_camp_place_occupied, 0),
		  (try_end),
        (else_try),        
          (call_script, "script_get_advcamp_pos_predefined", ":faction_no"), #fills pos1
          (party_set_position, ":adv_camp", pos1),
          (enable_party, ":adv_camp"),
        (try_end),
      (try_end),
      (set_fixed_point_multiplier, 1000),
      (position_get_x, reg2, pos13),
      (position_get_y, reg3, pos13),
      (display_message, "@SE advance camps spawned around {reg2},{reg3}!", 0x30FFC8),
    ]),
    ("movespawnC",[],"Move C theater center and spawn camps there", [
      (party_get_position, pos13, "p_main_party"),
      (party_set_position, "p_theater_c_center", pos13),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        #(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (faction_set_slot, ":faction_no", slot_faction_active_theater, theater_C),
        (faction_get_slot, ":adv_camp", ":faction_no", slot_faction_advance_camp),
        (try_begin),
          (faction_slot_eq, ":faction_no", slot_faction_home_theater, theater_C),
          (disable_party, ":adv_camp"),
		  (try_for_range, ":camp_pointer", "p_camplace_N1", "p_ancient_ruins"), # free up campable place
		      (store_distance_to_party_from_party,":dist", ":adv_camp", ":camp_pointer"),
		      (le, ":dist",1),
		      (party_set_slot, ":camp_pointer", slot_camp_place_occupied, 0),
		  (try_end),
        (else_try),        
          (call_script, "script_get_advcamp_pos_predefined", ":faction_no"), #fills pos1
          (party_set_position, ":adv_camp", pos1),
          (enable_party, ":adv_camp"),
        (try_end),
      (try_end),
      (set_fixed_point_multiplier, 1000),
      (position_get_x, reg2, pos13),
      (position_get_y, reg3, pos13),
      (display_message, "@C advance camps spawned around {reg2},{reg3}!", 0x30FFC8),
    ]),
    ("movespawnN",[],"Move N theater center and spawn camps there", [
      (party_get_position, pos13, "p_main_party"),
      (party_set_position, "p_theater_n_center", pos13),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        #(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (faction_set_slot, ":faction_no", slot_faction_active_theater, theater_N),
        (faction_get_slot, ":adv_camp", ":faction_no", slot_faction_advance_camp),
        (try_begin),
          (faction_slot_eq, ":faction_no", slot_faction_home_theater, theater_N),
          (disable_party, ":adv_camp"),
		  (try_for_range, ":camp_pointer", "p_camplace_N1", "p_ancient_ruins"), # free up campable place
		      (store_distance_to_party_from_party,":dist", ":adv_camp", ":camp_pointer"),
		      (le, ":dist",1),
		      (party_set_slot, ":camp_pointer", slot_camp_place_occupied, 0),
		  (try_end),
        (else_try),        
          (call_script, "script_get_advcamp_pos_predefined", ":faction_no"), #fills pos1
          (party_set_position, ":adv_camp", pos1),
          (enable_party, ":adv_camp"),
        (try_end),
      (try_end),
      (set_fixed_point_multiplier, 1000),
      (position_get_x, reg2, pos13),
      (position_get_y, reg3, pos13),
      (display_message, "@N advance camps spawned around {reg2},{reg3}!", 0x30FFC8),
    ]),
 ] for ct in range(cheat_switch)])+[
    ("continue",[],"Continue...", [(jump_to_menu, "mnu_camp_mvtest"),]),
    ]
  ),
( "mvtest_cutscenes",0,
   "Choose an option:",
   "none",
   [],
    [("intro",[], "Play intro.", [(jump_to_menu, "mnu_auto_intro_rohan"),]),
     ("joke",[],  "Play GA joke.", [(jump_to_menu, "mnu_auto_intro_joke"),]),
 ]+concatenate_scripts([[ 
     #("test",[],  "Play Gandalf test encounter.", [(jump_to_menu, "mnu_auto_convo"),]),
     ("gandalf_1",[], "Play Gandalf advice.", [(call_script, "script_start_conversation_cutscene", tld_cc_gandalf_advice),]),
     ("gandalf_2",[], "Play Gandalf ally down.", [(assign, "$g_tld_convo_subject", "fac_dale"),(call_script, "script_start_conversation_cutscene", tld_cc_gandalf_ally_down),]),
     ("gandalf_3",[], "Play Gandalf enemy down.", [(assign, "$g_tld_convo_subject", "fac_gundabad"),(call_script, "script_start_conversation_cutscene", tld_cc_gandalf_enemy_down),]),
     ("gandalf_4",[], "Play Gandalf victory.", [(call_script, "script_start_conversation_cutscene", tld_cc_gandalf_victory),]),
     ("nazgul_1",[], "Play Nazgul Baggins.", [(call_script, "script_start_conversation_cutscene", tld_cc_nazgul_baggins),]),
     ("nazgul_2",[], "Play Nazgul evil war.", [(call_script, "script_start_conversation_cutscene", tld_cc_nazgul_evil_war),]),
     ("nazgul_3",[], "Play Nazgul victory.", [(call_script, "script_start_conversation_cutscene", tld_cc_nazgul_victory),]),
     ("scenetest",[], "Enter conversation scene.", [
                                (modify_visitors_at_site,"scn_conversation_scene"),(reset_visitors),
                                (set_visitor,0,"trp_player"),
                                (set_visitor,1,"trp_gandalf"),
                                (set_jump_mission,"mt_test_gandalf"),
                                (jump_to_scene,"scn_conversation_scene"),
                                (change_screen_mission),
                                ]),
     ("partytest",[], "Create a Gandalf party following you.", [
                                (set_spawn_radius, 5),
                                (spawn_around_party, "p_main_party", "pt_gandalf"),
                                (assign, ":party", reg0),
                                (party_set_ai_behavior, ":party", ai_bhvr_attack_party),
                                (party_set_ai_object, ":party", "p_main_party"),
                                (party_set_flags, ":party", pf_default_behavior, 0),
                                (party_set_slot, ":party", slot_party_ai_state, spai_undefined),
                                (troop_set_slot, "trp_gandalf", slot_troop_leaded_party, ":party"),
                                (assign, "$g_tld_gandalf_state", tld_cc_gandalf_advice),
                                (display_message, "@Gandalf would like to have a little chat!", 0x30FFC8),
                                ]),
 ] for ct in range(cheat_switch)])+[
     ("back_mtest",[],"Back to main test menu.", [(jump_to_menu, "mnu_camp_mvtest"),]),
    ]
 ),
## MadVader test end
( "game_options",0,
	"^^^^^^^^Click on an option to toggle:","none",[],
    [
    ("game_options_restrict_items",[(try_begin),(eq,"$tld_option_crossdressing",0),(str_store_string, s7, "@ON"),
									(else_try),(str_store_string, s7, "@OFF (cheat)"),(try_end),
        ],"Restricted player equipment:  {s7}",[
        (store_sub, "$tld_option_crossdressing", 1, "$tld_option_crossdressing"),(val_clamp, "$tld_option_crossdressing", 0, 2)]),

    ("game_options_formations",[(try_begin),(neq, "$tld_option_formations", 0),(str_store_string, s7, "@ON"),
								(else_try),(str_store_string, s7, "@OFF"),(try_end),
        ],"Battle formations and AI:  {s7}",[
        (store_sub, "$tld_option_formations", 1, "$tld_option_formations"),(val_clamp, "$tld_option_formations", 0, 2)]),

	("game_options_town_menu",[(try_begin),(eq, "$tld_option_town_menu_hidden", 0),(str_store_string, s7, "@ON"),
								 (else_try),(str_store_string, s7, "@OFF"),(try_end),
	    ],"Town NPCs always accessible from Menus:  {s7}",[
	    (store_sub,"$tld_option_town_menu_hidden",1,"$tld_option_town_menu_hidden"),(val_clamp,"$tld_option_town_menu_hidden",0,2)]),

	("game_options_cutscenes",[(try_begin),(neq, "$tld_option_cutscenes", 0),(str_store_string, s7, "@ON"),
								 (else_try),(str_store_string, s7, "@OFF"),(try_end),
	    ],"Cutscenes:  {s7}",[
	    (store_sub,"$tld_option_cutscenes",1,"$tld_option_cutscenes"),(val_clamp, "$tld_option_cutscenes",0,2)]),

	("game_options_injuries",[(try_begin),(neq, "$tld_option_injuries", 0),(str_store_string, s7, "@ON"),
                                  (else_try),(str_store_string, s7, "@OFF"),(try_end),
	    ],"Injuries for companions:  {s7}.",[
		(store_sub,"$tld_option_injuries",1,"$tld_option_injuries"),(val_clamp,"$tld_option_injuries",0,2)]),
 
	("game_options_death",[(try_begin),(neq, "$tld_option_death_npc", 0),(str_store_string, s7, "@ON"),
							(else_try),(str_store_string, s7, "@OFF"),(try_end),
	    ],"Permanent death for lords and companions:  {s7}.",[
	     (store_sub, "$tld_option_death_npc", 1, "$tld_option_death_npc"),(val_clamp, "$tld_option_death_npc", 0, 2)]),

	("game_options_death2",[(try_begin),(neq, "$tld_option_death_player", 0),(str_store_string, s7, "@ON"),
							(else_try),(str_store_string, s7, "@OFF"),(try_end),
	    ],"Permanent death for player (that is YOU!):  {s7}.",[
	     (store_sub, "$tld_option_death_player", 1, "$tld_option_death_player"),(val_clamp, "$tld_option_death_player", 0, 2)]),

    ("game_options_morale",[(try_begin),(eq,"$tld_option_morale",1),(str_store_string, s7, "@ON"),
									(else_try),(str_store_string, s7, "@OFF"),(try_end),
        ],"Battle morale system:  {s7}",[
        (store_sub, "$tld_option_morale", 1, "$tld_option_morale"),(val_clamp, "$tld_option_morale", 0, 2)]),

    ("game_options_animal_ambushes",[(try_begin),(eq,"$tld_option_animal_ambushes",1),(str_store_string, s7, "@ON"),
									(else_try),(str_store_string, s7, "@OFF"),(try_end),
        ],"Animal ambushes:  {s7}",[
        (store_sub, "$tld_option_animal_ambushes", 1, "$tld_option_animal_ambushes"),(val_clamp, "$tld_option_animal_ambushes", 0, 2)]),

    ("game_options_tweaks",[],"Gameplay tweaks...",[(jump_to_menu, "mnu_camp_tweaks")]),

    ("game_options_back",[],"Back to camp menu.",[(jump_to_menu, "mnu_camp")]),
 ]),

( "camp_tweaks",0,
	"^^^^^^^^Choose an option that you would like to adjust.","none",[],
	[
   	 	("tweak_options_compat",[],"Compatibility tweaks...",[(jump_to_menu, "mnu_camp_compat_tweaks")]),
    		("tweak_options_strat",[],"Strategy tweaks...",[(jump_to_menu, "mnu_camp_strat_tweaks")]),
    		("tweak_options_back",[],"Back to options menu.",[(jump_to_menu, "mnu_game_options")]),
	]
),

( "camp_compat_tweaks",0,
	"^^^^^^^^Click on an option to change (hold shift to decrease):^(these are for compatibilty and are not cheats)","none",[],
	[	
    		("game_options_compat_party",
		[
			(assign, reg0, "$tld_option_max_parties"),
			(try_begin),
				(ge, "$tld_option_max_parties", tld_party_count_option_high_crash),
				(str_store_string, s1, "@{reg0} (will most likely cause save crashes)"),
			(else_try),
				(ge, "$tld_option_max_parties", tld_party_count_option_med_crash),
				(str_store_string, s1, "@{reg0} (could possibly cause save crashes)"),
			(else_try),
				(str_store_string, s1, "@{reg0}"),
			(try_end),
		],

		"Maximum number of parties: {s1}",
		[
			(try_begin),
				(key_is_down|this_or_next, key_left_shift),
				(key_is_down, key_right_shift),
				(val_sub, "$tld_option_max_parties", tld_party_count_option_increment),
				(try_begin),
					(lt, "$tld_option_max_parties", tld_party_count_option_min),
					(assign, "$tld_option_max_parties", tld_party_count_option_max),
				(try_end),
			(else_try),
				(val_add, "$tld_option_max_parties", tld_party_count_option_increment),
				(try_begin),
					(gt, "$tld_option_max_parties", tld_party_count_option_max),
					(assign, "$tld_option_max_parties", tld_party_count_option_min),
				(try_end),
			(try_end),
		]),

    		("game_options_compat_back",[],"Back to tweaks menu.",[(jump_to_menu, "mnu_camp_tweaks")]),
	]
),

( "camp_strat_tweaks",0,
	"^^^^^^^^Click on an option to toggle:^(warning: these are cheats!)","none",[],
    [
    ("strat_tweaks_siege_reqs",[
      (try_begin),
        (eq,"$tld_option_siege_reqs",0),(str_store_string, s7, "@Normal"),
	  (else_try),
        (eq,"$tld_option_siege_reqs",1),(str_store_string, s7, "@Defender only"),
	  (else_try),
        (str_store_string, s7, "@None"),
      (try_end),
        ],"Siege strength requirements: {s7}",[
        (val_add, "$tld_option_siege_reqs", 1),
        (val_mod, "$tld_option_siege_reqs", 3),]), #0-2

    ("strat_tweaks_siege_relax_rate",[
      (val_max, "$tld_option_siege_relax_rate", 50), #deals with old saves
      (assign, reg1, "$tld_option_siege_relax_rate"),
        ],"Siege str. req. relaxation rate: {reg1}",[
        (val_mul, "$tld_option_siege_relax_rate", 2),
        (try_begin),
          (eq, "$tld_option_siege_relax_rate", 400),
          (assign, "$tld_option_siege_relax_rate", 50),
        (try_end),]), #50, 100, 200
        
    ("strat_tweaks_regen_rate",[
      (try_begin),
        (eq,"$tld_option_regen_rate",0),(str_store_string, s7, "@Normal"),
	  (else_try),
        (eq,"$tld_option_regen_rate",1),(str_store_string, s7, "@Halved"),
	  (else_try),
        (eq,"$tld_option_regen_rate",2),(str_store_string, s7, "@Battles only"),
	  (else_try),
        (str_store_string, s7, "@None"),
      (try_end),
        ],"Strength regen rate: {s7}",[
        (val_add, "$tld_option_regen_rate", 1),
        (val_mod, "$tld_option_regen_rate", 4),]), #0,1,2,3
        
    ("strat_tweaks_siege_regen_limit",[
      (val_max, "$tld_option_regen_limit", 500), #deals with old saves
      (assign, reg1, "$tld_option_regen_limit"),
        ],"Factions don't regen below: {reg1}",[
        (val_add, "$tld_option_regen_limit", 500),
        (try_begin),
          (eq, "$tld_option_regen_limit", 2500),
          (assign, "$tld_option_regen_limit", 500),
        (try_end),]), #500/1000/1500/2000

    #swy-- added these two by per khamukkamu request, they make sense:
    ("strat_tweaks_influence_gain_rate",
      [
        (try_begin),
          (eq, "$tld_option_influence_gain_rate", 0),
          (str_store_string, s7, "@Normal"),
        (else_try),
          (eq, "$tld_option_influence_gain_rate", 1),
          (str_store_string, s7, "@Doubled"),
        (else_try),
          (eq, "$tld_option_influence_gain_rate", 2),
          (str_store_string, s7, "@Tripled"),
        (else_try),
          (eq, "$tld_option_influence_gain_rate", 3),
          (str_store_string, s7, "@Quadrupled"),
        (try_end),
      ],
      "Influence gain rate: {s7}",
      [
        (val_add, "$tld_option_influence_gain_rate", 1),
        (val_mod, "$tld_option_influence_gain_rate", 4),
      ]
    ), #0,1,2,3

    ("strat_tweaks_rank_gain_rate",
      [
        (try_begin),
          (eq, "$tld_option_rank_gain_rate", 0),
          (str_store_string, s7, "@Normal"),
        (else_try),
          (eq, "$tld_option_rank_gain_rate", 1),
          (str_store_string, s7, "@Doubled"),
        (else_try),
          (eq, "$tld_option_rank_gain_rate", 2),
          (str_store_string, s7, "@Tripled"),
        (else_try),
          (eq, "$tld_option_rank_gain_rate", 3),
          (str_store_string, s7, "@Quadrupled"),
        (try_end),
      ],
      "Rank gain rate: {s7}",
      [
        (val_add, "$tld_option_rank_gain_rate", 1),
        (val_mod, "$tld_option_rank_gain_rate", 4),
      ]
    ), #0,1,2,3

    ("strat_tweaks_back",[],"Back to tweaks menu.",[(jump_to_menu, "mnu_camp_tweaks")]),
 ]),

 
#-swy- Nothing leads to this menu, not even with cheats/dev thingie on, probably disabled for a good reason.
( "camp_chest_fill",0,
 "^^^^^^^^Please choose faction to get items from.",
 "none",
 [],
 [
 ]+concatenate_scripts([[  
 ("f_gondor"  ,[],"Gondor items"    ,[(call_script,"script_fill_camp_chests","fac_gondor"  ),(jump_to_menu, "mnu_camp"),]),
  ("f_rohan"   ,[],"Rohan items"     ,[(call_script,"script_fill_camp_chests","fac_rohan"   ),(jump_to_menu, "mnu_camp"),]),
  ("f_isengard",[],"Isengard items"  ,[(call_script,"script_fill_camp_chests","fac_isengard"),(jump_to_menu, "mnu_camp"),]),
  ("f_mordor"  ,[],"Mordor items"    ,[(call_script,"script_fill_camp_chests","fac_mordor"  ),(jump_to_menu, "mnu_camp"),]),
  ("f_dwarf"   ,[],"Dwarf items"     ,[(call_script,"script_fill_camp_chests","fac_dwarf"   ),(jump_to_menu, "mnu_camp"),]),
  ("f_lorien"  ,[],"Lothlorien items",[(call_script,"script_fill_camp_chests","fac_lorien"  ),(jump_to_menu, "mnu_camp"),]),
  ("f_woodelf" ,[],"Mirkwood items"  ,[(call_script,"script_fill_camp_chests","fac_woodelf" ),(jump_to_menu, "mnu_camp"),]),
  ("f_imladris",[],"Imladris items"  ,[(call_script,"script_fill_camp_chests","fac_imladris"),(jump_to_menu, "mnu_camp"),]),	   
  ("f_harad"   ,[],"Harad items"     ,[(call_script,"script_fill_camp_chests","fac_harad"   ),(jump_to_menu, "mnu_camp"),]),
  ("f_khand"   ,[],"Khand items"     ,[(call_script,"script_fill_camp_chests","fac_khand"   ),(jump_to_menu, "mnu_camp"),]),
  ("f_rhun"    ,[],"Rhun items"      ,[(call_script,"script_fill_camp_chests","fac_rhun"    ),(jump_to_menu, "mnu_camp"),]),	   
  ("f_dale"    ,[],"Dale items"      ,[(call_script,"script_fill_camp_chests","fac_dale"    ),(jump_to_menu, "mnu_camp"),]),
  ("f_umbar"   ,[],"Umbar items"     ,[(call_script,"script_fill_camp_chests","fac_umbar"   ),(jump_to_menu, "mnu_camp"),]),
  ("f_moria"   ,[],"Moria items"     ,[(call_script,"script_fill_camp_chests","fac_moria"   ),(jump_to_menu, "mnu_camp"),]),
  ("f_gundabad",[],"Gundabad items"  ,[(call_script,"script_fill_camp_chests","fac_gundabad"),(jump_to_menu, "mnu_camp"),]),
  ("f_dunland" ,[],"Dunland items"   ,[(call_script,"script_fill_camp_chests","fac_dunland" ),(jump_to_menu, "mnu_camp"),]),
 ] for ct in range(cheat_switch)])+[  
  ("go_back"   ,[],"Go back"         ,[(jump_to_menu, "mnu_camp"),]),
 ]
 ),
( "cheat_change_race",0,
 "^^^^^Please choose your race:^^Note: You should review your character in the face generator after making this change.",
 "none",
 [],
 [
 ]+concatenate_scripts([[ 
 ("race_test     " ,[],"TEST     " ,[(troop_set_type,"trp_player",16), (jump_to_menu, "mnu_camp"),]),	   
  ("race_male"      ,[],"Male"      ,[(troop_set_type,"trp_player", 0), (jump_to_menu, "mnu_camp"),]),
  ("race_female"    ,[],"Female"    ,[(troop_set_type,"trp_player", 1), (jump_to_menu,"mnu_camp"),]),
  ("race_gondor"    ,[],"Gondor"    ,[(troop_set_type,"trp_player", 2), (assign,"$players_kingdom","fac_gondor"),(jump_to_menu, "mnu_camp"),]),
  ("race_rohan"     ,[],"Rohan"     ,[(troop_set_type,"trp_player", 3), (assign,"$players_kingdom","fac_rohan"),(jump_to_menu, "mnu_camp"),]),
  ("race_dunlander" ,[],"Dunlander" ,[(troop_set_type,"trp_player", 4), (assign,"$players_kingdom","fac_dunland"),(jump_to_menu, "mnu_camp"),]),
  ("race_orc"       ,[],"Orc"       ,[(troop_set_type,"trp_player", 5), (jump_to_menu, "mnu_camp"),]),
  ("race_uruk"      ,[],"Uruk"      ,[(troop_set_type,"trp_player", 6), (jump_to_menu, "mnu_camp"),]),
  ("race_haradrim"  ,[],"Haradrim"  ,[(troop_set_type,"trp_player", 7), (jump_to_menu, "mnu_camp"),]),	   
  ("race_easterling",[],"Easterling",[(troop_set_type,"trp_player", 8), (jump_to_menu, "mnu_camp"),]),
  ("race_dwarf"     ,[],"Dwarf"     ,[(troop_set_type,"trp_player", 9), (jump_to_menu, "mnu_camp"),]),
  ("race_troll"     ,[],"Troll"     ,[(troop_set_type,"trp_player",10), (jump_to_menu, "mnu_camp"),]),	   
  ("race_dunedain"  ,[],"Dunedain"  ,[(troop_set_type,"trp_player",11), (jump_to_menu, "mnu_camp"),]),
  ("race_lothlorien",[],"Lothlorien",[(troop_set_type,"trp_player",12), (jump_to_menu, "mnu_camp"),]),
  ("race_rivendell" ,[],"Rivendell" ,[(troop_set_type,"trp_player",13), (jump_to_menu, "mnu_camp"),]),
  ("race_mirkwood"  ,[],"Mirkwood"  ,[(troop_set_type,"trp_player",14), (jump_to_menu, "mnu_camp"),]),
  ("race_evil_male" ,[],"Evil Male" ,[(troop_set_type,"trp_player",15), (jump_to_menu, "mnu_camp"),]),
 ] for ct in range(cheat_switch)])+[
  ("go_back"        ,[],"Go back"   ,[(jump_to_menu, "mnu_camp_cheat"),]),
 ]),  
 
("camp_action",0,
  "^^^^^^^^^     Which object?", "none",
 [(set_background_mesh, "mesh_ui_default_menu_window"),],
 [ 

    ("camp_customize_defilement",
		[
			# (CppCoder) Only evil players can do this, though only evil players should be able to aqquire the items anyway.
			(eq, cheat_switch, 1),
			(neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
			(troop_has_item_equipped|this_or_next, "trp_player", "itm_defiled_armor_gondor"),
			(troop_has_item_equipped|this_or_next, "trp_player", "itm_defiled_armor_rohan"),
			(troop_has_item_equipped, "trp_player", "itm_defiled_armor_dale"),
		],
		"Customize Defiled Armor",
		[			
			(try_for_range, ":item_id", defiled_items_begin, defiled_items_end),
				(troop_has_item_equipped, "trp_player", ":item_id"), # (CppCoder) Must be done for efficiency's sake
				(assign, "$g_defiled_armor_item", ":item_id"),
			(try_end),
			(start_presentation, "prsnt_customize_defilement"),
		]
	),

    ("camp_drink_water",
		[
			(player_has_item,"itm_ent_water"),
			(eq,"$g_ent_water_ever_drunk",0), # can drink only if never before
		],
		"Drink the Ent Water!",
		[
	    (troop_get_type,reg5,"trp_player"),
	    (troop_remove_item,"itm_ent_water"),
		(display_log_message,"@You drank the Ent Water..."),
		(assign,"$g_ent_water_ever_drunk",1),
		(assign,"$g_ent_water_taking_effect",1),
		(try_begin),
			(neg|is_between,reg5,tf_orc_begin, tf_orc_end),
			(jump_to_menu,"mnu_drank_ent_water_human"),
		(else_try),
			(jump_to_menu,"mnu_drank_ent_water_orc"),
		(try_end),
		]
	),


    # ("camp_recruit_prisoners",
       # [(troops_can_join, 1),
        # (store_current_hours, ":cur_time"),
        # (val_sub, ":cur_time", 24),
        # (gt, ":cur_time", "$g_prisoner_recruit_last_time"),
        # (try_begin),
          # (gt, "$g_prisoner_recruit_last_time", 0),
          # (assign, "$g_prisoner_recruit_troop_id", 0),
          # (assign, "$g_prisoner_recruit_size", 0),
          # (assign, "$g_prisoner_recruit_last_time", 0),
        # (try_end),
        # ], "Recruit some of your prisoners to your party.",[(jump_to_menu, "mnu_camp_recruit_prisoners"),],
	# ),
	
    #("action_read_book",[],"Select a book to read.",[(jump_to_menu, "mnu_camp_action_read_book"),]),
	
    #("action_modify_banner",[(eq, "$cheat_mode", 1)],"Cheat: Modify your banner.",
    #                                               [(start_presentation, "prsnt_banner_selection"), #(start_presentation, "prsnt_custom_banner"),
    #                                                ]),
    #("action_retire",[],"Retire from adventuring.",[(jump_to_menu, "mnu_retirement_verify"),]),
	
    ("camp_action_4",[],"Back.",[(jump_to_menu, "mnu_camp"),]),
   ]
 ),
################################ CHEAT/MODDING MENU END ########################################  

##     #TLD - assasination menus begin (Kolba)
( "assasins_attack_player_won",mnf_disable_all_keys,
    "You have successfully defeated assassins from {s2}, sent by {s3}.",
    "none",
    [#add prize
		#(call_script,"script_troop_add_gold","trp_player",100),#add gold
        (call_script, "script_add_faction_rps", "$ambient_faction", 100),
		(add_xp_to_troop,1000,"trp_player"),#add exp
		
		(troop_get_slot,":faction","trp_temp_array_a",0),#get number of enemy faction, which organised assasination
		(str_store_faction_name,s2,":faction"),#save faction name
		(faction_get_slot,":leader",":faction",slot_faction_leader),#get faction leader
		(str_store_troop_name,s3,":leader"),#save faction leader name
		],
    [("continue",[],"Continue...",[(leave_encounter),(change_screen_return)])],
 ),
( "assasins_attack_player_retreat",mnf_disable_all_keys,
  "You escaped with your life!",
    "none",
    [#add here any consequences of retreat
	],
    [("continue",[],"Continue...",[(leave_encounter),(change_screen_return)])],
 ),
# what is this? a cut and paste version of defeat? plase merge code rather than cutting and pasting. --- mtarini
( "assasins_attack_player_defeated",0,
    "You should not be reading this...",
    "none",
    [	# (troop_get_type, ":is_female", "trp_player"),
		# (try_begin),
			# (eq, ":is_female", 1),
			# (set_background_mesh, "mesh_pic_prisoner_fem"),
		# (else_try),
			# (set_background_mesh, "mesh_pic_prisoner_man"),
		# (try_end),
		
		#consequences of defeat
		(play_track,"track_captured",1),#music
		
		(troop_get_slot,":faction","trp_temp_array_a",0),#get number of assasin's faction
		(str_store_faction_name,s2,":faction"),#save it
		(faction_get_slot,":leader",":faction",slot_faction_leader),#get faction leader
		(str_store_troop_name,s3,":leader"),#save it
		
		(assign,"$capturer_party",1),
		
		#(troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
		(assign,":end",centers_end),#breaking control flow
		(try_for_range,":center",centers_begin,":end"),
            (party_is_active, ":center"), #TLD
	        (party_slot_eq, ":center", slot_center_destroyed, 0), #TLD
			(party_get_slot,":owner",":center",slot_town_lord),
			(eq,":owner",":leader"),
			(assign,"$capturer_party",":center"),#prison for player
			(assign,":end",centers_begin),#ending control flow
		(try_end),
		
		#freeing player's prisoners
		(party_get_num_prisoner_stacks,":num_prisoner_stacks","p_main_party"),
		(try_for_range,":stack_no",0,":num_prisoner_stacks"),
			(party_prisoner_stack_get_troop_id, ":stack_troop","p_main_party",":stack_no"),
			(troop_is_hero,":stack_troop"),
			(call_script,"script_remove_troop_from_prison",":stack_troop"),
		(try_end),
		
		(call_script,"script_loot_player_items","$g_enemy_party"),#player loose some equipment
		
		(assign,"$g_move_heroes",0),
		(party_clear, "p_temp_party"),
		
		(store_faction_of_party, ":fac","$g_enemy_party"),
		(party_set_faction, "p_temp_party", ":fac"), # mtarini: need this 
		
		(call_script, "script_party_add_party_prisoners", "p_temp_party", "p_main_party"),
		(call_script, "script_party_prisoners_add_party_companions", "p_temp_party", "p_main_party"),
		(distribute_party_among_party_group, "p_temp_party","$capturer_party"),
		
		(call_script,"script_party_remove_all_companions","p_main_party"),#removing all troops
		(assign, "$g_move_heroes",1),
		(call_script,"script_party_remove_all_prisoners","p_main_party"),#removing all prisoners
		
		#setting captivity
		(assign,"$g_player_is_captive",1),
		(assign,"$auto_menu",-1),
		

		#(set_camera_follow_party,"$capturer_party"),#camera
		#(store_random_in_range,":random_hours",30,60),#random time of captivity
		#(call_script,"script_event_player_captured_as_prisoner"),
		#(call_script,"script_stay_captive_for_hours",":random_hours"),
		#(assign,"$auto_menu","mnu_assasins_attack_captivity_check"),
		
		(assign, "$recover_after_death_menu", "mnu_recover_after_death_default"),
		(jump_to_menu, "mnu_tld_player_defeated"),
		
		],
    [
      # ("continue",[],"Continue...",[(leave_encounter),(change_screen_return)]),
    ],
  ),
#TLD - assasination menus end (Kolba)
 
################################ FANGORN MENU START ########################################
( "fangorn_danger",0, # player face fangor dangers
   "^^^^^^Strange, threatening noises all around you.^Are the trees talking? There's a sense of deep anger and pain in the air.^Your orders?",
   "none",
   [(store_add, reg10, "$player_looks_like_an_orc", "mesh_draw_fangorn"), (set_background_mesh, reg10),
    (troop_get_type,reg5,"trp_player"),
    
    #swy-- added unused merlkir illustration here... it looks cool!
    (eq, "$player_looks_like_an_orc", 1),
    (set_background_mesh, "mesh_draw_lorien_magic"),

    ],
   [("be_quiet_elf",
	 [(is_between,reg5,tf_elf_begin, tf_elf_end)], "Respect the hatred of the trees. Move along quietly.",
	 [(assign,"$g_fangorn_rope_pulled", -100), # disable fangorn menu from now on
	  (change_screen_map),
	 ]),
   ("be_quiet",
	 [(neg|is_between,reg5,tf_orc_begin, tf_orc_end),# no orc can do this
	  (neg|is_between,reg5,tf_elf_begin, tf_elf_end) # no elf can do this
	 ],
	 "Put the weapons down and stay quiet! Now out of here!",
	 [(val_add,"$g_fangorn_rope_pulled", 5), 
	  (val_clamp,"$g_fangorn_rope_pulled", 0,65), 
	  (call_script,"script_fangorn_deal_damage","p_main_party"),
	  (call_script,"script_after_fangorn_damage_to_player"),
	 ]
    ),
   ("be_bold",
	 [(neg|is_between,reg5,tf_elf_begin, tf_elf_end)], # no elf can do this
	 "Go on! I'm not afraid of plants or old myths!",
	 [(val_add,"$g_fangorn_rope_pulled", 30), 
	  (val_clamp,"$g_fangorn_rope_pulled", 0,75), 
	  (call_script,"script_fangorn_deal_damage","p_main_party"),
	  (call_script,"script_after_fangorn_damage_to_player"),
	 ]),
   ("fight_back",
	 [
	 (this_or_next|is_between,reg5,tf_orc_begin, tf_orc_end) ,# orcs olny option
	 (check_quest_active, "qst_investigate_fangorn"), #  or also whoever was given the quest to investigate can...
	 ]
	 ,"Let's find out! Search the area! Burn down a tree or two!",
	 [(store_random_in_range,":chance",0,100),
	  (try_begin),
	    (lt,":chance",60),
		(call_script,"script_fangorn_fight_ents"),
		(store_random_in_range, ":scene_to_use", "scn_forest_fangorn1", "scn_forest_ithilien1"),       
		#(assign,"$g_fangorn_rope_pulled", 0), # ents calm down after a good fight
		(val_max,"$g_fangorn_rope_pulled", 21), # this also means ents gets a max reinforcement of at least 3 
		(assign, "$g_encountered_party", "p_legend_fangorn"), # just so that the find music script dosn't go nuts
        	(set_jump_mission,"mt_fangorn_battle"),
        	(jump_to_scene,":scene_to_use" ),
        
		(set_battle_advantage, 0),
        	(assign, "$g_battle_result", 0),
        	(assign, "$g_next_menu", "mnu_fangorn_battle_debrief"),		
        	(jump_to_menu, "mnu_battle_debrief"),
        	(assign, "$g_mt_mode", vba_normal),
		(assign, "$cant_leave_encounter", 1),
        	(change_screen_mission),

	(else_try),
		(val_add,"$g_fangorn_rope_pulled", 30), 
		(val_clamp,"$g_fangorn_rope_pulled", 0,75), 
		(display_message,"@Fangorn search: failed."),
		(jump_to_menu, "mnu_fangorn_search_fails"),
	  (try_end),
	  #(change_screen_map),
	 ]),
   ]
 ),
( "fangorn_search_fails",0, # (orc) player searched fangorn but found nothing
   "^^^^^^You search the dark, thick forest but find nothing.^Still, you feel observed and threatened, more and more.",
   "none",[(store_add, reg10, "$player_looks_like_an_orc", "mesh_draw_fangorn"), (set_background_mesh, reg10),],[
    ("continue",[],"Continue...",
	 [(call_script,"script_fangorn_deal_damage","p_main_party"),
	  (call_script,"script_after_fangorn_damage_to_player"),
	 ]),
   ]
 ),
( "fangorn_battle_debrief",0, # player faced fangor dangers. Did he win?
    "you shouldn't be reading this",
	"none",[
		(try_begin),
			(eq, "$g_battle_result", 1),
			(jump_to_menu, "mnu_fangorn_battle_debrief_won"),
		(else_try),
			(assign, "$recover_after_death_menu", "mnu_recover_after_death_fangorn"),
		#	(jump_to_menu, "mnu_tld_player_defeated"),
			(jump_to_menu, "mnu_auto_return_to_map"),
		(try_end),
	 ],[]
 ),
( "fangorn_battle_debrief_won",0, # player faced fangor dangers, and won!
    "^^^A great victory!^^^So this is what all the myths about Fangorn meant...",
	"none",[],[
	("continue",[],"Continue...",[
		(change_screen_map),
		(try_begin),
			(check_quest_active, "qst_investigate_fangorn"),
			(neg|check_quest_succeeded, "qst_investigate_fangorn"),
			(neg|check_quest_failed, "qst_investigate_fangorn"),
			(call_script, "script_succeed_quest", "qst_investigate_fangorn"),
			(troop_add_item, "trp_player", "itm_ent_water", 0), #MV: reward for defeating the Ents
		(try_end),
	]),
 ]),
( "fangorn_killed_player_only",0, # player only was killed by fangorn
   "^^^^^^You wander in the thick, dark forest.^All of a sudden you are hit by something! Maybe a heavy branch fell on your head?^You stay unconcious only for minutes. You are badly hurt but you can go on.",
   "none",[(store_add, reg10, "$player_looks_like_an_orc", "mesh_draw_fangorn"), (set_background_mesh, reg10),],
		[("ow_get_out",[],"Ouch! Let's get out of this cursed place!",[(jump_to_menu,"mnu_auto_return_to_map")] ),]
 ),
( "fangorn_killed_troop_and_player",0, # player and troops were killed by fangorn
   "^^^^^^You wander in the thick, dark forest.^^All of a sudden you are hit by something! Maybe a heavy branch fell on your head.^^When you recover, minutes later, you find that not all of your troops were that lucky.^^",
   "none",[(store_add, reg10, "$player_looks_like_an_orc", "mesh_draw_fangorn"), (set_background_mesh, reg10),],
   [("ow_get_out",[],"Ouch! Let's get out of this cursed place!",[(jump_to_menu,"mnu_auto_return_to_map")] ),]
 ),
( "fangorn_killed_troop_only",0, # troops were killed by fangorn
   "^^^^^^^^You wander in the thick, dark forest. Your troops are fearful.^^All of a sudden, you hear screams from the rear! You hurry back, only to find a few of your troops on the ground, in a pool of blood.^^A few others are nowhere to be found...",
   "none",[(store_add, reg10, "$player_looks_like_an_orc", "mesh_draw_fangorn"), (set_background_mesh, reg10),],
   [("get_out",[],"Let's get out of this cursed place!",[(jump_to_menu,"mnu_auto_return_to_map")] ),]
 ),

#### CAPTURE TROLL MENU
( "can_capture_troll",0,"The downed wild troll still breaths!^^Its evil eyes stare at you filled with pain and rage.^Even now that it has been taken down, and lies helpless in a pool of its blood, it looks tremendously dangerous...",
  "none",[(set_background_mesh, "mesh_draw_wild_troll")], [
	("killit",[],"Dispatch it, now. Make sure it dies.",[(jump_to_menu,"$g_next_menu")],),
	("cageit1",[
	  (player_has_item,"itm_wheeled_cage"),(troops_can_join_as_prisoner,1),
	  (party_count_prisoners_of_type, ":num_trolls", "p_main_party", "trp_troll_of_moria"),(eq, ":num_trolls", 0),
	 ],
	 "Cage it and drag it around.",[
      (party_add_prisoners, "p_main_party", "trp_troll_of_moria", 1),
	  (display_message,"@Troll caged in wheeled cage."),
      (jump_to_menu,"$g_next_menu")],
	),
	("cageit2",[ # capture a second troll as prisoner
	   (player_has_item,"itm_wheeled_cage"),(troops_can_join_as_prisoner,1),
	   (party_count_prisoners_of_type, ":num_trolls", "p_main_party", "trp_troll_of_moria"),(eq, ":num_trolls", 1),
	],"Cage it together with the other troll.",[
      (party_add_prisoners, "p_main_party", "trp_troll_of_moria", 1),
	  (display_message,"@A second troll is caged in wheeled cage."),
      (jump_to_menu,"$g_next_menu")],
	),
  ]
 ),
  
################################ CHEAT/MODDING MENU START ########################################
# free magic item cheat (mtarini)   
("cheat_free_magic_item",0,"Which free magic item do you want?","none",[(set_background_mesh, "mesh_ui_default_menu_window")],
   [ ("cheat_free_magic_item_back",[],"Back",[(jump_to_menu, "mnu_camp_cheat")]), ]
   +
   [ ("mi20",[(neg|player_has_item,x),(str_store_item_name,s20,x)],"{s20}",[(troop_add_item ,"trp_player",x),(display_message, "@Here you are."),]) 
	for x in magic_items ]
 ),
# choose quest cheat (mtarini)
("cheat_impose_quest",0,"Current imposed quest:^{s20}^^Which quest do you want to impose?^(no other quests will be given)","none",[
    (set_background_mesh, "mesh_ui_default_menu_window"),
    (try_begin),(ge,"$cheat_imposed_quest",0),(str_store_quest_name,s20,"$cheat_imposed_quest"),(else_try),(str_store_string,s20,"@None"),(try_end),
  ],[
	("just_back",[],"Back",[(jump_to_menu, "mnu_camp_cheat")]),
	("none",[],"None",[(assign,"$cheat_imposed_quest",-1),(jump_to_menu, "mnu_cheat_impose_quest")]),
#	("night_bandits",[],"Mirkwood Sorcerer",[(assign,"$cheat_imposed_quest","qst_mirkwood_sorcerer")]),
#	("spears",[],"Lost Spears",[(assign,"$cheat_imposed_quest","qst_find_lost_spears")]),
    ]+[("mi21",[(str_store_quest_name,s21,x)],"{s21}",[(assign,"$cheat_imposed_quest",x),(jump_to_menu, "mnu_cheat_impose_quest")]) for x in range(qst_quests_end) ]+[
  ]),
  
  ### CHOSE TOWN WHERE TO RELOCATE PART 2: chose city (mtarini)
  ("teleport_to_town_part_two",0,"^^^^^^^^Ride Shadowfax:^to which city inside {s11}?","none",[(set_background_mesh, "mesh_ui_default_menu_window")],
  concatenate_scripts([[
  (
	"go_to_town_",
	[
	(store_faction_of_party, ":fact", center_list[y][0]),
	(eq, ":fact", "$teleport_menu_chosen_faction"),
	(str_store_party_name, s10, center_list[y][0]),],
	"{s10}.",
	[
		(str_store_party_name, s10, center_list[y][0]),
		(display_message, "@Player was moved to {s10}."),
		(party_relocate_near_party, "p_main_party", center_list[y][0], 3),
		(jump_to_menu, "mnu_camp"),
    ]
  )
  ]for y in range(len(center_list)) ])
  +[
  ("another_kingdom",[],"No, Another Kingdom",[(jump_to_menu, "mnu_teleport_to_town"),]),	   
 ]),
# CHOSE TOWN WHERE TO RELOCATE PART 1: chose faction (mtarini)
( "teleport_to_town",0,"^^^^^^^^Ride Shadowfax:^to which kingdom?","none",[(set_background_mesh, "mesh_ui_default_menu_window"),],
  concatenate_scripts([[
  (
	"go_to_town",
	[
	(str_store_faction_name, s10, faction_init[y][0]),
	(eq, "$teleport_menu_chosen_faction_group", y/7),],
	"{s10}.",
	[
		(assign, "$teleport_menu_chosen_faction", faction_init[y][0]),
		(jump_to_menu, "mnu_teleport_to_town_part_two"),
		(str_store_faction_name, s11, faction_init[y][0])
    ]
  )
  ]for y in range(len(faction_init)) ])
  +[
	("teleport_neutrals",[(eq, "$teleport_menu_chosen_faction_group", 2),],"Others/neutrals",[
		(assign, "$teleport_menu_chosen_faction", -1),
		(str_store_string, s11, "@neutral whereabouts"),
		(jump_to_menu, "mnu_teleport_to_town_part_two"),
	]),
	("teleport_others_factions",[(store_add, reg5, "$teleport_menu_chosen_faction_group", 1),],"More... ({reg5}/3)",[
		(try_begin),
			(eq, "$teleport_menu_chosen_faction_group", 2),
			(assign, "$teleport_menu_chosen_faction_group", 0),
		(else_try),
			(store_add, "$teleport_menu_chosen_faction_group", "$teleport_menu_chosen_faction_group", 1),
		(try_end),
		(jump_to_menu, "mnu_teleport_to_town"),
	]),
	("teleport_back",[],"Back to camp menu.",[(jump_to_menu, "mnu_camp"),]),
 ]),
### A MENU TO SELECT ANY TROOP (mtarini)
( "select_any_troop",0,
  "Select troops:^^^Current search parameters:^Faction: {s10}^Race: {s13}^Tier: {s11}^{s12}","none",
  code_to_set_search_string+[
  (assign,"$tmp_menu_entry_n",0),
  (assign,"$tmp_menu_skipped",0),
  ],
  [
  ]+concatenate_scripts([[
     ("trp",[ 
		(lt,"$tmp_menu_entry_n",tmp_menu_steps),
		
		(store_character_level, reg11, y),
		(store_div, reg14, reg11, 10),
		(this_or_next|eq, reg14, "$menu_select_any_troop_search_tier"),
		(eq, "$menu_select_any_troop_search_tier", tmp_menu_max_tier+1),
		
		(assign, ":ok", 1),
		(try_begin), (eq,"$menu_select_any_troop_search_hero", 0), 
			(try_begin),(troop_is_hero, y), (assign, ":ok", 0),(try_end),	
		(else_try),  (eq,"$menu_select_any_troop_search_hero", 1), 
			(try_begin),(neg|troop_is_hero, y), (assign, ":ok", 0),(try_end),	
		(try_end),		
		(eq, ":ok", 1),
		
		(store_troop_faction, reg12, y),
		(this_or_next|eq, reg12, "$menu_select_any_troop_search_fac"),
		(eq, "$menu_select_any_troop_search_fac", tmp_menu_max_fac+1),
		
		(troop_get_type, reg13, y),
		(this_or_next|eq, reg13, "$menu_select_any_troop_search_race"),
		(eq, "$menu_select_any_troop_search_race", len(race_names)),
		
		
		(val_add,"$tmp_menu_skipped",1),
		(gt,"$tmp_menu_skipped" , "$add_troop_menu_index"),
		(val_add,"$tmp_menu_entry_n",1),
		(str_store_troop_name, s11, y),
	 ],
	 "{s11} (lvl:{reg11})",
	 [ (try_begin), (eq, "$select_any_troop_add_selected_troops",1), (troop_join, y ),
	   (else_try), (assign, "$select_any_troop_result" , y), (jump_to_menu, "$select_any_troop_nextmenu"), (try_end),
	 ]
	 )
  ]for y in range(5,tmp_max_troop+1) ])
  +[
  ("prev_page" ,[],"[Prev Page]" ,[(val_sub, "$add_troop_menu_index", tmp_menu_steps),(val_max,  "$add_troop_menu_index", 0),(jump_to_menu, "mnu_select_any_troop"),]), 
  ("next_page" ,[],"[Next Page]" ,[(val_add, "$add_troop_menu_index", tmp_menu_steps), (jump_to_menu, "mnu_select_any_troop"),]), 
  ("opt" ,[],"[Search Option]" ,[(jump_to_menu, "mnu_select_any_troop_setup_search"),]), 
  ("done"   ,[ (eq, "$select_any_troop_add_selected_troops",1) ],"[Done]" ,[(jump_to_menu, "$select_any_troop_nextmenu"),]), 
  ("cancel"   ,[ (eq, "$select_any_troop_add_selected_troops",0) ],"[Cancel]" ,[(assign, "$select_any_troop_result" , -1), (jump_to_menu, "$select_any_troop_nextmenu"),]), 
 ]),
### ADD TROOPS CHEAT PART 2 (mtarini)
( "select_any_troop_setup_search",0,
  "Add troops: setup search parameters^^^Current parameters:^Faction: {s10}^Race: {s13}^Tier: {s11}^{s12}","none",
  code_to_set_search_string,
  [
	("one" ,[],"[Change Tier]" ,[
		(val_add, "$menu_select_any_troop_search_tier", 1),
		(try_begin) , (ge, "$menu_select_any_troop_search_tier", tmp_menu_max_tier+2), (assign, "$menu_select_any_troop_search_tier", 0), (try_end),
		(jump_to_menu, "mnu_select_any_troop_setup_search"),
	]), 
	("facup" ,[],"[Prev Faction]" ,[
		(val_sub, "$menu_select_any_troop_search_fac", 1),
		(try_begin) , (eq, "$menu_select_any_troop_search_fac", -1), (assign,"$menu_select_any_troop_search_fac", tmp_menu_max_fac+1), (try_end),
		(jump_to_menu, "mnu_select_any_troop_setup_search"),
	]), 
	("facdown" ,[],"[Next Faction]" ,[
		(val_add, "$menu_select_any_troop_search_fac", 1),
		(try_begin) , (ge, "$menu_select_any_troop_search_fac", tmp_menu_max_fac+2), (assign,"$menu_select_any_troop_search_fac", 0), (try_end),
		(jump_to_menu, "mnu_select_any_troop_setup_search"),
	]), 

	("raceup" ,[],"[Prev Race]" ,[
		(val_sub, "$menu_select_any_troop_search_race", 1),
		(try_begin), (eq, "$menu_select_any_troop_search_race", -1), (assign,"$menu_select_any_troop_search_race", len(race_names)), (try_end),
		(jump_to_menu, "mnu_select_any_troop_setup_search"),
	]), 
	("racedown" ,[],"[Next Race]" ,[
		(val_add, "$menu_select_any_troop_search_race", 1),
		(try_begin), 
			(ge, "$menu_select_any_troop_search_race", len(race_names)+1), 
			(assign,"$menu_select_any_troop_search_race", 0),
		(try_end),
		(jump_to_menu, "mnu_select_any_troop_setup_search"),
	]), 
	("three" ,[],"[Regulars or Heroes]" ,[
		(val_add, "$menu_select_any_troop_search_hero", 1),
		(try_begin), 
			(eq, "$menu_select_any_troop_search_hero", 3), 
			(assign,"$menu_select_any_troop_search_hero", 0), 
		(try_end),
		(jump_to_menu, "mnu_select_any_troop_setup_search"),
		]), 

	("done"   ,[],"[Done]" ,[(assign, "$add_troop_menu_index", 0),(jump_to_menu, "mnu_select_any_troop"),]), 
 ]),
( "camp_cheat",0,
   "Other Cheats Menu (for development use):^^This menu is intended for development use while we are working on improving this mod. If you enable this option then additonal CHEAT menu's will also appear in other game menu's. Please do not report any bugs with this functionality since it is for testing only.",
   "none",
	[(set_background_mesh, "mesh_ui_default_menu_window"),
	 (call_script, "script_determine_what_player_looks_like"), # if back from change race
	],
	[
 ]+concatenate_scripts([[	 
 	 ("cheat_disabable",[],
		"Disable cheat/modding options.",[(assign, "$cheat_mode", 0),	(jump_to_menu, "mnu_camp"),]),

	("crossdressing", [(assign,reg6, "$tld_option_crossdressing"), ], "Crossdressing: {reg6?Enabled:Disabled}", 
	  [(store_sub, "$tld_option_crossdressing", 1, "$tld_option_crossdressing"), (jump_to_menu, "mnu_camp_cheat"),]),

	("cheat_change_race",[],"Change your race (for development use).",[(jump_to_menu, "mnu_cheat_change_race"),]),	   
	("impose_quest", [], "Impose a quest...",  [(jump_to_menu, "mnu_cheat_impose_quest")]),
	("relocate_party", [],   "Move to town...", [(jump_to_menu, "mnu_teleport_to_town")]),
	("add_troops", [], "Add troops to player party.", [
	   (assign, "$select_any_troop_nextmenu","mnu_camp_cheat" ), 
	   (assign, "$select_any_troop_add_selected_troops",1 ), 
	   (jump_to_menu, "mnu_select_any_troop") 
	 ]),
	("cheat_get_item", [], "Gain a free magic item", [(jump_to_menu, "mnu_cheat_free_magic_item")]),
	("cheat_add_xp", [], "Add 1000 experience to player.", [(add_xp_to_troop, 1000, "trp_player"), (display_message, "@Added 1000 experience to player."), ]),	  	
    ("camp_mod_2",    [],
      "Raise player's attributes, skills, and proficiencies.",
      [ #attributes
         (troop_raise_attribute, "trp_player",ca_intelligence,20),
         (troop_raise_attribute, "trp_player",ca_strength,20),
		 (troop_raise_attribute, "trp_player",ca_agility,20),
		 (troop_raise_attribute, "trp_player",ca_charisma,20),
		 #skills
         (troop_raise_skill, "trp_player",skl_riding,10),
		 (troop_raise_skill, "trp_player",skl_shield,5),		#there is a bug in M&B 1.x where the shield skill helps out the other team so don't raise it too high
         (troop_raise_skill, "trp_player",skl_spotting,10),
         (troop_raise_skill, "trp_player",skl_pathfinding,10),
         (troop_raise_skill, "trp_player",skl_trainer,10),
         (troop_raise_skill, "trp_player",skl_leadership,10),
         (troop_raise_skill, "trp_player",skl_trade,10),
         (troop_raise_skill, "trp_player",skl_prisoner_management,10),
		(troop_raise_skill, "trp_player", skl_athletics, 10),
		(troop_raise_skill, "trp_player", skl_power_strike, 10),
		(troop_raise_skill, "trp_player", skl_power_draw, 10),
		(troop_raise_skill, "trp_player", skl_power_throw, 10),
		(troop_raise_skill, "trp_player", skl_weapon_master, 10),
		(troop_raise_skill, "trp_player", skl_horse_archery, 10),
		(troop_raise_skill, "trp_player", skl_ironflesh, 10),
		(troop_raise_skill, "trp_player", skl_inventory_management, 10),
	
		#proficiencies
		(troop_raise_proficiency_linear, "trp_player", wpt_one_handed_weapon, 350),
		(troop_raise_proficiency_linear, "trp_player", wpt_two_handed_weapon, 350),
		(troop_raise_proficiency_linear, "trp_player", wpt_polearm, 350),
		(troop_raise_proficiency_linear, "trp_player", wpt_archery, 350),
		(troop_raise_proficiency_linear, "trp_player", wpt_crossbow, 350),
		(troop_raise_proficiency_linear, "trp_player", wpt_throwing, 350),
		(troop_raise_proficiency_linear, "trp_player", wpt_firearm, 350),	 
		 
         (display_message, "@Attributes, skills and proficiencies raised."),
        ]
      ),      

     ("camp_mod_3",   [],
      "Add gear and gold to player.",
       [(troop_add_gold, "trp_player", 10000),
   
#		(troop_add_item, "trp_player","itm_mail_hauberk",0),
		(troop_add_item, "trp_player","itm_mail_mittens",0),
#		(troop_add_item, "trp_player","itm_mail_boots",0),
#		(troop_add_item, "trp_player","itm_shield_heater_c",0),
#		(troop_add_item, "trp_player","itm_bastard_sword_a",0),
		(troop_add_item, "trp_player","itm_gondor_bow",0),
		(troop_add_item, "trp_player","itm_arrows",0),		
#		(troop_add_item, "trp_player","itm_wargarmored_1c",0),		
		(troop_equip_items, "trp_player"),
		
        (troop_add_item, "trp_player","itm_arrows",0),
		(troop_add_item, "trp_player","itm_dried_meat",0),
		(troop_add_item, "trp_player","itm_tools",0),
		
	    (display_message, "@Items added to player inventory."),
        ]
       ),	  
	  
      #("camp_mod_1",   [],
	  #"Increase relations with all Factions.",
#       [(try_for_range,":faction",kingdoms_begin,kingdoms_end),
#		   (call_script, "script_set_player_relation_with_faction", ":faction", 40),
        #(try_end),
		#(display_message, "@Increased relations with all factions."),
        #]
       #),
	   
      #("camp_mod_1b", [],
	  #"Decrease relations with all Factions.",
#       [(try_for_range,":faction",kingdoms_begin,kingdoms_end),
#		   (call_script, "script_set_player_relation_with_faction", ":faction", -40),
        #(try_end),
		#(display_message, "@Decreased relations with all factions."),
        #]),	   

      ("camp_mod_4",   [],
      "Spawn a looter party nearby.",
      [  (spawn_around_party, "p_main_party", "pt_looters"),
         (display_message, "@Looter party was spawned nearby."),
      ]),
	  
      ("camp_mod_5",   [],
      "Fill merchants with faction stuff",
      [(call_script,"script_fill_merchants_cheat"),(display_message,"@DEBUG: Smiths just got stuffed!"),(jump_to_menu, "mnu_camp"),]),

	 #("test1",[],"Test: pay upkeep now", [(call_script,"script_make_player_pay_upkeep")]),
	 #("test2",[],"Test: make unpaid troop leave now", [(call_script, "script_make_unpaid_troop_go")]),
  ] for ct in range(cheat_switch)])+[	
	 ("cheat_back",[],"Back to camp menu.",[(jump_to_menu, "mnu_camp"),]),	 
 ]),

( "drank_ent_water_human",0,# human player drank Ent water
    "^^^You drink the water. It tastes clean and refreshing. It has a pleasant fragrance, as of musk.^You feel refreshed.^^However, you also have a strange, unnatural feeling. Something tells you that you'd better never, ever again drink this water.",
  "none",[  (try_begin),
              (troop_get_type, ":player_race", "trp_player"),
              (            eq, ":player_race",  tf_dwarf),
              # --
              (set_background_mesh, "mesh_draw_entdrink_dwarf"),
              
            (else_try),
              (call_script, "script_determine_what_player_looks_like"),
              (         eq, "$player_looks_like_an_orc", 1),
              # --
              (set_background_mesh, "mesh_draw_entdrink_orc"),
              
            (else_try),
              (set_background_mesh, "mesh_draw_entdrink_human"),
            (try_end),

  ],[("continue_dot",[],"Continue.",[(change_screen_return,0),] ),]
 ),
( "drank_ent_water_orc",0,# orc player drank Ent water (mtarini)
	"^^^You drink the water. It is just water.^Suddenly, you grasp your throath, in a raptus of pain.^Poisoned!^You choke, you throw up black blood, you almost pass away.^^It hurts, oh, it hurts.",
	"none",[(display_log_message,"@HP lost from poisoning."),(troop_set_health,"trp_player",5),]
	,[("i_shall_surv",[],"I... shall... survive!",[(change_screen_return,0)])]
 ),

( "end_game",0,
 "^^^^^The decision is made, and you resolve to give up your adventurer's\
 life and settle down. You sell off your weapons and armour, gather up\
 all your belongings, and ride off into the sunset....",
 "none",
 [],
 [("end_game_bye",[],"Farewell.",[(change_screen_quit)])]
 ),

#MV: DON'T REMOVE THIS AGAIN - IT'S USED IN A QUEST
  ("cattle_herd",mnf_scale_picture,
   "You encounter some people.",
   "none",
   [],
    [ ("cattle_drive_away",[],"Order them to follow.",
       [(party_set_slot, "$g_encountered_party", slot_cattle_driven_by_player, 1),
        (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_escort_party),
        (party_set_ai_object,"$g_encountered_party", "p_main_party"),
        (change_screen_return),
        ]),
      ("cattle_stop",[],"Bring them to a stop.",
       [(party_set_slot, "$g_encountered_party", slot_cattle_driven_by_player, 0),
        (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_hold),
        (change_screen_return),
        ]),
      ("leave",[],"Leave.",[(change_screen_return),]),
    ]
  ),

( "simple_encounter",mnf_enable_hot_keys,
    "^^^^^{s2}^You have {reg22} troops fit for battle against their {reg11}.^^The battle is taking place in {s3}{s4}.^^Your orders?",
    "none",
    [	#(set_background_mesh, "mesh_ui_default_menu_window"),
		(try_begin), 
			(eq, "$prebattle_talk_done",1),
			(assign, "$prebattle_talk_done",0),
			(call_script,"script_start_current_battle"),
		(try_end),
		
		# get region + landmark (mtarini)
		#(party_get_current_terrain, "$current_player_terrain","p_main_party"),
		#(call_script, "script_get_region_of_party","p_main_party"),(assign, "$current_player_region", reg1),
		#(call_script, "script_get_close_landmark","p_main_party"), (assign, "$current_player_landmark", reg0),
		
		(store_add, reg2, str_shortname_region_begin, "$current_player_region",),
		(str_store_string,s3,reg2),
		
		(str_clear, s4),
		(try_begin), 
			(call_script, "script_cf_store_landmark_description_in_s17", "$current_player_landmark"),
			(str_store_string,s4,"@, {s17}."), 
		(try_end),

        (assign, "$g_enemy_party", "$g_encountered_party"),
        (assign, "$g_ally_party", -1),
        (call_script, "script_encounter_calculate_fit"),
		(assign, reg22, reg10),
        (try_begin),
		  # first turn...
          (eq, "$new_encounter", 1),
          
          #(assign, "$g_encounter_is_in_village", 0),
          #(assign, "$g_encounter_type", 0),
          (try_begin),
            (party_slot_eq, "$g_enemy_party", slot_party_ai_state, spai_raiding_around_center),
            (party_get_slot, ":village_no", "$g_enemy_party", slot_party_ai_object),
            (store_distance_to_party_from_party, ":dist", ":village_no", "$g_enemy_party"),
            (try_begin),
              (lt, ":dist", raid_distance),
              #(assign, "$g_encounter_is_in_village", ":village_no"),
#              (assign, "$g_encounter_type", enctype_fighting_against_village_raid),
            (try_end),
          (try_end),

          (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
          (call_script, "script_encounter_init_variables"),
          (assign, "$encountered_party_hostile", 0),
          (assign, "$encountered_party_friendly", 0),
          
          #MV: Quest exceptions
          (assign, ":is_quest_party", 0),
          (try_begin),
            (this_or_next|eq, "$g_encountered_party_template", "pt_gandalf"),
            (this_or_next|eq, "$g_encountered_party_template", "pt_nazgul"),
            (eq, "$g_encountered_party_template", "pt_runaway_serfs"),
            (assign, ":is_quest_party", 1),
          (try_end),
          
          (try_begin),
            (this_or_next|gt, "$g_encountered_party_relation", 0),
            (eq, ":is_quest_party", 1),
            (assign, "$encountered_party_friendly", 1),
			# talk with non-hostile parties OR quest parties
			(assign, "$new_encounter", 0),
			(assign, "$talk_context", tc_party_encounter),
            (try_begin), #cutscene dialogs
              (eq, "$g_encountered_party_template", "pt_gandalf"),
              (gt, "$g_tld_gandalf_state", 0),
              (call_script, "script_start_conversation_cutscene", "$g_tld_gandalf_state"),
            (else_try), 
              (eq, "$g_encountered_party_template", "pt_nazgul"),
              (gt, "$g_tld_nazgul_state", 0),
              (call_script, "script_start_conversation_cutscene", "$g_tld_nazgul_state"),
            (else_try), #normal dialogs
			  (call_script, "script_setup_party_meeting", "$g_encountered_party"),
            (try_end),
          (try_end),
          (try_begin),
            (lt, "$g_encountered_party_relation", 0),
            (assign, "$encountered_party_hostile", 1),
            (try_begin),
              (encountered_party_is_attacker),
              (assign, "$cant_leave_encounter", 1),
            (try_end),
          (try_end),
        (else_try), 
		  #second or more wave
		  #          (try_begin),
		  #            (call_script, "script_encounter_calculate_morale_change"),
		  #          (try_end),
          (try_begin),
            # We can leave battle only after some troops have been killed. 
            (eq, "$cant_leave_encounter", 1),
            (call_script, "script_party_count_members_with_full_health", "p_main_party_backup"),
            (assign, ":org_total_party_counts", reg0),
            (call_script, "script_party_count_members_with_full_health", "p_encountered_party_backup"),
            (val_add, ":org_total_party_counts", reg0),

            (call_script, "script_party_count_members_with_full_health", "p_main_party"),
            (assign, ":cur_total_party_counts", reg0),
            (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
            (val_add, ":cur_total_party_counts", reg0),

            (store_sub, ":leave_encounter_limit", ":org_total_party_counts", 10),
            (lt, ":cur_total_party_counts", ":leave_encounter_limit"),
            (assign, "$cant_leave_encounter", 0),
          (try_end),
          (eq, "$g_leave_encounter",1),
          (change_screen_return),
        (try_end),

        #setup s2
        (try_begin),
          (party_is_active,"$g_encountered_party"),
          (str_store_party_name, s1,"$g_encountered_party"),
          (try_begin),
			(eq, "$new_encounter", 1),
			(eq, "$encountered_party_hostile", 1),
			(encountered_party_is_attacker),
			(call_script, "script_str_store_party_movement_verb", s10, "$g_encountered_party"),
            (str_store_string, s2,"@A group of {s1} is {s10} toward you."),
			#(str_store_string, s2,"@A group of {s1}  are {reg10?riding:marching} toward you."),
          (else_try),
			(eq, "$new_encounter", 1),
			(eq, "$encountered_party_hostile", 1),
			(neg|encountered_party_is_attacker),
            (str_store_string, s2,"@You are attacking a group of {s1}."),
          (else_try),
			(eq, "$new_encounter", 0),
            (str_store_string, s2,"@The battle against the group of {s1} continues."),
          (try_end),
        (try_end),
		
		
        (try_begin),
          (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
          (assign, ":num_enemy_regulars_remaining", reg0 ),
          (assign, ":enemy_finished",0),
          (try_begin),
            (eq, "$g_battle_result", 1),
            (eq, ":num_enemy_regulars_remaining", 0), #battle won
            (assign, ":enemy_finished",1),
          (else_try),
            (eq, "$g_engaged_enemy", 1),
            (le, "$g_enemy_fit_for_battle",0),
            (ge, "$g_friend_fit_for_battle",1),
            (assign, ":enemy_finished",1),
          (try_end),
          (this_or_next|eq, ":enemy_finished",1),
          (eq,"$g_enemy_surrenders",1),
          (assign, "$g_next_menu", -1),
          (jump_to_menu, "mnu_total_victory"),
        (else_try),
		  #     (eq, "$encountered_party_hostile", 1),
          (call_script, "script_party_count_members_with_full_health","p_main_party"),
          (assign, reg3, reg0),
          (assign, ":friends_finished",0),
          (try_begin),
            (eq, "$g_battle_result", -1),
            (eq, reg3, 0), #battle lost
            (assign,  ":friends_finished",1),
          (else_try),
            (eq, "$g_engaged_enemy", 1),
            (ge, "$g_enemy_fit_for_battle",1),
            (le, "$g_friend_fit_for_battle",0),
            (assign,  ":friends_finished",1),
          (try_end),
		  
          (this_or_next|eq,"$g_player_surrenders",1),
          (eq,  ":friends_finished",1),
		  (assign, "$recover_after_death_menu", "mnu_recover_after_death_default"),
          (assign, "$g_next_menu", "mnu_tld_player_defeated"),
          (jump_to_menu, "mnu_total_defeat"),
        (try_end),

		## set background mesh
		(set_background_mesh, "mesh_ui_default_menu_window"),
    (try_begin),
      (eq, "$g_encountered_party_template", "pt_looters"  ),
      (set_background_mesh, "mesh_draw_tribal_orcs"),
    (else_try),
      #swy-- if "wild goblins" or "troublesome goblins" show this illustration thingy...
      (this_or_next|eq, "$g_encountered_party_template", "pt_mountain_bandits"),
      (             eq, "$g_encountered_party_template", "pt_troublesome_bandits"),
      (set_background_mesh, "mesh_draw_mountain_goblins"),
    (else_try),
      #swy-- if "corsair renegades" or "corsair scouts" show this illustration thingy...
      (this_or_next|eq, "$g_encountered_party_template", "pt_sea_raiders"),
      (             eq, "$g_encountered_party_template", "pt_umbar_scouts"),
      (set_background_mesh, "mesh_draw_corsair_renegades"),
    (else_try),
      #swy-- if "dunland outcasts" or "dunland scouts" show this illustration thingy...
      (this_or_next|eq, "$g_encountered_party_template", "pt_dunland_scouts"),
      (             eq, "$g_encountered_party_template", "pt_steppe_bandits"),
      (set_background_mesh, "mesh_draw_dunland_outcasts"),
    (else_try),
      (is_between, "$g_encountered_party_template", "pt_forest_bandits" ,"pt_steppe_bandits"        ),
      (set_background_mesh, "mesh_draw_orc_raiders"),
    (else_try),
      (is_between, "$g_encountered_party_template", "pt_wild_troll" ,"pt_looters"),
      (set_background_mesh, "mesh_draw_wild_troll"),
    (try_end),
		
		
		# set reg21, to change the options string in the menu
		(try_begin), (encountered_party_is_attacker),
			(assign, reg21, 0),
		(else_try),
			(assign, reg21, 1),
		(try_end),
    ],
	
    [
      ("encounter_attack",[
          (this_or_next|eq, "$encountered_party_friendly", 0),
		  (is_between, "$g_encountered_party_template", "pt_wild_troll" ,"pt_looters"),
          # (neg|troop_is_wounded, "trp_player"), a test: what happes if I let player partecipate?
##          (store_troop_health,reg(5)),
##          (ge,reg(5),5),
          ],
         "{reg21?Charge_them:Prepare_to_face_them}.",[
			(try_begin),
				# talk with hostile troops after you have chose to attack
				(eq, "$new_encounter", 1),
				(assign, "$new_encounter", 0),
				(assign, "$prebattle_talk_done",1),
				(assign, "$talk_context", tc_party_encounter),
				(call_script, "script_setup_party_meeting", "$g_encountered_party"),
			(else_try),
				(call_script,"script_start_current_battle"),
			(try_end),

      ]),
      ("encounter_order_attack",[
          (eq, "$encountered_party_friendly", 0),
          (call_script, "script_party_count_members_with_full_health", "p_main_party"),(ge, reg0, 4),
          ],
           "Order your troops to {reg21?attack:face_them} without you.",[
		     (assign, "$new_encounter", 0),
		     (jump_to_menu,"mnu_order_attack_begin"),
                                                            #(simulate_battle,3)
		]),
		("special_whip",[
			(eq, "$new_encounter", 1),
		    (is_between, "$g_encountered_party_template", "pt_looters","pt_steppe_bandits"),
		    (player_has_item, "itm_angmar_whip_reward"),
			(str_store_item_name, s4, "itm_angmar_whip_reward"),
			(party_can_join_party, "$g_encountered_party","p_main_party"),
		],
		"Rush forward toward them cracking the {s4}.",[
			(call_script, "script_setup_party_meeting", "$g_encountered_party"),
			(assign,"$talk_context",tc_make_enemy_join_player),
		]),

 ]+concatenate_scripts([[	 
      ("debug_leave",[
          (eq,"$cant_leave_encounter", 1),
		  (eq, "$cheat_mode", 1),
          ],"DEBUG: avoid this battle.",[ (leave_encounter),(change_screen_return)]),
 ] for ct in range(cheat_switch)])+[

      ("encounter_leave",[
          (eq,"$cant_leave_encounter", 0),
          ],"Disengage.",[
###NPC companion changes begin
              #(try_begin),
              #    (eq, "$encountered_party_friendly", 0),
              #    (encountered_party_is_attacker),
              #    (call_script, "script_objectionable_action", tmt_aristocratic, "str_flee_battle"),
              #(try_end),
###NPC companion changes end
#Troop commentary changes begin
              # (try_begin),
                  # (eq, "$encountered_party_friendly", 0),
                  # (encountered_party_is_attacker),
                  # (party_get_num_companion_stacks, ":num_stacks", "p_encountered_party_backup"),
                  # (try_for_range, ":stack_no", 0, ":num_stacks"),
                    # (party_stack_get_troop_id,   ":stack_troop","p_encountered_party_backup",":stack_no"),
                    # (is_between, ":stack_troop", kingdom_heroes_begin, kingdom_heroes_end),
                    # (store_troop_faction, ":victorious_faction", ":stack_troop"),
                    # (call_script, "script_add_log_entry", logent_player_retreated_from_lord, "trp_player",  -1, ":stack_troop", ":victorious_faction"),
                  # (try_end),
              # (try_end),
#Troop commentary changes end
		# This is here so when you flee/leave it checks for routed parties -CC
		(try_begin),(call_script, "script_cf_spawn_routed_parties"),(try_end),
          	(leave_encounter),(change_screen_return)]),
			
      ("encounter_retreat",[
         (eq,"$cant_leave_encounter", 1),
         (call_script, "script_get_max_skill_of_player_party", "skl_tactics"),
         (assign, ":max_skill", reg0),
         (val_add, ":max_skill", 4),

         (call_script, "script_party_count_members_with_full_health", "p_collective_enemy", 0),
         (assign, ":enemy_party_strength", reg0),
         (val_div, ":enemy_party_strength", 2),

         (val_div, ":enemy_party_strength", ":max_skill"),
         (val_max, ":enemy_party_strength", 1),

         (call_script, "script_party_count_fit_regulars", "p_main_party"),
         (assign, ":player_count", reg0),
         (ge, ":player_count", ":enemy_party_strength"),
         ],"Pull back, leaving some soldiers behind to cover your retreat.",[(jump_to_menu, "mnu_encounter_retreat_confirm"),]),

 ]+concatenate_scripts([[		 
      ("encounter_surrender",[
         (eq,"$cant_leave_encounter", 1),
		 (eq, "$cheat_mode", 1),
          ],"DEBUG: surrender.",[(assign,"$g_player_surrenders",1)]),

	  ("encounter_cheat_heal",[
         (eq, "$cheat_mode",1),
		 (store_troop_health  , reg20, "trp_player",0), (lt, reg20,95),
          ],"CHEAT: heal yourself.",[
		    (troop_set_health  , "trp_player",100),
	        (display_message, "@CHEAT: healed!!!"),
			(jump_to_menu, "mnu_simple_encounter"),
		]),
 ] for ct in range(cheat_switch)])+[
    ]
 ),
( "encounter_retreat_confirm",0,
    "^^^^^As the party member with the highest tactics skill,\
   ({reg2}), {reg3?you devise:{s3} devises} a plan that will allow you and your men to escape with your lives,\
   but you'll have to leave {reg4} soldiers behind to stop the enemy from giving chase.",
    "none",
    [(set_background_mesh, "mesh_ui_default_menu_window"),
	 (call_script, "script_get_max_skill_of_player_party", "skl_tactics"),
     (assign, ":max_skill", reg0),
     (assign, ":max_skill_owner", reg1),
     (assign, reg2, ":max_skill"),
     (val_add, ":max_skill", 4),

     (call_script, "script_party_count_members_with_full_health", "p_collective_enemy", 0),
     (assign, ":enemy_party_strength", reg0),
     (val_div, ":enemy_party_strength", 2),

     (store_div, reg4, ":enemy_party_strength", ":max_skill"),
     (val_max, reg4, 1),
     
     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (assign, reg3, 1),
     (else_try),
       (assign, reg3, 0),
       (str_store_troop_name, s3, ":max_skill_owner"),
     (try_end),
     ],
    [
      ("leave_behind",[],"Go on. The sacrifice of these men will save the rest.",[
          (assign, ":num_casualties", reg4),
          (try_for_range, ":unused", 0, ":num_casualties"),
            (call_script, "script_cf_party_remove_random_regular_troop", "p_main_party"),
            (assign, ":lost_troop", reg0),
            (store_random_in_range, ":random_no", 0, 100),
            (ge, ":random_no", 30),
            (party_add_prisoners, "$g_encountered_party", ":lost_troop", 1),
           (try_end),
           (call_script, "script_change_player_party_morale", -20),
           (jump_to_menu, "mnu_encounter_retreat"),
          ]),
      ("dont_leave_behind",[],"No. We leave no one behind.",[(jump_to_menu, "mnu_simple_encounter"),]),
    ]
 ),
( "encounter_retreat",0,
    "^^^^^You tell {reg4} of your troops to hold the enemy while you retreat with the rest of your party.",
    "none",
    [],
    [("continue",[],"Continue...",[
###Troop commentary changes begin
          (call_script, "script_objectionable_action", tmt_aristocratic, "str_flee_battle"),
          (party_get_num_companion_stacks, ":num_stacks", "p_encountered_party_backup"),
          (try_for_range, ":stack_no", 0, ":num_stacks"),
              (party_stack_get_troop_id,   ":stack_troop","p_encountered_party_backup",":stack_no"),
              (is_between, ":stack_troop", kingdom_heroes_begin, kingdom_heroes_end),
              (store_troop_faction, ":victorious_faction", ":stack_troop"),
              (call_script, "script_add_log_entry", logent_player_retreated_from_lord_cowardly, "trp_player",  -1, ":stack_troop", ":victorious_faction"),
          (try_end),
###Troop commentary changes end  
		# This is here so when you flee it checks for routed parties -CC
	  (try_begin),(call_script, "script_cf_spawn_routed_parties"),(try_end),
          (leave_encounter),(change_screen_return)]),
    ]
 ),
( "order_attack_begin",0,
    "^^^^^^__________Your troops prepare to attack the enemy.",
    "none",
    [],
    [ ("order_attack_begin",[],"Order the attack to begin.", [(assign, "$g_engaged_enemy", 1),(jump_to_menu,"mnu_order_attack_2")]),
      ("call_back",[],"Call them back.",[(jump_to_menu,"mnu_simple_encounter")]),
    ]
 ),
( "order_attack_2",mnf_disable_all_keys,
    "^{s4}^Your casualties: {s8}^^Enemy casualties: {s9}",
    "none",
    [	(set_background_mesh, "mesh_ui_default_menu_window"),	
	
	# Reset routed count (needs to be here to prevent bugs...)
	(try_for_range, ":troop_no", 0, "trp_last"),
		(troop_set_slot, ":troop_no", slot_troop_routed_us, 0),
		(troop_set_slot, ":troop_no", slot_troop_routed_allies, 0),
		(troop_set_slot, ":troop_no", slot_troop_routed_enemies, 0),
	(try_end),
	
		(call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
		(assign, ":player_party_strength", reg0),
		(val_div, ":player_party_strength", 5),
		(call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
		(assign, ":enemy_party_strength", reg0),
		(val_div, ":enemy_party_strength", 5),
		#(call_script,"script_inflict_casualties_to_party", "p_main_party", ":enemy_party_strength"),
		(inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength", "p_temp_casualties"),
		(call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
		(str_store_string_reg, s8, s0),
		#(call_script,"script_inflict_casualties_to_party", "$g_encountered_party", ":player_party_strength"),
		(inflict_casualties_to_party_group, "$g_encountered_party", ":player_party_strength", "p_temp_casualties"),
		(call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
		(str_store_string_reg, s9, s0),
		(party_collect_attachments_to_party, "$g_encountered_party", "p_collective_enemy"),
		#(assign, "$cant_leave_encounter", 0),
		(assign, "$no_soldiers_left", 0),
		(try_begin),
		  (call_script, "script_party_count_members_with_full_health","p_main_party"),
		  (le, reg(0), 0),
		  (assign, "$no_soldiers_left", 1),
		  (str_store_string, s4, "str_order_attack_failure"),
		(else_try),
		  (call_script, "script_party_count_members_with_full_health","p_collective_enemy"),
		  (le, reg(0), 0),
		  (assign, ":continue", 0),
		  (party_get_num_companion_stacks, ":party_num_stacks", "p_collective_enemy"),
		  (try_begin),
			(eq, ":party_num_stacks", 0),
			(assign, ":continue", 1),
		  (else_try),
			(party_stack_get_troop_id, ":party_leader", "p_collective_enemy", 0),
			(try_begin),
			  (neg|troop_is_hero, ":party_leader"),
			  (assign, ":continue", 1),
			(else_try),
			  (troop_is_wounded, ":party_leader"),
			  (assign, ":continue", 1),
			(try_end),
		  (try_end),
		  (eq, ":continue", 1),
		  (assign, "$g_battle_result", 1),
		  (assign, "$no_soldiers_left", 1),
		  (str_store_string, s4, "str_order_attack_success"),
		(else_try),
		  (str_store_string, s4, "str_order_attack_continue"),
		(try_end),
    ],
    [("order_attack_continue",[(eq, "$no_soldiers_left", 0)],"Order your soldiers to continue the attack.",[(jump_to_menu,"mnu_order_attack_2")]),
     ("order_retreat",[(eq, "$no_soldiers_left", 0)],"Call your soldiers back.",[(jump_to_menu,"mnu_simple_encounter")]),
     ("continue",[(eq, "$no_soldiers_left", 1)],"Continue...",[(jump_to_menu,"mnu_simple_encounter")]),
    ]
 ),

# remove us - MV: reintroduced from Native
( "kingdom_army_quest_report_to_army",0,
   "{s8} sends word that he wishes you to join his new military campaign.\
   You need to bring at least {reg13} troops to the army,\
   and are instructed to raise more warriors with all due haste if you do not have enough.",
    "none",
    [   (set_background_mesh, "mesh_ui_default_menu_window"),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos0, 65),
        (position_set_y, pos0, 30),
        (position_set_z, pos0, 170),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$players_kingdom", pos0),
        
        (quest_get_slot, ":quest_target_troop", "qst_report_to_army", slot_quest_target_troop),
        (quest_get_slot, ":quest_target_amount", "qst_report_to_army", slot_quest_target_amount),
        (call_script, "script_get_information_about_troops_position", ":quest_target_troop", 0),
        (str_clear, s9),
        (try_begin),
          (eq, reg0, 1), #troop is found and text is correct
          (str_store_string, s9, s1),
        (try_end),
        (str_store_troop_name, s8, ":quest_target_troop"),
        (assign, reg13, ":quest_target_amount"),
      ],
    [
      ("reject",[],"Send a message you are too busy.",
       [   (quest_set_slot, "qst_report_to_army", slot_quest_dont_give_again_remaining_days, 7),
           (change_screen_return),
        ]),
      ("send_word",[],"Send word you'll join him shortly.",
       [   (quest_get_slot, ":quest_target_troop", "qst_report_to_army", slot_quest_target_troop),
           (quest_get_slot, ":quest_target_amount", "qst_report_to_army", slot_quest_target_amount),
           (str_store_troop_name_link, s13, ":quest_target_troop"),
           (assign, reg13, ":quest_target_amount"),
           (setup_quest_text, "qst_report_to_army"),
           (str_store_string, s2, "@{s13} asked you to report to him with at least {reg13} troops."),
           (call_script, "script_start_quest", "qst_report_to_army", ":quest_target_troop"),
           (call_script, "script_report_quest_troop_positions", "qst_report_to_army", ":quest_target_troop", 3),
           #Send Gandalf on a little chat
           (try_begin),
             (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
             (store_and, ":already_done", "$g_tld_conversations_done", tld_conv_bit_gandalf_advice),
             (eq, ":already_done", 0),
             (call_script, "script_send_on_conversation_mission", tld_cc_gandalf_advice),
           (try_end),
           (change_screen_return),
        ]),
     ]
 ),
( "kingdom_army_quest_messenger",0,
   "{s8} sends word that he wishes to speak with you about a task he needs performed.\
   He requests you to come and see him as soon as possible.",
    "none",
    [   (set_background_mesh, "mesh_ui_default_menu_window"),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos0, 65),
        (position_set_y, pos0, 30),
        (position_set_z, pos0, 170),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$players_kingdom", pos0),
        (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
        (str_store_troop_name, s8, ":faction_marshall"),
      ],
    [("continue",[],"Continue...",[(change_screen_return)])]
 ),
( "kingdom_army_quest_join_siege_order",0,
    "{s8} sends word that you are to join the siege of {s9} in preparation for a full assault.\
    Your troops are to take {s9} at all costs.",
    "none",
    [   (set_background_mesh, "mesh_ui_default_menu_window"),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos0, 65),
        (position_set_y, pos0, 30),
        (position_set_z, pos0, 170),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$players_kingdom", pos0),
        (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
        (quest_get_slot, ":quest_target_center", "qst_join_siege_with_army", slot_quest_target_center),
        (str_store_troop_name, s8, ":faction_marshall"),
        (str_store_party_name, s9, ":quest_target_center"),
      ],
    [
      ("continue",[],"Continue...",
       [   (call_script, "script_end_quest", "qst_follow_army"),
           (quest_get_slot, ":quest_target_center", "qst_join_siege_with_army", slot_quest_target_center),
           (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
           (str_store_troop_name_link, s13, ":faction_marshall"),
           (str_store_party_name_link, s14, ":quest_target_center"),
           (setup_quest_text, "qst_join_siege_with_army"),
           (str_store_string, s2, "@{s13} ordered you to join the assault against {s14}."),
           (call_script, "script_start_quest", "qst_join_siege_with_army", ":faction_marshall"),
           (change_screen_return),
        ]),
     ]
 ),
( "kingdom_army_follow_failed",0,
    "You have disobeyed orders and failed to follow {s8}. He sends a message he assumes you have more pressing matters, but warns his patience is not unlimited.",
    "none",
    [   (set_background_mesh, "mesh_ui_default_menu_window"),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos0, 65),
        (position_set_y, pos0, 30),
        (position_set_z, pos0, 170),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$players_kingdom", pos0),
        (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
        (str_store_troop_name, s8, ":faction_marshall"),
        (call_script, "script_abort_quest", "qst_follow_army", 1),
        #(call_script, "script_change_player_relation_with_troop", ":faction_marshall", -3),
      ],
    [("continue",[],"Continue...",[(change_screen_return)])]
 ),

( "battle_debrief",mnf_disable_all_keys,
    "{s11}^Your Casualties:{s8}{s10}^^Enemy Casualties:{s9}",
    "none",
    [(set_background_mesh, "mesh_ui_default_menu_window"),
	(call_script, "script_maybe_relocate_player_from_z0"),
    (val_add, "$battle_renown_total", "$battle_renown_value"),
	(call_script, "script_encounter_calculate_fit"),
	 
	(call_script, "script_party_count_fit_regulars", "p_main_party"),
    (assign, "$playerparty_postbattle_regulars", reg0),

	(try_begin), # set background picture for victory/defeat -- mtarini

		(this_or_next|eq, "$g_enemy_fit_for_battle",0),(eq, "$g_friend_fit_for_battle", 0 ), # battle is totally over: proceed!
		
		(try_begin),
			(eq, "$g_battle_result", 1),
			(assign, ":winning_side_race_group", "$player_side_race_group" ),
			(assign, ":losing_side_race_group",  "$enemy_side_race_group" ),
			(assign, ":winning_side_race", "$player_side_race" ),
			#(assign, ":losing_side_race",  "$enemy_side_race" ), # not used... yet
			(assign, ":winning_side_faction", "$player_side_faction" ),
			#(assign, ":losing_side_faction",  "$enemy_side_faction" ), # not used... yet
		(else_try),
			(assign, ":winning_side_race_group", "$enemy_side_race_group" ),
			(assign, ":losing_side_race_group",  "$player_side_race_group" ),
			(assign, ":winning_side_race", "$enemy_side_race" ),
			#(assign, ":losing_side_race",  "$player_side_race" ),   # not used... yet
			(assign, ":winning_side_faction", "$enemy_side_faction" ),
			#(assign, ":losing_side_faction",  "$player_side_faction" ), # not used... yet
		(try_end),

		# CppCoder quick search tag [VIKTOREE] (For adding the new victory paintings)
		
		(try_begin),
			# orc VS anything not orc
			( eq, ":winning_side_race_group", tf_orc ),
			(neq, ":losing_side_race_group",  tf_orc ),
			(store_random_in_range,":rnd",0,2),
			(try_begin),(eq,":rnd",0),(set_background_mesh, "mesh_draw_victory_orc"),  # specific victory-loss image:  orcs VS humans
			 (else_try),(set_background_mesh, "mesh_draw_victory_uruk"),
			(try_end),
		(else_try),	
			# orc VS orc
			( eq, ":winning_side_race_group", tf_orc ),
			( eq, ":losing_side_race_group",  tf_orc ),
			(neq, ":winning_side_faction",    fac_no_faction), # not good for winning tribals etc.
			(set_background_mesh, "mesh_draw_victory_orc_orc"),  # specific victory-loss image:  orcs VS orcs
		(else_try),
			# dwarf VS anything
			(eq, ":winning_side_race", tf_dwarf ),
			(set_background_mesh, "mesh_draw_victory_dwarf"),  # specific victory-loss image: dwarves VS anything
		(else_try),
			# evil men VS anything
			(eq, ":winning_side_race", tf_evil_man ),
			(set_background_mesh, "mesh_draw_victory_evilman"),  # specific victory-loss image: evil men VS anything
		(else_try),
			(eq, ":winning_side_faction", "fac_gondor" ),
			(set_background_mesh, "mesh_draw_victory_gondor"), # specific victory-loss image: gondor VS anything
		(else_try),
			(eq, ":winning_side_faction", "fac_rohan" ),
			(set_background_mesh, "mesh_draw_victory_rohan"), # specific victory-loss image: rohan VS anything
		(else_try),
			(eq, ":winning_side_faction", "fac_imladris" ),
			(set_background_mesh, "mesh_draw_victory_rivendell"), # specific victory-loss image: rivendell VS anything
		(else_try),
			(eq, ":winning_side_faction", "fac_woodelf" ),
			(set_background_mesh, "mesh_draw_victory_mirkwood"), # specific victory-loss image: mirkwood VS anything
		(else_try),
			(eq, ":winning_side_faction", "fac_dunland" ),
			(set_background_mesh, "mesh_draw_victory_dunland"), # specific victory-loss image: dunland VS anything
		(else_try),
			(eq, ":winning_side_faction", "fac_khand" ),
			(set_background_mesh, "mesh_draw_victory_khand"), # specific victory-loss image: khand VS anything
		(else_try),
			(eq, ":winning_side_faction", "fac_harad" ),
			(set_background_mesh, "mesh_draw_victory_harad"), # specific victory-loss image: harad VS anything
		(else_try),
			(eq, ":winning_side_faction", "fac_rhun" ),
			(set_background_mesh, "mesh_draw_victory_rhun"), # specific victory-loss image: rhun VS anything
		(else_try),
			(eq, ":winning_side_faction", "fac_beorn" ),
			(set_background_mesh, "mesh_draw_victory_beornings"), # specific victory-loss image: beorn VS anything
		(else_try),
			(eq, ":winning_side_faction", "fac_umbar" ),
			(set_background_mesh, "mesh_draw_victory_corsairs"), # specific victory-loss image: umbar VS anything
		(else_try),
			(eq, ":winning_side_race", tf_elf_begin),
			(eq, ":losing_side_race_group", tf_orc ),
			(set_background_mesh, "mesh_draw_lorien_arrows"),  # specific victory-loss image: elves VS orcs 
		(else_try),
			# generic  defeat image: orcs....
			(eq, "$g_battle_result", -1), (eq, "$player_looks_like_an_orc", 1),
			(set_background_mesh,  "mesh_draw_defeat_orc"), 
		(else_try),
			# generic  defeat image: anybody else....
			(eq, "$g_battle_result", -1), (neq, "$player_looks_like_an_orc", 1),
			(set_background_mesh,  "mesh_draw_defeat_human"), 
		(try_end),
		
		# special case override: ent image 
		(try_begin),  
			(eq, "$g_encountered_party", "p_legend_fangorn"),
			(eq, "$g_battle_result", -1),
			# override the victory image with this ent image 
			(store_add, reg10, "$player_looks_like_an_orc", "mesh_draw_ent_attack"), (set_background_mesh, reg10),
		(try_end),
	 (try_end),
	 
	 (str_clear, s11),
     (try_begin),
       (eq, "$g_battle_result", 1),
       (eq, "$g_enemy_fit_for_battle", 0),
       (str_store_string, s11, "@You were victorious!"),
#       (play_track, "track_bogus"), #clear current track.
#       (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
       #(try_begin),
			#(gt, "$g_friend_fit_for_battle", 1),
			#(set_background_mesh, "mesh_pic_victory"),

       #(try_end),
     (else_try),
       (eq, "$g_battle_result", -1),
       (ge, "$g_enemy_fit_for_battle",1),
       (this_or_next|le, "$g_friend_fit_for_battle",0),
       (             le, "$playerparty_postbattle_regulars", 0),
       (str_store_string, s11, "@The battle was lost. Your forces were utterly crushed."),
       #(set_background_mesh, "mesh_ui_default_menu_window"),
	   #(set_background_mesh, "mesh_pic_defeat"),
     (else_try),
       (eq, "$g_battle_result", -1),
       (str_store_string, s11, "@Your companions carry you away from the fighting."),
       #(troop_get_type, ":is_female", "trp_player"),
       #(try_begin),
       #  (eq, ":is_female", tf_female),
         #(set_background_mesh, "mesh_pic_wounded_fem"),
       #(else_try),
         #(set_background_mesh, "mesh_pic_wounded"),
       #(try_end),
     (else_try),
       (eq, "$g_battle_result", 1),
       (str_store_string, s11, "@You have defeated the enemy."),
       #(try_begin),
       #  (gt, "$g_friend_fit_for_battle", 1),
         #(set_background_mesh, "mesh_pic_victory"),
       #(try_end),
     (else_try),
       (eq, "$g_battle_result", 0),
       (str_store_string, s11, "@You have retreated from the fight."),
     (try_end),
#NPC companion changes begin
#check for excessive casualties, more forgiving if battle result is good
     (try_begin),
       (gt, "$playerparty_prebattle_regulars", 9),
       (store_add, ":divisor", 3, "$g_battle_result"), 
       (store_div, ":half_of_prebattle_regulars", "$playerparty_prebattle_regulars", ":divisor"),
       (lt, "$playerparty_postbattle_regulars", ":half_of_prebattle_regulars"),
       (call_script, "script_objectionable_action", tmt_egalitarian, "str_excessive_casualties"),
     (try_end),
#NPC companion changes end

	
     (call_script, "script_print_casualties_to_s0", "p_player_casualties", 0),
     (str_store_string_reg, s8, s0),
     (call_script, "script_print_casualties_to_s0", "p_enemy_casualties", 0),
     (str_store_string_reg, s9, s0),
     (str_clear, s10),
     (try_begin),
       (eq, "$any_allies_at_the_last_battle", 1),
       (call_script, "script_print_casualties_to_s0", "p_ally_casualties", 0),
       (str_store_string, s10, "@^^Ally Casualties:{s0}"),
     (try_end),
	 # # kill troll quest (mtarini)
     # (try_begin),
       # (check_quest_active, "qst_kill_troll"),
       # (eq, "$g_battle_result", 1),
	   # (quest_get_slot, ":quest_object_troop","qst_kill_troll", slot_quest_target_party),
	   # (eq, ":quest_object_troop", "$g_enemy_party"),
	   # (call_script, "script_succeed_quest", "qst_kill_troll"),
     # (try_end),
    ],
	[
	 #options for players:
	 # capture troll quest troll quest (mtarini)
	 ("inspect_troll",
	  [(eq, "$g_battle_result", 1),
	   (check_quest_active, "qst_capture_troll"),
	   (party_get_template_id, ":j", "$g_enemy_party"),(eq,":j","pt_wild_troll"),
	  ],"Inspect downed troll",[ (jump_to_menu, "mnu_can_capture_troll")]) ,
	  
     ("continue",[],"Continue...",
	[
		(try_begin),
			(gt, "$g_next_menu", -1),
			(jump_to_menu, "$g_next_menu"),
		(else_try),
            		(change_screen_return),
		(try_end),
		(try_begin),(call_script, "script_cf_spawn_routed_parties"),(try_end),  
	]),
	],
 ),

( "total_victory",0,
    "You shouldn't be reading this... {s9}",
    "none",
    [   # We exploit the menu condition system below.
        # The conditions should make sure that always another screen or menu is called.
        (assign, ":done", 0),

	(try_begin),
		(ge, "$battle_won", 0), # (CppCoder): Battle was won, or was neutral
					# (CppCoder): Gonna do more testing, is this required? Even if a battle is lost, shouldn't the troops spawn?
		(call_script, "script_cf_spawn_routed_parties"), 
	(try_end),  
					  
		(assign, ":ambient_faction_backup", "$ambient_faction"), #TLD
        
        (try_begin),
          # Talk to ally leader
          (eq, "$thanked_by_ally_leader", 0),
          (assign, "$thanked_by_ally_leader", 1),
          
#TLD begin - do this only once
		  # select what friendly faction was most interested in this victory (mtarini)
		  (assign, "$impressed_faction", "$players_kingdom"), # by default, it is player starting fatcion
		  (store_faction_of_party, ":defeated_faction", "$g_enemy_party"),
		
	      (str_store_faction_name, s4, ":defeated_faction"),
          #(display_log_message, "@DEBUG: player defeated a party of faction {s4}."),

		  (call_script, "script_find_closest_enemy_town_or_host", ":defeated_faction", "p_main_party"),
          (assign, ":impressed_party", reg0),
		
		  (try_begin),
			  (ge, ":impressed_party", 0),
			  (str_store_party_name, s3, ":impressed_party"),
			  (store_faction_of_party, "$impressed_faction", ":impressed_party"),
			  (try_begin),
                (is_between, ":impressed_party", centers_begin, centers_end), 
                (display_log_message, "@News of your victory against {s4} reach {s3}.", color_good_news),
                
			  (else_try), 
				(display_log_message, "@{s3} witnesses your victory against {s4}.", color_good_news),
			  (try_end), 
              (store_div, ":rank_increase", "$battle_renown_total", 2), # MV: give some rank increase according to renown (should be small 1-10) #was 4, now (1-20)
#(display_message, "@Debug: giving rank points for impressed faction."),		  
              (call_script, "script_increase_rank", "$impressed_faction", ":rank_increase"),
		  (else_try),
			  #(display_log_message, "@DEBUG: nobody directly interested witnesses your victory."),
		  (try_end),
		  (call_script, "script_set_ambient_faction","$impressed_faction"),
          
          # Bravery trait check (chance greater if outnumbered; uses battle_renown_value=0-50 to figure it out)
		  (try_begin),
            (ge, "$battle_renown_value", 20), #minimum renown for being outnumbered
            (troop_slot_eq, "trp_traits", slot_trait_bravery, 0),
            (store_random_in_range, ":random", 0, 100),
            (ge, "$battle_renown_value", ":random"),
            (call_script, "script_gain_trait", slot_trait_bravery),
		  (try_end),
          
#TLD end
          
          (gt, "$g_ally_party", 0),
          
          (store_add, ":total_str_without_player", "$g_starting_strength_friends", "$g_starting_strength_enemy_party"),
          (val_sub, ":total_str_without_player", "$g_starting_strength_main_party"),
          (store_sub, ":ally_strength_without_player", "$g_starting_strength_friends", "$g_starting_strength_main_party"),
          (store_mul, ":ally_advantage", ":ally_strength_without_player", 100),
          (val_add, ":total_str_without_player", 1),
          (val_div, ":ally_advantage", ":total_str_without_player"),
          #Ally advantage=50  means battle was evenly matched

          (store_sub, ":enemy_advantage", 100, ":ally_advantage"),
        
          (store_mul, ":faction_reln_boost", ":enemy_advantage", "$g_starting_strength_enemy_party"),
          (val_div, ":faction_reln_boost", 300),
          (val_min, ":faction_reln_boost", 50), #was 40 in 3.1 
          (val_div, ":faction_reln_boost", 2), #MV: nerf to be close to normal battles - MV: upped a bit after 3.1 - MV: not used at all in 3.15, back to renown

          (store_mul, "$g_relation_boost", ":enemy_advantage", ":enemy_advantage"),
          (val_div, "$g_relation_boost", 700),
          (val_clamp, "$g_relation_boost", 0, 20),
        
          (party_get_num_companion_stacks, ":num_ally_stacks", "$g_ally_party"),
          (gt, ":num_ally_stacks", 0), # anybody survived
          (store_faction_of_party, ":ally_faction","$g_ally_party"),
          
          (store_div, ":rank_increase", "$battle_renown_total", 5), # MV: give some rank increase according to renown (should be small 1-10) #was 4, now (1-20)
#(display_message, "@Debug: giving rank points for helping allies."),		  
		  (call_script, "script_increase_rank", ":ally_faction", "$g_relation_boost"), # MV - changed rank increase to renown calc
#		  (call_script, "script_increase_rank", ":ally_faction", ":faction_reln_boost"), # increase rank of helped faction (mtarini)
          #(call_script, "script_change_player_relation_with_faction", ":ally_faction", ":faction_reln_boost"),
          (party_stack_get_troop_id, ":ally_leader", "$g_ally_party"),
          (party_stack_get_troop_dna, ":ally_leader_dna", "$g_ally_party"),
          (try_begin),
            (troop_is_hero, ":ally_leader"),
            (troop_get_slot, ":hero_relation", ":ally_leader", slot_troop_player_relation),
            (assign, ":rel_boost", "$g_relation_boost"),
            (try_begin),
              (lt, ":hero_relation", -5),
              (val_div, ":rel_boost", 3),
            (try_end),
            (call_script,"script_change_player_relation_with_troop", ":ally_leader", ":rel_boost"),
          (try_end),
          (assign, "$talk_context", tc_ally_thanks),
          (call_script, "script_setup_troop_meeting",":ally_leader", ":ally_leader_dna"),
        (else_try),
          # Talk to enemy leaders
          (assign, ":done", 0),
          (party_get_num_companion_stacks, ":num_stacks", "p_encountered_party_backup"),
        
          (try_for_range, ":stack_no", "$last_defeated_hero", ":num_stacks"),
            (eq, ":done", 0),
            (party_stack_get_troop_id,   ":stack_troop","p_encountered_party_backup",":stack_no"),
            (party_stack_get_troop_dna,   ":stack_troop_dna","p_encountered_party_backup",":stack_no"),
            
            (troop_is_hero, ":stack_troop"),
            (store_add, "$last_defeated_hero", ":stack_no", 1),
        
            (call_script, "script_remove_troop_from_prison", ":stack_troop"),
            
            (troop_set_slot, ":stack_troop", slot_troop_leaded_party, -1),
            (store_troop_faction, ":defeated_faction", ":stack_troop"),

            (try_begin),
              (call_script, "script_cf_check_hero_can_escape_from_player", ":stack_troop"),
              (str_store_troop_name, s1, ":stack_troop"),
              (str_store_faction_name, s3, ":defeated_faction"),
              (str_store_string, s17, "@{s1} of {s3} managed to escape."),
              (display_log_message, "@{s17}"),
              (jump_to_menu, "mnu_enemy_slipped_away"),
              (assign, ":done", 1),
            (else_try),
              (assign, "$talk_context", tc_hero_defeated),
              (call_script, "script_setup_troop_meeting",":stack_troop", ":stack_troop_dna"),
              (assign, ":done", 1),
            (try_end),
          (try_end),
          (eq, ":done", 1),
        (else_try),
          # Talk to freed heroes
          (assign, ":done", 0),
          (party_get_num_prisoner_stacks, ":num_prisoner_stacks","p_encountered_party_backup"),
          (try_for_range, ":stack_no", "$last_freed_hero", ":num_prisoner_stacks"),
            (eq, ":done", 0),
            (party_prisoner_stack_get_troop_id,   ":stack_troop","p_encountered_party_backup",":stack_no"),
            (troop_is_hero, ":stack_troop"),
            (party_prisoner_stack_get_troop_dna,   ":stack_troop_dna","p_encountered_party_backup",":stack_no"),
            (store_add, "$last_freed_hero", ":stack_no", 1),
            (assign, "$talk_context", tc_hero_freed),
            (call_script, "script_setup_troop_meeting",":stack_troop", ":stack_troop_dna"),
            (assign, ":done", 1),
          (try_end),
          (eq, ":done", 1),
        (else_try),
          (eq, "$capture_screen_shown", 0),
          (assign, "$capture_screen_shown", 1),
          (party_clear, "p_temp_party"),

		  (party_set_faction, "p_temp_party", "$players_kingdom"),  # mtarini: need this to avoid to free enemyes
		
          (assign, "$g_move_heroes", 0),
          (call_script, "script_party_prisoners_add_party_companions", "p_temp_party", "p_collective_enemy"),
          (call_script, "script_party_add_party_prisoners", "p_temp_party", "p_collective_enemy"),

          (try_begin),
            (call_script, "script_party_calculate_strength", "p_collective_friends_backup",0),
            (assign,":total_initial_strength", reg(0)),
            (gt, ":total_initial_strength", 0),
#            (gt, "$g_ally_party", 0),
            (call_script, "script_party_calculate_strength", "p_main_party_backup",0),
            (assign,":player_party_initial_strength", reg(0)),
            # move ally_party_initial_strength/(player_party_initial_strength + ally_party_initial_strength) prisoners to ally party.
            # First we collect the share of prisoners of the ally party and distribute those among the allies.
            (store_sub, ":ally_party_initial_strength", ":total_initial_strength", ":player_party_initial_strength"),


#            (call_script, "script_party_calculate_strength", "p_ally_party_backup"),
#            (assign,":ally_party_initial_strength", reg(0)),
#            (store_add, ":total_initial_strength", ":player_party_initial_strength", ":ally_party_initial_strength"),
            (store_mul, ":ally_share", ":ally_party_initial_strength", 1000),
            (val_div, ":ally_share", ":total_initial_strength"),
            (assign, "$pin_number", ":ally_share"), #we send this as a parameter to the script.
            (party_clear, "p_temp_party_2"),
            (call_script, "script_move_members_with_ratio", "p_temp_party", "p_temp_party_2"),
        
            #TODO: This doesn't handle prisoners if our allies joined battle after us.
            (try_begin),
              (gt, "$g_ally_party", 0),
              (distribute_party_among_party_group, "p_temp_party_2", "$g_ally_party"),
            (try_end),
             #next if there's anything left, we'll open up the party exchange screen and offer them to the player.
          (try_end),

          
          (party_get_num_companions, ":num_rescued_prisoners", "p_temp_party"),
          (try_begin),
            (check_quest_active, "qst_rescue_prisoners"),
            (quest_set_slot, "qst_rescue_prisoners", slot_quest_target_center, ":num_rescued_prisoners"), #abusing a slot as a global
          (try_end),
		  
		  
          (party_get_num_prisoners,  ":num_captured_enemies", "p_temp_party"),
          (store_add, ":total_capture_size", ":num_rescued_prisoners", ":num_captured_enemies"),
          (gt, ":total_capture_size", 0),
          (change_screen_exchange_with_party, "p_temp_party"),
        (else_try),
          (eq, "$loot_screen_shown", 0),
          (assign, "$loot_screen_shown", 1),
          
          (try_begin),
            (check_quest_active, "qst_rescue_prisoners"),
            (neg|check_quest_succeeded, "qst_rescue_prisoners"),
            (neg|check_quest_failed, "qst_rescue_prisoners"),
            (quest_get_slot, ":available", "qst_rescue_prisoners", slot_quest_target_center), #before...
            (party_get_num_companions, ":not_rescued", "p_temp_party"), #...and after
            (store_sub, ":rescued", ":available", ":not_rescued"),
            (gt, ":rescued", 0), #ignore dismissing troops
            (quest_get_slot, ":total_rescued", "qst_rescue_prisoners", slot_quest_current_state),
            (val_add, ":total_rescued", ":rescued"),
            (quest_set_slot, "qst_rescue_prisoners", slot_quest_current_state, ":total_rescued"),
            (assign, reg1, ":total_rescued"),
            (str_store_string, s2, "@Prisoners rescued so far: {reg1}"),
            (add_quest_note_from_sreg, "qst_rescue_prisoners", 3, s2, 0),
            (quest_get_slot, ":quest_target_amount", "qst_rescue_prisoners", slot_quest_target_amount),
            (try_begin),
              (ge, ":total_rescued", ":quest_target_amount"),
              (call_script, "script_succeed_quest", "qst_rescue_prisoners"),
            (try_end),
          (try_end),

          (try_begin),
            (gt, "$g_ally_party", 0),
            (call_script, "script_party_add_party", "$g_ally_party", "p_temp_party"), #Add remaining prisoners to ally TODO: FIX it.
          (else_try),
            (party_get_num_attached_parties, ":num_quick_attachments", "p_main_party"),
            (gt, ":num_quick_attachments", 0),
            (party_get_attached_party_with_rank, ":helper_party", "p_main_party", 0),
            (call_script, "script_party_add_party", ":helper_party", "p_temp_party"), #Add remaining prisoners to our reinforcements
          (try_end),
          (troop_clear_inventory, "trp_temp_troop"),
          (call_script, "script_party_calculate_loot", "p_encountered_party_backup"),
          (gt, reg0, 0),
          (troop_sort_inventory, "trp_temp_troop"),

	# Clean loot
	# This code cleans the inventory of other forbidden items, such as maggoty bread or human flesh
	 (troop_get_inventory_capacity, ":inv_cap", "trp_temp_troop"),
	 (try_for_range, ":i_slot", 0, ":inv_cap"),
		(troop_get_inventory_slot, ":item_id", "trp_temp_troop", ":i_slot"),
		(try_begin),
			(faction_slot_eq,"$players_kingdom", slot_faction_side, faction_side_good),
			(eq|this_or_next, ":item_id", "itm_human_meat"),
			(eq, ":item_id", "itm_maggoty_bread"),
        		(troop_remove_item, "trp_temp_troop", ":item_id"),
		(try_end),
	  (try_end),
          (troop_sort_inventory, "trp_temp_troop"),	  

          (change_screen_loot, "trp_temp_troop"),
        (else_try),
          #finished all
          (try_begin),
            (le, "$g_ally_party", 0),
            (end_current_battle),
          (try_end),
		  
		  
          (call_script, "script_party_give_xp_and_gold", "p_encountered_party_backup"),
          (try_begin),
            (eq, "$g_enemy_party", 0),
            (display_message,"str_error_string"),
          (try_end),
          (call_script, "script_event_player_defeated_enemy_party", "$g_enemy_party"),
          (call_script, "script_clear_party_group", "$g_enemy_party", "$players_kingdom"),
          (try_begin),
            (eq, "$g_next_menu", -1),

#NPC companion changes begin
           (call_script, "script_post_battle_personality_clash_check"),
#NPC companion changes end

#Post 0907 changes begin
        (party_stack_get_troop_id,   ":enemy_leader","p_encountered_party_backup",0),
        (try_begin),
            (is_between, ":enemy_leader", kingdom_heroes_begin, kingdom_heroes_end),
            (neg|is_between, "$g_encountered_party", centers_begin, centers_end),
            (store_troop_faction, ":enemy_leader_faction", ":enemy_leader"),

            (try_begin),
                (eq, "$g_ally_party", 0),
                (call_script, "script_add_log_entry", logent_lord_defeated_by_player, "trp_player",  -1, ":enemy_leader", ":enemy_leader_faction"),
                (try_begin),
                  (eq, "$cheat_mode", 1),
                  (display_message, "@Victory comment. Player was alone"),
                (try_end),
            (else_try),
                (ge, "$g_strength_contribution_of_player", 40), 
                (call_script, "script_add_log_entry", logent_lord_defeated_by_player, "trp_player",  -1, ":enemy_leader", ":enemy_leader_faction"),
                (try_begin),
                  (eq, "$cheat_mode", 1),
                  (display_message, "@Ordinary victory comment. The player provided at least 40 percent forces."),
                (try_end),
            (else_try),
                (gt, "$g_starting_strength_enemy_party", 1000),
                (call_script, "script_get_closest_center", "p_main_party"),
                (assign, ":battle_of_where", reg0),
                (call_script, "script_add_log_entry", logent_player_participated_in_major_battle, "trp_player",  ":battle_of_where", -1, ":enemy_leader_faction"),
                (try_begin),
                  (eq, "$cheat_mode", 1),
                  (display_message, "@Player participation comment. The enemy had at least 1k starting strength."),
                (try_end),
            (else_try),
                (eq, "$cheat_mode", 1),
                (display_message, "@No victory comment. The battle was small, and the player provided less than 40 percent of allied strength"),
            (try_end),
        (try_end),
#Post 0907 changes end
            (val_add, "$g_total_victories", 1),
            
            # MV: handle post-victory quest checks
            (try_begin),
              # fail if messenger died in a battle
              (check_quest_active, "qst_escort_messenger"),
              (quest_get_slot, ":quest_object_troop", "qst_escort_messenger", slot_quest_object_troop),
              (party_count_companions_of_type, ":amount", "p_main_party", ":quest_object_troop"),
              (eq, ":amount", 0),
              (call_script, "script_abort_quest", "qst_escort_messenger", 1),
              #(call_script, "script_change_player_honor", -5),
            (try_end),
            
            # kill troll quest
            (try_begin),
              (check_quest_active, "qst_kill_troll"),
              (quest_get_slot, ":troll_party", "qst_kill_troll", slot_quest_target_party),
              (try_begin),
                (eq, ":troll_party", "$g_enemy_party"),
                (call_script, "script_succeed_quest", "qst_kill_troll"),
              (else_try),
                (party_get_num_attached_parties, ":num_attached_parties",  "$g_enemy_party"),
                (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
                  (party_get_attached_party_with_rank, ":attached_party", "$g_enemy_party", ":attached_party_rank"),
                  (eq, ":troll_party", ":attached_party"),
                  (call_script, "script_succeed_quest", "qst_kill_troll"),
                (try_end),
              (try_end),
            (try_end),

		# Spawn routed parties after battle. -CC
		(try_begin),(call_script, "script_cf_spawn_routed_parties"),(try_end),    

            (leave_encounter),
            (change_screen_return),
          (else_try),
            (jump_to_menu, "$g_next_menu"),
          (try_end),
        (try_end),
		
		(call_script, "script_set_ambient_faction",":ambient_faction_backup"),
		
		# TLD injure your KO-ed companions
		(try_begin),
			(eq, "$tld_option_injuries",1),
			(try_for_range, ":npc",companions_begin,companions_end), # assume companions are always in our main party, if ever spawned on battlefield
				(main_party_has_troop,":npc"),
				(troop_slot_eq, ":npc", slot_troop_wounded, 1), # was wounded in this battle?
				(troop_set_slot,":npc", slot_troop_wounded, 0),
				(store_random_in_range, reg12,0,10),
				(eq,reg12,0), #10% chance for injury
				(call_script,"script_injury_routine", ":npc"), # chances to get injury halved when victory
			(try_end),
		(try_end),
      ],
    [("continue",[],"Continue...",[(change_screen_return)]),]
 ),
( "enemy_slipped_away",0,
    "^^^^^{s17}",
    "none",
    [],
    [("continue",[],"Continue...",[(jump_to_menu,"mnu_total_victory")]),]
 ),
( "total_defeat",0,
    "You shouldn't be reading this...",
    "none",
    [     (play_track, "track_captured", 1),
          # Free prisoners
          (party_get_num_prisoner_stacks, ":num_prisoner_stacks","p_main_party"),
          (try_for_range, ":stack_no", 0, ":num_prisoner_stacks"),
            (party_prisoner_stack_get_troop_id, ":stack_troop","p_main_party",":stack_no"),
            (troop_is_hero, ":stack_troop"),
            (call_script, "script_remove_troop_from_prison", ":stack_troop"),
          (try_end),

          (call_script, "script_loot_player_items", "$g_enemy_party"),
          (assign, "$g_move_heroes", 0),
          (party_clear, "p_temp_party"),
		  (store_faction_of_party, ":fac","$g_enemy_party"),
		  (party_set_faction, "p_temp_party", ":fac"),

          (call_script, "script_party_add_party_prisoners", "p_temp_party", "p_main_party"),
          (call_script, "script_party_prisoners_add_party_companions", "p_temp_party", "p_main_party"),
          (distribute_party_among_party_group, "p_temp_party", "$g_enemy_party"),
        
          (call_script, "script_party_remove_all_companions", "p_main_party"),
          (assign, "$g_move_heroes", 1),
          (call_script, "script_party_remove_all_prisoners", "p_main_party"),

          (val_add, "$g_total_defeats", 1),
            
          # MV: handle post-defeat quest checks
          (try_begin),
            (check_quest_active, "qst_escort_messenger"),
            (call_script, "script_abort_quest", "qst_escort_messenger", 1),
            #(call_script, "script_change_player_honor", -5),
          (try_end),

          (try_begin),
            (store_random_in_range, ":random_no", 0, 100),
            (ge, ":random_no", "$g_player_luck"),
            (jump_to_menu, "mnu_permanent_damage"),
          (else_try),
            (try_begin),
              (eq, "$g_next_menu", -1),
              (leave_encounter),
              (change_screen_return),
            (else_try),
              (jump_to_menu, "$g_next_menu"),
            (try_end),
          (try_end),
          (try_begin),
            (gt, "$g_ally_party", 0),
            (call_script, "script_party_wound_all_members", "$g_ally_party"),
          (try_end),

	#Troop commentary changes begin
          (party_get_num_companion_stacks, ":num_stacks", "p_encountered_party_backup"),
          (try_for_range, ":stack_no", 0, ":num_stacks"),
            (party_stack_get_troop_id,   ":stack_troop","p_encountered_party_backup",":stack_no"),
            (is_between, ":stack_troop", kingdom_heroes_begin, kingdom_heroes_end),
            (store_troop_faction, ":victorious_faction", ":stack_troop"),
            (call_script, "script_add_log_entry", logent_player_defeated_by_lord, "trp_player",  -1, ":stack_troop", ":victorious_faction"),
          (try_end),
	#Troop commentary changes end
			# TLD injure your KO-ed companions
			(try_begin),
				(eq, "$tld_option_injuries",1),
				(try_for_range, ":npc",companions_begin,companions_end), # assume companions are always in our main party, if ever spawned on battlefield
					(main_party_has_troop,":npc"),
					(troop_slot_eq, ":npc", slot_troop_wounded, 1), # was wounded in this battle?
					(troop_set_slot,":npc", slot_troop_wounded, 0),
					(store_random_in_range, reg12,0,5),
					(eq,reg12,0), #20% chance for injury
					(call_script, "script_injury_routine", ":npc"),
				(try_end),
			(try_end),
      ],
    []
 ),

( "permanent_damage",mnf_disable_all_keys,
    "^^^^^{s0}",
    "none",
    [ (assign, ":end_cond", 1),
      (try_for_range, ":unused", 0, ":end_cond"),
        (store_random_in_range, ":random_attribute", 0, 4),
        (store_attribute_level, ":attr_level", "trp_player", ":random_attribute"),
        (try_begin),
          (gt, ":attr_level", 3),
          (neq, ":random_attribute", ca_charisma),
          (try_begin),
            (eq, ":random_attribute", ca_strength),
            (str_store_string, s0, "@Some of your tendons have been damaged in the battle. You lose 1 strength."),
          (else_try),
            (eq, ":random_attribute", ca_agility),
            (str_store_string, s0, "@You took a nasty wound which will cause you to limp slightly even after it heals. Your lose 1 agility."),
##          (else_try),
##            (eq, ":random_attribute", ca_charisma),
##            (str_store_string, s0, "@After the battle you are aghast to find that one of the terrible blows you suffered has left a deep, disfiguring scar on your face, horrifying those around you. Your charisma is reduced by 1."),
          (else_try),
##            (eq, ":random_attribute", ca_intelligence),
            (str_store_string, s0, "@You have trouble thinking straight after the battle, perhaps from a particularly hard hit to your head, and frequent headaches now plague your existence. Your intelligence is reduced by 1."),
          (try_end),
        (else_try),
          (lt, ":end_cond", 200),
          (val_add, ":end_cond", 1),
        (try_end),
      (try_end),
      (try_begin),
        (eq, ":end_cond", 200),
        (try_begin),
          (eq, "$g_next_menu", -1),
          (leave_encounter),
          (change_screen_return),
        (else_try),
          (jump_to_menu, "$g_next_menu"),
        (try_end),
      (else_try),
        (troop_raise_attribute, "trp_player", ":random_attribute", -1),
      (try_end),
      ],
    [
      ("s0",
       [
         (store_random_in_range, ":random_no", 0, 4),
         (try_begin),
           (eq, ":random_no", 0),
           (str_store_string, s0, "@Perhaps I'm getting unlucky..."),
         (else_try),
           (eq, ":random_no", 1),
           (str_store_string, s0, "@Retirement is starting to sound better and better."),
         (else_try),
           (eq, ":random_no", 2),
           (str_store_string, s0, "@No matter! I will persevere!"),
         (else_try),
           (eq, ":random_no", 3),
           (troop_get_type, ":is_female", "trp_player"),
           (try_begin),
             (eq, ":is_female", 1),
             (str_store_string, s0, "@What did I do to deserve this?"),
           (else_try),
             (str_store_string, s0, "@I suppose it'll make for a good story, at least..."),
           (try_end),
         (try_end),
         ],
       "{s0}",
       [
         (try_begin),
           (eq, "$g_next_menu", -1),
           (leave_encounter),
           (change_screen_return),
         (else_try),
           (jump_to_menu, "$g_next_menu"),
         (try_end),
         ]),
      ]
 ),
  
( "pre_join",0,
    "^^^^^You come across a battle between {s2} and {s1}. You decide to...",
    "none",
    [ (str_store_party_name, 1,"$g_encountered_party"),
      (str_store_party_name, 2,"$g_encountered_party_2"),
    ],
    [ ("pre_join_help_attackers",
	  [   (store_faction_of_party, ":attacker_faction", "$g_encountered_party_2"),
          (store_relation, ":attacker_relation", ":attacker_faction", "fac_player_supporters_faction"),
          (store_faction_of_party, ":defender_faction", "$g_encountered_party"),
          (store_relation, ":defender_relation", ":defender_faction", "fac_player_supporters_faction"),
          (ge, ":attacker_relation", 0),
          (lt, ":defender_relation", 0),
          ],
          "Move in to help the {s2}.",[
              (select_enemy,0),
              (assign,"$g_enemy_party","$g_encountered_party"),
              (assign,"$g_ally_party","$g_encountered_party_2"),
              (jump_to_menu,"mnu_join_battle")]),
      ("pre_join_help_defenders",[
          (store_faction_of_party, ":attacker_faction", "$g_encountered_party_2"),
          (store_relation, ":attacker_relation", ":attacker_faction", "fac_player_supporters_faction"),
          (store_faction_of_party, ":defender_faction", "$g_encountered_party"),
          (store_relation, ":defender_relation", ":defender_faction", "fac_player_supporters_faction"),
          (ge, ":defender_relation", 0),
          (lt, ":attacker_relation", 0),
          ],
          "Rush to the aid of the {s1}.",[
              (select_enemy,1),
              (assign,"$g_enemy_party","$g_encountered_party_2"),
              (assign,"$g_ally_party","$g_encountered_party"),
              (jump_to_menu,"mnu_join_battle")]),
      ("pre_join_leave",[],"Don't get involved.",[(leave_encounter),(change_screen_return)]),
    ]
 ),
( "join_battle",mnf_enable_hot_keys,
    "^^^You are helping {s2} against {s1}.^ You have {reg22} troops fit for battle against the enemy's {reg11}.^^The battle is taking place in {s3}{s4}.",
    "none",
    [(set_background_mesh, "mesh_ui_default_menu_window"),
	
		#(party_get_current_terrain, "$current_player_terrain","p_main_party"),
		#(call_script, "script_get_region_of_party","p_main_party"),(assign, "$current_player_region", reg1),	
		#(call_script, "script_get_close_landmark","p_main_party"), (assign, "$current_player_landmark", reg0),
		
		(store_add, reg2, str_shortname_region_begin, "$current_player_region"),
		(str_store_string,s3,reg2),
		
		(str_clear, s4),
		(try_begin), 
			(call_script, "script_cf_store_landmark_description_in_s17", "$current_player_landmark"),
			(str_store_string,s4,"@, {s17}"), 
		(try_end),
		
		(str_store_party_name, 1,"$g_enemy_party"),
        (str_store_party_name, 2,"$g_ally_party"),
        (call_script, "script_encounter_calculate_fit"),
        (assign, reg22, reg10), 

        (try_begin),
          (eq, "$new_encounter", 1),
          (assign, "$new_encounter", 0),
          (call_script, "script_encounter_init_variables"),
##          (assign, "$capture_screen_shown", 0),
##          (assign, "$loot_screen_shown", 0),
##          (assign, "$g_battle_result", 0),
##          (assign, "$cant_leave_encounter", 0),
##          (assign, "$last_defeated_hero", 0),
##          (assign, "$last_freed_hero", 0),
##          (call_script, "script_party_copy", "p_main_party_backup", "p_main_party"),
##          (call_script, "script_party_copy", "p_encountered_party_backup", "p_collective_enemy"),
##          (call_script, "script_party_copy", "p_ally_party_backup", "p_collective_ally"),
        (else_try), #second or more turn
          (eq, "$g_leave_encounter",1),
          (change_screen_return),
        (try_end),

        (try_begin),
          (call_script, "script_party_count_members_with_full_health","p_collective_enemy"),
          (assign, ":num_enemy_regulars_remaining", reg(0)),
          (assign, ":enemy_finished",0),
          (try_begin),
            (eq, "$g_battle_result", 1),
            (eq, ":num_enemy_regulars_remaining", 0), #battle won
            (assign, ":enemy_finished",1),
          (else_try),
            (eq, "$g_engaged_enemy", 1),
            (le, "$g_enemy_fit_for_battle",0),
            (ge, "$g_friend_fit_for_battle",1),
            (assign, ":enemy_finished",1),
          (try_end),
          (this_or_next|eq, ":enemy_finished",1),
          (eq,"$g_enemy_surrenders",1),
          (assign, "$g_next_menu", -1),
          (jump_to_menu, "mnu_total_victory"),
        (else_try),
#          (eq, "$encountered_party_hostile", 1),
          (call_script, "script_party_count_members_with_full_health","p_collective_friends"),
          (assign, ":ally_num_soldiers", reg(0)),
          (assign, ":battle_lost", 0),
          (try_begin),
            (eq, "$g_battle_result", -1),
            (eq, ":ally_num_soldiers", 0), #battle lost
            (assign, ":battle_lost",1),
          (try_end),
          (this_or_next|eq, ":battle_lost",1),
          (eq,"$g_player_surrenders",1),
        # TODO: Split prisoners to all collected parties.
        # NO Need? Let default battle logic do it for us. 
#          (assign, "$g_move_heroes", 0),
#          (call_script, "script_party_add_party_prisoners", "$g_enemy_party", "p_collective_ally"),
#          (call_script, "script_party_prisoners_add_party_companions", "$g_enemy_party", "p_collective_ally"),
        #TODO: Clear all attached allies.
#          (call_script, "script_party_remove_all_companions", "$g_ally_party"),
#          (call_script, "script_party_remove_all_prisoners", "$g_ally_party"),
          (leave_encounter),
          (change_screen_return),
        (try_end),
        
      ],
    [ ("join_attack",[
#          (neq, "$encountered_party_hostile", 0),
          (neg|troop_is_wounded, "trp_player"),
##          (store_troop_health,reg(5),"trp_player"),
##          (ge,reg(5),20),
          ],
                            "Charge the enemy.",[
                                (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
                                (assign, "$g_battle_result", 0),
                                (call_script, "script_calculate_renown_value"),
                                (call_script, "script_calculate_battle_advantage"),(set_battle_advantage, reg0),
                                (call_script, "script_calculate_battleside_races"),
                                
                                (set_party_battle_mode),
                                (set_jump_mission,"mt_lead_charge"),
								
                                (call_script, "script_jump_to_random_scene","$current_player_region","$current_player_terrain","$current_player_landmark"),
                                (assign, "$g_next_menu", "mnu_join_battle"),
                                (jump_to_menu, "mnu_battle_debrief"),
                                (change_screen_mission),
                                ]),

      ("join_order_attack",[
#          (gt, "$encountered_party_hostile", 0),
          (call_script, "script_party_count_members_with_full_health", "p_main_party"),(ge, reg(0), 3),
          ],
           "Order your troops to attack with your allies while you stay back.",[(party_set_next_battle_simulation_time, "$g_encountered_party", -1),
                                                                         (jump_to_menu,"mnu_join_order_attack"),
                                                            ]),
      
#      ("join_attack",[],"Lead a charge against the enemies",[(set_jump_mission,"mt_charge_with_allies"),
#                                (call_script, "script_setup_random_scene"),
#                                                             (change_screen_mission,0)]),
      ("join_leave",[],"Disengage.",[
        (try_begin),
           (neg|troop_is_wounded, "trp_player"),
           (call_script, "script_objectionable_action", tmt_aristocratic, "str_flee_battle"),
           (party_stack_get_troop_id, ":enemy_leader","$g_enemy_party",0),
           (call_script, "script_add_log_entry", logent_player_retreated_from_lord, "trp_player",  -1, ":enemy_leader", -1),
           (display_message, "@You retreated from battle."),
        (try_end),
        (leave_encounter),(change_screen_return)]),
		  
    ("join_cheat_heal",[
         (eq, "$cheat_mode",1),
		 (store_troop_health  , reg20, "trp_player",0), (lt, reg20,95),
          ],"CHEAT: heal yourself.",[
		    (troop_set_health  , "trp_player",100),
	        (display_message, "@CHEAT: healed!!!"),
			(jump_to_menu, "mnu_pre_join"),
		]),

    ]
 ),
( "join_order_attack",mnf_disable_all_keys,
    "{s4}^^Your casualties: {s8}^^Allies' casualties: {s9}^^Enemy casualties: {s10}",
    "none",
    [	(set_background_mesh, "mesh_ui_default_menu_window"),

	    	(call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
		(assign, ":player_party_strength", reg0),
		(val_div, ":player_party_strength", 5),

		(call_script, "script_party_calculate_strength", "p_collective_friends", 0),
		(assign, ":friend_party_strength", reg0),
		(val_div, ":friend_party_strength", 5),
		
		(call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
		(assign, ":enemy_party_strength", reg0),
		(val_div, ":enemy_party_strength", 5),

		(assign, ":enemy_party_strength_for_p", ":enemy_party_strength"),
		(val_mul, ":enemy_party_strength_for_p", ":player_party_strength"),
		(val_div, ":enemy_party_strength_for_p", ":friend_party_strength"),

		(val_sub, ":enemy_party_strength", ":enemy_party_strength_for_p"),
		(inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength_for_p", "p_temp_casualties"),
		(call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
		(str_store_string_reg, s8, s0),
		
		(inflict_casualties_to_party_group, "$g_enemy_party", ":friend_party_strength", "p_temp_casualties"),
		(call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
		(str_store_string_reg, s10, s0),
		
		(call_script, "script_collect_friendly_parties"),
#                                    (party_collect_attachments_to_party, "$g_ally_party", "p_collective_ally"),

		(inflict_casualties_to_party_group, "$g_ally_party", ":enemy_party_strength", "p_temp_casualties"),
		(call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
		(str_store_string_reg, s9, s0),
		(party_collect_attachments_to_party, "$g_enemy_party", "p_collective_enemy"),

#                                    (assign, "$cant_leave_encounter", 0),
		(assign, "$no_soldiers_left", 0),
		(try_begin),
		  (call_script, "script_party_count_members_with_full_health","p_main_party"),
		  (le, reg(0), 0),
		  (assign, "$no_soldiers_left", 1),
		  (str_store_string, s4, "str_join_order_attack_failure"),
		(else_try),
		  (call_script, "script_party_count_members_with_full_health","p_collective_enemy"),
		  (le, reg(0), 0),
		  (assign, "$g_battle_result", 1),
		  (assign, "$no_soldiers_left", 1),
		  (str_store_string, s4, "str_join_order_attack_success"),
		(else_try),
		  (str_store_string, s4, "str_join_order_attack_continue"),
		(try_end),
    ],
    [("continue",[],"Continue...",[(jump_to_menu,"mnu_join_battle")])]
 ),

( "test_scene",mnf_auto_enter,
    "You enter the test scene.",
    "none",
    [],
    [ ("enter",[],"Enter.",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_test_scene"],[change_screen_mission]]),
      ("leave",[],"Leave.",[(leave_encounter),(change_screen_return)]),
    ]
 ),

( "battlefields",0,
    "^^^^^^^^^Select a field...",
    "none",
    [],
    [ ("enter_f1",[],"Field 1",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_field_1"],[change_screen_mission]]),
      ("enter_f2",[],"Field 2",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_field_2"],[change_screen_mission]]),
      ("enter_f3",[],"Field 3",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_field_3"],[change_screen_mission]]),
      ("enter_f4",[],"Field 4",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_field_4"],[change_screen_mission]]),
      ("enter_f5",[],"Field 5",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_field_5"],[change_screen_mission]]),
      ("leave",[],"Leave.",[(leave_encounter),(change_screen_return)]),
    ]
 ),

( "join_siege_outside",0,
    "^^^^^^{s1} has come under siege by {s2}.",
    "none",
    code_to_set_city_background + [ 
	    (str_store_party_name, s1, "$g_encountered_party"),
        (str_store_party_name, s2, "$g_encountered_party_2"),
    ],
    [ ("approach_besiegers",[(store_faction_of_party, ":faction_no", "$g_encountered_party_2"),
                             (store_relation, ":relation", ":faction_no", "fac_player_supporters_faction"),
                             (ge, ":relation", 0),
                             (store_faction_of_party, ":faction_no", "$g_encountered_party"),
                             (store_relation, ":relation", ":faction_no", "fac_player_supporters_faction"),
                             (lt, ":relation", 0),
                             ],"Approach the siege camp.",[
          (jump_to_menu, "mnu_besiegers_camp_with_allies"),
                                ]),
      ("pass_through_siege",[(store_faction_of_party, ":faction_no", "$g_encountered_party"),
                             (store_relation, ":relation", ":faction_no", "fac_player_supporters_faction"),
                             (ge, ":relation", 0),
                             ],"Pass through the siege lines and enter {s1}.",
       [
            (jump_to_menu,"mnu_cut_siege_without_fight"),
          ]),
      ("leave",[],"Leave.",[(leave_encounter),(change_screen_return)]),
    ]
 ),
( "cut_siege_without_fight",0,
    "The besiegers let you approach the gates without challenge.",
    "none",
    [(set_background_mesh, "mesh_ui_default_menu_window"),],
    [
      ("continue",[],"Continue...",[(try_begin),
                                   (this_or_next|eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
                                   (eq, "$g_encountered_party_faction", "$players_kingdom"),
                                   (jump_to_menu, "mnu_town"),
                                 (else_try),
                                   (jump_to_menu, "mnu_castle_outside"),
                                 (try_end)]),
      ]
 ),
( "besiegers_camp_with_allies",mnf_enable_hot_keys,
    "{s1} remains under siege. The banners of {s2} fly above the camp of the besiegers,\
    where you and your troops are welcomed.",
    "none",
    code_to_set_city_background + [
        (str_store_party_name, s1, "$g_encountered_party"),
        (str_store_party_name, s2, "$g_encountered_party_2"),
        (assign, "$g_enemy_party", "$g_encountered_party"),
        (assign, "$g_ally_party", "$g_encountered_party_2"),
        (select_enemy, 0),
        (call_script, "script_encounter_calculate_fit"),
        (try_begin),
          (eq, "$new_encounter", 1),
          (assign, "$new_encounter", 0),
          (call_script, "script_encounter_init_variables"),
        (try_end),

        (try_begin),
          (eq, "$g_leave_encounter",1),
          (change_screen_return),
        (else_try),
          (assign, ":enemy_finished", 0),
          (try_begin),
            (eq, "$g_battle_result", 1),
            (assign, ":enemy_finished", 1),
          (else_try),
            (le, "$g_enemy_fit_for_battle", 0),
            (ge, "$g_friend_fit_for_battle", 1),
            (assign, ":enemy_finished", 1),
          (try_end),
          (this_or_next|eq, ":enemy_finished", 1),
          (eq, "$g_enemy_surrenders", 1),
##          (assign, "$g_next_menu", -1),#"mnu_castle_taken_by_friends"),
##          (jump_to_menu, "mnu_total_victory"),
          (call_script, "script_party_wound_all_members", "$g_enemy_party"),
          (leave_encounter),
          (change_screen_return),
        (else_try),
          (call_script, "script_party_count_members_with_full_health", "p_collective_friends"),
          (assign, ":ally_num_soldiers", reg0),
          (eq, "$g_battle_result", -1),
          (eq, ":ally_num_soldiers", 0), #battle lost
          (leave_encounter),
          (change_screen_return),
        (try_end),
        ],
    [
      ("talk_to_siege_commander",[]," Request a meeting with the commander.",[
                                (modify_visitors_at_site,"scn_conversation_scene"),(reset_visitors),
                                (set_visitor,0,"trp_player"),
                                (party_stack_get_troop_id, ":siege_leader_id","$g_encountered_party_2",0),
                                (party_stack_get_troop_dna,":siege_leader_dna","$g_encountered_party_2",0),
                                (set_visitor,17,":siege_leader_id",":siege_leader_dna"),
                                (set_jump_mission,"mt_conversation_encounter"),
                                (jump_to_scene,"scn_conversation_scene"),
                                (assign, "$talk_context", tc_siege_commander),
                                (change_screen_map_conversation, ":siege_leader_id")]),
      ("join_siege_with_allies",[(neg|troop_is_wounded, "trp_player")], "Join the next assault.",
       [
           (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
           (try_begin),
             (check_quest_active, "qst_join_siege_with_army"),
             (quest_slot_eq, "qst_join_siege_with_army", slot_quest_target_center, "$g_encountered_party"),
             (add_xp_as_reward, 250),
             (call_script, "script_end_quest", "qst_join_siege_with_army"),
             #Reactivating follow army quest
             (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
             (str_store_troop_name_link, s9, ":faction_marshall"),
             (setup_quest_text, "qst_follow_army"),
             (str_store_string, s2, "@{s9} wants you to follow his army until further notice."),
             (call_script, "script_start_quest", "qst_follow_army", ":faction_marshall"),
             #(assign, "$g_player_follow_army_warnings", 0),
           (try_end),
           (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_walls),

           (call_script, "script_calculate_battle_advantage"),
           (val_mul, reg0, 2),
           (val_div, reg0, 3), #scale down the advantage a bit in sieges.
           (set_battle_advantage, reg0),
           (set_party_battle_mode),
           (set_jump_mission,"mt_castle_attack_walls_ladder"),
           (jump_to_scene,":battle_scene"),
           (assign, "$g_siege_final_menu", "mnu_besiegers_camp_with_allies"),
           (assign, "$g_siege_battle_state", 1),
           #(assign, "$g_next_menu", "mnu_castle_besiege_inner_battle"),
           (assign, "$g_next_menu", "mnu_besiegers_camp_with_allies"),
           (jump_to_menu, "mnu_battle_debrief"),
           (change_screen_mission),
          ]),
      ("join_siege_stay_back", [(call_script, "script_party_count_members_with_full_health", "p_main_party"),
                                (ge, reg0, 3),
                                ],
       "Order your soldiers to join the next assault without you.",
       [
         (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
         (try_begin),
           (check_quest_active, "qst_join_siege_with_army"),
           (quest_slot_eq, "qst_join_siege_with_army", slot_quest_target_center, "$g_encountered_party"),
           (add_xp_as_reward, 100),
           (call_script, "script_end_quest", "qst_join_siege_with_army"),
           #Reactivating follow army quest
           (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
           (str_store_troop_name_link, s9, ":faction_marshall"),
           (setup_quest_text, "qst_follow_army"),
           (str_store_string, s2, "@{s9} wants you to follow his army until further notice."),
           (call_script, "script_start_quest", "qst_follow_army", ":faction_marshall"),
           #(assign, "$g_player_follow_army_warnings", 0),
         (try_end),
         (jump_to_menu,"mnu_castle_attack_walls_with_allies_simulate")]),
      ("leave",[],"Leave.",[(leave_encounter),(change_screen_return)]),
    ]
 ),


( "moria_must_escape",city_menu_color, # dungeon crawl: way out of moria
 "^^The book seems to give the account of the last attempt of dwarves to resettle in Moria.\
 Attempt which apparently ended with gruesome death for all involved. Perusing the book, \
 you stumble on the words 'true silver'! Studying the pages you suddenly understand \
 that those are the descriptions of dwarven stashes somewhere on the lower levels. Hah! \
 Would not it be cool to uncover the long lost dwarven mithril!? \
 ^You eagerly follow the directions, into a narrow winding tunnel and down... \
 ^...^After a couple of hours of fruitless search you understand that you are lost deep in Moria and need to find a way out.",
    "none",[(set_background_mesh, "mesh_town_moria"),],[
	  ("moria_exit_scene",[], "Find your way out!",[
			(modify_visitors_at_site,"scn_moria_deep_mines"),
			(reset_visitors),
            		(set_visitor,0,"trp_player"),
			(set_jump_mission,"mt_dungeon_crawl_moria_deep"),
            		(jump_to_scene, "scn_moria_deep_mines"),
			(jump_to_menu, "mnu_auto_return_to_map"),
            (change_screen_mission),
	  ]),
	  # ("moria_exit_found",[(eq,1,0)], "Exit is here!",[
			# (jump_to_menu, "mnu_auto_return_to_map"),
            # (change_screen_map),
	  # ], "Fresh air behind this door!"),
	]
 ),

( "castle_outside",city_menu_color,
    "You are outside {s2}.{s11} {s3} {s4}",
    "none",
    code_to_set_city_background + [
	    
        (assign, "$g_enemy_party", "$g_encountered_party"),
        (assign, "$g_ally_party", -1),
        (str_store_party_name, s2,"$g_encountered_party"),
        (call_script, "script_encounter_calculate_fit"),
        (assign,"$all_doors_locked",1),
		#(str_store_party_name, s15, "$g_encountered_party"),(display_message, "@castle_outside_menu: {s15}"),

        (assign, "$current_town","$g_encountered_party"),
        (try_begin),
          (eq, "$new_encounter", 1),
          (assign, "$new_encounter", 0),
          (call_script, "script_let_nearby_parties_join_current_battle", 1, 0),
          (call_script, "script_encounter_init_variables"),
          (assign, "$entry_to_town_forbidden",0),
          (assign, "$sneaked_into_town",0),
          #(assign, "$town_entered", 0),
#          (assign, "$waiting_for_arena_fight_result", 0),
          (assign, "$encountered_party_hostile", 0),
          (assign, "$encountered_party_friendly", 0),
          (try_begin),
            (gt, "$g_player_besiege_town", 0),
            (neq,"$g_player_besiege_town","$g_encountered_party"),
            (party_slot_eq, "$g_player_besiege_town", slot_center_is_besieged_by, "p_main_party"),
            (call_script, "script_lift_siege", "$g_player_besiege_town", 0),
            (assign,"$g_player_besiege_town",-1),
          (try_end),
          (try_begin),
            (lt, "$g_encountered_party_relation", 0),
            (assign, "$encountered_party_hostile", 1),
            (assign,"$entry_to_town_forbidden",1),
          (try_end),

          (assign,"$cant_sneak_into_town",0),
          (try_begin),
            (eq,"$current_town","$last_sneak_attempt_town"),
            (store_current_hours,reg(2)),
            (val_sub,reg(2),"$last_sneak_attempt_time"),
            (lt,reg(2),12),
            (assign,"$cant_sneak_into_town",1),
          (try_end),
        (else_try), #second or more turn
          (eq, "$g_leave_encounter",1),
          (change_screen_return),
        (try_end),

        (str_clear,s4),
        (try_begin), 
          (eq,"$entry_to_town_forbidden",1),
          (try_begin),
            (eq,"$cant_sneak_into_town",1),
            (str_store_string,s4,"str_sneaking_to_town_impossible"),
          (else_try),
            (str_store_string,s4,"str_entrance_to_town_forbidden"),
          (try_end),
        (try_end),

        (party_get_slot, ":center_lord", "$current_town", slot_town_lord),
        (store_faction_of_party, ":center_faction", "$current_town"),
        (str_store_faction_name,s9,":center_faction"),
        (try_begin),
          (ge, ":center_lord", 0),
          (str_store_troop_name,s8,":center_lord"),
          (str_store_string,s7,"@{s8} of {s9}"),
        (try_end),

        (try_begin), # same mnu_town
          (party_slot_eq,"$current_town",slot_party_type, spt_castle),
          (try_begin),
            (eq, ":center_lord", "trp_player"),
            (str_store_string,s11,"@ Your own banner flies over the castle gate."),
          (else_try),
            (ge, ":center_lord", 0),
            (str_store_string,s11,"@ You see the banner of {s7} over the castle gate."),
          (else_try),
            (str_store_string,s11,"@ This castle seems to belong to no one."),
          (try_end),
        (else_try),
          (try_begin),
            (eq, ":center_lord", "trp_player"),
            (str_store_string,s11,"@ Your own banner flies over the town gates."),
          (else_try),
            (ge, ":center_lord", 0),
            (str_store_string,s11,"@ You see the banner of {s7} over the town gates."),
          (else_try),
            (str_store_string,s11,"@ The townsfolk here have declared their independence."),
          (try_end),
        (try_end),

        (party_get_num_companions, reg(7),"p_collective_enemy"),
        (assign,"$castle_undefended",0),
        (str_clear, s3),
        (try_begin),
          (eq,reg(7),0),
          (assign,"$castle_undefended",1),
#          (party_set_faction,"$g_encountered_party","fac_neutral"),
#          (party_set_slot, "$g_encountered_party", slot_town_lord, stl_unassigned),
          (str_store_string, s3, "str_castle_is_abondened"),
        (else_try),
          (eq,"$g_encountered_party_faction","fac_player_supporters_faction"),
          (str_store_string, s3, "str_place_is_occupied_by_player"),
        (else_try),
          (lt, "$g_encountered_party_relation", 0),
          (str_store_string, s3, "str_place_is_occupied_by_enemy"),
#        (else_try),
#          (str_store_string, s3, "str_place_is_occupied_by_friendly"),
        (try_end),

        (try_begin),
          (eq, "$g_leave_town_outside",1),
          (assign, "$g_leave_town_outside",0),
          (assign, "$g_permitted_to_center", 0),
          (change_screen_return),
        (else_try),
          (check_quest_active, "qst_escort_messenger"),
          (quest_slot_eq, "qst_escort_messenger", slot_quest_target_center, "$g_encountered_party"),
          (quest_get_slot, ":quest_object_troop", "qst_escort_messenger", slot_quest_object_troop),
          (modify_visitors_at_site,"scn_conversation_scene"),
          (reset_visitors),
          (set_visitor,0, "trp_player"),
          (set_visitor,17, ":quest_object_troop"),
          (set_jump_mission, "mt_conversation_encounter"),
          (jump_to_scene, "scn_conversation_scene"),
          (assign, "$talk_context", tc_entering_center_quest_talk),
          (change_screen_map_conversation, ":quest_object_troop"),
        # (else_try),
          # (check_quest_active, "qst_kidnapped_girl"),
          # (quest_slot_eq, "qst_kidnapped_girl", slot_quest_giver_center, "$g_encountered_party"),
          # (quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 3),
          # (modify_visitors_at_site,"scn_conversation_scene"),
          # (reset_visitors),
          # (set_visitor,0, "trp_player"),
          # (set_visitor,17, "trp_kidnapped_girl"),
          # (set_jump_mission, "mt_conversation_encounter"),
          # (jump_to_scene, "scn_conversation_scene"),
          # (assign, "$talk_context", tc_entering_center_quest_talk),
          # (change_screen_map_conversation, "trp_kidnapped_girl"),
##        (else_try),
##          (gt, "$lord_requested_to_talk_to", 0),
##          (store_current_hours, ":cur_hours"),
##          (neq, ":cur_hours", "$quest_given_time"),
##          (modify_visitors_at_site,"scn_conversation_scene"),
##          (reset_visitors),
##          (assign, ":cur_lord", "$lord_requested_to_talk_to"),
##          (assign, "$lord_requested_to_talk_to", 0),
##          (set_visitor,0,"trp_player"),
##          (set_visitor,17,":cur_lord"),
##          (set_jump_mission,"mt_conversation_encounter"),
##          (jump_to_scene,"scn_conversation_scene"),
##          (assign, "$talk_context", tc_castle_gate_lord),
##          (change_screen_map_conversation, ":cur_lord"),
        (else_try),
          (eq, "$g_town_visit_after_rest", 1),
          (assign, "$g_town_visit_after_rest", 0),
          (jump_to_menu,"mnu_town"),
        # (else_try),
          # (party_slot_eq,"$g_encountered_party", slot_town_lord, "trp_player"),
          # (party_slot_eq,"$g_encountered_party", slot_party_type,spt_castle),
          # (jump_to_menu, "mnu_enter_your_own_castle"),
        (else_try),
          (party_slot_eq,"$g_encountered_party", slot_party_type,spt_castle),
          (ge, "$g_encountered_party_relation", 0),
          (this_or_next|eq,"$castle_undefended",1),
          (eq, "$g_permitted_to_center",1),
          (jump_to_menu, "mnu_town"),
        (else_try),
          (party_slot_eq,"$g_encountered_party", slot_party_type,spt_town),
          (ge, "$g_encountered_party_relation", 0),
          (jump_to_menu, "mnu_town"),
        (else_try),
          (eq, "$g_player_besiege_town", "$g_encountered_party"),
          (jump_to_menu, "mnu_castle_besiege"),
        (try_end),
        ],
    [

	  ("moria_enter",[
				(eq, "$current_town", "p_town_moria"),
				(this_or_next|eq, "$found_moria_entrance", 1),(eq,"$cheat_mode",1)
	        ], "Return into main hall of Moria trough the secret entrance",[
			(modify_visitors_at_site,"scn_moria_center",),
			(reset_visitors),
            (set_visitor,1,"trp_player"),
			(set_jump_mission,"mt_dungeon_crawl_moria_hall"),
            (jump_to_scene, "scn_moria_center"),
			(assign, "$found_moria_entrance", 1),
            (change_screen_mission),
	  ],"Enter Moria."),
	  
	  #Enter dungeon in Moria begin (mtarini)
      ("moria_secret",[
        (eq, "$current_town", "p_town_moria"),
	  	(eq,"$entry_to_town_forbidden",1), 
		(try_begin), (eq, "$found_moria_entrance", 1),
			(str_store_string, s12, "@Go to the secret entrance to Moria" ),
		(else_try),
			(str_store_string, s12, "@Search for a secret entrance to Moria" ),
		(try_end),
		
        ],"{s12}",[
            (modify_visitors_at_site,"scn_moria_secret_entry"),
			(reset_visitors),
            (set_visitor,0,"trp_player"),
			(set_jump_mission,"mt_dungeon_crawl_moria_entrance"),
            (jump_to_scene, "scn_moria_secret_entry"),
            (change_screen_mission),
       ]),
      #Enter dungeon in Moria end (mtarini)
	  
	  ("cheat_steal_book",[(eq, "$current_town", "p_town_moria"),(eq,"$cheat_mode",1),], "CHEAT: steal book now",[
			(troop_add_item, "trp_player","itm_book_of_moria",0),
			(try_begin),
				(faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
				(str_store_string, s12, "@Get book." ),
				(jump_to_menu,"mnu_moria_must_escape"),
				(finish_mission),
			(else_try),
				(str_store_string, s12, "str_empty_string"),
			(try_end),
	  ]
	  ,"Get the book"),

	  
      # ("approach_gates",[(this_or_next|eq,"$entry_to_town_forbidden",1),
                          # (party_slot_eq,"$g_encountered_party", slot_party_type,spt_castle)],
       # "Approach the gates and hail the guard.",[
                                                  # (jump_to_menu, "mnu_castle_guard"),
# ##                                                   (modify_visitors_at_site,"scn_conversation_scene"),(reset_visitors),
# ##                                                   (set_visitor,0,"trp_player"),
# ##                                                   (store_faction_of_party, ":cur_faction", "$g_encountered_party"),
# ##                                                   (faction_get_slot, ":cur_guard", ":cur_faction", slot_faction_guard_troop),
# ##                                                   (set_visitor,17,":cur_guard"),
# ##                                                   (set_jump_mission,"mt_conversation_encounter"),
# ##                                                   (jump_to_scene,"scn_conversation_scene"),
# ##                                                   (assign, "$talk_context", tc_castle_gate),
# ##                                                   (change_screen_map_conversation, ":cur_guard")
                                                   # ]),
 ]+concatenate_scripts([[	  
      ("town_sneak",[(eq, cheat_switch, 1),
					 (party_slot_eq,"$g_encountered_party", slot_party_type,spt_town),
                     (eq,"$entry_to_town_forbidden",1),
                     (eq,"$cant_sneak_into_town",0)],
       "TEST: Disguise yourself and try to sneak into the town.",
       [
         (faction_get_slot, ":player_alarm", "$g_encountered_party_faction", slot_faction_player_alarm),
         (party_get_num_companions, ":num_men", "p_main_party"),
         (party_get_num_prisoners, ":num_prisoners", "p_main_party"),
         (val_add, ":num_men", ":num_prisoners"),
         (val_mul, ":num_men", 2),
         (val_div, ":num_men", 3),
         (store_add, ":get_caught_chance", ":player_alarm", ":num_men"),
         (store_random_in_range, ":random_chance", 0, 100),
         (try_begin),
           (this_or_next|ge, ":random_chance", ":get_caught_chance"),
           (eq, "$g_last_defeated_bandits_town", "$g_encountered_party"),
           (assign, "$g_last_defeated_bandits_town", 0),
           (assign, "$sneaked_into_town",1),
           #(assign, "$town_entered", 1),
           (jump_to_menu,"mnu_sneak_into_town_suceeded"),
         (else_try),
           (jump_to_menu,"mnu_sneak_into_town_caught"),
         (try_end)
         ]),
      ("castle_start_siege",
       [ (eq, cheat_switch, 1),(eq, 0, 1), #MV: player can't start a sieg
           (this_or_next|party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
           (             party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, "p_main_party"),
           (store_relation, ":reln", "$g_encountered_party_faction", "fac_player_supporters_faction"),
           (lt, ":reln", 0),
           (lt, "$g_encountered_party_2", 1),
           (call_script, "script_party_count_fit_for_battle","p_main_party"),
           (gt, reg(0), 5),
           (try_begin),
             (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
             (assign, reg6, 1),
           (else_try),
             (assign, reg6, 0),
           (try_end),
           ],
       "Besiege the {reg6?town:castle}.",
       [
         (eq, "$cheat_mode", 1), #MV: player can't start a siege
         (assign,"$g_player_besiege_town","$g_encountered_party"),
         (store_relation, ":relation", "fac_player_supporters_faction", "$g_encountered_party_faction"),
         (val_min, ":relation", -40),
         (call_script, "script_set_player_relation_with_faction", "$g_encountered_party_faction", ":relation"),
         (call_script, "script_update_all_notes"),
         (jump_to_menu, "mnu_castle_besiege"),
         ]),


      ("cheat_castle_start_siege",
       [ (eq, cheat_switch, 1),
         (eq, "$cheat_mode", 1),
         (this_or_next|party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
         (             party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, "p_main_party"),
         (store_relation, ":reln", "$g_encountered_party_faction", "fac_player_supporters_faction"),
         (ge, ":reln", 0),
         (lt, "$g_encountered_party_2", 1),
         (call_script, "script_party_count_fit_for_battle","p_main_party"),
         (gt, reg(0), 1),
         (try_begin),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
           (assign, reg6, 1),
         (else_try),
           (assign, reg6, 0),
         (try_end),
           ],
       "CHEAT: Besiege the {reg6?town:castle}...",
       [   (assign,"$g_player_besiege_town","$g_encountered_party"),
           (jump_to_menu, "mnu_castle_besiege"),
           ]),
 ] for ct in range(cheat_switch)])+[
	   
 ]+concatenate_scripts([[
	  ("town_sneak",[(eq,0,1)],"Dont.",[]),
	  ("castle_start_siege",[(eq,0,1)],"Dont.",[]),
	  ("cheat_castle_start_siege",[(eq,0,1)],"Dont.",[]),
 ] for ct in range(1-cheat_switch)])+[

      ("castle_leave",[],"Leave.",[(change_screen_return,0)]),

 ]+concatenate_scripts([[
      ("castle_cheat_interior",[(eq, "$cheat_mode", 1)], "CHEAT! Interior.",[(set_jump_mission,"mt_ai_training"),
                                                       (party_get_slot, ":castle_scene", "$current_town", slot_town_castle),
                                                       (jump_to_scene,":castle_scene"),
                                                       (change_screen_mission)]),
      ("castle_cheat_exterior",[(eq, cheat_switch, 1),(eq, "$cheat_mode", 1)], "CHEAT! Exterior.",[
                                                       (set_jump_mission,"mt_ai_training"),
                                                       (party_get_slot, ":castle_scene", "$current_town", slot_castle_exterior),
                                                       (jump_to_scene,":castle_scene"),
                                                       (change_screen_mission)]),
      ("castle_cheat_town_walls",[(eq, cheat_switch, 1),(eq, "$cheat_mode", 1),(party_slot_eq,"$current_town",slot_party_type, spt_town),], "CHEAT! Town Walls.",
       [
         (party_get_slot, ":scene", "$current_town", slot_town_walls),
         (set_jump_mission,"mt_ai_training"),
         (jump_to_scene,":scene"),
         (change_screen_mission)]),
 ] for ct in range(cheat_switch)])+[
    ]
 ),
( "castle_besiege",mnf_enable_hot_keys,
    "You are laying siege to {s1}. {s2} {s3}",
    "none",
    code_to_set_city_background + [   (assign, "$g_siege_force_wait", 0),
        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
          (party_set_slot, "$g_encountered_party", slot_center_is_besieged_by, "p_main_party"),
          (store_current_hours, ":cur_hours"),
          (party_set_slot, "$g_encountered_party", slot_center_siege_begin_hours, ":cur_hours"),
          (assign, "$g_siege_method", 0),
          (assign, "$g_siege_sallied_out_once", 0),
        (try_end),

        (party_get_slot, ":town_food_store", "$g_encountered_party", slot_party_food_store),
        (call_script, "script_center_get_food_consumption", "$g_encountered_party"),
        (assign, ":food_consumption", reg0),
        (assign, reg7, ":food_consumption"),
        (assign, reg8, ":town_food_store"),
        (store_div, reg3, ":town_food_store", ":food_consumption"),

        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (assign, reg6, 1),
        (else_try),
          (assign, reg6, 0),
        (try_end),
        
        (try_begin),
          (gt, reg3, 0),
          (str_store_string, s2, "@The {reg6?town's:castle's} food stores should last for {reg3} more days."),
        (else_try),
          (str_store_string, s2, "@The {reg6?town's:castle's} food stores have run out and the defenders are starving."),
        (try_end),

        (str_store_string, s3, "str_empty_string"),
        (try_begin),
          (ge, "$g_siege_method", 1),
          (store_current_hours, ":cur_hours"),
          (try_begin),
            (lt, ":cur_hours",  "$g_siege_method_finish_hours"),
            (store_sub, reg9, "$g_siege_method_finish_hours", ":cur_hours"),
            (try_begin),
              (eq, "$g_siege_method", 1),
              (str_store_string, s3, "@You're preparing to attack the walls, the work should finish in {reg9} hours."),
            (else_try),
              (eq, "$g_siege_method", 2),
              (str_store_string, s3, "@Your forces are building a siege tower. They estimate another {reg9} hours to complete the build."),
            (try_end),
          (else_try),
            (try_begin),
              (eq, "$g_siege_method", 1),
              (str_store_string, s3, "@You are ready to attack the walls at any time."),
            (else_try),
              (eq, "$g_siege_method", 2),
              (str_store_string, s3, "@The siege tower is built and ready to make an assault."),
            (try_end),
          (try_end),
        (try_end),
        
        #Check if enemy leaves the castle to us...
        (try_begin),
          (eq, "$g_castle_left_to_player",1), #we come here after dialog. Empty the castle and send parties away.
          (assign, "$g_castle_left_to_player",0),
          (store_faction_of_party, ":castle_faction", "$g_encountered_party"),
          (party_set_faction,"$g_encountered_party","fac_neutral"), #temporarily erase faction so that it is not the closest town
          (party_get_num_attached_parties, ":num_attached_parties_to_castle","$g_encountered_party"),
          (try_for_range_backwards, ":iap", 0, ":num_attached_parties_to_castle"),
            (party_get_attached_party_with_rank, ":attached_party", "$g_encountered_party", ":iap"),
            (party_detach, ":attached_party"),
            (party_get_slot, ":attached_party_type", ":attached_party", slot_party_type),
            (eq, ":attached_party_type", spt_kingdom_hero_party),
            (store_faction_of_party, ":attached_party_faction", ":attached_party"),
            (call_script, "script_get_closest_center_of_faction", ":attached_party", ":attached_party_faction"),
            (try_begin),
              (gt, reg0, 0),
              (call_script, "script_party_set_ai_state", ":attached_party", spai_holding_center, reg0),
            (else_try),
              (call_script, "script_party_set_ai_state", ":attached_party", spai_patrolling_around_center, "$g_encountered_party"),
            (try_end),
          (try_end),
          (call_script, "script_party_remove_all_companions", "$g_encountered_party"),
          (change_screen_return),
          (party_collect_attachments_to_party, "$g_encountered_party", "p_collective_enemy"), #recalculate so that
          (call_script, "script_party_copy", "p_encountered_party_backup", "p_collective_enemy"), #leaving troops will not be considered as captured
          (party_set_faction,"$g_encountered_party",":castle_faction"), 
        (try_end),

        #Check for victory or defeat....
        (assign, "$g_enemy_party", "$g_encountered_party"),
        (assign, "$g_ally_party", -1),
        (str_store_party_name, 1,"$g_encountered_party"),
        (call_script, "script_encounter_calculate_fit"),
        
        (assign, reg11, "$g_enemy_fit_for_battle"),
        (assign, reg10, "$g_friend_fit_for_battle"),


        (try_begin),
          (eq, "$g_leave_encounter",1),
          (change_screen_return),
        (else_try),
          (call_script, "script_party_count_fit_regulars","p_collective_enemy"),
          (assign, ":enemy_finished", 0),
          (try_begin),
            (eq, "$g_battle_result", 1),
            (assign, ":enemy_finished", 1),
          (else_try),
            (le, "$g_enemy_fit_for_battle", 0),
            (ge, "$g_friend_fit_for_battle", 1),
            (assign, ":enemy_finished", 1),
          (try_end),
          (this_or_next|eq, ":enemy_finished", 1),
          (eq, "$g_enemy_surrenders", 1),
          (assign, "$g_next_menu", "mnu_castle_taken"),
          (jump_to_menu, "mnu_total_victory"),
        (else_try),
          (call_script, "script_party_count_members_with_full_health", "p_main_party"),
          (assign, ":main_party_fit_regulars", reg(0)),
          (eq, "$g_battle_result", -1),
          (eq, ":main_party_fit_regulars", 0), #all lost
		  (assign, "$recover_after_death_menu", "mnu_recover_after_death_town"),
          (assign, "$g_next_menu", "mnu_tld_player_defeated"),
          (jump_to_menu, "mnu_total_defeat"),
        (try_end),
    ],
	
    [ ("siege_request_meeting",[(eq, "$cant_talk_to_enemy", 0)],"Call for a meeting with the castle commander.", [
          (assign, "$cant_talk_to_enemy", 1),
          (assign, "$g_enemy_surrenders",0),
          (assign, "$g_castle_left_to_player",0),
          (assign, "$talk_context", tc_castle_commander),
          (party_get_num_attached_parties, ":num_attached_parties_to_castle","$g_encountered_party"),
          (try_begin),
            (gt, ":num_attached_parties_to_castle", 0),
            (party_get_attached_party_with_rank, ":leader_attached_party", "$g_encountered_party", 0),
            (call_script, "script_setup_party_meeting", ":leader_attached_party"),
          (else_try),
            (call_script, "script_setup_party_meeting", "$g_encountered_party"),
          (try_end),
           ]),
        
      ("wait_24_hours",[],"Wait until tomorrow.", [
          (assign,"$auto_besiege_town","$g_encountered_party"),
          (assign, "$g_siege_force_wait", 1),
          (store_time_of_day,":cur_time_of_day"),
          (val_add, ":cur_time_of_day", 1),
          (assign, ":time_to_wait", 31),
          (val_sub,":time_to_wait",":cur_time_of_day"),
          (val_mod,":time_to_wait",24),
          (val_add, ":time_to_wait", 1),
          (rest_for_hours_interactive, ":time_to_wait", 5, 1), #rest while attackable
          (assign, "$cant_talk_to_enemy", 0),
          (change_screen_return),
          ]),

      
      ("castle_lead_attack",
       [ (neg|troop_is_wounded, "trp_player"),
         (ge, "$g_siege_method", 1),
         (gt, "$g_friend_fit_for_battle", 3),
         (store_current_hours, ":cur_hours"),
         (ge, ":cur_hours", "$g_siege_method_finish_hours"),
         ],
       "Lead your soldiers in an assault.", [
           (try_begin),
             (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
             (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_walls),
           (else_try),
             (party_get_slot, ":battle_scene", "$g_encountered_party", slot_castle_exterior),
           (try_end),
           (call_script, "script_calculate_battle_advantage"),
           (assign, ":battle_advantage", reg0),
           (val_mul, ":battle_advantage", 2),
           (val_div, ":battle_advantage", 3), #scale down the advantage a bit in sieges.
           (set_battle_advantage, ":battle_advantage"),
           (set_party_battle_mode),
           (assign, "$g_siege_battle_state", 1),
           (assign, ":siege_sally", 0),
           (try_begin),
             (le, ":battle_advantage", -4), #we are outnumbered, defenders sally out
             (eq, "$g_siege_sallied_out_once", 0),
             (set_jump_mission,"mt_castle_attack_walls_defenders_sally"),
             (assign, "$g_siege_battle_state", 0),
             (assign, ":siege_sally", 1),
#           (else_try),
#             (party_slot_eq, "$current_town", slot_center_siege_with_belfry, 1),
#             (set_jump_mission,"mt_castle_attack_walls_belfry"),
           (else_try),
             (set_jump_mission,"mt_castle_attack_walls_ladder"),
           (try_end),
           (assign, "$cant_talk_to_enemy", 0),           
           (assign, "$g_siege_final_menu", "mnu_castle_besiege"),
           (assign, "$g_next_menu", "mnu_castle_besiege_inner_battle"),
           (assign, "$g_siege_method", 0), #reset siege timer
           (jump_to_scene,":battle_scene"),
           (try_begin),
             (eq, ":siege_sally", 1),
             (jump_to_menu, "mnu_siege_attack_meets_sally"),
           (else_try),
#           (jump_to_menu,"mnu_castle_outside"),
##           (assign, "$g_next_menu", "mnu_castle_besiege"),
             (jump_to_menu, "mnu_battle_debrief"),
             (change_screen_mission),
           (try_end),
       ]),
      ("attack_stay_back",
       [ (ge, "$g_siege_method", 1),
         (gt, "$g_friend_fit_for_battle", 3),
         (store_current_hours, ":cur_hours"),
         (ge, ":cur_hours",  "$g_siege_method_finish_hours"),
         ],
       "Order your soldiers to attack while you stay back...", [(assign, "$cant_talk_to_enemy", 0),(jump_to_menu,"mnu_castle_attack_walls_simulate")]),

      ("build_ladders",[(party_slot_eq, "$current_town", slot_center_siege_with_belfry, 0),(eq, "$g_siege_method", 0)],
       "Prepare ladders to attack the walls.", [(jump_to_menu,"mnu_construct_ladders")]),

      # ("build_siege_tower",[(party_slot_eq, "$current_town", slot_center_siege_with_belfry, 1),(eq, "$g_siege_method", 0)],
       # "Build a siege tower.", [(jump_to_menu,"mnu_construct_siege_tower")]),

      ("cheat_castle_lead_attack",[(eq, "$cheat_mode", 1),
                                   (eq, "$g_siege_method", 0)],
       "CHEAT: Instant build equipments.",
       [
         (assign, "$g_siege_method", 1),
         (assign, "$g_siege_method_finish_hours", 0),
         (jump_to_menu, "mnu_castle_besiege"),
       ]),
      ("lift_siege",[],"Abandon the siege.",
       [ (call_script, "script_lift_siege", "$g_player_besiege_town", 0),
         (assign,"$g_player_besiege_town", -1),
         (change_screen_return)]),
    ]
 ),
( "siege_attack_meets_sally",0,
    "^^^^^^The defenders sally out to meet your assault.",    "none",    [],
    [("continue",[], "Continue...", [(jump_to_menu, "mnu_battle_debrief"),(change_screen_mission),]),]
 ),
( "castle_besiege_inner_battle",0,
    "{s1}",
    "none",
    [   # (troop_get_type, ":is_female", "trp_player"),
        # (try_begin),
          # (eq, ":is_female", 1),
          # (set_background_mesh, "mesh_pic_siege_sighted_fem"),
        # (else_try),
          # (set_background_mesh, "mesh_pic_siege_sighted"),
        # (try_end),
        (assign, ":result", "$g_battle_result"),#will be reset at script_encounter_calculate_fit
        (call_script, "script_encounter_calculate_fit"),
        
# TODO: To use for the future:
            (str_store_string, s1, "@As a last defensive effort, you retreat to the main hall of the keep.\
 You and your remaining soldiers will put up a desperate fight here. If you are defeated, there's no other place to fall back to."),
            (str_store_string, s1, "@You've been driven away from the walls.\
 Now the attackers are pouring into the streets. IF you can defeat them, you can perhaps turn the tide and save the day."),
        (try_begin),
          (this_or_next|neq, ":result", 1),
          (this_or_next|le, "$g_friend_fit_for_battle", 0),
          (le, "$g_enemy_fit_for_battle", 0),
          (jump_to_menu, "$g_siege_final_menu"),
        (else_try),
          (call_script, "script_encounter_calculate_fit"),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (try_begin),
            (eq, "$g_siege_battle_state", 0),
            (eq, ":result", 1),
            (assign, "$g_battle_result", 0),
            (jump_to_menu, "$g_siege_final_menu"),
          (else_try),
            (eq, "$g_siege_battle_state", 1),
            (eq, ":result", 1),
            (str_store_string, s1, "@You've breached the town walls,\
 but the stubborn defenders continue to resist you in the streets!\
 You'll have to deal with them before you can attack the keep at the heart of the town."),
          (else_try),
            (eq, "$g_siege_battle_state", 2),
            (eq, ":result", 1),
            (str_store_string, s1, "@The town centre is yours,\
 but the remaining defenders have retreated to the castle.\
 It must fall before you can complete your victory."),
          (else_try),
            (jump_to_menu, "$g_siege_final_menu"),
          (try_end),
        (else_try),
          (try_begin),
            (eq, "$g_siege_battle_state", 0),
            (eq, ":result", 1),
            (assign, "$g_battle_result", 0),
            (jump_to_menu, "$g_siege_final_menu"),
          (else_try),
            (eq, "$g_siege_battle_state", 1),
            (eq, ":result", 1),
            (str_store_string, s1, "@The remaining defenders have retreated to the castle as a last defense. You must go in and crush any remaining resistance."),
          (else_try),
            (jump_to_menu, "$g_siege_final_menu"),
          (try_end),
        (try_end),
    ],
    [ ("continue",[],"Continue...",
       [   (try_begin),
             (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
             (try_begin),
               (eq, "$g_siege_battle_state", 1),
               (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_walls),
               (set_jump_mission, "mt_besiege_inner_battle_town_center"),
             (else_try),
               (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_walls),
               (set_jump_mission, "mt_besiege_inner_battle_castle"),
             (try_end),
           (else_try),
             (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_walls),
             (set_jump_mission, "mt_besiege_inner_battle_castle"),
           (try_end),
##           (call_script, "script_calculate_battle_advantage"),
##           (set_battle_advantage, reg0),
           (set_party_battle_mode),
           (jump_to_scene, ":battle_scene"),
           (val_add, "$g_siege_battle_state", 1),
           (assign, "$g_next_menu", "mnu_castle_besiege_inner_battle"),
           (jump_to_menu, "mnu_battle_debrief"),
           (change_screen_mission),
       ]),
    ]
 ),
( "construct_ladders",0,
    "As the party member with the highest Engineer skill ({reg2}), {reg3?you estimate:{s3} estimates} that it will take\
 {reg4} hours to build enough scaling ladders for the assault.",
    "none",
    [(call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
     (assign, ":max_skill", reg0),
     (assign, ":max_skill_owner", reg1),
     (assign, reg2, ":max_skill"),

     (store_sub, reg4, 14, ":max_skill"),
     (val_mul, reg4, 2),
     (val_div, reg4, 3),
     
     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (assign, reg3, 1),
     (else_try),
       (assign, reg3, 0),
       (str_store_troop_name, s3, ":max_skill_owner"),
     (try_end),
    ],
    [ ("build_ladders_cont",[],
       "Do it.", [
           (assign, "$g_siege_method", 1),
           (store_current_hours, ":cur_hours"),
           (call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
           (store_sub, ":hours_takes", 14, reg0),
           (val_mul, ":hours_takes", 2),
           (val_div, ":hours_takes", 3),
           (store_add, "$g_siege_method_finish_hours",":cur_hours", ":hours_takes"),
           (assign,"$auto_besiege_town","$current_town"),
           (rest_for_hours_interactive, 96, 5, 1), #rest while attackable. A trigger will divert control when attack is ready.
           (change_screen_return),
           ]),
      ("go_back_dot",[],"Go back.", [(jump_to_menu,"mnu_castle_besiege")]),],
 ),
( "castle_attack_walls_simulate",mnf_disable_all_keys,
    "{s4}^^Your casualties:{s8}^^Enemy casualties were: {s9}",
    "none",
    [   (troop_get_type, ":is_female", "trp_player"),
        (try_begin),
          (eq, ":is_female", 1),
          #(set_background_mesh, "mesh_pic_siege_sighted_fem"),
        (else_try),
          #(set_background_mesh, "mesh_pic_siege_sighted"),
        (try_end),
        
        (call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
        (assign, ":player_party_strength", reg0),
        (val_div, ":player_party_strength", 10),

        (call_script, "script_party_calculate_strength", "$g_encountered_party", 0),
        (assign, ":enemy_party_strength", reg0),
        (val_div, ":enemy_party_strength", 4),

        (inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s8, s0),

        (inflict_casualties_to_party_group, "$g_encountered_party", ":player_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s9, s0),

        (assign, "$no_soldiers_left", 0),
        (try_begin),
          (call_script, "script_party_count_members_with_full_health","p_main_party"),
          (le, reg(0), 0),
          (assign, "$no_soldiers_left", 1),
          (str_store_string, s4, "str_attack_walls_failure"),
        (else_try),
          (call_script, "script_party_count_members_with_full_health","$g_encountered_party"),
          (le, reg(0), 0),
          (assign, "$no_soldiers_left", 1),
          (assign, "$g_battle_result", 1),
          (str_store_string, s4, "str_attack_walls_success"),
        (else_try),
          (str_store_string, s4, "str_attack_walls_continue"),
        (try_end),
     ],
    [
##      ("lead_next_wave",[(eq, "$no_soldiers_left", 0)],"Lead the next wave of attack personally.", [
##           (party_get_slot, ":battle_scene", "$g_encountered_party", slot_castle_exterior),
##           (set_party_battle_mode),
##           (set_jump_mission,"mt_castle_attack_walls"),
##           (jump_to_scene,":battle_scene"),
##           (jump_to_menu,"mnu_castle_outside"),
##           (change_screen_mission),
##       ]),
##      ("continue_attacking",[(eq, "$no_soldiers_left", 0)],"Order your soldiers to keep attacking...", [
##                                    (jump_to_menu,"mnu_castle_attack_walls_3"),
##                                    ]),
##      ("call_soldiers_back",[(eq, "$no_soldiers_left", 0)],"Call your soldiers back.",[(jump_to_menu,"mnu_castle_outside")]),
      ("continue",[],"Continue...",[(jump_to_menu,"mnu_castle_besiege")]),
    ]
 ),
( "castle_attack_walls_with_allies_simulate",mnf_disable_all_keys,
    "{s4}^^Your casualties: {s8}^^Allies' casualties: {s9}^^Enemy casualties: {s10}",
    "none",
    [
        (troop_get_type, ":is_female", "trp_player"),
        (try_begin),
          (eq, ":is_female", 1),
          #(set_background_mesh, "mesh_pic_siege_sighted_fem"),
        (else_try),
          #(set_background_mesh, "mesh_pic_siege_sighted"),
        (try_end),

        (call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
        (assign, ":player_party_strength", reg0),
        (val_div, ":player_party_strength", 10),
        (call_script, "script_party_calculate_strength", "p_collective_friends", 0),
        (assign, ":friend_party_strength", reg0),
        (val_div, ":friend_party_strength", 10),

        (val_max, ":friend_party_strength", 1),

        (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
        (assign, ":enemy_party_strength", reg0),
        (val_div, ":enemy_party_strength", 4),

##        (assign, reg0, ":player_party_strength"),
##        (assign, reg1, ":friend_party_strength"),
##        (assign, reg2, ":enemy_party_strength"),
##        (assign, reg3, "$g_enemy_party"),
##        (assign, reg4, "$g_ally_party"),
##        (display_message, "@player_str={reg0} friend_str={reg1} enemy_str={reg2}"),
##        (display_message, "@enemy_party={reg3} ally_party={reg4}"),

        (assign, ":enemy_party_strength_for_p", ":enemy_party_strength"),
        (val_mul, ":enemy_party_strength_for_p", ":player_party_strength"),
        (val_div, ":enemy_party_strength_for_p", ":friend_party_strength"),
        (val_sub, ":enemy_party_strength", ":enemy_party_strength_for_p"),

        (inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength_for_p", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s8, s0),
                                    
        (inflict_casualties_to_party_group, "$g_enemy_party", ":friend_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s10, s0),

        (call_script, "script_collect_friendly_parties"),

        (inflict_casualties_to_party_group, "$g_ally_party", ":enemy_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s9, s0),

        (party_collect_attachments_to_party, "$g_enemy_party", "p_collective_enemy"),

        (assign, "$no_soldiers_left", 0),
        (try_begin),
          (call_script, "script_party_count_members_with_full_health", "p_main_party"),
          (le, reg0, 0),
          (assign, "$no_soldiers_left", 1),
          (str_store_string, s4, "str_attack_walls_failure"),
        (else_try),
          (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
          (le, reg0, 0),
          (assign, "$no_soldiers_left", 1),
          (assign, "$g_battle_result", 1),
          (str_store_string, s4, "str_attack_walls_success"),
        (else_try),
          (str_store_string, s4, "str_attack_walls_continue"),
        (try_end),
     ],
    [("continue",[],"Continue...",[(jump_to_menu,"mnu_besiegers_camp_with_allies")]),]
 ),
( "castle_taken_by_friends",0,
    "Nothing to see here.",
    "none",
    [   (party_clear, "$g_encountered_party"),
        (party_stack_get_troop_id, ":leader", "$g_encountered_party_2", 0),
        (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, ":leader"),
        (store_troop_faction, ":faction_no", ":leader"),
        #Reduce prosperity of the center by 5
        (call_script, "script_change_center_prosperity", "$g_encountered_party", -5),
        (call_script, "script_give_center_to_faction", "$g_encountered_party", ":faction_no"),
        (call_script, "script_add_log_entry", logent_player_participated_in_siege, "trp_player",  "$g_encountered_party", 0, "$g_encountered_party_faction"),
        (change_screen_return),
    ],
    [],
 ),
( "castle_taken",mnf_disable_all_keys,
    "{s3} has fallen to your troops, and you now have full control of the {reg2?town:castle}.\
  {reg1? It would seem that there is nothing stopping you from taking it for yourself...:}",# Only visible when castle is taken without being a vassal of a kingdom.
    "none",
    [   (party_clear, "$g_encountered_party"),
        (call_script, "script_lift_siege", "$g_encountered_party", 0),
        (assign, "$g_player_besiege_town", -1),
        (call_script, "script_add_log_entry", logent_castle_captured_by_player, "trp_player",  "$g_encountered_party", 0, "$g_encountered_party_faction"),
        (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, "trp_player"),
        #Reduce prosperity of the center by 5
        (call_script, "script_change_center_prosperity", "$g_encountered_party", -5),
        (call_script, "script_add_log_entry", logent_castle_captured_by_player, "trp_player", "$g_encountered_party", -1, "$g_encountered_party_faction"),
        (try_begin),
          (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
          (neq, "$players_kingdom", "fac_player_supporters_faction"),
          (call_script, "script_give_center_to_faction", "$g_encountered_party", "$players_kingdom"),
          (call_script, "script_order_best_besieger_party_to_guard_center", "$g_encountered_party", "$players_kingdom"),
          (jump_to_menu, "mnu_castle_taken_2"),
        (else_try),
          (call_script, "script_give_center_to_faction", "$g_encountered_party", "fac_player_supporters_faction"),
          (call_script, "script_order_best_besieger_party_to_guard_center", "$g_encountered_party", "fac_player_supporters_faction"),
          (str_store_party_name, s3, "$g_encountered_party"),
          (assign, reg1, 0),
          # (try_begin),
            # (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
            # (assign, reg1, 1),
          # (try_end),
        (try_end),
        (assign, reg2, 0),
        (try_begin),
          (is_between, "$g_encountered_party", centers_begin, centers_end),
          (assign, reg2, 1),
        (try_end),
    ],
    [ ("continue",[],"Continue...",[(assign, "$auto_enter_town", "$g_encountered_party"),(change_screen_return),]),],
 ),
( "castle_taken_2",mnf_disable_all_keys,
    "{s3} has fallen to your troops, and you now have full control of the castle.\
 It is time to send word to {s9} about your victory. {s5}",
    "none",
    [   (str_store_party_name, s3, "$g_encountered_party"),
        (str_clear, s5),
        (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
        (str_store_troop_name, s9, ":faction_leader"),
        (try_begin),
#          (eq, "$player_has_homage", 0),
          (assign, reg8, 0),
          (try_begin),
            (party_slot_eq, "$g_encountered_party", spt_town),
            (assign, reg8, 1),
          (try_end),
          (str_store_string, s5, "@However, since you are not a sworn {man/follower} of {s9}, there is no chance he would recognize you as the {lord/lady} of this {reg8?town:castle}."),
        (try_end),
    ],
    [ # commented by GA, no castle ownership in TLD
	  #("castle_taken_claim",[(eq, "$player_has_homage", 1)],"Request that {s3} be awarded to you.",
      # [
      #  (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, "trp_player"),
      #  (assign, "$g_castle_requested_by_player", "$current_town"),
      #  (assign, "$auto_enter_town", "$g_encountered_party"),
      #  (change_screen_return),
      #  ]),
      ("castle_taken_no_claim",[],"Ask no rewards.",
       [
        (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, -1),
        (assign, "$auto_enter_town", "$g_encountered_party"),
        (change_screen_return),
#        (jump_to_menu, "mnu_town"),
        ]),
    ],
 ),
 
( "siege_started_defender",mnf_scale_picture|mnf_enable_hot_keys,
    "{s1} is launching an assault against the walls of {s2}. You have {reg22} troops fit for battle against the enemy's {reg11}. You decide to...",
    "none",
    code_to_set_city_background + [
        (select_enemy,1),
        (assign, "$g_enemy_party", "$g_encountered_party_2"),
        (assign, "$g_ally_party", "$g_encountered_party"),
        (str_store_party_name, 1,"$g_enemy_party"),
        (str_store_party_name, 2,"$g_ally_party"),
        (call_script, "script_encounter_calculate_fit"),
        (assign, reg22, reg10), #TLD fix
        (try_begin),
          (eq, "$g_siege_first_encounter", 1),
          (call_script, "script_let_nearby_parties_join_current_battle", 1, 1), #MV from 0, 1, so no enemies standing by would join
          (call_script, "script_encounter_init_variables"),
        (try_end),

        (try_begin),
          (eq, "$g_siege_first_encounter", 0),
          (try_begin),
            (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
            (assign, ":num_enemy_regulars_remaining", reg0),
            (call_script, "script_party_count_members_with_full_health", "p_collective_friends"),
            (assign, ":num_ally_regulars_remaining", reg0),
            (assign, ":enemy_finished", 0),
            (try_begin),
              (eq, "$g_battle_result", 1),
              (eq, ":num_enemy_regulars_remaining", 0), #battle won
              (assign, ":enemy_finished",1),
            (else_try),
              (eq, "$g_engaged_enemy", 1),
              (le, "$g_enemy_fit_for_battle",0),
              (ge, "$g_friend_fit_for_battle",1),
              (assign, ":enemy_finished",1),
            (try_end),
            (this_or_next|eq, ":enemy_finished",1),
            (eq,"$g_enemy_surrenders",1),
            (assign, "$g_next_menu", -1),
            (jump_to_menu, "mnu_total_victory"),
          (else_try),
            (assign, ":battle_lost", 0),
            (try_begin),
              (this_or_next|eq, "$g_battle_result", -1),
              (troop_is_wounded,  "trp_player"),
              (eq, ":num_ally_regulars_remaining", 0),
              (assign, ":battle_lost",1),
            (try_end),
            (this_or_next|eq, ":battle_lost",1),
            (eq,"$g_player_surrenders",1),
			(assign, "$recover_after_death_menu", "mnu_recover_after_death_town"),
            (assign, "$g_next_menu", "mnu_tld_player_defeated"),
            (jump_to_menu, "mnu_total_defeat"),
          (else_try),
            # Ordinary victory/defeat.
            (assign, ":attackers_retreat", 0),
            (try_begin),
            #check whether enemy retreats
              (eq, "$g_battle_result", 1),
  ##            (store_mul, ":min_enemy_str", "$g_enemy_fit_for_battle", 2),
  ##            (lt, ":min_enemy_str", "$g_friend_fit_for_battle"),
              (assign, ":attackers_retreat", 1),
            (else_try),
              (eq, "$g_battle_result", 0),
              (store_div, ":min_enemy_str", "$g_enemy_fit_for_battle", 3),
              (lt, ":min_enemy_str", "$g_friend_fit_for_battle"),
              (assign, ":attackers_retreat", 1),
            (else_try),
              (store_random_in_range, ":random_no", 0, 100),
              (lt, ":random_no", 10),
              (neq, "$new_encounter", 1),
              (assign, ":attackers_retreat", 1),
            (try_end),
            (try_begin),
              (eq, ":attackers_retreat", 1),
              (party_get_slot, ":siege_hardness", "$g_encountered_party", slot_center_siege_hardness),
              (val_add, ":siege_hardness", 100),
              (party_set_slot, "$g_encountered_party", slot_center_siege_hardness, ":siege_hardness"),
              (party_set_slot, "$g_enemy_party", slot_party_retreat_flag, 1),

              (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
                (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
                #(troop_slot_eq, ":troop_no", slot_troop_is_prisoner, 0),
                (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
                (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
                (gt, ":party_no", 0),
                (party_slot_eq, ":party_no", slot_party_ai_state, spai_besieging_center),
                (party_slot_eq, ":party_no", slot_party_ai_object, "$g_encountered_party"),
                (party_slot_eq, ":party_no", slot_party_ai_substate, 1),
                (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
                (call_script, "script_party_set_ai_state", ":party_no", spai_besieging_center, "$g_encountered_party"),
              (try_end),
              (display_message, "@The enemy has been forced to retreat. The assault is over, but the siege continues."),
              (assign, "$g_battle_simulation_cancel_for_party", "$g_encountered_party"),
              (leave_encounter),
              (change_screen_return),
              (assign, "$g_battle_simulation_auto_enter_town_after_battle", "$g_encountered_party"),
            (try_end),
          (try_end),
        (try_end),
        (assign, "$g_siege_first_encounter", 0),
        (assign, "$new_encounter", 0),
        ],
    [
      ("siege_defender_join_battle",
       [
         (neg|troop_is_wounded, "trp_player"),
         ],
          "Join the battle.",[
              (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
              (assign, "$g_battle_result", 0),
              (try_begin),
                (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
                (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_walls),
              (else_try),
                (party_get_slot, ":battle_scene", "$g_encountered_party", slot_castle_exterior),
              (try_end),
              (call_script, "script_calculate_battle_advantage"),
              (val_mul, reg0, 2),
              (val_div, reg0, 3), #scale down the advantage a bit.
              (set_battle_advantage, reg0),
              (set_party_battle_mode),
#              (try_begin),
#                (party_slot_eq, "$current_town", slot_center_siege_with_belfry, 1),
#                (set_jump_mission,"mt_castle_attack_walls_belfry"),
#              (else_try),
                (set_jump_mission,"mt_castle_attack_walls_ladder"),
#              (try_end),
              (jump_to_scene,":battle_scene"),
              (assign, "$g_next_menu", "mnu_siege_started_defender"),
              (jump_to_menu, "mnu_battle_debrief"),
              (change_screen_mission)]),
      ("siege_defender_troops_join_battle",[(call_script, "script_party_count_members_with_full_health", "p_main_party"),
                                            (this_or_next|troop_is_wounded,  "trp_player"),
                                            (ge, reg0, 3)],
          "Order your men to join the battle without you.",[
              (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
              (select_enemy,1),
              (assign,"$g_enemy_party","$g_encountered_party_2"),
              (assign,"$g_ally_party","$g_encountered_party"),
              (assign,"$g_siege_join", 1),
              (jump_to_menu,"mnu_siege_join_defense")]),
##      ("siege_defender_do_not_join_battle",[(call_script, "script_party_count_fit_regulars","p_collective_ally"),
##                                            (gt, reg0, 0)],
##       "Don't get involved.", [(leave_encounter),
##                               (change_screen_return),
##           ]),

##      ("siege_defender_surrender",[(call_script, "script_party_count_fit_regulars","p_collective_ally"),
##                                   (this_or_next|eq, reg0, 0),
##                                   (party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player"),
##                                   ],
##       "Surrender.",[(assign, "$g_player_surrenders", 1),
##                     (jump_to_menu,"mnu_under_siege_attacked_continue")]),
    ]
 ),
( "siege_join_defense",mnf_scale_picture|mnf_disable_all_keys,
    "{s4}^^Your casualties: {s8}^^Allies' casualties: {s9}^^Enemy casualties: {s10}",
    "none",
    code_to_set_city_background + [
        (try_begin),
          (eq, "$g_siege_join", 1),
          (call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
          (assign, ":player_party_strength", reg0),
          (val_div, ":player_party_strength", 5),
        (else_try),
          (assign, ":player_party_strength", 0),
        (try_end),
        
        (call_script, "script_party_calculate_strength", "p_collective_ally", 0),
        (assign, ":ally_party_strength", reg0),
        (val_div, ":ally_party_strength", 5),
        (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
        (assign, ":enemy_party_strength", reg0),
        (val_div, ":enemy_party_strength", 10),

        (store_add, ":friend_party_strength", ":player_party_strength", ":ally_party_strength"),
        (assign, ":enemy_party_strength_for_p", ":enemy_party_strength"),
        (val_mul, ":enemy_party_strength_for_p", ":player_party_strength"),
        (val_div, ":enemy_party_strength_for_p", ":friend_party_strength"),

        (val_sub, ":enemy_party_strength", ":enemy_party_strength_for_p"),
        (inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength_for_p", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s8, s0),

        (inflict_casualties_to_party_group, "$g_ally_party", ":enemy_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s9, s0),
        (party_collect_attachments_to_party, "$g_ally_party", "p_collective_ally"),

        (inflict_casualties_to_party_group, "$g_enemy_party", ":friend_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s10, s0),
        (party_collect_attachments_to_party, "$g_enemy_party", "p_collective_enemy"),

        (try_begin),
          (call_script, "script_party_count_members_with_full_health","p_main_party"),
          (le, reg(0), 0),
          (str_store_string, s4, "str_siege_defender_order_attack_failure"),
        (else_try),
          (call_script, "script_party_count_members_with_full_health","p_collective_enemy"),
          (le, reg(0), 0),
          (assign, "$g_battle_result", 1),
          (str_store_string, s4, "str_siege_defender_order_attack_success"),
        (else_try),
          (str_store_string, s4, "str_siege_defender_order_attack_continue"),
        (try_end),
    ],
    [("continue",[],"Continue...",[(jump_to_menu,"mnu_siege_started_defender"),]),]
 ),

( "village_hunt_down_fugitive_defeated",0,
    "^^^^^A heavy blow from the fugitive sends you to the ground, and your vision spins and goes dark.\
 Time passes. When you open your eyes again you find yourself battered and bloody,\
 but luckily none of the wounds appear to be lethal.",
    "none",
    [],
    [("continue",[],"Continue...",[(jump_to_menu, "mnu_town"),]),],
 ),

( "town_bandits_failed",mnf_disable_all_keys,
    "^^^^^{s4} {s5}",
    "none",
    [
#      (call_script, "script_loot_player_items", 0),
      (store_troop_gold, ":total_gold", "trp_player"),
      (store_div, ":gold_loss", ":total_gold", 30),
      (store_random_in_range, ":random_loss", 40, 100),
      (val_add, ":gold_loss", ":random_loss"),
      (val_min, ":gold_loss", ":total_gold"),
      (troop_remove_gold, "trp_player",":gold_loss"),
      (party_set_slot, "$current_town", slot_center_has_bandits, 0),
      (party_get_num_companions, ":num_companions", "p_main_party"),
      (str_store_string, s4, "@The assasins beat you down and leave you for dead. ."),
      (str_store_string, s4, "@You have fallen. The bandits quickly search your body for valuables they can find,\
 then vanish into the night. They have left you alive, if only barely."),
      (try_begin),
        (gt, ":num_companions", 2),
        (str_store_string, s5, "@Luckily some of your companions came to search for you when you did not return, and find you lying in the ditch. They carried you to safety and dressed your wounds."),
      (else_try),
        (str_store_string, s5, "@Luckily some passing locals found you lying in the ditch, and recognised you as someone other than a simple beggar. They carried you to safety and dressed your wounds."),
      (try_end),
    ],
    [("continue",[],"Continue...",[(change_screen_return)]),],
 ),
( "town_bandits_succeeded",mnf_disable_all_keys,
    "^^^^^The goblins fall before you as wheat to a scythe! Soon you stand alone\
 while most of your attackers lie unconscious, dead or dying.\
 Surely the locals would be very grateful that you saved them from this menace.",
    "none",
    [
      (party_set_slot, "$current_town", slot_center_has_bandits, 0),
      (assign, "$g_last_defeated_bandits_town", "$g_encountered_party"),
      (try_begin),
        (check_quest_active, "qst_deal_with_night_bandits"),
        (neg|check_quest_succeeded, "qst_deal_with_night_bandits"),
        (quest_slot_eq, "qst_deal_with_night_bandits", slot_quest_target_center, "$g_encountered_party"),
        (call_script, "script_succeed_quest", "qst_deal_with_night_bandits"),
      (try_end),
      (store_mul, ":xp_reward", "$num_center_bandits", 117),
      (add_xp_to_troop, ":xp_reward", "trp_player"),
      (store_mul, ":gold_reward", "$num_center_bandits", 50),
      (quest_get_slot, ":quest_giver", "qst_deal_with_night_bandits", slot_quest_giver_troop),
      (store_troop_faction, ":quest_faction", ":quest_giver"),
      #(call_script, "script_troop_add_gold","trp_player",":gold_reward"),
      (call_script, "script_add_faction_rps", ":quest_faction", ":gold_reward"),
    ],
    [("continue",[],"Continue...",[(change_screen_return)]),],
 ),

( "town_brawl_lost",mnf_disable_all_keys,
    "^^^^^^You have been knocked out cold. The people you attacked quickly search you for valuables, before carrying on with their daily business.",
    "none",
    [ (store_troop_gold, ":total_gold", "trp_player"),
      (store_div, ":gold_loss", ":total_gold", 30),
      (store_random_in_range, ":random_loss", 40, 100),
      (val_add, ":gold_loss", ":random_loss"),
      (val_min, ":gold_loss", ":total_gold"),
      #(troop_remove_gold, "trp_player",":gold_loss"),
      (call_script, "script_add_faction_rps", "$ambient_faction", ":gold_loss"),
    ],
    [("continue",[],"Continue...",[(change_screen_return)]),],
 ),
( "town_brawl_won",mnf_disable_all_keys,
    "^^^^^You have beaten all the opponents and the guards sent to quell the disturbance. You quickly frisk them for valuables then vanish until tempers quieten down.^Maybe next time they would show more respect and back off.",
    "none",
    [ (store_random_in_range, ":random_gold", 200, 500),
      #(call_script, "script_troop_add_gold", "trp_player", ":random_gold"),
      (call_script, "script_add_faction_rps", "$ambient_faction", ":random_gold"),
    ],
    [("continue",[],"Continue...",[(change_screen_return)]),],
 ),
  
( "close",0,"Nothing.", "none",[(change_screen_return)],[]),

( "town",mnf_enable_hot_keys|city_menu_color,
	"You arrived in {s60}.{s12}{s13}",
    "none",
    code_to_set_city_background + [   
		
		(call_script, "script_unequip_items", "trp_player"), # after a shop, player returns to this menu so check here
		
		(try_begin),
          (eq, "$sneaked_into_town", 1),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_town_infiltrate),
        (else_try),
          #MV: commented this out - lets both the map travel and town music continue to this menu
          #(call_script, "script_music_set_situation_with_culture", mtf_sit_travel), 
        (try_end),
		(assign, "$current_town","$g_encountered_party"),   # mtarini...  was:(store_encountered_party,"$current_town"),
		
        (call_script, "script_update_center_recon_notes", "$current_town"),
        (assign, "$g_defending_against_siege", 0),
        (str_clear, s3),
        (party_get_battle_opponent, ":besieger_party", "$current_town"),
        (store_faction_of_party, ":encountered_faction", "$g_encountered_party"),
        (party_get_slot, ":encountered_subfaction", "$g_encountered_party", slot_party_subfaction),

		(try_begin),
			(eq, ":encountered_faction", "fac_gondor"),
			(neq, ":encountered_subfaction", 0),
			(store_add, ":str_subfaction", ":encountered_subfaction", "str_subfaction_gondor_name_begin"),
			(str_store_string, s61, ":str_subfaction"),
		(else_try),
			(str_store_faction_name, s61,":encountered_faction"), # non subfaction city get faction name in S61
		(try_end),

        (store_relation, ":faction_relation", ":encountered_faction", "fac_player_supporters_faction"),
		
		#(party_get_slot,reg22, "$current_town", slot_party_subfaction),
		#(party_get_slot,reg23, "$current_town", slot_town_weaponsmith),
		#(str_store_troop_name, s24, reg23 ),
		#(troop_get_slot, reg24, reg23 , slot_troop_subfaction),
		
        (try_begin),
          (gt, ":besieger_party", 0),
          (ge, ":faction_relation", 0),
          (store_faction_of_party, ":besieger_party_faction", ":besieger_party"),
          (store_relation, ":besieger_party_relation", ":besieger_party_faction", "fac_player_supporters_faction"),
          (lt, ":besieger_party_relation", 0),
          (assign, "$g_defending_against_siege", 1),
          (assign, "$g_siege_first_encounter", 1),
          (jump_to_menu, "mnu_siege_started_defender"),
        (try_end),

        #Quest menus
        (try_begin),
          (gt, "$quest_auto_menu", 0),
          (jump_to_menu, "$quest_auto_menu"),
          (assign, "$quest_auto_menu", 0),
        (try_end),

        (assign, "$talk_context", 0),
        (assign,"$all_doors_locked",0),

        (try_begin),
          (eq, "$g_town_visit_after_rest", 1),
          (assign, "$g_town_visit_after_rest", 0),
          #(assign, "$town_entered", 1),
        (try_end),

        (try_begin),
          (eq,"$g_leave_town",1),
          (assign,"$g_leave_town",0),
          (assign,"$g_permitted_to_center",0),
          (leave_encounter),
          (change_screen_return),
        (try_end),

        (str_store_party_name,s2, "$current_town"),
		(str_store_string, s60, s2),
        (party_get_slot, ":center_lord", "$current_town", slot_town_lord),
        (store_faction_of_party, ":center_faction", "$current_town"),
        (str_store_faction_name,s9,":center_faction"),
        (try_begin),
          (ge, ":center_lord", 0),
          (str_store_troop_name,s8,":center_lord"),
          (str_store_string,s7,"@{s8} of {s9}"),
        (try_end),
        
        #(try_begin),
        #  (party_slot_eq,"$current_town",slot_party_type, spt_town),
        #  (party_get_slot, ":prosperity", "$current_town", slot_town_prosperity),
        #  (val_add, ":prosperity", 5),
        #  (store_div, ":str_offset", ":prosperity", 10),
        #  (store_add, ":str_id", "str_town_prosperity_0",  ":str_offset"),
        #  (str_store_string, s10, ":str_id"),
        #(else_try),
        #  (str_store_string,s10,"@You are at {s2}."),
        #(try_end),
        
        (str_clear, s12),
        # (try_begin),
          # (party_slot_eq,"$current_town",slot_party_type, spt_town),
          # (party_get_slot, ":center_relation", "$current_town", slot_center_player_relation),
          # (call_script, "script_describe_center_relation_to_s3", ":center_relation"),
          # (assign, reg9, ":center_relation"),
          # (str_store_string, s12, "@ {s3} ({reg9})."),
		# (try_end),

        (str_clear, s13),

        #night?
        (try_begin), 
         (store_time_of_day,reg(12)),
         (ge,reg(12),5),
         (lt,reg(12),21),
         (assign,"$town_nighttime",0),
        (else_try),
         (assign,"$town_nighttime",1),
         (party_slot_eq,"$current_town",slot_party_type, spt_town),
         (str_store_string, s13, "str_town_nighttime"),
        (try_end),
        
        (try_begin), 
          (gt,"$entry_to_town_forbidden",0),
          (str_store_string, s13, "@{s13}^^You have successfully sneaked in."),
        (try_end),
		
		(assign, "$bs_day_sound", 0), # specific ambiance?
		(assign, "$bs_night_sound", 0),
	
        #(assign,"$castle_undefended",0),
        #(party_get_num_companions, ":castle_garrison_size", "p_collective_enemy"),
        #(try_begin),
        #  (eq,":castle_garrison_size",0),
        #  (assign,"$castle_undefended",1),
        #(try_end),
        ],
    [
       # stub menus to make passage 2 lead to castle
	   ("town_menu_0",[(eq,0,1),],"Go to some location.",
       [], "Door to some location."),

       ("town_approach",[(party_slot_eq,"$current_town",slot_party_type, spt_town),
          (this_or_next|eq,"$entry_to_town_forbidden",0),
          (eq, "$sneaked_into_town",1),
		  (try_begin),   # elder troop stores center common name in plural register
		    (neg|party_slot_eq, "$current_town", slot_town_elder, "trp_no_troop"),
			(party_get_slot, ":elder_troop", "$current_town", slot_town_elder),
		    (str_store_troop_name_plural, s1, ":elder_troop"),
		  (else_try),
		    (str_store_string, s1, "@the_place"),
		  (try_end),
		  ],"Approach {s1}...",
       [(call_script, "script_initialize_center_scene"),
		(assign, "$spawn_horse", 0),
		(try_begin),(troop_is_mounted, "trp_player"),(set_jump_entry, 1),
		 (else_try),                                 (set_jump_entry, 2),
		(try_end),
		(party_get_slot, ":town_scene", "$current_town", slot_town_center),
        (jump_to_scene, ":town_scene"),
        (change_screen_mission),
	   ]),

	   ("town_castle",[
          (party_slot_eq,"$current_town",slot_party_type, spt_town),
          (eq,"$entry_to_town_forbidden",0),
          (neg|party_slot_eq,"$current_town", slot_town_castle, -1),
		  
		  (try_begin),   # elder troop stores center common name in plural register
			(party_get_slot, ":barman_troop", "$current_town", slot_town_barman),
		    (neq, ":barman_troop",  "trp_no_troop"),
		    (neq, ":barman_troop",  -1),
			(party_get_slot, ":barman_troop", "$current_town", slot_town_barman),
		    (str_store_troop_name_plural, s1, ":barman_troop"),
		  (else_try),
		    (str_store_string, s1, "@the_castle"),
		  (try_end),
		  
#          (party_slot_eq, "$current_town", slot_castle_visited, 1), #check if scene has been visited before to allow entry from menu. Otherwise scene will only be accessible from the town center.
          ],"Go to {s1}.",
		  
       [
           (try_begin),
             (this_or_next|eq, "$all_doors_locked", 1),
             (eq, "$sneaked_into_town", 1),
             (display_message,"str_door_locked",0xFFFFAAAA),
           (else_try),
#             (party_get_slot, ":castle_scene", "$current_town", slot_town_castle),
#             (scene_slot_eq, ":castle_scene", slot_scene_visited, 0),
#             (display_message,"str_door_locked",0xFFFFAAAA),
#           (else_try),
             #(assign, "$town_entered", 1),
             (call_script, "script_enter_court", "$current_town"),
           (try_end),
        ], "Door to the castle."),
      
      ("town_center",[
          (party_slot_eq,"$current_town",slot_party_type, spt_town),
		  (party_slot_eq,"$current_town",slot_center_visited, 1),
          (this_or_next|eq,"$entry_to_town_forbidden",0),
          (eq, "$sneaked_into_town",1),
	   ], "Walk to the main square...",
     [ (call_script, "script_initialize_center_scene"),
	   (assign, "$spawn_horse", 1),
       #(assign, "$town_entered", 1),
	   (party_set_slot,"$current_town", slot_center_visited, 1),
	   (set_jump_entry, 0),
       (party_get_slot, ":town_scene", "$current_town", slot_town_center),
	   (jump_to_scene, ":town_scene"),
       (change_screen_mission),
	   ], "Door to the town center."),

	          
	   ("aw_chamber",
       [(eq, 1, 0)],"Never: Enter the AW chamber.",
       [ 
	  	 (set_jump_mission,"mt_aw_tomb"),
	     (jump_to_scene, "scn_aw_tomb"),
         (change_screen_mission),
       ],"Open the door."),

		
	  ("trade_with_arms_merchant",[(party_slot_eq,"$current_town",slot_party_type, spt_town),
	  (this_or_next|eq,"$tld_option_crossdressing", 1),(eq,"$entry_to_town_forbidden",0), #  crossdresser can get in
      (this_or_next|eq,"$tld_option_town_menu_hidden",0),(party_slot_eq, "$current_town", slot_weaponsmith_visited, 1), #check if weaponsmith has been visited before to allow entry from menu. Otherwise scene will only be accessible from the town center.
      (neg|party_slot_eq, "$current_town", slot_town_weaponsmith, "trp_no_troop"),
	  (party_get_slot, ":troop", "$current_town", slot_town_weaponsmith),
	  (str_store_troop_name_plural, s40, ":troop"),],
       "Visit the {s40}.",
       [(party_get_slot, ":troop", "$current_town", slot_town_weaponsmith),(change_screen_trade, ":troop")]),
		
	  ("trade_with_horse_merchant",[(party_slot_eq,"$current_town",slot_party_type, spt_town),
	  (this_or_next|eq,"$tld_option_crossdressing", 1),(eq,"$entry_to_town_forbidden",0), #  crossdresser can get in
      (this_or_next|eq,"$tld_option_town_menu_hidden",0),(party_slot_eq, "$current_town", slot_merchant_visited, 1), #check if horse_merchant has been visited before to allow entry from menu. Otherwise scene will only be accessible from the town center.
      (neg|party_slot_eq, "$current_town", slot_town_merchant, "trp_no_troop"),
	  (party_get_slot, ":troop", "$current_town", slot_town_merchant),
	  (str_store_troop_name_plural, s41, ":troop"),],
       "Visit the {s41}.",
       [(party_get_slot, ":troop", "$current_town", slot_town_merchant),(change_screen_trade, ":troop")]),

#	  ("improve_equipment",[
#		(party_slot_eq,"$current_town",slot_party_type, spt_town),
#	  	(this_or_next|eq,"$tld_option_crossdressing", 1),(eq,"$entry_to_town_forbidden",0), #  crossdresser can get in
#      		(this_or_next|eq,"$tld_option_town_menu_hidden",0),(party_slot_eq, "$current_town", slot_weaponsmith_visited, 1), #check if weaponsmith has been visited before to allow entry from menu. Otherwise scene will only be accessible from the town center.
#      		(neg|party_slot_eq, "$current_town", slot_town_weaponsmith, "trp_no_troop"),
#      		(call_script, "script_get_faction_rank", "$g_talk_troop_faction"), (assign, ":rank", reg0), #rank points to rank number 0-9
#     		(ge, ":rank", 9),
#	  	(party_get_slot, ":troop", "$current_town", slot_town_weaponsmith),
#	  	(str_store_troop_name, s40, ":troop"),],
#       "Have {s40} improve your equipment.",
#       [
#	(party_get_slot, ":troop", "$current_town", slot_town_weaponsmith),
#             (modify_visitors_at_site,"scn_conversation_scene"),(reset_visitors),
#             (set_visitor,	0,	"trp_player"),
#             (set_visitor,	17,	":troop"),
#             (set_jump_mission,"mt_conversation_encounter"),
#             (jump_to_scene,"scn_conversation_scene"),
#             (assign, "$talk_context", tc_improve_equipment),
#             (change_screen_map_conversation, ":troop")
#	]),


	   ("town_prison", [(eq,1,0)],"Never: Enter the prison.",
       [   (try_begin),
             (eq,"$all_doors_locked",1),
             (display_message,"str_door_locked",0xFFFFAAAA),
           (else_try),
             (this_or_next|party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
             (eq, "$g_encountered_party_faction", "$players_kingdom"),
             #(assign, "$town_entered", 1),
             (call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle"),
           (else_try),
             (display_message,"str_door_locked",0xFFFFAAAA),
           (try_end),
        ],"Door to the prison."),
		
		
	 #Enter dungeon in Erebor begin (Kolba)
      ("dungeon_enter",[(eq, cheat_switch, 1), # not done yet
	    (party_slot_eq,"$current_town",slot_party_type, spt_town),
        (eq, "$current_town", "p_town_erebor"),
        (quest_slot_ge, "qst_find_lost_spears", slot_quest_current_state, 1),
        ],"Search for the lost spears inside the mountains.",[
              (set_jump_mission, "mt_tld_erebor_dungeon"),
              (modify_visitors_at_site,"scn_erebor_dungeon_01"),	      
              (reset_visitors),
              (set_visitor,1,"trp_player"),
              (set_visitor, 2, "trp_goblin_gundabad"),
              (set_visitor, 3, "trp_fell_orc_warrior_gundabad"),
              (set_visitor, 4, "trp_orc_fighter_gundabad"),
              (jump_to_scene, "scn_erebor_dungeon_01"),
              (change_screen_mission),
       ],"Open the door."),
      #Enter dungeon in Erebor end (Kolba)	  
		
	("talk_to_castle_commander",[(party_slot_eq,"$current_town",slot_party_type, spt_town),
	   	  (eq,"$entry_to_town_forbidden",0), 
          (party_get_num_companions, ":no_companions", "$g_encountered_party"),
          (ge, ":no_companions", 1),
       ],"Visit the {s61} Barracks.",[
             (set_jump_mission,"mt_conversation_encounter"),
             (modify_visitors_at_site,"scn_conversation_scene"),(reset_visitors),
             (set_visitor,0,"trp_player"),
             (call_script, "script_get_party_max_ranking_slot", "$g_encountered_party"),
             (party_stack_get_troop_id, reg6,"$g_encountered_party",reg0),
             (party_stack_get_troop_dna,reg7,"$g_encountered_party",reg0),
             (set_visitor,17,reg6,reg7),
             (jump_to_scene,"scn_conversation_scene"),
             (assign, "$talk_context", tc_hire_troops),
             (change_screen_map_conversation, reg6)
             ]),
		
      ("speak_with_elder",[(party_slot_eq,"$current_town",slot_party_type, spt_town),
	  (this_or_next|eq,"$tld_option_crossdressing", 1),(eq,"$entry_to_town_forbidden",0), #  crossdresser can get in
      (this_or_next|eq,"$tld_option_town_menu_hidden",0),(party_slot_eq, "$current_town", slot_elder_visited, 1), #check if elder has been visited before to allow entry from menu. Otherwise scene will only be accessible from the town center.
      (neg|party_slot_eq, "$current_town", slot_town_elder, "trp_no_troop"),
	  (party_get_slot, ":elder_troop", "$current_town", slot_town_elder),
	  (str_store_troop_name, s6, ":elder_troop"),
	  ],
       "Speak with the {s6}.",
       [   (party_get_slot, ":elder_troop", "$current_town", slot_town_elder),
           (call_script, "script_setup_troop_meeting", ":elder_troop", 0),
        ]),

	  ("castle_wait",
       [   (party_slot_eq,"$current_town",slot_party_type, spt_town),
		   (eq,"$entry_to_town_forbidden",0),
           (this_or_next|ge, "$g_encountered_party_relation", 0),
           (eq,"$castle_undefended",1),
           (str_clear, s1),
           (str_clear, s2),
           (try_begin),
             #(neg|party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
             (party_get_num_companions, ":num_men", "p_main_party"),
             (store_div, reg1, ":num_men", 4),
             (val_add, reg1, 1),
             (store_troop_gold, ":gold", "trp_player"),
             (ge, ":gold", reg1),
             (str_store_string, s1, "@Stay indoors for some time ({reg1} Resource points per night)"),
           (else_try),
		     # not enough money... can rest anyway (but no health bonus)
             (str_store_string, s1, "@Camp outside for some time (free)"),
           (try_end),
			##           (eq, "$g_defending_against_siege", 0),
        ],
         "{s1}.",
         [ (assign,"$auto_enter_town","$current_town"),
           (assign, "$g_town_visit_after_rest", 1),
           (assign, "$g_last_rest_center", "$current_town"),
           (assign, "$g_last_rest_payment_until", -1),
           (rest_for_hours_interactive, 24 * 7, 5, 0), #rest while not attackable
           (change_screen_return),
          ]),

#      ("siege_leave",[(eq, "$g_defending_against_siege", 1)],"Try to break out...",[(jump_to_menu,"mnu_siege_break_out")]),#TODO: Go to Menu here.
 ]+concatenate_scripts([[ 
     ("town_cheat_alley",[(eq, cheat_switch, 1),(party_slot_eq,"$current_town",slot_party_type, spt_town),(eq, "$cheat_mode", 1)], "CHEAT: Go to the alley.",[
							(party_get_slot, reg(11), "$current_town", slot_town_alley),
							(set_jump_mission,"mt_ai_training"),
							(jump_to_scene,reg(11)),
							(change_screen_mission)]),
      ("castle_cheat_interior",[(eq, cheat_switch, 1),(eq, "$cheat_mode", 1)], "CHEAT! Interior.",[
							(set_jump_mission,"mt_ai_training"),
							(party_get_slot, ":castle_scene", "$current_town", slot_town_castle),
							(jump_to_scene,":castle_scene"),
							(change_screen_mission)]),
      ("castle_cheat_town_exterior",[(eq, cheat_switch, 1),(eq, "$cheat_mode", 1)], "CHEAT: Exterior.",[
							(try_begin),
								(party_slot_eq,"$current_town",slot_party_type, spt_castle),
								(party_get_slot, ":scene", "$current_town", slot_castle_exterior),
							(else_try),
								(party_get_slot, ":scene", "$current_town", slot_town_center),
							(try_end),
							(set_jump_mission,"mt_ai_training"),
							(jump_to_scene,":scene"),
							(change_screen_mission)]),
      ("castle_cheat_dungeon",[(eq, cheat_switch, 1),(eq, "$cheat_mode", 1)], "CHEAT: Prison.",[
							(set_jump_mission,"mt_ai_training"),
							(party_get_slot, ":castle_scene", "$current_town", slot_town_prison),
							(jump_to_scene,":castle_scene"),
							(change_screen_mission)]),
      ("castle_cheat_town_walls",[(eq, cheat_switch, 1),(eq, "$cheat_mode", 1),(party_slot_eq,"$current_town",slot_party_type, spt_town),], "CHEAT! Town Walls.",[
							(party_get_slot, ":scene", "$current_town", slot_town_walls),
							(set_jump_mission,"mt_ai_training"),
							(jump_to_scene,":scene"),
							(change_screen_mission)]),
      ("cheat_town_start_siege",[(eq, cheat_switch, 1),(eq, "$cheat_mode", 1),
								(party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
								(lt, "$g_encountered_party_2", 1),
								(call_script, "script_party_count_fit_for_battle","p_main_party"),
								(gt, reg(0), 1),
								(try_begin),
									(party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
									(assign, reg6, 1),
								(else_try),
									(assign, reg6, 0),
								(try_end)],
				   "CHEAT: Besiege the {reg6?town:castle}...",
				   [   (assign,"$g_player_besiege_town","$g_encountered_party"),
					   (jump_to_menu, "mnu_castle_besiege"),
					   ]),
      ("center_reports",[(eq, "$cheat_mode", 1),], "CHEAT: Show reports.",
						[(jump_to_menu,"mnu_center_reports")]),
      ("sail_from_port",[(eq, cheat_switch, 1),(party_slot_eq,"$current_town",slot_party_type, spt_town),(eq, "$cheat_mode", 1),#(party_slot_eq,"$current_town",slot_town_near_shore, 1),
                        ], "CHEAT: Sail from port.",
						[(assign, "$g_player_icon_state", pis_ship),
						(party_set_flags, "p_main_party", pf_is_ship, 1),
						(party_get_position, pos1, "p_main_party"),
						(map_get_water_position_around_position, pos2, pos1, 6),
						(party_set_position, "p_main_party", pos2),
						(assign, "$g_main_ship_party", -1),
						(change_screen_return)]),
 ] for ct in range(cheat_switch)])+[

 ]+concatenate_scripts([[ 
      ("town_cheat_alley",[(eq, 0, 1),], "CHEAT",[]),
	  ("castle_cheat_interior",[(eq, 0, 1),], "CHEAT",[]),
	  ("castle_cheat_town_exterior",[(eq, 0, 1),], "CHEAT",[]),
	  ("castle_cheat_dungeon",[(eq, 0, 1),], "CHEAT",[]),
	  ("castle_cheat_town_walls",[(eq, 0, 1),], "CHEAT",[]),
	  ("cheat_town_start_siege",[(eq, 0, 1),], "CHEAT",[]),
	  ("center_reports",[(eq, 0, 1),], "CHEAT",[]),
	  ("sail_from_port",[(eq, 0, 1),], "CHEAT",[]),
 ] for ct in range(1-cheat_switch)])+[

	  ("isengard_underground",[(party_slot_eq,"$current_town",slot_party_type, spt_town),(eq, "$current_town", "p_town_isengard"),(eq,"$entry_to_town_forbidden",0)
						], "Go to the underground caverns.",
						[(set_jump_mission, "mt_town_center"),
						(jump_to_scene, "scn_isengard_underground"),
						(change_screen_mission)]),
	  ("tirith_toplevel",[(party_slot_eq,"$current_town",slot_party_type, spt_town),(eq, "$current_town", "p_town_minas_tirith"),(eq,"$entry_to_town_forbidden",0)
						], "Climb up to the top level.",
						[(assign, "$bs_day_sound", "snd_wind_ambiance"),
						 (assign, "$bs_night_sound", "snd_wind_ambiance"),
						 (set_jump_mission, "mt_town_center"),
						 (jump_to_scene, "scn_minas_tirith_center_top"),
						 (change_screen_mission)]),
						
      ("town_leave",[],"Leave...",[
            (assign, "$g_permitted_to_center",0),
            (change_screen_return,0),
            (store_faction_of_party, ":fac", "$current_town"),
            (try_begin),
		(eq|this_or_next, ":fac", "fac_mordor"),
		(eq, ":fac", "fac_guldur"),
	    	(call_script, "script_update_respoint"), # Updates resource points		
	    (try_end),
          ],"Leave Area"),

    ]
 ),

( "disembark",0,
    "Do you wish to disembark?",
    "none",
    [(set_background_mesh, "mesh_ui_default_menu_window"), ],
    [("disembark_yes", [], "Yes.",
       [(assign, "$g_player_icon_state", pis_normal),
        (party_set_flags, "p_main_party", pf_is_ship, 0),
        (party_get_position, pos1, "p_main_party"),
		(map_get_land_position_around_position,pos0,pos1,1),
        (party_set_position, "p_main_party", pos0),
        (try_begin),
#          (eq,1,0),  # empty ship commented out, GA
		  (le, "$g_main_ship_party", 0),
          (set_spawn_radius, 0),
          (spawn_around_party, "p_main_party", "pt_none"),
          (assign, "$g_main_ship_party", reg0),
          (party_set_flags, "$g_main_ship_party", pf_is_static|pf_always_visible|pf_hide_defenders|pf_is_ship, 1),
          (str_store_troop_name, s1, "trp_player"),
          (party_set_name, "$g_main_ship_party", "@{s1}'s Ship"),
          (party_set_icon, "$g_main_ship_party", "icon_ship"),
          (party_set_slot, "$g_main_ship_party", slot_party_type, spt_ship),
        (try_end),
        (enable_party, "$g_main_ship_party"),
        (party_set_position, "$g_main_ship_party", pos0),
        (party_set_icon, "$g_main_ship_party", "icon_ship_on_land"),
        (assign, "$g_main_ship_party", -1),
        (change_screen_return),
        ]),
      ("disembark_no", [], "No.",
       [(party_get_position, pos1, "p_main_party"),
		(map_get_water_position_around_position,pos0,pos1,1),
        (party_set_position, "p_main_party", pos0),
		(party_set_ai_object,"p_main_party", "p_main_party"),
		(change_screen_return),
        ]),
    ]
 ),
( "ship_reembark",0,
    "Do you wish to embark?",
    "none",
    [],
    [ ("reembark_yes", [], "Yes.",
       [(assign, "$g_player_icon_state", pis_ship),
        (party_set_flags, "p_main_party", pf_is_ship, 1),
        (party_get_position, pos1, "p_main_party"),
        (map_get_water_position_around_position, pos2, pos1, 6),
        (party_set_position, "p_main_party", pos2),
        (assign, "$g_main_ship_party", "$g_encountered_party"),
        (disable_party, "$g_encountered_party"),
        (change_screen_return),
        ]),
      ("reembark_no", [], "No.",
       [(change_screen_return),
        ]),
    ]
 ),

( "center_reports",city_menu_color,
    "Town Name: {s1}^Rent Income: {reg1} denars^Tariff Income: {reg2} denars^Food Stock: for {reg3} days",
    "none",
    code_to_set_city_background + [
	 (set_background_mesh, "mesh_ui_default_menu_window"),

	 (party_get_slot, ":town_food_store", "$g_encountered_party", slot_party_food_store),
     (call_script, "script_center_get_food_consumption", "$g_encountered_party"),
     (assign, ":food_consumption", reg0),
     (store_div, reg3, ":town_food_store", ":food_consumption"),
     (str_store_party_name, s1, "$g_encountered_party"),
     (party_get_slot, reg1, "$g_encountered_party", slot_center_accumulated_rents),
     (party_get_slot, reg2, "$g_encountered_party", slot_center_accumulated_tariffs),
     ],
    [
      
      ("go_back_dot",[],"Go back.",
       [(try_begin),
          # (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
          # (jump_to_menu, "mnu_village"),
        # (else_try),
          (jump_to_menu, "mnu_town"),
        (try_end),
        ]),
    ]
 ),

( "sneak_into_town_suceeded",city_menu_color,
    "Disguised in the garments of a poor pilgrim, you fool the guards and make your way into the town.",
    "none",
     code_to_set_city_background +  [	],
    [("continue",[],"Continue...",[(assign, "$sneaked_into_town",1),(jump_to_menu,"mnu_town")])]
 ),
( "sneak_into_town_caught",city_menu_color,
    "As you try to sneak in, one of the guards recognizes you and raises the alarm!\
 You must flee back through the gates before all the guards in the town come down on you!",
    "none",
     code_to_set_city_background + [
	 (assign, "$recover_after_death_menu", "mnu_recover_after_death_town_alone"),
     #(assign,"$auto_menu","mnu_tld_player_defeated"),
    ],
    [("sneak_caught_fight",[],"Try to fight your way out!",
       [   (assign,"$all_doors_locked",1),
           (party_get_slot, ":sneak_scene", "$current_town",slot_town_center), # slot_town_gate),
           (set_jump_mission,"mt_sneak_caught_fight"),
           (modify_visitors_at_site,":sneak_scene"),(reset_visitors),
           (set_visitor,0,"trp_player"),
           (store_faction_of_party, ":town_faction","$current_town"),
           (faction_get_slot, ":tier_2_troop", ":town_faction", slot_faction_tier_2_troop),
           (faction_get_slot, ":tier_3_troop", ":town_faction", slot_faction_tier_3_troop),
           (try_begin),
             (gt, ":tier_2_troop", 0),
             (gt, ":tier_3_troop", 0),
             (assign,reg(0),":tier_3_troop"),
             (assign,reg(1),":tier_3_troop"),
             (assign,reg(2),":tier_2_troop"),
             (assign,reg(3),":tier_2_troop"),
           (else_try),
             (assign,reg(0),"trp_skirmisher_of_rohan"),
             (assign,reg(1),"trp_veteran_skirmisher_of_rohan"),
             (assign,reg(2),"trp_gondor_veteran_swordsmen"),
             (assign,reg(3),"trp_veteran_skirmisher_of_rohan"),
           (try_end),
           (assign,reg(4),-1),
           (shuffle_range,0,5),
           (set_visitor,1,reg(0)),
           (set_visitor,2,reg(1)),
           (set_visitor,3,reg(2)),
           (set_visitor,4,reg(3)),
 #          (jump_to_menu,"mnu_captivity_start_castle_defeat"),
           (set_passage_menu,"mnu_town"),
           (jump_to_scene,":sneak_scene"),
           (change_screen_mission),
        ]),
      ("sneak_caught_surrender",[],"Surrender.",
       [   (assign, "$recover_after_death_menu", "mnu_recover_after_death_town_alone"),
           (jump_to_menu,"mnu_tld_player_defeated"),
        ]),
    ]
 ),
( "sneak_into_town_caught_dispersed_guards",city_menu_color,
    "You drive off the guards and cover your trail before running off, easily losing your pursuers in the maze of streets.",
    "none",
    code_to_set_city_background + [],
     [("continue",[],"Continue...",[(assign, "$sneaked_into_town",1),(jump_to_menu,"mnu_town")])]
 ),
( "sneak_into_town_caught_ran_away",0,
    "You make your way back through the gates and quickly retreat to the safety out of town.",
    "none",
    [],
    [("continue",[],"Continue...",
       [ (assign,"$auto_menu",-1),
         (store_encountered_party,"$last_sneak_attempt_town"),
         (store_current_hours,"$last_sneak_attempt_time"),
         (change_screen_return),
        ]),
    ]
 ),

( "auto_training_ground_trainer", 0, "stub", "none",
	[	(jump_to_menu, "mnu_town"),
		(assign, "$talk_context", tc_town_talk),
		(party_get_slot, ":training_scene", "$g_encountered_party", slot_town_arena),
		(set_jump_mission, "mt_training_ground_trainer_talk"),
		(modify_visitors_at_site, ":training_scene"),
		(reset_visitors),
		(set_visitor, 0, "trp_player"),
		(jump_to_scene, ":training_scene"),
		(change_screen_mission),
		(music_set_situation, 0),
    ],
    []
 ),
  
## UNIFIED PLAYER DEFEATED MENUS... (mtarini)
###########################
# player death scenario in TLD: no capture, only injury
( "tld_player_defeated",0,
     "^^^^^Suddenly a shattering pain explodes in the back of your head! \ You shiver, as all the world goes black around you...^Is this your end?",
     "none",[
	 (store_add, reg10, "$player_looks_like_an_orc", "mesh_draw_defeat_human"), (set_background_mesh, reg10),
	 (val_add, "$number_of_player_deaths", 1),
	 ],[      
	    ("continue",[],"Continue...",
        [	(assign, "$auto_menu", "$recover_after_death_menu"),
            (rest_for_hours, 8, 8, 0),
			#(jump_to_menu, "$recover_after_death_menu"),
            
            #MV: lose some of your companions
            (try_for_range, ":npc", companions_begin, companions_end),
              (main_party_has_troop, ":npc"),
              (store_random_in_range, ":rand", 0, 100),
              (lt, ":rand", 30),
              (remove_member_from_party, ":npc", "p_main_party"),
              (troop_set_slot, ":npc", slot_troop_occupation, 0),
              (troop_set_slot, ":npc", slot_troop_playerparty_history, pp_history_scattered),
              (store_faction_of_party, ":victorious_faction", "$g_encountered_party"),
              (troop_set_slot, ":npc", slot_troop_playerparty_history_string, ":victorious_faction"),
              (troop_set_health, ":npc", 100),
            (try_end),
            
			(change_screen_map),
			(display_message,"@Time passes..."),
         ]),
	 ]
 ),
( "recover_after_death_fangorn",0,
    "You wake up. The forest is still around you. Every bone hurts. You are alive, by miracle.^^It was a defeat, but at least you were able to see what happened. ^Now you know what is going on in this accursed forest,^and you survived to tell. ^^Will anyone ever believe you?",
	"none",[(try_begin),
				(eq, "$g_battle_result", 1),
				(jump_to_menu, "mnu_fangorn_battle_debrief_won"),
			(else_try),
				(assign, "$recover_after_death_menu", "mnu_recover_after_death_fangorn"),
				(jump_to_menu, "mnu_tld_player_defeated"),
			(try_end),
	 ],[
	 ("continue",[],"Continue...",[
		(troop_set_health,"trp_player",0),
		(try_begin),
			(check_quest_active, "qst_investigate_fangorn"),
			(neg|check_quest_succeeded, "qst_investigate_fangorn"),
			(neg|check_quest_failed, "qst_investigate_fangorn"),
			(call_script, "script_succeed_quest", "qst_investigate_fangorn"),
		(try_end),
		(change_screen_map)])]
 ),
( "recover_after_death_moria",city_menu_color,
    "^^^^^You regain your conciousness. You are lying on soft soil, fresh air breezing on your face. You are outside!^The orcs must have taken you for dead and thrown you in some murky pit.^You must have been carried to the surface by an underground stream.",
    "none",[(set_background_mesh, "mesh_town_moria"),],[
	  ("whatever",[], "Get up!",[ (change_screen_map),(jump_to_menu,"mnu_castle_outside"), ]),
	]
 ),
( "recover_after_death_default",0,
     "^^^^^You regain your conciousness. You lie on the spot you fell.\
  The enemies must have taken you up for dead and left you there.\
  However, it seems that none of your wounds were lethal,\
  and although you feel awful, you find out you can still walk.\
  You get up and try to look for any other survivors from your party.",
     "none",
	 [(set_background_mesh, "mesh_ui_default_menu_window")],[      
	 ("continue",[],"Continue...",[(change_screen_map)])]
 ),
( "recover_after_death_town",0,
     "^^^^You regain your conciousness and find yourself at the town outskirts. \
  You are alive!\
  Nobody is around and you take your chance to drag yourself outside the town.\
  It seems that none of your wounds were lethal,\
  and although you feel awful, you can still walk.",
     "none",code_to_set_city_background,
	 [("continue",[],"Continue...",[(change_screen_map),
	 #(jump_to_menu,"mnu_castle_outside"),
	 ])]
 ),
( "recover_after_death_town_alone",0,
     "You regain your conciousness and find yourself at the town outskirts. \
  You are alive!\
  Nobody is around and you take your chance to drag yourself outside the town.\
 Your companions found you.\
 It seems that none of your wounds were lethal,\
  and although you feel awful, you can still walk.",
     "none",code_to_set_city_background,[      
	 ("continue",[],"Continue...",
        [   (change_screen_map),
            #(jump_to_menu,"mnu_castle_outside"),
         ]),
	 ]
 ),

( "notification_center_under_siege",0,
    "{s1} has been besieged by {s2} of {s3}!",
    "none",
    [(set_background_mesh, "mesh_ui_default_menu_window"),
      (str_store_party_name, s1, "$g_notification_menu_var1"),
      (str_store_troop_name, s2, "$g_notification_menu_var2"),
      (store_troop_faction, ":troop_faction", "$g_notification_menu_var2"),
      (str_store_faction_name, s3, ":troop_faction"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 62),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_center_note_mesh", "$g_notification_menu_var1", pos0),
      ],
    [("continue",[],"Continue...",[(change_screen_return)])]
 ),  
( "notification_one_side_left",0,
    "^^^^^The War of the Ring is over!^^The {s1} have defeated all their enemies and stand victorious!",
    "none",
    # $g_notification_menu_var1 - faction_side_*
    [ (assign, ":side", "$g_notification_menu_var1"),
      (try_begin),
        (eq, ":side", faction_side_good),
        (assign, ":faction", "fac_gondor"),
        (str_store_string, s1, "@Forces of Good"),
      (else_try),
        (eq, ":side", faction_side_eye),
        (assign, ":faction", "fac_mordor"),
        (str_store_string, s1, "@Forces of Mordor"),
      (else_try),
        #(eq, ":side", faction_side_hand),
        (assign, ":faction", "fac_isengard"),
        (str_store_string, s1, "@Forces of Isengard"),
      (try_end),
      
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", ":faction", pos0),
    ],
    [("continue",[],"Continue...",[(change_screen_return)])]
 ),
( "notification_total_defeat",0,
    "^^^^^The War of the Ring is over for you!^^The {s1} have been defeated by their enemies and you stand alone in defeat!",
    "none",
    # $g_notification_menu_var1 - faction_side_*
    [ (assign, ":side", "$g_notification_menu_var1"),
      
      (try_begin),
        (eq, ":side", faction_side_good),
        (assign, ":faction", "fac_gondor"),
        (str_store_string, s1, "@Forces of Good"),
      (else_try),
        (eq, ":side", faction_side_eye),
        (assign, ":faction", "fac_mordor"),
        (str_store_string, s1, "@Forces of Mordor"),
      (else_try),
        #(eq, ":side", faction_side_hand),
        (assign, ":faction", "fac_isengard"),
        (str_store_string, s1, "@Forces of Isengard"),
      (try_end),
      
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", ":faction", pos0),
    ],
    [("continue",[],"Continue...",[(change_screen_return)])]
 ),
( "notification_your_faction_collapsed",0,
    "^^^^^Your {s11} homeland was defeated!^Still, other allies remain in the War. You, together with anyone left from {s11}, can still help your side win.",
    "none",
    [ (str_store_faction_name, s11, "$players_kingdom"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$players_kingdom", pos0),
    ],
    [("continue",[],"Continue...", [(change_screen_return)])]
 ),
( "notification_faction_defeated",0,
    "^^^^^{s1} Defeated!^{s1} is no more, defeated by the forces of {s13}!",
    "none",
    [ (str_store_faction_name, s1, "$g_notification_menu_var1"),
    
      (assign, ":num_theater_enemies", 0),
      (str_store_string, s13, "@their enemies"), #defensive
      (faction_get_slot, ":faction_theater", "$g_notification_menu_var1", slot_faction_home_theater),
      (try_for_range_backwards, ":cur_faction", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
        (store_relation, ":cur_relation", ":cur_faction", "$g_notification_menu_var1"),
        (lt, ":cur_relation", 0),
        (faction_slot_eq, ":cur_faction", slot_faction_home_theater, ":faction_theater"),
        (try_begin),
          (eq, ":num_theater_enemies", 0),
          (str_store_faction_name, s13, ":cur_faction"),
        (else_try),
          (eq, ":num_theater_enemies", 1),
          (str_store_faction_name, s11, ":cur_faction"),
          (str_store_string, s13, "@{s11} and {s13}"),
        (else_try),
          (str_store_faction_name, s11, ":cur_faction"),
          (str_store_string, s13, "@{s11}, {s13}"),
        (try_end),
        (val_add, ":num_theater_enemies", 1),
      (try_end),
      
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      # (try_begin),
        # (is_between, "$g_notification_menu_var1", "fac_gondor", kingdoms_end), #Excluding player kingdom
        # (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_for_menu", "$g_notification_menu_var1", pos0),
      # (else_try),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      # (try_end),
      ],
    [("continue",[],"Continue...",[(change_screen_return)])]
 ),

( "ruins", 0,
    "^^^^You approach the {s1}. A once strong encampment was razed to the ground, though you can still see traces of fortifications and scattered rusty weapons.",
    "none",
    [(set_background_mesh, "mesh_ui_default_menu_window"),
     (str_store_party_name, s1, "$g_encountered_party"),
    ],
    [("leave",[],"Leave.",[(change_screen_return)])]
 ),
( "legendary_place",0,
    "^^^^You have followed the rumors and found {s1}. You can now explore this place and see for yourself if the rumors are true.",
    "none",
    [(set_background_mesh, "mesh_ui_default_menu_window"),
     (str_store_party_name, s1, "$g_encountered_party"),
    ],
    [("explore",[],"Explore this place.",
       [(set_jump_mission, "mt_legendary_place_visit"),
        (try_begin),
          (eq, "$g_encountered_party", "p_legend_amonhen"),
          (assign, ":lp_scene", "scn_amon_hen"),
		  (assign, "$bs_day_sound", "snd_wind_ambiance"),
		  (assign, "$bs_night_sound", "snd_night_ambiance"),
        (else_try),
          (eq, "$g_encountered_party", "p_legend_deadmarshes"),
          (assign, ":lp_scene", "scn_deadmarshes"),
		  (assign, "$bs_day_sound", "snd_deadmarshes_ambiance"),
		  (assign, "$bs_night_sound", "snd_deadmarshes_ambiance"),
        (else_try),
          (eq, "$g_encountered_party", "p_legend_mirkwood"),
          (assign, ":lp_scene", "scn_mirkwood"),
		  (assign, "$bs_day_sound", "snd_evilforest_ambiance"),
		  (assign, "$bs_night_sound", "snd_night_ambiance"),
        (else_try),
          #(eq, "$g_encountered_party", "p_legend_fangorn"),
          (assign, ":lp_scene", "scn_fangorn"),
		  (assign, "$bs_day_sound", "snd_fangorn_ambiance"),
		  (assign, "$bs_night_sound", "snd_night_ambiance"),
        (try_end),
        (modify_visitors_at_site,":lp_scene"),
        (reset_visitors),
        (set_visitor, 1, "trp_player"),
        (jump_to_menu, "mnu_legendary_place"),
        (jump_to_scene,":lp_scene"),
        (change_screen_mission),
       ]),
     ("leave",[],"Leave.",[(change_screen_return)]),
    ]
 ),

( "auto_return_to_map",0,"stub","none",[(change_screen_map)],[]),
#MV: hackery to get around change_screen_exchange_with_party limitations
( "auto_player_garrison",0,"stub","none",
    [(jump_to_menu, "mnu_auto_player_garrison_2"),
     (troop_get_slot, ":reserve_party", "trp_player", slot_troop_player_reserve_party),
     (change_screen_exchange_with_party, ":reserve_party")
    ],
    []
 ),
( "auto_player_garrison_2",0,"stub","none",
    [(jump_to_menu, "mnu_town"),
     
     (set_jump_mission,"mt_conversation_encounter"),
     (modify_visitors_at_site,"scn_conversation_scene"),(reset_visitors),
     (set_visitor,0,"trp_player"),
     (call_script, "script_get_party_max_ranking_slot", "$g_encountered_party"),
     (party_stack_get_troop_id, reg(6),"$g_encountered_party",reg0),
     (party_stack_get_troop_dna,reg(7),"$g_encountered_party",reg0),
     (set_visitor,17,reg(6),reg(7)),
     (jump_to_scene,"scn_conversation_scene"),
     (assign, "$talk_context", tc_hire_troops),
     (change_screen_map_conversation, reg(6)),
    ],
    []
 ),
( "auto_town_brawl",0,"stub","none",
    [
     (party_get_slot, ":town_scene", "$current_town", slot_town_center),
     (modify_visitors_at_site, ":town_scene"),
     (reset_visitors),
     (call_script, "script_init_town_walkers"),
     (set_jump_mission,"mt_town_brawl"),
     (jump_to_scene, ":town_scene"),
     (change_screen_mission),
    ],
    []
 ),
( "auto_intro_rohan",0,"stub","none",
    [
     (set_jump_mission,"mt_intro_rohan"),
     (assign, "$current_town", "p_town_edoras"),
     (modify_visitors_at_site,"scn_westfold_center"),
     (reset_visitors,0),
     (set_visitor, 1, "trp_player"), #needed
     (jump_to_scene,"scn_westfold_center"),
     (change_screen_mission),
    ],
    []
 ),
( "auto_intro_gondor",0,"stub","none",
    [
       (set_jump_mission, "mt_intro_gondor"),
       (assign, "$current_town", "p_town_minas_tirith"), #for the cabbage guards 
       (modify_visitors_at_site, "scn_minas_tirith_center"),
       (reset_visitors),
       (set_visitor, 1, "trp_player"),
       (jump_to_scene, "scn_minas_tirith_center"),
       (change_screen_mission),
    ],
    []
 ),
( "auto_intro_mordor",0,"stub","none",
    [
       (set_jump_mission, "mt_intro_mordor"),
       (assign, "$current_town", "p_town_minas_morgul"), #for the cabbage guards 
       (modify_visitors_at_site, "scn_minas_morgul_center"),
       (reset_visitors),
       (set_visitor, 1, "trp_player"),
       (jump_to_scene, "scn_minas_morgul_center"),
       (change_screen_mission),
    ],
    []
 ),
( "auto_intro_joke",0,"stub","none",
    [
       (set_jump_mission, "mt_intro_joke"),
       (modify_visitors_at_site, "scn_minas_tirith_castle"),
       (reset_visitors),
       (set_visitor, 1, "trp_player"),
       (jump_to_scene, "scn_minas_tirith_castle"),
       (change_screen_mission),
    ],
    []
 ),
( "auto_convo",0,"stub","none",
    [
       (set_jump_mission, "mt_test_gandalf"),
       (modify_visitors_at_site, "scn_conversation_scene"),
       (reset_visitors),
       (set_visitor, 0, "trp_player"),
       (set_visitor, 1, "$g_tld_convo_talker"),
       (jump_to_scene, "scn_conversation_scene"),
       (change_screen_mission),
    ],
    []
 ),
( "auto_conversation_cutscene",0,"stub","none",
    [
       (set_jump_mission, "mt_conversation_cutscene"),
       (modify_visitors_at_site, "scn_conversation_scene"),
       (reset_visitors),
       (set_visitor, 0, "trp_player"),
       (set_visitor, 1, "$g_tld_convo_talker"),
       (jump_to_scene, "scn_conversation_scene"),
       (change_screen_mission),
    ],
    []
 ),
 
###################### starting quest, GA ##############################  
( "starting_quest_good",0,
   "^^^^^^You spot a small caravan under attack from a band of orcs. What will you do?",
   "none",[],
   [("help",[], "Help the strangers!",
     [
     (set_jump_mission,"mt_tld_caravan_help"),
     (modify_visitors_at_site,"scn_starting_quest"),
      (reset_visitors),
      (set_visitor,0,"trp_player"),
      (set_visitors,7,"trp_brigand", 3),
      (set_visitors,8,"trp_brigand", 3),
      (set_visitors,9,"trp_start_quest_caravaneer", 1),
      (set_visitors,17,"trp_tribal_orc", 8),
      (set_visitors,18,"trp_mountain_goblin", 8),
      (set_visitors,19,"trp_fell_uruk_of_mordor", 1),
      (jump_to_scene,"scn_starting_quest"),
      (set_battle_advantage, 0),
      (assign, "$g_battle_result", 0),
      (assign, "$g_next_menu", "mnu_starting_quest_victory"),
      (assign, "$g_mt_mode", vba_normal),
      (assign, "$cant_leave_encounter", 1),
      
      (jump_to_menu, "mnu_starting_quest_victory"),
      (change_screen_mission),
      (assign,"$talk_context",tc_starting_quest),
#     (call_script, "script_setup_troop_meeting","trp_start_quest_caravaneer", 255),
      ]),
   ("go_your_way",[],"Leave them alone",[(change_screen_map),]),
 ]),
( "starting_quest_victory",0,"null","none",
    [(call_script, "script_setup_troop_meeting","trp_start_quest_caravaneer", 255),
#     (leave_encounter),
#     (change_screen_return),
	],[]
 ),

( "custom_battle_choose_faction1",0,
    "^^^^^^^^^^Choose your side and advantage:", "none", [(set_background_mesh, "mesh_relief01")],
    [
 ]+concatenate_scripts([[ 	
	#("good_2xmore",[],"Good faction, 2x advantage",[(assign,"$cbadvantage", 3),(jump_to_menu,"mnu_custom_battle_choose_faction2"),]),
     ("good_equal" ,[],"Good faction"         ,[(assign,"$cbadvantage", 2),(jump_to_menu,"mnu_custom_battle_choose_faction2"),]),
	 #("good_2xless",[],"Good faction, 2x handicap" ,[(assign,"$cbadvantage", 1),(jump_to_menu,"mnu_custom_battle_choose_faction2"),]),
     #("bad_2xmore" ,[],"Evil faction, 2x advantage",[(assign,"$cbadvantage",-3),(jump_to_menu,"mnu_custom_battle_choose_faction2"),]),
     ("bad_equal"  ,[],"Evil faction"         ,[(assign,"$cbadvantage",-2),(jump_to_menu,"mnu_custom_battle_choose_faction2"),]),
	 #("bad_2xless" ,[],"Evil faction, 2x handicap" ,[(assign,"$cbadvantage",-1),(jump_to_menu,"mnu_custom_battle_choose_faction2"),]),
     ("replay_prev",[],"Replay previous setup",[(jump_to_menu,"mnu_custom_battle_2"),]),
 ] for ct in range(cheat_switch)])+[
     ("go_back"    ,[],"Go back"              ,[(jump_to_menu,"mnu_start_game_3")]),
 ]),
( "custom_battle_choose_faction2",0,
    "^^^^^^^^^^Choose good faction", "none", [(set_background_mesh, "mesh_relief01")],
    [
 ]+concatenate_scripts([[	
	("cb_gondor"    ,[],"Gondor"    ,[(assign,"$faction_good",fac_gondor  ),(jump_to_menu,"mnu_custom_battle_choose_faction3"),]),
     ("cb_gondor1"   ,[],"Rohan"     ,[(assign,"$faction_good",fac_rohan   ),(jump_to_menu,"mnu_custom_battle_choose_faction3"),]),
     ("cb_gondor2"   ,[],"Lothlorien",[(assign,"$faction_good",fac_lorien  ),(jump_to_menu,"mnu_custom_battle_choose_faction3"),]),
     ("cb_gondor3"   ,[],"Rivendell" ,[(assign,"$faction_good",fac_imladris),(jump_to_menu,"mnu_custom_battle_choose_faction3"),]),
     ("cb_gondor4"   ,[],"Mirkwood"  ,[(assign,"$faction_good",fac_woodelf ),(jump_to_menu,"mnu_custom_battle_choose_faction3"),]),
     ("cb_gondor5"   ,[],"Dwarves"   ,[(assign,"$faction_good",fac_dwarf   ),(jump_to_menu,"mnu_custom_battle_choose_faction3"),]),
     ("cb_gondor6"   ,[],"Dale"      ,[(assign,"$faction_good",fac_dale    ),(jump_to_menu,"mnu_custom_battle_choose_faction3"),]),
     ("cb_gondor7"   ,[],"Beornings" ,[(assign,"$faction_good",fac_beorn   ),(jump_to_menu,"mnu_custom_battle_choose_faction3"),]),
 ] for ct in range(cheat_switch)])+[
     ("go_back"      ,[],"Go back"   ,[(jump_to_menu,"mnu_custom_battle_choose_faction1")]),
 ]),
( "custom_battle_choose_faction3",0,
    "^^^^^^^^^^Choose evil faction", "none", [(set_background_mesh, "mesh_relief01")],
    [
 ]+concatenate_scripts([[	
	("cb_mordor"    ,[],"Mordor"     ,[(assign,"$faction_evil",fac_mordor  ),(jump_to_menu,"mnu_custom_battle_2"),]),
     ("cb_mordor1"   ,[],"Isengard"   ,[(assign,"$faction_evil",fac_isengard),(jump_to_menu,"mnu_custom_battle_2"),]),
     ("cb_mordor2"   ,[],"Dunland"    ,[(assign,"$faction_evil",fac_dunland ),(jump_to_menu,"mnu_custom_battle_2"),]),
     ("cb_mordor3"   ,[],"Haradrim"   ,[(assign,"$faction_evil",fac_harad   ),(jump_to_menu,"mnu_custom_battle_2"),]),
     ("cb_mordor4"   ,[],"Easterlings",[(assign,"$faction_evil",fac_khand   ),(jump_to_menu,"mnu_custom_battle_2"),]),
     ("cb_mordor5"   ,[],"Moria"      ,[(assign,"$faction_evil",fac_moria   ),(jump_to_menu,"mnu_custom_battle_2"),]),
     ("cb_mordor6"   ,[],"Gundabad"   ,[(assign,"$faction_evil",fac_gundabad),(jump_to_menu,"mnu_custom_battle_2"),]),
     ("cb_mordor7"   ,[],"Rhun"       ,[(assign,"$faction_evil",fac_rhun    ),(jump_to_menu,"mnu_custom_battle_2"),]),
     ("cb_mordor8"   ,[],"Corsairs"   ,[(assign,"$faction_evil",fac_umbar   ),(jump_to_menu,"mnu_custom_battle_2"),]),
 ] for ct in range(cheat_switch)])+[
     ("go_back"      ,[],"Go back"    ,[(jump_to_menu,"mnu_custom_battle_choose_faction2")]),
	 ]
 ),

######################### TLD808 menus ##########################
( "ancient_ruins",0,
  "{s1}", "none", 
		[
			(set_background_mesh, "mesh_ui_default_menu_window"),
			(try_begin),
				(check_quest_succeeded, "qst_mirkwood_sorcerer"),
				(str_store_string, s1, "@Now that the sorcerer is dead, there is nothing left to be done here."),			
			(else_try),
				(check_quest_failed, "qst_mirkwood_sorcerer"),
				(str_store_string, s1, "@Now that the sorcerer has fled, there is nothing left to be done here."),
			(else_try),
				(str_store_string, s1, "@You approach a heavily guarded region of the forest..."),				
			(try_end),
		],
  [ ("rescue_mission",  [(neg|quest_slot_ge, "qst_mirkwood_sorcerer",slot_quest_current_state,2)],
  "Sneak into the sorcerer's lair under the night's cover.",
	[
	(try_begin),
		(neg|is_currently_night),
		(store_time_of_day, reg1),
		(assign, reg2, 24),
		(val_sub, reg2, reg1),
		(display_message, "@You wait for darkness to fall...", color_good_news),
		(rest_for_hours, reg2), #rest while not attackable
		(change_screen_map),
	(else_try),
		(set_party_battle_mode),
		(call_script, "script_initialize_general_rescue"),
		(call_script, "script_initialize_sorcerer_quest"),
		(assign, "$rescue_stage", 0),
		(assign, "$active_rescue", 5),
        	(quest_set_slot,"qst_mirkwood_sorcerer",slot_quest_current_state,3),
		(disable_party, "p_ancient_ruins"), # (CppCoder) Only one chance...
		(call_script, "script_set_meta_stealth"),
		(call_script, "script_crunch_stealth_results"),
		(call_script, "script_set_infiltration_player_record"),
		(try_begin),(ge, "$stealth_results", 3),(assign, "$rescue_stage", 0),(call_script, "script_infiltration_combat_1"),
		(display_message, "@You_are_quickly_discovered_by_the_enemy."),
		(display_message, "@Eliminate_them_before_the_alarm_spreads!"),
	 	(else_try),(eq, "$stealth_results", 2),(assign, "$rescue_stage", 1),(call_script, "script_infiltration_stealth_2"),
		(display_message, "@You_advance_stealthily_far_into_the_forest."),
		(display_message, "@Scout_this_area_alone_and_meet_your_men_beyond!"),
		(display_message, "@Be_stealthy_but_eliminate_any_threats_quickly!"),
	 	(else_try),(eq, "$stealth_results", 1),(assign, "$rescue_stage", 2),(call_script, "script_final_sorcerer_fight"),
		(display_message, "@You_have_evaded_the_patrols_and_crept_close_to_the_ruins!"),
		(display_message, "@You_have_found_the_sorcerer!"),
		(try_end),
		(assign, "$active_rescue", 5),
		(change_screen_mission),
	(try_end),
	]),
    ("next_rescue_scene", [(eq, 1, 0)], "_",  
						[
						 (try_begin),
							(neq, "$alarm_level", 0),
							(display_message, "@You cannot leave until the guards lose you!", color_bad_news),
						 (try_end),
						 (eq, "$alarm_level", 0),
						 (call_script, "script_store_hero_death"),
						 (call_script, "script_set_meta_stealth"),
						 (call_script, "script_crunch_stealth_results"),
						 (try_begin),
							(eq, "$rescue_stage", 0),
							(try_begin),
								(ge, "$stealth_results", 2),
								(assign, "$rescue_stage", 1),
								(call_script, "script_infiltration_stealth_2"),
								(display_message, "@Scout_this_area_alone_and_meet_your_men_beyond!"),
								(display_message, "@Be_stealthy_but_eliminate_any_threats_quickly!"),
							(else_try),
								(assign, "$rescue_stage", 2),
								(call_script, "script_final_sorcerer_fight"),
								(display_message, "@You_have_found_the_sorcerer!"),
								(display_message, "@Kill_him_quickly_before_he_escapes!"),
							(try_end),
						(else_try),
							(eq, "$rescue_stage", 1),
							(assign, "$rescue_stage", 2),
							(call_script, "script_final_sorcerer_fight"),
							(display_message, "@You_have_found_the_sorcerer!"),
							(display_message, "@Kill_him_quickly_before_he_escapes!"),
						(try_end)],"Continue_onward!"),
		("pick_troops1", [(neg|quest_slot_ge, "qst_mirkwood_sorcerer",slot_quest_current_state,2)], "Pick companions for the mission, {reg0} selected",
							[(party_get_num_companion_stacks, ":num_stacks","p_main_party"),
							(try_for_range, ":slot", 0, 40),
								(troop_set_slot,"trp_temp_array_a",":slot",0), # clear eligible troops array
							(try_end),
							(assign,":slot",1),
							(try_for_range, ":stack_no", 0, ":num_stacks"), # store troops eligible for stealth mission
							  (party_stack_get_troop_id,":stack_troop","p_main_party",":stack_no"),
							  (neq, ":stack_troop", "trp_player"),
							  (store_skill_level, reg1, skl_pathfinding, ":stack_troop"), # only troops with pathfinding or heroes can go on stealth missions
							  (this_or_next|gt, reg1, 0),
							  (troop_is_hero, ":stack_troop"),
								(troop_set_slot,"trp_temp_array_a",":slot",":stack_troop"),
								(val_add,":slot",1),
							(try_end),
							(assign,reg1,0),(assign,reg2,0),(assign,reg3,0),(assign,reg4,0),(assign,reg5,0),(assign,reg6,0),(assign,reg7,0),(assign,reg8,0),(assign,reg9,0),(assign,reg10,0),(assign,reg0,0),
							(jump_to_menu, "mnu_pick_troops")]),
		("leave", [], "Leave.",
							[(leave_encounter),
							(change_screen_return),
							(neg|eq, "$active_rescue", 0),
							(call_script, "script_infiltration_mission_final_casualty_tabulation")]),
	]
 ),
( "pick_troops", 0, 
  "Whom would you take with you into the stealth mission? \
   Currently you picked {reg0} companions. You can take up to 10 troops with you", "none",
   [(set_background_mesh, "mesh_ui_default_menu_window")], [ 
   #reg0 counts total # of companions picked
  ("troop1", [(troop_get_slot,":troop","trp_temp_array_a",1),(gt,":troop",0),(str_store_troop_name, s1, ":troop")],
   "{s1}: {reg1}", [(troop_get_slot,":troop","trp_temp_array_a",1),
                    (party_count_members_of_type, ":n", "p_main_party",":troop"),
					(try_begin),(lt,reg1,":n"),(lt,reg0,10),(val_add, reg1,1),(call_script, "script_set_hero_companion", ":troop"),
					(else_try),(val_sub,reg0,reg1),(assign,reg1,0),
					(try_end),(jump_to_menu, "mnu_pick_troops")]),  
  ("troop2", [(troop_get_slot,":troop","trp_temp_array_a",2),(gt,":troop",0),(str_store_troop_name, s2, ":troop")],
   "{s2}: {reg2}", [(troop_get_slot,":troop","trp_temp_array_a",2),
                    (party_count_members_of_type, ":n", "p_main_party",":troop"),
					(try_begin),(lt,reg2,":n"),(lt,reg0,10),(val_add, reg2,1),(call_script, "script_set_hero_companion", ":troop"),
					(else_try),(val_sub,reg0,reg2),(assign,reg2,0),
					(try_end),(jump_to_menu, "mnu_pick_troops")]),  
  ("troop3", [(troop_get_slot,":troop","trp_temp_array_a",3),(gt,":troop",0),(str_store_troop_name, s3, ":troop")],
   "{s3}: {reg3}", [(troop_get_slot,":troop","trp_temp_array_a",3),
                    (party_count_members_of_type, ":n", "p_main_party",":troop"),
					(try_begin),(lt,reg3,":n"),(lt,reg0,10),(val_add, reg3,1),(call_script, "script_set_hero_companion", ":troop"),
					(else_try),(val_sub,reg0,reg3),(assign,reg3,0),
					(try_end),(jump_to_menu, "mnu_pick_troops")]),  
  ("troop4", [(troop_get_slot,":troop","trp_temp_array_a",4),(gt,":troop",0),(str_store_troop_name, s4, ":troop")],
   "{s4}: {reg4}", [(troop_get_slot,":troop","trp_temp_array_a",4),
                    (party_count_members_of_type, ":n", "p_main_party",":troop"),
					(try_begin),(lt,reg4,":n"),(lt,reg0,10),(val_add, reg4,1),(call_script, "script_set_hero_companion", ":troop"),
					(else_try),(val_sub,reg0,reg4),(assign,reg4,0),
					(try_end),(jump_to_menu, "mnu_pick_troops")]),  
  ("troop5", [(troop_get_slot,":troop","trp_temp_array_a",5),(gt,":troop",0),(str_store_troop_name, s5, ":troop")],
   "{s5}: {reg5}", [(troop_get_slot,":troop","trp_temp_array_a",5),
                    (party_count_members_of_type, ":n", "p_main_party",":troop"),
					(try_begin),(lt,reg5,":n"),(lt,reg0,10),(val_add, reg5,1),(call_script, "script_set_hero_companion", ":troop"),
					(else_try),(val_sub,reg0,reg5),(assign,reg5,0),
					(try_end),(jump_to_menu, "mnu_pick_troops")]),  
  ("troop6", [(troop_get_slot,":troop","trp_temp_array_a",6),(gt,":troop",0),(str_store_troop_name, s6, ":troop")],
   "{s6}: {reg6}", [(troop_get_slot,":troop","trp_temp_array_a",6),
                    (party_count_members_of_type, ":n", "p_main_party",":troop"),
					(try_begin),(lt,reg6,":n"),(lt,reg0,10),(val_add, reg6,1),(call_script, "script_set_hero_companion", ":troop"),
					(else_try),(val_sub,reg0,reg6),(assign,reg6,0),
					(try_end),(jump_to_menu, "mnu_pick_troops")]),  
  ("troop7", [(troop_get_slot,":troop","trp_temp_array_a",7),(gt,":troop",0),(str_store_troop_name, s7, ":troop")],
   "{s7}: {reg7}", [(troop_get_slot,":troop","trp_temp_array_a",7),
                    (party_count_members_of_type, ":n", "p_main_party",":troop"),
					(try_begin),(lt,reg7,":n"),(lt,reg0,10),(val_add, reg7,1),(call_script, "script_set_hero_companion", ":troop"),
					(else_try),(val_sub,reg0,reg7),(assign,reg7,0),
					(try_end),(jump_to_menu, "mnu_pick_troops")]),  
  ("troop8", [(troop_get_slot,":troop","trp_temp_array_a",8),(gt,":troop",0),(str_store_troop_name, s8, ":troop")],
   "{s8}: {reg8}", [(troop_get_slot,":troop","trp_temp_array_a",8),
                    (party_count_members_of_type, ":n", "p_main_party",":troop"),
					(try_begin),(lt,reg8,":n"),(lt,reg0,10),(val_add, reg8,1),(call_script, "script_set_hero_companion", ":troop"),
					(else_try),(val_sub,reg0,reg8),(assign,reg8,0),
					(try_end),(jump_to_menu, "mnu_pick_troops")]),  
  ("troop9", [(troop_get_slot,":troop","trp_temp_array_a",9),(gt,":troop",0),(str_store_troop_name, s9, ":troop")],
   "{s9}: {reg9}", [(troop_get_slot,":troop","trp_temp_array_a",9),
                    (party_count_members_of_type, ":n", "p_main_party",":troop"),
					(try_begin),(lt,reg9,":n"),(lt,reg0,10),(val_add, reg9,1),(call_script, "script_set_hero_companion", ":troop"),
					(else_try),(val_sub,reg0,reg9),(assign,reg9,0),
					(try_end),(jump_to_menu, "mnu_pick_troops")]),  
  ("go_forward",   [], "End selecting companions and proceed.",  [#clear overflowing companions slots
					(store_add, ":empty", reg0, "fac_mission_companion_1"),
					(try_for_range, ":comp",":empty","fac_mission_companion_11"),
						(faction_set_slot, ":comp", slot_fcomp_troopid, 0),
						(faction_set_slot, ":comp", slot_fcomp_hp, 0),
					(try_end),
					(jump_to_menu, "mnu_ancient_ruins")]),  
 ]),  
( "burial_mound", 0, 
  "You_approach_the_burial_mound_of_{s1}_of_{s2}._\
  It_is_heaped_with_the_notched_weapons_of_his_fallen_enemies.", "none",
   [	(set_background_mesh, "mesh_ui_default_menu_window"),
		(store_encountered_party, ":mound"),
		(party_get_slot, ":hero", ":mound", slot_party_commander_party),
		(store_troop_faction, reg1,":hero"),
		(str_store_faction_name, s2, reg1),
		(str_store_troop_name, s1, ":hero")], [
  ("pay_respects", [(store_encountered_party, ":mound"),
					(party_get_slot, ":hero", ":mound", slot_party_commander_party),
					(store_troop_faction,":faction",":hero"),
					(store_relation, reg1, ":faction", "fac_player_faction"),
					(gt, reg1, 0),
					(party_get_slot, ":state", ":mound", slot_mound_state),
					(eq, ":state", 1)],
   "Kneel_and_pay_your_respects.", [(jump_to_menu, "mnu_burial_mound_respects")]),  
  ("swear_oath",   [(store_encountered_party, ":mound"),
					(party_get_slot, ":hero", ":mound", slot_party_commander_party),
					(store_troop_faction,":faction",":hero"),
					(store_relation, reg1, ":faction", "fac_player_faction"),
					(gt, reg1, 0),
					(party_get_slot, ":state", ":mound", slot_mound_state),
					(eq, ":state", 1),
					(check_quest_active|neg, "qst_oath_of_vengeance")],
   "Swear_an_oath_of_vengeance!",  [(jump_to_menu, "mnu_burial_mound_oath")]),  
  ("despoil",      [(store_encountered_party, ":mound"),
					(str_store_party_name, s1, ":mound"),
					(party_get_slot, ":hero", ":mound", slot_party_commander_party),
					(store_troop_faction,":faction",":hero"),
					(store_relation,reg1, ":faction", "fac_player_faction"),
					(neg|gt, reg1, 0)],
   "Desecrate_the_site",  [(jump_to_menu, "mnu_burial_mound_despoil")]),  
  ("leave_mound",        [], "Leave_the_mound.",  [(leave_encounter),(change_screen_return)]),
 ]),  
( "burial_mound_respects", 0, 
  "You kneel and pay your respects to {s1}, silently mouthing a prayer for a speedy journey to the afterlife.\
  There is nothing left to be done here.", "none",
					[(set_background_mesh, "mesh_ui_default_menu_window"),
					(store_encountered_party, ":mound"),
					(party_get_slot, ":hero", ":mound", slot_party_commander_party),
					(str_store_troop_name, s1, ":hero"),
					(party_set_slot, ":mound", slot_mound_state, 2),
					(store_random, ":rnd", 100),
					(try_begin),(is_between, ":rnd", 5, 15),
					(call_script, "script_cf_gain_trait_reverent"),
					 (else_try),		(neg|ge, ":rnd", 5),
					 (call_script, "script_cf_gain_trait_blessed"),
					(try_end)
					],[
  ("leave_mound",  [], "Leave_the_mound.",  [(leave_encounter),(change_screen_return)]),
 ]),  
( "burial_mound_oath", 0, 
  "You loudly swear an oath of vengeance for the death of {s4}. \
  You would relentlessly seek out the forces of {s3} and destroy them. \
  Your words carry far on the wind and who can say that they were not heard beyond the sea?", "none",
	[(set_background_mesh, "mesh_ui_default_menu_window"),
	(store_encountered_party, ":mound"),
	(party_get_slot, ":hero", ":mound", slot_party_commander_party),
	(str_store_troop_name, s4, ":hero"),
	(store_troop_faction, ":target", ":hero"),
	(quest_set_slot, "qst_oath_of_vengeance", 4, ":target"), # remember source ally faction
	(quest_set_slot, "qst_oath_of_vengeance", 5, ":hero"), # CppCoder: remember source hero
	
	(assign,":count",1000000),  # choose nearest enemy capital as target faction
	(assign,":target", 0),
	(try_for_range, ":fac", kingdoms_begin, kingdoms_end),
		(store_relation, ":dist", ":fac", "fac_player_faction"),
		(lt, ":dist", 0), #enemies only
		(faction_slot_eq,":fac",slot_faction_state, sfs_active), # enemy not dead yet
		(faction_get_slot, ":capital", ":fac", slot_faction_capital),
		(store_distance_to_party_from_party,":dist",":mound",":capital"),  # choose nearest enemy capital for vengeance
		(lt, ":dist", ":count"),
			(assign,":count",":dist"),
			(assign,":target", ":fac"),
	(try_end),
	
	(str_store_faction_name, s3, ":target"),
	(store_current_day, ":day"),
	(quest_set_slot, "qst_oath_of_vengeance", 1, ":day"),
	(quest_set_slot, "qst_oath_of_vengeance", 2, ":target"), # target faction
	(assign,":count", 0), # count and store initial killcount of target faction' parties
	(try_for_range, ":ptemplate", "pt_gondor_scouts", "pt_kingdom_hero_party"),
		(spawn_around_party,"p_main_party",":ptemplate"),
		(store_faction_of_party,":fac", reg0),
		(remove_party, reg0),
		(eq, ":fac", ":target"),
		(store_num_parties_destroyed_by_player, ":n", ":ptemplate"),
		(val_add,":count",":n"),
	(try_end),
	(quest_set_slot, "qst_oath_of_vengeance", 3, ":count"), # counter for destroyed parties of target faction at quest start
	(party_set_slot, ":mound", slot_mound_state, 3), # no more oaths from here
        (setup_quest_text, "qst_oath_of_vengeance"),
        (str_store_string, s2, "@Enraged by the death of {s4}, you have sworn an oath of vengeance upon the forces of {s3}. You must now destroy as many of the armies of {s3} as possible in the coming days. You are keenly aware that your followers have witnessed this oath and you do not wish to become known as an oathbreaker. An orgy of bloodletting must now begin!"),
	(call_script, "script_start_quest", "qst_oath_of_vengeance", "trp_player"),
	],[
    ("leave_mound", [], "Leave_the_mound.", [(leave_encounter),(change_screen_return)]),
 ]),
( "burial_mound_despoil", 0, 
  "You tear down the monument to {s1} with your own hands and defile the very stones with curses, fell chants and unspeakable acts.\
  Your followers fall back in fear of the dead but they seem to have renewed respect for your wickedness.", "none", 
	[(set_background_mesh, "mesh_draw_mound_desecrated"),
	(store_encountered_party, ":mound"),(party_get_slot, ":hero", ":mound", slot_party_commander_party),(str_store_troop_name, s1, ":hero"),
	 (store_random, ":rnd", 100),
	 (try_begin),(is_between, ":rnd", 5, 10),
	 (call_script, "script_cf_gain_trait_despoiler"),
	  (else_try),    (neg|ge, ":rnd", 5),    
	  (call_script, "script_cf_gain_trait_accursed"),
	 (try_end),
	 (party_set_slot, ":mound", slot_mound_state, 4),
	 (disable_party, ":mound")],[
 ("leave_mound", [], "Leave_the_mound.", [(leave_encounter),(change_screen_return)]),
 ]),
( "funeral_pyre", 0, 
  "You approach the charred remnants of the funeral pyre of {s3} of {s2}. \
  Here his corpse was ceremoniously burned by his personal bodyguards. \
  Nothing of value remains.", "none", 
   [(set_background_mesh, "mesh_draw_funeral_pyre"),
    (store_encountered_party, ":mound"),
	(party_get_slot, ":hero", ":mound", slot_party_commander_party),
	(str_store_troop_name, s3, ":hero"),
	(store_troop_faction,":faction",":hero"),
	(str_store_faction_name, s2, ":faction")],[
 ("swear_oath",   [(store_encountered_party, ":mound"),
					(party_get_slot, ":hero", ":mound", slot_party_commander_party),
					(store_troop_faction,":faction",":hero"),
					(store_relation, ":local2", ":faction", "fac_player_faction"),
					(gt, ":local2", 0),
					(party_get_slot, ":state", ":mound", slot_mound_state),
					(eq, ":state", 1),
					(check_quest_active|neg, "qst_oath_of_vengeance")],
   "Swear_an_oath_of_vengeance!",  [(jump_to_menu, "mnu_burial_mound_oath")]),  
 ("leave_pyre", [], "Leave_the_pyre.", [(leave_encounter),(change_screen_return)]), 
 ]),
( "town_ruins",mnf_enable_hot_keys|city_menu_color,
	"When you approach, you see that {s1} is {s2}",
    "none",
	code_to_set_city_background + [
	(try_begin),
		(eq, "$g_encountered_party", "p_town_isengard"),
		(str_store_string, s2, "@flooded. Somebody or something must have ruined the Isen dams."),
	(else_try),
		(str_store_string, s2, "@destroyed. Only smoldering ruins remain."),
	(try_end),
	(party_get_slot, ":elder_troop", "$g_encountered_party", slot_town_elder),
	(str_store_troop_name_plural, s1, ":elder_troop"), # elders store place referral, "trp_no_troop" stores "the_place"
    ],
    [("ruin_menu_0",[(eq, "$g_encountered_party", "p_town_isengard")],"Explore the place.",[
	    (modify_visitors_at_site,"scn_isengard_center_flooded"),
        (reset_visitors),
        (set_visitor, 1, "trp_player"),
        (jump_to_menu, "mnu_town_ruins"),
        (jump_to_scene,"scn_isengard_center_flooded"),
        (change_screen_mission),], "_"),
     ("ruin_leave",[],"Leave...",[(change_screen_return)]),
 ]),

("premutiny",0,"none","none", #dummy menu for showing orc pretender pre-mutiny dialog
   [(try_begin),
		(eq,"$mutiny_stage",0), # warning
		(call_script, "script_setup_troop_meeting", "trp_orc_pretender",100),
	(else_try),
		(change_screen_map),
	(try_end),
    ],[]
 ),
("mutiny",0,"{s1}","none",
   [(try_begin),
		(eq,"$mutiny_stage",5), # fight lost
		(str_store_string, s1, "@^^^You lost your fight against the mutiny! ^Seems like your orcs have a new commander now."),
		(party_get_num_companion_stacks, ":num_stacks","p_main_party"),
		(try_for_range, ":stack_no", 0, ":num_stacks"), # remove all orcs
			(party_stack_get_troop_id, ":stack_troop", "p_main_party" ,":stack_no"),
			(neg|troop_is_hero, ":stack_troop"),
			(troop_get_type, reg3, ":stack_troop"),
			(eq, reg3, tf_orc),
			(party_stack_get_size, reg3, "p_main_party",":stack_no"),
			(party_remove_members, "p_main_party", ":stack_troop", reg3),
		(try_end),
		(assign,"$mutiny_stage",0),
    (else_try),
		(eq,"$mutiny_stage",4), #fight won
		(str_store_string, s1, "@^^^You have slain the offender, and other orcs quickly fall back in line. ^ For some time the maggots will be quiet for sure."),
		(assign,"$mutiny_stage",0),
    (else_try),
		(eq,"$mutiny_stage",2), # pre-fight dialog begin
		(call_script, "script_setup_troop_meeting", "trp_orc_pretender",100),
	(else_try),
		(eq,"$mutiny_stage",3), # pre-fight dialog ended and fight on the way
		(modify_visitors_at_site, "scn_duel_scene"),
		(reset_visitors),
		(set_jump_entry, 0), 
		(set_visitor, 0, "trp_player"),
		(set_visitor, 1, "trp_orc_pretender"),
		(call_script, "script_party_copy", "p_encountered_party_backup", "p_main_party"),
		(party_remove_members, "p_encountered_party_backup", "trp_player", 1),
		(try_for_range, ":entry", 2, 29), # populate spectators
			(call_script, "script_cf_party_remove_random_regular_troop", "p_encountered_party_backup"), #returns reg0
			(store_random_in_range, reg1,1, 100000), #rnd dna
			(set_visitor,":entry",reg0, reg1),
		(try_end),
		(set_jump_mission, "mt_arena_challenge_fight"),
		(jump_to_scene, "scn_duel_scene"),
		(change_screen_mission),
	(try_end),
    ],[
    # ("start_fight",[(eq, "$party_meeting", 0), (eq, 1,0),],"Confront the mutinee!",[
		# (modify_visitors_at_site, "scn_duel_scene"),
		# (reset_visitors),
		# (set_jump_entry, 0), 
		# (set_visitor, 0, "trp_player"),
		# (set_visitor, 1, "trp_orc_pretender"),
		# (call_script, "script_party_copy", "p_encountered_party_backup", "p_main_party"),
		# (party_remove_members, "p_encountered_party_backup", "trp_player", 1),
		# (try_for_range, ":entry", 2, 29), # populate spectators
			# (call_script, "script_cf_party_remove_random_regular_troop", "p_encountered_party_backup"), #returns reg0
			# (store_random_in_range, reg1,1, 100000), #rnd dna
			# (set_visitor,":entry",reg0, reg1),
		# (try_end),
		# (set_jump_mission, "mt_arena_challenge_fight"),
		# (jump_to_scene, "scn_duel_scene"),
		# (change_screen_mission)]),
	("leave",[],"Leave.",[(change_screen_map)])]
 ),

# ("taunt",0,
 # "You taunted the defenders, shouting insults and parading a good distance away for some time. There was no reaction apart from several arrows which fell well short of your ranks. ^Looks like there is nothing to do here",
 # "none",
   # [],[("leave",[],"Back...",[(change_screen_return)])],
 # ),

# Death menu. Just a placeholder...
( "death", mnf_disable_all_keys,
    "You have been killed. Though the war still rages on, you will no longer be part of it.",
    "none",
    [(set_background_mesh, "mesh_ui_default_menu_window")],
	[("continue",[],"Continue...",[(change_screen_quit)])]
 ),

# Animal ambushes (CppCoder)
 ("animal_ambush", 0, 
 "You and your companions find yourselves separated from the rest of your party, when suddenly...",
 "none", 
 [
	(assign, ":ambush_troop", "trp_wolf"), # (CppCoder) Default, just in case something glitches...
	(assign, ":ambush_count", 1), 
	(try_begin),
		(eq|this_or_next, "$current_player_region", region_n_mirkwood),
		(eq, "$current_player_region", region_s_mirkwood),
		(assign, ":ambush_troop", "trp_spider"),
		(assign, ":ambush_scene", "scn_mirkwood_ambush"),
		(store_random_in_range, ":ambush_count", 1, 5), # 1 to 5 spiders...
	(else_try),
		(eq|this_or_next, "$current_player_region", region_grey_mountains),
		(eq, "$current_player_region", region_misty_mountains),
		(assign, ":ambush_scene", "scn_mountain_ambush"),
		(store_random, ":rnd", 100),
		(try_begin),
			(eq, "$players_kingdom", "fac_dunland"),
			(assign, ":ambush_troop", "trp_bear"),
			(assign, ":ambush_count", 1),			# 1 bear only
		(else_try),
			(neq, "$players_kingdom", "fac_beorn"), # If not a beorning there is a 40% chance of a bear ambush
			(lt, ":rnd", 40),
			(assign, ":ambush_troop", "trp_bear"),
			(assign, ":ambush_count", 1),
		(else_try),
			(assign, ":ambush_troop", "trp_wolf"),
			(store_random_in_range, ":ambush_count", 5, 9), # 5 to 8 wolves
		(try_end),
	(try_end),
	(assign, reg20, ":ambush_troop"),
	(assign, reg21, ":ambush_count"),
	(assign, reg22, ":ambush_scene"),
  
  #swy-- set the background mesh depending on what's going to attack us!
  (try_begin),
    (eq,":ambush_troop", "trp_spider"),
    (set_background_mesh, "mesh_draw_spiders"),
  (else_try),
    (eq,":ambush_troop", "trp_bear"),
    (set_background_mesh, "mesh_draw_bear"),
  (else_try),
    (eq,":ambush_troop", "trp_wolf"),
    (set_background_mesh, "mesh_draw_wolf"), #swy-- we don't have an illustration for wolves yet!
  (try_end)
 ],
 [
	("continue",[],"Continue...",
	[
	(set_jump_mission, "mt_animal_ambush"),
	(set_jump_entry, 0),
	(modify_visitors_at_site, reg22),
	(reset_visitors),

	(assign, ":cur_entry", 1),
	(try_for_range, ":npc", companions_begin, companions_end),
		(main_party_has_troop, ":npc"),
		(set_visitor, ":cur_entry", ":npc"),
		(val_add, ":cur_entry", 1),
	(try_end),

	(assign, ":cur_entry", 17),
	(try_for_range, ":unused", 0, reg21),
		(set_visitor, ":cur_entry", reg20),
		(val_add, ":cur_entry", 1),
	(try_end),

	(jump_to_scene, reg22),
	(change_screen_mission),
	]),
 ],
 ),

("animal_ambush_success", 0, "The {s2} {reg0?fall:falls} before you as wheat to a scythe! Soon all your attackers lie on the floor, wounded or dead. {s3}", "none", 
[
	(assign, reg5, -1), # Reward item id.
	(try_begin),
		(gt, reg21, 1),
		(assign, reg0, 1),
		(str_store_troop_name_plural, s2, reg20),
	(else_try),
		(assign, reg0, 0),
		(str_store_troop_name, s2, reg20),
	(try_end),
  
  (assign,":ambush_troop", reg20),
  
  #swy-- set the background mesh depending on what's going to attack us!
  (try_begin),
    (eq,":ambush_troop", "trp_spider"),
    (set_background_mesh, "mesh_draw_spiders"),
  (else_try),
    (eq,":ambush_troop", "trp_bear"),
    (set_background_mesh, "mesh_draw_bear"),
  (else_try),
    (eq,":ambush_troop", "trp_wolf"),
    (set_background_mesh, "mesh_draw_wolf"), #swy-- we don't have an illustration for wolves yet!
  (try_end),
  
	(str_store_string, s3, "@You cover up your tracks and move onward."), 
],
[
	("continue",[],"Continue...",[
		(store_mul, ":exp", 100, reg21),
		(add_xp_as_reward, ":exp"),
		(try_begin),
			(gt, reg5, -1),
			(troop_add_item, "trp_player",reg5),
		(try_end),
		(change_screen_map)]),
	("repeat",[(eq, cheat_switch, 1)],"DEBUG: Repeat...",[(jump_to_menu, "mnu_animal_ambush"),]),
]),

("animal_ambush_fail", 0, "The animals bite and tear at you{reg0?,: and your companion{reg2?s,:,}} but luckily you managed to fend them off. Hopefully they won't attack you again.", "none", 
[
  (assign,":ambush_troop", reg20),

  #swy-- set the background mesh depending on what's going to attack us!
  (try_begin),
    (eq,":ambush_troop", "trp_spider"),
    (set_background_mesh, "mesh_draw_spiders"),
  (else_try),
    (eq,":ambush_troop", "trp_bear"),
    (set_background_mesh, "mesh_draw_bear"),
  (else_try),
    (eq,":ambush_troop", "trp_wolf"),
    (set_background_mesh, "mesh_draw_wolf"), #swy-- we don't have an illustration for wolves yet!
  (try_end),

	(assign, reg0, 1),
	(assign, reg1, 0),
	(assign, reg2, 0),
	(try_for_range, ":npc", companions_begin, companions_end),
		(main_party_has_troop, ":npc"),
		(assign, reg0, 0),
		(val_add, reg1, 1),
	(try_end),
	(try_begin),
		(gt, reg1, 1),
		(assign, reg2, 1),
	(try_end),
],
[
	("continue",[],"Continue...",[(change_screen_map)]),
	("repeat",[(eq, cheat_switch, 1)],"DEBUG: Repeat...",[(jump_to_menu, "mnu_animal_ambush"),]),
]),

("build_your_scene",0,
 "You can build your own battlescene here, using one of the slots provided below and game Edit mode \
 (you need to switch edit mode ON in M&B lauching screen Options first). \
 You can then submit scenes you constructed (namely, sco files from TLD/SceneObj folder) \
 to the dev team of TLD, and if your scene is good, \
 it can appear in later releases as one of random battlegrounds!^^\
 Try to specify which region on map you want your scene to appear.^\
 Couple hints: avoid deep water, steep mountains and other impassable places, \
 unless you are experienced scene-maker and know how to bar AI troops \
 from walking where you don't want them, and make AI mesh in other places.^\
 (Entries #0-1 are for attackers, #4 for defenders, do not touch #5-8",
 "none",
   [(set_background_mesh, "mesh_ui_default_menu_window")],[
   ("scene1",[],"Battlefield5 (file scn_battlefield5.sco)",[(1261,"scn_battlefield5"),(1262,0),(1263,0,0),(1911,"mt_scene_chooser"),(1910, "scn_battlefield5"),(2048)]),
   ("scene2",[],"Battlefield6 (file scn_battlefield6.sco)",[(1261,"scn_battlefield6"),(1262,0),(1263,0,0),(1911,"mt_scene_chooser"),(1910, "scn_battlefield6"),(2048)]),
   ("scene3",[],"Battlefield7 (file scn_battlefield7.sco)",[(1261,"scn_battlefield7"),(1262,0),(1263,0,0),(1911,"mt_scene_chooser"),(1910, "scn_battlefield7"),(2048)]),
   ("scene4",[],"Battlefield8 (file scn_battlefield8.sco)",[(1261,"scn_battlefield8"),(1262,0),(1263,0,0),(1911,"mt_scene_chooser"),(1910, "scn_battlefield8"),(2048)]),
   ("scene5",[],"Battlefield9 (file scn_battlefield9.sco)",[(1261,"scn_battlefield9"),(1262,0),(1263,0,0),(1911,"mt_scene_chooser"),(1910, "scn_battlefield9"),(2048)]),
   ("back_3dot" ,[],"Back...",[(change_screen_quit)])],
 ),

# ("start_game_0",menu_text_color(0xFF000000)|mnf_disable_all_keys,
    # "Welcome, adventurer, to TLD. Let the TLD for Warband experience start nao!",
    # "none", [],
    # [ ("continue",[],"Continue...",[(jump_to_menu, "mnu_start_game_1")]),
      # ("go_back",[],"Go back",[(change_screen_quit)])]
# ),
] 

## quick scene chooser
import header_scenes
from template_tools import *
from module_scenes import scenes

sorted_scenes = sorted(scenes)
for i in xrange(len(sorted_scenes)):
  current_scene = list(sorted_scenes[i])
  current_scene[1] = get_flags_from_bitmap(header_scenes, "sf_", current_scene[1])
  sorted_scenes[i] = tuple(current_scene)

choose_scene_template = Game_Menu_Template(
  id="choose_scenes_",
  text="Choose a scene: (Page {current_page} of {num_pages})",
  optn_id="choose_scene_",
  optn_text="{list_item[0]}{list_item[1]}",
  optn_consq = [
    (modify_visitors_at_site,"scn_{list_item[0]}"),
	(reset_visitors,0),
    (set_visitor,0,"trp_player"),    
	(set_jump_mission,"mt_scene_chooser"),
	(jump_to_scene, "scn_{list_item[0]}"),
    (change_screen_mission)
  ]
)

if cheat_switch: 
  game_menus += choose_scene_template.generate_menus(sorted_scenes)