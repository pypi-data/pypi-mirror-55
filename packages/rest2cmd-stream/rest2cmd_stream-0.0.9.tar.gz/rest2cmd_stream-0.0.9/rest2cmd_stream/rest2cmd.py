# -*- coding: utf-8 -*-
import sys
import os
import json
import yaml
import string
import random
import shlex
import subprocess
# import socketio
import requests
from traceback import format_exc
from flask import Flask, request, jsonify

app = Flask(__name__)
app.url_map.strict_slashes = False

assert 'APP_ROOT' in os.environ, 'No APP_ROOT env variable found!'
APP_ROOT = os.environ['APP_ROOT']
print('APP_ROOT', APP_ROOT)

assert 'HTTP_MAP_PATH' in os.environ, 'No HTTP_MAP_PATH env variable found!'
HTTP_MAP_PATH = os.environ['HTTP_MAP_PATH']
print('HTTP_MAP_PATH', HTTP_MAP_PATH)

with open(HTTP_MAP_PATH, 'r') as f:
    try:
        HTTP_MAP = yaml.load(f, yaml.Loader)
    except yaml.YAMLError as exc:
        print('Problem loading yaml http map file', file=sys.stderr)
        print(exc, file=sys.stderr)
        sys.exit(1)

print('HTTP_MAP', HTTP_MAP, file=sys.stderr)
assert not isinstance('HTTP_MAP', dict), (
    'Wrong content in HTTP_MAP! Got %r' % HTTP_MAP
)


def execute(executable, command, plugin_path, stream=None):
    try:
        cmd = '%s %s' % (executable, command)
        parts = shlex.split(cmd)
        cwd = os.path.normpath(os.path.join(APP_ROOT, plugin_path))
        print(
            'Resolved as: %s | @%s | %s' % (cmd, cwd, parts), file=sys.stderr
        )
        proc = subprocess.Popen(
            parts,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd
        )
        # wait for the process to terminate
        # while proc.poll() is None:
        #     time.sleep(0.2)
        if stream != None:
            print("in stream")
            if stream['room'] != None and stream['url'] != None:
                stream_data('TESTING SENDING',
                            stream['room'], url=stream['url'])

                while True:
                    output = proc.stdout.readline().decode('utf8')
                    err = proc.stderr.readline().decode('utf8')
                    if proc.poll() is not None and output == '':
                        break
                    if output:
                        stream_data(output.strip(), '111', 'http://172.17.0.1:5000')
                        print(output.strip())
                    elif is_error and err != None:
                        stream_data(err, stream['room'], url=stream['url'])
                return {
                    'is_error': is_error,
                    'content': '=====END OF STREAM=====' if proc.poll() != None else None
                }
                # while True:
                #     err = proc.stderr.readline().decode('utf8')
                #     out = proc.stdout.readline().decode('utf8')
                    
                #     is_error = proc.returncode != 0 and proc.returncode != None
                #     print("{} ------ {}".format(is_error, proc.returncode), file=sys.stderr)
                #     if out == '' and proc.poll() is not None:
                #     # print("out is empty")
                #         break
                #     elif is_error and err != None:
                #         stream_data(err, stream['room'], url=stream['url'])
                #         return {
                #             'is_error': is_error,
                #             'content': err
                #         }
                #     else:
                #         print("out: %s" % out, file=sys.stderr)
                #         stream_data(out, stream['room'], url=stream['url'])
                #         # yield out
                # return {
                #     'is_error': is_error,
                #     'content': '=====END OF STREAM=====' if proc.poll() != None else None
                # }
            else:
                print('Haven\'t received room ID and/or stream URL.', file=sys.stderr)

        out, err = proc.communicate()
        # wrap response
        is_error = proc.returncode != 0
        content_stream = (err if is_error else out).decode('utf8').strip()
        content = content_stream.split('\n')
        return {
            'is_error': is_error,
            'content':  content
        }
    except Exception:
        return {
            'is_error': True,
            'content': format_exc().split('\n')
        }


def stream_data(out, room, url=None, sio=None):
    if sio != None:
        print(out, file=sys.stderr)
        # output = {'message': out, 'room': room}
        # sio.emit('push', output, '/notification')
    elif url != None:
        if url.startswith('https'):
            sent = requests.post(
                '{}/push/{}'.format(url, room), json={'message': out}, verify=False)
        # print('http://{}/push/{}'.format(url, room), file=sys.stderr)
        else:
            sent = requests.post('{}/push/{}'.format(url, room), json={'message': out},)

        print(sent.content, file=sys.stderr)
    else:
        print('No valid parameters passed!', file=sys.stderr) 
        raise NameError('No valid parameters passed!')

        
def format_status(output):
    if output['is_error']:
        return 400
    if len(output['content']) == 0:
        return 204
    return 200


def format_output(output, is_json):
    # if app outpput is json format, it means there is a single line
    # of output or there is empty output
    # if it's not json, simply return what is in output content
    if is_json and len(output['content']) > 0:
        # it should be single line, first one, with json content
        # try to parse it, and if it fails, failover to plain text lines
        # this could be case if output is an error, like traceback
        # and executable has no control over this and can't json it
        try:
            return json.loads(output['content'][0])
        except json.decoder.JSONDecodeError:
            pass
    return output['content']


def normalize_url_args(**url_args):
    normalized = {}
    for arg_name in url_args:
        value = url_args[arg_name]
        normalized[arg_name] = ('\'%s\'' if ' ' in value else '%s') % value
    return normalized


def route_handler(path, method, config):

    def _call(**url_args):
        x_groups = request.headers.get('X-GROUPS', '').split(',')
        groups = config.get('groups', None)
        room_id = request.headers.get('STREAM_ROOM', None)
        url = request.headers.get('STREAM_URL', None)
        print("{}:{}".format(url, room_id), file=sys.stderr)
        stream = None
        if room_id != None and url != None:
            stream = {'url': url, 'room': room_id}
            print("Ready to stream!", file=sys.stderr)

        if groups is not None:
            intersection = set(x_groups) & set(groups)
            if len(intersection) == 0:
                return jsonify({
                    'message': (
                        'You don\'t have permission to access this resource.'
                    )
                }), 403
        data = request.json or {}
        payload = {**url_args, 'http_payload': json.dumps(data)}
        for k, v in (data if isinstance(data, dict) else {}).items():
            payload['http_payload__%s' % k] = v
        payload = normalize_url_args(**payload)
        print('Got payload: %s', payload, file=sys.stderr)
        command_parts = [p % payload for p in config['command'].split()]
        command = ' '.join(command_parts)
        print('Executing: %s', command, file=sys.stderr)
        output = execute(
            config['executable'], 
            command, 
            config['plugin_path'], 
            stream=stream
        )
        print('Got output: %s', output, file=sys.stderr)
        content = format_output(output, config.get('is_json', False))
        status = format_status(output)
        print('http response(%d): %s' % (status, content), file=sys.stderr)
        return jsonify(content), status

    # id(_call) is always unique, but we need to randomize name
    _call.__name__ = ''.join(
        random.choice(string.ascii_lowercase) for _ in range(10)
    )
    app.route(path, methods=[method])(_call)


# dynamically create flask routes from http map
for method, routes in HTTP_MAP.items():
    for path, config in routes.items():
        route_handler(path, method, config)

print('Starting app ..', file=sys.stderr)

if __name__ == '__main__':
    app.run()
