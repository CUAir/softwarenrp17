import io
from flask import Flask, send_file, request, Response, jsonify
app = Flask(__name__)

shape_colors = {}
alpha_colors = {}

@app.route('/next-image',methods=["GET"])
def get_next_image():
    return jsonify({"img_name" : "001"})

@app.route('/get-image/<img_name>',methods=["GET"])
def get_image(img_name):
    return send_file(open("images/{}.jpg".format(img_name), "rb"),
                     attachment_filename="{}.jpg".format(img_name),
                     mimetype='image/jpg')


@app.route('/classify/<img_name>', methods=["POST"])
def classify_image(img_name):
    shape_color = request.args.get("shape_color")
    alpha_color = request.args.get("alpha_color")
    shape_colors[img_name] = shape_color
    alpha_colors[img_name] = alpha_color
    print "Added {}, {} for {}".format(shape_color, alpha_color, img_name)
    return Response("ok", status=201)

if __name__ == "__main__":
    app.run()
