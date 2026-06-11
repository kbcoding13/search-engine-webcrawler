import nltk
from nltk.corpus import stopwords
import string

# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('punkt_tab')

class Populate:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def tokenize(self, text:str):
        words = nltk.word_tokenize(text)
        filtered_words = [w for w in words if w.lower() not in self.stop_words and w not in string.punctuation]
        return filtered_words
    
pop = Populate()
lip = pop.tokenize("The FitnessGram™ Pacer Test is a multistage aerobic capacity test that progressively gets more difficult as it continues. The 20 meter pacer test will begin in 30 seconds. Line up at the start. The running speed starts slowly, but gets faster each minute after you hear this signal. [beep] A single lap should be completed each time you hear this sound. [ding] Remember to run in a straight line, and run as long as possible. The second time you fail to complete a lap before the sound, your test is over. The test will begin on the word start. On your mark, get ready, start.")
print(lip)