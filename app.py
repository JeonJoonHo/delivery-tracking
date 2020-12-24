from couriers.courier_factory import CourierFactory
from flask import make_response, request
from flask_api import FlaskAPI

app = FlaskAPI(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return make_response({'code': 200, 'message': 'success'}, 200)


@app.route('/tracking', methods=['GET'])
def tracking():
    response_object = {
        'code': 200,
        'message': 'success',
        'data': {}
    }

    params = request.args

    if 'courier_code' not in params:
        response_object['code'] = 404
        response_object['message'] = '운송장 미등록 또는 업체에서 상품을 준비중일 경우 확인되지 않을 경우가 있습니다.\n 해당 택배 업체로 문의 바랍니다.'
        return make_response(response_object, 404)

    if 'track_id' not in params:
        response_object['code'] = 404
        response_object['message'] = '운송장 미등록 또는 업체에서 상품을 준비중일 경우 확인되지 않을 경우가 있습니다.\n 해당 택배 업체로 문의 바랍니다.'
        return make_response(response_object, 404)

    courier = CourierFactory(str(params['courier_code']), params['track_id']).build()

    if courier == "":
        response_object['code'] = 404
        response_object['message'] = '운송장 미등록 또는 업체에서 상품을 준비중일 경우 확인되지 않을 경우가 있습니다.\n 해당 택배 업체로 문의 바랍니다.'
        return make_response(response_object, 404)

    response_object['data'] = courier.track()

    return make_response(response_object, 200)


# We only need this for local development.
if __name__ == '__main__':
    app.run()
