# AI-Powered Sales Workshop Resources

Public workshop library: https://hyagomatielo.github.io/ai-sales-workshop/

## Upload workshop materials (no coding required)

1. Open the [assets folder on GitHub](https://github.com/hyagomatielo/ai-sales-workshop/tree/main/assets).
2. Choose **Add file > Upload files** (you must be signed into the owner's account).
3. Drag your files onto the page.
4. Choose **Commit changes**, committing directly to **main**.
5. Wait for the [Publish workshop site workflow](https://github.com/hyagomatielo/ai-sales-workshop/actions) to turn green, usually a few minutes. Refresh the website.

Every uploaded file gets a download card automatically. There is no separate list to maintain.
Attendees do not need a GitHub account. Share the public library link above, not the repository link.
The library opens with clickable industry folders. Open a folder to see its files,
and use the breadcrumb links or your browser's Back button to navigate.
Folder URLs can be copied and shared directly.
Search finds files in the current folder and all its subfolders; searching from
**All folders** searches the entire library. Clear search to return to folder browsing.

### Names and folders

- Use helpful filenames, such as `Customer_Research_Prompts.txt`. Underscores and hyphens become spaces in card titles.
- Files directly inside `assets` appear alongside the top-level folders.
- Subfolders, such as `assets/Session 1/`, appear as clickable folders with their original names. Nested folders are supported. Folders appear when they contain published files; empty folders are not shown.
- Any regular file type is supported. Hidden files/folders (names beginning with a dot) are not published.
- GitHub's browser uploader limits each file to 25 MiB. Git blocks files larger than 100 MiB. Use an external hosting service for larger videos or archives; this site does not upload them for you.
- GitHub Pages is public. Do not upload credentials, personal information, confidential customer data, or material you do not have permission to distribute. Deleting a file does not remove it from Git history.

### Replace or remove a resource

Upload a replacement using the same filename and folder. To remove a file, open it on GitHub and use the file menu's **Delete file** action, then commit the change. The library updates automatically after deployment.

## Site administration

- Website text, styles, and search behavior are in [index.html](index.html).
- [scripts/build.py](scripts/build.py) copies public assets and generates `resources.json` in the ignored `_site` build folder.
- [.github/workflows/pages.yml](.github/workflows/pages.yml) tests, builds, and publishes on each push to `main`.
- GitHub **Settings > Pages > Build and deployment > Source** must be **GitHub Actions**.
- If publication fails, open the Actions tab and inspect the failed step. The site displays an explicit error with a retry button if the catalog cannot be loaded.
- No paid services, dependencies, tracking, or third-party scripts are used.

## Local preview

With Python 3.12 installed, run these commands from this project folder:

```powershell
python -m unittest discover -s tests -v
python scripts\build.py
python -m http.server 8000 --bind 127.0.0.1 --directory _site
```

Open http://127.0.0.1:8000. Stop the preview with Ctrl+C. Opening `index.html` directly from disk cannot load the catalog; use the HTTP preview.
