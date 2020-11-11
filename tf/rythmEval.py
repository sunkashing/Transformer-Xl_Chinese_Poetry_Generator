
import json
import re


def load_rhythm_list():

    with open("平水韵表.txt", encoding="UTF-8") as file:
        rhythm_lines = file.readlines()
    rhythm_dict = dict()
    for rhythm_line in rhythm_lines:
        rhythm_name = re.search(".*(?=[平上去入]声:)", rhythm_line).group() 
        rhythm_tune = re.search("[平上去入](?=声:)", rhythm_line).group() 
        rhythm_characters = re.sub(".*[平上去入]声:", "", rhythm_line)  
        for character in rhythm_characters:
            if character not in rhythm_dict:
                rhythm_dict[character] = list()
            rhythm_dict[character].append([rhythm_name, rhythm_tune])
    return rhythm_dict


RHYTHM_LIST = load_rhythm_list() 


def get_rhythm(character):

    rhythm_set = set()
    if character in RHYTHM_LIST:
        for rhythm_item in RHYTHM_LIST.get(character):
            rhythm_set.add(rhythm_item[0])
        if len(rhythm_set) == 1:
            return list(rhythm_set)[0]
        else:
            return "/".join(list(rhythm_set))
    else:
            return "Special Char"


def get_tone(character):
    """判断字所属的平仄
    若当前字不存在于平水韵表中或为无法确定平仄的多音字时，返回“中”

    :param character: <str> 一个字
    :return: <str> 平/仄/中
    """
    tone_set = set()
    if character in RHYTHM_LIST:
        for rhythm_item in RHYTHM_LIST.get(character):
            tone_set.add(re.sub("[上去入]", "Z", rhythm_item[1]))
        if len(tone_set) == 1:  # 若当前字不是多音字或是平仄相同的多音字
            if (list(tone_set)[0] == "平"):
                return "P"
            return list(tone_set)[0]
        else:
            return "*"
    else:
        return "*"


def inspect_sentence_tone(sentence_tone):
    """
    判断诗句是否为拗句

    :return: <bool> 诗句是否正确, <bool> 是否需要对句救, <str> 诗句情况详细说明
    """
    if re.match("[PZ*]?[P*]?[PZ*][Z*][P*][P*][Z*]", sentence_tone):  # (Z)ZPPZ
        return True, "ZZPPZ", 
    elif re.match("[PZ*]?[Z*]?[PZ*][P*][P*][Z*][Z*]", sentence_tone):  # (P)PPZZ
        return True, "PPPZZ", 
    elif re.match("[PZ*]?[P*]?[PZ*][Z*][Z*][P*][P*]", sentence_tone):  # (Z)ZZPP
        return True, "ZZZPP", 
    elif re.match("[PZ*]?[Z*]?[P*][P*][Z*][Z*][P*]", sentence_tone):  # PPZZP
        return True, "PPZZP", 
    elif re.match("[PZ*]?[P*]?[PZ*][Z*][Z*][P*][Z*]", sentence_tone):  # (Z)ZZPZ
        return True, "ZZPPZ", 
    elif re.match("[PZ*]?[P*]?[PZ*][Z*][PZ*][Z*][Z*]", sentence_tone):  # (Z)Z(P)ZZ
        return True, "ZZPPZ", 
    elif re.match("[PZ*]?[Z*]?[P*][P*][Z*][PZ*][Z*]", sentence_tone):  # PPZ(P)Z
        return True, "PPPZZ",
    elif re.match("[PZ*]?[Z*]?[PZ*][Z*][P*][P*][P*]", sentence_tone):  # (Z)ZPPP
        return True, "ZZZPP", 
    elif re.match("[PZ*]?[Z*]?[Z*][P*][P*][Z*][P*]", sentence_tone):  # ZPPZP
        return True, "PPZZP", 
    elif re.match("[PZ*]?[Z*]?[P*][P*][P*][Z*][P*]", sentence_tone):  # PPPZP
        return True, "PPZZP", 
    else:
        return False, "", "拗句"


def is_tone_same(tone_1, tone_2):
    """
    判断两个字PZ是否相同
    """
    if (tone_1 == "Z" or tone_1 == "*") and (tone_2 == "Z" or tone_2 == "*"):
        return True
    elif (tone_1 == "P" or tone_1 == "*") and (tone_2 == "P" or tone_2 == "*"):
        return True
    else:
        return False


