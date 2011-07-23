from header_common import *
from header_operations import *
from header_mission_templates import *
from header_animations import *
from header_sounds import *
from header_music import *
from module_constants import *
from module_mission_templates_TLD import *
from module_mission_templates_unneeded import *
from module_mission_templates_cutscenes import *

####################################################################################################################
#   Each mission-template is a tuple that contains the following fields:
#  1) Mission-template id (string): used for referencing mission-templates in other files.
#     The prefix mt_ is automatically added before each mission-template id
#
#  2) Mission-template flags (int): See header_mission-templates.py for a list of available flags
#  3) Mission-type(int): Which mission types this mission template matches.
#     For mission-types to be used with the default party-meeting system,
#     this should be 'charge' or 'charge_with_ally' otherwise must be -1.
#     
#  4) Mission description text (string).
#  5) List of spawn records (list): Each spawn record is a tuple that contains the following fields:
#    5.1) entry-no: Troops spawned from this spawn record will use this entry
#    5.2) spawn flags. 
#    5.3) alter flags. which equipment will be overriden
#    5.4) ai flags.
#    5.5) Number of troops to spawn.
#    5.6) list of equipment to add to troops spawned from here (maximum 8).
#  6) List of triggers (list).
#     See module_triggers.py for infomation about triggers.
#
#  Please note that mission templates is work in progress and can be changed in the future versions.
# 
####################################################################################################################

pilgrim_disguise = [itm_blackroot_hood,itm_pilgrim_disguise,itm_practice_staff]
af_castle_lord = af_override_horse | af_override_weapons| af_require_civilian
af_castle_warlord = af_override_horse | af_override_weapons | af_override_head | af_override_gloves

# dynamic fog in dungeons, governed by player triggering scene props (mtarini and GA)
dungeon_darkness_effect = (1, 0, 0, [(eq,"$dungeons_in_scene",1)], [ 
	(get_player_agent_no,":player"), 
    (agent_get_position,pos25,":player"),
 	(assign,":min_dist",200), # cycle through fog triggers, find closest one
	(assign,":min_pointer",-1),
    (try_for_range,":pointer","spr_light_fog_black0","spr_moria_rock"),
		(scene_prop_get_num_instances,":max_instance", ":pointer"),
		(ge,":max_instance", 1),
		(try_for_range,":instance_no",0,":max_instance"), # checking distance to player
			(scene_prop_get_instance, ":i", ":pointer", ":instance_no"),
			(ge, ":i", 0),
            (prop_instance_get_position,pos1,":i"),
            (get_distance_between_positions,":dist",pos1,pos25),
	        (le,":dist",":min_dist"),
			(assign, ":min_dist", ":dist"), 
			(assign, ":min_pointer", ":pointer"), 
        (try_end),
    (try_end),
	(try_begin), # setting fog thickness
		(neq,":min_pointer",-1),
		(try_begin),(eq,":min_pointer","spr_light_fog_black0"),(assign,reg11,10000), # 10000
		 (else_try),(eq,":min_pointer","spr_light_fog_black1"),(assign,reg11,120),# was 500
		 (else_try),(eq,":min_pointer","spr_light_fog_black2"),(assign,reg11,80), # was 200
		 (else_try),(eq,":min_pointer","spr_light_fog_black3"),(assign,reg11,40),  # was 120
		 (else_try),(eq,":min_pointer","spr_light_fog_black4"),(assign,reg11,20), # was 80
		 (else_try),(eq,":min_pointer","spr_light_fog_black5"),(assign,reg11,14), # was 20
		(try_end),
		(set_fog_distance,reg11,0x000001), 
		#(display_message, "@DEBUG: Fog distance: {reg11}"), 	
		(try_begin),(eq, reg11, 10000),(assign, "$player_is_inside_dungeon",0),
		 (else_try),				   (assign, "$player_is_inside_dungeon",1),
		(try_end),
	(try_end),
 ])
  
common_battle_mission_start = (ti_before_mission_start, 0, 0, [],
  [ (team_set_relation, 0, 2, 1),
    (team_set_relation, 1, 3, 1),
    (call_script, "script_change_banners_and_chest"),
    ])

common_battle_tab_press = (ti_tab_pressed, 0, 0, [],
  [ (try_begin),
      (eq, "$battle_won", 1),
      (call_script, "script_count_mission_casualties_from_agents"),
      (finish_mission,0),
    (else_try), #MV added this section
       (main_hero_fallen),
       (assign, "$pin_player_fallen", 1),
       (str_store_string, s5, "str_retreat"),
       (call_script, "script_simulate_retreat", 10, 20),
       (assign, "$g_battle_result", -1),
       (set_mission_result,-1),
       (call_script, "script_count_mission_casualties_from_agents"),
       (finish_mission,0),
    (else_try),
      (call_script, "script_cf_check_enemies_nearby"),
      (question_box,"str_do_you_want_to_retreat"),
    (else_try),
      (display_message,"str_can_not_retreat"),
    (try_end),
    ])

common_arena_fight_tab_press = (ti_tab_pressed, 0, 0, [],[(question_box,"str_give_up_fight")])

common_custom_battle_tab_press = (ti_tab_pressed, 0, 0, [],
  [ (try_begin),
      (neq, "$g_battle_result", 0),
      (call_script, "script_custom_battle_end"),
      (finish_mission),
    (else_try),
      (question_box,"str_give_up_fight"),
    (try_end),
    ])

custom_battle_check_victory_condition = (1, 60, ti_once,
  [ (store_mission_timer_a,reg1),
    (ge,reg1,10),
    (all_enemies_defeated, 2),
    (neg|main_hero_fallen, 0),
    (set_mission_result,1),
    (display_message,"str_msg_battle_won"),
    (assign, "$battle_won",1),
    (assign, "$g_battle_result", 1),
    ],
  [ (call_script, "script_custom_battle_end"),
    (finish_mission, 1),
    ])

custom_battle_check_defeat_condition = (1, 4, ti_once,
  [ (main_hero_fallen),
    (assign,"$g_battle_result",-1),
    ],
  [ (call_script, "script_custom_battle_end"),
    (finish_mission),
    ])

common_battle_victory_display = (10, 0, 0, [],[ (eq,"$battle_won",1),(display_message,"str_msg_battle_won")])

common_custom_battle_question_answered = (ti_question_answered, 0, 0, [],
   [ (store_trigger_param_1,":answer"),
     (eq,":answer",0),
     (assign, "$g_battle_result", -1),
     (call_script, "script_custom_battle_end"),
     (finish_mission),
   ])

common_music_situation_update = (30, 0, 0, [],[(call_script, "script_combat_music_set_situation_with_culture")])
common_battle_check_friendly_kills = (2, 0, 0, [],[ (call_script, "script_check_friendly_kills")])

common_battle_check_victory_condition = (1, 60, ti_once,
  [ (store_mission_timer_a,reg(1)),
    (ge,reg(1),10),
    (all_enemies_defeated, 5),
    #(neg|main_hero_fallen, 0), #MV
    (set_mission_result,1),
    (display_message,"str_msg_battle_won"),
    (assign,"$battle_won",1),
    (assign, "$g_battle_result", 1),
    (call_script, "script_play_victorious_sound"),
    ],
  [ (call_script, "script_count_mission_casualties_from_agents"),
    (finish_mission, 1),
    ])

common_battle_victory_display = (10, 0, 0, [],[ (eq,"$battle_won",1),(display_message,"str_msg_battle_won")])
common_battle_order_panel = (0, 0, 0, [],[(game_key_clicked, gk_view_orders),(start_presentation, "prsnt_battle")])
common_battle_order_panel_tick = (0.1, 0, 0, [], [ (eq, "$g_presentation_battle_active", 1),(call_script, "script_update_order_panel_statistics_and_map")])
common_battle_inventory = (ti_inventory_key_pressed, 0, 0, [],[(display_message,"str_use_baggage_for_inventory")])
common_inventory_not_available = (ti_inventory_key_pressed, 0, 0,[(display_message, "str_cant_use_inventory_now")],[])

common_battle_on_player_down =  (1, 4, ti_once, [(main_hero_fallen)],  [   # MV and MT
    (assign, "$pin_player_fallen", 1),
	#  check that battle still goes on MT
  	(store_normalized_team_count,":a", 0), 
	(store_normalized_team_count,":b", 1),
	(gt,":b",0),(gt,":a",0),
    (display_message, "str_player_down"), #MV
	
    #MV: not sure about this one, will see if it's needed
	# (set_show_messages, 0), #stop messages JL
	# (team_give_order, "$fplayer_team_no", grc_everyone, mordr_charge), #charges everyone JL
	# (try_begin),
	# (eq, "$tld_option_formations", 1), #if Formations is turned on JL
	# (team_set_order_listener, "$fplayer_team_no", grc_everyone,-1), #clear listener for everyone JL
	# (call_script, "script_player_order_formations", mordr_charge), #send formations order to charge JL
	# (try_end),
	# (team_give_order, "$fplayer_team_no", grc_everyone, mordr_fire_at_will), #JL PoP 3.3
	# (team_give_order, "$fplayer_team_no", grc_everyone, mordr_use_any_weapon), #JL PoP 3.3
	# (set_show_messages, 1), #show messages again JL
	# (display_message, "@Your troops are charging!"), # display message JL
              
    #Native calc retreat on player death
    # (str_store_string, s5, "str_retreat"),
    # (call_script, "script_simulate_retreat", 10, 20),
    # (assign, "$g_battle_result", -1),
    # (set_mission_result,-1),
    # (call_script, "script_count_mission_casualties_from_agents"),
    # (finish_mission,0)
])


## MadVader deathcam begin: this is a simple death camera from kt0, works by moving the player body so mouselook is automatic
common_init_deathcam = (0, 0, ti_once, [], [(assign, "$tld_camera_on", 0)])

common_start_deathcam = (
   0, 4, ti_once, # 4 seconds delay before the camera activates
   [ (main_hero_fallen),
     (eq, "$tld_camera_on", 0),
   ],
   [ (assign, "$tld_camera_on", 1),
   ]
)

common_move_forward_deathcam = (
   0, 0, 0,
   [  (eq, "$tld_camera_on", 1),
      (this_or_next|game_key_clicked, gk_move_forward),
      (game_key_is_down, gk_move_forward),
   ],
   [  (get_player_agent_no, ":player_agent"),
      (agent_get_look_position, pos1, ":player_agent"),
      (position_move_y, pos1, 18),
      (agent_set_position, ":player_agent", pos1),
   ]
)

common_move_backward_deathcam = (
   0, 0, 0,
   [  (eq, "$tld_camera_on", 1),
      (this_or_next|game_key_clicked, gk_move_backward),
      (game_key_is_down, gk_move_backward),
   ],
   [  (get_player_agent_no, ":player_agent"),
      (agent_get_look_position, pos1, ":player_agent"),
      (position_move_y, pos1, -18),
      (agent_set_position, ":player_agent", pos1),
   ]
)

common_move_left_deathcam = (
   0, 0, 0,
   [  (eq, "$tld_camera_on", 1),
      (this_or_next|game_key_clicked, gk_move_left),
      (game_key_is_down, gk_move_left),
   ],
   [  (get_player_agent_no, ":player_agent"),
      (agent_get_look_position, pos1, ":player_agent"),
      (position_move_x, pos1, -13),
      (agent_set_position, ":player_agent", pos1),
   ]
)


common_move_right_deathcam = (
   0, 0, 0,
   [  (eq, "$tld_camera_on", 1),
      (this_or_next|game_key_clicked, gk_move_right),
      (game_key_is_down, gk_move_right),
   ],
   [  (get_player_agent_no, ":player_agent"),
      (agent_get_look_position, pos1, ":player_agent"),
      (position_move_x, pos1, 13),
      (agent_set_position, ":player_agent", pos1),
   ]
)

common_deathcam_triggers = [
 	common_init_deathcam,
	common_start_deathcam,
	common_move_forward_deathcam,
	common_move_backward_deathcam,
	common_move_left_deathcam,
	common_move_right_deathcam,
]
## MadVader deathcam end

#AI triggers v3 by motomataru
AI_triggers = [  
	(ti_before_mission_start, 0, 0, [(eq, "$tld_option_formations", 1)], [
		(assign, "$cur_casualties", 0),
		(assign, "$prev_casualties", 0),
		(assign, "$prev_casualties2", 0), #adeed by JL to use for checking every second
		(assign, "$ranged_clock", 1),
		(assign, "$battle_phase", BP_Setup),
		(assign, "$clock_reset", 0),
		(assign, "$charge_activated", 0), # added for cav charge control -JL
		(assign, "$charge_ongoing",0), # added for cav charge control -JL
		(assign, "$inf_charge_activated", 0), # added for inf charge control -JL
		(assign, "$inf_charge_ongoing", 0), # added for inf charge control -JL
		(assign, "$arc_charge_activated", 0), # added for archer charge control -JL
		(assign, "$att_reinforcements_arrived",0), #added for seeing if reinforcements have arrived -JL
		(assign, "$def_reinforcements_arrived",0), #added for seeing if reinforcements have arrived -JL
		(assign, "$att_reinforcements_needed", 0), #added for seeing if reinforcements are needed -JL
		(assign, "$def_reinforcements_needed", 0), #added for seeing if reinforcements are needed -JL
		(assign, "$formai_disengage", 0), #added for controlling cavalry disengagement -JL
		(assign, "$formai_patrol_mode", 0), #added for controlling patrol mode -JL
	##JL code for assigning random local variables:
		(store_random_in_range, "$formai_rand0", -1000, AI_Self_Defence_Distance), #JL close retreat/advance/position range randomness
		(store_random_in_range, "$formai_rand2", 800, 1501), # JL positive only close range randomness
		(store_random_in_range, "$formai_rand1", 0, 501), #JL close hold position to archers for cavalry
		(store_random_in_range, "$formai_rand3", AI_charge_distance, 3001), # JL main charge distance randomness
		(store_random_in_range, "$formai_rand4", AI_Self_Defence_Distance, 3001), #JL alternative charge range randomness
		(store_random_in_range, "$formai_rand5", -1000, 0), #JL retreat range randomness
		(store_random_in_range, "$formai_rand6", 4000, 5001), #JL grand charge distance and firing distance range randomness
		(store_random_in_range, "$formai_rand7", 55, 66), #JL random decision comparative number (that partly decides when AI strives to execute a grand charge). A value of 30 = Patrol Mode. A value of 35 = enemy has >40% archers/others
		(store_random_in_range, "$formai_rand8", -100, 101), #JL random very short range positioning for inf around archers in x pos.			
		(assign, "$team0_default_formation", formation_default),
		(assign, "$team1_default_formation", formation_default),
		(assign, "$team2_default_formation", formation_default),
		(assign, "$team3_default_formation", formation_default),
		(init_position, Team0_Cavalry_Destination),
		(init_position, Team1_Cavalry_Destination),
		(init_position, Team2_Cavalry_Destination),
		(init_position, Team3_Cavalry_Destination),
		(assign, "$team0_reinforcement_stage", 0),
		(assign, "$team1_reinforcement_stage", 0),
	]),

	(0, AI_Delay_For_Spawn, ti_once, [(eq, "$tld_option_formations", 1)], [
		(set_fixed_point_multiplier, 100),
		(call_script, "script_battlegroup_get_position", Team0_Starting_Point, 0, grc_everyone),
		(call_script, "script_battlegroup_get_position", Team1_Starting_Point, 1, grc_everyone),
		(call_script, "script_battlegroup_get_position", Team2_Starting_Point, 2, grc_everyone),
		(call_script, "script_battlegroup_get_position", Team3_Starting_Point, 3, grc_everyone),
		(call_script, "script_field_tactics", 1)
	]),
    
	#JL new trigger for assigning randoms:
	(60, 0, 0, [(eq, "$tld_option_formations", 1)], [
	##JL code for assigning random local variables:
		(store_random_in_range, "$formai_rand0", -1000, AI_Self_Defence_Distance), #JL close retreat/advance/position range randomness
		(store_random_in_range, "$formai_rand2", 800, 1501), # JL positive only close range randomness
		(store_random_in_range, "$formai_rand1", -1000, AI_Self_Defence_Distance), #JL close retreat/advance/position range 2
		(store_random_in_range, "$formai_rand3", AI_charge_distance, 3001), # JL main charge distance randomness
		(store_random_in_range, "$formai_rand4", AI_Self_Defence_Distance, 3001), #JL alternative charge range randomness
		(store_random_in_range, "$formai_rand5", -1000, 0), #JL retreat range randomness
		(store_random_in_range, "$formai_rand6", 4000, 5001), #JL grand charge distance and firing distance range randomness
		(store_random_in_range, "$formai_rand7", 55, 66), #JL random decision comparative number (that partly decides when AI strives to execute a grand charge).
		(store_random_in_range, "$formai_rand8", -100, 101), #JL random very short range positioning for inf around archers in x pos.	
		#(display_message, "@Randoms  have been updated"),
	]), #End JL

	(1, .5, 0, [(eq, "$tld_option_formations", 1)], [	#delay to offset half a second from formations trigger
		(try_begin),
			(assign, "$prev_casualties2", "$cur_casualties"), #added by JL
			(call_script, "script_cf_count_casualties"),
			(assign, "$cur_casualties", reg0),
			(assign, "$battle_phase", BP_Fight),
		(try_end),
		
		(set_fixed_point_multiplier, 100),
		(call_script, "script_store_battlegroup_data"),
		(try_begin),	#reassess ranged position when fighting starts
			(eq, "$battle_phase", BP_Fight), #changed from ge to eq -JL
			(eq, "$clock_reset", 0),
			(call_script, "script_field_tactics", 1),
			(assign, "$ranged_clock", 0),
			(assign, "$clock_reset", 1),
		(else_try),	#reassess ranged position every five seconds after setup
			(ge, "$battle_phase", BP_Jockey),
			(store_mod, reg0, "$ranged_clock", 5),		
			(eq, reg0, 0),
			(call_script, "script_field_tactics", 1),
			(assign, "$team0_reinforcement_stage", "$defender_reinforcement_stage"),
			(assign, "$team1_reinforcement_stage", "$attacker_reinforcement_stage"),
		(else_try),
			(call_script, "script_field_tactics", 0),
		(try_end),

		(try_begin),
			(eq, "$battle_phase", BP_Setup),
			(assign, ":not_in_setup_position", 0),
			(try_for_range, ":bgteam", 0, 4),
				(neq, ":bgteam", "$fplayer_team_no"),
				(call_script, "script_battlegroup_get_size", ":bgteam", grc_everyone),
				(gt, reg0, 0),
				(call_script, "script_battlegroup_get_position", pos1, ":bgteam", grc_archers),
				(team_get_order_position, pos0, ":bgteam", grc_archers),
				(get_distance_between_positions, reg0, pos0, pos1),
				(gt, reg0, 500),
				(assign, ":not_in_setup_position", 1),
			(try_end),
			(eq, ":not_in_setup_position", 0),	#all AI reached setup position?
			(assign, "$battle_phase", BP_Jockey),
		(try_end),
		
		(val_add, "$ranged_clock", 1),
	]),
]

# Formations triggers v3 by motomataru
# Global variables	*_formation_type holds type of formation: see "Formation modes" in module_constants
#					*_formation_move_order hold the current move order for the formation
#					*_space hold the multiplier of extra space ordered into formation by the player

