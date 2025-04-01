import cv2
import mediapipe as mp
import pygame
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load Assets
background = pygame.image.load("background.jpg")
bucket_img = pygame.image.load("bucket.png")
ball_img = pygame.image.load("ball.png")

# Resize Images
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Fit screen
bucket_width, bucket_height = 150, 75  # Bigger bucket
bucket_img = pygame.transform.scale(bucket_img, (bucket_width, bucket_height))
ball_img = pygame.transform.scale(ball_img, (30, 30))  # Slightly bigger ball

# Game Variables
bucket = pygame.Rect(WIDTH // 2 - bucket_width // 2, HEIGHT - 120, bucket_width, bucket_height)
ball = pygame.Rect(np.random.randint(0, WIDTH - 30), 0, 30, 30)
score = 0

# Capture Video
cap = cv2.VideoCapture(0)
running = True

while running:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame for mirror effect
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb_frame)

    # Detect body position
    if result.pose_landmarks:
        left_hip = result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
        x_body = int(((left_hip.x + right_hip.x) / 2) * WIDTH)
        bucket.x = max(0, min(WIDTH - bucket.width, x_body))

    # Draw UI
    screen.blit(background, (0, 0))  # Set background
    screen.blit(bucket_img, bucket)  # Draw larger bucket
    screen.blit(ball_img, ball)  # Draw ball

    # Ball movement
    ball.y += 5
    if ball.y > HEIGHT:
        ball.x = np.random.randint(0, WIDTH - 30)
        ball.y = 0

    # Check collision
    if bucket.colliderect(ball):
        score += 1
        ball.x = np.random.randint(0, WIDTH - 30)
        ball.y = 0

    # Display Score
    font = pygame.font.Font(None, 48)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    # Show webcam video
    cv2.imshow("Body Tracking", frame)

    # Update Game Display
    pygame.display.flip()
    clock.tick(30)

    # Exit on keypress
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

cap.release()
cv2.destroyAllWindows()
pygame.quit()
