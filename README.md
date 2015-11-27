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
      title: SCRAPPED_TITLE
      url: SCRAPPED_URL
    }
```
#### Testing

**Unit tests** are located under the _tests_ folder.