# import streamlit as st
import streamlit.components.v1 as components
import base64

# audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
def display_audio_bar(audio_path):
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
    html_code = f"""
    <div style="width: 100%; max-width: 600px; margin: auto; font-family: Arial, sans-serif;">
    <audio id="audio" style="width: 100%; margin-bottom: 10px;">
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>

    <!-- Playback Controls -->
    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
        <button class="audio-btn" onclick="document.getElementById('audio').currentTime -= 10">⏪ -10s</button>
        <button class="audio-btn" onclick="togglePlay()">▶️/⏸️ Play/Pause</button>
        <button class="audio-btn" onclick="document.getElementById('audio').currentTime += 10">⏩ +10s</button>
    </div>

    <!-- Speed Controls -->
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <button class="audio-btn" onclick="changeSpeed(-0.25)">➖ Speed</button>
        <span id="speedDisplay" style="flex-grow: 1; text-align: center;">Speed: 1.0x</span>
        <button class="audio-btn" onclick="changeSpeed(0.25)">➕ Speed</button>
    </div>

    <!-- Seekable Slider -->
    <div style="margin-top: 10px;">
        <input type="range" id="seekSlider" value="0" min="0" max="100" step="0.1" style="width: 100%;">
        <div style="display: flex; justify-content: space-between; font-size: 12px;">
        <span id="currentTime">0:00</span>
        <span id="totalTime">0:00</span>
        </div>
    </div>

    <!-- Styling -->
    <style>
        .audio-btn {{
        background-color: #4a90e2;
        color: white;
        padding: 10px 16px;
        font-size: 14px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        }}
        .audio-btn:hover {{
        background-color: #357ABD;
        }}
        input[type=range] {{
        accent-color: #4a90e2;
        }}
    </style>

    <!-- JS Logic -->
    <script>
        const audio = document.getElementById('audio');
        const seekSlider = document.getElementById('seekSlider');
        const speedDisplay = document.getElementById('speedDisplay');
        const currentTimeText = document.getElementById('currentTime');
        const totalTimeText = document.getElementById('totalTime');

        function togglePlay() {{
        if (audio.paused) {{
            audio.play();
        }} else {{
            audio.pause();
        }}
        }}

        function changeSpeed(delta) {{
        let newRate = Math.round((audio.playbackRate + delta) * 100) / 100;
        if (newRate < 0.25) newRate = 0.25;
        if (newRate > 4.0) newRate = 4.0;
        audio.playbackRate = newRate;
        speedDisplay.textContent = "Speed: " + newRate.toFixed(2) + "x";
        }}

        function formatTime(seconds) {{
        const minutes = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60).toString().padStart(2, '0');
        return `${{minutes}}:${{secs}}`;
        }}

        audio.addEventListener('loadedmetadata', () => {{
        seekSlider.max = audio.duration;
        totalTimeText.textContent = formatTime(audio.duration);
        }});

        audio.addEventListener('timeupdate', () => {{
        seekSlider.value = audio.currentTime;
        currentTimeText.textContent = formatTime(audio.currentTime);
        }});

        seekSlider.addEventListener('input', () => {{
        audio.currentTime = seekSlider.value;
        }});
    </script>
    </div>
    """

    components.html(html_code, height=200)