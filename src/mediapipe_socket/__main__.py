from args import ArgParser, ParseArgs
from runner import MediaPipeSocketRunner

if __name__ == "__main__":
    args: ArgParser = ParseArgs()
    runner: MediaPipeSocketRunner = MediaPipeSocketRunner(args)
    runner.Run()
