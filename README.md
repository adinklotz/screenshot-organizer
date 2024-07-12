Windows Game Bar screenshots are all dumped into one directory, named by what game they come from. This little script sorts them by game into their own directories.

I also extended it to handle Steam screenshots. When you take a screenshot by pressing F12 in Steam, it saves it to a Steam directory, unhelpfully named by the game's numerical Steam ID.
I download the list of IDs from Steam and use that to identify the corresponding game and move it to that directory.

This is *extremely* quick and dirty. I wrote it a few years ago and have meant to go back and clean it up, but it continues to Work On My Machine™️ so I haven't had the need to yet.
Just keep in mind the code is pretty sloppy and it may be fragile if you try to use it on your machine.
