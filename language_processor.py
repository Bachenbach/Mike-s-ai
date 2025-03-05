# core/nlp/language_processor.py
import spacy
import nltk
from textblob import TextBlob
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

class LanguageProcessor:
    def __init__(self):
        # Initialize NLP models
        self.nlp = spacy.load('en_core_web_trf')  # Using transformer pipeline
        self.initialize_models()
        self.load_nltk_resources()
        
        # Initialize T5 for text processing
        self.t5_tokenizer = T5Tokenizer.from_pretrained('t5-base')
        self.t5_model = T5ForConditionalGeneration.from_pretrained('t5-base')
        
        # Initialize vectorizer
        self.tfidf = TfidfVectorizer()
        
        # Cache for processed results
        self.cache = {}

    def initialize_models(self):
        """Initialize various NLP models"""
        try:
            # Word2Vec model for word embeddings
            self.word2vec = Word2Vec.load('models/word2vec/trained_model.w2v')
        except:
            print("Training new Word2Vec model...")
            self.word2vec = None  # Will be trained on first use

    def load_nltk_resources(self):
        """Load required NLTK resources"""
        resources = [
            'punkt', 'averaged_perceptron_tagger', 
            'maxent_ne_chunker', 'words', 'stopwords',
            'wordnet'
        ]
        for resource in resources:
            try:
                nltk.data.find(f'tokenizers/{resource}')
            except LookupError:
                nltk.download(resource)

    async def process_text(self, text, tasks=None):
        """
        Comprehensive text processing
        tasks: list of tasks to perform (if None, perform all)
        """
        if not tasks:
            tasks = ['syntax', 'semantics', 'sentiment', 'entities', 'summary']

        # Cache check
        cache_key = f"{text}_{'-'.join(tasks)}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        results = {}
        doc = self.nlp(text)

        for task in tasks:
            if task == 'syntax':
                results['syntax'] = await self._analyze_syntax(doc)
            elif task == 'semantics':
                results['semantics'] = await self._analyze_semantics(text)
            elif task == 'sentiment':
                results['sentiment'] = await self._analyze_sentiment(text)
            elif task == 'entities':
                results['entities'] = await self._extract_entities(doc)
            elif task == 'summary':
                results['summary'] = await self._generate_summary(text)

        # Cache results
        self.cache[cache_key] = results
        return results

    async def _analyze_syntax(self, doc):
        """Detailed syntactic analysis"""
        return {
            'tokens': [
                {
                    'text': token.text,
                    'lemma': token.lemma_,
                    'pos': token.pos_,
                    'tag': token.tag_,
                    'dep': token.dep_,
                    'is_stop': token.is_stop
                } for token in doc
            ],
            'sentences': [str(sent) for sent in doc.sents],
            'noun_phrases': [str(chunk) for chunk in doc.noun_chunks]
        }

    async def _analyze_semantics(self, text):
        """Semantic analysis including word embeddings"""
        blob = TextBlob(text)
        words = [word.lower() for word in blob.words if word.isalnum()]
        
        # Get word embeddings if available
        embeddings = {}
        if self.word2vec:
            for word in words:
                try:
                    embeddings[word] = self.word2vec.wv[word].tolist()
                except KeyError:
                    continue

        return {
            'language': blob.detect_language(),
            'word_embeddings': embeddings,
            'key_phrases': self._extract_key_phrases(blob),
            'word_frequencies': blob.word_counts
        }

    async def _analyze_sentiment(self, text):
        """Multi-level sentiment analysis"""
        blob = TextBlob(text)
        doc = self.nlp(text)
        
        return {
            'overall': {
                'polarity': blob.sentiment.polarity,
                'subjectivity': blob.sentiment.subjectivity
            },
            'sentences': [
                {
                    'text': str(sent),
                    'sentiment': TextBlob(str(sent)).sentiment.polarity
                } for sent in doc.sents
            ]
        }

    async def _extract_entities(self, doc):
        """Enhanced named entity recognition"""
        entities = []
        for ent in doc.ents:
            entity = {
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char,
                'description': spacy.explain(ent.label_)
            }
            entities.append(entity)
        
        return entities

    async def _generate_summary(self, text):
        """Generate text summary using T5"""
        try:
            inputs = self.t5_tokenizer.encode(
                "summarize: " + text,
                return_tensors="pt",
                max_length=512,
                truncation=True
            )
            
            summary_ids = self.t5_model.generate(
                inputs,
                max_length=150,
                min_length=40,
                length_penalty=2.0,
                num_beams=4,
                early_stopping=True
            )
            
            summary = self.t5_tokenizer.decode(
                summary_ids[0],
                skip_special_tokens=True
            )
            
            return summary
        except Exception as e:
            print(f"Summary generation error: {str(e)}")
            return None

    def _extract_key_phrases(self, blob):
        """Extract important phrases using TextRank-like algorithm"""
        phrases = []
        for np in blob.noun_phrases:
            phrase = {
                'text': str(np),
                'importance_score': len(np.split())  # Simple scoring
            }
            phrases.append(phrase)
        return sorted(phrases, key=lambda x: x['importance_score'], reverse=True)

    async def analyze_conversation(self, conversation_history):
        """Analyze conversation patterns and context"""
        try:
            full_text = " ".join([turn['text'] for turn in conversation_history])
            doc = self.nlp(full_text)
            
            return {
                'topic_evolution': self._analyze_topic_evolution(conversation_history),
                'overall_sentiment': await self._analyze_sentiment(full_text),
                'key_entities': await self._extract_entities(doc),
                'conversation_summary': await self._generate_summary(full_text)
            }
        except Exception as e:
            print(f"Conversation analysis error: {str(e)}")
            return None

    def _analyze_topic_evolution(self, conversation_history):
        """Track how topics evolve through the conversation"""
        topics = []
        for turn in conversation_history:
            doc = self.nlp(turn['text'])
            topics.append({
                'timestamp': turn['timestamp'],
                'main_topics': [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]
            })
        return topics
