# -*- coding: utf-8 -*-

import script

from sanic import Sanic
from api import api
from tools.decorators import function_list, model_list
from tools.mongo import Mongo
from pymongo import UpdateOne

app = Sanic()
app.blueprint(api)


@app.listener("before_server_start")
async def before_server_start(request, loop):
    # client = await Mongo().client()
    # db = client.workflow
    db = await Mongo().db()
    model_bulk = [UpdateOne({'_id': m.get('_id')}, {"$set": m}, upsert=True) for m in model_list]
    function_bulk = [UpdateOne({'_id': f.get('_id')}, {"$set": f}, upsert=True) for f in function_list]

    await db.model.bulk_write(model_bulk)
    await db.function.bulk_write(function_bulk)


@app.listener('after_server_stop')
async def after_server_stop(request, loop):
    # client = await Mongo().client()
    # db = client.workflow
    db = await Mongo().db()
    await db.function.update_many({}, {"$set": {"active": False}})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001, workers=8)
