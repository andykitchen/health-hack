#!/usr/bin/env node

var http = require('http'),
    fs   = require('fs'),
    path = require('path'),
    url  = require('url')

http.createServer(handler).listen(8000)
console.log('http://localhost:8000/')

var mimeTypes = {
  '.html' : 'text/html',
  '.js'   : 'text/javascript',
  '.css'  : 'text/css',
  '.json' : 'application/json',
  '.gexf' : 'text/xml'
}

function handler(req, res) {
  var pathname = url.parse(req.url, true).pathname

  if (req.method !== 'GET') {
    res.writeHead(405)
    res.end('Unsupported request method')

    return
  }

  var filename = '.' + pathname

  fs.stat(filename, function(err, stats) {
    if(err) {
      if(err.code === 'ENOENT') {
        res.writeHead(404)
        res.end()
      } else {
        res.writeHead(500)
        res.end(err)
      }

    } else if(stats.isDirectory()) {
      res.setHeader('Location', pathname + 'index.html')
      res.writeHead(301)
      res.end()

    } else if(stats.isFile()) {
      var stream  = fs.createReadStream(filename)
      contentType = mimeTypes[path.extname(filename)] || 'text/plain'

      res.setHeader('Content-Type',  contentType + '; charset=utf-8')
      res.setHeader('Cache-Control', 'no-cache')
      res.setHeader('Pragma',        'no-cache')
      res.writeHead(200)

      stream.pipe(res)

    } else {
      res.writeHead(404)
      res.end()

    }
  })
}
