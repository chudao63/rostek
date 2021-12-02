from datetime import timedelta

REFRESH_EXP = timedelta(days=90)
ACCESS_EXP = timedelta(minutes=43200)

FILTER_JSON = [
    {
        "name" : "name",
        "label" : "Tên người dùng",
        "type" : "string"
    },
    {
        "name" : "role",
        "label" : "Chức năng",
        "type" : "list",
        "data" : []
    }
]


TABLE_JSON = [
    {
        "title": "Tên đăng nhập",
        "key": "username",
        "dataIndex": 'username',
        "active" : 1
    },
    {
        "title": "Mật khẩu",
        "key": "password",
        "dataIndex": 'password',
        "active" : 1
    },
    {
        "title": "Tên",
        "key": "name",
        "dataIndex": 'name',
        "active" : 1
    },
    {
        "title": "email",
        "key": "email",
        "dataIndex": 'email',
        "active" : 1
    },
    {
        "title": "Số điện thoại",
        "key": "phone",
        "dataIndex": 'phone',
        "active" : 1
    },
    {
        "title": "Chức năng",
        "key": "role_name",
        "dataIndex": 'role_name',
        "active" : 1
    },
    {
        "title": "Level",
        "key": "level",
        "dataIndex": 'level',
        "active" : 1
    },
    {
        "title": "active",
        "key": "active",
        "dataIndex": 'active',
        "active" : 1
    },
    {
        "title": "Tên doanh nghiệp",
        "key": "enterprise",
        "dataIndex": 'enterprise',
        "active" : 1
    },
    {
        "title": "Mô tả",
        "key": "description",
        "dataIndex": 'description',
        "active" : 1
    }
]