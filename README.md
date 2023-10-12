## Aesthetic Image Monitor for Live Streams

Capture the breathtaking moments of sunrise and sunset with the Aesthetic Image Monitor for Live Streams. Leveraging the prowess of OpenAI's CLIP model, this tool evaluates the aesthetic essence of images captured in real-time from various streams, curating the crème de la crème of the day's visual delight.

### Features:

- **AI-Powered Scoring**: Uses the state-of-the-art CLIP model from OpenAI to gauge the beauty of images.
- **Timed Captures**: Automatically harvests images during the golden hours of sunrise and sunset.
- **Daily Curation**: Reserves the top 3 aesthetically captivating images every day.
- **Rich Metadata**: Incorporates the aesthetic score, stream's URL, and capture timestamp within the EXIF data for each image.

### Installation:

1. **Set Up Repository**:
    ```bash
    git clone https://github.com/jonathanrbarney/mt-rose-image-bot
    cd mt-rose-image-bot
    ```

2. **Library Installation**:
    ```bash
    pip install -r requirements.txt
    ```

### Usage:

Simply kickstart the monitor script using:
```bash
python auto_score.py
```
Watch it come alive, capturing and curating moments from your chosen streams, and maintaining a daily portfolio of visual marvels.

### Directory Layout:

- All images are diligently stored in the `images` folder.
- For ease of access, daily captures are housed in sub-folders named by date in the `YYYYMMDD` format.

### Configuration:

- `urls`: Personalize streams by updating the list.
- `IMAGES_DIR`: Customize the primary directory for image storage.
- Geolocation Settings: Reset `latitude` and `longitude` as per the location to determine accurate sunrise and sunset times.
- `SUNRISE_OFFSET_HOURS`: Define the window around sunrise and sunset for capturing images.

### Contributions:

Your insights can elevate this project! Feel free to fork, enhance, and if you believe you've added value, send over a pull request.

### License:

Bask in the freedom of open-source. This venture thrives under the MIT License.

### Docker Deployment:

For those who prefer a containerized environment, there's a Dockerfile to simplify deployment. Once you have Docker installed:

1. **Build the Image**:
    ```bash
    docker build -t mt-rose-image-bot:latest .
    ```

2. **Run the Container**:
    ```bash
    docker run -v /path/to/local/images/folder:/app/images mt-rose-image-bot
    ```

Note: Replace `/path/to/local/images/folder` with the local directory path where you wish to store the images.

---

I hope you enjoy capturing and curating the visual wonders of our world with this tool. If you encounter issues or have suggestions, open an issue on the GitHub repository, and let's build together!