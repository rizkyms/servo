from moviepy.editor import VideoFileClip

# Ganti 'input_video.mov' dengan nama file video yang akan diedit
input_video_path = 'input_video.mov'
output_video_path = 'output_video.mov'

# Memuat video
video = VideoFileClip(input_video_path)

# Menghapus audio
video_no_audio = video.set_audio(None)

# Menyimpan video tanpa audio
video_no_audio.write_videofile(output_video_path, codec='libx264')

# Menutup video
video.close()