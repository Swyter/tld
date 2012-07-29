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

morale_scripts = [

	# script_cf_get_tier_morale
	# This script stores the agents tier morale based on race in reg0.
	# param0 = agent
	# TODO: Maybe add it so different races get different bonuses.
	("cf_agent_get_tier_morale",
	[
		(store_script_param, ":agent_no", 1),
		(assign, reg0, 0),
		(agent_get_troop_id,":troop", ":agent_no"),
		(store_character_level, ":level", ":troop"),	
		(try_begin),
			(is_between, ":level", 0, 6),
			(assign, reg0, 3),
		(else_try),
			(is_between, ":level", 7, 14),
			(assign, reg0, 6),
		(else_try),
			(is_between, ":level", 15, 23),
			(assign, reg0, 12),
		(else_try),
			(is_between, ":level", 24, 32),
			(assign, reg0, 18),
		(else_try),
			(assign, reg0, 25),
		(try_end),
	]),

	# script_cf_agent_get_leader
	# This script finds an agent's leader (heroes only), and stores his agent id in reg0.
	# param0 = agent
	("cf_agent_get_leader", 
	[
		(store_script_param, ":agent_no", 1),
		(assign, reg0, -1),
		(ge, ":agent_no", 0),
		(agent_get_party_id, ":party_no", ":agent_no"),
		(ge, ":party_no", 0),
		(party_stack_get_troop_id, ":troop", ":party_no", 0),
		(assign, ":continue", 1),
		(try_for_agents, ":cur_agent"),
			(eq, ":continue", 1),
			(agent_is_human, ":cur_agent"),
			(agent_get_troop_id, ":troop_no", ":cur_agent"),
			(troop_is_hero, ":troop"),
			(eq, ":troop", ":troop_no"),
			(assign, reg0, ":cur_agent"),
			(assign, ":continue", 0),
		(try_end),
	]),

	# script_cf_agent_get_leader_troop
	# This script finds an agent's leader, and stores his troop id in reg0.
	# param0 = agent
	("cf_agent_get_leader_troop", 
	[
		(store_script_param, ":agent_no", 1),
		(assign, reg0, -1),
		(ge, ":agent_no", 0),
		(agent_get_party_id, ":party_no", ":agent_no"),
		(gt, ":party_no", -1),
		(party_stack_get_troop_id, ":troop", ":party_no", 0),
		(try_begin),
			(troop_is_hero, ":troop"),
			(assign, reg0, ":troop"),
		(try_end),
	]),

	# script_cf_agent_get_faction
	# This script finds an agent's faction, and stores it in reg0.
	# param0 = agent
	("cf_agent_get_faction", 
	[
		(store_script_param, ":agent_no", 1),
		(assign, reg0, -1),
		(ge, ":agent_no", 0),
		(agent_get_troop_id, ":troop_no", ":agent_no"),
		(store_troop_faction, ":faction", ":troop_no"),
		(assign, reg0, ":faction"),
	]),

	# script_cf_agent_get_morale
	# This script calculates an agents morale, and stores it in reg1.
	# param0 = agent
	("cf_agent_get_morale", 
	[
		(store_script_param, ":agent_no", 1),
		(ge, ":agent_no", 0),
		(agent_get_class, ":class", ":agent_no"),
		(store_agent_hit_points,":hitpoints",":agent_no",0),
		(agent_get_troop_id,":troop_type", ":agent_no"),
		(troop_get_type, ":race", ":troop_type"),
		(store_character_level, ":troop_level", ":troop_type"),	
		(assign, ":leader", 0),
		(try_begin),
			(call_script, "script_cf_agent_get_leader_troop", ":agent_no"),
			(gt, reg0, -1),
			(store_skill_level,":leader","skl_leadership",reg0),
		(try_end),
		(val_div,":troop_level",10), # CC: was 10, changed for balance.
         	(val_div,":hitpoints",6), # CC: was 3, changed for balance.
         	(assign,reg1,100),
         	(val_sub,reg1,":hitpoints"),
         	(val_sub,reg1,":leader"),
         	(val_sub,reg1,":troop_level"),

		# leader bonuses
		(try_begin),
			(call_script, "script_cf_agent_get_leader", ":agent_no"),
			(gt, reg0, -1),
			(try_begin),
				(eq|this_or_next, ":race", tf_evil_man),
				(agent_is_alive, reg0),
				(val_sub, reg1, tld_morale_leader_important),
			(else_try),
				(eq|this_or_next, ":race", tf_gondor),
				(eq, ":race", tf_dunland),
				(agent_is_alive, reg0),
				(val_sub, reg1, tld_morale_leader_bonus),
			(else_try),
				(eq, ":race", tf_dwarf),
				(agent_is_alive|neg, reg0),
				(val_sub, reg1, tld_morale_leader_avenge),
			(else_try),
				(eq, ":race", tf_urukhai),
				(agent_is_alive|neg, reg0),
				(val_sub, reg1, tld_morale_leader_urukhai),
			(else_try),
				(agent_is_alive, reg0),
				(val_sub, reg1, tld_morale_leader_average),
			(try_end),
		(try_end),
	
		# What are the variables for enemy formations?
		(assign, ":formation", formation_none),
		(try_begin),
			(agent_is_ally, ":agent_no"),
			(try_begin),
				(eq, ":class", grc_infantry),
				(assign, ":formation", "$infantry_formation_type"),
			(else_try),
				(eq, ":class", grc_archers),
				(assign, ":formation", "$archer_formation_type"),
			(else_try),
				(eq, ":class", grc_cavalry),
				(assign, ":formation", "$cavalry_formation_type"),
			(try_end),
		(try_end),

		# Formation bonuses.
		(try_begin),
			(eq|this_or_next, ":race", tf_gondor),
			(eq|this_or_next, ":race", tf_male),
			(eq, ":race", tf_dunland),
			(gt, ":formation", formation_none),
			(val_sub, reg1, tld_morale_formation_bonus),
		(try_end),

		# Race bonuses / penalties.
		(try_begin),
			(eq, ":race", tf_orc),
			(val_sub, reg1, tld_morale_poor),
		(else_try),
			(eq|this_or_next, ":race", tf_rohan),
			(eq, ":race", tf_dunland),
			(val_sub, reg1, tld_morale_average),
		(else_try),
			(eq|this_or_next, ":race", tf_male),
			(eq|this_or_next, ":race", tf_female),
			(eq|this_or_next, ":race", tf_gondor),
			(eq|this_or_next, ":race", tf_lorien),
			(eq|this_or_next, ":race", tf_woodelf),
			(eq, ":race", tf_uruk),
			(val_sub, reg1, tld_morale_good),
		(else_try),
			(eq|this_or_next, ":race", tf_imladris),
			(eq|this_or_next, ":race", tf_urukhai),
			(eq|this_or_next, ":race", tf_harad),
			(eq|this_or_next, ":race", tf_dwarf),
			(eq, ":race", tf_evil_man),
			(val_sub, reg1, tld_morale_very_good),
		(else_try),
			(val_sub, reg1, tld_morale_average),
		(try_end),

		# Nazgul modifier and faction bonuses.
		(try_begin),
			(call_script, "script_cf_agent_get_faction", ":agent_no"),
			(gt, reg0, -1),
			(assign, ":faction", reg0),
			(faction_get_slot, ":faction_side", ":faction", slot_faction_side),
			(try_begin),
				(neq, ":faction_side", faction_side_eye), # Only eye troops are immune to nazgul
				(store_mul, ":nazgul_modifier", "$nazgul_in_battle", 20),
				(val_add, reg1, ":nazgul_modifier"),		
			(try_end),
			(try_begin),
				(eq|this_or_next, ":faction", fac_harad),
				(eq, ":faction", fac_khand),
				(val_sub, reg1, 20),
			(try_end),
		(try_end),
		
		(try_begin),
			(agent_slot_eq,":agent_no",slot_agent_rallied,1),
			(val_sub, reg1, 20),
		(try_end),

		# Tier morale
		(call_script, "script_cf_agent_get_tier_morale", ":agent_no"),
		(val_sub, reg1, reg0),
	]),

	# script_cf_spawn_routed_parties
	# This script spawns the routed parties nearby the player
	("cf_spawn_routed_parties", 
	[
		(eq, "$tld_option_morale", 1),
		(assign, ":total_parties", 0),

      		(try_for_parties, ":unused"),
        		(val_add, ":total_parties", 1),
      		(try_end),

      		(le, ":total_parties", "$tld_option_max_parties"),

		(try_begin),
			(eq, "$g_spawn_allies_routed", 1),
			(try_begin),
				# TODO: Scan for already routed parties.
				#(eq, 0, 1),
			#(else_try),
				(set_spawn_radius, 5),
            			(spawn_around_party, "p_main_party", "pt_routed_allies"),
            			(assign, ":routed_party", reg0),
				(call_script, "script_party_add_party", ":routed_party", "p_routed_allies"),
				(party_set_faction, ":routed_party", "$players_kingdom"),
				(party_clear, "p_routed_allies"),
				(assign, "$g_spawn_allies_routed", 0),
			(try_end),
		(try_end),
	
		(try_begin),
			(try_begin),
				# TODO: Scan for already routed parties.
				#(eq, 0, 1),
			#(else_try),
				(eq, "$g_spawn_enemies_routed", 1),
				(set_spawn_radius, 5),
            			(spawn_around_party, "p_main_party", "pt_routed_enemies"),
            			(assign, ":routed_party", reg0),
				(call_script, "script_party_add_party", ":routed_party", "p_routed_enemies"),
				(party_stack_get_troop_id, ":troop", ":routed_party", 0),
				(store_troop_faction, ":faction", ":troop"),
				(party_set_faction, ":routed_party", ":faction"),
				(party_clear, "p_routed_enemies"),
				(assign, "$g_spawn_enemies_routed", 0),
			(try_end),
		(try_end),
	]),


	# script_count_enemy_agents_around_agent
	# This script checks an agent for being surrounded by enemy agents, reg0 stores the number of agents
	# param1: agent to check; param2: max_distance
	("count_enemy_agents_around_agent", 
	[
		(store_script_param, ":agent_no", 1),
		(store_script_param, ":distance", 2),
		(assign, reg0, 0),
		(try_begin),
			(ge, ":agent_no", 0),
			(agent_get_position, pos1, ":agent_no"),
			(agent_get_team, ":team_a", ":agent_no"),
			(try_for_agents, ":cur_agent"),
				(agent_is_human, ":cur_agent"),
				(agent_is_alive, ":cur_agent"),
				(agent_get_position, pos2, ":cur_agent"),
				(get_distance_between_positions, ":dist", pos1, pos2),
				(lt, ":dist", ":distance"),
				(agent_get_team, ":team_b", ":cur_agent"),
				(teams_are_enemies, ":team_a", ":team_b"),
				(val_add, reg0, 1),
			(try_end),
		(try_end),
	]),

	# script_remove_agent_from_field
	# This script removes an agent from a battle and adds it to a routed party.
	# param1: agent to remove
	# TODO: minor improvements.
	("remove_agent_from_field", 
	[
		(store_script_param, ":agent_no", 1),
		(agent_get_troop_id, ":troop_no", ":agent_no"),

		# Remove agent's horse first.
		(agent_get_horse, ":horse_no", ":agent_no"),

		(try_begin),
			(ge, ":horse_no", 0),
			(call_script, "script_remove_agent", ":horse_no"),	
		(try_end),

		(try_begin),
			# Tell the player when a hero has left the battle
			(troop_is_hero, ":troop_no"),
      			(str_store_troop_name, s1, ":troop_no"),
			(assign, ":news_color", color_good_news),
			(try_begin),
        			(agent_is_ally, ":agent_no"),
				(assign, ":news_color", color_bad_news),
			(try_end),
			(display_message, "@{s1} has fled the battle!", ":news_color"),
			(call_script, "script_remove_agent", ":agent_no"),
		(else_try),
			# If the troop is a not hero, add it to a temp party
			(try_begin),
				(agent_is_ally, ":agent_no"),
				(agent_get_party_id, ":party_no", ":agent_no"),
				(agent_get_kill_count, ":agent_killed", ":agent_no"),
				(agent_get_kill_count, ":agent_wounded", ":agent_no", 1),
				(call_script, "script_remove_agent", ":agent_no"),
				(agent_get_kill_count, ":agent_killed_2", ":agent_no"),
				(agent_get_kill_count, ":agent_wounded_2", ":agent_no", 1),
				(assign, ":wounded", 0),
				(try_begin),
					(agent_is_wounded, ":agent_no"),
					(assign, ":wounded", 1),
				(try_end),
				(try_begin),
					# agent was killed
					(gt, ":agent_killed_2", ":agent_killed"),
			        	(party_add_members, "p_routed_allies", ":troop_no", 1),
					(try_begin),
						(eq, ":wounded", 1),
						(party_wound_members, "p_routed_allies", ":troop_no"),
					(try_end),
					(assign, "$g_spawn_allies_routed", 1),
				(else_try),
					# agent was wounded
					(gt, ":agent_wounded_2", ":agent_wounded"),
					(party_remove_members,":party_no",":troop_no", 1),
			        	(party_add_members, "p_routed_allies", ":troop_no", 1),
					(try_begin),
						(eq, ":wounded", 1),
						(party_wound_members, "p_routed_allies", ":troop_no"),
					(try_end),
					(assign, "$g_spawn_allies_routed", 1),
				(try_end),
			(else_try),	
			        (party_add_members, "p_routed_enemies", ":troop_no", 1),
				(try_begin),
					(agent_is_wounded, ":agent_no"),
					(party_wound_members, "p_routed_enemies", ":troop_no"),
				(try_end),
				(call_script, "script_remove_agent", ":agent_no"),
				(assign, "$g_spawn_enemies_routed", 1),
			(try_end),
		(try_end),

	]),

	# This script finds a position at the border nearest to the agent
	#
	("find_exit_position_at_pos4", 
	[
		(store_script_param, ":agent_no", 1),
		(try_begin),
			(le, ":agent_no", -1),
			(get_scene_boundaries, pos3, pos4),
			(position_get_x,":xmin",pos3),
			(position_get_y,":ymin",pos3),
			(position_get_x,":xmax",pos4),
			(position_get_y,":ymax",pos4),
			(init_position, pos20),
			(init_position, pos21),
			(init_position, pos22),
			(init_position, pos23),
			(store_random_in_range, ":rand_x", ":xmin", ":xmax"),
			(store_random_in_range, ":rand_y", ":ymin", ":ymax"),
			(position_set_x,pos20,":xmin"),
			(position_set_y,pos20,":rand_y"),
			(position_set_x,pos21,":xmax"),
			(position_set_y,pos21,":rand_y"),
			(position_set_x,pos22,":rand_x"),
			(position_set_y,pos22,":ymin"),
			(position_set_x,pos23,":rand_x"),
			(position_set_y,pos23,":ymax"),
			(store_random_in_range, ":rout_point", 0, 4),
			(val_add, ":rout_point", pos20),
			(copy_position, pos4, ":rout_point"),
			(position_set_z_to_ground_level, pos4),
		(else_try),
			(get_scene_boundaries, pos3, pos4),
			(agent_get_position, pos1, ":agent_no"),
			(position_set_z_to_ground_level, pos1),
			(position_set_z_to_ground_level, pos3),
			(position_set_z_to_ground_level, pos4),
			(position_get_x,":xmin",pos3),
			(position_get_y,":ymin",pos3),
			(position_get_x,":xmax",pos4),
			(position_get_y,":ymax",pos4),
			(position_get_x,":agent_x",pos1),
			(position_get_y,":agent_y",pos1),
			(init_position, pos20),
			(init_position, pos21),
			(init_position, pos22),
			(init_position, pos23),
			(position_set_x,pos20,":xmin"),
			(position_set_y,pos20,":agent_y"),
			(position_set_x,pos21,":xmax"),
			(position_set_y,pos21,":agent_y"),
			(position_set_x,pos22,":agent_x"),
			(position_set_y,pos22,":ymin"),
			(position_set_x,pos23,":agent_x"),
			(position_set_y,pos23,":ymax"),
			(position_set_z_to_ground_level, pos20),
			(position_set_z_to_ground_level, pos21),
			(position_set_z_to_ground_level, pos22),
			(position_set_z_to_ground_level, pos23),
			(assign, ":last_dist", 4000000),
			(try_for_range, ":index", 0, 4),
				(store_add, ":rout_point", ":index", pos20),
				(get_distance_between_positions, ":dist", pos1, ":rout_point"),
				(lt, ":dist", ":last_dist"),
				(assign, ":last_dist", ":dist"),
				(copy_position, pos4, ":rout_point"),
			(try_end),
		(try_end),
	]),

  #script_healthbars
    ("healthbars",
    [
	(assign,reg1,"$allies_coh_base"),
	(assign,reg2,"$enemies_coh"),
	(assign,reg3,"$new_kills"),
	(display_message,"@Your troops are at {reg1}% cohesion (+{reg3}% bonus), the enemy at {reg2}%!",0x6495ed),
     ]),

  #script_morale_check
    ("morale_check",
    [
            (try_begin),
              (lt,"$allies_coh",75),
              (store_random_in_range,":routed",1,101),
              (assign,":chance_ply",80),
              (val_sub,":chance_ply","$allies_coh"),
                (try_begin),            
                  (le,":routed",":chance_ply"),             
                  (display_message,"@Morale of your troops wavers!",color_bad_news),            
                  (call_script, "script_flee_allies"),
                (try_end),
            (try_end),

            (try_begin),
              (lt,"$enemies_coh",75),
              (store_random_in_range,":routed",1,101),
              (assign,":chance_ply",80),
              (val_sub,":chance_ply","$enemies_coh"),
                (try_begin),  
                  (le,":routed",":chance_ply"),             
                  (display_message,"@Morale of your enemies wavers!",color_good_news),            
                  (call_script, "script_flee_enemies"),
                (try_end),            
            (try_end),
     ]),

  #script_rout_check
    ("rout_check",
    [
	(assign,":ally","$allies_coh"),
	(assign,":enemy","$enemies_coh"),
	(val_sub,":ally",":enemy"),

                (try_begin),
                   (ge,":ally",40),
                  (display_message,"@Your enemies flee in terror!",color_good_news),  
                  (call_script, "script_rout_enemies"),
               (try_end),

                (try_begin),
                   (le,":ally",-40),
                  (display_message,"@Your troops flee in terror!",color_bad_news),  
                  (call_script, "script_rout_allies"),
               (try_end),
     ]),

	 
	 
##==============================================##
## 		FLEEING SCRIPTS 		##
##==============================================##

    ("flee_allies",
    [
	(call_script, "script_find_exit_position_at_pos4", -1),
		 
	(store_skill_level,":leader","skl_leadership","trp_player"),
	(try_for_agents,":agent"),
        	(agent_is_alive,":agent"),
        	(agent_is_human,":agent"),
        	(agent_is_ally,":agent"),
        	(store_agent_hit_points,":hitpoints",":agent",0),
		(agent_get_troop_id,":troop_type", ":agent"),
		(store_character_level, ":troop_level", ":troop_type"),
		(val_div,":troop_level",10),
		(val_add,":hitpoints",":troop_level"),		 
        	(assign,":chance_ply",100),
        	(val_sub,":chance_ply",":hitpoints"),
        	(val_sub,":chance_ply",":leader"),
        	(val_div,":chance_ply",2),
        	(store_random_in_range,":routed",1,101),
		(try_begin),
                	(le,":routed",":chance_ply"),
#               	(display_message,"@One ally runs!"),  
			(agent_get_position,pos2,":agent"),
			(position_move_z,pos2,200,0),
                	(agent_clear_scripted_mode,":agent"),
			(call_script, "script_find_exit_position_at_pos4", ":agent"),
			(agent_set_scripted_destination,":agent",pos4,1),
               	(try_end),
	(end_try),	
     ]),

	("flee_enemies",
	[
	(call_script, "script_find_exit_position_at_pos4", -1),

	(try_for_agents,":agent"),
         	(agent_is_alive,":agent"),
         	(agent_is_human,":agent"),
         	(neg|agent_is_ally,":agent"),
         	(store_agent_hit_points,":hitpoints",":agent",0),
		(agent_get_troop_id,":troop_type", ":agent"),
		(store_character_level, ":troop_level", ":troop_type"),
		(val_div,":troop_level",10),
		(val_add,":hitpoints",":troop_level"),		 
        	(assign,":chance_ply",100),
         	(val_sub,":chance_ply",":hitpoints"),
         	(val_sub,":chance_ply",4),
         	(val_div,":chance_ply",2),
         	(store_random_in_range,":routed",1,101),
	 	(try_begin),
                   	(le,":routed",":chance_ply"),
#                  	(display_message,"@One enemy runs!"),  
                	(agent_get_position,pos2,":agent"),
		 	(position_move_z,pos2,200,0),
                        (agent_clear_scripted_mode,":agent"),
			(call_script, "script_find_exit_position_at_pos4", ":agent"),
                        (agent_set_scripted_destination,":agent",pos4,1),
               (try_end),
	(end_try),	
	]),

##==============================================##
## 		ROUTING SCRIPTS 		##
##==============================================##

    ("rout_allies",
    [
	(call_script, "script_find_exit_position_at_pos4", -1),
	(try_for_agents,":agent"),
		(get_player_agent_no, ":player_agent"),
		(neq, ":player_agent", ":agent"),
         	(agent_is_alive,":agent"),
         	(agent_is_human,":agent"),
         	(agent_is_ally,":agent"),
		(call_script, "script_cf_agent_get_morale", ":agent"),
         	(assign, ":chance_ply", reg1),
         	(store_random_in_range,":routed",0,101),
		(assign, reg0, ":chance_ply"),
		(assign, reg1, ":routed"),
		#(display_message, "@{reg1} less than {reg0}"),
              	(try_begin),
                   	(le,":routed",":chance_ply"),
		   	(agent_slot_eq, ":agent", slot_agent_routed, 0),
		   	(agent_set_slot, ":agent", slot_agent_routed, 1),
              		(agent_get_position,pos2,":agent"),
		 	(position_move_z,pos2,200,0),
                        (agent_clear_scripted_mode,":agent"),
			(call_script, "script_find_exit_position_at_pos4", ":agent"),
                        (agent_set_scripted_destination,":agent",pos4,1),
           	(try_end),
		(try_begin),
                   	(le,":routed",":chance_ply"),
       			(store_random_in_range,":rand",1,101),
			(lt, ":rand", 67), # 67% chance.
			(agent_get_horse, ":horse", ":agent"),
			(try_begin),
				(gt, ":horse", -1),
          			(agent_set_animation, ":agent", "anim_nazgul_noooo_mounted_short"),
			(else_try),
          			(agent_set_animation, ":agent", "anim_nazgul_noooo_short"),	
			(try_end),
		(try_end),
	(try_end),	
     ]),

    ("rout_enemies",
    [
	(call_script, "script_find_exit_position_at_pos4", -1),
	
	(try_for_agents,":agent"),
         	(agent_is_alive,":agent"),
         	(agent_is_human,":agent"),
         	(neg|agent_is_ally,":agent"),
		(call_script, "script_cf_agent_get_morale", ":agent"),
         	(assign, ":chance_ply", reg1),
         	(store_random_in_range,":routed",0,101),
	 	(try_begin),
                   	(le,":routed",":chance_ply"),
		   	(agent_slot_eq, ":agent", slot_agent_routed, 0),
		   	(agent_set_slot, ":agent", slot_agent_routed, 1),
                	(agent_get_position,pos2,":agent"),
		 	(position_move_z,pos2,200,0),
                        (agent_clear_scripted_mode,":agent"),
			(call_script, "script_find_exit_position_at_pos4", ":agent"), 
                        (agent_set_scripted_destination,":agent",pos3,1),
               	(try_end),
		(try_begin),
                   	(le,":routed",":chance_ply"),
       			(store_random_in_range,":rand",1,101),
			(lt, ":rand", 67), # 67% chance.
			(agent_get_horse, ":horse", ":agent"),
			(try_begin),
				(gt, ":horse", -1),
          			(agent_set_animation, ":agent", "anim_nazgul_noooo_mounted_short"),
			(else_try),
          			(agent_set_animation, ":agent", "anim_nazgul_noooo_short"),	
			(try_end),
		(try_end),
	(try_end),
    ]),  

  

  #script_coherence
    ("coherence",
    [
	(get_scene_boundaries, pos3, pos4),	
	 
	(assign,":num_allies",0),
	(assign,":coh_allies",0),
	(assign,":num_enemies",0),
	(assign,":coh_enemies",0),
	(assign,":num_allies_alive",0),
	(assign,":num_enemies_alive",0),
	(assign,":num_allies_rallied",0),
	(assign,":num_enemies_rallied",0),

	(try_for_agents,":agent"),
		(agent_is_ally,":agent"),
		(agent_is_human,":agent"),
		(store_agent_hit_points,":hitpoints",":agent",0),
		(agent_get_troop_id,":troop_type", ":agent"),
		(store_character_level, ":troop_level", ":troop_type"),
#		(val_div,":troop_level",10),
		(val_mul,":hitpoints",":troop_level"),
		(val_add,":num_allies",":troop_level"),
		(val_add,":coh_allies",":hitpoints"),
		(try_begin),
			(agent_is_alive, ":agent"),
			(val_add, ":num_allies_alive", 1),
		(try_end),
		(try_begin),
			(agent_slot_eq,":agent",slot_agent_rallied,1),
			(val_add, ":num_allies_rallied", 1),
		(try_end),
	(else_try),
		(agent_is_human,":agent"),
		(store_agent_hit_points,":hitpoints",":agent",0),
		(agent_get_troop_id,":troop_type", ":agent"),
		(store_character_level, ":troop_level", ":troop_type"),
#		(val_div,":troop_level",10),
		(val_mul,":hitpoints",":troop_level"),
		(val_add,":num_enemies",":troop_level"),
		(val_add,":coh_enemies",":hitpoints"),
		(try_begin),
			(agent_is_alive, ":agent"),
			(val_add, ":num_enemies_alive", 1),
		(try_end),
		(try_begin),
			(agent_slot_eq,":agent",slot_agent_rallied,1),
			(val_add, ":num_enemies_rallied", 1),
		(try_end),
	(end_try),

	# Difference between in battle agents.
	(store_sub, ":advantage", ":num_allies_alive", ":num_enemies_alive"),

	(val_div,":coh_allies",":num_allies"),
	(assign,"$allies_coh_base",":coh_allies"),
	(val_add, "$allies_coh_base", ":advantage"),
	(val_add, "$allies_coh_base", ":num_allies_rallied"),
	(try_begin),
		(lt, "$allies_coh_base", 0),
		(assign, "$allies_coh_base", 0),
	(try_end),
	(assign,"$allies_coh","$allies_coh_base"),
	(val_div,":coh_enemies",":num_enemies"),
	(assign,"$enemies_coh",":coh_enemies"),
	(val_add,"$allies_coh","$new_kills"),
	(val_sub, "$enemies_coh", ":advantage"),
	(val_add, "$allies_coh", ":num_enemies_rallied"),
	(try_begin),
		(lt, "$enemies_coh", 0),
		(assign, "$enemies_coh", 0),
	(try_end),
	(try_begin),
		(lt, "$allies_coh", 0),
		(assign, "$allies_coh", 0),
	(try_end),
     ]),  
]