INSERT INTO Users (first_name, last_name, encrypted_password, email, created_at, updated_at, current_sign_in_at, last_sign_in_at, current_sign_in_ip, last_sign_in_ip, privilege) VALUES 
   ('Peter', 'Georgiev','75c979340a53d00cb0055d9b1b64d0ff8b2ca222a787c3d2d07f5c12420ed52ad131c5e31a2f544d','peter@test.test',NOW(),NOW(),NOW(),NOW(),'0.0.0.0','0.0.0.0', 2),
   ('Hanna', 'Yoo','c8ce8d9f4cb8e6d8db9cc9fe27c3542b3a0854a686213939600448f323ad091c4a9f74d68b02e9fe','hanna@test.test',NOW(),NOW(),NOW(),NOW(),'0.0.0.0','0.0.0.0', 2),
   ('Renee', 'Liu','6e21b0fa9d1bf36918de0ec988b8223077ad4c3d9360a046a4e195d02d687dc2ed482351d50e04c0','renee@test.test',NOW(),NOW(),NOW(),NOW(),'0.0.0.0','0.0.0.0', 2),
   ('Sam', 'Bhuiyan','c130c4424fc5fb196c960b6de928291471ebebe7d3a0dc34db575eb256aae07af2ee73a527195577','sam@test.test',NOW(),NOW(),NOW(),NOW(),'0.0.0.0','0.0.0.0', 2),
   ('Eriq', 'Augustine','f54f901bb496f5d75400005d290f7b396fec63e0d2f1191ca181f6faef6fc87b2451e776202632fa','eriq@test.test',NOW(),NOW(),NOW(),NOW(),'0.0.0.0','0.0.0.0', 1),
   ('Vishal', 'Venky','a37dd467b0cfb298ff84c48f28b7cbe0dd1df705097e9f0865ac8e37d9925bfa4f89084b678aa65f','vishal@test.test',NOW(),NOW(),NOW(),NOW(),'0.0.0.0','0.0.0.0', 0);

INSERT INTO Rooms VALUES
   ('RND','Recluse and defiance',1,'King',2,150,'modern'),
   ('IBS','Interim but salutary',1,'King',2,150,'traditional'),
   ('AOB','Abscond or bolster',2,'Queen',4,175,'traditional'),
   ('MWC','Mendicant with cryptic',2,'Double',4,125,'modern'),
   ('HBB','Harbinger but bequest',1,'Queen',2,100,'modern'),
   ('IBD','Immutable before decorum',2,'Queen',4,150,'rustic'),
   ('TAA','Thrift and accolade',1,'Double',2,75,'modern'),
   ('CAS','Convoke and sanguine',2,'King',4,175,'traditional'),
   ('RTE','Riddle to exculpate',2,'Queen',4,175,'rustic'),
   ('FNA','Frugal not apropos',2,'King',4,250,'traditional');

