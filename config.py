import pathlib

parent_dir = pathlib.Path(__file__).parent


class Config:
    LARGEST_POKEDEX_NUMBER = 1025
    SPRITE_CACHE_DIR = parent_dir / "sprite_cache"
