# -*- coding: utf-8 -*-

import uuid
from sanic import Blueprint, exceptions
from sanic.log import logger
from sanic.response import json
from tools.mongo import Mongo

app = Blueprint('App')


@app.route('/model/retrieve', methods=['GET'])
async def model_retrieve(request):
    """
    get all model
    :param request:
    :return:
    """
    db = await Mongo().db()
    models = db.model.find()
    return json(models)


@app.route('/function/retrieve', methods=['GET'])
async def function_retrieve(request):
    """
    get all function
    :param request:
    :return:
    """
    model = request.args.get('model')
    db = await Mongo().db()

    if not model:
        functions = db.function.find({'active': True})
    else:
        functions = db.function.find({'model': model, 'active': True})
    return json(functions)


@app.route('/function/execute', methods=['POST'])
async def function_execute(request):
    """
    :param request: functions: [{model: "model", function: "function"}]
    :return:
    """
    functions = request.json.get('functions', {})
    origin_data = request.json.get('origin_data', {})
    db = await Mongo().db()

    if not (functions and origin_data):
        raise exceptions.ServerError("请检查必要参数的传入！")

    # begin
    step = 0
    task_uuid = str(uuid.uuid4())

    for f in functions:
        complete_model = f.get('model')
        function = f.get('function')

        try:
            index = complete_model.rfind('.')
            module, model = complete_model[:index], complete_model[index+1:]
            Class = getattr(__import__(module, fromlist=[module]), model)

            if step == 0:
                data = origin_data
                await db.record.insert_one({
                    "task_uuid": task_uuid,
                    "step": 0,
                    "function": '.'.join([complete_model, function]),
                    "record": origin_data
                })
            else:
                rec = await db.record.find({'task_uuid': task_uuid, 'step': step}).to_list(length=1)
                # data = await rec.to_list(length=1)
                data = rec[0].get('record')
            step += 1

            record = await getattr(Class(), function)(data)
            # mongodb create
            val = {
                "task_uuid": task_uuid,
                "step": step,
                "function": '.'.join([complete_model, function]),
                "record": record
            }
            await db.record.insert_one(val)

        except AttributeError:
            raise exceptions.ServerError("请检查第%s步的方法" % step)
        except Exception as e:
            logger.error(e)
            raise exceptions.ServerError(e)

    return json(record)




