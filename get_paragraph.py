import Wikipedia

from nltk.stem.snowball import SnowballStemmer
import spacy

stemmer = SnowballStemmer(language='english')
nlp = spacy.load("en_core_web_sm")

with open('StopWords.txt', 'r') as f:
    stop_words = [line for line in f.read().splitlines() if line != '']

def get_top_categories(article_title):
    with open(f'metricOutput/{article_title}metricOutput.txt', 'r') as f:
        top_categories = [' '.join(line.split()[1:-1]) for line in f.read().splitlines()[9:14]]
        return top_categories

def get_paragraph_from_category(article_title, category):
    article = Wikipedia.getPlainArticle(article_title)
    paragraphs = [para for para in article.split('\n\n')]
    # Remove 'Category:' from category name if needed.
    if category.startswith("Category:"):
        category = category.split(":")[1]
    category_stemmed_words = [stemmer.stem(word) for word in category.split() if word not in stop_words]
    category_stemmed = ' '.join(category_stemmed_words)

    for para in paragraphs:
        doc = nlp(para)
        for sent in (doc.sents):
            sent_stemmed_words = [stemmer.stem(word.text) for word in sent if word.text not in stop_words]
            sent_stemmed = ' '.join(sent_stemmed_words)
            if [word in sent_stemmed_words for word in category_stemmed_words].count(True) >= len(category_stemmed_words) / 2:
                return sent.text
        # para_stemmed_words = [stemmer.stem(word) for word in para.split()]
        # para_stemmed = ' '.join(para_stemmed_words)
        # if [word in para_stemmed_words for word in category_stemmed_words].count(True) > len(category_stemmed_words) / 2:
        #     return para
    else:
        return None

if __name__ == '__main__':
    article_title = 'Mike Pence'
    categories = get_top_categories(article_title)
    for category in categories:
        para = get_paragraph_from_category(article_title, category)
        print(article_title, category)
        print(para)
        print()
        # if para:
        #     if category.startswith("Category:"):
        #             category = category.split(":")[1]
        #    last_name = article_title.split()[-1]
        #     if last_name in para:
        #         question = para.replace(last_name, f'which {category[:-1]}')[:-1] + '?'
        #         question = question[0].upper() + question[1:]
        #         print(question)
        #         print()
