# Promo Code Bot [PCB]

PCB is a bot used for copying any kind of promotion codes from a Twitter account and pasting it on a website.

## Configuration

Configuration step by step:
1. Run 'setup.py' & fill out the necessary boxes.
2. Install Tesseract OCR. To do that: (only for PCB v2)
   - On Windows: Download the installer from the official Tesseract repository on GitHub (https://github.com/UB-Mannheim/tesseract/wiki) and run it.
   - On macOS: Install Tesseract using Homebrew by running the command brew install tesseract.
   - On Linux: Use the package manager specific to your distribution. On Ubuntu, you can install Tesseract by running sudo apt-get install tesseract-ocr.


3. Make sure that you have downloaded all these libraries:
   - Tweepy
   - Pynput
   - PyperClip
   - Pytz
   - Kivy
   - Pytesseract (PCB v2)
   - PIL (PCB v2)


   To install a Python library, use the following command:
<pre>
pip install library_name
</pre>
   
4. The program should be ready to run.

## Usage

After configuration,PCB.py should display the following message:"code is now running..."; 
if that happens you should select the input box you want the code to be entered in and wait
until the program pastes the promotion code in the input box.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

