import spacy
import re
from cleantext import clean

model = spacy.load('nl_core_news_sm')

def clean_text(text, lower=False, to_ascii=True, no_currency_symbols=False, fix_unicode=True, sentence_tokenize=True, no_emails=False, no_phone_numbers=False, no_urls=False):
        clean(text,
              fix_unicode=fix_unicode,               # fix various unicode errors
              to_ascii=to_ascii,                  # transliterate to closest ASCII representation
              lower=lower,                     # lowercase text
              no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
              no_urls=no_urls,                  # replace all URLs with a special token
              no_emails=no_emails,                # replace all email addresses with a special token
              no_phone_numbers=no_phone_numbers,         # replace all phone numbers with a special token
              no_numbers=False,               # replace all numbers with a special token
              no_digits=False,                # replace all digits with a special token
              no_currency_symbols=no_currency_symbols,      # replace all currency symbols with a special token
              no_punct=False,                 # fully remove punctuation
              replace_with_url="<URL>",
              replace_with_email="<EMAIL>",
              replace_with_phone_number="<PHONE>",
              replace_with_number="<NUMBER>",
              replace_with_digit="0",
              replace_with_currency_symbol="<CUR>",
             )
        
        text = text.replace(' =','.')
        text = text.replace('= ','.')
        text = text.replace('=','.')
        text = text.replace('&nbsp;','')
        to_remove = "_.-()"
        pattern = "(?P<char>[" + re.escape(to_remove) + "])(?P=char)+"

        text = ' '.join(text.split())
        # text = re.sub(r"[-()\"#/@;:<>{}=~|.?,]", "", text)
        text = re.sub(pattern, r"\1", text)
        text = re.sub(r"[\"#/@;:<>{}=~|?^$]", "", text)
        text = text.replace(' .',' ')
        
        if sentence_tokenize:
            temp_text = ''
            sentences = []
            doc = model(text)
            for i, token in enumerate(doc.sents):
                temp_text = temp_text + token.text
                sentences.append(token.text)
            text = temp_text
            
        return text, (sentences if sentence_tokenize else None) 