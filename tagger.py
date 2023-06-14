import os
import sys
import argparse

unseen_tag = [1.4166312508853944e-10, 0.13755489460263493, 0.0012749682674599804, 0.002408273268168296, 0.00014166326675166453, 0.035982433914152144, 0.00014166326675166453, 1.4166312508853944e-10, 1.4166312508853944e-10, 0.0016999576427255986, 1.4166312508853944e-10, 0.006658167020824479, 0.0011333051423714408, 0.0025499363932568356, 0.0007083157671058224, 1.4166312508853944e-10, 0.004816546394673466, 0.0032582520186995325, 0.2668933278084714, 0.12678849709590592, 0.16390423586910324, 0.0008499788921943618, 0.0016999576427255986, 0.002974925768522454, 1.4166312508853944e-10, 0.0004249895169287435, 1.4166312508853944e-10, 1.4166312508853944e-10, 0.005241535769939084, 1.4166312508853944e-10, 1.4166312508853944e-10, 1.4166312508853944e-10, 0.0038249045190536903, 0.004108230769230769, 0.0005666526420172829, 1.4166312508853944e-10, 1.4166312508853944e-10, 1.4166312508853944e-10, 0.00014166326675166453, 0.00014166326675166453, 1.4166312508853944e-10, 1.4166312508853944e-10, 0.00028332639184020403, 1.4166312508853944e-10, 1.4166312508853944e-10, 1.4166312508853944e-10, 0.00028332639184020403, 0.00028332639184020403, 0.00014166326675166453, 0.00028332639184020403, 1.4166312508853944e-10, 0.00014166326675166453, 0.0005666526420172829, 0.013882986400339992, 0.036974075789771924, 0.03513245516362091, 0.033857487037824055, 0.025924352032865843, 0.008641450772064031, 0.0004249895169287435, 0.0009916420172829013, 0.0005666526420172829, 0.0014166313925485197, 0.0005666526420172829, 0.008641450772064031, 0.0014166313925485197, 1.4166312508853944e-10, 1.4166312508853944e-10, 1.4166312508853944e-10, 1.4166312508853944e-10, 1.4166312508853944e-10, 0.0022666101430797564, 0.010483071398215044, 0.0007083157671058224, 0.0025499363932568356, 0.0026915995183453747, 0.00014166326675166453, 0.0025499363932568356, 0.00014166326675166453, 0.005524862020116163, 0.002124947017991217, 0.0004249895169287435, 1.4166312508853944e-10, 0.00014166326675166453, 1.4166312508853944e-10, 1.4166312508853944e-10, 0.012324692024366058, 0.006233177645558861, 0.0016999576427255986, 0.0012749682674599804, 0.002408273268168296]

#function to go through trainig1 and makes dictionary of words, then go through training2 and see what words not in the dictionary add to unseen dictionary
def unseen_words(tag_list):
    #use read_training_files to get a list of sentences
    sentence1 , dummy= read_training_files(['training1.txt'])
    sentence2 ,dummy= read_training_files(['training2.txt'])
    #read the first file and add words to dictionary
    seen = {}
    unseen = {}
    total = 0
    for tag in tag_list: 
        seen[tag] = 0
        if tag != 'PUN':
            unseen[tag] = 1e-6
    #setup dictionary for seen words
    for sentence in sentence1:
        for word, pos in sentence:
            if word not in seen:
                seen[word] = 0
    for sentence in sentence2:
        for word, pos in sentence:
            if word not in seen:
                unseen[pos] += 1
                total += 1
    #normalize unseen dictionary
    for tag in unseen:
        unseen[tag] = unseen[tag]/total
    unseen_list = unseen.values()
    return unseen_list


#function that takes the sentences and returnns dictionary with frequency of each pos tag
def tag_count(sentences):
    pos_count = {}
    the_tags = []
    for sentence in sentences:
        index = 0
        for word, pos in sentence:
            if index ==80:
                # print(word)
                pass
            if index not in pos_count:
                pos_count[index] = {pos: 1}
            else:
                if pos not in pos_count[index]:
                    pos_count[index][pos] = 1
                else: 
                    count = pos_count[index][pos]
                    pos_count[index][pos] = count + 1
            index += 1
            if pos not in the_tags:
                the_tags.append(pos)
    most_frequent = {}
    for i in pos_count:
        max_count = 0
        max_pos = ''
        for pos in pos_count[i]:
            if pos =='PUN':
                continue
            if pos_count[i][pos] > max_count:
                max_count = pos_count[i][pos]
                max_pos = pos
        most_frequent[i] = max_pos

    return pos_count, most_frequent, the_tags

