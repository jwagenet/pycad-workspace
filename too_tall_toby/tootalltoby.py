from dataclasses import dataclass

from build123d import *


@dataclass
class Density:
    """Densities in g/mm^3"""
    ST = 7800 / 1e6   # carbon steel density
    AL = 2700 / 1e6   # aluminum alloy
    ABS = 1020 / 1e6  # ABS


class TooTallToby(BasePartObject):
    """Too Tall Toby wrapper class"""
    def __init__(self, part, ref_mass, density, show_mass=True):
        super().__init__(part=part)
        self.density = density
        self.ref_mass = ref_mass
        self.mass = self.volume * self.density

        if print:
            print(f"\npart mass = {self.mass:.02f}")
            print(f"ref mass = {self.ref_mass}")