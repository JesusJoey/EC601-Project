//Copyright Yang Qiao joeyang@bu.edu

var express = require('express');
var fs = require('fs');
var mongoose = require('mongoose');
var Schema = mongoose.Schema;
var multer = require('multer');

var imgPath='/Users/joe/Desktop/images/1.jpg';


mongoose.connect('mongodb://<dbuser>:<dbpassword>@ds153352.mlab.com:53352/ec601_database', {
  auth: {
    user:'',
    password:''
  },
  useNewUrlParser:true
}, function(err, client) {
  if (err) {
    console.log(err);
  }
  console.log('connect!!!');
});

var schema = new Schema(
	{ img: 
		{ data: Buffer, contentType: String }
	}
);
var Item = mongoose.model('Item',schema);

mongoose.connection.on('open', function () {
  console.error('mongo is open');

  // empty the collection
   Item.deleteOne(function (err) {
    if (err) throw err;
    console.error('removed old docs');
    // store an img in binary in mongo
    var a = new Item;

    a.img.data = fs.readFileSync(imgPath);
    a.img.contentType = 'image/jpg';
    a.save(function (err, a) {
      if (err) throw err;

      console.error('saved img to mongo');
      process.exit(0);
     });
   });
});