# function to read the training file and return a list of the POS tags
def read_tags(training_list_all):
    pos_tags = []
    tags = []
    tag_all = []
    length = 0
    all_len = 0
    for training_list in training_list_all:
        with open(training_list, 'r') as file:
            tags = []
            for line in file:
                if ":" in line:
                    # Remove newline characters and split the line into word and POS tag
                    word, pos = line.strip().split(' : ')
                    # Add the POS tag to the list of POS tags
                    if word in ['.', '!', '?',';']:
                        tags.append(pos) 
                        length += len(tags)
                        if length == 42829:
                            # print(tags)
                            pass
                        pos_tags.append(tags)
                        tags = []
                        tag_all.append(pos)
                        if len(tag_all) != length:
                            # print(tag_all)
                            pass
                        if len(tag_all) == 42830:
                            # print(tag_all)
                            pass
                        
                    else:
                        tags.append(pos)
                        tag_all.append(pos)
                        if len(tag_all) == 42830:
                            # print(tag_all)
                            pass
        if len(tags) != 0:
            pos_tags[-1].extend(tags)            
                        
    return pos_tags, tag_all
#function to read the training files and return a list of sentences
def read_training_files(training_list_all):
    sentences = []
    current_sentence = []
    dummy = []
    count = 0
    for training_list in training_list_all:
        with open(training_list, 'r') as file:
            for line in file:
                if count == 118:
                    # print(line)
                    pass
                if ":" in line :
                # Remove newline characters and split the line into word and POS tag
                    word, pos = line.strip().split(' : ')
                # Check if the word ends a sentence (i.e., it's a period, exclamation mark, or question mark)
                if word in ['.', '!', '?',';']:
                    # Add the word and POS tag to the current sentence
                    current_sentence.append((word, pos))
                    # Add the current sentence to the list of sentences
                    sentences.append(current_sentence)
                    count += 1
                    # Start a new sentence
                    current_sentence = []
                    dummy.append(word)
                else:
                    # Add the word and POS tag to the current sentence
                    current_sentence.append((word, pos))
                    dummy.append(word)
        if len(current_sentence) != 0:
            # Add the current sentence to the list of sentences
            sentences[-1].extend(current_sentence)
    
    return sentences, dummy

# function to read the test file and return a list of sentences
def read_test_file(test_file):
    sentences = []
    current_sentence = []
    dummy = []
    with open(test_file, 'r') as file:
        for line in file:
            # Check if the line is empty
            if line.strip() in ['.', '!', '?',';']:
                # Add the current sentence to the list of sentences
                current_sentence.append(line.strip())
                sentences.append(current_sentence)
                # Start a new sentence
                current_sentence = []
                dummy.append(line.strip())
            else:
                # Add the word to the current sentence
                current_sentence.append(line.strip())
                dummy.append(line.strip())
    if len(current_sentence) != 0:
        # Add the current sentence to the list of sentences
        sentences[-1].extend(current_sentence)

    return sentences, dummy
'''function to go through the file, add words to dictionary and add new dictionary of POS as values to the words in the old dictionary '''
def position_count(files):
    #create a dictionary to store the words and their POS tags
    word_pos = {}
    #read from the file
    for file in files:
        with open(file, 'r') as f:
            for line in f:
                #split the line into word and POS tag
                word, pos = line.strip().split(' : ')
                #if the word is already in the dictionary, add the POS tag to the list of POS tags
                if word in word_pos:
                    #check if the POS tag is already in the list of POS tags
                    if pos not in word_pos.get(word):
                        word_pos[word][pos]=1
                    else:
                        count = word_pos.get(word).get(pos)
                        word_pos[word][pos]=count+1
                #if the word is not in the dictionary, add the word as a key and the POS tag as a value
                else:
                    word_pos[word] = {pos: 1}
    return word_pos

