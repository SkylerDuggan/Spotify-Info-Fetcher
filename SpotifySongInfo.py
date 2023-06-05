import requests
import random
from tkinter import Tk, Text, Button, END, Label
from tkinter import ttk

client_id = "your id"
client_secret = "your secret"

def get_track_info(track_id):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    
    auth_response = requests.post("https://accounts.spotify.com/api/token", {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })

    if auth_response.status_code != 200:
        raise Exception(f"Failed to get access token: {auth_response.content}")

    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']
    
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    track_info_response = requests.get(url, headers=headers)
    if track_info_response.status_code != 200:
        raise Exception(f"Failed to get track info: {track_info_response.content}")

    track_info = track_info_response.json()
    artists = [artist['name'] for artist in track_info['artists']]
    song_name = track_info['name']
    album_name = track_info['album']['name'] if track_info['album']['album_type'] != 'single' else None
    return song_name, album_name, artists

def process_input():
    urls = text_input.get("1.0", END).split('\n')
    output_text.delete("1.0", END)
    artist_dict = {}
    color_dict = {}
    output_entries = []  
    for url in urls:
        if url.strip():  
            try:
                track_id = url.split('/')[-1]
                song_name, album_name, artist_list = get_track_info(track_id)
                main_artist = artist_list[0]
                if main_artist not in artist_dict:
                    artist_dict[main_artist] = 1
                else:
                    artist_dict[main_artist] += 1
                artist_name_str = ', '.join(artist_list)
                if album_name:
                    output = f"{song_name}, {album_name}, {artist_name_str}"
                else:
                    output = f"{song_name}, {artist_name_str}"
                output_entries.append((main_artist, output)) 
            except Exception as e:
                output_text.insert(END, f"Failed to process URL '{url}': {str(e)}\n\n")

    output_entries.sort(key=lambda x: x[0])

    for artist in artist_dict:
        if artist_dict[artist] > 1:
            color_dict[artist] = "#%06x" % random.randint(0, 0xFFFFFF)
            tag = artist.replace(" ", "_")
            output_text.tag_config(tag, foreground=color_dict[artist])

    for main_artist, output in output_entries:
        if artist_dict[main_artist] > 1:  
            tag = main_artist.replace(" ", "_")
            song_info, artist_info = output.rsplit(", ", 1)
            output_text.insert(END, f"{song_info}, ")
            output_text.insert(END, f"{artist_info}\n\n", tag)
        else:
            output_text.insert(END, f"{output}\n\n")  

root = Tk()
root.title('Spotify Track Info Fetcher')
root.geometry('500x600')

style = ttk.Style(root)
style.configure('.', font=('Arial', 12), foreground='white', background='black')

root.configure(background='black')

logo = Label(root, text="Skyler Duggan", font=("Arial", 24), fg="white", bg="black")
logo.pack(pady=(20,10))

input_label = Label(root, text="Enter Spotify URLs (one per line):", bg="black", fg="white")
input_label.pack(pady=(10,10))

text_input = Text(root, height=10, bg="black", fg="white")
text_input.pack(padx=20, fill='x')

process_button = Button(root, text="Get Track Info", command=process_input)
process_button.pack(pady=20)

output_label = Label(root, text="Track Info (Song, Album, Artist):", bg="black", fg="white")
output_label.pack(pady=(20,10))

output_text = Text(root, height=10, bg="black", fg="white")
output_text.pack(padx=20, pady=(0,20), fill='x')

root.mainloop()
