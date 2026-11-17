"""Regenerate only the final-horde, reveal and persistence integration graphs."""
from generate_cinematic_graphs import controller
from generate_combat_feedback import base_enemy
from generate_progression_graphs import combat_zone,director,activate_task
from generate_beacon_sequence import beacon
from generate_delivery_save import manager
controller();base_enemy();combat_zone();director();beacon();activate_task();manager()
import generate_dialogue_hud
