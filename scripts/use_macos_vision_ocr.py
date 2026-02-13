#!/usr/bin/env python3
"""
Use macOS Vision framework for better OCR accuracy.

This uses Apple's Vision framework which is the same engine used by Preview app.
"""

import sys
from pathlib import Path

try:
    from Cocoa import NSURL, NSImage
    from Vision import VNImageRequestHandler, VNRecognizeTextRequest
    import objc
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False
    print("PyObjC not available. Installing...")
    print("Run: pip install pyobjc-framework-Vision pyobjc-framework-Cocoa")


def extract_text_vision(image_path):
    """Extract text using macOS Vision framework."""
    if not VISION_AVAILABLE:
        return None
    
    try:
        # Load image
        image_url = NSURL.fileURLWithPath_(str(image_path))
        image = NSImage.alloc().initWithContentsOfURL_(image_url)
        
        if not image:
            return None
        
        # Create request handler
        handler = VNImageRequestHandler.alloc().initWithURL_options_(image_url, None)
        
        # Create text recognition request
        request = VNRecognizeTextRequest.alloc().init()
        
        # Use accurate recognition level
        request.setRecognitionLevel_(1)  # 0=fast, 1=accurate
        
        # Perform request
        error = None
        success = handler.performRequests_error_([request], error)
        
        if not success:
            return None
        
        # Extract text from results
        observations = request.results()
        if not observations:
            return None
        
        text_lines = []
        for observation in observations:
            if observation.isKindOfClass_(objc.lookUpClass('VNRecognizedTextObservation')):
                top_candidates = observation.topCandidates_(1)
                if top_candidates:
                    text = top_candidates[0].string()
                    text_lines.append(text)
        
        return '\n'.join(text_lines)
    
    except Exception as e:
        print(f"Vision OCR error: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 use_macos_vision_ocr.py <image_path>")
        sys.exit(1)
    
    image_path = Path(sys.argv[1])
    if not image_path.exists():
        print(f"Image not found: {image_path}")
        sys.exit(1)
    
    text = extract_text_vision(image_path)
    if text:
        print(text)
    else:
        print("Failed to extract text")
