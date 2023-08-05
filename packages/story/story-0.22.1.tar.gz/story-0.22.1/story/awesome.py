# -*- coding: utf-8 -*-
from random import choice, randint


left = (
    'cellular',
    'comsmic',
    'constant',
    'crystal',
    'electronic',
    'expansive',
    'light',
    'liquid',
    'lunar',
    'lunar',
    'magnetic',
    'mercious',
    'nebulous',
    'neon',
    'orbital',
    'phasic',
    'quantum',
    'solar',
    'solid',
    'spaceous',
    'super',
    'superfluid',
    'universal',
)

right = (
    'aluminium',
    'andromeda',
    'antimatter',
    'apollo',
    'argon',
    'arsenic',
    'asteroid',
    'atom',
    'belt',
    'beryllium',
    'bismuth',
    'blackhole',
    'boron',
    'boson',
    'bromine',
    'cadmium',
    'calcium',
    'carbon',
    'charge',
    'chlorine',
    'chromium',
    'cobalt',
    'collider',
    'comet',
    'copper',
    'cosmos',
    'curiosity',
    'deimos',
    'europa',
    'fermion',
    'fluorine',
    'force',
    'galaxy',
    'gallium',
    'gaseous',
    'germanium',
    'gold',
    'hadron',
    'helium',
    'higgs',
    'hydrogen',
    'indium',
    'iodine',
    'ion',
    'iridium',
    'iron',
    'jupiter',
    'kepler',
    'krypton',
    'lead',
    'lepton',
    'lithium',
    'magnesium',
    'mars',
    'mercury',
    'meteor',
    'molecule',
    'molecule',
    'molybdenum',
    'moon',
    'neptune',
    'neutrino',
    'neutron',
    'nickel',
    'niobium',
    'nitrogen',
    'opportunity',
    'oxygen',
    'palladium',
    'phobos',
    'phosphorus',
    'photon',
    'plasma',
    'platinum',
    'polymer',
    'potassium',
    'quark',
    'rhodium',
    'rocket',
    'rover',
    'rubidium',
    'ruthenium',
    'satellite',
    'scandium',
    'selenium',
    'silicon',
    'silver',
    'sirius',
    'sodium',
    'sol',
    'sputnik',
    'star',
    'strontium',
    'sulfur',
    'supernova',
    'technetium',
    'tin',
    'titanium',
    'uranium',
    'uranus',
    'vector',
    'venus',
    'voyager',
    'wormhole',
    'yttrium',
    'zinc',
    'zirconium',
)


def new():
    return f'{choice(left)}-{choice(right)}-{randint(0, 9999):04}'