formations_triggers = [
	(ti_before_mission_start, 0, 0, [(eq, "$tld_option_formations", 1)], [
		(assign, "$autorotate_at_player", formation_autorotate_at_player),
		(assign, "$infantry_formation_type", formation_default),	#type set by first call; depends on faction
		(assign, "$archer_formation_type", formation_default),
		(assign, "$cavalry_formation_type", formation_wedge),
		(assign, "$infantry_space", formation_start_spread_out),	#give a little extra space for ease of forming up
		(assign, "$archer_space", formation_start_spread_out),
		(assign, "$cavalry_space", 0),
		(assign, "$fclock", 1)
	]),
    
#JL: Simple start player troops in formations, when formations is disabled	
	(0, 1, ti_once, [(eq, "$tld_option_formations", 0)], [
		#(display_message, "@Forming up to meet the enemy at your command ..."),
		(get_player_agent_no, "$fplayer_agent_no"),
		(agent_get_team, "$fplayer_team_no", "$fplayer_agent_no"),
		(agent_get_position, pos1, "$fplayer_agent_no"),
		(set_show_messages, 0),
		(team_give_order, "$fplayer_team_no", grc_everyone, mordr_hold),
		(position_move_x, pos1, 1500),		#cavalry set up 15m RIGHT of leader
		(position_move_y, pos1, 500),		#cavalry set up 5m IN FRONT of leader
		(team_set_order_position, "$fplayer_team_no", grc_cavalry, pos1),
		(agent_get_position, pos1, "$fplayer_agent_no"),
		(position_move_x, pos1, -1500),		#infantry set up 15m LEFT of leader
		(position_move_y, pos1, 500),
		(team_set_order_position, "$fplayer_team_no", grc_infantry, pos1),
		(agent_get_position, pos1, "$fplayer_agent_no"),
		(position_move_y, pos1, 2000),		#archers set up 20m FRONT of leader
		(team_set_order_position, "$fplayer_team_no", grc_archers, pos1),
		(set_show_messages, 1),
	]),	 #End of standard start formations

# Start troops in formation
	(0, formation_delay_for_spawn, ti_once, [(eq, "$tld_option_formations", 1)], [
		(get_player_agent_no, "$fplayer_agent_no"),
		(agent_get_team, "$fplayer_team_no", "$fplayer_agent_no"),
		(call_script, "script_store_battlegroup_data"),
		
		#get team fixed data
		(assign, ":team0_avg_faction", 0),
		(assign, ":team1_avg_faction", 0),
		(assign, ":team2_avg_faction", 0),
		(assign, ":team3_avg_faction", 0),
		(try_for_agents, ":cur_agent"),
			(agent_is_human, ":cur_agent"),
			(agent_get_team, ":cur_team", ":cur_agent"),
			(agent_get_troop_id, ":cur_troop", ":cur_agent"),
			(store_troop_faction, ":cur_faction", ":cur_troop"),
			(try_begin),
				(eq, ":cur_team", 0),
				(val_add, ":team0_avg_faction", ":cur_faction"),
			(else_try),
				(eq, ":cur_team", 1),
				(val_add, ":team1_avg_faction", ":cur_faction"),
			(else_try),
				(eq, ":cur_team", 2),
				(val_add, ":team2_avg_faction", ":cur_faction"),
			(else_try),
				(eq, ":cur_team", 3),
				(val_add, ":team3_avg_faction", ":cur_faction"),
			(try_end),
		(try_end),
		(try_begin),
			(gt, "$team0_size", 0),
			(team_get_leader, ":fleader", 0),
			(try_begin),
				(ge, ":fleader", 0),
				(agent_get_troop_id, ":fleader_troop", ":fleader"),
				(store_troop_faction, "$team0_faction", ":fleader_troop"),
			(else_try),
				(store_mul, "$team0_faction", ":team0_avg_faction", 10),
				(val_div, "$team0_faction", "$team0_size"),
				(val_add, "$team0_faction", 5),
				(val_div, "$team0_faction", 10),
			(try_end),
		(try_end),
		(try_begin),
			(gt, "$team1_size", 0),
			(team_get_leader, ":fleader", 1),
			(try_begin),
				(ge, ":fleader", 0),
				(agent_get_troop_id, ":fleader_troop", ":fleader"),
				(store_troop_faction, "$team1_faction", ":fleader_troop"),
			(else_try),
				(store_mul, "$team1_faction", ":team1_avg_faction", 10),
				(val_div, "$team1_faction", "$team1_size"),
				(val_add, "$team1_faction", 5),
				(val_div, "$team1_faction", 10),
			(try_end),
		(try_end),
		(try_begin),
			(gt, "$team2_size", 0),
			(team_get_leader, ":fleader", 2),
			(try_begin),
				(ge, ":fleader", 0),
				(agent_get_troop_id, ":fleader_troop", ":fleader"),
				(store_troop_faction, "$team2_faction", ":fleader_troop"),
			(else_try),
				(store_mul, "$team2_faction", ":team2_avg_faction", 10),
				(val_div, "$team2_faction", "$team2_size"),
				(val_add, "$team2_faction", 5),
				(val_div, "$team2_faction", 10),
			(try_end),
		(try_end),
		(try_begin),
			(gt, "$team3_size", 0),
			(team_get_leader, ":fleader", 3),
			(try_begin),
				(ge, ":fleader", 0),
				(agent_get_troop_id, ":fleader_troop", ":fleader"),
				(store_troop_faction, "$team3_faction", ":fleader_troop"),
			(else_try),
				(store_mul, "$team3_faction", ":team3_avg_faction", 10),
				(val_div, "$team3_faction", "$team3_size"),
				(val_add, "$team3_faction", 5),
				(val_div, "$team3_faction", 10),
			(try_end),
		(try_end),
		
		(display_message, "@Forming ranks."),
		#keep cavalry on the map
		(call_script, "script_battlegroup_get_size", "$fplayer_team_no", grc_cavalry),
		(val_mul, reg0, 2),
		(convert_to_fixed_point, reg0),
		(store_sqrt, ":depth_cavalry", reg0),
		(convert_from_fixed_point, ":depth_cavalry"),
		(val_sub, ":depth_cavalry", 1),
		(store_mul, reg0, "$cavalry_space", 50),
		(val_add, reg0, 250),
		(val_mul, ":depth_cavalry", reg0),
		(store_mul, reg0, "$infantry_space", 50),
		(val_add, reg0, formation_minimum_spacing),
		(val_mul, reg0, 2),
		(val_sub, ":depth_cavalry", reg0),
		(try_begin),
			(gt, ":depth_cavalry", 0),
			(agent_get_position, pos49, "$fplayer_agent_no"),
			(copy_position, pos2, pos49),
			(call_script, "script_team_get_position_of_enemies", pos60, "$fplayer_team_no", grc_everyone),
			(call_script, "script_point_y_toward_position", pos2, pos60),
			(position_move_y, pos2, ":depth_cavalry"),
			(agent_set_position, "$fplayer_agent_no", pos2),	#fake out script_cf_formation
		(try_end),

		(call_script, "script_get_default_formation", "$fplayer_team_no"),
		(call_script, "script_player_attempt_formation", grc_infantry, reg0),
		(call_script, "script_player_attempt_formation", grc_cavalry, formation_wedge),
		(call_script, "script_player_attempt_formation", grc_archers, formation_default),
		(try_begin),
			(gt, ":depth_cavalry", 0),
			(agent_set_position, "$fplayer_agent_no", pos49),
		(try_end),

		(set_show_messages, 0),
		(try_for_range, reg0, 3, 9),
			(team_give_order, "$fplayer_team_no", reg0, mordr_hold),
		(try_end),

		#init troops for when formation ends
		(try_for_range, reg0, 0, "$infantry_space"),
			(team_give_order, "$fplayer_team_no", grc_infantry, mordr_spread_out),
		(try_end),
		(try_for_range, reg0, 0, "$archer_space"),
			(team_give_order, "$fplayer_team_no", grc_archers, mordr_spread_out),
		(try_end),
		(try_for_range, reg0, 0, "$cavalry_space"),
			(team_give_order, "$fplayer_team_no", grc_cavalry, mordr_spread_out),
		(try_end),
		(set_show_messages, 1),
	]),
#form ranks command
	(0, 0, 1, [(eq, "$tld_option_formations", 1),(key_clicked, key_for_ranks)], [
		(assign, "$fclock", 1),
		(call_script, "script_player_attempt_formation", grc_infantry, formation_ranks),
		(call_script, "script_player_attempt_formation", grc_archers, formation_ranks)
	]),
#form shield wall command
	(0, 0, 1, [(eq, "$tld_option_formations", 1),(key_clicked, key_for_shield)], [
		(assign, "$fclock", 1),
		(call_script, "script_player_attempt_formation", grc_infantry, formation_shield)
	]),
#form wedge command
	(0, 0, 1, [(eq, "$tld_option_formations", 1),(key_clicked, key_for_wedge)], [
		(assign, "$fclock", 1),
		(call_script, "script_player_attempt_formation", grc_infantry, formation_wedge),
		(call_script, "script_player_attempt_formation", grc_cavalry, formation_wedge)
	]),
#form square command
	(0, 0, 1, [(eq, "$tld_option_formations", 1),(key_clicked, key_for_square)], [
		(assign, "$fclock", 1),
		(call_script, "script_player_attempt_formation", grc_infantry, formation_square)
	]),
#end formation command
	(0, 0, 1, [(eq, "$tld_option_formations", 1),(key_clicked, key_for_undo)], [
		(assign, "$fclock", 1),
		(call_script, "script_player_order_formations", mordr_charge)
	]),
#charge ends formation
	(0, 0, 1, [(eq, "$tld_option_formations", 1),(game_key_clicked, gk_order_charge)], [
		(assign, "$fclock", 1),
		(call_script, "script_player_order_formations", mordr_charge)
	]),
#dismount ends formation
	(0, 0, 1, [(eq, "$tld_option_formations", 1),(game_key_clicked, gk_order_dismount)], [
		(assign, "$fclock", 1),
		(call_script, "script_player_order_formations", mordr_dismount),
	]),
#On hold, any formations reform in new location		
	(0, 0, 1, [(eq, "$tld_option_formations", 1),(game_key_clicked, gk_order_halt)], [
		(assign, "$fclock", 1),
		(call_script, "script_player_order_formations", mordr_hold)
	]),
#Follow is hold	repeated frequently
	(0, 0, 1, [(eq, "$tld_option_formations", 1),(game_key_clicked, gk_order_follow)], [
		(assign, "$fclock", 1),
		(call_script, "script_player_order_formations", mordr_follow)
	]),
#attempt to avoid simultaneous formations function calls
	(1, 0, 0, [	
        (eq, "$tld_option_formations", 1),
		(call_script, "script_store_battlegroup_data"),
		(neg|key_is_down, key_for_ranks),
		(neg|key_is_down, key_for_shield),
		(neg|key_is_down, key_for_wedge),
		(neg|key_is_down, key_for_square),
		(neg|key_is_down, key_for_undo),
		(neg|game_key_is_down, gk_order_charge),
		(neg|game_key_is_down, gk_order_dismount),
		(neg|game_key_is_down, gk_order_halt),
		(neg|game_key_is_down, gk_order_follow),
		(neg|game_key_is_down, gk_order_advance),
		(neg|game_key_is_down, gk_order_fall_back),
		(neg|game_key_is_down, gk_order_spread_out),
		(neg|game_key_is_down, gk_order_stand_closer)
	  ], [
		(set_fixed_point_multiplier, 100),
		(store_mod, ":fifth_second", "$fclock", 5),
		(call_script, "script_team_get_position_of_enemies", pos60, "$fplayer_team_no", grc_everyone),
		(try_begin),
			(eq, reg0, 0),	#no more enemies?
			(call_script, "script_formation_end", "$fplayer_team_no", grc_everyone),
		(else_try),
			(assign, "$autorotate_at_player", 0),
			(try_begin),
				(neq, "$infantry_formation_type", formation_none),
				(try_begin),
					(eq, "$infantry_formation_move_order", mordr_follow),
					(call_script, "script_cf_formation", "$fplayer_team_no", grc_infantry, "$infantry_space", "$infantry_formation_type"),
				(else_try),	#periodically reform
					(eq, ":fifth_second", 0),
					(team_get_movement_order, reg0, "$fplayer_team_no", grc_infantry),
					(neq, reg0, mordr_stand_ground),
					(call_script, "script_get_formation_position", pos1, "$fplayer_team_no", grc_infantry),
					(position_move_y, pos1, -2000),
					(call_script, "script_point_y_toward_position", pos1, pos60),
					(position_move_y, pos1, 2000),
					(call_script, "script_set_formation_position", "$fplayer_team_no", grc_infantry, pos1),					
					(call_script, "script_battlegroup_get_size", "$fplayer_team_no", grc_infantry),
					(assign, ":troop_count", reg0),
					(call_script, "script_get_centering_amount", "$infantry_formation_type", ":troop_count", "$infantry_space"),
					(position_move_x, pos1, reg0),
					(call_script, "script_form_infantry", "$fplayer_team_no", "$fplayer_agent_no", "$infantry_space", "$infantry_formation_type"),		
				(try_end),
			(try_end),
			(try_begin),
				(neq, "$cavalry_formation_type", formation_none),
				(try_begin),
					(eq, "$cavalry_formation_move_order", mordr_follow),
					(call_script, "script_cf_formation", "$fplayer_team_no", grc_cavalry, "$cavalry_space", "$cavalry_formation_type"),
				(else_try),	#periodically reform
					(eq, ":fifth_second", 0),
					(team_get_movement_order, reg0, "$fplayer_team_no", grc_cavalry),
					(neq, reg0, mordr_stand_ground),
					(call_script, "script_get_formation_position", pos1, "$fplayer_team_no", grc_cavalry),
					(call_script, "script_point_y_toward_position", pos1, pos60),
					(call_script, "script_set_formation_position", "$fplayer_team_no", grc_cavalry, pos1),
					(call_script, "script_form_cavalry", "$fplayer_team_no", "$fplayer_agent_no", "$cavalry_space"),
				(try_end),
			(try_end),
			(try_begin),
				(neq, "$archer_formation_type", formation_none),
				(try_begin),
					(eq, "$archer_formation_move_order", mordr_follow),
					(call_script, "script_cf_formation", "$fplayer_team_no", grc_archers, "$archer_space", "$archer_formation_type"),
				(else_try),	#periodically reform
					(eq, ":fifth_second", 0),
					(team_get_movement_order, reg0, "$fplayer_team_no", grc_archers),
					(neq, reg0, mordr_stand_ground),
					(call_script, "script_get_formation_position", pos1, "$fplayer_team_no", grc_archers),
					(position_move_y, pos1, -2000),
					(call_script, "script_point_y_toward_position", pos1, pos60),
					(position_move_y, pos1, 2000),
					(call_script, "script_set_formation_position", "$fplayer_team_no", grc_archers, pos1),
					(call_script, "script_battlegroup_get_size", "$fplayer_team_no", grc_archers),
					(assign, ":troop_count", reg0),
					(call_script, "script_get_centering_amount", formation_default, ":troop_count", "$archer_space"),
					(val_mul, reg0, -1),
					(position_move_x, pos1, reg0),
					(call_script, "script_form_archers", "$fplayer_team_no", "$fplayer_agent_no", "$archer_space", "$archer_formation_type"),		
				(try_end),
			(try_end),
			(assign, "$autorotate_at_player", formation_autorotate_at_player),
		(try_end),
		(val_add, "$fclock", 1),
	]),
	
	(0, 0, 0, [(eq, "$tld_option_formations", 1),(game_key_clicked, gk_order_advance)], [(call_script, "script_player_order_formations", mordr_advance)]),
	(0, 0, 0, [(eq, "$tld_option_formations", 1),(game_key_clicked, gk_order_fall_back)], [(call_script, "script_player_order_formations", mordr_fall_back)]),
	(0, 0, 0, [(eq, "$tld_option_formations", 1),(game_key_clicked, gk_order_spread_out)], [(call_script, "script_player_order_formations", mordr_spread_out)]),
	(0, 0, 0, [(eq, "$tld_option_formations", 1),(game_key_clicked, gk_order_stand_closer)], [(call_script, "script_player_order_formations", mordr_stand_closer)]),
]
#end formations triggers


tld_common_battle_scripts = [
 	custom_tld_spawn_troop,
	custom_tld_init_battle,
	custom_tld_horses_hate_trolls,
	tld_cheer_on_space_when_battle_over_press,
	tld_cheer_on_space_when_battle_over_release,
	nazgul_sweeps,
	custom_troll_hitting,
	custom_warg_sounds,
	#custom_lone_wargs_special_attack, # WIP, needs more work (mtarini)
	custom_lone_wargs_are_aggressive,
	tld_player_cant_ride,
#	cheat_kill_all_on_ctrl_k,  
	cheat_kill_self_on_ctrl_s,  
#	cheat_heal_self_on_ctrl_h
##        common_battle_kill_underwater,
	]
	
tld_siege_battle_scripts = [
 	custom_tld_spawn_troop,
	custom_tld_init_battle,
	tld_cheer_on_space_when_battle_over_press,
	tld_cheer_on_space_when_battle_over_release,
#	nazgul_sweeps,
	custom_troll_hitting,
#	cheat_kill_all_on_ctrl_k,  
#	cheat_kill_self_on_ctrl_s,  
	]

tld_common_peacetime_scripts = [
	tld_player_cant_ride,
	dungeon_darkness_effect,
] + custom_tld_bow_to_kings


