"""Regenera únicamente los assets modificados en esta revisión."""
from generate_delivery_controls import interface,player_camera
from generate_cinematic_graphs import controller
from generate_delivery_save import manager
from generate_progression_graphs import director
from generate_rubric_systems import systems
interface();player_camera();controller();manager();systems();director()
import generate_dialogue_hud
