
# GradeForge

This is a reimplementation of the first report card generator I made in late 2023. The extension contains code used to scrape the company's admin pages, and I have made that code private due to the potential risk of exposing sensitive details inadvertently.

As an internal tool the interface is not flashy, just doing what it needs to.

If you want to play around with it, you can serialize an object using ProtoBuf, and submit it easily using the following command:
`curl -X POST --data-raw $'\n\x06103348\x12\nNAme, Test(\x04' http://localhost:5000/generate`