from flask import Flask, request, redirect, jsonify
import boto3
import hashlib
import time
app = Flask(__name__)

REGION = 'us-east-2'
DB_NAME = 'UrlShortenerTable'

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(DB_NAME)

@app.route('/', methods=['GET'])
def landing():
    return f'hi last updated: {time.ctime(time.time())}'

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.json.get('url')
    shortened_url = hashlib.md5(original_url.encode()).hexdigest()[:6]

    table.put_item(Item={'shortId': shortened_url , 'shortUrl': request.url_root+shortened_url, 'originalUrl': original_url, 'createdAt': str(time.time())})
    return jsonify({'short_url': shortened_url})

@app.route('/<short_url>')
def redirect_url(short_url):
    response = table.get_item(Key={'shortId': short_url})
    if 'Item' in response:
        return redirect(response['Item']['originalUrl'])
    return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
