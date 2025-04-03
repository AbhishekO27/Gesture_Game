import cv2
import mediapipe as mp
import pygame
import numpy as np
import random

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
CAMERA_WIDTH, CAMERA_HEIGHT = 200, 150  # Small camera feed in the corner
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.mixer.init()

# Load Assets
background = pygame.image.load(r"D:\Marvinno\Gesture_Game\background.jpg").convert()

bucket_img = pygame.image.load(r"D:\Marvinno\Gesture_Game\tank.png").convert_alpha()
ball_img = pygame.image.load(r"D:\Marvinno\Gesture_Game\rain_drop.png").convert_alpha()
golden_ball_img = pygame.image.load(r"D:\Marvinno\Gesture_Game\golden_drop.png").convert_alpha()

# Resize Images
background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))

bucket_width = 150
bucket_height = int(bucket_img.get_height() * (bucket_width / bucket_img.get_width()))
bucket_img = pygame.transform.smoothscale(bucket_img, (bucket_width, bucket_height))

ball_width = 30
ball_height = int(ball_img.get_height() * (ball_width / ball_img.get_width()))
ball_img = pygame.transform.smoothscale(ball_img, (ball_width, ball_height))
golden_ball_img = pygame.transform.smoothscale(golden_ball_img, (ball_width, ball_height))

# Sounds
catch_sound = pygame.mixer.Sound(r"D:\Marvinno\Gesture_Game\catch.wav")

background_music = r"D:\Marvinno\Gesture_Game\bg_music.mp3"
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)

# Fonts
font = pygame.font.SysFont("Times New Roman", 48)

def draw_text(text, x, y, color=(255, 255, 255), size=48):
    font = pygame.font.SysFont("Times New Roman", size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Game Variables
bucket = pygame.Rect(WIDTH // 2 - bucket_width // 2, HEIGHT - 120, bucket_width, bucket_height)
ball = None  # Only one drop at a time
lives = 3
score = 0
ball_speed = 5
paused = False

# Camera Settings
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Capture width
cap.set(4, 360)  # Capture height

def spawn_ball():
    """ Spawns a new ball only if none exists. """
    global ball
    if ball is None:
        special = random.random() < 0.2  # 20% chance for a golden drop
        ball_type = "golden" if special else "normal"
        ball = {
            "rect": pygame.Rect(np.random.randint(0, WIDTH - ball_width), 0, ball_width, ball_height),
            "type": ball_type
        }

# Spawn the first ball
spawn_ball()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Mirror effect for natural movement
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB to fix blue tint
    frame = cv2.resize(frame, (640, 360))  # Resize to focus on relevant area
    result = pose.process(frame)

    # Detect body position
    if result.pose_landmarks:
        left_hip = result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
        
        # Normalize movement so slight shifts move the tank more
        x_body = ((left_hip.x + right_hip.x) / 2) * WIDTH
        bucket.x += (x_body - bucket.x) * 0.5  # Increased follow speed for better movement

        # Limit tank movement within screen
        bucket.x = max(0, min(bucket.x, WIDTH - bucket_width))

    screen.blit(background, (0, 0))
    screen.blit(bucket_img, bucket)

    if ball:
        ball["rect"].y += ball_speed
        if ball["type"] == "golden":
            screen.blit(golden_ball_img, ball["rect"])
        else:
            screen.blit(ball_img, ball["rect"])
    
    # Ball Collision & Removal
    if ball:
        if bucket.colliderect(ball["rect"]):  # Ball caught
            score += 5 if ball["type"] == "golden" else 1
            pygame.mixer.Sound.play(catch_sound)
            if score % 10 == 0:
                ball_speed += 1
            ball = None  # Remove the caught ball
        elif ball["rect"].y > HEIGHT:  # Ball missed
            lives -= 1
            ball = None  # Remove the missed ball
            if lives == 0:
                break

    # Spawn a new ball if the previous one is gone
    spawn_ball()

    # Draw Score and Lives Next to Each Other
    draw_text(f"Lives: {lives} | Score: {score}", WIDTH - 350, 20, (255, 255, 255), 48)

    # Convert camera frame for Pygame and display it
    frame = cv2.resize(frame, (CAMERA_WIDTH, CAMERA_HEIGHT))  # Resize for overlay
    frame = np.rot90(frame)  # Rotate to match Pygame coordinate system
    frame_surface = pygame.surfarray.make_surface(frame)  # Convert to Pygame surface
    screen.blit(pygame.transform.scale(frame_surface, (CAMERA_WIDTH, CAMERA_HEIGHT)), (10, 10))  # Resize before displaying

    pygame.display.flip()
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
                pygame.mixer.music.pause() if paused else pygame.mixer.music.unpause()

cap.release()
pygame.quit()
