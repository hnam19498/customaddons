console.log("hello world")
if (window.location.href.indexOf("products") > -1) {
    document.getElementsByClassName('price__regular')[0].after("discount code: 123")
}