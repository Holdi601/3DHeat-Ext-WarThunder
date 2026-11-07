"""
3DHeat War Thunder replay converter: .wrpl replays into the Parquet table and
match document the 3DHeat viewer reads. Standalone; the 3DHeat Watcher runs it
as a command (`heat3d-wt-replay`) when it is installed.

`heat3d-wt-level` reads the game's own levels into .glb levels for the viewer.
"""

__version__ = "0.2.0"
