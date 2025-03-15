# Sheet Music Reader

A web application that reads sheet music from PDF files and displays detected notes alongside an alto saxophone fingering chart.

## Features

- PDF file upload with drag-and-drop support
- Real-time PDF preview using PDF.js
- Automatic note detection from sheet music using Audiveris OMR (Optical Music Recognition)

## Requirements

- Python 3.8 or higher
- Flask
- pdf2image (for converting PDFs to images)
- OpenCV (for image processing)
- NumPy (for numerical operations)
- music21 (for music notation processing)
- Java 11 or higher (required for Audiveris)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sheet-music-reader.git
cd sheet-music-reader
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Java:
   Download and install Java 11 or higher from https://adoptium.net/


4. Verify Java installation:
```bash
java -version
```

Note: Audiveris is included in the repository under the `Audiveris` directory. The application will automatically use this version.

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Upload a PDF file containing sheet music by dragging and dropping it into the upload area or clicking to select a file

4. The application will:
   - Display a preview of the sheet music
   - Process the image using Audiveris OMR to detect musical notes
   - Show the detected notes below the preview
   - Display the alto saxophone fingering chart for reference

## How It Works

### PDF Preview
- Uses PDF.js to render the first page of the uploaded PDF
- Displays the sheet music in a clean, readable format

### Note Detection Process
1. The PDF is converted to an image using pdf2image
2. OpenCV is used to preprocess the image (grayscale, thresholding, etc.)
3. Audiveris OMR analyzes the preprocessed image to identify musical notes
4. The detected notes are extracted from the generated MusicXML file
5. Notes are filtered and displayed in a grid layout

### Fingering Chart
- Shows a comprehensive alto saxophone fingering chart
- Stays visible while scrolling through the sheet music
- Helps users identify the correct fingerings for detected notes

## Troubleshooting

### PDF Preview Issues
- Ensure the PDF file is not corrupted
- Try refreshing the page if the preview doesn't load
- Check browser console for any JavaScript errors

### Note Detection Problems
- Make sure the sheet music is clear and well-scanned
- Verify that Java 11 or higher is installed and accessible
- Check if the Audiveris directory is present in the project root
- Ensure you have sufficient permissions to execute the Audiveris batch file

## License

This project is licensed under the MIT License - see the LICENSE file for details. 