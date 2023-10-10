import args
import runner

if __name__ == "__main__":
    args = args.get_args()
    runner.run_mediapipe_socket(args)
