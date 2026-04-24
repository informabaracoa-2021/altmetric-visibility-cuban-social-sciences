# Brief guide: GitHub → Zenodo → DOI

## 1. Create the GitHub repository

1. Create a new repository on GitHub.
2. Add the curated repository files:
   - `README.md`
   - `LICENSE`
   - `CITATION.cff`
   - `.gitignore`
   - `requirements.txt`
   - `scripts/`
   - `results/`
   - `figures/`
   - `docs/`
3. Commit and push the repository to the default branch.

## 2. Upload the project to GitHub

From the local repository:

```bash
git init
git add .
git commit -m "Initial reproducible research repository"
git branch -M main
git remote add origin https://github.com/<USERNAME>/<REPOSITORY>.git
git push -u origin main
```

## 3. Create a release on GitHub

1. Open the repository main page.
2. Click **Releases**.
3. Click **Draft a new release**.
4. Create or choose a version tag (for example: `v1.0.0`).
5. Add a release title and release notes.
6. Publish the release.

## 4. Connect GitHub with Zenodo

1. Log in to Zenodo.
2. Go to the GitHub integration area in Zenodo.
3. Authorize Zenodo to access your GitHub account if needed.
4. Enable the specific repository you want Zenodo to archive.

## 5. Generate the DOI

After the GitHub release is published and the repository is enabled in Zenodo:

1. Zenodo creates an archived snapshot of that release.
2. Zenodo assigns a DOI to the archived version.
3. Use that DOI in:
   - `CITATION.cff`
   - `README.md`
   - the manuscript's **Code availability** statement

## 6. Update repository metadata after DOI minting

After Zenodo generates the DOI:

1. Replace DOI placeholders in `CITATION.cff`.
2. Update the citation section in `README.md`.
3. Add the Zenodo DOI badge to the GitHub repository if desired.
4. Update the manuscript to cite the archived repository version.

## 7. Recommended citation practice

Cite the archived Zenodo release rather than only the live GitHub repository, because the Zenodo record provides:
- a persistent DOI,
- version-specific archiving,
- and a stable scholarly reference.
