
import execjs

# import PyV8

cookie = "nNaviItem=1; Ecp_ClientId=8190803112400683814; cnkiUserKey=78a8a93b-d8ab-93a1-e250-d6fac7afa41f; ASP.NET_SessionId=zpacjv45ufzbvf45glf1wi45; AutoIpLogin=; LID=; Ecp_IpLoginFail=190806222.212.80.192; SID=130102; FileNameM=cnki%3A"


# def test_v8():
#     with PyV8.JSContext() as ctx:
#         ctx.eval("""
#              function add(x, y) {
#
#                  return x + y;
#                  }"""
#                  )
#         res = ctx.locals.add(1, 2)
#         print(res)


def main():
    with open('./set_cookie.js') as f:  # 执行 JS 文件
        ctx = execjs.compile(f.read())
        res = ctx.call('getCookie', "nNaviItem", cookie)
        res2 = ctx.call('setCookie', "nNaviItem", "Visit W3School")
        print(res)


if __name__ == '__main__':
    main()
    # test_v8()