def is_tone_differ(tone_1, tone_2):
    """
    判断两个字PZ是否不同
    :param tone_1:
    :param tone_2:
    :return:
    """
    if (tone_1 == "Z" or tone_1 == "*") and (tone_2 == "P" or tone_2 == "*"):
        return True
    elif (tone_1 == "P" or tone_1 == "*") and (tone_2 == "Z" or tone_2 == "*"):
        return True
    else:
        return False


def inspect_corresponding(first_type, second_type):
    """
    判断句子的对是否正确

    :param first_type: <str> 出句的正格
    :param second_type: <str> 对句的正格
    :return: <bool>
    """
    if len(first_type) != len(second_type):
        return False
    return is_tone_differ(first_type[-2], second_type[-2]) and is_tone_differ(first_type[-1], second_type[-1])


def inspect_sticky(last_second_type, this_first_type):
    """
    判断句子的黏是否正确

    :param last_second_type: <str> 前句对句的正格
    :param this_first_type: <str> 当前出句的正格
    :return: <bool>
    """
    if len(last_second_type) != len(this_first_type):
        return False
    return is_tone_same(last_second_type[-2], this_first_type[-2])


def poem_analyse(title, author, content):
    sentences = [sentence for sentence in re.split("[，。？！]", content) if sentence != ""]
    punctuations = re.findall("[，。？！]", content)
    # check if the poem follow number of characters.
    if len(sentences) != 4 and len(sentences) != 8:
        print("《" + title + "》", author, "诗句句数不是绝句或律诗")
        return False

    # ehck if the sentense follows length constrain
    if not all([len(sentence) == 5 or len(sentence) == 7 for sentence in sentences]):
        print("《" + title + "》", author, "诗文*句子的字数不是五言或七言")
        return False

    # check the Ping Ze evalue.
    sentence_tone_list = list()
    for sentence in sentences:
        sentence_tone_list.append("".join([get_tone(character) for character in sentence]))
    

    # 判断是否押P声韵
    if not all([sentence_tone_list[i][-1] in ["P", "*"] for i in range(len(sentences)) if i % 2 == 1]):
        print("《" + title + "》", author, "诗文没有押韵或押仄声韵")
        return False

    print("《" + title + "》", author)

    last_second_type = ""



    for i in range(int(len(sentences) / 2)):
        first_sentence = sentences[2 * i + 0]  # 出句内容
        second_sentence = sentences[2 * i + 1]  # 对句内容
        print("**********************************")
        print("first_sentence")
        print(first_sentence)
        print("second_sentence")
        print(second_sentence)
        first_tone = sentence_tone_list[2 * i + 0]  # 出句的P仄
        second_tone = sentence_tone_list[2 * i + 1]  # 对句的P仄
        print("tone")
        print(first_tone)
        print(second_tone)
        second_rhythm = "（" + get_rhythm(second_sentence[-1]) + "）"  # 对句的韵脚
        print("second_rhythm")
        print(second_rhythm)
        first_correct, first_type = inspect_sentence_tone(first_tone)
        second_correct, second_type = inspect_sentence_tone(second_tone)
        print("first_correct")
        print(first_correct)
        print("second_correct")
        print(second_correct)
        print("first_type")
        print(first_type)
        print("second_type")
        print(second_type)
        other_analysis = ""
        if first_correct and second_correct:
            if not inspect_corresponding(first_type, second_type):  # 判断是否对
                other_analysis += "【失对】"
            if last_second_type is not None and inspect_sticky(last_second_type, first_type):  # 判断是否黏
                other_analysis += "【失黏】"

        last_second_type = second_type

        output_sentence = first_sentence + punctuations[2 * i + 0] + second_sentence + punctuations[2 * i + 1]  # 第一行输出
        output_analysis = first_tone + "　" + second_tone + second_rhythm  # 第二行输出

        print(output_sentence)
        print(output_analysis)
        print("**********************************")

    return True


if __name__ == "__main__":
    # 载入整理完成的全唐诗文本语料
    with open("全唐诗.json", encoding="UTF-8") as file:
        poem_json = json.loads(file.read())
    for poem_item in poem_json["data"]:

        if poem_analyse(poem_item["title"], poem_item["author"], poem_item["content"].replace("\n", "")):
            print("点击回车继续...")
            input()
