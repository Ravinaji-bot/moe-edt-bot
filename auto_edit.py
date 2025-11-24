import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips, vfx

# --- CONFIGURATION (Settings) ---
INPUT_VIDEO_PATH = "input_clip.mp4"
BG_MUSIC_PATH = "bg_music.mp3"
OUTPUT_DIR = "output_clips"
CLIP_DURATION_SEC = 20 # Har clip ki lambai (seconds mein)

# Output directory/folder check karein
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def apply_advanced_edits(clip):
    """
    Copyright/Reused content se bachne ke liye advanced changes apply karta hai.
    """
    
    # 1. Dynamic Color Correction (Thoda sa brightness change)
    color_factor = random.uniform(0.95, 1.05) # 5% kam ya zyada
    edited_clip = clip.fx(vfx.colorx, color_factor)
    print(f"-> Color Correction applied (Factor: {color_factor:.2f})")

    # 2. Minor Resizing/Cropping (Thoda sa zoom)
    resize_factor = 0.95 # Clip ko 95% tak chota karega (slight zoom-in effect)
    resized_clip = edited_clip.resize(resize_factor)
    print(f"-> Resizing applied (Factor: {resize_factor:.2f})")
    
    # 3. Slight Random Speed Adjustment (Thodi si speed kam ya zyada)
    speed_factor = random.uniform(0.98, 1.02)
    final_clip = resized_clip.speedx(speed_factor)
    print(f"-> Speed Adjusted (Factor: {speed_factor:.2f})")
    
    return final_clip

def process_video_clip(input_path, music_path):
    """
    Video ko process karta hai aur export karta hai.
    """
    try:
        # 1. Video load karein
        original_clip = VideoFileClip(input_path)
        video_duration = original_clip.duration
        
        if video_duration < CLIP_DURATION_SEC:
            print(f"ERROR: Video ki lambai kam hai. Kam se kam {CLIP_DURATION_SEC} seconds chahiye.")
            return

        # 2. Random Segment (hissa) chunein
        max_start = video_duration - CLIP_DURATION_SEC
        start_time = random.uniform(0, max_start)
        
        # Segment cut karein
        sub_clip = original_clip.subclip(start_time, start_time + CLIP_DURATION_SEC)
        print(f"Video segment chuna gaya: {start_time:.2f}s se {start_time + CLIP_DURATION_SEC:.2f}s")

        # 3. Visual Editing lagoo karein
        processed_clip = apply_advanced_edits(sub_clip)
        
        # 4. Audio Mixing
        
        # Original Audio: Volume bahut kam kar dein (10% volume)
        original_audio = processed_clip.audio.volumex(0.1)
        
        # Background Music load karein
        bg_music = AudioFileClip(music_path).set_duration(processed_clip.duration)
        
        # Dono audio tracks ko mix karein
        final_audio = concatenate_audioclips([original_audio, bg_music])
        final_clip = processed_clip.set_audio(final_audio)

        # 5. Output File ka Naam (Unique/alag naam)
        output_filename = f"clip_edited_{int(start_time)}_{random.randint(100, 999)}.mp4"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        # 6. File export karein
        print(f"\n--- Output file ban rahi hai: {output_filename} ---")
        final_clip.write_videofile(
            output_path, 
            codec="libx264", 
            audio_codec="aac", 
            temp_audiofile='temp-audio.m4a', 
            remove_temp=True,
            fps=original_clip.fps
        )
        print(f"✅ SUCCESS! Edited clip save ho gayi: {output_path}")

    except Exception as e:
        print(f"❌ Koi error aa gaya: {e}")
        if "ffmpeg" in str(e).lower():
            print("\n**NOTE:** Agar FFmpeg ki error aa rahi hai, toh aapko FFmpeg alag se install karna pad sakta hai.")


if __name__ == "__main__":
    print("--- Movie Clip Auto Editor Shuru Ho Raha Hai ---")
    if not os.path.exists(INPUT_VIDEO_PATH) or not os.path.exists(BG_MUSIC_PATH):
        print(f"\nFATAL ERROR: Confirm karein ki yeh files same folder mein hain:")
        print(f"- Input Video: {INPUT_VIDEO_PATH}")
        print(f"- Background Music: {BG_MUSIC_PATH}")
    else:
        process_video_clip(INPUT_VIDEO_PATH, BG_MUSIC_PATH)
    print("-----------------------------------------------")
    