'''function to go though file add words to dictionary and add new dictionary of word as values to the POS in the old dictionary'''
def word_count(sentences):
    #create a dictionary to store the words and their POS tags
    pos_word = {}
    # initialize the dictionary with the POS tags
    #read from the file
    for sent in sentences:
        for line in sent:
            #split the line into word and POS tag
            word, pos = line[0],line[1]
            #if the word is already in the dictionary, add the POS tag to the list of POS tags
            if pos in pos_word:
                #check if the POS tag is already in the list of POS tags
                if word not in pos_word.get(pos):
                    pos_word[pos][word]=1
                else:
                    count = pos_word.get(pos).get(word)
                    pos_word[pos][word]=count+1
            #if the word is not in the dictionary, add the word as a key and the POS tag as a value
            else:
                pos_word[pos] = {word: 1}
    return pos_word

'''function to call position_count and convert the count values to probabilities'''
def emission_probability(sentences):
    pos_count = word_count(sentences)
    for word in pos_count:
        total = sum(pos_count[word].values())
        for pos in pos_count[word]:
            pos_count[word][pos] = pos_count[word][pos]/total
    return pos_count

'''function to take the sentences and return transition probabilities'''
def transition_probabilities(sentences,all_tags):
    transition_counts = {}
    #initialize the transition counts given all all the tags
    for tag in all_tags:
        transition_counts[tag]={}
        for next_tag in all_tags:
            transition_counts[tag][next_tag]=0
    for sentence in sentences:
        # Add start and end tags to sentence
        sentence = [('<s>','<s>')] + sentence + [('<e>','<e>')]
        for i in range(0, len(sentence)-1):
            current_tag = sentence[i][1]
            next_tag = sentence[i+1][1]
            if current_tag not in transition_counts:
                transition_counts[current_tag]={next_tag:1}
            else:
                if next_tag not in transition_counts[current_tag]:
                    transition_counts[current_tag][next_tag]=1
                else:
                    count = transition_counts[current_tag][next_tag]
                    transition_counts[current_tag][next_tag]=count+1
    for tag in transition_counts:
        total = sum(transition_counts[tag].values())
        if total == 0:
            total = 1e-10
        for next_tag in transition_counts[tag]:
            transition_counts[tag][next_tag] = transition_counts[tag][next_tag]/total
    return transition_counts

