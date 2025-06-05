"""
Custom audio player component for Streamlit apps.

Provides a stylized HTML5 audio player with playback controls,
speed adjustment, and a seekable timeline, embedded using Streamlit Components.
"""

import streamlit.components.v1 as components
import base64

class CustomAudioPlayer:
    """
    A custom audio player for Streamlit that provides enhanced playback controls,
    including seeking, speed adjustment, and a real-time progress slider.
    """

    def __init__(self, audio_path: str, player_width: int = 600, player_height: int = 200):
        """
        Initializes the CustomAudioPlayer instance.

        Args:
            audio_path (str): Path to the audio file to be played (MP3 format recommended).
            player_width (int): Maximum width of the player in pixels. Defaults to 600.
            player_height (int): Height of the rendered HTML player. Defaults to 200.
        """
        self.audio_path = audio_path
        self.player_width = player_width
        self.player_height = player_height
        self.audio_base64 = self._load_audio_base64()  # Load and encode audio on init

    def _load_audio_base64(self) -> str:
        """
        Reads the audio file from disk and encodes it to a base64 string.

        Returns:
            str: Base64-encoded audio content.
        """
        with open(self.audio_path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    def render(self):
        """
        Renders the custom audio player with playback, seeking, and speed controls.
        Embeds an HTML + JavaScript audio interface into the Streamlit app.
        """
        # HTML and JS for a styled, interactive audio player
        html_code = f"""
        <div style="width: 100%; max-width: {self.player_width}px; margin: auto; font-family: Arial, sans-serif;">
            <!-- Audio Element -->
            <audio id="audio" style="width: 100%; margin-bottom: 10px;">
                <source src="data:audio/mp3;base64,{self.audio_base64}" type="audio/mp3">
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

            <!-- Styling for Buttons and Slider -->
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

            <!-- JavaScript Logic -->
            <script>
                const audio = document.getElementById('audio');
                const seekSlider = document.getElementById('seekSlider');
                const speedDisplay = document.getElementById('speedDisplay');
                const currentTimeText = document.getElementById('currentTime');
                const totalTimeText = document.getElementById('totalTime');

                // Toggle play/pause
                function togglePlay() {{
                    if (audio.paused) {{
                        audio.play();
                    }} else {{
                        audio.pause();
                    }}
                }}

                // Change playback speed with upper/lower bounds
                function changeSpeed(delta) {{
                    let newRate = Math.round((audio.playbackRate + delta) * 100) / 100;
                    if (newRate < 0.25) newRate = 0.25;
                    if (newRate > 4.0) newRate = 4.0;
                    audio.playbackRate = newRate;
                    speedDisplay.textContent = "Speed: " + newRate.toFixed(2) + "x";
                }}

                // Format time in mm:ss
                function formatTime(seconds) {{
                    const minutes = Math.floor(seconds / 60);
                    const secs = Math.floor(seconds % 60).toString().padStart(2, '0');
                    return `${{minutes}}:${{secs}}`;
                }}

                // Set total duration when metadata is loaded
                audio.addEventListener('loadedmetadata', () => {{
                    seekSlider.max = audio.duration;
                    totalTimeText.textContent = formatTime(audio.duration);
                }});

                // Update slider and current time as audio plays
                audio.addEventListener('timeupdate', () => {{
                    seekSlider.value = audio.currentTime;
                    currentTimeText.textContent = formatTime(audio.currentTime);
                }});

                // Allow manual seeking
                seekSlider.addEventListener('input', () => {{
                    audio.currentTime = seekSlider.value;
                }});
            </script>
        </div>
        """

        # Render the HTML/JS audio player inside Streamlit
        components.html(html_code, height=self.player_height)
