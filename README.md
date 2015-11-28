![TravisCI](https://travis-ci.org/nathanIL/openews.svg?branch=master)
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
      title: SCRAPPED_TITLE,
      title_en: TRANSLATED_TO_EN_TITLE,
      url: SCRAPPED_URL,
      scraped_at: DATETIME_OBJECT
    }
```
compound indexes on: _url_ ASCENDING, _scraped_at_ DESCENDING
#### Testing

**Unit tests** are located under the _tests_ folder.