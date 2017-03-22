try:
    from imgloader import imgloader
except ImportError:
    from fileops.imgloader import imgloader
try:
    from processor.ocr import OCR
except  ImportError:
    from fileops.processor.ocr import OCR
try:
    from getfilename import getFileName
except ImportError:
    from fileops.getfilename import getFileName