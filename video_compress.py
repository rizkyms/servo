from moviepy.editor import VideoFileClip

# Ganti 'input_video.mp4' dengan nama file video yang akan dikompres
input_video_path = 'input_video.mp4'
output_video_path = 'output_video.mp4'

# Memuat video
video = VideoFileClip(input_video_path)

# Mengubah ukuran video (misalnya menjadi setengah dari ukuran aslinya)
video_resized = video.resize(0.5)

# Menyimpan video yang telah diubah ukuran
video_resized.write_videofile(output_video_path, codec='libx264')

# Menutup video
video.close()
