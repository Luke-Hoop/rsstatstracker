import requests
import matplotlib.pyplot as plt
import json
from django.http import JsonResponse, HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg

def api_request(request, username):
    api_url = f"https://api.wiseoldman.net/v2/players/{username}"
    headers = {
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        json_string = json.dumps(data)
        data = json.loads(json_string)

        skillData = data['latestSnapshot']['data']['skills']
        levelData = []
        for key, skill in skillData.items():
            for key, value in skill.items():
                if(key == 'metric'):
                    stat = value
                if(key == 'level'):
                    level = value
            if(stat != 'overall'):
                levelData.append([stat, level])
            
        return json.dumps(levelData)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)})

def process_data(request, username):
    json_data = api_request(request, username)
    data = json.loads(json_data)
    x_values = [item[0] for item in data]
    y_values = [item[1] for item in data]

    plt.bar(x_values, y_values, label=username)
    plt.xticks(rotation=45, horizontalalignment='right')
    plt.xlabel('Stat')
    plt.ylabel('Level')
    plt.title('OSRS Levels')
    plt.tight_layout()
    plt.legend()

    canvas = FigureCanvasAgg(plt.gcf())
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)

    return response

