"""A light-weight wrapper for the Latin WordNet API"""

import requests
from functools import lru_cache

class Semfields:
    def __init__(self, session, host, code=None, english=None, token=None):
        self.session = session
        self.host = host
        self.code = code
        self.english = english
        self.json = None
        self.token = token

    def get_auth(self):
        t = self.get_token()
        if t:
            return {'Authorization': f'Token {t}'}

    def get_token(self):
        return self.token

    def get(self):
        if self.json is None:
            self.json = self.session.get(
                f"{self.host}/api/semfields/{self.code}/?format=json"
            ).json()['results']
        return self.json

    def search(self):
        if self.english:
            return self.session.get(
                f"{self.host}/api/semfields?search={self.english}"
            ).json()["results"]
        else:
            return None

    def __iter__(self):
        return iter(self.get())

    @property
    def lemmas(self):
        return iter(
            self.session.get(
                f"{self.host}/api/semfields/{self.code}/lemmas/?format=json",
            ).json()["results"]
        )

    @property
    def synsets(self):
        return iter(
            self.session.get(
                f"{self.host}/api/semfields/{self.code}/synsets/?format=json",
            ).json()["results"]
        )


class Synsets:
    def __init__(self, session, host, pos=None, offset=None, gloss=None, token=None):
        self.session = session
        self.host = host
        self.offset = f"{offset}/" if offset else ""
        self.pos = f"{pos}/" if pos else ""
        self.gloss = gloss
        self.json = None
        self.token = token

    def get_auth(self):
        t = self.get_token()
        if t:
            return {'Authorization': f'Token {t}'}

    def get_token(self):
        return self.token

    def get(self):
        if self.json is None:
            self.json = []
            results = self.session.get(
                f"{self.host}/api/synsets/{self.pos}{self.offset}?format=json",
            ).json()
            while results:
                self.json.extend(results["results"])
                if results["next"]:
                    results = self.session.get(results["next"]).json()
                else:
                    results = None
            return self.json

    def search(self):
        if self.gloss:
            return self.session.get(
                f"{self.host}/api/synsets?search={self.gloss}"
            ).json()["results"]
        else:
            return None

    def __iter__(self):
        yield from self.get()

    @property
    def lemmas(self):
        return self.session.get(
            f"{self.host}/api/synsets/{self.pos}{self.offset}lemmas/?format=json"
        ).json()["results"]


    @property
    def relations(self):
        results = self.session.get(
            f"{self.host}/api/synsets/{self.pos}{self.offset}relations/?format=json"
        )
        if results:
            data = results.json()["results"]
            return data[0]["relations"]

    @property
    def sentiment(self):
        results = self.session.get(
            f"{self.host}/api/synsets/{self.pos}{self.offset}sentiment/?format=json"
        )
        if results:
            data = results.json()['results'][0]
            return data["sentiment"]


class Lemmas:
    def __init__(self, session, host, lemma=None, pos=None, morpho=None, uri=None, token=None):
        self.session = session
        self.host = host
        self.lemma = f"{lemma}/" if lemma else "*/"
        self.pos = f"{pos}/" if pos else "*/"
        self.morpho = f"{morpho}/" if morpho else ""
        self.uri = uri
        self.json = None
        self.token = token

    def get_auth(self):
        t = self.get_token()
        if t:
            return {'Authorization': f'Token {t}'}

    def get_token(self):
        return self.token
    
    def get(self):
        if self.json is None:
            if self.uri is not None:
                self.json = self.session.get(
                    f"{self.host}/api/uri/{self.uri}?format=json"
                ).json()["results"]
            else:
                self.json = []
                results = self.session.get(
                    f"{self.host}/api/lemmas/{self.lemma}{self.pos}{self.morpho}?format=json"
                ).json()
                while results:
                    self.json.extend(results["results"])
                    if results["next"]:
                        results = self.session.get(results["next"]).json()
                    else:
                        results = None
        return self.json

    def search(self):
        if self.lemma:
            results = self.json = self.session.get(
                f"{self.host}/api/lemmas/?search={self.lemma.strip('/')}"
                ).json()
            while results:
                yield from results["results"]
                if results["next"]:
                    results = self.session.get(results["next"]).json()
                else:
                    results = None

    def __iter__(self):
        return iter(self.get())

    @property
    def synsets(self):
        if self.uri is not None:
            results = self.session.get(
                f"{self.host}/api/uri/{self.uri}/synsets/?format=json"
            ).json()["results"]
        else:
            results = self.session.get(
                f"{self.host}/api/lemmas/{self.lemma}{self.pos}{self.morpho}synsets/?format=json"
            ).json()["results"]
        return results

    @property
    def relations(self):
        if self.uri is not None:
            return self.session.get(
                f"{self.host}/api/uri/{self.uri}/relations/?format=json"
            ).json()["results"]
        else:
            return self.session.get(
                f"{self.host}/api/lemmas/{self.lemma}{self.pos}{self.morpho}relations/?format=json"
            ).json()["results"]

    @property
    def synsets_relations(self):
        if self.uri is not None:
            return self.session.get(
                f"{self.host}/api/uri/{self.uri}/synsets/relations/?format=json"
            ).json()["results"]
        return self.session.get(
            f"{self.host}/api/lemmas/{self.lemma}{self.pos}{self.morpho}synsets/relations/?format=json"
        ).json()["results"]


