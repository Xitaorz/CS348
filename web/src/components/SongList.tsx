import { Card, CardContent, CardTitle } from "./ui/card";

type Song = {
  id: string;
  title: string;
  artist: string;
  album: string;
}

interface SongListProps {
  songs: Song[];
}

export function SongList({ songs }: SongListProps) {
  return (
    <div className="w-full flex flex-col items-center gap-5 m-5">
      {songs.map((song) => (
        <Card key={song.id} className="mb-2 p-4 w-xl">
          <CardTitle>

          {song.title}
          </CardTitle>
          <CardContent>
            <p>Artist: {song.artist}</p>
            <p>Album: {song.album}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}