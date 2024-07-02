from args import get_args
from runner import run_mediapipe_socket

if __name__ == "__main__":
    args = get_args()
    run_mediapipe_socket(args)
