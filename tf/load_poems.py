import json
import glob
import os
project_root = 'drive/My Drive/11785 Team Project/'
poem_root = os.path.join(project_root, 'chinese-poetry/json')
strain_root = os.path.join(project_root, 'chinese-poetry/strains/json')
poems_tsv = os.path.join(project_root, 'poems.tsv')

def parse_json():
    tang_poem_json = sorted(glob.glob(os.path.join(poem_root, 'poet.tang.[0-9]*.json')))
    tang_strain_json = sorted(glob.glob(os.path.join(strain_root, 'poet.tang.[0-9]*.json')))
    song_poem_json = sorted(glob.glob(os.path.join(poem_root, 'poet.song.[0-9]*.json')))
    song_strain_json = sorted(glob.glob(os.path.join(strain_root, 'poet.song.[0-9]*.json')))
    
    with open(poems_tsv, 'w') as w:
        w.write('Title\tDynasty\tType\tContent\tStrain\n')
        parse_poems_strains(w, tang_poem_json, tang_strain_json, 'Tang')
        parse_poems_strains(w, song_poem_json, song_strain_json, 'Song')

def parse_poems_strains(w, poem_json, strain_json, dynasty):
    # iterate every json file
    for i in range(len(poem_json)):
        poems = poem_json[i]
        strains = strain_json[i]
        # open one poem and strain json file
        with open(strains, 'r') as f_s:
            with open(poems, 'r') as f_p:
                str_data_p = f_p.read()
                str_data_s = f_s.read()
                dict_data_p = json.loads(str_data_p)
                dict_data_s = json.loads(str_data_s)
                # iterate every poem in a json file
                for j in range(len(dict_data_p)):
                    # iterate every line in a poem
                    parsed_poem = parse_poem(dict_data_p[j], dynasty)
                    if parsed_poem != '':
                        parsed_strain = parse_strain(dict_data_s[j])
                        w.write(parsed_poem + parsed_strain + '\n')

def parse_strain(strain):
    res = ''
    content = strain['strains']
    for i in range(len(content)):
        res += content[i]
    return res

def parse_poem(poem, dynasty):
    res = ''
    content = poem['paragraphs']

    # jueju_5 has 2 sentences and length 12 if plus comma and period each sentence
    # jueju_7 has 2 sentences and length 16 if plus comma and period each sentence
    if (len(content) != 2 or len(content[0]) != 12 or len(content[1]) != 12) and (len(content) != 2 or len(content[0]) != 16 or len(content[1]) != 16):
        return res
    
    res += poem['title']
    res += '\t'

    if dynasty == 'Tang':
        res += '唐\t'
    elif dynasty == 'Song':
        res += '宋\t'

    if (len(content[0]) == 12):
        res += '五言绝句\t'
    elif (len(content[0]) == 16):
        res += '七言绝句\t'

    # res += '【'
    for i in range(len(content)):
        res += content[i]
    # res += '】'
    res += '\t'
    
    return res