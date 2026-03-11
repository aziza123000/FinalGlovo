from fastapi import FastAPI
from mysite.database.db import engine, Base
from mysite.api.user_api import user_router
from mysite.api.category_api import category_router
from mysite.api.store_api import store_router
from mysite.api.product_api import product_router
from mysite.api.order_api import order_router
from mysite.api.review_api import review_router
import uvicorn
from mysite.api.chat_api import chat_router
from mysite.api.auth_api import auth_router
from mysite.api.contact_api import contact_router
from mysite.api.address_api import address_router
from mysite.api.store_menu_api import store_menu_router
from mysite.api.courier_api import courier_router
Base.metadata.create_all(bind=engine)

shop_app = FastAPI(title='loh')

shop_app.include_router(user_router)
shop_app.include_router(category_router)
shop_app.include_router(store_router)
shop_app.include_router(product_router)
shop_app.include_router(order_router)
shop_app.include_router(review_router)
shop_app.include_router(chat_router)
shop_app.include_router(auth_router)
shop_app.include_router(contact_router)
shop_app.include_router(address_router)
shop_app.include_router(store_menu_router)
shop_app.include_router(courier_router)
if __name__ == '__main__':
    uvicorn.run(shop_app, host='127.0.0.1', port=9000)
