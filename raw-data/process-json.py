import json
import os
if __name__ == '__main__':
    #find all json files in raw-data directory
    for json_file in os.listdir(os.getcwd()):
        if not json_file.endswith('.json'):
            continue
        # split the filename and extension
        print(json_file)
        filename, extension = os.path.splitext(json_file)

        layer=filename.split('-')[0]
        type=filename.split('-')[1]
        #create a new directory for each layer
        if not os.path.exists('processed-data/'+layer):
            os.makedirs('processed-data/'+layer)
        if not os.path.exists(f'processed-data/{layer}/{type}'):
            os.makedirs(f'processed-data/{layer}/{type}')
        #read the json file
        with open(json_file) as f:
            data = json.load(f)
            heights=[]
            if type=="locations":
                for item in data:
                    processed_data = []
                    for entry in item['layers']:
                        for attributes in entry['markers']:
                            #make a new json object with only the fields we need
                            name = attributes['name'] if 'name' in attributes else 'null'
                            new_entry = {'id':attributes['id'], 'name':name,'x':attributes['coords'][1],'y':attributes['coords'][0],'z':attributes['elv']}
                            heights.append(attributes['elv'])
                            processed_data.append(new_entry)
                    #write the new json object to a file
                    with open('processed-data/'+layer+'/'+type+'/'+item['name']+'.json', 'w') as outfile:
                        json.dump(processed_data, outfile)
            elif type=="materials":
                for item in data:
                    processed_data = []
                    for entry in item['markerCoords']:
                        #make a new json object with only the fields we need
                        new_entry = {'x':entry[0],'y':entry[1],'z':entry[2]}
                        heights.append(entry[2])
                        processed_data.append(new_entry)
                    #write the new json object to a file
                    with open('processed-data/'+layer+'/'+type+'/'+item['name']+'.json', 'w') as outfile:
                        json.dump(processed_data, outfile)
            heights.sort()
            print(heights[0],heights[-1])