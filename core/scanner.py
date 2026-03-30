import os
import lib.hashlib as hashlib


from lib.pathlib import Path
from lib.pathspec import PathSpec



class Scanner:
    def __init__(self, base_path, ignore_file=".syncignore", include_file=".syncinclude"):
        self.base_path = Path(base_path)
        self.ignore_file = self._load_ignore_spec(ignore_file)
        self.include_file= self._load_include_spec(include_file)

    def _load_ignore_spec(self, file):
        pass


    def _load_include_spec(self, file):
        pass

    def get_current_state(self):
        state = {}

        for root , dirs, files in os.walk(self.base_path):
            dirs[:] = [d for d in dirs if not self.spec.match_file(str(Path(root, d).relative_to(self.base_path)))]
            
            for file in files:
                full_path = Path(root) / file
                rel_path = str(full_path.relative_to(self.base_path))

                if not self.spec.match_file(rel_path):
                    state[rel_path] = self._hash_file(rel_path)

        return state


    def _hash_file(self, path)
        return hashlib.md5(open(path, 'rb').read()).hexdigest()

