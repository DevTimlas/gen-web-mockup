from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from flask_cors import CORS
import traceback

app = Flask(__name__)
CORS(app)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def gen_img(prompt, num_g=1):
    fin_res = {}
    for i in range(num_g):
        response = client.images.generate(
          model="dall-e-3",
          prompt=prompt,
          size="1024x1024",
          quality="standard",
          n=1,
        )
        
        image_url = response.data[0].url
        fin_res.update({f"img_{i}": image_url})
    return fin_res

def gen_img_old(prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    
    image_data = response.data[0]
    image_url = image_data.url
    return image_url

@app.route('/generate_image_url', methods=['POST'])
def generate_image_url():
    data = request.json
    prompt = data.get('prompt')
    num_g = int(data.get('n'))
    # print(prompt)

    if not prompt:
        return jsonify({'error': 'Prompt not provided'}), 400

    try:
        image_url = gen_img(prompt, num_g)
        return jsonify({'generates': image_url})
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
