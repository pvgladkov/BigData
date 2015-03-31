Input:

      UID    Timestamp    URL
      123    1422751272.768    http%3A%2F%2Fwww.ya.ru%2Fsample-page-1
      123    1422751272.769    http%3A%2F%2Fwww.ya.ru%2Fsample-page-2
      123    1422751272.770    http%3A%2F%2Fwww.ya.ru%2Fsample-page-3
      456    1354546464.210    http%3A%2F%2Fwww.ya.ru%2Fsample-page-1
      
Output:

      123    0    0    0    0    1
      456    1    1    1    1    1
      789    0    0    0    0    0