INSERT INTO Reservations VALUES
   (47496,'RND',STR_TO_DATE('01-JAN-10', '%d-%b-%y'),STR_TO_DATE('06-JAN-10', '%d-%b-%y'),150.00,1,0),
   (41112,'RND',STR_TO_DATE('06-JAN-10', '%d-%b-%y'),STR_TO_DATE('11-JAN-10', '%d-%b-%y'),135.00,1,0),
   (76809,'RND',STR_TO_DATE('12-JAN-10', '%d-%b-%y'),STR_TO_DATE('14-JAN-10', '%d-%b-%y'),187.50,1,0),
   (70172,'RND',STR_TO_DATE('23-JAN-10', '%d-%b-%y'),STR_TO_DATE('25-JAN-10', '%d-%b-%y'),150.00,1,0),
   (44358,'RND',STR_TO_DATE('25-JAN-10', '%d-%b-%y'),STR_TO_DATE('27-JAN-10', '%d-%b-%y'),150.00,2,0),
   (55344,'RND',STR_TO_DATE('30-JAN-10', '%d-%b-%y'),STR_TO_DATE('31-JAN-10', '%d-%b-%y'),135.00,1,0),
   (99471,'RND',STR_TO_DATE('31-JAN-10', '%d-%b-%y'),STR_TO_DATE('01-FEB-10', '%d-%b-%y'),135.00,1,0),
   (81473,'RND',STR_TO_DATE('01-FEB-10', '%d-%b-%y'),STR_TO_DATE('02-FEB-10', '%d-%b-%y'),127.50,1,1),
   (49253,'RND',STR_TO_DATE('03-FEB-10', '%d-%b-%y'),STR_TO_DATE('06-FEB-10', '%d-%b-%y'),150.00,1,0),
   (16748,'RND',STR_TO_DATE('21-FEB-10', '%d-%b-%y'),STR_TO_DATE('23-FEB-10', '%d-%b-%y'),135.00,1,0),
   (69316,'RND',STR_TO_DATE('26-FEB-10', '%d-%b-%y'),STR_TO_DATE('07-MAR-10', '%d-%b-%y'),150.00,1,0),
   (69844,'RND',STR_TO_DATE('07-MAR-10', '%d-%b-%y'),STR_TO_DATE('11-MAR-10', '%d-%b-%y'),172.50,1,0),
   (96839,'RND',STR_TO_DATE('11-MAR-10', '%d-%b-%y'),STR_TO_DATE('12-MAR-10', '%d-%b-%y'),150.00,1,0),
   (43911,'RND',STR_TO_DATE('12-MAR-10', '%d-%b-%y'),STR_TO_DATE('13-MAR-10', '%d-%b-%y'),127.50,1,0),
   (48382,'RND',STR_TO_DATE('13-MAR-10', '%d-%b-%y'),STR_TO_DATE('14-MAR-10', '%d-%b-%y'),150.00,1,0),
   (77032,'RND',STR_TO_DATE('14-MAR-10', '%d-%b-%y'),STR_TO_DATE('17-MAR-10', '%d-%b-%y'),172.50,1,0),
   (30043,'RND',STR_TO_DATE('17-MAR-10', '%d-%b-%y'),STR_TO_DATE('18-MAR-10', '%d-%b-%y'),150.00,2,0);
   
INSERT INTO Guests (first_name, last_name, email, reservation_code) VALUES
   ('ERASMO', 'KLEVER', 'erasmo.klever@test.test', 47496),
   ('EUGENIO', 'HOOLEY', 'eugenio.hooley@test.test', 41112),
   ('JERROD', 'WISWELL', 'jerrod.wiswell@test.test', 76809),
   ('PHEBE', 'ALMANZA', 'phebe almanza@test.test', 70172),
   ('CLINTON', 'BOBROW', 'clinton@bobrow@test.test', 44358),
   ('LIANA', 'RENSCH', 'liana.rensch@test.test', 55344),
   ('ANNETT', 'ABRAHAMS', 'annett.abrahams@test.test', 99471),
   ('YUK', 'EVERITT', 'yuk.everitt@test.test', 81473),
   ('GARRY', 'NANI', 'garry.nani@test.test', 49253),
   ('DONTE', 'KLIMKO', 'donte.klimko@test.test', 16748),
   ('JESSICA', 'SULOUFF', 'jessica.sulouff@test.test', 69316),
   ('CLINT', 'BONIOL', 'clint.boniol@test.test', 69844),
   ('ROD', 'ARANAS', 'rod.aranas@test.test', 96839),
   ('TEODORO', 'NEIN', 'teodoro.nein@test.test', 43911),
   ('ELEASE', 'SCHLADWEILER', 'elease.schladweiler@test.test', 48382),
   ('HERBERT', 'FRANC', 'herbert.franc@test.test', 77032),
   ('RHEA', 'HELFRITZ', 'rhea.helfritz@test.test', 30043);

INSERT INTO Comments VALUES
   (1, 'CLINTON', 'something@test.test', 'insert your comment here');




