#!/usr/bin/env python3
"""
Astrology AI - Automated GitHub Operations
Handles automatic commits, pushes, and releases
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

class GitHubAutomation:
    def __init__(self, repo_path=None):
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.git_available = self._check_git()
    
    def _check_git(self):
        """Check if git is available and we're in a git repository"""
        try:
            result = subprocess.run(
                ['git', 'status'], 
                cwd=self.repo_path,
                capture_output=True, 
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            print("❌ Git is not installed or not in PATH")
            return False
    
    def _run_git_command(self, command, check=True):
        """Run a git command and return the result"""
        try:
            result = subprocess.run(
                command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=check
            )
            return result
        except subprocess.CalledProcessError as e:
            print(f"❌ Git command failed: {' '.join(command)}")
            print(f"Error: {e.stderr}")
            return None
    
    def check_status(self):
        """Check repository status"""
        if not self.git_available:
            return False
        
        print("📊 Repository Status")
        print("=" * 40)
        
        # Check current branch
        result = self._run_git_command(['git', 'branch', '--show-current'])
        if result:
            print(f"🌿 Current branch: {result.stdout.strip()}")
        
        # Check status
        result = self._run_git_command(['git', 'status', '--porcelain'])
        if result:
            if result.stdout.strip():
                print("📝 Uncommitted changes found:")
                for line in result.stdout.strip().split('\n'):
                    print(f"   {line}")
            else:
                print("✅ Working directory clean")
        
        # Check remote status
        result = self._run_git_command(['git', 'remote', '-v'])
        if result:
            print(f"🔗 Remote repositories:")
            for line in result.stdout.strip().split('\n'):
                print(f"   {line}")
        
        return True
    
    def auto_commit_push(self, message=None, add_all=True):
        """Automatically commit and push changes"""
        if not self.git_available:
            print("❌ Git not available")
            return False
        
        print("🚀 Auto Commit & Push")
        print("=" * 30)
        
        # Check for changes
        result = self._run_git_command(['git', 'status', '--porcelain'])
        if not result or not result.stdout.strip():
            print("✅ No changes to commit")
            return True
        
        # Add files
        if add_all:
            print("📁 Adding all changes...")
            result = self._run_git_command(['git', 'add', '.'])
            if not result:
                return False
        
        # Create commit message
        if not message:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"🔄 Auto-update: {timestamp}"
        
        # Commit
        print(f"💾 Committing: {message}")
        result = self._run_git_command(['git', 'commit', '-m', message])
        if not result:
            return False
        
        # Push
        print("📡 Pushing to GitHub...")
        result = self._run_git_command(['git', 'push', 'origin', 'main'])
        if result:
            print("🎉 Successfully pushed to GitHub!")
            return True
        else:
            print("❌ Failed to push to GitHub")
            return False
    
    def create_release(self, version, message=None):
        """Create a new release with a version tag"""
        if not self.git_available:
            print("❌ Git not available")
            return False
        
        print(f"🏷️ Creating release: {version}")
        print("=" * 40)
        
        # Ensure we're up to date
        result = self._run_git_command(['git', 'pull', 'origin', 'main'])
        if not result:
            print("❌ Failed to pull latest changes")
            return False
        
        # Create tag
        tag_name = f"v{version}" if not version.startswith('v') else version
        tag_message = message or f"Release {tag_name}"
        
        print(f"🏷️ Creating tag: {tag_name}")
        result = self._run_git_command(['git', 'tag', '-a', tag_name, '-m', tag_message])
        if not result:
            return False
        
        # Push tag
        print("📡 Pushing tag to GitHub...")
        result = self._run_git_command(['git', 'push', 'origin', tag_name])
        if result:
            print(f"🎉 Release {tag_name} created successfully!")
            print("📦 GitHub Actions will automatically create the release")
            return True
        else:
            print("❌ Failed to push tag to GitHub")
            return False
    
    def sync_with_remote(self):
        """Sync local repository with remote"""
        if not self.git_available:
            return False
        
        print("🔄 Syncing with remote repository...")
        
        # Fetch latest changes
        result = self._run_git_command(['git', 'fetch', 'origin'])
        if not result:
            return False
        
        # Check if we're behind
        result = self._run_git_command(['git', 'status', '-uno'])
        if result and "behind" in result.stdout:
            print("📥 Pulling latest changes...")
            result = self._run_git_command(['git', 'pull', 'origin', 'main'])
            if result:
                print("✅ Successfully synced with remote")
                return True
            else:
                print("❌ Failed to pull changes")
                return False
        else:
            print("✅ Already up to date")
            return True
    
    def export_stats(self):
        """Export current knowledge base statistics"""
        try:
            # Change to astrology_ai directory
            astrology_dir = self.repo_path / "astrology_ai"
            if not astrology_dir.exists():
                print("❌ Astrology AI directory not found")
                return None
            
            # Run stats command
            result = subprocess.run([
                sys.executable, '-m', 'src.cli', 'stats'
            ], cwd=astrology_dir, capture_output=True, text=True)
            
            if result.returncode == 0:
                return result.stdout
            else:
                print(f"❌ Failed to get stats: {result.stderr}")
                return None
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
            return None


def main():
    parser = argparse.ArgumentParser(description="Astrology AI GitHub Automation")
    parser.add_argument('action', choices=['status', 'commit', 'push', 'release', 'sync', 'stats'], 
                       help='Action to perform')
    parser.add_argument('-m', '--message', help='Commit or release message')
    parser.add_argument('-v', '--version', help='Release version (for release action)')
    parser.add_argument('--no-add', action='store_true', help="Don't add all files before commit")
    
    args = parser.parse_args()
    
    automation = GitHubAutomation()
    
    if args.action == 'status':
        automation.check_status()
    
    elif args.action == 'commit':
        automation.auto_commit_push(
            message=args.message, 
            add_all=not args.no_add
        )
    
    elif args.action == 'push':
        # First commit if there are changes, then push
        automation.auto_commit_push(
            message=args.message or "🔄 Auto-push update",
            add_all=not args.no_add
        )
    
    elif args.action == 'release':
        if not args.version:
            print("❌ Release version required (-v/--version)")
            sys.exit(1)
        automation.create_release(args.version, args.message)
    
    elif args.action == 'sync':
        automation.sync_with_remote()
    
    elif args.action == 'stats':
        stats = automation.export_stats()
        if stats:
            print("📊 Current Statistics:")
            print(stats)
    
    print("\n🔗 Repository: https://github.com/Veg-briyani/vediq.git")


if __name__ == "__main__":
    main() 