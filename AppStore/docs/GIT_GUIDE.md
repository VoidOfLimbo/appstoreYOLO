# 🔧 Git Commands for AppStore Project

## 📋 Initial Setup

### Initialize Repository (if not already done)
```bash
cd c:\Users\John\Documents\python\AppStore
git init
```

### Check Current Status
```bash
git status
```

---

## 📦 First Commit

### Stage All Files
```bash
git add .
```

### Check What Will Be Committed
```bash
git status
```

### Commit with Message
```bash
git commit -m "Initial commit: AppStore with training and tracking features"
```

---

## 🌿 Connect to GitHub (appstoreYOLO)

### Add Remote Repository
```bash
git remote add origin https://github.com/VoidOfLimbo/appstoreYOLO.git
```

### Verify Remote
```bash
git remote -v
```

### Push to GitHub
```bash
git branch -M main
git push -u origin main
```

---

## 🔄 Regular Workflow

### Check Status
```bash
git status
```

### Stage Changes
```bash
# Stage all changes
git add .

# Stage specific file
git add main.py

# Stage specific directory
git add apps/training/
```

### Commit Changes
```bash
git commit -m "Add training app with Jupyter integration"
```

### Push to GitHub
```bash
git push
```

---

## 📝 Commit Message Examples

### Features
```bash
git commit -m "feat: Add StrongSORT tracking integration"
git commit -m "feat: Create model download script"
git commit -m "feat: Add Jupyter Lab integration"
```

### Fixes
```bash
git commit -m "fix: Handle PyTorch DLL loading error"
git commit -m "fix: Update TrainingApp __init__ signature"
git commit -m "fix: Improve UI spacing and margins"
```

### Documentation
```bash
git commit -m "docs: Add training notebooks README"
git commit -m "docs: Create quick start guide"
```

### Refactoring
```bash
git commit -m "refactor: Reorganize model directory structure"
git commit -m "refactor: Extract theme into separate file"
```

---

## 🔍 Useful Commands

### View Commit History
```bash
git log --oneline
git log --graph --oneline --all
```

### Check Differences
```bash
# See unstaged changes
git diff

# See staged changes
git diff --staged

# Compare with specific commit
git diff HEAD~1
```

### View File History
```bash
git log -- main.py
```

### Undo Changes

#### Unstage File
```bash
git reset HEAD main.py
```

#### Discard Changes in Working Directory
```bash
git checkout -- main.py
```

#### Undo Last Commit (keep changes)
```bash
git reset --soft HEAD~1
```

#### Undo Last Commit (discard changes)
```bash
git reset --hard HEAD~1
```

---

## 🌿 Branches

### Create New Branch
```bash
git branch feature/new-feature
```

### Switch to Branch
```bash
git checkout feature/new-feature
```

### Create and Switch in One Command
```bash
git checkout -b feature/new-feature
```

### List Branches
```bash
git branch
```

### Merge Branch
```bash
git checkout main
git merge feature/new-feature
```

### Delete Branch
```bash
git branch -d feature/new-feature
```

---

## 📥 Pull Changes

### Fetch and Merge
```bash
git pull
```

### Fetch Only
```bash
git fetch origin
```

---

## 🔖 Tags

### Create Tag
```bash
git tag v1.0.0
```

### Create Annotated Tag
```bash
git tag -a v1.0.0 -m "Version 1.0.0 - Initial release"
```

### Push Tags
```bash
git push --tags
```

### List Tags
```bash
git tag
```

---

## 🚨 Common Scenarios

### Forgot to Add Files to Last Commit
```bash
git add forgotten_file.py
git commit --amend --no-edit
```

### Change Last Commit Message
```bash
git commit --amend -m "New commit message"
```

### Stash Changes Temporarily
```bash
# Save changes
git stash

# List stashes
git stash list

# Apply latest stash
git stash apply

# Apply and remove stash
git stash pop
```

### View Remote Info
```bash
git remote show origin
```

---

## 📊 .gitignore Working?

### Check if File is Ignored
```bash
git check-ignore -v models/detection/yolo/yolov8s.pt
```

### Force Add Ignored File (if needed)
```bash
git add -f some_ignored_file.txt
```

### Remove File from Git but Keep Locally
```bash
git rm --cached models/yolov8s.pt
```

---

## 🔧 GitHub Configuration

### Set Username and Email
```bash
git config --global user.name "VoidOfLimbo"
git config --global user.email "your.email@example.com"
```

### Check Configuration
```bash
git config --list
```

---

## 📦 What's Committed vs Ignored

### ✅ Committed (in Git)
- Source code (*.py)
- Configuration files
- Documentation (*.md)
- Requirements.txt
- Project structure
- .gitignore and .gitkeep files
- Notebooks (*.ipynb)

### ❌ Ignored (not in Git)
- Models (*.pt, *.onnx, *.engine) - Too large!
- Virtual environments (.venv/)
- Training runs (runs/)
- Datasets (data/, datasets/)
- Cache files (__pycache__/)
- Log files (*.log)
- Build artifacts (dist/, build/)
- OS files (.DS_Store, Thumbs.db)

---

## 🎯 Recommended Workflow

### Daily Development
```bash
# 1. Start your day - get latest changes
git pull

# 2. Make changes to your code
# ... edit files ...

# 3. Check what changed
git status
git diff

# 4. Stage and commit
git add .
git commit -m "feat: Add new feature"

# 5. Push to GitHub
git push
```

### Feature Development
```bash
# 1. Create feature branch
git checkout -b feature/awesome-feature

# 2. Make changes and commit
git add .
git commit -m "feat: Implement awesome feature"

# 3. Push feature branch
git push -u origin feature/awesome-feature

# 4. Create Pull Request on GitHub
# (Done in browser)

# 5. After merge, switch back to main
git checkout main
git pull
```

---

## 💡 Pro Tips

1. **Commit Often:** Small, focused commits are better than large ones
2. **Write Good Messages:** Explain *why*, not just *what*
3. **Check Before Committing:** Always run `git status` and `git diff`
4. **Don't Commit Large Files:** Models should be downloaded, not committed
5. **Use Branches:** Keep main stable, develop in branches
6. **Pull Regularly:** Stay up to date with remote changes
7. **Test Before Pushing:** Make sure code runs before pushing

---

## 🆘 Emergency Commands

### Undo Everything (DANGER!)
```bash
# Discard ALL local changes
git reset --hard HEAD

# Remove all untracked files
git clean -fd
```

### Recover Deleted Branch
```bash
# Find commit hash
git reflog

# Recreate branch
git checkout -b recovered-branch <commit-hash>
```

---

## 📞 Need Help?

```bash
# Get help for any command
git help <command>
git help commit
git help push

# Quick reference
git <command> --help
```

---

**Happy Coding!** 🚀

*Remember: Commit early, commit often, push regularly!*
