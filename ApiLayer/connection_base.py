import httplib
import json
import socket

from django.conf import settings
from CommonMethods import BaseMethods

def openstack_api_connection(base_url, method, header, port, version,
                             tenant_id=None, url_parameters=None, body=None):
    '''
    :param url: (string)
    :param method: (string) [POST | GET | PUT | DELETE ]
    :param header: (JSON Object) headers for request
    :param url_parameters: (JSON Object)
    :param body: (JSON Object)
    :return: (JSON Object) Data fetched from openstack api
    '''
    extra_url = BaseMethods.url_para_to_url(**url_parameters)
    conn = httplib.HTTPConnection('%s:%s' % (settings.OPENSTACK_CONTROLLER_IP, port))
    req_header = header
    req_body = None if body is None else json.dumps(body)

    # Perform API request
    status = None
    data = None

    # TODO(pwwp):
    # use <finally> to handle success or error data
    try:
        conn.request(method,
                     '/%s/'%(version) + '' if tenant_id is None else '%s/'%(tenant_id)  + base_url + extra_url,
                     headers=req_header, body=req_body)
        response = conn.getresponse()
        if response.status != 200:
            error = {'status': 'failed',
                     'code': response.status,
                     'msg': response.reason,
                     'data': ''}
            return error
        else:
            data = {'status': 'success',
                    'data': json.loads(response.read())}
            return data
    except socket.error, e:
        return {'status': 'failed',
                'error_message': e.strerror
                }
    except httplib.HTTPException, e:
        return {'status': 'failed',
                'error_message': e.message
                }
