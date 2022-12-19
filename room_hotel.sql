CREATE EXTENSION IF NOT EXISTS citext;
CREATE DOMAIN email AS citext
  CHECK ( value ~ '^[a-zA-Z0-9.!#$%&''*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$' );
/*
text_of_comment
https://en.wikipedia.org/wiki/ISO/IEC_5218
0 = 未知；
1 = 男性；
2 = 女性；
9 = 不適用。
*/
CREATE DOMAIN gender CHAR(1)
    CHECK (value IN ( 'F' , 'M' ) )
    ;
/*
https://zh.wikipedia.org/zh-tw/E.164
*/
CREATE TYPE credit_cards AS (
    safety_number  CHARACTER VARYING,
    card_id     CHARACTER VARYING,
    expire_date           DATE
);

CREATE TABLE booking.member
(
    email email NOT NULL,
    name CHARACTER VARYING NOT NULL,
    password CHARACTER VARYING NOT NULL,
    gender SMALLINT NOT NULL,
    member_id SERIAL NOT NULL,
    phone CHARACTER VARYING(15),
    member_type SMALLINT NOT NULL DEFAULT 0,
    image_path VARCHAR,
    credit_cards credit_cards,
    PRIMARY KEY (member_id),
    UNIQUE (email, member_id)
);

CREATE TABLE booking.hotel(
    ID SERIAL PRIMARY KEY,
    HOTEL_NAME VARCHAR NOT NULL,
    REGULATION VARCHAR,
    CITY VARCHAR,
    REGION VARCHAR,
    ROAD_AND_NUMBER VARCHAR,
    CERTIFICATE_NUMBER VARCHAR,
    IMAGE_PATH VARCHAR,
	MEMBER_ID INT NOT NULL,
    FOREIGN KEY(MEMBER_ID) REFERENCES booking.member(MEMBER_ID)
);

-- ROOM
CREATE TABLE booking.room(
    ID SERIAL PRIMARY KEY,
    ROOM_NAME VARCHAR NOT NULL,
    QUANTITY INT,
    CAPACITY INT,
    BED_TYPE VARCHAR,
    INTRODUCTION VARCHAR,
    INSTALLATION VARCHAR,
    ORIGINAL_PRICE INT,
    IAE_PRICE INT,
	HOTEL_ID INT NOT NULL,
    FOREIGN KEY(HOTEL_ID) REFERENCES booking.hotel(ID)
);
-- facilities
CREATE TABLE booking.facilities(
    ID SERIAL PRIMARY KEY,
    FACILITY_NAME VARCHAR
);
CREATE TABLE booking.ROOM_FACILITY(   -- relation between room and facility
    ID SERIAL PRIMARY KEY,
    FACILITY_ID INT NOT NULL,
    ROOM_ID INT NOT NULL,
    FOREIGN KEY(FACILITY_ID) REFERENCES booking.facilities(ID),
    FOREIGN KEY(ROOM_ID) REFERENCES booking.room(ID)
);
-- services
CREATE TABLE booking.services(
    ID SERIAL PRIMARY KEY,
    SERVICES_NAME VARCHAR
);
CREATE TABLE booking.room_service(   -- relation between room and facility
    ID SERIAL PRIMARY KEY,
    SERVICES_ID INT NOT NULL,
    ROOM_ID INT NOT NULL,
    FOREIGN KEY(SERVICES_ID) REFERENCES booking.service(ID),
    FOREIGN KEY(ROOM_ID) REFERENCES booking.room(ID)
);


-- Stars and Comments
CREATE TABLE booking.rating(
    ID SERIAL PRIMARY KEY,
    EVALUATION INT NOT NULL,
    COMMENTS VARCHAR,
	IMAGE_PATH VARCHAR,
    ORDER_ID INT NOT NULL,
    FOREIGN KEY(ORDER_ID) REFERENCES booking.order(id)
);

CREATE TABLE booking.usedcoupon
(
    member_id SERIAL NOT NULL,
    coupon_id integer NOT NULL,
    order_id    integer  NOT NULL,
    Usage_date timestamp without time zone,
    FOREIGN KEY(member_id) REFERENCES booking.member(member_id),
    FOREIGN KEY(coupon_id) REFERENCES booking.coupon(id),
    FOREIGN KEY(order_id) REFERENCES booking.order(id),
    PRIMARY KEY (member_id,coupon_id)
);

CREATE TABLE booking.coupon(
  id SERIAL PRIMARY KEY,
  type SMALLINT,
  member_id int NOT NULL,
  discount varchar,
  end_date TIMESTAMP,
  start_date TIMESTAMP,
  FOREIGN KEY(member_id) REFERENCES booking.member(member_id)
);

CREATE TABLE booking.order(
  id SERIAL PRIMARY KEY,
  fee int,
  member_id int NOT NULL,
  room_id int NOT NULL,
  amount int,
  payment_method SMALLINT,
  end_date TIMESTAMP,
  start_date TIMESTAMP,
  note varchar,
  FOREIGN KEY(member_id) REFERENCES booking.member(member_id),
  FOREIGN KEY(room_id) REFERENCES booking.room(id)
);

INSERT INTO booking.member(
	email, name, password, gender, phone, member_type)
	VALUES ('ben@gmail.com', 'ben','fdsjal', 0, '246546', 0);

INSERT INTO booking."room"(
	room_name, HOTEL_ID)
	VALUES ('dsfa',1);

INSERT INTO booking."order"(
	member_id, room_id)
	VALUES (1,1);
