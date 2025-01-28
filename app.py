import os
import shutil
import subprocess
from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import safe_join

app = Flask(__name__)

# Define output folder structure
base_output_folder = r'D:\Demux\output_folder'
vocals_folder = os.path.join(base_output_folder, 'Vocals')
others_folder = os.path.join(base_output_folder, 'Others')

# Ensure folders exist
os.makedirs(vocals_folder, exist_ok=True)
os.makedirs(others_folder, exist_ok=True)

# Check if GPU is available
def check_gpu():
    import torch
    if torch.cuda.is_available():
        return f"GPU is available: {torch.cuda.get_device_name(0)}"
    else:
        return "GPU is not available. Demucs will use the CPU."


@app.route('/download/<folder>/<filename>')
def download(folder, filename):
    try:
        file_path = safe_join(base_output_folder, folder, filename)
        if os.path.exists(file_path):
            return send_from_directory(os.path.dirname(file_path), filename, as_attachment=True)
        else:
            return "File not found", 404
    except Exception as e:
        return str(e), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    gpu_status = check_gpu()
    demucs_status = "Demucs is installed and ready."
    message = ""
    process_type = None
    original_audio = ""
    vocals_audio = ""
    others_audio = ""

    if request.method == 'POST':
        process_type = request.form['process_type']

        if process_type == 'batch_processing':
            folder_path = request.form['folder_path']
            if os.path.isdir(folder_path):
                audio_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp3', '.wav'))]
                if audio_files:
                    for audio_file in audio_files:
                        input_file = os.path.join(folder_path, audio_file)
                        song_name = os.path.splitext(audio_file)[0]
                        output_path = os.path.join(base_output_folder, 'mdx_extra', song_name)

                        # Run Demucs
                        command = [
                            'demucs', '--two-stems', 'vocals', input_file,
                            '-o', base_output_folder,
                            '-n', 'mdx_extra'
                        ]
                        subprocess.run(command, check=True)

                        # Move processed files to respective folders
                        move_processed_files(output_path, song_name)

                    message = "Batch processing complete. Vocals and other stems have been organized."
                else:
                    message = "No audio files found in the specified folder."
            else:
                message = "The provided folder path does not exist."

        elif process_type == 'single_file':
            temp_directory = 'temp'
            if not os.path.exists(temp_directory):
                os.makedirs(temp_directory)

            audio_file = request.files['audio_file']
            if audio_file:
                input_file = os.path.join(temp_directory, audio_file.filename)
                audio_file.save(input_file)

                song_name = os.path.splitext(audio_file.filename)[0]
                output_path = os.path.join(base_output_folder, 'mdx_extra', song_name)

                # Run Demucs
                command = [
                    'demucs', '--two-stems', 'vocals', input_file,
                    '-o', base_output_folder,
                    '-n', 'mdx_extra'
                ]
                subprocess.run(command, check=True)

                # Move processed files to respective folders
                move_processed_files(output_path, song_name)

                original_audio = audio_file.filename
                vocals_audio = f"{song_name}_vocals.wav"
                others_audio = f"{song_name}_others.wav"

                message = "Single file processed. Vocals and other stems have been organized."

    return render_template('index.html', gpu_status=gpu_status, demucs_status=demucs_status, message=message,
                           process_type=process_type,
                           original_audio=original_audio, vocals_audio=vocals_audio, others_audio=others_audio)


def move_processed_files(output_path, song_name):
    """Move processed files to the correct folders and rename them."""
    vocals_file = os.path.join(output_path, 'vocals.wav')
    others_file = os.path.join(output_path, 'no_vocals.wav')

    if os.path.exists(vocals_file):
        shutil.move(vocals_file, os.path.join(vocals_folder, f"{song_name}_vocals.wav"))
    if os.path.exists(others_file):
        shutil.move(others_file, os.path.join(others_folder, f"{song_name}_others.wav"))


if __name__ == '__main__':
    port = int(os.environ.get("PORT",4000))
    app.run(host="0.0.0.0", port=port)
