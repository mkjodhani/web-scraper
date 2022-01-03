from flask import Flask,request,send_file
import shutil, hashlib, os
from scripts.scraper.amazonScraper import Scraper
root = "cache"
if not os.path.isdir(root):
    os.mkdir(root)

app = Flask(__name__)
@app.route("/amazonscraper",methods=['POST'])
def amazonScraper():
    if request.method == 'POST':
        url = "https://www.amazon.in/s?k="
        directory = request.form['directory']
        name = request.form['name']
        maxItems = request.form['maxItems']
        saveType = request.form['saveType']
        outputName = request.form['outputName']
        session_data = f'{directory} {name} {maxItems} {saveType} {outputName}'
        hash = hashlib.sha1(session_data.encode("UTF-8")).hexdigest()
        # shutil.make_archive(output_filename, 'zip', directory)
        os.mkdir(root + "/" + hash)
        directory_name = root + "/" + hash + "/" + directory
        scraper = Scraper(directory_name,url+name.replace(" ", "+"),int(maxItems),int(saveType),outputName)
        dataFrame = scraper.amazonScrapper()
        shutil.make_archive(root+"/downloads/"+ hash,'zip',directory_name.replace(directory_name.split("/")[-1],""))     
        return hash
    else:
        return {"errorCode":"402","message":"GET is not supported"}
    







@app.route('/downloads/<filename>', methods=['GET', 'POST'])
def download(filename):
    return send_file(f'{root}/downloads/{filename}.zip',as_attachment=True)

if __name__ == "__main__":
    app.run()