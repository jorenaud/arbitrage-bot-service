from rbasis.urlrouter import router
from . import views

def RegPath():
    router.register(r'menu',                views.menu,                     "menu",                 "")
    router.register(r'user',                views.userView,                 "user",                 "")
    router.register(r'privilege',           views.privilegeView,            "privilege",            "")
    router.register(r'accesshistory',       views.accesshistoryView,        "accesshistory",        "")
    router.register(r'eventhistory',        views.eventhistoryView,         "eventhistory",         "")
    router.register(r'cmenu',               views.cmenu,                    "cmenu",                "")
    router.register(r'orders',              views.ordersView,               "orders",               "")
    router.register(r'adminemails',         views.adminemailsView,          "adminemails",          "")
    router.register(r'roles',               views.roleView,                 "roles",                "")
    router.register(r'plans',               views.planView,                 "plans",                "")
    router.register(r'interval',            views.intervalView,             "interval",             "")
    router.register(r'botList',             views.botListView,              "botList",              "")
    router.register(r'price',               views.priceView,                "price",                "")
    router.register(r'bot',                 views.botView,                  "bot",                  "")
    router.register(r'news',                views.newsView,                 "news",                 "")