class LatinWordNet:
    def __init__(self, host="https://latinwordnet.exeter.ac.uk", token=None):
        self.host = host.rstrip("/")
        self.token = token

        self.session = requests.Session()

    @lru_cache(maxsize=None)
    def lemmatize(self, form: str, pos: str = None):
        results = self.session.get(
            f"{self.host}/lemmatize/{form}/{f'{pos}/' if pos else ''}?format=json"
        )
        return iter(results.json()) if results else []

    @lru_cache(maxsize=None)
    def translate(self, language: str, form: str, pos: str = "*"):
        pos = f"{pos}/" if pos else ""
        results = self.session.get(
            f"{self.host}/translate/{language}/{form}/{pos}?format=json"
        )
        return iter(results.json()) if results else []

    @lru_cache(maxsize=None)
    def sentiment_analysis(self, text, weighting=None, excluded=None):
        """
        :param text: The string to be analyzed.
        :param weighting: 'average', 'harmonic' or 'geometric'
        :param excluded: List of 3-uples consisting of ('lemma', 'morpho', 'uri') to be excluded from analysis
        :return: List of possible analyses with scores
        """
        
        data = {
                'text': text,
        }
        if weighting:
            data['weighting'] = weighting
        if excluded:
            data['excluded'] = excluded
        results = self.session.post(f"{self.host}/sentiment/", data=data, verify=True)
        return results

    @lru_cache(maxsize=None)
    def lemmas(self, lemma=None, pos=None, morpho=None):
        return Lemmas(self.session, self.host, lemma, pos, morpho)

    @lru_cache(maxsize=None)
    def lemmas_by_uri(self, uri):
        return Lemmas(self.session, self.host, uri=uri)

    @lru_cache(maxsize=None)
    def synsets(self, pos: str = None, offset: str = None, gloss: str = None):
        return Synsets(self.session, self.host, pos, offset, gloss)

    @lru_cache(maxsize=None)
    def semfields(self, code: str = None, english: str = None):
        return Semfields(self.session, self.host, code, english)

    @lru_cache(maxsize=None)
    def index(self, pos=None, morpho=None):
        pos = f"{pos}/" if pos else "*/"
        morpho = f"{morpho}/" if morpho else ""
        results = self.session.get(
            f"{self.host}/api/index/{pos}{morpho}/?format=json"
        ).json()
        while results:
            yield from results["results"]
            if results["next"]:
                results = self.session.get(results["next"]).json()
            else:
                results = None

    def obtain_auth_token(self, username, password):
        results = self.session.post(f"{self.host}/api-token-auth/", data={'username': username, 'password': password},
                                    verify=True)
        if results:
            self.session.headers.update({'Authorization': f'Token {results.json()["token"]}'})


relation_types = {
    '!': 'antonyms',
    '@': 'hypernyms',
    '~': 'hyponyms',
    '#m': 'member-of',
    '#s': 'substance-of',
    '#p': 'part-of',
    '%m': 'has-member',
    '%s': 'has-substance',
    '%p': 'has-part',
    '=': 'attribute-of',
    '|': 'nearest',
    '+r': 'has-role',
    '-r': 'is-role-of',
    '*': 'entails',
    '>': 'causes',
    '^': 'also-see',
    '$': 'verb-group',
    '&': 'similar-to',
    '<': 'participle',
    '+c': 'composed-of',
    '-c': 'composes',
    '\\': 'derived-from',
    '/': 'related-to',
    }
