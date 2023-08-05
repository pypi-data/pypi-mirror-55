tessy
=====

__tessy__ is a Python wrapper for 
[Google's Tesseract-OCR](https://github.com/tesseract-ocr/tesseract), 
an optical character recognition engine used to *detect and extract* text data from 
various image file formats.


## Features

- No initial dependencies beside [Tesseract](https://github.com/tesseract-ocr/tesseract).
- Supports input image in `PNG`, `JPG`, `JPEG`, `GIF`, `TIF` and `BMP` format.
- Supports multiple input images via text file *(.txt)*.
- Supports image objects from: 
  * [Pillow](https://github.com/python-pillow/Pillow) *(Image)*
  * [wxPython](https://github.com/wxWidgets/wxPython) *(wx.Image)*
  * [PyQt4](https://www.riverbankcomputing.com/software/pyqt/download)/
    [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5)/
    [PySide](https://github.com/pyside/pyside-setup) *(QImage)*
  * [OpenCV](https://github.com/skvark/opencv-python) *(ndarray)*
- Dynamically detect and import the corresponding image module on runtime.
- Supports `txt`, `box`, `pdf`, `hocr`, `tsv` and `osd` as output file format.
- Supports multiple output format.
- Can convert any raw output data to `string`, `bytes` or `dict` *(except pdf)*.
- Works on macOS, Linux and Windows.
- Well [documented](https://github.com/k4rian/tessy#api).