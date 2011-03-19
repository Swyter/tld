﻿from module_constants import *

strings = [
  ("no_string", "NO STRING!"),
  ("empty_string", " "),
  ("yes", "Yes."),
  ("no", "No."),
# Strings before this point are hardwired.  
  ("blank_string", " "),
  ("error_string", "ERROR!!!ERROR!!!!ERROR!!!ERROR!!!ERROR!!!ERROR!!!!ERROR!!!ERROR!!!!ERROR!!!ERROR!!!!ERROR!!!ERROR!!!!ERROR!!!ERROR!!!!ERROR!!!ERROR!!!!!"),
##  ("none", "none"),
  ("noone", "no one"),
##  ("nothing", "nothing"),
  ("s0", "{s0}"),
  ("blank_s1", " {s1}"),
  ("reg1", "{reg1}"),
  ("s50_comma_s51", "{s50}, {s51}"),
  ("s50_and_s51", "{s50} and {s51}"),
  ("s5_s_party", "{s5}'s Party"),

  ("given_by_s1_at_s2", "Given by {s1} at {s2}"),
  ("given_by_s1_in_wilderness", "Given by {s1} whilst in the field"),
  ("s7_raiders", "{s7} Raiders"),

  ("bandits_eliminated_by_another", "The troublesome bandits have been eliminated by another party."),
  ("msg_battle_won","Battle won! Press tab key to leave..."),
  ("tutorial_map1","You are now viewing the overland map. Left-click on the map to move your party to that location, enter the selected town, or pursue the selected party. Time will pause on the overland map if your party is not moving, waiting or resting. To wait anywhere simply press and hold down the space bar."),


  ("change_color_1", "Change Color 1"),
  ("change_color_2", "Change Color 2"),
  ("change_background", "Change Background Pattern"),
  ("change_flag_type", "Change Flag Type"),
  ("change_map_flag_type", "Change Map Flag Type"),
  ("randomize", "Randomize"),
  ("sample_banner", "Sample banner:"),
  ("sample_map_banner", "Sample map banner:"),
  ("number_of_charges", "Number of charges:"),
  ("change_charge_1",       "Change Charge 1"),
  ("change_charge_1_color", "Change Charge 1 Color"),
  ("change_charge_2",       "Change Charge 2"),
  ("change_charge_2_color", "Change Charge 2 Color"),
  ("change_charge_3",       "Change Charge 3"),
  ("change_charge_3_color", "Change Charge 3 Color"),
  ("change_charge_4",       "Change Charge 4"),
  ("change_charge_4_color", "Change Charge 4 Color"),
  ("change_charge_position", "Change Charge Position"),
  ("choose_position", "Choose position:"),
  ("choose_charge", "Choose a charge:"),
  ("choose_background", "Choose background pattern:"),
  ("choose_flag_type", "Choose flag type:"),
  ("choose_map_flag_type", "Choose map flag type:"),
  ("choose_color", "Choose color:"),
  ("accept", "Accept"),
  ("charge_no_1", "Charge #1:"),
  ("charge_no_2", "Charge #2:"),
  ("charge_no_3", "Charge #3:"),
  ("charge_no_4", "Charge #4:"),
  ("change", "Change"),
  ("plus", "+"),
  ("minus", "-"),
  ("color_no_1", "Color #1:"),
  ("color_no_2", "Color #2:"),
  ("charge", "Charge"),
  ("color", "Color"),
  ("flip_horizontal", "Flip Horizontal"),
  ("flip_vertical", "Flip Vertical"),
  ("hold_fire", "Hold Fire"),
  ("blunt_hold_fire", "Blunt / Hold Fire"),
  
  
##  ("tutorial_camp1","This is training ground where you can learn the basics of the game. Use A, S, D, W keys to move and the mouse to look around."),
##  ("tutorial_camp2","F is the action key. You can open doors, talk to people and pick up objects with F key. If you wish to leave a town or retreat from a battle, press the TAB key."),
##  ("tutorial_camp3","Training Ground Master wishes to speak with you about your training. Go near him, look at him and press F when you see the word 'Talk' under his name. "),
##  ("tutorial_camp4","To see the in-game menu, press the Escape key. If you select Options, and then Controls from the in-game menu, you can see a complete list of key bindings."),
##  ("tutorial_camp6","You've received your first quest! You can take a look at your current quests by pressing the Q key. Do it now and check the details of your quest."),
##  ("tutorial_camp7","You've completed your quest! Go near Training Ground Master and speak with him about your reward."),
##  ("tutorial_camp8","You've gained some experience and weapon points! Press C key to view your character and increase your weapon proficiencies."),
##  ("tutorial_camp9","Congratulations! You've finished the tutorial of Mount&Blade. Press TAB key to leave the training ground."),

##  ("tutorial_enter_melee", "You are entering the melee weapon training area. The chest nearby contains various weapons which you can experiment with. If you wish to quit this tutorial, press TAB key."),
##  ("tutorial_enter_ranged", "You are entering the ranged weapon training area.  The chest nearby contains various ranged weapons which you can experiment with. If you wish to quit this tutorial, press TAB key."),
##  ("tutorial_enter_mounted", "You are entering the mounted training area. Here, you can try different kinds of weapons while riding a horse. If you wish to quit this tutorial, press TAB key."),

#  ("tutorial_usage_sword", "Sword is a very versatile weapon which is very fast in both attack and defense. Usage of one handed swords are affected by your one handed weapon proficiency. Focus on the sword and press F key to pick it up."),
#  ("tutorial_usage_axe", "Axe is a heavy (and therefore slow) weapon which can deal high damage to the opponent. Usage of one handed axes are affected by your one handed weapon proficiency. Focus on the axe and press F key to pick it up."),
#  ("tutorial_usage_club", "Club is a blunt weapon which deals less damage to the opponent than any other one handed weapon, but it knocks you opponents unconscious so that you can take them as a prisoner. Usage of clubs are affected by your one handed weapon proficiency. Focus on the club and press F key to pick it up."),
#  ("tutorial_usage_battle_axe", "Battle axe is a long weapon and it can deal high damage to the opponent. Usage of battle axes are affected by your two handed weapon proficiency. Focus on the battle axe and press F key to pick it up."),
#  ("tutorial_usage_spear", "Spear is a very long weapon which lets the wielder to strike the opponent earlier. Usage of the spears are affected by your polearm proficiency. Focus on the spear and press F key to pick it up."),
#  ("tutorial_usage_short_bow", "Short bow is a common ranged weapon which is easy to reload but hard to master at. Usage of short bows are affected by your archery proficiency. Focus on the short bow and arrows and press F key to pick them up."),
#  ("tutorial_usage_crossbow", "Crossbow is a heavy ranged weapon which is easy to use and deals high amount of damage to the opponent. Usage of crossbows are affected by your crossbow proficiency. Focus on the crossbow and bolts and press F key to pick them up."),
#  ("tutorial_usage_throwing_daggers", "Throwing daggers are easy to use and throwing them takes a very short time. But they deal light damage to the opponent. Usage of throwing daggers are affected byyour throwing weapon proficiency. Focus on the throwing daggers and press F key to pick it up."),
#  ("tutorial_usage_mounted", "You can use your weapons while you're mounted. Polearms like the lance here can be used for couched damage against opponents. In order to do that, ride your horse at a good speed and aim at your enemy. But do not press the attack button."),

##  ("tutorial_melee_chest", "The chest near you contains some of the melee weapons that can be used throughout the game. Look at the chest now and press F key to view its contents. Click on the weapons and move them to your Arms slots to be able to use them."),
##  ("tutorial_ranged_chest", "The chest near you contains some of the ranged weapons that can be used throughout the game. Look at the chest now and press F key to view its contents. Click on the weapons and move them to your Arms slots to be able to use them."),
##
##  ("tutorial_item_equipped", "You have equipped a weapon. Move your mouse scroll wheel up to wield your weapon. You can also switch between your weapons using your mouse scroll wheel."),

  ("tutorial_ammo_refilled", "Ammo refilled."),
  ("tutorial_failed", "You have been beaten this time, but don't worry. Follow the instructions carefully and you'll do better next time.\
 Press the Tab key to return to to the menu where you can retry this tutorial."),

  ("tutorial_1_msg_1","In this tutorial you will learn the basics of movement and combat.\
 In Mount&Blade you use the mouse to control where you are looking, and the WASD keys of your keyboard to move.\
 Your first task in the training is to locate the yellow flag in the room and move over it.\
 You can press the Tab key at any time to quit this tutorial or to exit any other area in the game.\
 Go to the yellow flag now."),
  ("tutorial_1_msg_2","Well done. Next we will cover attacking with weapons.\
 For the purposes of this tutorial you have been equipped with bow and arrows, a sword and a shield.\
 You can draw different weapons from your weapon slots by using the scroll wheel of your mouse.\
 In the default configuration, scrolling up pulls out your next weapon, and scrolling down pulls out your shield.\
 If you are already holding a shield, scrolling down will put your shield away instead.\
 Try changing your wielded equipment with the scroll wheel now. When you are ready,\
 go to the yellow flag to move on to your next task."),
  ("tutorial_1_msg_3","Excellent. The next part of this tutorial covers attacking with melee weapons.\
 You attack with your currently wielded weapon by using your left mouse button.\
 Press and hold the button to ready an attack, then release the button to strike.\
 If you hold down the left mouse button for a while before releasing, your attack will be more powerful.\
 Now draw your sword and destroy the four dummies in the room."),
  ("tutorial_1_msg_4","Nice work! You've destroyed all four dummies. You can now move on to the next room."),
  ("tutorial_1_msg_5","As you see, there is an archery target on the far side of the room.\
 Your next task is to use your bow to put three arrows into that target. Press and hold down the left mouse button to notch an arrow.\
 You can then fire the arrow by releasing the left mouse button. Note the targeting reticule in the centre of your screen,\
 which shows you the accuracy of your shot.\
 In order to achieve optimal accuracy, let fly your arrow when the reticule is at its smallest.\
 Try to shoot the target now."),
  ("tutorial_1_msg_6","Well done! You've learned the basics of moving and attacking.\
 With a little bit of practice you will soon master them.\
 In the second tutorial you can learn more advanced combat skills and face armed opponents.\
 You can press the Tab key at any time to return to the tutorial menu."),

  ("tutorial_2_msg_1","This tutorial will teach you how to defend yourself with a shield and how to battle armed opponents.\
 For the moment you are armed with nothing but a shield.\
 Your task is not to attack, but to successfully protect yourself from harm with your shield.\
 There is an armed opponent waiting for you in the next room.\
 He will try his best to knock you unconscious, while you must protect yourself with your shield\
 by pressing and holding the right mouse button.\
 Go into the next room now to face your opponent.\
 Remember that you can press the Tab key at any time to quit this tutorial or to exit any other area in the game."),
  ("tutorial_2_msg_2","Press and hold down the right mouse button to raise your shield. Try to remain standing for thirty seconds. You have {reg3} seconds to go."),
  ("tutorial_2_msg_3","Well done, you've succeeded in defending against an armed opponent.\
 The next phase of this tutorial will pit you and your shield against a force of enemy archers.\
 Move on to the next room when you're ready to face the archers."),
  ("tutorial_2_msg_4","Defend yourself from arrows by raising your shield with the right mouse button. Try to remain standing for thirty seconds. You have {reg3} seconds to go."),
  ("tutorial_2_msg_5","Excellent, you've put up a succesful defence against archers.\
 There is a reward waiting for you in the next room."),
  ("tutorial_2_msg_6","In the default configuration,\
 the F key on your keyboard is used for non-violent interaction with objects and humans in the gameworld.\
 To pick up the sword on the altar, look at it and press F when you see the word 'Equip'."),
  ("tutorial_2_msg_7","A fine weapon! Now you can use it to deliver a bit of payback.\
 Go back through the door and dispose of the archers you faced earlier."),
  ("tutorial_2_msg_8","Very good. Your last task before finishing this tutorial is to face the maceman.\
 Go through the door now and show him your steel!"),
  ("tutorial_2_msg_9","Congratulations! You have now learned how to defend yourself with a shield and even had your first taste of combat with armed opponents.\
 Give it a bit more practice and you'll soon be a renowned swordsman.\
 The next tutorial covers directional defence, which is one of the most important elements of Mount&Blade combat.\
 You can press the Tab key at any time to return to the tutorial menu."),

  ("tutorial_3_msg_1","This tutorial is intended to give you an overview of parrying and defence without a shield.\
 Parrying attacks with your weapon is a little bit more difficult than blocking them with a shield.\
 When you are defending with a weapon, you are only protected from one direction, the direction in which your weapon is set.\
 If you are blocking upwards, you will parry any overhead swings coming against you, but you will not stop thrusts or attacks to your sides.\
 Either of these attacks would still be able to hit you.\
 That's why, in order to survive without a shield, you must learn directional defence.\
 Go pick up up the quarterstaff now to begin practice."),
  ("tutorial_3_msg_2","By default, the direction in which you defend (by clicking and holding your right mouse button) is determined by the attack direction of your closest opponent.\
 For example, if your opponent is readying a thrust attack, pressing and holding the right mouse button will parry thrust attacks, but not side or overhead attacks.\
 You must watch your opponent carefully and only initiate your parry AFTER the enemy starts to attack.\
 If you start BEFORE he readies an attack, you may parry the wrong way altogether!\
 Now it's time for you to move on to the next room, where you'll have to defend yourself against an armed opponent.\
 Your task is to defend yourself successfully for thirty seconds with no equipment other than a simple quarterstaff.\
 Your quarterstaff's attacks are disabled for this tutorial, so don't worry about attacking and focus on your defence instead.\
 Move on to the next room when you are ready to initiate the fight."),
  ("tutorial_3_msg_3","Press and hold down the right mouse button to defend yourself with your staff after your opponent starts his attack.\
 Try to remain standing for thirty seconds. You have {reg3} seconds to go."),
  ("tutorial_3_msg_4","Well done, you've succeeded this trial!\
 Now you will be pitted against a more challenging opponent that will make things more difficult for you.\
 Move on to the next room when you're ready to face him."),
  ("tutorial_3_msg_5","Press and hold down the right mouse button to defend yourself with your staff after your opponent starts his attack.\
 Try to remain standing for thirty seconds. You have {reg3} seconds to go."),
  ("tutorial_3_msg_6","Congratulations, you still stand despite the enemy's best efforts.\
 The time has now come to attack as well as defend.\
 Approach the door and press the F key when you see the word 'Go'."),

  ("tutorial_3_2_msg_1","Your staff's attacks have been enabled again. Your first opponent is waiting in the next room.\
 Defeat him by a combination of attack and defence."),
  ("tutorial_3_2_msg_2","Defeat your opponent with your quarterstaff."),
  ("tutorial_3_2_msg_3","Excellent. Now the only thing standing in your way is one last opponent.\
 He is in the next room. Move in and knock him down."),
  ("tutorial_3_2_msg_4","Defeat your opponent with your quarterstaff."),
  ("tutorial_3_2_msg_5","Well done! In this tutorial you have learned how to fight ably without a shield.\
 Train hard and train well, and no one shall be able to lay a stroke on you.\
 In the next tutorial you may learn horseback riding and cavalry combat.\
 You can press the Tab key at any time to return to the tutorial menu."),

  ("tutorial_4_msg_1","Welcome to the fourth tutorial.\
 In this sequence you'll learn about riding a horse and how to perform various martial exercises on horseback.\
 We'll start by getting you mounted up.\
 Approach the horse, and press the 'F' key when you see the word 'Mount'."),
  ("tutorial_4_msg_2","While on horseback, the WASD keys control your horse's movement, not your own.\
 Ride your horse and try to follow the yellow flag around the course.\
 When you reach the flag, it will move to the next waypoint on the course until you reach the finish."),
  ("tutorial_4_msg_3","Very good. Next we'll cover attacking enemies from horseback. Approach the yellow flag now."),
  ("tutorial_4_msg_4","Draw your sword (using the mouse wheel) and destroy the four targets.\
 Try hitting the dummies as you pass them at full gallop -- this provides an extra challenge,\
 but the additional speed added to your blow will allow you to do more damage.\
 The easiest way of doing this is by pressing and holding the left mouse button until the right moment,\
 releasing it just before you pass the target."),
  ("tutorial_4_msg_5","Excellent work. Now let us try some target shooting from horseback. Go near the yellow flag now."),
  ("tutorial_4_msg_6","Locate the archery target beside the riding course and shoot it three times with your bow.\
 Although you are not required to ride while shooting, it's recommended that you try to hit the target at various speeds and angles\
 to get a feel for how your horse's speed and course affects your aim."),
  ("tutorial_4_msg_7","Congratulations, you have finished this tutorial.\
 You can press the Tab key at any time to return to the tutorial menu."),
# Ryan END

  ("tutorial_5_msg_1","TODO: Follow order to the flag"),
  ("tutorial_5_msg_2","TODO: Move to the flag, keep your units at this position"),
  ("tutorial_5_msg_3","TODO: Move to the flag to get the archers"),
  ("tutorial_5_msg_4","TODO: Move archers to flag1, infantry to flag2"),
  ("tutorial_5_msg_5","TODO: Enemy is charging. Fight!"),
  ("tutorial_5_msg_6","TODO: End of battle."),

  ("trainer_help_1", "This is a training ground where you can learn the basics of the game. Use A, S, D, W keys to move and the mouse to look around."),
  ("trainer_help_2", "To speak with the trainer, go near him, look at him and press the 'F' key when you see the word 'Talk' under his name.\
 When you wish to leave this or any other area or retreat from a battle, you can press the TAB key."),

  ("custom_battle_1", "Captain Malvogil and his Gondor company intercepted Harad reinforcement group.\
 Shouting out his warcry, he spurs his horse forward, and leads his loyal men to a fierce battle."),
  ("custom_battle_2", "Lord Mleza is leading a patrol of horsemen and archers\
 in search of a group of bandits who plundered a caravan and ran away to the hills.\
 Unfortunately the bandits have recently met two other large groups who want a share of their booty,\
 and spotting the new threat, they decide to combine their forces."),
  ("custom_battle_3", "Lord Grimbold of Rohan is leading the last defence of the walls against an army if Isengard.\
 Now, as the besiegers prepare for a final assault on the walls, he must hold the walls with courage and bright steel."),
  ("custom_battle_4", "When the scouts inform Lord Grainwad of the approach of an Rhun war band,\
 he decides to quickly prepare the defences of his camp and try to hold against superior numbers."),
  ("custom_battle_5", "Captain Ugluk has brought his fierce orksies into the west with the promise of plunder.\
 If he can make this dwarf stronghold fall to him today, his masters in Barad-Dur will be mightily pleased."),
  ("custom_battle_6", "Grishnakh and his orc raider squad were as keen as possible in escaping Elven patrols.\
 But one's good fortunes may not last forever, and it seems like filthy paleskins will have their share now."),
  ("custom_battle_7", "Cosairs have set up their camp on the shores of Gondor! How dare they.\
 Let us strike them before they get reinforcements and drive them off into the sea, where they belong."),
 
  ("finished", "(Finished)"),

  ("delivered_damage", "Delivered {reg60} damage."),
  ("archery_target_hit", "Distance: {reg61} yards. Score: {reg60}"),
  
  ("use_baggage_for_inventory","Use your baggage to access your inventory during battle (it's at your starting position)."),
##  ("cant_leave_now","Can't leave the area now."),
  ("cant_use_inventory_now","Can't access inventory now."),
  ("cant_use_inventory_arena","Can't access inventory in the arena."),
  ("cant_use_inventory_disguised","Can't access inventory while you're disguised."),
  ("cant_use_inventory_tutorial","Can't access inventory in the training camp."),
  ("1_denar", "1 Resource Pts."),
  ("reg1_denars", "{reg1} Resource Pts."),

  # Eglish calendar TLD -- mtarini
#  ("january_reg1_reg2", "T.A. {reg2}, January {reg1}"),
#  ("february_reg1_reg2", "T.A. {reg2}, February {reg1}"),
#  ("march_reg1_reg2", "T.A. {reg2}, March {reg1}"),
#  ("april_reg1_reg2", "T.A. {reg2}, April {reg1}"),
#  ("may_reg1_reg2", "T.A. {reg2}, May {reg1}"),
#  ("june_reg1_reg2", "T.A. {reg2}, June {reg1}"),
#  ("july_reg1_reg2", "T.A. {reg2}, July {reg1}"),
#  ("august_reg1_reg2", "T.A. {reg2}, August {reg1}"),
#  ("september_reg1_reg2", "T.A. {reg2}, September {reg1}"),
#  ("october_reg1_reg2", "T.A. {reg2}, October {reg1}"),
#  ("november_reg1_reg2", "T.A. {reg2}, November {reg1}"),
#  ("december_reg1_reg2", "T.A. {reg2}, December {reg1}"),
 

# TLD -- Quenya name (Steward's Reckoning)  MONTHS -- mtarini
#  
  ("january_reg1_reg2",   "T.A.{reg2}, Narvinyë {reg1} (Jan)"),
  ("february_reg1_reg2",  "T.A.{reg2}, Nénimë {reg1} (Feb)"),
  ("march_reg1_reg2",     "T.A.{reg2}, Súlìmë {reg1} (Mar)"),
  ("april_reg1_reg2",     "T.A.{reg2}, Víressë {reg1 (Apr)}"),
  ("may_reg1_reg2",       "T.A.{reg2}, Lótessë {reg1} (May)"),
  ("june_reg1_reg2",      "T.A.{reg2}, Náríë {reg1} (Jun)"),
  ("july_reg1_reg2",      "T.A.{reg2}, Cermië {reg1} (Jul)"),
  ("august_reg1_reg2",    "T.A.{reg2}, Urimë {reg1} (Aug)"),
  ("september_reg1_reg2", "T.A.{reg2}, Yavannië {reg1} (Sep)"),
  ("october_reg1_reg2",   "T.A.{reg2}, Narquelië {reg1} (Oct)"),
  ("november_reg1_reg2",  "T.A.{reg2}, Hísimë {reg1} (Nov)"),
  ("december_reg1_reg2",  "T.A.{reg2}, Ringarë {reg1} (Dec)"),

# TLD -- Quenya name (Steward's Reckoning) SPECIAL DAYS-- mtarini
  ("calendar_spec_day_1", "T.A.{reg2}, Yestarë (First Day)"),
  ("calendar_spec_day_2", "T.A.{reg2}, Tuilérë (Spring Day)"),
  ("calendar_spec_day_3", "T.A.{reg2}, Loëndë (Midyear's Day)"),
  ("calendar_spec_day_4", "T.A.{reg2}, Yáviérë (Harvest Day)"),
  ("calendar_spec_day_5", "T.A.{reg2}, Mettarë (Last Day)"),
  
  
##  ("you_approach_town","You approach the town of "),
##  ("you_are_in_town","You are in the town of "),
##  ("you_are_in_castle","You are at the castle of "),
##  ("you_sneaked_into_town","You have sneaked into the town of "),

  ("town_nighttime"," It is late at night and honest folk have abandoned the streets."),
  ("door_locked","The door is locked."),
  ("castle_is_abondened","The castle seems to be unoccupied."),
  ("town_is_abondened","The town has no garrison defending it."),
  ("place_is_occupied_by_player","The place is held by your own troops."),
  ("place_is_occupied_by_enemy", "The place is held by hostile troops."),
  ("place_is_occupied_by_friendly", "The place is held by friendly troops."),

  ("do_you_want_to_retreat", "Are you sure you want to retreat?"),
  ("give_up_fight", "Give up the fight?"),
  ("do_you_wish_to_leave_tutorial", "Do you wish to leave the tutorial?"),
  ("do_you_wish_to_surrender", "Do you wish to surrender?"),
  ("can_not_retreat", "Can't retreat, there are enemies nearby!"),
##  ("can_not_leave", "Can't leave. There are enemies nearby!"),

  ("s1_joined_battle_enemy", "{s1} has joined the battle on the enemy side."),
  ("s1_joined_battle_friend", "{s1} has joined the battle on your side."),

#  ("entrance_to_town_forbidden","It seems that the town guards have been warned of your presence and you won't be able to enter the town unchallenged."),
  ("entrance_to_town_forbidden","The town guards are on the lookout for intruders and it seems that you won't be able to pass through the gates unchallenged."),
  ("sneaking_to_town_impossible","The town guards are alarmed. You wouldn't be able to sneak through that gate no matter how well you disguised yourself."),

  ("battle_won", "You have won the battle!"),
  ("battle_lost", "You have lost the battle!"),

  ("attack_walls_success", "After a bloody fight, your brave soldiers manage to claim the walls from the enemy."),
  ("attack_walls_failure", "Your soldiers fall in waves as they charge the walls, and the few who remain alive soon rout and run away, never to be seen again."),
  ("attack_walls_continue", "A bloody battle ensues and both sides fight with equal valour. Despite the efforts of your troops, the castle remains in enemy hands."),

  ("order_attack_success", "Your men fight bravely and defeat the enemy."),
  ("order_attack_failure", "You watch the battle in despair as the enemy cuts your soldiers down, then easily drives off the few ragged survivors."),
  ("order_attack_continue", "Despite an extended skirmish, your troops were unable to win a decisive victory."),

  ("join_order_attack_success", "Your men fight well alongside your allies, sharing in the glory as your enemies are beaten."),
  ("join_order_attack_failure", "You watch the battle in despair as the enemy cuts your soldiers down, then easily drives off the few ragged survivors."),
  ("join_order_attack_continue", "Despite an extended skirmish, neither your troops nor your allies were able to win a decisive victory over the enemy."),

  ("siege_defender_order_attack_success", "The men of the garrison hold their walls with skill and courage, breaking the enemy assault and skillfully turning the defeat into a full-fledged rout."),
  ("siege_defender_order_attack_failure", "The assault quickly turns into a bloodbath. Valiant efforts are for naught; the overmatched garrison cannot hold the walls, and the enemy puts every last defender to the sword."),
  ("siege_defender_order_attack_continue", "Repeated, bloody attempts on the walls fail to gain any ground, but too many enemies remain for the defenders to claim a true victory. The siege continues."),


  ("hero_taken_prisoner", "{s1} of {s3} has been taken prisoner by {s2}."),
  ("hero_freed", "{s1} of {s3} has been freed from captivity by {s2}."),
  ("center_captured", "{s2} have taken {s1} from {s3}."),

  ("troop_relation_increased", "Your relation with {s1} has increased from {reg1} to {reg2}."),
  ("troop_relation_detoriated", "Your relation with {s1} has deteriorated from {reg1} to {reg2}."),
  ("faction_relation_increased", "Your relation with {s1} has increased from {reg1} to {reg2}."),
  ("faction_relation_detoriated", "Your relation with {s1} has deteriorated from {reg1} to {reg2}."),
  
  ("party_gained_morale", "Your party gains {reg1} morale."),
  ("party_lost_morale",   "Your party loses {reg1} morale."),

  ("qst_follow_spy_noticed_you", "The spy has spotted you! He's making a run for it!"),
  ("father", "father"),
  ("husband", "husband"),
  ("wife", "wife"),
  ("daughter", "daughter"),
  ("mother", "mother"),
  ("son", "son"),
  ("brother", "brother"),
  ("sister", "sister"),
  ("he", "He"),
  ("she", "She"),
  ("s3s_s2", "{s3}'s {s2}"),
  ("s5_is_s51", "{s5} is {s51}."),
  ("s5_is_the_ruler_of_s51", "{s5} is the ruler of {s51}. "),
  ("s5_is_a_nobleman_of_s6", "{s5} is a nobleman of {s6}. "),
##  ("your_debt_to_s1_is_changed_from_reg1_to_reg2", "Your debt to {s1} is changed from {reg1} to {reg2}."),

  ("relation_mnus_100", "Vengeful"), # -100..-94
  ("relation_mnus_90",  "Vengeful"),  # -95..-84
  ("relation_mnus_80",  "Vengeful"),
  ("relation_mnus_70",  "Hateful"),
  ("relation_mnus_60",  "Hateful"),
  ("relation_mnus_50",  " Hostile"),
  ("relation_mnus_40",  "  Angry"),
  ("relation_mnus_30",  "    Resentful"),
  ("relation_mnus_20",  "      Grumbling"),
  ("relation_mnus_10",  "        Suspicious"),
  ("relation_plus_0",   "         Indifferent"),# -5...4
  ("relation_plus_10",  "          Cooperative"), # 5..14
  ("relation_plus_20",  "           Welcoming"),
  ("relation_plus_30",  "            Favorable"),
  ("relation_plus_40",  "             Supportive"),
  ("relation_plus_50",  "              Friendly"),
  ("relation_plus_60",  "               Gracious"),
  ("relation_plus_70",  "                 Fond"),
  ("relation_plus_80",  "                  Loyal"),
  ("relation_plus_90",  "                   Devoted"),

  ("relation_mnus_100_ns", "{s60} is vengeful towards you."), # -100..-94
  ("relation_mnus_90_ns",  "{s60} is vengeful towards you."),  # -95..-84
  ("relation_mnus_80_ns",  "{s60} is vengeful towards you."),
  ("relation_mnus_70_ns",  "{s60} is hateful towards you."),
  ("relation_mnus_60_ns",  "{s60} is hateful towards you."),
  ("relation_mnus_50_ns",  "{s60} is hostile towards you."),
  ("relation_mnus_40_ns",  "{s60} is angry towards you."),
  ("relation_mnus_30_ns",  "{s60} is resentful against you."),
  ("relation_mnus_20_ns",  "{s60} is grumbling against you."),
  ("relation_mnus_10_ns",  "{s60} is suspicious towards you."),
  ("relation_plus_0_ns",   "{s60} is indifferent against you."),# -5...4
  ("relation_plus_10_ns",  "{s60} is cooperative towards you."), # 5..14
  ("relation_plus_20_ns",  "{s60} is welcoming towards you."),
  ("relation_plus_30_ns",  "{s60} is favorable to you."),
  ("relation_plus_40_ns",  "{s60} is supportive to you."),
  ("relation_plus_50_ns",  "{s60} is friendly to you."),
  ("relation_plus_60_ns",  "{s60} is gracious to you."),
  ("relation_plus_70_ns",  "{s60} is fond of you."),
  ("relation_plus_80_ns",  "{s60} is loyal to you."),
  ("relation_plus_90_ns",  "{s60} is devoted to you."),
  
  ("relation_reg1", " Relation: {reg1}"),

  ("center_relation_mnus_100", "The populace hates you with a passion"), # -100..-94
  ("center_relation_mnus_90",  "The populace hates you intensely"), # -95..-84
  ("center_relation_mnus_80",  "The populace hates you strongly"), 
  ("center_relation_mnus_70",  "The populace hates you"), 
  ("center_relation_mnus_60",  "The populace is hateful to you"), 
  ("center_relation_mnus_50",  "The populace is extremely hostile to you"), 
  ("center_relation_mnus_40",  "The populace is very hostile to you"), 
  ("center_relation_mnus_30",  "The populace is hostile to you"), 
  ("center_relation_mnus_20",  "The populace is against you"), 
  ("center_relation_mnus_10",  "The populace is opposed to you"), 
  ("center_relation_plus_0",   "The populace is indifferent to you"), 
  ("center_relation_plus_10",  "The populace is acceptive to you"), 
  ("center_relation_plus_20",  "The populace is cooperative to you"), 
  ("center_relation_plus_30",  "The populace is somewhat supportive to you"), 
  ("center_relation_plus_40",  "The populace is supportive to you"), 
  ("center_relation_plus_50",  "The populace is very supportive to you"), 
  ("center_relation_plus_60",  "The populace is loyal to you"), 
  ("center_relation_plus_70",  "The populace is highly loyal to you"), 
  ("center_relation_plus_80",  "The populace is devoted to you"), 
  ("center_relation_plus_90",  "The populace is fiercely devoted to you"),

  ("town_prosperity_0",   "The poverty of the town of {s60} is unbearable"),
  ("town_prosperity_10",   "The squalorous town of {s60} is all but deserted."),
  ("town_prosperity_20",   "The town of {s60} looks a wretched, desolate place."),
  ("town_prosperity_30",   "The town of {s60} looks poor and neglected."),
  ("town_prosperity_40",   "The town of {s60} appears to be struggling."),
  ("town_prosperity_50",   "The town of {s60} seems unremarkable."),
  ("town_prosperity_60",   "The town of {s60} seems to be flourishing."),
  ("town_prosperity_70",   "The prosperous town of {s60} is bustling with activity."),
  ("town_prosperity_80",   "The town of {s60} looks rich and well-maintained."),
  ("town_prosperity_90",   "The town of {s60} is opulent and crowded with well-to-do people."),
  ("town_prosperity_100",  "The glittering town of {s60} openly flaunts its great wealth."),

  ("village_prosperity_0",   "The poverty of the village of {s60} is unbearable."),
  ("village_prosperity_10",  "The village of {s60} looks wretchedly poor and miserable."),
  ("village_prosperity_20",  "The village of {s60} looks very poor and desolate."),
  ("village_prosperity_30",  "The village of {s60} looks poor and neglected."),
  ("village_prosperity_40",  "The village of {s60} appears to be somewhat poor and struggling."),
  ("village_prosperity_50",  "The village of {s60} seems unremarkable."),
  ("village_prosperity_60",  "The village of {s60} seems to be flourishing."),
  ("village_prosperity_70",  "The village of {s60} appears to be thriving."),
  ("village_prosperity_80",  "The village of {s60} looks rich and well-maintained."),
  ("village_prosperity_90",  "The village of {s60} looks very rich and prosperous."),
  ("village_prosperity_100", "The village of {s60}, surrounded by vast, fertile fields, looks immensely rich."),

  ("war_report_minus_4",   "we are about to lose the war"),
  ("war_report_minus_3",   "the situation looks bleak"),
  ("war_report_minus_2",   "things aren't going too well for us"),
  ("war_report_minus_1",   "we can still win the war if we rally"),
  ("war_report_0",   "we are evenly matched with the enemy"),
  ("war_report_plus_1",   "we have a fair chance of winning the war"),
  ("war_report_plus_2",   "things are going quite well"),
  ("war_report_plus_3",   "we should have no difficulty defeating them"),
  ("war_report_plus_4",   "we are about to win the war"),


  ("persuasion_summary_very_bad", "You try your best to persuade {s50},\
 but none of your arguments seem to come out right. Every time you start to make sense,\
 you seem to say something entirely wrong that puts you off track.\
 By the time you finish speaking you've failed to form a single coherent point in your own favour,\
 and you realise that all you've done was dig yourself deeper into a hole.\
 Unsurprisingly, {s50} does not look impressed."),
  ("persuasion_summary_bad",      "You try to persuade {s50}, but {reg51?she:he} outmanoeuvres you from the very start.\
 Even your best arguments sound hollow to your own ears. {s50}, likewise,\
 has not formed a very high opinion of what you had to say."),
  ("persuasion_summary_average",  "{s50} turns out to be a skilled speaker with a keen mind,\
 and you can't seem to bring forth anything concrete that {reg51?she:he} cannot counter with a rational point.\
 In the end, neither of you manage to gain any ground in this discussion."),
  ("persuasion_summary_good",     "Through quick thinking and smooth argumentation, you manage to state your case well,\
 forcing {s50} to concede on several points. However, {reg51?she:he} still expresses doubts about your request."),
  ("persuasion_summary_very_good","You deliver an impassioned speech that echoes through all listening ears like poetry.\
 The world itself seems to quiet down in order to hear you better .\
 The inspiring words have moved {s50} deeply, and {reg51?she:he} looks much more well-disposed towards helping you."),
  

# meet_spy_in_enemy_town quest secret sentences
  ("secret_sign_1",  "The armoire dances at midnight..."),
  ("secret_sign_2",  "I am selling these fine Khergit tapestries. Would you like to buy some?"),
  ("secret_sign_3",  "The friend of a friend sent me..."),
  ("secret_sign_4",  "The wind blows hard from the east and the river runs red..."),
  
  ("countersign_1",  "But does he dance for the dresser or the candlestick?"),
  ("countersign_2",  "Yes I would, do you have any in blue?"),
  ("countersign_3",  "But, my friend, your friend's friend will never have a friend like me."),
  ("countersign_4",  "Have you been sick?"),

# Names  
  ("name_1",  "Albard"),
  ("name_2",  "Euscarl"),
  ("name_3",  "Sigmar"),
  ("name_4",  "Talesqe"),
  ("name_5",  "Ritmand"),
  ("name_6",  "Aels"),
  ("name_7",  "Raurqe"),
  ("name_8",  "Bragamus"),
  ("name_9",  "Taarl"),
  ("name_10", "Ramin"),
  ("name_11", "Shulk"),
  ("name_12", "Putar"),
  ("name_13", "Tamus"),
  ("name_14", "Reichad"),
  ("name_15", "Walcheas"),
  ("name_16", "Rulkh"),
  ("name_17", "Marlund"),
  ("name_18", "Auguryn"),
  ("name_19", "Daynad"),
  ("name_20", "Joayah"),
  ("name_21", "Ramar"),
  ("name_22", "Caldaran"),
  ("name_23", "Brabas"),
  ("name_24", "Kundrin"),
  ("name_25", "Pechnak"),

# Surname
  ("surname_1",  "{s50} of Uxhal"),
  ("surname_2",  "{s50} of Wercheg"),
  ("surname_3",  "{s50} of Reyvadin"),
  ("surname_4",  "{s50} of Suno"),
  ("surname_5",  "{s50} of Jelkala"),
  ("surname_6",  "{s50} of Veluca"),
  ("surname_7",  "{s50} of Halmar"),
  ("surname_8",  "{s50} of Curaw"),
  ("surname_9",  "{s50} of Sargoth"),
  ("surname_10", "{s50} of Tihr"),
  ("surname_11", "{s50} of Zendar"),
  ("surname_12", "{s50} of Rivacheg"),
  ("surname_13", "{s50} of Wercheg"),
  ("surname_14", "{s50} of Ehlerdag"),
  ("surname_15", "{s50} of Yaragar"),
  ("surname_16", "{s50} of Burglen"),
  ("surname_17", "{s50} of Shapeshte"),
  ("surname_18", "{s50} of Hanun"),
  ("surname_19", "{s50} of Saren"),
  ("surname_20", "{s50} of Tosdhar"),
  ("surname_21", "{s50} the Long"),
  ("surname_22", "{s50} the Gaunt"),
  ("surname_23", "{s50} Silkybeard"),
  ("surname_24", "{s50} the Sparrow"),
  ("surname_25", "{s50} the Pauper"),
  ("surname_26", "{s50} the Scarred"),
  ("surname_27", "{s50} the Fair"),
  ("surname_28", "{s50} the Grim"),
  ("surname_29", "{s50} the Red"),
  ("surname_30", "{s50} the Black"),
  ("surname_31", "{s50} the Tall"),
  ("surname_32", "{s50} Star-Eyed"),
  ("surname_33", "{s50} the Fearless"),
  ("surname_34", "{s50} the Valorous"),
  ("surname_35", "{s50} the Cunning"),
  ("surname_36", "{s50} the Coward"),
  ("surname_37", "{s50} Bright"),
  ("surname_38", "{s50} the Quick"),
  ("surname_39", "{s50} the Minstrel"),
  ("surname_40", "{s50} the Bold"),
  ("surname_41", "{s50} Hot-Head"),
  
  ("surnames_end", "surnames_end"),
  

  ("number_of_troops_killed_reg1", "Number of troops killed: {reg1}"),
  ("number_of_troops_wounded_reg1", "Number of troops wounded: {reg1}"),
  ("number_of_own_troops_killed_reg1", "Number of friendly troops killed: {reg1}"),
  ("number_of_own_troops_wounded_reg1", "Number of friendly troops wounded: {reg1}"),

  ("retreat", "Retreat!"),
  ("siege_continues", "Fighting Continues..."),
  ("casualty_display", "Your casualties: {s10}^Enemy casualties: {s11}{s12}"),
  ("casualty_display_hp", "^You were wounded for {reg1} hit points."),

# Quest log texts
  ("quest_log_updated", "Quest log has been updated..."),

  ("banner_selection_text", "You have been awarded the right to carry a banner.\
 Your banner will signify your status and bring you honour. Which banner do you want to choose?"),


# Retirement Texts: s7=village name; s8=castle name; s9=town name
  ("retirement_text_1", "Only too late do you realise that your money won't last.\
 It doesn't take you long to fritter away what little you bothered to save,\
 and you fare poorly in several desperate attempts to start adventuring again.\
 You end up a beggar in {s9}, living on alms and the charity of the church."),
  ("retirement_text_2", "Only too late do you realise that your money won't last.\
 It doesn't take you long to fritter away what little you bothered to save.\
 Once every denar has evaporated in your hands you are forced to start a life of crime in the backstreets of {s9},\
 using your skills to eke out a living robbing coppers from women and poor townsmen."),
  ("retirement_text_3", "Only too late do you realise that your money won't last.\
 It doesn't take you long to fritter away what little you bothered to save,\
 and you end up a penniless drifter, going from tavern to tavern\
 blagging drinks from indulgent patrons by regaling them with war stories that no one ever believes."),
  ("retirement_text_4", "The silver you've saved doesn't last long,\
 but you manage to put together enough to buy some land near the village of {s7}.\
 There you become a free farmer, and you soon begin to attract potential {wives/husbands}.\
 In time the villagers come to treat you as their local hero.\
 You always receive a place of honour at feasts, and your exploits are told and retold in the pubs and taverns\
 so that the children may keep a memory of you for ever and ever."),
  ("retirement_text_5", "The silver you've saved doesn't last long,\
 but it's enough to buy a small tavern in {s9}. Although the locals are wary of you at first,\
 they soon accept you into their midst. In time your growing tavern becomes a popular feasthall and meeting place.\
 People come for miles to eat or stay there due to your sheer renown and the epic stories you tell of your adventuring days."),
  ("retirement_text_6", "You've saved wisely throughout your career,\
 and now your silver and your intelligence allow you to make some excellent investments to cement your future.\
 After buying several shops and warehouses in {s9}, your shrewdness turns you into one of the most prominent merchants in town,\
 and you soon become a wealthy {man/woman} known as much for your trading empire as your exploits in battle."),
  ("retirement_text_7", "As a landed noble, however minor, your future is all but assured.\
 You settle in your holdfast at {s7}, administrating the village and fields,\
 adjudicating the local courts and fulfilling your obligations to your liege lord.\
 Occasionally your liege calls you to muster and command in his campaigns, but these stints are brief,\
 and you never truly return to the adventuring of your younger days. You have already made your fortune.\
 With your own hall and holdings, you've few wants that your personal wealth and the income of your lands cannot afford you."),
  ("retirement_text_8", "There is no question that you've done very well for yourself.\
 Your extensive holdings and adventuring wealth are enough to guarantee you a rich and easy life for the rest of your days.\
 Retiring to your noble seat in {s8}, you exchange adventure for politics,\
 and you soon establish yourself as a considerable power in your liege lord's kingdom.\
 With intrigue to busy yourself with, your own forests to hunt, a hall to feast in and a hundred fine war stories to tell,\
 you have little trouble making the best of the years that follow."),
  ("retirement_text_9", "As a reward for your competent and loyal service,\
 your liege lord decrees that you be given a hereditary title, joining the major nobility of the realm.\
 Soon you complete your investitute as baron of {s7}, and you become one of your liege's close advisors\
 and adjutants. Your renown garners you much subtle pull and influence as well as overt political power.\
 Now you spend your days playing the games of power, administering your great fiefs,\
 and recounting the old times of adventure and glory."),
  ("retirement_text_10", "Though you started from humble beginnings, your liege lord holds you in high esteem,\
 and a ripple of shock passes through the realm when he names you to the hereditary title of {count/countess} of {s9}.\
 Vast fiefs and fortunes are now yours to rule. You quickly become your liege's most trusted advisor,\
 almost his equal and charged with much of the running of his realm,\
 and you sit a throne in your own splendourous palace as one of the most powerful figures in Calradia."),


#NPC companion changes begin


# Objectionable actions

# humanitarian
  ("loot_village", "attack innocent villagers"),
  ("steal_from_villagers", "steal from poor villagers"),
  ("rob_caravan", "rob a merchant caravan"), # possibly remove
  ("sell_slavery", "sell people into slavery"),

# egalitarian
  ("men_hungry", "run out of food"), ##Done - simple triggers
  ("men_unpaid", "not be able to pay the men"),
#  ("party_crushed", "get ourselves slaughtered"), ##Done - game menus
  ("excessive_casualties", "turn every battle into a bloodbath for our side"),

# chivalric
  ("surrender", "surrender to the enemy"), ##Done - game menus
  ("flee_battle", "run from battle"), ##Done - game menus
  ("pay_bandits", "pay off common bandits"),

# honest
  ("fail_quest", "fail a quest which we undertook on word of honour"),

# quest-related strings
  ("squander_money", "squander money given to us in trust"),
  ("murder_merchant", "involve ourselves in cold-blooded murder"),
  ("round_up_serfs", "round up serfs on behalf of some noble"),


# Fates suffered by companions in battle
  ("battle_fate_1", "We were separated in the heat of battle"),
  ("battle_fate_2", "I was wounded and left for dead"),
  ("battle_fate_3", "I was knocked senseless by the enemy"),
  ("battle_fate_4", "I was taken and held for ransom"),
  ("battle_fate_5", "I got captured, but later managed to escape"),


# strings for opinion
  ("npc_morale_report", "I'm {s6} your choice of companions, {s7} your style of leadership, and {s8} the general state of affairs"), 
  ("happy", "happy about"),
  ("content", "content with"),
  ("concerned", "concerned about"),
  ("not_happy", "not at all happy about"),
  ("miserable", "downright appalled at"),  


  ("morale_reg1",    " Morale: {reg1}"),
  ("bar_enthusiastic", "                   Enthusiastic"),  
  ("bar_content",      "              Content"),
  ("bar_weary",        "          Weary"),
  ("bar_disgruntled",  "     Disgruntled"),
  ("bar_miserable",    "  Miserable"),  


#other strings
  ("here_plus_space", "here "),

#NPC strings
#npc1 = Mablung
#npc2 = Gondor NPC
#npc3 = Eowyn  
#npc4 = Rohan NPC
#npc5 = Glorfindel
#npc6 = Ulfas
#npc7 = Dwarf NPC
#npc8 = Beorn NPC
#npc9 = Gulm
#npc10 = Durgash
#npc11 = Ufthak
#npc12 = Gorbag
#npc13 = Harad NPC
#npc14 = Umbar NPC
#npc15 = Moria NPC
#npc16 = Rhun NPC
  
  ("npc1_intro", "Hail, warrior."),
  ("npc2_intro", "Good day to you!"),
  ("npc3_intro", "Good day to you!"),
  ("npc4_intro", "Good day to you!"),
  ("npc5_intro", "Hail {playername}. What can I do for you?"),
  ("npc6_intro", "Hail, warrior."),
  ("npc7_intro", "Good day to you!"),
  ("npc8_intro", "Good day to you!"),
  ("npc9_intro", "You!"),
  ("npc10_intro", "Good day to you!"),
  ("npc11_intro", "You!"),
  ("npc12_intro", "Good day to you!"),
  ("npc13_intro", "Good day to you!"),
  ("npc14_intro", "Good day to you!"),
  ("npc15_intro", "Good day to you!"),
  ("npc16_intro", "Good day to you!"),

  ("npc1_intro_response_1", "Hello. What's your story?"),
  ("npc2_intro_response_1", "Hello. What's your story?"),
  ("npc3_intro_response_1", "Hello. What's your story?"),
  ("npc4_intro_response_1", "Hello. What's your story?"),
  ("npc5_intro_response_1", "Hail Glorfindel! It may be presumptuous of me to ask, but my company could use your skill in the coming battles. Any help you can offer would be greatly valued."),
  ("npc6_intro_response_1", "Hello. What's your story?"),
  ("npc7_intro_response_1", "Hello. What's your story?"),
  ("npc8_intro_response_1", "Hello. What's your story?"),
  ("npc9_intro_response_1", "Hello. What's your story?"),
  ("npc10_intro_response_1", "Hello. What's your story?"),
  ("npc11_intro_response_1", "Hello. What's your story?"),
  ("npc12_intro_response_1", "Hello. What's your story?"),
  ("npc13_intro_response_1", "Hello. What's your story?"),
  ("npc14_intro_response_1", "Hello. What's your story?"),
  ("npc15_intro_response_1", "Hello. What's your story?"),
  ("npc16_intro_response_1", "Hello. What's your story?"),

  ("npc1_intro_response_2", "Never mind."),
  ("npc2_intro_response_2", "Never mind."),
  ("npc3_intro_response_2", "Never mind."),
  ("npc4_intro_response_2", "Never mind."),
  ("npc5_intro_response_2", "Never mind."),
  ("npc6_intro_response_2", "Never mind."),
  ("npc7_intro_response_2", "Never mind."),
  ("npc8_intro_response_2", "Never mind."),
  ("npc9_intro_response_2", "They call me Gulm! I have gutted my sergeant and his snagas now hunt for me. I would come with you and hunt men in the south while the snagas of Isengard gnash their teeth."),
  ("npc10_intro_response_2", "Never mind."),
  ("npc11_intro_response_2", "They call me Ufthak! My unit is dead and gone to worms. If you need a warrior, it is me."),
  ("npc12_intro_response_2", "Never mind."),
  ("npc13_intro_response_2", "Never mind."),
  ("npc14_intro_response_2", "Never mind."),
  ("npc15_intro_response_2", "Never mind."),
  ("npc16_intro_response_2", "Never mind."),

#backstory intro
  ("npc1_backstory_a", "I have recently recovered from a wound and am just now returned from the houses of healing. My commander has bid me rest longer and my company has returned to service without me, if you would have me  I will ride with you for a time and hunt the orcs who slip past the great river. I have no stomach for beds and bandages."),
  ("npc2_backstory_a", "It's a long story..."),
  ("npc3_backstory_a", "It's a long story..."),
  ("npc4_backstory_a", "It's a long story..."),
  ("npc5_backstory_a", "It's a long story..."),
  ("npc6_backstory_a", "I have recently recovered from wounds sustained in an orc raid and am just now returned from the care of the healers. It would be long before I could rejoin my unit as they are far afield. If you wish I could seek reassignment with you for a time and so find orcs to slay all the sooner."),
  ("npc7_backstory_a", "It's a long story..."),
  ("npc8_backstory_a", "It's a long story..."),
  ("npc9_backstory_a", "You should know that I am a slayer in the service of the White Hand. What there is to know of killing men, I know it."),
  ("npc10_backstory_a", "It's a long story..."),
  ("npc11_backstory_a", "You should know that I am a slayer in service to the Great Eye. I will kill for you!"),
  ("npc12_backstory_a", "It's a long story..."),
  ("npc13_backstory_a", "It's a long story..."),
  ("npc14_backstory_a", "It's a long story..."),
  ("npc15_backstory_a", "It's a long story..."),
  ("npc16_backstory_a", "It's a long story..."),

#backstory main body
  ("npc1_backstory_b", "You should know that I am a ranger in the service of Faramir. I know much of tracking and scouting and my skill with bow and sword is known to the orc."),
  ("npc2_backstory_b", "...blah blah blah..."),
  ("npc3_backstory_b", "...blah blah blah..."),
  ("npc4_backstory_b", "...blah blah blah..."),
  ("npc5_backstory_b", "...blah blah blah..."),
  ("npc6_backstory_b", "...blah blah blah..."),
  ("npc7_backstory_b", "...blah blah blah..."),
  ("npc8_backstory_b", "...blah blah blah..."),
  ("npc9_backstory_b", "...blah blah blah..."),
  ("npc10_backstory_b", "...blah blah blah..."),
  ("npc11_backstory_b", "...blah blah blah..."),
  ("npc12_backstory_b", "...blah blah blah..."),
  ("npc13_backstory_b", "...blah blah blah..."),
  ("npc14_backstory_b", "...blah blah blah..."),
  ("npc15_backstory_b", "...blah blah blah..."),
  ("npc16_backstory_b", "...blah blah blah..."),

#backstory recruit pitch
  ("npc1_backstory_c", "...and I ended up here."),
  ("npc2_backstory_c", "...and I ended up here."),
  ("npc3_backstory_c", "...and I ended up here."),
  ("npc4_backstory_c", "...and I ended up here."),
  ("npc5_backstory_c", "...and I ended up here."),
  ("npc6_backstory_c", "...and I ended up here."),
  ("npc7_backstory_c", "...and I ended up here."),
  ("npc8_backstory_c", "...and I ended up here."),
  ("npc9_backstory_c", "...and I ended up here."),
  ("npc11_backstory_c", "...and I ended up here."),
  ("npc12_backstory_c", "...and I ended up here."),
  ("npc13_backstory_c", "...and I ended up here."),
  ("npc14_backstory_c", "...and I ended up here."),
  ("npc15_backstory_c", "...and I ended up here."),
  ("npc16_backstory_c", "...and I ended up here."),


### use these if there is a short period of time between the last meeting 
  ("npc1_backstory_later", "I've been turning tricks, whaddaya think? Har-har."),
  ("npc2_backstory_later", "I've been turning tricks, whaddaya think? Har-har."),
  ("npc3_backstory_later", "I've been turning tricks, whaddaya think? Har-har."),
  ("npc4_backstory_later", "I've been turning tricks, whaddaya think? Har-har."),
  ("npc5_backstory_later", "Have you reconsidered? I wish to hunt orc again."),
  ("npc6_backstory_later", "I've been turning tricks, whaddaya think? Har-har."),
  ("npc7_backstory_later", "I've been turning tricks, whaddaya think? Har-har."),
  ("npc8_backstory_later", "I've been turning tricks, whaddaya think? Har-har."),
  ("npc9_backstory_later", "Have you reconsidered? I will serve well."),
  ("npc10_backstory_later", "I've been turning tricks, whaddaya think? Har-har."),
  ("npc11_backstory_later", "Have you reconsidered? I will serve well."),
  ("npc12_backstory_later", "I've been turning tricks, whaddaya think? Har-har."),
  ("npc13_backstory_later", "I've been turning tricks, whaddaya think? Har-har."),
  ("npc14_backstory_later", "I've been turning tricks, whaddaya think? Har-har."),
  ("npc15_backstory_later", "I've been turning tricks, whaddaya think? Har-har."),
  ("npc16_backstory_later", "I've been turning tricks, whaddaya think? Har-har."),


  ("npc1_backstory_response_1", "If you're looking for work, I can use experienced fighters."),
  ("npc2_backstory_response_1", "If you're looking for work, I can use experienced fighters."),
  ("npc3_backstory_response_1", "If you're looking for work, I can use experienced fighters."),
  ("npc4_backstory_response_1", "If you're looking for work, I can use experienced fighters."),
  ("npc5_backstory_response_1", "If you're looking for work, I can use experienced fighters."),
  ("npc6_backstory_response_1", "If you're looking for work, I can use experienced fighters."),
  ("npc7_backstory_response_1", "If you're looking for work, I can use experienced fighters."),
  ("npc8_backstory_response_1", "If you're looking for work, I can use experienced fighters."),
  ("npc9_backstory_response_1", "You will do."),
  ("npc10_backstory_response_1", "If you're looking for work, I can use experienced fighters."),
  ("npc11_backstory_response_1", "You will do."),
  ("npc12_backstory_response_1", "If you're looking for work, I can use experienced fighters."),
  ("npc13_backstory_response_1", "If you're looking for work, I can use experienced fighters."),
  ("npc14_backstory_response_1", "If you're looking for work, I can use experienced fighters."),
  ("npc15_backstory_response_1", "If you're looking for work, I can use experienced fighters."),
  ("npc16_backstory_response_1", "If you're looking for work, I can use experienced fighters."),

  ("npc1_backstory_response_2", "No, sorry. Nothing I can do for you."),
  ("npc2_backstory_response_2", "No, sorry. Nothing I can do for you."),
  ("npc3_backstory_response_2", "No, sorry. Nothing I can do for you."),
  ("npc4_backstory_response_2", "No, sorry. Nothing I can do for you."),
  ("npc5_backstory_response_2", "No, sorry. Nothing I can do for you."),
  ("npc6_backstory_response_2", "No, sorry. Nothing I can do for you."),
  ("npc7_backstory_response_2", "No, sorry. Nothing I can do for you."),
  ("npc8_backstory_response_2", "No, sorry. Nothing I can do for you."),
  ("npc9_backstory_response_2", "I don't need you, slave."),
  ("npc10_backstory_response_2", "No, sorry. Nothing I can do for you."),
  ("npc11_backstory_response_2", "I don't need you, slave."),
  ("npc12_backstory_response_2", "No, sorry. Nothing I can do for you."),
  ("npc13_backstory_response_2", "No, sorry. Nothing I can do for you."),
  ("npc14_backstory_response_2", "No, sorry. Nothing I can do for you."),
  ("npc15_backstory_response_2", "No, sorry. Nothing I can do for you."),
  ("npc16_backstory_response_2", "No, sorry. Nothing I can do for you."),

  ("npc1_signup", "Indeed? You would do well to enlist me."),
  ("npc2_signup", "Indeed? You would do well to enlist me."),
  ("npc3_signup", "Indeed? You would do well to enlist me."),
  ("npc4_signup", "Indeed? You would do well to enlist me."),
  ("npc5_signup", "I see. I admit I have heard of you and your exploits."),
  ("npc6_signup", "Indeed? You would do well to enlist me."),
  ("npc7_signup", "Indeed? You would do well to enlist me."),
  ("npc8_signup", "Indeed? You would do well to enlist me."),
  ("npc9_signup", "Indeed? You would do well to enlist me."),
  ("npc10_signup", "Indeed? You would do well to enlist me."),
  ("npc11_signup", "Indeed? You would do well to enlist me."),
  ("npc12_signup", "Indeed? You would do well to enlist me."),
  ("npc13_signup", "Indeed? You would do well to enlist me."),
  ("npc14_signup", "Indeed? You would do well to enlist me."),
  ("npc15_signup", "Indeed? You would do well to enlist me."),
  ("npc16_signup", "Indeed? You would do well to enlist me."),

  ("npc1_signup_2", "It would take a moment to gather my things and meet you at the gates."),
  ("npc2_signup_2", "You won't regret taking me on."),
  ("npc3_signup_2", "You won't regret taking me on."),
  ("npc4_signup_2", "You won't regret taking me on."),
  ("npc5_signup_2", "Perhaps by joining your company and striking hard where I am not expected, the Enemy will be unbalanced. I will come."),
  ("npc6_signup_2", "You won't regret taking me on."),
  ("npc7_signup_2", "You won't regret taking me on."),
  ("npc8_signup_2", "You won't regret taking me on."),
  ("npc9_signup_2", "You won't regret taking me on."),
  ("npc10_signup_2", "You won't regret taking me on."),
  ("npc11_signup_2", "You won't regret taking me on."),
  ("npc12_signup_2", "You won't regret taking me on."),
  ("npc13_signup_2", "You won't regret taking me on."),
  ("npc14_signup_2", "You won't regret taking me on."),
  ("npc15_signup_2", "You won't regret taking me on."),
  ("npc16_signup_2", "You won't regret taking me on."),


  ("npc1_signup_response_1", "I could use a skilled ranger, you are welcome to join."),
  ("npc2_signup_response_1", "Very well. I'll be glad to have you with us."),
  ("npc3_signup_response_1", "Very well. I'll be glad to have you with us."),
  ("npc4_signup_response_1", "Very well. I'll be glad to have you with us."),
  ("npc5_signup_response_1", "We are glad to have the company of an Elf-lord."),
  ("npc6_signup_response_1", "Very well. I'll be glad to have you with us."),
  ("npc7_signup_response_1", "Very well. I'll be glad to have you with us."),
  ("npc8_signup_response_1", "Very well. I'll be glad to have you with us."),
  ("npc9_signup_response_1", "Very well. I'll be glad to have you with us."),
  ("npc10_signup_response_1", "Very well. I'll be glad to have you with us."),
  ("npc11_signup_response_1", "Very well. I'll be glad to have you with us."),
  ("npc12_signup_response_1", "Very well. I'll be glad to have you with us."),
  ("npc13_signup_response_1", "Very well. I'll be glad to have you with us."),
  ("npc14_signup_response_1", "Very well. I'll be glad to have you with us."),
  ("npc15_signup_response_1", "Very well. I'll be glad to have you with us."),
  ("npc16_signup_response_1", "Very well. I'll be glad to have you with us."),

#11
  ("npc1_signup_response_2", "I have no need of your company at the moment, good luck to you."),
  ("npc2_signup_response_2", "Sorry, I've changed my mind."),
  ("npc3_signup_response_2", "Sorry, I've changed my mind."),
  ("npc4_signup_response_2", "Sorry, I've changed my mind."),
  ("npc5_signup_response_2", "On second thought, I don't think we need more Elves."),
  ("npc6_signup_response_2", "Sorry, I've changed my mind."),
  ("npc7_signup_response_2", "Sorry, I've changed my mind."),
  ("npc8_signup_response_2", "Sorry, I've changed my mind."),
  ("npc9_signup_response_2", "Sorry, I've changed my mind."),
  ("npc10_signup_response_2", "Sorry, I've changed my mind."),
  ("npc11_signup_response_2", "Sorry, I've changed my mind."),
  ("npc12_signup_response_2", "Sorry, I've changed my mind."),
  ("npc13_signup_response_2", "Sorry, I've changed my mind."),
  ("npc14_signup_response_2", "Sorry, I've changed my mind."),
  ("npc15_signup_response_2", "Sorry, I've changed my mind."),
  ("npc16_signup_response_2", "Sorry, I've changed my mind."),

  ("npc1_payment", "I'll join you for {reg3} coins."),
  ("npc2_payment", "I'll join you for {reg3} coins."),
  ("npc3_payment", "I'll join you for {reg3} coins."),
  ("npc4_payment", "I'll join you for {reg3} coins."),
  ("npc5_payment", "We should be off soon. The value of my coming will be diminished if the Enemy senses my presence before we have struck. I'll join you for {reg3} coins."),
  ("npc6_payment", "I'll join you for {reg3} coins."),
  ("npc7_payment", "I'll join you for {reg3} coins."),
  ("npc8_payment", "I'll join you for {reg3} coins."),
  ("npc9_payment", "I'll join you for {reg3} coins."),
  ("npc10_payment", "I'll join you for {reg3} coins."),
  ("npc11_payment", "I'll join you for {reg3} coins."),
  ("npc12_payment", "I'll join you for {reg3} coins."),
  ("npc13_payment", "I'll join you for {reg3} coins."),
  ("npc14_payment", "I'll join you for {reg3} coins."),
  ("npc15_payment", "I'll join you for {reg3} coins."),
  ("npc16_payment", "I'll join you for {reg3} coins."),

  ("npc1_payment_response", "Certainly. Here's {reg3} coins."),
  ("npc2_payment_response", "Certainly. Here's {reg3} coins."),
  ("npc3_payment_response", "Certainly. Here's {reg3} coins."),
  ("npc4_payment_response", "Certainly. Here's {reg3} coins."),
  ("npc5_payment_response", "Certainly. Here's {reg3} coins."),
  ("npc6_payment_response", "Certainly. Here's {reg3} coins."),
  ("npc7_payment_response", "Certainly. Here's {reg3} coins."),
  ("npc8_payment_response", "Certainly. Here's {reg3} coins."),
  ("npc9_payment_response", "Certainly. Here's {reg3} coins."),
  ("npc10_payment_response", "Certainly. Here's {reg3} coins."),
  ("npc11_payment_response", "Certainly. Here's {reg3} coins."),
  ("npc12_payment_response", "Certainly. Here's {reg3} coins."),
  ("npc13_payment_response", "Certainly. Here's {reg3} coins."),
  ("npc14_payment_response", "Certainly. Here's {reg3} coins."),
  ("npc15_payment_response", "Certainly. Here's {reg3} coins."),
  ("npc16_payment_response", "Certainly. Here's {reg3} coins."),




  ("npc1_morality_speech", "Oy -- boss. Please don't take this the wrong way, but it's a hard life and it's a bit much that we {s21}. Take a little more care in the future, captain, if you don't mind my saying."),
  ("npc2_morality_speech", "I hope you don't mind my saying so, but it's a bit hard for me to see us {s21}. Maybe I ought to try to be more of a hardened soldier, but if we could try to exercise a little mercy from time to time, I'd sleep better."),
  ("npc3_morality_speech", "Perhaps it is not my place to say so, {sir/madame}, but I confess that I am somewhat shocked that we {s21}. Of course I realize that war is cruel, but there is no need to make it more cruel than necessary."),
  ("npc4_morality_speech", "Your pardon -- just so you know, the men of the House of Rolf do not care to {s21}. I will not be pleased if you continue to take this course."),
  ("npc5_morality_speech", "Pardon me, captain. It is not good to {s21}. Your first duty is to the men who have taken your salt. The least they can expect is food, pay, the opportunity to loot, and that you not waste their lives needlessly."),
  ("npc6_morality_speech", "Excuse me, {sir/madame}. As you know, I joined with you to right wrongs, protect the innocent, and make amends for my sin. I did not expect to {s21}."),
  ("npc7_morality_speech", "Captain -- I do not like to see us {s21}. Such are the actions of a common bandit chief, with no regard for his followers."),
  ("npc8_morality_speech", "I was not pleased that you decided to {s21}. To fall in battle is an honour, but to fight in a warband led by a coward is a disgrace."),
  ("npc9_morality_speech", "{Sir/Madame} -- it is not my way to {s21}. Men of my house will accept death but not dishonour. Please do not make me ashamed to serve under you."),
  ("npc10_morality_speech", "Begging your pardon, captain. I can't say that I'm happy to see us {s21}. Those are just simple people, trying to make a living. If we could try to go easy on the poor wretches, captain, I'd feel much better."),
  ("npc11_morality_speech", "Excuse me, captain. It's not good that we {s21}. I've followed armies and warbands for 30 years, and the least the soldiers expect of a leader is to feed them, pay them, and do {his/her} best to keep their sorry skins intact as best {he/she} can."),
  ("npc12_morality_speech", "Captain -- I do not like to see us {s21}. I am prepared to be a warrior, but not a brigand. Pray let us try to show a little more compassion."),
  ("npc13_morality_speech", "Captain, if we can avoid it, I'd prefer not to {s21}. Calradia is a small place, and one's reputation is precious. I would not care for one of my rivals to include this latest unfortunate incident in a satirical verse."),
  ("npc14_morality_speech", "I do not care to {s21}. No one with a reputation for cowardice will be properly feared by his men."),
  ("npc15_morality_speech", "{Sir/Madame} -- just so you know my opinion, any commander with sense will not let his company {s21}.I hope you don't mind me speaking so bluntly."),
  ("npc16_morality_speech", "Captain. I don't like to {s21}. So many throats left uncut, and so many purses left unexplored..."),


  ("npc1_2ary_morality_speech", "Boss -- just so you know, I've got no problem if we {s21}. Living to fight another day makes good sense to me."),
  ("npc2_2ary_morality_speech", "{Sir/Madame} -- I'm not altogether happy that we {s21}. I'm a merchant, and in our business one is bonded by one's word. I don't want a reputation for dishonesty -- that would spell my end as a trader, {sir/madame}."),
  ("npc3_2ary_morality_speech", "{Sir/Madame} -- I think it was a brave decision you took to {s21}. There is no shame in finding a way to avoid the spilling of blood."),
  ("npc4_2ary_morality_speech", "Your pardon -- whatever anyone else says, I think nothing of it that you {s21}. You should adopt whatever ruse you need to survive in these troubled times."),
  ("npc5_2ary_morality_speech", "[No secondary moral code]"),
  ("npc6_2ary_morality_speech", "{Sir/Madame} -- you may choose to {s21}, but would prefer to have no part in it. Such is not the path to my redemption."),
  ("npc7_2ary_morality_speech", "[No secondary moral code]"),
  ("npc8_2ary_morality_speech", "[No secondary moral code]"),
  ("npc9_2ary_morality_speech", "Captain, I am dismayed that you {s21}. A {gentleman/gentlewoman} such as yourself should exhibit the highest standards of honour at all times."),
  ("npc10_2ary_morality_speech", "{Brother/Sister} -- I can't say I like to see us {s21}. You should treat your men well, and they'll repay with interest."),
  ("npc11_2ary_morality_speech", "[No secondary moral code]"),
  ("npc12_2ary_morality_speech", "[No secondary moral code]"),
  ("npc13_2ary_morality_speech", "[No secondary moral code]"),
  ("npc14_2ary_morality_speech", "Captain -- you should not let it bother you that you {s21}. Armies are made to do their leaders' bidding, and hardships are part of a soldier's life."),
  ("npc15_2ary_morality_speech", "You know, friend {playername}, it's none too reassuring to see how you just {s21}. If you can break your word to them, you can break your word to me, is how I figure it."),
  ("npc16_2ary_morality_speech", "Captain -- just so you know, it's no problem by me that we {s21}. We do what we need to do to live, and they'd do the same to us if they were in our shoes."),

  ("npc1_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc2_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc3_personalityclash_speech", "Did I mention I hate {s11}?."),
  ("npc4_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc5_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc6_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc7_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc8_personalityclash_speech", "Did I mention I hate {s11}?"), 
  ("npc9_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc10_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc11_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc12_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc13_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc14_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc15_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc16_personalityclash_speech", "Did I mention I hate {s11}?"),

  ("npc1_personalityclash_speech_b", "I hate {s11}."),
  ("npc2_personalityclash_speech_b", "I hate {s11}."),
  ("npc3_personalityclash_speech_b", "I hate {s11}."),
  ("npc4_personalityclash_speech_b", "I hate {s11}."),
  ("npc6_personalityclash_speech_b", "I hate {s11}."),
  ("npc7_personalityclash_speech_b", "I hate {s11}."),
  ("npc8_personalityclash_speech_b", "I hate {s11}."),
  ("npc9_personalityclash_speech_b", "I hate {s11}."),
  ("npc10_personalityclash_speech_b", "I hate {s11}."),
  ("npc11_personalityclash_speech_b", "I hate {s11}."),
  ("npc12_personalityclash_speech_b", "I hate {s11}."),
  ("npc13_personalityclash_speech_b", "I hate {s11}."),
  ("npc14_personalityclash_speech_b", "I hate {s11}."),
  ("npc15_personalityclash_speech_b", "I hate {s11}."),
  ("npc16_personalityclash_speech_b", "I hate {s11}."),

 
### set off by behavior after victorious battle
  ("npc1_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc2_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc3_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc4_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc5_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc6_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc7_personalityclash2_speech", "Did I mention I hate {s11}?"), 
  ("npc8_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc9_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc10_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc12_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc13_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc14_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc15_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc16_personalityclash2_speech", "Did I mention I hate {s11}?"),
   
  ("npc1_personalityclash2_speech_b", "I hate {s11}."), 
  ("npc2_personalityclash2_speech_b", "I hate {s11}."),
  ("npc3_personalityclash2_speech_b", "I hate {s11}."),
  ("npc4_personalityclash2_speech_b", "I hate {s11}."),
  ("npc5_personalityclash2_speech_b", "I hate {s11}."),
  ("npc6_personalityclash2_speech_b", "I hate {s11}."),
  ("npc7_personalityclash2_speech_b", "I hate {s11}."),
  ("npc8_personalityclash2_speech_b", "I hate {s11}."),
  ("npc9_personalityclash2_speech_b", "I hate {s11}."),
  ("npc10_personalityclash2_speech_b", "I hate {s11}."), 
  ("npc11_personalityclash2_speech_b", "I hate {s11}."),
  ("npc12_personalityclash2_speech_b", "I hate {s11}."),
  ("npc13_personalityclash2_speech_b", "I hate {s11}."),
  ("npc14_personalityclash2_speech_b", "I hate {s11}."),
  ("npc15_personalityclash2_speech_b", "I hate {s11}."),
  ("npc16_personalityclash2_speech_b", "I hate {s11}."),


  ("npc1_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc2_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc3_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc4_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc5_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc6_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc7_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc8_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc9_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc10_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc11_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc12_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc13_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc14_personalityclash_speech", "Did I mention I like {s11}?"),
  ("npc15_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc16_personalitymatch_speech", "Did I mention I like {s11}?"),
   
  ("npc1_personalitymatch_speech_b", "I like {s11}."),
  ("npc2_personalitymatch_speech_b", "I like {s11}."),
  ("npc3_personalitymatch_speech_b", "I like {s11}."),
  ("npc4_personalitymatch_speech_b", "I like {s11}."),
  ("npc5_personalitymatch_speech_b", "I like {s11}."),
  ("npc6_personalitymatch_speech_b", "I like {s11}."),
  ("npc7_personalitymatch_speech_b", "I like {s11}."),
  ("npc8_personalitymatch_speech_b", "I like {s11}."),
  ("npc9_personalitymatch_speech_b", "I like {s11}."),
  ("npc10_personalitymatch_speech_b", "I like {s11}."),
  ("npc11_personalitymatch_speech_b", "I like {s11}."),
  ("npc12_personalitymatch_speech_b", "I like {s11}."),
  ("npc13_personalitymatch_speech_b", "I like {s11}."),
  ("npc14_personalityclash_speech_b", "I like {s11}."),
  ("npc15_personalitymatch_speech_b", "I like {s11}."),
  ("npc16_personalitymatch_speech_b", "I like {s11}."),

  
  ("npc1_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc2_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc3_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc4_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc5_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc6_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc7_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc8_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc9_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc10_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc11_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc12_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc13_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc14_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc15_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc16_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),

  ("npc1_rehire_speech", "It's good to see you. Will you allow me to serve with you once again?"),
  ("npc2_rehire_speech", "It's good to see you. Will you allow me to serve with you once again?"),
  ("npc3_rehire_speech", "It's good to see you. Will you allow me to serve with you once again?"),
  ("npc4_rehire_speech", "It's good to see you. Will you allow me to serve with you once again?"),
  ("npc5_rehire_speech", "It's good to see you. Will you allow me to serve with you once again?"),
  ("npc6_rehire_speech", "It's good to see you. Will you allow me to serve with you once again?"),
  ("npc7_rehire_speech", "It's good to see you. Will you allow me to serve with you once again?"),
  ("npc8_rehire_speech", "It's good to see you. Will you allow me to serve with you once again?"),
  ("npc9_rehire_speech", "It's good to see you. Will you allow me to serve with you once again?"),
  ("npc10_rehire_speech", "It's good to see you. Will you allow me to serve with you once again?"),
  ("npc11_rehire_speech", "It's good to see you. Will you allow me to serve with you once again?"),
  ("npc12_rehire_speech", "It's good to see you. Will you allow me to serve with you once again?"),
  ("npc13_rehire_speech", "It's good to see you. Will you allow me to serve with you once again?"),
  ("npc14_rehire_speech", "It's good to see you. Will you allow me to serve with you once again?"),
  ("npc15_rehire_speech", "It's good to see you. Will you allow me to serve with you once again?"),
  ("npc16_rehire_speech", "It's good to see you. Will you allow me to serve with you once again?"),

#local color strings
  ("npc1_home_intro", "Hey, look!"),
  ("npc2_home_intro", "Hey, look!"),
  ("npc3_home_intro", "Hey, look!"),
  ("npc4_home_intro", "Hey, look!"),
  ("npc5_home_intro", "Hey, look!"),
  ("npc6_home_intro", "Hey, look!"),
  ("npc7_home_intro", "Hey, look!"),
  ("npc8_home_intro", "Hey, look!"),
  ("npc9_home_intro", "Hey, look!"),
  ("npc10_home_intro", "Hey, look!"),
  ("npc11_home_intro", "Hey, look!"),
  ("npc12_home_intro", "Hey, look!"),
  ("npc13_home_intro", "Hey, look!"),
  ("npc14_home_intro", "Hey, look!"),
  ("npc15_home_intro", "Hey, look!"),
  ("npc16_home_intro", "Hey, look!"),


  ("npc1_home_description", "Do you know that town?"),
  ("npc2_home_description", "Do you know that town?"),
  ("npc3_home_description", "Do you know that town?"),
  ("npc4_home_description", "Do you know that town?"),
  ("npc5_home_description", "Do you know that town?"),
  ("npc6_home_description", "Do you know that town?"),
  ("npc7_home_description", "Do you know that town?"),
  ("npc8_home_description", "Do you know that town?"),
  ("npc9_home_description", "Do you know that town?"),
  ("npc10_home_description", "Do you know that town?"),
  ("npc11_home_description", "Do you know that town?"),
  ("npc12_home_description", "Do you know that town?"),
  ("npc13_home_description", "Do you know that town?"),
  ("npc14_home_description", "Do you know that town?"),
  ("npc15_home_description", "Do you know that town?"),
  ("npc16_home_description", "Do you know that town?"),

  ("npc1_home_description_2", "Edoras smells of horse manure, har-har!"),
  ("npc2_home_description_2", "Edoras smells of horse manure, har-har!"),
  ("npc3_home_description_2", "Minas Tirith looks like a wedding cake, har-har!"),
  ("npc4_home_description_2", "Minas Tirith looks like a wedding cake, har-har!"),
  ("npc5_home_description_2", "Minas Tirith looks like a wedding cake, har-har!"),
  ("npc6_home_description_2", "Minas Tirith looks like a wedding cake, har-har!"),
  ("npc7_home_description_2", "Minas Tirith looks like a wedding cake, har-har!"),
  ("npc8_home_description_2", "Minas Tirith looks like a wedding cake, har-har!"),
  ("npc9_home_description_2", "Minas Morgul, where Nazguls drink all day, har-har!"),
  ("npc10_home_description_2", "Minas Morgul, where Nazguls drink all day, har-har!"),
  ("npc11_home_description_2", "Doesn't Orthanc look like a giant... something?"),
  ("npc12_home_description_2", "Doesn't Orthanc look like a giant... something?"),
  ("npc13_home_description_2", "Minas Morgul, where Nazguls drink all day, har-har!"),
  ("npc14_home_description_2", "Minas Morgul, where Nazguls drink all day, har-har!"),
  ("npc15_home_description_2", "Minas Morgul, where Nazguls drink all day, har-har!"),
  ("npc16_home_description_2", "Minas Morgul, where Nazguls drink all day, har-har!"),

  ("npc1_home_recap", "Did I tell you Edoras smells of horse manure, har-har!"),
  ("npc2_home_recap", "Did I tell you Edoras smells of horse manure, har-har!"),
  ("npc3_home_recap", "Did I tell you Minas Tirith looks like a wedding cake, har-har!"),
  ("npc4_home_recap", "Did I tell you Minas Tirith looks like a wedding cake, har-har!"),
  ("npc5_home_recap", "Did I tell you Minas Tirith looks like a wedding cake, har-har!"),
  ("npc6_home_recap", "Did I tell you Minas Tirith looks like a wedding cake, har-har!"),
  ("npc7_home_recap", "Did I tell you Minas Tirith looks like a wedding cake, har-har!"),
  ("npc8_home_recap", "Did I tell you Minas Tirith looks like a wedding cake, har-har!"),
  ("npc9_home_recap", "I told you, Minas Morgul is where Nazguls drink all day, har-har!"),
  ("npc10_home_recap", "I told you, Minas Morgul is where Nazguls drink all day, har-har!"),
  ("npc11_home_recap", "Didn't I mention Orthanc look like a giant... something?"),
  ("npc12_home_recap", "Didn't I mention Orthanc look like a giant... something?"),
  ("npc13_home_recap", "I told you, Minas Morgul is where Nazguls drink all day, har-har!"),
  ("npc14_home_recap", "I told you, Minas Morgul is where Nazguls drink all day, har-har!"),
  ("npc15_home_recap", "I told you, Minas Morgul is where Nazguls drink all day, har-har!"),
  ("npc16_home_recap", "I told you, Minas Morgul is where Nazguls drink all day, har-har!"),

  ("npc1_honorific", "{sir/madame}"),
  ("npc2_honorific", "{sir/madame}"),
  ("npc3_honorific", "commander"),
  ("npc4_honorific", "commander"),
  ("npc5_honorific", "{sir/madame}"),
  ("npc6_honorific", "{sir/madame}"),
  ("npc7_honorific", "captain"),
  ("npc8_honorific", "captain"),
  ("npc9_honorific", "commander"),
  ("npc10_honorific", "commander"),
  ("npc11_honorific", "commander"),
  ("npc12_honorific", "commander"),
  ("npc13_honorific", "captain"),
  ("npc14_honorific", "captain"),
  ("npc15_honorific", "captain"),
  ("npc16_honorific", "captain"),


#NPC companion changes end

#Troop Commentaries begin
#Tags for comments are = allied/enemy, friendly/unfriendly, and then those related to specific reputations
#Also, there are four other tags which refer to groups of two or more reputations (spiteful, benevolent, chivalrous, and coldblooded)
#The game will select the first comment in each block which meets all the tag requirements

#Beginning of game comments
("comment_intro_liege_affiliated", "I am told that you are pledged to one of the pretenders who disputes my claim to the crown of Calradia. But we may still talk."),

("comment_intro_famous_liege", "Your fame runs before you! Perhaps it is time that you sought a liege worthy of your valor."),
("comment_intro_famous_martial", "Your fame runs before you! Perhaps we shall test each other's valor in a tournament, or on the battlefield!"),
("comment_intro_famous_badtempered", "I've heard of you. Well, I'm not one for bandying words, so if you have anything to say, out with it."),
("comment_intro_famous_pitiless", "I know your name. It strikes fear in men's hearts. That is good. Perhaps we should speak together, some time."),
("comment_intro_famous_cunning", "Ah, yes. At last we meet. You sound like a good {man/woman} to know. Let us speak together, from time to time."),
("comment_intro_famous_sadistic", "I know your name -- and from what I hear, I'll warrant that many a grieving widow knows too. But that is no concern of mine."),
("comment_intro_famous_goodnatured", "I've heard of you! It's very good to finally make your acquaintance."),
("comment_intro_famous_upstanding", "I know your name. They say you are a most valiant warrior. I can only hope that your honour and mercy matches your valor."),

("comment_intro_noble_liege", "I see that you carry a nobleman's banner, although I do not recognize the device. Know that I am always looking for good men to fight for me, once they prove themselves to be worthy of my trust."),
("comment_intro_noble_martial", "I see that you carry a nobleman's banner, but I do not recognize the device. Perhaps one day we shall test each other's valor in a tournament, or on the battlefield!"),
("comment_intro_noble_badtempered", "I don't recognize the device on your banner. No doubt another foreigner come to our lands, as if we didn't have so many here already."),
("comment_intro_noble_pitiless", "I see that you carry a nobleman's banner, but I do not recognize the device. Another vulture come to grow fat on the leftovers of war, no doubt!"),
("comment_intro_noble_cunning", "I see that you carry a nobleman's banner, but I do not recognize the device. Still, it is always worthwhile to make the acquaintance of {men/women} who may one day prove themselves to be great warriors."),
("comment_intro_noble_sadistic", "I see that you carry a nobleman's banner, but I do not recognize the device. Perhaps you are the bastard {son/daughter} of a puffed-up cattle thief? Or perhaps you stole it?"),
("comment_intro_noble_goodnatured", "I see that you carry a nobleman's banner, but I do not recognize the device. Forgive my ignorance, {sir/madame}! It is good to make your acquaitance."),
("comment_intro_noble_upstanding", "I see that you carry a nobleman's banner, but I do not recognize the device. No doubt you have come to Calradia in search of wealth and glory. If this indeed is the case, then I only ask that you show mercy to those poor souls caught in the path of war."),

("comment_intro_common_liege", "You may be of common birth, but know that I am always looking for good men to fight for me, if they can prove themselves to be worthy of my trust."),
("comment_intro_common_martial", "Perhaps you are not of gentle birth, but if you prove yourself a {man/woman} of valor, then I would be pleased to try my strength against yours in the tournament or on the battlefield."),
("comment_intro_common_badtempered", "Speak quickly, if you have anything to say, for I have no time to be bandying words with common soldiers of fortune."),
("comment_intro_common_pitiless", "You have the look of a mercenary, another vulture come to grow fat on the misery of this land."),
("comment_intro_common_cunning", "Well... I have not heard of you, but you have the look of a {man/woman} who might make something of {himself/herself}, some day."),
("comment_intro_common_sadistic", "Normally I cut the throats of impudent commoners who barge into my presence uninvited, but I am in a good mood today."),
("comment_intro_common_goodnatured", "Well, you look like a good enough sort."),
("comment_intro_common_upstanding", "Peace to you, and always remember to temper your valor with mercy, your courage with honour."),


#Actions vis-a-vis civilians
  ("comment_you_raided_my_village_enemy_benevolent",    "You have attacked innocent farmers under my protection in the village of {s51}.  I will punish you for your misdeeds!"), 
  ("comment_you_raided_my_village_enemy_spiteful",      "You have raided my village of {s51}, destroying my property and killing the tenants. I will take my compensation in blood!"), 
  ("comment_you_raided_my_village_enemy_coldblooded",   "You have raided my village of {s51}, destroying my property and killing the tenants. I will make you think twice before you disrupt my revenues like that again."), 
  ("comment_you_raided_my_village_enemy",               "You have raided my village of {s51}, destroying my property and killing tenants under my protection. You will pay the price for your crime!"), 
  ("comment_you_raided_my_village_unfriendly_spiteful", "You have raided my village of {s51}. Do it again and I'll gut you like a fish."),
  ("comment_you_raided_my_village_friendly",            "You have raided my village of {s51}. This will place a grave strain on our friendship."),
  ("comment_you_raided_my_village_default",             "You have raided my village of {s51}. If you continue to behave this way, we may soon come to blows."),

  ("comment_you_robbed_my_village_enemy_coldblooded", "You have robbed my tenants in the village of {s51}. I take that as a personal insult."), 
  ("comment_you_robbed_my_village_enemy",             "You have robbed innocent farmers under my protection in the village of {s51}.  I will punish you for your misdeeds!"), 
  ("comment_you_robbed_my_village_friendly_spiteful", "I have heard that you pinched some food from my tenants at {s51}. Well, I'll not begrudge you a scrap or two, but keep in mind that I'm the one who must listen to their whining afterward."),
  ("comment_you_robbed_my_village_friendly",          "I have heard that you requisitioned supplies from my tenants at {s51}. I am sure that you would not have done so were you not desperately in need."),
  ("comment_you_robbed_my_village_default",           "You have robbed my tenants in the village of {s51}. If you continue to behave this way, we may soon come to blows."),

  ("comment_you_accosted_my_caravan_enemy",          "You have been accosting caravans under my protection. But your trail of brigandage will soon come to an end."),
  ("comment_you_accosted_my_caravan_default",        "You have been accosting caravans under my protection. This sort of behavior must stop."),

  ("comment_you_helped_villagers_benevolent",                "I heard that you gave charity to my tenants in the village of {s51}. I had been neglectful in my duties as lord and protector, and I appreciate what you have done."),
  ("comment_you_helped_villagers_friendly_cruel",            "I heard that you gave charity to my tenants in the village of {s51}. I appreciate that you meant well, but I'd rather you not undercut my authority like that."),
  ("comment_you_helped_villagers_friendly",                  "I heard that you gave charity to my tenants in the village of {s51}. Times are hard, and I know that you mean well, so I will not object to you providing them with assistance."),
  ("comment_you_helped_villagers_unfriendly_spiteful",       "I heard that you gave charity to my tenants in the village of {s51}. As amusing as it is to see you grubbing for favor among my vassals, I would ask you to mind your own business."),
  ("comment_you_helped_villagers_cruel",                     "I heard that you gave charity to my tenants in the village of {s51}. As the peasants' lord and protector, it is most properly my duty to assist them in times of hardship. You may mean well, but your actions still undercut my authority. I would thank you to leave them alone."),
  ("comment_you_helped_villagers_default",                   "I heard that you gave charity to my tenants in the village of {s51}. Times are hard, and I know that you mean well, but try not to make a habit of it. I am their lord and protector, and I would rather not have them go looking to strangers for assistance."),


#Combat-related events


  ("comment_you_captured_a_castle_allied_friendly",            "I heard that you have besieged and taken {s51}. That was a great dead, and I am proud to call you my friend!"), 
  ("comment_you_captured_a_castle_allied_spiteful",            "I heard that you have besieged and taken {s51}. Good work! Soon, we will have all their fortresses to despoil, their treasuries to ransack, their grieving widows to serve us our wine."), 
  ("comment_you_captured_a_castle_allied_unfriendly_spiteful", "I heard that you have besieged and taken {s51}. Well, every dog has his day, or so they say. Enjoy it while you can, until your betters kick you back out in the cold where you belong."), 
  ("comment_you_captured_a_castle_allied_unfriendly",          "I heard that you have besieged and taken {s51}. Whatever our differences in the past, I must offer you my congratulations."), 
  ("comment_you_captured_a_castle_allied",                     "I heard that you have besieged and taken {s51}. We have them on the run!"), 

  ("comment_you_captured_my_castle_enemy_spiteful",            "I hear that you have broken into my home at {s51}. I hope the dungeon is to your liking, as you will be spending much time there in the years to come."),
  ("comment_you_captured_my_castle_enemy_chivalrous",          "You hold {s51}, my rightful fief. I hope you will give me the chance to win it back!"),
  ("comment_you_captured_my_castle_enemy",                     "You have something that belongs to me -- {s51}. I will make you relinquish it."),

###Add some variation to these
  ("comment_we_defeated_a_lord_unfriendly_spiteful",           "I suppose you will want to drink to the memory of our victory over {s54}. Well, save your wine -- it will take more than that to wipe out the stain of your earlier disgraces."), 
  ("comment_we_defeated_a_lord_unfriendly",                    "I will not forget how we fought together against {s54}, but I can also not forget the other matters that lie between us."), 
  ("comment_we_defeated_a_lord_cruel",                         "That was a great victory over {s54}, wasn't it? We made of his army a feast for the crows!"), 
  ("comment_we_defeated_a_lord_quarrelsome",                   "I won't forget how we whipped {s54}? I enjoyed that."), 
  ("comment_we_defeated_a_lord_upstanding",                    "I will not forget our victory over {s54}. Let us once again give thanks to heaven, and pray that we not grow too proud."), 
  ("comment_we_defeated_a_lord_default",                       "That was a great victory over {s54}, wasn't it? I am honoured to have fought by your side."), 

  ("comment_we_fought_in_siege_unfriendly_spiteful",           "I suppose you will want to drink to the memory of our capture of {s51}. Well, save your wine -- it will take more than that to wipe out the stain of your earlier disgraces."), 
  ("comment_we_fought_in_siege_unfriendly",                    "I will not forget how we together we stormed {s51}, but I can also not forget the other matters that lie between us."), 
  ("comment_we_fought_in_siege_cruel",                         "I won't forget how we broke through the walls of {s51} and put its defenders to the sword. It is a sweet memory."), 
  ("comment_we_fought_in_siege_quarrelsome",                   "Remember how the enemy squealed when we came over the walls of {s51}? They had thought they were safe! We wiped the smug smiles of their faces!"), 
  ("comment_we_fought_in_siege_upstanding",                    "I will not forget our capture of {s51}. Let us once again give thanks to heaven, and pray that we not grow too proud."), 
  ("comment_we_fought_in_siege_default",                       "I will not forget how together we captured {s51}. I am honoured to have fought by your side."), 

  ("comment_we_fought_in_major_battle_unfriendly_spiteful",    "I suppose you will want to drink to the memory of our great victory near {s51}. Well, save your wine -- it will take more than that to wipe out the stain of your earlier disgraces."), 
  ("comment_we_fought_in_major_battle_unfriendly",             "I will not forget how we fought together in the great battle near {s51}, but I can also not forget the other matters that lie between us."), 
  ("comment_we_fought_in_major_battle_cruel",                  "I won't forget the great battle near {s51}, when we broke through the enemy lines and they ran screaming before us. It is a sweet memory."), 
  ("comment_we_fought_in_major_battle_quarrelsome",            "That was a fine fight near {s51}, when we made those bastards run!"), 
  ("comment_we_fought_in_major_battle_upstanding",             "I will not forget how we fought side by side at the great battle near {s51}. Let us once again give thanks to heaven, and pray that we not grow too proud."), 
  ("comment_we_fought_in_major_battle_default",                "I will not forget how we fought side by side at the great battle near {s51}. I am honoured to have fought by your side."), 




  ("comment_you_defeated_a_lord_allied_liege",                   "So, you crossed swords with that rascal they call {s54}, and emerged victorious. I am very happy to hear that."), 
  ("comment_you_defeated_a_lord_allied_unfriendly_spiteful",     "I heard that you fought and defeated {s54}. Every dog has its day, I suppose."), 
  ("comment_you_defeated_a_lord_allied_spiteful",                "I heard that you fought and defeated that dog {s54}. Ah, if only I could have heard him whimpering for mercy."), 
  ("comment_you_defeated_a_lord_allied_unfriendly_chivalrous",   "I heard that you fought and defeated {s54}. I hope that you did not use dishonourable means to do so."),
  ("comment_you_defeated_a_lord_allied",                         "I heard that you fought and defeated {s54}. I wish you joy of your victory."), 

  ("comment_you_defeated_me_enemy_chivalrous", "I will not begrudge you your victory the last time that we met, but I am anxious for another round!"), 
  ("comment_you_defeated_me_enemy_spiteful",   "I have been looking forward to meeting you again. Your tricks will not deceive me a second time, and I will relish hearing your cries for mercy."), 
  ("comment_you_defeated_me_enemy",            "When last we met, {playername}, you had the better of me. But I assure you that it will not happen again!"), 

  ("comment_I_defeated_you_enemy_spiteful",          "Back for more? Make me fight you again, and I'll feed your bowels to my hounds."), 
  ("comment_I_defeated_you_enemy_chivalrous",        "Come to test your valor against me again, {playername}?"), 
  ("comment_I_defeated_you_enemy_benevolent",        "So once again you come at me? Will you ever learn?"), 
  ("comment_I_defeated_you_enemy_coldblooded",       "You are persistent, but a nuisance."),
  ("comment_I_defeated_you_enemy",                   "How many times must I chastise you before you learn to keep your distance?"), 


  ("comment_we_were_defeated_unfriendly_spiteful",   "Last I saw you, you had been struck down by the men of {s54}. I blame you for that disaster. What a pity to see that you survived."), 
  ("comment_we_were_defeated_unfriendly",            "Last I saw you, you had been struck down by the men of {s54}. Well, I see that you survived."), 
  ("comment_we_were_defeated_cruel",                 "Last I saw you, you had been struck down by the men of {s54}. Don't worry -- we'll find him, and make him choke on his victory."), 
  ("comment_we_were_defeated_default",               "Last I saw you, you had been struck down by the men of {s54}. It is good to see you alive and well."), 

  ("comment_you_were_defeated_allied_friendly_spiteful",      "I heard that {s54} gave you a hard time. Don't worry, friend -- I'll find him for you, and make you a gift of his head."), 
  ("comment_you_were_defeated_allied_unfriendly_cruel",       "I had heard that {s54} slaughtered your men like sheep. But here you are, alive. Such a disappointment!"), 
  ("comment_you_were_defeated_allied_spiteful",               "I heard that {s54} crushed you underfoot like an ant. Hah! Children should not play games made for grown-ups, little {boy/girl}!"), 
  ("comment_you_were_defeated_allied_pitiless",               "I heard that {s54} defeated you, and scattered your forces. That is most disappointing..."), 
  ("comment_you_were_defeated_allied_unfriendly_upstanding",  "I heard that {s54} defeated you. Perhaps you should consider if you have considered any misdeeds, that might cause heaven to rebuke you in this way."), 
  ("comment_you_were_defeated_allied_unfriendly",             "I heard that {s54} defeated you. Look, try not to get too many of our men killed, will you?"), 
  ("comment_you_were_defeated_allied",                        "I heard that {s54} defeated you. But take heart -- the tables will soon be turned!"), 

  ("comment_you_helped_my_ally_unfriendly_chivalrous",        "I heard that you saved {s54} from likely defeat. Whatever else I may think of you, I must at least commend you for that."), 
  ("comment_you_helped_my_ally_unfriendly",                   "[revelance should be zero, and this message should not appear]"), 
  ("comment_you_helped_my_ally_liege",                        "I heard that you saved my vassal {s54} from likely defeat. "), 
  ("comment_you_helped_my_ally_unfriendly_spiteful",          "I heard that you rode to the rescue of our poor {s54}. Did you think him a damsel in distress? No matter -- it's a common mistake."), 
  ("comment_you_helped_my_ally_spiteful",                     "I heard that you saved {s54} from a whipping. You should have let him learn his lesson, in my opinion."), 
  ("comment_you_helped_my_ally_chivalrous",                   "I heard that you got {s54} out of a tight spot. That was a noble deed."), 
  ("comment_you_helped_my_ally_default",                   "I heard that you got {s54} out of a tight spot. Good work!"), 
 
  ("comment_you_were_defeated_allied_unfriendly",             "I heard that {s54} defeated you. Look, try not to get too many of our men killed, will you?"), 
  ("comment_you_were_defeated_allied",                        "I heard that {s54} defeated you. But take heart -- the tables will soon be turned!"), 

  ("comment_you_abandoned_us_unfriendly_spiteful",     "You worm! You left us alone to face {s54}, didn't you? I spit at you."), 
  ("comment_you_abandoned_us_unfriendly_pitiless",     "Well... You abandoned me in the middle of a battle with {s54}, didn't you? I'll see you buried in a traitor's grave."), 
  ("comment_you_abandoned_us_spiteful",                "You disappeared in the middle of that battle with {s54}... I hope you have a good explanation. Did your bowels give out? Were you shaking too hard with fear to hold your weapon?"), 
  ("comment_you_abandoned_us_chivalrous",              "What happened? You disappeared in the middle of that battle against {s54}. I can only hope that you were too badly wounded to stand, for I would be ashamed to have gone into battle alongside a coward."), 
  ("comment_you_abandoned_us_benefitofdoubt",          "What happened? You disappeared in the middle of that battle against {s54}. I assume that you must have been wounded, but it did look suspicious."), 
  ("comment_you_abandoned_us_default",                 "What happened? One moment you were fighting with us against {s54}, the next moment you were nowhere to be found?"), 

  ("comment_you_ran_from_me_enemy_spiteful",          "Last time we met, you ran from me like a whipped dog. Have you come back to bark at me again, or to whine for mercy?"), 
  ("comment_you_ran_from_me_enemy_chivalrous",        "Last time we met, you fled from me. Learn to stand and fight like a gentleman!"), 
  ("comment_you_ran_from_me_enemy_benevolent",        "When I saw you flee the last time that we met, I had hoped that I would not have to fight you again."), 
  ("comment_you_ran_from_me_enemy_coldblooded",       "Last time we met, you fled from me. That was a wise decision"),
  ("comment_you_ran_from_me_enemy",                   "You may have been able to escape the last time we crossed paths, but the next time I doubt that you be so lucky."), 

  ("comment_you_ran_from_foe_allied_chivalrous",      "They say that you fled from {s54}, leaving your men behind. I pray that this is not true, for such conduct does dishonour to us all."), 
  ("comment_you_ran_from_foe_allied_upstanding",      "They say that you fled from {s54}, leaving your men behind. I do not always believe such rumors, and I also know that desperate straits call for desperate measures. But I beg you to take more care of your good name, for men will not fight in our armies if they hear that we abandon them on the field of battle."), 
  ("comment_you_ran_from_foe_allied_spiteful",        "By the way, they said that you ran away from {s54} like a quaking little rabbit, leaving your men behind to be butchered. Ha! What a sight that would have been to see!"), 


  ("comment_you_defeated_my_friend_enemy_pragmatic",  "You may have bested {s54}, but you cannot defeat us all."), 
  ("comment_you_defeated_my_friend_enemy_chivalrous", "I have heard that you defeated {s54}, and ever since have been anxious to cross swords with you."), 
  ("comment_you_defeated_my_friend_enemy_spiteful",   "Your fame runs before you, {playername}. {s54} may have fallen for your tricks, but if you fight me, you'll find a me a much more slippery foe."), 
  ("comment_you_defeated_my_friend_enemy",            "They say that you have defeated {s54}. But I will be a truer test of your skill at arms."), 

  ("comment_you_captured_a_lord_allied_friendly_spiteful",   "I heard that you captured {s54}. I hope that you squeezed him for every denar."), 
  ("comment_you_captured_a_lord_allied_unfriendly_spiteful", "I heard that you captured {s54}. Your coffers must be well-bloated with ransom by now. Such a pity that money cannot transform a low-born cur into a gentleman!"), 
  ("comment_you_captured_a_lord_allied_chivalrous",          "I heard that you captured {s54}. Well done. I assume, of course, that he has been been treated with the honours due his rank."), 
  ("comment_you_captured_a_lord_allied",                     "I heard that you captured {s54}. Well done. His ransom must be worth quite something."), 

  ("comment_you_let_go_a_lord_allied_chivalrous",            "I heard that you captured {s54}, but then let him go. Such chivalry does a credit to our cause."),
  ("comment_you_let_go_a_lord_allied_upstanding",            "I heard that you captured {s54}, but then let him go. Well, that was an honourable course of action, if possibly also a dangerous one."),
  ("comment_you_let_go_a_lord_allied_coldblooded",           "I heard that you captured {s54}, but then let him go. That was most chivalrous of you, but chivalry does not win wars."),
  ("comment_you_let_go_a_lord_allied_unfriendly_spiteful",   "I heard that you captured {s54}, but then let him go. How very chivalrous of you! No doubt the widows and orphans he leaves in his wake will want to commend you in person."),
  ("comment_you_let_go_a_lord_allied",                       "I heard that you captured {s54}, but then let him go. Well, I will not tell you what to do with your own prisoners."),


  ("comment_you_let_me_go_spiteful",                    "When last we met, you had me at your mercy and allowed me to go free. I hope you enjoyed toying with me, like a cat with a mouse, because soon I will have you at my mercy, to slay or humiliate according to my fancy."),
  ("comment_you_let_me_go_enemy_chivalrous",            "When last we met, you had me at your mercy and allowed me to go free. That was most chivalrous of you, and I will not forget. But I also must remember my oath to my liege, and our kingdoms are still at war."),
  ("comment_you_let_me_go_enemy_coldblooded",           "When last we met, you had me at your mercy and allowed me to go free. But we are still enemies, and I cannot promise to repay your mercy in kind."),
  ("comment_you_let_me_go_enemy",                       "When last we met, you had me at your mercy and allowed me to go free. That was kind of you. But we are still at war."),
  ("comment_you_let_me_go_default",                     "When last we met, you had me at your mercy and allowed me to go free. That was kind of you, and I am glad that our kingdoms are no longer at war."),


#Internal faction events
  ("comment_pledged_allegiance_allied_martial_unfriendly",             "I heard that you have pledged allegiance to our lord, {s54}. Pray do not disgrace us by behaving in a cowardly fashion."),
  ("comment_pledged_allegiance_allied_martial",                        "I heard that you have pledged allegiance to our lord, {s54}. I look forward to fighting alongside you against our foes."),
  ("comment_pledged_allegiance_allied_quarrelsome_unfriendly",         "I heard that you have pledged allegiance to our lord, {s54}. Bah. Do yourself a favor, and stay out of my way."),
  ("comment_pledged_allegiance_allied_quarrelsome",                    "I heard that you have pledged allegiance to our lord, {s54}. Fight hard against our foes, respect your betters, and don't cross me, and we'll get along fine."),
  ("comment_pledged_allegiance_allied_selfrighteous_unfriendly",       "I heard that you have pledged allegiance to our lord, {s54}. If I were he, I would not trust you to clean the sculleries."),
  ("comment_pledged_allegiance_allied_selfrighteous",                  "I heard that you have pledged allegiance to our lord, {s54}. Fight bravely and you will be well-rewarded. Betray us, and we shall make of you the kind of example that will not soon be forgotten."),
  ("comment_pledged_allegiance_allied_cunning_unfriendly",             "I heard that you have pledged allegiance to our lord, {s54}. I do not pretend to be happy about his decision, but perhaps it is better to have you inside our tent pissing out, than the other way around."),
  ("comment_pledged_allegiance_allied_cunning",                        "I heard that you have pledged allegiance to our lord, {s54}. That is good. The more skilled fighters we have with us in these troubled times, the better. I shall be watching your progress."),
  ("comment_pledged_allegiance_allied_debauched_unfriendly",           "I heard that you have pledged allegiance to our lord, {s54}. No doubt you will soon betray him, and I will have the pleasure of watching you die a traitor's death."),
  ("comment_pledged_allegiance_allied_debauched",                      "I heard that you have pledged allegiance to our lord, {s54}. Excellent... I am sure that you and I will become very good friends. But remember -- if you betray us, it will be the biggest mistake you will ever make."),
  ("comment_pledged_allegiance_allied_goodnatured_unfriendly",         "I heard that you have pledged allegiance to our lord, {s54}. Well, I can't say that I would have trusted you, but perhaps you deserve the benefit of the doubt."),
  ("comment_pledged_allegiance_allied_goodnatured",                    "I heard that you have pledged allegiance to our lord, {s54}. Good {man/woman}! Our lord is a noble soul, and rewards loyalty and valor with kindness and generosity."),
  ("comment_pledged_allegiance_allied_upstanding_unfriendly",          "I heard that you have pledged allegiance to our lord, {s54}. Alas, from what I know of you I fear that you will disgrace us, but I will be happy if you prove me wrong."),
  ("comment_pledged_allegiance_allied_upstanding",                     "I heard that you have pledged allegiance to our lord, {s54}. Fight against our foes with valor, but also with honour and compassion. A good name is as valuable as a sharp sword or a swift horse in affairs of arms."),


  ("comment_our_king_granted_you_a_fief_allied_friendly_cruel",     "I heard that {s54} granted you {s51} as a fief. Don't forget -- spare the whip and spoil the peasant!"),
  ("comment_our_king_granted_you_a_fief_allied_friendly_cynical",   "I heard that {s54} granted you {s51} as a fief. I am glad to see you prosper -- but be careful. Men are vipers, envious and covetous of their neighbours' wealth. Stay close to me, and I'll watch your back."),

  ("comment_our_king_granted_you_a_fief_allied_friendly",              "I heard that {s54} granted you {s51} as a fief. May your new lands prosper."),
  ("comment_our_king_granted_you_a_fief_allied_unfriendly_upstanding", "I heard that {s54} granted you {s51} as a fief. But keep in mind that pride goes before a fall."),
  ("comment_our_king_granted_you_a_fief_allied_unfriendly_spiteful",   "I heard that {s54} granted you {s51} as a fief. I suspect, however, that fortune is only raising you up so as to humble you even more, when it casts you back into the dung from whence you came."),
  ("comment_our_king_granted_you_a_fief_allied_spiteful",              "I heard that {s54} granted you {s51} as a fief. Let's hope you are indeed deserving of our lord's favor."),

  ("comment_our_king_granted_you_a_fief_allied",                       "I heard that {s54} granted you {s51} as a fief. You seem to be doing very well for yourself."),

  ("comment_you_renounced_your_alliegance_enemy_friendly",             "I heard that you renounced your allegiance to our lord, {s54}. It grieves me that we must now meet on the field of battle."),
  ("comment_you_renounced_your_alliegance_friendly",                   "I heard that you renounced your allegiance to our lord, {s54}. Let us pray that we may not come to blows."),
  ("comment_you_renounced_your_alliegance_unfriendly_spiteful",        "I always had you figured for a traitor to {s54}, and now it seems I was proven right. I hope you are prepared to die a traitor's death!"),
  ("comment_you_renounced_your_alliegance_unfriendly_moralizing",      "I heard that you renounced your allegiance to our lord, {s54}. I am forced to consider you a traitor."),
  ("comment_you_renounced_your_alliegance_enemy",                      "I heard that you renounced your allegiance to our lord, {s54}. Well, it is the way of the world for old comrades to become enemies."),
  ("comment_you_renounced_your_alliegance_default",                    "I heard that you renounced your allegiance to our lord, {s54}. Well, that is your decision, but do not expect me to go easy on you when we meet on the battlefield."),


  ("personality_archetypes",   "liege"),
  ("martial",                  "martial"),
  ("quarrelsome",              "bad-tempered"),
  ("selfrighteous",            "pitiless"),
  ("cunning",                  "cunning"),
  ("debauched",                "sadistic"),
  ("goodnatured",              "good-natured"),
  ("upstanding",               "upstanding"),

  ("surrender_demand_default",        "Yield or die!"),
  ("surrender_demand_martial",        "The odds are not in your favor today. You may fight us, but there is also no shame if you yield now."),
  ("surrender_demand_quarrelsome",    "I've got you cornered. Give up, or I'll ride you down like a dog."),
  ("surrender_demand_pitiless",       "You cannot defeat me, and I'll teach you a painful lesson if you try. Yield!"),
  ("surrender_demand_cunning",        "You are outmatched today. Give up -- if not for your own sake, then think of your men!"),
  ("surrender_demand_sadistic",       "Surrender or I'll gut you like a fish!"),
  ("surrender_demand_goodnatured",    "We have the advantage of you. Yield, and you will be well-treated."),
  ("surrender_demand_upstanding",     "You may fight us, but many of your men will be killed, and you will probably lose. Yield, and spare us both the unnecessary bloodshed."),

  ("surrender_offer_default",        "Stop! I yield!"),
  ("surrender_offer_martial",        "Stop! I yield!"),
  ("surrender_offer_quarrelsome",    "Enough! You win today, you dog! Ach, the shame of it!"),
  ("surrender_offer_pitiless",       "I yield! You have won. Cursed be this day!"),
  ("surrender_offer_cunning",        "Stop! I yield to you!"),
  ("surrender_offer_sadistic",       "I give up! I give up! Call back your dogs!"),
  ("surrender_offer_goodnatured",    "I yield! Congratulations on your victory, {sir/madame}!"),
  ("surrender_offer_upstanding",     "I yield! Grant me the honours of war, and do yourself credit!"),

  ("prisoner_released_default",       "You have my gratitude, {sir/madame}. I shall not forget your kindness."),
  ("prisoner_released_martial",       "You are indeed a {man/woman} of honour, {sir/madame}. I shall not forget this!"),
  ("prisoner_released_quarrelsome",   "I'm free? Well... Good bye, then."),
  ("prisoner_released_pitiless",      "Thank you. When you are finally defeated, I will request for your death to be swift and merciful. Unless, that is, you care to join us... Good bye, for now."),
  ("prisoner_released_cunning",       "Am I? You are a good {man/woman}. I will try to find a way to repay you."),
  ("prisoner_released_sadistic",      "Am I? So refined is your cruelty, that you would rather see me free and humiliated, than in chains. Enjoy your triumph!"),
  ("prisoner_released_goodnatured",   "You are indeed a {man/woman} of honour, {sir/madame}. I shall not forget this!"),
  ("prisoner_released_upstanding",    "You are indeed a {man/woman} of honour, {sir/madame}. I shall not forget this!"),

#Post 0907 changes begin
  ("enemy_meet_default",              "Who are you, that comes in arms against me?"),
  ("enemy_meet_martial",              "What is your name, {sir/madame}? If we come to blows, I would know whom I fight."),
  ("enemy_meet_quarrelsome",          "Who the hell are you?"),
  ("enemy_meet_pitiless",             "Who are you? Speak, so that I may know whom I slay."),
  ("enemy_meet_cunning",              "Tell me your name. It is always good to know your enemy."),
  ("enemy_meet_sadistic",             "Who are you? Speak quick, before I cut your tongue out."),
  ("enemy_meet_goodnatured",          "What is your name, {sir/madame}? If we come to blows, I would know whom I fight."),
  ("enemy_meet_upstanding",           "Who are you, who would come in arms to dispute our righteous cause?"),

  ("battle_won_default",              "You have proven yourself a most valued ally, today."),
  ("battle_won_martial",              "There is no greater fortune than the chance to show one's valor on the field of arms!"),
  ("battle_won_quarrelsome",          "Hah! We showed those bastards a thing or two, there, didn't we?"),
  ("battle_won_pitiless",             "Together, we will make the foe learn to fear our names, and to quail at our coming!"),
  ("battle_won_cunning",              "Now, we must be sure to press our advantage, so that the blood shed today is not wasted."),
  ("battle_won_sadistic",             "Now let us strip their dead and leave them for the crows, so that all will know the fate of those who come against us."),
  ("battle_won_goodnatured",          "That was a good scrap! No joy like the joy of victory, eh?"),
  ("battle_won_upstanding",           "Now, let us give thanks to the heavens for our victory, and mourn the many fine men who have fallen today."),

  ("battle_won_grudging_default",     "You helped turn the tide on the field, today. Whatever I may think of you, I cannot fault you for your valor."),
  ("battle_won_grudging_martial",     "{playername} -- you have shown yourself a worthy {man/woman} today, whatever your misdeeds in the past."),
  ("battle_won_grudging_quarrelsome", "Hmf. Yours is not a face which I normally like to see, but I suppose today I should thank you for your help."),
  ("battle_won_grudging_pitiless",    "Your help was most valuable today. I would not imagine that you came to help me out of kindness, but I nonetheless thank you."),
  ("battle_won_grudging_cunning",     "It would be unwise of me not to thank you for coming to help me in my hour of need. So... You have my gratitude."),
  ("battle_won_grudging_sadistic",    "Well! How touching! {playername} has come to rescue me."),
  ("battle_won_grudging_goodnatured", "{playername}! I can't say that we've always gotten along in the past, but you fought well today. My thanks to you!"),
  ("battle_won_grudging_upstanding",  "Perhaps I was wrong about you. Your arrival was most timely. You have my gratitude."),

  ("battle_won_unfriendly_default",         "So you're here. Well, better late than never, I suppose."),
  ("battle_won_unfriendly_martial",         "We have hard harsh words in the past, but for now let us simply enjoy our victory."),
  ("battle_won_unfriendly_quarrelsome",     "If you're standing there waiting for thanks, you can keep waiting. Your help wasn't really needed, but I guess you had nothing better to do, right?"),
  ("battle_won_unfriendly_pitiless",        "You have come here, like a jackal to a lion's kill. Very well then, help yourself to the spoils. I shall not stop you."),
  ("battle_won_unfriendly_cunning",         "{playername}... Well, I suppose your arrival didn't hurt, although I won't pretend that I'm happy to see you."),
  ("battle_won_unfriendly_sadistic",        "Back off, carrion fowl! This was my victory, however hard you try to steal the glory for yourself."),
  ("battle_won_unfriendly_goodnatured",     "Oh, it's you. Well, I suppose I should thank you for your help."),
  ("battle_won_unfriendly_upstanding",      "Thank you for coming to my support. Now I will be off, before I say something that I regret."),

  ("troop_train_request_default",               "I need someone like you to knock them into shape."),
  ("troop_train_request_martial",               "They need someone to show them the meaning of valor."),
  ("troop_train_request_quarrelsome",           "Fat lazy bastards. They make me puke."),
  ("troop_train_request_pitiless",              "They are more afraid of the enemy than they are of me, and this will not do."),
  ("troop_train_request_cunning",               "But men, like swords, are tempered and hardened by fire."),
  ("troop_train_request_sadistic",              "They need someone with steel in his back to flog some courage into them, or kill them trying."),
  ("troop_train_request_goodnatured",           "They're good enough lads, but I am afraid that they are not quite ready for a battle just yet."),
  ("troop_train_request_upstanding",            "It would be tantamount to murder for me to lead them into combat in their current state."),

  ("unprovoked_attack_default",               "What? Why do you attack us? Speak, you rascal!"),
  ("unprovoked_attack_martial",               "I have no objection to a trial of arms, but I would ask you for what reason you attack us?"),
  ("unprovoked_attack_quarrelsome",           "You're making a big mistake, {boy/girl}. What do you think you're doing?"),
  ("unprovoked_attack_pitiless",              "Indeed? If you really want to die today, I'd be more than happy to oblige you, but I am curious as to what you hope to accomplish."),
  ("unprovoked_attack_cunning",               "Really? I think that you are acting most unwisely. What do you hope to gain by this?"),
  ("unprovoked_attack_sadistic",              "What's this? Do you enjoy having your eyes put out?"),
  ("unprovoked_attack_goodnatured",           "Why do you do this? We've got no quarrel, {sir/madame}."),
  ("unprovoked_attack_upstanding",            "I consider this an unprovoked assault, and will protest to your king. Why do you do this?"),

  ("unnecessary_attack_default",               "I will not hesitate to cut you down if pressed, but I will offer you the chance to ride away from this."),
  ("unnecessary_attack_martial",               "I am eager to take you up on your challenge, {sir/madame}, although I will give you a minute to reconsider."),
  ("unnecessary_attack_quarrelsome",           "Bah! I'm in no mood for this nonsense today. Get out of my way."),
  ("unnecessary_attack_pitiless",              "I am in a merciful mood today. I will pretend that I did not hear you."),
  ("unnecessary_attack_cunning",               "I don't see what you have to gain by making an enemy of me. Maybe you should just ride away."),
  ("unnecessary_attack_sadistic",              "I have no time to waste on a worm like you. Get out of my way."),
  ("unnecessary_attack_goodnatured",           "I don't see what you have to gain by picking a fight, {sir/madame}. You can still ride away."),
  ("unnecessary_attack_upstanding",            "If a fight is what you wish, {sir/madame}, then you will have one, but I will yet offer you the chance to back down."),

  ("lord_challenged_default",                   "As you wish. Prepare to die!"),
  ("lord_challenged_martial",                   "So be it. Defend yourself!"),
  ("lord_challenged_quarrelsome",               "You impudent whelp! I'll crush you!"),
  ("lord_challenged_pitiless",                  "If you so badly wish to die, then I have no choice but to oblige you."),
  ("lord_challenged_cunning",                   "Well, if you leave me no choice..."),
  ("lord_challenged_sadistic",                  "You heap of filth! I'll make you wish you'd never been born."),
  ("lord_challenged_goodnatured",               "Very well. I had hoped that we might avoid coming to blows, but I see that have no choice."),
  ("lord_challenged_upstanding",                "So be it. It saddens me that you cannot be made to see reason."),

  ("lord_mission_failed_default",               "Well, I am disappointed, but I am sure that you will have many chances to redeem yourself."),
  ("lord_mission_failed_martial",               "There is no honour in failing a quest which you endeavoured to take, but I will accept your word on it."),
  ("lord_mission_failed_quarrelsome",           "You failed? Bah. I should have expected as much from the likes of you."),
  ("lord_mission_failed_pitiless",              "You failed? Well. You disappoint me. That is a most unwise thing to do."),
  ("lord_mission_failed_cunning",               "Well, I am disappointed, but no one can guarantee that the winds of fortune will always blow their way."),
  ("lord_mission_failed_sadistic",              "Indeed? Those who fail me do not always live to regret it."),
  ("lord_mission_failed_goodnatured",           "Oh well. It was a long shot, anyway. Thank you for making an effort."),
  ("lord_mission_failed_upstanding",            "Very well. I am sure that you gave it your best effort."),

  ("lord_follow_refusal_default",       "Follow you? You forget your station, {sir/madame}."),
  ("lord_follow_refusal_martial",       "Perhaps if you one day prove yourself a valorous and honourable warrior, then I would follow you. But not today."),
  ("lord_follow_refusal_quarrelsome",   "Follow someone like you? I don't think so."),
  ("lord_follow_refusal_pitiless",      "Lords like me do not follow people like you, {sir/madame}."),
  ("lord_follow_refusal_cunning",       "First show me that you are the type of {man/woman} who will not lead me into disaster, and then perhaps I will follow you."),
  ("lord_follow_refusal_sadistic",      "I think not! Rather, you should follow me, as a whipped cur follows {his/her} master."),
  ("lord_follow_refusal_goodnatured",   "Um, I am a bit pressed with errands right now. Perhaps at a later date."),
  ("lord_follow_refusal_upstanding",    "First show me that you are worthy to lead, and then perhaps I will follow."),



  ("lord_insult_default",               "base varlot"),
  ("lord_insult_martial",               "dishonourable knave"),
  ("lord_insult_quarrelsome",           "filth-swilling bastard"),
  ("lord_insult_pitiless",              "low-born worm"),
  ("lord_insult_cunning",               "careless oaf"),
  ("lord_insult_sadistic",              "sniveling cur"),
  ("lord_insult_goodnatured",           "unpleasant fellow"),
  ("lord_insult_upstanding",            "disgraceful scoundrel"),


  ("rebellion_dilemma_default",                 "[liege]"),
  ("rebellion_dilemma_martial",                 "{s45} was clearly wronged. Although I gave an oath to {s46}, it does not bind me to support him if he usurped his throne illegally."),
  ("rebellion_dilemma_quarrelsome",             "Hmm. {s46} has never given me my due, so I don't figure I owe him much. However, maybe {s45} will be no better, and {s46} has at least shown himself ."),
  ("rebellion_dilemma_pitiless",                "Hmm. {s45} says {reg3?she:he} is the rightful heir to the throne. That is good -- it absolves me of my oath to {s46}. But still I must weight my decision carefully."),
  ("rebellion_dilemma_cunning",                 "Hmm. I gave an oath of homage to {s46}, yet the powerful are not bound by their oaths as our ordinary people. Our duty is to our own ability to rule, to impose order and prevent the war of all against all."),
  ("rebellion_dilemma_sadistic",                "Hmm. In this vile world, a wise man must think of himself, for no one else will. So -- what's in it for me?"),
  ("rebellion_dilemma_goodnatured",             "I do not know what to say. I gave an oath to {s46} as the lawful ruler, but if he is not the lawful ruler, I don't know if I am still bound."),
  ("rebellion_dilemma_upstanding",              "This is troublesome. It is a grave thing to declare my homage to {s46} to be null and void, and dissolve the bonds which keep our land from sinking into anarchy. Yet I am also pledged to support the legitimacy of the succession, and {s45} also has a valid claim to the throne."),

  ("rebellion_dilemma_2_default",               "[liege]"),
  ("rebellion_dilemma_2_martial",               "On the other hand, {s46} has led us in war and peace, and I am loathe to renounce my allegiance."),
  ("rebellion_dilemma_2_quarrelsome",           "So tell me, why should I turn my back on the bastard I know, in favor of {reg3?a woman:the bastard} I don't know?"),
  ("rebellion_dilemma_2_pitiless",              "It is a most perilous position to be in, to be asked whom I would make {reg3?ruler:king} of this land. Yet it is also a time of opportunity, for me to reap the rewards that have always been my due!"),
  ("rebellion_dilemma_2_cunning",               "{s46} has been challenged, and thus he will never be able to rule as strongly as one whose claim has never been questioned. Yet if {s45} takes the throne by force, {reg3?she:he} will not be as strong as one who succeeded peacefully."),
  ("rebellion_dilemma_2_sadistic",              "Perhaps if I join {s45} while {reg3?she:he} is still weak {reg3?she:he} will enrich me, but perhaps if I bring {s46} your head he will give me an even greater reward."),
  ("rebellion_dilemma_2_goodnatured",           "{s46} has always treated me decently, yet it's true that he did wrong to {s45}. I hesitate to renounce my homage to {s46}, yet I also don't think it's right to support injustice."),
  ("rebellion_dilemma_2_upstanding",            "I feel that I must do whatever is best for the realm, to avoid it being laid waste by civil war and ravaged by its enemies."),


  ("rebellion_prior_argument_very_favorable",   "I have already heard some arguments for supporting your candidate for the throne, and I tend to agree with them."),
  ("rebellion_prior_argument_favorable",        "I have already heard some arguments for supporting your candidate for the throne, and I tend to agree with them."),
  ("rebellion_prior_argument_unfavorable",      "I have already heard some arguments for supporting your candidate for the throne, but I do not find them convincing."),
  ("rebellion_prior_argument_very_unfavorable", "I have already heard some arguments for supporting your candidate for the throne, but I disagree with most of them."),

  ("rebellion_rival_default",                   "[liege]"),
  ("rebellion_rival_martial",                   "{s49} your ally {s44} once questioned my honour and my bravery. It's not often I get the chance to face him in battle, and make him retract his statement."),
  ("rebellion_rival_quarrelsome",               "{s49} you're working with {s44}. He's a crafty weasel, and I don't trust him one bit."),
  ("rebellion_rival_pitiless",                  "{s49} you seem to have enlisted the support of {s44} -- who is soft, and weak, and not fit to govern a fief, and whom I have always detested."),
  ("rebellion_rival_cunning",                   "{s49} {s44}, who has already joined you, is headstrong and quarrelsome, and a bit of liability."),
  ("rebellion_rival_sadistic",                  "{s49} I have no desire to fight alongside your ally {s44}, who puts on such a nauseating display of virtue."),
  ("rebellion_rival_goodnatured",               "{s49} I'd be reluctant to be on the same side as {s44}, who has quite a reputation for cruelty."),
  ("rebellion_rival_upstanding",                "{s49} your ally {s44} is in my opinion a dangerous, unreliable, and highly unprincipled man."),

  ("rebellion_argument_favorable",              "I respect your line of argument"),
  ("rebellion_argument_neutral",                "I find your line of argument only moderately compelling"),
  ("rebellion_argument_unfavorable",            "I do not find your line of argument compelling"),

  ("rebellion_persuasion_favorable",            "you state your case eloquently"),
  ("rebellion_persuasion_neutral",              "you make a reasonable case"),
  ("rebellion_persuasion_unfavorable",          "you make an unconvincing case"),

  ("rebellion_relation_very_favorable",         "I have the greatest respect for you personally."),
  ("rebellion_relation_favorable",              "I know and respect you personally."),
  ("rebellion_relation_neutral",                "I do not know you as well as I might like."),
  ("rebellion_relation_unfavorable",            "I do not trust you."),

  ("and_comma_3", "Furthermore, "),
  ("but_comma_3", "However,"),

  ("and_comma_1", ", and "),
  ("but_comma_1", ", but "),

  ("and_comma_2", ". Moreover, "),
  ("but_comma_2", ". Nonetheless, "),


  ("rebellion_agree_default",               "[liege]"),
  ("rebellion_agree_martial",               "I have decided. I will back {s45} as the rightful heir."),
  ("rebellion_agree_quarrelsome",           "Ahh, I've thought long enough. I never did like {s46} much anyway. Let's go take his throne away from him."),
  ("rebellion_agree_pitiless",              "You are fortunate. I have decided to join you. Pray do not give me cause to regret this decision."),
  ("rebellion_agree_cunning",               "This is a most dangerous decision, but after careful consideration, I have decided that I will join you. Let's hope it is for the best."),
  ("rebellion_agree_sadistic",              "I have decided. I will back your {reg3?woman:man} {s45}. But you'd best make sure that {reg3?she:he} rewards me well!"),
  ("rebellion_agree_goodnatured",           "All right. I think your {reg3?woman:man} will be a good ruler. I'll join you."),
  ("rebellion_agree_upstanding",            "So be it. My first duty is to this realm, and to save it from lawlessness I will back {s45} and renounce my homage to {s46}. May the Heavens forgive me if I do wrong."),


  ("rebellion_refuse_default",              "[liege]"),
  ("rebellion_refuse_martial",              "I am sorry. {s45} has a good claim, but it's not enough for me to turn my back on {s46}. I will remain loyal to my liege."),
  ("rebellion_refuse_quarrelsome",          "Nah. Your whelp {s45} doesn't have what it takes to rule this realm. I'm sticking with {s46}."),
  ("rebellion_agree_pitiless",              "No. I will not join your rebellion. I count it little more than the tantrum of a child, denied a bauble which {reg3?she:he} thinks should be {reg3?hers:his}. I will stick with {s46}, whose ability to rule is well-tested."),
  ("rebellion_agree_cunning",               "I am sorry. You do not give me reason for confidence that you will win. Many will die, but I do not wish to be among them. I will continue to back {s46}."),
  ("rebellion_agree_sadistic",              "No. I won't play your little game. You grasp at a crown, but I think instead you'll get a quick trip to the scaffold, and I'll be there by {s46}'s side to watch the headsman's axe drop."),
  ("rebellion_agree_goodnatured",           "I am sorry. I don't feel right turning my back on {s46}. No hard feelings when me meet on the battlefield."),
  ("rebellion_agree_upstanding",            "I am sorry. {s45}'s claim is not strong enough for me to inflict the curse of civil disorder on the poor wretches of this land. I will continue to back {s46}. May the Heavens forgive me if I do wrong."),

  ("talk_later_default",                    "[liege]"),
  ("talk_later_martial",                    "Now is not the time to talk politics! I am here today with my fellow lords, armed for battle. You'd better prepare to fight."),
  ("talk_later_quarrelsome",                "Do you expect me to discuss betraying my liege with you, while we are surrounded by his army? What do you take me for, a bloody idiot?"),
  ("talk_later_pitiless",                   "Still your tongue! Whatever I have to say on this matter, I will not say it here and now, while we are in the midst of our army."),
  ("talk_later_cunning",                    "This is hardly the time or the place for such a discussion. Perhaps we can discuss it at a later time and a different place, but for now we're still foes."),
  ("talk_later_sadistic",                   "You should have your mouth sewn shut! Can you imagine what would happen if the other vassals see me talking to you of treason?"),
  ("talk_later_goodnatured",                "So you wish to discuss your rebellion with me? Try that again when we aren't surrounded by my liege's army, and I will hear what you have to say."),
  ("talk_later_upstanding",                 "Whatever my thoughts on the legitimacy of the succession, I am not about to discuss them here and now. If we meet again when we can talk in privacy, I will hear what you have to say on the matter. But for now, consider me your enemy."),


  ("gossip_about_character_default",        "They say that {s6} doesn't possess any interesting character traits."),
  ("gossip_about_character_martial",        "They say that {s6} loves nothing more than war."),
  ("gossip_about_character_quarrelsome",    "They say that {s6} almost came to blows with another lord lately, because the man made a joke about his nose."),
  ("gossip_about_character_selfrighteous",  "I heard that {s6} had a squire executed because the unfortunate man killed a deer in his forest."),
  ("gossip_about_character_cunning",        "They say that {s6} is a cunning opponent."),
  ("gossip_about_character_sadistic",       "They say that {s6} likes to torture his enemies. I wouldn't want to get on the bad side of that man."),
  ("gossip_about_character_goodnatured",    "They say that {s6} is a good man and treats people living in his lands decently. That is more than what can be said for most of the nobles."),
  ("gossip_about_character_upstanding",     "People say that it is good to be in the service of {s6}. He is good to his followers, and rewards them if they work well."),

  ("latest_rumor",        "The latest rumor you heard about {s6} was:"),


#steve post 0912 changes begin

  ("swadian_rebellion_pretender_intro",    "I am Isolla, rightful Queen of the Swadians."),
  ("vaegir_rebellion_pretender_intro",     "My name is Valdym. Some men call me 'the Bastard.' I am a prince of the Vaegirs, but by all rights I should be their king, instead of my cousin Yaroglek."),
  ("khergit_rebellion_pretender_intro",    "I am Dustum Khan, son of Janakir Khan, and rightful Khan of the Khergits."),
  ("nord_rebellion_pretender_intro",       "I am Lethwin Far-Seeker, son of Hakrim the Old, who should be king of the Nords of Calradia."),
  ("rhodok_rebellion_pretender_intro",     "I am Lord Kastor, the rightful King of the Rhodoks, who will free them from tyranny."),

  ("swadian_rebellion_pretender_story_1",  "I was the only child of my father, King Esterich. Although I am a woman, he loved me like a son and named me his heir -- not once, but several times, before the grandest nobles of the land so that none could doubt his intention. There is no law that bars a woman from ruling -- indeed, we Swadians tell tales of warrior queens who ruled us in our distant past."),
  ("vaegir_rebellion_pretender_story_1",   "My father died when I was young, leaving me in the care of his brother, the regent Burelek. But rather than hold the throne until I came of age, this usurper used his newfound power to accuse my mother of adultery, and to claim that I was not my father's son. She was executed for treason, and I was declared a bastard."),
  ("khergit_rebellion_pretender_story_1",  "Sanjar Khan and I are brothers, sons of the old Janakir Khan, although of different mothers. Although I was the younger brother, all those who knew the old Khan will testify that throughout my father's life, I was his favorite, entrusted with the responsibilities of government. Sanjar busied himself with hunts and feasts to win the affection of the more dissolate of my father's commanders."),
  ("nord_rebellion_pretender_story_1",     "I am called the Far-Seeker because I have travelled great distances, even by the standards of the Nords, in search of knowledge. Before I came of age, my father sent me abroad on a tour of study at the courts and universities in the lands overseas. If the Nords are to call themselves the heirs of the Calradian empire, then they must act the part, and know something of law and letters, and not call themselves content merely to fight, plunder, and drink."),
  ("rhodok_rebellion_pretender_story_1",   "The Rhodoks are a free people, and not slaves to any hereditary monarch. The king must be chosen from one of the leading noble families of the land, by a council drawn by lot from the patricians of the cities of Jelkala, Veluca, and Yalen. The council meets on a field before Jelkala, and no man is allowed to appear in arms during their deliberations, on pain of death."),

  ("swadian_rebellion_pretender_story_2",  "Yet when my father died, his cousin Harlaus convinced the nobles that no Swadian king of sound mind could name a woman as his heir. Harlaus said that his designation of me was the act of a madman, and thus had no legal standing, and that he, as my father's closest male relative, should of take the throne."),
  ("vaegir_rebellion_pretender_story_2",   "I was smuggled abroad by a faithful servant, but now I am of age and have returned to reclaim what is rightfully mine. Burelek died soon after his act of perfidy -- the judgment of heaven, no doubt. His son Yaroglek now calls himself king, but as his claim is tainted, he is no less a usurper than his father, and I will topple him from his throne."),
  ("khergit_rebellion_pretender_story_2",  "According to Khergit custom, when a man dies his herds are split between all his sons, equally. So too it is with the khanate. When I heard of my father's death, I was away inspecting our borders, but I hurried home to Tulga, ready to give Sanjar his due and share the khanate with him. But when I arrived, I found that he rushed his supporters to the court, to have himself proclaimed as the sole khan."),
  ("nord_rebellion_pretender_story_2",     "My father died however before I completed my course of study, and as I hurried home to claim his throne my ship was wrecked by a storm. One of my father's thanes, Ragnar, seized this opportunity and spread rumors that I had died abroad. He summoned a gathering of his supporters to have himself proclaimed king, and has taken the past few years to consolidate his power."),
  ("rhodok_rebellion_pretender_story_2",   "During the last selection, there were but two candidates, myself, and Lord Graveth. While the council was deliberating, Graveth appeared, sword in hand, telling them that a Swadian raiding party was about to descend on the field of deliberation -- which was true, by the way -- and if he were not elected king, then he would leave them to their fate."),

  ("swadian_rebellion_pretender_story_3",  "I will admit that I did my cause no good by cursing Harlaus and all who listened to him as traitors, but I also believe that the magistrates who ruled in his favor were bought. No matter -- I will raise an army of loyal subjects, who would honour their old king's memory and will. And if anyone doubts that a woman can wield power, then I will prove them wrong by taking Harlaus' ill-gotten crown away from him."),
  ("vaegir_rebellion_pretender_story_3",   "Until I have my rights restored in the sight of all the Vaegirs, I will bear the sobriquet, 'the Bastard', to remind me of what I must do."),
  ("khergit_rebellion_pretender_story_3",  "My brother thinks that Khergits will only respect strength: a leader who takes what he wants, when he wants it. But I think that he misreads the spirit of our people.--we admire a resolute leader, but even more we a just one, and we know that a man who does not respect his own brother's rights will not respect the rights of his followers."),
  ("nord_rebellion_pretender_story_3",     "So I remain in exile -- except now I am not looking for sages to tutor me in the wisdom of faraway lands, but warriors, to come with me back to the land of the Nords and regain my throne. If Ragnar doubts my ability to rule, then let him say so face to face, as we stare at each other over the rims of our shields. For a warrior can be a scholar, and a scholar a warrior, and to my mind, only one who combines the two is fit to be king!"),
  ("rhodok_rebellion_pretender_story_3",   "Well, Graveth defeated the Swadians, and for that, as a Rhodok, I am grateful. When I am king, I will myself place the wreath of victory on his head. But after that I will have it separated from his shoulders, for by his actions he has shown himself a traitor to the Rhodok confederacy and its sacred custom."),

  ("swadian_rebellion_monarch_response_1", "Isolla thinks she should be Queen of the Swadians? Well, King Esterich had a kind heart, and doted on his daughter, but a good-hearted king who doesn't use his head can be a curse to his people. Isolla may tell you stories of warrior queens of old, but you might also recall that all the old legends end in the same way -- with the Swadians crushed underfoot by the armies of the Calradic Emperor."),
  ("vaegir_rebellion_monarch_response_1",  "Were Valdym to come to me in peace, I would laden him with titles and honours, and he would become the greatest of my vassals. But as he comes in war, I will drag him before me in chains and make him acknowledge me as rightful sovereign, then cut his tongue from his mouth so that he cannot recant."),
  ("khergit_rebellion_monarch_response_1", "My brother Dustum has perhaps told you of his insistence upon splitting the khanate, as though it were a herd of sheep. Let me tell you something. Ever since the Khergits established themselves on this land, the death of every khan has had the same result -- the land was divided, the khan's sons went to war, and the strongest took it all anyway. I simply had the foresight to stave off the civil war in advance."),
  ("nord_rebellion_monarch_response_1",    "Lethwin 'Far-Seeker'? Lethwin Inkfingers, is more like it. Perhaps you have heard the expression, 'Unhappy is the land whose king is a child.' Unhappy too is the land whose king is a student. You want the Nords to be ruled by a beardless youth, whose hand bears no callouses left by a sword's grip, who has never stood in a shield wall? If Lethwin were king, his thanes would laugh at him to his face!"),
  ("rhodok_rebellion_monarch_response_1",  "No doubt Lord Kastor told you that I defiled the hallowed Rhodok custom by interfering with the patricians' election of a king. Well, let me tell you something. The patricians of the towns make longwinded speeches about our ancient liberties, but then choose as their king whichever noble last sat in their villa and sipped a fine wine and promised to overlook their unpaid taxes."),

  ("swadian_rebellion_monarch_response_2", "Those who weep for the plight of a Swadian princess denied her father's throne should reflect instead on the fate of a Swadian herdswoman seized by a Vaegir raider and taken as chattel to the slave markets. Talk to me of queens and old stories when our warlike neighbors are vanquished, and our land is at peace."),
  ("vaegir_rebellion_monarch_response_2",  "Whatever my father may or may not have done to secure the throne does not matter. I have inherited it, and that is final. If every old claim were to be brought up anew, if every man's inheritance could be called into question at any time, then it would be the end of the institution of kingship, and we would live in a state of constant civil war."),
  ("khergit_rebellion_monarch_response_2", "Dustum would make a fine assessor of flocks, or adjudicator of land disputes. But can you imagine such a man as khan? We would be run off of our land in no time by our neighbors, and return to our old days of starving and freezing on the steppe."),
  ("nord_rebellion_monarch_response_2",    "Old Hakrim may have had fancy ideas about how to dispose of his kingdom, but it is not just royal blood that makes a King of the Nords. I am king by acclamation of the thanes, and by right of being the strongest. That counts for more than blood, and woe to any man in this land who says otherwise."),
  ("rhodok_rebellion_monarch_response_2",  "The only liberty that concerns them is their liberty to grow fat. Meanwhile, my men sleep out on the steppe, and eat dry bread and salt fish, and scan the horizon for burning villages, and shed our blood to keep the caravan routes open. Here's an idea -- if I ever meet a merchant who limps from a Khergit arrow-wound or a Swadian sword-stroke, then I'll say, 'Here's a man whose counsel is worth taking.'"),


#steve post 0912 changes end




  ("credits_1", "Mount&Blade Copyright 2001-2008 Taleworlds Entertainment"),
  ("credits_2", "Game design:^Armagan Yavuz^Steve Negus^Cem Cimenbicer"),
  ("credits_3", "Programming:^Armagan Yavuz^Cem Cimenbicer"),
  ("credits_4", "CG Artists:^Ipek Yavuz^Ozgur Saral^Mustafa Ozturk"),
  ("credits_8", "Animation:^Pinar Cekic^Umit Singil"),
  ("credits_5", "Concept Artist:^Ganbat Badamkhand"),
  ("credits_6", "Writing:^Steve Negus^Ryan A. Span^Armagan Yavuz"),
  ("credits_9", "Original Music:^Jesse Hopkins"),
  ("credits_7", "Additional Modeling:^Hilmi Aric^Ahmet Sarisakal^Katie Beedham^^^Additional Writing:^Michael Buhler^Patrick Desjardins^^^Voice Talents:^Tassilo Egloffstein^Jade E Henderson^^^\
Original Music Composed by:^Jesse Hopkins^\
Violin Solos Performed by:^Zoriy Zinger^\
Main Theme and Scherzo Performed by:^The Russian State Symphony Cinema Orchestra, Conducted by Sergei Skripka^^^\
Sound Samples:^Audiosparx.com^^^\
Mount&Blade Map Editor:^Matt Stentiford^^^\
Taleworlds Forum Programming:^Brett Flannigan www.fenrisoft.com^^^\
Mount&Blade Tutorial written by:^Edward Spoerl^^^\
Gameplay Videos:^Jemes Muia^^^\
Motion Capture System:^NaturalPoint-Optitrack Arena^^^\
Horse Motion Capture Animation Supplied by:^Richard Widgery & Kinetic Impulse^^^\
Ragdoll Physics:^Newton Game Dynamics^^^\
Sound and Music Program Library:^FMOD Sound System by Firelight Technologies^^^\
Copy Protection:^Themida by Oreans Technologies^^^\
Skybox Textures:^Jay Weston www.hyperfocaldesign.com^^^\
Third Party Art Libraries Used:^Texturemonk^Mayang Textures^cgtextures.com^3d.sk^^\
Unofficial Mount&Blade Editor:^Josh Dahlby^^^\
Many thanks to Marco Tarini for the Mountain shader idea!^^^\
Special Thanks to:^Ibrahim Dogan^Nova Language Works^Selim Kurtulus and UPS Turkey^^^\
Taleworlds.com Forum Administrators and Moderators:^Janus^Archonsod^Narcissus^Nairagorn^Lost Lamb^Deus Ex^Merentha^Volkier^Okin^Instag0\
^Deniz^ego^Guspav^Hallequin^Invictus^okiN^Raz^rejenorst^Skyrage^ThVaz^^^\
Spanish Translation^^Translators:^Anabel 'Rhaenys' Diaz^Analia 'Immortality' Dobarro^Anoik^^Medieval Consultant:^Enric 'Palafoxx' Clave^^Language Tester:^Theo de Moree^^^\
Mount&Blade Community Suggestions and Feedback:^\
13 Chain Bloody Spider^\
Aenarion^\
AgentSword^\
Ahadhran^\
Albino^\
Allegro^\
allthesedamnnamesare^\
Amman de Stazia^\
Ancientwanker^\
Anrea 'Skree' Giongiani^\
Aqtai^\
Art Falmingaid^\
bryce777^\
Bugman^\
Buxton^\
Calandale^\
Cartread^\
Chel^\
Chilly5^\
Cirdan^\
Cleaning agent^\
Cymro^\
DaBlade^\
DaLagga^\
Damien^\
danover^\
Dearahn^\
Deathblow^\
Destichado^\
Dryvus^\
dunnno^\
D'Sparil^\
ealabor^\
Ealdormann Hussey^\
EasyCo506^\
El Duke^\
Elias Maluco^\
Eogan^\
ex_ottoyuhr^\
Fisheye^\
Fossi^\
fujiwara^\
Fuzzpilz^\
GandalfTheGrey^\
Gerif^\
Grocat^\
Guspav^\
Halden The Borch shooter^\
Hallequin^\
Handel^\
Hardcode^\
Haupper^\
Hellequin^\
Highelf^\
Highlander^\
Ibrahim Turgut^\
Iesu^\
Ilex^\
Ingolifs^\
Invictus^\
Itchrelief^\
Jlgx50^\
JHermes^\
Jik^\
john259^\
JonathanStrange^\
jpgray^\
kamov23^\
Kayback^\
Khalid Ibn Walid^\
KON_Air^\
Lady Tanith^\
Larry Knight^\
LavaLampMaster^\
Leprechaun^\
Lhorkan^\
Llew2^\
Maelstorm^\
Manitas^\
Maw^\
MAXHARDMAN^\
Merentha^\
Merlkir^\
Michael Elijah 'ironpants' Bell-Rao^\
mihoshi^\
Mirathei^\
mkeller^\
Momaw^\
Morgoth2005^\
MrCrotch^\
mtarini^\
n00854180t^\
Naridill^\
Nicholas Altaman\
okiN^\
oksir^\
Oldtimer^\
Ollieh^\
oRGy^\
Oubliette^\
Patrick 'nox' Gallaty^\
Pavlov^\
Rando^\
Raz^\
rejenorst^\
Rjii^\
Ron Losey^\
Rorthic^\
RR_raptor^\
Scion^\
Seff^\
shenzay^\
Shadowmoses^\
shikamaru 1993^\
Silver^\
silverkatana^\
Sir Prince^\
Sirgigor^\
Skyrage^\
Smoson^\
sneakey pete^\
Stefano^\
Stella^\
Stonewall382^\
Talak^\
Tankai^\
TG^\
thelast^\
The Phoenix^\
The Pope^\
The Yogi^\
Thingy Master^\
Thormac^\
Thus_Spake_Nosferatu^\
ThVaz^\
Toygar Birinci^\
Tuckles^\
Tul^\
Ursca^\
Vaerraent^\
Vilhjalmr^\
Volkier^\
vuk^\
Wanderer^\
WhoCares^\
Winter^\
Worbah^\
Yoshiboy^\
...and many many other wonderful Mount&Blade players!^^\
(This is only a small sample of all the players who have contributed to the game by providing suggestions and feedback.^\
This list has been compiled by sampling only a few threads in the Taleworlds Forums.^\
Unfortunately compiling an exhaustive list is almost impossible.^\
We apologize sincerely if you contributed your suggestions and feedback but were not listed here, and please know that we are grateful to you all the same...)\
"),
  ("credits_10", "Paradox Interactive^^President and CEO:^Theodore Bergqvist^^Executive Vice President:^Fredrik Wester\
^^Chief Financial Officer:^Lena Eriksson^^Finance & Accounting:^Annlouise Larsson^^VP Sales & Marketing US:^Reena M. Miranda\
^^VP Sales & Marketing EU:^Martin Sirc^^Distribution Manager Nordic:^Erik Helmfridsson^^Director of PR & Marketing:^Susana Meza\
^^PR & Marketing:^Sofia Forsgren^^Product Manager:^Boel Bermann\
"),
  ("credits_11", "Logotype:^Jason Brown^^Cover Art:^Piotr Fox Wysocki\
^^Layout:^Christian Sabe^Melina Grundel^^Poster:^Piotr Fox Wysocki^^Map & Concept Art:^Ganbat Badamkhand\
^^Manual Editing:^Digital Wordsmithing: Ryan Newman, Nick Stewart^^Web:^Martin Ericsson^^Marketing Assets:^2Coats\
^^Localization:^S&H Entertainment Localization^^GamersGate:^Ulf Hedblom^Andreas Pousette^Martin Ericson^Christoffer Lindberg\
"),
  ("credits_12", "Thanks to all of our partners worldwide, in particular long-term partners:\
^Koch Media (Germany & UK)^Blue Label (Italy & France)^Friendware (Spain)^New Era Interactive Media Co. Ltd. (Asia)\
^Snowball (Russia)^Pinnacle (UK)^Porto Editora (Portugal)^Hell-Tech (Greece)^CD Projekt (Poland, Czech Republic, Slovakia & Hungary)\
^Paradox Scandinavian Distribution (Scandinavia)\
"),

### TLD strings
 ("faction_strength_crushed"           , "crushed"),
 ("faction_strength_spent_and_wavering", "spent and wavering"),
 ("faction_strength_weakened"          , "weakened"),
 ("faction_strength_in_good_state"     , "in a good state"),
 ("faction_strength_strong"            , "strong"),
 ("faction_strength_very strong"       , "very strong"),
 ("faction_strength_unmatched"         , "unmatched"),

# TLD theater names
 ("theater_SE", "Gondor"),
 ("theater_SW", "Rohan"),
 ("theater_C", "South Rhovanion"),
 ("theater_N", "North Rhovanion"), 
 
#################################
# TLD faction ranks
#
     ("tfr_name_strings_begin", "tfr_name_strings_begin"),
     ]+concatenate_scripts([
        concatenate_scripts([
                [(tld_faction_ranks[fac][rnk][2][pos][0].lower().replace(" ", "_"), tld_faction_ranks[fac][rnk][2][pos][0]) for pos in range(len(tld_faction_ranks[fac][rnk][2]))
            ] for rnk in range(len(tld_faction_ranks[fac]))
        ]) for fac in range(len(tld_faction_ranks))
     ])+[
    ("promote", "You have been working well for the realm. Now you can be:"),
#
# TLD faction ranks end
#################################

 ("subfaction_gondor_name_begin" , "Gondor"),
 
 ("subfaction_gondor_name1" , "Pelargir" ) ,
 ("subfaction_gondor_name2" , "Dol Amroth" ),
 ("subfaction_gondor_name3" , "Lamedon" ) ,
 ("subfaction_gondor_name4" , "Lossarnach" ),
 ("subfaction_gondor_name5" , "Pinnath Gelin" ),
 ("subfaction_gondor_name6" , "Ithilien" ), 
 ("subfaction_gondor_name7" , "Blackroot Vale" ) ,
 
#### TLD shop/bar rumors
("default_rumor", "The War. Everybody is talking about the war."),
# Rohan
("rohan_rumor_begin", "It breaks my heart to see my babies off to war!  But without them the men would have to walk."),
("rohan_rumor_2", "I hear the Orcs eat horses.  Savages!  Oh, yeah, they also eat prisoners.  That's bad, too, of course."),
("rohan_rumor_3", "There are no horses finer than Rohan's. Even the Elves get their horses from us!"),
("rohan_rumor_4", "If you're a healer of men please treat my horses with just as much care should they be wounded."),
("rohan_rumor_5", "Bring me 8 Sumpter Horses, - he says... after the 7 he asked for yesterday.  Makes you wonder."),
("rohan_rumor_6", "Gondor prefers sturdier horses. Our riders enjoy speed. The Elves buy only the best, which means from us of course -- so to get the very best Rohan horse you'll have to buy it from them."),
("rohan_rumor_7", "I've seen examples of the Desert Mare and Variag Kataphract.  Rohan horses are superior but require a more experienced rider to handle."),
("rohan_rumor_8", "Wargs are slow but very maneuverable.  They're also quite fragile compared to a well-bred warhorse."),
("rohan_rumor_9", "No army fights Rohan without pikes and spears to set against our horsemen.  Saruman will cut down the whole Fangorn forest equipping his armies before this war is done."),
("rohan_rumor_10", "Being the best horsemen in the realm starts with raising the best horses."),
("rohan_rumor_11", "Most of the horses for sale in Gondor came from us. They prefer a slightly stronger, slower horse that can carry a little more armor."),
("rohan_rumor_12", "orses are the backbone of our economy, you know. Everybody gets their horses from us!"),
("rohan_rumor_13", "Orcs are tough but don't wear much protection. They're no match for a good axe."),
("rohan_rumor_14", "Our throwing axes and spears are bulky, but how many chances do your cavalry have to throw a missile before they ride down the foe? Make your one shot count by throwing something with some heft."),
("rohan_rumor_15", "Hitting an orc with an arrow loosed from the back of a horse looks difficult because it is, but the price of charging a rank of long pikes is higher."),
("rohan_rumor_16", "Gondor practices archery. We practice horse archery. Dunlendings practice neither."),
("rohan_rumor_17", "Many of Saruman's orcs are deadly archers. Many are not. A wise cavalry commander shouldn't wait to discover which is which."),

("gondor_rumor_begin", "If everyone traded horses for wargs tomorrow Rohan's children would be thrown into poverty the day after. But then who'd want to ride a warg?"),
("gondor_rumor_2", "Here in Gondor there is nothing under the sun we don't make, build, or grow in some quantity."),
("gondor_rumor_3", "We speculate that food is the orcs' most limiting resource. That would explain the cannibalism, wouldn't it?"),
("gondor_rumor_4", "Rohan has a reputation for its horses, but they also produce an abundance of basic foods at lower cost than Gondor. It may be bland, but it keeps their armies in the field and their people hard at work."),
("gondor_rumor_5", "The Shadow's near-limitless supplies are borne on the backs of an equally vast pool of slave labor."),
("gondor_rumor_6", "Elves build a few things extremely well and charge outrageously for them. Fortunately their demand for human spices is insatiable. Lembas must've tasted terrible before we came along."),
("gondor_rumor_7", "Orcs are literally born into slavery. We don't know exactly how long it takes to birth one -- if they even have mothers -- but we do know they're born ready to work. The economics of sustained conflict look very bleak."),
("gondor_rumor_8", "The Corsairs would've profited far more from trading with us than invading. What plunder could've matched the booty they'd have hauled away selling old Numenorian artifacts to every minor noble in Gondor?"),
("gondor_rumor_9", "Horses? Yes, I sell them. Yes, they're genuine Rohan. You military types think Gondor horses aren't fit for pulling carts, never mind that they were sired by beasts imported from Rohan.  *sigh*"),
("gondor_rumor_10", "Between Sauron and Saruman it is only Saruman who exhibits greed in the conventional sense. He'll deal with anyone and do anything if there's profit in it. What he does with his money is anyone's guess, but rumor has it his agents are well-paid. Whether his lust for money is a sign of weakness or wisdom I cannot say."),
("gondor_rumor_11", "Dol Guldur ... a slave economy built mostly underground, that's all I know."),
("gondor_rumor_12", "Moria? Ahh, the treasures they used to bring out of there! They paid well, too, for food, supplies, wine and ale ... all that's gone, now."),
("other_rumor_begin", "Moria? Ahh, the treasures they used to bring out of there! They paid well, too, for food, supplies, wine and ale ... all that's gone, now."),

("tld_introduction","TLD Introduction - you should go to Edoras."),

("tld_erebor_dungeon","The smell of death surrounds me. I'd better be careful"),
("tld_spear_hit","Ouch!"),    

]
