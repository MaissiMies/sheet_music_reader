import os
import subprocess
import xml.etree.ElementTree as ET
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from PIL import Image
from music21 import *
import glob
import pdf2image
import tempfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max file size for PDFs
ALLOWED_EXTENSIONS = {'pdf'}

# Update path to point to the Audiveris batch file
AUDIVERIS_PATH = os.path.join(os.path.dirname(__file__), 'Audiveris', 'bin', 'Audiveris.bat')
if not os.path.exists(AUDIVERIS_PATH):
    # Fallback to environment variable if not found in project directory
    AUDIVERIS_PATH = os.getenv('AUDIVERIS_PATH', AUDIVERIS_PATH)

# Path to local poppler installation
POPPLER_PATH = os.path.join(os.path.dirname(__file__), 'poppler-24.08.0', 'Library', 'bin')
if not os.path.exists(POPPLER_PATH):
    print(f"Warning: Poppler not found at {POPPLER_PATH}. Please ensure poppler is installed correctly.")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_pdf_to_images(pdf_path):
    """Convert PDF file to a list of images."""
    try:
        # Convert PDF to images using local poppler installation
        images = pdf2image.convert_from_path(
            pdf_path,
            dpi=300,  # Higher DPI for better quality
            fmt='png',
            poppler_path=POPPLER_PATH,  # Specify the path to poppler
            use_pdftocairo=True,  # Use pdftocairo for better quality
            grayscale=False,  # Keep color
            size=(None, None),  # Maintain original size
            thread_count=2,  # Use multiple threads for faster processing
            use_cropbox=True,  # Use cropbox for better page detection
            strict=False  # Be more lenient with PDF parsing
        )
        
        # Save images to temporary files
        image_paths = []
        for i, image in enumerate(images):
            temp_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                f"temp_page_{i}.png"
            )
            # Save with high quality
            image.save(temp_path, 'PNG', quality=100, optimize=False)
            image_paths.append(temp_path)
            print(f"Saved page {i+1} to {temp_path}")
        
        return image_paths
    except Exception as e:
        print(f"Error converting PDF: {str(e)}")
        raise Exception(f"Failed to convert PDF: {str(e)}")

def process_sheet_music(file_path):
    try:
        # Create output directory for Audiveris
        output_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        print("Converting PDF to images...")
        image_paths = convert_pdf_to_images(file_path)
        print(f"Converted PDF to {len(image_paths)} images")
        
        all_notes = []
        
        # Process each image
        for img_path in image_paths:
            print(f"Processing image: {img_path}")
            print(f"Output directory: {output_dir}")
            
            # Verify image exists and is readable
            if not os.path.exists(img_path):
                raise Exception(f"Image file not found: {img_path}")
            
            # Run Audiveris OMR using the batch file with more verbose output
            cmd = [
                AUDIVERIS_PATH,
                '-batch',
                '-export',
                '-option', 'org.audiveris.omr.sheet.Picture.maxWH=4000',
                '-option', 'org.audiveris.omr.sheet.Scale.minInterline=12',
                '-output', output_dir,
                img_path
            ]
            
            print(f"Running command: {' '.join(cmd)}")
            
            process = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            print(f"Process stdout: {process.stdout}")
            print(f"Process stderr: {process.stderr}")
            
            if process.returncode != 0:
                raise Exception(f"Audiveris failed: {process.stderr}")
            
            # List all files in output directory
            print("Files in output directory:")
            for file in os.listdir(output_dir):
                print(f"- {file}")
            
            # Try to find any generated files
            base_name = os.path.splitext(os.path.basename(img_path))[0]
            possible_extensions = ['.mxl', '.xml', '.musicxml']
            xml_path = None
            
            for ext in possible_extensions:
                test_path = os.path.join(output_dir, base_name + ext)
                if os.path.exists(test_path):
                    xml_path = test_path
                    print(f"Found output file: {xml_path}")
                    break
            
            if not xml_path:
                # Try searching for any XML files
                xml_files = glob.glob(os.path.join(output_dir, '*.xml')) + \
                           glob.glob(os.path.join(output_dir, '*.mxl')) + \
                           glob.glob(os.path.join(output_dir, '*.musicxml'))
                
                if xml_files:
                    xml_path = xml_files[0]
                    print(f"Found alternative output file: {xml_path}")
                else:
                    raise Exception("No MusicXML file generated. Check if the image contains readable sheet music.")
            
            # Parse the MusicXML file using music21
            print(f"Parsing MusicXML file: {xml_path}")
            score = converter.parse(xml_path)
            page_notes = []
            
            # Extract notes from the score
            for element in score.recurse():
                if isinstance(element, note.Note):
                    # Get the note name without octave number
                    note_name = element.name
                    page_notes.append(note_name)
                elif isinstance(element, chord.Chord):
                    # For chords, get all note names
                    for pitch in element.pitches:
                        note_name = pitch.name
                        page_notes.append(note_name)
            
            print(f"Extracted notes from page: {page_notes}")
            all_notes.extend(page_notes)
            
            # Clean up temporary files
            try:
                os.remove(xml_path)
                os.remove(img_path)  # Clean up temporary image
            except Exception as e:
                print(f"Warning: Error during cleanup: {str(e)}")
        
        # Final cleanup
        try:
            if os.path.exists(output_dir):
                for file in os.listdir(output_dir):
                    os.remove(os.path.join(output_dir, file))
                os.rmdir(output_dir)
        except Exception as e:
            print(f"Warning: Error during final cleanup: {str(e)}")
        
        return all_notes
    except Exception as e:
        print(f"Error in process_sheet_music: {str(e)}")
        raise Exception(f"Failed to process sheet music: {str(e)}")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            notes = process_sheet_music(filepath)
            os.remove(filepath)  # Clean up the uploaded file
            return jsonify({
                'notes': notes
            })
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type. Only PDF files are supported.'}), 400

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Verify Audiveris installation
    if not os.path.exists(AUDIVERIS_PATH):
        print("Warning: Audiveris not found at specified path. Please set AUDIVERIS_PATH environment variable.")
    
    app.run(debug=True) 