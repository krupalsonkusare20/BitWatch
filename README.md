# BitWatch — Error Detection and Correction Simulator

BitWatch is an interactive learning website for understanding error detection and correction in computer networks.

## Features

- Learn about **Parity**, **Checksum**, **CRC**, and **Hamming (7,4)** codes.
- Explore worked examples, notes, and real-world applications.
- Interact with the simulator by flipping received bits and observing whether an error is detected, missed, or corrected.
- Try short knowledge-check quizzes.
- Open linked learning videos and reference notes.

## Technologies

- HTML
- CSS
- JavaScript

The current version is a self-contained web app: its styling and JavaScript are included in `index.html`. No build step or package installation is required.

## Run locally

1. Download or clone this repository.
2. Open `index.html` in a modern web browser.
3. Navigate to **Simulator** or open a lesson and select **Try it**.

Some fonts are loaded from Google Fonts, and video/reference links require an internet connection. The core website and simulator run in the browser.

## Publish with GitHub Pages

1. Create a GitHub repository, for example `BitWatch`.
2. Upload `index.html` and `README.md` to the repository's **root** directory.
3. Open the repository's **Settings**.
4. Select **Pages** in the sidebar.
5. Under **Build and deployment**, choose **Deploy from a branch**.
6. Select branch `main` and folder `/(root)`, then save.
7. Wait for the deployment to finish. GitHub will show the public website URL in the Pages section.

Anyone with the published URL can open and use the simulator in their browser; they do not need to download the source code.

## Repository structure

```text
BitWatch/
├── index.html
└── README.md
```

## Notes

- This project is a browser-based educational simulator, not a server-backed application.
- If you later split the CSS or JavaScript into separate files, update the HTML references and upload those files too.
- Add screenshots to the repository if you want to showcase the interface on the GitHub project page.
