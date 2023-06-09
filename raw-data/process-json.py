import json
import os
if __name__ == '__main__':
    #find all json files in raw-data directory
    for json_file in os.listdir('./raw-data'):

        # split the filename and extension
        filename, extension = os.path.splitext(json_file)
        layer=filename.split('-')[0]
        type=filename.split('-')[1]
        #create a new directory for each layer
        if not os.path.exists('processed-data/'+layer):
            os.makedirs('processed-data/'+layer)
        if not os.path.exists(f'processed-data/{layer}/{type}'):
            os.makedirs(f'processed-data/{layer}/{type}')
        #read the json file
        with open('raw-data/'+json_file) as f:
            data = json.load(f)
            if type=="locations":
                for item in data:
                    processed_data = []
                    for entry in item['layers']['markers']:
                        #make a new json object with only the fields we need
                        new_entry = {'name':entry['name'],'x':entry['coords'][0],'y':entry['coords'][1],'z':entry['elv'][2]}
                        processed_data.append(new_entry)
                    #write the new json object to a file
                    with open('processed-data/'+layer+'/'+item['name']+'.json', 'w') as outfile:
                        json.dump(processed_data, outfile)
            elif type=="materials":
                for item in data:
                    processed_data = []
                    for entry in item['markerCoords']:
                        #make a new json object with only the fields we need
                        new_entry = {'x':entry[0],'y':entry[1],'z':entry[2]}
                        processed_data.append(new_entry)
                    #write the new json object to a file
                    with open('processed-data/'+layer+'/'+item['name']+'.json', 'w') as outfile:
                        json.dump(processed_data, outfile)