'''function to take the emission probabilities and a sentence and return a matrix of word and POS tag probabilities'''
''' the keys of the emission probabilities are tags and the values are a dictionary of words and their probabilities'''
def emission_matrix(emission_probs, sentence):
    matrix = {}
    unseen_prob = [1.4166312508853944e-10, 0.13755489460263493, 0.0012749682674599804, 0.002408273268168296, 0.00014166326675166453, 0.035982433914152144, 0.00014166326675166453, 1.4166312508853944e-10, 1.4166312508853944e-10, 0.0016999576427255986, 1.4166312508853944e-10, 0.006658167020824479, 0.0011333051423714408, 0.0025499363932568356, 0.0007083157671058224, 1.4166312508853944e-10, 0.004816546394673466, 0.0032582520186995325, 0.2668933278084714, 0.12678849709590592, 0.16390423586910324, 0.0008499788921943618, 0.0016999576427255986, 0.002974925768522454, 1.4166312508853944e-10, 0.0004249895169287435, 1.4166312508853944e-10, 1.4166312508853944e-10, 0.005241535769939084, 1.4166312508853944e-10, 1.4166312508853944e-10, 1.4166312508853944e-10, 0.0038249045190536903, 0.004108230769230769, 0.0005666526420172829, 1.4166312508853944e-10, 1.4166312508853944e-10, 1.4166312508853944e-10, 0.00014166326675166453, 0.00014166326675166453, 1.4166312508853944e-10, 1.4166312508853944e-10, 0.00028332639184020403, 1.4166312508853944e-10, 1.4166312508853944e-10, 1.4166312508853944e-10, 0.00028332639184020403, 0.00028332639184020403, 0.00014166326675166453, 0.00028332639184020403, 1.4166312508853944e-10, 0.00014166326675166453, 0.0005666526420172829, 0.013882986400339992, 0.036974075789771924, 0.03513245516362091, 0.033857487037824055, 0.025924352032865843, 0.008641450772064031, 0.0004249895169287435, 0.0009916420172829013, 0.0005666526420172829, 0.0014166313925485197, 0.0005666526420172829, 0.008641450772064031, 0.0014166313925485197, 1.4166312508853944e-10, 1.4166312508853944e-10, 1.4166312508853944e-10, 1.4166312508853944e-10, 1.4166312508853944e-10, 0.0022666101430797564, 0.010483071398215044, 0.0007083157671058224, 0.0025499363932568356, 0.0026915995183453747, 0.00014166326675166453, 0.0025499363932568356, 0.00014166326675166453, 0.005524862020116163, 0.002124947017991217, 0.0004249895169287435, 1.4166312508853944e-10, 0.00014166326675166453, 1.4166312508853944e-10, 1.4166312508853944e-10, 0.012324692024366058, 0.006233177645558861, 0.0016999576427255986, 0.0012749682674599804, 0.002408273268168296]
    for sent in sentence:
        for tag in emission_probs.keys():
            for word in emission_probs[tag].keys():
                if word == sent:
                    if word in matrix:
                        matrix[sent][tag] = emission_probs[tag][word]
                    else:
                        matrix[sent] = {tag: emission_probs[tag][word]}
            #if the word never appeared, create a uniform probability across all tags
        if sent not in list(matrix.keys()):
            # tag_counts = {tag: 1 for tag in emission_probs.keys()}
            # tag_prob = {list(emission_probs.keys())[i]:unseen_prob[i] for i in range(len(list(emission_probs.keys())))}
            # matrix[sent] = tag_prob
            tag_counts = {tag: 1 for tag in emission_probs.keys()}
            tag_prob = {tag:1/len(tag_counts) for tag in emission_probs.keys()}
            matrix[sent] = tag_prob

       

    return matrix

'''implement viterbi algorithm'''

def viterbi(sentence, transition_probs, emission_probs,most_frequent):
    # Initialize the matrix
    # print(sentence)
    # sentence = ['<s>'] + sentence + ['<e>']
    matrix = emission_matrix(emission_probs, sentence)
    prob = {}
    total_prob = []
    prev_tag_map = {}
    for tag in matrix[sentence[0]].keys():
        if transition_probs['<s>'][tag] == 0:
            transition_probs['<s>'][tag] = 1e-10
        probability = transition_probs['<s>'][tag] * matrix[sentence[0]][tag]
        prob[tag] = probability
    total_prob.append([prob])

    prev={}
    prev[0]=None

    for i in range(1, len(sentence)):
        prob = {}
        new_prev_tag_map = {}
        prev[i]={}
        for tag in matrix[sentence[i]].keys():
            max_prob = 0
            max_prev_tag = None
            for prev_tag in total_prob[i - 1][0].keys():
                if tag in transition_probs[prev_tag]:
                    if transition_probs[prev_tag][tag] == 0:
                        transition_probs[prev_tag][tag] = 1e-10
                    probability = transition_probs[prev_tag][tag] * matrix[sentence[i]][tag] * total_prob[i - 1][0][prev_tag] #[0] because its in a inner list

                    if probability > max_prob:
                        max_prob = probability
                        prev[i][tag] = prev_tag
            prob[tag] = max_prob
        total_prob.append([prob])



    # Backtrack to get most likely tag sequence
    most_likely_tags = []
    max_prob = 0
    final_tag = None


    # Get final tag with maximum probability
    for tag in total_prob[-1][0]:
        if total_prob[-1][0][tag] > max_prob:
            max_prob = total_prob[-1][0][tag]
            final_tag = tag
    
    
    current_tag = final_tag
    most_likely_tags.insert(0, current_tag)
    # Start backtracking from last tag to first
    for i in range(len(sentence)-1, 0, -1):
       
        if i == 1:
            prev_tag = "<s>"
        else:
            next = prev[i][current_tag]
            # insert
            most_likely_tags.insert(0, next)
            current_tag = prev[i][current_tag]
        
    most_likely_tags.insert(0, current_tag)
    
    return most_likely_tags

