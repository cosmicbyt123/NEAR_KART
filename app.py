from flask import Flask, jsonify,render_template,request,Blueprint

from routes.routes import products_bp

app=Flask(__name__)
app.secret_key = "dev-secret"
app.register_blueprint(products_bp)
if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)

