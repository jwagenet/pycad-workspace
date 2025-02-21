from dataclasses import dataclass

from build123d import Solid, BasePartObject


@dataclass
class Density:
    """Densities in g/mm^3"""
    ST = 7800 / 1e6   # carbon steel density
    AL = 2700 / 1e6   # aluminum alloy
    ABS = 1020 / 1e6  # ABS


class TooTallToby(BasePartObject):
    """Too Tall Toby wrapper class"""
    def __init__(self, part: Solid, id: str, name: str, ref_mass: float, density: float, tolerance: float = 1):
        super().__init__(part=part)
        self.id = id
        self.name = name
        self.density = density
        self.ref_mass = ref_mass
        self.mass = self.volume * self.density
        self.tolerance = tolerance

    def show_properties(self):
        mass_diff = abs(self.ref_mass - self.mass)
        print(f"\npart mass = {self.mass:.02f}")
        print(f"ref mass = {self.ref_mass}")
        print(f"in tolerance: {self.tolerance > mass_diff}, in sig fig {.01 > mass_diff}")