[![Build Status](https://travis-ci.org/nathanIL/openews.svg?branch=master)](https://travis-ci.org/nathanIL/openews?branch=master)
[![Coverage Status](https://coveralls.io/repos/nathanIL/openews/badge.svg?branch=master&service=github)](https://coveralls.io/github/nathanIL/openews?branch=master)
# Openews

An NLP (Natural Language Processing) based experimental project aimed to bundle news from various sources.

## Architecture
#### Components
1. MongoDB - database layer.
2. Redis - queuing scrapper jobs.
3. Flask - REST / Web services.

#### Concepts
* _Scrapper_: New collector.
* _DataProcessor_: Processes raw data collected by scrappers and structure it (this is the NLP part). 
* _Job_: A Queued Scrapper.
* _Worker_: A Python process running and waiting for _Jobs_ to be added to the queue, then execute them.
* _Server_: A RESTful web server managing all the services.

#### Data Flow
1. Scrappers are queued by _rq_ as jobs in redis to the **_scrapper_jobs_** queue once every X minutes (scheduled by 
_cron_ or equivalent method).
2. When the jobs are executed by a worker, the scrappers begin collecting the _data_ (news) from the various resources, 
each collects its own resources asynchronously ( _gevent_ ).
3. Each scrapper stores its scrapped data in a nested document inside _raw_ database, the nested object is named as
the scrapper class name in lower case letters. A typical scrapper document has the following fields:
```
{
        category: string,
        title: string,
        url: string,
        scraped_at: datetime.utcnow()
        (1)bundled: 1,
        (2)title_en: string
}
```
_Notes_:
    * (1) _bundled_ is an optional property which is available only when the document was already classified by the NLP 
    process. it means that this document was found similar to other documents and was bundled with them.
    * (2) _title_en_ is also an optional property which is available only if a translation was performed. The original
    is _title_. 
4. DataProcessors are queued by _rq_ as jobs in redis to the **_nlp_process_** queue once every T minutes (scheduled by 
_cron_ or equivalent method). If similar documents are found in _raw_ database, they will be stored in the _bundled_ 
database in the following structure:


##### Details
 * Compound indexe on: _url_ ASCENDING
 * In case translation was made to _title_ then it will be stored in _title_en_.


#### OS dependencies
The following packages are required (names might be slightly different depending on the linux distro):

* libxml2-dev 
* libxslt1-dev 
* python-dev
* liblas-devel.x86_64 (aka: libblas-dev)
* lapack-devel.x86_64 (aka liblapack-dev)

#### Testing

**Unit tests** are using _nose_ located under the _tests_ folder, can be exectuded by running:

1. First create a _virtualenv_:
```
$ virtualenv -p python3 venv
```
2. Load the virtual environment ( _virtualenv_ ):
```
$ source venv/bin/activate
```

3. Install all the development dependencies:
```
$ pip install -r requirements-dev.txt
```
4. Run the test suite:
```
$ export OPENEWS_DEVELOPMENT_ENV="true"; nosetests -v -s tests/; unset OPENEWS_DEVELOPMENT_ENV;
```
