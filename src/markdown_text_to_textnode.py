from textnode import TextNode

def markdown_text_to_textnode (sentence, delimiter, text_type=None):

    if type(sentence) == str:

        valid_delim = {
            '`': 'code',
            '*': 'italic',
            '**': 'bold'
        }

        # Potentially need to wrap around a try block wih a else/finally
        for delim in delimiter:
            if not delim in valid_delim:
                raise Exception(f'{delim} is not a valid markdown syntax. Review your input.')

        # Initial parameters
        sentence = sentence.replace(' ', '| |')
        sentence = sentence.split('|')
        plain_text = ''
        marked_sent_dic = {}
        textnode_list = []
        # remaining_sentence = sentence
        nested_check = False

    for word in sentence:

        if not word.startswith(delimiter): # and not nested_check:
            plain_text += f'{word}'

        if word.startswith(delimiter) and not word.endswith(delimiter):
            textnode_list.append(TextNode(plain_text))
            plain_text = ''
            nested_check = True
            # active_delim = delimiter #Might need
            marked_sent_dic[valid_delim[delimiter]] = word.strip(delimiter)
            
        if not word.startswith(delimiter) and nested_check:
            marked_sent_dic[valid_delim[delimiter]] += word

        if word.endswith(delimiter) and nested_check:
            nested_check = False
            textnode_list.append(TextNode(marked_sent_dic[valid_delim[delimiter]], valid_delim[delimiter]))
            marked_sent_dic = {}

        if word.startswith(delimiter) and word.endswith(delimiter):
            textnode_list.append(TextNode(word.strip(delimiter), valid_delim[delimiter]))

        # if word.startswith(delimiter) and nested_check:
        #     split_delim_to_textnode()

    return textnode_list
