[![Build Status](https://travis-ci.org/nathanIL/openews.svg?branch=master)](https://travis-ci.org/nathanIL/openews?branch=master)
[![Coverage Status](https://coveralls.io/repos/nathanIL/openews/badge.svg?branch=master&service=github)](https://coveralls.io/github/nathanIL/openews?branch=master)
# Openews

An NLP based experimental project

#### Architecture
### Components
1. MongoDB - database layer ( _openews_ database )
2. Redis - queuing Scrappers.
3. Flask - REST / Web services.

### Data Flow
1. Scrappers ( _Scrapper_ implementation ) collecting the _data_ (titles).
2. _data_ is stored to _raw_ collection as the following document schema:
```
    { _id: ...,
      scrapper: SCRAPPER_CLASS_NAME,
      categories: [
       {     title: SCRAPPED_TITLE,
              category: A,
              title_en: TRANSLATED_TO_EN_TITLE,
              url: SCRAPPED_URL,
              scraped_at: DATETIME_OBJECT 
       },
       {     title: SCRAPPED_TITLE,
              category: Y,
              title_en: TRANSLATED_TO_EN_TITLE,
              url: SCRAPPED_URL,
              scraped_at: DATETIME_OBJECT 
       },       
      ]
    }
```

##### Details
 * Compound indexes on: _url_ ASCENDING, _scraped_at_ DESCENDING.
 * In case translation was made to _title_ then it will be stored in _title_en_.


#### OS dependencies
The following packages are required (names might be slightly different depending on the linux distro):

* libxml2-dev 
* libxslt1-dev 
* python-dev

#### Testing

**Unit tests** are located under the _tests_ folder.