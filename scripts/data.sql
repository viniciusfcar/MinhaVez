create database minhavez;
create user vinicius identified by 'carneiro007';
grant all privileges on minhavez.* to 'vinicius'@'%';
flush privileges;