# flake8: noqa

import random
from fastapi import FastAPI, HTTPException, Request, Response
import uuid
from fastapi.responses import RedirectResponse
import requests
import logging
import sys
from starlette_exporter import PrometheusMiddleware, handle_metrics


app_name = 'hello'
app = FastAPI(title=app_name, version='0.0.1', description=app_name, swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})
app.add_middleware(
    PrometheusMiddleware,
    app_name=app_name,
    prefix='app',
    labels={
      "service": "hello",
    },
    group_paths=True,
    buckets=[0.1, 0.5, 1, 2.5, 10],
    skip_paths=['/docs', '/openapi.json', '/'],
    skip_methods=['OPTIONS'],
    )
app.add_route("/metrics", handle_metrics)


logger = logging.getLogger(app_name)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)8s] %(name)s %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.info('API is starting up http://127.0.0.1:8000/')


@app.get("/")
async def root():
    return RedirectResponse("/docs")


@app.get("/api/v1/hello")
async def hello(request: Request, response: Response):
    request_id = request.headers.get('x-request-id', str(uuid.uuid4()))
    response.headers["x-response-id"] = request_id
    retval = {
            "response_id": request_id,
            "data": []
        }
    retval['data'].append('test-app-shubham works!')
    return retval


@app.get("/api/v1/fallible/{pass_weight}/{fail_weight}")
async def fallible_hello(
        request: Request, response: Response, pass_weight: float, fail_weight: float):
    request_id = request.headers.get('x-request-id', str(uuid.uuid4()))
    response.headers["x-response-id"] = request_id
    retval = {
            "response_id": request_id,
            "data": []
        }

    choice = random.choices(('pass', 'fail'), weights=[pass_weight, fail_weight])
    logger.info('pass_weight: {}, fail_weight: {}, choice: {}'.format(pass_weight, fail_weight, choice))
    if choice == ['pass']:
        retval['data'] = ["fallible pass"]
    else:
        raise HTTPException(status_code=500, detail="error: fallibe fail")
    return retval


@app.get("/api/v1/employee/{employee_id}")
async def get_employee(
        request: Request, response: Response, employee_id: int):

    request_id = request.headers.get('x-request-id', str(uuid.uuid4()))
    response.headers["x-response-id"] = request_id
    retval = {
            "response_id": request_id,
            "data": []
        }
    service_url =  'http://test-app-employee/api/v1/employee/{}'.format(employee_id)
    try:
        service_request = requests.get(service_url, headers={'x-request-id': request_id}, timeout=5)
        if service_request.status_code == 200:
            service_response = service_request.json()
            if service_response['data']:
                retval['data'] = service_response['data']
                return retval
            else:
                raise HTTPException(
                    status_code=500,
                    detail="error: upstream microservice {} malformed response".format(service_url)
                )
        else:
            raise HTTPException(
                status_code=500,
                detail="error: upstream microservice {} returned status code {}".format(service_url, service_request.status_code)
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail="exception: upstream microservice {} - {}".format(service_url, e))


@app.get("/api/v1/httpbin/headers")
async def get_employee(
        request: Request, response: Response):

    request_id = request.headers.get('x-request-id', str(uuid.uuid4()))
    response.headers["x-response-id"] = request_id
    retval = {
            "response_id": request_id,
            "data": []
        }
    service_url = 'https://httpbin.org/headers'
    try:
        service_request = requests.get(service_url, headers={'x-request-id': request_id}, timeout=5)
        if service_request.status_code == 200:
            service_response = service_request.json()
            retval['data'].append({
                'request': service_url,
                'response': service_response
            })
            return retval
        else:
            raise HTTPException(
                status_code=500,
                detail="error: upstream microservice {} malformed response".format(service_url)
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail="exception: upstream microservice {} - {}".format(service_url, e))

