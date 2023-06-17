Unit Tests Report
=================

We use Python's built-in module `unittest` and Django's testing framework for the unit testing of our project. They allow us to ensure that individual sections of code are functioning correctly and help us maintain a high-quality and robust codebase.

Test Coverage
-------------

Test coverage describes the degree to which the source code of the program is tested by our current suite of tests. Here are the current coverage percentages for each of the modules:

.. code-block:: text

    Module                                          Coverage
    manage.py                                       83%
    movie_api/__init__.py                           100%
    movie_api/admin.py                              100%
    movie_api/apps.py                               100%
    movie_api/migrations                            100%
    movie_api/models.py                             90%
    movie_api/serializers.py                        96%
    movie_api/tests                                 100%
    movie_api/urls.py                               100%
    movie_api/views.py                              98%
    moviemate                                       100%
    scraper/__init__.py                             100%
    scraper/admin.py                                100%
    scraper/apps.py                                 100%
    scraper/migrations                              100%
    scraper/models.py                               100%
    scraper/scraper.py                              79%
    scraper/tasks.py                                65%
    scraper/tests                                   95-100%
    user_api/__init__.py                            100%
    user_api/admin.py                               100%
    user_api/apps.py                                100%
    user_api/migrations                             100%
    user_api/models.py                              81%
    user_api/serializers.py                         90%
    user_api/tests                                  80-100%
    user_api/urls.py                                100%
    user_api/validations.py                         93%
    user_api/views.py                               95%

Total coverage: 91%

Improving Test Coverage
-----------------------

Even though we already have high test coverage, we strive to improve this figure continuously. Lower coverage in some modules can be due to several reasons, such as the complexity of the code or its dependence on external systems. We aim to keep improving our tests to cover as much code as possible and ensure the robustness of our system.
