"""Local entry point: regenerate the four cinematic integration graphs only."""
from generate_cinematic_graphs import controller
from generate_progression_graphs import director,hostage
controller();hostage();director()
import generate_dialogue_hud