mission_templates = [
  ( "town_default",0,-1,
    "Default town visit",
    [(0,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (1,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),(2,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (3,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (4,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),(5,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),(6,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),(7,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (8,mtef_scene_source,af_override_horse,0,1,[]),(9,mtef_visitor_source,af_override_horse,0,1,[]),(10,mtef_scene_source,af_override_horse,0,1,[]),(11,mtef_scene_source,af_override_horse,0,1,[]),
     (12,mtef_scene_source,af_override_horse,0,1,[]),(13,mtef_scene_source,0,0,1,[]),(14,mtef_scene_source,0,0,1,[]),(15,mtef_scene_source,0,0,1,[]),
     (16,mtef_visitor_source,af_override_horse,0,1,[]),(17,mtef_visitor_source,af_override_horse,0,1,[]),(18,mtef_visitor_source,af_override_horse,0,1,[]),(19,mtef_visitor_source,af_override_horse,0,1,[]),(20,mtef_visitor_source,af_override_horse,0,1,[]),(21,mtef_visitor_source,af_override_horse,0,1,[]),(22,mtef_visitor_source,af_override_horse,0,1,[]),(23,mtef_visitor_source,af_override_horse,0,1,[]),(24,mtef_visitor_source,af_override_horse,0,1,[]),
     (25,mtef_visitor_source,af_override_horse,0,1,[]),(26,mtef_visitor_source,af_override_horse,0,1,[]),(27,mtef_visitor_source,af_override_horse,0,1,[]),(28,mtef_visitor_source,af_override_horse,0,1,[]),(29,mtef_visitor_source,af_override_horse,0,1,[]),(30,mtef_visitor_source,af_override_horse,0,1,[]),(31,mtef_visitor_source,af_override_horse,0,1,[]),
     ],
    [ (ti_on_agent_spawn, 0, 0, [],[(store_trigger_param_1, ":agent_no"),(call_script, "script_init_town_agent", ":agent_no")]),
      (1, 0, ti_once, [], [(store_current_scene, ":cur_scene"),(scene_set_slot, ":cur_scene", slot_scene_visited, 1)]),
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),
      (ti_inventory_key_pressed, 0, 0, [(set_trigger_result,1)],[]),
      (ti_tab_pressed, 0, 0, [(set_trigger_result,1)],[]),
]),
 
# This template is used in party encounters and such.
  ( "conversation_encounter",0,-1,
    "Conversation_encounter",
    [( 0,mtef_visitor_source,af_override_fullhelm,0,1,[]),( 1,mtef_visitor_source,0,0,1,[]),
     ( 2,mtef_visitor_source,af_override_fullhelm,0,1,[]),( 3,mtef_visitor_source,0,0,1,[]),( 4,mtef_visitor_source,0,0,1,[]),( 5,mtef_visitor_source,0,0,1,[]),( 6,mtef_visitor_source,0,0,1,[]),
     ( 7,mtef_visitor_source,af_override_fullhelm,0,1,[]),( 8,mtef_visitor_source,0,0,1,[]),( 9,mtef_visitor_source,0,0,1,[]),(10,mtef_visitor_source,0,0,1,[]),(11,mtef_visitor_source,0,0,1,[]),
    #prisoners now...
     (12,mtef_visitor_source,0,0,1,[]),(13,mtef_visitor_source,0,0,1,[]),(14,mtef_visitor_source,0,0,1,[]),(15,mtef_visitor_source,0,0,1,[]),(16,mtef_visitor_source,0,0,1,[]),
    #Other party
     (17,mtef_visitor_source,af_override_fullhelm,0,1,[]),(18,mtef_visitor_source,0,0,1,[]),(19,mtef_visitor_source,0,0,1,[]),(20,mtef_visitor_source,0,0,1,[]),(21,mtef_visitor_source,0,0,1,[]),
     (22,mtef_visitor_source,0,0,1,[]),(23,mtef_visitor_source,0,0,1,[]),(24,mtef_visitor_source,0,0,1,[]),(25,mtef_visitor_source,0,0,1,[]),(26,mtef_visitor_source,0,0,1,[]),
     (27,mtef_visitor_source,0,0,1,[]),(28,mtef_visitor_source,0,0,1,[]),(29,mtef_visitor_source,0,0,1,[]),(30,mtef_visitor_source,0,0,1,[]),
	# opponent troops cheering
	 (31,mtef_defenders|mtef_team_1,0,aif_start_alarmed,1,[]),(32,mtef_attackers|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [ # other people in the backgroud
	  (1, 0, ti_once, [(neq,"$party_meeting",0)], 
	    [   # a small comment about the purpose of this? Position of enemy/freindly troops changes according to attacking/non attacking?
			# GA: encountered party can be either attacker or defender, and those spawn in different entries
			(try_begin),(encountered_party_is_attacker),
				(add_reinforcements_to_entry,32,8),  
		    (else_try),								
				(add_reinforcements_to_entry,31,8),
			(try_end),
		]
	   ),

		# freindly greetings (after 0.2 secs)
		(0, 0.2, ti_once, [], [ 
			(eq,"$party_meeting",1), # feindly
			(try_for_agents,":agent"),
				
				(agent_is_human, ":agent"),
				(agent_get_entry_no,":e",":agent"),(eq,":e",17),
				(agent_get_troop_id, ":trp", ":agent"),
				(troop_get_type, ":race", ":trp"),
				(store_troop_faction, ":fac", ":trp"),
				(assign, ":greet_ani", -1),
				(try_begin), (is_between,  ":race", tf_elf_begin, tf_elf_end), 
					(assign, ":greet_ani", "anim_greet_elf"),
				(else_try), (eq,  ":race", tf_orc), 
					(assign, ":greet_ani", "anim_greet_orc"),
				(else_try),
					(this_or_next|eq, ":fac", "fac_gondor"),
					(this_or_next|eq, ":fac", "fac_umbar"),
					(eq, ":fac", "fac_rohan"),
					(assign, ":greet_ani", "anim_greet_human"),
				(else_try), (is_between,  ":race", tf_orc_begin, tf_orc_end),  # other orcs
					(assign, ":greet_ani", "anim_greet_goaway"),
				(else_try), # all others
					(assign, ":greet_ani", "anim_greet_simple"),
				(try_end),
				(try_begin),
					(gt,":greet_ani",0), 
					(agent_get_horse,":e",":agent"),					
					(try_begin),(ge,":e",0), 
						(val_add, ":greet_ani", 1),
					(try_end),
				
					(agent_set_animation, ":agent", ":greet_ani"),
				(try_end),
			(try_end),
			
		]),
	   
     (3, 2, 0, [], [ 
#	         (entry_point_get_position,pos1,0),
		(team_set_relation, 0, 1, 1),
		(set_show_messages, 0),
		(team_give_order, 1, grc_everyone, mordr_hold),
		(team_give_order, 1, grc_archers, mordr_stand_ground),
		(set_show_messages, 1),
		(try_begin),
			 (eq,"$party_meeting",-1), # hostile, and only once
			 (try_for_agents,":agent"),
				(agent_get_entry_no,":e",":agent"),
				(this_or_next|neq,":e",0),(neq,":e",17), # <== WARINING: this makes no sense (mtairni)
				
				(store_random_in_range,":rnd",0,10),(lt,":rnd",5), # 50% of times
				
				(agent_get_horse,":e",":agent"),					
				(try_begin),(eq,":e",-1), 
					(agent_set_animation, ":agent", "anim_cheer"),
				(else_try),
					(agent_set_animation, ":agent", "anim_cheer_player_ride"),
				(try_end),
			(try_end),
		(try_end),
		(assign,"$party_meeting",0),
	  ]),
	],
  ),
  
#----------------------------------------------------------------
#mission templates before this point are hardwired into the game.
#-----------------------------------------------------------------
  ( "town_center",0,-1,
    "Default town visit",
    [(0,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (1,mtef_scene_source|mtef_team_0,0,0,1,[]),
     (2,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),(3,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (4,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),(5,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (6,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),(7,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     
     (8 ,mtef_scene_source,af_override_horse,0,1,[]),
     (9 ,mtef_visitor_source,af_override_horse,0,1,[]),(10,mtef_visitor_source,af_override_horse,0,1,[]),(11,mtef_visitor_source,af_override_horse,0,1,[]),(12,mtef_visitor_source,af_override_horse,0,1,[]),(13,mtef_scene_source,0,0,1,[]),(14,mtef_scene_source,0,0,1,[]),(15,mtef_scene_source,0,0,1,[]),
     (16,mtef_visitor_source,af_override_horse,0,1,[]),(17,mtef_visitor_source,af_override_horse,0,1,[]),(18,mtef_visitor_source,af_override_horse,0,1,[]),(19,mtef_visitor_source,af_override_horse,0,1,[]),(20,mtef_visitor_source,af_override_horse,0,1,[]),(21,mtef_visitor_source,af_override_horse,0,1,[]),(22,mtef_visitor_source,af_override_horse,0,1,[]),(23,mtef_visitor_source,af_override_horse,0,1,[]),
     (24,mtef_visitor_source,af_override_horse,0,1,[]),(25,mtef_visitor_source,af_override_horse,0,1,[]),(26,mtef_visitor_source,af_override_horse,0,1,[]),(27,mtef_visitor_source,af_override_horse,0,1,[]),(28,mtef_visitor_source,af_override_horse,0,1,[]),(29,mtef_visitor_source,af_override_horse,0,1,[]),(30,mtef_visitor_source,af_override_horse,0,1,[]),(31,mtef_visitor_source,af_override_horse,0,1,[]),
     (32,mtef_visitor_source,af_override_horse|af_override_weapons|af_override_head,0,1,[]),(33,mtef_visitor_source,af_override_horse|af_override_weapons,0,1,[]),(34,mtef_visitor_source,af_override_horse|af_override_weapons|af_override_head,0,1,[]),(35,mtef_visitor_source,af_override_horse|af_override_weapons,0,1,[]),(36,mtef_visitor_source,af_override_horse,0,1,[]),(37,mtef_visitor_source,af_override_horse|af_override_head,0,1,[]),(38,mtef_visitor_source,af_override_horse|af_override_weapons,0,1,[]),(39,mtef_visitor_source,af_override_horse,0,1,[]),
     (40,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(41,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(42,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(43,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (44,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(45,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(46,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(47,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     ],
    tld_common_peacetime_scripts +[
        (1, 0, ti_once, [],
         [ (get_player_agent_no, "$current_player_agent"),
           (try_begin),
             (eq, "$g_mt_mode", tcm_default),
             (store_current_scene, ":cur_scene"),
             (scene_set_slot, ":cur_scene", slot_scene_visited, 1),
           (try_end),
           (call_script, "script_init_town_walker_agents"),
           (try_begin),
             (eq, "$sneaked_into_town", 1),
             (call_script, "script_music_set_situation_with_culture", mtf_sit_town_infiltrate),
           (else_try),
             (call_script, "script_music_set_situation_with_culture", mtf_sit_travel),
           (try_end),
          ]),
        (ti_before_mission_start, 0, 0, [], [
			(call_script, "script_change_banners_and_chest"),
			(try_begin),# remove beam bridges in osgiliath (for non battle scenes)
				(store_current_scene, ":cur_scene"),
				(this_or_next|eq,  ":cur_scene", "scn_east_osgiliath_center"),
				(eq,  ":cur_scene", "scn_west_osgiliath_center"),
				(replace_scene_props, "spr_osgiliath_broken_bridge_beams", "spr_empty"),
			(try_end),
			# check if dungeons are present in a scene
			(assign, "$dungeons_in_scene", 0), 
			(try_for_range,":cur_scene","spr_light_fog_black0","spr_moria_rock"),
				(scene_prop_get_num_instances,":max_instance", ":cur_scene"),
				(ge,":max_instance", 1),
				(assign, "$dungeons_in_scene", 1), 
			(try_end),
		]),
        (ti_inventory_key_pressed, 0, 0,
         [ (try_begin),
             (eq, "$g_mt_mode", tcm_default),
             (set_trigger_result,1),
           (else_try),
             (eq, "$g_mt_mode", tcm_disguised),
             (display_message,"str_cant_use_inventory_disguised"),
           (else_try),
             (display_message, "str_cant_use_inventory_now"),
           (try_end),
           ], []),
        (ti_tab_pressed, 0, 0,
         [ (try_begin),
             (this_or_next|eq, "$g_mt_mode", tcm_default),
             (eq, "$g_mt_mode", tcm_disguised),
             (try_begin),
               (check_quest_active, "qst_hunt_down_fugitive"),
               (neg|check_quest_succeeded, "qst_hunt_down_fugitive"),
               (neg|check_quest_failed, "qst_hunt_down_fugitive"),
               (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_current_state, 1),
               (quest_get_slot, ":quest_object_troop", "qst_hunt_down_fugitive", slot_quest_object_troop),
               (try_begin),
                 (call_script, "script_cf_troop_agent_is_alive", ":quest_object_troop"),
                 (call_script, "script_fail_quest", "qst_hunt_down_fugitive"),
               (else_try),
                 (call_script, "script_succeed_quest", "qst_hunt_down_fugitive"),
               (try_end),
             (try_end),
             (set_trigger_result,1),
           (else_try),
             (display_message, "@Cannot leave now."),
           (try_end),
           ], []),

        (ti_on_leave_area, 0, 0,[(try_begin),(eq, "$g_defending_against_siege", 0),(assign,"$g_leave_town",1),(try_end)],[]),

        (0, 0, ti_once, [], [
		   (party_slot_eq, "$current_town", slot_party_type, spt_town),
           (call_script, "script_town_init_doors", 0),
           (try_begin),
		      (party_get_slot, ":a","$current_town",slot_center_ambient_sound_always),
		      (try_begin),(gt,":a",0),(play_sound, ":a", sf_looping),(try_end),
              (neg|is_currently_night),
                (party_get_slot, ":a","$current_town",slot_center_ambient_sound_day),
			    (try_begin),(gt,":a",0),(play_sound, ":a", sf_looping),(try_end),
           (try_end),
        ]),
        (3, 0, 0, [(call_script, "script_tick_town_walkers")], []),
        (2, 0, 0, [(call_script, "script_center_ambiance_sounds")], []),
        (1, 0, ti_once, [(check_quest_active, "qst_hunt_down_fugitive"),
                       (neg|check_quest_succeeded, "qst_hunt_down_fugitive"),
                       (neg|check_quest_failed, "qst_hunt_down_fugitive"),
                       (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_current_state, 1),
                       (quest_get_slot, ":quest_object_troop", "qst_hunt_down_fugitive", slot_quest_object_troop),
                       (assign, ":not_alive", 0),
                       (try_begin),
                         (call_script, "script_cf_troop_agent_is_alive", ":quest_object_troop"),
                       (else_try),
                         (assign, ":not_alive", 1),
                       (try_end),
                       (this_or_next|main_hero_fallen),
                       (eq, ":not_alive", 1),
                       ],
         [(try_begin),
            (main_hero_fallen),
            (jump_to_menu, "mnu_village_hunt_down_fugitive_defeated"),
            (call_script, "script_fail_quest", "qst_hunt_down_fugitive"),
            (finish_mission, 4),
          (else_try),
            #(call_script, "script_change_player_relation_with_center", "$current_town", -2),
            (call_script, "script_succeed_quest", "qst_hunt_down_fugitive"),
          (try_end),
         ]),
		 	  # check for different checkpoints reach (merchants, center of town etc)
	  (2, 0, 0, [],
       [(agent_get_position, pos1, "$current_player_agent"),
		(try_begin),
			(party_slot_eq, "$current_town", slot_center_visited, 0),
			(entry_point_get_position, pos2, 0),
			(get_distance_between_positions, ":dist", pos2, pos1),
			(lt, ":dist", 500),
			(party_set_slot, "$current_town", slot_center_visited, 1),
			(display_message, "@You_have_reached_main_square..."),
		(try_end),
		(try_begin),
			(party_slot_eq, "$current_town", slot_weaponsmith_visited, 0),
#			(neg|party_slot_eq, "$current_town", slot_town_weaponsmith, "trp_no_troop"),
			(entry_point_get_position, pos2, 10),
			(get_distance_between_positions, ":dist", pos2, pos1),
			(lt, ":dist", 300),
			(party_set_slot, "$current_town", slot_weaponsmith_visited, 1),
			(display_message, "@You_have_found_the_local_smithy..."),
		(try_end),      
		(try_begin),
			(party_slot_eq, "$current_town", slot_elder_visited, 0),
#			(neg|party_slot_eq, "$current_town", slot_town_elder, "trp_no_troop"),
			(entry_point_get_position, pos2, 11),
			(get_distance_between_positions, ":dist", pos2, pos1),
			(lt, ":dist", 300),
			(party_set_slot, "$current_town", slot_elder_visited, 1),
			(display_message, "@You_have_found_the_local_authority..."),
		(try_end),      
		(try_begin),
			(party_slot_eq, "$current_town", slot_merchant_visited, 0),
#			(neg|party_slot_eq, "$current_town", slot_town_merchant, "trp_no_troop"),
			(entry_point_get_position, pos2, 12),
			(get_distance_between_positions, ":dist", pos2, pos1),
			(lt, ":dist", 300),
			(party_set_slot, "$current_town", slot_merchant_visited, 1),
			(display_message, "@You_have_found_the_local_warehouse..."),
		(try_end),      
		]),
        ],
    ),

  ( "bandits_at_night",0,-1,
    "Default town visit",
    [(0,mtef_scene_source|mtef_team_2, af_override_horse, 0, 1, pilgrim_disguise), #MV: player set to team 2
     (1,mtef_scene_source|mtef_team_0,0,0,1,[]),
     (2,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (3,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (4,mtef_visitor_source|mtef_team_0, af_override_horse, aif_start_alarmed, 1, []),
     (5,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (6,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (7,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     
     (8,mtef_visitor_source,af_override_horse,0,1,[]),
     (9,mtef_visitor_source,af_override_horse,0,1,[]),(10,mtef_visitor_source,af_override_horse,0,1,[]),(11,mtef_visitor_source,af_override_horse,aif_start_alarmed,1,[]),(12,mtef_visitor_source,af_override_horse,0,1,[]),(13,mtef_visitor_source,0,0,1,[]),(14,mtef_visitor_source,0,0,1,[]),(15,mtef_visitor_source,0,0,1,[]),
     (16,mtef_visitor_source,af_override_horse,0,1,[]),(17,mtef_visitor_source,af_override_horse,0,1,[]),(18,mtef_visitor_source,af_override_horse,0,1,[]),(19,mtef_visitor_source,af_override_horse,0,1,[]),(20,mtef_visitor_source,af_override_horse,0,1,[]),(21,mtef_visitor_source,af_override_horse,0,1,[]),(22,mtef_visitor_source,af_override_horse,0,1,[]),(23,mtef_visitor_source,af_override_horse,0,1,[]),
     (24,mtef_visitor_source,af_override_horse,0,1,[]),(25,mtef_visitor_source,af_override_horse,0,1,[]),(26,mtef_visitor_source,af_override_horse,0,1,[]),(27,mtef_visitor_source,af_override_horse,aif_start_alarmed,1,[]),(28,mtef_visitor_source,af_override_horse,aif_start_alarmed,1,[]),(29,mtef_visitor_source,af_override_horse,0,1,[]),(30,mtef_visitor_source,af_override_horse,0,1,[]),(31,mtef_visitor_source,af_override_horse,0,1,[]),
     (32,mtef_visitor_source,af_override_horse,0,1,[]),(33,mtef_visitor_source,af_override_horse,0,1,[]),(34,mtef_visitor_source,af_override_horse,0,1,[]),(35,mtef_visitor_source,af_override_horse,0,1,[]),(36,mtef_visitor_source,af_override_horse,0,1,[]),(37,mtef_visitor_source,af_override_horse,0,1,[]),(38,mtef_visitor_source,af_override_horse,0,1,[]),(39,mtef_visitor_source,af_override_horse,0,1,[]),
     (40,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(41,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(42,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(43,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (44,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(45,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(46,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(47,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     ],
    tld_common_battle_scripts+[
      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (agent_get_troop_id, ":troop_no", ":agent_no"),
         (neq, ":troop_no", "trp_player"),
         (agent_set_team, ":agent_no", 1), #bandits are team 1
         ]),

      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest"), (team_set_relation, 1, 0, 0),(team_set_relation, 2, 0, 0),]), #MV: both player and bandits neutral to guards
      common_inventory_not_available,
      
      (ti_tab_pressed  , 0, 0,[(display_message, "@Cannot leave now.")], []),
      (ti_on_leave_area, 0, 0,[(try_begin),(eq, "$g_defending_against_siege", 0),(assign,"$g_leave_town",1),(try_end)], []),
      (0, 0, ti_once, [],
       [ (call_script, "script_music_set_situation_with_culture", mtf_sit_ambushed),
         (set_party_battle_mode),
         (party_slot_eq, "$current_town", slot_party_type, spt_town),
         (call_script, "script_town_init_doors", 0),
        ]),

      (1, 4, ti_once,
       [ (store_mission_timer_a,":cur_time"),
         (ge, ":cur_time", 5),
         (this_or_next|main_hero_fallen),
         (num_active_teams_le,2) #MV: was 1
         ],
       [ (try_begin),
           (main_hero_fallen),
           (jump_to_menu, "mnu_town_bandits_failed"),
         (else_try),
           (jump_to_menu, "mnu_town_bandits_succeeded"),
         (try_end),
         (finish_mission),
         ]),
      ],
    ),

  ( "town_brawl",0,-1,
    "Town brawl with walkers",
    [(0,mtef_scene_source|mtef_team_1, af_override_horse|af_override_weapons, aif_start_alarmed, 1, [itm_wood_club]), #MV: player set to team 1 (guards are enemies)
     (1,mtef_scene_source|mtef_team_0,0,0,1,[]),
     (2,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (3,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (4,mtef_visitor_source|mtef_team_0, af_override_horse, aif_start_alarmed, 1, []),
     (5,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (6,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (7,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     
     (8,mtef_scene_source,af_override_horse,0,1,[]),
     (9,mtef_visitor_source,af_override_horse,0,1,[]),(10,mtef_visitor_source,af_override_horse,0,1,[]),(11,mtef_visitor_source,af_override_horse,aif_start_alarmed,1,[]),(12,mtef_visitor_source,af_override_horse,0,1,[]),(13,mtef_scene_source,0,0,1,[]),(14,mtef_scene_source,0,0,1,[]),(15,mtef_scene_source,0,0,1,[]),
     (16,mtef_visitor_source,af_override_horse,0,1,[]),(17,mtef_visitor_source,af_override_horse,0,1,[]),(18,mtef_visitor_source,af_override_horse,0,1,[]),(19,mtef_visitor_source,af_override_horse,0,1,[]),(20,mtef_visitor_source,af_override_horse,0,1,[]),(21,mtef_visitor_source,af_override_horse,0,1,[]),(22,mtef_visitor_source,af_override_horse,0,1,[]),(23,mtef_visitor_source,af_override_horse,0,1,[]),
     (24,mtef_visitor_source,af_override_horse,0,1,[]),(25,mtef_visitor_source,af_override_horse,0,1,[]),(26,mtef_visitor_source,af_override_horse,0,1,[]),(27,mtef_visitor_source,af_override_horse,aif_start_alarmed,1,[]),(28,mtef_visitor_source,af_override_horse,aif_start_alarmed,1,[]),(29,mtef_visitor_source,af_override_horse,0,1,[]),(30,mtef_visitor_source,af_override_horse,0,1,[]),(31,mtef_visitor_source,af_override_horse,0,1,[]),
     
     #walkers: some friends, some enemies
     (32,mtef_visitor_source|mtef_team_2,af_override_horse|af_override_weapons,aif_start_alarmed,1,[itm_wood_club]),
     (33,mtef_visitor_source|mtef_team_2,af_override_horse|af_override_weapons,aif_start_alarmed,1,[itm_wood_club]),
     (34,mtef_visitor_source|mtef_team_2,af_override_horse|af_override_weapons,aif_start_alarmed,1,[itm_wood_club]),
     (35,mtef_visitor_source|mtef_team_2,af_override_horse|af_override_weapons,aif_start_alarmed,1,[itm_wood_club]),
     (36,mtef_visitor_source|mtef_team_1,af_override_horse|af_override_weapons,aif_start_alarmed,1,[itm_wood_club]),
     (37,mtef_visitor_source|mtef_team_1,af_override_horse|af_override_weapons,aif_start_alarmed,1,[itm_wood_club]),
     (38,mtef_visitor_source|mtef_team_1,af_override_horse|af_override_weapons,aif_start_alarmed,1,[itm_wood_club]),
     (39,mtef_visitor_source|mtef_team_1,af_override_horse|af_override_weapons,aif_start_alarmed,1,[itm_wood_club]),
     #(40,mtef_visitor_source|mtef_team_1,af_override_horse|af_override_weapons,aif_start_alarmed,1,[itm_wood_club]),
     ],
    tld_common_battle_scripts+[
      (ti_before_mission_start, 0, 0, [], [
        (call_script, "script_change_banners_and_chest"),
        (mission_disable_talk),
        #remove some cabbage guard spawn points, so castle and prison guards don't spawn
        (replace_scene_props, "spr_troop_prison_guard", "spr_empty"),
        (replace_scene_props, "spr_troop_castle_guard", "spr_empty"),
        # remove all other guards except the first five - doesn't work!
        # (init_position, pos1),
        # (position_move_z, pos1, -1000000),
        # (scene_prop_get_num_instances, ":num_guards", "spr_troop_guard"),
        # (try_for_range, ":count", 5, ":num_guards"),
          # (scene_prop_get_instance, ":guard_instance", "spr_troop_guard", ":count"),
          # (prop_instance_set_position, ":guard_instance", pos1), #does this work?? how do you remove a single prop?
        # (try_end),
        ]),
      
      common_inventory_not_available,
      (ti_tab_pressed  , 0, 0,[(display_message, "@Cannot leave now.")], []),
      (ti_on_leave_area, 0, 0,[(try_begin),(eq, "$g_defending_against_siege", 0),(assign,"$g_leave_town",1),(try_end)], []),
      (0, 0, ti_once, [],
       [ (call_script, "script_music_set_situation_with_culture", mtf_sit_ambushed),
         (set_party_battle_mode),
         (party_slot_eq, "$current_town", slot_party_type, spt_town),
         (call_script, "script_town_init_doors", 0),
        ]),

      (1, 4, ti_once,
       [ (store_mission_timer_a,":cur_time"),
         (ge, ":cur_time", 5),
         (this_or_next|main_hero_fallen),
         (num_active_teams_le, 1)
         ],
       [ (try_begin),
          (main_hero_fallen),
          (jump_to_menu, "mnu_town_brawl_lost"),
         (else_try),
          (jump_to_menu, "mnu_town_brawl_won"),
         (try_end),
         (finish_mission),
         ]),
      ],
),

# FANGORN BATTLE VS random ents!!! (mtarini)  
( "fangorn_battle",mtf_battle_mode,charge,
    "You lead your men to battle Ents!",
    [
     (1,mtef_team_1,0,aif_start_alarmed,12,[]),
     (0,mtef_team_1,0,aif_start_alarmed,0,[]),
     (2,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
     (3,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
    ],
	tld_common_battle_scripts+[   
		common_battle_tab_press,
		common_inventory_not_available, 
		(0, 0, ti_once, [], [(assign,"$battle_won",0),
                           (assign,"$defender_reinforcement_stage",0),
                           (assign,"$attacker_reinforcement_stage",0),
                           (assign,"$g_presentation_battle_active", 0),
                           #(call_script, "script_place_player_banner_near_inventory"),
                           (call_script, "script_combat_music_set_situation_with_culture"),
        ]),
		common_music_situation_update,
		common_battle_check_friendly_kills,
		(ti_before_mission_start, 0, 0, [],
		[
         (team_set_relation, 1, 0, -1),
		 (team_set_relation, 1, 2, -1),
         #(team_set_relation, 1, 3, 1),
         ]),
		(35,0,0, [], [
		   (store_random_in_range,":d100",1,101),
		   (lt,":d100",35), # 35% of the times...
		   (this_or_next|lt,":d100",8), # 8%: every 35 secs an ent appears anyway
		   (gt,"$g_fangorn_rope_pulled",10), # or an ent appears at cost of 10 points of 
		   (val_sub,"$g_fangorn_rope_pulled",10),
		   (val_max,"$g_fangorn_rope_pulled",0),
		   (store_random_in_range,":entry_point",2,5),
		   (add_visitors_to_current_scene, ":entry_point", "trp_ent", 1),
		   (display_message, "@New ent reached battle scene..."),
		]),
		common_battle_check_victory_condition,
		common_battle_victory_display,

	  (1, 4, ti_once, [(main_hero_fallen)],
        [     (assign, "$pin_player_fallen", 1),
              (str_store_string, s5, "str_retreat"),
              (call_script, "script_simulate_retreat", 10, 20),
              (assign, "$g_battle_result", -1),
              (set_mission_result,-1),
              (call_script, "script_count_mission_casualties_from_agents"),
              (finish_mission,0)]),

      #common_battle_inventory,
      common_battle_order_panel,
      common_battle_order_panel_tick,
    ]
),
  
( "lead_charge",mtf_battle_mode,charge,
  "You lead your men to battle.",
	[(1,mtef_defenders|mtef_team_0,0,aif_start_alarmed,12,[]),
     (0,mtef_defenders|mtef_team_0,0,aif_start_alarmed,0,[]),
     (4,mtef_attackers|mtef_team_1,0,aif_start_alarmed,12,[]),
     (4,mtef_attackers|mtef_team_1,0,aif_start_alarmed,0,[]),

     (8,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),  # this needs be the 5th entry point, for WARGS
     (5,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),  # this needs be the 5th entry point, for WARGS
     (6,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),  # this needs be the 6th entry point, for WARGS
     (7,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),  # this needs be the 7th entry point, for WARGS
     (8,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),  # this needs be the 8th entry point, for WARGS
     ],
    formations_triggers + AI_triggers +
    common_deathcam_triggers+
    tld_common_battle_scripts+[

      common_battle_tab_press,

      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (assign, "$pin_player_fallen", 0),
        (try_begin),
          (store_mission_timer_a, ":elapsed_time"),
          (gt, ":elapsed_time", 20),
          (str_store_string, s5, "str_retreat"),
          (call_script, "script_simulate_retreat", 10, 20),
        (try_end),
        (call_script, "script_count_mission_casualties_from_agents"),
        (finish_mission,0),]),

      (ti_before_mission_start, 0, 0, [],
       [ (team_set_relation, 0, 2, 1),
         (team_set_relation, 1, 3, 1),
         (call_script, "script_place_player_banner_near_inventory_bms"),
         ]),

      (0, 0, ti_once, [], [(assign,"$battle_won",0),
                           (assign,"$defender_reinforcement_stage",0),
                           (assign,"$attacker_reinforcement_stage",0),
                           (assign,"$g_presentation_battle_active", 0),
                           (call_script, "script_place_player_banner_near_inventory"),
                           (call_script, "script_combat_music_set_situation_with_culture"),
                           ]),

      common_music_situation_update,
      common_battle_check_friendly_kills,

      (1, 0, 5, [(lt,"$defender_reinforcement_stage",2),
                 (store_mission_timer_a,":mission_time"),
                 (ge,":mission_time",10),
                 (store_normalized_team_count,":num_defenders", 0),
                 (lt,":num_defenders",6)],
           [(add_reinforcements_to_entry,0,7),(val_add,"$defender_reinforcement_stage",1)]),
      
      (1, 0, 5, [(lt,"$attacker_reinforcement_stage",2),
                 (store_mission_timer_a,":mission_time"),
                 (ge,":mission_time",10),
                 (store_normalized_team_count,":num_attackers", 1),
                 (lt,":num_attackers",6)],
           [(add_reinforcements_to_entry,3,7),(val_add,"$attacker_reinforcement_stage",1)]),
      
      common_battle_check_victory_condition,
      common_battle_victory_display,
	  common_battle_on_player_down,
      common_battle_inventory,

      #AI Tiggers
      (0, 0, ti_once, [(eq, "$tld_option_formations", 0),(store_mission_timer_a,":mission_time"),(ge,":mission_time",2)],
       [(call_script, "script_select_battle_tactic"),
        (call_script, "script_battle_tactic_init")]),

#MV: commented out - why do this?? and key_u is "undo formation"
      #TLD horn blowing begin (Kolba)
      # (0, 0, ti_once, [(key_clicked, key_u)], [(play_sound, "snd_evil_horn")]),
      #TLD horn blowing end (Kolba)
      
      (5, 0, 0, [(eq, "$tld_option_formations", 0),(store_mission_timer_a,":mission_time"),(ge,":mission_time",3),(call_script, "script_battle_tactic_apply")], []),

      common_battle_order_panel,
      common_battle_order_panel_tick,
    ],
  ),

  #TLD - assasins attack begin (Kolba)
  ( "assasins_attack",mtf_battle_mode,-1,
	"assasins",
	[(0,mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
	 (1,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	],
        tld_common_battle_scripts+[
		common_music_situation_update,
		common_battle_check_friendly_kills,
		common_battle_victory_display,
		common_battle_inventory,
			
		#if we are going to escape
		(ti_question_answered,0,0,[],[
			(store_trigger_param_1,":answer"),
			(eq,":answer",0),
			(assign,"$g_battle_result",-1),
			(jump_to_menu,"mnu_assasins_attack_player_retreat"),#jump to retreat menu
			(finish_mission,0),
		]),

		#if player dies
		(1,4,ti_once,[(main_hero_fallen)],[
			(assign,"$pin_player_fallen",1),
			(assign,"$g_battle_result",-1),
			(set_mission_result,-1),
			(jump_to_menu,"mnu_assasins_attack_player_defeated"),#jump to defeat menu
			(finish_mission,0),
		]),
		
		(ti_tab_pressed,0,0,[],[
			(try_begin),#If the battle is won, missions ends.
				(eq,"$battle_won",1),
				(jump_to_menu,"mnu_assasins_attack_player_won"),#jump to menu, where player gets message and prize
				(finish_mission,0),
			(else_try),#check if there are enemies nearby
				(call_script, "script_cf_check_enemies_nearby"),
				(question_box,"str_do_you_want_to_retreat"),
			(try_end),
    ]),

		#Victory conditions
		#checking victory conditions (here it's set to 60 secunds)
		(1,60,ti_once,[
			(store_mission_timer_a,reg1),
			(ge,reg1,10),
			(all_enemies_defeated,5),
			(neg|main_hero_fallen,0),
			#if enemies are defeated and player survives, we continue
			(set_mission_result,1),
			(display_message,"str_msg_battle_won"),
			(assign,"$battle_won",1),
			(assign,"$g_battle_result",1),
			(call_script,"script_play_victorious_sound"),
		],
		[	(jump_to_menu,"mnu_assasins_attack_player_won"),#jump to menu, where player gets message and prize
			(finish_mission,1),
		]),
	],
),
#Kolba end

  ( "visit_town_castle",0,-1,
    "You enter the halls of the lord.",
    [(0,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons|af_override_head,0,1,[]),
     (1,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),(2,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),(3,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]), (4,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]), #for doors
     (5,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(6,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(7,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (8,mtef_visitor_source,af_override_horse,0,1,[]),(9,mtef_visitor_source,af_override_horse,0,1,[]),(10,mtef_scene_source,af_override_horse,0,1,[]),(11,mtef_scene_source,af_override_horse,0,1,[]),
     (12,mtef_visitor_source,af_override_horse,0,1,[]),(13,mtef_visitor_source,0,0,1,[]),(14,mtef_visitor_source,0,0,1,[]),(15,mtef_visitor_source,0,0,1,[]),
     (16,mtef_visitor_source,af_castle_warlord,0,1,[]),(17,mtef_visitor_source,af_castle_warlord,0,1,[]),(18,mtef_visitor_source,af_castle_warlord,0,1,[]),(19,mtef_visitor_source,af_castle_warlord,0,1,[]),(20,mtef_visitor_source,af_castle_warlord,0,1,[]),(21,mtef_visitor_source,af_castle_warlord,0,1,[]),(22,mtef_visitor_source,af_castle_warlord,0,1,[]),(23,mtef_visitor_source,af_castle_warlord,0,1,[]),(24,mtef_visitor_source,af_castle_warlord,0,1,[]),
     (25,mtef_visitor_source,af_castle_warlord,0,1,[]),(26,mtef_visitor_source,af_castle_warlord,0,1,[]),(27,mtef_visitor_source,af_castle_warlord,0,1,[]),(28,mtef_visitor_source,af_castle_warlord,0,1,[]),(29,mtef_visitor_source,af_castle_warlord,0,1,[]),(30,mtef_visitor_source,af_castle_warlord,0,1,[]),(31,mtef_visitor_source,af_castle_warlord,0,1,[])
     ],
    tld_common_peacetime_scripts + [
      (ti_on_agent_spawn       , 0, 0, [],[ (store_trigger_param_1, ":agent_no"),(call_script, "script_init_town_agent", ":agent_no")]),
      (ti_before_mission_start , 0, 0, [],[(call_script, "script_change_banners_and_chest"),]),
      (ti_inventory_key_pressed, 0, 0, [(set_trigger_result,1)], []),
      (ti_tab_pressed          , 0, 0, [(set_trigger_result,1)], []),
	  
      (0, 0, ti_once, [], [
        #(set_fog_distance, 150, 0xFF736252)
        (try_begin),
          (eq, "$talk_context", tc_court_talk),
#          (call_script, "script_music_set_situation_with_culture", mtf_sit_lords_hall),
        (else_try),
          (call_script, "script_music_set_situation_with_culture", 0), #prison
        (try_end),
        ]),	  
    ],
),
  
( "village_attack_bandits",mtf_battle_mode,charge,
  "You lead your men to battle.",
[    (3,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     (1,mtef_team_0|mtef_use_exact_number,0,aif_start_alarmed, 7,[]),
     (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
     ],
    tld_common_battle_scripts+[
      common_battle_tab_press,

      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (assign, "$pin_player_fallen", 0),
        (str_store_string, s5, "str_retreat"),
        (call_script, "script_simulate_retreat", 10, 20),
        (assign, "$g_battle_result", -1),
        (call_script, "script_count_mission_casualties_from_agents"),
        (finish_mission,0),]),

      (0, 0, ti_once, [], [(assign, "$battle_won", 0),
                           (assign, "$defender_reinforcement_stage", 0),
                           (assign, "$attacker_reinforcement_stage", 0),
                           (assign, "$g_presentation_battle_active", 0),
                           (try_begin),
                             (eq, "$g_mt_mode", vba_after_training),
                             (add_reinforcements_to_entry, 1, 6),
                           (else_try),
                             (add_reinforcements_to_entry, 1, 29),
                           (try_end),
                           (call_script, "script_combat_music_set_situation_with_culture"),
                           ]),

      common_music_situation_update,
      common_battle_check_friendly_kills,
      common_battle_check_victory_condition,
      common_battle_victory_display,

      (1, 4, ti_once, [(main_hero_fallen)],
          [
              (assign, "$pin_player_fallen", 1),
              (str_store_string, s5, "str_retreat"),
              (call_script, "script_simulate_retreat", 10, 20),
              (assign, "$g_battle_result", -1),
              (set_mission_result, -1),
              (call_script, "script_count_mission_casualties_from_agents"),
              (finish_mission, 0)]),

      common_battle_inventory,      
      common_battle_order_panel,
      common_battle_order_panel_tick,
    ],
),

( "castle_attack_walls_defenders_sally",mtf_battle_mode,-1,
  "You attack the walls of the castle...",
    [
     (0,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,12,[]),
     (0,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,0,[]),
     (3,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,12,[]),
     (3,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,0,[]),
     ],
    formations_triggers + AI_triggers +
    common_deathcam_triggers+
    tld_siege_battle_scripts+[
      
      (ti_before_mission_start, 0, 0, [],
       [ (team_set_relation, 0, 2, 1),
         (team_set_relation, 1, 3, 1),
         (call_script, "script_change_banners_and_chest"),
         (call_script, "script_remove_siege_objects"),
         ]),

      common_battle_tab_press,

      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (assign, "$pin_player_fallen", 0),
        (str_store_string, s5, "str_retreat"),
        (call_script, "script_simulate_retreat", 5, 20),
        (call_script, "script_count_mission_casualties_from_agents"),
        (finish_mission,0),]),
        
      (0, 0, ti_once, [], [(assign,"$battle_won",0),
                           (assign,"$g_presentation_battle_active", 0),
                           (call_script, "script_combat_music_set_situation_with_culture"),
                           ]),
      
      common_music_situation_update,
      common_battle_check_friendly_kills,

      (1, 60, ti_once, [(store_mission_timer_a, reg(1)),
                        (ge, reg(1), 10),
                        (all_enemies_defeated, 2),
                        (neg|main_hero_fallen,0),
                        (set_mission_result,1),
                        (display_message,"str_msg_battle_won"),
                        (assign, "$battle_won", 1),
                        (assign, "$g_battle_result", 1),
                        (assign, "$g_siege_sallied_out_once", 1),
                        (assign, "$g_siege_method", 1), #reset siege timer
                        (call_script, "script_play_victorious_sound"),
                        ],
           [(call_script, "script_count_mission_casualties_from_agents"),
            (finish_mission,1)]),

      common_battle_victory_display,
	  common_battle_on_player_down,
      common_battle_order_panel,
      common_battle_order_panel_tick,
      common_battle_inventory,
    ],
),

( "castle_attack_walls_ladder",mtf_battle_mode,-1,
  "You attack the walls of the castle...",
    [# Attacker initial spawn point (was 0)
     (47,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,12,[]),
     # Initial defender spawn point (was 11)
     (40,mtef_defenders|mtef_team_0|mtef_infantry_first,af_override_horse,aif_start_alarmed,12,[]),
     # Defender choke points (was 10)
     (41,mtef_defenders|mtef_team_0|mtef_infantry_first,af_override_horse,aif_start_alarmed,0,[]), # team left flank
     (42,mtef_defenders|mtef_team_0|mtef_infantry_first,af_override_horse,aif_start_alarmed,0,[]), # team center
     (43,mtef_defenders|mtef_team_0|mtef_infantry_first,af_override_horse,aif_start_alarmed,0,[]), # team right flank
     # Defender reinforcements (was 15)
     (44,mtef_defenders|mtef_team_0|mtef_infantry_first,af_override_horse,aif_start_alarmed,6,[]), #entry 5 for add_reinforcements_to_entry
     (45,mtef_defenders|mtef_team_0|mtef_infantry_first,af_override_horse,aif_start_alarmed,6,[]),
     (46,mtef_defenders|mtef_team_0|mtef_infantry_first,af_override_horse,aif_start_alarmed,6,[]),
     # Attacker reinforcements (was 0)
     (47,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,6,[]), #entry 8 for add_reinforcements_to_entry
     (48,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,6,[]),
     (49,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,6,[]),
     # defender archer target positions (was 40-43)
     (50,mtef_defenders|mtef_team_0|mtef_archers_first|mtef_use_exact_number,af_override_horse,aif_start_alarmed,2,[]), # team left flank
     (51,mtef_defenders|mtef_team_0|mtef_archers_first|mtef_use_exact_number,af_override_horse,aif_start_alarmed,2,[]),
     (52,mtef_defenders|mtef_team_0|mtef_archers_first|mtef_use_exact_number,af_override_horse,aif_start_alarmed,2,[]),
	 (53,mtef_defenders|mtef_team_0|mtef_archers_first|mtef_use_exact_number,af_override_horse,aif_start_alarmed,2,[]),
	 (54,mtef_defenders|mtef_team_0|mtef_archers_first|mtef_use_exact_number,af_override_horse,aif_start_alarmed,3,[]), # team center
     (55,mtef_defenders|mtef_team_0|mtef_archers_first|mtef_use_exact_number,af_override_horse,aif_start_alarmed,3,[]),
     (56,mtef_defenders|mtef_team_0|mtef_archers_first|mtef_use_exact_number,af_override_horse,aif_start_alarmed,2,[]), # team right flank
	 (57,mtef_defenders|mtef_team_0|mtef_archers_first|mtef_use_exact_number,af_override_horse,aif_start_alarmed,2,[]),
     (58,mtef_defenders|mtef_team_0|mtef_archers_first|mtef_use_exact_number,af_override_horse,aif_start_alarmed,2,[]),
     (59,mtef_defenders|mtef_team_0|mtef_archers_first|mtef_use_exact_number,af_override_horse,aif_start_alarmed,2,[]),
	 # attacker archer target positions
     (60,0,0,0,0,[]), 
     (61,0,0,0,0,[]),
     (62,0,0,0,0,[]),
	],
    common_deathcam_triggers+
    tld_siege_battle_scripts+[

 (ti_before_mission_start, 0, 0, [],
  [ (team_set_relation, 0, 2, 1),(team_set_relation, 0, 4, 1),(team_set_relation, 4, 2, 1), # TLD expand teams
    (team_set_relation, 1, 3, 1),(team_set_relation, 1, 5, 1),(team_set_relation, 5, 3, 1),
	(team_set_relation, 6, 0, 1),(team_set_relation, 6, 2, 1),(team_set_relation, 6, 4, 1), # TLD gate aggravator team
	(assign, "$gate_aggravator_agent",-1), # can be reassigned by destructible gate scene prop presence
    (call_script, "script_change_banners_and_chest"),
    ]),
	
     common_battle_tab_press,
  
 (ti_question_answered, 0, 0, [],
   [ (store_trigger_param_1,":answer"),
     (eq,":answer",0),
     (assign, "$pin_player_fallen", 0),
     (get_player_agent_no, ":player_agent"),
     (agent_get_team, ":agent_team", ":player_agent"),
     (try_begin),
       (neq, "$attacker_team", ":agent_team"),
       (neq, "$attacker_team_2", ":agent_team"),
       (neq, "$attacker_team_3", ":agent_team"), # TLD
	   (str_store_string, s5, "str_siege_continues"),
       (call_script, "script_simulate_retreat", 8, 15),
     (else_try),
       (str_store_string, s5, "str_retreat"),
       (call_script, "script_simulate_retreat", 5, 20),
     (try_end),
     (call_script, "script_count_mission_casualties_from_agents"),
     (finish_mission,0),
   ]),
 
 (0, 0, ti_once, [],
   [(assign,"$battle_won",0),
    (assign,"$defender_reinforcement_stage",0),
    (assign,"$attacker_reinforcement_stage",0),
    (assign,"$g_presentation_battle_active", 0),
	(assign,"$telling_counter",0),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_siege),
 
    (assign, "$defender_team"  , 0),(assign, "$attacker_team"  , 1),
    (assign, "$defender_team_2", 2),(assign, "$attacker_team_2", 3),
	(assign, "$defender_team_3", 4),(assign, "$attacker_team_3", 5),
  ]),
  
 (5, 0, 0, [(lt,"$telling_counter",3)],[ # need to repeat orders several times for the bitches to listen
    (val_add, "$telling_counter",1),
	(set_show_messages, 0),
    (entry_point_get_position, pos10, 41), #TLD, was 10
    (team_give_order, "$defender_team", grc_infantry, mordr_hold),
    (team_give_order, "$defender_team", grc_infantry, mordr_stand_closer),
    (team_give_order, "$defender_team", grc_infantry, mordr_stand_closer),
    (team_give_order, "$defender_team", grc_archers, mordr_stand_ground),
    (team_set_order_position, "$defender_team", grc_infantry, pos10),
	(team_set_order_position, "$attacker_team", grc_everyone, pos10),
    (entry_point_get_position, pos10, 60), #TLD, was 10
	(team_give_order, "$attacker_team", grc_archers, mordr_stand_ground),
	(team_set_order_position, "$attacker_team", grc_archers, pos10),
    
	(entry_point_get_position, pos11, 42), #TLD
    (team_give_order, "$defender_team_2", grc_infantry, mordr_hold),
    (team_give_order, "$defender_team_2", grc_infantry, mordr_stand_closer),
    (team_give_order, "$defender_team_2", grc_infantry, mordr_stand_closer),
    (team_give_order, "$defender_team_2", grc_archers, mordr_stand_ground),
    (team_set_order_position, "$defender_team_2", grc_infantry, pos11),
	(team_set_order_position, "$attacker_team_2", grc_everyone, pos11),
	(entry_point_get_position, pos11, 61), #TLD, was 10
	(team_give_order, "$attacker_team_2", grc_archers, mordr_stand_ground),
	(team_set_order_position, "$attacker_team_2", grc_archers, pos11),

    (entry_point_get_position, pos12, 43), #TLD
    (team_give_order, "$defender_team_3", grc_infantry, mordr_hold),
    (team_give_order, "$defender_team_3", grc_infantry, mordr_stand_closer),
    (team_give_order, "$defender_team_3", grc_infantry, mordr_stand_closer),
    (team_give_order, "$defender_team_3", grc_archers, mordr_stand_ground),
    (team_set_order_position, "$defender_team_3", grc_infantry, pos12),
	(team_set_order_position, "$attacker_team_3", grc_everyone, pos12),
	(entry_point_get_position, pos12, 62), #TLD, was 10
	(team_give_order, "$attacker_team_3", grc_archers, mordr_stand_ground),
	(team_set_order_position, "$attacker_team_3", grc_archers, pos12),
    (set_show_messages, 1),
	# put gate aggravator in place
	# (entry_point_get_position, pos13, 39),
	# (agent_set_scripted_destination,"$gate_aggravator_agent",pos13,1),
	# (agent_set_position,"$gate_aggravator_agent",pos13),
  ]),
  
  (0, 0, 2,[(this_or_next|game_key_clicked, key_o),(game_key_is_down, key_o)],
   [(entry_point_get_position, pos10, 42),(team_set_order_position, "$defender_team"  , grc_everyone, pos10),
	(entry_point_get_position, pos10, 42),(team_set_order_position, "$defender_team_2", grc_everyone, pos10),
    (entry_point_get_position, pos10, 43),(team_set_order_position, "$defender_team_3", grc_everyone, pos10),
	(display_message,"@On your positions, bitches!!"),
  ]),
	
  (0, 2, ti_once, [], [(try_for_agents, ":agent_no"),(agent_set_slot, ":agent_no", slot_agent_is_not_reinforcement, 1),(try_end)]),

  (3, 0, 5, [],
    [(lt, "$defender_reinforcement_stage", 15),
     (store_mission_timer_a,":mission_time"),
     (ge,":mission_time",10),
		(try_begin),
		   (store_normalized_team_count,":num_defenders",0),
		   (lt,":num_defenders",10),
		   (add_reinforcements_to_entry, 5, 7), #TLD, was 4, 7
		   (val_add,"$defender_reinforcement_stage",1),
		(try_end),
		(try_begin),
		   (store_normalized_team_count,":num_defenders",2),
		   (lt,":num_defenders",10),
		   (add_reinforcements_to_entry, 6, 7), #TLD, was 4, 7
		   (val_add,"$defender_reinforcement_stage",1),
		(try_end),
		(try_begin),
		   (store_normalized_team_count,":num_defenders",4),
		   (lt,":num_defenders",10),
		   (add_reinforcements_to_entry, 7, 7), #TLD, was 4, 7
		   (val_add,"$defender_reinforcement_stage",1),
		(try_end),
		(try_begin),
		 (ge, "$defender_reinforcement_stage", 5),
			(set_show_messages, 0),
			(team_give_order, "$defender_team"  , grc_infantry, mordr_charge), #AI desperate charge:infantry!!!
			(team_give_order, "$defender_team_2", grc_infantry, mordr_charge),
			(team_give_order, "$defender_team_3", grc_infantry, mordr_charge),
			(set_show_messages, 1),
			(display_message,"@Defenders: infantry CHARGE!!"),
			(ge, "$defender_reinforcement_stage", 14),
				(set_show_messages, 0),
				(team_give_order, "$defender_team"  , grc_everyone, mordr_charge), #AI desperate charge: everyone!!!
				(team_give_order, "$defender_team_2", grc_everyone, mordr_charge),
				(team_give_order, "$defender_team_3", grc_everyone, mordr_charge),
				(set_show_messages, 1),
				(display_message,"@Defenders: everyone CHARGE!!"),
	   (try_end),
	
	# put gate aggravator in place
	(try_begin),
		(neq, "$gate_aggravator_agent",-1),
		(eq, "$gate_breached",0),
		(entry_point_get_position, pos13, 39),
		(agent_set_scripted_destination,"$gate_aggravator_agent",pos13,1),
		(agent_set_position,"$gate_aggravator_agent",pos13),
		(agent_set_hit_points,"$gate_aggravator_agent",100,0),
	(try_end),
   ]),
   (2, 0, 0,[(gt, "$defender_reinforcement_stage", 0)],[(call_script, "script_siege_move_archers_to_archer_positions")]),

 (1, 0, 5,
   [(lt,"$attacker_reinforcement_stage",15),
#    (store_mission_timer_a,":mission_time"),(ge,":mission_time",10),
    (store_normalized_team_count,":num_attackers",1),(lt,":num_attackers",6)],
   [(add_reinforcements_to_entry, 8, 8),(val_add,"$attacker_reinforcement_stage", 1)]),
 (1, 0, 5,
   [(lt,"$attacker_reinforcement_stage",15),
#    (store_mission_timer_a,":mission_time"),(ge,":mission_time",10),
    (store_normalized_team_count,":num_attackers",3),(lt,":num_attackers",6)],
   [(add_reinforcements_to_entry, 9, 8),(val_add,"$attacker_reinforcement_stage", 1)]),
 (1, 0, 5,
   [(lt,"$attacker_reinforcement_stage",15),
#    (store_mission_timer_a,":mission_time"),(ge,":mission_time",10),
    (store_normalized_team_count,":num_attackers",5),(lt,":num_attackers",6)],
   [(add_reinforcements_to_entry,10, 8),(val_add,"$attacker_reinforcement_stage", 1)]),

 # (5, 0, 0, [], #Make sure attackers do not stall on the ladders...
   # [(try_for_agents, ":agent_no"),  
      # (agent_is_human, ":agent_no"),
      # (agent_is_alive, ":agent_no"),
      # (agent_get_team, ":agent_team", ":agent_no"),
      # (this_or_next|eq, ":agent_team", "$attacker_team"),(this_or_next|eq, ":agent_team", "$attacker_team_2"),(eq, ":agent_team", "$attacker_team_3"),
      # (agent_ai_set_always_attack_in_melee, ":agent_no", 1),
    # (try_end),
   # ]),
      common_battle_check_friendly_kills,
      common_battle_check_victory_condition,
      common_battle_victory_display,
      common_siege_refill_ammo,
      common_siege_check_defeat_condition,
      common_battle_order_panel,
      common_battle_order_panel_tick,
      common_inventory_not_available,
   
 (5, 0, 0,[], # distribute agents among teams
   [(try_for_agents, ":agent"),
		(agent_is_alive,":agent"),
		(agent_is_human,":agent"),
		(agent_slot_eq,":agent",slot_agent_arena_team_set,0),
		(store_random_in_range, ":team", 0,3),
		(try_begin), # when gate breached assign more people to medium team (which is gate oriented)
			(eq,"$gate_breached",1),
			(store_random_in_range, ":x",0,2),
			(eq, ":x",1),
			(assign, ":team", 1),
		(try_end),
		(val_mul, ":team", 2),
		(try_begin),
			(neg|agent_is_defender,":agent"),
			(val_add,":team",1),
		(try_end),
		(agent_set_team, ":agent", ":team"),
		(agent_set_slot,":agent",slot_agent_arena_team_set,1),
	(try_end),
	]),

 (20, 0, 0,[], # report attackers and defenders distribution
   [(assign,reg0,0),(assign,reg1,0),(assign,reg2,0),(assign,reg3,0),(assign,reg4,0),(assign,reg5,0),
	(try_for_agents, ":agent"),
		(agent_is_alive,":agent"),
		(agent_is_human,":agent"),
		(agent_get_team, ":team", ":agent"),
		(try_begin),(eq,":team",0),(val_add, reg0,1),
		 (else_try),(eq,":team",1),(val_add, reg1,1),
		 (else_try),(eq,":team",2),(val_add, reg2,1),
		 (else_try),(eq,":team",3),(val_add, reg3,1),
		 (else_try),(eq,":team",4),(val_add, reg4,1),
		 (else_try),(eq,":team",5),(val_add, reg5,1),
		(try_end),
	(try_end),
	(set_show_messages, 1),
	(display_message, "@Attackers:{reg1}/{reg3}/{reg5} Defenders:{reg0}/{reg2}/{reg4}")]),
##      (15, 0, 0,
##       [
##         (get_player_agent_no, ":player_agent"),
##         (agent_get_team, ":agent_team", ":player_agent"),
##         (neq, "$attacker_team", ":agent_team"),
##         (assign, ":non_ranged", 0),
##         (assign, ":ranged", 0),
##         (assign, ":ranged_pos_x", 0),
##         (assign, ":ranged_pos_y", 0),
##         (set_fixed_point_multiplier, 100),
##         (try_for_agents, ":agent_no"),
##           (eq, ":non_ranged", 0),
##           (agent_is_human, ":agent_no"),
##           (agent_is_alive, ":agent_no"),
##           (neg|agent_is_defender, ":agent_no"),
##           (agent_get_class, ":agent_class", ":agent_no"),
##           (try_begin),
##             (neq, ":agent_class", grc_archers),
##             (val_add, ":non_ranged", 1),
##           (else_try),
##             (val_add, ":ranged", 1),
##             (agent_get_position, pos0, ":agent_no"),
##             (position_get_x, ":pos_x", pos0),
##             (position_get_y, ":pos_y", pos0),
##             (val_add, ":ranged_pos_x", ":pos_x"),
##             (val_add, ":ranged_pos_y", ":pos_y"),
##           (try_end),
##         (try_end),
##         (try_begin),
##           (eq, ":non_ranged", 0),
##           (gt, ":ranged", 0),
##           (val_div, ":ranged_pos_x", ":ranged"),
##           (val_div, ":ranged_pos_y", ":ranged"),
##           (entry_point_get_position, pos0, 10),
##           (init_position, pos1),
##           (position_set_x, pos1, ":ranged_pos_x"),
##           (position_set_y, pos1, ":ranged_pos_y"),
##           (position_get_z, ":pos_z", pos0),
##           (position_set_z, pos1, ":pos_z"),
##           (get_distance_between_positions, ":dist", pos0, pos1),
##           (gt, ":dist", 1000), #average position of archers is more than 10 meters far from entry point 10
##           (team_give_order, "$attacker_team", grc_archers, mordr_hold),
##           (team_set_order_position, "$attacker_team", grc_archers, pos0),
##         (else_try),
##           (team_give_order, "$attacker_team", grc_everyone, mordr_charge),
##         (try_end),
##         ],
##       []),
    ],
),
  
( "training_ground_training", mtf_arena_fight, -1,
    "Training.",
    [ (0,mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (1,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (2,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (3,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      # Player
      (4,mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[]),
      # Opponents
      (5,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (6,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (7,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (8,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      # Spares
      (9,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (10,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (11,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      # Player team
      (12,mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[]), #player
      (13,mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (14,mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (15,mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      # Enemy team
      (16,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (17,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (18,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (19,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (20,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (21,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (22,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (23,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (24,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (25,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (26,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (27,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
    ],
    [ (0, 0, ti_once, [], [(eq, "$g_tld_training_mode", abm_gauntlet),(start_presentation, "prsnt_gauntlet")]),
      (0, 0, ti_once, [], [#(play_sound, "snd_arena_ambiance", sf_looping),
							(call_script, "script_music_set_situation_with_culture", mtf_sit_arena)]),
      
      # terrible workaround for the buggy? add_visitors_to_current_scene
      (0.2, 0, 0, [(eq, "$g_tld_training_mode", abm_gauntlet)],
      [
         (store_add, ":enemies", "$g_tld_training_wave", 2),
         (assign, ":alive_enemies", 0),
         (try_for_agents, ":agent_no"), # count enemy agents spawned
           (agent_is_alive, ":agent_no"),
           (agent_is_human, ":agent_no"),
           (agent_get_team, ":team_no", ":agent_no"),
           (eq, ":team_no", 1),
           (val_add, ":alive_enemies", 1),
         (try_end),
# (assign, reg1, ":enemies"),
# (assign, reg2, ":alive_enemies"),
# (display_message, "@Spawned/alive: {reg1}/{reg2}."),
         (store_sub, ":enemies_to_kill", ":alive_enemies", ":enemies"), # the number of extra enemies to eliminate
	     (set_show_messages, 0),
         (init_position, pos1),
         (try_for_agents, ":agent_no"), #kill the first ":enemies_to_kill" enemy agents
           (gt, ":enemies_to_kill", 0),
           (agent_is_alive, ":agent_no"),
           (agent_is_human, ":agent_no"),
           (agent_get_team, ":team_no", ":agent_no"),
           (eq, ":team_no", 1),
           # suicide
		   (agent_get_horse, ":horse", ":agent_no"),
		   (try_begin),
             (gt, ":horse", -1), 
             (agent_set_hit_points, ":horse", 0, 1),
	         (agent_deliver_damage_to_agent, ":agent_no", ":horse"),
             (agent_set_position, ":horse", pos1),
		   (try_end),
           (agent_set_hit_points, ":agent_no", 0, 1),
	       (agent_deliver_damage_to_agent, ":agent_no", ":agent_no"),
           (agent_set_position, ":agent_no", pos1),
           (val_sub, ":enemies_to_kill", 1),
         (try_end),
	     (set_show_messages, 1),
      ]),
      
      # spawn next wave of enemies
      (1, 0, 0,
       [
         (eq, "$g_tld_training_mode", abm_gauntlet),
         (neg|main_hero_fallen),
         (num_active_teams_le, 1)
         ],
       [
         (store_add, ":enemies", "$g_tld_training_wave", 3),
         (assign, ":enemy_entry_point", 16), #first entry point
         (assign, ":spawnings", ":enemies"),
         (val_min, ":spawnings", 12), #total entry points
         
         (store_div, ":to_spawn", ":enemies", ":spawnings"), #1 or more
         (store_add, ":to_spawn_plus_one", ":to_spawn", 1), #2 or more
         (store_mod, ":one_extra", ":enemies", ":spawnings"), #0-11
# (assign, reg1, ":enemies"),
# (assign, reg2, ":spawnings"),
# (assign, reg3, ":to_spawn"),
# (assign, reg4, ":one_extra"),
# (display_message, "@Enemies {reg1}. Spawnings {reg2}. To spawn {reg3}. One extra {reg4}."),

         (store_character_level, ":player_level_bias", "trp_player"),
         (val_clamp, ":player_level_bias", 1, 30), #1-29
         (val_sub, ":player_level_bias", 15), #-14..+14
         (try_for_range, ":spawn_number", 0, ":spawnings"),
           (store_random_in_range, ":random_no", 0, 100),
           (val_add, ":random_no", ":player_level_bias"), #-14..+113
           (try_begin),
             (lt, ":random_no", 20),
             (faction_get_slot, ":opponent", "$g_encountered_party_faction", slot_faction_tier_1_troop),
           (else_try),
             (lt, ":random_no", 40),
             (faction_get_slot, ":opponent", "$g_encountered_party_faction", slot_faction_tier_2_troop),
           (else_try),
             (lt, ":random_no", 60),
             (faction_get_slot, ":opponent", "$g_encountered_party_faction", slot_faction_tier_3_troop),
           (else_try),
             (lt, ":random_no", 80),
             (faction_get_slot, ":opponent", "$g_encountered_party_faction", slot_faction_tier_4_troop),
           (else_try),
             (faction_get_slot, ":opponent", "$g_encountered_party_faction", slot_faction_tier_5_troop),
           (try_end),
           
           (try_begin),
             (lt, ":spawn_number", ":one_extra"),
             (add_visitors_to_current_scene, ":enemy_entry_point", ":opponent", ":to_spawn_plus_one"),
# (assign, reg1, ":enemy_entry_point"),
# (assign, reg2, ":to_spawn_plus_one"),
# (display_message, "@Entry {reg1}: {reg2}."),
           (else_try),
             (add_visitors_to_current_scene, ":enemy_entry_point", ":opponent", ":to_spawn"),
# (assign, reg1, ":enemy_entry_point"),
# (assign, reg2, ":to_spawn"),
# (display_message, "@Entry {reg1}: {reg2}."),
           (try_end),
           (val_add, ":enemy_entry_point", 1),
         (try_end),
         (val_add, "$g_tld_training_wave", 1),
         (assign, reg1, "$g_tld_training_wave"),
         (display_message, "@Reached Gauntlet wave {reg1}!", 0x30FFC8),
         ]),
      
      # finish mission
      (1, 3, ti_once,
       [ (assign, ":gauntlet_finished", 0),
         (try_begin),
           (eq, "$g_tld_training_mode", abm_gauntlet),
           (main_hero_fallen),
           (assign, ":gauntlet_finished", 1),
         (try_end),
         (assign, ":one_team_left", 0),
         (try_begin),
           (neq, "$g_tld_training_mode", abm_gauntlet),
           (num_active_teams_le, 1),
           (assign, ":one_team_left", 1),
         (try_end),
         (this_or_next|eq, ":gauntlet_finished", 1),
         (this_or_next|main_hero_fallen),
         (eq, ":one_team_left", 1)
         ],
       [
         (try_begin),
           (eq, "$g_tld_training_mode", abm_gauntlet),
           (troop_set_slot, "$g_talk_troop", slot_troop_trainer_training_result, "$g_tld_training_wave"),
         (else_try),
           (neg|main_hero_fallen),
           (troop_set_slot, "$g_talk_troop", slot_troop_trainer_training_result, 100),
         (else_try),
           (assign, ":alive_enemies", 0),
           (try_for_agents, ":agent_no"),
             (agent_is_alive, ":agent_no"),
             (agent_is_human, ":agent_no"),
             (agent_get_team, ":team_no", ":agent_no"),
             (eq, ":team_no", 1),
             (val_add, ":alive_enemies", 1),
           (try_end),
           (store_sub, ":dead_enemies", "$g_tld_training_opponents", ":alive_enemies"),
           (store_mul, ":training_result", ":dead_enemies", 100),
           (val_div, ":training_result", "$g_tld_training_opponents"),
           (troop_set_slot, "$g_talk_troop", slot_troop_trainer_training_result, ":training_result"),
         (try_end),
         (jump_to_menu, "mnu_auto_training_ground_trainer"),
         (finish_mission),
         ]),
    ],
),

( "training_ground_trainer_talk", 0, -1,
    "Training.",
    [ (0,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons,0,1,[]),
      (1,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons,0,1,[]),
      (2,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons,0,1,[]),
      (3,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons,0,1,[]),
      (4,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons,0,1,[]),
      (5,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons,0,1,[]),
      (6,mtef_scene_source|mtef_team_0,0,0,1,[]),
    ],
    [ (ti_before_mission_start , 0, 0,[],[(call_script, "script_change_banners_and_chest")]),
      (ti_inventory_key_pressed, 0, 0,[(set_trigger_result,1)], []),
      (ti_tab_pressed          , 0, 0,[(set_trigger_result,1)], []),
      # (0.0, 1.0, 2.0,
      # [(lt, "$trainer_help_message", 2),
        # ],
      # [(try_begin),
         # (eq, "$trainer_help_message", 0),
         # (tutorial_box, "str_trainer_help_1", "@Tutorial"),
       # (else_try),
         # (tutorial_box, "str_trainer_help_2", "@Tutorial"),
       # (try_end),
       # (val_add, "$trainer_help_message", 1),
          # ]),
    ],
),

( "arena_melee_fight",mtf_arena_fight,-1,
  "You enter a melee fight in the arena.",
    [ (0 ,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows,itm_saddle_horse]),
      (1 ,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_practice_sword]),
      (2 ,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_saddle_horse]),
      (3 ,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_arena_lance,itm_tab_shield_small_round_b,itm_saddle_horse]),
      (4 ,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows]),
      (5 ,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_tab_shield_small_round_b ]),
      (6 ,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_saddle_horse ]),
      (7 ,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_arena_lance,itm_tab_shield_small_round_b,itm_saddle_horse]),

      (8 ,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows]),
      (9 ,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_arena_lance,itm_tab_shield_small_round_b,itm_saddle_horse]),
      (10,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_sword]),
      (11,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_tab_shield_small_round_b]),
      (12,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows,itm_saddle_horse]),
      (13,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_arena_lance,itm_tab_shield_small_round_b,itm_saddle_horse]),
      (14,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_sword]),
      (15,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_tab_shield_small_round_b]),

      (16,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows,itm_saddle_horse]),
      (17,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_sword]),
      (18,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_saddle_horse]),
      (19,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_arena_lance,itm_tab_shield_small_round_b,itm_saddle_horse]),
      (20,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows]),
      (21,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_tab_shield_small_round_b ]),
      (22,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_saddle_horse ]),
      (23,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_arena_lance,itm_tab_shield_small_round_b,itm_saddle_horse]),
      (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows,itm_saddle_horse]),
      (25,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword]),
      (26,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_saddle_horse]),
      (27,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_arena_lance,itm_tab_shield_small_round_b,itm_saddle_horse]),
      (28,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows]),
      (29,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_tab_shield_small_round_b]),
      (30,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_saddle_horse]),
      (31,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_arena_lance,itm_tab_shield_small_round_b,itm_saddle_horse]),
      (32, mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_sword]),
      (33,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_staff]),
      (34,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword, itm_tab_shield_small_round_b]),
      (35,mtef_visitor_source|mtef_team_4,af_override_all,aif_start_alarmed,1,[itm_practice_staff]),
      (36, mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows]),
      (37,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_sword, itm_tab_shield_small_round_b]),
      (38,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword]),
      (39,mtef_visitor_source|mtef_team_4,af_override_all,aif_start_alarmed,1,[itm_practice_staff]),
#40-49 not used yet
      #(24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows,itm_saddle_horse]),
      #(24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword]),
      #(24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_saddle_horse]),
      #(24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_arena_lance,itm_tab_shield_small_round_b,itm_saddle_horse]),
      #(24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows]),
      #(24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_tab_shield_small_round_b]),
      #(24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_saddle_horse]),
      #(24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_arena_lance,itm_tab_shield_small_round_b,itm_saddle_horse]),
      #(24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows,itm_saddle_horse]),
      #(24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows,itm_saddle_horse]),

      (50, mtef_scene_source,af_override_horse|af_override_weapons|af_override_head,0,1,[]),
      (51, mtef_visitor_source,af_override_horse|af_override_weapons|af_override_head,0,1,[]),
      (52, mtef_scene_source,af_override_horse,0,1,[]),
#not used yet:
      (53, mtef_scene_source,af_override_horse,0,1,[]),(54, mtef_scene_source,af_override_horse,0,1,[]),(55, mtef_scene_source,af_override_horse,0,1,[]),
#used for torunament master scene

      (56, mtef_visitor_source|mtef_team_0, af_override_all, aif_start_alarmed, 1, [itm_practice_sword, itm_tab_shield_small_round_b, itm_leather_jerkin]),
      (57, mtef_visitor_source|mtef_team_0, af_override_all, aif_start_alarmed, 1, [itm_practice_sword, itm_tab_shield_small_round_b, itm_leather_jerkin]),
    ],
    tournament_triggers
),

( "arena_challenge_fight",mtf_arena_fight|mtf_commit_casualties,-1,
  "You enter a melee fight in the arena.",
    [ (56, mtef_visitor_source|mtef_team_0, 0, aif_start_alarmed, 1, []),(58, mtef_visitor_source|mtef_team_2, 0, aif_start_alarmed, 1, []),
    ],
    [ common_inventory_not_available,
      (ti_tab_pressed, 0, 0, [(display_message, "@Cannot leave now.")], []),
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),
      (0, 0, ti_once, [],[(call_script, "script_music_set_situation_with_culture", mtf_sit_arena)]),

    (1, 4, ti_once, [(this_or_next|main_hero_fallen),(num_active_teams_le,1)],
     [     (try_begin),
             (main_hero_fallen),
             # (call_script, "script_fail_quest", "qst_duel_for_lady"),
           (else_try),
             # (call_script, "script_succeed_quest", "qst_duel_for_lady"),
           (try_end),
           (finish_mission),
      ]),
    ],
),

( "tutorial_1",0,-1,
  "You enter the training ground.",
    [ (0,mtef_leader_only,af_override_horse|af_override_weapons,0,1,[itm_rohan_shield_c|itm_leather_boots,itm_black_tunic,itm_dale_sword,itm_leather_boots,itm_short_bow,itm_arrows]), #af_override_weapons
    ],
    [ (ti_tab_pressed, 0, 0, [],[	(try_begin),(lt, "$tutorial_1_state", 5),(question_box, "str_do_you_wish_to_leave_tutorial"),
									 (else_try),							 (finish_mission,0),
									(try_end)]),
      (ti_question_answered, 0, 0, [],[(store_trigger_param_1,":answer"),(eq,":answer",0),(finish_mission,0)]),
      (ti_inventory_key_pressed, 0, 0, [(display_message, "str_cant_use_inventory_tutorial")], []),
      (0, 0, ti_once, [(assign, "$tutorial_1_state", 0),
                       (assign, "$tutorial_1_msg_1_displayed", 0),
                       (assign, "$tutorial_1_msg_2_displayed", 0),
                       (assign, "$tutorial_1_msg_3_displayed", 0),
                       (assign, "$tutorial_1_msg_4_displayed", 0),
                       (assign, "$tutorial_1_msg_5_displayed", 0),
                       (assign, "$tutorial_1_msg_6_displayed", 0),
                       ], []),
	  tutorial1,
]),

( "tutorial_2",mtf_arena_fight,-1,
  "You enter the training ground.",
    [   (0,mtef_leader_only|mtef_team_0,af_override_horse|af_override_weapons,0,1,[itm_rohan_shield_b]),
        (2,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
        (4,mtef_visitor_source|mtef_team_1,0,0,1,[]),
    ],
    [ (ti_tab_pressed, 0, 0, [],[(try_begin),(lt, "$tutorial_2_state", 9),(question_box,"str_do_you_wish_to_leave_tutorial"),
        (else_try),(finish_mission,0),
        (try_end)]),
      (ti_question_answered, 0, 0, [],[(store_trigger_param_1,":answer"),(eq,":answer",0),(finish_mission,0)]),
      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_tutorial")], []),
      (0, 0, ti_once, [(store_mission_timer_a, ":cur_time"),(gt, ":cur_time", 2),(main_hero_fallen),(assign, "$tutorial_2_state", 100)], []),
      (0, 0, ti_once, [(assign, "$tutorial_2_state", 0),
                       (assign, "$tutorial_2_msg_1_displayed", 0),
                       (assign, "$tutorial_2_msg_2_displayed", 0),
                       (assign, "$tutorial_2_msg_3_displayed", 0),
                       (assign, "$tutorial_2_msg_4_displayed", 0),
                       (assign, "$tutorial_2_msg_5_displayed", 0),
                       (assign, "$tutorial_2_msg_6_displayed", 0),
                       (assign, "$tutorial_2_msg_7_displayed", 0),
                       (assign, "$tutorial_2_msg_8_displayed", 0),
                       (assign, "$tutorial_2_msg_9_displayed", 0),
                       (assign, "$tutorial_2_melee_agent_state", 0),
                       ], []),
      (10, 0, 0, [(call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_archer"),(agent_refill_ammo, reg0)], []),
	  tutorial2,
]),

( "tutorial_3",mtf_arena_fight,-1,
    "You enter the training ground.",
    [   (0,mtef_leader_only|mtef_team_0,af_override_horse|af_override_weapons,0,1,[]),
        (3,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
        (5,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [ (ti_tab_pressed, 0, 0, [],[(try_begin),(lt, "$tutorial_3_state", 12),(question_box,"str_do_you_wish_to_leave_tutorial"),
        (else_try),(finish_mission,0),
        (try_end)]),
      (ti_question_answered, 0, 0, [],[(store_trigger_param_1,":answer"),(eq,":answer",0),(finish_mission,0)]),
      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_tutorial")], []),
      (0, 0, ti_once, [(store_mission_timer_a, ":cur_time"),(gt, ":cur_time", 2),(main_hero_fallen),(assign, "$tutorial_3_state", 100)], []),
      (0, 0, ti_once, [(assign, "$tutorial_3_state", 0),
                       (assign, "$tutorial_3_msg_1_displayed", 0),
                       (assign, "$tutorial_3_msg_2_displayed", 0),
                       (assign, "$tutorial_3_msg_3_displayed", 0),
                       (assign, "$tutorial_3_msg_4_displayed", 0),
                       (assign, "$tutorial_3_msg_5_displayed", 0),
                       (assign, "$tutorial_3_msg_6_displayed", 0),
                       ], []),
	tutorial3,
]),

  ( "tutorial_3_2",mtf_arena_fight,-1,
    "You enter the training ground.",
    [   (0,mtef_leader_only|mtef_team_0,af_override_horse|af_override_weapons,0,1,[itm_practice_staff]), 
        (4,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
        (6,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [ (ti_tab_pressed, 0, 0, [],[(try_begin), (lt, "$tutorial_3_state", 5),(question_box,"str_do_you_wish_to_leave_tutorial"),
        (else_try),(finish_mission,0),
        (try_end)]),
      (ti_question_answered, 0, 0, [],[(store_trigger_param_1,":answer"),(eq,":answer",0),(finish_mission,0)]),
      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_tutorial")], []),
      (0, 0, ti_once, [(store_mission_timer_a, ":cur_time"),(gt, ":cur_time", 2),(main_hero_fallen),(assign, "$tutorial_3_state", 100)], []),
      (0, 0, ti_once, [(assign, "$tutorial_3_state", 0),
                       (assign, "$tutorial_3_msg_1_displayed", 0),
                       (assign, "$tutorial_3_msg_2_displayed", 0),
                       (assign, "$tutorial_3_msg_3_displayed", 0),
                       (assign, "$tutorial_3_msg_4_displayed", 0),
                       (assign, "$tutorial_3_msg_5_displayed", 0),
                       ], []),
	tutorial3_2,      
]),

( "tutorial_4",mtf_arena_fight,-1,
  "You enter the training ground.",
    [ (0,mtef_leader_only|mtef_team_0,af_override_horse|af_override_weapons,0,1,[itm_practice_sword,itm_practice_bow,itm_arrows]), #af_override_weapons
    ],
    [(ti_tab_pressed, 0, 0, [],[(try_begin),(lt, "$tutorial_4_state", 11),(question_box,"str_do_you_wish_to_leave_tutorial"),
        (else_try),(finish_mission,0),
        (try_end)]),
      (ti_question_answered, 0, 0, [],[(store_trigger_param_1,":answer"),(eq,":answer",0),(finish_mission,0)]),
      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_tutorial")], []),
      (0, 0, ti_once, [(assign, "$tutorial_4_state", 0),
                       (assign, "$tutorial_4_msg_1_displayed", 0),
                       (assign, "$tutorial_4_msg_2_displayed", 0),
                       (assign, "$tutorial_4_msg_3_displayed", 0),
                       (assign, "$tutorial_4_msg_4_displayed", 0),
                       (assign, "$tutorial_4_msg_5_displayed", 0),
                       (assign, "$tutorial_4_msg_6_displayed", 0),
                       (assign, "$tutorial_4_msg_7_displayed", 0),
                       ], []),
	tutorial4,
]),

( "tutorial_5",mtf_arena_fight,-1,
  "You enter the training ground.",
    [   (0,mtef_visitor_source|mtef_team_0,af_override_horse|af_override_weapons,0,1,[itm_practice_sword,itm_tab_shield_small_round_b,itm_practice_bow,itm_arrows,itm_saddle_horse]),
		(0,mtef_visitor_source|mtef_team_0,0,0,1,[]),
        (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
        (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
        (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
        (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
        (13,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(14,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
        (15,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(16,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     ],
    [(ti_tab_pressed, 0, 0, [],[(try_begin),(lt, "$tutorial_5_state", 5),(question_box,"str_do_you_wish_to_leave_tutorial"),
								(else_try),(finish_mission,0),
								(try_end)]),
      (ti_question_answered, 0, 0, [],[(store_trigger_param_1,":answer"),(eq,":answer",0),(finish_mission,0)]),
      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_tutorial")], []),
      (0, 0, ti_once, [(store_mission_timer_a, ":cur_time"),(gt, ":cur_time", 2),(main_hero_fallen),(assign, "$tutorial_5_state", 100)], []),
      (0, 0, ti_once, [(assign, "$tutorial_5_state", 0),
                       (assign, "$tutorial_5_msg_1_displayed", 0),
                       (assign, "$tutorial_5_msg_2_displayed", 0),
                       (assign, "$tutorial_5_msg_3_displayed", 0),
                       (assign, "$tutorial_5_msg_4_displayed", 0),
                       (assign, "$tutorial_5_msg_5_displayed", 0),
                       (assign, "$tutorial_5_msg_6_displayed", 0),
                       ], []),
      (0, 0, ti_once, [(set_show_messages, 0),(team_give_order, 0, grc_everyone, mordr_stand_ground),(set_show_messages, 1),
                       (store_mission_timer_a, ":cur_time"),(gt, ":cur_time", 3)], []),
      (0, 0, 0, [(call_script, "script_cf_turn_windmill_fans", 0)], []),
	tutorial5,
]),

("camera_test",0,-1,
 "camera Test.",
    [],
    [ (1, 0, 0, [(mission_cam_set_mode,1),
          (entry_point_get_position, pos3, 3),
          (mission_cam_set_position, pos3)], []),
#      (ti_before_mission_start, 0, 0, [], [(set_rain, 1,100)]),
      (ti_tab_pressed, 0, 0, [],[(finish_mission,0)]),
    ],
  ),

# ( "custom_battle_football",mtf_battle_mode,-1,
    # "The match starts in a minute!",
    # [
		# (0, mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (1, mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (2, mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (3, mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (4, mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (5, mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (6, mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a,itm_lossarnach_cloth_cap]),
		# (7, mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),

		# (16,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a,itm_lossarnach_cloth_cap]),
		# (17,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (18,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (19,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (20,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (21,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (22,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),

     # ],
    # [
      # common_custom_battle_tab_press,
      # common_custom_battle_question_answered,
      # common_inventory_not_available,
      # common_music_situation_update,
      # custom_battle_check_victory_condition,
      # common_battle_victory_display,
      # custom_battle_check_defeat_condition,

    # (0, 0, ti_once,
       # [ (assign, "$defender_team", 0),
         # (assign, "$attacker_team", 1), # (display_message,"@DEBUG: mission template football"),
#         (assign, "$defender_team_2", 3),
#         (assign, "$attacker_team_2", 2),
       # ], []),
################## FOOTBALL BEGIN ############################################
		# football_init,
		# football_kick_ball,
		# football_fly_ball,				
	# ],
# ),

( "besiege_inner_battle_castle",mtf_battle_mode,-1,
  "You attack the walls of the castle...",
    [(0 , mtef_attackers|mtef_use_exact_number|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (6 , mtef_attackers|mtef_use_exact_number|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (7 , mtef_attackers|mtef_use_exact_number|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (16, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (17, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (18, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (19, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (20, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     ],
    tld_common_battle_scripts+[
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),

      common_battle_tab_press,

      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (assign, "$pin_player_fallen", 0),
        (str_store_string, s5, "str_retreat"),
        (call_script, "script_simulate_retreat", 5, 20),
        (assign, "$g_battle_result", -1),
        (set_mission_result,-1),
        (call_script, "script_count_mission_casualties_from_agents"),
        (finish_mission,0),
        ]),
        
      (0, 0, ti_once, [], [(assign,"$battle_won",0),
                           (assign,"$g_presentation_battle_active", 0),
                           (call_script, "script_music_set_situation_with_culture", mtf_sit_ambushed),
                           ]),
      
      #AI Tiggers
      (0, 0, ti_once, [
          (assign, "$defender_team", 0),
          (assign, "$attacker_team", 1),
          (assign, "$defender_team_2", 2),
          (assign, "$attacker_team_2", 3),
          ], []),

      common_battle_check_friendly_kills,
      common_battle_check_victory_condition,
      common_battle_victory_display,
	  common_battle_on_player_down,
      common_battle_order_panel,
      common_battle_order_panel_tick,
      common_battle_inventory,
    ],
  ),

  ( "besiege_inner_battle_town_center",mtf_battle_mode,-1,
    "You attack the walls of the castle...",
    [
     (0 , mtef_attackers|mtef_use_exact_number|mtef_team_1,af_override_horse,aif_start_alarmed,4,[]),
     (2 , mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (23, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (24, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (25, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (26, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (27, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (28, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     ],
    tld_common_battle_scripts+[
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),

      common_battle_tab_press,

      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (assign, "$pin_player_fallen", 0),
        (str_store_string, s5, "str_retreat"),
        (call_script, "script_simulate_retreat", 5, 20),
        (assign, "$g_battle_result", -1),
        (set_mission_result,-1),
        (call_script, "script_count_mission_casualties_from_agents"),
        (finish_mission,0),
        ]),
        
      (0, 0, ti_once, [], [(assign,"$battle_won",0),
                           (assign,"$g_presentation_battle_active", 0),
                           (call_script, "script_music_set_situation_with_culture", mtf_sit_ambushed),
                           ]),
      
      #AI Tiggers
      (0, 0, ti_once, [
          (assign, "$defender_team", 0),
          (assign, "$attacker_team", 1),
          (assign, "$defender_team_2", 2),
          (assign, "$attacker_team_2", 3),
          ], []),

      common_battle_check_friendly_kills,
      common_battle_check_victory_condition,
      common_battle_victory_display,
	  common_battle_on_player_down,
      common_battle_order_panel,
      common_battle_order_panel_tick,
      common_battle_inventory,
    ],
  ),

  ( "sneak_caught_fight",mtf_arena_fight,-1,
    "You must fight your way out!",
    [
      (0,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,pilgrim_disguise),
      (25,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (32,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
#      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
    ],
    tld_common_battle_scripts+[
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),
      (ti_tab_pressed, 0, 0, [],
       [(question_box,"str_do_you_wish_to_surrender")]),
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),(eq,":answer",0),
	   (assign, "$recover_after_death_menu", "mnu_recover_after_death_town_alone"),
	   (jump_to_menu,"mnu_tld_player_defeated"),(finish_mission,0),]),
      
      (1, 0, ti_once, [],
       [
         (play_sound,"snd_sneak_town_halt"),
         (call_script, "script_music_set_situation_with_culture", mtf_sit_fight),
         ]),
      (0, 3, 0, [(main_hero_fallen,0)],
       [(assign, "$recover_after_death_menu", "mnu_recover_after_death_town_alone"),(jump_to_menu,"mnu_tld_player_defeated"),(finish_mission,0)]),
      (5, 1, ti_once, [(num_active_teams_le,1),(neg|main_hero_fallen)],
       [(assign,"$auto_menu",-1),(jump_to_menu,"mnu_sneak_into_town_caught_dispersed_guards"),(finish_mission,1)]),
      (ti_on_leave_area, 0, ti_once, [],
       [(assign,"$auto_menu",-1),(jump_to_menu,"mnu_sneak_into_town_caught_ran_away"),(finish_mission,0)]),

      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_arena")], []),
      
    ],
  ),

   ("ai_training",0,-1,
    "You start training.",
    [
#     (0,0,af_override_horse,aif_start_alarmed,1,[]),
     (0,0,0,aif_start_alarmed,30,[]),
#     (1,mtef_no_leader,0,0|aif_start_alarmed,5,[]),
#     (0,mtef_no_leader,0,0|aif_start_alarmed,0,[]),
#     (3,mtef_enemy_party|mtef_reverse_order,0,aif_start_alarmed,6,[]),
#     (4,mtef_enemy_party|mtef_reverse_order,0,aif_start_alarmed,0,[]),
     ],
    tld_common_battle_scripts+[
#      (ti_before_mission_start, 0, 0, [], [(set_rain, 1,100)]),
      (ti_tab_pressed, 0, 0, [],[(finish_mission,0)]),
      (0, 0, ti_once, [], [(assign,"$g_presentation_battle_active", 0),]),

      common_battle_order_panel,
      common_battle_order_panel_tick,
    ],
  ),

   ("legendary_place_visit",0,-1,
    "You visit a legendary place.",
    [
     (0,mtef_scene_source|mtef_team_0,0,0,1,[]),
     (1,mtef_scene_source|mtef_team_0,0,0,1,[]),
     (16,mtef_scene_source|mtef_team_0,0,0,1,[]),
     (17,mtef_scene_source|mtef_team_0,0,0,1,[]),
     (18,mtef_scene_source|mtef_team_0,0,0,1,[]),
     (19,mtef_scene_source|mtef_team_0,0,0,1,[]),
     ],
    [
      (ti_tab_pressed, 0, 0, [],[(finish_mission,0)]),
    ],
  ),
  
  ( "custom_battle",mtf_battle_mode,-1,
    "You lead your men to battle.",
    [
      (0 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(1 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(3 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(5 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(7 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (8 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(9 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(19,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(21,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(23,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (24,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(25,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(27,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(29,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(31,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    tld_common_battle_scripts+[
      common_custom_battle_tab_press,
      common_custom_battle_question_answered,
      common_inventory_not_available,
      
      (0, 0, ti_once, [],
        [ (assign, "$g_battle_result", 0),
          (call_script, "script_combat_music_set_situation_with_culture"),
         ]),
			
      common_music_situation_update,
      custom_battle_check_victory_condition,
      common_battle_victory_display,
      custom_battle_check_defeat_condition,

    ],
  ),

  ( "custom_battle_siege",mtf_battle_mode,-1,
    "You lead your men to battle.",
    [
      (0 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(1 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(3 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(5 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(7 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (8 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(9 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(19,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(21,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(23,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (24,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(25,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(27,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(29,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(31,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    tld_common_battle_scripts+[
      common_battle_mission_start,

      (0, 0, ti_once,
       [ (assign, "$defender_team", 0),
         (assign, "$attacker_team", 1),
         (assign, "$defender_team_2", 2),
         (assign, "$attacker_team_2", 3),
         ], []),

      common_custom_battle_tab_press,
      common_custom_battle_question_answered,
      common_inventory_not_available,
      common_custom_siege_init,
      common_music_situation_update,
      custom_battle_check_victory_condition,
      common_battle_victory_display,
      custom_battle_check_defeat_condition,
      common_siege_attacker_do_not_stall,
      common_siege_refill_ammo,
      common_siege_init_ai_and_belfry,
      common_siege_move_belfry,
      common_siege_rotate_belfry,
      common_siege_assign_men_to_belfry,
      common_siege_ai_trigger_init_2,
      ],
    ),

  ( "custom_battle_5",mtf_battle_mode,-1,
    "You lead your men to battle.",
    [
      (0 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(1 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (2 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(3 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (4 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(5 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (6 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(7 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (8 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(9 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(11,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(13,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(15,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(17,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(19,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(21,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(23,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (24,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(25,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(27,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(29,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(31,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (40,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(41,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(43,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(45,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(47,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),

     ],
    tld_common_battle_scripts+[
	  common_custom_battle_tab_press,
      common_custom_battle_question_answered,
      common_custom_siege_init,
      common_inventory_not_available,
      common_music_situation_update,
      custom_battle_check_victory_condition,
      common_battle_victory_display,
      custom_battle_check_defeat_condition,
      
      (0, 0, ti_once,
       [ (assign, "$defender_team", 1),
         (assign, "$attacker_team", 0),
         (assign, "$defender_team_2", 3),
         (assign, "$attacker_team_2", 2), #		 (display_message,"@MT gunda vs dwarves siege attack 2"),
         ], []),

      common_siege_ai_trigger_init_2,
      common_siege_attacker_do_not_stall,
      common_siege_refill_ammo,
      common_siege_init_ai_and_belfry,
      common_siege_move_belfry,
      common_siege_rotate_belfry,
      common_siege_assign_men_to_belfry,
    ],
  ),
  
########################## TLD TEMPLATES ###############################
  ( "custom_battle_HD",mtf_battle_mode,-1,
    "You wait on the walls for the incoming horde.",
    [
		(0 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(1 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
		(2 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(3 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
		(4 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(5 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
		(6 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(7 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
		(8 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(9 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
		(10,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(11,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
		(12,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(13,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
		(14,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(15,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
#		(40,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
#		(41,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
#		(42,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
#		(43,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
#		(44,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
#		(45,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
#		(46,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
#		(47,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),

		(16,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(17,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
		(18,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(19,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
		(20,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(21,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
		(22,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(23,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
		(24,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(25,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
		(26,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(27,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
		(28,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(29,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
		(30,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(31,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     ],
    tld_common_battle_scripts+[
      common_custom_battle_tab_press,
      common_custom_battle_question_answered,
      common_custom_siege_init,
      common_inventory_not_available,
      common_music_situation_update,
      custom_battle_check_victory_condition,
      common_battle_victory_display,
      custom_battle_check_defeat_condition,

	(ti_before_mission_start,0,0,[],[(set_rain,1,100)]),

    (0, 0, ti_once,
       [(assign, "$defender_team", 0),
        (assign, "$attacker_team", 1),
        (assign, "$defender_team_2", 3),
        (assign, "$attacker_team_2", 2),
        (set_fog_distance, 80, 0x010101), #		 (display_message,"@DEBUG: mission template HD"),
       ], []),

      common_siege_ai_trigger_init_2,
      common_siege_attacker_do_not_stall,
      common_siege_refill_ammo,

		ballista_init,ballista_operate,ballista_disengage,ballista_shoot,ballista_reload_pause,ballista_reload,ballista_fly_missile,ballista_toggle_fire_arrow,
		ballista_missile_illumination,ballista_camera_alignment,ballista_turn_up,ballista_turn_down,ballista_turn_left,ballista_turn_right,ballista_aim,

################## THUNDER AND LIGHTNING BEGIN ###############################
	(3, 0.2, 6, [(store_random_in_range,":rnd",1,5),(eq,":rnd",1),(set_fog_distance, 200, 0xaaaaaa),],
				[(set_fog_distance, 80, 0x010101),(play_sound,"snd_thunder"),(assign, "$lightning_cycle",1),]),
	(0.4,0.1, 6,[(eq,"$lightning_cycle",1),(set_fog_distance, 150, 0x777777),],		###### Lightning afterflashes 
				[(set_fog_distance, 80, 0x010101),(assign,"$lightning_cycle",2),]),
	(0.5,0.1, 6,[(eq,"$lightning_cycle",2),(set_fog_distance, 120, 0x555555),],
				[(set_fog_distance, 80, 0x010101),(assign,"$lightning_cycle",0),]),
################## THUNDER AND LIGHTNING END #################################
		HD_ladders_init,HD_ladders_rise,
		stonelobbing_init_stone,stonelobbing_pick_stone,stonelobbing_throw_stone,stonelobbing_fly_stone,stonelobbing_carry_stone,
    ],
  ),
	
  ( "custom_battle_dynamic_scene", mtf_battle_mode,-1,
    "You lead your men to random scenery battle!",
    [
      (0 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(1 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(3 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(5 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(7 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (8 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(9 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(19,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(21,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(23,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (24,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(25,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(27,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(29,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(31,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    tld_common_battle_scripts+
	[
    common_custom_battle_tab_press,
    common_custom_battle_question_answered,
    common_inventory_not_available,
    common_music_situation_update,
    custom_battle_check_victory_condition,
    common_battle_victory_display,
    custom_battle_check_defeat_condition,

    (0, 0, ti_once,
       [(assign, "$defender_team", 0),
        (assign, "$attacker_team", 1),
        (assign, "$defender_team_2", 3),
        (assign, "$attacker_team_2", 2), 
					#(assign,"$mask",1),
#		(display_message,"@DEBUG: mission template dynamic scene"),
       ],[]),
	   
	   horse_whistle_init,horse_whistle,
######################################## tree selection and 
		scene_set_flora_init,scene_set_flora_army_spawn,
#		custom_commander_camera,
#		scene_init_fog,scene_set_fog,
#		test_val_and,
	],
),

 (  "tld_caravan_help",mtf_battle_mode,-1,
    "You rush to help the caravan.",
    [ (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(7,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (8,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(9,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(19,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(21,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(23,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (24,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(25,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(27,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(29,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(31,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      common_custom_battle_tab_press,
      common_custom_battle_question_answered,
      common_inventory_not_available,
      common_siege_ai_trigger_init_2,
      
	  (0, 0, ti_once, [],[(assign, "$g_battle_result", 0)]),

      custom_battle_check_victory_condition,
      common_battle_victory_display,
      custom_battle_check_defeat_condition,
    ],
),

(   "tld_erebor_dungeon",0,-1,
    "Default town visit",
    [(0,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (1,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (2,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
     (3,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
     (4,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
     (5,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (6,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
	 ],
	 [
	##  (ti_tab_pressed, 0, 0, [(set_trigger_result,1)], []),
	##      (ti_inventory_key_pressed, 0, 0, [(set_trigger_result,1),], []),
	  
	##  
	##  (1, 0, ti_once, [], [(tutorial_box,"str_tld_erebor_dungeon"),]),n, 5, "$agent_no_player"),
	##            (entry_point_get_position, 2, 0),   (1, 0, 0, [],
		
	(ti_before_mission_start, 0, 0, [],[(assign, "$trap_is_active", 1),(assign, "$atak", 0),(team_set_relation, 0, 1, -1),(assign, "$dungeons_in_scene",1)]),
	dungeon_darkness_effect,


	(0, 0, 0, [(eq, "$trap_is_active", 1)],
	[
	(scene_prop_get_instance, ":instance", "spr_spear_trap_1", 0),
	(prop_instance_get_position, pos1, ":instance"),
	(get_player_agent_no, ":agent"),
	(agent_get_position, pos2, ":agent"),
	(get_distance_between_positions, ":dist", pos1, pos2),
	(le, ":dist", 200),
	(display_message, "str_tld_spear_hit", 0xFFFFAAFF),
	(position_move_z, pos1, 70),
	(prop_instance_animate_to_position, ":instance", pos1, 100),
	(store_agent_hit_points,":hp",":agent",0),
	(val_sub,":hp",20),
	(agent_set_hit_points,":agent",":hp"),
	(agent_play_sound,":agent","snd_spear_trap"),
	(agent_play_sound,":agent","snd_man_hit_pierce_strong"),
	(try_begin),
	(le, ":hp", 1),
	(agent_deliver_damage_to_agent, ":agent", ":agent"),
	(try_end),
	(assign, "$atak", 1),
	]),
	(1, 3, 0, [(eq, "$atak", 1),],
	[
	(assign, "$atak", 0),
	(scene_prop_get_instance, ":instance", "spr_spear_trap_1", 0),
	(prop_instance_get_position, pos1, ":instance"),
	(position_move_z, pos1, -70),
	(prop_instance_animate_to_position, ":instance", pos1),
	]),
]),

########################### custom battle faction troops showoff
( "custom_battle_parade",mtf_battle_mode,-1,
    "You line up your troops for the parade",
    [ (0 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(1 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (2 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(3 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (4 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(5 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (6 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(7 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (8 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(9 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(11,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(13,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(15,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (16,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(17,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(19,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(21,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(23,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (24,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(25,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(27,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(29,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),

      (30,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(31,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (32,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(33,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(35,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(37,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(39,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (40,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(41,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(43,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(45,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(47,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (48,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(49,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(51,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(53,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(55,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (56,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(57,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(59,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
     ],
    tld_common_battle_scripts+[
      common_custom_battle_tab_press,
      common_custom_battle_question_answered,
      common_inventory_not_available,
      
      (0, 0, ti_once, [],
        [ (assign, "$g_battle_result", 0),
          (assign, "$defender_team", 0),
          (assign, "$attacker_team", 1),
          (assign, "$defender_team_2", 2),
          (assign, "$attacker_team_2", 3),
		  (team_set_relation, 0, 2, 1),
		  (team_set_relation, 0, 1, -1),
          (call_script, "script_combat_music_set_situation_with_culture"),
         ]),

      (0,0,0, [	(key_clicked, key_f3)],#fight after F3 pressed
		[(display_message,"@THREE.. TWO... ONE.... FIGHT!"),
		 (try_for_agents,":agent"),
		    (agent_is_human),
			(agent_get_entry_no,":entry",":agent"),
			(try_begin),(ge,":entry",30),(agent_set_team,":agent",1),
            (else_try)                  ,(agent_set_team,":agent",0),
			(try_end),
		 (try_end),
		 (team_give_order, 0, grc_everyone, mordr_charge),
		 (team_give_order, 1, grc_everyone, mordr_charge),
		 ]),
			
      common_music_situation_update,
#      custom_battle_check_victory_condition,
      common_battle_victory_display,
      custom_battle_check_defeat_condition,
    ],
  ),
########################### end custom battle faction troops showoff

( "aw_tomb",0,-1,
    "silence...",
    [(0,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons|af_override_head,0,1,() ),],
    custom_tld_bow_always
	 +
	[
	(ti_tab_pressed, 0, 0, [], [(question_box,"@Leave the place in silence?")]),
	(ti_question_answered, 0, 0, [], [ (store_trigger_param_1,":answer"), (eq,":answer",0), (finish_mission), ]),
	(0,0,ti_once,[],[(music_set_situation, 0),]),
	],
),


( "dungeon_crawl_moria_entrance",0,-1,
    "Explore around Moria",
    [(0 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(1 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(4 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),],
    [
    (ti_tab_pressed, 0, 0, [(eq, "$player_is_inside_dungeon",0)],[(question_box,"@Leave scene?")]),
    (ti_tab_pressed, 0, 0, [(eq, "$player_is_inside_dungeon",1)],[(question_box,"@Trace back your steps and go back in the open now?")]),
	(ti_question_answered, 0, 0, [], [ (store_trigger_param_1,":answer"), (eq,":answer",0), (finish_mission), ]),
	(ti_before_mission_start, 0, 0, [], [ (assign, "$player_is_inside_dungeon",0), (assign, "$dungeons_in_scene",1)]),
	dungeon_darkness_effect,
  ],
),


# daungeon crawl
( "dungeon_crawl_moria_entrance",0,-1,
    "Explore around Moria",
    [(0 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(1 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(4 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),],
    [
    (ti_tab_pressed, 0, 0, [(eq, "$player_is_inside_dungeon",0)],[(question_box,"@Leave scene?")]),
    (ti_tab_pressed, 0, 0, [(eq, "$player_is_inside_dungeon",1)],[(question_box,"@Trace back your steps and go back in the open now?")]),
	(ti_question_answered, 0, 0, [], [ (store_trigger_param_1,":answer"), (eq,":answer",0), (finish_mission), ]),
	(ti_before_mission_start, 0, 0, [], [ (assign, "$player_is_inside_dungeon",0),(assign, "$dungeons_in_scene",1)]),
	dungeon_darkness_effect,
  ],
),

( "dungeon_crawl_moria_hall",0,-1,
    "Explore around Moria",
    [(0 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(1 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(4 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),],
    [
    (ti_tab_pressed, 0, 0, [],[(question_box,"@Trace back your steps and go back in the open now?")]),
	(ti_question_answered, 0, 0, [], [ (store_trigger_param_1,":answer"), (eq,":answer",0), (finish_mission)]),
	(ti_before_mission_start, 0, 0, [], [(assign, "$dungeons_in_scene",1)]),
	dungeon_darkness_effect,
  ],
),


( "dungeon_crawl_moria_deep",mtf_battle_mode,-1,
    "Lost in Moria! Orcs are everywhere! You must find a way out!",
    [(0 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(1 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(4 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),],
    [
    (ti_tab_pressed, 0, 0, [],[(question_box,"@There is no way out! Surrender to orcs?")]),
	(ti_question_answered, 0, 0, [], [ 
		(troop_remove_item, "trp_player","itm_book_of_moria"),(store_trigger_param_1,":answer"), (eq,":answer",0), (assign, "$recover_after_death_menu", "mnu_recover_after_death_moria"), (jump_to_menu,"mnu_tld_player_defeated"), (finish_mission), 
	]),
	(ti_before_mission_start, 0, 0, [], [ (set_fog_distance,18,0x000001),(assign, "$dungeons_in_scene",1)]),
	dungeon_darkness_effect,
  ],
),

( "scene_chooser",mtf_battle_mode,-1,
    "You go to the scene",
    [(0 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(1 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(4 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),],
    [
	(ti_tab_pressed, 0, 0, [],[(finish_mission,0)]),
	(ti_before_mission_start, 0, 0, [], [(assign, "$dungeons_in_scene",1)]),	
	dungeon_darkness_effect,
  ],
),


############ 808 stealth & rescue
( "infiltration_stealth_mission", mtf_battle_mode,  -1,
  "Default_town_visit", 
[(0,mtef_visitor_source|mtef_team_1,af_override_horse,                1,1,[]),
( 1,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),  
( 2,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),  
( 3,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),  
( 4,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),  
( 5,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),  
( 6,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
( 7,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
( 8,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
( 9,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(10,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(11,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(12,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(13,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(14,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(15,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(16,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(17,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]), 
(18,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(19,mtef_visitor_source|mtef_team_2,                0,aif_start_alarmed,1,[]), 
(20,mtef_visitor_source|mtef_team_2,                0,aif_start_alarmed,1,[]), 
],
[
(0,0,ti_once,[],[
#  (team_set_relation, 2, 1, 0),
#  (team_set_relation, 3, 1, -1),
#  (team_set_relation, 3, 2, 1),
  (call_script, "script_infiltration_mission_synch_agents_and_troops"),
#  (call_script, "script_infiltration_mission_set_hit_points"),
  (try_for_range, reg10, 1, 32),
      (entry_point_get_position, reg10, reg10),
  (try_end),
  (get_player_agent_no, "$current_player_agent"),
  (assign, "$alarm_level", 0),
]),

#(5,0,0,[],[(call_script, "script_infiltration_mission_update_companion_casualties")]),

(ti_tab_pressed,0,0,[],[(try_begin),(this_or_next|eq, "$battle_won", 1),(eq, "$battle_won", 2),(finish_mission),(try_end)]),
(ti_question_answered,0,0,[],[(store_trigger_param_1, ":local0"),(eq, ":local0", 0),(finish_mission)]),
(1,4,ti_once,[(main_hero_fallen)],[(call_script, "script_rescue_failed"),(assign, "$battle_won", 2),(set_mission_result, -1),(finish_mission)]),
(1,0,ti_once,[(eq, "$sneak_tut", 0)],[
  (tutorial_box, "@Stealth mini-game tutorial: There are two alarm levels. Level 1 is set off by the guards seeing a dead body or by them spotting you. Level 2 is set off by the guards spotting you when level 1 is already active. Level two is dangerous because guards will continue to arrive. You can avoid being spotted by staying hidden. To hid simply move behind various bits of cover."),
  (assign, "$sneak_tut", 1),
]),

(3,0,0,[],[ 
  (try_for_agents, ":enemy"),
    (agent_is_human, ":enemy"),
    (agent_is_alive, ":enemy"),
    (neg|eq, ":enemy", "$current_player_agent"),
	(store_agent_hit_points,":hp",":enemy",0),
	(try_begin),
        (eq, ":hp", 100), # healthy agents can patrol
		(agent_set_speed_limit,":enemy",4),
		(agent_get_position, pos32, ":enemy"),
		(try_for_range, "$positions", 1, 21),
			(get_distance_between_positions, "$position_distance", "$positions", pos32),
			(neg|gt, "$position_distance", 400),
			(agent_get_slot, "$last_agent_position", ":enemy", 10),
			(store_current_scene, reg45),
			(try_begin),
				(eq, reg45, "$rescue_stealth_scene_1"),
				(neg|eq, "$active_rescue", 4),
				(call_script, "script_mt_sneak_1", ":enemy"),
			(else_try),
				(eq, reg45, "$rescue_stealth_scene_2"),
				(neg|eq, "$active_rescue", 4),
				(call_script, "script_mt_sneak_2", ":enemy"),
			(else_try),
				(eq, "$active_rescue", 4),
				(call_script, "script_isen_sneak_1", ":enemy"),
			(try_end),
			(try_begin),
				(neg|gt, "$position_distance", 200),
				(agent_set_slot, ":enemy", 10, "$positions"),
			(try_end),
		(try_end),
	(else_try), # wounded agents do not patrol, bash player instead
		(agent_clear_scripted_mode,":enemy"),
		(agent_set_speed_limit,":enemy",10),
	(try_end),
(try_end),
]),

(5,0,0,[],[ 
  (agent_get_position, pos33, "$current_player_agent"),
  (try_for_range, ":entries21_32", 21, 32),
    (get_distance_between_positions, ":dist", ":entries21_32", 33),
    (neg|gt, ":dist", 150),
    (eq, "$player_hiding", 0),
    (assign, "$player_hiding", ":entries21_32"),
    (display_message, "@You_are_now_hidden."),
    # (try_begin),
        # (eq, "$hiding_tut", 0),
        # (tutorial_box, "@Stealth_mini-game_tutorial:_There_are_two_alarm_levels._Level_1_is_set_off_by_the_guards_seeing_a_dead_body_or_by_them_spotting_you._Level_2_is_set_off_by_the_guards_spotting_you_when_level_1_is_already_active._Level_two_is_dangerous_because_guards_will_continue_to_arrive._You_can_avoid_being_spotted_by_staying_hidden._To_hid_simply_move_behind_various_bits_of_cover."),
        # (assign, "$hiding_tut", 1),
    # (try_end),
  (try_end),
  (assign, reg25, 0),
  (try_for_range, ":entries21_32", 21, 32),
    (get_distance_between_positions, ":dist", ":entries21_32", pos33),
    (ge, "$player_hiding", 1),
    (ge, ":dist", 150),
    (val_add, reg25, 1),
  (try_end),
  (try_begin),
    (eq, reg25, 11),
    (display_message, "@You_move_out_of_hiding."),
    (assign, "$player_hiding", 0),
  (try_end),
]),

(3,0,0,[],[ 
  (try_for_agents, ":agent"),
    (agent_is_human, ":agent"),
    (agent_is_alive|neg, ":agent"),
    (neg|eq, ":agent", "$current_player_agent"),
    (agent_get_position, pos34, ":agent"),
    (try_for_agents, ":enemy"),
        (agent_is_human, ":enemy"),
        (agent_is_alive, ":enemy"),
        (neg|eq, ":enemy", "$current_player_agent"),
        (agent_get_position, pos32, ":enemy"),
        (get_distance_between_positions, ":dist", pos32, pos34),
        (try_begin),
            (eq, "$alarm_level", 0),
            (neg|gt, ":dist", 600),
            (assign, "$alarm_level", 1),
            (display_message, "@The_guards_have_spotted_a_dead_body!"),
            (display_message, "@Alarm_Level_is_now_at_1!", 4294945450),
            (play_sound, "snd_man_yell"),
            (reset_mission_timer_a),
        (try_end),
    (try_end),
  (try_end),
]),

(5,0,0,[(store_mission_timer_a, ":time"),(ge, ":time", 25)],[ 
  (try_begin),
    (eq, "$alarm_level", 1),
    (assign, "$alarm_level", 0),
    (display_message, "@Alarm_Level_is_now_at_0!", 4289396650),
    (reset_mission_timer_a),
  (else_try),
    (eq, "$alarm_level", 2),
    (assign, "$alarm_level", 1),
    (display_message, "@Alarm_Level_is_now_at_1!", 4289396650),
    (reset_mission_timer_a),
  (try_end),
]),

(10,0,0,[(eq, "$alarm_level", 2)],[
  (try_begin),
    (eq, "$spawn_cycle", 0),
    (set_visitor, 19, "$guard_troop2", 0),
    (set_visitor, 20, "$guard_troop3", 0),
    (assign, "$spawn_cycle", 1),
  (try_end),
  (store_random_in_range, ":rnd", 0, 2),
  (try_begin),(eq, ":rnd", 0),(eq, "$spawn_cycle", 1),(add_reinforcements_to_entry, 19, 1),
   (else_try),(eq, ":rnd", 1),(eq, "$spawn_cycle", 1),(add_reinforcements_to_entry, 20, 1),
  (try_end),
]),

(3,0,0,[],[ 
  (try_for_agents, ":agent"),
    (agent_is_human, ":agent"),
    (agent_is_alive, ":agent"),
    (neg|eq, ":agent", "$current_player_agent"),
    (agent_get_position, pos32, ":agent"),
    (agent_get_position, pos33, "$current_player_agent"),
    (get_distance_between_positions, ":dist", pos33, pos32),
    (try_begin),
        (neg|gt, ":dist", 1200),
        (neg|position_is_behind_position, pos33, pos32),
        (eq, "$player_hiding", 0),
        (try_begin),
            (eq, "$alarm_level", 0),
            (display_message, "@The_guards_have_spotted_you!"),
            (display_message, "@Alarm_Level_is_now_at_1!", 4294945450),
#            (play_sound, [opmask_sound]53, 0),
            (reset_mission_timer_a),
            (assign, "$alarm_level", 1),
            (store_random_in_range, ":rnd", 0, 11),
			(try_begin),
                (ge, ":rnd", "$meta_stealth"),
                (val_add, "$meta_alarm", 1),
            (try_end),
        (else_try),
            (eq, "$alarm_level", 1),
#			(agent_set_team  , ":agent", 3),
            (display_message, "@The_guards_have_spotted_you!"),
            (display_message, "@Alarm_Level_is_now_at_2!", 4294945450),
            (play_sound, "snd_man_yell"),
			(store_agent_hit_points, ":hp", ":agent", 1), # mark enemy as the one who spotted you (will not return to patrol)
			(val_sub,":hp",1),
			(agent_set_hit_points, ":agent", ":hp", 1),
            (reset_mission_timer_a),
            (assign, "$alarm_level", 2),
            (try_begin),
                (store_random_in_range, ":rnd", 0, 11),
                (ge, ":rnd", "$meta_stealth"),
                (val_add, "$meta_alarm", 1),
            (try_end),
            (store_random_in_range, ":rnd", 0, 2),
            (try_begin),(eq, ":rnd", 0),(set_visitor, 20, "$guard_troop2", 0),
             (else_try),                (set_visitor, 20, "$guard_troop3", 0),
            (try_end),
            (add_reinforcements_to_entry, 20, 1),
        (try_end),
    (try_end),
(try_end),
]),
  ],
),
 
( "infiltration_combat_mission",mtf_battle_mode,0,
  "You_lead_your_men_to_battle.",
[(0,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
( 1,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
( 2,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
( 3,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
( 4,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
( 5,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
( 6,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
( 7,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
( 8,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
( 9,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
(10,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(11,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(12,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(13,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(14,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(15,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(16,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(17,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(18,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(19,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(20,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(21,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(22,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(23,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(24,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(25,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(26,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(27,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(28,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(29,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(30,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
(31,mtef_visitor_source|mtef_team_2, 271,aif_start_alarmed,1,[]),
(32,mtef_visitor_source|mtef_team_2, 271,aif_start_alarmed,1,[]),
(33,mtef_visitor_source|mtef_team_2, 271,aif_start_alarmed,1,[]),
(34,mtef_visitor_source|mtef_team_2, 271,aif_start_alarmed,1,[]),
(35,mtef_visitor_source|mtef_team_2, 271,aif_start_alarmed,1,[]),
(36,mtef_visitor_source|mtef_team_2, 271,aif_start_alarmed,1,[]),
],
[
(0,0,ti_once,[],[
(call_script, "script_infiltration_mission_synch_agents_and_troops"),
(call_script, "script_infiltration_mission_set_hit_points"),
(call_script, "script_wounded_hero_cap_mission_health"),
]),

(5,0,0,[],[(call_script, "script_infiltration_mission_update_companion_casualties")]),

(1,4,ti_once,[(main_hero_fallen),],[
(call_script, "script_rescue_failed"),
(call_script, "script_infiltration_mission_update_companion_casualties"),
(set_mission_result, -1),
(finish_mission),
]),

(5,0,ti_once,[(this_or_next|eq, "$rescue_stage", 2),
                           (eq, "$rescue_stage", 4),
              (store_mission_timer_a, reg13),
              (ge, reg13, 90),
],[
(try_begin),
    (ge, "$meta_alarm", 9),
    (set_visitor, 21, "$guard_troop8", 0),(set_visitor, 22, "$guard_troop8", 0),(set_visitor, 23, "$guard_troop8", 0),(set_visitor, 24, "$guard_troop8", 0),(set_visitor, 25, "$guard_troop8", 0),
(else_try),
    (is_between, "$meta_alarm", 6, 9),
    (set_visitor, 21, "$guard_troop3", 0),(set_visitor, 22, "$guard_troop3", 0),(set_visitor, 23, "$guard_troop3", 0),(set_visitor, 24, "$guard_troop3", 0),(set_visitor, 25, "$guard_troop3", 0),
(else_try),
    (is_between, "$meta_alarm", 5, 7),
    (set_visitor, 21, "$guard_troop2", 0),(set_visitor, 22, "$guard_troop2", 0),(set_visitor, 23, "$guard_troop2", 0),(set_visitor, 24, "$guard_troop2", 0),(set_visitor, 25, "$guard_troop2", 0),
(try_end),
(reset_mission_timer_a),
]),

(2,0,0,[(eq, "$rescue_stage", 5)],[
(get_player_agent_no, ":player"),
(agent_get_position, pos5, ":player"),
(entry_point_get_position, pos6, 31),
(try_begin),
    (get_distance_between_positions, ":dist", pos5, pos6),
    (try_begin),
        (neg|ge, ":dist", 400),
#        (assign, "$dungeon_rescue", 1),
        (call_script, "script_infiltration_mission_update_companion_casualties"),
        (start_mission_conversation, "$rescue_convo_troop"),
    (try_end),
(try_end),
]),
(ti_tab_pressed,0,0,[],[(try_begin),(eq, "$battle_won", 1),(finish_mission),(try_end)]),
(ti_question_answered,0,0,[],[(store_trigger_param_1, ":answer"),(eq, ":answer", 0),(finish_mission)]),
 ],
),

( "sorcerer_mission",mtf_battle_mode,0,
  "You_lead_your_men_to_battle.",
[(0 ,mtef_visitor_source|mtef_team_1 ,af_override_horse, aif_start_alarmed, 1,[]),  
( 1 ,mtef_visitor_source|mtef_team_1 ,af_override_horse, aif_start_alarmed, 1,[]),  
( 2 ,mtef_visitor_source|mtef_team_1 ,af_override_horse, aif_start_alarmed, 1,[]),  
( 3 ,mtef_visitor_source|mtef_team_1 ,af_override_horse, aif_start_alarmed, 1,[]), 
( 4 ,mtef_visitor_source|mtef_team_1 ,af_override_horse, aif_start_alarmed, 1,[]), 
( 5 ,mtef_visitor_source|mtef_team_1 ,af_override_horse, aif_start_alarmed, 1,[]), 
( 6 ,mtef_visitor_source|mtef_team_1 ,af_override_horse, aif_start_alarmed, 1,[]), 
( 7 ,mtef_visitor_source|mtef_team_1 ,af_override_horse, aif_start_alarmed, 1,[]), 
( 8 ,mtef_visitor_source|mtef_team_1 ,af_override_horse, aif_start_alarmed, 1,[]), 
( 9 ,mtef_visitor_source|mtef_team_1 ,af_override_horse, aif_start_alarmed, 1,[]), 
(10 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]), 
(11 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]), 
(12 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]), 
(13 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]), 
(14 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]), 
(15 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]),  
(16 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]), 
(17 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]), 
(18 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]), 
(19 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]),  
(20 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]),  
(21 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]),  
(22 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]),  
(23 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]), 
(24 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]), 
(25 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]), 
(26 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]),  
],
[
(0,0,ti_once,[],[ (call_script, "script_infiltration_mission_synch_agents_and_troops"),
				  (call_script, "script_infiltration_mission_set_hit_points"),
				  (call_script, "script_wounded_hero_cap_mission_health"),
]),

(2,0,0, [], [(call_script, "script_infiltration_mission_update_companion_casualties")]),
(1,4,ti_once,[(main_hero_fallen)],[(call_script, "script_infiltration_mission_update_companion_casualties"),(set_mission_result, -1),(finish_mission)]),

(5,0, ti_once, [
  (try_for_agents, ":agent"),
    (agent_is_ally|neg, ":agent"),
    (agent_is_alive, ":agent"),
    (agent_get_troop_id, ":troop", ":agent"),
    (eq, ":troop", "trp_black_numenorean_sorcerer"),
    (agent_get_slot, ":slot1", ":agent", 1),
  (try_end),
  (ge, ":slot1", 3),
],[
 (try_begin),
    (ge, "$meta_alarm", 9),
    (set_visitor, 21, "$guard_troop8", 0),(set_visitor, 22, "$guard_troop8", 0),(set_visitor, 23, "$guard_troop8", 0),(set_visitor, 24, "$guard_troop8", 0),(set_visitor, 25, "$guard_troop8", 0),
 (else_try),
    (is_between, "$meta_alarm", 6, 9),
    (set_visitor, 21, "$guard_troop3", 0),(set_visitor, 22, "$guard_troop3", 0),(set_visitor, 23, "$guard_troop3", 0),(set_visitor, 24, "$guard_troop3", 0),(set_visitor, 25, "$guard_troop3", 0),
 (else_try),
    (is_between, "$meta_alarm", 5, 7),
    (set_visitor, 21, "$guard_troop2", 0),(set_visitor, 22, "$guard_troop2", 0),(set_visitor, 23, "$guard_troop2", 0),(set_visitor, 24, "$guard_troop2", 0),(set_visitor, 25, "$guard_troop2", 0),
 (try_end),
 (reset_mission_timer_a),
]),

(5,0,0, [],  [
  (try_for_agents, ":agent"),
    (agent_is_ally|neg, ":agent"),
    (agent_is_alive, ":agent"),
    (agent_get_troop_id, ":troop", ":agent"),
    (eq, ":troop", "trp_black_numenorean_sorcerer"),
    (agent_get_slot, ":slot1", ":agent", 1),
    (try_begin),
        (eq, ":slot1", 0),
        (entry_point_get_position, pos5, 30),
        (agent_set_scripted_destination, ":agent", pos5),
        (agent_set_slot, ":agent", 1, 1),
    (else_try),
        (eq, ":slot1", 1),
        (agent_set_animation, ":agent", "anim_defend_up_staff_keep"),
#        (play_sound, [opmask_sound]119, 0),
        (assign, ":numenemies", 0),
        (try_for_agents, ":enemies"),
            (agent_is_alive, ":enemies"),
            (agent_is_ally|neg, ":enemies"),
            (val_add, ":numenemies", 1),
        (try_end),
        (neg|gt, ":numenemies", 6),
        (agent_set_slot, ":agent", 1, 2),
    (else_try),
        (eq, ":slot1", 2),
        (store_random, ":rnd", 4),
        (try_begin),
            (neg|ge, ":rnd", 2),
            (entry_point_get_position, pos6, 31),
            (agent_set_scripted_destination, ":agent", pos6),
            (display_message, "@The_sorcerer_is_fleeing!_Kill_him!", 4294967040),
            (agent_set_slot, ":agent", 1, 3),
        (else_try),
            (ge, ":rnd", 2),
            (agent_clear_scripted_mode, ":agent"),
            (agent_set_slot, ":agent", 1, 4),
        (try_end),
    (else_try),
        (eq, ":slot1", 3),
        (agent_get_position, pos7, ":agent"),
        (get_distance_between_positions, ":dist", pos6, pos7),
        (neg|ge, ":dist", 500),
        (display_message, "@The_sorcerer_has_fled!", 4294901760),
        (display_message, "@Report_this_ill_news_to_the_Lady_at_once.", 4294901760),
#        (assign, "$sorcerer_quest", 3),
        (quest_set_slot,"qst_mirkwood_sorcerer",slot_quest_current_state,3),
		(fail_quest,"qst_mirkwood_sorcerer"),
        (agent_set_slot, ":agent", 1, 4),
		(set_mission_result, -1),
        (finish_mission),
    (try_end),
  (try_end),
]),

(2,0,0, [(neg|quest_slot_eq,"qst_mirkwood_sorcerer",slot_quest_current_state,2)],[
  (try_for_agents, ":deadenemy"),
    (agent_is_human, ":deadenemy"),
    (agent_is_ally|neg, ":deadenemy"),
    (agent_is_alive|neg, ":deadenemy"),
    (agent_get_troop_id, ":troop", ":deadenemy"),
    (eq, ":troop", "trp_black_numenorean_sorcerer"),
#    (assign, "$sorcerer_quest", 2),
	(quest_set_slot,"qst_mirkwood_sorcerer",slot_quest_current_state,2),
    (display_message, "@The_sorcerer_is_dead!", 4294967040),
	(succeed_quest,"qst_mirkwood_sorcerer"),
	(eq,"$rescue_stage",1), #dummy usage of global var
#    (scene_prop_get_instance, ":local1", [opmask_scene_prop]528, 0),
#    (prop_instance_get_position, pos1, ":local1"),
#    (copy_position, pos2, pos1),
#    (position_move_z, pos2, -1500, 0),
#    (prop_instance_animate_to_position, ":local1", pos2, pos1),
  (try_end),
]),

(1,60, ti_once, [
  (store_mission_timer_a, ":time"),
  (ge, ":time", 10),
  (all_enemies_defeated),
  (neg|main_hero_fallen),
#  (neg|eq, "$sorcerer_quest", 3),
  (neg|quest_slot_eq,"qst_mirkwood_sorcerer",slot_quest_current_state,3),
  (assign, "$g_battle_result", 1),
  (assign, "$battle_won", 1),
  (set_mission_result, 1),
  (display_message, "@The battle is won!"),
  (call_script, "script_infiltration_mission_update_companion_casualties"),
],[
#  (assign, "$sorcerer_quest", 2),
  (quest_set_slot,"qst_mirkwood_sorcerer",slot_quest_current_state,2),
  (finish_mission),
]),

(ti_tab_pressed,0,0, [],[(try_begin),(eq, "$battle_won", 1),(finish_mission),(try_end)]),
(ti_question_answered,0,0, [],[(store_trigger_param_1, ":local0"),(eq, ":local0", 0),(finish_mission)]),
  ],
),

( "pick_troops", 0, 0, "You_pick_your_stealthy_men.", [
  [0, 1536, 0, 1, 1, []],  
  [1,  256, 0,17, 0, []]],
  [(1,1,ti_once,[],[(start_mission_conversation, "trp_barman")])]
),

( "battle_wall_mission",mtf_battle_mode,0,
  "You_lead_your_men_to_battle.", [
  ( 0,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
  ( 1,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
  ( 2,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
  ( 3,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
  ( 4,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
  ( 5,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
  ( 6,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
  ( 7,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
  ( 8,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
  ( 9,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
  (10,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
  (11,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
  (12,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
  (13,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
  (14,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
  (15,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
  (16,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
  (17,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
  (18,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
  (19,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
  (20,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
  (21,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
  (22,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
  (23,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
  (24,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
  (25,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
  (26,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
],[
(0,0,ti_once,[],[
(call_script, "script_infiltration_mission_synch_agents_and_troops"),
(call_script, "script_infiltration_mission_set_hit_points"),
(call_script, "script_wounded_hero_cap_mission_health"),
#(try_begin),(eq, "$active_rescue", 1),(play_sound, [opmask_sound]133, 0),
# (else_try),(eq, "$active_rescue", 2),(play_sound, [opmask_sound]134, 0),
# (else_try),(eq, "$active_rescue", 3),(play_sound, [opmask_sound]135, 0),
# (else_try),(eq, "$active_rescue", 4),(play_sound, [opmask_sound]136, 0),
#(try_end),
]),

(1,0,0,[],[(call_script, "script_infiltration_mission_update_companion_casualties")]),

(1,4,ti_once,[(main_hero_fallen)],[
(call_script, "script_rescue_failed"),
(call_script, "script_infiltration_mission_update_companion_casualties"),
(set_mission_result, -1),
(finish_mission),
]),

(5,0,0,[(store_mission_timer_a, reg13),(ge, reg13, 60)],[
(try_begin),
    (ge, "$meta_alarm", 8),
    (set_visitor, 20, "$wall_mounted_troop5", 0),
    (set_visitor, 21, "$wall_mounted_troop5", 0),
    (set_visitor, 22, "$wall_mounted_troop5", 0),
    (set_visitor, 19, "$wall_mounted_troop5", 0),
    (set_visitor, 18, "$wall_mounted_troop5", 0),
    (add_reinforcements_to_entry, 20, 1),
    (add_reinforcements_to_entry, 21, 1),
    (add_reinforcements_to_entry, 22, 1),
    (add_reinforcements_to_entry, 23, 1),
    (add_reinforcements_to_entry, 24, 1),
    (reset_mission_timer_a),
(else_try),
    (neg|gt, "$meta_alarm", 7),
    (set_visitor, 20, "$wall_mounted_troop3", 0),
    (set_visitor, 21, "$wall_mounted_troop3", 0),
    (set_visitor, 22, "$wall_mounted_troop3", 0),
    (set_visitor, 19, "$wall_mounted_troop3", 0),
    (set_visitor, 18, "$wall_mounted_troop3", 0),
    (add_reinforcements_to_entry, 20, 1),
    (add_reinforcements_to_entry, 21, 1),
    (add_reinforcements_to_entry, 22, 1),
    (add_reinforcements_to_entry, 23, 1),
    (add_reinforcements_to_entry, 24, 1),
    (reset_mission_timer_a),
(try_end),
]),

(ti_tab_pressed      ,0,0,[],[(try_begin),(eq, "$battle_won", 1),(finish_mission),(try_end)]),
(ti_question_answered,0,0,[],[(store_trigger_param_1, ":local0"),(eq, ":local0", 0),(finish_mission)]),
  ],
),
] + mission_templates_cutscenes
