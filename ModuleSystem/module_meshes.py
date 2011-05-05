from header_meshes import *

####################################################################################################################
#  Each mesh record contains the following fields:
#  1) Mesh id: used for referencing meshes in other files. The prefix mesh_ is automatically added before each mesh id.
#  2) Mesh flags. See header_meshes.py for a list of available flags
#  3) Mesh resource name: Resource name of the mesh
#  4) Mesh translation on x axis: Will be done automatically when the mesh is loaded
#  5) Mesh translation on y axis: Will be done automatically when the mesh is loaded
#  6) Mesh translation on z axis: Will be done automatically when the mesh is loaded
#  7) Mesh rotation angle over x axis: Will be done automatically when the mesh is loaded
#  8) Mesh rotation angle over y axis: Will be done automatically when the mesh is loaded
#  9) Mesh rotation angle over z axis: Will be done automatically when the mesh is loaded
#  10) Mesh x scale: Will be done automatically when the mesh is loaded
#  11) Mesh y scale: Will be done automatically when the mesh is loaded
#  12) Mesh z scale: Will be done automatically when the mesh is loaded
####################################################################################################################

meshes = [
  ("ui_default_menu_window", 0, "ui_default_menu_window", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_bandits", 0, "pic_bandits", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_mb_warrior_1", 0, "pic_mb_warrior_1", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("relief01", 0, "relief01", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("draw_tribal_orcs", 0, "draw_tribal_orcs", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("draw_orc_raiders", 0, "draw_orc_raiders", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("draw_wild_troll", 0, "draw_wild_troll", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("draw_fangorn", 0, "draw_fangorn", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("draw_fangorn_orc", 0, "draw_fangorn_orc", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("draw_ent_attack", 0, "draw_ent_attack", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("draw_ent_attack_orc", 0, "draw_ent_attack_orc", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("draw_entdrink_human", 0, "draw_entdrink_human", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("draw_victory_orc", 0, "draw_victory_orc", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("draw_victory_dwarf", 0, "draw_victory_dwarf", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("draw_defeat_human", 0, "draw_defeat_human", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("draw_defeat_orc", 0, "draw_defeat_orc", 0, 0, 0, 0, 0, 0, 1, 1, 1),

  ("town_west_emnet", 0, "town_west_emnet", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("town_dol_guldur", 0, "town_dol_guldur", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("town_isengard", 0, "town_isengard", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("town_minas_tirith", 0, "town_minas_tirith", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("town_morannon", 0, "town_morannon", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("town_edoras", 0, "town_edoras", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("town_pelargir", 0, "town_pelargir", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("town_dol_amroth", 0, "town_dol_amroth", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("town_minas_morgul", 0, "town_minas_morgul", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("town_osgilliath", 0, "town_osgilliath", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("town_thranduils", 0, "town_thranduils", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("town_rivendell_camp", 0, "town_rivendell_camp", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("town_moria", 0, "town_moria", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("town_hornburg", 0, "town_hornburg", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("town_esgaroth", 0, "town_esgaroth", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("town_caras_galadhon", 0, "town_caras_galadhon", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("town_beorns_house", 0, "town_beorns_house", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  
  ("pic_prisoner_man", 0, "pic_prisoner_man", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_prisoner_fem", 0, "pic_prisoner_fem", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_prisoner_wilderness", 0, "pic_prisoner_wilderness", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  #("pic_siege_sighted", 0, "pic_siege_sighted", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  #("pic_siege_sighted_fem", 0, "pic_siege_sighted_fem", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_camp", 0, "pic_camp", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  #("pic_payment", 0, "pic_payment", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_escape_1", 0, "pic_escape_1", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_escape_1_fem", 0, "pic_escape_1_fem", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_victory", 0, "pic_victory", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_defeat", 0, "pic_defeat", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_wounded", 0, "pic_wounded", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_wounded_fem", 0, "pic_wounded_fem", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_steppe_bandits", 0, "pic_steppe_bandits", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_mountain_bandits", 0, "pic_mountain_bandits", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_sea_raiders", 0, "pic_sea_raiders", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_deserters", 0, "pic_deserters", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_forest_bandits", 0, "pic_forest_bandits", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_cattle", 0, "pic_cattle", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_looted_village", 0, "pic_looted_village", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_village_p", 0, "pic_village_p", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_village_s", 0, "pic_village_s", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_village_w", 0, "pic_village_w", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_recruits", 0, "pic_recruits", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_arms_swadian", 0, "pic_arms_swadian", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_arms_vaegir", 0, "pic_arms_vaegir", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_arms_khergit", 0, "pic_arms_khergit", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_arms_nord", 0, "pic_arms_nord", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("pic_arms_rhodok", 0, "pic_arms_rhodok", 0, 0, 0, 0, 0, 0, 1, 1, 1),

  ("portrait_blend_out", 0, "portrait_blend_out", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("load_window", 0, "load_window", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("checkbox_off", render_order_plus_1, "checkbox_off", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("checkbox_on", render_order_plus_1, "checkbox_on", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("white_plane", 0, "white_plane", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("white_dot", 0, "white_dot", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("player_dot", 0, "player_dot", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("flag_infantry", 0, "flag_infantry", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("flag_archers", 0, "flag_archers", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("flag_cavalry", 0, "flag_cavalry", 0, 0, 0, 0, 0, 0, 1, 1, 1),

  ("color_picker", 0, "color_picker",  0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("custom_map_banner_01", 0, "custom_map_banner_01",  0, 0, 0, -90, 0, 90, 1, 1, 1),
  ("custom_map_banner_02", 0, "custom_map_banner_02",  0, 0, 0, -90, 0, 90, 1, 1, 1),
  ("custom_map_banner_03", 0, "custom_map_banner_03",  0, 0, 0, -90, 0, 90, 1, 1, 1),
  ("custom_banner_01", 0, "custom_banner_01",  0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("custom_banner_02", 0, "custom_banner_02",  0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("custom_banner_bg", 0, "custom_banner_bg",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg01", 0, "custom_banner_fg01",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg02", 0, "custom_banner_fg02",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg03", 0, "custom_banner_fg03",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg04", 0, "custom_banner_fg04",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg05", 0, "custom_banner_fg05",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg06", 0, "custom_banner_fg06",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg07", 0, "custom_banner_fg07",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg08", 0, "custom_banner_fg08",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg09", 0, "custom_banner_fg09",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg10", 0, "custom_banner_fg10",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg11", 0, "custom_banner_fg11",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg12", 0, "custom_banner_fg12",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg13", 0, "custom_banner_fg13",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg14", 0, "custom_banner_fg14",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg15", 0, "custom_banner_fg15",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg16", 0, "custom_banner_fg16",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg17", 0, "custom_banner_fg17",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg18", 0, "custom_banner_fg18",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg19", 0, "custom_banner_fg19",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg20", 0, "custom_banner_fg20",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg21", 0, "custom_banner_fg21",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg22", 0, "custom_banner_fg22",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_fg23", 0, "custom_banner_fg23",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_01", 0, "custom_banner_charge_01",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_02", 0, "custom_banner_charge_02",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_03", 0, "custom_banner_charge_03",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_04", 0, "custom_banner_charge_04",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_05", 0, "custom_banner_charge_05",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_06", 0, "custom_banner_charge_06",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_07", 0, "custom_banner_charge_07",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_08", 0, "custom_banner_charge_08",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_09", 0, "custom_banner_charge_09",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_10", 0, "custom_banner_charge_10",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_11", 0, "custom_banner_charge_11",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_12", 0, "custom_banner_charge_12",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_13", 0, "custom_banner_charge_13",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_14", 0, "custom_banner_charge_14",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_15", 0, "custom_banner_charge_15",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_16", 0, "custom_banner_charge_16",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_17", 0, "custom_banner_charge_17",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_18", 0, "custom_banner_charge_18",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_19", 0, "custom_banner_charge_19",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_20", 0, "custom_banner_charge_20",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_21", 0, "custom_banner_charge_21",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_22", 0, "custom_banner_charge_22",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_23", 0, "custom_banner_charge_23",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_24", 0, "custom_banner_charge_24",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_25", 0, "custom_banner_charge_25",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_26", 0, "custom_banner_charge_26",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_27", 0, "custom_banner_charge_27",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_28", 0, "custom_banner_charge_28",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_29", 0, "custom_banner_charge_29",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_30", 0, "custom_banner_charge_30",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_31", 0, "custom_banner_charge_31",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_32", 0, "custom_banner_charge_32",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_33", 0, "custom_banner_charge_33",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_34", 0, "custom_banner_charge_34",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_35", 0, "custom_banner_charge_35",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_36", 0, "custom_banner_charge_36",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_37", 0, "custom_banner_charge_37",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_38", 0, "custom_banner_charge_38",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_39", 0, "custom_banner_charge_39",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_40", 0, "custom_banner_charge_40",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_41", 0, "custom_banner_charge_41",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_42", 0, "custom_banner_charge_42",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_43", 0, "custom_banner_charge_43",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_44", 0, "custom_banner_charge_44",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_45", 0, "custom_banner_charge_45",  0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("custom_banner_charge_46", 0, "custom_banner_charge_46",  0, 0, 0, 0, 0, 0, 10, 10, 10),

#TLD begin
  ("tableau_mesh_shield_kite"  , 0, "tableau_mesh_shield_kite"  , 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("tableau_mesh_shield_tower" , 0, "tableau_mesh_shield_tower" , 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("tableau_mesh_shield_square", 0, "tableau_mesh_shield_square", 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("tableau_mesh_shield_round" , 0, "tableau_mesh_shield_round" , 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("tableau_mesh_shield_harad" , 0, "tableau_mesh_shield_harad" , 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("tableau_mesh_shield_rohan" , 0, "tableau_mesh_shield_rohan" , 0, 0, 0, 0, 0, 0, 10, 10, 10),
  #TLD end

  ("tableau_mesh_custom_banner", 0, "tableau_mesh_custom_banner", 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("tableau_mesh_custom_banner_square", 0, "tableau_mesh_custom_banner_square", 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("tableau_mesh_custom_banner_tall", 0, "tableau_mesh_custom_banner_tall", 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("tableau_mesh_custom_banner_short", 0, "tableau_mesh_custom_banner_short", 0, 0, 0, 0, 0, 0, 10, 10, 10),

  ("tableau_mesh_shield_round_1",  0, "tableau_mesh_shield_round_1", 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("tableau_mesh_shield_round_2",  0, "tableau_mesh_shield_round_2", 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("tableau_mesh_shield_round_3",  0, "tableau_mesh_shield_round_3", 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("tableau_mesh_shield_round_4",  0, "tableau_mesh_shield_round_4", 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("tableau_mesh_shield_round_5",  0, "tableau_mesh_shield_round_5", 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("tableau_mesh_shield_small_round_1",  0, "tableau_mesh_shield_small_round_1", 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("tableau_mesh_shield_small_round_2",  0, "tableau_mesh_shield_small_round_2", 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("tableau_mesh_shield_small_round_3",  0, "tableau_mesh_shield_small_round_3", 0, 0, 0, 0, 0, 0, 10, 10, 10),
#  ("tableau_mesh_shield_kite_1",   0, "tableau_mesh_shield_kite_1",  0, 0, 0, 0, 0, 0, 10, 10, 10),
#  ("tableau_mesh_shield_kite_2",   0, "tableau_mesh_shield_kite_2",  0, 0, 0, 0, 0, 0, 10, 10, 10),
#  ("tableau_mesh_shield_kite_3",   0, "tableau_mesh_shield_kite_3",  0, 0, 0, 0, 0, 0, 10, 10, 10),
#  ("tableau_mesh_shield_kite_4",   0, "tableau_mesh_shield_kite_4",  0, 0, 0, 0, 0, 0, 10, 10, 10),
#  ("tableau_mesh_shield_heater_1", 0, "tableau_mesh_shield_heater_1",  0, 0, 0, 0, 0, 0, 10, 10, 10),
#  ("tableau_mesh_shield_heater_2", 0, "tableau_mesh_shield_heater_2",  0, 0, 0, 0, 0, 0, 10, 10, 10),
#  ("tableau_mesh_shield_pavise_1", 0, "tableau_mesh_shield_pavise_1",  0, 0, 0, 0, 0, 0, 10, 10, 10),
#  ("tableau_mesh_shield_pavise_2", 0, "tableau_mesh_shield_pavise_2",  0, 0, 0, 0, 0, 0, 10, 10, 10),

  ("heraldic_armor_bg", 0, "heraldic_armor_bg",  0, 0, 0, 0, 0, 0, 10, 10, 10),

#  ("tableau_mesh_heraldic_armor_a", 0, "tableau_mesh_heraldic_armor_a",  0, 0, 0, 0, 0, 0, 1, 1, 1),
#  ("tableau_mesh_heraldic_armor_b", 0, "tableau_mesh_heraldic_armor_b",  0, 0, 0, 0, 0, 0, 1, 1, 1),
#  ("tableau_mesh_heraldic_armor_c", 0, "tableau_mesh_heraldic_armor_c",  0, 0, 0, 0, 0, 0, 1, 1, 1),
#  ("tableau_mesh_heraldic_armor_d", 0, "tableau_mesh_heraldic_armor_d",  0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("tableau_mesh_heraldic_rohan_armor", 0, "tableau_mesh_heraldic_rohan_armor",  0, 0, 0, 0, 0, 0, 1, 1, 1),

#  ("outer_terrain_plain_1", 0, "ter_border_a", -90, 0, 0, 0, 0, 0, 1, 1, 1),
  ("banner_a01", 0, "banner_a01", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_a02", 0, "banner_a02", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_a03", 0, "banner_a03", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_a04", 0, "banner_a04", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_a05", 0, "banner_a05", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_a06", 0, "banner_a06", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_a07", 0, "banner_a07", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_a08", 0, "banner_a08", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_a09", 0, "banner_a09", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_a10", 0, "banner_a10", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_a11", 0, "banner_a11", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_a12", 0, "banner_a12", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_a13", 0, "banner_a13", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_a14", 0, "banner_a14", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_a15", 0, "banner_f21", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_a16", 0, "banner_a16", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_a17", 0, "banner_a17", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_a18", 0, "banner_a18", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_a19", 0, "banner_a19", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_a20", 0, "banner_a20", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_a21", 0, "banner_a21", 0, 0, 0, -90, 0, 0, 1, 1, 1),
# B and C banners are not used
  ("banner_d01", 0, "banner_d01", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_d02", 0, "banner_d02", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_d03", 0, "banner_d03", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_d04", 0, "banner_d04", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_d05", 0, "banner_d05", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_d06", 0, "banner_d06", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_d07", 0, "banner_d07", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_d08", 0, "banner_d08", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_d09", 0, "banner_d09", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_d10", 0, "banner_d10", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_d11", 0, "banner_d11", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_d12", 0, "banner_d12", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_d13", 0, "banner_d13", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_d14", 0, "banner_d14", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_d15", 0, "banner_d15", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_d16", 0, "banner_d16", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_d17", 0, "banner_d17", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_d18", 0, "banner_d18", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_d19", 0, "banner_d19", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_d20", 0, "banner_d20", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_d21", 0, "banner_d21", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_e01", 0, "banner_e01", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_e02", 0, "banner_e02", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_e03", 0, "banner_e03", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_e04", 0, "banner_e04", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_e05", 0, "banner_e05", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_e06", 0, "banner_e06", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_e07", 0, "banner_e07", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_e08", 0, "banner_e08", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_e09", 0, "banner_e09", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_e10", 0, "banner_e10", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_e11", 0, "banner_e11", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_e12", 0, "banner_e12", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_e13", 0, "banner_e13", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_e14", 0, "banner_e14", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_e15", 0, "banner_e15", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_e16", 0, "banner_e16", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_e17", 0, "banner_e17", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_e18", 0, "banner_e18", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_e19", 0, "banner_e19", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_e20", 0, "banner_e20", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_e21", 0, "banner_e21", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_f01", 0, "banner_f01", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_f02", 0, "banner_f02", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_f03", 0, "banner_f03", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_f04", 0, "banner_f04", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_f05", 0, "banner_f05", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_f06", 0, "banner_f06", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_f07", 0, "banner_f07", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_f08", 0, "banner_f08", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_f09", 0, "banner_f09", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_f10", 0, "banner_f10", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_f11", 0, "banner_f11", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_f12", 0, "banner_f12", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_f13", 0, "banner_f13", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_f14", 0, "banner_f14", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_f15", 0, "banner_f15", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_f16", 0, "banner_f16", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_f17", 0, "banner_f17", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_f18", 0, "banner_f18", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_f19", 0, "banner_f19", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_f20", 0, "banner_f20", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banner_f21", 0, "banner_a15", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  


  ("arms_a01", 0, "arms_a01", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_a02", 0, "arms_a02", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_a03", 0, "arms_a03", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_a04", 0, "arms_a04", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_a05", 0, "banner_a05", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_a06", 0, "arms_a06", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_a07", 0, "banner_a07", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_a08", 0, "arms_a08", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_a09", 0, "banner_a09", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_a10", 0, "banner_a10", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_a11", 0, "banner_a11", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_a12", 0, "arms_a12", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_a13", 0, "arms_a13", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_a14", 0, "banner_a14", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_a15", 0, "banner_f21", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_a16", 0, "arms_a16", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_a17", 0, "arms_a17", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_a18", 0, "arms_a18", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_a19", 0, "arms_a19", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_a20", 0, "arms_a20", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_a21", 0, "arms_a21", 0, 0, 0, -90, 0, 0, 1, 1, 1),
# B and C banners are not used
  ("arms_d01", 0, "banner_d01", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_d02", 0, "arms_d02", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_d03", 0, "arms_d03", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_d04", 0, "arms_d04", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_d05", 0, "banner_d05", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_d06", 0, "arms_d06", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_d07", 0, "arms_d07", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_d08", 0, "arms_d08", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_d09", 0, "arms_d09", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_d10", 0, "banner_d10", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_d11", 0, "arms_d11", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_d12", 0, "arms_d12", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_d13", 0, "arms_d13", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_d14", 0, "arms_d14", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_d15", 0, "arms_d15", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_d16", 0, "arms_d16", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_d17", 0, "arms_d17", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_d18", 0, "arms_d18", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_d19", 0, "arms_d19", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_d20", 0, "arms_d20", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_d21", 0, "arms_d21", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_e01", 0, "banner_e01", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_e02", 0, "arms_e02", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_e03", 0, "banner_e03", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_e04", 0, "banner_e04", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_e05", 0, "banner_e05", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_e06", 0, "banner_e06", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_e07", 0, "banner_e07", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_e08", 0, "banner_e08", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_e09", 0, "banner_e09", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_e10", 0, "banner_e10", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_e11", 0, "banner_e11", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_e12", 0, "banner_e12", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_e13", 0, "banner_e13", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_e14", 0, "banner_e14", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_e15", 0, "banner_e15", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_e16", 0, "banner_e16", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_e17", 0, "banner_e17", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_e18", 0, "banner_e18", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_e19", 0, "banner_e19", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_e20", 0, "banner_e20", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_e21", 0, "banner_e21", 0, 0, 0, -90, 0, 0, 1, 1, 1),

  ("arms_f01", 0, "banner_f01", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_f02", 0, "banner_f02", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_f03", 0, "banner_f03", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_f04", 0, "banner_f04", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_f05", 0, "banner_f05", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_f06", 0, "banner_f06", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_f07", 0, "banner_f07", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_f08", 0, "banner_f08", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_f09", 0, "banner_f09", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_f10", 0, "banner_f10", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_f11", 0, "banner_f11", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_f12", 0, "banner_f12", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_f13", 0, "banner_f13", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_f14", 0, "banner_f14", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_f15", 0, "banner_f15", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_f16", 0, "banner_f16", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_f17", 0, "banner_f17", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_f18", 0, "banner_f18", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_f19", 0, "banner_f19", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_f20", 0, "banner_f20", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("arms_f21", 0, "banner_a15", 0, 0, 0, -90, 0, 0, 1, 1, 1),

  ("banners_default_a", 0, "banners_default_a", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banners_default_b", 0, "banners_default_b", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banners_default_c", 0, "banners_default_c", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banners_default_d", 0, "banners_default_d", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("banners_default_e", 0, "banners_default_e", 0, 0, 0, -90, 0, 0, 1, 1, 1),
#### TLD Rhun circular patterns
  ("circular_8mosaic1", 0, "circular_8mosaic1", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("circular_8mosaic2", 0, "circular_8mosaic2", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("circular_8mosaic3", 0, "circular_8mosaic3", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("circular_8mosaic4", 0, "circular_8mosaic4", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("circular_8mosaic5", 0, "circular_8mosaic5", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("circular_8mosaic6", 0, "circular_8mosaic6", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("circular_8mosaic7", 0, "circular_8mosaic7", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("circular_8mosaic8", 0, "circular_8mosaic8", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("circular_8mosaic9", 0, "circular_8mosaic9", 0, 0, 0, -90, 0, 0, 1, 1, 1),
  ("circular_8mosaic10",0, "circular_8mosaic10",0, 0, 0, -90, 0, 0, 1, 1, 1),
#### Far Harad shield paint
  ("far_harad_shield_paint", 0, "harad_tableau_paint_mesh", 0, 0, 0, 0, 0, 0, 10, 10, 10),
#### Civilian clothes tableau
  ("tableau_mesh_gondor_tunic_a", 0, "tableau_mesh_gondor_tunic_a", 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("tableau_mesh_gondor_tunic_b", 0, "tableau_mesh_gondor_tunic_b", 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("tableau_mesh_rohan_tunic"   , 0, "tableau_mesh_rohan_tunic"   , 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("tableau_mesh_dale_tunic"    , 0, "tableau_mesh_dale_tunic"    , 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("tableau_mesh_woodman_tunic" , 0, "tableau_mesh_woodman_tunic" , 0, 0, 0, 0, 0, 0, 10, 10, 10),
#### TLD rohan shield paintings
  ("rohan_paint_1", 0, "rohan_paint_mesh_a", 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("rohan_paint_2", 0, "rohan_paint_mesh_b", 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("rohan_paint_3", 0, "rohan_paint_mesh_f", 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("rohan_paint_4", 0, "rohan_paint_mesh_g", 0, 0, 0, 0, 0, 0, 10, 10, 10),
  ("rohan_paint_5", 0, "rohan_paint_mesh_c", 0, 0, 0, 0, 0, 0, 10, 10, 10), # here start paitings suitable for bulb-centered shields
  ("rohan_paint_6", 0, "rohan_paint_mesh_d", 0, 0, 0, 0, 0, 0, 10, 10, 10),  
  ("rohan_paint_7", 0, "rohan_paint_mesh_e", 0, 0, 0, 0, 0, 0, 10, 10, 10),  
]
