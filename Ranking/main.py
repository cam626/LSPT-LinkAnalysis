import sys
from flask import Flask, request, jsonify

from src import ranker


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/ranking', methods=["GET"])
def ranking():
    args = request.args
    for i in ['query']:
        try:
            assert i in args
        except AssertionError:
            return 'ERROR: Missing argument: %s' % i

    query = request.args.get('query')
    test = True if request.args.get('test') == 'true' else False
    res = ranker.ranking(query, test)
    return jsonify(res)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('USAGE: <PORT>')
        sys.exit()
    app.run('0.0.0.0', port=int(sys.argv[1]), threaded=True)
