import numpy as np
import pandas as pd
import nltk
from unidecode import unidecode
from nltk.tokenize import RegexpTokenizer
nltk.download('stopwords')
from nltk.corpus import stopwords
sw_nltk = stopwords.words('spanish') + ["usted", "ustedes"]
sw_nltk = list(map(lambda x: unidecode(x), sw_nltk))

# TODO: ignorar enlaces (http:// https://)
# TODO: ignorar <Multimedia omitido>
# TODO: ver que hacer con los emojis
# TODO: ver que hacer con el código de programación enviado por whatsapp
# TODO: ignorar numeros
# TODO: ignorar JAJAJAJA jajajajaj hahahaha ejeje uyyy uffff mmmmmmm

data = [
    {
        "date": "2020-01-01",
        "text": """
            El hijo de rana, Rinrín renacuajo
            Salió esta mañana muy tieso y muy majo
            Con pantalón corto, corbata a la moda
            Sombrero encintado y chupa de boda.
            -¡Muchacho, no salgas!- le grita mamá
            pero él hace un gesto y orondo se va.
        """
    },
    {
        "date": "2020-01-02",
        "text": """
            Halló en el camino, a un ratón vecino
            Y le dijo: -¡amigo!- venga usted conmigo,
            Visitemos juntos a doña ratona
            Y habrá francachela y habrá comilona.
            A poco llegaron, y avanza ratón,
            Estírase el cuello, coge el aldabón,
            Da dos o tres golpes, preguntan: ¿quién es?
            -Yo doña ratona, beso a usted los pies
            ¿Está usted en casa? -Sí señor sí estoy,
            y celebro mucho ver a ustedes hoy;
        """
    },
    {
        "date": "2020-01-03",
        "text": """
            estaba en mi oficio, hilando algodón,
            pero eso no importa; bienvenidos son.
            Se hicieron la venia, se dieron la mano,
            Y dice Ratico, que es más veterano:
            Mi amigo el de verde rabia de calor,
            Démele cerveza, hágame el favor.
        """
    },
]

class Solver:
    def __init__(self, df):
        self.df = df
        self.words_count = {}

    def proccess_row(self, paragraph):
        tokenizer = RegexpTokenizer(r'\w+')
        paragraph = unidecode(paragraph.lower())
        paragraph = tokenizer.tokenize(paragraph)
        paragraph = [word for word in paragraph if word not in sw_nltk]
        return paragraph

    def count_words(self, paragraph):
        for word in paragraph:
            try:
                self.words_count[word] += 1
            except KeyError:
                self.words_count[word] = 1
    
    def run(self):
        for (text,) in zip(self.df["text"]):
            paragraph = self.proccess_row(text)
            self.count_words(paragraph)
        return self.words_count
    
df = pd.DataFrame(data)
result = Solver(df).run()

count = pd.DataFrame.from_dict(result, orient='index', columns=['count']).reset_index()
count.columns = ['word', 'count']
count = count.sort_values('count')
print(count)

