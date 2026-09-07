import subprocess
import sys

def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/sync_github.py <github-repo-url>')
        print('Example: python scripts/sync_github.py https://github.com/your-username/yt-autopilot-x.git')
        return
    repo_url = sys.argv[1]
    subprocess.run(['git', 'remote', 'remove', 'origin'], capture_output=True)
    subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True)
    subprocess.run(['git', 'branch', '-M', 'main'], check=True)
    print(f'Configured remote origin -> {repo_url}')
    print('Pushing to remote...')
    subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
    print('Successfully synchronized to private GitHub repository!')

if __name__ == '__main__':
    main()
