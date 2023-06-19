from rollcall import app, MEMBERS, ALTIDS
import os
import glob
import csv


def setupDirs():
    dataDir = os.path.join(os.getcwd(), 'data')
    app.config['DATA'] = dataDir
    os.makedirs(dataDir, exist_ok=True)
    os.makedirs(os.path.join(dataDir, 'faces'), exist_ok=True)
    return dataDir


def getAllMembers():
    '''Reads all members into a global dictionary
    Output:
        - dictionary of all members, keyed by member ID
        - dictionary of member IDs, keyed by altId
    '''
    global MEMBERS, ALTIDS
    for file in glob.glob(os.path.join(app.config['DATA'], '*.csv')):
        with open(os.path.join(app.config['DATA'], file)) as f:
            reader = csv.DictReader(f, quotechar='"')
            for row in reader:
                id = row['Mem No'].replace('\t', '')
                id = f'{int(id):06d}'
                altId = row['SA Identity No'].replace('\t', '')
                language = row['Language'].replace('\t', '')
                language = language[0:1] if len(language) > 1 else 'A'
                member = {
                    'id': id,
                    'altId': altId,
                    'name': row['Preferred Name'].replace('\t', ''),
                    'surname': row['Surname'].replace('\t', ''),
                    'language': language
                }
                if not id in MEMBERS.keys(): MEMBERS[id] = member
                if not altId in ALTIDS.keys(): ALTIDS[altId] = id


def findMember(member):
    '''Finds a member by id or altId
    Input: a dictionary containing the id or altId
    Output: the member from the global list, if found
    '''
    global MEMBERS, ALTIDS
    altId = member.get('altId') # If the altId is provided...
    id = ALTIDS.get(altId) if altId else member.get('id') # ...lookup the id or get directly
    if not id: return None
    id = f'{int(id):06}'
    m = MEMBERS.get(id)
    return MEMBERS.get(id)
