#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""URL shortening service to be used in a microservices environment.

"""

# Standard
import hashlib
import logging
import logging.config
import logging.handlers

# Third party
import validators
import tornado.web
import tornado.ioloop
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Local
from .settings import *
from .models import URL, Base

# Logging
logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class InvalidUrlException(tornado.web.HTTPError):
    pass


class PrometheusHandler(tornado.web.RequestHandler):
    """Microservice instrumentation endpoint with Prometheus
    If this service is part of a microservices architecture it would need
    an instrumentation endpoint. See http://microservices.io for
    architecture info
    """
    def get(self):
        # TODO: Export metrics
        pass


class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        """Preparing database connection"""
        self.engine = create_engine(DATABASE)
        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        Base.metadata.bind = self.engine

        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    def hash(self, url):
        """Hashing the long url into the key to look and redirect to the
        long url.

        :param url: String
        :return: String md5
        """

        # TODO: Change this to a shorter string usable by humans. MD5 is too
        # long for typing in the url but ok for computers
        h = hashlib.md5()
        h.update(url)
        return h.hexdigest()

    def valid(self, url):
        """Validating the url prior to saving in the DB.

        :param url: String
        :return: Boolean
        """
        if validators.url(url):
            return True
        return False

    def create(self, long_url):
        """Retrieves or creates URL records

        :param long_url: Long url
        :return: Short url
        """
        short_url = self.hash(long_url)

        # Retrieve record from DB
        record = self.retrieve(short_url)
        if not record:
            # Create record in DB
            record = URL(short=short_url, long=long_url)
            self.session.add(record)
            self.session.commit()

        return record

    def retrieve(self, url):
        """Retrieves a record from the DB

        :param url: Short url
        :return: record from the database
        """
        return self.session.query(URL).filter(URL.short == url).first()


class ShortHandler(BaseHandler):
    """Endpoint handler for creating short urls and redirecting."""

    def post(self, *args):
        """Creates a short url from a long url."""
        if self.valid(self.request.body.decode("utf-8")):
            record = self.create(self.request.body)
            self.write(record.short)
        else:
            raise InvalidUrlException(reason='Invalid URL', status_code=400)

    def get(self, url):
        """Retrieve and redirect to long url in DB.

        :param url: Short url
        :return: Redirects or response message.
        """
        if url:
            # Get the url record from the urls table
            record = self.retrieve(url)
            if record:
                self.redirect(record.long)
            else:
                raise InvalidUrlException(reason='Not Found', status_code=404)

        else:
            # Not sure what to put here. Since this is the root / it should
            # have some sort of response.
            # One option is to check for content type to differentiate humans
            # from services
            # if content type is 'text/html' show an html tool page for humans
            # if content type is 'text/plain' show this message or maybe
            # application/json and return a json response body
            self.write('Welcome to the link shortening service')


def service():
    svc = tornado.web.Application([
        # Instrumentation endpoint
        # (r"/metric", PrometheusHandler),

        (r"/(.*)", ShortHandler),
    ])
    svc.listen(HTTP_PORT)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    service()