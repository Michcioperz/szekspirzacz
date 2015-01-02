#!/usr/bin/env node

var irc = require('irc');
var osoby = {};

var akcja = require('./sztuka.json')

akcja.forEach(function(line) {
    if (line.split("::")[0] == "osoba") {
        osoba = line.split("::")[1];
        osoby[osoba] = new irc.Client('127.0.0.1', osoba, { channels: ['#hamlet'] });
        osoby[osoba].addListener('error', console.log);
    }
    if (line.split("::")[0] == "kwestia") {
        console.log("kwestia");
        osoba = line.split("::")[1];
        strofa = line.split("::")[2];
        osoby[osoba].say("#hamlet", strofa);
    }
});
