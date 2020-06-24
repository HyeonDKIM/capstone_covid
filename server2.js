var express = require('express');
var http = require('http');
var static = require('serve-static');
var path = require('path');
var bodyParser = require('body-parser');
var cors = require('cors');

var mongoose = require('mongoose');

var app = express();

var db;
function connectDB(){
    var databaseUrl = 'mongodb://localhost:27017/corona';

    mongoose.connect(databaseUrl);
    db = mongoose.connection;

    db.on('open', function(){
        console.log('데이터베이스에 연결됨 : ' + databaseUrl);
    });
    db.on('disconnected', function() {
        console.log('데이터베이스 연결 끊어짐.');
    });
    db.on('error', console.error.bind(console, 'mongoose 연결 에러.'));
}


app.set('port', process.env.PORT || 8080);
app.use(express.static(__dirname + '/'));
app.use('/public',static(path.join(__dirname, 'public')));


app.use(cors());
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});


app.use(bodyParser.urlencoded({extended:false}));
app.use(bodyParser.json());

var router = express.Router();

var addressUrl;
router.route('/process/mask').post(function(req, res){
  console.log('/process/mask 라우팅 함수 호출됨.');
  var paramAddress = req.body.address || req.query.address;
  console.log('요청 파라미터 : ' + paramAddress);
  addressUrl = "https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByAddr/json?address=" + paramAddress
  res.redirect('/public/mask.html');
});

app.get('/api/maskinfo', function(req, res){
  res.redirect(addressUrl);
})

app.get('/api/patientroute', function(req, result){
  console.log("patientroute request");
  db.collection("PatientRoute").find().toArray(function(err,res){
    if(err) throw err;
    result.json(res);
  })
});

app.get('/api/patient', function(req, result){
	db.collection("PatientInfo").find().toArray(function(err, res){
		if (err) throw err;
		result.json(res);
	})
});

app.get('/api/patient_num', function(req, result){
	db.collection("Time").find().toArray(function(err, res){
		if (err) throw err;
		result.json(res);
	})
});

app.get('/api/world', function(req, result){
	db.collection("WorldData").find().toArray(function(err, res){
		if (err) throw err;
		result.json(res);
	})
});

app.get('/api/patient_region', function(req, result){
	db.collection("TimeProvince").find().toArray(function(err, res){
		if (err) throw err;
		result.json(res);
	})
});

app.get('/api/patient_route', function(req, result){
	db.collection("PatientRoute").find().toArray(function(err, res){
		if (err) throw err;
		result.json(res);
	})
});

app.get('/api/patient_place', function(req, result){
  db.collection("PatientRoute").aggregate([{$group: {_id: "$patient_id", longitude: {$first: "$longitude"}, latitude: {$first:"$latitude"}}}]).toArray(function(err, res){
    if (err) throw err;
    result.json(res);
  })
});

app.use('/', router);

app.all('*', function(req, res){
    res.status(404).send('<h1>요청하신 페이지는 없습니다.</h1>');
}); //all-모든 요청에 대해서 처리하겠다.

var server = http.createServer(app).listen(app.get('port'), function(){
    console.log('익스프레스로 웹 서버를 실행함 : ' + app.get('port'));
    connectDB();
});
