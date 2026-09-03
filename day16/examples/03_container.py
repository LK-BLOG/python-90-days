"""容器协议"""
class Playlist:
    def __init__(self, name, songs):
        self.name = name
        self._songs = list(songs)
    def __len__(self):
        return len(self._songs)
    def __bool__(self):
        return len(self._songs) > 0
    def __getitem__(self, index):
        return self._songs[index]
    def __contains__(self, song):
        return song in self._songs
    def __iter__(self):
        return iter(self._songs)
    def add(self, song):
        self._songs.append(song)

pl = Playlist('My Music', ['Song A', 'Song B'])
print(len(pl))          # 2
print('Song A' in pl)   # True
print(pl[0])            # Song A
for s in pl: print(s)   # Song A, Song B
