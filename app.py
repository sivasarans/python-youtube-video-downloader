from flask import Flask, render_template, request, Response
from pytube import YouTube
import time

app = Flask(__name__, static_url_path='/static')

def generate_progress():
    for i in range(11):
        time.sleep(0.5)  # Simulate download time
        progress = i * 10
        print(f"Download Progress: {progress}%")
        yield f"data: {progress}\n\n"

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/download', methods=['GET', 'POST'])
def download():
    try:
        video_url = request.form['video_url']
        selected_quality = request.form['selected_quality']

        # Validate the video URL
        if "youtube.com" not in video_url and "youtu.be" not in video_url:
            raise ValueError("Invalid YouTube video URL")

        # Get the output directory from the form or use the current directory
        output_directory = "."

        # Download the video
        yt = YouTube(video_url)
        video_stream = yt.streams.filter(file_extension="mp4", res=selected_quality).first()
        video_stream.download(output_directory)

        # Render the success template with the video title
        return f"Download Successful\nTitle: {yt.title}"
    except Exception as e:
        # Render the error template with the error message
        error_message = f"Error: {e}"
        return render_template('error.html', error_message=error_message)

@app.route('/progress')
def progress():
    return Response(generate_progress(), content_type='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)
