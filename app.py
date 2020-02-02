import sys
from fixerapp import app
from fixerapp.api import rates
from fixerapp.rate_ingestor import RateIngestor

def main(argv):
    app.register_blueprint(rates)

    if argv[1] == 'api':
        app.run()
    elif argv[1] == 'ingest':
        RateIngestor.process()
    else:
        print('Sorry no valid option given')
        exit(-1)


if __name__ == '__main__':
    main(sys.argv)