#function to read training file and put all the words in one list



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--trainingfiles",
        action="append",
        nargs="+",
        required=True,
        help="The training files."
    )
    parser.add_argument(
        "--testfile",
        type=str,
        required=True,
        help="One test file."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file."
    )
    args = parser.parse_args()

    print(args.trainingfiles[0])
    training_list = args.trainingfiles[0]


    
    # training_list = ['training1.txt']
    # testfile  = 'test2.txt'
    # outputfile = 'output.txt'
    '''print("training files are {}".format(training_list))

    print("test file is {}".format(args.testfile))

    print("output file is {}".format(args.outputfile))


    print("Starting the tagging process.")'''
    #read the training files and put all the words in one list


    the_taggings = ["<s>", "AJ0", "AJC", "AJS", "AT0", "AV0", "AVP", "AVQ", "CJC", "CJS", "CJT",
                    "CRD", "DPS", "DT0", "DTQ", "EX0", "ITJ", "NN0", "NN1", "NN2", "NP0", "ORD", 
                    "PNI", "PNP", "PNQ", "PNX", "POS", "PRF", "PRP", "PUL", "PUN", "PUQ", "PUR",
                    "TO0", "UNC", "VBB", "VBD", "VBG", "VBI", "VBN", "VBZ", "VDB", "VDD", "VDG",
                    "VDI", "VDN", "VDZ", "VHB", "VHD", "VHG", "VHI", "VHN", "VHZ", "VM0", "VVB",
                    "VVD", "VVG", "VVI", "VVN", "VVZ", "XX0", "ZZ0", "AJ0-AV0", "AJ0-VVN", "AJ0-VVD",
                    "AJ0-NN1", "AJ0-VVG", "AVP-PRP", "AVQ-CJS", "CJS-PRP", "CJT-DT0", "CRD-PNI", "NN1-NP0",
                    "NN1-VVB", "NN1-VVG", "NN2-VVZ", "VVD-VVN", "AV0-AJ0", "VVN-AJ0", "VVD-AJ0", "NN1-AJ0",
                    "VVG-AJ0", "PRP-AVP", "CJS-AVQ", "PRP-CJS", "DT0-CJT", "PNI-CRD", "NP0-NN1", "VVB-NN1",
                    "VVG-NN1", "VVZ-NN2", "VVN-VVD"]
   

    # Read the training files
    sentences,dummy = read_training_files(training_list)
    tag_count , tag_freq, the_tag_list = tag_count(sentences)
    pos,train_tags = read_tags(training_list)
    test_sent,test_dummy = read_test_file(args.testfile)
    # test_sent,test_dummy = read_test_file(testfile)
    em_probability = emission_probability(sentences)
    print(len(em_probability))
    tr_prob = transition_probabilities(sentences, the_taggings)
    test = ['and','ray','altered','course','to','sit','opposite','him']
    all_tags = []
    # dumb, truth_tags = read_tags(['training2.txt'])
    # unseen_words(the_taggings)

    # emission_matrix(emission_probability,['turning','off','the','blah'])
    #check to see if number of elements in pos which is a list of lists is is the same as train_tags
    total_elements = 0
    for sublist in pos:
        total_elements += len(sublist)
    if total_elements != len(train_tags):
        print("error")


    i = 0
    length = 0 
    for sent in test_sent:
        tags = viterbi(sent, tr_prob, em_probability,tag_freq)
        all_tags.extend(tags)
        i+=1
       

  

    # check the accuracy
    # count = 0
    # for i in range(len(truth_tags)):
    #         if all_tags[i] == truth_tags[i]:
    #             count = count+1
    # print(count/len(truth_tags))
    # print(count)
    # print(len(truth_tags))
    
    #use the all_tags to write to the output file in format word : tag
    k=0
    with open(args.outputfile,'w') as f:
    # with open(outputfile,'w') as f:
        for i in range(len(test_sent)):
            for j in range(len(test_sent[i])):
                f.write(test_sent[i][j] + ' : ' + all_tags[k] + '\n')
                k+=1


    # test = ['Detective','Chief','Inspector','John','McLeish','gazed','doubtfully','at','the','plate','before','him']
    # test = ['and','the','man','altered','course','to','sit','opposite','him']
