# Sheet Music Reader

A web application that reads sheet music from PDF files and displays detected notes alongside an alto saxophone fingering chart.

## Features

- PDF file upload with drag-and-drop support
- Real-time PDF preview using PDF.js
- Automatic note detection from sheet music
- Interactive alto saxophone fingering chart
- Responsive layout optimized for 1920x1080 displays
- Clean, modern user interface

## Requirements

- Python 3.7+
- Flask
- pdf2image
- pytesseract
- OpenCV (cv2)
- NumPy

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sheet-music-reader.git
cd sheet-music-reader
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Install Tesseract OCR:
- Windows: Download and install from https://github.com/UB-Mannheim/tesseract/wiki
- Linux: `sudo apt-get install tesseract-ocr`
- macOS: `brew install tesseract`

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Upload a PDF file containing sheet music:
   - Drag and drop the file into the upload area
   - Or click the upload area to select a file

4. The application will:
   - Display a preview of the PDF
   - Process the sheet music to detect notes
   - Show the detected notes in a grid layout
   - Display the alto saxophone fingering chart for reference

## Project Structure

```
sheet_music_reader/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── static/            # Static files
│   └── Fingering_Chart.jpg
└── templates/         # HTML templates
    └── index.html     # Main application template
```

## Features in Detail

### PDF Preview
- Uses PDF.js for client-side PDF rendering
- Shows the first page of the uploaded PDF
- Maintains aspect ratio and quality

### Note Detection
- Processes PDF files to extract sheet music
- Identifies musical notes using OCR
- Displays notes in a clean, grid-based layout

### Fingering Chart
- Shows alto saxophone fingering positions
- Sticky positioning for easy reference
- Optimized size for 1920x1080 displays

## Troubleshooting

1. If the PDF preview doesn't show up:
   - Ensure the PDF file is not corrupted
   - Check browser console for any JavaScript errors
   - Try refreshing the page

2. If notes are not detected:
   - Ensure the PDF contains clear, readable sheet music
   - Check if Tesseract OCR is properly installed
   - Verify the PDF file permissions

3. If the layout appears broken:
   - Ensure your browser is up to date
   - Try clearing browser cache
   - Check if you're using a supported browser (Chrome, Firefox, Edge)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 