import json

def create_stats():
    with open("stats.json",'w') as f:
        data = {'damage_dealt': 0,
                'damage_taken': 0,
                'waves_completed': 0
                 
                 }
        json.dump(data, f)


def update_stats(parameter, amount):
    with open('stats.json','r') as f:
        data = json.load(f)
        data[parameter] += amount
    with open('stats.json','w') as f:
        json.dump(data, f)

def disp_stats():
    with open('stats.json','r') as f:
        data = json.load(f)
        a = data['damage_dealt']
        b = data['damage_taken']
        c = data['waves_completed']

        string = "Damage Dealt: " + str(a) + "\nDamage Taken: " + str(b) + "\nWaves Completed: " + str(c)
        

    return string

