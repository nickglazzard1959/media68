#!/bin/bash
#
# Given a lot of videos files with mysterious names in a single level
# (or two level) tree, create a tree of symbolic links which orgaanises them
# into categories and gives them meaningful names.
#
SOURCE=/massbackup/contents/videos
LISTS=/massbackup/contents/videolib
LINK="ln -s -f"
#
# Ensure lists root exists.
mkdir -p ${LISTS}
#
# Remove top level category trees.
rm -rf ${LISTS}/movies
rm -rf ${LISTS}/tv
rm -rf ${LISTS}/music
rm -rf ${LISTS}/other
#
# Create category directories.
mkdir -p ${LISTS}/movies
mkdir -p ${LISTS}/tv
mkdir -p ${LISTS}/music
mkdir -p ${LISTS}/other
mkdir -p ${LISTS}/movies/hammer
mkdir -p ${LISTS}/movies/horror
mkdir -p ${LISTS}/movies/scifi
mkdir -p ${LISTS}/movies/b-movies
mkdir -p ${LISTS}/movies/hollywood
mkdir -p ${LISTS}/movies/independent
mkdir -p ${LISTS}/movies/british
mkdir -p ${LISTS}/movies/foreign-language
#
# Begin creating links.
${LINK} ${SOURCE}/2001_comp.mp4 ${LISTS}/movies/scifi/2001_A_Space_Odyssey.mp4
#
${LINK} ${SOURCE}/aap_experimental_tape_1989_comp.mp4 ${LISTS}/other/Array_Productions_1989.mp4
#
${LINK} ${SOURCE}/abominable_comp.mp4 ${LISTS}/movies/hammer/Abominable_Snowman.mp4
#
mkdir -p ${LISTS}/tv/Partners_In_Crime
${LINK} ${SOURCE}/ac-partners-d1_comp.mp4 ${LISTS}/tv/Partners_In_Crime/Disk1.mp4
${LINK} ${SOURCE}/ac-partners-d2_comp.mp4 ${LISTS}/tv/Partners_In_Crime/Disk2.mp4
${LINK} ${SOURCE}/ac-partners-d3_comp.mp4 ${LISTS}/tv/Partners_In_Crime/Disk3.mp4
#
${LINK} ${SOURCE}/american_werewolf_comp.mp4 ${LISTS}/movies/horror/American_Werewolf_In_London.mp4
#
${LINK} ${SOURCE}/APL_demonstration_1975-_DTpQ4Kk2wA.mp4  ${LISTS}/other/APL_Demo_Imperial_1975.mp4
#
mkdir -p ${LISTS}/tv/Ascent_Of_Man
${LINK} ${SOURCE}/ascent_of_man_d1_comp.mp4 ${LISTS}/tv/Ascent_Of_Man/Disk1.mp4
${LINK} ${SOURCE}/ascent_of_man_d2_comp.mp4 ${LISTS}/tv/Ascent_Of_Man/Disk2.mp4
${LINK} ${SOURCE}/ascent_of_man_d4_comp.mp4 ${LISTS}/tv/Ascent_Of_Man/Disk3.mp4
#
mkdir -p ${LISTS}/tv/Avengers_1963
${LINK} ${SOURCE}/avengers_1963_d1_comp.mp4 ${LISTS}/tv/Avengers_1963/Disk1.mp4
${LINK} ${SOURCE}/avengers_1963_d2_comp.mp4 ${LISTS}/tv/Avengers_1963/Disk2.mp4
${LINK} ${SOURCE}/avengers_1963_d3_partial_comp.mp4 ${LISTS}/tv/Avengers_1963/Disk3a.mp4
${LINK} ${SOURCE}/avengers_1963_d3_part2_comp.mp4 ${LISTS}/tv/Avengers_1963/Disk3b.mp4
${LINK} ${SOURCE}/avengers_1963_d4_comp.mp4 ${LISTS}/tv/Avengers_1963/Disk4.mp4
${LINK} ${SOURCE}/avengers_1963_d5_comp.mp4 ${LISTS}/tv/Avengers_1963/Disk5.mp4
${LINK} ${SOURCE}/avengers_1963_d6_comp.mp4 ${LISTS}/tv/Avengers_1963/Disk6.mp4
${LINK} ${SOURCE}/avengers_1963_d7_comp.mp4 ${LISTS}/tv/Avengers_1963/Disk7.mp4
${LINK} ${SOURCE}/avengers_1983_d8_comp.mp4 ${LISTS}/tv/Avengers_1963/Disk8.mp4
#
${LINK} ${SOURCE}/beat_girl_comp.mp4 ${LISTS}/movies/b-movies/Beat_Girl.mp4
#
${LINK} ${SOURCE}/beowulf_comp.mp4 ${LISTS}/movies/hollywood/Beowulf.mp4
#
${LINK} ${SOURCE}/bicyclettes_comp.mp4 ${LISTS}/movies/independent/Les_Bicyclettes_de_Belsize.mp4
#
${LINK} ${SOURCE}/blithe_spirit_comp.mp4 ${LISTS}/movies/british/Blithe_Spirit.mp4
#
mkdir -p ${LISTS}/tv/Black_Books
${LINK} ${SOURCE}/black_books_comp.mp4 ${LISTS}/tv/Black_Books/Disk1.mp4
#
${LINK} ${SOURCE}/bunny_lake_comp.mp4 ${LISTS}/movies/british/Bunny_Lake_Is_Missing.mp4
#
${LINK} ${SOURCE}/bunuel_chambermaid_comp.mp4  ${LISTS}/movies/foreign-language/Diary_Of_A_Chambermaid.mp4
${LINK} ${SOURCE}/bunuel_discreet_comp.mp4  ${LISTS}/movies/foreign-language/Discreet_Charm_Of_The_Bourgoisie.mp4
${LINK} ${SOURCE}/bunuel_obscure_comp.mp4  ${LISTS}/movies/foreign-language/That_Obscure_Object_Of_Desire.mp4
#
${LINK} ${SOURCE}/circus_comp.mp4 ${LISTS}/movies/hammer/Vampire_Circus.mp4
#
${LINK} ${SOURCE}/cocteau_belle_comp.mp4 ${LISTS}/movies/foreign-language/La_Belle_Et_La_Bete.mp4
${LINK} ${SOURCE}/cocteau_blood_comp.mp4 ${LISTS}/movies/foreign-language/Blood_Of_A_Poet.mp4
${LINK} ${SOURCE}/cocteau_orpheus_comp.mp4 ${LISTS}/movies/foreign-language/Orphee.mp4
${LINK} ${SOURCE}/cocteau_testament_comp.mp4 ${LISTS}/movies/foreign-language/Testament_Of_A_Poet.mp4
#
mkdir -p ${LISTS}/tv/The_Coroner
${LINK} ${SOURCE}/coroner-1_comp.mp4 ${LISTS}/tv/The_Coroner/Episode1.mp4
#
${LINK} ${SOURCE}/countess_comp.mp4 ${LISTS}/movies/hammer/Countess_Dracula.mp4
#
${LINK} ${SOURCE}/cross_roads_comp.mp4 ${LISTS}/movies/horror/Crossroads-Christopher-Lee.mp4
#
${LINK} ${SOURCE}/damned_comp.mp4  ${LISTS}/movies/hammer/The_Damned.mp4
#
mkdir -p ${LISTS}/tv/Danger_Man
${LINK} ${SOURCE}/danger-man-d1_comp.mp4  ${LISTS}/tv/Danger_Man/Disk1.mp4
${LINK} ${SOURCE}/danger-man-d2a_comp.mp4  ${LISTS}/tv/Danger_Man/Disk2a.mp4
${LINK} ${SOURCE}/danger-man-d2b_comp.mp4  ${LISTS}/tv/Danger_Man/Disk2b.mp4
${LINK} ${SOURCE}/danger-man-d3_comp.mp4  ${LISTS}/tv/Danger_Man/Disk3.mp4
${LINK} ${SOURCE}/danger-man-d4_comp.mp4  ${LISTS}/tv/Danger_Man/Disk4.mp4
#
${LINK} ${SOURCE}/daughters_of_darkness_comp.mp4 ${LISTS}/movies/horror/Daughters_Of_Darkness.mp4
#
${LINK} ${SOURCE}/day-earth-caught-fire_comp.mp4 ${LISTS}/movies/scifi/The_Day_The_Earth_Caught_Fire.mp4
#
${LINK} ${SOURCE}/deadly_run_betacam_comp.mp4  ${LISTS}/movies/foreign-language/Deadly_Run_Betamax.mp4
#
${LINK} ${SOURCE}/death_at_broadcasting_house_comp.mp4 ${LISTS}/movies/british/Death_At_Broadcasting_House.mp4
#
${LINK} ${SOURCE}/death_french_garden_comp.mp4 ${LISTS}/movies/foreign-language/Death_In_A_French_Garden.mp4
#
${LINK} ${SOURCE}/death_line_comp.mp4 ${LISTS}/movies/horror/Death_Line.mp4
#
${LINK} ${SOURCE}/desk_set_comp.mp4  ${LISTS}/movies/hollywood/Desk_Set.mp4
#
${LINK} ${SOURCE}/devil_comp.mp4 ${LISTS}/movies/hammer/The_Devil_Rides_Out.mp4
#
${LINK} ${SOURCE}/diabolique_comp.mp4  ${LISTS}/movies/foreign-language/Diabolique.mp4
#
${LINK} ${SOURCE}/dogma_comp.mp4 ${LISTS}/movies/hollywood/Dogma.mp4
#
${LINK} ${SOURCE}/dracula_comp.mp4 ${LISTS}/movies/hammer/Dracula.mp4
#
${LINK} ${SOURCE}/eal_showreel_1985_comp.mp4   ${LISTS}/other/Electronic_Arts_1985.mp4
#
mkdir -p ${LISTS}/movies/british/Edgar_Wallace
mkdir -p ${LISTS}/movies/british/Edgar_Wallace/Series_1
mkdir -p ${LISTS}/movies/british/Edgar_Wallace/Series_2
mkdir -p ${LISTS}/movies/british/Edgar_Wallace/Series_3
mkdir -p ${LISTS}/movies/british/Edgar_Wallace/Series_4
mkdir -p ${LISTS}/movies/british/Edgar_Wallace/Series_5
mkdir -p ${LISTS}/movies/british/Edgar_Wallace/Series_6
mkdir -p ${LISTS}/movies/british/Edgar_Wallace/Series_7
${LINK} ${SOURCE}/ew-s1-d1_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Series_1/Disk_1.mp4
${LINK} ${SOURCE}/ew-s1-d2_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Series_1/Disk_2.mp4
${LINK} ${SOURCE}/ew-s1-d3_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Series_1/Disk_3.mp4
${LINK} ${SOURCE}/ew-s2-d1_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Series_2/Disk_1.mp4
${LINK} ${SOURCE}/ew-s2-d2_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Series_2/Disk_2.mp4
${LINK} ${SOURCE}/ew-s2-d3_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Series_2/Disk_3.mp4
${LINK} ${SOURCE}/ew-s3-d1_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Series_3/Disk_1.mp4
${LINK} ${SOURCE}/ew-s3-d2_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Series_3/Disk_2.mp4
${LINK} ${SOURCE}/ew-s3-d3_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Series_3/Disk_3.mp4
${LINK} ${SOURCE}/ew-s4-d1_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Series_4/Disk_1.mp4
${LINK} ${SOURCE}/ew-s4-d2_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Series_4/Disk_2.mp4
${LINK} ${SOURCE}/ew-s4-d3_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Series_4/Disk_3.mp4
${LINK} ${SOURCE}/ew-s5-d1_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Series_5/Disk_1.mp4
${LINK} ${SOURCE}/ew-s5-d2_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Series_5/Disk_2.mp4
${LINK} ${SOURCE}/ew-s5-d3_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Series_5/Disk_3.mp4
${LINK} ${SOURCE}/ew-s6-d1_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Series_6/Disk_1.mp4
${LINK} ${SOURCE}/ew-s6-d2_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Series_6/Disk_2.mp4
${LINK} ${SOURCE}/ew-s7-d1_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Series_7/Disk_1.mp4
${LINK} ${SOURCE}/ew-s7-d2_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Series_7/Disk_2.mp4
#
${LINK} ${SOURCE}/fast_lady_comp.mp4  ${LISTS}/movies/british/The_Fast_Lady.mp4
#
${LINK} ${SOURCE}/forbidden-planet_comp.mp4  ${LISTS}/movies/scifi/Forbidden_Planet.mp4
#
${LINK} ${SOURCE}/frankenstein_comp.mp4  ${LISTS}/movies/hammer/Frankenstein.mp4
#
mkdir -p ${LISTS}/tv/Fringe
mkdir -p ${LISTS}/tv/Fringe/Series_1
${LINK} ${SOURCE}/fringe-s1d1.mp4 ${LISTS}/tv/Fringe/Series_1/Disk_1.mp4
#
mkdir -p ${LISTS}/tv/BBC_Christmas_Ghost_Stories
${LINK} ${SOURCE}/ghost-chris-1_comp.mp4 ${LISTS}/tv/BBC_Christmas_Ghost_Stories/Disk_1.mp4
${LINK} ${SOURCE}/ghost-chris-2_comp.mp4 ${LISTS}/tv/BBC_Christmas_Ghost_Stories/Disk_2.mp4
${LINK} ${SOURCE}/ghost-chris-3_comp.mp4 ${LISTS}/tv/BBC_Christmas_Ghost_Stories/Disk_3.mp4
${LINK} ${SOURCE}/ghost-chris-4_comp.mp4 ${LISTS}/tv/BBC_Christmas_Ghost_Stories/Disk_4.mp4
#
${LINK} ${SOURCE}/gorgon_comp.mp4 ${LISTS}/movies/hammer/The_Gorgon.mp4
#
${LINK} ${SOURCE}/grosse_point_blank_comp.mp4 ${LISTS}/movies/hollywood/Grosse_Point_Blank.mp4
#
${LINK} ${SOURCE}/hell_comp.mp4 ${LISTS}/movies/hammer/Frankenstein_and_the_Monster_from_Hell.mp4
#
${LINK} ${SOURCE}/hell_house_comp.mp4 ${LISTS}/movies/horror/Hell_House.mp4
#
mkdir -p ${LISTS}/tv/The_Human_Jungle
mkdir -p ${LISTS}/tv/The_Human_Jungle/Series_1
mkdir -p ${LISTS}/tv/The_Human_Jungle/Series_2
${LINK} ${SOURCE}/hj-s1-d1_comp.mp4   ${LISTS}/tv/The_Human_Jungle/Series_1/Disk_1.mp4
${LINK} ${SOURCE}/hj-s1-d2-a_comp.mp4   ${LISTS}/tv/The_Human_Jungle/Series_1/Disk_2a.mp4
${LINK} ${SOURCE}/hj-s1-d2-b_comp.mp4   ${LISTS}/tv/The_Human_Jungle/Series_1/Disk_2b.mp4
${LINK} ${SOURCE}/hj-s1-d3_comp.mp4   ${LISTS}/tv/The_Human_Jungle/Series_1/Disk_2.mp4
${LINK} ${SOURCE}/hj-s2-d4_comp.mp4   ${LISTS}/tv/The_Human_Jungle/Series_2/Disk_1.mp4
${LINK} ${SOURCE}/hj-s2-d5_comp.mp4   ${LISTS}/tv/The_Human_Jungle/Series_2/Disk_2.mp4
${LINK} ${SOURCE}/hj-s2-d6_comp.mp4   ${LISTS}/tv/The_Human_Jungle/Series_2/Disk_3.mp4
${LINK} ${SOURCE}/hj-s2-d7_comp.mp4   ${LISTS}/tv/The_Human_Jungle/Series_2/Disk_4.mp4
#
mkdir -p ${LISTS}/tv/Hammer_House_of_Horror
${LINK} ${SOURCE}/hoh-d1.mp4 ${LISTS}/tv/Hammer_House_of_Horror/Disk_1.mp4
${LINK} ${SOURCE}/hoh-d2_comp.mp4 ${LISTS}/tv/Hammer_House_of_Horror/Disk_2.mp4
${LINK} ${SOURCE}/hoh-d3_comp.mp4 ${LISTS}/tv/Hammer_House_of_Horror/Disk_3.mp4
#
${LINK} ${SOURCE}/horror_express_comp.mp4 ${LISTS}/movies/horror/Horror_Express.mp4
#
${LINK} ${SOURCE}/hot-fuzz_comp.mp4 ${LISTS}/movies/british/Hot_Fuzz.mp4
#
${LINK} ${SOURCE}/houndbaskervilles_comp.mp4 ${LISTS}/movies/hammer/Hound_of_the_Baskervilles.mp4
#
${LINK} ${SOURCE}/hp_goblet_of_fire_comp.mp4  ${LISTS}/movies/hollywood/Harry_Potter_and_the_Goblet_of_Fire.mp4
#
${LINK} ${SOURCE}/inferno_comp.mp4  ${LISTS}/movies/horror/Inferno.mp4
#
${LINK} ${SOURCE}/jubilee_comp.mp4 ${LISTS}/movies/british/Jubilee.mp4
#
${LINK} ${SOURCE}/KODACHROME_TWO-COLOR_TEST_SHOTS_NO._III-NOFH-gl1cpQ.mkv ${LISTS}/other/Kodachrome_2_colour_historic_tests.mkv
#
${LINK} ${SOURCE}/logans_run_comp.mp4  ${LISTS}/movies/hollywood/Logans_Run.mp4
#
${LINK} ${SOURCE}/london_nobody_knows_comp.mp4 ${LISTS}/other/The_London_Nobody_Knows.mp4
#
${LINK} ${SOURCE}/lovers_comp.mp4 ${LISTS}/movies/hammer/The_Vampire_Lovers.mp4
#
${LINK} ${SOURCE}/lucy_comp.mp4 ${LISTS}/movies/hollywood/Lucy.mp4
#
mkdir -p ${LISTS}/tv/Maigret
mkdir -p ${LISTS}/tv/Maigret/Cremer
${LINK} ${SOURCE}/maigret-cremer-d1_comp.mp4 ${LISTS}/tv/Maigret/Cremer/Disk1.mp4
${LINK} ${SOURCE}/maigret-cremer-d2_comp.mp4 ${LISTS}/tv/Maigret/Cremer/Disk2.mp4
${LINK} ${SOURCE}/maigret-cremer-d3_comp.mp4 ${LISTS}/tv/Maigret/Cremer/Disk3.mp4
#
mkdir -p ${LISTS}/tv/Maigret/Gambon
${LINK} ${SOURCE}/maigret-gambon-d1_comp.mp4 ${LISTS}/tv/Maigret/Gambon/Disk1.mp4
${LINK} ${SOURCE}/maigret-gambon-d2_comp.mp4 ${LISTS}/tv/Maigret/Gambon/Disk2.mp4
${LINK} ${SOURCE}/maigret-gambon-d3_comp.mp4 ${LISTS}/tv/Maigret/Gambon/Disk3.mp4
${LINK} ${SOURCE}/maigret-gambon-d4_comp.mp4 ${LISTS}/tv/Maigret/Gambon/Disk4.mp4
#
${LINK} ${SOURCE}/malpertuis_betacam_comp.mp4 ${LISTS}/movies/horror/Malpertuis_Betacam.mp4
${LINK} ${SOURCE}/malpertuis_comp.mp4 ${LISTS}/movies/horror/Malpertuis.mp4
#
${LINK} ${SOURCE}/marat_sade_comp.mp4 ${LISTS}/movies/british/Marat-Sade.mp4
#
${LINK} ${SOURCE}/marienbad_comp.mp4  ${LISTS}/movies/foreign-language/Last_Year_at_Marienbad.mp4
#
${LINK} ${SOURCE}/masque_red_death_comp.mp4 ${LISTS}/movies/horror/Masque_of_the_Red_Death.mp4
#
mkdir -p ${LISTS}/movies/scifi/The_Matrix
${LINK} ${SOURCE}/matrix_part_1_comp.mp4 ${LISTS}/movies/scifi/The_Matrix/Part_1.mp4
${LINK} ${SOURCE}/matrix_part_2_comp.mp4 ${LISTS}/movies/scifi/The_Matrix/Part_2.mp4
${LINK} ${SOURCE}/matrix_part_3_comp.mp4 ${LISTS}/movies/scifi/The_Matrix/Part_3.mp4
#
${LINK} ${SOURCE}/medusa_touch_comp.mp4 ${LISTS}/movies/horror/The_Medusa_Touch.mp4
#
${LINK} ${SOURCE}/metropolis_comp.mp4 ${LISTS}/movies/scifi/Metropolis.mp4
#
${LINK} ${SOURCE}/mummy_comp.mp4 ${LISTS}/movies/hammer/The_Mummy.mp4
#
${LINK} ${SOURCE}/munchhausen_1943_comp.mp4  ${LISTS}/movies/foreign-language/Munchhausen_1943.mp4
#
${LINK} ${SOURCE}/night_eagle_comp.mp4 ${LISTS}/movies/horror/Night_Eagle.mp4
#
${LINK} ${SOURCE}/orson_welles_1985_part_1_comp.mp4 ${LISTS}/other/Orson_Welles_Interview_1_1985.mp4
${LINK} ${SOURCE}/orson_welles_1985_part_2_comp.mp4 ${LISTS}/other/Orson_Welles_Interview_2_1985.mp4
#
${LINK} ${SOURCE}/pans_labyrinth_comp.mp4 ${LISTS}/movies/horror/Pans_Labyrinth.mp4
#
${LINK} ${SOURCE}/peeping-tom_comp.mp4 ${LISTS}/movies/british/Peeping_Tom.mp4
#
${LINK} ${SOURCE}/picnic_at_hanging_rock_comp.mp4 ${LISTS}/movies/foreign-language/Picnic_at_Hanging_Rock.mp4
#
${LINK} ${SOURCE}/pit_comp.mp4 ${LISTS}/movies/hammer/Quatermass_and_the_Pit.mp4
#
mkdir -p ${LISTS}/music/P_J_Harvey
${LINK} ${SOURCE}/pjh_let_england_shake_comp.mp4 ${LISTS}/music/P_J_Harvey/Let_England_Shake.mp4
${LINK} ${SOURCE}/pjh_st_lukes_comp.mp4 ${LISTS}/music/P_J_Harvey/Live_at_St_Lukes.mp4
#
${LINK} ${SOURCE}/plague_comp.mp4 ${LISTS}/movies/hammer/Plague_of_the_Zombies.mp4
#
mkdir -p ${LISTS}/tv/Person_of_Interest
mkdir -p ${LISTS}/tv/Person_of_Interest/Series_1
${LINK} ${SOURCE}/poi-s1d2_comp.mp4 ${LISTS}/tv/Person_of_Interest/Series_1/Disk_2.mp4
${LINK} ${SOURCE}/poi-s1d3_comp.mp4 ${LISTS}/tv/Person_of_Interest/Series_1/Disk_3.mp4
${LINK} ${SOURCE}/poi-s1d4_comp.mp4 ${LISTS}/tv/Person_of_Interest/Series_1/Disk_4.mp4
${LINK} ${SOURCE}/poi-s1d5_comp.mp4 ${LISTS}/tv/Person_of_Interest/Series_1/Disk_5.mp4
${LINK} ${SOURCE}/poi-s1d6_comp.mp4 ${LISTS}/tv/Person_of_Interest/Series_1/Disk_6.mp4
#
mkdir -p ${LISTS}/tv/Person_of_Interest/Series_2
${LINK} ${SOURCE}/poi-s2d1_comp.mp4 ${LISTS}/tv/Person_of_Interest/Series_2/Disk_1.mp4
${LINK} ${SOURCE}/poi-s2d2_comp.mp4 ${LISTS}/tv/Person_of_Interest/Series_2/Disk_2.mp4
${LINK} ${SOURCE}/poi-s2d3_comp.mp4 ${LISTS}/tv/Person_of_Interest/Series_2/Disk_3.mp4
${LINK} ${SOURCE}/poi-s2d4_comp.mp4 ${LISTS}/tv/Person_of_Interest/Series_2/Disk_4.mp4
${LINK} ${SOURCE}/poi-s2d5a_comp.mp4 ${LISTS}/tv/Person_of_Interest/Series_2/Disk_5a.mp4
${LINK} ${SOURCE}/poi-s2d5b_comp.mp4 ${LISTS}/tv/Person_of_Interest/Series_2/Disk_5b.mp4
${LINK} ${SOURCE}/poi-s2d6_comp.mp4 ${LISTS}/tv/Person_of_Interest/Series_2/Disk_6.mp4
#
mkdir -p ${LISTS}/tv/Person_of_Interest/Series_3
${LINK} ${SOURCE}/poi-s3d1_comp.mp4 ${LISTS}/tv/Person_of_Interest/Series_3/Disk_1.mp4
${LINK} ${SOURCE}/poi-s3d2_comp.mp4 ${LISTS}/tv/Person_of_Interest/Series_3/Disk_2.mp4
${LINK} ${SOURCE}/poi-s3d3_comp.mp4 ${LISTS}/tv/Person_of_Interest/Series_3/Disk_3.mp4
${LINK} ${SOURCE}/poi-s3d4_comp.mp4 ${LISTS}/tv/Person_of_Interest/Series_3/Disk_4.mp4
${LINK} ${SOURCE}/poi-s3d5_comp.mp4 ${LISTS}/tv/Person_of_Interest/Series_3/Disk_5.mp4
${LINK} ${SOURCE}/poi-s3d6a_comp.mp4 ${LISTS}/tv/Person_of_Interest/Series_3/Disk_6a.mp4
${LINK} ${SOURCE}/poi-s3d6b_comp.mp4 ${LISTS}/tv/Person_of_Interest/Series_3/Disk_6b.mp4
#
mkdir -p ${LISTS}/tv/Person_of_Interest/Series_4
${LINK} ${SOURCE}/poi-s4d1_comp.mp4 ${LISTS}/tv/Person_of_Interest/Series_4/Disk_1.mp4
${LINK} ${SOURCE}/pois4d2a.mp4 ${LISTS}/tv/Person_of_Interest/Series_4/Disk_2a.mp4
${LINK} ${SOURCE}/pois4d2b.mp4 ${LISTS}/tv/Person_of_Interest/Series_4/Disk_2b.mp4
${LINK} ${SOURCE}/pois4d3.mp4 ${LISTS}/tv/Person_of_Interest/Series_4/Disk_3.mp4
${LINK} ${SOURCE}/pois4d4.mp4 ${LISTS}/tv/Person_of_Interest/Series_4/Disk_4.mp4
${LINK} ${SOURCE}/pois4d5.mp4 ${LISTS}/tv/Person_of_Interest/Series_4/Disk_5.mp4
${LINK} ${SOURCE}/pois4d6.mp4 ${LISTS}/tv/Person_of_Interest/Series_4/Disk_6.mp4
#
mkdir -p ${LISTS}/tv/Person_of_Interest/Series_5
${LINK} ${SOURCE}/pois5d1.mp4 ${LISTS}/tv/Person_of_Interest/Series_5/Disk_1.mp4
${LINK} ${SOURCE}/pois5d2.mp4 ${LISTS}/tv/Person_of_Interest/Series_5/Disk_2.mp4
${LINK} ${SOURCE}/pois5d3.mp4 ${LISTS}/tv/Person_of_Interest/Series_5/Disk_3.mp4
#
${LINK} ${SOURCE}/prince_comp.mp4 ${LISTS}/movies/hammer/Prince_of_Darkness.mp4
#
mkdir -p ${LISTS}/tv/The_Prisoner
${LINK} ${SOURCE}/prisoner-d1_comp.mp4 ${LISTS}/tv/The_Prisoner/Disk_1.mp4
${LINK} ${SOURCE}/prisoner-d2_comp.mp4 ${LISTS}/tv/The_Prisoner/Disk_2.mp4
${LINK} ${SOURCE}/prisoner-d3_comp.mp4 ${LISTS}/tv/The_Prisoner/Disk_3.mp4
${LINK} ${SOURCE}/prisoner-d4_comp.mp4 ${LISTS}/tv/The_Prisoner/Disk_4.mp4
${LINK} ${SOURCE}/prisoner-d5_comp.mp4 ${LISTS}/tv/The_Prisoner/Disk_5.mp4
#
${LINK} ${SOURCE}/quatermass.mp4 ${LISTS}/movies/hammer/The_Quatermass_Experiment.mp4
${LINK} ${SOURCE}/quatermass2.mp4 ${LISTS}/movies/hammer/Quatermass_2.mp4
#
${LINK} ${SOURCE}/red_shoes_comp.mp4 ${LISTS}/movies/british/The_Red_Shoes.mp4
#
${LINK} ${SOURCE}/reptile_comp.mp4 ${LISTS}/movies/hammer/The_Reptile.mp4
#
${LINK} ${SOURCE}/revenge_comp.mp4 ${LISTS}/movies/hammer/The_Revenge_of_Frankenstein.mp4
#
${LINK} ${SOURCE}/russian_ark_comp.mp4  ${LISTS}/movies/foreign-language/Russian_Ark.mp4
#
mkdir -p ${LISTS}/music/Siouxsie_and_the_Banshees
${LINK} ${SOURCE}/satb_7_year_itch_comp.mp4 ${LISTS}/music/Siouxsie_and_the_Banshees/Seven_Year_Itch.mp4
${LINK} ${SOURCE}/satb_finale_comp.mp4 ${LISTS}/music/Siouxsie_and_the_Banshees/Finale.mp4
${LINK} ${SOURCE}/satb_nocturne_comp.mp4 ${LISTS}/music/Siouxsie_and_the_Banshees/Nocturne.mp4
#
${LINK} ${SOURCE}/shaun-dead_comp.mp4 ${LISTS}/movies/british/Shaun_of_the_Dead.mp4
#
${LINK} ${SOURCE}/shoestring_dept_s_comp.mp4 ${LISTS}/other/Shoestring_and_Department_S_fragments.mp4
#
${LINK} ${SOURCE}/small_world_of_sammy_lee_comp.mp4 ${LISTS}/movies/british/The_Small_World_of_Sammy_Lee.mp4
#
${LINK} ${SOURCE}/solaris_comp.mp4  ${LISTS}/movies/foreign-language/Solaris.mp4
#
mkdir -p ${LISTS}/tv/Spaced
${LINK} ${SOURCE}/spaced_series_1_comp.mp4 ${LISTS}/tv/Spaced/Series_1.mp4
${LINK} ${SOURCE}/spaced_series_2_comp.mp4 ${LISTS}/tv/Spaced/Series_2.mp4
#
${LINK} ${SOURCE}/stalker_part1_comp.mp4  ${LISTS}/movies/foreign-language/Stalker_Part1.mp4
${LINK} ${SOURCE}/stalker_part2_comp.mp4  ${LISTS}/movies/foreign-language/Stalker_Part2.mp4
#
mkdir -p ${LISTS}/tv/One_Offs
${LINK} ${SOURCE}/stonetape_comp.mp4 ${LISTS}/tv/One_Offs/The_Stone_Tape.mp4
#
${LINK} ${SOURCE}/suspiria_comp.mp4 ${LISTS}/movies/horror/Suspiria.mp4
#
${LINK} ${SOURCE}/the_anniversary_comp.mp4 ${LISTS}/movies/british/The_Anniversary.mp4
#
${LINK} ${SOURCE}/theatre-blood_comp.mp4 ${LISTS}/movies/horror/Theatre_of_Blood.mp4
#
${LINK} ${SOURCE}/the_blood_beast_terror_comp.mp4 ${LISTS}/movies/horror/The_Blood_Beast_Terror.mp4
#
${LINK} ${SOURCE}/the_final_programme_comp.mp4 ${LISTS}/movies/british/The_Final_Programme.mp4
#
${LINK} ${SOURCE}/the_raven_comp.mp4 ${LISTS}/movies/horror/The_Raven.mp4
#
${LINK} ${SOURCE}/the_thing_1982_comp.mp4 ${LISTS}/movies/scifi/The_Thing_1982.mp4
${LINK} ${SOURCE}/the_thing_2011_comp.mp4 ${LISTS}/movies/scifi/The_Thing_2011.mp4
#
${LINK} ${SOURCE}/this_island_earth_comp.mp4 ${LISTS}/movies/scifi/This_Island_Earth.mp4
#
${LINK} ${SOURCE}/tomb_comp.mp4 ${LISTS}/movies/hammer/Blood_from_the_Mummys_Tomb.mp4
#
${LINK} ${SOURCE}/twins_comp.mp4 ${LISTS}/movies/hammer/Twins_of_Evil.mp4
#
mkdir -p ${LISTS}/tv/Two_Pints_of_Lager
${LINK} ${SOURCE}/two_pints_series_1_comp.mp4 ${LISTS}/tv/Two_Pints_of_Lager/Series_1.mp4
${LINK} ${SOURCE}/two_pints_series_2_comp.mp4 ${LISTS}/tv/Two_Pints_of_Lager/Series_2.mp4
#
${LINK} ${SOURCE}/wererabbit_comp.mp4 ${LISTS}/movies/british/Curse_of_the_Were-Rabbit.mp4
#
${LINK} ${SOURCE}/whistle_and_ill_come_comp.mp4 ${LISTS}/tv/One_Offs/Whistle_and_I_ll_Come_to_You.mp4
#
mkdir -p ${LISTS}/tv/Whitechapel
mkdir -p ${LISTS}/tv/Whitechapel/Series_1
${LINK} ${SOURCE}/whitechapel_series_1_comp.mp4 ${LISTS}/tv/Whitechapel/Series_1/Series_1.mp4
mkdir -p ${LISTS}/tv/Whitechapel/Series_2
${LINK} ${SOURCE}/whitechapel_series_2_comp.mp4 ${LISTS}/tv/Whitechapel/Series_2/Series_2.mp4
mkdir -p ${LISTS}/tv/Whitechapel/Series_3
${LINK} ${SOURCE}/whitechapel_series_3_disk_1_comp.mp4 ${LISTS}/tv/Whitechapel/Series_3/Disk_1.mp4
${LINK} ${SOURCE}/whitechapel_series_3_disk_2_comp.mp4 ${LISTS}/tv/Whitechapel/Series_3/Disk_2.mp4
mkdir -p ${LISTS}/tv/Whitechapel/Series_4
${LINK} ${SOURCE}/whitechapel_season4_part1_comp.mp4 ${LISTS}/tv/Whitechapel/Series_4/Disk_1.mp4
${LINK} ${SOURCE}/whitechapel_season4_part2_comp.mp4 ${LISTS}/tv/Whitechapel/Series_4/Disk_2.mp4
#
${LINK} ${SOURCE}/wicker_man_comp.mp4 ${LISTS}/movies/horror/The_Wicker_Man.mp4
#
${LINK} ${SOURCE}/x_files_comp.mp4 ${LISTS}/movies/scifi/X_Files.mp4
#
${LINK} ${SOURCE}/xtheunknown_comp.mp4 ${LISTS}/movies/hammer/X_the_Unknown.mp4
#
${LINK} ${SOURCE}/zero_de_conduit_various_cribb_comp.mp4 ${LISTS}/other/Zero_de_Conduit_and_Sgt_Cribb_fragments.mp4
#
# ============
#
SOURCE=/massbackup/contents/videos/from_uk_pvr
#
${LINK} ${SOURCE}/A_Message_From_Mars_comp.mp4 ${LISTS}/movies/scifi/A_Message_From_Mars_1913.mp4
#
${LINK} ${SOURCE}/Calling_Paul_Temple_comp.mp4 ${LISTS}/movies/b-movies/Calling_Paul_Temple.mp4
#
${LINK} ${SOURCE}/Clash_By_Night_comp.mp4 ${LISTS}/movies/b-movies/Clash_By_Night.mp4
#
${LINK} ${SOURCE}/Colonel_March_Investigates_comp.mp4  ${LISTS}/movies/british/Colonel_March_Investigates.mp4
#
${LINK} ${SOURCE}/Cone_of_Silence_comp.mp4 ${LISTS}/movies/british/Cone_of_Silence.mp4
#
${LINK} ${SOURCE}/Cosh_Boy_comp.mp4 ${LISTS}/movies/b-movies/Cosh_Boy.mp4
#
${LINK} ${SOURCE}/Dangerous_Cargo_comp.mp4 ${LISTS}/movies/b-movies/Dangerous_Cargo.mp4
#
${LINK} ${SOURCE}/Early_One_Morning_comp.mp4${LISTS}/other/Early_One_Morning.mp4
#
${LINK} ${SOURCE}/Empire_Flying_Boats_1936_comp.mp4 ${LISTS}/other/Empire_Flying_Boats_1936.mp4
#
mkdir -p ${LISTS}/movies/british/Edgar_Wallace/Other
${LINK} ${SOURCE}/EW_Accidental_Death_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Other/Accidental_Death.mp4
${LINK} ${SOURCE}/EW_Downfall_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Other/Downfall.mp4
${LINK} ${SOURCE}/EW_Fourth_Square_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Other/Fourth_Square.mp4
${LINK} ${SOURCE}/EW_The_Partner_comp.mp4 ${LISTS}/movies/british/Edgar_Wallace/Other/The_Partner.mp4
#
${LINK} ${SOURCE}/Flannelfoot_comp.mp4 ${LISTS}/movies/b-movies/Flannelfoot.mp4
#
${LINK} ${SOURCE}/Gelignite_Gang_comp.mp4 ${LISTS}/movies/b-movies/Gelignite_Gang.mp4
#
${LINK} ${SOURCE}/Good_Morning_Boys_comp.mp4 ${LISTS}/movies/british/Good_Morning_Boys.mp4
#
${LINK} ${SOURCE}/Haunted_Palace_comp.mp4 ${LISTS}/other/Haunted_Palace.mp4
#
${LINK} ${SOURCE}/Hell_Is_A_City_comp.mp4 ${LISTS}/movies/hammer/Hell_Is_A_City.mp4
#
${LINK} ${SOURCE}/Jigsaw_comp.mp4 ${LISTS}/movies/british/Jigsaw.mp4
#
${LINK} ${SOURCE}/Kill_Me_Tomorrow_comp.mp4 ${LISTS}/movies/b-movies/Kill_Me_Tomorrow.mp4
#
${LINK} ${SOURCE}/Make_Mine_Mink_comp.mp4 ${LISTS}/movies/british/Make_Mine_Mink.mp4
#
${LINK} ${SOURCE}/marilyn_comp.mp4 ${LISTS}/movies/b-movies/Marilyn.mp4
#
${LINK} ${SOURCE}/Night_Mail_comp.mp4 ${LISTS}/other/Night_Mail.mp4
#
${LINK} ${SOURCE}/Noose_1948_comp.mp4 ${LISTS}/movies/b-movies/Noose_1948.mp4
#
${LINK} ${SOURCE}/Operation_Diplomat_comp.mp4 ${LISTS}/movies/b-movies/Operation_Diplomat.mp4
#
${LINK} ${SOURCE}/Orpheum_comp.mp4 ${LISTS}/other/Orpheum.mp4
#
${LINK} ${SOURCE}/Park_Plaza_605_comp.mp4 ${LISTS}/movies/b-movies/Park_Plaza_605.mp4
#
${LINK} ${SOURCE}/Pit_of_Darkness_comp.mp4 ${LISTS}/movies/b-movies/Pit_of_Darkness.mp4
#
${LINK} ${SOURCE}/Rogues_Yarn_comp.mp4 ${LISTS}/movies/b-movies/Rogues_Yarn.mp4
#
${LINK} ${SOURCE}/Sally_Visits_Kew_1949_comp.mp4 ${LISTS}/other/Sally_Visits_Kew_1949.mp4
#
${LINK} ${SOURCE}/Sapphire_comp.mp4 ${LISTS}/movies/british/Sapphire.mp4
#
${LINK} ${SOURCE}/Seance_On_A_Wet_Afternoon_comp.mp4 ${LISTS}/movies/british/Seance_On_A_Wet_Afternoon.mp4
#
${LINK} ${SOURCE}/Seven_Days_To_Noon_comp.mp4 ${LISTS}/movies/british/Seven_Days_To_Noon.mp4
#
${LINK} ${SOURCE}/Shakedown_1959_comp.mp4 ${LISTS}/movies/b-movies/Shakedown_1959.mp4
#
${LINK} ${SOURCE}/Smokescreen_comp.mp4 ${LISTS}/movies/b-movies/Smokescreen.mp4
#
${LINK} ${SOURCE}/Stock_Car_comp.mp4 ${LISTS}/movies/b-movies/Stock_Car.mp4
#
${LINK} ${SOURCE}/The_Broken_Horseshoe_comp.mp4 ${LISTS}/movies/b-movies/The_Broken_Horseshoe.mp4
#
${LINK} ${SOURCE}/The_Case_Of_Charles_Peace_comp.mp4  ${LISTS}/movies/british/The_Case_Of_Charles_Peace.mp4
#
${LINK} ${SOURCE}/The_Challenge_comp.mp4 ${LISTS}/movies/b-movies/The_Challenge.mp4
#
${LINK} ${SOURCE}/The_Dark_Man_comp.mp4 ${LISTS}/movies/b-movies/The_Dark_Man.mp4
#
${LINK} ${SOURCE}/The_Delavine_Affair_comp.mp4 ${LISTS}/movies/b-movies/The_Delavine_Affair.mp4
#
${LINK} ${SOURCE}/The_Frightened_City_comp.mp4 ${LISTS}/movies/british/The_Frightened_City.mp4
#
${LINK} ${SOURCE}/The_Girl_In_The_Picture_comp.mp4 ${LISTS}/movies/b-movies/The_Girl_In_The_Picture.mp4
#
${LINK} ${SOURCE}/The_Good_Die_Young_comp.mp4 ${LISTS}/movies/b-movies/The_Good_Die_Young.mp4
#
${LINK} ${SOURCE}/The_House_On_Marsh_Road_comp.mp4 ${LISTS}/movies/b-movies/The_House_On_Marsh_Road.mp4
#
${LINK} ${SOURCE}/The_Innocents_comp.mp4  ${LISTS}/movies/british/The_Innocents.mp4
#
${LINK} ${SOURCE}/The_Partys_Over_comp.mp4 ${LISTS}/movies/british/The_Partys_Over.mp4
#
${LINK} ${SOURCE}/Third_Alibi_comp.mp4 ${LISTS}/movies/b-movies/Third_Alibi.mp4
#
${LINK} ${SOURCE}/Tread_Softly_Stranger_comp.mp4 ${LISTS}/movies/british/Tread_Softly_Stranger.mp4
#
${LINK} ${SOURCE}/Witness_In_The_Dark_comp.mp4 ${LISTS}/movies/b-movies/Witness_In_The_Dark.mp4
#
${LINK} ${SOURCE}/Woman_Eater_comp.mp4 ${LISTS}/movies/b-movies/Woman_Eater.mp4
#
${LINK} ${SOURCE}/Yield_To_The_Night_comp.mp4  ${LISTS}/movies/british/Yield_To_The_Night.mp4

