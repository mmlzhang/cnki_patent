function clearAll() {
    var obj = document.getElementsByName('FileNameM');
    if (obj != null) {
        if (obj.length) {
            for (var i = 0; i < obj.length; i++) {
                obj[i].checked = false;
            }
        }
        else
            document.getElementsByName('FileNameM').checked = false;
    }
    setCookie("FileNameM", "cnki:");
    updateCounter();
}


function clearAllMarks(form) {
    e = document.forms[0].elements;
    for (i = 0; i < e.length; i++) {
        if (e[i].type == "checkbox" && e[i].name == "FileNameM") {
            e[i].checked = false;
        }
    }
    setCookie("FileNameM", "cnki:");
    updateCounter();
}
function getCookie(Name, cookies) {
    var search = Name + "=";
    if (cookies.length > 0) {
        offset = cookies.indexOf(search);
        if (offset != -1) {
            offset += search.length;
            end = cookies.indexOf(";", offset);
            if (end == -1)
                end = cookies.length;
            return unescape(cookies.substring(offset, end));
        }
    }
}
function setCookie(name, value) {
    return name + "=" + escape(value) + ";" + "path=/";
}
function addToCookie(v) {
    company = "cnki";
    cookie = new String(getCookie("FileNameM"));
    if ((cookie.length > 0) && ((cookie.substring(0, cookie.indexOf(':')) == company))) {
        if (cookie.length - 1 == cookie.indexOf(':')) {
            setCookie("FileNameM", cookie + v);
        } else {
            setCookie("FileNameM", cookie + "," + v);
        }
    } else {
        setCookie("FileNameM", company + ":" + v);
    }
}
function removeFromCookie(v) {
    var company = "cnki";
    var cookie = new String(getCookie("FileNameM"));
    if (cookie.substring(0, cookie.indexOf(':')) == company) {
        if (cookie.length < 5) { return; } else { cookie += ','; cookie = cookie.replace(v + ',', ''); if (cookie.length > 5) { cookie = cookie.substring(0, cookie.length - 1); } setCookie('FileNameM', cookie); }
    } else { cookie = ""; }
    if (cookie != "") { setCookie("FileNameM", (cookie.indexOf(company + ":") != -1 ? "" : company + ":") + cookie); }
    else { setCookie("FileNameM", company + ":"); }
}