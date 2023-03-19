import subprocess


def trim_video(input_file_name, output_file_name, start, end):
    cmd_str = f"..\..\\ffmpeg\\bin\\ffmpeg.exe -an -ss {start} -to {end} -i {input_file_name} -y {output_file_name}"
    subprocess.run(cmd_str, shell=True)
