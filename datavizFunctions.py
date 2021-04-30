import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import preprocessing

df = preprocessing.df


def createWordCloud(company_number, image_number):
    font_path = './Sigmar_One/SigmarOne-Regular.ttf'
    mask_path = './imageonline-co-textimage2.png'
    mask = np.array(Image.open(mask_path))
    text = df['Job Description'][company_number]
    company = df["Company Name"][company_number]
    wordcloud = WordCloud(width=1000, height=500, background_color='White', contour_width=3, contour_color='black',
                          stopwords=STOPWORDS, font_path=font_path, mask=mask).generate(text)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.title(company)
    plt.savefig(f'./assets/wordcloud{image_number}.png')
    return company, wordcloud


def create_TopNFeatures(company, n_features):
    text = df['Job Description'][int(company):int(company) + 1]
    vectoriser = TfidfVectorizer(stop_words='english')
    model = vectoriser.fit_transform(text)
    indices = np.argsort(vectoriser.idf_)[::-1]
    keywords = vectoriser.get_feature_names()
    top_n_features = [keywords[i] for i in indices[:n_features]]
    return top_n_features
