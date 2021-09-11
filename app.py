from flask import Flask, render_template,redirect
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/<user_id>')
def show_menu(user_id):
    # show all memories to users
    return render_template('user.html', user_id=user_id)    

@app.route('/<user_id>/photo/<asset_id>')
def show_photo(user_id, asset_id):
    # Get the description of the photo
    filename='static/'+ user_id + '/photos/' + asset_id + '.txt'
    print(filename)
    description=''
    if os.path.isfile(filename):
        with open(filename, "r") as file:
            description = file.readline()

    # show a specific photo to a user
    return render_template('photo.html', user_id=user_id, asset_id=asset_id, 
        description=description)

@app.route('/<user_id>/delete/photo/<asset_id>')
def delete_photo(user_id, asset_id):
    # delete photo
    filename_photo = 'static/'+user_id+'/photos/'+asset_id+'.jpg'
    if os.path.exists(filename_photo):
        ## Try to delete the file ##
        try:
            os.remove(filename_photo)
        except OSError as e:  ## if failed, report it back to the user ##
            print("Error: %s - %s." % (e.filename_photo, e.strerror))
    else:
        print("The file does not exist") 

    # delete photo description
    filename_photo_desc = 'static/'+user_id+'/photos/'+asset_id+'.txt'
    if os.path.exists(filename_photo_desc):
        ## Try to delete the file ##
        try:
            os.remove(filename_photo_desc)
        except OSError as e:  ## if failed, report it back to the user ##
            print("Error: %s - %s." % (e.filename_photo_desc, e.strerror))
    else:
        print("The file does not exist") 

    return render_template('success.html', user_id=user_id)
    #return redirect("/photos/"+user_id, code=302)

@app.route('/<user_id>/carousel')
def show_carousel(user_id):
    
    files = get_files(user_id, '/photos')

    # show the user profile for that user
    return render_template('carousel.html', user_id=user_id, photos=files)

@app.route('/<user_id>/photos')
def show_thumbnails(user_id):
    
    files = get_files(user_id, '/photos')

    # create photos dictionary {photo_id, photo_description}
    photos = {}
    for f in files: 
        photos[f]=""

    get_photo_descriptions(user_id, '/photos', photos)

    return render_template('photo_cards.html', user_id=user_id, photos=photos)

@app.route('/<user_id>/voice/<asset_id>')
def show_voice(user_id, asset_id):
    # show the voice message for that user
    return render_template('voice.html', user_id=user_id, asset_id=asset_id)

@app.route('/<user_id>/delete/voice/<asset_id>')
def delete_voice(user_id, asset_id):
    # delete photo
    filename = 'static/'+user_id+'/voices/'+asset_id+'.ogg'
    if os.path.exists(filename):
        ## Try to delete the file ##
        try:
            os.remove(filename)
        except OSError as e:  ## if failed, report it back to the user ##
            print("Error: %s - %s." % (e.filename, e.strerror))
    else:
        print("The file does not exist") 

    return render_template('success.html', user_id=user_id)
    #return redirect("/photos/"+user_id, code=302)

@app.route('/<user_id>/voices')
def show_voices(user_id):
    files = get_files(user_id, '/voices')

    # show the voice messages for that user
    return render_template('voices.html', user_id=user_id, voices=files)

@app.route('/<user_id>/message/<asset_id>')
def show_message(user_id, asset_id):
    # get messages from file
    messages_file = 'static/' + user_id + '/messages.txt'
    with open(messages_file) as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content] 

    # show all messages for the user
    return render_template('messages.html', user_id=user_id, messages=content)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

def get_files(user_id, type):
    # get user photos
    mypath='static/'+ user_id + type
    Path(mypath).mkdir(parents=True, exist_ok=True)
    files = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".jpg")]
    # order files
    files.sort(key=lambda x: os.path.getmtime(mypath + '/' + x))

    # get just file names
    filenames = [os.path.splitext(x)[0] for x in files] 

    return filenames

def get_photo_descriptions(user_id, type, photos_dict):
    mypath='static/'+ user_id + type

    files = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".txt")]
    # order files
    files.sort(key=lambda x: os.path.getmtime(mypath + '/' + x))
    
    for filename in files:
        with open(mypath + '/' + filename, "r") as file:
            filename_without_ext=os.path.splitext(filename)[0]
            photos_dict[filename_without_ext]=file.read()


if __name__ == '__main__':
    app.run(debug=True)