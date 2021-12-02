LOGIN_TESTCASE = [
    {
        "url": "/login",
        "method" : "POST",
        "data" : {
            "username": "admin",
            "password" : "rostek"
        }
    }
]

LOGIN_QC_TESTCASE = [
    {
        "url": "/login",
        "method" : "POST",
        "data" : {
            "username": "qc",
            "password" : "123456"
        }
    }
]


LOGIN_TECH_TESTCASE = [
    {
        "url": "/login",
        "method" : "POST",
        "data" : {
            "username": "tech1",
            "password" : "123456"
        }
    }
]

LOGOUT_TESTCASE = [
    {
        "url": "/logout",
        "method" : "POST"
    }
]

USER_TESTCASE = [
    {
        "url": "/user",
        "method" : "GET",
        "params" : []
    },
    {
        "url": "/user",
        "method" : "POST",
        "data" : {
            "password" : "",
            "id" : "admin1"
        }
    },
    {
        "url": "/user",
        "method" : "PATCH",
        "data" : {
            "id" : "manager",
            "admin_password" : "rostek"
        }
    },
    # {
    #     "url": "/user",
    #     "method" : "DELETE",
    #     "data" : {
    #         "id" : "manager",
    #         "admin_password" : "rostek"
    #     }
    # }
]

USER_LIST_TESTCASE = [
    {
        "url": "/user/list_id_tech",
        "method" : "GET",
        "params" : []
    },
    {
        "url": "/user/list_id_qc",
        "method" : "GET",
        "params" : []
    }
    ,
    {
        "url": "/user/list_id_manager",
        "method" : "GET",
        "params" : []
    }
]



USER_ROLE_TESTCASE = [
    {
        "url": "/userrole",
        "method" : "GET",
        "params" : []
    },
    # {
    #     "url"       : "/userrole",
    #     "method"    : "POST",
    #     "data"      : {
    #         "id" : "admin"
    #     }
    # }
]

USER_PROFILE_TESTCASE = [
    {
        "url": "/profile",
        "method" : "GET",
        "params" : []
    },
    {
        "url"       : "/profile",
        "method"    : "PATCH",
        "data"      : {
            "id" : "admin"
        }
    }
]


# loi
# USER_REFRESHTOKEN_TESTCASE = [
#     {
#         "url": "/refresh_token",
#         "method" : "POST",
#         "data" : {
            
#         }
#     }
# ]


# USER_REVOKE_REFRESHTOKEN_TESTCASE = [
#     {
#         "url": "/revoke_refresh_token",
#         "method" : "POST",
#         "data" : {
            
#         }
#     }
# ]