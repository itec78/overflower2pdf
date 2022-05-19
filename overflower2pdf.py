from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from io import BytesIO
from PIL import Image
import os

from fpdf import FPDF

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1000,800")
chrome_options.add_argument("--force-device-scale-factor=2.0")

driver = webdriver.Chrome(options=chrome_options)
os.makedirs('out', exist_ok=True)

for x in range(0, 1000):
    fname = os.path.join("out","flower%s.pdf" % (str(x).zfill(4)))
    print(fname)

    if not os.path.isfile(fname):
        driver.get("https://overflower.bleeptrack.de/?singleImg=free&lineart")
        png = driver.get_screenshot_as_png() # saves screenshot of entire page
        im = Image.open(BytesIO(png)) # uses PIL library to open image in memory

        #crop the image
        l=600
        cx = 900
        cy = 900

        left = cx -l
        top = cy -l
        right = left + (2*l)
        bottom = top + (2*l)

        im = im.crop((left, top, right, bottom)) # defines crop points
        im.save("/tmp/flower.png") # saves new cropped image

        # Compose the page
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()

        w = 180
        pdf.image("/tmp/flower.png",w=w, x=(210-w)/2, y=20)

        w = 180
        pdf.set_xy((210-w)/2, 275)
        pdf.set_font('Times', '', 16)
        pdf.set_text_color(68, 68, 68)
        pdf.cell(w=w, align='C', txt="Overflower by bleeptrack - https://bleeptrack.de/projects/overflower/", border=0)

        pdf.output(fname,'F')
