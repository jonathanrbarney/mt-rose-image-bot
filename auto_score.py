import os
import time
import uuid
from datetime import datetime, timedelta, timezone
from PIL import Image, ExifTags
from get_score import get_score
import ffmpeg
import pytz
from suntime import Sun, SunTimeException
import piexif

pst = pytz.timezone("US/Pacific")

# List of stream URLs
urls = [
    "https://5f4ad95bcff44.streamlock.net:444/mtrosecam/mtrosecam.stream/playlist.m3u8",
    "https://5b8462eb3469a.streamlock.net:444/mtrosesummit/mtrosesummit.stream/playlist.m3u8",
    "https://5b8462eb3469a.streamlock.net:444/mtroseslidebowl/mtroseslidebowl.stream/playlist.m3u8",
    "https://5f4ad95bcff44.streamlock.net:444/mtrosewcl/mtrosewcl.stream/playlist.m3u8",
    "https://5f9f690034fb0.streamlock.net:444/mtrose1/mtrose1.stream/playlist.m3u8",
]

IMAGES_DIR = "images"

latitude, longitude = 39.3155556, -119.8847222
sun = Sun(latitude, longitude)

SUNRISE_OFFSET_HOURS = 1


def capture_image(url, filename):
    try:
        stream = ffmpeg.input(url)

        # Apply the vframes option (capture only one frame)
        stream = ffmpeg.output(stream, filename, vframes=1, y=None, update=1)

        ffmpeg.run(stream, quiet=True)
        # ffmpeg.run(stream)
    except Exception as e:
        print(f"Error executing ffmpeg: {e}")


def set_exif_data(image_file_name, image_url, aesthetic_score):
    # Load the image using PIL
    img = Image.open(image_file_name)

    # Check if the image has EXIF data
    exif_data = img.info.get("exif")
    if exif_data:
        exif_dict = piexif.load(exif_data)
    else:
        # If no EXIF data is present, initialize with a default empty dictionary for each category
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}

    # Convert the aesthetic_score, image_url, and current date-time into bytes format
    aesthetic_score_bytes = str(aesthetic_score).encode("utf-8")
    image_url_bytes = image_url.encode("utf-8")
    current_datetime_bytes = (
        datetime.now().strftime("%Y:%m:%d %H:%M:%S").encode("utf-8")
    )

    # Use the 'ImageDescription' tag for aesthetic score, 'Make' tag for image url,
    # and 'DateTime' tag for the current date-time
    # Note: This is for demonstration purposes only, and you might want to choose other tags for these data points
    exif_dict["0th"][piexif.ImageIFD.ImageDescription] = aesthetic_score_bytes
    exif_dict["0th"][piexif.ImageIFD.Make] = image_url_bytes
    exif_dict["0th"][piexif.ImageIFD.DateTime] = current_datetime_bytes

    exif_bytes = piexif.dump(exif_dict)
    img.save(image_file_name, exif=exif_bytes)
    img.close()  # Close the image after saving changes


def get_today_folder():
    today = datetime.now(pst).strftime("%Y%m%d")
    folder_path = os.path.join(IMAGES_DIR, today)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


def get_sunrise_sunset_in_utc(now_time):
    local_date = now_time.date()
    sunrise = sun.get_sunrise_time(local_date)
    sunset = sun.get_sunrise_time(local_date)
    return sunrise, sunset


def get_top_images_from_folder(folder):
    image_files = [f for f in os.listdir(folder) if f.endswith(".jpg")]
    top_images = [{"score": 0, "path": ""} for _ in range(3)]

    for img_file in image_files:
        path = os.path.join(folder, img_file)
        try:
            score = get_score(path)
            for i, img in enumerate(top_images):
                if score > img["score"]:
                    top_images.insert(i, {"score": score, "path": path})
                    top_images.pop()
                    break
        except Exception as e:
            print(f"Error calculating score for {path}: {e}")

    return sorted(top_images, key=lambda x: x["score"], reverse=True)


def monitor_streams(interval):
    today_folder = get_today_folder()
    top_images = get_top_images_from_folder(today_folder)

    while True:
        current_time = datetime.utcnow().replace(tzinfo=timezone.utc)
        sunrise, sunset = get_sunrise_sunset_in_utc(current_time)

        if (
            sunrise - timedelta(hours=SUNRISE_OFFSET_HOURS)
            < current_time
            < sunset + timedelta(hours=SUNRISE_OFFSET_HOURS)
        ):
            for idx, url in enumerate(urls):
                temp_filename = os.path.join(today_folder, f"{str(uuid.uuid4())}.jpg")
                capture_image(url, temp_filename)

                try:
                    score = get_score(temp_filename)
                    set_exif_data(temp_filename, url, score)

                    for i, img in enumerate(top_images):
                        if score > img["score"]:
                            top_images.insert(
                                i, {"score": score, "path": temp_filename}
                            )
                            top_images.pop()
                            break

                    top_images = sorted(
                        top_images, key=lambda x: x["score"], reverse=True
                    )
                except Exception as e:
                    print(f"Error calculating score for {temp_filename}: {e}")
                    os.remove(temp_filename)

        print("-" * 80)
        print(f"Top 3 images at {time.strftime('%H:%M:%S')}:")
        for i, img in enumerate(top_images):
            print(f"Top {i + 1}: {img['path']} with score {img['score']}")

        for file_path in os.listdir(today_folder):
            if os.path.join(today_folder, file_path) not in [
                x["path"] for x in top_images
            ]:
                os.remove(os.path.join(today_folder, file_path))

        if today_folder != get_today_folder():
            today_folder = get_today_folder()
            top_images = get_top_images_from_folder(today_folder)

        processing_end = datetime.utcnow().replace(tzinfo=timezone.utc)
        processing_time = (processing_end - current_time).seconds

        time.sleep(max(interval - processing_time, 0))


if __name__ == "__main__":
    monitor_streams(60)
